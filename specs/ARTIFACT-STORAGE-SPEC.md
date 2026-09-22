# Artifact Storage Specification

## 1. Purpose

This is the single canonical reference for where every generated artifact lives on disk and how it is named. It closes the open item IMPLEMENTATION-PLAN.md has carried since early in this repository's build: *"Define artifact storage conventions for `design/`, `analysis/`, `requirements/`, and canonical GitHub Issues."*

Two problems this resolves, both found by actually auditing the repo rather than assumed:

- **Inconsistent nesting.** Only `design/` had a real multi-level convention (`design/<product-slug>/<feature-slug>/v<version>/`). Every other artifact type had a different, shallower, ad hoc depth invented as the first dry run went. (`product-slug` is now `platform-slug`, with an optional `app-slug` level added -- see section 4.)
- **Generic filenames.** `bundle.md`, `design-analysis.md`, `business-requirements.md`, and a bare `BPR-001.md` all depend entirely on their folder path for identity. Opened as an editor tab, attached to a message, or found in a search result, none of them says what they are. A file's name should identify it on its own, and the artifact ID already in every file's metadata should be visible in the name too, so the chain from Design Handoff Bundle through to Task can be followed by reading filenames, not only by opening files and reading their internal cross-reference tables.

## 2. Relationship to Other Artifacts

- [ARTIFACT-RELATIONSHIP-MODEL.md](ARTIFACT-RELATIONSHIP-MODEL.md) defines the *structural* data model -- artifact types, ID formats, and cardinality between them. This document defines their *physical location and filename* -- a different concern, kept separate rather than folded in.
- Every artifact-type spec's own storage-convention section (DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md §8, DESIGN-ANALYSIS-SPEC.md §2, etc.) now points here rather than defining its own convention independently, so there is exactly one place this can drift out of sync. The one deliberate exception is section 10 below -- the `design` branch's native-export shape is explicitly *not* governed by this convention.
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
| Journey | `journey` | `JRN-<number>`, global (not feature-scoped) |
| Capability | `capability` | `CAP-<number>`, global (not feature-scoped) |
| Business Rule | `business-rule` | `BRULE-<number>`, global (not feature-scoped) |

A filename this pattern produces is never ambiguous: `design-analysis-cart-optimization-DA-001.md` tells you the type, the feature, and the exact artifact, with no folder context required. Journey, Capability, and Business Rule are the one exception to the `feature-slug` component -- see section 4.1.

### 4.1 Journey, Capability, and Business Rule: Product-Level, Not Feature-Scoped

This section builds out [ARTIFACT-RELATIONSHIP-MODEL.md](ARTIFACT-RELATIONSHIP-MODEL.md) section 3.1's model into a real storage location. Every other artifact type above belongs to exactly one feature -- that's why `feature-slug` is part of its filename and its folder path. A Journey, Capability, or Business Rule is different in kind: it describes the product, and a later Design Analysis for a *different* feature may need to cite the same one. Nesting it under a feature-slug the way `sources/`, `analysis/`, etc. do would make that impossible to express -- a Capability shared by two features can't live under both.

So these three nest one level shallower -- directly under the platform (and app, where present), with no feature-slug segment at all:

```text
<platform-slug>/[<app-slug>/]capabilities/capability-<slug>-<CAP-id>.md
<platform-slug>/[<app-slug>/]journeys/journey-<slug>-<JRN-id>.md
<platform-slug>/[<app-slug>/]business-rules/business-rule-<slug>-<BRULE-id>.md
```

`<slug>` here is a short descriptive slug for the entity itself (e.g. `review-extraction-confidence`), not a feature. Each has a registry under `registries/` at the repository root, alongside `SOURCE-REGISTRY.md`, following the same "index here, real detail in the entity's own file" pattern: [CAPABILITY-REGISTRY.md](../registries/CAPABILITY-REGISTRY.md), [JOURNEY-REGISTRY.md](../registries/JOURNEY-REGISTRY.md), [BUSINESS-RULE-REGISTRY.md](../registries/BUSINESS-RULE-REGISTRY.md).

