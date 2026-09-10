# Evidence and Traceability Rule

## 1. Purpose

This document establishes one explicit rule that governs every artifact in this repository's pipeline:

> **Every generated requirement, and everything derived from it, must carry an explicit evidence relationship back to the design or source element that produced it.**

Without this rule stated once, in one place, "analyze the design and draft requirements" quietly becomes an instruction an agent can satisfy by reading a design document and writing stories that sound plausible. This document makes the evidence relationship a required, checkable property of every requirement, Story, and Task -- not a best practice left to agent judgment.

This is a cross-cutting rule, not a new artifact. It does not replace the detailed evidence classification already defined in [DESIGN-ANALYSIS-SPEC.md](DESIGN-ANALYSIS-SPEC.md) section 5 -- that remains the single detailed definition of each classification value. This document is the single place that states the rule itself, gives the full cross-artifact traceability chain, and gives a plain-language quick reference for applying it consistently from a Design Handoff Bundle all the way to a canonical Task.

## 2. Relationship to Other Artifacts

- [DESIGN-ANALYSIS-SPEC.md](DESIGN-ANALYSIS-SPEC.md) section 5 defines the detailed evidence classification values. This document does not redefine them; it maps them to a simpler quick-reference model and states where each one is enforced.
- [DESIGN-HANDOFF-BUNDLE-SPEC.md](DESIGN-HANDOFF-BUNDLE-SPEC.md) is where the chain starts -- screens, elements, and interactions are the source evidence.
- [DESIGN-ANALYSIS-REVIEW-SPEC.md](DESIGN-ANALYSIS-REVIEW-SPEC.md) section 6 describes the procedure that produces classified observations.
- [BUSINESS-REQUIREMENTS-SPEC.md](BUSINESS-REQUIREMENTS-SPEC.md) sections 6 and 9 require every requirement to carry evidence and classification, and define the traceability chain from source to Story.
- [BUSINESS-PR-SPEC.md](BUSINESS-PR-SPEC.md) section 6's Required Stage Trace is where this rule becomes structurally enforced: a Story with a broken or missing evidence chain fails the Business PR quality gate.
- [CANONICAL-TASK-SPEC.md](CANONICAL-TASK-SPEC.md) preserves the chain one hop further via its `Source Story` and `Story Version` fields.

## 3. The Traceability Chain

Every requirement must be able to answer, without gaps: *where in the source material did this come from, and how confident are we?*

```text
Design Handoff Bundle
     |
     +-- Screen: upload-document (screens/upload-document.md)
     |       +-- Element: upload-btn
     |
     +-- User Flow: upload-flow (user-flows/upload.mmd)
                      |
                      v
              Design Analysis
              (observation + classification, per DESIGN-ANALYSIS-SPEC.md section 4)
                      |
                      v
              Business Requirement BR-012
              (BUSINESS-REQUIREMENTS-SPEC.md section 5)
                      |
                      v
              Story STORY-023
                      |
                      v
              Business PR Stage Trace
              (BUSINESS-PR-SPEC.md section 6 -- the structural check)
                      |
                      v
              Canonical Task TASK-041
              (CANONICAL-TASK-SPEC.md -- Source Story reference preserves the chain)
```

A requirement, Story, or Task that cannot be walked back to a Screen, Element, User Flow, or an explicitly recorded human source is not evidence-based and must not be treated as approved.

## 3.1 Source-of-Truth When a Source Has Multiple Representations

