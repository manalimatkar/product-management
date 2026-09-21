"""Stage this repo's real content into site-src/ for MkDocs to build.

MkDocs refuses to use the repo root as docs_dir (it must be a real child
directory of wherever mkdocs.yml lives), so this script copies the actual
content folders into site-src/ unchanged -- same relative layout, same
filenames -- so every existing internal markdown link keeps resolving
exactly as it does on GitHub. Not a rewrite: source files are canonical,
this staging copy is disposable and gitignored.

Scope, confirmed 2026-09-21: this site is for one sample project's actual
product content (pdf-workflow/workflow-manager -- its Design Analysis,
Journeys, Capabilities, Business Rules) not for this repository's own
agent framework. specs/, templates/, and the root framework docs
(README.md, CLAUDE.md, PRD.md, IMPLEMENTATION-PLAN.md) describe the
Business Agent and the pipeline that produced this content -- they don't
belong in a site about the sample project, any more than .claude/ and
.github/ do. A separate
site for the framework itself may exist later, but that's a distinct,
not-yet-started effort, not this one. registries/ stays in scope: it's
the actual index of this sample project's Journeys/Capabilities/Business
Rules (100% sample-project data today), and the relationship graph
depends on it.

Also generates the Journey/Capability/Business Rule relationship-graph
page (generate_relationship_graph.py) straight into the staged copy --
that page is computed from the registries at build time, never authored,
so it isn't one of the real content dirs copied below.

Usage: python .github/scripts/build_docs_site.py
"""

import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
STAGING_DIR = REPO_ROOT / "site-src"

CONTENT_DIRS = ["registries", "pdf-workflow"]
CONTENT_FILES = []


def main() -> None:
    if STAGING_DIR.exists():
        shutil.rmtree(STAGING_DIR)
    STAGING_DIR.mkdir()

    for name in CONTENT_DIRS:
        src = REPO_ROOT / name
        if src.is_dir():
            shutil.copytree(src, STAGING_DIR / name)

    for name in CONTENT_FILES:
        src = REPO_ROOT / name
        if src.is_file():
            shutil.copy2(src, STAGING_DIR / name)

    graph_script = Path(__file__).resolve().parent / "generate_relationship_graph.py"
    graph_out = STAGING_DIR / "relationships" / "index.md"
    result = subprocess.run(
        [sys.executable, str(graph_script), "--repo-root", str(REPO_ROOT), "--out", str(graph_out)],
        cwd=REPO_ROOT,
    )
    if result.returncode != 0:
        raise SystemExit("build_docs_site.py: relationship graph generation failed, aborting build.")

    md_count = sum(1 for _ in STAGING_DIR.rglob("*.md"))
    print(f"Staged {md_count} markdown files into {STAGING_DIR}")


if __name__ == "__main__":
    main()
