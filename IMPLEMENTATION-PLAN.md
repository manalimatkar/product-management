# Implementation Plan Outline

## Purpose
Build an agent-driven product development system that transforms dropped design and instruction files into governed planning artifacts in a business repository, then hands approved technical work to one or more engineering repositories.

This is an implementation outline. It identifies the work to be designed and delivered without prematurely selecting the final agent runtime, data store, or automation framework.

## Product Boundary

### Business Repository
The business repository is the product-planning workspace and source of truth for:

- source-input references
- business requirements
- Epics
- Stories
- acceptance criteria
- decisions
- technical tasks and spikes
- Business PRs
- Business Owner approvals
- agent workflow records
- project or Kanban views

### Engineering Repository
Engineering repositories own:

- code
- tests
- architecture documentation
- implementation PRs
- CI/CD
- engineering quality gates

Engineering repositories receive implementation changes and references to canonical business-repository Tasks and design handoff bundles. They do not receive copied requirements, Stories, or Tasks. Versioned design handoff bundles remain in the business repository. The UX designer is the producer in Claude Design; the Business Agent consumes the committed bundle and does not regenerate or rewrite it.

The number of engineering repositories must remain configurable.

## End-to-End Flow

```text
Versioned Claude Design handoff bundle committed to business repo
        |
        v
Business Agent design analysis
        |
        v
Business requirements, Epic, Stories, acceptance criteria,
decisions, tasks, and spikes
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
Technical Agent reads business repo and analyzes engineering repo(s)
        |
        v
Canonical Tasks / Spikes enriched with technical detail
        |
        v
Architect Review and Approval
        |
        v
Tasks become Technical Ready
        |
        v
Developer Agent
        |
        v
Code, tests, implementation PR, CI/CD, quality gates
```

## Implementation Areas

### 1. Source Input Intake
Design the mechanism for dropping or registering:

- Claude design files
- Figma files or exports
- written instructions
- PDFs
- screenshots
- mockups

The system must preserve the source reference and make it available to the Business Agent.

### 2. Business Artifact Generation
Implement Business Agent capabilities to draft:

- business requirements
- Epics
- Stories
- acceptance criteria
- decisions
- dependencies
- technical tasks
- spikes

The output must be reviewable as a Business PR. Generated content must be clearly distinguishable from human approval.

### 3. Business Review and Approval
Implement the Business PR convention and verification rules:

- Business Owner approval is required
- approval is attributable to a person
- approval applies to the reviewed Business PR version
- the PR must be merged before technical analysis begins
- unapproved or unmerged content cannot trigger the Technical Agent

### 4. Post-Merge Trigger
Implement a GitHub Action or equivalent event handler that validates the Business PR merge and approval before invoking the Technical Agent.

The trigger must pass enough context to identify:

- business repository revision
- Epic and Stories
- source requirements
- target engineering repositories
- approval evidence

### 5. Technical Analysis
Implement Technical Agent capabilities to:

- read the merged business artifacts
- inspect relevant engineering repositories
- identify impacted areas and dependencies
- enrich canonical Tasks and Spikes with technical findings
- identify target applications and repositories
- propose implementation guidance and dependencies
- identify spikes and unresolved risks

### 6. Architect Review
Provide a reviewable technical decomposition on the canonical Tasks and enforce an Architect decision before Tasks become technically ready.

The Architect decision must be attributable and tied to the reviewed Task or Spike versions. Revisions must be recorded against the affected canonical work items.

### 7. Canonical Task Readiness
After Architect approval, mark the canonical Tasks technically ready in the business repository. Tasks must retain links to:

- business repository
- Business PR
- Epic and Story
- technical findings and implementation guidance
- acceptance criteria

Do not create duplicate Tasks in engineering repositories. A Task identifies its target application and repository.

### 8. Design Handoff Bundles
Commit durable Claude design artifacts and application-specific UI design handoff bundles in the business repository. Each bundle must reference the relevant Epic, Story, and Task and contain the UI pages or implementation-relevant design material needed by the Developer Agent.

### 9. Developer Agent Execution
Enable the Developer Agent to act on technically ready canonical Tasks within the target repository. The engineering repository remains authoritative for implementation PRs, tests, CI/CD, and quality gates.

### 9. Traceability and Status
Provide traceability across:

```text
Source input -> Requirement -> Epic -> Story -> Design Handoff Bundle ->
Business PR -> Business Owner Approval -> Merge -> Canonical Task ->
Architect Approval -> Technical Ready -> Implementation PR -> Code
```

Support status visibility across the business repository and multiple engineering repositories without replacing repo-level workflows.

## Approval Gates

### Gate A: Business Scope
Business Owner approval of the Business PR is required before merge is accepted as a technical handoff.

