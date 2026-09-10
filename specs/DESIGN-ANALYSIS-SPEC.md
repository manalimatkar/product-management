# Design Analysis Artifact Specification

## 1. Purpose

The Design Analysis is the bridge between versioned product source material and business requirements. It is reusable across product, service, process, platform, and change initiatives.

It explains what the Business Agent understood from the design before it creates or updates business requirements, Epics, Stories, acceptance criteria, decisions, and open questions.

The artifact exists to make the transformation inspectable:

```text
Versioned Product Source Material
        |
        v
Design Analysis
        |
        v
Actors, goals, capabilities, behavior, and outcomes
        |
        v
Business Requirements and Rules
        |
        v
Stories and Acceptance Criteria
        |
        v
Business Review PR
```

The Design Analysis is a business/product analysis artifact. It must not become a technical design document. UI-specific fields are an optional analysis module, not a requirement for every product.

## 2. Ownership and Lifecycle

### Producer

The Business Agent creates the Design Analysis from configured, versioned product source material. A Design Handoff Bundle is one supported source type.

### Human Review

The configured product or business reviewer reviews the Design Analysis as part of the applicable review package. The approved analysis must identify the exact source versions that were reviewed.

### Source Immutability

The Business Agent must read and reference the configured source material. It must not regenerate, rewrite, or silently modify authoritative sources.

If an authoritative source needs to change, its owner creates a new source version or revision. The Design Analysis is then regenerated or revised against that explicit version.

### Location

The Design Analysis belongs in the business repository, under its own product and feature. The authoritative naming and folder convention -- for this artifact and every other artifact type -- is [ARTIFACT-STORAGE-SPEC.md](ARTIFACT-STORAGE-SPEC.md):

```text
<platform-slug>/[<app-slug>/]analysis/<feature-slug>/design-analysis-<feature-slug>-<DA-id>.md
```

## 3. Required Metadata

Every Design Analysis must include:

| Field | Requirement |
| --- | --- |
| Analysis ID | Stable identifier for the analysis |
| Feature | Feature or initiative name |
| Source Material | Repository path or link to the source material(s) -- an analysis may cite more than one registered source; see [ARTIFACT-RELATIONSHIP-MODEL.md](ARTIFACT-RELATIONSHIP-MODEL.md) section 7 |
| Source Version | Exact source version, or `Not Versioned` |
| Analysis Version | Version of this analysis artifact |
| Created By | Business Agent identity or run identifier |
| Created At | Timestamp |
| Status | Draft, In Review, Approved, Superseded, or Rejected |
| Related Epic | Epic reference when known |
| Related Stories | Story references when known |

The metadata must be sufficient to answer:

> Which source version produced these requirements, and which analysis version did the configured reviewer approve?

## 4. Required Artifact Structure

### Business Agent Activity 1: Understand the Design

The first Business Agent activity is to build an intermediate understanding of the Design Handoff Bundle. It must complete this activity before identifying capabilities or drafting requirements.

The agent must extract and record:

- screens and pages
- user flows
- navigation between screens or flows
- user actions and available controls
- inputs and expected outputs
- visible system states
- loading, empty, success, and error scenarios
- roles and permissions represented by the design
- visible business rules
- referenced external systems or actors
- design assumptions and unresolved ambiguity

The output of this activity is an evidence-based inventory and behavioral description. It is not yet a requirement list and must not contain technical implementation decisions.

For every extracted item, the analysis must identify:

- what was observed
- where it was observed in the Design Handoff Bundle
- whether it is explicit or interpreted
- what remains unknown

The agent must not jump directly from a screen or visual element to a requirement without first recording the design understanding that supports it.

