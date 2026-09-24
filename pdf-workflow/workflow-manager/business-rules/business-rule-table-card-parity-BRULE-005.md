# Business Rule: Table/Card Parity

| | |
| --- | --- |
| Rule ID | `BRULE-005` |
| Platform / App | pdf-workflow / workflow-manager |
| Scope | Mapping Report |
| Status | Active -- kept as a modeling constraint; Card view itself not built this phase |

## Statement

Table view and Card view must show identical filtered/grouped data and share all state (search, filter, in-progress edit). Kept as the modeling constraint for whenever Card view is picked up, even though only Table view is built right now (see `CAP-003`).

## Evidence

The View toggle renders the exact same filtered/grouped data; switching never resets search, confidence filter, source filter, or an in-progress edit. Explicit, High confidence -- `SRC-003`.

## Governs

- [CAP-003](../capabilities/capability-switch-table-card-views-CAP-003.md) -- Switch Between Table and Card Views

## Appears in

- [DA-003](../analysis/mapping-report/design-analysis-mapping-report-DA-003.md) -- introduced here, feeds `BR-003`.
