# Design Handoff Bundle Specification

## 1. Purpose

This specification defines the structure and file layout for a versioned Design Handoff Bundle: the optional, UI-oriented source-material type described conceptually in [PRODUCT-SOURCE-MATERIAL-SPEC.md](PRODUCT-SOURCE-MATERIAL-SPEC.md) section 7.

This repository is a product-management and governance framework, not an engineering repository. The bundle records design intent, structure, and business-relevant behavior so the Business Agent can produce a Design Analysis. It must never become a technical implementation specification.

**This bundle format is deliberately scalable, not all-or-nothing.** PRD.md already names several shapes a design source can take -- a fully detailed handoff, a bare Figma link with a short note, a written Markdown document with attached screenshots, or Claude Design wireframe images. All of them register through this same structure; the difference is how much of it is filled in. Section 6.1 shows this range concretely, from a one-paragraph reference through a fully detailed screen record. There is exactly one design-source format in this repository, not one format for "real" bundles and an undocumented fallback for everything else.

## 2. Relationship to Other Artifacts

- [PRODUCT-SOURCE-MATERIAL-SPEC.md](PRODUCT-SOURCE-MATERIAL-SPEC.md) section 7 defines the Design Handoff Bundle conceptually as one configured source type among several. This document is the concrete, fillable realization of that section for repositories that choose it.
- [DESIGN-ANALYSIS-SPEC.md](DESIGN-ANALYSIS-SPEC.md) section 4.3 defines what the Business Agent extracts from a bundle; section 6 defines what it must never infer. This structure is written so that boundary is easy to keep, not only a matter of agent discipline.
- [BUSINESS-REPOSITORY-WORKFLOW.md](BUSINESS-REPOSITORY-WORKFLOW.md) describes how a committed bundle enters the Business Agent process.
- [REQUIREMENTS-VERSIONING-SPEC.md](REQUIREMENTS-VERSIONING-SPEC.md) section 4's `MAJOR.MINOR` version format is reused here for bundle versioning, so the same version vocabulary applies across the repository.
- [FRAMEWORK-CONFIGURATION-SPEC.md](FRAMEWORK-CONFIGURATION-SPEC.md) section 10 governs who may hold which role against this artifact; this document does not hardcode role names.
- Section 6.2 below (the native Claude Design export shape) has its own storage location -- a persistent `design` branch, not `ARTIFACT-STORAGE-SPEC.md`'s `<root>/<platform-slug>/...` convention -- and its own trigger mechanism, detailed in [GITHUB-PLATFORM-ADAPTER-SPEC.md](GITHUB-PLATFORM-ADAPTER-SPEC.md) section 6.1.
- [CLAUDE-DESIGN-READING-SPEC.md](CLAUDE-DESIGN-READING-SPEC.md) is the sibling document for *reading* a native Claude Design export accurately -- this document defines its storage and format only, per section 3's own stated scope.

## 3. Scope

This specification covers:

- bundle-level identity and manifest (`bundle.md`, shorthand for the real filename pattern in [ARTIFACT-STORAGE-SPEC.md](ARTIFACT-STORAGE-SPEC.md) section 5)
- screen or page-level structure (`screens/*.md`, same shorthand)
- how the bundle scales down to a lightweight design reference (section 6.1)
- the boundary between design intent and technical implementation
- the distinction between a bundle's own status and its source readiness

It does not define how the Business Agent interprets a bundle (see [DESIGN-ANALYSIS-SPEC.md](DESIGN-ANALYSIS-SPEC.md)) or how a bundle is registered, checked for readiness, or superseded as a source (see [PRODUCT-SOURCE-MATERIAL-SPEC.md](PRODUCT-SOURCE-MATERIAL-SPEC.md) sections 8-9 and 12).

See also [EVIDENCE-SPEC.md](EVIDENCE-SPEC.md) for how the evidence classifications used in this bundle (section 6) feed the repository-wide traceability chain.

## 4. Design vs. Implementation Boundary

Per [DESIGN-ANALYSIS-SPEC.md](DESIGN-ANALYSIS-SPEC.md) section 6, a Design Handoff Bundle must never encode, as a binding element of the bundle itself:

