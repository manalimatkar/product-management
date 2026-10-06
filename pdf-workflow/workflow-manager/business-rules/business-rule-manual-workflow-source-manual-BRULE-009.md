# Business Rule: Manual Workflows Show Manual Source

| | |
| --- | --- |
| Rule ID | `BRULE-009` |
| Platform / App | pdf-workflow / workflow-manager |
| Scope | Mapping Report -- field source shown per row |
| Status | Active |

## Statement

In a manually created workflow, every row's field source is shown as "manual". No field in a hand-built workflow can be LLM-sourced, whatever an individual mapping would otherwise say.

## Evidence

The dark `designs/Mapping Report.dc.html` forces each row's shown source to `manual` when the workflow's creation method is `manual`. The README's Files section states the same: "when a workflow's source is `manual`, every field row's source is forced to show `manual` (there's no LLM in a manually-created workflow, so a field can never be LLM-sourced there)." Explicit, High confidence -- `SRC-003`.

## Governs

- [CAP-001](../capabilities/capability-review-extraction-confidence-CAP-001.md) -- Review Extraction Confidence and Structure

## Appears in

- [DA-003](../analysis/mapping-report/design-analysis-mapping-report-DA-003.md) -- introduced here, feeds `BR-015`.

## Revision history

| Date | Change |
| --- | --- |
| 2026-10-06 | Created from `DA-003` v2.0. |
