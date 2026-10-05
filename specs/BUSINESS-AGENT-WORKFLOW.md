# Business Agent Workflow

## 1. Purpose

This document is the single, ordered contract for one Business Agent run: from an approved Design Analysis to a submitted Business PR. It answers the TODO left open in [PRD.md](../PRD.md) section 13: "Define the complete Business Agent process from Design Handoff Bundle ingestion through Business PR creation" -- together with [DESIGN-ANALYSIS-AGENT-WORKFLOW.md](DESIGN-ANALYSIS-AGENT-WORKFLOW.md), which covers the first half of that path, from source material to an approved Design Analysis.

The business side of the pipeline is two agent stages, not one. The Design Analysis Agent establishes what was designed and what it means; this stage turns that approved understanding into reviewable scope -- Business Requirements, Epics, Stories, Acceptance Criteria, and the Business PR. This stage never re-analyzes the source and never starts from an analysis that hasn't passed its own review.

It is a synthesis document, not a new set of rules. Every step below is already governed in detail by an existing specification; this document orders those steps into one procedure and states, in one place, the input contract, the output contract, and what the Business Agent must never do. Where this document and a cited section disagree, the cited section is authoritative -- this document must be corrected to match it, not the reverse.

## 2. Relationship to Other Artifacts

- [DESIGN-ANALYSIS-AGENT-WORKFLOW.md](DESIGN-ANALYSIS-AGENT-WORKFLOW.md) is the previous stage, and produces this stage's input.
- [DESIGN-ANALYSIS-SPEC.md](DESIGN-ANALYSIS-SPEC.md) and [DESIGN-ANALYSIS-REVIEW-SPEC.md](DESIGN-ANALYSIS-REVIEW-SPEC.md) govern the input artifact and the review gate it must have passed.
- [BUSINESS-REQUIREMENTS-SPEC.md](BUSINESS-REQUIREMENTS-SPEC.md) governs the requirements stage.
- [BUSINESS-PR-SPEC.md](BUSINESS-PR-SPEC.md) governs Epic/Story decomposition and the Business PR itself.
- [EVIDENCE-SPEC.md](EVIDENCE-SPEC.md) governs the evidence rule that runs through every step.
- [AGENT-RESPONSIBILITIES.md](AGENT-RESPONSIBILITIES.md) governs the Business Agent's authority boundary.

## 3. Input Contract

The Business Agent begins from one thing only: an approved Design Analysis.

```text
Approved Design Analysis
  (DESIGN-ANALYSIS-AGENT-WORKFLOW.md section 5.1:
   review PR merged, Status field reads Approved)
        |
        v
Business Requirements  (this stage)
```

Entry condition: the Design Analysis has passed its review gate (`GATE-003`, DESIGN-ANALYSIS-REVIEW-SPEC.md §11) -- its review PR is merged and its own `Status` field reads `Approved`. If the Design Analysis is still `Draft` or `In Review`, or was `Rejected` or `Blocked`, the Business Agent must not proceed -- it records the blocker and stops (section 8 below).

The hand-off is started manually by default: the Business Owner asks for Business Requirements to be derived from a named, approved Design Analysis (DESIGN-ANALYSIS-AGENT-WORKFLOW.md section 5.1).

## 4. Processing

| # | Step | Governed by |
| --- | --- | --- |
| 1 | Confirm the Design Analysis is approved | DESIGN-ANALYSIS-REVIEW-SPEC.md §11, §13 (Approval Recording); section 3 above |
| 2 | Derive Business Requirements | BUSINESS-REQUIREMENTS-SPEC.md §2, §5-6 -- see section 4.4 for updating the source Design Analysis's own traceability fields once Requirements exist |
| 3 | Group requirements into Epics | BUSINESS-REQUIREMENTS-SPEC.md §12; BUSINESS-PR-SPEC.md §7 (Epic boundary follows business capability, never an application or repository boundary); see section 4.2 for an Epic threatened by an unresolved ambiguity |
| 4 | Generate Stories | BUSINESS-PR-SPEC.md §7 (independently valuable, observable, traceable, no technical slicing, one approval decision each) |
| 5 | Generate Acceptance Criteria | BUSINESS-REQUIREMENTS-SPEC.md §7 |
| 6 | Carry forward unresolved decisions | Carried forward from the Design Analysis, never resolved by the agent -- EVIDENCE-SPEC.md §6; BUSINESS-REQUIREMENTS-SPEC.md §6 |
| 7 | Prepare Business PR | BUSINESS-PR-SPEC.md §8 (Required Business PR Content), including the Required Stage Trace (§6) |

### 4.1 No Re-Analysis

The Business Agent works from the approved Design Analysis, not from the source material. If deriving a requirement reveals that the Design Analysis is wrong or incomplete -- a missing flow, a misread rule -- the Business Agent does not patch the gap itself. It stops, records what it found, and the Design Analysis goes back through the Design Analysis Agent and its review gate (DESIGN-ANALYSIS-AGENT-WORKFLOW.md section 8.1). Requirements built on an analysis the reviewer never saw are exactly what the separate gate exists to prevent.

