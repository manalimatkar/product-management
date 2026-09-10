# Business Rule: Horizontal Scroll on Mobile

| | |
| --- | --- |
| Rule ID | `BRULE-008` |
| Platform / App | pdf-workflow / workflow-manager |
| Scope | Mapping Report, responsive behavior |
| Status | Active |

## Statement

Below roughly 900px, the mapping table uses horizontal scroll -- never a stacked-card row layout. The source explicitly left this open rather than silently picking one; resolved by direct Business Owner input.

## Evidence

Manali, `PR #17` review comment, 2026-09-08: "Keep table horizontal scroll." Human Provided, High confidence. Resolves what the source's own text flagged as an unmade choice ("decide with the user... Don't silently pick one").

## Governs

- [CAP-001](../capabilities/capability-review-extraction-confidence-CAP-001.md) -- Review Extraction Confidence and Structure
- [CAP-002](../capabilities/capability-filter-and-search-mappings-CAP-002.md) -- Filter and Search Mappings
- [CAP-004](../capabilities/capability-edit-mapped-field-details-CAP-004.md) -- Edit a Mapped Field's Details

## Appears in

- [DA-003](../analysis/mapping-report/design-analysis-mapping-report-DA-003.md) -- introduced here, feeds `BR-002`, `BR-004`, `BR-006`.
