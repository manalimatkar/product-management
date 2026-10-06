# Capability: Unlink an Incorrect Mapping

| | |
| --- | --- |
| Capability ID | `CAP-005` |
| Platform / App | pdf-workflow / workflow-manager |
| Status | Active |

## Business purpose

Let the reviewer remove a wrong mapping while understanding its cost -- a confirmation dialog that says what will be removed, that it can't be undone, and, for a list, how many sub-fields go with it.

## Used by journeys

- [JRN-002](../journeys/journey-remove-incorrectly-extracted-field-JRN-002.md) -- the whole journey is this capability.

## Evidence

In the dark `designs/Mapping Report.dc.html`, each row's "Delete field" control opens a dialog titled "Delete this field?" stating that the field (and, for a list, its N sub-fields) will be removed from the workflow and that this can't be undone; Cancel or Delete; "Field removed" confirms. Explicit, High confidence -- `SRC-003`. The README calls the action "unlink" and describes removing the mapping; which of the two is removed is open (`DEC-008` in `DA-003`).

## Governed by

- [BRULE-007](../business-rules/business-rule-no-confirmation-except-unlink-BRULE-007.md) -- deleting a mapped field is the one exception to "structural edits never require confirmation."

## Appears in

- [DA-003](../analysis/mapping-report/design-analysis-mapping-report-DA-003.md) -- introduced here, feeds `BR-008`.

## Revision history

| Date | Change |
| --- | --- |
| 2026-10-06 | Evidence revised against the dark design file (`DA-003` v2.0): the dialog states a sub-field count rather than naming sub-fields; what is removed is pending `DEC-008`. |
| 2026-09-10 | Registered from `DA-003`. |
