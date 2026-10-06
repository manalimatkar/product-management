# Capability: Review Extraction Confidence and Structure

| | |
| --- | --- |
| Capability ID | `CAP-001` |
| Platform / App | pdf-workflow / workflow-manager |
| Status | Active |

## Business purpose

Let the reviewer judge how much attention a workflow's mapping needs, and browse it, before working through it in detail -- an at-a-glance summary (Total / High / Medium / Low / Average confidence), a collapsible Page → Section → row hierarchy, and a screen that names how the workflow was created and leaves out the confidence elements for a workflow built by hand.

## Used by journeys

None yet. The three recorded journeys (`JRN-001`-`003`) start mid-task rather than walking through the initial summary -- see [CAPABILITY-REGISTRY.md](../../../registries/CAPABILITY-REGISTRY.md).

## Evidence

In the dark `designs/Mapping Report.dc.html`: five confidence-banded stat tiles, counted over every mapping; a collapsible Page → Section → row hierarchy, all expanded at first, where a page can hold several sections; a "Back to dashboard" link; a creation-method tag; and, for a manually created workflow, no stat tiles or confidence filter. Explicit, High confidence -- `SRC-003`.

## Governed by

- [BRULE-006](../business-rules/business-rule-pdf-path-only-BRULE-006.md) -- confidence-review elements only for extraction-based workflows.
- [BRULE-008](../business-rules/business-rule-horizontal-scroll-mobile-BRULE-008.md) -- responsive behavior below ~900px.
- [BRULE-009](../business-rules/business-rule-manual-workflow-source-manual-BRULE-009.md) -- manual workflows show every row's source as manual.

## Appears in

- [DA-003](../analysis/mapping-report/design-analysis-mapping-report-DA-003.md) -- introduced here, feeds `BR-001`, `BR-002`, `BR-015`, and `BR-018`.

## Revision history

| Date | Change |
| --- | --- |
| 2026-10-06 | Evidence re-sourced to the dark design file; scope extended to the creation-method adaptation and the return link; now governed by `BRULE-006` and `BRULE-009` (`DA-003` v2.0). |
| 2026-09-10 | Registered from `DA-003`. |
