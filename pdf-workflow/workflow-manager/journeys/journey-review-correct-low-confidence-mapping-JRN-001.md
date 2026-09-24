# Journey: Review and Correct a Low-Confidence Field Mapping

| | |
| --- | --- |
| Journey ID | `JRN-001` |
| Platform / App | pdf-workflow / workflow-manager |
| Actor | Workflow manager user (reviewer) |
| Status | Active |

## Goal

Find a mapping the extraction likely got wrong and fix it.

## Preconditions

A PDF-created workflow has been processed and its Mapping Report is open.

## Steps

1. Select the "Low" confidence filter. *(uses [CAP-002](../capabilities/capability-filter-and-search-mappings-CAP-002.md))*
2. Click the pencil icon on a flagged field row -- it expands in place with kind-specific edit controls; any other open row collapses. *(uses [CAP-004](../capabilities/capability-edit-mapped-field-details-CAP-004.md))*
3. Correct the label/type (or sub-fields, if a `field-group`).
4. Click Save -- the change persists, a toast confirms, the panel closes.

## Expected outcome

The field's label/type (or sub-structure) reflects the reviewer's correction and is saved.

## Uses capabilities

- [CAP-002](../capabilities/capability-filter-and-search-mappings-CAP-002.md) -- Filter and Search Mappings
- [CAP-004](../capabilities/capability-edit-mapped-field-details-CAP-004.md) -- Edit a Mapped Field's Details

## Source

`SRC-003`, via [DA-003](../analysis/mapping-report/design-analysis-mapping-report-DA-003.md) (originally recorded as `JRN-001` in the pre-reformat version of that document, then folded into narrative "for example" prose under "Editing a mapped field" during the 2026-09-08 reformat; re-instated as a real, addressable ID here 2026-09-10).
