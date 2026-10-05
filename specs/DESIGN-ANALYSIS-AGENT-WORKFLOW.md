# Design Analysis Agent Workflow

## 1. Purpose

This document is the single, ordered contract for one Design Analysis Agent run: from registered, ready source material to an approved Design Analysis. It is the first of two business-side agent stages. The second, the Business Agent, starts only from the approved Design Analysis this stage produces -- see [BUSINESS-AGENT-WORKFLOW.md](BUSINESS-AGENT-WORKFLOW.md).

The two stages are separate because they are different jobs. This stage answers *what was designed and what does it mean* -- an accurate, evidence-backed account of the proposed experience. The Business Agent stage answers *what must the product do, broken into reviewable scope* -- Requirements, Epics, Stories, and the Business PR. Keeping them apart gives the Design Analysis its own review gate, so Requirements are never built on an analysis nobody has checked.

Like BUSINESS-AGENT-WORKFLOW.md, this is a synthesis document, not a new set of rules. Every step below is governed in detail by an existing specification; this document orders those steps and states the input contract, the output contract, and what this agent must never do. Where this document and a cited section disagree, the cited section is authoritative.

## 2. Relationship to Other Artifacts

- [PRODUCT-SOURCE-MATERIAL-SPEC.md](PRODUCT-SOURCE-MATERIAL-SPEC.md) governs the input.
- [DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md](DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md) governs the optional UI-design source type; [CLAUDE-DESIGN-READING-SPEC.md](CLAUDE-DESIGN-READING-SPEC.md) governs how to read a native Claude Design export accurately.
- [DESIGN-ANALYSIS-SPEC.md](DESIGN-ANALYSIS-SPEC.md) governs the artifact this stage produces; [DESIGN-ANALYSIS-REVIEW-SPEC.md](DESIGN-ANALYSIS-REVIEW-SPEC.md) governs its review gate.
- [EVIDENCE-SPEC.md](EVIDENCE-SPEC.md) governs the evidence rule that runs through every step.
- [ARTIFACT-RELATIONSHIP-MODEL.md](ARTIFACT-RELATIONSHIP-MODEL.md) section 3.1 governs the Journey, Capability, and Business Rule records and registries this stage creates or cites.
- [AGENT-RESPONSIBILITIES.md](AGENT-RESPONSIBILITIES.md) governs this agent's authority boundary.
- [BUSINESS-AGENT-WORKFLOW.md](BUSINESS-AGENT-WORKFLOW.md) is the next stage, and consumes this stage's output.

## 3. Input Contract

The Design Analysis Agent begins from source material that has already been registered and checked for readiness:

```text
Source Material
  (registered per PRODUCT-SOURCE-MATERIAL-SPEC.md sections 4 and 8)
        |
        v
Design Handoff Bundle (optional, per DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md)
  or another configured source type (PRODUCT-SOURCE-MATERIAL-SPEC.md section 3)
        |
        v
Design Analysis  (this stage)
```

Entry condition: readiness must be `Ready` or `Ready with Limitations` per [PRODUCT-SOURCE-MATERIAL-SPEC.md](PRODUCT-SOURCE-MATERIAL-SPEC.md) section 9. If readiness is `Blocked`, the agent must not proceed -- it records the blocker and stops (section 8 below).

For a native Claude Design export, this entry condition is signaled by a tracked GitHub Issue (`agent:design-analysis`/`status:queued`, opened by `.github/workflows/design-branch-intake.yml` on merge into the `design` branch) naming the readiness value directly -- see GITHUB-PLATFORM-ADAPTER-SPEC.md section 6.1 and DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md section 6.2. A hand-authored bundle instead uses the legacy PR-comment path GITHUB-PLATFORM-ADAPTER-SPEC.md section 6.1 also describes.

## 4. Processing

Steps run in order and together produce one coherent Design Analysis. Steps 2-8 must all complete before step 9 is finalized.

| # | Step | Governed by |
| --- | --- | --- |
| 1 | Validate source readiness | PRODUCT-SOURCE-MATERIAL-SPEC.md §9; DESIGN-ANALYSIS-REVIEW-SPEC.md §5 (Source Readiness Check) |
| 2 | Identify screens | DESIGN-ANALYSIS-SPEC.md §4.3 (Optional UI Design Inventory) |
| 3 | Identify user flows | DESIGN-ANALYSIS-SPEC.md §4.3, §4.6 (User Journeys and Workflows) -- map the flow before decomposing it (DESIGN-ANALYSIS-SPEC.md §4, analysis order) |
| 4 | Identify actors | DESIGN-ANALYSIS-SPEC.md §4.2 (Product Context and Domain Inventory) |
| 5 | Identify capabilities | DESIGN-ANALYSIS-SPEC.md §4.5 -- check the Capability registry before minting a new ID |
| 6 | Identify observable behaviors and the information users see or provide | DESIGN-ANALYSIS-SPEC.md §4.4 (Product Understanding), §4.17 (Information Analysis), §4.18 (Existing vs. New Experience) |
| 7 | Identify business rules | DESIGN-ANALYSIS-SPEC.md §4.7 -- check the Business Rule registry before minting a new ID |
| 8 | Identify ambiguities and scope boundary | DESIGN-ANALYSIS-SPEC.md §4.10-4.12 (Decisions, Assumptions, Exclusions and Limitations); EVIDENCE-SPEC.md §4-6 |
| 9 | Produce the Design Analysis | DESIGN-ANALYSIS-SPEC.md (full artifact), including §4.14-4.16 (Problem, Goals, Success Metrics); self-review per section 4.1 below before finalizing; submit for review per DESIGN-ANALYSIS-REVIEW-SPEC.md §10-11 |

