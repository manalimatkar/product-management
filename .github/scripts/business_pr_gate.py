#!/usr/bin/env python3
"""
Business PR merge gate -- GITHUB-PLATFORM-ADAPTER-SPEC.md section 6.

Two modes:
  check  -- pre-merge validation. The Business PR file must exist and its
            Required Stage Trace (BUSINESS-PR-SPEC.md section 6) must have
            at least one completed (non-placeholder) row, and the PR
            description must carry a checked Business Owner sign-off
            checkbox (see BUSINESS_OWNER_SIGNOFF_RE below). A small
            technical-detail keyword scan is reported as a WARNING only,
            never a hard fail -- FRAMEWORK-CONFIGURATION-SPEC.md section 10
            is explicit that ROLE-009 runs *mechanical* checks, not
            judgment calls, and a keyword scan is not reliable enough to
            stand in for the actual judgment BUSINESS-PR-SPEC.md section 9
            requires.
  apply  -- post-merge: parses the Epic/Story blocks so the workflow can
            create one GitHub Issue per Epic and Story.

Business PR identity itself is established by *where* this workflow is
triggered (paths: business-prs/**, per GITHUB-PLATFORM-ADAPTER-SPEC.md
section 4's mapping table) -- no separate label is defined for the PR
itself in that table, so none is invented here.

**Business Owner sign-off is a PR-description checkbox, not a GitHub PR
review.** Same finding as design_branch_gate.py, discovered 2026-09-04:
GitHub never lets a PR's author formally Approve their own PR, and this
repository has no separate agent/bot identity, so a `listReviews`-based
check can never pass whenever the same account both opens the Business PR
and is the accountable Business Owner. See GITHUB-PLATFORM-ADAPTER-SPEC.md
section 8 and DESIGN-HANDOFF-BUNDLE-SPEC.md section 6.2 for the fuller
rationale; this script applies the identical fix.
"""
import argparse
import json
import re
import sys
from pathlib import Path

BPR_PATH_RE = re.compile(r"^business-prs/.+/business-pr-[^/]+\.md$")
# Exact required PR-description line, checked vs. unchecked -- same pattern
# and same rationale as design_branch_gate.py's REVIEWER_SIGNOFF_RE.
BUSINESS_OWNER_SIGNOFF_RE = re.compile(
    r"^\s*-\s*\[( |x|X)\]\s*\*\*Business Owner sign-off \(ROLE-001\):?\*\*",
    re.MULTILINE,
)
STAGE_TRACE_HEADING_RE = re.compile(r"^##\s*\d+\.\s*Required Stage Trace\s*$", re.MULTILINE)
EPIC_HEADING_RE = re.compile(r"^##\s*\d+\.\s*Epic:\s*`([^`]+)`\s*--\s*(.+?)\s*$", re.MULTILINE)
STORY_HEADING_RE = re.compile(r"^###\s*Story\s*`([^`]+)`:\s*(.+?)\s*$", re.MULTILINE)
# Any top-level "## " heading (Business Rules, Dependencies, Required Stage
# Trace, ...) OR a "### Story" heading bounds a Story's body. Without the
# top-level-heading half of this, the LAST Story in an Epic would swallow
# every section after it (Stage Trace through Business Owner Decision),
# since nothing else stops it before the next Epic (or end of file).
BOUNDARY_RE = re.compile(r"^(##\s.*|###\s*Story\s*`[^`]+`:.*)$", re.MULTILINE)

# Heuristic only -- see module docstring. Not exhaustive, not authoritative.
TECH_KEYWORDS = [
    "react", "angular", "vue.js", "endpoint", "rest api", "graphql", "sql",
    "database schema", "microservice", "kubernetes", "docker", "npm package",
    "backend service", "frontend framework", "json schema", "http method",
    "postgres", "mongodb", "redis", "typescript", "javascript framework",
]


def find_bpr_path(changed_files):
    return [f for f in changed_files if BPR_PATH_RE.match(f)]


