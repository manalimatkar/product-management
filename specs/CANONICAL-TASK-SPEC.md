# Canonical Task and Spike Specification

## 1. Purpose

This specification defines the minimum content and lifecycle of a canonical Task or Spike: the technical decomposition of an approved Story, enriched by the Technical Agent and gated by Architect approval before it may reach a Developer Agent or human developer.

[TECHNICAL-HANDOFF.md](TECHNICAL-HANDOFF.md) describes this flow narratively. This document gives it a structured schema, the same way [DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md](DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md) did for the Design Handoff Bundle and [BUSINESS-PR-SPEC.md](BUSINESS-PR-SPEC.md) did for the Business PR.

## 2. Relationship to Other Artifacts

- [TECHNICAL-HANDOFF.md](TECHNICAL-HANDOFF.md) defines the entry condition, the Architect review gate, and the failure/blocking conditions this document assumes.
- [TECHNICAL-AGENT-WORKFLOW.md](TECHNICAL-AGENT-WORKFLOW.md) orders this document's rules, together with TECHNICAL-HANDOFF.md's, into one end-to-end Technical Agent procedure, and defines the optional Technical Plan referenced by this document's `Technical Plan` field (section 6).
- [AGENT-RESPONSIBILITIES.md](AGENT-RESPONSIBILITIES.md) defines what the Technical Agent may and may not do.
- [BUSINESS-PR-SPEC.md](BUSINESS-PR-SPEC.md) defines the Business PR whose merge is this stage's entry trigger, and the Stage Trace a Task must extend rather than replace.
- Per [PRD.md](../PRD.md) section 7.6, canonical Tasks and Spikes remain GitHub Issues in the business repository. This specification assumes that representation; [GITHUB-PLATFORM-ADAPTER-SPEC.md](GITHUB-PLATFORM-ADAPTER-SPEC.md) confirms it as this repository's chosen adapter (decided 2026-08-31) and defines the exact Issue content, labels, and creation trigger. A different platform adapter remains configurable per [FRAMEWORK-CONFIGURATION-SPEC.md](FRAMEWORK-CONFIGURATION-SPEC.md) section 13 if this repository's needs change. Until a real GitHub setup exists, [ARTIFACT-STORAGE-SPEC.md](ARTIFACT-STORAGE-SPEC.md) section 8 defines a local-file fallback at `<platform-slug>/[<app-slug>/]tasks/<feature-slug>/canonical-task-<feature-slug>-<TASK-id>.md` (and `spike-...` for Spikes) -- see GITHUB-PLATFORM-ADAPTER-SPEC.md section 7 for how a local file transitions to an Issue.

## 3. Entry Condition

A canonical Task or Spike may be created or enriched only when, per [TECHNICAL-HANDOFF.md](TECHNICAL-HANDOFF.md):

1. the Business PR has been merged into the business repository
2. Business Owner approval is recorded on that PR
3. the merged Epic and Stories are available
4. the relevant engineering repository or repositories are identified

A draft, open, rejected, or unapproved Business PR is not a valid entry condition. The Technical Agent must not begin decomposition against unmerged or unapproved scope.

## 4. The Technical Decomposition Transformation

Continuing the controlled transformation from [BUSINESS-PR-SPEC.md](BUSINESS-PR-SPEC.md) section 3, the technical stage asks its own narrow set of questions -- never the business questions that came before it, and never implementation code:

```text
APPROVED, MERGED BUSINESS PR (Epic + Stories + Acceptance Criteria)
        |
        v
   Which engineering repository or repositories are affected?
   What is the implementation approach, at a guidance level?
   What dependencies, sequencing, and architecture impacts exist?
   What must still be investigated before this can be estimated?
        |
        v
CANONICAL TASK / SPIKE (technical detail enriched)
        |
        v
   Is the decomposition feasible and consistent with the
   engineering repositories?
   ARCHITECT REVIEW
        |
        v
TECHNICAL READY
        |
        v
   DEVELOPER AGENT OR HUMAN DEVELOPER
```

A Task records an implementation *approach* and *guidance* -- enough for a Developer Agent to begin -- not the code itself. Writing code is the Developer Agent's responsibility, not the Technical Agent's, per [AGENT-RESPONSIBILITIES.md](AGENT-RESPONSIBILITIES.md).

## 5. Task vs. Spike

