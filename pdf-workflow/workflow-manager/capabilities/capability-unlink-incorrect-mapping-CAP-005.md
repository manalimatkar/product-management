# Capability: Unlink an Incorrect Mapping

| | |
| --- | --- |
| Capability ID | `CAP-005` |
| Platform / App | pdf-workflow / workflow-manager |
| Status | Active |

## Business purpose

Let the reviewer remove a wrong mapping while understanding its cost -- a confirmation dialog that, for a FieldGroup, names the specific sub-fields that would be lost.

## Used by journeys

- [JRN-002](../journeys/journey-remove-incorrectly-extracted-field-JRN-002.md) -- the entire journey is this capability, end to end.

## Evidence

Clicking unlink opens a confirmation dialog before the mapping is removed; for a FieldGroup, the dialog names the sub-fields that would be lost. Explicit, High confidence -- `SRC-003`.

## Governed by

- [BRULE-007](../business-rules/business-rule-no-confirmation-except-unlink-BRULE-007.md) -- unlink is the sole exception to "structural edits never require confirmation."

## Appears in

- [DA-003](../analysis/mapping-report/design-analysis-mapping-report-DA-003.md) -- introduced here, feeds `BR-008`.
