# Capability: Filter and Search Mappings

| | |
| --- | --- |
| Capability ID | `CAP-002` |
| Platform / App | pdf-workflow / workflow-manager |
| Status | Active |

## Business purpose

Let the reviewer narrow a potentially large mapping down to what actually needs checking -- live text search plus a confidence-band filter, both applying at the field level with the containing Section/Page hidden once nothing inside still matches.

## Used by journeys

- [JRN-001](../journeys/journey-review-correct-low-confidence-mapping-JRN-001.md) -- the reviewer filters to Low confidence as the first step, to find what actually needs fixing before opening anything.

## Evidence

Filters are two rows sharing one state; search is live with no submit button; the confidence filter and search both apply at the field level, propagating visibility up to the containing Section and Page. Explicit, High confidence -- `SRC-003`.

## Governed by

- [BRULE-004](../business-rules/business-rule-hierarchical-filter-visibility-BRULE-004.md) -- hierarchical visibility rule.
- [BRULE-008](../business-rules/business-rule-horizontal-scroll-mobile-BRULE-008.md) -- responsive behavior below ~900px.

## Appears in

- [DA-003](../analysis/mapping-report/design-analysis-mapping-report-DA-003.md) -- introduced here, feeds `BR-004`.