### 4.1 Self-Review and Traceability, Before Finalizing a Design Analysis (and Any Record File It Produces)

Evidence and classification being present and correct (steps 1-8, DESIGN-ANALYSIS-SPEC.md section 5) is necessary but not sufficient -- a Design Analysis that is technically complete but unreadable to its actual audience has still failed step 9. This applies to the Design Analysis document itself and to every Journey, Capability, and Business Rule record file the agent writes or updates alongside it (`ARTIFACT-RELATIONSHIP-MODEL.md` section 3.1). Before finalizing any of them:

1. **Read the draft as its target reader would** -- a Business Analyst or Designer who has never seen this feature, not a reviewer auditing evidence. Confirm the feature-area narrative is understandable on its own, without needing to resolve an evidence link, a classification tag, or a Gherkin block to follow what the product does. If it isn't, the content is misplaced, not missing -- move it to the Requirements register or Evidence and Traceability section (DESIGN-ANALYSIS-SPEC.md section 4, `DESIGN-ANALYSIS-TEMPLATE.md`); don't delete it.
2. **Confirm no commentary about this document's own revision history appears in its primary content.** A note like "an earlier draft misread this" or "format revised because..." describes the document, not the product, and belongs in a Revision History or Review history section -- never repeated inside the content. This failure mode is easy to reintroduce even while fixing it -- it recurred three separate times across `DA-003`'s revision history, and again in its Journey/Capability/Business Rule record files. Check for it explicitly; do not assume a prior pass already caught it.
3. **Confirm the writing reads as product documentation, not the agent narrating its own process.** Two distinct failure modes, both found on a sweep of this repository's own generated content:
   - **No self-assessment of the analysis's own quality, honesty, or rigor** -- a phrase like "the clearest real example in this registry" or "an honest gap this document surfaces" grades the writing instead of stating the fact. State the fact; let a human reader judge its quality.
   - **No filler intensifiers used out of habit rather than for information** -- `genuinely`, `real` (as an intensifier, not as a meaningful adjective like "real submissions" vs. test data), `actually`, `honest(ly)` are common tells. Before keeping one, check whether removing it changes what the sentence says -- if not, cut it.
4. **Confirm traceability is walkable, not just present.** Every Requirement candidate, Capability, and Business Rule must link upstream to the exact source reference that produced it (EVIDENCE-SPEC.md section 7). Downstream links (Story, Epic, Business PR) are added later by the Business Agent (BUSINESS-AGENT-WORKFLOW.md section 4.4) -- at this stage they correctly read `Pending`.

DESIGN-ANALYSIS-SPEC.md section 7's Quality Checks are the governing checklist for all four; this section states why they are a required step here, not a second definition of them.

### 4.2 Do Not Improve the Design

This agent documents what was designed, not what should have been designed. If the source is incomplete, the gap is information worth surfacing -- record it as a Gap, Assumption, or Decision Required (DESIGN-ANALYSIS-SPEC.md sections 4.10-4.11). Filling it with what an application "normally" does, or with a better idea, is the failure this rule exists to prevent: a reviewer can't tell an invented behavior from a designed one once it's written down as a requirement candidate.

## 5. Output Contract

A completed Design Analysis Agent run produces exactly these artifacts:

| Output | Specified in |
| --- | --- |
| Design Analysis | DESIGN-ANALYSIS-SPEC.md; DESIGN-ANALYSIS-TEMPLATE.md |
| Journey, Capability, and Business Rule records, new or updated, plus their registry rows | ARTIFACT-RELATIONSHIP-MODEL.md §3.1; ARTIFACT-STORAGE-SPEC.md §4.1 |
| Design Analysis review PR | GITHUB-PLATFORM-ADAPTER-SPEC.md §4 (Design Analysis row), §8 (Decision resolution via PR review comment) |

Business Requirements, Epics, Stories, and the Business PR are not outputs of this stage. They belong to the Business Agent, and must not be drafted until this stage's output is approved.

### 5.1 Hand-off to the Business Agent

