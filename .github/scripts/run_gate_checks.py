#!/usr/bin/env python3
"""
Run the right merge gate(s) against a real PR or a local diff, without
waiting for GitHub Actions to run it in CI first.

This repository has three gate scripts, each triggered on a different path
shape and each requiring inputs (--changed-files-json, --pr-body-file) that
a CI workflow already has lying around but a human or agent checking things
locally does not:

  design_branch_gate.py  -- PRs into the `design` branch, native Claude
                             Design exports (<platform>/[<app>/]design/v<N>/)
  bundle_gate.py          -- PRs into `main`, hand-authored bundles
                             (<platform>/[<app>/]design/<feature-slug>/v<ver>/)
  business_pr_gate.py     -- PRs into `main`, Business PRs
                             (<platform>/[<app>/]business-prs/<feature-slug>/)

This script builds those inputs (from a real PR via `gh`, or from a local
base/head diff), picks whichever gate(s) actually apply by reusing each
gate script's own path-matching function directly (imported, not
reimplemented -- avoids the two copies drifting apart), runs `check` for
each as a real subprocess (matching exactly how the GitHub Actions workflow
invokes them), and prints one consolidated report.

It only ever runs `check` (pre-merge validation). It never runs `apply` --
that mutates files (a cover sheet, a bundle's frontmatter) and is meant to
run once, on an actual merge, not repeatedly while checking things locally.

Usage:
  python .github/scripts/run_gate_checks.py --pr 24
  python .github/scripts/run_gate_checks.py --base main --head my-branch
  python .github/scripts/run_gate_checks.py --base main --head my-branch --pr-body-file body.txt

Exit code 0 if every applicable gate passed (or none applied); 1 if any
applicable gate failed.
"""
import argparse
import contextlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

import bundle_gate  # noqa: E402
import business_pr_gate  # noqa: E402
import design_branch_gate  # noqa: E402


def get_changed_files_and_body(args):
    if args.pr:
        files_raw = subprocess.run(
            ["gh", "pr", "diff", str(args.pr), "--name-only"],
            capture_output=True, text=True, check=True,
        ).stdout
        changed_files = [f for f in files_raw.splitlines() if f.strip()]
        body = subprocess.run(
            ["gh", "pr", "view", str(args.pr), "--json", "body", "-q", ".body"],
            capture_output=True, text=True, check=True,
        ).stdout
        return changed_files, body

    if not args.base or not args.head:
        print("Either --pr, or both --base and --head, are required.")
        sys.exit(2)

    files_raw = subprocess.run(
        ["git", "diff", "--name-only", f"{args.base}...{args.head}"],
        capture_output=True, text=True, check=True,
    ).stdout
    changed_files = [f for f in files_raw.splitlines() if f.strip()]

    if args.pr_body_file:
        body = Path(args.pr_body_file).read_text(encoding="utf-8")
    else:
        body = ""
        print(
            "Note: no --pr-body-file given for a local diff -- sign-off checkbox checks "
            "will correctly report as missing, since there's no PR description to read yet."
        )

    return changed_files, body


def get_head_ref(args):
    """The exact commit whose files the gate scripts must read from disk --
    design_branch_gate.py in particular reads repo_root/version_dir/... as
    real files, not from the diff, so this has to be precise, not just
    'whatever happens to be checked out right now' (a real bug caught while
    testing this script: run from a branch that never had the PR's own
    files, every design_branch_gate check reported them "missing")."""
    if args.pr:
        return subprocess.run(
            ["gh", "pr", "view", str(args.pr), "--json", "headRefOid", "-q", ".headRefOid"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    return args.head


@contextlib.contextmanager
def checkout_at(ref):
    """A real, isolated checkout of `ref` via a temporary git worktree --
    never touches the caller's actual working directory or index, and
    works regardless of which branch is currently checked out there."""
    with tempfile.TemporaryDirectory() as tmp:
        worktree_path = Path(tmp) / "worktree"
        subprocess.run(
            ["git", "worktree", "add", "--detach", str(worktree_path), ref],
            capture_output=True, text=True, check=True,
        )
        try:
            yield worktree_path
        finally:
            subprocess.run(
                ["git", "worktree", "remove", "--force", str(worktree_path)],
                capture_output=True, text=True,
            )


GATES = [
    {
        "name": "design_branch_gate",
        "module": design_branch_gate,
        "matches": lambda files: bool(design_branch_gate.find_version_dirs(files)),
        "extra_args": lambda repo_root: ["--repo-root", repo_root],
    },
    {
        "name": "bundle_gate",
        "module": bundle_gate,
        "matches": lambda files: bool(bundle_gate.find_bundle_path(files)),
        "extra_args": lambda repo_root: [],
    },
    {
        "name": "business_pr_gate",
        "module": business_pr_gate,
        "matches": lambda files: bool(business_pr_gate.find_bpr_path(files)),
        "extra_args": lambda repo_root: [],
    },
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pr", help="A real PR number -- fetches changed files and body via gh.")
    parser.add_argument("--base", help="Base ref for a local diff (used with --head).")
    parser.add_argument("--head", help="Head ref for a local diff (used with --base).")
    parser.add_argument(
        "--pr-body-file",
        help="Path to a text file with the intended PR description, for a local diff "
        "(sign-off checkbox checks need this to mean anything).",
    )
    args = parser.parse_args()

    changed_files, body = get_changed_files_and_body(args)

    if not changed_files:
        print("No changed files found -- nothing to check.")
        sys.exit(0)

    applicable = [g for g in GATES if g["matches"](changed_files)]

    if not applicable:
        print(f"Checked {len(changed_files)} changed file(s): no gate applies to this change.")
        print("(This is a legitimate outcome -- e.g. a framework/docs-only change.)")
        sys.exit(0)

    head_ref = get_head_ref(args)
    overall_passed = True

    with checkout_at(head_ref) as worktree_path, tempfile.TemporaryDirectory() as tmp:
        changed_files_path = Path(tmp) / "changed-files.json"
        changed_files_path.write_text(json.dumps(changed_files))
        pr_body_path = Path(tmp) / "pr-body.txt"
        pr_body_path.write_text(body, encoding="utf-8")

        for gate in applicable:
            output_path = Path(tmp) / f"{gate['name']}-output.json"
            script_path = SCRIPT_DIR / f"{gate['name']}.py"
            cmd = [
                sys.executable, str(script_path), "check",
                "--changed-files-json", str(changed_files_path),
                "--pr-body-file", str(pr_body_path),
                "--output-json", str(output_path),
            ] + gate["extra_args"](str(worktree_path))

            print(f"\n=== {gate['name']} (checked out at {head_ref[:12]}) ===")
            # cwd=worktree_path so bundle_gate.py / business_pr_gate.py -- which
            # resolve their matched file paths relative to cwd, not a --repo-root
            # flag -- read the PR's actual files, not whatever happens to be
            # checked out in the caller's own working directory.
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(worktree_path))
            print(result.stdout.strip())
            if result.returncode != 0:
                overall_passed = False
                if result.stderr.strip():
                    print(result.stderr.strip(), file=sys.stderr)

    print("\n" + ("=" * 40))
    if overall_passed:
        print(f"PASSED -- {len(applicable)} gate(s) applied, all clean.")
    else:
        print(f"FAILED -- at least one of {len(applicable)} applicable gate(s) reported problems above.")
    sys.exit(0 if overall_passed else 1)


if __name__ == "__main__":
    main()
