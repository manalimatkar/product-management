#!/usr/bin/env python3
"""
Fetch a real PR's review comments, with enough context to see what each one
is actually answering -- the mechanical half of resolving a Design
Analysis's open Decisions from a review, per DESIGN-ANALYSIS-REVIEW-SPEC.md
and the pattern this repository already uses (established 2026-09-08:
Decisions get resolved via direct PR review comments, not chat, not a
separate Issue).

This does NOT decide what a comment means or write the resolution into the
Design Analysis -- that stays a judgment call for whoever (or whatever
agent) reads the output, per this repository's standing rule that no
agent may resolve a Decision Required item on its own reasoning. It only
gathers the raw material accurately, which by itself was the fiddly part:
GitHub review comments report their `line` as null once the file has been
revised since the comment was made (the pre-reformat DA-003 is a real
example -- three PRs touched it after these comments landed). The comment
still carries `original_line` and `commit_id`, which together pin exactly
which line of exactly which version of the file the comment was actually
about -- that's what this script resolves, by reading the file as it stood
at that commit, not the file's current content.

Verified directly against this repository's own real history: PR #17's
four inline comments, at original_line 681-684 of DA-003 as it stood at
their commit_id, land exactly on the DEC-001 through DEC-004 table rows,
in order -- confirmed by reading that exact historical version of the file.

Fetches three things:
  - inline (line-anchored) review comments, each with surrounding context
    from the file as it existed at the comment's own commit
  - general PR-level comments (not anchored to any line)
  - each review's own top-level body (a "Changes requested"/"Approved"
    submission can carry its own overall comment, separate from any
    inline ones)

Usage:
  python .github/scripts/fetch_review_comments.py --pr 17
  python .github/scripts/fetch_review_comments.py --pr 17 --context-lines 5
  python .github/scripts/fetch_review_comments.py --pr 17 --repo owner/name
"""
import argparse
import json
import subprocess
import sys


def gh_api(path, args=None):
    cmd = ["gh", "api", path] + (args or [])
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"gh api {path} failed: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    return json.loads(result.stdout)


def current_repo():
    result = subprocess.run(
        ["gh", "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"],
        capture_output=True, text=True, check=True,
    )
    return result.stdout.strip()


_file_cache = {}


def file_at_commit(repo, commit_id, path):
    key = (commit_id, path)
    if key not in _file_cache:
        result = subprocess.run(
            ["git", "show", f"{commit_id}:{path}"],
            capture_output=True, text=True,
        )
        _file_cache[key] = result.stdout.splitlines() if result.returncode == 0 else None
    return _file_cache[key]


def context_around(lines, line_number, context_lines):
    if lines is None or line_number is None:
        return None
    start = max(0, line_number - 1 - context_lines)
    end = min(len(lines), line_number + context_lines)
    return {
        "first_line_number": start + 1,
        "lines": lines[start:end],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pr", required=True, type=int)
    parser.add_argument("--repo", help="owner/name -- defaults to the current repo")
    parser.add_argument(
        "--context-lines", type=int, default=3,
        help="Lines of surrounding context to pull from the file's state at the comment's own commit.",
    )
    args = parser.parse_args()

    repo = args.repo or current_repo()

    inline_raw = gh_api(f"repos/{repo}/pulls/{args.pr}/comments")
    issue_comments_raw = gh_api(f"repos/{repo}/issues/{args.pr}/comments")
    reviews_raw = gh_api(f"repos/{repo}/pulls/{args.pr}/reviews")

    inline = []
    for c in inline_raw:
        line_number = c.get("original_line") or c.get("line")
        lines = file_at_commit(repo, c["commit_id"], c["path"]) if line_number else None
        inline.append({
            "path": c["path"],
            "line": line_number,
            "author": c["user"]["login"],
            "created_at": c["created_at"],
            "body": c["body"],
            "context": context_around(lines, line_number, args.context_lines),
            "html_url": c["html_url"],
        })

    issue_comments = [
        {
            "author": c["user"]["login"],
            "created_at": c["created_at"],
            "body": c["body"],
        }
        for c in issue_comments_raw
    ]

    reviews = [
        {
            "author": r["user"]["login"],
            "state": r["state"],
            "submitted_at": r.get("submitted_at"),
            "body": r["body"],
        }
        for r in reviews_raw
        if r.get("body")
    ]

    result = {
        "pr": args.pr,
        "repo": repo,
        "inline_comments": inline,
        "general_comments": issue_comments,
        "review_bodies": reviews,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
