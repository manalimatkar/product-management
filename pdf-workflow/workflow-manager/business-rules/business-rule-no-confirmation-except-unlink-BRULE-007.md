# Business Rule: No Confirmation Except Unlink

| | |
| --- | --- |
| Rule ID | `BRULE-007` |
| Platform / App | pdf-workflow / workflow-manager |
| Scope | Mapping Report |
| Status | Active |

## Statement

Structural edits (add page/section/field, delete empty page/section, reorder) never require confirmation; deleting (unlinking) a mapped field is the one exception. The rule governs several Capabilities at once rather than being produced by any one of them.

## Evidence

The README (Interactions & behavior section): "Add page/section/field, delete empty page/section, and reorder (page/section/field)... all are optimistic, no confirmation except unlink." The dark `designs/Mapping Report.dc.html` confirms it for deleting empty pages and sections, reordering, and the "Delete field" confirmation dialog. Explicit, High confidence -- `SRC-003`. The dark file has no add controls, so the "add" part applies only if adding happens on this screen (`DEC-006` in `DA-003`).

## Governs

- [CAP-005](../capabilities/capability-unlink-incorrect-mapping-CAP-005.md) -- Unlink an Incorrect Mapping (the one exception)
- [CAP-006](../capabilities/capability-manually-add-structure-CAP-006.md) -- Manually Add Structure
- [CAP-007](../capabilities/capability-remove-empty-structure-CAP-007.md) -- Remove Empty Structure
- [CAP-008](../capabilities/capability-reorder-structure-CAP-008.md) -- Reorder Structure

## Appears in

- [DA-003](../analysis/mapping-report/design-analysis-mapping-report-DA-003.md) -- introduced here, feeds `BR-008`, `BR-009`, `BR-010`, `BR-011`, `BR-012`, `BR-013`.

## Revision history

| Date | Change |
| --- | --- |
| 2026-10-06 | Evidence checked against the dark design file (`DA-003` v2.0); the add part is noted as pending `DEC-006`. |
| 2026-09-10 | Registered from `DA-003`. |
