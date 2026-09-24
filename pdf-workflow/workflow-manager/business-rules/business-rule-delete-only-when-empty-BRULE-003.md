# Business Rule: Delete Only When Empty

| | |
| --- | --- |
| Rule ID | `BRULE-003` |
| Platform / App | pdf-workflow / workflow-manager |
| Scope | Mapping Report |
| Status | Active |

## Statement

A page or section may be deleted only when it has zero children.

## Evidence

Delete (trash) icon on a page/section appears only when it has zero children. Explicit, High confidence -- `SRC-003`.

## Governs

- [CAP-007](../capabilities/capability-remove-empty-structure-CAP-007.md) -- Remove Empty Structure

## Appears in

- [DA-003](../analysis/mapping-report/design-analysis-mapping-report-DA-003.md) -- introduced here, feeds `BR-012`.
