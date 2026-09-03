# Product Requirements Document: Agent-Driven Product Development System

## 1. Overview

This system is an agent-driven product development workspace spanning a business repository and one or more engineering repositories.

The UX designer creates designs in Claude Design from product and design source material such as Figma designs, written instructions, PDFs, screenshots, and mockups. The designer then commits versioned design handoff documents to the business repository as a first-class product artifact. The Business Agent reads the committed bundle, creates a design analysis, and translates it into structured product-development artifacts including business requirements, Epics, Stories, acceptance criteria, decisions, technical Tasks, Spikes, project views, and workflow records. The Business Agent does not regenerate or rewrite the design handoff bundle.

The Business Owner reviews and approves the resulting Business PR. The merge of that approved Business PR is the handoff event that allows the Technical Agent to read the business repository and analyze the relevant engineering repositories. The Technical Agent enriches canonical Tasks and Spikes, which remain GitHub Issues in the business repository. An Architect reviews and approves the technical decomposition. Only then may Tasks become technically ready for the Developer Agent or human developers.

The business repository is the single source of truth for product intent and work. Engineering repositories own implementation and delivery. The system does not copy requirements, Stories, or Tasks into engineering repositories; it connects them through immutable GitHub links and references. Engineering repositories contain code, tests, architecture documentation, implementation PRs, CI/CD, and quality gates. Design handoff bundles remain in the business repository and are referenced by engineering work.

## 2. Problem Statement

Product intent commonly arrives as fragmented design files, instructions, documents, and visual references. Turning that material into complete and consistent agile development artifacts requires repeated manual interpretation and coordination. Important context can be lost between design, product planning, technical decomposition, and implementation.

The problem becomes more difficult when implementation is distributed across multiple engineering repositories and AI agents participate in the work. Agents can accelerate drafting and decomposition, but they need clear artifact boundaries, review points, and authority rules. Without those boundaries:

- source design intent may not be reflected in the business requirements
- Epics, Stories, acceptance criteria, decisions, tasks, and spikes may be incomplete or inconsistent
- technical analysis may begin from unapproved business scope
- engineering issues may be created without an approved technical approach
- business stakeholders may lose visibility into how their approved intent becomes code
- cross-repository work may lose its original context and traceability

This system provides a governed path from unstructured product inputs to business planning artifacts and then to approved engineering work.

## 3. Goals and Non-Goals

### Goals

1. Accept versioned Claude Design handoff bundles as the primary input to the business/product process.
2. Convert approved design context into structured business requirements and agile product artifacts in the business repository.
3. Use a Business PR as the reviewable package for an Epic, Stories, acceptance criteria, decisions, and related planning artifacts.
4. Require Business Owner approval before the approved business scope is merged and handed to the Technical Agent.
5. Use the merged Business PR as the explicit trigger for technical analysis.
6. Enable the Technical Agent to analyze the business repository together with one or more engineering repositories.
7. Require Architect approval of the technical decomposition before canonical Tasks become technically ready.
8. Preserve traceability from source input through business artifacts, canonical Tasks, design handoff bundles, implementation PRs, and code.
9. Support agent-driven work while retaining human authority at the defined approval gates.
10. Provide visibility into the relationship between business planning and engineering delivery across repositories.

### Non-Goals

1. This is not a replacement for code repositories or their local engineering workflows.
2. It does not own application code, tests, CI/CD, deployment, or engineering quality gates.
3. It does not define the internal architecture of application repositories.
4. It is not a general enterprise PM suite for OKRs, capacity planning, financial planning, or workforce management.
5. It does not prescribe a specific LLM, model, prompt design, or agent runtime.
6. It does not remove human approval from business scope or technical planning.

## 4. Users and Authorities

### Product or Business Owner
Reviews and approves the Business PR containing the business scope package. This approval allows the merged package to be handed to the Technical Agent.

### Business Agent
Reads the committed, versioned design handoff bundle, produces a design analysis, and drafts business and agile planning artifacts in the business repository. It does not regenerate or rewrite the design bundle.

### Architect
Reviews and approves the technical decomposition produced after the approved Business PR is merged. This approval makes canonical Tasks technically ready for development.

### Technical Agent
Reads the approved business artifacts and analyzes relevant engineering repositories to enrich canonical Tasks and Spikes with technical findings, implementation guidance, dependencies, target applications, and repository references.

### Developer Agent
Works from technically ready canonical Tasks in the business repository and implements them in the target engineering repository. It operates within the engineering repository's existing PR, testing, CI/CD, and quality-gate process.

### Human Developer and Engineering Reviewer
Implement, review, and merge code in the engineering repository according to that repository's standards.

### Portfolio or Product Reviewer
Uses the business repository and cross-repository references to understand initiative status, scope, decisions, and delivery progress.

