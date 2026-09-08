---
screenId: cart-full
screenName: Cart with Items
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