A Design Analysis still narrates a Capability/Journey/Business Rule in its own prose, for a reader who wants to understand the feature without jumping between files -- but the ID it uses is assigned from the registry, not invented locally, and its entry links out to the registry file as the canonical, cross-feature record.

## 4. Folder Convention

Platform (and app, where present) is always the top-level root; every artifact type nests *under* it, then feature: `<platform-slug>/[<app-slug>/]<type-root>/<feature-slug>/`. This matches the shape already used for the `design` branch (section 10) -- everything belonging to one platform/app lives under one subtree, browsable as a unit, rather than scattered across six type-named roots at the repository's own top level.

```text
<platform-slug>/[<app-slug>/]sources/<feature-slug>/source-<feature-slug>-<SRC-id>.md
<platform-slug>/[<app-slug>/]analysis/<feature-slug>/design-analysis-<feature-slug>-<DA-id>.md
<platform-slug>/[<app-slug>/]requirements/<feature-slug>/business-requirements-<feature-slug>-<REQSET-id>.md
<platform-slug>/[<app-slug>/]business-prs/<feature-slug>/business-pr-<feature-slug>-<BPR-id>.md
<platform-slug>/[<app-slug>/]tasks/<feature-slug>/canonical-task-<feature-slug>-<TASK-id>.md
<platform-slug>/[<app-slug>/]tasks/<feature-slug>/spike-<feature-slug>-<SPIKE-id>.md
<platform-slug>/[<app-slug>/]tasks/<feature-slug>/technical-plan-<feature-slug>-<TP-id>.md
```

The optional Technical Plan is defined in [TECHNICAL-AGENT-WORKFLOW.md](TECHNICAL-AGENT-WORKFLOW.md) section 4.1 -- most Tasks never produce one.

**Platform is always present** -- the top-level identifier for the overall project or monolith an artifact belongs to (previously called `product-slug`).

**App is optional.** It is inserted only when a platform genuinely contains multiple, distinct applications sharing one stack -- for example a platform with a web app, an API app, and an LLM layer, each wanting its own separable set of business artifacts. When a platform's features sit directly on it, with no meaningful application-level subdivision, the app segment is omitted entirely -- not left as an empty or placeholder folder. Section 6 shows both shapes.

Whether a given platform uses the app layer is a one-time structural decision made when the platform is first registered (see [PRODUCT-SOURCE-MATERIAL-SPEC.md](PRODUCT-SOURCE-MATERIAL-SPEC.md)), and should stay consistent across every feature under that platform -- a platform should not mix flat and app-nested features, since that would make the depth unpredictable when browsing.

The folder groups everything for one feature together for browsing; the filename identifies each file on its own once you're inside it, or once it's out of it.

## 5. `design/` -- Bundle-Level and Screen-Level Naming

