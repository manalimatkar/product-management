# Business Rule: PDF Path Only

| | |
| --- | --- |
| Rule ID | `BRULE-006` |
| Platform / App | pdf-workflow / workflow-manager |
| Scope | Mapping Report -- confidence-review chrome specifically |
| Status | Active |

## Statement

The confidence-review report applies only to workflows created via the PDF path. Scope-defining, not tied to a single Capability -- it constrains *when the whole feature is meaningful*, narrower than "only the confidence-review chrome" per `DA-003`'s `BR-015` revision.

## Evidence

This report only applies to PDF-created workflows; manually-created workflows get no report; the LLM path is named as an explicit future reuse target, not built now. Explicit, High confidence -- `SRC-003`.

## Governs

Scope-defining rule, not tied to one Capability -- see `DA-003`'s `BR-015` for the full narrowing (confidence-review chrome only, not the whole screen, since the underlying structure editor is reused across creation paths -- `CAP-006`).

## Appears in

- [DA-003](../analysis/mapping-report/design-analysis-mapping-report-DA-003.md) -- introduced here, feeds `BR-015`.
