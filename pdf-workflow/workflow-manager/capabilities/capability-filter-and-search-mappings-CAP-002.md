# Capability: Filter and Search Mappings

| | |
| --- | --- |
| Capability ID | `CAP-002` |
| Platform / App | pdf-workflow / workflow-manager |
| Status | Active |

## Business purpose

Let the reviewer narrow a potentially large mapping down to what needs checking -- live search over the extracted PDF text plus a confidence-band filter, both applying at the row level, with a section or page hidden once nothing inside it still matches.

## Used by journeys

- [JRN-001](../journeys/journey-review-correct-low-confidence-mapping-JRN-001.md) -- the reviewer filters to Low confidence as the first step, to find what needs fixing before opening anything.

## Evidence

In the dark `designs/Mapping Report.dc.html`: "Search PDF text" filters as the user types, matching the extracted PDF text and ignoring case, with no submit; the Confidence control (All / High / Medium / Low) is shown unless the workflow was created manually; visibility propagates up to the containing section and page; when nothing matches, "No mappings match the current filter." is shown. Explicit, High confidence -- `SRC-003`.

## Governed by

- [BRULE-004](../business-rules/business-rule-hierarchical-filter-visibility-BRULE-004.md) -- hierarchical visibility rule.
- [BRULE-006](../business-rules/business-rule-pdf-path-only-BRULE-006.md) -- the confidence filter appears only for extraction-based workflows.
- [BRULE-008](../business-rules/business-rule-horizontal-scroll-mobile-BRULE-008.md) -- responsive behavior below ~900px.

## Appears in

- [DA-003](../analysis/mapping-report/design-analysis-mapping-report-DA-003.md) -- introduced here, feeds `BR-004`.

## Revision history

| Date | Change |
| --- | --- |
| 2026-10-06 | Evidence re-sourced to the dark design file; now governed by `BRULE-006` (`DA-003` v2.0). |
| 2026-09-10 | Registered from `DA-003`. |
