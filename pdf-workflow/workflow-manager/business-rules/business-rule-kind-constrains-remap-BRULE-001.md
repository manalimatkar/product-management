# Business Rule: Kind Constrains Remap

| | |
| --- | --- |
| Rule ID | `BRULE-001` |
| Platform / App | pdf-workflow / workflow-manager |
| Scope | Mapping edit |
| Status | Active |

## Statement

A mapping's `kind` constrains which `targetType`s it may be remapped to (e.g. `field` → `Field` only, `field-group` → `FieldGroup` only). A wrong-kind remap must not be offered, not just discouraged.

## Evidence

The README: "`kind` determines which `targetType` a row can be reassigned to ... don't allow cross-kind remapping." The dark `designs/Mapping Report.dc.html` maps each kind to one target type, with the comment "kind = what the PDF element actually is; drives which SEED_TARGETS it can map to." Explicit, High confidence -- `SRC-003`. The Mapping Report itself offers no remap control, so on that screen the rule holds by absence; it constrains remapping wherever remapping is offered.

## Governs

- [CAP-004](../capabilities/capability-edit-mapped-field-details-CAP-004.md) -- Edit a Mapped Field's Details

## Appears in

- [DA-003](../analysis/mapping-report/design-analysis-mapping-report-DA-003.md) -- introduced here, feeds `BR-005`.

## Revision history

| Date | Change |
| --- | --- |
| 2026-10-06 | Evidence revised against the dark design file (`DA-003` v2.0): no remap control on the Mapping Report. |
| 2026-09-10 | Registered from `DA-003`. |
