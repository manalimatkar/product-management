#!/usr/bin/env python3
"""
Generate the docs site's home page (site-src/index.md).

Computed at build time from the registries, the same way
generate_relationship_graph.py is -- counts and links can't go stale
because nothing here is hand-typed.

Usage:
  python .github/scripts/generate_index_page.py --repo-root . --out site-src/index.md
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_registries import REGISTRIES, parse_registry  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    counts = {}
    for registry in REGISTRIES:
        rows, errors = parse_registry(repo_root, registry)
        if errors:
            print("Refusing to generate the index page -- a registry doesn't verify clean:")
            for e in errors:
                print(f"  - {e}")
            sys.exit(1)
        counts[registry["prefix"]] = len(rows or {})

    body = f"""# pdf-workflow / workflow-manager

This site documents one real product -- the Mapping Report screen of `pdf-workflow`'s
`workflow-manager` app -- as analyzed through this repository's Design Analysis process.
It is generated directly from the underlying registries and analysis files; nothing on
this page is hand-maintained.

Currently documented: **{counts["JRN-"]} Journeys**, **{counts["CAP-"]} Capabilities**,
**{counts["BRULE-"]} Business Rules**.

## Start here

- **[Journey → Capability → Business Rule Relationship Graph](relationships/index.md)** --
  the fastest way to see how everything connects, with a hover definition and a click-through
  on every block.
- **[Mapping Report Design Analysis](pdf-workflow/workflow-manager/analysis/mapping-report/design-analysis-mapping-report-DA-003.md)** --
  the full analysis: what the feature does, its requirements, and the evidence behind them.

## Registries

The product-level index of every Journey, Capability, and Business Rule this analysis has
identified -- each row links to its own full record.

- [Journey Registry](registries/JOURNEY-REGISTRY.md)
- [Capability Registry](registries/CAPABILITY-REGISTRY.md)
- [Business Rule Registry](registries/BUSINESS-RULE-REGISTRY.md)
- [Source Registry](registries/SOURCE-REGISTRY.md)
"""
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(body, encoding="utf-8")
    print(f"Wrote index page to {out_path}")


if __name__ == "__main__":
    main()
