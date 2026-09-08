# Business PR Specification

## 1. Purpose

This specification defines the minimum content of a Business PR: the reviewable package the Business Owner approves before the Technical Agent may begin analysis.

A Business PR must never be a single-shot jump from a design or source document straight to Epics and Stories. It is the review point for a **controlled transformation** that passes through every stage below, in order, with each stage's guiding questions answered and evidenced. The PR's job is to make that transformation inspectable, not just to present its final output.

## 2. Relationship to Other Artifacts

- [DESIGN-ANALYSIS-SPEC.md](DESIGN-ANALYSIS-SPEC.md) and [DESIGN-ANALYSIS-REVIEW-SPEC.md](DESIGN-ANALYSIS-REVIEW-SPEC.md) define how source material becomes an approved Design Analysis -- the first controlled transition.
- [BUSINESS-REQUIREMENTS-SPEC.md](BUSINESS-REQUIREMENTS-SPEC.md) defines how an approved analysis becomes Business Requirements -- the second controlled transition.
- [REQUIREMENTS-VERSIONING-SPEC.md](REQUIREMENTS-VERSIONING-SPEC.md) governs how those requirements are identified and versioned.
- [BUSINESS-REPOSITORY-WORKFLOW.md](BUSINESS-REPOSITORY-WORKFLOW.md) and [AGENT-RESPONSIBILITIES.md](AGENT-RESPONSIBILITIES.md) define the Business Owner gate this PR exists to satisfy, and what the Business Agent may and may not do.
- This document adds the missing piece: the third controlled transition (Business Requirements to Epic and Stories), and the packaging contract that proves all three transitions actually happened before a human is asked to approve anything.

## 3. The Controlled Transformation

A Business PR is not "read a design, write some stories." Each artifact in the chain answers a different, narrower question than the one before it, and each stage's output is the *only* permitted input to the next:

```text
SOURCE MATERIAL (e.g. Design Handoff Bundle)
        |
        v
   What does the user see?
   What can the user do?
   What behavior is implied?
   What business capability does this represent?
        |
        v
DESIGN ANALYSIS
        |
        v
   What does the product need to do?
   What rules exist?
   What decisions are explicit, and which are still required?
   What is ambiguous?
        |
        v
BUSINESS REQUIREMENTS
        |
        v
   What must the product accomplish, observably, for whom?
        |
        v
EPIC + STORIES
        |
        v
   What independently valuable behavior should be delivered,
   without yet deciding how it will be built?
        |
        v
BUSINESS PR
```

No stage may be skipped, and no stage may answer a question that belongs to a later stage. In particular, no stage in this chain may answer "how will this be built" -- that question belongs entirely to the Technical Agent, after this PR is approved and merged (see [TECHNICAL-HANDOFF.md](TECHNICAL-HANDOFF.md)).

## 4. Anti-Pattern: The Technical Jump

The failure this specification exists to prevent:

> "The screen has a button" -> "Create Angular component X and call API Y."

That is a jump from a raw design observation directly to a technical implementation decision, skipping Design Analysis, Business Requirements, and Epic/Stories entirely. [DESIGN-ANALYSIS-SPEC.md](DESIGN-ANALYSIS-SPEC.md) section 6 and [BUSINESS-REQUIREMENTS-SPEC.md](BUSINESS-REQUIREMENTS-SPEC.md) section 3 already forbid the Business Agent from making this jump during analysis and requirements drafting. This document exists because forbidding it during drafting is not enough -- a Business Owner reviewing only a finished Story has no way to see whether the jump happened upstream. The Business PR must therefore expose the trace described in section 6, not just the final Stories, so the jump is visible (and rejectable) at review time even if it slipped past an earlier stage.

The correct chain for the same observation:

| Stage | Answer |
| --- | --- |
| Design Analysis | The design shows a button labeled "Remove" on each cart item (Explicit); clicking it is strongly implied to remove that item from the cart. |
| Business Requirements | BR-004: The product must allow the user to remove an item from their cart, with confirmation before the removal takes effect. |
| Epic/Story | STORY-004: As a shopper, I can remove an item I no longer want from my cart, so my cart reflects what I intend to buy. |
| Technical Agent (later, after this PR is merged) | Decides the component, API, and implementation approach. Not part of this PR. |

