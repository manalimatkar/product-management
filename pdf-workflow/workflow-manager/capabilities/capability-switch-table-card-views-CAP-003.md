# Capability: Switch Between Table and Card Views

| | |
| --- | --- |
| Capability ID | `CAP-003` |
| Platform / App | pdf-workflow / workflow-manager |
| Status | Active -- Table view only, this phase |

## Business purpose

Let the reviewer choose a layout without losing filter or edit state. The design fully specifies both Table and Card views sharing identical data and state; direct feedback on `PR #17` ("for now work on table view") scoped the actual *build* to Table only -- Card view is deferred, not rejected (see `BR-003`, `GAP-004` in `DA-003`).

## Used by journeys

None -- Table view is the only rendering built this phase, so no journey exercises a view toggle yet.

## Evidence

The View toggle renders the exact same filtered/grouped data; switching never resets search, confidence filter, source filter, or an in-progress edit. Explicit, High confidence -- `SRC-003`. Narrowed to Table-only for this build by Human Provided input (Manali, `PR #17`).

## Governed by

- [BRULE-005](../business-rules/business-rule-table-card-parity-BRULE-005.md) -- kept as the modeling constraint for whenever Card view is actually built.

## Appears in

- [DA-003](../analysis/mapping-report/design-analysis-mapping-report-DA-003.md) -- introduced here, feeds `BR-003`.
