---
bundleId: checkout/cart-optimization@v1.0
bundleName: Cart Optimization Redesign
platformSlug: checkout                            # was productSlug before 2026-09-01; this platform has no app-level subdivision
featureSlug: cart-optimization
version: "1.0"
status: Approved
readiness: null                                   # See checkout/sources/cart-optimization/source-cart-optimization-SRC-001.md for the actual registered readiness outcome (Ready with Limitations) -- DESIGN-HANDOFF-BUNDLE-SPEC.md section 11 leaves whether this should be written back here as an open decision; the source registry is authoritative for now.
owner:
  name: Manali
  role: Product Designer
reviewedBy: []
createdAt: 2026-08-31
effectiveAt: null
supersedes: null
supersededBy: null
externalReferences: []
knownLimitations:
  - "No mobile-specific frames were provided; only the desktop layout is represented in this bundle."
  - "Maximum cart size and coupon-code format are not shown anywhere in the source frames."
experienceRequirements:
  targetPlatforms: [web desktop]
  accessibility: "WCAG 2.1 Level AA"
  rtl: false
  darkMode: false
tags: [checkout, cart, ux-improvement]
businessContext:
  objective: Reduce cart abandonment and improve item-management experience
  successMetrics: [Cart abandonment rate, Time to checkout]
  priority: High
  targetRelease: Q4 2026
---

## Manifest

### Screens

| ID | Name | File | States | Depends On |
| --- | --- | --- | --- | --- |
| `cart-empty` | Empty Cart State | `screens/screen-cart-empty-cart-optimization.md` | default | -- |
| `cart-full` | Cart with Items | `screens/screen-cart-full-cart-optimization.md` | default, editing | cart-empty |

### Flows

| ID | Name | File | Start Screen | End Screen |
| --- | --- | --- | --- | --- |
| `add-item-flow` | User Adds Item to Cart | `user-flows/flow-add-item-cart-optimization.mmd` | product-detail | cart-full |

### Assets

None referenced in this dry-run bundle.
