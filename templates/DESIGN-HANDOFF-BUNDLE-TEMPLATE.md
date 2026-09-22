# Design Handoff Bundle Templates

Reusable starting points for the structure defined in [DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md](../specs/DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md). Designers use these as starting points; the Business Agent and intake process read them directly -- no separate machine schema to validate against.

Section 6.1 of the spec shows how these scale down for a bare Figma link, a written document with screenshots, or wireframe images. Parts 1-3 below show the fully detailed case; skip whatever a lighter source doesn't need.

**Naming:** the `File:` line under each Part below uses `bundle.md` / `design-spec.md` / `screens/*.md` as shorthand. The actual filenames this repository uses are `design-handoff-<feature-slug>-v<version>.md`, `design-spec-<feature-slug>-v<version>.md`, and `screen-<screen-id>-<feature-slug>.md`, per [ARTIFACT-STORAGE-SPEC.md](../specs/ARTIFACT-STORAGE-SPEC.md) section 5.

---

## Part 1: `bundle.md` Template

**File:** `[platform-slug]/[app-slug (optional)]/design/[feature-slug]/v[version]/design-handoff-[feature-slug]-v[version].md` (shorthand: `bundle.md`)

```markdown
---
bundleId: checkout/cart-optimization@v1.0
bundleName: Cart Optimization Redesign
platformSlug: checkout                            # was productSlug before 2026-09-01
appSlug: null                                      # set only when this platform has an app layer (ARTIFACT-STORAGE-SPEC.md section 4)
featureSlug: cart-optimization
version: "1.0"
status: Draft
readiness: null
owner:
  name: YOUR NAME
  email: your.email@company.com
  role: Product Designer
reviewedBy: []
createdAt: 2026-08-31
effectiveAt: null
supersedes: null
supersededBy: null
externalReferences:
  - tool: Figma
    url: https://figma.com/design/FILE_KEY
    note: Source frames for all screens
knownLimitations: []
experienceRequirements:
  targetPlatforms: [web desktop, web mobile]
  accessibility: "WCAG 2.1 Level AA"
  rtl: false
  darkMode: true
tags: [checkout, cart, ux-improvement]
businessContext:
  objective: Reduce cart abandonment and improve item-management experience
  successMetrics: [Cart abandonment rate, Time to checkout, Add-to-cart conversion]
  priority: High
  targetRelease: Q4 2026
---

## Manifest

### Screens

| ID | Name | File | States | Depends On |
| --- | --- | --- | --- | --- |
| `cart-empty` | Empty Cart State | `screens/screen-cart-empty-cart-optimization.md` | default | -- |
| `cart-full` | Cart with Items | `screens/screen-cart-full-cart-optimization.md` | default, item-hover, editing | cart-empty |

### Flows

| ID | Name | File | Start Screen | End Screen |
| --- | --- | --- | --- | --- |
| `add-item-flow` | User Adds Item to Cart | `user-flows/flow-add-item-cart-optimization.mmd` | product-detail | cart-full |

### Assets

- Colors: `assets/colors.*`
- Typography: `assets/typography.*`
- Spacing: `assets/spacing.*`
- Icons: `assets/icons/`
- Images: `assets/images/`
```

---

## Part 2: `design-spec.md` Template

**File:** `[platform-slug]/[app-slug (optional)]/design/[feature-slug]/v[version]/design-spec-[feature-slug]-v[version].md` (shorthand: `design-spec.md`)

This is the narrative companion to `bundle.md` and `screens/*.md` -- the business-readable explanation. Per-screen element/interaction detail belongs in `screens/*.md`, not duplicated here; this file explains *why*, those files record *what*.

