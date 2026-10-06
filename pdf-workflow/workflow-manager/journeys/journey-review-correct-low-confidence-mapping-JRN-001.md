# Journey: Review and Correct a Low-Confidence Field Mapping

| | |
| --- | --- |
| Journey ID | `JRN-001` |
| Platform / App | pdf-workflow / workflow-manager |
| Actor | Workflow manager user (reviewer) |
| Status | Active |

## Goal

Find a mapping the extraction likely got wrong and fix it.

## Preconditions

A workflow created by PDF conversion has been processed and its Mapping Report is open.

## Steps

1. Select the "Low" confidence filter -- only rows below 50% confidence remain, with emptied sections and pages hidden. *(uses [CAP-002](../capabilities/capability-filter-and-search-mappings-CAP-002.md))*
2. Find the flagged row -- for example "Anticipated Start Date", a field at 42%.
3. For a field or list row, which offers no inline edit: select "Manage page fields" on that row's page header and make the correction in the Workflow Page Editor. *(uses [CAP-009](../capabilities/capability-open-page-editor-from-report-CAP-009.md))*
4. For a description or custom row: open it for editing, correct its text or label, and select Save -- "Changes saved" confirms it. The design offers this in Card view only; whether it is part of this phase is open (`DEC-007` in `DA-003`). *(uses [CAP-004](../capabilities/capability-edit-mapped-field-details-CAP-004.md))*

## Expected outcome

The flagged mapping is corrected -- in the Workflow Page Editor for a field or list, or in place for a description or custom element.

## Alternate paths

- With unsaved changes in an inline edit, opening another row or selecting Cancel asks "Discard unsaved changes?" first.

## Uses capabilities

- [CAP-002](../capabilities/capability-filter-and-search-mappings-CAP-002.md) -- Filter and Search Mappings
- [CAP-009](../capabilities/capability-open-page-editor-from-report-CAP-009.md) -- Open the Workflow Page Editor from the Report
- [CAP-004](../capabilities/capability-edit-mapped-field-details-CAP-004.md) -- Edit a Mapped Field's Details

## Source

`SRC-003` (dark `designs/Mapping Report.dc.html`, including its seed data), via [DA-003](../analysis/mapping-report/design-analysis-mapping-report-DA-003.md).

## Revision history

| Date | Change |
| --- | --- |
| 2026-10-06 | Steps revised against the dark design file (`DA-003` v2.0): field and list corrections go through the Workflow Page Editor (`CAP-009` added); inline editing covers descriptions and custom elements only. |
| 2026-09-10 | Given its own ID and record, from `DA-003`'s narrative. |
