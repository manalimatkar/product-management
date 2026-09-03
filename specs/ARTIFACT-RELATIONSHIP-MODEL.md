# Artifact Relationship Model

## 1. Purpose

This document is the single structural data model for this repository: every artifact type, its canonical ID format, and exactly how it relates to every other artifact -- cardinality, the field that carries the reference, and what happens across the graph when one artifact is superseded.

It is distinct from two documents that already exist:

- [EVIDENCE-SPEC.md](EVIDENCE-SPEC.md) defines the *evidence lineage* for one requirement -- how confident we are and where it came from.
- [BUSINESS-AGENT-WORKFLOW.md](BUSINESS-AGENT-WORKFLOW.md) defines the *process order* -- what happens before what.

This document defines the *structure* underneath both: how many of artifact X can point to artifact Y, and what that reference field is called.

## 2. Relationship to Other Artifacts

This document is this repository's filled-in default profile for two placeholder sections in [FRAMEWORK-CONFIGURATION-SPEC.md](FRAMEWORK-CONFIGURATION-SPEC.md):

- section 9 (Artifact Configuration) -- the artifact inventory in section 3 below is this repository's concrete answer to that section's template table
- section 15 (Traceability Configuration) -- the relationship table in section 4 below is this repository's concrete answer to that section's required-links question

Versioning mechanics referenced here are defined in [REQUIREMENTS-VERSIONING-SPEC.md](REQUIREMENTS-VERSIONING-SPEC.md). Where this document states a cardinality rule that conflicts with prose elsewhere, this document is the correction -- the conflicting doc should be read as informal shorthand for the rule stated here.

## 3. Artifact Inventory

