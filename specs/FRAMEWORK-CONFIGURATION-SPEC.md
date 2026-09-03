# Framework Configuration Specification

## 1. Purpose

The product-development framework provides reusable rules for turning product intent into reviewed, traceable delivery work. Each product-development effort configures the framework for its own domain, people, artifacts, tools, and delivery model.

This configuration layer prevents the framework core from assuming that every product is design-led, user-interface based, Agile, GitHub-based, or organized around the same approval roles.

```text
Framework Core
  - evidence and traceability
  - artifact lifecycle
  - review and approval rules
  - authority boundaries
  - change management
        +
Product Configuration
  - source types
  - analysis modules
  - artifact types
  - lifecycle stages
  - roles and gates
  - platform adapters
  - delivery repositories
```

## 2. Scope

This specification defines the configuration required before applying the framework to a product, initiative, or change effort.

It does not define:

- a particular agent runtime or model
- application architecture
- implementation technology
- a mandatory project-management methodology
- the content of a specific product requirement

## 3. Configuration Principles

A product configuration must:

- make product-specific choices explicit
- distinguish required behavior from optional modules
- preserve human authority at configured approval gates
- define what agents may draft, change, or transition
- identify the evidence supporting each generated artifact
- retain version and change history
- support one or more downstream delivery repositories or systems
- avoid silently applying a default where a decision affects scope, risk, or authority

A configuration may use the framework defaults, replace them, or disable optional stages when the product context does not require them.

## 4. Configuration Metadata

| Field | Value |
| --- | --- |
| Configuration ID | `CONFIG-<number>` |
| Product or Portfolio | `<name>` |
| Configuration Version | `<version>` |
| Owner | `<person or role>` |
| Effective Date | `<date>` |
| Status | Draft / In Review / Approved / Superseded |
| Framework Version | `<framework version>` |
| Review Reference | `<review package or link>` |
| Approval Reference | `<approval event or Pending>` |

## 5. Product Context

### Product or Initiative Description

`<What product, service, process, platform, or change effort is covered?>`

### Primary Outcomes

- `<business or user outcome>`

### Product Domains

- `<domain, market, internal process, regulated area, or other context>`

### Constraints

- `<legal, regulatory, organizational, operational, or delivery constraint>`

### Exclusions

- `<areas not governed by this configuration>`

## 6. Source Configuration

Define which sources may initiate or inform analysis.

**This repository's filled-in default profile, decided 2026-09-01.** Source types are carried forward from [PRODUCT-SOURCE-MATERIAL-SPEC.md](PRODUCT-SOURCE-MATERIAL-SPEC.md) section 3, not reinvented here. Only Design material has actually been exercised (the `checkout` dry run); every other type is supported by the framework core but not yet required or registered against a real instance.

| Source Type | Required | Accepted Forms | Authority or Reliability | Owner | Handling Notes |
| --- | --- | --- | --- | --- | --- |
| Design material (Design Handoff Bundle) | Yes | The four shapes DESIGN-HANDOFF-BUNDLE-SPEC.md section 6.1 defines: fully detailed bundle, bare external-tool reference, written document with screenshots, AI-generated wireframes | Bundle's own `status`/`readiness` fields carry authority (DESIGN-HANDOFF-BUNDLE-SPEC.md section 7) | `ROLE-005` Producing Designer | The only source type this repository has registered a real instance of. Readiness assigned per `GATE-001`, combined with Bundle Acceptance (`GATE-002`) into one PR-merge event (GITHUB-PLATFORM-ADAPTER-SPEC.md section 6.1). |
| Product or business brief | No | vision statement, opportunity statement, business case | `ROLE-001` Business Owner, if enabled | Not yet assigned | Supported by the framework core; not yet used in this repository. |
| User or customer evidence | No | interviews, feedback, support cases | Source owner named at registration | Not yet assigned | Supported; not yet used. |
| Process material | No | procedures, workflows, operating models | Source owner named at registration | Not yet assigned | Supported; not yet used. |
| Policy or regulatory material | No | policy, regulation, contract | Highest-authority rule applies (section 6 below: legal/regulatory overrides internal preference) | Not yet assigned | Supported; not yet used. No regulatory analysis module is enabled either -- see section 7. |
| Domain or data material | No | glossary, domain model, data definitions | Source owner named at registration | Not yet assigned | Supported; not yet used. |
| Technical context | No | existing-system documentation, architecture constraints | `ROLE-002` Architect, if enabled | Not yet assigned | Supported; would typically be consumed by the Technical Agent stage rather than the Business Agent stage. |
| Instruction or change request | No | written request, approved change proposal | `ROLE-001` Business Owner | Not yet assigned | Supported; not yet used -- this repository's dry run began from a Design Handoff Bundle, not a written instruction. |
| Measurement or experiment evidence | No | metrics, hypotheses, results | Source owner named at registration | Not yet assigned | Supported; not yet used. No experiment/discovery analysis module is enabled either -- see section 7. |

