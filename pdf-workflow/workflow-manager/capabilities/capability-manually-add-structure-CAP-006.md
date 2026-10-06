# Capability: Manually Add Structure

| | |
| --- | --- |
| Capability ID | `CAP-006` |
| Platform / App | pdf-workflow / workflow-manager |
| Status | Active -- unconfirmed, pending `DEC-006` in `DA-003` |

## Business purpose

Let the reviewer fill in whatever the PDF extraction missed -- add a page, section, or field with a short inline form and no confirmation -- and let a new workflow begin from the same screen, after its Workflow Settings are saved, whatever its creation path.

## Used by journeys

- [JRN-003](../journeys/journey-add-section-extraction-missed-JRN-003.md) -- the whole journey is this capability.

## Evidence

The README describes "+ Add page", "+ Add section", and "+ Add field" on the Mapping Report, each with no confirmation, with a hand-added section grouping like an extracted one. The Business Owner described a new workflow starting on this screen by adding a page (Manali, `PR #17`, Human Provided). The dark `designs/Mapping Report.dc.html` contains none of these add controls. README and Human Provided; not confirmed by the design file -- where adding happens is open (`DEC-006` in `DA-003`).

## Governed by

- [BRULE-007](../business-rules/business-rule-no-confirmation-except-unlink-BRULE-007.md) -- structural edits never require confirmation.

## Appears in

- [DA-003](../analysis/mapping-report/design-analysis-mapping-report-DA-003.md) -- introduced here, feeds `BR-009`, `BR-010`, `BR-011`, `BR-016`.

## Revision history

| Date | Change |
| --- | --- |
| 2026-10-06 | Marked unconfirmed (`DA-003` v2.0): the add controls come from the README and are absent from the dark design file. |
| 2026-09-10 | Registered from `DA-003`. |
