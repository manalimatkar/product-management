---
name: verify-design-analysis
description: Checks a Design Analysis artifact's internal traceability -- every ID-only heading unique, every markdown link resolves, every evidence entry has an inbound citation. Use after drafting or revising any Design Analysis, before opening or updating its review PR.
---

# Verify Design Analysis

This repository's Design Analysis format (`templates/DESIGN-ANALYSIS-TEMPLATE.md`) depends on two things holding for real, everywhere in the document: every linkable item (`BR-`, `CAP-`, `OBS-`, `GAP-`, `DEC-`, `ASM-`, `TECH-`, `BRULE-`) has exactly one ID-only heading, and every `[text](#anchor)` link actually resolves to one. Neither is obvious by eye in an 800-line document -- this is exactly the kind of drift that produced real breakage this session (`BR-003`'s anchor changing when its title was reworded, before the ID-only-heading rule existed).

## When to run this

- After drafting a new Design Analysis (Business Agent workflow step 9).
- After any revision -- a review round, a Decision resolution, a narrowing/scope change like `BR-003`'s.
- Before opening or updating that analysis's review PR. A Design Analysis with broken internal links is not ready for review, whatever else it says.

## How to run it

```bash
python .github/scripts/verify_design_analysis.py <path-to-the-DA-file.md>
```

## Reading the output

- **`PASSED`, exit code 0** -- every ID is unique and every link resolves. Warnings may still print; read them.
- **`FAILED`, exit code 1** -- a duplicated ID heading or a broken link. Fix every listed error before treating the document as done. A broken link here means a reviewer clicking "Evidence: [OBS-014]" lands nowhere -- don't ship that.
- **Warnings** (do not fail the check) -- an entry in the Evidence and Traceability section that nothing else in the document links to. This usually means one of two things: a genuinely orphaned entry (something was cut from the narrative but its evidence entry wasn't removed), or a missing citation (the entry is real and used, but the "Evidence:"/"Related:" link that should point to it was never added). Either way, look at it -- don't ignore a warning just because it doesn't fail the check.

## What this does not check

- Whether the evidence classification (`Explicit` / `Strongly Implied` / `Assumption` / `Human Provided`) is the *correct* one for what's cited -- that's a judgment call, not a mechanical check (`EVIDENCE-SPEC.md`).
- Whether every required section from `DESIGN-ANALYSIS-SPEC.md` section 4 is present in substance -- use that document's own Quality Checklist for that.
- HTML usage, table formatting, or anything else about the document's prose -- this tool is scoped to ID/link integrity only.

If you're extending this skill to run automatically (e.g. as a status check on Design Analysis review PRs, alongside `design_branch_gate.py`/`business_pr_gate.py`), that's a real next step but hasn't been built -- this is a manual, on-demand check today.
