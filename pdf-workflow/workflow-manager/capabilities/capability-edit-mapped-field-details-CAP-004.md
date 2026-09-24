# Capability: Edit a Mapped Field's Details

| | |
| --- | --- |
| Capability ID | `CAP-004` |
| Platform / App | pdf-workflow / workflow-manager |
| Status | Active |

## Business purpose

Let the reviewer correct what the extraction got wrong, with controls appropriate to what kind of element it is -- a single Text box for headings/descriptions, Label+type for a Field, Label+per-item list+Min/Max for a FieldGroup, Label only for Custom. In-place expansion, never a dropdown remap.

## Used by journeys

- [JRN-001](../journeys/journey-review-correct-low-confidence-mapping-JRN-001.md) -- opening the first flagged field, correcting its label/type, and saving is the core of this journey.

## Evidence

Editing surfaces differ by `kind`; only one row may be in edit mode at a time; every edit panel ends in an explicit Cancel/Save; navigating away with a dirty edit prompts a discard-confirmation. Explicit, High confidence -- `SRC-003`, directly re-verified against the real v4 text (an earlier pass working from a stale test version thought it had found a dropdown-based contradiction here; none exists in the current source).

## Governed by

- [BRULE-001](../business-rules/business-rule-kind-constrains-remap-BRULE-001.md) -- a mapping's `kind` constrains which `targetType`s it may remap to.
- [BRULE-002](../business-rules/business-rule-one-edit-at-a-time-BRULE-002.md) -- only one field row may be in edit mode at a time.
- [BRULE-008](../business-rules/business-rule-horizontal-scroll-mobile-BRULE-008.md) -- responsive behavior below ~900px.

## Appears in

- [DA-003](../analysis/mapping-report/design-analysis-mapping-report-DA-003.md) -- introduced here, feeds `BR-005`, `BR-006`, `BR-007`, `BR-014`.
