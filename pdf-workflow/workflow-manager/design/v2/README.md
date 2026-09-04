# Handoff: Workflow Manager UI (Dashboard + Mapping Report)

## Overview
Two screens for the Formwork workflow manager: the **Workflows dashboard** (landing/create + workflow list) and the **Mapping Report** (PDF-extraction-to-field mapping review, with a collapsible Page → Section → Field accordion).

## About the design files
The files in `designs/` are **HTML design references** (built as standalone prototypes), not production code. They show the intended layout, spacing, colors, typography, and interaction states. The task is to **recreate these designs inside the existing Angular app** at `workflow-manager/` — not to copy/paste the HTML.

I looked at your repo (`pdf-workflow/workflow-manager`) and found matching real components already scaffolded:
- `src/app/features/dashboard/dashboard.component.ts`
- `src/app/features/mapping-report/mapping-report.component.ts`

**Important mismatch to resolve first:** the existing Angular components are built with **Angular Material + Tailwind, light theme** (`bg-gray-50`, `mat-raised-button`, etc.). These new designs are in **Nocturne**, a dense dark UI system (near-black `#161826` ground, Inter type, single purple accent `#9184d9`, outlined buttons, OKLCH tonal ramps). Decide up front whether:
1. Nocturne becomes the new global theme (swap Material's theme tokens / Tailwind config to Nocturne's palette, or drop Material for the plain CSS component classes Nocturne ships), or
2. These are just references for a future restyle and current Material components stay as-is for now.
Recreate using whichever your codebase should standardize on — don't hand-copy the HTML/CSS wholesale into Material's DOM structure.

## Fidelity
**High-fidelity.** Treat colors, spacing, type sizes, and component states in the HTML as final; implement pixel-close using Angular Material components (or plain elements) styled to match.

## Screens

### 1. Dashboard (`designs/Workflow Dashboard.dc.html`)
- **Header**: org mark (initial-in-square) + org name, left; user menu (avatar+name, dropdown: Account settings / Log out) and a gear icon (Org settings / Members / Billing dropdown), right.
- **Create section**: "Describe in text" full-width chat-style input tile up top; below it a 2-column grid of "Upload PDF" (inline drag-drop dropzone, file chip once selected) and "Manually create" (icon + description, no action needed inline).
- **Workflow list**: search input (50% width) + status segmented filter (`All/Ready/Processing/Error`) + sort menu, result count; below, a responsive card grid (`repeat(auto-fill, minmax(230px,1fr))`), each card: icon, title, status tag, updated time, Open + Preview buttons.
- **Footer**: copyright + Documentation/Support/Status links.
- Header block spacing: `h1` margin-bottom = 1 step, description margin-bottom = 1.5 steps (Nocturne `--space-1` / `--space-6`) before the next content block — no extra padding stacking.

