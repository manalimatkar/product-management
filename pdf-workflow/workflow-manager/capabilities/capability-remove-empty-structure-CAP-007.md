# Capability: Remove Empty Structure

| | |
| --- | --- |
| Capability ID | `CAP-007` |
| Platform / App | pdf-workflow / workflow-manager |
| Status | Active |

## Business purpose

Let the reviewer clean up structure that's no longer needed, without risking accidental data loss -- delete is only ever offered on a page or section that already has zero children.

## Used by journeys

None yet. `DA-003`'s three recorded journeys don't walk through a delete path -- see [CAPABILITY-REGISTRY.md](../../../CAPABILITY-REGISTRY.md)'s note on this.

## Evidence

Delete (trash) icon on a page/section appears only when it has zero children; no confirmation dialog, since nothing is lost. Explicit, High confidence -- `SRC-003`.

## Governed by

- [BRULE-003](../business-rules/business-rule-delete-only-when-empty-BRULE-003.md) -- a page or section may be deleted only when it has zero children.
- [BRULE-007](../business-rules/business-rule-no-confirmation-except-unlink-BRULE-007.md) -- structural edits never require confirmation.

## Appears in

- [DA-003](../analysis/mapping-report/design-analysis-mapping-report-DA-003.md) -- introduced here, feeds `BR-012`.
