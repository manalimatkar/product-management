# Product Source Material Specification

## 1. Purpose

This specification defines the source-material contract for product analysis. It ensures that agents receive identifiable, versioned, authoritative, and reviewable inputs before producing a Design Analysis or another configured analysis artifact.

The framework supports many source types. A visual Design Handoff Bundle is one optional source type, not a requirement for every product-development effort.

```text
Registered Source Material
        |
        v
Source Readiness Check
        |
        v
Configured Product Analysis
        |
        v
Business Requirements and Downstream Work
```

## 2. Scope

This specification covers:

- source registration
- source identity and versioning
- source authority and ownership
- accepted source types and formats
- completeness and readability checks
- source conflicts and limitations
- references from analysis artifacts
- source changes and supersession

It does not define how agents interpret sources. Analysis behavior is defined by the applicable analysis specification and review process.

## 3. Supported Source Types

A product configuration selects the source types relevant to its context.

| Source Type | Examples | Typical Use |
| --- | --- | --- |
| Product or business brief | vision, opportunity statement, business case | goals and outcomes |
| User or customer evidence | interviews, feedback, research, support cases | needs and problems |
| Design material | UI designs, service blueprints, prototypes, mockups | intended behavior and experience |
| Process material | procedures, workflows, operating models | operational behavior and handoffs |
| Policy or regulatory material | policy, regulation, control, contract | obligations and constraints |
| Domain or data material | glossary, domain model, data definitions | concepts and relationships |
| Technical context | existing-system documentation, architecture constraints | implementation context and boundaries |
| Instruction or change request | written request, approved change proposal | requested scope and intent |
| Measurement or experiment evidence | metrics, hypotheses, results | outcomes and learning |
| Other configured source | `<description>` | `<purpose>` |

A source type must not be treated as authoritative merely because it is listed as supported. Authority is determined by the active product configuration and source metadata.

## 4. Source Metadata

Every registered source must include:

| Field | Requirement |
| --- | --- |
| Source ID | Stable identifier, such as `SRC-001` |
| Source Name | Human-readable name |
| Source Type | Configured source category |
| Location | Repository path, URL, system reference, or attachment ID -- for a native Claude Design export on the `design` branch, a `branch`/`path`/commit-SHA pointer (ARTIFACT-STORAGE-SPEC.md section 10) rather than a `main`-relative path |
| Version | Explicit version or `Not Versioned` |
| Status | Draft, Active, Superseded, Withdrawn, or Unavailable |
| Owner | Person, role, team, or external authority |
| Authority Level | Authority defined by product configuration |
| Created At | Source creation timestamp when known |
| Effective At | Date the source becomes applicable when relevant |
| Registered By | Person, agent, or system |
| Registered At | Registration timestamp |
| Access Notes | Access restrictions or retrieval instructions |

A source reference must be durable enough for a reviewer or agent to locate the exact material used by an analysis.

## 5. Source Versioning

A source is versioned whenever its meaning, scope, authority, or applicable content changes.

The source owner should use a clear version format, such as:

```text
v1.0, v1.1, v2.0
```

or another configured convention. The version must not be silently changed after an analysis references it.

A new source version must record:

- predecessor version
- change summary
- change reason
- changed sections or content
- effective date
- affected analysis and downstream artifacts
- whether prior approvals remain valid

A source marked `Not Versioned` must still have a retrieval timestamp or equivalent identity record so the analysis can state what was reviewed.

## 6. Source Authority

When multiple sources address the same subject, the product configuration must define how authority is determined.

| Authority Factor | Example |
| --- | --- |
| Legal or regulatory authority | applicable regulation overrides internal preference |
| Approved business decision | recorded decision overrides an unapproved suggestion |
| Effective date | current policy overrides expired policy |
| Named source owner | designated owner controls the source |
| Approval status | approved material overrides draft material |
| Scope | source applies only to its defined product or domain |

If authority cannot be determined, the agent must record a conflict or Decision Required item. It must not silently select a source.

## 7. Optional Design Handoff Bundle

When UI or other design material is used, the product configuration may enable a Design Handoff Bundle as a structured source.

A Design Handoff Bundle may contain:

- design purpose and scope
- screens, pages, or views
- user journeys and flows
- interaction and behavior notes
- states and edge cases
- assets and content guidance
- accessibility or experience requirements
- links to external design tools
- version and change notes

The bundle must identify:

- bundle ID
- bundle version
- producing designer, team, or source owner
- related product or initiative
- included files and folders
- external references
- known limitations
- approval or acceptance status

The Business or product agent consumes the bundle and references it. It must not silently regenerate, rewrite, or replace the authoritative source.