- APIs, endpoints, HTTP methods, or request/response payloads
- databases, storage services, or caching mechanisms
- specific browser or OS version support
- numeric performance targets not explicitly stated by the business
- service boundaries, deployment, or infrastructure choices

Interactions are recorded as **trigger to business outcome**, never as a technical call contract. Where the bundle records a platform or experience constraint (for example, an accessibility level, or a stated need to work offline), it is recorded because it is a stated business or product requirement, not because it constrains a technical implementation. Anything that reads like an implementation decision belongs to the Technical Agent's later analysis, not the bundle.

## 5. `bundle.md` -- Bundle Identity and Manifest

**Naming note:** this section uses `bundle.md` as shorthand throughout. The actual filename this repository uses is `design-handoff-<feature-slug>-v<version>.md`, per [ARTIFACT-STORAGE-SPEC.md](ARTIFACT-STORAGE-SPEC.md) section 5 -- the same self-describing-filename rule applied to every other artifact type in this repository.

`bundle.md` satisfies the general Source Metadata fields required by [PRODUCT-SOURCE-MATERIAL-SPEC.md](PRODUCT-SOURCE-MATERIAL-SPEC.md) section 4 (Source ID, Source Name, Version, Status, Owner, timestamps) together with the Design Handoff Bundle-specific fields required by section 7 (included files, external references, known limitations, approval or acceptance status).

It opens with a YAML frontmatter block for the compact, structured fields, followed by Markdown sections for anything narrative. YAML rather than JSON because it is meant to be hand-edited by a designer -- no braces, no trailing-comma errors, comments allowed.

```markdown
---
bundleId: checkout/cart-optimization@v1.0        # {platformSlug}/[{appSlug}/]{featureSlug}@v{MAJOR.MINOR} -- fulfills Source ID and bundle ID (PRODUCT-SOURCE-MATERIAL-SPEC.md sections 4 and 7). appSlug segment present only when the platform has an app layer (ARTIFACT-STORAGE-SPEC.md section 4).
bundleName: Cart Optimization Redesign            # Source Name
platformSlug: checkout                            # was productSlug before 2026-09-01
appSlug: null                                      # set only when this platform has an app-level subdivision (ARTIFACT-STORAGE-SPEC.md section 4); null/omitted otherwise
featureSlug: cart-optimization
version: "1.0"                                    # MAJOR.MINOR, consistent with REQUIREMENTS-VERSIONING-SPEC.md section 4. Draft iterations may use 0.1, 0.2, etc.
status: Draft                                     # Draft / In Review / Approved / Superseded / Withdrawn -- the bundle's own authoring lifecycle. Not the same as readiness -- see section 7.
readiness: null                                   # Ready / Ready with Limitations / Blocked / Not Applicable -- assigned by the intake process, not the designer. Absent (null) until intake has run.
owner:
  name: YOUR NAME
  role: Product Designer                          # Role per the active Role Configuration (FRAMEWORK-CONFIGURATION-SPEC.md section 10). Illustrative, not a closed set.
reviewedBy: []                                    # Optional bundle-level design acceptance -- [{name, role, reviewedAt}]. Separate from, and does not substitute for, the Business Owner or Architect approval gates.
createdAt: 2026-08-31
effectiveAt: null                                 # Date the bundle becomes the applicable source, if different from createdAt.
supersedes: null                                  # bundleId this version supersedes, if any.
supersededBy: null
externalReferences:                                # Links to the external design tool(s) that produced this bundle, or that this is entirely a reference to. Design-tool choice is provenance, not a business or technical decision.
  - tool: Figma
    url: https://figma.com/design/FILE_KEY
    note: Source frames for all screens
knownLimitations:                                  # Explicit gaps, unreadable areas, or excluded material, per PRODUCT-SOURCE-MATERIAL-SPEC.md section 10.
  - "example: no mobile frames provided"
experienceRequirements:                            # Business/product-level experience commitments only. Deliberately excludes specific browser/OS versions and numeric performance targets -- see section 4.
  targetPlatforms: [web desktop]
  accessibility: "WCAG 2.1 Level AA"
  rtl: false
  darkMode: false
tags: [checkout, cart, ux-improvement]
businessContext:
  objective: Reduce cart abandonment and improve item-management experience
  successMetrics: [Cart abandonment rate, Time to checkout]
  priority: High                                   # Low / Medium / High / Critical
  targetRelease: Q4 2026                            # Free-form target timing, per the active configuration.
---

## Manifest

### Screens

| ID | Name | File | States | Depends On |
| --- | --- | --- | --- | --- |
| `cart-empty` | Empty Cart State | `screens/screen-cart-empty-cart-optimization.md` | default | -- |
| `cart-full` | Cart with Items | `screens/screen-cart-full-cart-optimization.md` | default, editing | cart-empty |

*(Leave this table empty, or omit it, when the bundle is a lightweight reference with no structured screen breakdown -- see section 6.1.)*

### Flows

| ID | Name | File | Start Screen | End Screen |
| --- | --- | --- | --- | --- |
| `add-item-flow` | User Adds Item to Cart | `user-flows/flow-add-item-cart-optimization.mmd` | product-detail | cart-full |

### Assets

Design tokens and content assets referenced by the bundle, if any -- point at whatever format the design system already exports (these are tool-native files, not authored in this framework):

- Colors: `assets/colors.*`
- Typography: `assets/typography.*`
- Spacing: `assets/spacing.*`
- Icons: `assets/icons/`
- Images: `assets/images/`
```

