# Capability: Reorder Structure

| | |
| --- | --- |
| Capability ID | `CAP-008` |
| Platform / App | pdf-workflow / workflow-manager |
| Status | Active |

## Business purpose

Let the reviewer fix the order pages, sections, or fields appear in -- up/down controls moving one item at a time among its siblings.

## Used by journeys

None yet. `DA-003`'s three recorded journeys don't walk through a reorder path -- see [CAPABILITY-REGISTRY.md](../../../registries/CAPABILITY-REGISTRY.md)'s note on this.

## Evidence

Every page, section, and field row has up/down reorder chevrons; order is stored as an explicit override list per level, falling back to natural order for anything not yet moved. Explicit, High confidence -- `SRC-003`. Exact storage/sync mechanism is a Technical Unknown (`TECH-002` in `DA-003`), not a business concern.

## Governed by

- [BRULE-007](../business-rules/business-rule-no-confirmation-except-unlink-BRULE-007.md) -- structural edits never require confirmation.

## Appears in

- [DA-003](../analysis/mapping-report/design-analysis-mapping-report-DA-003.md) -- introduced here, feeds `BR-013`.
