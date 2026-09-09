#!/usr/bin/env python3
"""Verify a Design Analysis artifact's internal traceability, per
templates/DESIGN-ANALYSIS-TEMPLATE.md's format (narrative-first, ID-only
headings, real markdown links -- no HTML, no numbered sections).

This formalizes the ad hoc check written twice by hand during the DA-003
reformat (2026-09-08): once before a merge-conflict resolution, once after,
to prove no ID or cross-link was silently dropped. It is meant to be run
after drafting or revising ANY Design Analysis, before opening or updating
its review PR -- see .claude/skills/verify-design-analysis/SKILL.md.

Checks:
  1. Every ID-only heading (`##### BR-003`, never a title in the heading
     itself) is unique -- no ID defined twice.
  2. Every `[text](#anchor)` link resolves to a real heading, using the
     same slug algorithm GitHub applies (lowercase, strip punctuation,
     spaces -> hyphens).
  3. Every linkable evidence entry (OBS-/GAP-/DEC-/ASM-/TECH-/BRULE-/CAP-)
     has at least one inbound link from elsewhere in the document -- an
     entry nothing points to is either orphaned or its citation was lost.
  4. A summary count per ID prefix, so a reviewer can eyeball totals
     against what the analysis narrative claims (e.g. "16 requirements").

Usage:
  python .github/scripts/verify_design_analysis.py <path-to-DA-file.md>

Exit code 0 if no errors (warnings are printed but do not fail the check);
exit code 1 if any heading is duplicated, any link is broken, or the file
cannot be read.
"""

import re
import sys

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
LINK_RE = re.compile(r"\]\(#([a-z0-9-]+)\)")
ID_ONLY_RE = re.compile(r"^[A-Z]+-\d+$")
LINKABLE_PREFIXES = ("OBS-", "GAP-", "DEC-", "ASM-", "TECH-", "BRULE-", "CAP-", "BR-")


def slugify(heading_text):
    """Reproduce GitHub's heading-to-anchor slug algorithm closely enough
    for this repository's ID-only headings (no inline formatting/code
    spans to strip beyond what these headings actually contain)."""
    s = heading_text.lower()
    s = re.sub(r"[^a-z0-9 -]", "", s)
    s = s.strip()
    s = re.sub(r"\s+", "-", s)
    return s


def main():
    if len(sys.argv) != 2:
        print("Usage: python verify_design_analysis.py <path-to-DA-file.md>")
        return 1

    path = sys.argv[1]
    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        print(f"ERROR: could not read {path}: {e}")
        return 1

    errors = []
    warnings = []

    headings = HEADING_RE.findall(text)
    anchor_owner = {}  # slug -> heading text that first claimed it
    id_heading_count = {}  # exact ID string -> count

    for _hashes, heading_text in headings:
        slug = slugify(heading_text)
        if slug in anchor_owner and anchor_owner[slug] != heading_text:
            errors.append(
                f"Duplicate anchor #{slug}: both \"{anchor_owner[slug]}\" "
                f"and \"{heading_text}\" resolve to it."
            )
        anchor_owner.setdefault(slug, heading_text)

        if ID_ONLY_RE.match(heading_text):
            id_heading_count[heading_text] = id_heading_count.get(heading_text, 0) + 1

    for id_str, count in id_heading_count.items():
        if count > 1:
            errors.append(f"ID heading {id_str} appears {count} times -- must be unique.")

    links = LINK_RE.findall(text)
    inbound_count = {}
    for slug in links:
        inbound_count[slug] = inbound_count.get(slug, 0) + 1
        if slug not in anchor_owner:
            errors.append(f"Link to #{slug} does not resolve to any heading in this file.")

    for id_str in id_heading_count:
        if not any(id_str.startswith(p) for p in LINKABLE_PREFIXES):
            continue
        slug = slugify(id_str)
        # An entry always contains its own heading; a real "used by" or
        # "Evidence:" citation means something ELSE in the document also
        # links to it. We can't easily tell self-links from real ones
        # without tracking source position, so this is a soft check: zero
        # inbound links at all (including from its own future "used by"
        # line, which points the other way) is worth flagging.
        if slug not in inbound_count:
            warnings.append(
                f"{id_str} (#{slug}) has no inbound links from anywhere else in the "
                f"document -- check it isn't orphaned (cited by nothing, or its own "
                f"\"used by\" back-link is missing)."
            )

    prefix_counts = {}
    for id_str in id_heading_count:
        prefix = id_str.rsplit("-", 1)[0] + "-"
        prefix_counts[prefix] = prefix_counts.get(prefix, 0) + 1

    print(f"Checked: {path}")
    print(f"Headings: {len(headings)}   Links: {len(links)}")
    print("ID counts by prefix:")
    for prefix in sorted(prefix_counts):
        print(f"  {prefix:<8} {prefix_counts[prefix]}")

    if warnings:
        print("\nWarnings (review, does not fail the check):")
        for w in warnings:
            print(f"  - {w}")

    if errors:
        print("\nERRORS:")
        for e in errors:
            print(f"  - {e}")
        print(f"\nFAILED: {len(errors)} error(s).")
        return 1

    print("\nPASSED: every ID unique, every link resolves.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
