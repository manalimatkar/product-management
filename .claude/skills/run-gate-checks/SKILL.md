---
name: run-gate-checks
description: Runs the right merge gate(s) -- design_branch_gate, bundle_gate, or business_pr_gate -- against a real PR or a local diff, before it's actually opened or merged. Use before opening a PR into the design branch or main whenever the change touches a native design export, a hand-authored bundle, or a Business PR.
---

# Run Gate Checks

This repository has three merge gates, each tied to a specific path shape and each written to run inside GitHub Actions, where a workflow step already has the exact inputs they need (a JSON list of changed files, the PR description as a text file) sitting ready. Checking any of them by hand meant reconstructing those inputs manually every time. `run_gate_checks.py` does that reconstruction, picks whichever gate(s) actually apply, and runs them for real.

## When to run this

- Before opening a PR into the `design` branch (native Claude Design export upload) -- confirms `design_branch_gate` will pass before GitHub ever sees it.
- Before opening a PR into `main` that adds or changes a hand-authored Design Handoff Bundle -- `bundle_gate`.
- Before opening a PR into `main` that adds or changes a Business PR -- `business_pr_gate`.
- Against an already-open PR, any time -- to check current status without waiting for the CI workflow to run.

## How to run it

Against a real, already-open PR:

```bash
python .github/scripts/run_gate_checks.py --pr <number>
```

Against a local branch that doesn't have a PR yet (the more common case, since this repo's own working practice is not to open a PR until the change is ready):

```bash
python .github/scripts/run_gate_checks.py --base main --head <your-branch>
```

A local diff has no real PR description yet, so sign-off-checkbox checks will correctly report as missing -- that's accurate, not a bug. To check what happens once a sign-off line is added, write the intended PR description to a file and pass it:

```bash
python .github/scripts/run_gate_checks.py --base main --head <your-branch> --pr-body-file draft-pr-body.txt
```

## What it actually does

Determines which gate(s) apply by reusing each gate script's own path-matching logic directly (imported, not re-implemented, so the two can't drift apart) -- never guesses from the branch name alone. Then creates a real, isolated `git worktree` checkout of the exact commit being checked (this matters: `design_branch_gate` in particular reads real files from disk, not from the diff -- checking from whatever happens to be your *current* branch, if it never had those files, silently reports them "missing" even when they're genuinely present in the change being checked. This was a real bug caught while building this tool, not a hypothetical one), runs each applicable gate's `check` subcommand as a real subprocess against that checkout, and prints one consolidated report.

It only ever runs `check` (pre-merge validation), never `apply` -- `apply` mutates real files (a cover sheet, a bundle's frontmatter) and is meant to run once, on an actual merge, not repeatedly while checking things locally.

## Reading the output

- **`PASSED`, exit code 0** -- every applicable gate is clean. If it also says "no gate applies to this change," that's a legitimate outcome too (e.g. a framework/docs-only change like this one) -- not every change is supposed to trigger a gate.
- **`FAILED`, exit code 1** -- at least one applicable gate reported problems, listed under that gate's own name. Fix everything listed before opening the PR for real.

## Verified against, not just written

Tested against real cases before being trusted: a real merged PR with no applicable gate (`#24`), a real merged PR where `design_branch_gate` genuinely applies and passes (`#15`), and a local scratch commit exercising `business_pr_gate`'s both outcomes -- correctly failed with no sign-off checkbox present, correctly passed once one was added. A fourth historical PR (`#4`) was checked and correctly reported "no gate applies" -- its paths predate the 2026-09-08 platform-first path migration, so the current gate regex correctly no longer matches them; not a tool bug, genuinely obsolete history.
