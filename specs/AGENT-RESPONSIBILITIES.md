# Agent Responsibilities

## Purpose
This document defines the responsibilities and boundaries of the agents in the product-development system. It does not define the implementation of any particular model or automation engine.

## Design Analysis Agent

See [DESIGN-ANALYSIS-AGENT-WORKFLOW.md](DESIGN-ANALYSIS-AGENT-WORKFLOW.md) for the ordered procedure this responsibility list applies to.

### Responsibility
Analyze approved, ready source material and document what was designed and what it means -- the Design Analysis -- without adding to or improving the design.

### May

- read approved, ready source inputs
- identify business goals, users, outcomes, flows, capabilities, behaviors, information, and business rules represented by the design
- create or update Journey, Capability, and Business Rule records and their registry rows
- record observations, assumptions, gaps, decisions required, technical unknowns, and scope boundaries
- prepare the Design Analysis review PR
- revise the Design Analysis in response to review feedback

### May not

- draft Business Requirements, Epics, Stories, or a Business PR
- invent behavior, rules, or states the source doesn't show
- resolve a Decision Required item on its own reasoning
- approve or merge the Design Analysis review PR
- impersonate the Business Owner
- modify the source material

## Business Agent

See [BUSINESS-AGENT-WORKFLOW.md](BUSINESS-AGENT-WORKFLOW.md) for the ordered procedure this responsibility list applies to.

### Responsibility
Turn an approved Design Analysis into reviewable business scope in the business repository: Business Requirements, Epics, Stories, Acceptance Criteria, and the Business PR.

### May

- read an approved Design Analysis and the records it cites
- draft business requirements
- create or update Epics and Stories
- propose acceptance criteria
- carry forward assumptions, decisions, dependencies, and open questions
- update the source Design Analysis's forward links (`Related Epic`, `Related Stories`)
- prepare a Business PR
- revise content in response to review feedback

### May not

- start from a Design Analysis that hasn't passed its review gate
- re-analyze source material, or edit the Design Analysis's content
- approve the Business PR
- impersonate the Business Owner
- merge the Business PR
- trigger technical analysis before the Business PR is approved and merged
- create engineering-repository issues directly

## Technical Agent

### Responsibility
Translate approved Stories into canonical technical Tasks and Spikes in the business repository, using the relevant engineering repositories as context.

### May

- read merged business artifacts
- inspect engineering repository structure and existing implementation context
- identify impacted repositories and areas
- enrich canonical Tasks and Spikes with technical findings and implementation guidance
- identify target applications and repositories
- identify technical dependencies, risks, and spikes
- produce or update optional technical planning detail when a Task needs it
- submit the Task decomposition for Architect review
- mark Tasks technically ready only after Architect approval

### May not

- analyze or act on unapproved business scope as an authorized handoff
- alter Business Owner approval
- merge the Business PR
- treat its own technical detail as approved
- mark Tasks technically ready before Architect approval
- create duplicate Tasks in engineering repositories
- implement code as a substitute for Developer Agent responsibility

## Developer Agent

### Responsibility
Implement a technically ready canonical Task in the target engineering repository.

### May

- read the linked canonical Task and its design handoff bundle, where applicable
- modify code and tests within task scope
- update architecture documentation when required by the task
- open implementation PRs
- respond to code-review feedback
- report implementation status and blockers

### May not

- create duplicate planning work in the engineering repository
- change business scope or Business Owner approval
- approve the Technical Plan
- bypass engineering-repository CI/CD or quality gates
- expand task scope without returning the change for review

## Human Authorities

### Business Owner
Approves the Design Analysis, which authorizes the Business Agent to derive Business Requirements from it. Approves the Business PR containing the Epic and Stories, which authorizes technical analysis after merge.

### Architect
Reviews and approves the Technical Plan. This authorizes creation of engineering issues.

### Engineering Reviewer
Reviews implementation PRs in the engineering repository and applies repository quality gates.

## Gate Summary

| Action | Required authority or condition |
| --- | --- |
| Create Design Analysis | Design Analysis Agent may draft, from ready source material |
| Merge Design Analysis review PR | Business Owner approval |
| Start Business Agent | Merged, approved Design Analysis |
| Create Epic and Stories | Business Agent may draft |
| Merge Business PR | Business Owner approval |
| Start Technical Agent analysis | Merged Business PR with Business Owner approval |
| Create Technical Plan | Technical Agent after business handoff |
| Make canonical Task technically ready | Architect approval of technical decomposition |
| Implement code | Developer Agent with technically ready canonical Task |
| Merge implementation PR | Engineering repository review and quality gates |

## Audit Requirement
Each agent action must identify the agent role, target artifact, source artifact, timestamp, and resulting change. Human approvals must identify the approving person and the artifact version reviewed.
