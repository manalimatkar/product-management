#!/usr/bin/env python3
"""
Check that every comment on a Design Analysis review PR actually left a
real trace in the document -- the completeness half resolve-review-decisions
needs that verify_design_analysis.py can't provide. That script only checks
a document's own internal structure (unique IDs, resolved links); it has no
way to know whether real PR feedback was fully incorporated. A comment that
never got addressed is a silent gap unless something checks for it.

Two checks, both mechanical, neither a guess at what a comment means:

1. Completeness. Every comment fetch_review_comments.py returns for this
   file (inline anchored to it, plus every general/review comment on the
   PR) should have its own `html_url` permalink cited somewhere in the
   target document -- that's what resolve-review-decisions' step 3 now
   requires when it records a resolution. Any comment whose permalink is
   nowhere in the file is reported. This script cannot judge whether that
   comment was legitimately not-actionable (a side remark, a question
   back) or genuinely missed -- same reason resolve-review-decisions never
   resolves a Decision on its own reasoning. It only makes the gap visible
   so a human can make that call.

2. Attribution sanity check. For every comment that DOES have a citation,
   confirm the ID the citing entry claims to resolve actually appears on
   the comment's own anchored line -- not just anywhere in its surrounding
   context window. This matters because several inline comments can share
   one context block (e.g. four comments on four adjacent rows of the same
   table all see all four rows within +/-3 lines), which would make every
   ID in that block look like a plausible match for every comment in it.
   Tested directly: an early version of this check used the whole context
   window and missed a deliberately introduced wrong attribution (DEC-002
   claimed instead of the comment's real DEC-003) precisely because of
   this. Narrowing to the exact anchored line fixed it. A mismatch is
   flagged as worth double-checking, not a hard failure -- a general
   comment (no line anchor at all) can legitimately resolve something with
   no ID textually nearby (DA-003's own BR-003 narrowing is exactly this
   case), so those fall back to the comment's own body text only.

Usage:
  python .github/scripts/check_review_completeness.py --pr 17 --file pdf-workflow/workflow-manager/analysis/mapping-report/design-analysis-mapping-report-DA-003.md

Exit code 0 if every comment is accounted for; 1 if any are missing
(mismatches alone don't fail the check -- they're worth a look, not proof
of an error).
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ID_RE = re.compile(r"\b(BR|CAP|JRN|BRULE|OBS|GAP|DEC|ASM|TECH)-\d+\b")


def fetch(pr, repo):
    script = Path(__file__).resolve().parent / "fetch_review_comments.py"
    cmd = [sys.executable, str(script), "--pr", str(pr)]
    if repo:
        cmd += ["--repo", repo]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        sys.exit(1)
    return json.loads(result.stdout)


def anchor_line_text(c):
    """The single line the comment is actually attached to, not the whole
    context window -- see module docstring for why this distinction is
    the one that makes the mismatch check actually work."""
    ctx = c.get("context")
    if not ctx or c.get("line") is None:
        return ""
    idx = c["line"] - ctx["first_line_number"]
    if 0 <= idx < len(ctx["lines"]):
        return ctx["lines"][idx]
    return ""


def collect_comments(data, target_file):
    target_posix = Path(target_file).as_posix()
    comments = []
    for c in data["inline_comments"]:
        if c["path"] != target_posix:
            # Normalized to forward slashes on both sides before comparing --
            # GitHub's API always returns posix-style paths, but --file can
            # arrive Windows-style (backslashes) depending on how the caller
            # built the path. An exact-string comparison silently excludes
            # every inline comment, with no error, if the two styles don't
            # match -- found by testing, not assumed: an early version of
            # this script did exactly that on Windows.
            continue  # a comment on a different file in the same PR isn't this document's concern
        comments.append({"kind": "inline", "html_url": c["html_url"], "body": c["body"], "attribution_text": c["body"] + "\n" + anchor_line_text(c)})
    for c in data["general_comments"]:
        comments.append({"kind": "general", "html_url": c["html_url"], "body": c["body"], "attribution_text": c["body"]})
    for r in data["review_bodies"]:
        comments.append({"kind": "review", "html_url": r.get("html_url"), "body": r["body"], "attribution_text": r["body"]})
    return comments


def check(comments, doc_text):
    missing, mismatches = [], []
    for c in comments:
        if c["html_url"] and c["html_url"] in doc_text:
            idx = doc_text.index(c["html_url"])
            window = doc_text[idx: idx + 400]
            claimed_ids = {m.group(0) for m in ID_RE.finditer(window)}
            source_ids = {m.group(0) for m in ID_RE.finditer(c["attribution_text"])}
            if claimed_ids and not (claimed_ids & source_ids):
                mismatches.append((c["html_url"], sorted(claimed_ids), sorted(source_ids)))
        else:
            missing.append(c)
    return missing, mismatches


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pr", required=True, type=int)
    parser.add_argument("--file", required=True, help="Path to the Design Analysis being checked, relative to repo root")
    parser.add_argument("--repo")
    args = parser.parse_args()

    data = fetch(args.pr, args.repo)
    comments = collect_comments(data, args.file)
    doc_text = Path(args.file).read_text(encoding="utf-8")
    missing, mismatches = check(comments, doc_text)

    if missing:
        print(f"UNACCOUNTED-FOR COMMENTS ({len(missing)}) on PR #{args.pr} -- no trace of these in {args.file}:")
        for c in missing:
            preview = " ".join(c["body"].split())[:100]
            print(f"  - [{c['kind']}] {c['html_url']}")
            print(f"    {preview}")
        print("  For each: confirm it was legitimately not-actionable, or was actually missed.")
    else:
        print(f"All {len(comments)} relevant comments on PR #{args.pr} have a citation in {args.file}.")

    if mismatches:
        print(f"\nWORTH DOUBLE-CHECKING ({len(mismatches)}) -- the citing entry's claimed ID doesn't appear in the comment itself or its context:")
        for url, claimed, source in mismatches:
            print(f"  - {url}")
            print(f"    entry claims: {claimed}")
            print(f"    comment/context mentions: {source or '(nothing)'}")

    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