### 4.2 An Ambiguity That Could Eliminate an Epic

When the Design Analysis carries a Decision Required item that, if resolved one way, would eliminate an Epic entirely, the Epic is still included in the Business PR at step 7 -- with its Status set to `Blocked` and the triggering Decision Required item referenced directly on it. It is never silently omitted.

This matches how this repository already treats every other unresolved Decision Required and Assumption: BUSINESS-PR-SPEC.md section 9 requires every unresolved item to stay visible in the PR, and PRODUCT-SOURCE-MATERIAL-SPEC.md section 12's "must not silently alter" rule applies the same principle to change handling generally. Scope under real uncertainty stays visible to the Business Owner rather than disappearing from the reviewed PR without anyone deciding to drop it.

### 4.3 Self-Review of the Design Analysis

Moved to [DESIGN-ANALYSIS-AGENT-WORKFLOW.md](DESIGN-ANALYSIS-AGENT-WORKFLOW.md) section 4.1 -- it governs the Design Analysis and its record files, which the Design Analysis Agent produces. The same product-documentation voice rules (no self-assessment, no filler intensifiers, no revision-history commentary in primary content) apply to everything this stage writes as well: Business Requirements, Epics, Stories, and the Business PR description.

### 4.4 Keeping Downstream Links Current

A Design Analysis's `Related Epic` / `Related Stories` metadata fields (DESIGN-ANALYSIS-SPEC.md section 3) and each requirement's own forward reference start as `Pending` and stay accurate only if something updates them. When step 2 produces Business Requirements, and step 3 groups them into Epics, the Business Agent returns to the source Design Analysis and fills in those fields and links -- this is a required part of steps 2-3, not a separate, optional cleanup pass. Only the metadata and forward links change; the analysis content itself is not edited at this stage (section 4.1).

## 5. Output Contract

A completed Business Agent run produces exactly these artifacts, each already specified elsewhere and each required as part of the Business PR per [BUSINESS-PR-SPEC.md](BUSINESS-PR-SPEC.md) section 8:

| Output | Specified in |
| --- | --- |
| Business Requirements | BUSINESS-REQUIREMENTS-SPEC.md |
| Epics | BUSINESS-REQUIREMENTS-SPEC.md §12; BUSINESS-PR-SPEC.md §7 |
| Stories | BUSINESS-PR-SPEC.md §3 (Epic and Stories) |
| Acceptance Criteria | BUSINESS-REQUIREMENTS-SPEC.md §7 |
| Business Decisions (Decisions Required) | BUSINESS-REQUIREMENTS-SPEC.md §7; EVIDENCE-SPEC.md §6 |
| Open Questions / Assumptions | BUSINESS-REQUIREMENTS-SPEC.md §6; DESIGN-ANALYSIS-SPEC.md §4.11 |
| Traceability | BUSINESS-PR-SPEC.md §6 (Required Stage Trace); EVIDENCE-SPEC.md §3 |
| Updated forward links on the source Design Analysis | Section 4.4 |

None of these is optional. A Business PR missing any of them fails the quality gate in [BUSINESS-PR-SPEC.md](BUSINESS-PR-SPEC.md) section 9. The Design Analysis itself is an input, cited by the Business PR's Stage Trace, not an output of this stage.

## 6. The Business Agent MUST NOT

This consolidates the technical-inference boundary in [DESIGN-ANALYSIS-SPEC.md](DESIGN-ANALYSIS-SPEC.md) section 6 and the process boundary in [AGENT-RESPONSIBILITIES.md](AGENT-RESPONSIBILITIES.md) into one checklist. The Business Agent must not:

- start from a Design Analysis that hasn't passed its review gate (section 3)
- re-analyze the source material, or edit the Design Analysis's content -- only its forward-link metadata (sections 4.1, 4.4)
- choose programming languages, frameworks, or UI component libraries (for example, deciding to use an Angular component)
- choose APIs, endpoints, or payloads
- choose databases or storage services
- choose service boundaries, cloud providers, infrastructure, or deployment architecture
- create engineering Tasks or Spikes -- those exist only after this PR is approved and merged, per CANONICAL-TASK-SPEC.md §3
- modify engineering repositories
- approve or merge its own Business PR
- regenerate, rewrite, or silently modify the source Design Handoff Bundle or other source material
- convert an `Assumption`, `Decision Required`, or `Technical Unknown` into a confirmed requirement (EVIDENCE-SPEC.md §6)
- trigger technical analysis before the Business PR is approved and merged

If a step in section 4 would require crossing one of these lines to proceed, the Business Agent must stop and record the item as a Decision Required or Technical Unknown instead of resolving it.

## 7. End-to-End Diagram

```text
   Approved Design Analysis  (DESIGN-ANALYSIS-AGENT-WORKFLOW.md)
        |
        v
   Business Requirements  (step 2)
        |
        v
   Epics + Stories + Acceptance Criteria  (steps 3-5)
        |
        v
   Business Decisions + Open Questions  (step 6, carried forward, not resolved)
        |
        v
   Business PR  (step 7)
        |
        v
   Business Owner Review  (GATE-004, BUSINESS-PR-SPEC.md §10)
```