### Field-to-requirement mapping

| Field | Satisfies |
| --- | --- |
| `bundleId`, `bundleName` | Source ID, Source Name (PRODUCT-SOURCE-MATERIAL-SPEC.md 4) |
| `version`, `supersedes`, `supersededBy` | Source Version and supersession (PRODUCT-SOURCE-MATERIAL-SPEC.md 5, 12) |
| `status` | Bundle's own lifecycle (this document, section 7) |
| `readiness` | Readiness outcome (PRODUCT-SOURCE-MATERIAL-SPEC.md 9) |
| `owner`, `reviewedBy` | Owner and approval/acceptance status (PRODUCT-SOURCE-MATERIAL-SPEC.md 4, 7) |
| `createdAt`, `effectiveAt` | Created At, Effective At (PRODUCT-SOURCE-MATERIAL-SPEC.md 4) |
| Manifest, `externalReferences` | Included files/folders, external references (PRODUCT-SOURCE-MATERIAL-SPEC.md 7) |
| `knownLimitations` | Completeness and quality record (PRODUCT-SOURCE-MATERIAL-SPEC.md 10) |

## 6. `screens/*.md` -- Screen or Page Definition

**Naming note:** the actual filename is `screen-<screen-id>-<feature-slug>.md`, per [ARTIFACT-STORAGE-SPEC.md](ARTIFACT-STORAGE-SPEC.md) section 5.

Each screen or page referenced in the Manifest gets its own file. A screen file records, per state: what the state is, whether it is directly shown or inferred, which elements are present, and what each interactive element's trigger and business-level outcome are.

```markdown
---
screenId: cart-full
screenName: Cart with Items
externalReference:                       # Optional pointer into the external design tool for this screen. Provenance only.
  tool: Figma
  fileKey: abc123xyz
  nodeId: "1:42"
designTokensUsed: [color-primary, color-error, typography-heading-2, typography-body-1, spacing-sm, spacing-md]
---

## State: default

**Description:** Cart displaying one or more items, ready for interaction.
**Evidence:** Explicit

### Elements & Interactions

| Element ID | Type | Label | Trigger | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- |
| `header` | header | Your Cart | -- | -- | -- |
| `item-list` | list | Cart Items | -- | -- | -- |
| `remove-btn` | button | Remove | click | shows a confirmation before removing the item | Explicit |
| `confirm-remove-btn` | button | Confirm Remove | click | removes the item from the cart and updates the totals | Strongly Implied |
| `coupon-input` | input | Coupon Code | -- | -- | -- |
| `coupon-btn` | button | Apply | click | validates the coupon; on success shows a confirmation and applies the discount, on failure shows an inline error and keeps the input focused | Explicit |

## State: editing

**Description:** User is changing an item's quantity.
**Evidence:** Strongly Implied
**Diff from `default`:** the item row's quantity control is visually highlighted as active.

<!-- Duplicate the "## State: <name>" block for each additional state. Elements with no interaction leave Trigger/Outcome/Evidence as "--". -->
```