| Artifact | Canonical ID Format | Defined In | Produced By | Stored As |
| --- | --- | --- | --- | --- |
| Source Material | `SRC-<number>` | PRODUCT-SOURCE-MATERIAL-SPEC.md §4 | Source owner | Registry entry |
| Design Handoff Bundle | `{platformSlug}/[{appSlug}/]{featureSlug}@v{MAJOR.MINOR}` | DESIGN-HANDOFF-BUNDLE-SPEC.md §5 | Designer | `bundle.md` + files |
| Design Analysis | `ANALYSIS-<number>` (feature-scoped) | DESIGN-ANALYSIS-SPEC.md §3 | Business Agent | Markdown, `analysis/<feature>/` |
| Business Requirements Set | `REQSET-<number>`, requirements `BR-<number>` | REQUIREMENTS-VERSIONING-SPEC.md §3; BUSINESS-REQUIREMENTS-SPEC.md §4 | Business Agent | Markdown |
| Epic | `EPIC-<number>` | BUSINESS-REQUIREMENTS-SPEC.md §12 | Business Agent | Markdown or Issue |
| Story | `STORY-<number>` | BUSINESS-PR-SPEC.md §7 | Business Agent | Markdown or Issue |
| Business PR | `BPR-<number>` | BUSINESS-PR-SPEC.md §5 | Business Agent | PR / review package |
| Canonical Task | `TASK-<number>` | CANONICAL-TASK-SPEC.md §6 | Technical Agent | GitHub Issue |
| Spike | `SPIKE-<number>` | CANONICAL-TASK-SPEC.md §7 | Technical Agent | GitHub Issue |
| Technical Plan (optional) | `TP-<number>` | TECHNICAL-AGENT-WORKFLOW.md §4.1 | Technical Agent | Markdown, `tasks/<feature>/` |
| Implementation PR | *(engineering repository's own numbering)* | TECHNICAL-HANDOFF.md | Developer Agent | Engineering repository PR |

`Design Analysis` has no canonical ID format defined elsewhere in the repository; `ANALYSIS-<number>` is proposed here for consistency with every other artifact's format and should be adopted or replaced explicitly, not left implicit. `Technical Plan` (optional -- most Tasks never produce one) follows the same pattern, defined directly in TECHNICAL-AGENT-WORKFLOW.md section 4.1 rather than proposed here first.

## 4. Relationship Table

| Parent | Child | Cardinality | Reference Field | Notes |
| --- | --- | --- | --- | --- |
| Source Material | Design Analysis | N:1 | `Source Material` (Analysis metadata) | One analysis may cite multiple registered sources (PRODUCT-SOURCE-MATERIAL-SPEC.md §11: "one or more Source IDs"). See section 7 below -- this corrects a singular-field inconsistency found in DESIGN-ANALYSIS-SPEC.md. |
| Design Handoff Bundle | Design Analysis | 1:1 (per Analysis version) | `Source Material` / `Source Version` | One bundle version is one of possibly several sources; see PRODUCT-SOURCE-MATERIAL-SPEC.md §7. |
| Design Analysis | Business Requirements Set | 1:1 (per Requirements Set version) | `Analysis Artifact` / `Analysis Version` | One approved analysis version produces one requirements set; a later requirements revision may still cite the same analysis version. |
| Business Requirements Set | Requirement (`BR-xxx`) | 1:N | membership in the set | A set contains one or more individual requirements. |
| Requirement (`BR-xxx`) | Epic | N:1 | grouping in BUSINESS-REQUIREMENTS-SPEC.md §12 | A requirements set groups into one or more Epics; each requirement belongs to exactly one Epic. |
| Epic | Story | 1:N | Epic reference on the Story | Standard decomposition. |
| Requirement (`BR-xxx`) | Story | N:N | Stage Trace "Business Requirement(s)" (BUSINESS-PR-SPEC.md §6) | A Story may satisfy more than one requirement, and a requirement may be delivered across more than one Story. Every pairing must appear in the Stage Trace -- see section 7 below for why this is N:N rather than 1:N. |
| Epic | Business PR | 1:N (recommended) | Business PR `Epic` field | Resolved here: one Business PR carries Stories from exactly one Epic. An Epic may span multiple Business PRs (phased delivery), but a single PR does not mix Stories from multiple Epics. See section 7. |
| Business PR | Story | 1:N | Business PR `Stories Included` | A PR carries one or more Stories, all from the same Epic. |
| Story | Canonical Task | 1:N | Task `Source Story` | A Story may produce multiple Tasks targeting different applications or repositories (CANONICAL-TASK-SPEC.md §10). |
| Canonical Task | Spike | N:N | Task `Required Spikes` / Spike `Blocks` | A Task may be blocked by more than one Spike; a Spike may block more than one Task (CANONICAL-TASK-SPEC.md §5, §7). |
| Canonical Task | Implementation PR | 1:N | Implementation PR references exactly one Task | Resolved here: an Implementation PR must reference exactly one canonical Task. If work naturally spans multiple Tasks, they are sequenced or merged as Tasks before implementation, not silently combined at the PR level. See section 7. |

## 5. Full Relationship Diagram

```text
Source Material (N)
        |  N:1
        v
Design Handoff Bundle --1:1(per version)--> Design Analysis
        |                                        |
        |                                        | 1:1 (per version)
        |                                        v
        |                              Business Requirements Set
        |                                        |
        |                                        | 1:N
        |                                        v
        |                                   Requirement (BR-xxx)
        |                                    |            |
        |                              N:1   |            |  N:N
        |                                    v            v
        |                                  Epic  <--1:N-- (grouping)
        |                                    |
        |                                    | 1:N
        |                                    v
        |                                  Story  <---------------+
        |                                    |    N:N (via Stage Trace)
        |                                    | 1:N                |
        |                                    v                    |
        |                              Canonical Task ----N:N---- Spike
        |                                    |
        |                                    | 1:N
        |                                    v
        |                            Implementation PR
        |
        +-- Business PR: carries Stories from exactly one Epic (1:N Epic->PR recommended)
```

## 6. Versioning Propagation

Consolidating the change-impact rules already defined per artifact (this table adds nothing new -- it is the single place to see them together):

| When this changes | Effect on children | Governed by |
| --- | --- | --- |
| Source Material (new version) | Design Analysis must be reassessed for impact; a new Analysis version is required if conclusions may change | PRODUCT-SOURCE-MATERIAL-SPEC.md §12 |
| Design Analysis (Major revision) | Business Requirements must be reassessed; prior requirement approval may be invalidated | DESIGN-ANALYSIS-REVIEW-SPEC.md §14 |
| Business Requirement (Major change) | Affected Stories and Tasks require impact review; approval reopens | REQUIREMENTS-VERSIONING-SPEC.md §9-10 |
| Story (Major change) | Every Canonical Task referencing it is forced to `Technical Readiness: Blocked`, even if previously `Technical Ready` | CANONICAL-TASK-SPEC.md §12 |
| Design Handoff Bundle (new version, superseding) | Design Analysis built on the prior version must be reassessed against the new bundle | DESIGN-HANDOFF-BUNDLE-SPEC.md §7; PRODUCT-SOURCE-MATERIAL-SPEC.md §12 |

A superseded artifact is never deleted; its children keep their reference to the exact version they were built against, per [REQUIREMENTS-VERSIONING-SPEC.md](REQUIREMENTS-VERSIONING-SPEC.md) section 11.

## 7. Cardinality Decisions Made Here

Three relationships had no explicit rule anywhere in the repository. Each is resolved here with rationale; treat these as defaults, not immutable law -- override them explicitly if the team decides differently, and update this document if so.

**Design Analysis source cardinality (N:1, not 1:1).** `DESIGN-ANALYSIS-SPEC.md` section 3's metadata table lists a single `Source Material` / `Source Version` field, but `PRODUCT-SOURCE-MATERIAL-SPEC.md` section 11 requires every analysis observation to reference "one or more Source IDs." The N:1 model in section 4 above is the correct one; `DESIGN-ANALYSIS-SPEC.md`'s metadata table should be read as accepting a list, and has been corrected with a pointer to this document (see section 8).

**Epic-to-Business-PR (1:N, PR scoped to one Epic).** Nothing previously stated whether a PR may mix Stories from multiple Epics. Resolved as: no -- a Business PR stays scoped to one Epic, so a Business Owner reviews one coherent capability at a time; an Epic that needs phased delivery spans multiple sequential PRs instead. This keeps the Stage Trace ([BUSINESS-PR-SPEC.md](BUSINESS-PR-SPEC.md) section 6) simple to audit.

**Task-to-Implementation-PR (1:N, PR scoped to one Task).** Nothing previously stated whether one Implementation PR could close multiple canonical Tasks. Resolved as: no -- every Implementation PR references exactly one Task, so traceability from code back to a single canonical Task stays unambiguous. Work that naturally spans multiple Tasks should be resequenced or merged as Tasks before implementation begins, not combined silently in the engineering repository.

## 8. Corrections Applied to Existing Documents

- `DESIGN-ANALYSIS-SPEC.md` section 3 now points to this document's section 7 for the corrected source cardinality, rather than implying a single source.

## 9. Open Decisions

- Should Requirement-to-Story remain N:N, or should the framework require every Story to trace to exactly one Requirement (simpler Stage Trace, less flexible decomposition)?
- Should an Epic be allowed to close before every one of its phased Business PRs is merged, or must all PRs for an Epic merge before the Epic itself is considered delivered?
- Does a Spike ever produce its own Implementation PR (e.g., a throwaway prototype), or is it always investigation-only with zero code output, as CANONICAL-TASK-SPEC.md currently implies?
- Should this document's relationship table be the literal schema validated by tooling, or remain a human-readable reference with validation defined separately?