**Analysis order, added 2026-09-10: understand flows before decomposing into capabilities.** This is a generic rule, common to every source tool -- not something that changes between a Claude Design export, a Figma link, or a written spec. Build an end-to-end understanding of what the actor is actually trying to accomplish, step by step (this activity's "user flows," expanded in section 4.4 and 4.6), *before* decomposing that understanding into discrete capabilities (section 4.5) and requirements (section 4.8). Capabilities and requirements should emerge from an understood flow, not be assembled first from a flat inventory of screens or elements and then stitched into a flow afterward -- the second order produces requirements that are individually plausible but don't cohere into anything an actor would actually do. This section's own list above (screens, then flows, then actions, then states...) is a checklist of what to extract, not the order to extract it in.

**Reading the source accurately, added 2026-09-10:** this activity is where reading *technique* matters most (distinct from analysis *order*, above), and where a Design Analysis has previously fallen short (see `CLAUDE.md`'s history of the retracted `DA-002` and the first draft of `DA-003`). `EVIDENCE-SPEC.md` section 3.1 states the generic rules -- read the most literal representation available, cross-check a descriptive document against the literal artifact rather than trusting it alone, locate actual data rather than stopping at the logic that operates on it, and don't trust an unverified verification technique. These generic rules are tool-agnostic; how they apply concretely depends on which tool produced the source -- for a native Claude Design export, see [CLAUDE-DESIGN-READING-SPEC.md](CLAUDE-DESIGN-READING-SPEC.md) (the dark `.dc.html` file as sole source of truth, the README as reference only). A different source tool gets its own sibling reading-spec document, not a rewrite of this one.

**Check the registry before minting a new Journey, Capability, or Business Rule ID, added 2026-09-10.** Unlike an Observation, Gap, Decision, Assumption, or Technical Unknown -- all genuinely scoped to this one analysis -- a Journey, Capability, or Business Rule is product-level (`ARTIFACT-RELATIONSHIP-MODEL.md` section 3.1) and has a real registry: [JOURNEY-REGISTRY.md](../JOURNEY-REGISTRY.md), [CAPABILITY-REGISTRY.md](../CAPABILITY-REGISTRY.md), [BUSINESS-RULE-REGISTRY.md](../BUSINESS-RULE-REGISTRY.md). Before assigning a new `JRN-`/`CAP-`/`BRULE-` ID, check whether an existing entry is genuinely the same one -- cite it and link to its record instead of re-deriving a new ID locally. This matters most for Business Rules, which typically constrain behavior across features rather than being produced by any one of them -- a rule like "structural edits never require confirmation" should be inherited by a later, unrelated analysis, not silently re-derived or contradicted.

### 4.1 Source Summary

Describe the source material without changing it:

- what the source material is for
- what feature or user problem it addresses
- which files and folders were reviewed
- which source files were unavailable, unclear, or excluded
- the source version used, when versioned

Each significant observation must include a source reference such as a file path, screen name, flow name, or section identifier.

### 4.2 Product Context and Domain Inventory

Record the product context that is independent of any particular interface or delivery technology:

- actors, roles, and affected parties
- user or business goals
- domain concepts and terminology
- capabilities and outcomes
- workflows or operating processes
- business rules and policies
- known states and lifecycle transitions
- external actors, systems, or dependencies

The inventory describes what the product or process enables. It must be present even when no visual design exists.

### 4.3 Optional UI Design Inventory

When the source includes a user interface, record its observable contents:

- pages and screens
- navigation paths
- user flows
- user actions
- inputs and outputs
- visible content
- controls and interactions
- loading states
- empty states
- success states
- error states
- validation messages
- roles or permissions represented
- external systems referenced
- assets relevant to user behavior

The UI inventory describes what is present. It does not infer why a technical implementation was chosen. For non-UI products, this section may be marked `Not Applicable`.

### 4.4 Product Understanding

Explain the behavior represented by the source material in user and business terms.

For each flow, describe:

- actor
- starting condition
- user intent
- user action
- expected system response
- resulting state
- alternate paths
- failure or recovery behavior
- evidence from the Design Handoff Bundle

Use plain business language. For example:

> A user selects a supported document, starts an upload, sees progress, and receives a completion or failure indication.

Do not write implementation choices such as storage services, API patterns, frameworks, or database schemas.

### 4.5 Capabilities

Group related behaviors into business capabilities.

Each capability must include:

- Capability ID
- name
- business purpose
- participating user or role
- supporting design references
- behaviors included
- related requirements, once created
- unresolved decisions

Example:

```text
Capability: Document Processing

Behaviors:
- upload a document
- view processing status
- review extracted content
- submit the result
```

A capability describes what the product enables. It does not define service boundaries or application ownership.

**Capabilities are product-level, not analysis-scoped -- added 2026-09-10, registry built the same day.** A Capability ID is global, assigned from [CAPABILITY-REGISTRY.md](../CAPABILITY-REGISTRY.md) -- check it before minting a new one; cite an existing entry when the analysis is genuinely describing the same Capability. See [ARTIFACT-RELATIONSHIP-MODEL.md](ARTIFACT-RELATIONSHIP-MODEL.md) section 3.1 for the full model and why a Capability's realness is proven by which Journeys actually depend on it, not by its description sounding similar to one from a different analysis.

### 4.6 User Journeys and Workflows

Describe end-to-end user journeys, business workflows, or operational processes. A journey may connect screens, service interactions, decisions, or offline activities.

Each journey must include:

- journey ID
- user or role
- goal
- preconditions
- ordered steps
- expected outcome
- alternate paths
- error paths
- source references

A journey may cross multiple screens or applications. The Business Agent must preserve the user outcome even when the design is distributed across multiple areas.

**Journeys are product-level, not analysis-scoped -- added 2026-09-10, registry built the same day.** A Journey ID is global, assigned from [JOURNEY-REGISTRY.md](../JOURNEY-REGISTRY.md). Map the journey *before* decomposing it into capabilities (this section's own analysis-order rule, stated in Activity 1 above) -- a capability's business purpose only really makes sense once the journey it serves is understood. Journeys are also the mechanism that proves whether a Capability is genuinely shared across use cases or unique to one: see [ARTIFACT-RELATIONSHIP-MODEL.md](ARTIFACT-RELATIONSHIP-MODEL.md) section 3.1. A prior revision of this repository's own Design Analysis template had folded journey IDs into narrative prose for readability, removing exactly the addressability this section depends on -- reverted in `DA-003` the same day this registry was built; keep Journey IDs as real, addressable headings going forward, not prose.

### 4.7 Business Rules

Record rules that affect user or business behavior.

Examples:

- unsupported document types cannot be submitted
- a user must complete required fields before continuing
- only an authorized role may approve a request
- a completed operation must show a clear confirmation

Each rule must include:

- Rule ID
- rule statement
- scope
- evidence classification
- design reference
- confidence
- related requirement or decision

A technical constraint is not a business rule unless the design explicitly presents it as a product behavior or policy.

**Business Rules are product-level, not analysis-scoped -- added 2026-09-10, registry built the same day.** A Business Rule ID is global, assigned from [BUSINESS-RULE-REGISTRY.md](../BUSINESS-RULE-REGISTRY.md) -- check it before minting a new one. A Business Rule typically *governs* a Journey or Capability rather than being produced by one -- it's a cross-cutting constraint, which is exactly why it needs to be visible to a future, unrelated analysis rather than silently re-derived (or worse, silently contradicted) each time. See [ARTIFACT-RELATIONSHIP-MODEL.md](ARTIFACT-RELATIONSHIP-MODEL.md) section 3.1 for the full model.

### 4.8 Business Requirements

Requirements must be atomic, observable, and testable.

Each requirement must include:

- Requirement ID
- requirement statement
- business capability
- actor or user role
- user outcome
- source observation references
- evidence classification
- assumptions, if any
- related business rules
- related decisions
- related acceptance criteria

Preferred form:

> The user must be able to submit a supported document for processing.

Avoid vague forms such as:

> The application should provide a good document experience.

Requirements must describe what the product must do, not how the system will implement it.

### 4.9 Acceptance Criteria

Acceptance criteria must express observable behavior using business language.

Use Given / When / Then where appropriate:

```text
Given the user selects a supported document
When the user starts the upload
Then the product shows upload progress
And the product confirms completion when the upload succeeds
```

Acceptance criteria must cover relevant:

- happy paths
- validation behavior
- loading behavior
- empty states
- error states
- permission behavior
- recovery behavior

Do not encode a technical implementation as an acceptance criterion.

### 4.10 Decisions and Open Questions

The Design Analysis must explicitly identify information that cannot be safely determined from the bundle.

Each item must include:

- Decision ID
- question or unresolved choice
- why it matters
- affected capability or requirement
- evidence showing the gap
- proposed owner
- status

Examples:

- What document formats are supported?
- What is the maximum document size?
- Which roles may approve the submission?
- Is the operation recoverable after failure?

The Business Agent must not invent answers to unresolved business questions.

### 4.11 Assumptions

Assumptions are interpretations used to continue analysis when evidence is incomplete but the interpretation does not establish a binding business rule.

Each assumption must include:

- Assumption ID
- statement
- evidence or reasoning
- impact if false
- owner for confirmation
- status

Assumptions must remain visible in the Business PR. They must not be presented as confirmed requirements.

### 4.12 Exclusions and Limitations

Record what the analysis does not establish:

- behavior absent from the design
- technical decisions intentionally deferred
- roles not represented
- unsupported flows
- missing assets or source files
- areas requiring technical analysis later

This section prevents downstream agents from treating silence as a decision.

### 4.13 Requirement Mapping

End the artifact with a mapping from design evidence to capabilities, requirements, and Stories.

Example:

| Design Reference | Capability | Requirement | Story | Decision |
| --- | --- | --- | --- | --- |
| `screens/upload.md` | Document Processing | BR-001 | STORY-001 | BD-001 |

Every generated requirement must have at least one source reference or be explicitly marked as a human-provided addition.

See [EVIDENCE-SPEC.md](EVIDENCE-SPEC.md) for the plain-language evidence rule, the full cross-artifact traceability chain, and a quick-reference mapping onto the classifications defined below.

## 5. Evidence Classification

Every observation, rule, requirement, and interpretation must use one of these classifications:

### Explicit
Directly stated or visibly represented in the Design Handoff Bundle.

Example:

> The upload screen contains a control for selecting a document.

### Strongly Implied
Not stated word-for-word, but required to make an explicitly represented user flow coherent.

Example:

> Selecting a supported document starts an upload operation.

Strongly implied items may be drafted, but must be labeled as inferred and remain reviewable by the Business Owner.

### Assumption
A provisional interpretation used because the design is incomplete. It must not become a confirmed requirement without human review.

Example:

> The selected document remains available if the user navigates away and returns.

### Decision Required
The design does not provide enough evidence to choose a business behavior or policy.

Example:

> The maximum supported document size is not defined.

Decision-required items must not be silently inferred.

### Technical Unknown
The business behavior is sufficiently clear, but implementation details are not defined. These belong to the Technical Agent, not the Business Agent.

Example:

> The design requires upload progress, but does not determine whether the implementation uses polling, streaming, or another mechanism.

## 6. Inference Rules

### The Business Agent may infer

The Business Agent may infer only business behavior that is necessary to explain a coherent user journey and is strongly supported by the design.

It may infer:

- that a visible action has an intended user outcome
- that a flow moves from one visible state to the next
- that a success or error state communicates the corresponding outcome
- that a required field must be completed before the related action succeeds
- that a repeated interaction belongs to the same capability
- that a visible role restriction affects access to the represented behavior

All inferences must be labeled `Strongly Implied` and linked to design evidence.

### The Business Agent must flag

The Business Agent must create a Decision Required item instead of guessing when the design does not determine:

- business policy
- supported formats or limits
- user eligibility or authority
- data retention or deletion behavior
- pricing, entitlement, or priority rules
- required integrations as a business commitment
- behavior for an unrepresented edge case
- conflict between design sources
- a choice that changes scope or user outcome

### The Business Agent must not infer

The Business Agent must not choose or imply:

- programming languages or frameworks
- APIs, endpoints, or payloads
- databases or storage services
- cloud providers or infrastructure
- service boundaries
- event or messaging patterns
- authentication implementation
- deployment architecture
- repository ownership
- performance targets not stated by the business
- technical task decomposition

These are Technical Agent concerns or later engineering decisions.

## 7. Quality Checks

A Design Analysis is ready for Business PR review only when:

- the exact Design Handoff Bundle version is recorded
- all reviewed source areas are listed
- the universal product context and domain inventory are complete
- each capability has evidence
- each requirement is atomic and testable
- each requirement has a source reference or human-origin marker
- all strong inferences are labeled
- unresolved business decisions are explicit
- technical choices are excluded or clearly deferred
- user journeys include relevant alternate and failure paths
- requirements, rules, Stories, and acceptance criteria are cross-referenced
- limitations and missing source information are visible

## 8. Approval and Change Rules

- Business Owner approval applies to the Design Analysis and related business artifacts for the identified Design Handoff Bundle version.
- A new design version requires impact analysis against the existing Design Analysis and approved requirements.
- A changed design must not silently change an approved requirement.
- A superseded Design Analysis remains available for audit.
- Technical Agents may consume only the approved Design Analysis and its referenced design version for downstream decomposition.

## 9. Example Transformation

### Design observation

The bundle shows an upload screen with a file selector, upload progress indicator, completion state, and failure message.

### Design Analysis

Capability: Document Processing

Explicit observations:

- the user can select a file
- progress is shown during upload
- completion is communicated
- failure is communicated

Strongly implied behavior:

- selecting a supported file starts an upload operation
- the operation has a pending state before completion or failure

Decision required:

- supported document formats are not defined
- maximum document size is not defined

### Business requirements

- BR-001: The user must be able to select a document for upload.
- BR-002: The product must show upload progress while the upload is in progress.
- BR-003: The product must confirm when the upload completes successfully.
- BR-004: The product must inform the user when the upload fails.

### Explicitly deferred technical decisions

- upload protocol
- storage mechanism
- API design
- retry implementation
- service ownership

## 10. Relationship to the Next Stage

The Design Analysis and Business PR answer:

> What does the product need to do, and what evidence supports that conclusion?

The Technical Agent answers later:

> How should the approved product behavior be decomposed and implemented across the engineering repositories?

The boundary between these questions must remain intact.

## 11. Reusable Template

The concrete artifact format is defined in [DESIGN-ANALYSIS-TEMPLATE.md](../templates/DESIGN-ANALYSIS-TEMPLATE.md). Business Agent runs should use that template or produce an equivalent artifact containing every required section.

**Format revised 2026-09-08 -- narrative first, not numbered-sections-first.** The original template organized the artifact as a fixed sequence of numbered sections (1. Metadata, 2. Source Summary, ... 16. Requirement Mapping), each holding tables keyed by ID. Real use (`DA-003`) surfaced a genuine usability problem raised directly by Manali: a new Business Analyst or Designer reading the artifact had to reassemble a feature's actual shape by cross-referencing IDs across a dozen tables, rather than reading a coherent account of how the feature works. This is an *editorial* revision per REQUIREMENTS-VERSIONING-SPEC.md section 9 (presentation only) -- every piece of required content in the list below still appears, none was dropped or reworded in substance:

- source and design version metadata
- a plain-language overview, before any ID appears
- the feature described as prose, grouped by feature area rather than by artifact type, with each Business Requirement given its own ID-only heading (stable anchor) plus statement, acceptance criteria, evidence link, classification, and confidence inline -- not scattered across separate sections
- capabilities, given their own stable entry point only where a later stage (Stories) will need to reference one directly
- open Decisions surfaced near the top, resolved or not
- what's explicitly not built yet, surfaced near the top rather than buried at the end
- an "Evidence and Traceability" section for everything that supports a claim above but isn't needed to understand the feature itself: observations, business rules, assumptions, decisions (full detail), gaps, and technical unknowns -- each with a real link back to what cited it
- a quality checklist

The lower-level UI inventory this spec's section 4.3 permits (screens, navigation, controls, states) is folded into the feature-area prose rather than kept as separate ID catalogs (`SCR-`, `NAV-`, `ACT-`, `STATE-`, `PATH-`, `JRN-`, `DOMAIN-`) -- nothing in this pipeline traces to those IDs directly, only to Requirements, Capabilities, and Business Rules, so preserving them as prose detail rather than permanent anchors loses no traceability. No HTML is used anywhere in the template, consistent with this repository's standing format preference -- every cross-reference is a real markdown link to a heading with a stable ID-only anchor.

## 12. Optional Analysis Modules

The core analysis must work without a visual design. Product configurations may enable additional modules, such as:

- UI design inventory: screens, navigation, controls, visual states, and assets
- service or process analysis: handoffs, operating steps, queues, and exception paths
- regulatory or control analysis: obligations, controls, evidence, and audit events
- data or domain analysis: entities, relationships, ownership, and lifecycle
- experiment or discovery analysis: hypotheses, evidence, outcomes, and learning criteria

Each module must add evidence-backed detail without replacing the core actors, goals, capabilities, behavior, outcomes, rules, assumptions, decisions, and traceability sections.

## 13. TODOs Before Implementation

- Define the required folder and file conventions for a Design Handoff Bundle.
- Define the design version format and how a Story records the approved version.
- Define the minimum evidence required for each source type, including screens, flows, assets, and design notes.
- Define how the Business Agent handles conflicting information within one bundle or across design versions.
- Define the confidence threshold for labeling an observation `Strongly Implied`.
- Define which ambiguities require a formal Business Decision versus a visible assumption.
- Define who owns and resolves each Decision Required item.
- Define how missing or unreadable source files block or limit analysis.
- Define the minimum completeness criteria for the Design Analysis before Business PR review.
- Define how a new design version triggers impact analysis against existing requirements and Stories.
- ~~Define the exact Business Agent output format and validation checks.~~ **Resolved 2026-09-08** -- see section 11 and [DESIGN-ANALYSIS-TEMPLATE.md](../templates/DESIGN-ANALYSIS-TEMPLATE.md)'s own Quality Checklist, exercised for real against `DA-003`.
- Define whether the Business Owner approves the Design Analysis separately or only through the complete Business PR.
