# Journey: Add a Section the Extraction Missed

| | |
| --- | --- |
| Journey ID | `JRN-003` |
| Platform / App | pdf-workflow / workflow-manager |
| Actor | Workflow manager user (reviewer) |
| Status | Active |

## Goal

Fill in structure the PDF extraction didn't capture.

## Preconditions

A page is expanded.

## Steps

1. Click "+ Add section" -- an inline form appears (title required, description optional). *(uses [CAP-006](../capabilities/capability-manually-add-structure-CAP-006.md))*
2. Enter a title, click Add.
3. The new section appears immediately, grouped under that page exactly like an extracted one (synthetic mapped heading, 100% confidence).

## Expected outcome

A new section exists, grouped correctly, ready to receive fields.

## Uses capabilities

- [CAP-006](../capabilities/capability-manually-add-structure-CAP-006.md) -- Manually Add Structure

## Source

`SRC-003`, via [DA-003](../analysis/mapping-report/design-analysis-mapping-report-DA-003.md) (originally recorded as `JRN-003` in the pre-reformat version of that document, then folded into narrative "for example" prose under "Manually adding structure" during the 2026-09-08 reformat; re-instated as a real, addressable ID here 2026-09-10).
