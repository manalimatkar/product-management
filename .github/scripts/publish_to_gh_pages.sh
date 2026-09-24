#!/bin/bash
# Publish a built docs site (a directory of static files) into a subdirectory
# of the gh-pages branch, without disturbing anything else already there --
# the main site's own root content, or any other PR's preview subfolder.
#
# Why this exists instead of the modern actions/deploy-pages flow: that flow
# replaces the entire published site on every run, which is fine for a single
# deployment but cannot support multiple simultaneous PR previews coexisting
# alongside the main site. The classic "deploy from a branch" model can,
# because it's just files committed to a real git branch -- each deploy only
# touches its own subdirectory.
#
# Verified against a real, isolated scratch git remote before being trusted
# here (not just reasoned about): first-ever deploy creating the branch from
# nothing, two previews coexisting, a main-site update surviving alongside
# both previews, a preview rebuild, and cleanup removing one preview while
# the other and the main site survive. Two real bugs were found and fixed
# during that testing, not assumed away:
#   1. The cleanup step that clears a destination directory before copying
#      in a fresh build, applied naively to the root destination ("."),
#      deleted .git itself -- .git is just another top-level entry from
#      find's perspective. Fixed by excluding it explicitly.
#   2. The same cleanup, once .git was excluded, still deleted every open
#      PR's preview subfolder on a root (main-site) deploy, because those
#      subfolders are also top-level siblings of the root destination.
#      Fixed by also excluding anything matching `pr-*`.
#
# Usage:
#   publish_to_gh_pages.sh <build_dir> <dest_subdir> <commit_message>
#
# <dest_subdir> is "." for the main site, or "pr-<number>" for a preview.
#
# Auth note, found by actually running this in CI, not assumed: actions/
# checkout wires GITHUB_TOKEN into git as an http.extraheader, scoped to the
# .git directory it checked out -- it does NOT transfer to a fresh `git
# clone`/`git init` into a separate temp directory, which is exactly what
# this script does for its own worktree. Real symptom hit on the first live
# run: "fatal: could not read Username for 'https://github.com'". Fixed by
# building an explicitly authenticated URL from GITHUB_TOKEN + GITHUB_REPOSITORY
# (both already set by the Actions runner; only GITHUB_TOKEN needs to be
# passed into the step's `env:` explicitly) rather than trusting ambient
# credential state. Falls back to the plain `origin` URL when those aren't
# set, so this script still runs unmodified against a real scratch remote
# for local testing.
#
# Requires GIT_AUTHOR/COMMITTER identity to already be configured by the
# caller (the workflow sets this to github-actions[bot], not a real person,
# since these are machine-generated publish commits, not authored content).

set -euo pipefail

build_dir="$1"
dest_dir="$2"
commit_msg="$3"

if [ ! -d "$build_dir" ]; then
  echo "publish_to_gh_pages.sh: build_dir '$build_dir' does not exist" >&2
  exit 1
fi

if [ -n "${GITHUB_TOKEN:-}" ] && [ -n "${GITHUB_REPOSITORY:-}" ]; then
  remote_url="https://x-access-token:${GITHUB_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"
else
  remote_url=$(git remote get-url origin)
fi
max_attempts=5

for attempt in $(seq 1 "$max_attempts"); do
  tmp=$(mktemp -d)
  worktree="$tmp/gh-pages"

  if git ls-remote --exit-code --heads origin gh-pages > /dev/null 2>&1; then
    git clone -q --branch gh-pages --single-branch "$remote_url" "$worktree"
  else
    mkdir -p "$worktree"
    git -C "$worktree" init -q
    git -C "$worktree" checkout --orphan gh-pages -q
    git -C "$worktree" remote add origin "$remote_url"
  fi
  git -C "$worktree" config user.name "github-actions[bot]"
  git -C "$worktree" config user.email "41898282+github-actions[bot]@users.noreply.github.com"

  mkdir -p "$worktree/$dest_dir"
  # Clear only the destination's own prior content -- never .git, and never a
  # sibling pr-*/ preview folder, even when the destination is root itself.
  find "$worktree/$dest_dir" -mindepth 1 -maxdepth 1 ! -name '.git' ! -name 'pr-*' -exec rm -rf {} + 2>/dev/null || true
  cp -r "$build_dir/." "$worktree/$dest_dir/"

  git -C "$worktree" add -A
  if git -C "$worktree" diff --cached --quiet; then
    echo "publish_to_gh_pages.sh: nothing changed, skipping commit"
    rm -rf "$tmp"
    exit 0
  fi
  git -C "$worktree" commit -q -m "$commit_msg"

  if git -C "$worktree" push origin gh-pages; then
    rm -rf "$tmp"
    exit 0
  fi

  echo "publish_to_gh_pages.sh: push rejected (attempt $attempt/$max_attempts) -- likely a concurrent deploy, retrying" >&2
  rm -rf "$tmp"
done

echo "publish_to_gh_pages.sh: failed to push after $max_attempts attempts" >&2
exit 1