Merge of an Approved Business PR is where this document's scope ends -- see [TECHNICAL-AGENT-WORKFLOW.md](TECHNICAL-AGENT-WORKFLOW.md) for the mirrored, ordered contract covering everything from that merge to Technical Ready Tasks and Spikes.

## 8. Failure and Blocking Conditions

The Business Agent must stop and record a blocker, rather than proceeding, when:

- the Design Analysis has not passed its review gate (section 3)
- deriving a requirement reveals the Design Analysis is wrong or incomplete (section 4.1)
- a requirement candidate has no evidence and is not `Human Provided` (EVIDENCE-SPEC.md §7)
- completing a step would require a decision listed in section 6 above

A blocked run must state the reason, the affected step, and the owner who can unblock it, consistent with the failure-handling pattern already used in [TECHNICAL-HANDOFF.md](TECHNICAL-HANDOFF.md).

### 8.1 Resuming After `Changes Requested`

Whether a `Changes Requested` outcome from Business Owner review requires re-running the full sequence depends on the same Major/Editorial distinction REQUIREMENTS-VERSIONING-SPEC.md section 9 already uses for approval validity, applied here rather than defined a second time:

- **Editorial feedback** -- wording, an acceptance criterion's phrasing, a Story description -- may be patched directly at the step that produced it and resubmitted, without re-running earlier steps, provided the audit record confirms meaning was unchanged.
- **Material feedback** -- a wrong actor, a business rule that doesn't actually apply, anything that changes meaning -- must flow back through whichever step actually produced it, and every step downstream of that one must be re-run. If the root cause is in the Design Analysis itself, it goes back through the Design Analysis Agent and its review gate (section 4.1), not patched here.

The Business Agent classifies feedback as Editorial or Material using this same test, not a second, competing definition.

## 9. One-Page Compliance Checklist

- [ ] The Design Analysis was approved (review PR merged, `Status: Approved`) before any requirement was drafted (step 1)
- [ ] The source material was not re-analyzed and the Design Analysis's content was not edited -- only its forward links (sections 4.1, 4.4)
- [ ] Once Business Requirements/Epics exist, the source Design Analysis's `Related Epic`/`Related Stories` fields and requirement links were updated, not left `Pending` (section 4.4)
- [ ] Every Epic groups a coherent business capability, not an application or repository (step 3)
- [ ] An Epic threatened by an unresolved ambiguity is included and marked `Blocked`, never omitted (section 4.2)
- [ ] Every Story is independently valuable and free of technical slicing (step 4)
- [ ] Acceptance criteria are observable in business language (step 5)
- [ ] Every unresolved decision and assumption is still visible in the PR, not silently resolved (step 6)
- [ ] The Business PR includes every output in section 5, including a complete Stage Trace (step 7)
- [ ] Everything written follows the product-documentation voice rules (section 4.3)
- [ ] No output contains a technical implementation detail (section 6)
- [ ] The Business Agent has not approved or merged its own PR

## 10. Revision History

*This table is what and when, not why -- the current rule and its rationale live at the cited section, not here.*

| Date | Section | Change |
| --- | --- | --- |
| 2026-10-05 | all | Split in two. Former steps 1-9 (source readiness through producing the Design Analysis) moved to the new `DESIGN-ANALYSIS-AGENT-WORKFLOW.md`, along with former section 4.3 (self-review). This document now covers only approved Design Analysis to Business PR, renumbered steps 1-7. Former section 4.1 (continuous 15-step run with one pause trigger) replaced by section 4.1 (no re-analysis) -- the Design Analysis review gate now always runs separately, matching how `DA-003` was reviewed in practice. |
| 2026-09-25 | 4.3 | Extended section 4.3 to every Journey/Capability/Business Rule record file, not just the Design Analysis, and added the product-documentation voice step (no self-assessment, no filler intensifiers). |
| 2026-09-21 | 4.3, 4.4 | Added the self-review-before-finalizing requirement and the keep-downstream-links-current requirement, after real use (`DA-003`) needed a direct rewrite to add both after the fact. |
| 2026-09-03 | 3 | Native Claude Design export entry condition changed from a PR-comment signal to a tracked GitHub Issue (`design-branch-intake.yml`); the PR-comment path continues for hand-authored bundles only. |
| 2026-09-01 | 4.1 | Decided steps 1-15 run continuously by default (single combined Business Owner review) rather than as two separately-gated runs. Superseded 2026-10-05. |
| 2026-09-01 | 4.2 | Decided an Epic threatened by an unresolved Decision Required item stays in the Business PR, marked `Blocked`, rather than being omitted. |
| 2026-09-01 | 8.1 | Decided `Changes Requested` resumption uses the existing Major/Editorial distinction (`REQUIREMENTS-VERSIONING-SPEC.md` section 9) rather than a new one. |
