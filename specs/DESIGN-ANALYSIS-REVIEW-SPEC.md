# Design Analysis Review Specification

## 1. Purpose

This specification defines how a product agent creates, validates, reviews, approves, and revises a Design Analysis or equivalent product analysis artifact.

The process applies to product, service, process, platform, regulatory, operational, and change initiatives. A visual design is an optional source, not a prerequisite.

The review process ensures that analysis is evidence-based, uncertainty is visible, and business requirements are not created from unsupported assumptions.

## 2. Relationship to Other Artifacts

- [FRAMEWORK-CONFIGURATION-SPEC.md](FRAMEWORK-CONFIGURATION-SPEC.md) defines the product-specific sources, roles, modules, and approval gates.
- [DESIGN-ANALYSIS-SPEC.md](DESIGN-ANALYSIS-SPEC.md) defines the required analysis content and evidence model.
- [DESIGN-ANALYSIS-TEMPLATE.md](../templates/DESIGN-ANALYSIS-TEMPLATE.md) provides the reusable output format.
- Business Requirements are created only from analysis that has passed the configured review gate.
- [REQUIREMENTS-VERSIONING-SPEC.md](REQUIREMENTS-VERSIONING-SPEC.md) section 9's Major/Editorial classification is reused by section 18 below to route review depth, not only approval validity.

```text
Configured Sources
        |
        v
Source Readiness Check
        |
        v
Analysis Draft
        |
        v
Completeness and Evidence Validation
        |
        v
Configured Review
        |
        +--> Changes Requested --> Revised Analysis
        |
        v
Approved Analysis
        |
        v
Business Requirements
```

## 3. Roles and Authority

The active product configuration defines the names and authorities for these responsibilities:

| Responsibility | Default Role | Authority |
| --- | --- | --- |
| Source owner | Source-specific owner | Confirms source accuracy and version |
| Analysis producer | Business or product agent | Creates and revises drafts |
| Domain reviewer | Product, business, or domain reviewer | Confirms intent, rules, and outcomes |
| Final approver | Configured business authority | Approves the analysis version |
| Technical reviewer | Technical or architecture role, when needed | Reviews technical unknowns without changing business intent |

The producer must not approve its own analysis unless the product configuration explicitly permits it and documents the compensating control.

## 4. Entry Conditions

Analysis may begin only when:

- the product or initiative is identified
- the configured source types are known
- source locations or references are available
- source versions or `Not Versioned` status are recorded
- the required analysis modules are selected
- the applicable reviewer and approver roles are known
- the intended outcome or problem is stated, even if incomplete

If an entry condition is missing, the agent must record a blocking or limiting issue before drafting conclusions.

## 5. Source Readiness Check

Before interpreting source material, the product agent records:

| Check | Result | Evidence or Action |
| --- | --- | --- |
| Source can be accessed | Pass / Fail | `<reference>` |
| Source identity is known | Pass / Fail | `<reference>` |
| Source version is known | Pass / Not Versioned / Fail | `<version>` |
| Required source types are present | Pass / Fail | `<reference>` |
| Source is readable and complete | Pass / Limited / Fail | `<notes>` |
| Conflicts are detected | Yes / No | `<source references>` |
| Authority of each source is known | Pass / Fail | `<owner or rule>` |

The agent must not silently fill gaps caused by missing, unreadable, or inaccessible sources. It must record the limitation and state whether analysis can continue, continue with restrictions, or must stop.

## 6. Analysis Procedure

The product agent follows these steps in order.

### Step 1: Establish Source Context

Record the purpose, scope, source versions, source limitations, affected product area, and intended outcome.

### Step 2: Build the Universal Product Inventory

Identify, where applicable:

- actors and affected parties
- goals and needs
- domain concepts and terminology
- capabilities
- workflows or journeys
- expected outcomes
- business rules and policies
- states and transitions
- external actors or dependencies

### Step 3: Apply Optional Analysis Modules

Run only modules enabled by the product configuration. Examples include:

- UI screens, navigation, controls, and visual states
- service or operational process steps and handoffs
- regulatory obligations and controls
- data concepts and lifecycle
- experiments, hypotheses, and learning criteria

Module outputs must map to universal observations and source evidence.

### Step 4: Record Observations Before Conclusions

Each significant observation records its source, description, classification, confidence, implication, and unknowns. The agent must not jump directly from source material to an approved requirement.

### Step 5: Derive Capabilities and Behavior

Group related observations into capabilities, workflows, rules, states, and outcomes. Explain the relationship between each conclusion and its evidence.

