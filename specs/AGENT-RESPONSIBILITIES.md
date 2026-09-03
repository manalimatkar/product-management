# Agent Responsibilities

## Purpose
This document defines the responsibilities and boundaries of the agents in the product-development system. It does not define the implementation of any particular model or automation engine.

## Business Agent

See [BUSINESS-AGENT-WORKFLOW.md](BUSINESS-AGENT-WORKFLOW.md) for the ordered, end-to-end procedure this responsibility list applies to.

### Responsibility
Transform source design and instruction files into structured product artifacts in the business repository.

### May

- read approved source inputs
- identify business goals, users, and outcomes
- draft business requirements
- create or update Epics and Stories
- propose acceptance criteria
- record assumptions, decisions, dependencies, and open questions
- prepare a Business PR
- revise content in response to review feedback

### May not

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
Approves the Business PR containing the Epic and Stories. This authorizes technical analysis after merge.

### Architect
Reviews and approves the Technical Plan. This authorizes creation of engineering issues.

### Engineering Reviewer
Reviews implementation PRs in the engineering repository and applies repository quality gates.

## Gate Summary

| Action | Required authority or condition |
| --- | --- |
| Create Epic and Stories | Business Agent may draft |
| Merge Business PR | Business Owner approval |
| Start Technical Agent analysis | Merged Business PR with Business Owner approval |
| Create Technical Plan | Technical Agent after business handoff |
| Make canonical Task technically ready | Architect approval of technical decomposition |
| Implement code | Developer Agent with technically ready canonical Task |
| Merge implementation PR | Engineering repository review and quality gates |

## Audit Requirement
Each agent action must identify the agent role, target artifact, source artifact, timestamp, and resulting change. Human approvals must identify the approving person and the artifact version reviewed.