- **Task**: implementation work whose approach is understood well enough to decompose, sequence, and hand to a Developer Agent once Architect-approved.
- **Spike**: an investigation required before a Task can be responsibly estimated or decomposed. A Spike typically resolves a `Technical Unknown` flagged during Design Analysis (see [DESIGN-ANALYSIS-SPEC.md](DESIGN-ANALYSIS-SPEC.md) section 5) or a technical uncertainty the Technical Agent discovers while inspecting the engineering repositories.

A Task that depends on an unresolved Spike must record that dependency and must not be marked Technical Ready until the Spike is resolved and its findings are folded back into the Task (section 9).

## 6. Required Task Fields

| Field | Requirement |
| --- | --- |
| Task ID | Stable identifier, e.g. `TASK-<number>` |
| Title | Short, outcome-oriented |
| Business Repository | Reference to this repository |
| Business PR | Reference to the approved, merged Business PR |
| Epic | Epic reference |
| Source Story | Story ID this Task decomposes (immutable reference) |
| Story Version | Exact Story/Requirements version this Task was created against |
| Acceptance Criteria | Preserved from the Story, unchanged in meaning |
| Target Platform | The platform this Task's Story belongs to (`platform-slug`, ARTIFACT-STORAGE-SPEC.md section 4) |
| Target Application | The application within that platform this Task affects (`app-slug`) -- populated only when the platform has an app-level subdivision; blank/not-applicable otherwise |
| Target Repository | The specific engineering repository this Task targets |
| Implementation Approach | Guidance-level description of how the Story will be realized |
| Technical Plan | Reference to a Technical Plan document, only when one exists (TECHNICAL-AGENT-WORKFLOW.md section 4.1) -- optional; most Tasks have none, and use the fields on this table instead |
| Technical Findings | What the Technical Agent found in the engineering repository relevant to this Task |
| Dependencies and Sequencing | Other Tasks, Spikes, or external work this depends on or blocks |
| Architecture References | Links to relevant architecture documentation in the engineering repository |
| Testing and Quality Considerations | What must be verified, at a guidance level |
| Unresolved Technical Risks | Risks not yet mitigated or decided |
| Required Spikes | Spike IDs that must resolve before this Task can be estimated |
| Constraints | Technical constraints the Developer Agent must respect |
| Created By | Technical Agent run or author |
| Created At | Timestamp |
| Status | `Draft` / `In Review` / `Rework Required` |
| Technical Readiness | `Not Ready` / `Ready for Architect Review` / `Technical Ready` / `Blocked` |
| Architect | Named reviewer or `Pending` |
| Approval Reference | Attributable Architect approval event or `Pending` |

`Status` is the Technical Agent's own drafting lifecycle. `Technical Readiness` is a separate field, set only through the Architect Review Gate (section 9) -- the same status-versus-readiness split used for the Design Handoff Bundle in [DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md](DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md) section 7. A Task with `Status: Draft` can never simultaneously hold `Technical Readiness: Technical Ready`.

## 7. Required Spike Fields

| Field | Requirement |
| --- | --- |
| Spike ID | Stable identifier, e.g. `SPIKE-<number>` |
| Title | Short description of the unknown to resolve |
| Originates From | `Technical Unknown` ID from Design Analysis, or a Technical Agent-identified uncertainty |
| Blocks | Task IDs that cannot reach Technical Readiness until this resolves |
| Investigation Scope | What will be examined, and where |
| Expected Output | What the Spike must produce (a decision, a recommendation, a feasibility answer) |
| Owner | Person or agent responsible for the investigation |
| Status | `Open` / `In Progress` / `Resolved` / `Abandoned` |
| Findings | Recorded once resolved |
| Resolved At | Timestamp |

A Spike's findings become Technical Findings on the Task(s) it blocks (section 6); the Spike itself is not implementation work and does not produce an implementation PR.

## 8. Boundary Rules

Per [AGENT-RESPONSIBILITIES.md](AGENT-RESPONSIBILITIES.md), the Technical Agent may enrich Tasks and Spikes with the fields in sections 6-7, but must not:

- analyze or act on unapproved or unmerged business scope
- alter Business Owner approval or the approved Epic/Story content
- merge the Business PR
- treat its own technical detail as approved
- mark a Task `Technical Ready` before Architect approval
- create duplicate Tasks in engineering repositories
- implement code as a substitute for Developer Agent responsibility

### Scope Change During Technical Analysis

