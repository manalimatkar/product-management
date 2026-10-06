# Business Rule: Table/Card Parity

| | |
| --- | --- |
| Rule ID | `BRULE-005` |
| Platform / App | pdf-workflow / workflow-manager |
| Scope | Mapping Report |
| Status | Active -- kept as a modeling constraint; Card view itself not built this phase |

## Statement

Table view and Card view must show identical filtered/grouped data and share all state (search, filter, in-progress edit). Kept as the modeling constraint for whenever Card view is picked up, even though only Table view is built now (see `CAP-003`).

## Evidence

In the dark `designs/Mapping Report.dc.html`, one shared set of state (search, confidence filter, open edit, collapsed pages and sections) drives both renderings, and switching views changes only which one is shown. The README: "switching views never resets anything." Explicit, High confidence -- `SRC-003`. The two views share data and state but not every control: in the design, inline editing appears only in Card view.

## Governs

- [CAP-003](../capabilities/capability-switch-table-card-views-CAP-003.md) -- Switch Between Table and Card Views

## Appears in

- [DA-003](../analysis/mapping-report/design-analysis-mapping-report-DA-003.md) -- introduced here, feeds `BR-003`.

## Revision history

| Date | Change |
| --- | --- |
| 2026-10-06 | Evidence revised against the dark design file (`DA-003` v2.0): no source filter exists; noted that inline editing appears only in Card view. |
| 2026-09-10 | Registered from `DA-003`. |
