#!/usr/bin/env python3
"""
Generate the Journey -> Capability -> Business Rule relationship-graph
page for the docs site.

Computed directly from the three registries at build time -- never hand-
authored, so it can't drift from what verify_registries.py already treats
as ground truth. Reuses parse_registry() and the section regexes from
verify_registries.py rather than re-parsing the registries a second way;
only draws an edge from a relationship that script's own two-way checks
have verified is stated on both sides.

Usage:
  python .github/scripts/generate_relationship_graph.py --repo-root . --out site-src/relationships/index.md

Exit code 0 on success; 1 if the registries themselves don't verify clean
(this script refuses to graph unverified data).
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_registries import (  # noqa: E402
    REGISTRIES,
    CAP_GOVERNED_BY_RE,
    JRN_USES_CAPABILITIES_RE,
    LINK_RE_TMPL,
    check_capability_rule_links,
    check_two_way_links,
    parse_registry,
)

NAME_RE = re.compile(r"^#\s+(?:Journey|Capability|Business Rule):\s*(.+?)\s*$", re.MULTILINE)


def record_name(rows, entity_id, fallback=None):
    text = rows.get(entity_id, {}).get("record_text", "")
    m = NAME_RE.search(text)
    return m.group(1) if m else (fallback or entity_id)


def mermaid_id(entity_id):
    return entity_id.replace("-", "_")


def cited(record_text, section_re, prefix):
    section = section_re.search(record_text or "")
    return re.findall(LINK_RE_TMPL.format(prefix=prefix), section.group(1)) if section else []


def build(repo_root):
    parsed = {}
    for registry in REGISTRIES:
        rows, errors = parse_registry(repo_root, registry)
        if errors:
            return None, errors
        parsed[registry["prefix"]] = rows or {}

    jrn_rows, cap_rows, brule_rows = parsed["JRN-"], parsed["CAP-"], parsed["BRULE-"]

    verify_errors = check_two_way_links(cap_rows, jrn_rows) + check_capability_rule_links(cap_rows, brule_rows)
    if verify_errors:
        return None, verify_errors

    jrn_to_caps = {jrn_id: cited(jrn.get("record_text"), JRN_USES_CAPABILITIES_RE, "CAP") for jrn_id, jrn in jrn_rows.items()}
    cap_to_rules = {cap_id: cited(cap.get("record_text"), CAP_GOVERNED_BY_RE, "BRULE") for cap_id, cap in cap_rows.items()}

    caps_with_journey = {cap_id for caps in jrn_to_caps.values() for cap_id in caps}
    caps_with_rule = {cap_id for cap_id, rules in cap_to_rules.items() if rules}
    rules_with_cap = {r for rules in cap_to_rules.values() for r in rules}

    # Path of each record relative to repo_root, so links work regardless of
    # which platform/app subtree a Capability or Business Rule lives under --
    # never hardcode "pdf-workflow/workflow-manager/..." here.
    site_rel = {}
    for rows in (cap_rows, brule_rows):
        for entity_id, row in rows.items():
            site_rel[entity_id] = row["record_path"].relative_to(repo_root).as_posix()

    return {
        "jrn_rows": jrn_rows, "cap_rows": cap_rows, "brule_rows": brule_rows,
        "jrn_to_caps": jrn_to_caps, "cap_to_rules": cap_to_rules,
        "orphan_caps": sorted(set(cap_rows) - caps_with_journey),
        "orphan_rules": sorted(set(brule_rows) - rules_with_cap),
        "caps_with_rule": caps_with_rule,
        "site_rel": site_rel,
    }, []


def render_mermaid(data):
    lines = ["```mermaid", "flowchart LR"]
    for jrn_id in sorted(data["jrn_rows"]):
        name = record_name(data["jrn_rows"], jrn_id)
        lines.append(f'    {mermaid_id(jrn_id)}["{jrn_id}<br/>{name}"]')
    for cap_id in sorted(data["cap_rows"]):
        name = record_name(data["cap_rows"], cap_id)
        lines.append(f'    {mermaid_id(cap_id)}("{cap_id}<br/>{name}")')
    for brule_id in sorted(data["brule_rows"]):
        name = record_name(data["brule_rows"], brule_id)
        lines.append(f'    {mermaid_id(brule_id)}{{{{"{brule_id}<br/>{name}"}}}}')

    for jrn_id, caps in sorted(data["jrn_to_caps"].items()):
        for cap_id in caps:
            lines.append(f"    {mermaid_id(jrn_id)} --> {mermaid_id(cap_id)}")
    for cap_id, rules in sorted(data["cap_to_rules"].items()):
        for brule_id in rules:
            lines.append(f"    {mermaid_id(cap_id)} -.governed by.-> {mermaid_id(brule_id)}")

    lines.append("```")
    return "\n".join(lines)


def render_page(data):
    parts = []
    parts.append("# Journey → Capability → Business Rule Relationship Graph")
    parts.append(
        "Generated at build time from [JOURNEY-REGISTRY.md](../registries/JOURNEY-REGISTRY.md), "
        "[CAPABILITY-REGISTRY.md](../registries/CAPABILITY-REGISTRY.md), and "
        "[BUSINESS-RULE-REGISTRY.md](../registries/BUSINESS-RULE-REGISTRY.md) -- not hand-authored, "
        "so it can't drift from those registries. Only draws an edge where "
        "`verify_registries.py` has confirmed the relationship is stated on both "
        "sides, not just one. Solid arrows: a Journey uses a Capability. Dashed "
        "arrows: a Business Rule governs a Capability -- a constraint, not a step "
        "in the flow, per "
        "[ARTIFACT-RELATIONSHIP-MODEL.md](../specs/ARTIFACT-RELATIONSHIP-MODEL.md) section 3.1."
    )
    parts.append(render_mermaid(data))

    site_rel = data["site_rel"]
    parts.append("## Journeys")
    for jrn_id in sorted(data["jrn_rows"]):
        name = record_name(data["jrn_rows"], jrn_id)
        caps = data["jrn_to_caps"].get(jrn_id, [])
        cap_links = ", ".join(f"[{c}](../{site_rel[c]})" for c in caps) if caps else "*(none)*"
        parts.append(f"- **{jrn_id}** -- {name}. Uses: {cap_links}")

    parts.append("## Capabilities")
    for cap_id in sorted(data["cap_rows"]):
        name = record_name(data["cap_rows"], cap_id)
        rules = data["cap_to_rules"].get(cap_id, [])
        rule_links = ", ".join(f"[{r}](../{site_rel[r]})" for r in rules) if rules else "*(none)*"
        parts.append(f"- **{cap_id}** -- {name}. Governed by: {rule_links}")

    if data["orphan_caps"]:
        parts.append("## Capabilities with no Journey yet")
        parts.append(
            "A real, honest gap, not smoothed over -- see each Capability's own "
            "record and `CAPABILITY-REGISTRY.md`'s note on it."
        )
        for cap_id in data["orphan_caps"]:
            parts.append(f"- **{cap_id}** -- {record_name(data['cap_rows'], cap_id)}")

    if data["orphan_rules"]:
        parts.append("## Business Rules with no single Capability")
        parts.append("Scope-defining rules, or rules governing the screen as a whole rather than one Capability.")
        for brule_id in data["orphan_rules"]:
            parts.append(f"- **{brule_id}** -- {record_name(data['brule_rows'], brule_id)}")

    return "\n\n".join(parts) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    data, errors = build(repo_root)
    if errors:
        print("Refusing to generate the relationship graph -- the registries don't verify clean:")
        for e in errors:
            print(f"  - {e}")
        return 1

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render_page(data), encoding="utf-8")
    print(f"Wrote relationship graph to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
