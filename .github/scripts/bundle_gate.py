#!/usr/bin/env python3
"""
Design Handoff Bundle merge gate -- GITHUB-PLATFORM-ADAPTER-SPEC.md section 6.1.

Two modes:
  check  -- pre-merge validation (GATE-002 checklist completeness + Design
            Reviewer approval is checked separately, in the workflow, via
            the GitHub API). Exits non-zero if the checklist isn't complete
            or the bundle file can't be found.
  apply  -- post-merge: computes and writes bundle.md's status/readiness
            fields from its own knownLimitations field.

This is a mechanical pre-check (ROLE-009, FRAMEWORK-CONFIGURATION-SPEC.md
section 10), not a judgment call. It never substitutes for the human
Design Reviewer's actual approval -- it only verifies the approval exists
and the checklist is complete, per that section's "may not substitute its
pass for the accountable reviewer's approval" rule.
"""
import argparse
import json
import re
import sys
from pathlib import Path

import yaml

# 1-2 leading segments (<platform-slug>/[<app-slug>/]) before the design/
# root -- widened 2026-09-08 when ARTIFACT-STORAGE-SPEC.md moved this root out
# from the repository top level to nest under platform/app.
BUNDLE_PATH_RE = re.compile(r"^(?:[^/]+/){1,2}design/.+/v[^/]+/design-handoff-[^/]+\.md$")
CHECKLIST_HEADING_RE = re.compile(r"#+\s*Pre-Registration Checklist", re.IGNORECASE)
UNCHECKED_RE = re.compile(r"^\s*-\s*\[\s*\]", re.MULTILINE)
# Same PR-description sign-off pattern as design_branch_gate.py's
# REVIEWER_SIGNOFF_RE -- added 2026-09-04 after live testing found GitHub
# blocks a PR author from ever approving their own PR (see that script's
# module docstring for the full rationale).
REVIEWER_SIGNOFF_RE = re.compile(
    r"^\s*-\s*\[( |x|X)\]\s*\*\*Design Reviewer sign-off \(ROLE-004\):?\*\*",
    re.MULTILINE,
)


def find_bundle_path(changed_files):
    return [f for f in changed_files if BUNDLE_PATH_RE.match(f)]


def check(args):
    changed_files = json.loads(Path(args.changed_files_json).read_text())
    body = Path(args.pr_body_file).read_text(encoding="utf-8") if args.pr_body_file else ""

    problems = []
    bundle_matches = find_bundle_path(changed_files)

    if len(bundle_matches) == 0:
        problems.append(
            "No design-handoff-*.md bundle file found under design/.../v<version>/ in this PR's "
            "changed files -- this workflow only runs on paths under design/, but the bundle file "
            "itself wasn't found. Confirm the PR actually includes bundle.md."
        )
        bundle_path = None
    elif len(bundle_matches) > 1:
        problems.append(
            f"Found {len(bundle_matches)} bundle.md-shaped files in this PR ({bundle_matches}); "
            "expected exactly one Design Handoff Bundle per PR. Split into separate PRs."
        )
        bundle_path = bundle_matches[0]
    else:
        bundle_path = bundle_matches[0]

    signoff_match = REVIEWER_SIGNOFF_RE.search(body)
    if not signoff_match:
        problems.append(
            "PR description has no 'Design Reviewer sign-off (ROLE-004)' checkbox line. "
            "Paste it into the PR description before merging -- GitHub cannot substitute a "
            "PR review here, since the author and the required reviewer are the same account "
            "until this repository has a separate agent identity."
        )
    elif signoff_match.group(1).lower() != "x":
        problems.append(
            "The 'Design Reviewer sign-off (ROLE-004)' checkbox is present but unchecked. "
            "Check it only once you have actually reviewed and accept this bundle."
        )

    heading_match = CHECKLIST_HEADING_RE.search(body)
    if not heading_match:
        problems.append(
            "PR description has no 'Pre-Registration Checklist' section "
            "(DESIGN-HANDOFF-BUNDLE-TEMPLATE.md Part 4). Paste the checklist into the PR "
            "description and check every box before merging."
        )
    else:
        after = body[heading_match.end():]
        next_heading = re.search(r"\n#{1,6}\s", after)
        section = after[: next_heading.start()] if next_heading else after
        unchecked = UNCHECKED_RE.findall(section)
        if unchecked:
            problems.append(
                f"Pre-Registration Checklist has {len(unchecked)} unchecked item(s) still in the "
                "PR description. GATE-002 requires every item checked before merge."
            )

    result = {"bundle_path": bundle_path, "passed": len(problems) == 0, "problems": problems}
    Path(args.output_json).write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        sys.exit(1)


def apply(args):
    bundle_path = Path(args.bundle_path)
    raw = bundle_path.read_text(encoding="utf-8")

    fm_match = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.DOTALL)
    if not fm_match:
        print(f"::error::{bundle_path} has no parseable YAML frontmatter.")
        sys.exit(1)

    frontmatter = yaml.safe_load(fm_match.group(1)) or {}
    rest = fm_match.group(2)

    known_limitations = frontmatter.get("knownLimitations") or []
    readiness = "Ready" if len(known_limitations) == 0 else "Ready with Limitations"

    frontmatter["status"] = "Approved"
    frontmatter["readiness"] = readiness

    new_frontmatter = yaml.safe_dump(
        frontmatter, sort_keys=False, default_flow_style=False, allow_unicode=True
    )
    bundle_path.write_text(f"---\n{new_frontmatter}---\n{rest}", encoding="utf-8")

    result = {
        "bundle_path": str(bundle_path),
        "status": "Approved",
        "readiness": readiness,
        "known_limitations": known_limitations,
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
    p_check.set_defaults(func=check)

    p_apply = sub.add_parser("apply")
    p_apply.add_argument("--bundle-path", required=True)
    p_apply.add_argument("--output-json", required=True)
    p_apply.set_defaults(func=apply)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
