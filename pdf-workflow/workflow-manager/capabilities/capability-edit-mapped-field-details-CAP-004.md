# Capability: Edit a Mapped Field's Details

| | |
| --- | --- |
| Capability ID | `CAP-004` |
| Platform / App | pdf-workflow / workflow-manager |
| Status | Active -- inline editing pending `DEC-007` in `DA-003` |

## Business purpose

Let the reviewer correct what the extraction got wrong without leaving the report, where the element is simple enough to edit in place: a description's text or a custom element's label. Each mapping's target type is shown as a compact label (e.g. `Field-List-3x`) so it can be read without opening anything. Fields and lists are edited in the Workflow Page Editor instead (`CAP-009`), and no control on this screen changes a mapping's target type.

## Used by journeys

- [JRN-001](../journeys/journey-review-correct-low-confidence-mapping-JRN-001.md) -- when the flagged row is a description or custom element, the reviewer corrects it in place.

## Evidence

In the dark `designs/Mapping Report.dc.html`: Card view rows for descriptions offer a single text area, and for custom elements a single label input, each with Save and Cancel; only one row can be open at a time; Save shows "Changes saved"; unsaved changes trigger "Discard unsaved changes?" on switching rows or cancelling, and the browser's leave-page warning on leaving. Field and list rows have no inline edit, and Table view rows have no edit control. Explicit, High confidence -- `SRC-003`. The README's Label + type and per-item list editors for fields and lists are not in the dark file.

## Governed by

- [BRULE-001](../business-rules/business-rule-kind-constrains-remap-BRULE-001.md) -- a mapping's `kind` constrains which `targetType`s it may remap to.
- [BRULE-002](../business-rules/business-rule-one-edit-at-a-time-BRULE-002.md) -- only one row may be in edit mode at a time.
- [BRULE-008](../business-rules/business-rule-horizontal-scroll-mobile-BRULE-008.md) -- responsive behavior below ~900px.

## Appears in

- [DA-003](../analysis/mapping-report/design-analysis-mapping-report-DA-003.md) -- introduced here, feeds `BR-005`, `BR-006`, `BR-007`, `BR-014`.

## Revision history

| Date | Change |
| --- | --- |
| 2026-10-06 | Purpose and evidence revised against the dark design file (`DA-003` v2.0): inline editing covers descriptions and custom elements only, in Card view; field and list editing moved to the Workflow Page Editor. |
| 2026-09-10 | Registered from `DA-003`. |
