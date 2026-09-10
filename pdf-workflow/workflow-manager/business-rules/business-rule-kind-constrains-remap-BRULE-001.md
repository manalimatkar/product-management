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

Each mapping has a `kind` (what the PDF element is) and maps to a target whose `targetType` is the discriminant; a `kind` can only remap within its own family. Explicit, High confidence -- `SRC-003`.

## Governs

- [CAP-004](../capabilities/capability-edit-mapped-field-details-CAP-004.md) -- Edit a Mapped Field's Details

## Appears in

- [DA-003](../analysis/mapping-report/design-analysis-mapping-report-DA-003.md) -- introduced here, feeds `BR-005`.
