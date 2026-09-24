# Product Management

`product-management` is the business and product-development repository for an agent-driven software delivery process.

It is the single source of truth for product intent and planned work. Engineering repositories remain responsible for implementation and delivery.

## Purpose

The repository transforms approved design context into structured product-development artifacts:

```text
Versioned Design Handoff Bundle
        |
        v
Design Analysis
        |
        v
Business Requirements
        |
        v
Epic + Stories + Acceptance Criteria
        |
        v
Business Review PR
        |
        v
Business Owner Approval
        |
        v
Technical Agent Analysis
        |
        v
Canonical Tasks and Spikes
        |
        v
Architect Approval
        |
        v
Technical Ready
        |
        v
Developer Agent or Human Developer
```

## Repository Responsibilities

This repository contains and governs:

- versioned design handoff bundles
- design analysis
- business requirements
- Epics and Stories
- acceptance criteria
- canonical technical Tasks and Spikes
- business decisions and open questions
- approvals and workflow state
- project or Kanban views (board columns defined in specs/FRAMEWORK-CONFIGURATION-SPEC.md section 8)
- references to engineering repositories and implementation PRs

Engineering repositories contain:

- application code
- tests
- architecture documentation
- implementation PRs
- CI/CD
- engineering quality gates

Requirements, Stories, and Tasks are not copied into engineering repositories. Engineering work references the canonical Task in this repository.

## Design Handoff

The UX designer creates designs in Claude Design and commits versioned design handoff documents to this repository.

A design handoff bundle is a first-class product artifact. It may contain:

- design specification
- UI pages and screens
- user flows
- assets
- interaction details
- implementation-relevant design notes

The Business Agent consumes the committed bundle. It does not regenerate or rewrite the design handoff.

A Story must reference the applicable design handoff bundle and version.

**Two upload paths (specs/DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md section 6.2, added 2026-09-03):** a genuine Claude Design export lands untouched on a persistent `design` branch (`<platform-slug>/[<app-slug>/]design/v<N>/`), not `main` -- its merge opens a tracked GitHub Issue that is the real Business Agent trigger. A hand-authored bundle (a bare Figma link, a written spec + screenshots) still goes directly against `main`'s existing `design/` convention, unchanged.

## Agents and Responsibilities

### Business Agent

- reads the approved design handoff bundle
- produces Design Analysis
- identifies capabilities, user intent, and behavior
- drafts business requirements, Epics, Stories, and acceptance criteria
- identifies business rules, assumptions, and open decisions
- prepares a Business PR

The Business Agent does not make technical architecture decisions, approve business scope, or merge the Business PR.

