# Technical Agent Workflow

## 1. Purpose

This document is the single, ordered, end-to-end contract for one Technical Agent run: from a merged, approved Business PR to Architect-approved, Technically Ready canonical Tasks and Spikes. It answers the TODO left open in [PRD.md](../PRD.md) section 13 and [IMPLEMENTATION-PLAN.md](../IMPLEMENTATION-PLAN.md): "What minimum content must a Technical Plan contain before Architect review?" / "exact Technical Plan format." Closing that question surfaced two smaller ones already tracked alongside it -- the reference format an Implementation PR uses to link back to a canonical Task (section 6.1), and change management when a Story changes after canonical Tasks already exist (section 8.1) -- both resolved here in the same pass, per CLAUDE.md open item 4.

It is a synthesis document, not a new set of rules, mirroring [BUSINESS-AGENT-WORKFLOW.md](BUSINESS-AGENT-WORKFLOW.md)'s shape for the technical side of the pipeline. Every step below is already governed in detail by an existing specification; this document orders those steps into one procedure and states, in one place, the input contract, the output contract, and what the Technical Agent must never do. Where this document and a cited section disagree, the cited section is authoritative -- this document must be corrected to match it, not the reverse.

## 2. Relationship to Other Artifacts

- [TECHNICAL-HANDOFF.md](TECHNICAL-HANDOFF.md) governs the entry condition, the Architect Review Gate, and the failure/blocking conditions this document assumes and orders into one procedure.
- [CANONICAL-TASK-SPEC.md](CANONICAL-TASK-SPEC.md) governs the Task/Spike schema, the Task-vs-Spike distinction, the structured Architect Review Gate outcome table, and the Change Management rule (section 12) this document's step ordering follows rather than restates.
- [AGENT-RESPONSIBILITIES.md](AGENT-RESPONSIBILITIES.md) governs the Technical Agent's authority boundary (May / May not).
- [BUSINESS-PR-SPEC.md](BUSINESS-PR-SPEC.md) governs the input this stage begins from -- the approved, merged Business PR -- and the Stage Trace this stage must extend one hop further, never replace.
- [GITHUB-PLATFORM-ADAPTER-SPEC.md](GITHUB-PLATFORM-ADAPTER-SPEC.md) governs the Task/Spike GitHub Issue representation; section 6.1 below concretizes its `Traces to:` line requirement for the one reference direction it had not yet made concrete.
- [ARTIFACT-RELATIONSHIP-MODEL.md](ARTIFACT-RELATIONSHIP-MODEL.md) governs the Story:Task (1:N), Task:Spike (N:N), and Task:Implementation-PR (1:N) cardinality this document assumes throughout.

## 3. Input Contract

The Technical Agent does not begin from an arbitrary state of the business repository. It begins only once [TECHNICAL-HANDOFF.md](TECHNICAL-HANDOFF.md)'s Entry Condition is verified by a GitHub Action:

```text
Business PR (Approved, Merged)
  (BUSINESS-PR-SPEC.md sections 10-11)
        |
        v
Merged Epic + Stories
        |
        v
Canonical Task(s) / Spike(s)
```

Entry condition -- all four must hold:

1. the Business PR has been merged into the business repository
2. the Business Owner approval is recorded on that PR
3. the merged Epic and Stories are available
4. the handoff identifies the relevant engineering repository or repositories

A draft, open, rejected, or unapproved Business PR is not a valid entry condition. The Technical Agent must not begin decomposition against unmerged or unapproved scope.

## 4. Processing

Steps 1-8 run in order for each Story reaching this stage. Unlike the Business Agent's single Business PR review point, this stage is not one gate for the whole PR -- per [CANONICAL-TASK-SPEC.md](CANONICAL-TASK-SPEC.md) section 10, each Task a Story produces is independently enriched, reviewed, and approved, and does not wait on sibling Tasks unless a recorded dependency says otherwise (section 4.2 below).

