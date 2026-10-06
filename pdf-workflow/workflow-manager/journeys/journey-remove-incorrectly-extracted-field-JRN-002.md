# Journey: Remove an Incorrectly Extracted Field

| | |
| --- | --- |
| Journey ID | `JRN-002` |
| Platform / App | pdf-workflow / workflow-manager |
| Actor | Workflow manager user (reviewer) |
| Status | Active |

## Goal

Remove a mapping that shouldn't exist at all.

## Preconditions

Mapping Report open, the row visible.

## Steps

1. Select "Delete field" (trash icon) on the row. *(uses [CAP-005](../capabilities/capability-unlink-incorrect-mapping-CAP-005.md))*
2. A dialog titled "Delete this field?" says the field will be removed from the workflow and that this can't be undone; for a list, it says how many sub-fields go with it.
3. Select Delete -- the row disappears and "Field removed" confirms it.

## Expected outcome

The mapping is gone, and the reviewer knew beforehand what would be lost.

## Alternate paths

- Select Cancel in the dialog -- nothing is removed.

## Uses capabilities

- [CAP-005](../capabilities/capability-unlink-incorrect-mapping-CAP-005.md) -- Unlink an Incorrect Mapping

## Source

`SRC-003` (dark `designs/Mapping Report.dc.html`), via [DA-003](../analysis/mapping-report/design-analysis-mapping-report-DA-003.md). Whether deleting removes only the mapping or the workflow field itself is open (`DEC-008` in `DA-003`).

## Revision history

| Date | Change |
| --- | --- |
| 2026-10-06 | Steps revised against the dark design file (`DA-003` v2.0): control is "Delete field"; the dialog states a sub-field count rather than naming sub-fields. |
| 2026-09-10 | Given its own ID and record, from `DA-003`'s narrative. |
