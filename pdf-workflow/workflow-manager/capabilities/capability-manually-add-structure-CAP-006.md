# Capability: Manually Add Structure

| | |
| --- | --- |
| Capability ID | `CAP-006` |
| Platform / App | pdf-workflow / workflow-manager |
| Status | Active |

## Business purpose

Let the reviewer fill in whatever the PDF extraction missed -- add a page, section, or field via a low-ceremony inline form, no confirmation. Also doubles as the starting surface for a brand-new workflow, right after Workflow Settings are saved, regardless of creation path.

## Used by journeys

- [JRN-003](../journeys/journey-add-section-extraction-missed-JRN-003.md) -- the entire journey is this capability, end to end.

## Evidence

"+ Add page/section/field" appends new structure with no confirmation dialog; a manually-added item groups exactly like something the extraction found for real (a synthetic mapped heading at 100% confidence). This same surface is also where a brand-new workflow lands after Workflow Settings are saved -- Human Provided (Manali, `PR #17`), refining the source's own PDF-only scope note. Explicit + Human Provided, High confidence -- `SRC-003`.

## Governed by

- [BRULE-007](../business-rules/business-rule-no-confirmation-except-unlink-BRULE-007.md) -- structural edits never require confirmation.

## Appears in

- [DA-003](../analysis/mapping-report/design-analysis-mapping-report-DA-003.md) -- introduced here, feeds `BR-009`, `BR-010`, `BR-011`, `BR-016`.
