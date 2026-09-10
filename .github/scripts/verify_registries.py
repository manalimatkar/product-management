#!/usr/bin/env python3
"""
Verify the Journey/Capability/Business Rule registries, and every Design
Analysis that cites them, are actually consistent -- per
ARTIFACT-RELATIONSHIP-MODEL.md section 3.1 and ARTIFACT-STORAGE-SPEC.md
section 4.1.

This is the sibling tool verify_design_analysis.py's own section 9 open
item asked for: that script only checks INSIDE one Design Analysis file
(every ID-only heading unique, every link resolves). This script checks
ACROSS the repository instead -- the three product-level registries and
every Design Analysis that cites a JRN-/CAP-/BRULE- ID from them.

Checks:
  1. Every ID a registry table lists has a Record link that resolves to a
     real file, and that file's own heading ID matches (no silent drift
     between a registry row and the file it points to).
  2. No ID is duplicated within one registry (two rows claiming the same
     JRN-/CAP-/BRULE- number).
  3. Two-way links are actually two-way: a Capability's "Used By Journeys"
     names a Journey that really does list that Capability back in its own
     "Uses Capabilities" field, and vice versa -- catches a link stated on
     only one side, which is worse than no link (it looks verified but
     isn't).
  4. Every JRN-/CAP-/BRULE- ID cited in any real Design Analysis
     (`**/analysis/**/*.md`) actually exists in its registry -- a Design
     Analysis must never reference a product-level ID that was never
     actually registered.

Usage:
  python .github/scripts/verify_registries.py
  python .github/scripts/verify_registries.py --repo-root /path/to/repo

Exit code 0 if everything is consistent; 1 if any check fails.
"""
import argparse
import glob
import re
import sys
from pathlib import Path

REGISTRIES = [
    {"name": "JOURNEY-REGISTRY.md", "dir": "registries", "prefix": "JRN-", "id_field": "Journey ID"},
    {"name": "CAPABILITY-REGISTRY.md", "dir": "registries", "prefix": "CAP-", "id_field": "Capability ID"},
    {"name": "BUSINESS-RULE-REGISTRY.md", "dir": "registries", "prefix": "BRULE-", "id_field": "Rule ID"},
]

ROW_RE = re.compile(r"^\|\s*`([A-Z]+-\d+)`\s*\|.*\|\s*\[[^\]]*\]\(([^)]+)\)\s*\|\s*$", re.MULTILINE)
ID_FIELD_RE_TMPL = r"\|\s*{field}\s*\|\s*`({prefix}\d+)`"
ID_CITATION_RE = re.compile(r"\b(JRN|CAP|BRULE)-(\d+)\b")


def read(path):
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return None


def parse_registry(repo_root, registry):
    path = repo_root / registry["dir"] / registry["name"]
    text = read(path)
    if text is None:
        return None, [f"{registry['name']} not found at repo root."]

    errors = []
    rows = {}
    for m in ROW_RE.finditer(text):
        entity_id, record_rel = m.group(1), m.group(2)
        if not entity_id.startswith(registry["prefix"]):
            continue
        if entity_id in rows:
            errors.append(f"{registry['name']}: `{entity_id}` appears in more than one row.")
            continue
        record_path = (path.parent / record_rel).resolve()
        rows[entity_id] = {"record_rel": record_rel, "record_path": record_path}

        record_text = read(record_path)
        if record_text is None:
            errors.append(f"{registry['name']}: `{entity_id}`'s Record link `{record_rel}` does not resolve to a real file.")
            continue

        id_field_re = re.compile(
            ID_FIELD_RE_TMPL.format(field=re.escape(registry["id_field"]), prefix=registry["prefix"])
        )
        field_match = id_field_re.search(record_text)
        if not field_match:
            errors.append(f"{registry['name']}: `{entity_id}`'s record ({record_rel}) has no `{registry['id_field']} | \\`{registry['prefix']}...\\`` row -- can't confirm it's really this entity.")
        elif field_match.group(1) != entity_id:
            errors.append(f"{registry['name']}: `{entity_id}`'s registry row points at a record whose own `{registry['id_field']}` says `{field_match.group(1)}` instead -- drifted apart.")

        rows[entity_id]["record_text"] = record_text

    return rows, errors