If technical analysis reveals that the approved business scope cannot be implemented as written, is significantly more expensive than assumed, or requires a materially different user-facing behavior, the Technical Agent must not silently narrow, expand, or reinterpret the Story to fit. It must:

1. Record the conflict as an Unresolved Technical Risk or a new Decision Required item on the Task.
2. Identify the affected Story and Business Requirement.
3. Escalate back through the business-repository process (a new Business PR revision or a linked follow-up) rather than resolving it unilaterally.
4. Leave the Task blocked or marked with the conflict visible until the business-side decision is made.

This mirrors [TECHNICAL-HANDOFF.md](TECHNICAL-HANDOFF.md)'s Engineering Repository Boundary: "Any material scope change must be sent back through the business-repository process."

## 9. Architect Review Gate

Consistent with the outcome vocabulary already used in [DESIGN-ANALYSIS-REVIEW-SPEC.md](DESIGN-ANALYSIS-REVIEW-SPEC.md) section 11 and [BUSINESS-PR-SPEC.md](BUSINESS-PR-SPEC.md) section 10:

| Outcome | Meaning | Required Action |
| --- | --- | --- |
| `Approved` | Technical decomposition is feasible and consistent with the engineering repositories | Set Technical Readiness to `Technical Ready`; record Architect, date, and exact Task version |
| `Changes Requested` | Decomposition needs revision | Record findings; Technical Agent revises and resubmits |
| `Rejected` | Decomposition is not viable as proposed | Record rationale; Task returns to `Draft` or is closed |
| `Blocked` | A required Spike, dependency, or business decision is unresolved | Record blocker, owner, and condition for resuming |

### Approval Recording

| Field | Value |
| --- | --- |
| Task ID | `<ID>` |
| Task Version | `<version>` |
| Outcome | Approved / Changes Requested / Rejected / Blocked |
| Architect | `<identity>` |
| Decision Date | `<timestamp>` |
| Conditions | `<conditions or None>` |
| Approval Evidence | `<link or record>` |

Architect approval applies to the exact reviewed Task version. A later material change to the Task's technical detail invalidates prior approval and requires re-review, mirroring [REQUIREMENTS-VERSIONING-SPEC.md](REQUIREMENTS-VERSIONING-SPEC.md) section 9's approval-validity rule.

## 10. One Story, Multiple Tasks

A single Story may produce multiple Tasks targeting different applications or engineering repositories. Each Task:

- retains its own `Source Story` and `Story Version` reference back to the same Story
- is independently enriched, reviewed, and approved by the Architect
- does not require the other Tasks from the same Story to reach Technical Readiness at the same time, unless a recorded dependency (section 6) says otherwise

## 11. No Duplicate Tasks in Engineering Repositories

Canonical Tasks and Spikes remain in the business repository. They are not copied into engineering repositories as a second source of truth. An implementation PR in the engineering repository references the canonical Task ID; it does not restate the Task's business content. See [TECHNICAL-HANDOFF.md](TECHNICAL-HANDOFF.md) "Canonical Tasks" and "Engineering Repository Boundary."

## 12. Change Management

If the Story or Business Requirement a Task was created against changes after the Task exists:

1. Identify every Task referencing the affected Story or Requirement ID.
2. Determine whether the change is compatible (per [REQUIREMENTS-VERSIONING-SPEC.md](REQUIREMENTS-VERSIONING-SPEC.md) section 6's Editorial/Minor/Major classification) with the Task's current technical detail.
3. For a Major change, mark the affected Task `Technical Readiness: Blocked` and require re-review, even if it was previously `Technical Ready`.
4. Preserve the previous Task version for audit.
5. Do not allow a Developer Agent to begin or continue work on a Task whose upstream Story version has been superseded without re-review.

## 13. Reusable Template

The concrete Task and Spike issue templates are defined in [CANONICAL-TASK-TEMPLATE.md](../templates/CANONICAL-TASK-TEMPLATE.md).

## 14. Open Decisions

- Should Technical Readiness re-review be triggered automatically on any upstream Story change, or only on changes classified Major?
- What minimum Technical Findings are required before a Task is eligible for Architect review, versus acceptable to leave as an open risk?
- How are Spikes time-boxed, and what happens to Tasks blocked on a Spike that stalls?
- Should multiple Tasks from one Story require a combined Architect review, or may each be reviewed independently as this document currently allows?
- What machine-checkable rule can flag a Task whose Implementation Approach has silently altered Story-level user-facing behavior (a Scope Change per section 8) rather than just its technical realization?