`type` is an open, non-exhaustive category (`header`, `button`, `input`, `list`, `card`, `modal`, `form-group`, `image`, `icon`, `group`, `spacer`, `other`, or whatever the active design system defines) -- not a closed enum. Outcomes must never include HTTP methods, endpoints, payloads, or other technical implementation detail (DESIGN-ANALYSIS-SPEC.md section 6); they describe the resulting user-visible or business outcome in plain language. `Evidence` uses the vocabulary from [DESIGN-ANALYSIS-SPEC.md](DESIGN-ANALYSIS-SPEC.md) section 5 (`Explicit` / `Strongly Implied` / `Assumption` / `Decision Required`) -- an optional designer-supplied hint; the Business Agent still performs its own classification during analysis.

### 6.1 Scaling Down: Lightweight Design References

Not every design source is a fully detailed handoff, and this format does not require one. The same `bundle.md` + `screens/*.md` structure scales down cleanly:

**A bare external-tool reference** (e.g. a Figma file with no local breakdown yet): fill only `bundle.md`'s frontmatter and `externalReferences`; leave the Manifest's Screens table empty or omit it; use `knownLimitations` to say the detail lives in the external tool, not here. No `screens/*.md` files exist yet. The Business Agent, and any human analyst, works from the external tool directly, and the Design Analysis records that explicitly as its source.

**Written instructions or a PDF with screenshots**: `bundle.md`'s frontmatter still carries identity/status/ownership. Point `externalReferences` or an `assets/` entry at the document and screenshot files. `design-spec.md` ([DESIGN-HANDOFF-BUNDLE-TEMPLATE.md](../templates/DESIGN-HANDOFF-BUNDLE-TEMPLATE.md) Part 2) carries the narrative in prose, referencing the screenshots inline (`![checkout screen](assets/images/checkout.png)`) rather than transcribing them into a full `screens/*.md` element table -- unless and until someone does that transcription, in which case a `screens/*.md` file can be added later without changing the bundle's identity.

**Claude Design or other AI-generated wireframes/mockups**: treated the same as any other image-based source -- referenced from `assets/images/` and `design-spec.md`, with `externalReferences` noting the tool (e.g. `tool: Claude Design`) as provenance only, exactly as section 5's example already shows.

**A fully detailed handoff**: every screen gets its own `screens/<screen-id>.md` file per the schema above, referenced from the Manifest.

In every case, the artifact is registered as a source the same way (`PRODUCT-SOURCE-MATERIAL-SPEC.md` sections 8-9), and Design Analysis can proceed once readiness allows it -- a thinner bundle simply carries more `Assumption` and `Decision Required` classifications forward, and more items in `knownLimitations`, which is exactly what the evidence rule is for.

## 6.2 The Native Claude Design Export Shape (`design` branch)

Sections 5-6.1 above describe a hand-authored bundle -- `bundle.md` frontmatter, a narrative `design-spec.md`, structured `screens/*.md` tables -- filled in by a person, scaling down for lighter sources. That format was never validated against what Claude Design's own canvas export tool actually produces, and it doesn't match it: verified directly against a real export (`pdf-workflow` repository, `workflow-manager/design/`), a real handoff is a rich prose `README.md` (problem statement, per-screen breakdown, interactions, state shape, tokens, accessibility gaps, an implementation-order recommendation -- everything section 6's `design-spec.md` tries to hand-reconstruct, already written), an optional `PARITY_RULE.md`, and self-contained `designs/*.dc.html` canvas artboards (dark + `(Light)` pairs) backed by a design-token bundle under `designs/_ds/`. There is no YAML frontmatter and no per-screen element table anywhere in it.

This section defines how that real shape is handled -- **the primary, recommended path when the source is a genuine Claude Design export**, sitting beside sections 5-6.1's hand-authored shapes rather than replacing them (those stay the right format for a bare Figma link or a written spec with screenshots, per this document's own scalable-not-all-or-nothing framing in section 1).

