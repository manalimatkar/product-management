# Capability: Review Extraction Confidence and Structure

| | |
| --- | --- |
| Capability ID | `CAP-001` |
| Platform / App | pdf-workflow / workflow-manager |
| Status | Active |

## Business purpose

Let the reviewer gauge how much attention a workflow's mapping needs before working through it in detail -- an at-a-glance summary (Total / High / Medium / Low / Average confidence) plus a collapsible Page → Section → Field hierarchy to browse.

## Used by journeys

None yet. `DA-003`'s three recorded journeys (`JRN-001`-`003`) all start mid-task rather than narrating the initial stat-tile glance -- see [CAPABILITY-REGISTRY.md](../../../CAPABILITY-REGISTRY.md)'s note on this. Worth a Journey covering the "does this workflow need my attention" moment if this feature-slice is revisited.

## Evidence

Five confidence-banded stat tiles are visible before any interaction; the mapping itself is browsable as a collapsible Page → Section → Field hierarchy; a page can contain multiple sections. Explicit, High confidence -- `SRC-003` (`pdf-workflow/workflow-manager/design/v4/README.md`).

## Governed by

- [BRULE-008](../business-rules/business-rule-horizontal-scroll-mobile-BRULE-008.md) -- responsive behavior below ~900px.

## Appears in

- [DA-003](../analysis/mapping-report/design-analysis-mapping-report-DA-003.md) -- introduced here, feeds `BR-001` and `BR-002`.
