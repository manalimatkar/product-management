"""MkDocs build hook: stamps each rendered page with (a) the exact
repo-relative source file path it came from and (b) the correct
relative URL back to comment-map.json at the site root -- both as
data-* attributes on <body>. The in-preview commenting widget reads
these to know which entry in comment-map.json (generate_comment_map.py)
applies to the page currently open, without any path-depth math of its
own client-side (GitHub Pages preview subpaths like /repo/pr-5/... make
that fragile to get right in JS).

Registered via mkdocs.yml's `hooks:` key. Deliberately does this by
string-replacing the rendered HTML (`on_post_page`) rather than a
template override, so it works with the Material theme unmodified --
no forked/copied template to keep in sync with upstream. Reuses
mkdocs.utils.get_relative_url -- the exact function MkDocs itself uses
to compute every other page-relative asset link -- rather than
re-deriving the "how many ../ to reach root" math by hand.
"""

from mkdocs.utils import get_relative_url


def on_post_page(output, page, config, **kwargs):
    src_path = page.file.src_uri  # e.g. "pdf-workflow/.../DA-003.md" -- matches comment-map.json's file keys exactly, since build_docs_site.py stages files unchanged.
    comment_map_url = get_relative_url("comment-map.json", page.url)
    attrs = f'data-source-file="{src_path}" data-comment-map-url="{comment_map_url}"'
    return output.replace("<body", f"<body {attrs}", 1)
