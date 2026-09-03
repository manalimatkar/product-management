# Artifact Storage Specification

## 1. Purpose

This is the single canonical reference for where every generated artifact lives on disk and how it is named. It closes the open item IMPLEMENTATION-PLAN.md has carried since early in this repository's build: *"Define artifact storage conventions for `design/`, `analysis/`, `requirements/`, and canonical GitHub Issues."*

Two problems this resolves, both found by actually auditing the repo rather than assumed:

- **Inconsistent nesting.** Only `design/` had a real multi-level convention (`design/<product-slug>/<feature-slug>/v<version>/`). Every other artifact type had a different, shallower, ad hoc depth invented as the first dry run went. (Terminology updated 2026-09-01, see section 4 -- `product-slug` is now `platform-slug`, with an optional `app-slug` level added.)
- **Generic filenames.** `bundle.md`, `design-analysis.md`, `business-requirements.md`, and a bare `BPR-001.md` all depend entirely on their folder path for identity. Opened as an editor tab, attached to a message, or found in a search result, none of them says what they are. A file's name should identify it on its own, and the artifact ID already in every file's metadata should be visible in the name too, so the chain from Design Handoff Bundle through to Task can be followed by reading filenames, not only by opening files and reading their internal cross-reference tables.

## 2. Relationship to Other Artifacts

- [ARTIFACT-RELATIONSHIP-MODEL.md](ARTIFACT-RELATIONSHIP-MODEL.md) defines the *structural* data model -- artifact types, ID formats, and cardinality between them. This document defines their *physical location and filename* -- a different concern, kept separate rather than folded in.
- Every artifact-type spec's own storage-convention section (DESIGN-HANDOFF-BUNDLE-SPEC.md §8, DESIGN-ANALYSIS-SPEC.md §2, etc.) now points here rather than defining its own convention independently, so there is exactly one place this can drift out of sync.
- [PRD.md](../PRD.md) section 7.7 requires each Design Handoff Bundle to be committed under a feature-specific `design/` area with an explicit version -- this document is the concrete realization of that requirement, extended consistently to every other artifact type.

## 3. Naming Convention