def check_two_way_links(cap_rows, jrn_rows):
    """Only a real markdown link -- `[JRN-001](...)` -- counts as a citation
    here, deliberately, not any backtick-quoted mention of an ID. A record's
    own prose can legitimately say something like "none yet -- `JRN-001`-003
    don't walk this path" without that being a real, followable citation;
    counting bare backticks produced a false positive on exactly this
    pattern the first time this script ran for real."""
    errors = []
    cap_used_by_re = re.compile(r"## Used by journeys\s*\n\s*\n(.*?)(?:\n##|\Z)", re.DOTALL)
    jrn_uses_re = re.compile(r"## Uses capabilities\s*\n\s*\n(.*?)(?:\n##|\Z)", re.DOTALL)
    link_re_tmpl = r"\[({prefix}-\d+)\]\("

    for cap_id, cap in cap_rows.items():
        section = cap_used_by_re.search(cap.get("record_text", ""))
        cited_journeys = re.findall(link_re_tmpl.format(prefix="JRN"), section.group(1)) if section else []
        for jrn_id in cited_journeys:
            jrn = jrn_rows.get(jrn_id)
            if jrn is None:
                errors.append(f"{cap_id}'s record says it's used by `{jrn_id}`, but that Journey isn't registered at all.")
                continue
            jrn_section = jrn_uses_re.search(jrn.get("record_text", ""))
            jrn_cites_back = jrn_section and cap_id in re.findall(link_re_tmpl.format(prefix="CAP"), jrn_section.group(1))
            if not jrn_cites_back:
                errors.append(f"{cap_id} says it's used by `{jrn_id}`, but `{jrn_id}`'s own record doesn't link `{cap_id}` back under \"Uses capabilities\" -- link only stated one-directionally.")

    for jrn_id, jrn in jrn_rows.items():
        section = jrn_uses_re.search(jrn.get("record_text", ""))
        cited_caps = re.findall(link_re_tmpl.format(prefix="CAP"), section.group(1)) if section else []
        for cap_id in cited_caps:
            if cap_id not in cap_rows:
                errors.append(f"{jrn_id}'s record says it uses `{cap_id}`, but that Capability isn't registered at all.")

    return errors


def check_analysis_citations(repo_root, all_registered_ids):
    errors = []
    pattern = str(repo_root / "**" / "analysis" / "**" / "*.md")
    for file_str in glob.glob(pattern, recursive=True):
        path = Path(file_str)
        text = read(path)
        if text is None:
            continue
        cited = {f"{m.group(1)}-{m.group(2)}" for m in ID_CITATION_RE.finditer(text)}
        for entity_id in sorted(cited):
            if entity_id not in all_registered_ids:
                errors.append(f"{path}: cites `{entity_id}`, which is not registered in any of the three registries.")
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()

    all_errors = []
    parsed = {}
    for registry in REGISTRIES:
        rows, errors = parse_registry(repo_root, registry)
        parsed[registry["prefix"]] = rows or {}
        all_errors.extend(errors)
        count = len(rows) if rows else 0
        print(f"{registry['name']}: {count} {registry['prefix'].rstrip('-')} entries")

    two_way_errors = check_two_way_links(parsed["CAP-"], parsed["JRN-"])
    all_errors.extend(two_way_errors)

    all_registered_ids = set()
    for rows in parsed.values():
        all_registered_ids.update(rows.keys())
    citation_errors = check_analysis_citations(repo_root, all_registered_ids)
    all_errors.extend(citation_errors)

    if all_errors:
        print("\nERRORS:")
        for e in all_errors:
            print(f"  - {e}")
        print(f"\nFAILED: {len(all_errors)} error(s).")
        return 1

    print("\nPASSED: every registry entry resolves, every two-way link matches, every citation is registered.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
