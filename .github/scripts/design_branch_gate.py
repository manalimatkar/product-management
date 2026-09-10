#!/usr/bin/env python3
"""
Design branch intake gate -- for native Claude Design exports landing on the
persistent `design` branch (not `main`). See specs/DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md
section 6.2 and specs/GITHUB-PLATFORM-ADAPTER-SPEC.md section 6.1.

Sibling to, not a replacement for, bundle_gate.py -- that script still governs
the hand-authored `bundle.md` path against `main` (a bare Figma link, a
written spec + screenshots -- DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md section 6.1).
This script governs the native, tool-exported path instead: a version folder
of untouched Claude Design output (README.md, optionally PARITY_RULE.md,
designs/*.dc.html, support files, _ds/ tokens) plus one small framework-added
file, _cover-sheet.md.

Two modes, same split as bundle_gate.py:
  check  -- pre-merge validation. Exits non-zero if the version folder isn't
            structurally sound, or the PR description doesn't carry a
            checked Design Reviewer sign-off line. Never touches file
            content beyond reading it.
  apply  -- post-merge: regenerates _cover-sheet.md's machine-written fields
            (screens, knownLimitations, readiness, status) from the native
            files. Never edits README.md, PARITY_RULE.md, or anything under
            designs/ -- those stay byte-identical to what was exported.

This is a mechanical pre-check (ROLE-009, FRAMEWORK-CONFIGURATION-SPEC.md
section 10), not a judgment call -- it never substitutes for the human
Design Reviewer's actual approval, only verifies the drop is structurally
complete enough to read.

**Reviewer sign-off is a PR-description checkbox, not a GitHub PR review.**
Discovered 2026-09-04: GitHub never allows a PR's author to formally
Approve their own PR, on any plan, with no setting to disable it -- and
this repository has no separate agent/bot GitHub identity, so the upload
PR's author and the required Design Reviewer are, today, unavoidably the
same account. A `listReviews`-based check can therefore never pass. The
required signal instead is an explicit, exact checkbox line in the PR
description (DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md section 6.2), the same pattern
bundle_gate.py already uses for the Pre-Registration Checklist -- see
`REVIEWER_SIGNOFF_RE` below for the exact required text.
"""
import argparse
import json
import re
import sys
from pathlib import Path

import yaml

# Matches "<platform>/design/v<N>/..." or "<platform>/<app>/design/v<N>/...",
# i.e. one or two leading segments before the literal "design/v<N>/" anchor --
# DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md section 6.2's folder shape. Deliberately does
# not care what precedes it beyond that, since app is optional.
VERSION_DIR_RE = re.compile(r"^((?:[^/]+/){1,2}design/v\d+)/")

DC_HTML_REF_RE = re.compile(r"`(designs/[^`]+\.dc\.html)`")
LIGHT_SUFFIX_RE = re.compile(r"^(.*) \(Light\)\.dc\.html$")

KNOWN_LIMITATIONS_HEADING_RE = re.compile(
    r"^#{1,6}\s*.*\b(known ux issues|known limitations|open items|open questions)\b",
    re.IGNORECASE | re.MULTILINE,
)
LIST_ITEM_RE = re.compile(r"^\s*(?:[-*]|\d+\.)\s+(.*)$", re.MULTILINE)

# The exact required PR-description line, checked vs. unchecked. Copy this
# verbatim from templates/DESIGN-HANDOFF-BUNDLE-TEMPLATE.md Part 5a --
# matching is deliberately strict (exact phrase, case-insensitive on the
# word "Design Reviewer sign-off" only) so a paraphrase doesn't silently pass.
REVIEWER_SIGNOFF_RE = re.compile(
    r"^\s*-\s*\[( |x|X)\]\s*\*\*Design Reviewer sign-off \(ROLE-004\):?\*\*",
    re.MULTILINE,
)


def find_version_dirs(changed_files):
    dirs = set()
    for f in changed_files:
        m = VERSION_DIR_RE.match(f)
        if m:
            dirs.add(m.group(1))
    return sorted(dirs)


