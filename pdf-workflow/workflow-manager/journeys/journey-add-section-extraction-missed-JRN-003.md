# Journey: Add a Section the Extraction Missed

| | |
| --- | --- |
| Journey ID | `JRN-003` |
| Platform / App | pdf-workflow / workflow-manager |
| Actor | Workflow manager user (reviewer) |
| Status | Active -- unconfirmed, pending `DEC-006` in `DA-003` |

## Goal

Fill in structure the PDF extraction didn't capture.

## Preconditions

A page is expanded.

## Steps

1. Select "+ Add section" -- an inline form appears (title required, description optional). *(uses [CAP-006](../capabilities/capability-manually-add-structure-CAP-006.md))*
2. Enter a title, select Add.
3. The new section appears under that page in the same way as an extracted one.

## Expected outcome

A new section exists under the page, ready to receive fields.

## Uses capabilities

- [CAP-006](../capabilities/capability-manually-add-structure-CAP-006.md) -- Manually Add Structure

## Source

`SRC-003`'s README, via [DA-003](../analysis/mapping-report/design-analysis-mapping-report-DA-003.md). The dark `designs/Mapping Report.dc.html` has no add controls, so whether this journey happens on the Mapping Report is open (`DEC-006` in `DA-003`).

## Revision history

| Date | Change |
| --- | --- |
| 2026-10-06 | Marked unconfirmed (`DA-003` v2.0): the steps come from the README and are absent from the dark design file. |
| 2026-09-10 | Given its own ID and record, from `DA-003`'s narrative. |