This stage ends at the Design Analysis review gate (`GATE-003`, FRAMEWORK-CONFIGURATION-SPEC.md section 11): the Design Analysis review PR is approved and merged, and the Design Analysis's own `Status` field reads `Approved`. That approved, merged Design Analysis is the Business Agent's entry condition (BUSINESS-AGENT-WORKFLOW.md section 3).

The hand-off is started manually by default -- the Business Owner asks for Business Requirements to be derived from a named, approved Design Analysis. Automating it (for example, a GitHub Issue opened when an approved Design Analysis merges, the same way design-branch intake already works) is a reasonable later step, not built yet.

## 6. The Design Analysis Agent MUST NOT

The Design Analysis Agent must not:

- draft Business Requirements, Epics, Stories, Acceptance Criteria for Stories, or a Business PR -- those belong to the Business Agent, after this stage is approved
- choose programming languages, frameworks, UI component libraries, APIs, endpoints, payloads, databases, storage services, service boundaries, cloud providers, infrastructure, or deployment architecture
- invent business rules, validation, permissions, error handling, workflow states, notifications, or integrations the source does not show (section 4.2)
- regenerate, rewrite, or silently modify the source Design Handoff Bundle or other source material
- convert an `Assumption`, `Decision Required`, or `Technical Unknown` into a confirmed requirement candidate (EVIDENCE-SPEC.md §6)
- resolve a `Decision Required` item on its own reasoning -- only the Business Owner resolves one, via a PR review comment (GITHUB-PLATFORM-ADAPTER-SPEC.md §8)
- approve or merge its own Design Analysis review PR

If a step in section 4 would require crossing one of these lines to proceed, the agent must stop and record the item as a Decision Required or Technical Unknown instead of resolving it.

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
   Design Analysis Review  (GATE-003, DESIGN-ANALYSIS-REVIEW-SPEC.md §10-13)
        |
        v
   Approved Design Analysis  --> Business Agent (BUSINESS-AGENT-WORKFLOW.md)
```

## 8. Failure and Blocking Conditions

The Design Analysis Agent must stop and record a blocker, rather than proceeding, when:

- source readiness is `Blocked` (PRODUCT-SOURCE-MATERIAL-SPEC.md §9)
- a source file needed for the analysis is missing or unreadable (DESIGN-ANALYSIS-REVIEW-SPEC.md §16)
- the Design Analysis cannot pass its own quality checks (DESIGN-ANALYSIS-SPEC.md §7)
- completing a step would require a decision listed in section 6 above

A blocked run must state the reason, the affected step, and the owner who can unblock it, consistent with the failure-handling pattern already used in [TECHNICAL-HANDOFF.md](TECHNICAL-HANDOFF.md).

### 8.1 Resuming After `Changes Requested`

Whether a `Changes Requested` outcome on the Design Analysis review requires re-running from step 1 depends on the Major/Editorial distinction REQUIREMENTS-VERSIONING-SPEC.md section 9 already defines:

- **Editorial feedback** -- wording, a narrative's phrasing -- may be patched directly and resubmitted, without re-running earlier steps, provided meaning is unchanged.
- **Material feedback** -- a wrong actor, a rule that doesn't apply, anything that changes meaning -- must flow back through whichever step produced it, and every step downstream of that one must be re-run.

Review comments are incorporated with the `resolve-review-decisions` procedure (GITHUB-PLATFORM-ADAPTER-SPEC.md §8).

## 9. One-Page Compliance Checklist

- [ ] Source readiness confirmed before any analysis began (step 1)
- [ ] Every source file and every major screen and flow was reviewed (steps 2-3)
- [ ] The Design Analysis covers screens, flows, actors, capabilities, behaviors, information, existing-vs-new experience, rules, ambiguities, and scope boundary (steps 2-8) before being finalized (step 9)
- [ ] Problem, Goals, and Success Metrics are each grounded in evidence or recorded as a Decision Required (step 9)
- [ ] The registries were checked before any new `JRN-`/`CAP-`/`BRULE-` ID was minted (steps 3, 5, 7)
- [ ] Before finalizing, the Design Analysis and every record file passed the self-review in section 4.1
- [ ] Nothing was added that the source doesn't show (section 4.2)
- [ ] No Business Requirements, Epics, Stories, or Business PR were drafted (section 6)
- [ ] No output contains a technical implementation detail (section 6)
- [ ] The agent has not approved or merged its own Design Analysis review PR

## 10. Revision History

*This table is what and when, not why -- the current rule and its rationale live at the cited section.*

| Date | Section | Change |
| --- | --- | --- |
| 2026-10-05 | all | Created by splitting steps 1-9 out of `BUSINESS-AGENT-WORKFLOW.md` into their own agent and stage, with the Design Analysis review gate (`GATE-003`) now always separate from the Business PR review. Self-review (section 4.1) moved here from `BUSINESS-AGENT-WORKFLOW.md` section 4.3. Section 4.2 and the information-analysis and existing-vs-new-experience coverage in step 6 adopted from a Design Analysis agent prompt Manali supplied. |