## 5. Required Business PR Metadata

| Field | Requirement |
| --- | --- |
| Business PR ID | Stable identifier, e.g. `BPR-<number>` |
| Feature or Initiative | Product area covered |
| Source Material | Reference and version (e.g. Design Handoff Bundle ID and version) |
| Design Analysis | Artifact reference and approved version |
| Business Requirements | Requirements Set ID and approved Requirements Version |
| Epic | Epic reference |
| Stories | Story references included in this PR |
| Created By | Business Agent run or author |
| Created At | Timestamp |
| Status | `Draft` / `In Review` / `Changes Requested` / `Approved` / `Rejected` |
| Business Owner | Named approver or `Pending` |
| Approval Reference | Attributable approval event or `Pending` |

This section is the structural enforcement point for the evidence rule defined in [EVIDENCE-SPEC.md](EVIDENCE-SPEC.md).

### Storage

This artifact is stored at `<platform-slug>/[<app-slug>/]business-prs/<feature-slug>/business-pr-<feature-slug>-<BPR-id>.md`, per [ARTIFACT-STORAGE-SPEC.md](ARTIFACT-STORAGE-SPEC.md), until this repository has a real GitHub setup. Once it does, per [GITHUB-PLATFORM-ADAPTER-SPEC.md](GITHUB-PLATFORM-ADAPTER-SPEC.md) section 4, the Business PR becomes an actual GitHub Pull Request -- its diff is the changed Design Analysis/Business Requirements files, and this template's content becomes the PR description in full.

## 6. Required Stage Trace

Every Business PR must include a Stage Trace: a per-Story mapping proving the full chain exists with no gap and no skipped stage.

| Story | Business Requirement(s) | Design Analysis Evidence | Source Reference | Classification |
| --- | --- | --- | --- | --- |
| `STORY-004` | `BR-004` | Capability: Cart Management; Observation: "Remove" control on `cart-full` screen | `checkout/design/cart-optimization/v1.0/screens/screen-cart-full-cart-optimization.md` | Explicit / Strongly Implied |

Rules for the Stage Trace:

- Every row must resolve back to a Business Requirement ID. A Story with no traceable requirement fails the PR quality gate (section 9).
- Every Business Requirement referenced must resolve back to Design Analysis evidence, or be explicitly marked `Human Provided` with its human source recorded (per [BUSINESS-REQUIREMENTS-SPEC.md](BUSINESS-REQUIREMENTS-SPEC.md) section 6). A requirement with neither is not eligible for inclusion.
- A row may not contain a technical detail (framework, component name, API, endpoint, schema) anywhere in its cells. Presence of one is a Stage Trace violation, not a stylistic note -- reject or revise before review.
- The Stage Trace is what a Business Owner actually reviews to confirm the transformation was controlled. Reviewing only the Story text is not sufficient evidence of approval.

## 7. Epic and Story Decomposition

Business Requirements answer *what the product must accomplish*. Epic and Stories answer a narrower question that has no dedicated artifact spec elsewhere in this repository: **what independently valuable behavior should be delivered?**

A Story drafted from an approved Business Requirement must satisfy all of the following before it may appear in a Business PR:

- **Independently valuable**: it describes a business or user outcome that stands on its own, not a technical component, layer, or implementation step.
- **Observable**: its acceptance criteria describe behavior a Business Owner can recognize as done, in business language, per [BUSINESS-REQUIREMENTS-SPEC.md](BUSINESS-REQUIREMENTS-SPEC.md) section 7.
- **Traceable**: it maps to one or more approved Business Requirement IDs, and through them to Design Analysis evidence or a recorded human source (section 6).
- **Free of technical decomposition**: it must not slice work along technical boundaries ("build the modal," "wire up the endpoint"). If a requirement seems to need more than one Story, split it along business outcome or user-visible behavior, not along implementation layers.
- **Scoped to one approval decision**: a Business Owner must be able to approve or reject it as a coherent unit without needing to approve an unrelated behavior bundled into the same Story.

