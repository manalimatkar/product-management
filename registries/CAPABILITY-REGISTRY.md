# Capability Registry

The running index of every Capability registered under [ARTIFACT-STORAGE-SPEC.md](https://github.com/manalimatkar/product-management/blob/main/specs/ARTIFACT-STORAGE-SPEC.md) section 4.1 and [ARTIFACT-RELATIONSHIP-MODEL.md](https://github.com/manalimatkar/product-management/blob/main/specs/ARTIFACT-RELATIONSHIP-MODEL.md) section 3.1. Each row here has a full record at `<platform-slug>/[<app-slug>/]capabilities/capability-<slug>-<CAP-id>.md`.

This file is an index, not a record -- add one row per Capability here; put the actual detail (business purpose, evidence, which Journeys use it) in that Capability's own file.

A Capability is product-level, not feature-scoped: the same Capability can be cited by more than one Design Analysis, for more than one feature, over time. Its ID is global and assigned once here -- never re-minted per analysis. Before creating a new Capability, check this table first; cite an existing row if the analysis is genuinely describing the same one. A Capability's realness is proven by which Journeys actually depend on it -- see `Used By Journeys` below, not the Name column.

| Capability ID | Name | Platform / App | Used By Journeys | Used By Analyses | Record |
| --- | --- | --- | --- | --- | --- |
| `CAP-001` | Review Extraction Confidence and Structure | pdf-workflow / workflow-manager | *(none yet -- see note)* | `DA-003` | [pdf-workflow/workflow-manager/capabilities/capability-review-extraction-confidence-CAP-001.md](../pdf-workflow/workflow-manager/capabilities/capability-review-extraction-confidence-CAP-001.md) |
| `CAP-002` | Filter and Search Mappings | pdf-workflow / workflow-manager | `JRN-001` | `DA-003` | [pdf-workflow/workflow-manager/capabilities/capability-filter-and-search-mappings-CAP-002.md](../pdf-workflow/workflow-manager/capabilities/capability-filter-and-search-mappings-CAP-002.md) |
| `CAP-003` | Switch Between Table and Card Views | pdf-workflow / workflow-manager | *(none -- Table-view-only this phase, see `BR-003`)* | `DA-003` | [pdf-workflow/workflow-manager/capabilities/capability-switch-table-card-views-CAP-003.md](../pdf-workflow/workflow-manager/capabilities/capability-switch-table-card-views-CAP-003.md) |
| `CAP-004` | Edit a Mapped Field's Details | pdf-workflow / workflow-manager | `JRN-001` | `DA-003` | [pdf-workflow/workflow-manager/capabilities/capability-edit-mapped-field-details-CAP-004.md](../pdf-workflow/workflow-manager/capabilities/capability-edit-mapped-field-details-CAP-004.md) |
| `CAP-005` | Unlink an Incorrect Mapping | pdf-workflow / workflow-manager | `JRN-002` | `DA-003` | [pdf-workflow/workflow-manager/capabilities/capability-unlink-incorrect-mapping-CAP-005.md](../pdf-workflow/workflow-manager/capabilities/capability-unlink-incorrect-mapping-CAP-005.md) |
| `CAP-006` | Manually Add Structure | pdf-workflow / workflow-manager | `JRN-003` | `DA-003` | [pdf-workflow/workflow-manager/capabilities/capability-manually-add-structure-CAP-006.md](../pdf-workflow/workflow-manager/capabilities/capability-manually-add-structure-CAP-006.md) |
| `CAP-007` | Remove Empty Structure | pdf-workflow / workflow-manager | *(none yet -- see note)* | `DA-003` | [pdf-workflow/workflow-manager/capabilities/capability-remove-empty-structure-CAP-007.md](../pdf-workflow/workflow-manager/capabilities/capability-remove-empty-structure-CAP-007.md) |
| `CAP-008` | Reorder Structure | pdf-workflow / workflow-manager | *(none yet -- see note)* | `DA-003` | [pdf-workflow/workflow-manager/capabilities/capability-reorder-structure-CAP-008.md](../pdf-workflow/workflow-manager/capabilities/capability-reorder-structure-CAP-008.md) |

**First real entries, 2026-09-10** -- migrated from `DA-003`, which originally defined `CAP-001`-`008` as analysis-scoped IDs before this registry existed. `CAP-001`, `CAP-007`, and `CAP-008` genuinely having no Journey yet is an honest finding this migration surfaced, not smoothed over: `DA-003`'s three journeys (`JRN-001`-`003`, themselves just re-instated as real IDs from prose this same session) don't happen to walk through viewing the confidence summary as an explicit step, or a remove/reorder path, end to end. Worth a Journey covering those if/when this feature-slice is revisited -- not invented here to make the table look complete.

## Adding a Capability

1. Check this table first -- is an existing analysis's Capability actually the same one?
2. If genuinely new, assign the next unused `CAP-<number>`.
3. Create its record at `<platform-slug>/[<app-slug>/]capabilities/capability-<slug>-<CAP-id>.md`.
4. Add one row to the table above.
5. In the Design Analysis that introduces or touches it, cite the `CAP-<id>` and link to its record -- don't re-derive the ID locally.
6. Keep `Used By Journeys` and `Used By Analyses` in sync with the record's own content -- this index should never fall out of sync with the files it points to.
