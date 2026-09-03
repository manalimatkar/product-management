# Requirements Versioning Specification

## 1. Purpose

This specification defines how Business Requirements are identified, versioned, approved, changed, superseded, and referenced by downstream product and delivery artifacts.

Versioning must preserve the exact business intent that was reviewed and approved at each point in time. No downstream work may rely on an ambiguous or silently changed requirement.

## 2. Scope

This policy applies to Business Requirements and their associated requirement sets. The same principles may be adopted by other configured artifact types.

It does not define source-material versioning, technical implementation versioning, or a particular repository platform. Platform-specific storage and review mechanisms are defined by the active framework configuration.

## 3. Two Levels of Identity

Requirements use two separate identities:

### Requirement Identity

A stable Requirement ID identifies the continuing business concept across revisions.

Example: `BR-014`

The ID remains stable when the requirement is clarified without changing its business meaning. It must not be reused for an unrelated requirement.

### Requirement Set Version

A Requirements Version identifies the complete set of requirements reviewed together.

Example: `REQSET-003 v1.2`

Every requirement set version records the included requirement IDs and the exact source and analysis versions used.

## 4. Version Format

The default version format is semantic document versioning:

```text
MAJOR.MINOR
```

Examples:

- `1.0`: first approved or baseline requirements set
- `1.1`: compatible clarification or additive change that does not alter approved business intent
- `2.0`: material change that affects approved scope, outcome, policy, acceptance behavior, or downstream impact

Draft iterations before approval may use:

```text
0.1, 0.2, 0.3
```

A product configuration may use another format, but it must preserve the distinction between artifact identity, artifact version, requirement identity, and approval revision.

## 5. Version Assignment

The requirements producer assigns a new version when:

- the artifact is first created
- a reviewer requests a change
- a source or analysis version changes
- a requirement is added, removed, split, merged, or materially rewritten
- a business rule, decision, assumption, dependency, or acceptance criterion changes
- a change affects downstream work

Versions must increase monotonically. A version must never be changed after approval; a later version must be created instead.

## 6. Change Classification

Every revision records its change level.

| Change Level | Meaning | Examples | Version Change | Approval Effect |
| --- | --- | --- | --- | --- |
| Editorial | No change to meaning | Grammar, formatting, broken link correction | Patch or repository revision | Existing approval may remain valid if configured |
| Minor | Meaning remains compatible | Clarification, added evidence, non-binding detail | Increment MINOR | Reviewer confirms whether re-approval is needed |
| Major | Approved intent or impact changes | Scope, outcome, policy, actor, rule, acceptance behavior, or dependency change | Increment MAJOR | Prior approval expires; re-review required |

If classification is uncertain, treat the change as Major until the configured authority decides otherwise.

## 7. Requirement-Level Change Rules

| Change | Requirement ID | Required Action |
| --- | --- | --- |
| Editorial wording only | Preserve | Record editorial revision |
| Clarification with same meaning | Preserve | Record evidence and rationale |
| New independent behavior | New ID | Add requirement and map its evidence |
| Requirement removed from scope | Preserve | Mark `Superseded` or `Withdrawn`; do not delete history |
| Requirement meaning changes | Preserve or create successor ID | Record relationship and impact; re-review |
| Requirement split | Retain original history | Create new IDs and map them to the predecessor |
| Requirements merged | Retain predecessor history | Select successor ID and record all predecessors |
| Unrelated replacement | New ID | Never reuse an old ID |

A stable ID should be retained when a reviewer can still recognize the same business obligation or outcome. Create a successor ID when retaining the ID would conceal a material change in identity or intent.

## 8. Required Version Record

Each requirements version must record:

| Field | Requirement |
| --- | --- |
| Requirements Set ID | Stable identifier |
| Requirements Version | Version being recorded |
| Change Level | Editorial, Minor, or Major |
| Status | Draft, In Review, Approved, Superseded, Withdrawn, or Rejected |
| Previous Version | Immediate predecessor or `None` |
| Source Version(s) | Exact source versions |
| Analysis Version(s) | Exact analysis versions, when applicable |
| Changed By | Person, agent, or system identity |
| Changed At | Timestamp |
| Change Summary | Concise description |
| Change Reason | Review, source change, decision, defect, or other reason |
| Affected Requirements | Requirement IDs |
| Affected Downstream Items | Story, work-item, or delivery IDs |
| Approval Reference | Approval for this exact version or `Pending` |

