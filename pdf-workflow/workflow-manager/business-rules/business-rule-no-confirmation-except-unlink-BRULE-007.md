# Business Rule: No Confirmation Except Unlink

| | |
| --- | --- |
| Rule ID | `BRULE-007` |
| Platform / App | pdf-workflow / workflow-manager |
| Scope | Mapping Report |
| Status | Active |

## Statement

Structural edits (add page/section/field, delete empty page/section, reorder) never require confirmation; unlinking a mapping is the sole exception. The clearest real example in this registry of a Business Rule that genuinely governs several Capabilities at once, rather than being produced by any one of them.

## Evidence

Source (Interactions & behavior section): "Add page/section/field, delete empty page/section, and reorder (page/section/field)... all are optimistic, no confirmation except unlink." Explicit, High confidence -- `SRC-003`. A new line in v4 not present in the retracted v2 drop.

## Governs

- [CAP-005](../capabilities/capability-unlink-incorrect-mapping-CAP-005.md) -- Unlink an Incorrect Mapping (the one exception)
- [CAP-006](../capabilities/capability-manually-add-structure-CAP-006.md) -- Manually Add Structure
- [CAP-007](../capabilities/capability-remove-empty-structure-CAP-007.md) -- Remove Empty Structure
- [CAP-008](../capabilities/capability-reorder-structure-CAP-008.md) -- Reorder Structure

## Appears in

- [DA-003](../analysis/mapping-report/design-analysis-mapping-report-DA-003.md) -- introduced here, feeds `BR-008`, `BR-009`, `BR-010`, `BR-011`, `BR-012`, `BR-013`.
