"""Stage this repo's real content into site-src/ for MkDocs to build.

MkDocs refuses to use the repo root as docs_dir (it must be a real child
directory of wherever mkdocs.yml lives), so this script copies the actual
content folders into site-src/ unchanged -- same relative layout, same
filenames -- so every existing internal markdown link keeps resolving
exactly as it does on GitHub. Not a rewrite: source files are canonical,
this staging copy is disposable and gitignored.

Usage: python .github/scripts/build_docs_site.py
"""

import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
STAGING_DIR = REPO_ROOT / "site-src"

CONTENT_DIRS = ["registries", "specs", "templates", "pdf-workflow"]
CONTENT_FILES = ["README.md", "CLAUDE.md", "PRD.md", "IMPLEMENTATION-PLAN.md"]


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

    md_count = sum(1 for _ in STAGING_DIR.rglob("*.md"))
    print(f"Staged {md_count} markdown files into {STAGING_DIR}")


if __name__ == "__main__":
    main()
