# Capability: Switch Between Table and Card Views

| | |
| --- | --- |
| Capability ID | `CAP-003` |
| Platform / App | pdf-workflow / workflow-manager |
| Status | Active -- Table view only, this phase |

## Business purpose

Let the reviewer choose a layout without losing search, filter, or edit state. The design specifies both Table and Card views over the same data and state; direct feedback on `PR #17` ("for now work on table view") scoped the build to Table only -- Card view is deferred, not rejected (see `BR-003`, `GAP-004` in `DA-003`). In the design, Card view is also the only view with inline editing (see `DEC-007` in `DA-003`).

## Used by journeys

None -- Table view is the only rendering built this phase, so no journey uses a view toggle yet.

## Evidence

In the dark `designs/Mapping Report.dc.html`, one shared set of state (search, confidence filter, open edit, collapsed pages and sections) drives both renderings; switching views changes only which one is shown. Card view rows for descriptions and custom elements carry an edit control; Table view rows don't. Explicit, High confidence -- `SRC-003`. Narrowed to Table only for this build by Human Provided input (Manali, `PR #17`).

## Governed by

- [BRULE-005](../business-rules/business-rule-table-card-parity-BRULE-005.md) -- kept as the modeling constraint for whenever Card view is built.

## Appears in

- [DA-003](../analysis/mapping-report/design-analysis-mapping-report-DA-003.md) -- introduced here, feeds `BR-003`.

## Revision history

| Date | Change |
| --- | --- |
| 2026-10-06 | Evidence re-sourced to the dark design file: no source filter exists; inline editing appears only in Card view (`DA-003` v2.0). |
| 2026-09-10 | Registered from `DA-003`. |
