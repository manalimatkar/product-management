# Technical Handoff

## Purpose
This document defines the flow from an approved business package to canonical technical Tasks in the business repository and implementation in engineering repositories.

See [TECHNICAL-AGENT-WORKFLOW.md](TECHNICAL-AGENT-WORKFLOW.md) for the detailed, ordered, step-by-step Technical Agent procedure this document's rules feed into, mirroring how BUSINESS-AGENT-WORKFLOW.md relates to BUSINESS-REPOSITORY-WORKFLOW.md.

## Entry Condition
The Technical Agent may begin only when a GitHub Action verifies that:

1. the Business PR has been merged into the business repository
2. the Business Owner approval is recorded on that PR
3. the merged Epic and Stories are available
4. the handoff identifies the relevant engineering repository or repositories

The Technical Agent must not treat a draft, open, rejected, or unapproved Business PR as a valid handoff.

## Technical Agent Analysis
The Technical Agent reads:

- the merged Epic and Stories
- business requirements and acceptance criteria
- recorded decisions, assumptions, and dependencies
- relevant engineering repository code and documentation
- existing architecture and implementation constraints

It enriches canonical Tasks and Spikes in the business repository with:

- affected engineering repositories
- implementation approach
- technical findings and implementation guidance
- dependencies and sequencing
- required spikes or investigations
- architecture impacts
- testing and quality considerations
- unresolved technical risks

The Task is the handoff contract between agents. A separate Technical Plan document is optional and should be used only when the scope requires more detail than the canonical Tasks can contain.

Any optional Technical Plan is a proposal until approved by an Architect. Where no separate plan is needed, the Architect approves the technical detail on the canonical Tasks and Spikes.

## Architect Review Gate
The Architect reviews the technical decomposition on the canonical Tasks for feasibility and consistency with the engineering repositories. The Architect may:

- approve the technical decomposition
- request revisions
- reject the plan with rationale

Architect approval does not replace Business Owner approval. Business Owner approval authorizes technical analysis; Architect approval makes the canonical Tasks technically ready for development.

See [CANONICAL-TASK-SPEC.md](CANONICAL-TASK-SPEC.md) for the structured Task and Spike schema, the status-versus-technical-readiness distinction, and the Architect review gate implementing this section.

## Canonical Tasks
After Architect approval, the canonical Tasks remain in the business repository and become available to the Developer Agent. Each Task must include durable references to:

- the business repository
- the Business PR
- the Epic
- the source Story
- technical findings and implementation guidance
- the target engineering repository

Tasks are not copied into engineering repositories. A Story may produce multiple Tasks targeting different applications or repositories.

## Design Handoff Bundle
For UI work, the UX designer creates the UI pages in Claude Design and commits versioned application-specific design handoff documents before business analysis. The committed bundle remains in the business repository as a first-class design artifact. It must link to the canonical Story and Task and be referenced by the Developer Agent; the Business Agent and Technical Agent must not regenerate or rewrite it.

Canonical Tasks must preserve the business context and acceptance criteria needed by the Developer Agent.

## Engineering Repository Boundary
The engineering repository owns:

- code
- tests
- architecture documentation
- implementation PRs
- CI/CD
- engineering quality gates

The engineering repository does not redefine the approved business scope. Any material scope change must be sent back through the business-repository process.

## Developer Agent Entry Condition
The Developer Agent may act only on a technically ready canonical Task with an identified target engineering repository. It then works within the engineering repository's normal branch, PR, review, CI/CD, and quality-gate process.

## Failure and Blocking Conditions
The handoff must stop when:

- Business Owner approval cannot be verified
- the Business PR is not merged
- required business artifacts are missing
- the Technical Plan is incomplete or not approved
- target repository information is unavailable
- required traceability links cannot be created

A blocked handoff must be visible and must include a reason.

## Required Traceability Chain

```text
Source design or instruction
  -> Business Requirement
  -> Epic
  -> Story
  -> Business PR
  -> Business Owner Approval
  -> Business PR Merge
  -> Canonical Task with technical detail
  -> Architect Approval
  -> Design Handoff Bundle, where applicable
  -> Developer Agent
  -> Implementation PR
  -> Code and Tests
```
