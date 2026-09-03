# Source Registry

The running index of every source registered under [PRODUCT-SOURCE-MATERIAL-SPEC.md](specs/PRODUCT-SOURCE-MATERIAL-SPEC.md). Each row here has a full registration record at `sources/<source-id>.md`, filled from [PRODUCT-SOURCE-MATERIAL-TEMPLATE.md](templates/PRODUCT-SOURCE-MATERIAL-TEMPLATE.md).

This file is an index, not a record -- add one row per registered source here; put the actual detail (owner, access notes, readiness check, limitations) in that source's own file under `sources/`.

| Source ID | Name | Type | Version | Status | Readiness | Owner | Record |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SRC-001` | Cart Optimization Redesign -- Design Handoff Bundle v1.0 | Design material | 1.0 | Active | Ready with Limitations | Manali, Product Designer | [sources/checkout/cart-optimization/source-cart-optimization-SRC-001.md](sources/checkout/cart-optimization/source-cart-optimization-SRC-001.md) |

## Adding a Source

1. Assign the next unused `SRC-<number>`.
2. Fill Part 1 (and Part 2, once access is confirmed) of [PRODUCT-SOURCE-MATERIAL-TEMPLATE.md](templates/PRODUCT-SOURCE-MATERIAL-TEMPLATE.md) into `sources/<source-id>.md`.
3. Add one row to the table above, linking `Record` to that file.
4. Update the row's `Status` and `Readiness` whenever they change on the underlying record -- this index should never fall out of sync with the individual files it points to.
