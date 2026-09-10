# Journey Registry

The running index of every Journey registered under [ARTIFACT-STORAGE-SPEC.md](../specs/ARTIFACT-STORAGE-SPEC.md) section 4.1 and [ARTIFACT-RELATIONSHIP-MODEL.md](../specs/ARTIFACT-RELATIONSHIP-MODEL.md) section 3.1. Each row here has a full record at `<platform-slug>/[<app-slug>/]journeys/journey-<slug>-<JRN-id>.md`.

This file is an index, not a record -- add one row per Journey here; put the actual detail (actor, goal, ordered steps, which Capabilities it needs) in that Journey's own file.

A Journey is product-level, not feature-scoped: the same end-to-end goal can span features and get touched by more than one analysis over time. Map the Journey *before* decomposing it into Capabilities (`DESIGN-ANALYSIS-SPEC.md` section 4.6) -- a Journey is what proves a Capability is real and, eventually, whether it's shared across use cases or unique to one.

| Journey ID | Name | Actor | Platform / App | Uses Capabilities | From Analysis | Record |
| --- | --- | --- | --- | --- | --- | --- |
| `JRN-001` | Review and Correct a Low-Confidence Field Mapping | Workflow manager user (reviewer) | pdf-workflow / workflow-manager | `CAP-002`, `CAP-004` | `DA-003` | [pdf-workflow/workflow-manager/journeys/journey-review-correct-low-confidence-mapping-JRN-001.md](../pdf-workflow/workflow-manager/journeys/journey-review-correct-low-confidence-mapping-JRN-001.md) |
| `JRN-002` | Remove an Incorrectly Extracted Field | Workflow manager user (reviewer) | pdf-workflow / workflow-manager | `CAP-005` | `DA-003` | [pdf-workflow/workflow-manager/journeys/journey-remove-incorrectly-extracted-field-JRN-002.md](../pdf-workflow/workflow-manager/journeys/journey-remove-incorrectly-extracted-field-JRN-002.md) |
| `JRN-003` | Add a Section the Extraction Missed | Workflow manager user (reviewer) | pdf-workflow / workflow-manager | `CAP-006` | `DA-003` | [pdf-workflow/workflow-manager/journeys/journey-add-section-extraction-missed-JRN-003.md](../pdf-workflow/workflow-manager/journeys/journey-add-section-extraction-missed-JRN-003.md) |

**First real entries, 2026-09-10** -- re-instated from `DA-003`'s narrative "For example:" prose, where they'd been folded during the 2026-09-08 reformat (a real regression, self-flagged: that reformat removed exactly the addressability this registry now depends on). Same three journeys, same real steps, now given back a stable ID and a real file instead of being unreachable prose.

## Adding a Journey

1. Check this table first -- is an existing analysis's Journey actually the same end-to-end goal?
2. If genuinely new, assign the next unused `JRN-<number>`.
3. Create its record at `<platform-slug>/[<app-slug>/]journeys/journey-<slug>-<JRN-id>.md`.
4. Add one row to the table above.
5. Map the Journey *before* decomposing it into Capabilities -- see `DESIGN-ANALYSIS-SPEC.md` section 4.6.
6. Keep `Uses Capabilities` in sync with the record's own content, and with each cited Capability's own `Used By Journeys` row in `CAPABILITY-REGISTRY.md` -- the link is two-way, stated in both places, not implied from one.