An Epic groups Stories that share one coherent business outcome. It inherits the same rule: an Epic boundary follows the business capability it represents, not an application, service, or repository boundary -- those are Technical Agent concerns (see [DESIGN-ANALYSIS-SPEC.md](DESIGN-ANALYSIS-SPEC.md) section 6 for the full list of decisions that stay out of business-side artifacts).

## 8. Required Business PR Content

A complete Business PR must contain, or link to:

1. the metadata in section 5
2. a summary of the business problem and desired outcome (from Business Requirements section 2)
3. the Epic and its Stories, each with acceptance criteria
4. the Stage Trace (section 6) covering every Story
5. assumptions and Decisions Required carried forward from the Design Analysis and Business Requirements (unresolved items must remain visible, not silently dropped)
6. business rules and dependencies relevant to the included scope
7. explicit exclusions -- what this PR intentionally does not cover
8. the affected engineering repository or repositories, if already known at this stage (identification only -- not implementation guidance)
9. a request for a specific review outcome (section 10)

## 9. Quality Gate Before Business Owner Review

A Business PR is ready for review only when:

- the exact Design Handoff Bundle (or other source) version, Design Analysis version, and Requirements Version are all recorded and consistent with each other
- every Story in the PR has a complete, gap-free Stage Trace (section 6)
- no cell in the Stage Trace, requirement, or Story contains a technical implementation detail
- every unresolved Decision Required and Assumption from the upstream artifacts is still visible, not resolved by the Business Agent inventing an answer
- acceptance criteria are observable and testable in business language
- scope and exclusions are explicit
- the PR identifies itself as generated content, distinguishable from human approval, per [AGENT-RESPONSIBILITIES.md](AGENT-RESPONSIBILITIES.md)

The Business Agent may not approve or merge its own Business PR, and may not treat this checklist as satisfied on its own authority -- see [AGENT-RESPONSIBILITIES.md](AGENT-RESPONSIBILITIES.md).

## 10. Business Owner Review Outcomes

Consistent with the outcome vocabulary in [DESIGN-ANALYSIS-REVIEW-SPEC.md](DESIGN-ANALYSIS-REVIEW-SPEC.md) section 11:

| Outcome | Meaning | Required Action |
| --- | --- | --- |
| `Approved` | Business scope is authorized for technical handoff once merged | Record approver, date, and exact PR revision |
| `Changes Requested` | Scope needs revision before it can be approved | Record findings; Business Agent revises and resubmits |
| `Rejected` | Scope is not authorized | Record rationale; PR does not proceed |
| `Blocked` | A required decision, source, or authority is unavailable | Record blocker, owner, and condition for resuming |

Approval applies to the exact reviewed PR revision, not to a later silently-changed version, per [REQUIREMENTS-VERSIONING-SPEC.md](REQUIREMENTS-VERSIONING-SPEC.md) section 9.

## 11. Merge as Handoff Trigger

Merge of an approved Business PR is the explicit boundary between business planning and technical analysis. This is defined in [BUSINESS-REPOSITORY-WORKFLOW.md](BUSINESS-REPOSITORY-WORKFLOW.md) ("Merge as the Handoff Trigger") and is not redefined here; this specification governs only what the PR must contain before that point.

## 12. Reusable Template

The concrete PR description format is defined in [BUSINESS-PR-TEMPLATE.md](../templates/BUSINESS-PR-TEMPLATE.md).

## 13. Open Decisions

- Should the Stage Trace be a required PR section, or a machine-generated check run against the PR's referenced artifacts?
- What automated validation can catch a technical-detail leak in the Stage Trace before human review (a keyword/pattern check against DESIGN-ANALYSIS-SPEC.md section 6's forbidden categories)?
- Can Design Analysis approval and Business Requirements approval be combined into this single PR review, or must they remain separate review packages before the PR is opened (see DESIGN-ANALYSIS-REVIEW-SPEC.md section 17)?
- How many Stories, or how much scope, may one Business PR carry before it should be split?
- Who owns resolving a Decision Required item that blocks Business Owner approval, when no owner was assigned upstream?