### Step 6: Separate Certainty Levels

Classify each conclusion as:

- `Explicit`: directly stated or represented
- `Strongly Implied`: necessary to explain a coherent behavior and supported by evidence
- `Assumption`: provisional interpretation
- `Decision Required`: business choice not established by the source
- `Technical Unknown`: implementation question outside product analysis
- `Human Provided`: explicitly supplied by an authorized human

### Step 7: Record Requirements Candidates

Draft candidate requirements only from explicit, strongly implied, or human-provided conclusions. Preserve evidence and classification on every candidate.

### Step 8: Record Gaps and Decisions

For every uncertainty that affects scope, policy, eligibility, outcome, risk, or user behavior, create a Decision Required item rather than selecting an answer silently.

## 7. Inference and Decision Rules

The product agent may infer behavior only when all of the following are true:

- the behavior is necessary to explain an explicit source flow or outcome
- the source evidence is identified
- the inference does not create new policy or scope
- the inference does not select technical implementation
- the inference is labeled `Strongly Implied`

The agent must create a decision item when an uncertainty affects:

- business policy or eligibility
- scope or product commitment
- user outcome
- legal, regulatory, safety, or financial behavior
- authority or permissions
- data retention, ownership, or access
- handling of an unrepresented edge case
- interpretation of conflicting sources

An assumption may be used temporarily only when it does not establish a binding requirement and its owner and impact are recorded.

## 8. Conflict Handling

When sources conflict, the agent must:

1. Record each conflicting statement and its source.
2. Identify the configured source-authority rule.
3. Avoid choosing a winner when authority is not established.
4. Mark affected conclusions as `Decision Required` or `Conflict`.
5. Identify the owner responsible for resolution.
6. Reassess affected observations and requirements after resolution.

A newer source version does not automatically supersede an older version unless the configured versioning rule says it does.

## 9. Completeness Validation

The analysis is complete enough for review only when:

- source identity, version, and limitations are recorded
- the product problem or outcome is stated
- universal actors, goals, capabilities, workflows, and outcomes are addressed
- enabled optional modules are completed or marked not applicable
- significant observations have evidence and classifications
- requirements candidates trace to evidence or human input
- business rules are recorded separately from technical unknowns
- assumptions and decisions are visible
- conflicts and gaps have owners or explicit limitations
- scope and exclusions are stated
- traceability is complete

Completeness does not mean that every decision is resolved. Open decisions may remain visible for reviewer resolution.

## 10. Review Package

The configured review package must include:

- the analysis artifact and version
- source references and source versions
- enabled analysis modules
- evidence and observation records
- requirements candidates and traceability
- assumptions, decisions, conflicts, and limitations
- a summary of unresolved blockers
- the requested review outcome

The package must identify the exact artifact revision under review. A comment, informal message, or draft that does not identify a version is not sufficient approval evidence.

## 11. Review Outcomes

The configured reviewer may return one of these outcomes:

| Outcome | Meaning | Required Action |
| --- | --- | --- |
| `Approved` | Analysis is sufficient for the next configured stage | Record approver, date, and exact version |
| `Changes Requested` | Analysis can proceed after specified corrections | Record findings and create a new version |
| `Rejected` | Analysis is unsuitable or outside scope | Record rationale and stop or redirect |
| `Blocked` | Required source, decision, or authority is unavailable | Record blocker and owner |
| `Not Applicable` | Configured analysis is not needed for this effort | Record rationale and substitute control |

Approval of an analysis does not approve business scope unless the product configuration explicitly combines those gates.

## 12. Review Checklist

The reviewer should confirm:

- [ ] The analysis applies to the correct product or initiative.
- [ ] All required sources and versions are identified.
- [ ] Source limitations and conflicts are visible.
- [ ] Universal product context is complete.
- [ ] Enabled optional modules are complete or marked not applicable.
- [ ] Observations are distinguished from interpretations.
- [ ] Evidence supports each significant conclusion.
- [ ] Strong inferences are labeled and justified.
- [ ] Assumptions are not presented as confirmed requirements.
- [ ] Business decisions are not silently invented.
- [ ] Technical unknowns are separated from business decisions.
- [ ] Requirements candidates are atomic, observable, and traceable.
- [ ] Scope, exclusions, dependencies, and outcomes are clear.
- [ ] The requested review outcome and next stage are explicit.

## 13. Approval Recording

An approval record must include:

