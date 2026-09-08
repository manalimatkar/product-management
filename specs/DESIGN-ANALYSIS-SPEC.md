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

The template standardizes:

- source and design version metadata
- design inventory
- observation records
- evidence classification and confidence
- user journeys and capabilities
- business rules and requirements
- acceptance criteria
- assumptions and decisions required
- technical unknowns
- conflicts and gaps
- requirement-to-source mapping
- review outcome and quality checklist

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
- Define the exact Business Agent output format and validation checks.
- Define whether the Business Owner approves the Design Analysis separately or only through the complete Business PR.