**Where it lives -- a separate, persistent `design` branch, not `main`.** A native export is uploaded via PR into a long-lived `design` branch, untouched:

```text
<platform-slug>/[<app-slug>/]design/v<N>/
  README.md              # byte-identical to the export -- never edited by this framework
  PARITY_RULE.md          # untouched, when present
  designs/
    *.dc.html              # untouched, including "(Light)" variants
    support.js
    _ds/<system>-<uuid>/  # untouched (styles.css, _ds_bundle.js)
  _cover-sheet.md          # the one file this framework adds -- see below
```

Two small normalizations vs. the raw tool output, both a stated default and overridable: the version folder is a plain `v<N>/` (the platform/app/`design` path segments already carry the app's identity, so a real export's own `design_handoff_<app>_v<N>/` folder name is redundant once nested here), and every version gets an explicit folder including the first (the tool itself leaves v1 unsuffixed). Versions are bare integers (`v1`, `v2`, `v3`, ...), matching Claude Design's own scheme -- **not** the `MAJOR.MINOR` format section 2 cites for the hand-authored path; `PRODUCT-SOURCE-MATERIAL-SPEC.md` section 5 already permits "another configured convention," so this is a documented divergence, not a spec change there.

This branch's folder shape is deliberately **not** governed by `ARTIFACT-STORAGE-SPEC.md`'s `<platform-slug>/[<app-slug>/]<type-root>/...` convention -- that convention governs curated *outputs* committed to `main` (Design Analysis, Requirements, the Business PR); `design` is a raw landing zone the Business Agent reads from, closer in kind to an external Figma file than to a generated artifact. `main`'s own existing `<platform-slug>/[<app-slug>/]design/<feature-slug>/v<version>/` root (section 8) keeps governing the hand-authored path and the one existing dry-run example under it.

**Scope, default/overridable:** the `design` branch is required only for tool-produced exports (Claude Design being the concrete case today). A hand-authored bundle with no export tool behind it may still be authored directly against `main`'s existing `design/` convention per section 6.1 -- there's nothing raw to protect from reformatting in that case, so the extra branch ceremony isn't earning its cost there.