| Field | Value |
| --- | --- |
| Analysis ID | `<ID>` |
| Analysis Version | `<version>` |
| Review Package | `<reference>` |
| Outcome | Approved / Changes Requested / Rejected / Blocked / Not Applicable |
| Reviewer | `<identity and role>` |
| Decision Date | `<timestamp>` |
| Conditions | `<conditions or None>` |
| Next Stage | `<configured stage>` |
| Approval Evidence | `<link or record>` |

Approval applies only to the recorded version and conditions. A later material change requires re-review.

## 14. Revision and Change Impact

A new analysis version is required when:

- an authoritative source changes
- a source conflict is resolved
- a business decision changes an outcome or rule
- a material assumption is confirmed or rejected
- a requirement candidate changes meaning or scope
- an enabled analysis module produces material new findings
- a reviewer requests changes that affect conclusions

For each revision, record:

- previous analysis version
- new analysis version
- change reason
- changed observations and conclusions
- affected requirements and downstream items
- whether prior approval remains valid
- required re-review and owner

Previously approved versions must remain available for audit. Downstream artifacts must not silently continue using a superseded analysis when the configuration requires re-review.

## 15. Handoff to Business Requirements

The analysis may move to Business Requirements when its configured review gate is satisfied and:

- the approved or permitted analysis version is identified
- all requirement candidates have evidence or human-origin records
- unresolved decisions are visible
- the next artifact type is defined by configuration
- no blocking limitation is hidden in the analysis

The Business Requirements process must preserve the analysis version and all relevant traceability links.

## 16. Failure and Blocking Conditions

The agent must stop or mark the analysis blocked when:

- authoritative sources cannot be accessed
- required source material is missing
- a material conflict has no resolution authority
- the product outcome cannot be distinguished from implementation detail
- required reviewer or approver authority is unavailable
- traceability cannot be established
- a requested inference would create unsupported business policy or scope

A blocked analysis must state the reason, impact, owner, and condition for resuming.

## 17. Default Profile Mapping

For this repository's initial profile:

- source material may include versioned design handoff bundles
- the Business Agent is the analysis producer
- the Business Owner is the default business reviewer
- the Business PR is the default review package
- approval is recorded against the exact reviewed revision
- Design Analysis approval and Business Scope approval may be combined through the Business PR when configured
- GitHub is the initial platform adapter

These are defaults, not universal framework rules. The active framework configuration takes precedence.

## 18. Tiered Review Depth

This section exists in response to review-load raised as a critique of this repository's own single-reviewer setup: it reuses the Major/Editorial classification [REQUIREMENTS-VERSIONING-SPEC.md](REQUIREMENTS-VERSIONING-SPEC.md) section 9 already defines, to route review *effort*, not only the resumption behavior BUSINESS-AGENT-WORKFLOW.md section 8.1 already uses that same classification for.

- **Editorial-classified revision** (wording/phrasing only; zero new unresolved `Decision Required`/`Technical Unknown` items) -- may use a lightweight path: the configured reviewer is notified with the review package (section 10) plus the reviewer-aid summary (section 18.1), and the revision auto-advances to the next configured stage after a stated objection window (default 24 hours, overridable per initiative) unless the reviewer objects within it. This never means the review step was skipped -- the package must still have been delivered and the window must still have run -- only that a "no objection within the window" outcome substitutes for an explicit `Approved` when the classification and evidence support it.
- **Material-classified revision** (any new actor, business rule, or unresolved `Decision Required`) -- always uses the full review path (sections 10-13); no shortcut applies, regardless of unresolved-item count.
- This changes *when* a reviewer must actively act, never *what* they are authorized to decide -- it does not weaken or bypass reviewer authority, and it does not apply to the Design Handoff Bundle's own acceptance gate (`GATE-002`, a different gate), only to Design Analysis / Business Scope review under this specification.
- An objection, whether during the window or discovered after auto-advance, is handled the same as a `Changes Requested` outcome (section 11) -- auto-advance is not a one-way door.

### 18.1 Reviewer-Aid Summary

The review package (section 10) must be preceded by a short, auto-generated summary: what changed since the last reviewed version, what is new, which items remain unresolved, and which tier (18 above) this revision routed to and why. The summary orients the reviewer's attention -- it carries no approval authority of its own and never substitutes for the review package itself.

## 19. Revision History

| Date | Section | Change |
| --- | --- | --- |
| 2026-09-03 | 18 | Added tiered review depth (Editorial fast path with an objection window, vs. always-full Material review), in response to single-reviewer review-load. |
