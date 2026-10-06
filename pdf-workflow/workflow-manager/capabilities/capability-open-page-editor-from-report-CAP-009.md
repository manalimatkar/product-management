# Capability: Open the Workflow Page Editor from the Report

| | |
| --- | --- |
| Capability ID | `CAP-009` |
| Platform / App | pdf-workflow / workflow-manager |
| Status | Active |

## Business purpose

Let the reviewer move from spotting a problem with a field or list mapping to the screen where it can be fully edited. Fields and lists carry options, validation, and sub-fields, so the Mapping Report doesn't edit them in place; every page header has a "Manage page fields" link to the Workflow Page Editor instead.

## Used by journeys

- [JRN-001](../journeys/journey-review-correct-low-confidence-mapping-JRN-001.md) -- after filtering to a low-confidence field, the reviewer continues to the Workflow Page Editor to correct it.

## Evidence

Every page header in the dark `designs/Mapping Report.dc.html` has a "Manage page fields" link to `Workflow Page Editor.dc.html`; field and list rows offer no inline edit, with the script comment "Field and field-group rows now edit exclusively in the Workflow Page Editor." The README describes the report's inline editing as "a lightweight subset" that "links here for anything more." Explicit, High confidence -- `SRC-003`. Whether the editor opens at the specific page is not shown.

## Governed by

None recorded.

## Appears in

- [DA-003](../analysis/mapping-report/design-analysis-mapping-report-DA-003.md) -- introduced here, feeds `BR-017`.

## Revision history

| Date | Change |
| --- | --- |
| 2026-10-06 | Created from `DA-003` v2.0. |
