# Business Agent Workflow

## 1. Purpose

This document is the single, ordered, end-to-end contract for one Business Agent run: from registered source material to a submitted Business PR. It answers the TODO left open in [PRD.md](../PRD.md) section 13: "Define the complete Business Agent process from Design Handoff Bundle ingestion through Business PR creation."

It is a synthesis document, not a new set of rules. Every step below is already governed in detail by an existing specification; this document orders those steps into one procedure and states, in one place, the input contract, the output contract, and what the Business Agent must never do. Where this document and a cited section disagree, the cited section is authoritative -- this document must be corrected to match it, not the reverse.

## 2. Relationship to Other Artifacts

- [PRODUCT-SOURCE-MATERIAL-SPEC.md](PRODUCT-SOURCE-MATERIAL-SPEC.md) governs the input.
- [DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md](DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md) governs the optional UI-design source type.
- [DESIGN-ANALYSIS-SPEC.md](DESIGN-ANALYSIS-SPEC.md) and [DESIGN-ANALYSIS-REVIEW-SPEC.md](DESIGN-ANALYSIS-REVIEW-SPEC.md) govern the analysis stage and its review gate.
- [BUSINESS-REQUIREMENTS-SPEC.md](BUSINESS-REQUIREMENTS-SPEC.md) governs the requirements stage.
- [BUSINESS-PR-SPEC.md](BUSINESS-PR-SPEC.md) governs Epic/Story decomposition and the Business PR itself.
- [EVIDENCE-SPEC.md](EVIDENCE-SPEC.md) governs the evidence rule that runs through every step.
- [AGENT-RESPONSIBILITIES.md](AGENT-RESPONSIBILITIES.md) governs the Business Agent's authority boundary.

## 3. Input Contract

The Business Agent does not begin from an arbitrary document. It begins from source material that has already been registered and checked for readiness:

```text
Source Material
  (registered per PRODUCT-SOURCE-MATERIAL-SPEC.md sections 4 and 8)
        |
        v
Design Handoff Bundle (optional, per DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md)
  or another configured source type (PRODUCT-SOURCE-MATERIAL-SPEC.md section 3)
        |
        v
Design Analysis
```

Entry condition: readiness must be `Ready` or `Ready with Limitations` per [PRODUCT-SOURCE-MATERIAL-SPEC.md](PRODUCT-SOURCE-MATERIAL-SPEC.md) section 9. If readiness is `Blocked`, the Business Agent must not proceed -- it records the blocker and stops (section 8 below).

For a native Claude Design export, this entry condition is signaled by a tracked GitHub Issue (`agent:business`/`status:queued`, opened by `.github/workflows/design-branch-intake.yml` on merge into the `design` branch) naming the readiness value directly -- see GITHUB-PLATFORM-ADAPTER-SPEC.md section 6.1 and DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md section 6.2. A hand-authored bundle instead uses the legacy PR-comment path GITHUB-PLATFORM-ADAPTER-SPEC.md section 6.1 also describes.

## 4. Processing

Steps 1-9 run in order and together produce one coherent Design Analysis. Steps 2-8 must all complete before step 9 is finalized -- a requirement must never be drafted in step 10 from a partially-completed analysis.