The configuration must define:

- **how sources are registered**: PRODUCT-SOURCE-MATERIAL-SPEC.md section 8, using PRODUCT-SOURCE-MATERIAL-TEMPLATE.md and indexed in SOURCE-REGISTRY.md
- **how source identity and version are recorded**: PRODUCT-SOURCE-MATERIAL-SPEC.md sections 4-5 (`SRC-<number>` IDs, explicit version or `Not Versioned`)
- **which sources are authoritative when they conflict**: PRODUCT-SOURCE-MATERIAL-SPEC.md section 6's Authority Factor table; this repository's solo-operator instance (section 10 below) has not yet had a real conflict to apply it to
- **how inaccessible, incomplete, or unreadable sources are handled**: PRODUCT-SOURCE-MATERIAL-SPEC.md section 10's Completeness and Quality record, feeding a `Blocked` outcome at `GATE-001`
- **who may add, replace, or approve a source**: `ROLE-005` drafts and adds; `GATE-002` (`ROLE-004` final call) and `GATE-001` (`ROLE-009` mechanical) approve and ready it, per sections 10-11 above
- **how long source evidence is retained**: not yet configured beyond PRODUCT-SOURCE-MATERIAL-SPEC.md section 13's general rule -- this repository's own practice everywhere else is to keep superseded material, never delete it (ARTIFACT-STORAGE-SPEC.md section 7), and nothing establishes a reason to treat sources differently

## 7. Analysis Modules

The framework core analyzes intent, actors, outcomes, capabilities, rules, states, evidence, assumptions, and decisions. Additional modules may be enabled for a product context.

**This repository's filled-in default profile, decided 2026-09-01.** Modules are carried forward from [DESIGN-ANALYSIS-SPEC.md](DESIGN-ANALYSIS-SPEC.md) section 12's list, not reinvented here. Reviewer is `ROLE-001` Business Owner for every enabled module, per `GATE-003`'s Approval Authority (section 11 above) -- this repository does not yet configure a separate technical reviewer for any module (DESIGN-ANALYSIS-REVIEW-SPEC.md section 3's optional "Technical reviewer" row is unused).

| Module | Enabled | Required Inputs | Output | Reviewer |
| --- | --- | --- | --- | --- |
| General product analysis | Yes | Any registered, ready source | Design Analysis universal inventory (DESIGN-ANALYSIS-SPEC.md section 4.2) | `ROLE-001` |
| User-interface design analysis | Yes | Design Handoff Bundle | UI Design Inventory (DESIGN-ANALYSIS-SPEC.md section 4.3) | `ROLE-001` |
| Service or process analysis | No | Process sources | -- | -- |
| Regulatory or control analysis | No | Policy sources | -- | -- |
| Data or domain analysis | No | Domain sources | -- | -- |
| Experiment or discovery analysis | No | Research sources | -- | -- |

Only the two enabled modules are backed by a registered source type in section 6 above -- an unenabled module has no source to run against yet, not merely an unset flag. Enabling one later requires enabling its corresponding source type in section 6 first.

An optional module may add domain-specific fields, but it must preserve the core evidence, classification, decision, and traceability rules.

## 8. Lifecycle Configuration

Configure the stages used by this product effort.

**This repository's filled-in default profile, decided 2026-09-01.** The generic default lifecycle below maps directly onto this repository's own gates and artifacts -- it was never a separate design, just an unstated one until now. **These stages are this repository's kanban board columns**: an artifact instance (a feature, in practice) sits in exactly one stage at a time and moves forward only when that stage's Exit Condition is met, and -- consistent with a kanban rather than a batch/sprint model -- different features may sit in different stages concurrently, with no requirement that the whole repository advance together. Within a stage, each artifact's own `status` / `readiness` / `Technical Readiness` field (`Draft` / `In Review` / `Approved` / ... per each artifact-type spec) is the finer-grained column state a reader would actually see on a board. IMPLEMENTATION-PLAN.md's Phase 1 already names "project or Kanban views" as the intended visualization of this exact table -- unbuilt (it depends on a real platform adapter instance, e.g. GitHub Projects, which needs open item 8 resolved first), not a new gap.