**Added 2026-09-10**, generalizing a rule worked out concretely against a real Claude Design export (see `DESIGN-HANDOFF-BUNDLE-SPEC.md` section 6.2 for that source type's specific application). Source material is rarely one flat document. It commonly ships as a descriptive document (a README, a spec) *plus* a more literal artifact (code, an interactive prototype, a structured data file) describing the same thing -- and the two can disagree, or one can simply be unreliable. This section states how to handle that, for any source type, not just a native design export.

1. **Always find and read the most literal, executable representation available, not only its prose description.** A prose document is a *claim about* the artifact; it can be incomplete, stale, or simply wrong. Where a literal artifact exists (code, a data file, a structured export), that is the primary evidence -- the descriptive document is context, not a substitute.
2. **When a source has both, cross-check them rather than defaulting to the prose.** Disagreement between the two is a Gap (`DESIGN-ANALYSIS-SPEC.md` section 4.13 -- Conflicts and Gaps), not a reason to silently prefer whichever is easier to read.
3. **A claim in a descriptive document that hasn't been checked against the literal artifact is not yet `Explicit`.** If it's confirmed by the literal artifact, classify normally. If it can't be confirmed, or is contradicted, downgrade it -- record it as an `Assumption` if still plausible, or as a `Gap` if genuinely in conflict -- never record it as `Explicit` on the descriptive document's word alone.
4. **When a source offers multiple equivalent variants of the same thing** (e.g. a theme variant, a localized copy, a platform-specific export), **designate one variant as canonical and read that one** -- don't treat variants as interchangeable, and don't assume they actually stay in sync just because a rule says they should. This matters most when the tool or process producing the source is known to be unreliable at keeping variants aligned; in that case treat the non-canonical variant as unverified, not as a second independent source.
5. **Locate the actual data, not just the logic that operates on it.** A literal artifact's behavior is often defined as logic operating over a separate data definition (a seed array, a config block, a fixture) -- reading the logic alone and stopping there gives an incomplete picture even though the file was technically read. Find and read the data itself.
6. **Before trusting a new verification technique, confirm it's accurate on a known case.** A technique meant to double-check evidence (rendering a page, running a script, diffing two files) can itself be wrong -- and a plausible-looking negative result (e.g., an element appearing empty) can be mistaken for a real finding about the source when it's actually a limitation of the technique. Test a new technique against something already known to be true before trusting what it reports elsewhere; an unverified verification step is worse than no verification step, because it produces confident-looking false negatives.

## 4. Evidence Classification -- Quick Reference

Use these four questions to classify any observation before it becomes a requirement:

| Classification | Question it answers | Meaning |
| --- | --- | --- |
| **Explicit** | Is it directly stated or shown? | Something directly stated or visibly represented in the design. |
| **Inferred** | Is it reasonably necessary for the design to work? | Something not stated word-for-word, but required to make an explicitly represented behavior coherent. |
| **Unknown** | Does the design simply not establish this? | A gap where the agent can propose a provisional interpretation, but it must remain visible and unconfirmed. |
| **Business Decision Required** | Can the agent safely guess this? | A gap the agent must never guess -- it blocks the requirement until a human decides. |

This is the mental model every reviewer should apply. Two of these four correspond directly to a repository classification value already defined in [DESIGN-ANALYSIS-SPEC.md](DESIGN-ANALYSIS-SPEC.md) section 5; the other two split into finer distinctions the repository already needs downstream. Section 5 below maps all of it.

## 5. Mapping to the Repository's Detailed Classification

| Quick-Reference Bucket | Repository Value | Defined In | Notes |
| --- | --- | --- | --- |
| Explicit | `Explicit` | DESIGN-ANALYSIS-SPEC.md section 5 | Same concept, same name. |
| Inferred | `Strongly Implied` | DESIGN-ANALYSIS-SPEC.md section 5 | Same concept; "Inferred" is the plain-language name for a labeled, evidence-backed inference. |
| Unknown | `Assumption` | DESIGN-ANALYSIS-SPEC.md section 5 | A provisional interpretation used to continue analysis; must not become a confirmed requirement without review. |
| Unknown (implementation-only) | `Technical Unknown` | DESIGN-ANALYSIS-SPEC.md section 5 | A special case of "the design does not establish this" where the *business* behavior is already clear -- only the implementation is undefined. Owned by the Technical Agent, never the Business Agent. |
| Business Decision Required | `Decision Required` | DESIGN-ANALYSIS-SPEC.md section 5 | Same concept, same behavior: must never be silently resolved. |
| *(provenance, not confidence)* | `Human Provided` | BUSINESS-REQUIREMENTS-SPEC.md section 6 | Supplied directly by an authorized human, not derived from design evidence at all. Recorded so the chain in section 3 can terminate at a person instead of a screen. |

No artifact in this repository should introduce a sixth term or a synonym for one of these. If a new artifact needs an evidence label, it uses one of the values in this table.

## 6. What Each Classification Permits Downstream

| Classification | May become a drafted requirement? | Required action |
| --- | --- | --- |
| Explicit | Yes | Record the source reference. |
| Inferred (Strongly Implied) | Yes, labeled | Record the source reference and the reasoning that makes the inference necessary. |
| Unknown (Assumption) | No, not as a confirmed requirement | Record as an Assumption; keep visible through Business PR; owner confirms before it becomes binding. |
| Unknown (Technical Unknown) | No | Record and defer explicitly to the Technical Agent; do not resolve at the business stage. |
| Business Decision Required (Decision Required) | Never | Record as a Decision Required item with an owner; block the requirement until answered. |
| Human Provided | Yes | Record the human source and authority; still subject to the same review as any other requirement. |

This restates, in one place, the behavior already required piecemeal by [DESIGN-ANALYSIS-SPEC.md](DESIGN-ANALYSIS-SPEC.md) section 6 ("The Business Agent must not infer...") and [BUSINESS-REQUIREMENTS-SPEC.md](BUSINESS-REQUIREMENTS-SPEC.md) section 6 ("must not convert an Assumption... into an approved requirement").

## 7. Required Evidence Field

Every requirement, Story, and Task must carry, at minimum:

- a **source reference** (a Screen ID, Element ID, User Flow ID, file path, or recorded human source)
- a **classification** using one of the values in section 5
- for anything other than `Explicit`, a **stated rationale** -- why the inference is necessary, why the assumption was made, or why the decision is required

This is not a new field invented here -- it is already present as the `Evidence` and `Classification` columns on every Business Requirement ([BUSINESS-REQUIREMENTS-SPEC.md](BUSINESS-REQUIREMENTS-SPEC.md) section 5) and as the `Classification` column in every Business PR's Stage Trace ([BUSINESS-PR-SPEC.md](BUSINESS-PR-SPEC.md) section 6). This document is what makes clear that leaving that field blank, or filling it with a guess instead of a real source reference, is a rule violation, not a formatting gap.

## 8. Worked Example

Continuing the upload scenario from [DESIGN-ANALYSIS-SPEC.md](DESIGN-ANALYSIS-SPEC.md) section 9:

The Design Handoff Bundle's `upload-document` screen shows a file selector, an upload-progress indicator, a completion state, and a failure message; its `upload-flow` user flow connects Product Detail to Preview.

| Observation | Classification | Reasoning | Downstream |
| --- | --- | --- | --- |
| The screen shows a control for selecting a document | Explicit | Directly visible on `upload-document` | BR-012: "The user must be able to select a document for upload." |
| Selecting a document starts the upload | Inferred | Necessary to explain the flow from selection to progress | BR-013: "The product must begin upload immediately upon a valid selection." |
| Maximum document size | Unknown (Assumption) | Not shown anywhere in the bundle; analysis proceeds noting no limit is confirmed | ASM-004, carried forward visibly, not a binding requirement |
| Which roles may upload | Business Decision Required | The design shows no role distinction at all, and eligibility is a policy choice, not something safe to guess | DEC-002, blocks any role-scoped requirement until a Business Owner answers it |
| Whether progress uses polling or streaming | Unknown (Technical Unknown) | Business need (show progress) is clear; the mechanism is not a business decision | Deferred to the Technical Agent's Task, never resolved here |

Only the Explicit and Inferred rows may become approved Business Requirements and, eventually, Stories such as `STORY-023`. The Assumption and Decision Required rows must stay visible in the Business PR (per [BUSINESS-PR-SPEC.md](BUSINESS-PR-SPEC.md) section 8) exactly as classified, never silently dropped or silently resolved.

## 9. Where This Rule Is Enforced

| Checkpoint | Mechanism |
| --- | --- |
| Design Handoff Bundle | `evidence` hints on screen states and interactions (DESIGN-HANDOFF-BUNDLE-SPEC.md section 6) |
| Design Analysis | Every observation, rule, requirement, and interpretation classified per DESIGN-ANALYSIS-SPEC.md section 5; Requirement Mapping table (section 4.13) |
| Design Analysis Review | Reviewer checklist explicitly confirms "observations are distinguished from interpretations" and "assumptions are not presented as confirmed requirements" (DESIGN-ANALYSIS-REVIEW-SPEC.md section 12) |
| Business Requirements | `Evidence` and `Classification` fields required on every requirement (BUSINESS-REQUIREMENTS-SPEC.md sections 5-6); Traceability Map (section 9) |
| Business PR | Required Stage Trace -- a Story with a broken chain fails the quality gate (BUSINESS-PR-SPEC.md sections 6 and 9) |
| Canonical Task | `Source Story` and `Story Version` preserve the chain into the technical stage (CANONICAL-TASK-SPEC.md section 6) |

A gap at any checkpoint in this table is a defect in the artifact, not a stylistic omission.

## 10. Open Decisions

- Should the Business PR quality gate (BUSINESS-PR-SPEC.md section 9) be extended to mechanically reject a Stage Trace row whose classification is `Business Decision Required` but which is still linked to an included Story, rather than relying on reviewer judgment to catch it?
- What confidence threshold distinguishes `Explicit` from `Strongly Implied` when a design is ambiguous rather than simply silent? (Also open in DESIGN-ANALYSIS-SPEC.md section 13.)
- Should `Human Provided` requirements require a lighter or heavier review than design-derived ones, given they have no design evidence to independently check?
- Should this document's four-bucket quick reference be the label actually shown to a Business Owner in review tooling, with the six detailed values kept as internal/agent-facing detail only?
