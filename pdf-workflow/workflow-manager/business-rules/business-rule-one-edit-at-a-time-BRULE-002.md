# Business Rule: One Edit at a Time

| | |
| --- | --- |
| Rule ID | `BRULE-002` |
| Platform / App | pdf-workflow / workflow-manager |
| Scope | Mapping Report |
| Status | Active |

## Statement

Only one field row may be in edit mode at a time. Opening a new one collapses whatever was already open.

## Evidence

Kind-specific edit controls; every panel ends with Cancel/Save; only one field may be expanded at a time. Explicit, High confidence -- `SRC-003`.

## Governs

- [CAP-004](../capabilities/capability-edit-mapped-field-details-CAP-004.md) -- Edit a Mapped Field's Details

## Appears in

- [DA-003](../analysis/mapping-report/design-analysis-mapping-report-DA-003.md) -- introduced here, feeds `BR-007`.