| Stage ID | Stage Name | Purpose | Entry Condition | Exit Condition | Required Artifact | Enabled |
| --- | --- | --- | --- | --- | --- | --- |
| `STAGE-001` | Source Intake | Register source material and check it fit for analysis | Source submitted for registration | `readiness:` set to `Ready`, `Ready with Limitations`, or `Not Applicable` (`GATE-001`) | Source Material | Yes |
| `STAGE-002` | Analysis | Business Agent produces a Design Analysis from ready source material | `STAGE-001` exit condition met | Design Analysis passes its own quality checks and is ready for review (often combined into `STAGE-004`'s review, per DESIGN-ANALYSIS-REVIEW-SPEC.md section 17 and this repository's own BPR-001 precedent) | Design Analysis | Yes |
| `STAGE-003` | Business Definition | Business Requirements, Epic, and Stories are drafted from the analysis | Analysis reviewable per `STAGE-002` | Business PR assembled and ready for Business Owner review | Business Requirements, Epic, Stories | Yes |
| `STAGE-004` | Scope Review | Business Owner reviews and approves the Business PR | Business PR ready (section 9 quality gate, BUSINESS-PR-SPEC.md) | PR `status:` -> Approved and merged (`GATE-004`, combined with `GATE-003` by this repository's default) | Business PR | Yes |
| `STAGE-005` | Technical Definition | Technical Agent enriches canonical Tasks and Spikes with technical detail | Merged, approved Business PR (`STAGE-004` exit) | Architect reviews and approves (`GATE-005`) | Canonical Task / Spike | Yes |
| `STAGE-006` | Delivery Readiness | Task becomes available to a Developer Agent | Architect approval (`STAGE-005` exit) | `Technical Readiness:` -> Technical Ready | Technically Ready Task | Yes |
| `STAGE-007` | Implementation or Execution | Developer Agent implements the Task in its target engineering repository | Technically Ready Task (`STAGE-006` exit) | Implementation PR merged (`GATE-006`) | Implementation PR | Yes |
| `STAGE-008` | Outcome Validation | Validate delivered work against the approved design and business outcome | Implementation PR merged (`STAGE-007` exit) | Not defined | Not defined | **No** |

`STAGE-008` is disabled honestly, not by a considered trade-off: this framework currently has no compensating control for it anywhere in the pipeline, which is itself the gap already tracked as CLAUDE.md open item 11. The "skipping a stage must identify equivalent control" rule below is stated plainly as unsatisfied here rather than papered over with an invented one -- item 11 remains the place this gets designed, not this table.

The `checkout` dry run has cleared `STAGE-001` through `STAGE-004` for real (Business PR `BPR-001` approved 2026-08-31, per CLAUDE.md open item 7); `STAGE-005` onward remain illustrative-only, since no real engineering repository exists yet (open item 8).

A typical default lifecycle is:

```text
Source Intake
  -> Analysis
  -> Business Definition
  -> Scope Review
  -> Technical Definition
  -> Delivery Readiness
  -> Implementation or Execution
  -> Outcome Validation
```

The configuration must state whether a stage is required, optional, skipped, or repeated. Skipping a stage must include a reason and identify which other stage provides equivalent control.

This repository's filled-in default profile for this section and section 15 below is [ARTIFACT-RELATIONSHIP-MODEL.md](ARTIFACT-RELATIONSHIP-MODEL.md) -- the table above names the stages; that document names the artifacts and cardinality moving through them.

## 9. Artifact Configuration

Define the artifact types used by this product effort. The framework does not require every configuration to use Epics, Stories, Tasks, or Spikes.

| Artifact Type | Purpose | Required | Storage or System | Producer | Reviewer | Canonical ID Format |
| --- | --- | --- | --- | --- | --- | --- |
| `<business requirement>` | `<purpose>` | Yes/No | `<location/system>` | `<role/agent>` | `<role>` | `<format>` |
| `<initiative>` | `<purpose>` | Yes/No | `<location/system>` | `<role/agent>` | `<role>` | `<format>` |
| `<work item>` | `<purpose>` | Yes/No | `<location/system>` | `<role/agent>` | `<role>` | `<format>` |

For each artifact type, define:

- required fields
- allowed statuses
- versioning rules
- source and parent references
- approval requirements
- change and supersession behavior
- whether it is a file, issue, record, or external object
- which downstream artifacts it may create

## 10. Role Configuration

Roles are configured per product context. A role may be performed by a person, group, agent, or system, but authority must be attributable.

**This repository's filled-in default profile, decided 2026-09-01.** This is a solo-operator instance on a personal GitHub account (not an organization account) -- every human role below is currently held by the same person. Responsibilities and permissions are carried forward from AGENT-RESPONSIBILITIES.md and DESIGN-HANDOFF-BUNDLE-TEMPLATE.md's Bundle Acceptance table, not invented here.

| Role ID | Role Name | Identity | Responsibilities | May Draft | May Approve | May Transition | May Not Do |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ROLE-001` | Business Owner | Manali (manali.matkar@gmail.com; GitHub username: `manalimatkar`, repository live 2026-09-03 -- see CLAUDE.md open item 8) | Approves the Business PR; final authority on business scope | -- | Business PR (BUSINESS-PR-SPEC.md section 10); Epic/Story acceptance criteria | Business PR `status:` Draft -> Approved; `readiness:` -> Ready | Draft the Business PR it is reviewing; approve its own Business-Agent-drafted output without review |
| `ROLE-002` | Architect | Manali (same identity as ROLE-001) | Reviews and approves the Technical Plan / technical decomposition | -- | Technical Plan; Canonical Task and Spike technical-readiness (CANONICAL-TASK-SPEC.md section 9) | Canonical Task `tech-ready:` false -> true | Approve its own technical output without review; mark a Task technically ready before this review; bypass Business Owner approval |
| `ROLE-003` | Engineering Reviewer | Manali (same identity as ROLE-001) | Reviews Implementation PRs in the engineering repository; applies its quality gates | -- | Implementation PR merge | Implementation PR Open -> Merged | Change business scope or Business Owner approval; approve its own Developer-Agent-drafted output without review |
| `ROLE-004` | Design Reviewer | Manali (same identity as ROLE-001) | Reviews the Design Handoff Bundle for Bundle Acceptance (DESIGN-HANDOFF-BUNDLE-TEMPLATE.md) | -- | Design Handoff Bundle `status:` -> Approved | Bundle `status:` Draft -> Approved | Approve a bundle it produced as Producing Designer without a distinct, separately recorded review pass (see solo-operator note below) |
| `ROLE-005` | Producing Designer | Manali (same identity as ROLE-001) | Produces the Design Handoff Bundle | Design Handoff Bundle, screens, flows | -- | -- | Approve its own bundle in the Design Reviewer role without a distinct review pass |
| `ROLE-006` | Business Agent | agent | Transforms approved source material into business artifacts (AGENT-RESPONSIBILITIES.md) | Design Analysis, Business Requirements, Epic and Stories, Business PR | -- | -- | Approve or merge the Business PR; impersonate the Business Owner; trigger technical analysis before merge |
| `ROLE-007` | Technical Agent | agent | Translates approved Stories into canonical Tasks and Spikes | Canonical Task, Spike, technical planning detail | -- | -- | Mark a Task technically ready; alter Business Owner approval; merge the Business PR |
| `ROLE-008` | Developer Agent | agent | Implements a technically ready canonical Task | Implementation PR, code and tests within task scope | -- | -- | Approve its own Implementation PR; change business scope; bypass engineering CI/CD gates |
| `ROLE-009` | Compliance/Gate Assistant Agent | agent | Runs the mechanical completeness checklist already defined at each gate (DESIGN-HANDOFF-BUNDLE-TEMPLATE.md Part 4, DESIGN-ANALYSIS-REVIEW-SPEC.md section 12, BUSINESS-PR-SPEC.md section 9, CANONICAL-TASK-SPEC.md structural checks) and produces a pre-check report before the human reviewer's judgment pass; independent of the agent that drafted the artifact under review | Pre-check/checklist reports | Source Material readiness outcome only (PRODUCT-SOURCE-MATERIAL-SPEC.md section 9), when no authority conflict exists | -- | Make the final call at any gate that requires business, technical, or design judgment (Bundle Acceptance, Design Analysis Review, Business PR, Architect Review, Implementation PR); resolve an authority conflict or Decision Required item itself -- must escalate to Business Owner instead; substitute its pass for the accountable reviewer's approval |

The configuration must identify:

- **business or product authority**: `ROLE-001` Business Owner (Manali)
- **domain reviewers**: `ROLE-004` Design Reviewer (Manali)
- **technical or architecture authority**: `ROLE-002` Architect (Manali)
- **delivery authority**: `ROLE-003` Engineering Reviewer (Manali)
- **agents and their limited permissions**: `ROLE-006`/`ROLE-007`/`ROLE-008`/`ROLE-009`, per the May Draft / May Not Do columns above. `ROLE-009` is the one exception to "no agent role ever appears in a May Approve column" -- it may finalize the Source Readiness outcome (a data-completeness check, not a business/technical/design judgment), with a mandatory escalation to `ROLE-001` when authority can't be determined automatically. Every other agent role, including `ROLE-009` at every other gate, never approves.
- **separation-of-duty requirements**: none enforced between human roles -- this is a personal-account, single-operator instance, and `ROLE-001` through `ROLE-005` are the same identity. The sharpest case is `ROLE-004`/`ROLE-005`: the same person produces the Design Handoff Bundle and reviews it for Bundle Acceptance. `ROLE-009` (decided 2026-09-01, see section 11) partially mitigates this -- an agent independent of the Producing Designer now runs the completeness checklist before the human review, so the mechanical part of the review is no longer self-certified even though the final Approved call still is. This is accepted as a stated solo-operator default, not a structural recommendation -- if a second reviewer ever joins, Design Reviewer should be the first role reassigned, since design self-review is the weakest link in evidence classification (EVIDENCE-SPEC.md).
- **fallback authority when the primary reviewer is unavailable**: not defined -- there is only one identity to fall back to. Left open in section 19 below rather than invented.

An agent must not approve its own generated work unless the configuration explicitly permits it and records the associated control. No agent role above is granted that permission.

## 11. Approval Gate Configuration

Approval gates are configured controls, not assumptions about a particular organization.

**This repository's filled-in default profile, decided 2026-09-01.** Every gate below follows the same two-step shape: `ROLE-009` (Compliance/Gate Assistant Agent) runs the mechanical completeness checklist that the relevant spec already defines, then the accountable human or agent role in section 10 makes the actual approval call on what the checklist can't judge. `ROLE-009` never replaces the accountable authority -- it only removes the mechanical-checking part of that authority's workload, per the discussion that led to adding `ROLE-009` in section 10.

| Gate ID | Gate Name | Approval Authority | Applies To | Required Evidence | Transition Authorized | Failure or Rework Path |
| --- | --- | --- | --- | --- | --- | --- |
| `GATE-001` | Source Readiness Check | `ROLE-009` directly (data-completeness, not judgment); escalates to `ROLE-001` on an unresolved authority conflict | Source Material | Completed readiness checklist (PRODUCT-SOURCE-MATERIAL-SPEC.md section 9) | `readiness:` null -> Ready / Ready with Limitations / Blocked / Not Applicable | `Blocked` outcome recorded with the missing item; source owner corrects and resubmits |
| `GATE-002` | Design Handoff Bundle Acceptance | `ROLE-009` pre-check, `ROLE-004` Design Reviewer final call | Design Handoff Bundle | Completed Pre-Registration Checklist (DESIGN-HANDOFF-BUNDLE-TEMPLATE.md Part 4) + Design Reviewer sign-off | Bundle `status:` Draft -> Approved | Checklist gap or Changes Requested cited; Producing Designer revises, new version registered (never overwritten, ARTIFACT-STORAGE-SPEC.md section 7) |
| `GATE-003` | Design Analysis Review | `ROLE-009` pre-check, `ROLE-001` Business Owner final call | Design Analysis | Completed Review Checklist (DESIGN-ANALYSIS-REVIEW-SPEC.md section 12) | Analysis `status:` -> Approved / Changes Requested / Rejected / Blocked (section 11) | `Changes Requested`/`Rejected`/`Blocked` recorded with findings; Business Agent revises and resubmits |
| `GATE-004` | Business PR Review (Epic, Stories, Business Requirements) | `ROLE-009` pre-check (BUSINESS-PR-SPEC.md section 9 quality gate), `ROLE-001` Business Owner final call -- never delegable, see section 10 | Business PR | Passed section 9 quality gate + complete Stage Trace | PR `status:` -> Approved / Changes Requested / Rejected / Blocked (section 10) | Findings recorded; Business Agent revises and resubmits; four open Decisions from a prior review are not silently resolved by resubmission |
| `GATE-005` | Architect Review | `ROLE-009` pre-check (structural completeness -- dependencies, repo references, Stage-Trace-style consistency), `ROLE-002` Architect final call | Canonical Task / Spike | Completed structural checklist + Architect judgment on feasibility | `tech-ready:` false -> true (CANONICAL-TASK-SPEC.md section 9) | Findings recorded; Technical Agent revises and resubmits; `Blocked` records the unresolved dependency/spike/business decision |
| `GATE-006` | Implementation PR Review | `ROLE-009`-equivalent CI/quality-gate checks (once a real engineering repository exists, open item 8), `ROLE-003` Engineering Reviewer final call | Implementation PR | Passing engineering-repository CI/quality gates + Engineering Reviewer sign-off | Implementation PR Open -> Merged | Standard engineering-repository review/rework cycle; not otherwise specified by this framework |

Each required gate must define:

- **the artifact or transition being approved**: the "Applies To" and "Transition Authorized" columns above
- **the exact version under review**: every gate above ties to a specific artifact version, per the versioning/supersession rule already established in ARTIFACT-STORAGE-SPEC.md section 7 and REQUIREMENTS-VERSIONING-SPEC.md section 9 -- approval never silently carries forward to a later revision
- **the approving authority**: the "Approval Authority" column above; the accountable half never changes even when `ROLE-009` pre-checks
- **whether approval must be individual or collective**: individual at every gate -- this is a solo-operator instance (section 10), so collective approval does not apply yet
- **how approval is recorded**: in the artifact's own file, per each spec's existing Approval Recording section (e.g. CANONICAL-TASK-SPEC.md section 9, BUSINESS-PR-SPEC.md section 10/12) -- not solely as a GitHub PR review, per GITHUB-PLATFORM-ADAPTER-SPEC.md's files-stay-canonical principle
- **whether approval expires after a material change**: yes, uniformly -- a material change to the reviewed artifact invalidates prior approval and requires re-review, mirroring REQUIREMENTS-VERSIONING-SPEC.md section 9 and CANONICAL-TASK-SPEC.md section 9
- **what happens when approval is rejected or withdrawn**: the "Failure or Rework Path" column above; `Rejected` and `Blocked` are recorded with rationale/blocker rather than silently discarded, per each gate's own outcome vocabulary

## 12. Review Package Configuration

Define how artifacts are assembled for review.

**This repository's filled-in default profile, decided 2026-09-01.** One review package per gate defined in section 11 above -- this section names what each package actually contains; section 11 named who reviews it and what it authorizes.

| Review Package | Included Artifacts | Required Checks | Approval Gate | Publication or Merge Action |
| --- | --- | --- | --- | --- |
| Source Readiness Package | Source Material registration record | PRODUCT-SOURCE-MATERIAL-SPEC.md section 9 readiness checklist | `GATE-001` | Registry entry (or, for a Design Handoff Bundle, `bundle.md`'s own frontmatter, per GITHUB-PLATFORM-ADAPTER-SPEC.md section 6.1) updated with the `readiness:` outcome |
| Bundle Acceptance Package | Design Handoff Bundle (`bundle.md`, screens, flows) | DESIGN-HANDOFF-BUNDLE-TEMPLATE.md Part 4 Pre-Registration Checklist | `GATE-002` | Bundle `status:` Draft -> Approved, via the upload PR's merge (GITHUB-PLATFORM-ADAPTER-SPEC.md section 6.1) |
| Design Analysis / Business PR Review Package | Design Analysis, Business Requirements, Epic, Stories, Stage Trace -- combined into one package by this repository's default (DESIGN-ANALYSIS-REVIEW-SPEC.md section 17, exercised for real by `BPR-001`) | DESIGN-ANALYSIS-REVIEW-SPEC.md section 12 checklist + BUSINESS-PR-SPEC.md section 9 quality gate | `GATE-003` and `GATE-004` combined into one Business Owner decision | Business PR merge (BUSINESS-PR-SPEC.md section 11; GITHUB-PLATFORM-ADAPTER-SPEC.md section 6) |
| Architect Review Package | Canonical Task(s) / Spike(s), technical findings, dependencies | CANONICAL-TASK-SPEC.md section 9 structural checklist + Architect feasibility judgment | `GATE-005` | `Technical Readiness:` -> Technical Ready |
| Implementation Review Package | Implementation PR (code, tests) | The target engineering repository's own CI/CD and quality gates | `GATE-006` | Implementation PR Open -> Merged |

Every package above is a GitHub Pull Request, per GITHUB-PLATFORM-ADAPTER-SPEC.md section 13 -- except the Source Readiness and Bundle Acceptance packages, which are the same PR (the bundle's upload PR, section 6.1). This repository has not yet configured a review package that is a document review, workflow record, or ticket group instead of a PR; the option remains available per this section's closing paragraph below if a future artifact type doesn't fit the PR shape.

A review package must make visible:

- source evidence
- generated artifacts
- assumptions and unresolved decisions
- scope and exclusions
- impact of changes
- approval status and reviewed versions
- downstream implications

This repository's Business PR package satisfies all seven directly through BUSINESS-PR-SPEC.md section 8's Required Business PR Content list -- no separate mechanism was built to surface them a second time.

The package may be a pull request, document review, workflow record, ticket group, or another configured mechanism.

## 13. Platform and Storage Adapters

The framework core uses platform-neutral concepts. This section maps them to the tools used by the product effort.

This repository's default profile, decided 2026-08-31 ("GitHub-light" -- see [GITHUB-PLATFORM-ADAPTER-SPEC.md](GITHUB-PLATFORM-ADAPTER-SPEC.md) for the full mapping and rationale):

| Framework Concept | Platform or Tool | Representation | Authority Notes |
| --- | --- | --- | --- |
| Source registry | Git repository (this business repository) | Committed Markdown files under `sources/` (ARTIFACT-STORAGE-SPEC.md) | Files stay canonical; no GitHub-native object |
| Review package | GitHub Pull Request | The Business PR itself -- diff is the changed Design Analysis/Business Requirements files, description is the full PR content | Per BUSINESS-REPOSITORY-WORKFLOW.md's "GitHub review or equivalent attributable approval event" |
| Approval event | GitHub PR review | An "Approve" review by the Business Owner, plus the same decision recorded in the PR description's own Business Owner Decision table | Redundant by design -- the file-recorded decision is the durable one |
| Canonical work item | GitHub Issue | One Issue per Epic, Story, Task, and Spike (GITHUB-PLATFORM-ADAPTER-SPEC.md section 4) | Confirms PRD.md section 7.6 for Task/Spike; extends the same treatment to Epic/Story |
| Automation trigger | GitHub Action | Triggered on PR merge; verifies approval and Stage Trace completeness before invoking the Technical Agent (GITHUB-PLATFORM-ADAPTER-SPEC.md section 6) | Blocked on section 10 (Role Configuration) being filled in -- see that document's section 6 |
| Delivery repository | Engineering repository (separate from this business repository) | Implementation PRs reference the canonical Task by ID, per TECHNICAL-HANDOFF.md | Out of scope for the business-repository adapter itself |

GitHub PRs, Issues, Projects, and Actions may be used as an implementation adapter. They are not requirements of the framework core -- the table above is this repository's chosen instance, not a mandated default for every deployment of this framework.

This table maps *storage* adapters only -- where artifacts are tracked once produced. It has a sibling table for *execution* adapters -- which AI platform actually produces them -- in [EXECUTION-ADAPTER-SPEC.md](EXECUTION-ADAPTER-SPEC.md), added 2026-09-03. The two are independent: a stage executed on Claude, ChatGPT, or Copilot all write to the same storage adapter above, unchanged.

**Added 2026-09-03:** this repository now has a second long-lived branch, `design`, alongside `main` -- a raw landing zone for native Claude Design exports, with its own independent folder shape and its own merge gate (`.github/workflows/design-branch-intake.yml`), deliberately not governed by ARTIFACT-STORAGE-SPEC.md's storage convention above. See DESIGN-HANDOFF-BUNDLE-SPEC.md section 6.2, ARTIFACT-STORAGE-SPEC.md section 10, and GITHUB-PLATFORM-ADAPTER-SPEC.md section 6.1.

## 14. Delivery Configuration

Define where approved work is delivered.

**This repository's filled-in default profile, decided 2026-09-01.** The registration process is fully specified below; no concrete delivery target is registered yet, because no real engineering repository exists (CLAUDE.md open item 8 -- the same blocker already noted against GITHUB-PLATFORM-ADAPTER-SPEC.md sections 6 and 6.1). This is what PRD.md section 13's "how are engineering repositories registered, selected, and authorized" question was waiting on: registration is a row added to the table below once a real repository exists, following the process this section defines -- not a separate mechanism still to be designed.

| Delivery Target ID | Application, Service, or Process | Repository or System | Work Item Mapping | Responsible Role | Quality Gates |
| --- | --- | --- | --- | --- | --- |
| `TARGET-001` | *(none registered)* | *(none registered)* | Canonical Task references exactly one target, per ARTIFACT-RELATIONSHIP-MODEL.md section 7 ("Task-to-Implementation-PR (1:N, PR scoped to one Task)") | `ROLE-003` Engineering Reviewer, once a target exists | `GATE-006`, per that target's own engineering-repository CI/CD |

The configuration must support:

- **no delivery repository, where the effort ends at product definition**: exercised for real -- the `checkout` dry run stopped at an approved Business PR with no delivery target registered (CLAUDE.md open item 7)
- **one delivery target**: supported by the table above; not yet exercised against a real repository
- **multiple delivery targets for one business outcome**: supported by design, not by accident -- ARTIFACT-RELATIONSHIP-MODEL.md section 4's Story:Task 1:N cardinality exists specifically so "a Story may produce multiple Tasks targeting different applications or repositories" (CANONICAL-TASK-SPEC.md section 10), each with its own `TARGET-<id>` row once real
- **non-code delivery such as operations, policy, content, or process change**: supported in principle -- the framework core is explicitly domain-agnostic (section 2 above) and Delivery Target's "Application, Service, or Process" column already admits a non-code target; not yet exercised, since every artifact type this repository has actually built assumes an engineering repository downstream
- **target-specific technical review and quality gates**: `GATE-006` is defined once, generically, in section 11 above; each target's actual CI/quality checks are whatever that target's own engineering repository enforces -- this framework does not redefine them, per GITHUB-PLATFORM-ADAPTER-SPEC.md section 4's note that the Implementation PR is "out of scope for the business-repository adapter itself"

## 15. Traceability Configuration

Define the required lineage for the configured lifecycle.

```text
Source
  -> Analysis
  -> Business Definition
  -> Review Package
  -> Approval
  -> Delivery Work
  -> Outcome Evidence
```

The configuration must specify:

- required links between artifact types
- immutable identifiers used in links
- minimum traceability before each gate
- how missing or broken references are surfaced
- how one artifact maps to many downstream targets
- how downstream work maps back to the approved business version

## 16. Change and Version Configuration

Define what constitutes a material change.

**This repository's filled-in default profile, decided 2026-09-01.** Every row below consolidates a rule already defined elsewhere -- this section does not invent a new change-management policy, it names which existing rule governs each of the framework's four generic change types.

| Change Type | Example | Affected Artifacts | Re-review Required | Owner |
| --- | --- | --- | --- | --- |
| Source change | A Design Handoff Bundle is registered as a new version (e.g. v1.0 -> v1.1) | Design Analysis is reassessed for impact; everything built on it if conclusions change | Yes, if the change affects analysis conclusions; not automatic for an Editorial-only source change (PRODUCT-SOURCE-MATERIAL-SPEC.md section 12) | `ROLE-005` Producing Designer initiates; `ROLE-009`/`ROLE-004` assess impact at `GATE-002`/`GATE-001` |
| Outcome change | A business decision changes a stated success metric or desired outcome | Business Requirements and any Epic/Stories built to the prior outcome | Yes -- classified Major (REQUIREMENTS-VERSIONING-SPEC.md section 6) | `ROLE-001` Business Owner |
| Scope change | A requirement's authority or eligibility rule changes (REQUIREMENTS-VERSIONING-SPEC.md section 14's manager/delegate example) | Requirements Set (new `MAJOR` version), affected Stories and Tasks | Yes, always Major (REQUIREMENTS-VERSIONING-SPEC.md section 6) | `ROLE-001` Business Owner |
| Implementation change | Technical analysis finds the approved scope cannot be built as written (CANONICAL-TASK-SPEC.md section 8, "Scope Change During Technical Analysis") | Canonical Task marked `Blocked`, escalated back to the business-repository process rather than resolved unilaterally | Yes -- returns to Business Owner review, never resolved by the Technical Agent alone | `ROLE-002` Architect identifies; `ROLE-001` Business Owner re-decides |

The configuration must define how to:

- **create a new version**: REQUIREMENTS-VERSIONING-SPEC.md section 5; ARTIFACT-STORAGE-SPEC.md section 7 (a new artifact ID and a new file, never an overwrite)
- **identify impacted artifacts**: ARTIFACT-RELATIONSHIP-MODEL.md section 6's Versioning Propagation table -- the single consolidated place this repository already keeps this
- **preserve the previously approved version**: ARTIFACT-STORAGE-SPEC.md sections 7 and 9's non-destructive supersession rule, applied uniformly to every artifact type
- **withdraw or reopen downstream work**: REQUIREMENTS-VERSIONING-SPEC.md section 10; CANONICAL-TASK-SPEC.md section 12
- **record the reason, actor, and timestamp**: each artifact type's own Change/Version Record and Approval Recording fields (REQUIREMENTS-VERSIONING-SPEC.md section 8; CANONICAL-TASK-SPEC.md section 9's Approval Recording table)
- **validate that stale work cannot proceed unnoticed**: CANONICAL-TASK-SPEC.md section 12's step 5 is this repository's concrete mechanism -- "Do not allow a Developer Agent to begin or continue work on a Task whose upstream Story version has been superseded without re-review"

## 17. Quality and Completeness Rules

Before configuration approval, verify that:

- the product context and outcomes are clear
- allowed source types and authority are defined
- required analysis modules are selected
- lifecycle stages and skip rules are explicit
- artifact types and canonical identifiers are defined
- roles and separation of duties are documented
- approval gates identify authorities and reviewed versions
- review packages and rework paths are defined
- platform choices are mapped as adapters
- delivery targets and quality gates are known
- traceability requirements are complete
- material-change rules are explicit
- unresolved configuration decisions are visible

## 18. Framework Defaults for This Repository

The current repository provides a default product-development profile with these initial choices:

- versioned design handoff bundles are a supported source type
- Design Analysis and Business Requirements are separate artifacts
- Business Owner approval governs business scope
- Architect approval governs technical readiness
- the business repository is the planning system of record
- engineering repositories own implementation and delivery
- GitHub is the initial platform adapter
- Epics, Stories, acceptance criteria, Tasks, and Spikes are the initial delivery artifact types
- the lifecycle stages in section 8 are treated as kanban board columns (continuous flow, features advancing independently), not sprint-batched phases

These are defaults for this implementation, not universal framework requirements. A product configuration may replace them when its context requires a different model.

## 19. Open Configuration Decisions

- No fallback authority is defined for section 10's roles (solo-operator instance, one identity holds every human role) -- revisit if a second reviewer ever joins.
- `ROLE-004` Design Reviewer and `ROLE-005` Producing Designer are the same identity today, so Design Handoff Bundle review is self-review in practice -- accepted as a solo-operator default in section 10, not resolved as a structural recommendation.
- Which configuration fields must be machine-validated?
- Which framework defaults are mandatory controls rather than replaceable choices?
- How are configuration versions selected for a specific initiative?
- Who approves changes to an active configuration?
- How are platform adapters validated for equivalent approval and traceability behavior?
- What minimum evidence is required for non-design source types?
- Which optional analysis modules should be standardized first?
