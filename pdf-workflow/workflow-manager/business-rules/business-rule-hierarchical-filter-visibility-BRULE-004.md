# Business Rule: Hierarchical Filter Visibility

| | |
| --- | --- |
| Rule ID | `BRULE-004` |
| Platform / App | pdf-workflow / workflow-manager |
| Scope | Search/filter |
| Status | Active |

## Statement

A Section is visible only if it has a matching field or its own heading matches; a Page is visible only if it has a visible Section. Filtering never leaves an empty Section or Page on screen.

## Evidence

Search and confidence filters apply at the field level; visibility propagates up the hierarchy. Explicit, High confidence -- `SRC-003`.

## Governs

- [CAP-002](../capabilities/capability-filter-and-search-mappings-CAP-002.md) -- Filter and Search Mappings

## Appears in

- [DA-003](../analysis/mapping-report/design-analysis-mapping-report-DA-003.md) -- introduced here, feeds `BR-004`.
