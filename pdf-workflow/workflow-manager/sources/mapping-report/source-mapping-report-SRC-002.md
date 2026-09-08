# Source: Mapping Report (Workflow Manager) -- Design Handoff v2

## Registration

| Field | Value |
| --- | --- |
| Source ID | `SRC-002` |
| Source Name | Mapping Report -- Design Handoff v2 |
| Source Type | Design material |
| Location | `branch: design`, `path: pdf-workflow/workflow-manager/design/v2/`, `commit: b29e1be0b4c0da414e831423991ae16b9b394b6c` -- per ARTIFACT-STORAGE-SPEC.md section 10's pointer format for native Claude Design exports on the `design` branch |
| Version | `2` (integer, matches the native export's own versioning -- DESIGN-HANDOFF-BUNDLE-SPEC.md section 6.2) |
| Status | Active |
| Owner | Manali, Producing Designer (`ROLE-005`) |
| Authority Level | Design Reviewer-accepted per `GATE-002`'s PR-description sign-off (PR #2, merged 2026-09-04) |
| Created At | 2026-09-03 (drop uploaded) |
| Effective At | 2026-09-04 (merge into `design`) |
| Registered By | Business Agent (this run) |
| Registered At | 2026-09-04 |
| Access Notes | Native Claude Design export: `README.md` (prose handoff), `PARITY_RULE.md`, `designs/Mapping Report.dc.html` + `designs/Mapping Report (Light).dc.html`, shared `_ds/nocturne-8201375c-.../` token bundle. This registration scopes only to the **Mapping Report** feature-slice of the v2 drop -- the same drop also contains Workflow Dashboard and Workflow Settings Dialog material, registered (or to be registered) separately, per DESIGN-HANDOFF-BUNDLE-SPEC.md section 6.2's per-feature-slice rule. |

## If This Source Is a Design Handoff Bundle

This source is the native-export shape (DESIGN-HANDOFF-BUNDLE-SPEC.md section 6.2), not the hand-authored `bundle.md` shape -- there is no separate bundle-manifest file to point to beyond the `Location` above. `README.md`'s "### 2. Mapping Report" section (plus the shared "Interactions & behavior," "State management," "Responsive behavior," and "Known UX issues" sections, where they describe Mapping Report specifically) is the reviewed narrative; `designs/Mapping Report.dc.html` / `(Light).dc.html` are the visual canvas artboards.

## Known Limitations

- **Two internal contradictions found in `README.md` itself, not yet reconciled by the source author** -- carried forward as `GAP-001` and `GAP-002` in the consuming Design Analysis (`DA-002`) rather than silently resolved here:
  1. The "Screens" section states the old dropdown-based remap pattern "was removed," replaced by an in-place expand-to-edit panel -- but the separate "Interactions & behavior" section still describes the old dropdown-`<select>` remap pattern as current.
  2. The "Known UX issues" section states unlink now opens a confirmation dialog and Save shows a toast -- but "Interactions & behavior" still says unlink is "optimistic, no confirm dialog in the reference."
- Mobile/tablet behavior for the mapping table is explicitly flagged in the source as an unmade decision ("decide with the user whether to horizontally scroll... or collapse... Don't silently pick one") -- not a gap in the source's completeness, but an explicit open business decision the source itself defers.
- No numeric bound is stated anywhere for how many pages, sections, or fields a workflow may contain, nor any limit on `FieldGroup` sub-field counts.
- `Mapping Card Layouts.dc.html` also existed in the v1 export under this same app but is superseded by this v2 material for Mapping Report and was not separately reviewed -- noted for completeness, not treated as a conflicting source.

## Related Sources

| Relationship | Source ID | Notes |
| --- | --- | --- |
| Related to | *(none registered yet)* | The same v2 drop's Workflow Dashboard and Workflow Settings Dialog material is unregistered as of this record -- register separately per feature-slice when analyzed. |

---

## Readiness Check

| Check | Result | Evidence or Action |
| --- | --- | --- |
| Source can be accessed | Pass | `design` branch, `pdf-workflow/workflow-manager/design/v2/`, verified readable at commit `b29e1be0` |
| Source identity is known | Pass | Branch/path/commit pointer above; native export, no separate bundle ID |
| Source version is known | Pass | `2` |
| Required source types are present (per active configuration) | Pass | Design material, per PRODUCT-SOURCE-MATERIAL-SPEC.md section 15's default profile |
| Source is readable and complete | Limited | `README.md`'s Mapping Report section is extensive and detailed; the two internal contradictions above and the deferred mobile-layout decision keep this from a clean `Pass` |
| Conflicts with another registered source are detected | No | No other registered source addresses Mapping Report |
| Authority of this source is known | Pass | `ROLE-005` Producing Designer, sign-off recorded on PR #2 |

**Readiness outcome:** `Ready with Limitations`

The limitations above (two unreconciled internal contradictions, one explicitly-deferred mobile decision, no stated structural bounds) are carried forward into `DA-002` per PRODUCT-SOURCE-MATERIAL-SPEC.md section 9 -- as `GAP-001`, `GAP-002`, and corresponding `DEC-*` items, not silently resolved.

**Blocking reason (if `Blocked`):** Not Applicable
