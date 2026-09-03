# Business Repository Workflow

## Purpose
The UX designer creates the design in Claude Design. The designer then commits versioned design handoff documents to the business repository, where the bundle becomes the input to the Business Agent process.

 The committed bundle may contain:
The versioned design handoff bundle is a first-class product artifact and must not be regenerated or rewritten by the Business Agent. Source inputs and design provenance should be retained or referenced so generated artifacts can be traced back to their origin.
## Inputs
The Business Agent may consume:

- Claude design files
Versioned Claude Design handoff bundle committed to repo
- written instructions
- PDFs
- screenshots
- mockups
- other approved product or design source material
 The Business Agent reads the committed design handoff bundle, produces a design analysis, and transforms the approved design context into a reviewable Business PR containing, as applicable:
Source inputs must be retained or referenced so generated artifacts can be traced back to their origin.

See [BUSINESS-AGENT-WORKFLOW.md](BUSINESS-AGENT-WORKFLOW.md) for the detailed, step-by-step Business Agent procedure this section summarizes.

## Workflow
The Business Agent may reference and associate the versioned design handoff bundle with the related Story and canonical Task, but must not regenerate or rewrite the bundle.
```text
Requirement or design input
        |
        v
Business Agent
        |
        v
Epic + Stories
        |
        v
Business PR
        |
        v
Business Owner Approval
        |
        v
Merge into business repository
        |
        | GitHub Action
        v
Technical Agent
```

## Business Agent Output
The Business Agent transforms source material into a reviewable Business PR containing, as applicable:

The Business Agent may draft and revise these artifacts. It may not approve them or merge the Business PR.

See [BUSINESS-PR-SPEC.md](BUSINESS-PR-SPEC.md) for the required minimum content of the Business PR, including the controlled Design-to-Story transformation and the Stage Trace that makes it reviewable.

## Business Owner Gate
The Business Owner reviews the Business PR as a coherent product scope package. Approval confirms that:

The business repository owns product intent, planning artifacts, canonical Tasks, and design handoff bundles. It does not own implementation code, tests, CI/CD, or engineering-repository quality gates. Engineering repositories reference the canonical Task and design bundle rather than receiving copied planning content.
- the business problem and desired outcome are understood
- the Epic and Stories represent the intended scope
- acceptance criteria are sufficient for technical analysis
- known decisions, assumptions, and dependencies are visible
- the content is ready for technical decomposition

The Business Owner approval must be represented by a GitHub review or equivalent attributable approval event. A Business PR cannot be merged as an approved input to the Technical Agent without this approval.

## Merge as the Handoff Trigger
Merge is the explicit boundary between business planning and technical analysis. A GitHub Action may invoke the Technical Agent only after it verifies that:

- the Business PR is merged
- required Business Owner approval exists
- the merged artifacts are available in the business repository
- the event identifies the relevant Epic and Stories

A comment, draft PR, or unapproved branch must not trigger technical analysis.

## Ownership Boundary
The business repository owns product intent and planning artifacts. It does not own implementation code, tests, CI/CD, or engineering-repository quality gates.

## Acceptance Criteria
The business workflow is complete when a reviewer can identify:

- the original source input
- the Business Agent output
- the Business PR
- the approving Business Owner
- the merge event that authorized technical analysis