| # | Step | Governed by |
| --- | --- | --- |
| 1 | Validate source readiness | PRODUCT-SOURCE-MATERIAL-SPEC.md §9; DESIGN-ANALYSIS-REVIEW-SPEC.md §5 (Source Readiness Check) |
| 2 | Identify screens | DESIGN-ANALYSIS-SPEC.md §4.3 (Optional UI Design Inventory) |
| 3 | Identify user flows | DESIGN-ANALYSIS-SPEC.md §4.3, §4.6 (User Journeys and Workflows) |
| 4 | Identify actors | DESIGN-ANALYSIS-SPEC.md §4.2 (Product Context and Domain Inventory) |
| 5 | Identify capabilities | DESIGN-ANALYSIS-SPEC.md §4.5 |
| 6 | Identify observable behaviors | DESIGN-ANALYSIS-SPEC.md §4.4 (Product Understanding) |
| 7 | Identify business rules | DESIGN-ANALYSIS-SPEC.md §4.7 |
| 8 | Identify ambiguities | DESIGN-ANALYSIS-SPEC.md §4.10-4.11 (Decisions and Assumptions); EVIDENCE-SPEC.md §4-6 |
| 9 | Produce Design Analysis | DESIGN-ANALYSIS-SPEC.md (full artifact); self-review and traceability check per section 4.3 before finalizing; submit for review per DESIGN-ANALYSIS-REVIEW-SPEC.md §10-11 |
| 10 | Derive Business Requirements | BUSINESS-REQUIREMENTS-SPEC.md §2, §5-6 -- begins only from an analysis that has passed its configured review gate (DESIGN-ANALYSIS-REVIEW-SPEC.md §11, or the combined-review default in §17); see section 4.1 for when step 9 must pause before this step runs, and section 4.4 for updating the source Design Analysis's own traceability fields once Requirements exist |
| 11 | Group requirements into Epics | BUSINESS-REQUIREMENTS-SPEC.md §12; BUSINESS-PR-SPEC.md §7 (Epic boundary follows business capability, never an application or repository boundary); see section 4.2 for an Epic threatened by an unresolved ambiguity |
| 12 | Generate Stories | BUSINESS-PR-SPEC.md §7 (independently valuable, observable, traceable, no technical slicing, one approval decision each) |
| 13 | Generate Acceptance Criteria | BUSINESS-REQUIREMENTS-SPEC.md §7 |
| 14 | Identify unresolved decisions | Carried forward, never resolved by the agent -- EVIDENCE-SPEC.md §6; BUSINESS-REQUIREMENTS-SPEC.md §6 |
| 15 | Prepare Business PR | BUSINESS-PR-SPEC.md §8 (Required Business PR Content), including the Required Stage Trace (§6) |

### 4.1 Continuous Execution, With One Pause Trigger