### 2. Mapping Report (`designs/Mapping Report.dc.html`)
- **Header**: same org header as dashboard (shared component — build once, reuse).
- **Page intro**: workflow title (`h1`, 22px) + one-line description.
- **Stat tiles**: 5 equal-width tiles (Total / High ≥80% / Medium 50–79% / Low <50% / Avg confidence), each with a 2px top border colored by its confidence band and value/label stacked inside.
- **Filters, two rows**: row 1 is the search input (50% width) + a "Created from" segmented control (PDF/LLM/Manual — see scope note below); row 2 is "Confidence" (All/High/Medium/Low, chip labels tinted by band) + "View" (Table/Cards). All four controls share one filter/view state regardless of row.
- **View toggle**: the "View" segmented control (Table / Cards) is two renderings of the exact same filtered/grouped data and shares all state (search, confidence filter, source filter, in-progress edit) — switching views never resets anything. Light and dark themes both implement this toggle identically.
- **Field data model — kind + targetType** (replaces an earlier label/heading-only model; implement this schema, not a flat field list):
  - Each extracted PDF element has a **`kind`**: `heading` | `description` | `field` | `field-group` | `custom` — this is *what the PDF element is*.
  - Each maps to a workflow-side target whose **`targetType`** is the discriminant: `Section` | `Content` (static text/title, collects no data) | `Field` (single input) | `FieldGroup` (repeating set, e.g. multiple emergency contacts) | `Custom` (an app-specific component, e.g. a signature pad).
  - `kind` determines which `targetType` a row can be reassigned to (a `field` can only remap to another `Field`; a `field-group` only to another `FieldGroup`, etc.) — don't allow cross-kind remapping.
  - The "Target Type" column/tag shown to the user is a **compound label**: `{displayType}-{detail}`, e.g. `Field-Text`, `Field-Date`, `Field-List-3x` (the field-group's item count), `Custom-App-signature-pad`. Description-kind rows show just `Text` (no detail suffix).
- **Mapping table/cards — collapsible 3-level accordion** (this is the core interaction, and differs from the current flat Material table):
  - **Page** (top level) — chevron + "Page N" + "{sections} · {fields}" summary. Click toggles all its sections.
  - **Section** (nested) — chevron + `Section` tag + section label + field count + (if the section heading itself was mapped) a confidence %. Click toggles its fields. A page can contain **multiple sections** — don't assume one section per page.
  - **Field row** (leaf): PDF text | source `kind` tag | Target Type tag (see above) | Maps-to label | confidence % | source icon (llm/manual) | edit (pencil/chevron) + unlink (×) icon buttons. Table view puts these in real `<table>` columns; Card view puts the same fields in a card with a "FROM PDF [kind] MAPS TO [target type]" header line.
  - **Card view is fully built out** (not a separate exploration — it's the second state of the same `View` toggle described above), with the same collapsible-card-per-field structure, kind-specific edit controls, and unlink/discard confirmation dialogs as Table view.
  - **No inline `<select>` remapping.** The old "pick a different target from a dropdown" pattern was removed. Instead, clicking the pencil **expands the row in place** (a full-width `colspan` row in Table view; an inset panel inside the card in Card view) showing kind-specific edit controls:
    - `heading`/`description` (text kinds): a single **Text** textarea (edits the content verbatim).
    - `field`: **Label** text input + **Field type** select (text/number/date/email/select/checkbox/textarea).
    - `field-group`: **Label** input, an editable **Fields per item** list (each sub-field has its own label input + type select + remove button, plus "+ Add field"), and **Min items**/**Max items** number inputs.
    - `custom` (and any kind without a more specific editor): **Label** input only.
    - Every edit panel ends with **Cancel**/**Save** buttons. Only one field can be expanded at a time (expanding a new one collapses whichever was open).
  - Search and the confidence filter apply at the field level; a Section only shows if it has a matching field or its own heading matches; a Page only shows if it has a visible section.
  - No pagination — everything is reachable via the accordion; there is no "expand/collapse all" control (each row toggles itself).
- **Footer**: same as dashboard.

## Scope note: this report is PDF-conversion-specific
The reference now includes a demo **"Created from" toggle** with three options — **PDF / LLM / Manual** — showing how the report adapts: switching it relabels the source column/header (e.g. "From PDF" → "From LLM" → "From manual entry") everywhere via one `sourceLabel` value, without branching any other logic. This is illustrative, not a real data-wiring — in the real build, drive it from the workflow's actual creation method instead of a manual toggle.
Workflows can be created three ways (per the Dashboard's "Describe in text" / "Upload PDF" / "Manually create" options), but this Mapping Report only applies to the **PDF path** — confidence and source (llm/manual) are meaningless without an extraction step to review.
- **Manually-created workflows**: no report needed. The user authored the fields directly; the workflow/form editor already shows that structure, so a mapping report would just be a redundant read-only mirror of it. Don't build one. The "Manual" option on the Created-from toggle is there for the demo/reference only.
- **LLM-based workflows** (description text is parsed into structure): there's a real argument for a lightweight equivalent later (same class of risk as PDF extraction — the LLM can misread intent), but it's lower-stakes and out of scope for this handoff. If/when it's built, reuse this same component: swap the "From PDF" column for "From LLM" (the relevant excerpt, or "Generated from description" if untraceable), keep confidence as the LLM's self-reported certainty, and default source to `llm`. Don't build a separate report component for it.

## Known UX issues — resolved in the current reference
The unlink-confirmation and save-feedback gaps flagged in earlier review passes are now implemented in both themes: unlinking opens a confirm dialog (names the sub-field cost for FieldGroups), Save shows a toast, and navigating away from a dirty edit (row switch or `beforeunload`) prompts a discard-confirmation dialog. Remaining open items:
1. **No persistent context while editing.** Once a field row is expanded for edit, especially on a long page, there's no breadcrumb reminding the user which field/section they're editing if they scroll.
4. **Compound type tags (`Field-List-3x`, `Custom-App-signature-pad`) need onboarding.** They're compact but non-obvious on first encounter — consider a tooltip or one-time legend, especially for FieldGroup/Custom.
5. **Low-confidence rows don't visually escalate.** A <50%-confidence row (the ones most needing human review) has the same visual weight as a 96% row apart from a muted color — consider a stronger cue or default-sorting low-confidence to the top.
6. **Table/Card view markup duplication.** In the HTML reference the two views' edit panels are hand-duplicated (same fields, two places) — in the real implementation, extract this once (e.g. a shared row/card-edit component) so future edits to the edit panel don't need to land twice.

### 3. Workflow Settings Dialog (`designs/Workflow Settings Dialog.dc.html`)
- Modal (`.dialog-backdrop` + `.dialog`) opened from a workflow's settings entry point (e.g. `workflow-editor`'s `workflow-settings-dialog.component.ts`).
- Houses the per-workflow theme override fields (accent color, logo) described below under "Per-workflow theme override" — this is the dialog referenced there.
- Light variant: `designs/Workflow Settings Dialog (Light).dc.html`.

## Interactions & behavior
- Header user/settings menus: click toggles, an invisible fixed-position backdrop closes on outside click.
- Search: live filter, no submit button, resets no other filter state.
- Confidence segmented control: single-select, restyles the checked chip with an accent outline (`box-shadow: inset 0 0 0 1px accent`) and accent text.
- Row edit (mapping table): clicking the pencil turns the "Mapped to" cell into a `<select>` of all fields/sections (grouped, "— Unlink —" as first option) with save (check) / cancel (x) icon buttons; clicking unlink removes the mapping row entirely (optimistic, no confirm dialog in the reference — add one if your product needs it).
- Collapse/expand state should persist for the session (component state), not need to be recomputed on filter change — only visibility of already-expanded content changes.

## State management
- `mappings: MappingEntry[]` (already exists per `ApiService`/`MappingEntry`) — group client-side into Page → Section → Field for render; don't refetch per level.
- `searchTerm: string`, `confidenceFilter: 'all'|'high'|'medium'|'low'`.
- `collapsedPageIds: Set<number>`, `collapsedSectionIds: Set<string>` — default empty (all expanded).
- `editingMappingId: string | null`, `editTargetId: string` for the inline remap row.
- Section→Field ownership: derive from your workflow schema's field/section order (in the reference, each field is owned by the nearest preceding Section in the target list) — confirm this matches how sections/fields are actually modeled in `WorkflowStore` before implementing.

## Theming architecture — define once, inherit everywhere

The light/dark exploration (`designs/Workflow Dashboard (Light).dc.html`, `designs/Mapping Report (Light).dc.html`) validated a pattern worth carrying into the Angular app as-is, instead of letting each component hardcode its own colors:

1. **One token layer, set at the root, never duplicated per component.** Define every color as a CSS custom property (`--wfl-bg`, `--wfl-surface`, `--wfl-surface-alt`, `--wfl-border`, `--wfl-text`, `--wfl-text-muted`, `--wfl-accent`, `--wfl-accent-bg`, `--wfl-tag-bg`, `--wfl-input-bg`, plus the confidence-band colors) on a single root scope — in Angular that's `:root` in `styles.scss` (or a `[data-theme]` attribute on `<html>`/`<body>`), not on individual components. A component's SCSS never redeclares a hex value — it only ever consumes `var(--wfl-*)`.
2. **Component styles reference tokens, never hex.** Shared building blocks (button, card, tag, field/input, segmented control, menu, switch) get ONE class definition each (in a shared stylesheet or Angular Material theme overrides), written once against `var(--wfl-*)`. Every feature component (dashboard, mapping report, and anything built after) reuses those classes — it does not write its own `.btn`/`.card` rules. This is why swapping `data-theme="dark"` on the root instantly reflows the whole app: the cascade does the work, no component-level JS or per-component style maps.
3. **Theme switching is a single state flip, not a per-component prop.** Toggling light/dark should set one value (e.g. an Angular signal/service `ThemeService.theme`) that writes `data-theme` on `<html>` and/or swaps which token block is active; no component should take a `theme` input and branch its own styles — if a component needs to react to theme, it does so only by living inside the themed root and using tokens, never by importing color logic itself.
4. **New components inherit for free.** Because tokens live above the component tree, any new screen/component added later automatically matches the current theme the moment it uses the shared classes/tokens — nothing to "wire up" per component. Enforce this in review: a new component's SCSS should contain zero hex codes.
5. **Where this lived in the HTML reference:** the DC prototypes set all `--wfl-*` values as inline custom properties on one outer wrapper div (simulating `:root`) and defined `.btn`, `.card`, `.tag`, `.field`, `.input`, `.seg`, etc. once in a shared `<style>` block — mirror that split exactly as (a) `:root` token file and (b) one shared component stylesheet in Angular, rather than Tailwind utility classes or inline styles repeated per component.

## Design tokens (Nocturne, if adopted)
- Ground: `#161826`. Text: `#e9e9ed`. Accent: `#9184d9` (mono-accent, one hue only).
- Tonal ramps 100–900 per role (neutral/accent), OKLCH-generated — dark steps (700–900) for fills/hovers/borders on this dark ground, 500 = base, 100–300 for text on tints.
- Font: Inter, both heading and body, weight capped at 500 (no bold headings).
- Radius: 8px (`--radius-md`). Spacing scale: density 0.7× (compact).
- Buttons: outlined only, never solid-filled, even for primary actions.
- Full token/CSS: `_ds/nocturne-8201375c-.../styles.css` in this project — copy or port the `:root` variable block into your Angular theme (SCSS vars, CSS custom properties, or Tailwind config extension).

## Assets
No images/photos used on either screen — all icons are inline Phosphor-style SVGs (stroke, 1.5–2px width, `currentColor`). Recreate as an Angular icon set or keep inline SVG.

## Responsive behavior
The HTML references were authored at desktop width; neither the design conversation nor the components define mobile/tablet breakpoints. Apply your app's existing breakpoint scale (or Angular CDK's `BreakpointObserver` if none exists) with this intent, not literal pixel copying:
- **Dashboard**: the 2-column "Manually create" / tile grid (`grid-template-columns: 1fr 1fr`) and the workflow card grid (`repeat(auto-fill, minmax(230px,1fr))`) should collapse to a single column below ~640px; the auto-fill grid already reflows fluidly down to phone width, just confirm the 230px minmax isn't wider than the smallest supported viewport.
- **Mapping Report table**: the accordion's field table has 6 columns (PDF text, Type, Mapped to, Confidence, Source, actions) that will not fit a phone screen — decide with the user whether to horizontally scroll the table (simplest, matches the desktop reference) or collapse each row into a stacked card below a breakpoint (better mobile UX, more work). Don't silently pick one.
- **Header/nav**: user menu, settings gear, and (light theme) the dark-mode switch should remain reachable at all widths — collapse the org name to just the icon, and/or move settings behind a single overflow menu, below ~480px.
- **Search + filter rows**: the `width:50%` search field and inline segmented control should stack to full-width, one per row, below ~640px rather than compressing.
- Test both the light and dark token sets at each breakpoint — don't assume a breakpoint fix validated in one theme holds in the other.

## Accessibility
The HTML references are visual/interaction prototypes only — they are missing several things a production build must add:
- **Color contrast**: re-check text-on-tint pairs after picking final tokens, especially muted text (`--wfl-text-muted` / `--color-neutral-400`) on `--wfl-surface-alt` and confidence-band colors (medium/amber, low/red) against both the light and dark surface — WCAG AA (4.5:1 body text, 3:1 large text/icons) at both ends of the toggle, not just the default theme.
- **Keyboard support**: every custom dropdown (user menu, settings menu, sort menu, row action menus) in the reference opens/closes via `onClick` div overlays only — in the real build these need `role="menu"`/`role="menuitem"`, arrow-key navigation, `Escape` to close, and focus return to the trigger button on close. The reference's "click outside to close" pattern (a fixed full-screen div) is not a substitute for real focus trapping.
- **Focus visibility**: define a visible `:focus-visible` ring using the accent token on every interactive element (buttons, inputs, segmented options, the theme switch, accordion toggles) — do not rely on browser defaults, and do not remove outlines without replacing them.
- **Labels & semantics**: the segmented "Confidence"/"Status" controls are radio groups — keep `role="radiogroup"` + `aria-labelledby` (already in the reference) and ensure each `<input type="radio">` has an accessible name via its wrapping `<label>` (already true) when you port to Angular Material or custom components. Icon-only buttons (edit, unlink, more-actions, remove-file, settings gear, theme switch) need `aria-label`s — the reference has most of these; audit for any missed when re-implementing.
- **Accordion semantics** (Mapping Report): Page/Section toggle rows should be real buttons with `aria-expanded` reflecting state and (ideally) `aria-controls` pointing at the region they reveal, so screen reader users get expand/collapse state — the reference tracks this in component state but doesn't expose `aria-expanded` in markup; add it in the real build.
- **Live regions**: the toast notifications (dashboard) and inline validation (PDF-not-a-PDF error) should be announced via `aria-live="polite"` regions, not just visually appended text.
- **Dark-mode toggle**: expose it as a real switch with `role="switch"` and `aria-checked`, not a bare clickable `<span>` (the reference uses a styled span for visual speed — swap for a semantic control, e.g. Material's slide toggle, when implementing).
- **Reduced motion**: respect `prefers-reduced-motion` for the spinner animation and any menu/accordion transitions you add.

## Converting these designs to Angular — best practices

### Component architecture
- **Standalone components** (already the pattern in this codebase — see the `standalone: true` components under `features/`). One component per screen (`DashboardComponent`, `MappingReportComponent`), with true repeating units broken out as children only once they have real state/inputs of their own (e.g. a `WorkflowCardComponent`, a `MappingRowComponent`, an `AccordionSectionComponent`) — don't extract a component for something that appears once.
- **Smart/presentational split**: keep data fetching, filtering, and mutation in the route-level component (backed by `WorkflowStore`/`ApiService`), and pass filtered view-models down via `@Input()` to presentational children. Presentational components should have no store/service injections.
- **Signals over manual subscriptions**: model list/filter/theme state as `signal()`/`computed()` (Angular 16+) rather than manually-managed observables with `subscribe()` — mirrors the reference's `renderVals()` derivation-per-render pattern (search+filter+sort recomputed from source state) cleanly, and avoids memory-leak-prone manual subscriptions.
- **The Page → Section → Field accordion** is real nested state, not just a template `@for` — model it as computed signals (`pageGroups = computed(() => …)`) exactly like `renderVals()` does, so expand/collapse only recomputes visibility, not the underlying grouping.

### Styling
- Angular **component-scoped styles (ViewEncapsulation.Emulated, the default)** are the natural home for the shared token-consuming classes (`.btn`, `.card`, `.tag`, etc.) IF you centralize them in one shared stylesheet imported by every component (`styleUrls: ['./shared/ui-kit.css', ...]` or a global `styles.css` include) rather than redeclaring them per component — Angular's view encapsulation does not stop a shared, globally-loaded stylesheet from cascading normally, so the "one token layer, inherited everywhere" architecture (previous section) still works.
- Prefer **CSS custom properties over SCSS variables** for the theme tokens specifically, since SCSS variables are compile-time-only and can't flip at runtime — you need the light/dark toggle to change actual CSS custom property values on `:root`/`[data-theme]` at runtime, which SCSS `$variables` cannot do (SCSS is fine for spacing/breakpoint constants that never change per-theme).
- If keeping Angular Material: use Material's own theming API (`mat.theme()`/M3 tokens in Angular 17+, or `mat-core`+custom theme in older Material) and map your `--wfl-*` tokens onto Material's palette variables so Material components (buttons, menus, table) pick up the same theme automatically — don't hand-style Material components with overrides that fight its ViewEncapsulation (`::ng-deep` is deprecated and brittle; use Material's documented theming mixins instead).

### Interaction & state parity with the reference
- Dropdown menus (user, settings, sort, row actions): implement with **Angular CDK Overlay + `cdkMenu`** (or Material's `MatMenu`) instead of the reference's manual fixed-backdrop-div pattern — CDK menu gives you focus trapping, keyboard nav, and `aria-expanded`/`role="menu"` for free, which the HTML reference deliberately skipped for prototyping speed.
- Drag-and-drop PDF upload: use the native `dragover`/`drop` handlers as in the reference (no CDK needed for this simple case), but route the actual upload through your existing API service/interceptor pipeline, not inline `setTimeout` fakes.
- Theme persistence: store the light/dark choice in the same place other user prefs live in this app (likely a user-settings endpoint or `localStorage` via an Angular service), applied on app bootstrap before first paint to avoid a flash of the wrong theme.

### Testing
- Unit-test the derived signals/computed values (filtered list, grouped accordion tree, confidence stats) in isolation from the DOM — this is exactly the logic that lived in `renderVals()` in the reference and is the highest-value thing to cover.
- Add the accordion expand/collapse and menu-open/close interactions to the existing Playwright e2e suite (`e2e/`) alongside whatever flows it already covers, since these are the most stateful new UI pieces.

### Per-workflow theme override (confirmed requirement)
`workflow-manager`'s workflow editor should expose a theme/branding control (accent color, logo, maybe surface tone) as part of a workflow's settings — stored with the workflow record, not just a user/app-level preference. `workflow-client` then resolves its active theme as: **per-workflow override (if set) → org default → system light/dark**. Concretely:
- Add a `theme` field (e.g. `{ accent?: string, logoUrl?: string }`) to the workflow schema/`WorkflowStore`, editable from `workflow-editor`'s settings dialog (`workflow-settings-dialog.component.ts` already exists as the natural home for this control).
- `workflow-client` reads the workflow's `theme` at render time and sets the `--wfl-accent` (etc.) custom properties on its root for that submission session — everything below it (buttons, links, focus rings) inherits automatically since it's already token-driven, no per-component changes needed.
- Keep the accent as the only override surface initially (matches Nocturne's own "accent as the one brand knob" philosophy) rather than exposing every token — full palette editing is a bigger, separate feature if ever needed.
- `workflow-manager` and `platform-admin` are unaffected by a workflow's custom theme — that override only applies inside `workflow-client`'s rendering of that specific workflow.



### Dashboard
```
Page shell:     display:flex; flex-direction:column; min-height:100vh
Nav:            flex row, [brand] ... margin-left:auto ... [user menu][settings]
Create section: flex column, gap 16px
  "Describe in text" tile:        full width, single card
  Upload/Manually create row:     display:grid; grid-template-columns: 1fr 1fr; gap:16px
                                   → @media (max-width: 640px): grid-template-columns: 1fr
Workflow list header: flex row, [h1 + count] ... wraps at narrow widths
Filter row:     display:flex; align-items:flex-start; gap:16px; flex-wrap:wrap
                  search field: width:50%  → @media (max-width:640px): width:100%
                  status seg:   auto width, wraps below search on overflow
                  sort button:  margin-left:auto (desktop) → static, full-width (mobile)
Workflow grid:  display:grid; grid-template-columns: repeat(auto-fill, minmax(230px,1fr)); gap:12px
                  (already fluid — reflows to 1 column under ~260px viewport content width;
                   no breakpoint override needed, just confirm minmax floor vs. smallest target device)
Footer:         flex row, space-between, wraps to stacked centered on narrow widths
```

### Mapping Report
```
Page shell:     display:flex; flex-direction:column; min-height:100vh
Nav:            same structure as Dashboard's (shared header component)
Stat tiles:     display:flex; gap:12px; flex-wrap:wrap — 5 tiles, flex:1 each
                  → @media (max-width: 900px): wrap to 2 tiles/row (flex-basis: calc(50% - gap))
                  → @media (max-width: 480px): 1 tile/row (flex-basis: 100%)
Filter row:     display:flex; align-items:flex-start; gap:16px; flex-wrap:wrap
                  search: width:50% → 100% under 640px (same rule as Dashboard)
                  confidence seg: auto width
Accordion:      single column, no grid — each Page/Section is a full-width block;
                  the nested field table is the one piece needing a mobile decision (see
                  Responsive section above: horizontal scroll vs. stacked-card rows)
Table columns (desktop):
  PDF text (flex/auto, min ~280px) | Type (auto) | Mapped to (auto, ~220px) |
  Confidence (fixed ~100px) | Source (auto, ~70px) | Actions (fixed ~64px)
  → below ~900px: wrap table in horizontal scroll container (simplest) rather than
    resizing columns, to avoid truncating "PDF text" / "Mapped to" content
Footer:         same as Dashboard's
```

### Shared breakpoint scale to standardize on
Use whatever scale the codebase's existing components already reference (check `workflow-editor`/`submissions-list` for precedent); if none exists yet, adopt:
```
sm:  480px   (single-column forms, stacked footer)
md:  640px   (search/filter rows go full-width, 2-col grids → 1-col)
lg:  900px   (stat tiles wrap, table scroll kicks in)
xl:  1280px+ (desktop reference layout, as designed)
```

## UI architecture — structuring the codebase for this and future screens

### Layering (bottom to top, each layer only depends on the one below it)
```
1. Tokens        --wfl-* CSS custom properties (:root / [data-theme]) — colors only here.
2. Primitives    Shared classes/components with zero business logic: button, card, tag,
                 field/input, segmented control, menu, switch, accordion row. Each consumes
                 tokens, never a hex. Lives in a `shared/ui/` (or `libs/ui-kit`, given this
                 is an Nx-style monorepo — see `libs/` at the repo root) module, exported once.
3. Patterns      Composed, still generic: a filter bar (search+segmented+sort), a stat-tile
                 row, a dropdown-menu-with-backdrop, a collapsible tree row. These combine
                 primitives but still don't know about "workflows" or "mappings".
4. Features      `dashboard/`, `mapping-report/`, etc. — the only layer allowed to import
                 `ApiService`/`WorkflowStore` and know what a "workflow" or "mapping" is.
```
Never let layer 2 or 3 import from layer 4. If a "primitive" starts needing workflow-specific data, it's actually a feature-layer component and should move down... i.e. up into `features/`.

### Where this lives in the actual repo
Given `libs/` already exists at the monorepo root: put layers 1–3 there as a shared, independently-versioned library (e.g. `libs/ui-kit`) that both `workflow-manager` and `platform-admin` can import — don't let UI-kit code live inside `workflow-manager/src/app/shared` if `platform-admin` will ever need the same look. If the two apps are meant to diverge visually, keep them separate and say so explicitly rather than copy-pasting and letting them drift silently.

### Governance rules for "inherited everywhere" to actually hold
- **A new component may not declare a color, font-size, spacing value, radius, or shadow that isn't a token reference.** Enforce with a lint rule (stylelint `declaration-property-value-disallowed-list` on hex/rgb patterns) rather than code-review vigilance alone.
- **One canonical implementation per primitive.** If two features both need a dropdown menu, that's a signal to promote the existing one to `ui-kit`, not to write a second one — audit for this now, since the reference's user-menu/settings-menu/sort-menu/row-menu are all the same pattern already (worth consolidating into one `DropdownMenuComponent` before or during this build, not after).
- **Theme is a cross-cutting concern owned by one service**, not by each feature checking `isDark` — components never branch on theme; they only ever consume the current token values via the cascade.
- **Document the primitive set** (a lightweight internal Storybook-style catalog, even just one showcase route) so the next engineer reaches for the existing `.btn`/`.card`/accordion-row instead of rebuilding it inline inside a new feature — this is what actually prevents the "styles nested deep in component level" problem long-term, more than any one architectural rule.

## Files
- `designs/Workflow Dashboard.dc.html` / `designs/Workflow Dashboard (Light).dc.html`
- `designs/Mapping Report.dc.html` / `designs/Mapping Report (Light).dc.html`
- `designs/Workflow Settings Dialog.dc.html` / `designs/Workflow Settings Dialog (Light).dc.html`
- `PARITY_RULE.md` — the project's binding rule: every dark/light pair must be structurally, behaviorally, and data identical; only color differs. Applied throughout all three screens above — carry this rule into the Angular build (one token layer, section "Theming architecture" below) rather than letting the two themes drift.
All design files are self-contained HTML — open directly in a browser to see the live reference (view source for exact markup/spacing/colors).

## Suggested implementation order
1. Decide on the theme question above (Nocturne vs. keep Material light) — this affects every subsequent step.
2. Port design tokens into the codebase (SCSS/CSS vars or Tailwind config).
3. Build/restyle the shared header + footer as one component, used by both screens (and any others).
4. Rebuild `mapping-report.component.ts`'s table as the 3-level accordion described above — this is the biggest structural change from what exists today (a flat Material table with pagination).
5. Restyle `dashboard.component.ts`'s create tiles and workflow grid to match.