`design/` (the hand-authored path, section 6.1 of DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md -- distinct from the `design` *branch*'s own native-export shape in section 10 below) keeps its existing versioned path, now `<platform-slug>/[<app-slug>/]design/<feature-slug>/v<version>/`, which already carries the version -- something no other artifact type has yet (see section 7). Its files use the same self-describing principle, substituting version or screen/flow ID for a sequential artifact ID since bundles and screens don't have one:

```text
<platform-slug>/[<app-slug>/]design/<feature-slug>/v<version>/
  design-handoff-<feature-slug>-v<version>.md      (bundle identity + manifest; was bundle.md)
  design-spec-<feature-slug>-v<version>.md          (narrative; was design-spec.md)
  screens/
    screen-<screen-id>-<feature-slug>.md            (was screens/<screen-id>.md)
  user-flows/
    flow-<flow-id>-<feature-slug>.mmd                (was user-flows/<flow-id>.mmd)
  assets/
    (tool-native formats, unchanged)
```

## 6. Worked Example: a Flat Platform

No flat-platform instance exists in this repository yet -- the real example, `pdf-workflow`/`workflow-manager`, uses the app-layer shape instead (see the next section). The pattern below is illustrative only; no files exist at these exact paths:

```text
<platform-slug>/design/<feature-slug>/v<version>/design-handoff-<feature-slug>-v<version>.md
<platform-slug>/design/<feature-slug>/v<version>/screens/screen-<screen-id>-<feature-slug>.md
<platform-slug>/design/<feature-slug>/v<version>/user-flows/flow-<flow-id>-<feature-slug>.mmd
<platform-slug>/sources/<feature-slug>/source-<feature-slug>-<SRC-id>.md
<platform-slug>/analysis/<feature-slug>/design-analysis-<feature-slug>-<DA-id>.md
<platform-slug>/requirements/<feature-slug>/business-requirements-<feature-slug>-<REQSET-id>.md
<platform-slug>/business-prs/<feature-slug>/business-pr-<feature-slug>-<BPR-id>.md
```

Reading down this list top to bottom is reading the controlled transformation (BUSINESS-PR-SPEC.md section 3) itself -- each filename names the artifact, and each artifact's own metadata table names the one before it. A flat platform (no distinct applications) omits the app segment entirely, as shown here -- this is the flat, two-level shape.

### A Platform With an App Layer

```text
<platform-slug>/<app-slug>/sources/<feature-slug>/source-<feature-slug>-<SRC-id>.md
<platform-slug>/<app-slug>/analysis/<feature-slug>/design-analysis-<feature-slug>-<DA-id>.md
```

A platform with, say, a web application and a separate API application uses two different `app-slug` values here, each with its own independent set of sources, analyses, requirements, and so on -- while still sharing one `platform-slug` and one FRAMEWORK-CONFIGURATION-SPEC.md configuration. `pdf-workflow` (`workflow-manager` app) is a real instance of this shape -- see `registries/SOURCE-REGISTRY.md` and `pdf-workflow/workflow-manager/analysis/mapping-report/design-analysis-mapping-report-DA-003.md`.

## 7. Versioning and Supersession

Only `design/` has a version folder today. Design Analysis, Business Requirements, and Business PRs can all be superseded too (DESIGN-ANALYSIS-SPEC.md, BUSINESS-REQUIREMENTS-SPEC.md section 11, REQUIREMENTS-VERSIONING-SPEC.md), but had nowhere for a new version to go without overwriting the old one. Under this convention, a new version gets a new artifact ID and therefore a new file, sitting beside the old one:

```text
<platform-slug>/analysis/<feature-slug>/design-analysis-<feature-slug>-DA-001.md   (Status: Superseded)
<platform-slug>/analysis/<feature-slug>/design-analysis-<feature-slug>-DA-002.md   (Status: Approved)
```

The superseded file is never deleted or overwritten -- its `Status` field changes, and the newer artifact's metadata records what it supersedes, per each artifact-type spec's own change-management section. This mirrors how `design/` already keeps every `v<version>/` folder rather than overwriting `v1.0` when `v1.1` ships.

## 8. Canonical Tasks and Spikes: Local Fallback

Per [CANONICAL-TASK-SPEC.md](CANONICAL-TASK-SPEC.md) section 2 and [PRD.md](../PRD.md) section 7.6, canonical Tasks and Spikes are meant to live as GitHub Issues once this repository has a real engineering-adjacent GitHub setup. That does not exist yet (see CLAUDE.md's open items). Until it does, the `<platform-slug>/[<app-slug>/]tasks/<feature-slug>/` layout in section 4 is the local-file fallback, so the Technical Agent stage is not blocked on git existing. When GitHub Issues become the actual store -- this repository's chosen adapter, see [GITHUB-PLATFORM-ADAPTER-SPEC.md](GITHUB-PLATFORM-ADAPTER-SPEC.md) section 7 -- a retired local file's `Status` is set to `Superseded` and a `GitHub Issue: #<number>` line is added; the file itself is kept, never deleted, per the same non-destructive rule as section 7 above.

## 9. Revision History

*What and when -- the current rule lives at the cited section, not here.*

| Date | Section | Change |
| --- | --- | --- |
| 2026-09-01 | 4 | Decided the app layer is optional, present only when a platform genuinely has multiple distinct applications, not required for every platform. |
| 2026-09-08 | 4 | Re-migrated to platform-first order (`<platform-slug>/[<app-slug>/]<type-root>/<feature-slug>/`), to match the `design` branch's own shape (section 10). The six former top-level type roots (`sources/`, `analysis/`, `requirements/`, `business-prs/`, `design/`, `tasks/`) no longer exist at the repository root. All real files at the time were moved and every cross-reference swept and verified. |
| 2026-08-31 | 6 | First real test of this convention: the cart-optimization dry-run files were renamed and moved to match it immediately, not left to apply "going forward" only. Every internal cross-reference (metadata tables, Stage Traces, the Source Registry) was swept and verified. |
| 2026-08-31 | 8 | Decided what links a retired local Task/Spike fallback file to its eventual GitHub Issue, once one exists -- see section 8 and `GITHUB-PLATFORM-ADAPTER-SPEC.md` section 7. |

## 10. The `design` Branch: An Independent Shape

[DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md](DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md) section 6.2 defines a second design-source location: a persistent `design` branch (not `main`), holding native Claude Design exports untouched. Its folder shape --

```text
<platform-slug>/[<app-slug>/]design/v<N>/
```

-- is **not** governed by this document's `<root>/<platform-slug>/[<app-slug>/]<feature-slug>/` convention (sections 3-4), despite the visual similarity. The distinction is deliberate: sections 3-9 above govern where this framework's own *generated, curated* artifacts live once produced -- Design Analysis, Business Requirements, the Business PR, all committed to `main`. A raw export sitting on `design` is unprocessed input the Business Agent reads, structurally the same category as an external Figma file or a PDF, just git-hosted instead of externally hosted -- it becomes a governed artifact only once a `sources/.../source-*.md` registration record (section 4 above) formally cites it. `main`'s own existing `design/<platform-slug>/[<app-slug>/]<feature-slug>/v<version>/` root (section 5) is unaffected and keeps governing the hand-authored bundle path (DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md section 6.1) and the one existing dry-run example under it.

**How a `main`-side artifact points back at `design`-branch source.** Since a native export carries no `bundleId`/version frontmatter to cite (unlike a hand-authored `bundle.md`), a `sources/.../source-*.md` record's `Location` field (`PRODUCT-SOURCE-MATERIAL-SPEC.md` section 4) and a Design Analysis's `Source Material` field (`DESIGN-ANALYSIS-SPEC.md` section 3) instead cite a three-part pointer:

```text
branch: design
path: <platform-slug>/[<app-slug>/]design/v<N>/
commit: <merge commit SHA>
```

A commit SHA pins an exact snapshot even after `design`'s tip advances to a later version -- `git show <SHA>:<path>/README.md` retrieves exactly what was analyzed. Registration is **per feature-slice**, not per version drop (a version can bundle several unrelated features) -- see DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md section 6.2 for the full rationale.

## 11. Open Decisions

- Should `feature-slug` be required to be globally unique across all platforms, or only unique within its `platform-slug` (and `app-slug`, where present)? (This convention currently assumes the latter -- two platforms could each have a `cart-optimization` feature without collision, since the platform-slug folder disambiguates them, but no spec states this explicitly yet.)
- ~~Should the storage hierarchy always include an app level, even for a platform with only one application?~~ **Resolved**: no -- app is optional, present only when a platform genuinely has multiple distinct applications. See section 4.
- Should this filename convention be enforced by a lint/check script, or remain a documented convention only?
- ~~When Canonical Tasks and Spikes do move to real GitHub Issues, what exactly links the retired local file to the Issue~~ -- **Resolved**, see section 8 above and GITHUB-PLATFORM-ADAPTER-SPEC.md section 7.
