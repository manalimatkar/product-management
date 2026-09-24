#!/usr/bin/env python3
"""
Compute, for every ID-only heading (BR-006, DEC-002, ...) in every staged
content file, its exact line number in the source markdown file -- the
data the in-preview commenting widget needs to post a real inline GitHub
PR review comment (path + line) for whichever section a reviewer clicks
"Comment" on.

Reuses verify_design_analysis.py's own heading regex and ID pattern
rather than re-deriving them, so the two can't drift apart. Reuses
build_docs_site.py's discover_content_dirs() so the set of files
scanned here always matches the set actually staged into the site --
scanning more would map IDs a reviewer could never actually see a
Comment button for; scanning less would silently break commenting on
whatever was missed.

Usage:
  python .github/scripts/generate_comment_map.py --repo-root . --out site-src/comment-map.json \
      [--commit-sha <sha>] [--pr-number <n>] [--repo <owner/name>]

commit-sha/pr-number/repo are omitted for the main-site build (no PR to
comment on there); the widget checks for their presence and hides itself
entirely when they're absent, rather than trying to comment against a
PR that doesn't exist.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_design_analysis import HEADING_RE, ID_ONLY_RE  # noqa: E402
from build_docs_site import discover_content_dirs  # noqa: E402


def line_map_for_file(path: Path) -> dict:
    """Return {ID: line_number (1-indexed)} for every ID-only heading in path."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    ids = {}
    for i, line in enumerate(lines, start=1):
        m = HEADING_RE.match(line)
        if not m:
            continue
        heading_text = m.group(2).strip()
        if ID_ONLY_RE.match(heading_text):
            ids[heading_text] = i
    return ids


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--out", required=True)
    parser.add_argument("--commit-sha", default=None)
    parser.add_argument("--pr-number", default=None)
    parser.add_argument("--repo", default=None)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()

    files = {}
    for content_dir in discover_content_dirs():
        for md_path in sorted((repo_root / content_dir).rglob("*.md")):
            id_map = line_map_for_file(md_path)
            if not id_map:
                continue
            rel_path = md_path.relative_to(repo_root).as_posix()
            files[rel_path] = id_map

    payload = {
        "repo": args.repo,
        "commit_sha": args.commit_sha,
        "pr_number": int(args.pr_number) if args.pr_number else None,
        "files": files,
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    total_ids = sum(len(v) for v in files.values())
    print(f"Wrote comment map to {out_path}: {len(files)} file(s), {total_ids} ID(s).")


if __name__ == "__main__":
    main()
