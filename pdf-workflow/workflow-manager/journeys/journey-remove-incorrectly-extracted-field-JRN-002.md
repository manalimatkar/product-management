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

Mapping Report open, the field row visible.

## Steps

1. Click the unlink (×) icon on a field row. *(uses [CAP-005](../capabilities/capability-unlink-incorrect-mapping-CAP-005.md))*
2. A confirmation dialog opens, naming the sub-field cost if the row is a `FieldGroup`.
3. Confirm -- the mapping is removed.

## Expected outcome

The mapping is gone; the reviewer understood what (if anything) was lost.

## Uses capabilities

- [CAP-005](../capabilities/capability-unlink-incorrect-mapping-CAP-005.md) -- Unlink an Incorrect Mapping

## Source

`SRC-003`, via [DA-003](../analysis/mapping-report/design-analysis-mapping-report-DA-003.md) (originally recorded as `JRN-002` in the pre-reformat version of that document, then folded into narrative "for example" prose under "Unlinking a mapping" during the 2026-09-08 reformat; re-instated as a real, addressable ID here 2026-09-10).