**Runnable, not just described** -- this everything above has been an authority/responsibility description since this document was written; as of 2026-09-09 there is a real, invokable definition of it for Claude Code: [.claude/agents/business-agent.md](https://github.com/manalimatkar/product-management/blob/main/.claude/agents/business-agent.md). See the `.claude/` entry in Documents below.

### Technical Agent

- starts after the approved Business PR is merged
- reads the business repository
- analyzes relevant engineering repositories
- decomposes approved Stories into canonical Tasks and Spikes
- adds technical findings, implementation guidance, dependencies, target application, and repository references
- prepares Tasks for Architect review

### Developer Agent

- starts from a technically ready canonical Task
- works in the target engineering repository
- implements code and tests within Task scope
- opens implementation PRs that reference the canonical Task
- follows the engineering repository's CI/CD and quality gates

## Approval Gates

### Business Owner Approval

The Business Owner approves the Business PR containing the design analysis, requirements, Epic, Stories, acceptance criteria, decisions, and open questions. The PR must be approved and merged before technical analysis begins.

### Architect Approval

The Architect reviews the Technical Agent's decomposition and technical detail on the canonical Tasks and Spikes. Tasks become `Technical Ready` only after this approval.

### Engineering Review

Implementation is reviewed in the target engineering repository through its normal PR, testing, CI/CD, and quality-gate process.

## Canonical Traceability

```text
Design Handoff Bundle
  -> Design Analysis
  -> Business Requirement
  -> Epic
  -> Story
  -> Business PR
  -> Business Owner Approval
  -> Merge
  -> Canonical Task
  -> Architect Approval
  -> Technical Ready
  -> Implementation PR
  -> Code and Tests
```

A single Story may produce multiple Tasks targeting different applications or engineering repositories.

## Documents

Organized 2026-09-01 (see ARTIFACT-STORAGE-SPEC.md for how generated instances -- nested per platform/app as `<platform-slug>/[<app-slug>/]{sources,design,analysis,requirements,business-prs,tasks}/...` since 2026-09-08 -- are organized separately from these framework documents).

### Root

- [PRD.md](PRD.md) - product definition, goals, requirements, and constraints
- [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md) - implementation roadmap and delivery phases
- [SOURCE-REGISTRY.md](registries/SOURCE-REGISTRY.md) - the running index of every registered source
- [JOURNEY-REGISTRY.md](registries/JOURNEY-REGISTRY.md), [CAPABILITY-REGISTRY.md](registries/CAPABILITY-REGISTRY.md), [BUSINESS-RULE-REGISTRY.md](registries/BUSINESS-RULE-REGISTRY.md) - added 2026-09-10, same "index here, real detail in the entity's own file" pattern as SOURCE-REGISTRY.md, for the three artifact types that are product-level rather than scoped to one Design Analysis. See ARTIFACT-RELATIONSHIP-MODEL.md section 3.1.

### specs/ -- the rules each artifact type and process must follow

- [BUSINESS-REPOSITORY-WORKFLOW.md](specs/BUSINESS-REPOSITORY-WORKFLOW.md) - business-stage workflow and Business Owner gate
- [DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md](specs/DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md) - Design Handoff Bundle schema, manifest, and design/implementation boundary
- [CLAUDE-DESIGN-READING-SPEC.md](specs/CLAUDE-DESIGN-READING-SPEC.md) - how to read a native Claude Design export accurately (dark `.dc.html` as source of truth, README as reference only) -- tool-specific, sibling to a future Figma equivalent; the generic analysis method (flows before capabilities) stays in DESIGN-ANALYSIS-SPEC.md
- [DESIGN-ANALYSIS-SPEC.md](specs/DESIGN-ANALYSIS-SPEC.md) - Design Analysis structure, evidence, and Business Agent inference rules
- [DESIGN-ANALYSIS-REVIEW-SPEC.md](specs/DESIGN-ANALYSIS-REVIEW-SPEC.md) - analysis intake, validation, review, approval, and change process
- [PRODUCT-SOURCE-MATERIAL-SPEC.md](specs/PRODUCT-SOURCE-MATERIAL-SPEC.md) - source registration, authority, versioning, readiness, and change handling
- [ARTIFACT-STORAGE-SPEC.md](specs/ARTIFACT-STORAGE-SPEC.md) - single naming and folder convention for every generated artifact type
- [GITHUB-PLATFORM-ADAPTER-SPEC.md](specs/GITHUB-PLATFORM-ADAPTER-SPEC.md) - the chosen GitHub-light platform adapter: how every artifact maps onto Issues, PRs, and labels
- [EXECUTION-ADAPTER-SPEC.md](specs/EXECUTION-ADAPTER-SPEC.md) - the sibling execution adapter: how a pipeline stage is invoked on Claude, ChatGPT, or Copilot, and how any single stage can be run independently on any of them
- [BUSINESS-REQUIREMENTS-SPEC.md](specs/BUSINESS-REQUIREMENTS-SPEC.md) - Business Requirements structure, boundaries, evidence, and lifecycle
- [BUSINESS-PR-SPEC.md](specs/BUSINESS-PR-SPEC.md) - Business PR minimum content, the controlled Design-to-Story transformation, and the required Stage Trace
- [EVIDENCE-SPEC.md](specs/EVIDENCE-SPEC.md) - the evidence rule: classification quick reference and the required traceability chain from source to Task
- [REQUIREMENTS-VERSIONING-SPEC.md](specs/REQUIREMENTS-VERSIONING-SPEC.md) - requirement identity, versioning, approval validity, and change impact
- [ARTIFACT-RELATIONSHIP-MODEL.md](specs/ARTIFACT-RELATIONSHIP-MODEL.md) - the structural data model: artifact IDs, cardinality between every artifact type, and versioning propagation. Section 3.1 covers how Journeys, Capabilities, and Business Rules -- reading a `CAP-`/`JRN-`/`BRULE-` ID in any generated Design Analysis starts here.
- [HANDOFF-SEQUENCE.md](specs/HANDOFF-SEQUENCE.md) - the same pipeline as a PlantUML sequence diagram: who does what, in order, with the governing rule noted at each step
- [FRAMEWORK-CONFIGURATION-SPEC.md](specs/FRAMEWORK-CONFIGURATION-SPEC.md) - configurable sources, artifacts, roles, gates, platforms, and delivery targets
- [TECHNICAL-HANDOFF.md](specs/TECHNICAL-HANDOFF.md) - technical analysis, Task readiness, and engineering boundary
- [CANONICAL-TASK-SPEC.md](specs/CANONICAL-TASK-SPEC.md) - canonical Task and Spike schema, Technical Agent boundary, and the Architect review gate
- [BUSINESS-AGENT-WORKFLOW.md](specs/BUSINESS-AGENT-WORKFLOW.md) - the ordered, end-to-end Business Agent contract from source material to Business PR
- [TECHNICAL-AGENT-WORKFLOW.md](specs/TECHNICAL-AGENT-WORKFLOW.md) - the ordered, end-to-end Technical Agent contract from a merged Business PR to Technical Ready Tasks and Spikes
- [AGENT-RESPONSIBILITIES.md](specs/AGENT-RESPONSIBILITIES.md) - agent permissions and responsibilities

### templates/ -- reusable, fillable starting points

- [DESIGN-HANDOFF-BUNDLE-TEMPLATE.md](templates/DESIGN-HANDOFF-BUNDLE-TEMPLATE.md) - reusable Design Handoff Bundle templates and checklist
- [DESIGN-ANALYSIS-TEMPLATE.md](templates/DESIGN-ANALYSIS-TEMPLATE.md) - reusable Design Analysis artifact template
- [PRODUCT-SOURCE-MATERIAL-TEMPLATE.md](templates/PRODUCT-SOURCE-MATERIAL-TEMPLATE.md) - reusable source registration record and readiness check
- [BUSINESS-PR-TEMPLATE.md](templates/BUSINESS-PR-TEMPLATE.md) - reusable Business PR template
- [BUSINESS-REQUIREMENTS-TEMPLATE.md](templates/BUSINESS-REQUIREMENTS-TEMPLATE.md) - reusable Business Requirements artifact template
- [CANONICAL-TASK-TEMPLATE.md](templates/CANONICAL-TASK-TEMPLATE.md) - reusable Task and Spike issue templates

### .claude/ -- runnable agent and skill definitions (Claude Code, the reference execution platform per EXECUTION-ADAPTER-SPEC.md section 4)

Added 2026-09-09, closing the gap between describing an agent (this document, AGENT-RESPONSIBILITIES.md, BUSINESS-AGENT-WORKFLOW.md) and being able to actually invoke one. Deliberately thin -- per EXECUTION-ADAPTER-SPEC.md section 3, no platform gets its own version of a workflow document, so these files point at the real specs rather than restating them.

- [.claude/agents/business-agent.md](https://github.com/manalimatkar/product-management/blob/main/.claude/agents/business-agent.md) - a real Claude Code subagent definition for `ROLE-006`: declared tool access, and instructions that point at BUSINESS-AGENT-WORKFLOW.md, AGENT-RESPONSIBILITIES.md, EVIDENCE-SPEC.md, and the relevant templates, plus the hard constraints restated for safety.
- [.claude/skills/verify-design-analysis/SKILL.md](https://github.com/manalimatkar/product-management/blob/main/.claude/skills/verify-design-analysis/SKILL.md) - checks a Design Analysis's internal traceability (every ID-only heading unique, every link resolves, every evidence entry has an inbound citation), backed by `.github/scripts/verify_design_analysis.py`. Run after drafting or revising any Design Analysis, before opening or updating its review PR.
- `.claude/skills/verify-registries/SKILL.md` - the cross-repo sibling: checks the Journey/Capability/Business Rule registries and every Design Analysis that cites them are consistent, backed by `.github/scripts/verify_registries.py`. Run after touching a registry or record, or citing a new product-level ID. *(Not linked -- still only on the local `agents` branch, not pushed anywhere yet, so there's nowhere real to point to. Becomes a link, matching the others above, once it merges to `main`.)*
- [.claude/skills/run-gate-checks/SKILL.md](https://github.com/manalimatkar/product-management/blob/main/.claude/skills/run-gate-checks/SKILL.md) - runs the right merge gate (`design_branch_gate`, `bundle_gate`, or `business_pr_gate`) against a real PR or a local diff, backed by `.github/scripts/run_gate_checks.py`. Run before asking for a PR to be opened whenever the change touches a native design export, a hand-authored bundle, or a Business PR.
- [.claude/skills/resolve-review-decisions/SKILL.md](https://github.com/manalimatkar/product-management/blob/main/.claude/skills/resolve-review-decisions/SKILL.md) - turns a Design Analysis review PR's comments into recorded resolutions (new Observations, updated Decisions and Requirements), backed by `.github/scripts/fetch_review_comments.py`. Fetches comments with real context; matching a comment to what it answers stays a human-supervised reading step, never automated.

## Current Status

This repository currently defines the product model and workflow. Specific implementation choices such as artifact formats, GitHub object mapping, automation runtime, and agent runtime remain design decisions for the next stage.