def stage_trace_completed_rows(content):
    heading = STAGE_TRACE_HEADING_RE.search(content)
    if not heading:
        return 0
    after = content[heading.end():]
    next_heading = re.search(r"\n#{1,6}\s", after)
    section = after[: next_heading.start()] if next_heading else after
    rows = [
        line for line in section.splitlines()
        if line.strip().startswith("|") and not line.strip().startswith("| ---")
    ]
    data_rows = rows[1:] if rows else []  # drop header row
    real_rows = [r for r in data_rows if "<" not in r]
    return len(real_rows)


def check(args):
    changed_files = json.loads(Path(args.changed_files_json).read_text())
    pr_body = Path(args.pr_body_file).read_text(encoding="utf-8") if args.pr_body_file else ""
    bpr_matches = find_bpr_path(changed_files)

    problems = []
    warnings = []
    bpr_path = None

    signoff_match = BUSINESS_OWNER_SIGNOFF_RE.search(pr_body)
    if not signoff_match:
        problems.append(
            "PR description has no 'Business Owner sign-off (ROLE-001)' checkbox line "
            "(BUSINESS-PR-TEMPLATE.md). Paste it into the PR description before merging -- "
            "GitHub cannot substitute a PR review here, since the author and the required "
            "reviewer are the same account until this repository has a separate agent identity."
        )
    elif signoff_match.group(1).lower() != "x":
        problems.append(
            "The 'Business Owner sign-off (ROLE-001)' checkbox is present but unchecked. "
            "Check it only once you have actually reviewed and accept this Business PR."
        )

    if len(bpr_matches) == 0:
        problems.append("No business-pr-*.md file found under business-prs/.../ in this PR.")
    elif len(bpr_matches) > 1:
        problems.append(f"Found {len(bpr_matches)} Business PR files in one PR; expected exactly one.")
        bpr_path = bpr_matches[0]
    else:
        bpr_path = bpr_matches[0]

    content = Path(bpr_path).read_text(encoding="utf-8") if bpr_path else ""

    if bpr_path:
        completed_rows = stage_trace_completed_rows(content)
        if completed_rows == 0:
            problems.append(
                "Required Stage Trace (BUSINESS-PR-SPEC.md section 6) has no completed rows -- "
                "still only the template placeholder, or the section is missing entirely."
            )

        lowered = content.lower()
        hit_keywords = sorted({kw for kw in TECH_KEYWORDS if kw in lowered})
        if hit_keywords:
            warnings.append(
                "Heuristic technical-detail scan flagged possible leaked implementation terms: "
                + ", ".join(hit_keywords)
                + ". Keyword scan only, not a judgment call -- review manually."
            )

    result = {"bpr_path": bpr_path, "passed": len(problems) == 0, "problems": problems, "warnings": warnings}
    Path(args.output_json).write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        sys.exit(1)


def apply(args):
    bpr_path = Path(args.bpr_path)
    content = bpr_path.read_text(encoding="utf-8")

    epics = []
    epic_matches = list(EPIC_HEADING_RE.finditer(content))
    for i, m in enumerate(epic_matches):
        epic_id, epic_name = m.group(1), m.group(2)
        start = m.end()
        end = epic_matches[i + 1].start() if i + 1 < len(epic_matches) else len(content)
        epic_body_full = content[start:end]

        boundaries = list(BOUNDARY_RE.finditer(epic_body_full))
        story_boundaries = [b for b in boundaries if b.group(0).lstrip().startswith("###")]

        stories = []
        for sm in story_boundaries:
            story_id_m = re.match(r"###\s*Story\s*`([^`]+)`:\s*(.+?)\s*$", sm.group(0).strip())
            story_id, story_title = story_id_m.group(1), story_id_m.group(2)
            s_start = sm.end()
            later = [b.start() for b in boundaries if b.start() > sm.start()]
            s_end = min(later) if later else len(epic_body_full)
            stories.append({
                "id": story_id,
                "title": story_title,
                "body": epic_body_full[s_start:s_end].strip(),
            })

        epic_body = (
            epic_body_full[: boundaries[0].start()].strip() if boundaries else epic_body_full.strip()
        )
        epics.append({"id": epic_id, "name": epic_name, "body": epic_body, "stories": stories})

    result = {"bpr_path": str(bpr_path), "epics": epics}
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
    p_apply.add_argument("--bpr-path", required=True)
    p_apply.add_argument("--output-json", required=True)
    p_apply.set_defaults(func=apply)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
