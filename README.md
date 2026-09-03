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

## Agents and Responsibilities

### Business Agent

- reads the approved design handoff bundle
- produces Design Analysis
- identifies capabilities, user intent, and behavior
- drafts business requirements, Epics, Stories, and acceptance criteria
- identifies business rules, assumptions, and open decisions
- prepares a Business PR

The Business Agent does not make technical architecture decisions, approve business scope, or merge the Business PR.

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

Organized 2026-09-01 (see ARTIFACT-STORAGE-SPEC.md for how generated instances under `sources/`, `design/`, `analysis/`, `requirements/`, `business-prs/`, `tasks/` are organized separately from these framework documents).

### Root

- [PRD.md](PRD.md) - product definition, goals, requirements, and constraints
- [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md) - implementation roadmap and delivery phases
- [SOURCE-REGISTRY.md](SOURCE-REGISTRY.md) - the running index of every registered source

### specs/ -- the rules each artifact type and process must follow

- [BUSINESS-REPOSITORY-WORKFLOW.md](specs/BUSINESS-REPOSITORY-WORKFLOW.md) - business-stage workflow and Business Owner gate
- [DESIGN-HANDOFF-BUNDLE-SPEC.md](specs/DESIGN-HANDOFF-BUNDLE-SPEC.md) - Design Handoff Bundle schema, manifest, and design/implementation boundary
- [DESIGN-ANALYSIS-SPEC.md](specs/DESIGN-ANALYSIS-SPEC.md) - Design Analysis structure, evidence, and Business Agent inference rules
- [DESIGN-ANALYSIS-REVIEW-SPEC.md](specs/DESIGN-ANALYSIS-REVIEW-SPEC.md) - analysis intake, validation, review, approval, and change process
- [PRODUCT-SOURCE-MATERIAL-SPEC.md](specs/PRODUCT-SOURCE-MATERIAL-SPEC.md) - source registration, authority, versioning, readiness, and change handling
- [ARTIFACT-STORAGE-SPEC.md](specs/ARTIFACT-STORAGE-SPEC.md) - single naming and folder convention for every generated artifact type
- [GITHUB-PLATFORM-ADAPTER-SPEC.md](specs/GITHUB-PLATFORM-ADAPTER-SPEC.md) - the chosen GitHub-light platform adapter: how every artifact maps onto Issues, PRs, and labels
- [BUSINESS-REQUIREMENTS-SPEC.md](specs/BUSINESS-REQUIREMENTS-SPEC.md) - Business Requirements structure, boundaries, evidence, and lifecycle
- [BUSINESS-PR-SPEC.md](specs/BUSINESS-PR-SPEC.md) - Business PR minimum content, the controlled Design-to-Story transformation, and the required Stage Trace
- [EVIDENCE-SPEC.md](specs/EVIDENCE-SPEC.md) - the evidence rule: classification quick reference and the required traceability chain from source to Task
- [REQUIREMENTS-VERSIONING-SPEC.md](specs/REQUIREMENTS-VERSIONING-SPEC.md) - requirement identity, versioning, approval validity, and change impact
- [ARTIFACT-RELATIONSHIP-MODEL.md](specs/ARTIFACT-RELATIONSHIP-MODEL.md) - the structural data model: artifact IDs, cardinality between every artifact type, and versioning propagation
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

## Current Status

This repository currently defines the product model and workflow. Specific implementation choices such as artifact formats, GitHub object mapping, automation runtime, and agent runtime remain design decisions for the next stage.
