# Product Source Material Template

Reusable formats implementing [PRODUCT-SOURCE-MATERIAL-SPEC.md](../specs/PRODUCT-SOURCE-MATERIAL-SPEC.md). Every other artifact in this pipeline already had a fillable template; this was the one gap -- Source Material is artifact #1 in the chain and previously had only a table of required fields buried in the spec, nothing to actually fill in. Use this instead.

Every source registered with this template gets one row added to [SOURCE-REGISTRY.md](../SOURCE-REGISTRY.md) -- see that file for the running index across all sources.

---

## Part 1: Source Registration Record

**File:** `<platform-slug>/[<app-slug>/]sources/<feature-slug>/source-<feature-slug>-<source-id>.md` (see [ARTIFACT-STORAGE-SPEC.md](../specs/ARTIFACT-STORAGE-SPEC.md) section 4)

```markdown
# Source: <Source Name>

## Registration

| Field | Value |
| --- | --- |
| Source ID | `SRC-<number>` |
| Source Name | `<human-readable name>` |
| Source Type | `<one of: Product/business brief, User/customer evidence, Design material, Process material, Policy/regulatory material, Domain/data material, Technical context, Instruction/change request, Measurement/experiment evidence, Other configured source>` |
| Location | `<repository path, URL, system reference, or attachment ID>` |
| Version | `<explicit version, or "Not Versioned">` |
| Status | `Draft` / `Active` / `Superseded` / `Withdrawn` / `Unavailable` |
| Owner | `<person, role, team, or external authority>` |
| Authority Level | `<per the active product configuration -- see FRAMEWORK-CONFIGURATION-SPEC.md §6>` |
| Created At | `<source creation timestamp, or Unknown>` |
| Effective At | `<date the source becomes applicable, or Not Applicable>` |
| Registered By | `<person, agent, or system>` |
| Registered At | `<timestamp>` |
| Access Notes | `<access restrictions or retrieval instructions, or None>` |

## If This Source Is a Design Handoff Bundle

If `Source Type` is Design material and the source is a versioned Design Handoff Bundle, its bundle-specific fields (manifest, screens, flows, assets, experience requirements) live in `bundle.md` per [DESIGN-HANDOFF-BUNDLE-SPEC.md](../specs/DESIGN-HANDOFF-BUNDLE-SPEC.md) section 5 -- do not duplicate them here. `Location` above should point at that bundle's path, and `Version` should match its `version` field exactly.

## Known Limitations

- `<missing files or sections, unreadable formats, stale content, unverified links, or None>`

## Related Sources

| Relationship | Source ID | Notes |
| --- | --- | --- |
| `Supersedes` / `Conflicts with` / `Depends on` / `Related to` | `SRC-<number>` | `<notes>` |
```

---

## Part 2: Source Readiness Check

**File:** append to the same source file, or record inline in the consuming Design Analysis per [DESIGN-ANALYSIS-REVIEW-SPEC.md](../specs/DESIGN-ANALYSIS-REVIEW-SPEC.md) section 5.

```markdown
## Readiness Check

| Check | Result | Evidence or Action |
| --- | --- | --- |
| Source can be accessed | Pass / Fail | `<reference>` |
| Source identity is known | Pass / Fail | `<reference>` |
| Source version is known | Pass / Not Versioned / Fail | `<version>` |
| Required source types are present (per active configuration) | Pass / Fail | `<reference>` |
| Source is readable and complete | Pass / Limited / Fail | `<notes>` |
| Conflicts with another registered source are detected | Yes / No | `<source IDs, or None>` |
| Authority of this source is known | Pass / Fail | `<owner or rule>` |

**Readiness outcome:** `Ready` / `Ready with Limitations` / `Blocked` / `Not Applicable`

If `Ready with Limitations`, the specific limitations must be carried forward into any Design Analysis that consumes this source (per PRODUCT-SOURCE-MATERIAL-SPEC.md §9). If `Blocked`, analysis must not begin until the blocking condition is resolved -- record the reason and owner below.

**Blocking reason (if `Blocked`):** `<reason, owner, condition for resuming, or Not Applicable>`
```

---

## Part 3: Version History

*(Only needed once a source is revised after its first registration -- see PRODUCT-SOURCE-MATERIAL-SPEC.md §5.)*

```markdown
## Version History

| Version | Predecessor | Change Summary | Change Reason | Effective Date | Affected Analysis/Downstream | Prior Approvals Still Valid? |
| --- | --- | --- | --- | --- | --- | --- |
| `<version>` | `<predecessor version or None>` | `<summary>` | `<reason>` | `<date>` | `<references or None>` | Yes / No / Reassess |
```

---

## Storage Convention

The authoritative naming and folder convention -- for this artifact and every other artifact type -- is [ARTIFACT-STORAGE-SPEC.md](../specs/ARTIFACT-STORAGE-SPEC.md):

```text
<platform-slug>/[<app-slug>/]sources/<feature-slug>/source-<feature-slug>-<SRC-id>.md   (Registration Record + Readiness Check + Version History)
```

For a Design Handoff Bundle specifically, this registration record points at its actual content under `<platform-slug>/[<app-slug>/]design/<feature-slug>/v<version>/` (DESIGN-HANDOFF-BUNDLE-SPEC.md §8) -- the registration record and the bundle content are not the same file.

---

## Pre-Registration Checklist

*(Restates PRODUCT-SOURCE-MATERIAL-SPEC.md §14 as something to actually check off.)*

- [ ] Product, initiative, or change effort is identified
- [ ] Source ID and type are recorded
- [ ] Location and exact version (or retrieval identity) are recorded
- [ ] Owner and authority are identified
- [ ] Effective status and date are known when relevant
- [ ] Access and readability are confirmed
- [ ] Missing, stale, restricted, or conflicting material is visible in Known Limitations
- [ ] Required source types for the active configuration are present
- [ ] If this source is a Design Handoff Bundle, its bundle-specific metadata is complete per DESIGN-HANDOFF-BUNDLE-SPEC.md
- [ ] Readiness Check (Part 2) is complete with an outcome recorded
- [ ] This source has been added to [SOURCE-REGISTRY.md](../SOURCE-REGISTRY.md)