```markdown
# Design Specification: Cart Optimization Redesign

## Executive Summary
[2-3 sentences explaining the feature and the business outcome it is intended to produce]

---

## Feature Overview

### Problem Statement
[What pain point are we solving?]

### Solution Overview
[High-level description of the redesign, in product/business terms]

### Success Criteria
- Metric 1: [specific, measurable]
- Metric 2: [specific, measurable]

---

## Screens

| Screen | Purpose | Detail |
| --- | --- | --- |
| Empty Cart (`cart-empty`) | Displayed when the user has no items in their cart | `screens/screen-cart-empty-cart-optimization.md` |
| Cart with Items (`cart-full`) | Displays cart with one or more items | `screens/screen-cart-full-cart-optimization.md` |

*(If a screen has no `screens/*.md` file yet -- a lightweight reference, per DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md section 6.1 -- describe it here in prose instead, and reference any attached screenshot: `![cart with items](assets/images/cart-full.png)`.)*

### Business Rules
- Quantity per item stays within a stated minimum and maximum (state the actual bound as a business rule, not an implementation limit)
- Pricing shown to the user must always reflect the current cart state

---

## User Flows

### Flow 1: Add Item to Cart
- **ID**: `add-item-flow`
- **File**: `user-flows/flow-add-item-cart-optimization.mmd`
- **Start**: Product detail screen
- **End**: Cart full screen
- **Happy Path**:
  1. User views product details
  2. User adds the item to the cart
  3. User sees confirmation that the item was added
  4. Cart reflects the new item
- **Error Path**:
  1. Adding the item does not succeed
  2. User sees a message that the action did not succeed and may retry

### Flow 2: Remove Item from Cart
- **Happy Path**:
  1. User views cart with items
  2. User initiates removal of an item
  3. User confirms the removal
  4. Item is removed; totals update
- **Cancellation Path**:
  1. User initiates removal
  2. User cancels instead of confirming
  3. Nothing changes

---

## Experience Requirements

*(Business-level commitments only. Exact browser/OS support, response-time targets, and caching or retry behavior are Technical Agent decisions made later -- see DESIGN-ANALYSIS-SPEC.md section 6 -- and do not belong in this section. These should match `bundle.md`'s `experienceRequirements` exactly.)*

- **Target platforms**: web desktop, web mobile
- **Accessibility**: WCAG 2.1 Level AA
- **Dark mode**: required
- **RTL**: not required for v1.0

---

## Accessibility & Compliance

### WCAG 2.1 Level AA
- All interactive elements are keyboard accessible (tab order documented below)
- Form inputs have associated labels
- Error messages are announced to assistive technology
- Color is not the sole means of conveying information

### Tab Order
[item -> quantity -> remove -> coupon input -> apply button]

### Screen Reader Testing
- Tested with: [tools used]

---

## Design Tokens Used

### Colors
- `color-primary` -- action buttons, highlights
- `color-error` -- error messages, remove icon
- `color-success` -- success messages, confirmations

### Typography
- `heading-2` -- screen title
- `body-1` -- item descriptions, prices

### Spacing
- `spacing-sm`, `spacing-md`, `spacing-lg`

---

## Version History

### v1.0 (Current)
- [Date]: Initial design
- Includes: empty state, full cart, coupon flow

---

## Bundle Acceptance

*(This records design-level acceptance of the bundle itself -- it is separate from, and does not substitute for, Business Owner approval of the Business PR or Architect approval of the technical decomposition.)*

| Role (per active Role Configuration, section 11's GATE-002) | Name | Date | Status |
| --- | --- | --- | --- |
| Producing Designer | [Your Name] | [Date] | Draft |
| Compliance Pre-Check (`ROLE-009`) | agent | [Date] | Pass / Fail -- see findings against this checklist |
| Design Reviewer | [Reviewer Name] | -- | Pending |

---

## Appendix: Design Decisions

### Why a confirmation before removal?
[Rationale -- mistake prevention, undo capability, etc.]

### Why is pricing always shown as current cart state?
[Business rationale -- trust, accuracy -- not an implementation reason]
```

---

## Part 3: `screens/*.md` Template

**File:** `[platform-slug]/[app-slug (optional)]/design/[feature-slug]/v[version]/screens/screen-cart-full-cart-optimization.md`

```markdown
---
screenId: cart-full
screenName: Cart with Items
externalReference:
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
| `coupon-input` | input | Coupon Code | change | enables the Apply button once a code has been entered | Explicit |
| `coupon-btn` | button | Apply | click | validates the coupon; on success shows a confirmation and applies the discount, on failure shows an inline error and keeps the input focused | Explicit |

## State: editing

**Description:** User is changing an item's quantity.
**Evidence:** Strongly Implied
**Diff from `default`:** the item row's quantity control is visually highlighted as active.

<!-- Duplicate the "## State: <name>" block for each additional state. -->
```

---

## Part 4: Pre-Registration Checklist for Designers

```markdown
# Pre-Registration Checklist

## Content Completeness
- [ ] bundle.md frontmatter has all required fields (DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md section 5)
- [ ] design-spec.md covers every section, and every screen in bundle.md's Manifest is at least named there
- [ ] Every screen in the Manifest that has structured detail has a corresponding screens/*.md file (a lightweight reference, section 6.1, may have none yet -- that's fine, say so in knownLimitations)
- [ ] Every state named in a screens/*.md file is complete (Description, Evidence, and either Elements & Interactions or a Diff)
- [ ] Every flow referenced has a corresponding user-flows/*.mmd file
- [ ] All assets referenced exist under assets/

## Cross-References
- [ ] Manifest's screen and flow File columns match the actual files
- [ ] All Start Screen/End Screen and interaction outcomes referencing navigation use real screen IDs
- [ ] All element IDs are unique within their screen

## Design vs. Implementation Boundary
- [ ] No interaction outcome includes an HTTP method, endpoint, or payload
- [ ] No section states a specific browser or OS version requirement
- [ ] No section states a numeric performance target that the business did not state
- [ ] experienceRequirements contains only business-level platform/accessibility commitments

## Accessibility
- [ ] Interactive elements are described as keyboard accessible
- [ ] Tab order is documented in design-spec.md
- [ ] Accessibility level is stated in bundle.md's experienceRequirements

## Bundle Acceptance
- [ ] Owner is identified in bundle.md
- [ ] Any design-level reviewedBy entries carry a role and timestamp
- [ ] knownLimitations lists anything incomplete, excluded, unclear, or -- for a lightweight reference -- not yet broken down at all
- [ ] **Design Reviewer sign-off (ROLE-004):** I have reviewed this bundle and accept it. *(This exact checked line, pasted into the PR description, is what bundle_gate.py's merge gate checks; not a GitHub PR review, since GitHub never lets a PR's author formally approve their own PR. Check only once genuinely reviewed. See GITHUB-PLATFORM-ADAPTER-SPEC.md section 8.)*

## Ready to Register?
Once the checks above pass:
1. Set `status` to `Approved` in bundle.md (bundle's own lifecycle -- see DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md section 7)
2. Register the bundle as source material per PRODUCT-SOURCE-MATERIAL-SPEC.md sections 8-9; the intake process assigns `readiness`
3. Once `readiness` is `Ready` or `Ready with Limitations`, the bundle is available for Design Analysis
4. Tag the commit: `[platform-slug]/[app-slug (optional)]/design/[feature-slug]/v[version]`
```

---

## Part 5: `_cover-sheet.md` Template (native Claude Design export, `design` branch)

**File:** `<platform-slug>/[<app-slug> (optional)]/design/v<N>/_cover-sheet.md`

Only for a genuine Claude Design export uploaded to the persistent `design` branch, per [DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md](../specs/DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md) section 6.2 -- **not** used for Parts 1-4's hand-authored path against `main`. Sits alongside the untouched native files (`README.md`, optionally `PARITY_RULE.md`, `designs/*.dc.html`, `designs/_ds/`); never edit those.

Only the first five fields below are filled in before opening the PR. `status`, `readiness`, `knownLimitations`, and `screens` are left `null`/empty and are written by `.github/workflows/design-branch-intake.yml` on merge -- do not fill them in by hand.

```markdown
---
platformSlug: pdf-workflow
appSlug: workflow-manager        # omit entirely when this platform has no app layer (ARTIFACT-STORAGE-SPEC.md section 4)
version: 4                        # integer, matches the v<N>/ folder name -- not MAJOR.MINOR (section 6.2)
priorVersion: 3                   # the last version you're aware was analyzed; null for v1
sourceTool: Claude Design
uploadedBy:
  name: YOUR NAME
  role: Producing Designer        # Role per the active Role Configuration (FRAMEWORK-CONFIGURATION-SPEC.md section 10)
uploadedAt: 2026-09-03
status: null                      # written on merge
readiness: null                   # written on merge
knownLimitations: []              # written on merge, scraped from README.md
screens: []                       # written on merge, from designs/*.dc.html
---
```

Before opening the PR into `design`, confirm (the merge gate checks these mechanically, but catching it yourself first avoids a round trip):
- `README.md` is present and has real content, with at least one `##` heading.
- At least one `designs/*.dc.html` file is present.
- Every `.dc.html` file named in backticks in `README.md` actually exists under `designs/`.
- If `PARITY_RULE.md` is present, every `(Light).dc.html` file has a same-named non-Light counterpart, and vice versa.

## Part 5a: PR Description Sign-off (native path only)

Paste this exact line into the description of every PR opened against the `design` branch, unchecked at first:

```markdown
- [ ] **Design Reviewer sign-off (ROLE-004):** I have reviewed this drop and accept it.
```

Check the box only once you have actually reviewed the drop, then merge. This replaces a GitHub PR review as the approval signal for this one gate -- GitHub never allows a PR's author to formally Approve their own PR, and this repository has no separate agent/bot GitHub identity, so the account opening an upload PR and the required Design Reviewer are, today, the same account. `design_branch_gate.py check` looks for this exact line (see `REVIEWER_SIGNOFF_RE`) -- a paraphrase won't match, and approving *after* merge does not retroactively satisfy it, since the gate only runs at PR-update and merge time. See DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md section 6.2.

## Summary

| File (shorthand) | Actual filename pattern | Purpose |
| --- | --- | --- |
| `bundle.md` | `design-handoff-<feature-slug>-v<version>.md` | Identity, manifest, status, and readiness for the bundle as a whole (hand-authored path, `main`) |
| `design-spec.md` | `design-spec-<feature-slug>-v<version>.md` | Business-readable narrative: problem, solution, cross-cutting requirements, tokens, acceptance (hand-authored path, `main`) |
| `screens/*.md` | `screens/screen-<screen-id>-<feature-slug>.md` | Structured screen/state/element/interaction/evidence records (hand-authored path, `main`) |
| `user-flows/*.mmd` | `user-flows/flow-<flow-id>-<feature-slug>.mmd` | Traversable user journeys (hand-authored path, `main`) |
| `assets/` | (tool-native, unchanged) | Design tokens and content assets, tool-native formats (hand-authored path, `main`) |
| `_cover-sheet.md` | unchanged (leading underscore is the actual name) | Status/readiness/version bookkeeping for a native export (native path, `design` branch, section 6.2) |

See [ARTIFACT-STORAGE-SPEC.md](../specs/ARTIFACT-STORAGE-SPEC.md) section 5 for the hand-authored path's naming convention, and section 10 for the `design` branch's independent shape.

Designers use the templates in Parts 1-3 as starting points for the hand-authored path, filling in only as much as the source material actually supports -- see [DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md](../specs/DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md) section 6.1. For a genuine Claude Design export, use Part 5 instead and leave the native files untouched.