### Gate B: Technical Decomposition
Architect approval of the technical detail on the canonical Task is required before the Task becomes technically ready.

### Gate C: Engineering Execution
The Developer Agent requires a technically ready canonical Task and remains subject to engineering-repository quality gates.

## Phased Delivery

### Phase 1: Business Repository Foundation
- define artifact conventions
- define source-input registration
- define Business PR structure
- define approval evidence
- create initial project/Kanban view (the board's columns are now defined -- see specs/FRAMEWORK-CONFIGURATION-SPEC.md section 8)

### Phase 2: Business Agent
- ingest source materials
- draft requirements and planning artifacts
- generate Business PR content
- capture agent output and source references

### Phase 3: Business Approval Handoff
- validate Business Owner approval
- validate merge event
- implement GitHub Action trigger
- produce an auditable handoff record

### Phase 4: Technical Agent and Task Review
- read business repository artifacts
- inspect engineering repositories
- enrich canonical Tasks and Spikes with technical detail
- implement Architect review and approval

### Phase 5: Task Readiness and Design Handoff
- mark canonical Tasks technically ready
- link application-specific design handoff bundles
- preserve acceptance criteria and lineage
- support one business Story mapping to work in multiple repos

### Phase 6: Developer Agent and Visibility
- enable Developer Agent execution
- integrate implementation PR references
- expose cross-repo status and traceability
- validate quality-gate and failure paths

## Automation Roadmap (started 2026-09-03)

Manali's stated goal for this phase: a platform-agnostic automated system (tools/skills/agents runnable on Claude, ChatGPT, or Copilot interchangeably), with the ability to run any single pipeline stage independently, not only a full end-to-end automation. The original 5-item sequence (real repo -> Execution Adapter spec -> Tool Contract -> reference implementation -> runner) was revised the same day: prove a working solution before generalizing, matching this repository's established pattern of proving the minimum first (the dry run, the GitHub-light adapter).

Revised sequence:

1. Wire up the git automation already fully specified in GITHUB-PLATFORM-ADAPTER-SPEC.md sections 6 and 6.1 but never built. **DONE 2026-09-03** -- see `.github/workflows/business-pr-merge.yml` and `.github/workflows/design-bundle-merge.yml`, and their supporting `.github/scripts/*.py`. Enforcing an actual merge block still requires enabling required status checks in the repository's branch protection settings (a GitHub UI/API step, not something a workflow file can do by itself) -- see those files' own header comments.
2. Run one real feature through the Business Agent on Claude, against the actual repository -- not the illustrative dry run. Not started; needs to run from Manali's own terminal or local Claude Code, since this Cowork session can't reach GitHub.
3. Confirm item 1's automation actually fires on that real merge.
4. Repeat for the Technical Agent stage on the same feature.
5. Only then, write the Tool Contract -- distilled from what steps 2 and 4 actually needed, not speculated in advance.

This supersedes the item-3/item-4 ordering implied by the original roadmap recorded in specs/EXECUTION-ADAPTER-SPEC.md's Open Decisions -- that document's content stays accurate as written (it describes what's still undecided about generalizing to ChatGPT/Copilot), this section is the sequencing decision for how to get there. See CLAUDE.md's numbered open-items list (item 14) for live status.

## Validation Scenarios

1. A dropped Figma export produces a Business PR with requirements, Epic, Stories, and acceptance criteria.
2. A Business PR without Business Owner approval cannot become an authorized handoff.
3. A merged approved Business PR triggers the Technical Agent.
4. The Technical Agent cannot mark a Task technically ready before Architect approval.
5. Architect approval makes the correctly linked canonical Task available for development.
6. A Developer Agent can trace a canonical Task back to the approved Business PR and its design handoff bundle.
7. A material business-scope change cannot silently alter already-created engineering work.
8. A multi-repository Story retains one business origin and multiple engineering outcomes.

## Open Design Decisions

**Reviewed 2026-09-01** -- corrected to reflect what this session actually resolved.

- ~~exact storage and format of business-repository artifacts~~ Resolved -- see [specs/ARTIFACT-STORAGE-SPEC.md](specs/ARTIFACT-STORAGE-SPEC.md).
- exact Figma and file-ingestion mechanism -- still open (the structural shape of a Figma-sourced bundle is defined in specs/DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md section 6.1; the actual API/access mechanism is not).
- ~~GitHub Issues, Markdown, Projects, or a hybrid for each artifact type~~ Resolved -- "GitHub-light", see [specs/GITHUB-PLATFORM-ADAPTER-SPEC.md](specs/GITHUB-PLATFORM-ADAPTER-SPEC.md).
- ~~how target engineering repositories are registered and selected~~ Resolved 2026-09-01 -- [specs/FRAMEWORK-CONFIGURATION-SPEC.md](specs/FRAMEWORK-CONFIGURATION-SPEC.md) section 14 now defines the registration process; a concrete `TARGET-001` instance is pending a real engineering repository (open item 8).
- ~~exact Technical Plan format~~ Resolved 2026-09-01 -- see [specs/TECHNICAL-AGENT-WORKFLOW.md](specs/TECHNICAL-AGENT-WORKFLOW.md) section 4.1.
- ~~agent runtime and model selection -- still open, and out of scope for this framework's documentation (an infrastructure/tooling decision, not a governance question).~~ Partially resolved 2026-09-03 -- see [specs/EXECUTION-ADAPTER-SPEC.md](specs/EXECUTION-ADAPTER-SPEC.md): which platform (Claude, ChatGPT, Copilot) executes a stage is now a defined invocation contract. Exact model selection within a platform, and credential/config management, stay out of scope -- still an operator/runtime choice.
- whether Developer Agent execution is enabled in the first release or added after handoff -- still open, a scoping decision.

## TODOs Before Implementation Planning Is Final

- ~~Confirm the end-to-end design-to-requirements process and Business Agent activity boundaries.~~ Resolved -- see [specs/BUSINESS-AGENT-WORKFLOW.md](specs/BUSINESS-AGENT-WORKFLOW.md).
- ~~Define the Design Handoff Bundle contract, versioning, and approval relationship.~~ Resolved -- see [specs/DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md](specs/DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md).
- ~~Define the Design Analysis schema and validation rules.~~ Resolved -- see [specs/DESIGN-ANALYSIS-SPEC.md](specs/DESIGN-ANALYSIS-SPEC.md) and [specs/DESIGN-ANALYSIS-REVIEW-SPEC.md](specs/DESIGN-ANALYSIS-REVIEW-SPEC.md).
- ~~Define artifact storage conventions for `design/`, `analysis/`, `requirements/`, and canonical GitHub Issues.~~ Naming and folder layout defined 2026-08-31 in ARTIFACT-STORAGE-SPEC.md, covering a local-file fallback for canonical Tasks/Spikes too. The separate question below (Markdown vs. GitHub Issues/Projects as the actual storage medium) is still open.
- ~~Decide which artifacts are Markdown files, GitHub Issues, GitHub Projects, or a hybrid.~~ Resolved 2026-08-31 -- "GitHub-light": files stay canonical, Issues for Epic/Story/Task/Spike, PR for Business PR, labels for workflow state. See GITHUB-PLATFORM-ADAPTER-SPEC.md.
- ~~Define the Business PR template and required review checks.~~ Resolved -- see [templates/BUSINESS-PR-TEMPLATE.md](templates/BUSINESS-PR-TEMPLATE.md) and specs/BUSINESS-PR-SPEC.md section 9's Quality Gate.
- ~~Define how Business Owner approval is verified for the exact merged revision.~~ Resolved -- see specs/BUSINESS-PR-SPEC.md section 10 and specs/REQUIREMENTS-VERSIONING-SPEC.md section 9.
- ~~Define the canonical Task schema, including Target Application and target repository.~~ Resolved -- see [specs/CANONICAL-TASK-SPEC.md](specs/CANONICAL-TASK-SPEC.md).
- ~~Define the Architect review mechanism for Task technical detail.~~ Resolved -- see specs/CANONICAL-TASK-SPEC.md section 9 (Architect Review Gate).
- ~~Define how Tasks move to `Technical Ready`.~~ Resolved -- same section as above.
- ~~Define the reference format used by engineering PRs to link back to Tasks and design handoff bundles.~~ Resolved 2026-09-01 -- see [specs/TECHNICAL-AGENT-WORKFLOW.md](specs/TECHNICAL-AGENT-WORKFLOW.md) section 6.1: `Traces to: TASK-<id> (business repository: <name>)`. A design handoff bundle reference is not duplicated alongside it -- the Task's own `Source Story` field already carries the chain back to the bundle, per EVIDENCE-SPEC.md section 3's traceability chain.
- ~~Define change management when a design or approved Story changes after Tasks exist.~~ Resolved -- it turned out CANONICAL-TASK-SPEC.md section 12 already fully defined this case; cross-referenced in [specs/TECHNICAL-AGENT-WORKFLOW.md](specs/TECHNICAL-AGENT-WORKFLOW.md) section 8.1, 2026-09-01.
- Define failure handling for incomplete design analysis, unresolved decisions, and broken references. -- partially answered: DESIGN-ANALYSIS-REVIEW-SPEC.md's outcome vocabulary (Blocked/Rejected) and Decision Required tracking cover most of this, but broken-reference handling specifically isn't spelled out -- still open.
- Define post-delivery validation and feedback capture. -- still open; nothing in this framework currently closes the loop after implementation.