## 9. Approval and Validity

Approval applies to one exact Requirements Version, not to the requirements set indefinitely.

Approval becomes invalid or requires confirmation when:

- a Major change is made
- a source or analysis change alters business meaning
- an assumption becomes a different business decision
- a requirement, rule, outcome, or acceptance criterion changes materially
- a downstream item is affected in a way defined as material by configuration
- an approval condition is no longer true

Editorial changes may retain approval only when the configured approval policy permits it and the audit record confirms that meaning was unchanged.

An agent may prepare a new version, but it may not create approval evidence on behalf of the configured human authority.

This Major/Editorial classification is also reused, unchanged, by [DESIGN-ANALYSIS-REVIEW-SPEC.md](DESIGN-ANALYSIS-REVIEW-SPEC.md) section 18 to route review *depth* (a lightweight, time-boxed path for Editorial revisions vs. the full review path for Material ones) and by [BUSINESS-AGENT-WORKFLOW.md](BUSINESS-AGENT-WORKFLOW.md) section 8.1 to route re-run scope after `Changes Requested` -- one test, two consumers, never a second competing definition.

## 10. Downstream References

Every downstream artifact that depends on a Business Requirement must reference:

- Requirements Set ID
- Requirements Version
- Requirement ID or IDs
- source and analysis versions when required by configuration

A reference must identify the approved version used, not merely the latest file or a mutable path.

When a requirements version is superseded:

1. Identify affected downstream items.
2. Mark each item as unaffected, review required, blocked, or superseded.
3. Reopen the applicable review or approval gate.
4. Prevent new downstream work from using an invalid version.
5. Preserve links to the previously approved version for audit.

## 11. History and Storage

The active platform configuration defines where versions are stored. Regardless of platform, the history must support:

- immutable or recoverable prior versions
- comparison between adjacent versions
- the identity of the change author
- timestamped change reasons
- approval evidence for each approved version
- links to affected source, analysis, and downstream artifacts
- supersession and successor relationships

Deleting an approved version is prohibited unless a documented retention policy requires removal and preserves an auditable deletion record.

## 12. Review Workflow

```text
Draft v0.x
   |
   v
Configured Review
   |---- Changes Requested ----> New Draft Version
   |
   v
Approved v1.x
   |
   |---- Compatible change ----> Review v1.x or v1.(x+1)
   |
   |---- Material change ------> Review v2.0
   |
   v
Superseded by later approved version
```

The active configuration determines whether Business Requirements are approved separately or as part of a larger review package.

## 13. Versioning Quality Gate

A requirements version is ready for approval only when:

- its set ID and version are unique
- the predecessor is identified
- every changed requirement is listed
- change level and rationale are recorded
- source and analysis versions are recorded
- affected downstream items are identified
- traceability remains complete
- approval scope is explicit
- unresolved decisions and assumptions remain visible
- the artifact does not silently alter approved business intent

## 14. Examples

### Minor Clarification

`BR-014 v1.0` states that a user can submit a request. `v1.1` clarifies the wording to identify the submitting role without changing the outcome or scope. The Requirement ID remains `BR-014`.

### Major Scope Change

`BR-014 v1.0` allows a manager to approve a request. A later decision allows both managers and delegates to approve it. This changes authority and policy, so the requirements set becomes `v2.0`, approval is reopened, and affected Stories and Tasks require impact review.

### Requirement Split

`BR-020 v1.0` combines submission and cancellation. The review separates them into `BR-020` and `BR-021`. The history records that both requirements originated from `BR-020 v1.0`.

## 15. Open Decisions

- Should the active configuration require semantic versions or permit date-based versions?
- Which editorial changes may retain approval without reviewer confirmation?
- What downstream changes are material enough to block work automatically?
- Which platform mechanism provides immutable version references?
- How long must superseded and withdrawn versions be retained?