def check(args):
    changed_files = json.loads(Path(args.changed_files_json).read_text())
    repo_root = Path(args.repo_root)
    pr_body = Path(args.pr_body_file).read_text(encoding="utf-8") if args.pr_body_file else ""

    problems = []

    signoff_match = REVIEWER_SIGNOFF_RE.search(pr_body)
    if not signoff_match:
        problems.append(
            "PR description has no 'Design Reviewer sign-off (ROLE-004)' checkbox line "
            "(DESIGN-HANDOFF-BUNDLE-TEMPLATE.md Part 5a). Paste it into the PR description "
            "before merging -- GitHub cannot substitute a PR review here, since the author "
            "and the required reviewer are the same account until this repository has a "
            "separate agent identity (see this script's module docstring)."
        )
    elif signoff_match.group(1).lower() != "x":
        problems.append(
            "The 'Design Reviewer sign-off (ROLE-004)' checkbox is present but unchecked. "
            "Check it only once you have actually reviewed and accept this drop."
        )

    version_dirs = find_version_dirs(changed_files)

    if len(version_dirs) == 0:
        problems.append(
            "No <platform>/[<app>/]design/v<N>/ version folder found in this PR's changed "
            "files. This workflow only runs on PRs into the design branch touching that shape."
        )
        Path(args.output_json).write_text(
            json.dumps({"version_dir": None, "passed": False, "problems": problems}, indent=2)
        )
        sys.exit(1)
    elif len(version_dirs) > 1:
        problems.append(
            f"Found {len(version_dirs)} distinct version folders in this PR ({version_dirs}); "
            "expected exactly one per PR. Split into separate PRs."
        )

    version_dir = version_dirs[0]
    vdir_path = repo_root / version_dir

    readme_path = vdir_path / "README.md"
    readme_text = ""
    if not readme_path.is_file():
        problems.append(f"{version_dir}/README.md is missing.")
    else:
        readme_text = readme_path.read_text(encoding="utf-8")
        if len(readme_text.encode("utf-8")) <= 500:
            problems.append(
                f"{version_dir}/README.md is too small (<=500 bytes) to be a real Claude "
                "Design handoff document."
            )
        if not re.search(r"^#{2,6}\s+\S", readme_text, re.MULTILINE):
            problems.append(f"{version_dir}/README.md has no '##'-level heading.")

    designs_dir = vdir_path / "designs"
    dc_html_files = sorted(p.name for p in designs_dir.glob("*.dc.html")) if designs_dir.is_dir() else []
    if not dc_html_files:
        problems.append(f"No designs/*.dc.html files found under {version_dir}.")

    # Rule 4: every .dc.html path referenced in README.md resolves to a real file.
    # One-directional deliberately -- see DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md section 6.2.
    for ref in DC_HTML_REF_RE.findall(readme_text):
        if not (vdir_path / ref).is_file():
            problems.append(f"README.md references `{ref}`, but that file doesn't exist.")

    # Rule 5: PARITY_RULE.md present -> every Light/dark pair is complete.
    if (vdir_path / "PARITY_RULE.md").is_file():
        dark_names = {f for f in dc_html_files if not f.endswith(" (Light).dc.html")}
        light_names = {f for f in dc_html_files if f.endswith(" (Light).dc.html")}
        for dark in dark_names:
            base = dark[: -len(".dc.html")]
            expected_light = f"{base} (Light).dc.html"
            if expected_light not in light_names:
                problems.append(
                    f"PARITY_RULE.md is present but {version_dir}/designs/{expected_light} "
                    f"is missing (dark counterpart {dark} exists)."
                )
        for light in light_names:
            m = LIGHT_SUFFIX_RE.match(light)
            expected_dark = f"{m.group(1)}.dc.html"
            if expected_dark not in dark_names:
                problems.append(
                    f"PARITY_RULE.md is present but {version_dir}/designs/{expected_dark} "
                    f"is missing (light counterpart {light} exists)."
                )

    result = {"version_dir": version_dir, "passed": len(problems) == 0, "problems": problems}
    Path(args.output_json).write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        sys.exit(1)


def scrape_known_limitations(readme_text):
    heading_match = KNOWN_LIMITATIONS_HEADING_RE.search(readme_text)
    if not heading_match:
        return []
    after = readme_text[heading_match.end():]
    next_heading = re.search(r"\n#{1,6}\s", after)
    section = after[: next_heading.start()] if next_heading else after
    return [item.strip() for item in LIST_ITEM_RE.findall(section) if item.strip()]


def apply(args):
    repo_root = Path(args.repo_root)
    vdir_path = repo_root / args.version_dir

    readme_text = (vdir_path / "README.md").read_text(encoding="utf-8")
    designs_dir = vdir_path / "designs"
    screens = sorted(p.name for p in designs_dir.glob("*.dc.html")) if designs_dir.is_dir() else []
    known_limitations = scrape_known_limitations(readme_text)
    readiness = "Ready" if len(known_limitations) == 0 else "Ready with Limitations"

    cover_sheet_path = vdir_path / "_cover-sheet.md"
    raw = cover_sheet_path.read_text(encoding="utf-8")
    fm_match = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.DOTALL)
    if not fm_match:
        print(f"::error::{cover_sheet_path} has no parseable YAML frontmatter.")
        sys.exit(1)

    frontmatter = yaml.safe_load(fm_match.group(1)) or {}
    rest = fm_match.group(2)

    frontmatter["status"] = "Received"
    frontmatter["readiness"] = readiness
    frontmatter["knownLimitations"] = known_limitations
    frontmatter["screens"] = screens

    new_frontmatter = yaml.safe_dump(
        frontmatter, sort_keys=False, default_flow_style=False, allow_unicode=True
    )
    cover_sheet_path.write_text(f"---\n{new_frontmatter}---\n{rest}", encoding="utf-8")

    result = {
        "version_dir": args.version_dir,
        "status": "Received",
        "readiness": readiness,
        "known_limitations": known_limitations,
        "screens": screens,
    }
    Path(args.output_json).write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="mode", required=True)

    p_check = sub.add_parser("check")
    p_check.add_argument("--changed-files-json", required=True)
    p_check.add_argument("--pr-body-file", required=True)
    p_check.add_argument("--output-json", required=True)
    p_check.add_argument("--repo-root", default=".")
    p_check.set_defaults(func=check)

    p_apply = sub.add_parser("apply")
    p_apply.add_argument("--version-dir", required=True)
    p_apply.add_argument("--output-json", required=True)
    p_apply.add_argument("--repo-root", default=".")
    p_apply.set_defaults(func=apply)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