| # | Step | Governed by |
| --- | --- | --- |
| 1 | Verify entry condition | TECHNICAL-HANDOFF.md "Entry Condition" |
| 2 | Read merged business artifacts (Epic, Stories, requirements, acceptance criteria, recorded decisions, assumptions, dependencies) | TECHNICAL-HANDOFF.md "Technical Agent Analysis" |
| 3 | Inspect the relevant engineering repository or repositories (code, documentation, existing architecture, implementation constraints) | TECHNICAL-HANDOFF.md "Technical Agent Analysis" |
| 4 | Identify affected engineering repositories per Story | CANONICAL-TASK-SPEC.md §4; a Story may produce multiple Tasks targeting different applications or repositories (§10) |
| 5 | Determine implementation approach, at a guidance level | CANONICAL-TASK-SPEC.md §4 -- approach and guidance only, never the code itself (§4, citing AGENT-RESPONSIBILITIES.md) |
| 6 | Identify dependencies, sequencing, and architecture impacts | CANONICAL-TASK-SPEC.md §6 required fields |
| 7 | Identify required Spikes for any unresolved Technical Unknown | CANONICAL-TASK-SPEC.md §5, §7 -- originates from a Design Analysis `Technical Unknown` (BUSINESS-AGENT-WORKFLOW.md step 8) or a Technical Agent-discovered uncertainty |
| 8 | Enrich the canonical Task(s) and Spike(s) with the fields required by CANONICAL-TASK-SPEC.md sections 6-7 | CANONICAL-TASK-SPEC.md §6-7 |
| 9 | Submit for Architect Review | CANONICAL-TASK-SPEC.md §9 |

### 4.1 Technical Plan: Optional, and Its Format When Used

**Resolved 2026-09-01** (see section 10). [TECHNICAL-HANDOFF.md](TECHNICAL-HANDOFF.md) already establishes that "the Task is the handoff contract between agents. A separate Technical Plan document is optional and should be used only when the scope requires more detail than the canonical Tasks can contain." This section makes that concrete rather than leaving "more detail than the Tasks can contain" undefined.

**Default: no separate Technical Plan.** The Task and Spike fields in [CANONICAL-TASK-SPEC.md](CANONICAL-TASK-SPEC.md) sections 6-7 are the default, sufficient handoff contract for the large majority of Tasks. Where no separate plan is needed, the Architect approves the technical detail directly on the canonical Tasks and Spikes, per TECHNICAL-HANDOFF.md's Architect Review Gate.

**When used:** only when technical detail spans multiple Tasks and would otherwise have to be duplicated on each one -- a shared architecture decision, a cross-Task sequencing rationale, or investigation context feeding more than one Task from the same Story or Epic. A Technical Plan is a Markdown document, stored per [ARTIFACT-STORAGE-SPEC.md](ARTIFACT-STORAGE-SPEC.md)'s convention:

```text
tasks/<platform-slug>/[<app-slug>/]<feature-slug>/technical-plan-<feature-slug>-<TP-id>.md
```

using `TP-<number>` as its canonical ID -- extending [ARTIFACT-RELATIONSHIP-MODEL.md](ARTIFACT-RELATIONSHIP-MODEL.md) section 3's inventory the same way `ANALYSIS-<number>` was proposed there for Design Analysis. Every Task it covers references it via a `Technical Plan` field (added to CANONICAL-TASK-SPEC.md section 6, additive -- it does not replace or change the meaning of any existing field). A Technical Plan carries its own Architect approval record, identical in shape to CANONICAL-TASK-SPEC.md section 9's Approval Recording table, since it is reviewed under the same Architect Review Gate as the Tasks it covers, not a separate gate of its own. This document does not prescribe required internal sections for a Technical Plan the way DESIGN-ANALYSIS-SPEC.md does for a Design Analysis -- per TECHNICAL-HANDOFF.md, "any optional Technical Plan is a proposal until approved by an Architect," and its content is whatever the specific initiative needs.

### 4.2 Spike-Blocked Tasks Progress Independently

