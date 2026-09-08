# Source Registry

The running index of every source registered under [PRODUCT-SOURCE-MATERIAL-SPEC.md](specs/PRODUCT-SOURCE-MATERIAL-SPEC.md). Each row here has a full registration record at `<platform-slug>/[<app-slug>/]sources/<feature-slug>/source-<feature-slug>-<source-id>.md`, filled from [PRODUCT-SOURCE-MATERIAL-TEMPLATE.md](templates/PRODUCT-SOURCE-MATERIAL-TEMPLATE.md).

This file is an index, not a record -- add one row per registered source here; put the actual detail (owner, access notes, readiness check, limitations) in that source's own file under its platform/app's `sources/` folder.

| Source ID | Name | Type | Version | Status | Readiness | Owner | Record |
| --- | --- | --- | --- | --- | --- | --- | --- |
| *(none currently registered)* | | | | | | | |

**Cleared 2026-09-08.** The illustrative `checkout/cart-optimization` dry run (`SRC-001`) and the `pdf-workflow/workflow-manager` Mapping Report analysis built against the wrong drop version (`SRC-002`, based on v2 -- should have used v4) were both removed, along with all their downstream artifacts (Design Analysis, Business Requirements, Business PR) and the `design`-branch content they pointed at. Next real registration starts fresh against v4. See CLAUDE.md open item 18.

## Adding a Source

1. Assign the next unused `SRC-<number>`.
2. Fill Part 1 (and Part 2, once access is confirmed) of [PRODUCT-SOURCE-MATERIAL-TEMPLATE.md](templates/PRODUCT-SOURCE-MATERIAL-TEMPLATE.md) into `<platform-slug>/[<app-slug>/]sources/<feature-slug>/source-<feature-slug>-<source-id>.md`.
3. Add one row to the table above, linking `Record` to that file.
4. Update the row's `Status` and `Readiness` whenever they change on the underlying record -- this index should never fall out of sync with the individual files it points to.