## 5. End-to-End Workflow

```text
BUSINESS REPOSITORY

Versioned Design Handoff Bundle committed to business repo
        |
        v
Business Agent analyzes the bundle
        |
        v
Design Analysis + Epic + Stories + business requirements + acceptance criteria
        |
        v
Business PR
        |
        v
Business Owner Approval
        |
        v
Merge
        |
        | GitHub Action
        v
TECHNICAL AGENT
        |
        | reads business repo
        | analyzes engineering repo(s)
        v
Canonical Tasks / Spikes enriched with technical detail
        |
        v
Architect Review
        |
        v
Architect Approval
        |
        v
Tasks become Technical Ready
        |
        v
Developer Agent or Human Developer
        |
        v
ENGINEERING REPOSITORY
Code + Tests + Architecture Docs + PRs + CI/CD + Quality Gates
```

## 6. Approval Gates

### Gate 1: Business Scope Approval

The Business Owner must approve the Business PR before it can be merged as an authorized technical handoff. Approval applies to the reviewed PR version and must be attributable.

This gate authorizes the business scope represented by the Epic and Stories and technical analysis of that approved scope after merge. It does not authorize engineering Issue creation or code implementation.

### Gate 2: Technical Decomposition Approval

The Architect must approve the Technical Agent's decomposition and technical detail before canonical Tasks become technically ready. Approval applies to the reviewed Task or Spike versions and must be attributable.

This gate authorizes the Developer Agent or human developers to act on the canonical Tasks in their target engineering repositories. It does not create duplicate Tasks in those repositories and does not replace Business Owner approval.

### Gate 3: Engineering Quality Gates

Implementation remains subject to the engineering repository's existing code review, testing, CI/CD, and quality-gate process.

## 7. Functional Requirements

### 7.1 Source Input Intake

- The system must support registering or dropping Claude design files, Figma files or exports, written instructions, PDFs, screenshots, mockups, and similar source material.
- The system must preserve source references and make them available to the Business Agent.
- Generated artifacts must be traceable to the source material used to create them.

### 7.2 Business Artifact Generation

- The Business Agent must be able to draft business requirements, Epics, Stories, acceptance criteria, decisions, dependencies, technical tasks, and spikes.
- Generated artifacts must be created in the business repository.
- Draft output must remain distinguishable from human approval.
- The Business Agent must be able to revise artifacts based on review feedback.

### 7.3 Business PR and Approval

- The system must package the generated business artifacts in a Business PR.
- The Business PR must identify the source material and affected artifacts.
- Business Owner approval must be attributable and associated with the reviewed PR version.
- A Business PR must not be treated as an authorized technical handoff until it is approved and merged.
- The Business Agent must not approve or merge its own Business PR.

### 7.4 Technical Analysis

- A GitHub Action or equivalent automation must detect the approved Business PR merge.
- The Technical Agent must read the merged business artifacts.
- The Technical Agent must analyze the relevant engineering repository or repositories.
- The Technical Agent must enrich canonical Tasks and Spikes with implementation approach, impacted applications and repositories, dependencies, sequencing, risks, testing considerations, and architecture references.
- A separate Technical Plan may be created only when the scope requires more detail than the canonical Tasks can contain.
- The Technical Agent must not mark Tasks technically ready before Architect approval.

### 7.5 Architect Review

- The Technical Plan must be a reviewable artifact with a version and attributable author.
- The Architect must be able to approve, reject, or request revisions.
- Architect approval must be tied to the reviewed Technical Plan version.
- A revised Technical Plan must return through the required review before Issue creation.

### 7.6 Canonical Task Management

- Technical Tasks and Spikes must remain canonical GitHub Issues in the business repository.
- A Story may produce multiple Tasks targeting different applications or repositories.
- Each Task must include the originating Story, acceptance criteria, technical findings, implementation guidance, target application, target repository, dependencies, architecture references, and constraints.
- The system must not copy the requirement, Story, or Task into an engineering repository as a second source of truth.
- A Task may become technically ready only after Architect approval of its technical decomposition.

### 7.7 Design Handoff Bundles

- Durable Claude Design artifacts must be committed under the business repository's feature-specific `design/` area.
- Each design handoff bundle must have an explicit version number so the approved design input can be identified later.
- Figma remains an external design tool; the business repository stores a reference document with the Figma link, status, related Epic or Story, and notes.
- For UI work, the business repository must contain an application-specific design handoff bundle with the resulting UI pages and implementation-relevant design material.
- The design handoff bundle must link to the canonical Story and Task and must be referenced by engineering work without duplicating the business artifacts.

### 7.8 Developer Execution

