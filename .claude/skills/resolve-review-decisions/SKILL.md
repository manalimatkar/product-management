---
name: resolve-review-decisions
description: Turns a Design Analysis review PR's comments into recorded resolutions -- new Observation entries, updated Decisions, updated Business Requirements -- the way DA-003's DEC-001 through DEC-004 were resolved by hand. Use once a Business Owner has left review comments on an open Design Analysis PR and you need to incorporate them.
---

# Resolve Review Decisions

This repository's established pattern (2026-09-08): open Decisions on a Design Analysis get resolved directly on its review PR -- inline comments on the specific line, or a general comment on the PR -- never in chat, never as a separate Issue. This skill is the mechanical half of turning those comments into the document's actual recorded resolution. It is deliberately not fully automated: **matching a comment to the Decision it answers, and judging whether it actually resolves that Decision, stays a human-supervised, agent-assisted reading step, never a script's guess.**

## Hard constraint, restated from `.claude/agents/business-agent.md`

**Never mark a `Decision Required` item resolved on your own reasoning.** Only transcribe what the Business Owner actually said. If a comment is ambiguous, off-topic, or doesn't clearly answer the Decision it's attached to, leave the Decision open and flag the ambiguity back -- don't guess at what they probably meant.

## Step 1 -- fetch the raw comments

```bash
python .github/scripts/fetch_review_comments.py --pr <number>
```

This returns three things, each real and unedited:

- **`inline_comments`** -- comments anchored to a specific line, each with a few lines of surrounding context pulled from the file *as it existed at that comment's own commit* (not the file's current content -- the two can differ once the file's been revised since). This is what makes a comment interpretable: a comment's `original_line` on its own is just a number, but paired with the context lines it resolves to "this is answering `DEC-001`'s row," the same way `PR #17`'s four comments were matched to `DEC-001`-`DEC-004` by reading exactly this context.
- **`general_comments`** -- comments not anchored to any line at all. Don't skip these -- `DA-003`'s `BR-003` narrowing (Card view deferred to Table-only) came from a general comment, not an inline one.
- **`review_bodies`** -- a review submission's own overall comment (e.g. attached to "Changes requested"), separate from any inline comments it might also carry.

## Step 2 -- match each comment to what it's actually answering

Read every comment's context and decide, concretely:

- Which specific ID (a `DEC-`, or a `BR-` left unchecked in the Review Outcome task list, or something else entirely) is this comment attached to?
- Does it actually answer that item, or is it a side note, a question back, or something unrelated? Only the former gets recorded as a resolution.
- Is it resolving the item outright, resolving it with a scope change (like `BR-003`'s narrowing), or explicitly deferring it (like `DEC-004`'s "deferred until login exists" -- a real resolution, just not an answer to the literal question asked)?

## Step 3 -- record it in the Design Analysis, in the shape this repository already uses

For each resolved item:

1. Add a new `OBS-<next number>` entry in the Evidence and Traceability section: who said it, on which PR, the comment quoted directly (fix only obvious typos if quoting inline, or quote verbatim and note the typo), classified `Human Provided`, confidence `High`. Link it `↩ used by` whatever it resolves.
2. Update the `DEC-<id>` entry itself: mark **Resolved** (or **Resolved (deferred)** when that's what actually happened), with a link to the new Observation.
3. Update every Business Requirement or Business Rule the resolution actually affects -- not just the Decision's own line. If a comment narrows or extends a requirement's scope (like `BR-003` or `BR-015`), say so explicitly in that requirement's own entry, the way `BR-003`'s "Revised... narrowed rather than removed" note does -- never silently rewrite a requirement's statement without a visible note explaining why it changed.
4. If a resolution reveals something the original analysis didn't have at all (like `DA-003`'s `BR-016`, which didn't exist until a comment described a whole third entry path into the report), add it as a new, properly ID'd entry -- don't force a new fact into an existing item that doesn't actually cover it.

## Step 4 -- verify before calling it done

Run the `verify-design-analysis` skill against the file. A resolution pass that adds new `OBS-`/`DEC-` cross-links is exactly the kind of edit that can quietly break an anchor or leave a new entry with no inbound link.

## What this skill does not do

- Does not touch the PR's sign-off checkbox or its Review Outcome task-list checkboxes -- that stays the Business Owner's own action, not something this skill or the agent using it performs on their behalf.
- Does not open or update the PR -- run `run-gate-checks` and get an explicit go-ahead before that, same as any other change.
- Does not resolve a Decision the comments don't actually address -- an unresolved item stays open and visible, exactly as `DESIGN-ANALYSIS-SPEC.md` requires.

## Verified against

`fetch_review_comments.py` was run against the real `PR #17` before this skill was written down: all four inline comments resolved to exactly the right `DEC-001`-`DEC-004` rows (confirmed by reading `DA-003` as it stood at each comment's own commit, not its current content), and the general comments correctly surfaced the `BR-003` narrowing that an inline-only search would have missed entirely.