See [DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md](DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md) for the structured schema and file templates implementing this section.
See [PRODUCT-SOURCE-MATERIAL-TEMPLATE.md](../templates/PRODUCT-SOURCE-MATERIAL-TEMPLATE.md) and [SOURCE-REGISTRY.md](../SOURCE-REGISTRY.md) for the fillable registration record and running index this section requires.

## 8. Registration and Intake

Before analysis begins, the source owner or configured intake process must:

1. Register each source and assign a stable Source ID.
2. Record its type, location, version, owner, and authority.
3. Confirm that the agent can access the source.
4. Record any access, format, or completeness limitation.
5. Identify related sources and expected conflicts.
6. Associate the source with the product, initiative, or change effort.
7. Select the analysis modules that may consume it.

Sources may be added during analysis only when the new source is registered, versioned, and its effect on existing conclusions is assessed.

## 9. Readiness Checks

A source set is ready for analysis when:

- the product or initiative is identified
- required source types are present
- each source has a stable identity
- exact versions or retrieval identities are recorded
- access is confirmed
- sources are readable enough for their intended use
- authority and effective status are known
- known conflicts are recorded
- limitations are visible
- the requested outcome or question is stated

For a native Claude Design export, this check is run mechanically by `.github/workflows/design-branch-intake.yml` on merge into the `design` branch, per DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md section 6.2 -- readiness is computed the same way (limitations present or absent) as for any other source, just derived from the export's own README.md rather than a hand-authored field.

Readiness outcomes are:

- `Ready`: analysis may proceed normally
- `Ready with Limitations`: analysis may proceed, but limitations must be carried forward
- `Blocked`: analysis must wait for missing access, authority, or required material
- `Not Applicable`: the source type is not required for this configuration

## 10. Completeness and Quality

The source owner or intake process must record:

- missing files or sections
- unreadable or unsupported formats
- stale or expired content
- contradictory sources
- unverified external links
- assumptions about omitted material
- privacy, security, or access restrictions

The agent must not treat absent evidence as evidence that a behavior, rule, or outcome does not exist.

## 11. Analysis References

Every analysis observation must reference one or more Source IDs and, where possible:

- file path or document section
- page, screen, flow, or record identifier
- quoted or summarized evidence
- source version
- retrieval timestamp for unversioned material

An analysis must distinguish:

```text
Source evidence -> Observation -> Interpretation -> Requirement candidate
```

A source reference alone does not prove that an interpretation is explicit. The analysis classification and reasoning remain required.

## 12. Conflict and Change Handling

When a source changes or conflicts with another source:

1. Register the new version or conflicting source.
2. Identify affected observations, conclusions, and requirements.
3. Determine authority using configured rules.
4. Create a Decision Required item when authority or intent is unresolved.
5. Create a new analysis version when conclusions may change.
6. Reassess affected requirements and downstream work.
7. Preserve the previous source and analysis references for audit.

A source change must not silently alter an approved analysis or requirement.

## 13. Retention and Access

The active product configuration defines retention and access rules. It must preserve enough information to reproduce or inspect the analysis, subject to privacy, security, and legal requirements.

The source record must state:

- who may view the source
- whether agents may process it
- whether external links are relied upon
- how restricted content is summarized or referenced
- how withdrawal or deletion affects existing analyses

Restricted or deleted source material must leave an auditable limitation record where policy permits.

## 14. Source Quality Checklist

- [ ] Product, initiative, or change effort is identified.
- [ ] Source ID and type are recorded.
- [ ] Location and exact version or retrieval identity are recorded.
- [ ] Owner and authority are identified.
- [ ] Effective status and date are known when relevant.
- [ ] Access and readability are confirmed.
- [ ] Missing, stale, restricted, or conflicting material is visible.
- [ ] Required source types for the configuration are present.
- [ ] Optional Design Handoff Bundle metadata is complete when enabled.
- [ ] Intended analysis and outcome are stated.
- [ ] Source references can be carried into analysis and requirements.

## 15. Default Profile Mapping

For this repository's initial profile:

- versioned design handoff bundles are supported sources
- Claude Design is an external source-production tool
- durable design artifacts are stored in the business repository
- source material is consumed, not silently rewritten, by agents
- GitHub paths and links are the initial source-location adapter
- source versions are retained for analysis and downstream traceability

These are implementation defaults. The active framework configuration controls the source types, authority, storage, and retention rules for each product context.

## 16. Open Decisions

- Which source types are mandatory for each analysis module?
- Which source formats must be machine-readable?
- What authority rules apply when sources conflict?
- What retrieval identity is sufficient for unversioned external sources?
- Which restricted sources may agents process?
- What source changes automatically trigger analysis re-review?
- How long must withdrawn or superseded sources remain available?
