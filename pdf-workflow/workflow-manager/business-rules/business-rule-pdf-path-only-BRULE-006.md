# Business Rule: Confidence Review Only for Extracted Workflows

| | |
| --- | --- |
| Rule ID | `BRULE-006` |
| Platform / App | pdf-workflow / workflow-manager |
| Scope | Mapping Report -- confidence-review elements specifically |
| Status | Active |

## Statement

The confidence-review elements of the Mapping Report (stat tiles and confidence filter) appear only for a workflow whose structure came from an extraction step -- PDF conversion in this phase. A manually created workflow uses the same screen without them.

## Evidence

The dark `designs/Mapping Report.dc.html` shows the stat tiles and confidence filter unless the workflow's creation method is `manual`, and still shows a manually created workflow's structure. The Business Owner described the same screen as the starting point for building a workflow from scratch (Manali, `PR #17`, Human Provided). The README's Scope note says the report applies "only to the PDF path" and that manually created workflows need "no report"; that wording is narrowed by the two sources above to the confidence-review elements only. Explicit, High confidence -- `SRC-003`.

The design also shows these elements for workflows created from LLM instructions; the README places that creation path outside this handoff.

## Governs

- [CAP-001](../capabilities/capability-review-extraction-confidence-CAP-001.md) -- Review Extraction Confidence and Structure (stat tiles)
- [CAP-002](../capabilities/capability-filter-and-search-mappings-CAP-002.md) -- Filter and Search Mappings (confidence filter)

## Appears in

- [DA-003](../analysis/mapping-report/design-analysis-mapping-report-DA-003.md) -- introduced here, feeds `BR-015`.

## Revision history

| Date | Change |
| --- | --- |
| 2026-10-06 | Restated against the dark design file (`DA-003` v2.0): the rule covers the confidence-review elements, not the whole screen, and now governs `CAP-001` and `CAP-002` instead of standing as scope-defining only. Title changed from "PDF Path Only"; file name kept. |
| 2026-09-10 | Registered from `DA-003`. |
