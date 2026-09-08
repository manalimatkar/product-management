# Business Requirements Artifact Specification

## 1. Purpose

The Business Requirements artifact translates approved product analysis and source evidence into a clear statement of what the product, service, process, or change effort must achieve for users and the business.

It is the controlled product definition used to create or update an Epic, Stories, and acceptance criteria. It must remain understandable to a Business Owner and must not become a technical design document.

```text
Approved Product Analysis
        |
        v
Business Requirements
        |
        v
Epic + Stories + Acceptance Criteria
        |
        v
Configured Review Package and Approval
```

## 2. Ownership and Lifecycle

### Producer

The configured product agent drafts the Business Requirements artifact from an approved or reviewable analysis. The analysis may be a Design Analysis, research analysis, process analysis, regulatory analysis, domain analysis, or another configured analysis type.

### Human Review

The configured business or product authority reviews the requirements through the configured review package. Approval confirms that the outcome, scope, rules, and acceptance criteria represent the intended behavior.

### Source Relationship

Every generated requirement must reference:

- the exact source material and version
- the analysis artifact and analysis version, when an analysis is used
- one or more observations, capabilities, rules, or decisions from that analysis

A requirement labeled `Human Provided` may originate outside the analysis, but its source and author must be recorded.

### Status

A requirement may have one of these statuses:

- `Draft`
- `In Review`
- `Approved`
- `Implemented`
- `Superseded`
- `Rejected`

A requirement must not be treated as approved solely because an agent created it.

## 3. Business and Technical Boundary

Business Requirements define:

- the user or business problem
- the desired business outcome
- users, roles, and actors
- observable product behavior
- business rules and policy
- scope, exclusions, and dependencies
- business-level acceptance criteria

Business Requirements must not prescribe:

- programming languages or frameworks
- services, APIs, databases, or schemas
- system architecture or deployment design
- code structure or implementation tasks
- technical estimates or implementation sequencing

Technical questions belong in the applicable analysis artifact or in the later technical handoff.

## 4. Required Metadata

Every Business Requirements artifact must include:

| Field | Requirement |
| --- | --- |
| Requirements ID | Stable identifier for the requirements set |
| Feature or Initiative | Product area being defined |
| Source Material | Exact repository path or link |
| Source Version | Exact source version, or `Not Versioned` |
| Analysis Artifact | Path or link to the analysis, when applicable |
| Analysis Version | Exact analysis version |
| Requirements Version | Version of this artifact |
| Created By | Business Agent run or author |
| Created At | Timestamp |
| Status | Draft, In Review, Approved, or another defined status |
| Related Parent | Parent initiative or artifact reference when known |
| Review Package | Review reference when created |
| Required Approval | Approval reference or `Pending` |

### Storage

This artifact is stored at `<platform-slug>/[<app-slug>/]requirements/<feature-slug>/business-requirements-<feature-slug>-<REQSET-id>.md`, per [ARTIFACT-STORAGE-SPEC.md](ARTIFACT-STORAGE-SPEC.md), which also governs how a new Requirements Version is stored as a new file rather than an overwrite (section 7).

## 5. Requirement Record

Each requirement must contain:

- a stable requirement ID
- a short, outcome-oriented name
- one unambiguous requirement statement
- the actor or beneficiary
- the business outcome
- the related capability
- source evidence and classification
- applicable business rules
- assumptions and decisions
- dependencies
- scope and exclusions
- business-level acceptance criteria
- related parent or downstream work items when available

A requirement should express one coherent outcome. Split requirements when they have different actors, outcomes, approval decisions, or independent acceptance criteria.

Use this form for the statement:

> The product must `<observable behavior>` for `<actor>` so that `<business outcome>`.

See [EVIDENCE-SPEC.md](EVIDENCE-SPEC.md) for the repository-wide evidence rule and traceability chain this section implements.

## 6. Evidence and Inference Rules

The configured product agent may create a requirement when:

- it is directly stated by the source or analysis
- it is strongly implied by documented design behavior and evidence
- it is explicitly provided by a human product or business stakeholder

The requirement must preserve its classification:

- `Explicit`
- `Strongly Implied`
- `Human Provided`

The product agent must not convert an `Assumption`, `Decision Required`, `Technical Unknown`, unresolved conflict, or missing source into an approved requirement. It must record the item and identify the clarification or approval needed.

## 7. Acceptance Criteria

Acceptance criteria must describe observable business behavior using examples where possible:

```text
Given <starting condition>
When <user action or business event>
Then <observable product behavior>
```

Criteria should cover applicable:

- primary behavior
- validation
- loading, empty, success, and error states
- permissions
- alternate paths
- recovery behavior

Acceptance criteria must not contain implementation instructions.

## 8. Scope and Dependencies

The artifact must distinguish:

- in-scope behavior
- explicitly out-of-scope behavior
- business dependencies
- external actors or systems
- decisions that block approval
- assumptions that require confirmation

A technical dependency may be recorded as a handoff question, but it must not be resolved through an invented technical choice.

## 9. Traceability

The requirements set must provide traceability in both directions:

```text
Design Source -> Observation -> Capability or Rule -> Requirement -> Acceptance Criteria -> Story
```

Every generated requirement must have at least one source reference. Every significant capability and business rule identified by the analysis must be mapped to a requirement, explicitly excluded, or listed as unresolved.

## 10. Quality Gate Before Configured Review

The product agent may propose the artifact for the configured review only when:

- metadata identifies exact design and analysis versions
- each requirement has a stable ID and clear statement
- requirements describe business outcomes rather than technical solutions
- evidence and classifications are recorded
- business rules, assumptions, decisions, and dependencies are visible
- acceptance criteria are observable and testable at the business level
- scope and exclusions are explicit
- unresolved blockers are identified
- traceability is complete
- related parent and downstream work-item references are present when already created

The configured reviewer may approve, request changes, or reject the requirements through the configured review package.

## 11. Change Management

Requirements versioning follows [REQUIREMENTS-VERSIONING-SPEC.md](REQUIREMENTS-VERSIONING-SPEC.md). A stable Requirement ID identifies the business concept, while the Requirements Version identifies the complete set reviewed together. Major changes invalidate prior approval and require re-review.

If the source material, analysis, or business decision changes:

1. Create a new artifact version.
2. Identify affected requirements, Stories, and acceptance criteria.
3. Record the reason and source of the change.
4. Mark replaced requirements as `Superseded` rather than deleting history.
5. Reopen or update the configured review package when approval scope changes.

The approved version must remain identifiable for any downstream work-item or delivery reference.

## 12. Relationship to Later Artifacts

Business Requirements are the input to the next configured decomposition step:

- an initiative, Epic, or equivalent groups a coherent outcome
- Stories, use cases, work packages, controls, or equivalent items describe valuable slices of behavior
- acceptance criteria or configured completion criteria make each item reviewable
- downstream technical or operational work is created only after the configured business scope is approved

Downstream agents or delivery roles may ask questions about the requirements, but must not silently change business intent.