**`_cover-sheet.md`** -- one small manifest per version folder (default/overridable filename; the leading underscore echoes the native `_ds/` folder's own convention, so it reads as framework-added metadata rather than part of the export). It carries only what the native files structurally can't (status/readiness/version bookkeeping), never duplicating README.md's content:

```yaml
---
platformSlug: pdf-workflow
appSlug: workflow-manager        # omitted when the platform has no app layer (ARTIFACT-STORAGE-SPEC.md section 4)
version: 4                        # integer, matches the version folder name
priorVersion: 3                   # null for v1 -- drives incremental, per-feature-slice re-analysis (see below)
sourceTool: Claude Design
uploadedBy: { name: Manali, role: Producing Designer }   # ROLE-005
uploadedAt: 2026-09-03
status: null                      # written on merge by design-branch-intake.yml: Received
readiness: null                   # written on merge: Ready / Ready with Limitations (PRODUCT-SOURCE-MATERIAL-SPEC.md section 9; Blocked/Not Applicable can't arise mechanically here)
knownLimitations: []              # scraped from README.md's "Known UX issues"/"Open Items"-style heading
screens: []                       # regenerated from designs/*.dc.html at merge time
---
```

Only five fields are human-filled before opening the PR (`platformSlug`, `appSlug`, `priorVersion`, `sourceTool`, `uploadedBy`); the rest are machine-written by `.github/workflows/design-branch-intake.yml` on merge (`.github/scripts/design_branch_gate.py`), mirroring how the hand-authored path's `bundle.md` gets its `status`/`readiness` machine-written today (section 9), just on a different branch and a thinner file. Everything else the hand-authored `bundle.md` carries (`experienceRequirements`, `businessContext`, `tags`, per-screen Evidence hints) is not a real gap for this shape -- the native `README.md` already carries that content in prose, which the Business Agent reads directly during Design Analysis.

**Readiness, mechanically assigned** (never a judgment call -- `ROLE-009`'s charter, `FRAMEWORK-CONFIGURATION-SPEC.md` section 10): the merge gate checks the version folder is structurally sound -- `README.md` present and substantial, at least one `designs/*.dc.html` file, every `.dc.html` path `README.md` references in backticks actually exists, and (when `PARITY_RULE.md` is present) every dark/`(Light)` pair is complete -- before it will merge at all. On merge, `knownLimitations` is scraped from README.md's own "Known UX issues" / "Open Items" heading (a real, recurring section in actual exports) and `readiness` follows the same rule as the hand-authored path: empty -> `Ready`; non-empty -> `Ready with Limitations`.

**Design Reviewer sign-off is a PR-description checkbox, not a GitHub PR review.** GitHub never allows a pull request's author to formally Approve their own PR -- a platform rule, not a repository setting, true on every plan. This repository has no separate agent/bot GitHub identity (see `EXECUTION-ADAPTER-SPEC.md`'s scope, which stops at the invocation contract), so the account that opens an upload PR and the account required to act as `ROLE-004` are, today, unavoidably the same. The gate therefore checks for an exact checkbox line in the PR description instead (`templates/DESIGN-HANDOFF-BUNDLE-TEMPLATE.md` Part 5a), the same pattern the hand-authored path already uses for its Pre-Registration Checklist (section 9 below) -- checked only once genuinely reviewed, verified by `design_branch_gate.py`'s `REVIEWER_SIGNOFF_RE`. This is a stated, deliberate trade-off: less tamper-resistant than a platform-verified review, but the only signal that actually works today; a separate bot identity (opening upload PRs under its own account, freeing the human account to use a real GitHub review) is the noted future fix, not yet built.

**Trigger:** merge into `design` opens one GitHub Issue (`agent:business` + `status:queued` labels) naming the platform/app/version, branch, path, merge commit SHA, and computed readiness -- a durable, visible work-queue item, not a PR comment nothing consumes (contrast section 6.1's older mechanism on `main`, kept only for the hand-authored path). See `GITHUB-PLATFORM-ADAPTER-SPEC.md` section 6.1 for the full mechanism.

**Incremental, per feature-slice -- not one registration per drop.** A version is a whole-app snapshot spanning unrelated features (a real export can bundle a dashboard, a reporting screen, and an entire unrelated auth flow in one version). `_cover-sheet.md`'s `priorVersion` field lets the Business Agent diff the new version's screen list against whatever it last actually analyzed: `sources/.../source-<feature-slug>-SRC-*.md` registration happens **per feature-slice**, not per drop -- one drop can produce several registration records, each citing the same `branch: design` / `path:` / commit SHA, each with its own readiness judgment. Feature-slices with no material change since their last **Approved** Business PR are left alone entirely -- no re-analysis, no new registration, no new PR.

**Pointer back from `main`.** Since there's no `bundleId`/version frontmatter to cite (unlike the hand-authored path's `bundle.md`), both the `sources/.../source-*.md` registration record and the Design Analysis's `Source Material` field (`DESIGN-ANALYSIS-SPEC.md` section 3, already generic) cite a three-part pointer instead:

```text
branch: design
path: pdf-workflow/workflow-manager/design/v4/
commit: <merge commit SHA>
```

A commit SHA pins an exact snapshot even after `design`'s tip moves on to a later version -- `git show <SHA>:<path>/README.md` retrieves exactly what was analyzed, satisfying `PRODUCT-SOURCE-MATERIAL-SPEC.md` section 5's retrieval-identity requirement.

### 6.2.1 Reading This Format Accurately

Reading/interpretation technique moved to its own document, [CLAUDE-DESIGN-READING-SPEC.md](CLAUDE-DESIGN-READING-SPEC.md) -- it's out of scope for this document, by this document's own section 3 ("It does not define how the Business Agent interprets a bundle"). Kept as a pointer rather than silently deleted, so a link into the old location still lands somewhere useful. Every rule that was here (dark `.dc.html` as sole source of truth, light theme excluded, README as reference only, the failed-screenshot finding) is unchanged in substance, just relocated.

## 7. Status vs. Readiness

- `status` is the bundle's own authoring lifecycle, set and moved forward by its owner: `Draft -> In Review -> Approved`, with `Superseded` or `Withdrawn` at end of life.
- Readiness (`Ready` / `Ready with Limitations` / `Blocked` / `Not Applicable`) is assigned separately, during source registration, per [PRODUCT-SOURCE-MATERIAL-SPEC.md](PRODUCT-SOURCE-MATERIAL-SPEC.md) section 9. It is not authored by the designer.
- A bundle with `status: Approved` is necessary but not sufficient for the Business Agent to treat it as ready; the intake process still determines `readiness`.

## 8. Storage Convention

The full naming and folder convention -- for this bundle and for every other artifact type in the repository -- is defined once in [ARTIFACT-STORAGE-SPEC.md](ARTIFACT-STORAGE-SPEC.md), consistent with [PRD.md](../PRD.md) section 7.7 and the `design/` area referenced in [README.md](../README.md). Summary (ARTIFACT-STORAGE-SPEC.md section 5):

```text
<platform-slug>/[<app-slug>/]design/<feature-slug>/v<version>/
  design-handoff-<feature-slug>-v<version>.md
  design-spec-<feature-slug>-v<version>.md
  screens/
    screen-<screen-id>-<feature-slug>.md
  user-flows/
    flow-<flow-id>-<feature-slug>.mmd
  assets/
    icons/
    images/
    (design-token exports in whatever format the design system produces)
```

For a lightweight reference (section 6.1), only the identity file -- and often the design spec -- may exist under this path; the rest of the layout is filled in only as detail accumulates.

## 9. Relationship to Approval Gates

A Design Handoff Bundle's own review or acceptance (recorded in `reviewedBy`) is a design-quality check performed before the bundle is registered as source material. It is separate from, and does not substitute for, the Business Owner approval gate (Business PR) or the Architect approval gate (technical decomposition) defined in [AGENT-RESPONSIBILITIES.md](AGENT-RESPONSIBILITIES.md) and [TECHNICAL-HANDOFF.md](TECHNICAL-HANDOFF.md).

## 10. Reusable Template

The concrete file templates are defined in [DESIGN-HANDOFF-BUNDLE-TEMPLATE.md](../templates/DESIGN-HANDOFF-BUNDLE-TEMPLATE.md).

## 11. Open Decisions

- Which fields, beyond the required set, should be mandatory for this repository's default profile?
- ~~Should `readiness` be written back into `bundle.md` by the intake process, or tracked only in the source registry?~~ **Resolved:** written back into `bundle.md`'s own frontmatter, as part of the combined Bundle-Acceptance-plus-readiness-assignment automation triggered by the bundle's upload PR merging -- see GITHUB-PLATFORM-ADAPTER-SPEC.md section 6.1.
- What is the minimum number and shape of elements/interactions before a screen is considered evidence-complete for Design Analysis?
- Should screen-level `Evidence` hints from designers carry any weight in the Business Agent's own classification, or remain purely informative?
- How are non-UI product/service/process initiatives (which do not use this bundle type at all, per PRODUCT-SOURCE-MATERIAL-SPEC.md section 3) expected to satisfy an equivalent structured-source contract?

## 12. Revision History

*What and when -- the current rule and its rationale live at the cited section, not here.*

| Date | Section | Change |
| --- | --- | --- |
| 2026-09-10 | 6.2 | Reading/interpretation technique moved out into its own sibling document, `CLAUDE-DESIGN-READING-SPEC.md`. |
| 2026-09-04 | 6.2 | Discovered, exercising the gate against a real PR, that GitHub never lets a PR's author formally approve their own PR -- switched Design Reviewer sign-off to a PR-description checkbox. |
| 2026-09-03 | 6.2 | Added the native Claude Design export shape (the `design` branch), after verifying the hand-authored `bundle.md`/`screens/*.md` format never actually matched what the tool produces. |
| 2026-09-01 | 11 | Resolved: `readiness` is written back into `bundle.md`'s own frontmatter, not tracked only in the source registry. |
- Section 6.1 resolves *design*-source variety (bundle vs. Figma link vs. screenshots vs. wireframes). It does not define whether the same lightweight-reference pattern should be formalized for non-design source types too, or whether the generic `PRODUCT-SOURCE-MATERIAL-TEMPLATE.md` registration record already covers that adequately.