Steps 1-15 run as one continuous Business Agent invocation by default, ending in Design Analysis approval and Business Scope approval being combined through the Business PR -- the "combined-review default" DESIGN-ANALYSIS-REVIEW-SPEC.md section 17 already allows "when configured." (The combined-vs-separate *review-package configuration* question in that section is a separate, still-open item -- this section resolves the Business Agent's own execution shape, not that configuration question.)

The Business Agent must instead pause after step 9 -- submitting the Design Analysis for its own review per DESIGN-ANALYSIS-REVIEW-SPEC.md sections 10-11, before proceeding to step 10 -- when either is true:

- the Design Analysis carries more than three unresolved `Decision Required` or `Technical Unknown` items (a default threshold; may be overridden per initiative), or
- the source readiness recorded at step 1 was `Ready with Limitations` rather than `Ready`

Either condition is evidence the analysis itself is less certain than usual, and building Requirements, Epics, Stories, and a Business PR on top of it risks compounding an error before anyone has checked it. Outside these triggers, the agent proceeds straight through to step 15.

### 4.2 An Ambiguity That Could Eliminate an Epic

When step 8 surfaces a Decision Required item that, if resolved one way, would eliminate an Epic entirely, the Epic is still included in the Business PR at step 15 -- with its Status set to `Blocked` and the triggering Decision Required item referenced directly on it. It is never silently omitted.

This matches how this repository already treats every other unresolved Decision Required and Assumption: BUSINESS-PR-SPEC.md section 9 requires every unresolved item to stay visible in the PR, and PRODUCT-SOURCE-MATERIAL-SPEC.md section 12's "must not silently alter" rule applies the same principle to change handling generally. Scope under real uncertainty stays visible to the Business Owner rather than disappearing from the reviewed PR without anyone deciding to drop it.

### 4.3 Self-Review and Traceability, Before Finalizing a Design Analysis

This section exists because real use (`DA-003`) needed a full, direct rewrite to fix what it now requires up front, instead of catching the problem after the fact. Evidence and classification being present and correct (steps 1-8, DESIGN-ANALYSIS-SPEC.md section 5) is necessary but not sufficient -- a Design Analysis that is technically complete but unreadable to its actual audience has still failed step 9. Before finalizing:

1. **Read the draft as its target reader would** -- a Business Analyst or Designer who has never seen this feature, not a reviewer auditing evidence. Confirm the feature-area narrative is understandable on its own, without needing to resolve an evidence link, a classification tag, or a Gherkin block to follow what the product does. If it isn't, the content is misplaced, not missing -- move it to the Requirements register or Evidence and Traceability section (DESIGN-ANALYSIS-SPEC.md section 4, `DESIGN-ANALYSIS-TEMPLATE.md`); don't delete it.
2. **Confirm no commentary about this document's own revision history appears in its primary content.** A note like "an earlier draft misread this" or "format revised because..." describes the document, not the product, and belongs in DESIGN-ANALYSIS-SPEC.md section 11's changelog -- never repeated inside an instance. This failure mode is easy to reintroduce even while actively fixing it -- it recurred three separate times across `DA-003`'s real revision history, including once while removing an earlier instance of itself. Check for it explicitly; do not assume a prior pass already caught it.
3. **Confirm traceability is walkable, not just present.** Every Requirement, Capability, and Business Rule must link upstream to the exact source reference that produced it (already required by EVIDENCE-SPEC.md section 7) -- and, once a downstream artifact exists for it (a Story, an Epic, a Business PR), it must link there too, by a real link, not just a fact recorded in the metadata table. See section 4.4 for when this update happens.

DESIGN-ANALYSIS-SPEC.md section 7's Quality Checks are the governing checklist for all three; this section states why they are a required step here, not a second definition of them.

### 4.4 Keeping Downstream Links Current

A Design Analysis's `Related Epic` / `Related Stories` metadata fields (DESIGN-ANALYSIS-SPEC.md section 3) and each Requirement's own forward reference start as `Pending` and stay accurate only if something updates them. When step 10 produces Business Requirements, and step 11 groups them into Epics, the agent returns to the source Design Analysis and fills in those fields and links -- this is a required part of steps 10-11, not a separate, optional cleanup pass. A Design Analysis whose metadata still reads `Pending` after its Requirements have actually been drafted is out of date, not merely incomplete.

## 5. Output Contract

A completed Business Agent run produces exactly these artifacts, each already specified elsewhere and each required as part of the Business PR per [BUSINESS-PR-SPEC.md](BUSINESS-PR-SPEC.md) section 8:

| Output | Specified in |
| --- | --- |
| Design Analysis | DESIGN-ANALYSIS-SPEC.md |
| Business Requirements | BUSINESS-REQUIREMENTS-SPEC.md |
| Epics | BUSINESS-REQUIREMENTS-SPEC.md §12; BUSINESS-PR-SPEC.md §7 |
| Stories | BUSINESS-PR-SPEC.md §3 (Epic and Stories) |
| Acceptance Criteria | BUSINESS-REQUIREMENTS-SPEC.md §7 |
| Business Decisions (Decisions Required) | BUSINESS-REQUIREMENTS-SPEC.md §7; EVIDENCE-SPEC.md §6 |
| Open Questions / Assumptions | BUSINESS-REQUIREMENTS-SPEC.md §6; DESIGN-ANALYSIS-SPEC.md §4.11 |
| Traceability | BUSINESS-PR-SPEC.md §6 (Required Stage Trace); EVIDENCE-SPEC.md §3 |

None of these is optional. A Business PR missing any of them fails the quality gate in [BUSINESS-PR-SPEC.md](BUSINESS-PR-SPEC.md) section 9.

## 6. The Business Agent MUST NOT

This consolidates the technical-inference boundary in [DESIGN-ANALYSIS-SPEC.md](DESIGN-ANALYSIS-SPEC.md) section 6 and the process boundary in [AGENT-RESPONSIBILITIES.md](AGENT-RESPONSIBILITIES.md) into one checklist. The Business Agent must not:

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
Source Material
        |
        v
Design Handoff Bundle / other configured source  --[readiness: Ready]-->
        |
        v
   Design Analysis  (steps 1-9)
        |
        v
   Business Requirements  (step 10)
        |
        v
   Epics + Stories + Acceptance Criteria  (steps 11-13)
        |
        v
   Business Decisions + Open Questions  (step 14, carried forward, not resolved)
        |
        v
   Business PR  (step 15)
        |
        v
   Business Owner Review  (BUSINESS-PR-SPEC.md §10)
```

Merge of an Approved Business PR is where this document's scope ends -- see [TECHNICAL-AGENT-WORKFLOW.md](TECHNICAL-AGENT-WORKFLOW.md) for the mirrored, ordered contract covering everything from that merge to Technical Ready Tasks and Spikes.

## 8. Failure and Blocking Conditions

The Business Agent must stop and record a blocker, rather than proceeding, when:

- source readiness is `Blocked` (PRODUCT-SOURCE-MATERIAL-SPEC.md §9)
- the Design Analysis cannot pass its own quality checks (DESIGN-ANALYSIS-SPEC.md §7)
- a requirement candidate has no evidence and is not `Human Provided` (EVIDENCE-SPEC.md §7)
- completing a step would require a decision listed in section 6 above

A blocked run must state the reason, the affected step, and the owner who can unblock it, consistent with the failure-handling pattern already used in [TECHNICAL-HANDOFF.md](TECHNICAL-HANDOFF.md).

### 8.1 Resuming After `Changes Requested`

Whether a `Changes Requested` outcome -- from Design Analysis review or Business Owner review -- requires re-running the full sequence from step 1 depends on the same Major/Editorial distinction REQUIREMENTS-VERSIONING-SPEC.md section 9 already uses for approval validity, applied here rather than defined a second time:

- **Editorial feedback** -- wording, an acceptance criterion's phrasing, a Story description -- may be patched directly at the step that produced it and resubmitted, without re-running earlier steps, provided the audit record confirms meaning was unchanged.
- **Material feedback** -- a wrong actor, a business rule that doesn't actually apply, anything that changes meaning -- must flow back through whichever step actually produced it (not necessarily step 1), and every step downstream of that one must be re-run. Patching only the symptom risks the same artifact drift REQUIREMENTS-VERSIONING-SPEC.md exists to prevent.

The Business Agent classifies feedback as Editorial or Material using this same test, not a second, competing definition.

## 9. One-Page Compliance Checklist

- [ ] Source readiness confirmed before any analysis began (step 1)
- [ ] Design Analysis covers screens, flows, actors, capabilities, behaviors, rules, and ambiguities (steps 2-8) before being finalized (step 9)
- [ ] Before finalizing, the Design Analysis passed the self-review in section 4.3 -- read as its target reader would read it, narrative and audit-trail evidence structurally separated, no inline revision commentary about the document's own history
- [ ] If the Design Analysis has more than three unresolved Decision Required/Technical Unknown items, or source readiness was `Ready with Limitations`, the run paused for review before step 10 (section 4.1)
- [ ] Business Requirements were derived only from a reviewed/approved Design Analysis (step 10)
- [ ] Once Business Requirements/Epics exist, the source Design Analysis's own `Related Epic`/`Related Stories` fields and requirement links were updated to match, not left `Pending` (section 4.4)
- [ ] Every Epic groups a coherent business capability, not an application or repository (step 11)
- [ ] An Epic threatened by an unresolved ambiguity is included and marked `Blocked`, never omitted (section 4.2)
- [ ] Every Story is independently valuable and free of technical slicing (step 12)
- [ ] Acceptance criteria are observable in business language (step 13)
- [ ] Every unresolved decision and assumption is still visible in the PR, not silently resolved (step 14)
- [ ] The Business PR includes all eight outputs in section 5, including a complete Stage Trace (step 15)
- [ ] No output contains a technical implementation detail (section 6)
- [ ] The Business Agent has not approved or merged its own PR

## 10. Revision History

*No open decisions remain in this document -- every question this section once tracked is resolved and stated directly at its governing section (4.1, 4.2, 4.3, 4.4, 8.1). This table is what and when, not why -- the current rule and its rationale live at the cited section, not here.*

| Date | Section | Change |
| --- | --- | --- |
| 2026-09-21 | 4.3, 4.4 | Added the self-review-before-finalizing requirement and the keep-downstream-links-current requirement, after real use (`DA-003`) needed a direct rewrite to add both after the fact. |
| 2026-09-03 | 3 | Native Claude Design export entry condition changed from a PR-comment signal to a tracked GitHub Issue (`design-branch-intake.yml`); the PR-comment path continues for hand-authored bundles only. |
| 2026-09-01 | 4.1 | Decided steps 1-15 run continuously by default (single combined Business Owner review) rather than as two separately-gated runs. |
| 2026-09-01 | 4.2 | Decided an Epic threatened by an unresolved Decision Required item stays in the Business PR, marked `Blocked`, rather than being omitted. |
| 2026-09-01 | 8.1 | Decided `Changes Requested` resumption uses the existing Major/Editorial distinction (`REQUIREMENTS-VERSIONING-SPEC.md` section 9) rather than a new one. |
