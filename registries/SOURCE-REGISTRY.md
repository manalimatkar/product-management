# Source Registry

The running index of every source registered under [PRODUCT-SOURCE-MATERIAL-SPEC.md](../specs/PRODUCT-SOURCE-MATERIAL-SPEC.md). Each row here has a full registration record at `<platform-slug>/[<app-slug>/]sources/<feature-slug>/source-<feature-slug>-<source-id>.md`, filled from [PRODUCT-SOURCE-MATERIAL-TEMPLATE.md](../templates/PRODUCT-SOURCE-MATERIAL-TEMPLATE.md).

This file is an index, not a record -- add one row per registered source here; put the actual detail (owner, access notes, readiness check, limitations) in that source's own file under its platform/app's `sources/` folder.

| Source ID | Name | Type | Version | Status | Readiness | Owner | Record |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SRC-003` | Mapping Report -- Design Handoff v4 (pdf-workflow/workflow-manager, native Claude Design export on `design` branch) | Design material | 4 | Active | Ready with Limitations | Manali, Producing Designer | [pdf-workflow/workflow-manager/sources/mapping-report/source-mapping-report-SRC-003.md](../pdf-workflow/workflow-manager/sources/mapping-report/source-mapping-report-SRC-003.md) |

**`SRC-001`/`SRC-002` cleared 2026-09-08**, not reused. `SRC-001` (illustrative `checkout/cart-optimization` dry run) and `SRC-002` (a Mapping Report analysis mistakenly built against the `design` branch's v2 test drop, not the specified v4) were both removed along with all downstream artifacts. `SRC-003` above is the real, correctly-sourced replacement. See CLAUDE.md open items 17-19.

## Adding a Source

1. Assign the next unused `SRC-<number>`.
2. Fill Part 1 (and Part 2, once access is confirmed) of [PRODUCT-SOURCE-MATERIAL-TEMPLATE.md](../templates/PRODUCT-SOURCE-MATERIAL-TEMPLATE.md) into `<platform-slug>/[<app-slug>/]sources/<feature-slug>/source-<feature-slug>-<source-id>.md`.
3. Add one row to the table above, linking `Record` to that file.
4. Update the row's `Status` and `Readiness` whenever they change on the underlying record -- this index should never fall out of sync with the individual files it points to.
