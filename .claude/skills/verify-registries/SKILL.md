---
name: verify-registries
description: Checks the Journey/Capability/Business Rule registries and every Design Analysis that cites them are actually consistent -- every registry row resolves to a real file, every two-way "used by"/"uses" link is genuinely two-way, every JRN-/CAP-/BRULE- ID cited anywhere is actually registered. Use after adding or editing a registry entry, or after a Design Analysis cites a new product-level ID.
---

# Verify Registries

`verify-design-analysis` checks *inside* one Design Analysis file. This is its cross-repo sibling, for the three product-level registries `ARTIFACT-RELATIONSHIP-MODEL.md` section 3.1 defines -- Journey, Capability, and Business Rule are global IDs, assigned once from a registry, cited by any Design Analysis that needs them. Nothing checks that consistency holds across files except this.

## When to run this

- After adding a new Journey, Capability, or Business Rule to its registry.
- After editing an existing entity's own record (especially its "Used by journeys" / "Uses capabilities" fields).
- After a Design Analysis cites a `JRN-`/`CAP-`/`BRULE-` ID, new or existing.
- Before asking for a PR to be opened on any change touching a registry or an entity record.

## How to run it

```bash
python .github/scripts/verify_registries.py
```

## What it checks

1. Every ID a registry table lists has a Record link that resolves to a real file, and that file's own ID field matches -- catches a registry row and its record drifting apart.
2. No ID is duplicated within one registry.
3. Two-way links are actually two-way -- a Capability saying it's used by a Journey only counts if that Journey's own record links the Capability back. A link stated on only one side is worse than no link: it looks verified but isn't.
4. Every `JRN-`/`CAP-`/`BRULE-` ID cited anywhere in a real Design Analysis (`**/analysis/**/*.md`) actually exists in its registry -- a Design Analysis must never reference a product-level ID nobody registered.

**Only real markdown links count as citations for check 3**, deliberately -- not any backtick-quoted mention of an ID. A record's own prose can legitimately say something like *"none yet -- `JRN-001`-003 don't walk this path"* without that being a real, followable citation. This was a genuine false positive caught while building the tool, not a hypothetical edge case -- fixed by requiring an actual `[JRN-001](...)` link, not just backticks.

## Reading the output

- **`PASSED`, exit code 0** -- every registry entry resolves, every two-way link matches, every citation is registered.
- **`FAILED`, exit code 1** -- each error names exactly which registry, which ID, and what's wrong. Fix everything listed before treating a registry change as done.

## Verified against

Tested against the real registries before being trusted: a deliberately broken Record link (correctly caught), and the real migration of `DA-003`'s `CAP-001`-`008`, `BRULE-001`-`008`, and `JRN-001`-`003` into the registries for the first time (correctly passed once the false positive above was fixed).