Per [CANONICAL-TASK-SPEC.md](CANONICAL-TASK-SPEC.md) section 10, multiple Tasks from one Story reach Technical Readiness independently -- this stage's own kanban shape, more visibly than the Business Agent's single-PR gate (FRAMEWORK-CONFIGURATION-SPEC.md section 8's `STAGE-005`/`STAGE-006` columns). Each Task or Spike moves through Draft -> In Review -> Architect Review -> Technical Ready at whatever pace its own investigation takes. A Task with a Required Spike (section 6, `Required Spikes` field) sits blocked in that column until the Spike resolves and its findings are folded back into the Task (CANONICAL-TASK-SPEC.md §5, §7, §11) -- it does not hold up unrelated Tasks from the same Story or Epic.

## 5. Output Contract

A completed Technical Agent run produces exactly these artifacts, each already specified elsewhere:

| Output | Specified in |
| --- | --- |
| Canonical Task(s) | CANONICAL-TASK-SPEC.md §6 |
| Spike(s), where required | CANONICAL-TASK-SPEC.md §7 |
| Technical Findings | CANONICAL-TASK-SPEC.md §6 (`Technical Findings` field) |
| Dependencies and Sequencing | CANONICAL-TASK-SPEC.md §6 (`Dependencies and Sequencing` field) |
| Optional Technical Plan, where used | section 4.1 above |
| Unresolved Technical Risks | CANONICAL-TASK-SPEC.md §6 (`Unresolved Technical Risks` field) |
| Architect Review outcome | CANONICAL-TASK-SPEC.md §9 (`Technical Ready` / `Changes Requested` / `Rejected` / `Blocked`) |

A Task or Spike missing any required field from CANONICAL-TASK-SPEC.md sections 6-7 is not eligible for Architect Review.

## 6. The Technical Agent MUST NOT

This consolidates [CANONICAL-TASK-SPEC.md](CANONICAL-TASK-SPEC.md) section 8's boundary rules and [AGENT-RESPONSIBILITIES.md](AGENT-RESPONSIBILITIES.md)'s "Technical Agent / May not" list into one checklist. The Technical Agent must not:

- analyze or act on unapproved or unmerged business scope
- alter Business Owner approval, or the approved Epic/Story content itself
- merge the Business PR
- treat its own technical detail as approved
- mark a Task or Spike `Technical Ready` before Architect approval
- create duplicate Tasks in engineering repositories
- implement code, or substitute its own output for Developer Agent responsibility
- silently narrow, expand, or reinterpret a Story when technical analysis reveals it cannot be built as written -- it must escalate instead, per CANONICAL-TASK-SPEC.md section 8's "Scope Change During Technical Analysis"

If a step in section 4 would require crossing one of these lines to proceed, the Technical Agent must stop and record an Unresolved Technical Risk or a new Decision Required item instead of resolving it unilaterally.

### 6.1 Engineering PR Reference Format (`Traces to:`)

**Resolved 2026-09-01** (see section 10). [GITHUB-PLATFORM-ADAPTER-SPEC.md](GITHUB-PLATFORM-ADAPTER-SPEC.md) section 3 already requires that "every Issue and PR body must include a `Traces to:` line citing the artifact IDs it implements or is implemented by, using the same evidence-chain vocabulary EVIDENCE-SPEC.md already defines." That rule was stated generically; this is its concrete form for the one reference direction not yet made concrete -- an Implementation PR, living in an engineering repository, referencing a canonical Task that lives in this business repository:

```text
Traces to: TASK-<id> (business repository: <business-repo-name>)
```

placed in the Implementation PR description, satisfying [ARTIFACT-RELATIONSHIP-MODEL.md](ARTIFACT-RELATIONSHIP-MODEL.md) section 4's resolved cardinality: "an Implementation PR must reference exactly one canonical Task." Where the Task exists as a real GitHub Issue (GITHUB-PLATFORM-ADAPTER-SPEC.md section 4) rather than the local-file fallback, the reference additionally becomes a cross-repository Issue link where the platform supports it (e.g. `owner/business-repo#<issue-number>`) -- but the `TASK-<id>` form is always present regardless, since files stay canonical (GITHUB-PLATFORM-ADAPTER-SPEC.md section 3) and an Issue number is a secondary cross-reference, never the primary identifier.

## 7. End-to-End Diagram

```text
Business PR (Approved, Merged)
        |
        v
   Read merged business artifacts + inspect engineering repositories  (steps 1-3)
        |
        v
   Canonical Task(s) / Spike(s) enriched  (steps 4-8)
        |
        v
   Optional Technical Plan, where scope needs it  (section 4.1)
        |
        v
   Architect Review  (CANONICAL-TASK-SPEC.md §9)
        |
        v
   Technical Ready
        |
        v
   Developer Agent  (TECHNICAL-HANDOFF.md; out of scope for this document)
```

## 8. Failure and Blocking Conditions

The Technical Agent must stop and record a blocker, rather than proceeding, when:

- Business Owner approval cannot be verified
- the Business PR is not merged
- required business artifacts are missing
- an optional Technical Plan (section 4.1), where used, is incomplete or not approved
- target repository information is unavailable
- required traceability links cannot be created
- a required Spike, dependency, or business decision is unresolved (CANONICAL-TASK-SPEC.md §9's `Blocked` outcome)
- technical analysis reveals the approved scope cannot be built as written (CANONICAL-TASK-SPEC.md §8's Scope Change -- must escalate, never silently resolve)

A blocked run must state the reason, the affected Task or Spike, and the owner who can unblock it, consistent with [TECHNICAL-HANDOFF.md](TECHNICAL-HANDOFF.md)'s own Failure and Blocking Conditions and the same pattern [BUSINESS-AGENT-WORKFLOW.md](BUSINESS-AGENT-WORKFLOW.md) section 8 uses.

### 8.1 Change Management When a Story Changes After Tasks Exist

This is already fully defined, not newly resolved here -- [CANONICAL-TASK-SPEC.md](CANONICAL-TASK-SPEC.md) section 12 ("Change Management") already covers exactly this case: identify every Task referencing the affected Story or Requirement ID; classify the change Editorial/Minor/Major per REQUIREMENTS-VERSIONING-SPEC.md section 6; a Major change marks the affected Task `Technical Readiness: Blocked` and requires re-review, even if it was previously `Technical Ready`; the previous Task version is preserved for audit; and a Developer Agent must not begin or continue work on a Task whose upstream Story version has been superseded without re-review. PRD.md section 13 and IMPLEMENTATION-PLAN.md tracked this as still open because neither document's open-item list was cross-referencing CANONICAL-TASK-SPEC.md section 12 -- restated here for completeness, not reinvented (see section 10).

## 9. One-Page Compliance Checklist

- [ ] Entry condition verified before any Task or Spike work began (section 3)
- [ ] Every Task and Spike traces back to its Source Story and Story Version, unchanged (CANONICAL-TASK-SPEC.md §6-7)
- [ ] The relevant engineering repository was inspected before an implementation approach was proposed (steps 2-3)
- [ ] A Task depending on an unresolved Spike is not marked Technical Ready (section 4.2)
- [ ] An optional Technical Plan, where used, follows section 4.1's format and carries its own Architect approval record
- [ ] No Task, Spike, or Technical Plan record contains actual code
- [ ] A scope conflict discovered during analysis was escalated, never silently resolved (section 6; CANONICAL-TASK-SPEC.md §8)
- [ ] Technical Readiness was set only after Architect approval, never by the Technical Agent itself
- [ ] Every Implementation PR's `Traces to:` line follows section 6.1's format
- [ ] A Major change to the upstream Story after a Task exists blocked that Task, per CANONICAL-TASK-SPEC.md §12 (section 8.1)

## 10. Open Decisions

- ~~What minimum content must a Technical Plan contain before Architect review?~~ Resolved 2026-09-01 -- see section 4.1. Default is none (Task/Spike fields suffice); when scope genuinely spans multiple Tasks, a Markdown document per ARTIFACT-STORAGE-SPEC.md's convention, reviewed under the same Architect Review Gate as the Tasks it covers.
- ~~What reference format do Implementation PRs use to link back to canonical Tasks?~~ Resolved 2026-09-01 -- see section 6.1. `Traces to: TASK-<id> (business repository: <name>)`, extending GITHUB-PLATFORM-ADAPTER-SPEC.md section 3's existing rule to the one reference direction it had not yet made concrete.
- ~~How is change management handled when a design or approved Story changes after canonical Tasks already exist downstream?~~ Already resolved, not newly so -- see section 8.1. CANONICAL-TASK-SPEC.md section 12 already defines this in full; PRD.md and IMPLEMENTATION-PLAN.md's open-item tracking simply wasn't cross-referencing it.