- The Developer Agent or human developer must receive a technically ready canonical Task with valid upstream references.
- Implementation must remain inside the engineering repository's normal workflow.
- The Developer Agent must not silently expand the approved Issue scope.
- Implementation PRs must retain references to the engineering Issue and upstream business context.

### 7.9 Traceability and Visibility

- The system must preserve the chain from source input to requirement, Epic, Story, design handoff bundle where applicable, Business PR, approval, merge, canonical Task, Architect approval, implementation PR, and code.
- A Story may produce Tasks targeting multiple applications and engineering repositories while retaining one business origin.
- Missing or invalid required links must be visible as an exception.
- Reviewers must be able to see business scope, approval evidence, technical status, and engineering delivery status across repositories.

### 7.9 Decisions and Change History

- Business decisions, approvals, technical reviews, revisions, and handoff events must be recorded with actor and timestamp.
- Changes to approved business scope must remain distinguishable from the original approved version.
- Changes affecting an approved Technical Plan or created engineering Issues must be surfaced for review.

## 8. Non-Functional Requirements

- Approval and handoff controls must be structurally enforced rather than dependent on agent behavior or convention.
- Every generated artifact, approval, merge-triggered handoff, technical review, and Issue creation event must be auditable.
- The workflow must be understandable to product, architecture, and engineering stakeholders.
- The design must support an evolving number of engineering repositories without hardcoding a fixed set.
- The business artifact model must remain portable beyond a particular automation engine or agent runtime.
- The system should prefer GitHub-native and lightweight mechanisms where they satisfy the requirements.
- Failure states, missing approvals, and broken traceability must be visible and actionable.

## 9. Success Metrics

- 100% of Business PR handoffs to the Technical Agent have verifiable Business Owner approval and merge evidence.
- 100% of canonical Tasks trace to an approved Story and Business PR.
- Zero Tasks become technically ready from an unapproved or unmerged Business PR.
- Zero Tasks become technically ready before Architect approval of their technical decomposition.
- 100% of implementation PRs can be traced back to a canonical Task and its originating Story.
- Business Owners can review generated planning artifacts without manually reconstructing source context.
- A multi-repository initiative can be understood from the business repository and linked engineering artifacts.

## 10. Constraints and Assumptions

- GitHub is the initial platform of record for repositories, PRs, reviews, Issues, and Actions.
- The business repository is the planning workspace and source of truth for product intent.
- Engineering repositories remain separate and own implementation delivery.
- The number of engineering repositories is not fixed in the design.
- Agent model selection, invocation mechanism, prompt engineering, and runtime infrastructure are deferred implementation decisions.
- Human Business Owner and Architect approvals remain required gates.

## 11. Dependencies

- GitHub repositories, PRs, reviews, Issues, and Actions
- source-file access for supported design and instruction formats
- an automation layer capable of invoking the Technical Agent after verified merge and approval
- an LLM or equivalent capability for Business, Technical, and Developer Agent roles
- access to relevant engineering repositories for technical analysis

## 12. Risks

- Agents may produce incomplete or incorrect interpretations of visual or written source material.
- Business PR approval may be treated as a formality unless the reviewed artifact version is clearly identified.
- Technical analysis may use stale engineering-repository context.
- Traceability may decay if references are optional or manually maintained.
- Cross-repository Issue creation may produce inconsistent conventions.
- Scope may expand into replacing all engineering or enterprise PM tooling.

## 13. Open Questions

**Reviewed 2026-09-01** -- several items below were resolved by later work in this session without being struck through; corrected now so this list reflects what's actually still open.

