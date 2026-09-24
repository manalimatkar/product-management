"""Stage this repo's real content into site-src/ for MkDocs to build.

MkDocs refuses to use the repo root as docs_dir (it must be a real child
directory of wherever mkdocs.yml lives), so this script copies the actual
content folders into site-src/ unchanged -- same relative layout, same
filenames -- so every existing internal markdown link keeps resolving
exactly as it does on GitHub. Not a rewrite: source files are canonical,
this staging copy is disposable and gitignored.

Scope, confirmed 2026-09-21, generalized 2026-09-24: this site is for
real product content -- whatever platform this framework has actually
been used to analyze (pdf-workflow/workflow-manager today, not
necessarily the only one ever) -- not for this repository's own agent
framework. specs/, templates/, and the root framework docs (README.md,
CLAUDE.md, PRD.md, IMPLEMENTATION-PLAN.md) describe the Business Agent
and the pipeline that produces this content -- they don't belong in a
site about the product(s) it produced, any more than .claude/ and
.github/ do. A separate site for the framework itself may exist later,
but that's a distinct, not-yet-started effort, not this one. registries/
stays in scope: it's the actual index of every registered product's
Journeys/Capabilities/Business Rules, and the relationship graph depends
on it.

Content dirs are discovered, not hardcoded: every top-level directory
except FRAMEWORK_DIRS below is treated as product content. A hardcoded
list (e.g. naming "pdf-workflow" specifically) would silently exclude
the next real product this framework analyzes -- discovery means a new
platform-slug folder is staged automatically, no code change needed.
FRAMEWORK_DIRS is deliberately named as what to *exclude* (a small,
stable set) rather than what to include (an open-ended, growing set).

Also generates two pages straight into the staged copy, computed at build
time rather than authored, so neither is one of the real content dirs
copied below: the home page (generate_index_page.py) and the Journey/
Capability/Business Rule relationship graph (generate_relationship_graph.py).

Usage: python .github/scripts/build_docs_site.py
"""

import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
STAGING_DIR = REPO_ROOT / "site-src"

# Everything NOT listed here is treated as product content and staged.
# Keep this in sync with .gitignore's own entries plus this repo's fixed
# framework folders -- it should rarely change, unlike the product list.
FRAMEWORK_DIRS = {
    ".git", ".github", ".claude", ".venv",  # tooling / hidden
    "specs", "templates",  # framework docs
    "site", "site-src",  # this script's own build output (gitignored)
}
CONTENT_FILES = []


def discover_content_dirs() -> list[str]:
    return sorted(
        p.name
        for p in REPO_ROOT.iterdir()
        if p.is_dir() and p.name not in FRAMEWORK_DIRS and not p.name.startswith(".")
    )


def main() -> None:
    if STAGING_DIR.exists():
        shutil.rmtree(STAGING_DIR)
    STAGING_DIR.mkdir()

    content_dirs = discover_content_dirs()
    for name in content_dirs:
        src = REPO_ROOT / name
        shutil.copytree(src, STAGING_DIR / name)

    for name in CONTENT_FILES:
        src = REPO_ROOT / name
        if src.is_file():
            shutil.copy2(src, STAGING_DIR / name)

    scripts_dir = Path(__file__).resolve().parent
    for script_name, out_rel in (
        ("generate_index_page.py", "index.md"),
        ("generate_relationship_graph.py", "relationships/index.md"),
    ):
        result = subprocess.run(
            [sys.executable, str(scripts_dir / script_name), "--repo-root", str(REPO_ROOT), "--out", str(STAGING_DIR / out_rel)],
            cwd=REPO_ROOT,
        )
        if result.returncode != 0:
            raise SystemExit(f"build_docs_site.py: {script_name} failed, aborting build.")

    md_count = sum(1 for _ in STAGING_DIR.rglob("*.md"))
    print(f"Staged content dirs: {', '.join(content_dirs)}")
    print(f"Staged {md_count} markdown files into {STAGING_DIR}")


if __name__ == "__main__":
    main()
