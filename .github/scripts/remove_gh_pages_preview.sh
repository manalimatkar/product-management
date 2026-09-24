#!/bin/bash
# Remove one PR's preview subdirectory from the gh-pages branch, leaving the
# main site and every other PR's preview untouched. Run when a preview PR
# closes (merged or not), so previews don't accumulate indefinitely.
#
# Usage:
#   remove_gh_pages_preview.sh <dest_subdir> <commit_message>
#
# <dest_subdir> is "pr-<number>" -- this script deliberately refuses to
# remove "." (the main site) or anything that doesn't look like a preview
# folder, since a typo here would otherwise be destructive to the real site.

set -euo pipefail

dest_dir="$1"
commit_msg="$2"

case "$dest_dir" in
  pr-*) ;;
  *)
    echo "remove_gh_pages_preview.sh: refusing to remove '$dest_dir' -- only a pr-<number> folder is a valid target" >&2
    exit 1
    ;;
esac

remote_url=$(git remote get-url origin)
max_attempts=5

for attempt in $(seq 1 "$max_attempts"); do
  if ! git ls-remote --exit-code --heads origin gh-pages > /dev/null 2>&1; then
    echo "remove_gh_pages_preview.sh: gh-pages branch doesn't exist -- nothing to clean up"
    exit 0
  fi

  tmp=$(mktemp -d)
  worktree="$tmp/gh-pages"
  git clone -q --branch gh-pages --single-branch "$remote_url" "$worktree"
  git -C "$worktree" config user.name "github-actions[bot]"
  git -C "$worktree" config user.email "41898282+github-actions[bot]@users.noreply.github.com"

  if [ ! -d "$worktree/$dest_dir" ]; then
    echo "remove_gh_pages_preview.sh: '$dest_dir' doesn't exist on gh-pages -- nothing to clean up"
    rm -rf "$tmp"
    exit 0
  fi

  git -C "$worktree" rm -rf -q "$dest_dir"
  git -C "$worktree" commit -q -m "$commit_msg"

  if git -C "$worktree" push origin gh-pages; then
    rm -rf "$tmp"
    exit 0
  fi

  echo "remove_gh_pages_preview.sh: push rejected (attempt $attempt/$max_attempts) -- likely a concurrent deploy, retrying" >&2
  rm -rf "$tmp"
done

echo "remove_gh_pages_preview.sh: failed to push after $max_attempts attempts" >&2
exit 1
