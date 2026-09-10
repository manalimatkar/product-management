# Business Rule Registry

The running index of every Business Rule registered under [ARTIFACT-STORAGE-SPEC.md](../specs/ARTIFACT-STORAGE-SPEC.md) section 4.1 and [ARTIFACT-RELATIONSHIP-MODEL.md](../specs/ARTIFACT-RELATIONSHIP-MODEL.md) section 3.1. Each row here has a full record at `<platform-slug>/[<app-slug>/]business-rules/business-rule-<slug>-<BRULE-id>.md`.

This file is an index, not a record -- add one row per Business Rule here; put the actual detail (statement, scope, evidence) in that rule's own file.

A Business Rule is product-level, not feature-scoped -- and unlike a Journey or Capability, it typically *governs* one or more of them rather than being produced by any single one (`ARTIFACT-RELATIONSHIP-MODEL.md` section 3.1). Before creating a new Business Rule, check this table first -- a future, unrelated analysis needs to inherit an already-established rule like "structural edits never need confirmation," not silently re-derive it or contradict it.

| Rule ID | Statement (short) | Governs | Platform / App | From Analysis | Record |
| --- | --- | --- | --- | --- | --- |
| `BRULE-001` | A mapping's `kind` constrains which `targetType`s it may remap to | `CAP-004` | pdf-workflow / workflow-manager | `DA-003` | [pdf-workflow/workflow-manager/business-rules/business-rule-kind-constrains-remap-BRULE-001.md](../pdf-workflow/workflow-manager/business-rules/business-rule-kind-constrains-remap-BRULE-001.md) |
| `BRULE-002` | Only one field row may be in edit mode at a time | `CAP-004` | pdf-workflow / workflow-manager | `DA-003` | [pdf-workflow/workflow-manager/business-rules/business-rule-one-edit-at-a-time-BRULE-002.md](../pdf-workflow/workflow-manager/business-rules/business-rule-one-edit-at-a-time-BRULE-002.md) |
| `BRULE-003` | A page or section may be deleted only when it has zero children | `CAP-007` | pdf-workflow / workflow-manager | `DA-003` | [pdf-workflow/workflow-manager/business-rules/business-rule-delete-only-when-empty-BRULE-003.md](../pdf-workflow/workflow-manager/business-rules/business-rule-delete-only-when-empty-BRULE-003.md) |
| `BRULE-004` | A Section/Page is visible only if it has a visible match beneath it | `CAP-002` | pdf-workflow / workflow-manager | `DA-003` | [pdf-workflow/workflow-manager/business-rules/business-rule-hierarchical-filter-visibility-BRULE-004.md](../pdf-workflow/workflow-manager/business-rules/business-rule-hierarchical-filter-visibility-BRULE-004.md) |
| `BRULE-005` | Table and Card views must show identical data and share all state | `CAP-003` | pdf-workflow / workflow-manager | `DA-003` | [pdf-workflow/workflow-manager/business-rules/business-rule-table-card-parity-BRULE-005.md](../pdf-workflow/workflow-manager/business-rules/business-rule-table-card-parity-BRULE-005.md) |
| `BRULE-006` | This report applies only to workflows created via the PDF path | *(scope-defining -- no single Capability)* | pdf-workflow / workflow-manager | `DA-003` | [pdf-workflow/workflow-manager/business-rules/business-rule-pdf-path-only-BRULE-006.md](../pdf-workflow/workflow-manager/business-rules/business-rule-pdf-path-only-BRULE-006.md) |
| `BRULE-007` | Structural edits never require confirmation; unlink is the sole exception | `CAP-005`, `CAP-006`, `CAP-007`, `CAP-008` | pdf-workflow / workflow-manager | `DA-003` | [pdf-workflow/workflow-manager/business-rules/business-rule-no-confirmation-except-unlink-BRULE-007.md](../pdf-workflow/workflow-manager/business-rules/business-rule-no-confirmation-except-unlink-BRULE-007.md) |
| `BRULE-008` | Below ~900px, the mapping table uses horizontal scroll, never stacked cards | `CAP-001`, `CAP-002`, `CAP-004` | pdf-workflow / workflow-manager | `DA-003` | [pdf-workflow/workflow-manager/business-rules/business-rule-horizontal-scroll-mobile-BRULE-008.md](../pdf-workflow/workflow-manager/business-rules/business-rule-horizontal-scroll-mobile-BRULE-008.md) |

**First real entries, 2026-09-10** -- migrated from `DA-003`. `BRULE-007` and `BRULE-008` are the clearest real examples of why Business Rules are modeled separately from Capabilities in the first place: each genuinely governs *several* Capabilities at once (structural low-ceremony editing; responsive table behavior), rather than being produced by any single one. `BRULE-006` governs the screen's overall PDF-only scope rather than one Capability -- carried forward honestly as scope-defining, matching how the original analysis recorded it ("N/A -- a scope-defining rule rather than a capability of its own").

## Adding a Business Rule

1. Check this table first -- does an already-established rule already cover this, from a different feature or a different analysis?
2. If genuinely new, assign the next unused `BRULE-<number>`.
3. Create its record at `<platform-slug>/[<app-slug>/]business-rules/business-rule-<slug>-<BRULE-id>.md`.
4. Add one row to the table above.
5. In the Design Analysis that introduces or touches it, cite the `BRULE-<id>` and link to its record -- don't re-derive the ID locally.
6. A future analysis for an unrelated feature must check this table before inventing a rule that might already be established here -- silently re-deriving or contradicting an existing rule is exactly the failure mode this registry exists to prevent.
