#!/bin/bash
# Post or update the docs-preview comment on a PR -- idempotent, so pushing
# several commits to the same open PR updates one comment rather than
# spamming a new one each time. Finds an existing comment by a hidden
# marker and PATCHes it; otherwise creates one.
#
# Requires GH_TOKEN in the environment (the workflow's own GITHUB_TOKEN is
# sufficient) and must run inside a checkout of the repo, so `gh` can infer
# owner/repo.
#
# Usage:
#   post_preview_comment.sh <pr-number> <body-text>

set -euo pipefail

pr="$1"
body="$2"
marker="<!-- docs-preview-comment -->"
full_body="$marker
$body"

existing_id=$(gh api "repos/{owner}/{repo}/issues/$pr/comments" --jq ".[] | select(.body | startswith(\"$marker\")) | .id" | head -1)

if [ -n "$existing_id" ]; then
  gh api "repos/{owner}/{repo}/issues/comments/$existing_id" -X PATCH -f body="$full_body" > /dev/null
  echo "Updated existing preview comment ($existing_id) on PR #$pr"
else
  gh api "repos/{owner}/{repo}/issues/$pr/comments" -X POST -f body="$full_body" > /dev/null
  echo "Posted new preview comment on PR #$pr"
fi