Every artifact file (outside `design/`'s bundle-level and screen-level files, which use the pattern in section 5) follows:

```text
<type-slug>-<feature-slug>-<artifact-id>.md
```

| Component | Meaning | Example |
| --- | --- | --- |
| `type-slug` | Fixed short name for the artifact type (table below) | `design-analysis` |
| `feature-slug` | The feature this artifact belongs to -- same slug used in its `design/` path | `cart-optimization` |
| `artifact-id` | The artifact's own stable ID, exactly as it appears in that artifact's metadata | `DA-001` |

### Type slugs

| Artifact Type | `type-slug` | ID format (from ARTIFACT-RELATIONSHIP-MODEL.md) |
| --- | --- | --- |
| Source Registration Record | `source` | `SRC-<number>` |
| Design Analysis | `design-analysis` | `DA-<number>` |
| Business Requirements | `business-requirements` | `REQSET-<number>` |
| Business PR | `business-pr` | `BPR-<number>` |
| Canonical Task (local fallback) | `canonical-task` | `TASK-<number>` |
| Spike (local fallback) | `spike` | `SPIKE-<number>` |
| Technical Plan (optional) | `technical-plan` | `TP-<number>` |

A filename this pattern produces is never ambiguous: `design-analysis-cart-optimization-DA-001.md` tells you the type, the feature, and the exact artifact, with no folder context required.

## 4. Folder Convention

**Revised 2026-09-01.** Every artifact type nests under its own root, then `<platform-slug>/[<app-slug>/]<feature-slug>/`:

```text
sources/<platform-slug>/[<app-slug>/]<feature-slug>/source-<feature-slug>-<SRC-id>.md
analysis/<platform-slug>/[<app-slug>/]<feature-slug>/design-analysis-<feature-slug>-<DA-id>.md
requirements/<platform-slug>/[<app-slug>/]<feature-slug>/business-requirements-<feature-slug>-<REQSET-id>.md
business-prs/<platform-slug>/[<app-slug>/]<feature-slug>/business-pr-<feature-slug>-<BPR-id>.md
tasks/<platform-slug>/[<app-slug>/]<feature-slug>/canonical-task-<feature-slug>-<TASK-id>.md
tasks/<platform-slug>/[<app-slug>/]<feature-slug>/spike-<feature-slug>-<SPIKE-id>.md
tasks/<platform-slug>/[<app-slug>/]<feature-slug>/technical-plan-<feature-slug>-<TP-id>.md
```

The optional Technical Plan is defined in [TECHNICAL-AGENT-WORKFLOW.md](TECHNICAL-AGENT-WORKFLOW.md) section 4.1 -- most Tasks never produce one.

**Platform is always present** -- the top-level identifier for the overall project or monolith an artifact belongs to (what this section called `product-slug` before 2026-09-01).

**App is optional.** It is inserted only when a platform genuinely contains multiple, distinct applications sharing one stack -- for example a platform with a web app, an API app, and an LLM layer, each wanting its own separable set of business artifacts. When a platform's features sit directly on it, with no meaningful application-level subdivision, the app segment is omitted entirely -- not left as an empty or placeholder folder. Section 6 shows both shapes.

Whether a given platform uses the app layer is a one-time structural decision made when the platform is first registered (see [PRODUCT-SOURCE-MATERIAL-SPEC.md](PRODUCT-SOURCE-MATERIAL-SPEC.md)), and should stay consistent across every feature under that platform -- a platform should not mix flat and app-nested features, since that would make the depth unpredictable when browsing.

The folder groups everything for one feature together for browsing; the filename identifies each file on its own once you're inside it, or once it's out of it.

## 5. `design/` -- Bundle-Level and Screen-Level Naming

`design/` keeps its existing versioned path, now `design/<platform-slug>/[<app-slug>/]<feature-slug>/v<version>/` (DESIGN-HANDOFF-BUNDLE-SPEC.md section 8), which already carries the version -- something no other artifact type has yet (see section 7). Its files use the same self-describing principle, substituting version or screen/flow ID for a sequential artifact ID since bundles and screens don't have one:

```text
design/<platform-slug>/[<app-slug>/]<feature-slug>/v<version>/
  design-handoff-<feature-slug>-v<version>.md      (bundle identity + manifest; was bundle.md)
  design-spec-<feature-slug>-v<version>.md          (narrative; was design-spec.md)
  screens/
    screen-<screen-id>-<feature-slug>.md            (was screens/<screen-id>.md)
  user-flows/
    flow-<flow-id>-<feature-slug>.mmd                (was user-flows/<flow-id>.mmd)
  assets/
    (tool-native formats, unchanged)
```

## 6. Worked Example: Cart Optimization

The full chain for the dry-run "cart optimization" example, after migrating to this convention (2026-08-31):

```text
design/checkout/cart-optimization/v1.0/design-handoff-cart-optimization-v1.0.md
design/checkout/cart-optimization/v1.0/screens/screen-cart-empty-cart-optimization.md
design/checkout/cart-optimization/v1.0/screens/screen-cart-full-cart-optimization.md
design/checkout/cart-optimization/v1.0/user-flows/flow-add-item-cart-optimization.mmd
sources/checkout/cart-optimization/source-cart-optimization-SRC-001.md
analysis/checkout/cart-optimization/design-analysis-cart-optimization-DA-001.md
requirements/checkout/cart-optimization/business-requirements-cart-optimization-REQSET-001.md
business-prs/checkout/cart-optimization/business-pr-cart-optimization-BPR-001.md
```

Reading down this list top to bottom is reading the controlled transformation (BUSINESS-PR-SPEC.md section 3) itself -- each filename names the artifact, and each artifact's own metadata table names the one before it.

`checkout` is this example's `platform-slug`. Nothing about this fictional shopping platform describes multiple distinct applications, so the app segment is omitted -- this is the flat, two-level shape. No files moved when the app-layer option was added 2026-09-01; only the term `product-slug` changed to `platform-slug` throughout this repository's specs.

### Illustrative Only: a Platform With an App Layer

Purely to show the other shape -- not a real registered platform in this repository, and no files exist at these paths:

```text
sources/<platform-slug>/<app-slug>/<feature-slug>/source-<feature-slug>-SRC-001.md
analysis/<platform-slug>/<app-slug>/<feature-slug>/design-analysis-<feature-slug>-DA-001.md
```

A platform with, say, a web application and a separate API application would use two different `app-slug` values here, each with its own independent set of sources, analyses, requirements, and so on -- while still sharing one `platform-slug` and one FRAMEWORK-CONFIGURATION-SPEC.md configuration.

## 7. Versioning and Supersession

Only `design/` has a version folder today. Design Analysis, Business Requirements, and Business PRs can all be superseded too (DESIGN-ANALYSIS-SPEC.md, BUSINESS-REQUIREMENTS-SPEC.md section 11, REQUIREMENTS-VERSIONING-SPEC.md), but had nowhere for a new version to go without overwriting the old one. Under this convention, a new version gets a new artifact ID and therefore a new file, sitting beside the old one:

```text
analysis/checkout/cart-optimization/design-analysis-cart-optimization-DA-001.md   (Status: Superseded)
analysis/checkout/cart-optimization/design-analysis-cart-optimization-DA-002.md   (Status: Approved)
```

The superseded file is never deleted or overwritten -- its `Status` field changes, and the newer artifact's metadata records what it supersedes, per each artifact-type spec's own change-management section. This mirrors how `design/` already keeps every `v<version>/` folder rather than overwriting `v1.0` when `v1.1` ships.

## 8. Canonical Tasks and Spikes: Local Fallback

Per [CANONICAL-TASK-SPEC.md](CANONICAL-TASK-SPEC.md) section 2 and [PRD.md](../PRD.md) section 7.6, canonical Tasks and Spikes are meant to live as GitHub Issues once this repository has a real engineering-adjacent GitHub setup. That does not exist yet (see CLAUDE.md's open items). Until it does, the `tasks/<platform-slug>/[<app-slug>/]<feature-slug>/` layout in section 4 is the local-file fallback, so the Technical Agent stage is not blocked on git existing. When GitHub Issues become the actual store -- confirmed 2026-08-31 as this repository's chosen adapter, see [GITHUB-PLATFORM-ADAPTER-SPEC.md](GITHUB-PLATFORM-ADAPTER-SPEC.md) section 7 -- a retired local file's `Status` is set to `Superseded` and a `GitHub Issue: #<number>` line is added; the file itself is kept, never deleted, per the same non-destructive rule as section 7 above.

## 9. Migration Note

On 2026-08-31 the cart-optimization dry-run files were renamed and moved to match this convention (see section 6) -- this was the first real test of the convention, done immediately rather than left to apply "going forward" only, at the user's explicit direction. Every internal cross-reference (metadata tables, Stage Traces, the Source Registry) was swept and verified afterward.

## 10. Open Decisions

- Should `feature-slug` be required to be globally unique across all platforms, or only unique within its `platform-slug` (and `app-slug`, where present)? (This convention currently assumes the latter -- two platforms could each have a `cart-optimization` feature without collision, since the platform-slug folder disambiguates them, but no spec states this explicitly yet.)
- ~~Should the storage hierarchy always include an app level, even for a platform with only one application?~~ Resolved 2026-09-01: no -- app is optional, present only when a platform genuinely has multiple distinct applications. See section 4.
- Should this filename convention be enforced by a lint/check script, or remain a documented convention only?
- ~~When Canonical Tasks and Spikes do move to real GitHub Issues, what exactly links the retired local file to the Issue~~ -- resolved 2026-08-31, see section 8 above and GITHUB-PLATFORM-ADAPTER-SPEC.md section 7.