- Which exact source-file formats and Figma access patterns are included in the first release? -- partially answered: [DESIGN-HANDOFF-BUNDLE-SPEC.md](specs/DESIGN-HANDOFF-BUNDLE-SPEC.md) section 6.1 defines all four source shapes structurally, but *which ones ship in the first release* is a scoping decision, not a documentation gap, and remains open.
- ~~Which business artifact types are Markdown files, GitHub Issues, GitHub Projects, or another GitHub-native representation?~~ Resolved 2026-08-31 -- see [GITHUB-PLATFORM-ADAPTER-SPEC.md](specs/GITHUB-PLATFORM-ADAPTER-SPEC.md) and FRAMEWORK-CONFIGURATION-SPEC.md section 13.
- ~~How are engineering repositories registered, selected, and authorized for Technical Agent analysis?~~ Resolved 2026-09-01 -- [FRAMEWORK-CONFIGURATION-SPEC.md](specs/FRAMEWORK-CONFIGURATION-SPEC.md) section 14 now defines the full registration process; the one remaining gap is a concrete `TARGET-001` instance, which needs a real engineering repository to exist first (open item 8), same blocker as elsewhere in this repository.
- ~~What minimum content must a Business PR contain before Business Owner review?~~ Resolved -- see [BUSINESS-PR-SPEC.md](specs/BUSINESS-PR-SPEC.md) section 9's Quality Gate.
- ~~What minimum content must a Technical Plan contain before Architect review?~~ Resolved 2026-09-01 -- see [TECHNICAL-AGENT-WORKFLOW.md](specs/TECHNICAL-AGENT-WORKFLOW.md) section 4.1. Default is no separate Technical Plan (the Task/Spike schema in CANONICAL-TASK-SPEC.md suffices); when scope spans multiple Tasks, a Markdown document reviewed under the same Architect Review Gate.
- ~~How are material changes handled after a Business PR is merged or engineering Issues exist?~~ Resolved -- it turned out [CANONICAL-TASK-SPEC.md](specs/CANONICAL-TASK-SPEC.md) section 12 already fully defined this case; this list just wasn't cross-referencing it. Restated in [TECHNICAL-AGENT-WORKFLOW.md](specs/TECHNICAL-AGENT-WORKFLOW.md) section 8.1, 2026-09-01.
- Is Developer Agent code implementation included in the first release, or does the first release stop at engineering Issue creation? -- still open; a scoping decision, not a documentation gap.
- ~~What happens when a source design file changes after business artifacts have been approved?~~ Resolved -- see [PRODUCT-SOURCE-MATERIAL-SPEC.md](specs/PRODUCT-SOURCE-MATERIAL-SPEC.md) section 12 (Conflict and Change Handling) and REQUIREMENTS-VERSIONING-SPEC.md section 9.

### Process Definition TODOs

- ~~Define the complete Business Agent process from Design Handoff Bundle ingestion through Business PR creation.~~ Resolved -- see [BUSINESS-AGENT-WORKFLOW.md](specs/BUSINESS-AGENT-WORKFLOW.md).
- ~~Define the required Design Analysis artifact format and evidence model.~~ Resolved -- see DESIGN-ANALYSIS-SPEC.md and EVIDENCE-SPEC.md.
- ~~Define the allowed inference boundary for the Business Agent.~~ Resolved -- see DESIGN-ANALYSIS-SPEC.md's inference rules and EVIDENCE-SPEC.md's classification vocabulary.
- ~~Define the minimum information required before a requirement can be drafted.~~ Resolved -- see BUSINESS-REQUIREMENTS-SPEC.md and EVIDENCE-SPEC.md.
- ~~Define the minimum information required before a Story can enter Business Owner review.~~ Resolved -- see BUSINESS-PR-SPEC.md section 9's Quality Gate.
- ~~Define how Business Owner approval identifies the approved Design Handoff Bundle and Design Analysis versions.~~ Resolved -- see BUSINESS-PR-SPEC.md's Stage Trace and version-recording requirements.
- Define ownership and due dates for unresolved business decisions. -- still open, and a real gap: BPR-001's own four open Decisions (DEC-001..DEC-004) have no owner or due date tracked anywhere in this repository today.
- ~~Define how design, requirement, and Story changes affect already-approved artifacts.~~ Resolved -- see REQUIREMENTS-VERSIONING-SPEC.md section 9 and PRODUCT-SOURCE-MATERIAL-SPEC.md section 12.
- ~~Define the exact canonical Task fields required before Architect review and before `Technical Ready`.~~ Resolved -- see CANONICAL-TASK-SPEC.md's schema and section 9 (Architect Review Gate).
- ~~Define how implementation PRs reference canonical Tasks without copying business artifacts.~~ Resolved 2026-09-01 -- see [TECHNICAL-AGENT-WORKFLOW.md](specs/TECHNICAL-AGENT-WORKFLOW.md) section 6.1: `Traces to: TASK-<id> (business repository: <name>)`.
- Define post-delivery validation against the approved design and business outcome. -- still open; nothing in this framework currently closes the loop after implementation, and this is lowest-urgency since nothing upstream has been exercised against a real repository yet.

## 14. Design Analysis

The Design Analysis is the required bridge between the versioned Design Handoff Bundle and business requirements. It records the screens, flows, behaviors, states, capabilities, business rules, requirements, acceptance criteria, assumptions, and unresolved decisions identified from the design.

The Business Agent must label each conclusion as explicit, strongly implied, an assumption, a decision required, or a technical unknown. It may infer strongly implied business behavior when supported by design evidence, but it must flag unresolved business policy and must not choose technical implementation details. The complete specification is maintained in [DESIGN-ANALYSIS-SPEC.md](specs/DESIGN-ANALYSIS-SPEC.md).

## 15. Artifact Set

This PRD defines the product baseline. Supporting workflow and design artifacts should remain separate as the implementation evolves:

- business repository workflow
- agent responsibilities and permissions
- technical handoff contract
- implementation plan
