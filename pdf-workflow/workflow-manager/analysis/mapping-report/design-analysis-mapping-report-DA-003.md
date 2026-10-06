# Design Analysis: Mapping Report (Workflow Manager)

> Describes what the Mapping Report feature does and why, based on its design source. It does not define technical implementation.

---

| Field | Value |
| --- | --- |
| Analysis ID | `DA-003` |
| Feature | Mapping Report (pdf-workflow / workflow-manager) |
| Source Material | `SRC-003` -- `branch: design`, `path: pdf-workflow/workflow-manager/design/v4/`, `commit: f5de2a0fbdac4033b2a8aecf523d15948c6801f5` (native files unchanged at the `design` branch head; only `_cover-sheet.md` differs) |
| Source Version | `4` |
| Analysis Version | `2.0` |
| Created By | Business Agent workflow (v1.0-1.1); Design Analysis Agent (v2.0) |
| Created At | 2026-09-08; revised 2026-10-06 |
| Status | `Draft` |
| Related Epic | Pending -- created at the Business PR stage |
| Related Stories | Pending -- created at the Business PR stage |
| Business Owner Approval | Pending for v2.0. v1.1 was approved 2026-09-08 -- see [Review history](#review-history) |

Replaces `DA-002`, which was deleted rather than marked `Superseded` because it analyzed the `design` branch's v2 test drop instead of v4.

## What this is

When a workflow is created by uploading a PDF, the product extracts the PDF's pages, sections, and fields automatically and attaches a confidence score to each proposed mapping. The Mapping Report is where a reviewer checks that extraction: they see how confident it was overall, browse the result page by page, narrow it down to what looks wrong, delete what shouldn't be there, fix the order, and send anything that needs full field editing on to the Workflow Page Editor. A workflow created by hand uses the same screen to show its structure, without the confidence information.

The design was drawn at desktop width only, and it shows no loading, failure, or permission states. Three questions about it are open: where new pages, sections, and fields get added; whether inline editing is part of this phase; and what deleting a field removes.

## Problem

Automatic extraction gives every proposed mapping a confidence score instead of treating extraction as reliable, and the source names extraction as carrying risk when it discusses the related LLM-based creation path ("same class of risk as PDF extraction -- the LLM can misread intent"). Without a review step, an incorrectly extracted or mapped field would carry through unchecked into a workflow used to collect submissions.

Evidence: [OBS-026](#obs-026). Strongly Implied, Medium confidence.

## Goals

Catch and correct an incorrect or low-confidence field extraction before a workflow goes live to collect submissions.

Evidence: [OBS-026](#obs-026). Strongly Implied, Medium confidence.

## Success Metrics

Not defined in source. **Decision Required** -- see [DEC-005](#dec-005), owner: Business Owner.

## Reviewing the mapping

The screen opens with a "Back to dashboard" link, the workflow's name, a one-line description ("How extracted PDF text was mapped to workflow fields and sections."), and a tag naming how the workflow was created: PDF conversion, LLM instructions, or Manually created.

Before touching anything, the reviewer sees five stat tiles -- Total, High (80% or more), Medium (50-79%), Low (under 50%), and Average confidence -- each edged in its band's color, so they can judge at a glance how much attention this workflow needs. The tiles count every mapping in the workflow, not just the ones currently visible, so the summary stays put while the reviewer filters.

Below that, the mapping is a collapsible three-level hierarchy: Page, then Section (a page can hold several), then the individual mapped rows. A page header reads like "Page 2 -- 2 sections · 5 fields". A section header shows its title, a short description if it has one, its field count, and -- when the section heading itself came from the PDF -- that heading's confidence. Section headings appear only in these headers, never as rows of their own. Everything starts expanded; a page or section the reviewer collapses stays collapsed while they change the search or filter. There is no pagination and no "expand all / collapse all" -- each page and section opens and closes on its own.

Each row shows the PDF text (the column is titled after the creation method, e.g. "From PDF"), the element's Type (Heading, Text, Field, List, or Custom), its Target Type, what it Maps to, its confidence, and its Field source (llm or manual), with controls to move it up or down and to delete it.

Search ("Search PDF text") narrows the list as the reviewer types, matching the extracted PDF text and ignoring case, with no submit button. A confidence control (All / High / Medium / Low) narrows the same list. Both work at the row level: a section stays visible only while it still has a matching row or its own heading matches, and a page stays visible only while it still has a visible section. When nothing matches, the screen says "No mappings match the current filter."

**Table view only, for this phase.** The design also includes a Card view -- the same data and the same search, filter, and edit state, laid out as cards -- but building it is deferred; see [BR-003](#br-003) for the decision and [BRULE-005](#brule-005) for the constraint that keeps it addable later. In the design, Card view is also the only place inline editing appears, which matters for the next section. Below roughly 900px the table scrolls sideways rather than reflowing into stacked cards; see [BRULE-008](#brule-008).

## Editing what the extraction got wrong

Every mapping has a kind -- what the PDF element is: a heading, a description, a single field, a field group (a repeating set such as several emergency contacts), or a custom element (such as a signature pad) -- and a target type it maps to in the workflow. The reviewer sees the target type as a compact label such as `Field-Date`, `Field-List-3x` (a list of three sub-fields), or `Custom-App-signature-pad`, so sub-cases are distinguishable without opening anything (exact label format: [BR-005](#br-005)). The kind limits which target types a mapping may take ([BRULE-001](#brule-001)), but this screen offers no control for changing a mapping's target at all.

Fields and lists -- the rows that carry options, validation, and sub-fields -- are not edited on this screen. Every page header has a "Manage page fields" link that opens the Workflow Page Editor, which the source describes as the full editing surface; the report's own editing is deliberately lightweight ([BR-017](#br-017)).

That lightweight editing, in the design, appears only in Card view and only for descriptions (a text box holding the description) and custom elements (a single label box). Only one row can be open for editing at a time. Save (a check mark) keeps the change and shows "Changes saved"; Cancel closes the panel. If there are unsaved changes, switching to another row or pressing Cancel first asks "Discard unsaved changes?" with "Keep editing" and "Discard"; leaving the page triggers the browser's own leave-page warning. Because this phase builds Table view only, and the design's Table view rows have no edit control, whether this inline editing is part of this phase is open -- see [DEC-007](#dec-007).

##### JRN-001
**Review and correct a low-confidence field mapping.** A reviewer filters to Low confidence and finds "Anticipated Start Date" at 42%. It's a field, so the row offers no inline edit; they select "Manage page fields" on Page 2's header and make the correction in the Workflow Page Editor. Had the flagged row been a description or a custom element, they could have corrected it in place instead (pending [DEC-007](#dec-007)). Uses [CAP-002](#cap-002), [CAP-009](#cap-009), and [CAP-004](#cap-004). Registry: [JOURNEY-REGISTRY.md](../../../../registries/JOURNEY-REGISTRY.md) / [full record](../../journeys/journey-review-correct-low-confidence-mapping-JRN-001.md).

## Deleting a mapped field

Every row has a "Delete field" control. It opens a dialog titled "Delete this field?" that names the field, says it will be removed from the workflow, and warns that this can't be undone; for a list, it also says how many sub-fields go with it. Nothing is removed unless the reviewer selects Delete, and a "Field removed" message confirms it afterward.

The README calls this "unlinking" a mapping -- removing the link between the PDF element and the workflow field -- while the dialog text says the field itself leaves the workflow. Which one is meant is open; see [DEC-008](#dec-008).

##### JRN-002
**Remove an incorrectly extracted field.** A reviewer decides the "Emergency contacts" list mapping is wrong, selects Delete field, reads that it and its 3 sub-fields will be removed from the workflow and that this can't be undone, and confirms -- the row disappears and "Field removed" appears. Uses [CAP-005](#cap-005). Registry: [JOURNEY-REGISTRY.md](../../../../registries/JOURNEY-REGISTRY.md) / [full record](../../journeys/journey-remove-incorrectly-extracted-field-JRN-002.md).

## Adding structure, and starting a new workflow

The README describes three low-ceremony ways to add what the extraction missed: "+ Add page" appends a new, empty, numbered page; "+ Add section" opens a small inline form (title required, description optional); and "+ Add field" does the same for a field (label required, type chosen). In each, Add stays disabled until the required part is filled in, and nothing asks for confirmation. A section added by hand would sit in the hierarchy exactly like an extracted one.

The Business Owner has described the same screen as the starting point for a brand-new workflow: after its Workflow Settings are saved, the user lands here and begins by adding a page ([BR-016](#br-016)).

The design file itself contains none of these add controls. With nothing to show, it displays only "No mappings match the current filter." Whether adding happens here, as the README and the Business Owner describe, or has moved to the Workflow Page Editor along with field editing, is open -- see [DEC-006](#dec-006). Until it's decided, the add requirements below are recorded as unconfirmed.

##### JRN-003
**Add a section the extraction missed.** As the README describes it: a reviewer expands a page, selects "+ Add section", enters a title, and selects Add -- the new section appears under that page like an extracted one. The design file does not contain this control, so this journey is unconfirmed until [DEC-006](#dec-006) is decided. Uses [CAP-006](#cap-006). Registry: [JOURNEY-REGISTRY.md](../../../../registries/JOURNEY-REGISTRY.md) / [full record](../../journeys/journey-add-section-extraction-missed-JRN-003.md).

## Removing empty structure, and reordering

A page or section shows a delete control only once it's empty -- a page with no sections, a section with no fields. There's nothing to lose, so there's no confirmation; the item disappears and "Page deleted" or "Section deleted" confirms it. A page or section that still has content can't be deleted; empty it first.

Every page, section, and row has up and down controls that move it one place among its neighbors; the first item's "up" and the last item's "down" are disabled. The order is kept as a per-level list of overrides on top of the original order, so moving one item doesn't require restating the rest (how that's stored is a technical question -- see [TECH-002](#tech-002)).

## How the screen adapts to how a workflow was created

How a workflow was created comes from the workflow itself, not from a control on this screen.

- **PDF conversion** -- everything described above: the confidence tiles, the confidence filter, and a first column titled "From PDF".
- **Manually created** -- the same structure on the same screen, without the stat tiles or the confidence filter; the first column reads "From manual entry", and every row's source shows "manual", since nothing in a hand-built workflow can come from the LLM ([BRULE-009](#brule-009)).
- **LLM instructions** -- the design shows the confidence elements and a "From LLM" column, but the README places this creation path outside this handoff; see "Not built yet" below.

The README's scope note says manually created workflows need no report at all. The Business Owner's clarification that this screen is also where a new workflow starts, and the design file's own manual mode, both point the other way: only the confidence-review elements are specific to extraction ([BR-015](#br-015), [GAP-003](#gap-003)).

## Who sees this

No permission or role distinction appears anywhere in the Mapping Report material -- one reviewer role covers everything described here. The shared header does show organization-level "Members" and "Billing" options, implying a multi-user organization, but whether reviewing or editing mappings is limited to some members has been deferred until a login capability exists ([DEC-004](#dec-004)).

Each mapping arrives already carrying a kind and a confidence score, extracted from the PDF before the reviewer sees the report. How that extraction works is a question for the technical stage ([TECH-001](#tech-001)).

## Information users see or provide

| Concept | Shown / entered | Purpose to the user | Required? | Editable? | Unknowns |
| --- | --- | --- | --- | --- | --- |
| Workflow name | Shown | Which workflow is under review | Not shown | No, not on this screen | -- |
| Creation method | Shown, as a tag | Whether there is an extraction to review | Not shown | No | -- |
| Confidence summary (total, count per band, average) | Shown, extraction-based workflows only | How much attention this workflow needs | -- | No | How confidence is produced ([TECH-001](#tech-001)); whether the 80% / 50% band limits are fixed |
| Page number, with section and field counts | Shown | Orientation in a long document | -- | Order only (reorder) | No upper bound on pages stated |
| Section title | Shown | What the section is | Required when adding a section, per the README | No, not on this screen | Where sections are added ([DEC-006](#dec-006)) |
| Section description | Shown when present | A note for whoever reviews the mapping; the README says people filling in the form never see it | Optional, per the README | No, not on this screen | Set when a section is added, per the README ([DEC-006](#dec-006)) |
| Heading confidence | Shown in a section header, when the heading came from the PDF | How sure the extraction was about the section itself | -- | No | -- |
| PDF text | Shown -- shortened in Table view, in full in Card view | What the extraction read | -- | No | -- |
| Type (kind) | Shown | What kind of element the PDF text is | -- | No | -- |
| Target type | Shown, as a compact label | What the element became in the workflow | -- | No, not on this screen | Where a remap happens is not shown on this screen |
| Maps to | Shown | What the workflow calls the element | -- | Description text and custom labels, inline (pending [DEC-007](#dec-007)); fields and lists, in the Workflow Page Editor | -- |
| Confidence | Shown, per row | How sure the extraction was | -- | No | -- |
| Field source | Shown (llm or manual) | Whether a person or the LLM produced the mapping | -- | No | -- |
| Number of sub-fields in a list | Shown, in the target type label and the delete dialog | What deleting a list would take with it | -- | No, not on this screen | -- |
| Search text | Entered | Find specific PDF text | No | Yes | -- |
| Confidence filter | Chosen (All / High / Medium / Low) | Focus on one confidence band | No -- defaults to All | Yes | Not offered for manually created workflows |
| View (Table / Cards) | Chosen | Choose a layout | -- | Yes | Card view deferred ([BR-003](#br-003)) |

## Existing vs. new experience

**Existing.** The README describes today's Mapping Report as a flat table with pagination. The design file shows only the new screen, so this description can't be checked against it ([ASM-002](#asm-002)).

**New.** The confidence summary; the Page / Section / row hierarchy with collapsible levels; search and confidence filtering that hide empty sections and pages; kind and target type labels; deleting a field behind a confirmation; deleting empty pages and sections; reordering at every level; the hand-off to the Workflow Page Editor; and adapting the screen to how the workflow was created.

**Changed.** Browsing moves from a paged flat list to the hierarchy, with everything reachable without paging.

**Removed.** Pagination. The README also says an "old" pattern of picking a different target from a dropdown was removed, without saying whether that pattern is in today's product or was only in an earlier design draft.

## Requirements

*Every Business Requirement's full statement, acceptance criteria, and evidence classification -- in the same order the narrative above introduces them, not flat ID order. Click a `BR-XXX` reference from the narrative to jump straight here.*

##### BR-018
**Return to the dashboard.**

The product must let the reviewer leave the Mapping Report for the Workflows dashboard.

```text
Given the Mapping Report is open
When the reviewer selects "Back to dashboard"
Then the Workflows dashboard opens
```

Capability: [CAP-001](#cap-001). Evidence: [OBS-032](#obs-032). Explicit, High confidence.

##### BR-001
**Show the extraction confidence summary.**

The product must show the reviewer, before any interaction, how many mappings fall into each confidence band (High / Medium / Low), the total count, and the average confidence.

```text
Given a workflow created by PDF conversion
When its Mapping Report opens
Then five tiles show Total, High (80% or more), Medium (50-79%), Low (under 50%), and Avg confidence
And each tile's top edge is colored by its confidence band
And the counts cover every mapping in the workflow, whatever search or filter is applied
```

Capability: [CAP-001](#cap-001). Evidence: [OBS-001](#obs-001). Explicit, High confidence.

##### BR-002
**Browse mappings as a Page → Section → row hierarchy.**

The product must let the reviewer browse mappings as a collapsible three-level hierarchy (Page, then Section, then the mapped rows), where a page may contain more than one section.

```text
Given a workflow with several pages, one of which holds more than one section
When the reviewer views the mapping
Then pages, sections, and rows show as a collapsible three-level hierarchy, all expanded at first
And each page header shows its page number and its section and field counts
And each section header shows its title, its description if it has one, its field count, and its heading's confidence when the heading came from the PDF
And each row shows the PDF text, Type, Target Type, Maps to, Confidence, and Field source

Given the reviewer has collapsed a page or a section
When the search or confidence filter changes
Then that page or section stays collapsed
```

Capability: [CAP-001](#cap-001). Evidence: [OBS-006](#obs-006), [OBS-007](#obs-007). Explicit, High confidence.

##### BR-003
**Table view, with state that would survive a future view toggle.**

The product must provide the mapping review as a Table view, with search, confidence filter, and in-progress-edit state modeled independently of presentation -- so a Card view, if and when it's built, can be added without restructuring this state.

```text
Given the reviewer has an active search term, a confidence filter, or a row open for editing
Then that state is held independently of how it's rendered (not coupled to Table-view-specific markup)
And Table view is the only rendering built and shown in this phase -- no Card view toggle is presented
```
Note: the source's own criterion (switching Table↔Card without losing state) becomes the acceptance test for whenever Card view is picked up later. In the design, Table view rows carry no inline edit control -- see [DEC-007](#dec-007).

Capability: [CAP-003](#cap-003). Evidence: [OBS-003](#obs-003), [OBS-025](#obs-025). Explicit (shared Table/Card state), narrowed by Human Provided input (Table only for now) -- see [GAP-004](#gap-004).

**Narrowed 2026-09-08, not removed** -- see [GAP-004](#gap-004) for the full `PR #17` review history.

##### BR-004
**Search and filter by confidence, with hierarchical visibility.**

The product must let the reviewer search mappings by their PDF text and filter by confidence band, applying at the row level, with a Section shown only while it has a visible row or its heading matches, and a Page shown only while it has a visible Section.

```text
Given rows at several confidence levels across several sections and pages
When the reviewer selects the "Low" confidence filter
Then only rows below 50% confidence remain visible
And any Section with no remaining row, whose own heading doesn't match, is hidden
And any Page with no remaining Section is hidden

Given the reviewer types in "Search PDF text"
Then the list narrows as they type, matching the extracted PDF text regardless of case, with no submit step

Given nothing matches the current search and filter
Then the screen shows "No mappings match the current filter."
```

Capability: [CAP-002](#cap-002). Evidence: [OBS-002](#obs-002), [OBS-013](#obs-013). Explicit, High confidence.

##### BR-005
**Show a compound Target Type label; offer no remap control.**

The product must show each mapping's target type as a compound label combining the display type and a kind-specific detail (field type, item count, or custom component name), and must not offer a control on this screen for changing a mapping's target type.

```text
Given a list mapping with 3 sub-fields
When the reviewer views its Target Type
Then it reads "Field-List-3x"

Given a description mapping
When the reviewer views its Target Type
Then it reads "Text", with no detail suffix

Given any mapping row
Then no dropdown or other control for changing its target type is offered
```

Capability: [CAP-004](#cap-004). Evidence: [OBS-004](#obs-004), [OBS-005](#obs-005), [OBS-008](#obs-008). Explicit, High confidence.

##### BR-017
**Open the Workflow Page Editor to edit a page's fields.**

The product must offer, on every page header, a way to open the Workflow Page Editor, where field and list mappings are edited.

```text
Given a page in the Mapping Report
When the reviewer selects "Manage page fields" on its header
Then the Workflow Page Editor opens

Given a field or list row
Then the row itself offers no inline edit control
```
Whether the Workflow Page Editor opens at that specific page is not shown in the design.

Capability: [CAP-009](#cap-009). Evidence: [OBS-027](#obs-027), [OBS-028](#obs-028). Explicit, High confidence. See [GAP-005](#gap-005).

##### BR-006
**Edit a description's text or a custom element's label in place.**

The product must let the reviewer correct a description's text or a custom element's label in place, without leaving the Mapping Report.

```text
Given a description mapping is opened for editing
Then the edit panel shows a single text box holding the description's text, with Save and Cancel

Given a custom mapping is opened for editing
Then the edit panel shows a single label box, with Save and Cancel

Given a field or list mapping
Then no inline edit panel is offered (see BR-017)
```

Capability: [CAP-004](#cap-004). Evidence: [OBS-010](#obs-010), [OBS-027](#obs-027). Explicit, High confidence for the design. The design offers this only in Card view, so whether it is part of this Table-only phase is pending [DEC-007](#dec-007). See [GAP-005](#gap-005).

##### BR-007
**One edit panel open at a time, with explicit Save/Cancel.**

The product must allow only one row's edit panel to be open at a time, and every edit panel must end in an explicit Save or Cancel.

```text
Given description row A is open for editing with no unsaved changes
When the reviewer opens row B for editing
Then row A closes without saving
And row B opens with its own edit panel

Given an edit panel is open
When the reviewer selects Save
Then the change is kept, the panel closes, and "Changes saved" confirms it

Given an edit panel is open with no unsaved changes
When the reviewer selects Cancel
Then the panel closes and nothing changes
```

Capability: [CAP-004](#cap-004). Evidence: [OBS-010](#obs-010), [OBS-035](#obs-035). Explicit, High confidence. Pending [DEC-007](#dec-007) for this phase, same as [BR-006](#br-006).

##### BR-014
**Warn before discarding an unsaved edit.**

The product must warn the reviewer before an unsaved edit is lost, whether by switching rows, cancelling, or leaving the page.

```text
Given an edit panel is open with unsaved changes
When the reviewer opens another row for editing, or selects Cancel
Then a dialog titled "Discard unsaved changes?" says the edits haven't been saved and discarding will lose them
And "Keep editing" returns to the open edit with the changes intact
And "Discard" drops the changes (and opens the other row, if that's what was asked)

Given an edit panel is open with unsaved changes
When the reviewer tries to leave the page
Then the browser's leave-page warning appears
```

Capability: [CAP-004](#cap-004). Evidence: [OBS-011](#obs-011), [OBS-035](#obs-035). Explicit, High confidence. Pending [DEC-007](#dec-007) for this phase, same as [BR-006](#br-006).

##### BR-008
**Delete a mapped field, with confirmation that states the cost.**

The product must, when the reviewer deletes a mapped field, confirm first, state what will be lost (including, for a list, how many sub-fields), and remove it only on confirmation.

```text
Given the list mapping "Emergency contacts" with 3 sub-fields
When the reviewer selects Delete field
Then a dialog titled "Delete this field?" says deleting "Emergency contacts" will remove it and its 3 sub-fields from the workflow, and that this can't be undone
And the mapping is removed only if the reviewer selects Delete
And "Field removed" confirms the removal

Given the same dialog
When the reviewer selects Cancel
Then nothing is removed
```

Capability: [CAP-005](#cap-005). Evidence: [OBS-029](#obs-029), [OBS-009](#obs-009), [OBS-011](#obs-011). Explicit, High confidence for the confirmation. What exactly is removed -- the mapping or the workflow field -- is pending [DEC-008](#dec-008); see [GAP-007](#gap-007).

##### BR-009
**Manually add a page.**

The product must let the reviewer add a new, empty, auto-numbered page with no confirmation dialog, shown expanded and ready to receive a section.

```text
Given the reviewer selects "+ Add page"
Then a new page is added, numbered one higher than the highest existing page number
And it shows expanded, with only a "+ Add section" prompt
And no confirmation dialog is shown
```

Capability: [CAP-006](#cap-006). Evidence: [OBS-014](#obs-014), [OBS-012](#obs-012), [OBS-022](#obs-022), [OBS-030](#obs-030). **Assumption, Medium confidence** -- described in the README and consistent with the Business Owner's account of a new workflow, but absent from the design file. Unconfirmed until [DEC-006](#dec-006); see [GAP-006](#gap-006).

##### BR-010
**Manually add a section.**

The product must let the reviewer add a new section to a page via an inline form (title required, description optional), creating a section that groups with extracted sections in the same way.

```text
Given a page with zero or more existing sections
When the reviewer adds a section with a title and no description
Then Add is available only once the title is not empty
And the new section appears under that page in the same way as an extracted section, at 100% confidence
```

Capability: [CAP-006](#cap-006). Evidence: [OBS-015](#obs-015), [OBS-030](#obs-030). **Assumption, Low confidence** -- described in the README only; absent from the design file. Unconfirmed until [DEC-006](#dec-006); see [GAP-006](#gap-006).

##### BR-011
**Manually add a field.**

The product must let the reviewer add a new field to a section via an inline form (label required, type chosen), appearing straight away in the right place with no reload.

```text
Given a section is expanded
When the reviewer adds a field with a label and a type
Then Add is available only once the label is not empty
And the new field appears immediately after that section's existing fields, with no page reload
```

Capability: [CAP-006](#cap-006). Evidence: [OBS-016](#obs-016), [OBS-030](#obs-030). **Assumption, Low confidence** -- described in the README only; absent from the design file. Unconfirmed until [DEC-006](#dec-006); see [GAP-006](#gap-006).

##### BR-016
**Provide this screen as the starting surface for a new workflow.**

The product must, after a new workflow's settings are saved, take the user to this screen with no structure yet, so they can begin building it by adding a page -- whatever the workflow's creation path.

```text
Given a new workflow's settings have just been saved
When the user is returned to the workflow
Then they land on the Mapping Report's structure view, with no pages yet
And they begin by adding a page
```

Capability: [CAP-006](#cap-006). Evidence: [OBS-021](#obs-021), [OBS-022](#obs-022). Human Provided, High confidence, from direct clarification on `PR #17` -- see [GAP-003](#gap-003). How the "add a page" step appears depends on [DEC-006](#dec-006): the design file has no add control, and with no structure it shows only "No mappings match the current filter." ([OBS-030](#obs-030)).

##### BR-012
**Delete only empty structure.**

The product must offer a delete action on a page or section only when it has no children, and must delete it without confirmation.

```text
Given a page with no sections
Then a delete control is shown on its header

Given a page with at least one section
Then no delete control is shown for that page

Given an empty section
When the reviewer deletes it
Then it is removed immediately, with no confirmation dialog
And "Section deleted" confirms it ("Page deleted" for a page)
```

Capability: [CAP-007](#cap-007). Evidence: [OBS-017](#obs-017). Explicit, High confidence.

##### BR-013
**Reorder pages, sections, and rows.**

The product must let the reviewer move a page, section, or row one position among its neighbors, without requiring every item at that level to be re-specified.

```text
Given three rows in one section, in order A, B, C
When the reviewer selects "Move down" on row A
Then the order becomes B, A, C
And rows not explicitly moved keep their original relative order

Given the first item at any level
Then its "Move up" control is disabled
And the last item's "Move down" control is disabled
```

Capability: [CAP-008](#cap-008). Evidence: [OBS-018](#obs-018). Explicit, High confidence.

##### BR-015
**Adapt the screen to how the workflow was created.**

The product must name the workflow's creation method on screen, show the confidence-review elements (stat tiles and confidence filter) for a workflow created by PDF conversion, and hide them for a manually created workflow while still showing its structure.

```text
Given a workflow created by PDF conversion
Then a "PDF conversion" tag is shown, the first column reads "From PDF", and the stat tiles and confidence filter are shown

Given a manually created workflow
Then a "Manually created" tag is shown and the first column reads "From manual entry"
And the stat tiles and confidence filter are not shown
And every row's Field source shows "manual"
And the page / section / row structure is still shown (see BR-016)
```

Capability: [CAP-001](#cap-001). Evidence: [OBS-031](#obs-031), [OBS-019](#obs-019). Explicit, High confidence. The design also shows a third mode, for workflows created from LLM instructions; the README places that path outside this handoff -- see "Not built yet".

**Revised** -- see [GAP-003](#gap-003) and [GAP-008](#gap-008).

## Open Decisions

`DEC-001`-`DEC-004` were resolved on `PR #17`'s review.

- [DEC-001](#dec-001): how the reviewer reaches the Mapping Report -- **Resolved**, three entry paths (PDF conversion, reopening an existing mapping, starting a new workflow).
- [DEC-002](#dec-002): empty state for a workflow with no mappings -- **Resolved**, via the new-workflow flow ([BR-016](#br-016)).
- [DEC-003](#dec-003): table layout on narrow screens -- **Resolved**, horizontal scroll, not stacked cards ([BRULE-008](#brule-008)).
- [DEC-004](#dec-004): org role/permission requirements -- **Resolved (deferred)**, no permission layer until login exists.
- [DEC-005](#dec-005): success metric for this feature -- **Open**, owner: Business Owner.
- [DEC-006](#dec-006): where pages, sections, and fields get added -- **Open**, owner: Business Owner. Blocks [BR-009](#br-009)-[BR-011](#br-011) and [JRN-003](#jrn-003).
- [DEC-007](#dec-007): whether inline editing is part of this Table-only phase -- **Open**, owner: Business Owner. Affects [BR-006](#br-006), [BR-007](#br-007), [BR-014](#br-014).
- [DEC-008](#dec-008): what "Delete field" removes -- **Open**, owner: Business Owner. Affects [BR-008](#br-008).

[DEC-006](#dec-006)-[DEC-008](#dec-008) change what gets built and need an answer before Business Requirements are drafted for the affected areas. [DEC-005](#dec-005) affects how success is measured after launch, not what gets built. The Technical Unknowns ([TECH-001](#tech-001)-[TECH-004](#tech-004)) are for the Technical Agent stage and don't block Business Requirements.

## Not built yet

- **Card view** -- designed, deferred for this phase. See [BR-003](#br-003), [GAP-004](#gap-004).
- **Workflows created from LLM instructions** -- the design shows how this screen would adapt, but the README places this path outside this handoff ("out of scope for this handoff"), to reuse this screen if it's built later.
- **Org-level permissions** -- deferred until login exists. See [DEC-004](#dec-004).
- **Loading, error, and failure states** for opening the report, saving, deleting, and reordering -- not represented in the source, not assumed.
- **Open UX issues the source itself lists as unresolved** -- no reminder of which row is being edited after scrolling, no explanation of the compact target type labels, and no stronger signal for low-confidence rows. The source suggests remedies but designs none. See [GAP-009](#gap-009).
- **Limits** -- no upper bound is stated for pages, sections, fields, or a list's sub-fields.
- **Technical questions for the Technical Agent** -- the extraction mechanism, reorder storage, the README's framework and theme guidance, and its accessibility and responsive notes. See [TECH-001](#tech-001)-[TECH-004](#tech-004).
- This analysis covers only the Mapping Report feature-slice of the v4 drop. The drop's other screens (Dashboard, Workflow Settings Dialog, Workflow Page Editor, the sign-in screens) are out of scope here and, per DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md section 6.2, registered and analyzed separately if taken up.

**Potentially related** -- areas the design touches but doesn't define here; named, not analyzed.

- **Workflow Page Editor** -- where field and list mappings are edited; every page header links to it ([BR-017](#br-017)). It may also be where adding structure now happens ([DEC-006](#dec-006)).
- **Workflows dashboard** -- the "Back to dashboard" destination, and the source of each workflow's creation method.
- **Workflow Settings Dialog** -- the step before a new workflow lands on this screen ([BR-016](#br-016)).
- **Shared header menus** -- account settings, log out, organization settings, Members, Billing; tied to the deferred permissions question ([DEC-004](#dec-004)).
- **Light theme** -- the source keeps a light variant of this screen under a parity rule (only colors may differ); the light file was not read for behavior.

---

## Capabilities

*Grouped by the Journey that needs them, per `ARTIFACT-RELATIONSHIP-MODEL.md` section 3.1. Listed here as a stable entry point for the Business Requirements stage, which will reference these directly when grouping Stories. Full evidence for each lives in its own record, linked below.*

### Serving [JRN-001](#jrn-001) -- Review and correct a low-confidence field mapping

The reviewer narrows the list to what needs fixing, then corrects it -- in the Workflow Page Editor for fields and lists, or in place for descriptions and custom elements.

##### CAP-002
**Filter and Search Mappings.** Let the reviewer narrow a potentially large mapping down to what needs checking. *(↩ used by [BR-004](#br-004))* Registry: [CAPABILITY-REGISTRY.md](../../../../registries/CAPABILITY-REGISTRY.md) / [full record](../../capabilities/capability-filter-and-search-mappings-CAP-002.md).

##### CAP-009
**Open the Workflow Page Editor from the Report.** Let the reviewer move from spotting a problem with a field or list to the screen where it can be fully edited. *(↩ used by [BR-017](#br-017))* Registry: [CAPABILITY-REGISTRY.md](../../../../registries/CAPABILITY-REGISTRY.md) / [full record](../../capabilities/capability-open-page-editor-from-report-CAP-009.md).

##### CAP-004
**Edit a Mapped Field's Details.** Let the reviewer correct a description's text or a custom element's label in place, and see each mapping's target type without opening it. *(↩ used by [BR-005](#br-005), [BR-006](#br-006), [BR-007](#br-007), [BR-014](#br-014))* Registry: [CAPABILITY-REGISTRY.md](../../../../registries/CAPABILITY-REGISTRY.md) / [full record](../../capabilities/capability-edit-mapped-field-details-CAP-004.md).

### Serving [JRN-002](#jrn-002) -- Remove an incorrectly extracted field

##### CAP-005
**Unlink an Incorrect Mapping.** Let the reviewer remove a wrong mapping while understanding its cost. *(↩ used by [BR-008](#br-008))* Registry: [CAPABILITY-REGISTRY.md](../../../../registries/CAPABILITY-REGISTRY.md) / [full record](../../capabilities/capability-unlink-incorrect-mapping-CAP-005.md).

### Serving [JRN-003](#jrn-003) -- Add a section the extraction missed

Unconfirmed until [DEC-006](#dec-006) is decided.

##### CAP-006
**Manually Add Structure.** Let the reviewer fill in whatever the extraction missed, and let a new workflow begin from the same screen whatever its creation path. *(↩ used by [BR-009](#br-009), [BR-010](#br-010), [BR-011](#br-011), [BR-016](#br-016))* Registry: [CAPABILITY-REGISTRY.md](../../../../registries/CAPABILITY-REGISTRY.md) / [full record](../../capabilities/capability-manually-add-structure-CAP-006.md).

### Not yet tied to a Journey

Identified from the source, but none of the three recorded journeys walks through them end to end.

##### CAP-001
**Review Extraction Confidence and Structure.** Let the reviewer judge how much attention a workflow's mapping needs, and browse it, before working through it in detail. *(↩ used by [BR-018](#br-018), [BR-001](#br-001), [BR-002](#br-002), [BR-015](#br-015))* Registry: [CAPABILITY-REGISTRY.md](../../../../registries/CAPABILITY-REGISTRY.md) / [full record](../../capabilities/capability-review-extraction-confidence-CAP-001.md).

##### CAP-003
**Switch Between Table and Card Views.** Let the reviewer choose a layout without losing filter or edit state -- Table view only is built this phase, so no journey uses a view toggle. *(↩ used by [BR-003](#br-003))* Registry: [CAPABILITY-REGISTRY.md](../../../../registries/CAPABILITY-REGISTRY.md) / [full record](../../capabilities/capability-switch-table-card-views-CAP-003.md).

##### CAP-007
**Remove Empty Structure.** Let the reviewer clean up structure that's no longer needed, without risking accidental data loss. *(↩ used by [BR-012](#br-012))* Registry: [CAPABILITY-REGISTRY.md](../../../../registries/CAPABILITY-REGISTRY.md) / [full record](../../capabilities/capability-remove-empty-structure-CAP-007.md).

##### CAP-008
**Reorder Structure.** Let the reviewer fix the order pages, sections, or rows appear in. *(↩ used by [BR-013](#br-013))* Registry: [CAPABILITY-REGISTRY.md](../../../../registries/CAPABILITY-REGISTRY.md) / [full record](../../capabilities/capability-reorder-structure-CAP-008.md).

## Evidence and Traceability

*Reference material. Each entry below is what an "Evidence" link above jumps to -- not needed to understand the feature, needed to audit a specific claim. Every entry ends with a "used by" link back to whatever cited it.*

### Source reviewed

`SRC-003`, read directly from the `design` branch at the commit in the metadata table:

- `designs/Mapping Report.dc.html` (dark) -- markup, the inline script, and its seed data (`SEED_TARGETS`, `SEED`: a "New Hire Onboarding" workflow, 3 pages, 15 mappings). Per CLAUDE-DESIGN-READING-SPEC.md section 4, this file is the source of truth for behavior.
- `README.md` -- read in full; used for business framing, scope, and naming, with every behavioral claim checked against the dark file. Where the two disagree, the dark file is recorded as the behavior and the disagreement as a Gap.
- `PARITY_RULE.md` and `_cover-sheet.md` (readiness `Ready with Limitations`; its listed limitations are the README's open UX issues -- see [OBS-033](#obs-033)).

Excluded: `designs/Mapping Report (Light).dc.html`, not read for behavior (CLAUDE-DESIGN-READING-SPEC.md section 4); shared infrastructure (`support.js`, `image-slot.js`, `_ds/`) checked for presence only; the README's framework-conversion, theming, and implementation-order guidance, recorded as Technical Unknowns ([TECH-003](#tech-003), [TECH-004](#tech-004)); all other screens' files.

### Observations

##### OBS-001
Dark file: five tiles labeled "Total", "High ≥ 80%", "Medium 50–79%", "Low < 50%", "Avg confidence", each with a 2px top border in its band's color. Counts and the rounded average are computed over every mapping in the workflow, not the filtered set. The tiles render only when the workflow was not manually created. Explicit, High. *(↩ used by [BR-001](#br-001))*

##### OBS-002
Dark file: the first filter row holds the "Search PDF text" input (placeholder "Search extracted text…") and the View control (Table / Cards); the second holds the Confidence control (All / High / Medium / Low), shown only when the workflow was not manually created. Search filters live as the user types, matches the extracted PDF text only, and ignores case. The dark file has no "Created from" control and no source filter (see [GAP-008](#gap-008)). Explicit, High. *(↩ used by [BR-004](#br-004))*

##### OBS-003
Dark file: one shared set of state (search term, confidence filter, open edit, collapsed pages and sections) drives both the Table and the Card rendering; switching views changes only which rendering is shown. README: "switching views never resets anything." Explicit, High. *(↩ used by [BR-003](#br-003), [BRULE-005](#brule-005))*

##### OBS-004
README: each extracted element has a `kind` (`heading` | `description` | `field` | `field-group` | `custom`) and maps to a target whose `targetType` (`Section` | `Content` | `Field` | `FieldGroup` | `Custom`) is the discriminant; "`kind` determines which `targetType` a row can be reassigned to ... don't allow cross-kind remapping." Dark file: each kind maps to one target type, with the comment "kind = what the PDF element actually is; drives which SEED_TARGETS it can map to." The dark file offers no control for changing a mapping's target. Explicit, High. *(↩ used by [BR-005](#br-005), [BRULE-001](#brule-001))*

##### OBS-005
Dark file: the Target Type label is `{displayType}-{detail}` -- e.g. `Field-Text`, `Field-Date`, `Field-List-3x` (item count), `Custom-App-signature-pad`; description rows show `Text` with no suffix. Type labels shown per kind: Heading, Text, Field, List, Custom. Explicit, High. *(↩ used by [BR-005](#br-005))*

##### OBS-006
Dark file: Page header -- chevron, "Page N", "{n} sections · {m} fields" (visible counts). Section header -- chevron, "Section" tag, title, description line when present, "{n} fields", and the heading's confidence when a heading mapping exists. Headings are not listed as rows. Seed page 2 holds two sections (Employment Details, Compensation). Pages and sections start expanded; collapse state is held separately from search and filter, so changing a filter doesn't reset it. No pagination and no expand/collapse-all control. Explicit, High. *(↩ used by [BR-002](#br-002))*

##### OBS-007
Dark file, Table view columns: the creation-method column ("From PDF" / "From LLM" / "From manual entry", PDF text shortened to 60 characters) | Type | Target Type | Maps to | Confidence | Field source (llm or manual, with icon) | actions (Move up, Move down, Delete field). Card view shows the same data per row -- type → target type, source, confidence, full PDF text, and the mapped label. Explicit, High. *(↩ used by [BR-002](#br-002))*

##### OBS-008
README (Screens section): "No inline `<select>` remapping. The old 'pick a different target from a dropdown' pattern was removed." Dark file: no `<select>` anywhere on the screen. Explicit, High. *(↩ used by [BR-005](#br-005))*

##### OBS-009
README (Interactions & behavior section): "clicking the pencil expands the row/card in place with kind-specific fields ... and Cancel/Save actions — there is no remap-via-dropdown; clicking unlink opens a confirm dialog (names the sub-field cost for FieldGroups) before removing the mapping." The dark file confirms the confirmation dialog and the absence of dropdown remapping; its edit behavior differs (see [OBS-027](#obs-027)) and its dialog states a sub-field count rather than names (see [OBS-029](#obs-029)). Explicit for the parts the dark file confirms, High. *(↩ used by [BR-008](#br-008))*

##### OBS-010
Dark file, Card view edit panel: a description gets a single text area holding its text; a custom element gets a single label input; each panel ends with Save (check mark) and Cancel (×) buttons. Only one row can be open for editing at a time -- opening another closes the first. Explicit, High. *(↩ used by [BR-006](#br-006), [BR-007](#br-007), [BRULE-002](#brule-002))*

##### OBS-011
README (Known UX issues section): "unlinking opens a confirm dialog (names the sub-field cost for FieldGroups), Save shows a toast, and navigating away from a dirty edit (row switch or `beforeunload`) prompts a discard-confirmation dialog." Confirmed by the dark file, with the differences noted in [OBS-029](#obs-029) and [OBS-035](#obs-035). Explicit, High. *(↩ used by [BR-008](#br-008), [BR-014](#br-014))*

##### OBS-012
README (Interactions & behavior section): "Add page/section/field, delete empty page/section, and reorder (page/section/field) ... all are optimistic, no confirmation except unlink." Dark file: deleting an empty page or section and reordering have no confirmation; deleting a field does. The add controls are absent from the dark file ([OBS-030](#obs-030)). Explicit for delete and reorder, High. *(↩ used by [BR-009](#br-009), [BRULE-007](#brule-007))*

##### OBS-013
Dark file: search and the confidence filter apply to rows; a section is visible when it has a visible row or its heading matches; a page is visible when it has a visible section (or was added by hand); when no page is visible the screen shows "No mappings match the current filter." Explicit, High. *(↩ used by [BR-004](#br-004), [BRULE-004](#brule-004))*

##### OBS-014
README: "+ Add page" appends a new, empty, auto-numbered page (max existing + 1), shown expanded with just a "+ Add section" prompt, no confirmation dialog. Not present in the dark file ([OBS-030](#obs-030)). README only -- Assumption, Medium. *(↩ used by [BR-009](#br-009))*

##### OBS-015
README: "+ Add section" opens an inline form (title required, description optional); Add is disabled until the title is filled; saving creates a `Section` target plus a synthetic heading mapping (`mappedBy: 'manual'`, confidence 100%). Not present in the dark file ([OBS-030](#obs-030)). README only -- Assumption, Low. *(↩ used by [BR-010](#br-010))*

##### OBS-016
README: "+ Add field" opens an inline form (label required, field type chosen); Add is disabled until the label is filled; the new `Field` target is inserted right after that section's fields and appears without a reload. Not present in the dark file ([OBS-030](#obs-030)). README only -- Assumption, Low. *(↩ used by [BR-011](#br-011))*

##### OBS-017
Dark file: a "Delete empty page" control shows only when a page has no sections; a "Delete empty section" control shows only when a section has no rows (counted before any filter). Deleting removes the item immediately with no dialog and shows "Page deleted" or "Section deleted". Explicit, High. *(↩ used by [BR-012](#br-012), [BRULE-003](#brule-003))*

##### OBS-018
Dark file: every page, section, and row has Move up / Move down controls; each move swaps one position; the first item's Move up and the last item's Move down are disabled. Order is held as an override list per level (page order; section order per page; row order per section), falling back to the original order for items not yet moved. Explicit, High. How the override lists are stored is a Technical Unknown -- see [TECH-002](#tech-002). *(↩ used by [BR-013](#br-013))*

##### OBS-019
README (Scope note): "this Mapping Report only applies to the **PDF path**"; "Manually-created workflows: no report needed ... Don't build one"; LLM-based workflows are "out of scope for this handoff", with a note to reuse this screen if built later. README, reference material; its manual-workflow statement is refined by [OBS-021](#obs-021) and differs from the dark file ([OBS-031](#obs-031)). *(↩ used by [BR-015](#br-015), [BRULE-006](#brule-006), [GAP-003](#gap-003))*

##### OBS-020
README (Responsive behavior section): the mapping table's narrow-screen behavior -- horizontal scroll or stacked cards -- is left open: "decide with the user ... Don't silently pick one." The dark file's mapping area already scrolls horizontally. Explicit, High -- a source-flagged open decision, not an omission. *(↩ used by [DEC-003](#dec-003), resolved by [OBS-023](#obs-023))*

##### OBS-021
Manali, [`PR #17` review comment](https://github.com/manalimatkar/product-management/pull/17#discussion_r3960647709), 2026-09-08: "Mapping Report is view used to see workflow-page structure. It can be triggered by [the] process of pdf to workflow conversion on pdf upload, or it can also load an existing mapping for review, or it can also act as a start from scratch for workflow creation." Human Provided, High. Refines the README's Scope note, which frames the report as PDF-path-only. *(↩ used by [BR-016](#br-016), [GAP-003](#gap-003), resolves [DEC-001](#dec-001))*

##### OBS-022
Manali, [`PR #17` review comment](https://github.com/manalimatkar/product-management/pull/17#discussion_r3960657394), 2026-09-08: "For [a] new workflow, [the] user experience is to first go to [the] workflow settings page, and then on save[,] user will land on [the] workflow mapping page where they start by adding [a] page." Human Provided, High. *(↩ used by [BR-016](#br-016), [BR-009](#br-009), resolves [DEC-002](#dec-002))*

##### OBS-023
Manali, [`PR #17` review comment](https://github.com/manalimatkar/product-management/pull/17#discussion_r3960664130), 2026-09-08: "Keep table horizontal scroll." Human Provided, High. *(↩ used by [BRULE-008](#brule-008), resolves [DEC-003](#dec-003))*

##### OBS-024
Manali, [`PR #17` review comment](https://github.com/manalimatkar/product-management/pull/17#discussion_r3960668770), 2026-09-08: "This is deferred for later when login capability is enabled." (re: org role/permission distinctions for reviewing or editing mappings) Human Provided, High. *(↩ resolves [DEC-004](#dec-004))*

##### OBS-025
Manali, [`PR #17` review comment](https://github.com/manalimatkar/product-management/pull/17#issuecomment-5589857757) (Review Outcome, `BR-003` left unchecked), 2026-09-08: "For now work on table view." Human Provided, High. Card view is deferred for this phase, not rejected. *(↩ used by [BR-003](#br-003), [GAP-004](#gap-004))*

##### OBS-026
README (Scope note) and dark file: every proposed mapping carries a confidence score rather than being treated as reliable, and the screen describes itself as showing "How extracted PDF text was mapped to workflow fields and sections." Discussing the LLM-based creation path, the README says it carries "the same class of risk as PDF extraction -- the LLM can misread intent." No single sentence states the resulting problem or goal -- synthesized across these passages. Strongly Implied, Medium. *(↩ used by [Problem](#problem), [Goals](#goals))*

##### OBS-027
Dark file: field and list rows are not editable inline -- the script's comment reads "Field and field-group rows now edit exclusively in the Workflow Page Editor (they carry too much associated data — options, validation, sub-fields — for this report's simple inline label/type switch)." The edit (pencil) control appears only in Card view, and only on description and custom rows; Table view rows have no edit control. Explicit, High. *(↩ used by [BR-017](#br-017), [BR-006](#br-006), [GAP-005](#gap-005), [DEC-007](#dec-007))*

##### OBS-028
Dark file: every page header has a "Manage page fields" link that opens `Workflow Page Editor.dc.html`. README: "the Mapping Report's inline edit panel deliberately only exposes a lightweight subset and links here for anything more." Explicit, High. *(↩ used by [BR-017](#br-017))*

##### OBS-029
Dark file: every row (both views) has a "Delete field" control (trash icon). It opens a dialog titled "Delete this field?" with, for a list, `Deleting "<label>" will remove it and its <N> sub-fields from the workflow. This can't be undone.` and otherwise `Deleting "<label>" will remove this field from the workflow. This can't be undone.`; buttons Cancel and Delete. Confirming removes the row and shows "Field removed". Explicit, High. *(↩ used by [BR-008](#br-008), [GAP-007](#gap-007))*

##### OBS-030
Dark file: no "+ Add page", "+ Add section", or "+ Add field" control and no logic to add anything. The script keeps a list of hand-added pages and can display a section description, but nothing on the screen fills either. When no page is visible -- including when a workflow has no mappings -- the screen shows only "No mappings match the current filter." Explicit, High. *(↩ used by [BR-009](#br-009), [BR-010](#br-010), [BR-011](#br-011), [BR-016](#br-016), [GAP-002](#gap-002), [GAP-006](#gap-006))*

##### OBS-031
Dark file: the creation method is read from the workflow (`pdf`, `instructions`, or `manual`; the README's demo note says to "drive it from the workflow's actual creation method"). It shows as a tag -- "PDF conversion", "LLM instructions", "Manually created" -- and titles the first column "From PDF", "From LLM", or "From manual entry". The stat tiles and confidence filter show unless the workflow was created manually. In a manually created workflow every row's Field source shows "manual"; the README's Files section states the same ("there's no LLM in a manually-created workflow, so a field can never be LLM-sourced there"). Explicit, High. *(↩ used by [BR-015](#br-015), [BRULE-006](#brule-006), [BRULE-009](#brule-009), [GAP-003](#gap-003), [GAP-008](#gap-008))*

##### OBS-032
Dark file: above the title, a "Back to dashboard" link to `Workflow Dashboard.dc.html`; then the workflow name, the line "How extracted PDF text was mapped to workflow fields and sections.", and the creation-method tag. Explicit, High. *(↩ used by [BR-018](#br-018), [GAP-001](#gap-001))*

##### OBS-033
README (Known UX issues, "Remaining open items") and `_cover-sheet.md` (`knownLimitations`): (1) no breadcrumb reminding the user which field or section they're editing after they scroll; (4) compound type tags "need onboarding ... consider a tooltip or one-time legend"; (5) low-confidence rows don't visually escalate -- "consider a stronger cue or default-sorting low-confidence to the top"; (6) Table/Card edit-panel markup duplication (technical -- see [TECH-003](#tech-003)). Explicit, High. *(↩ used by [GAP-009](#gap-009))*

##### OBS-034
README: the accordion "differs from the current flat Material table"; implementation step 4: "Rebuild `mapping-report.component.ts`'s table as the 3-level accordion ... the biggest structural change from what exists today (a flat Material table with pagination)." README only; the dark file shows only the new screen. *(↩ used by [ASM-002](#asm-002))*

##### OBS-035
Dark file: Save shows "Changes saved". With unsaved changes, opening another row's edit or selecting Cancel opens a dialog titled "Discard unsaved changes?" -- "Your edits to this field haven't been saved. Discarding will lose them." -- with "Keep editing" and "Discard"; Discard drops the changes and, if another row was requested, opens it. Leaving the page with unsaved changes triggers the browser's standard leave-page warning, not this dialog. Explicit, High. *(↩ used by [BR-007](#br-007), [BR-014](#br-014))*

### Business Rules

##### BRULE-001
A mapping's `kind` constrains which `targetType`s it may be remapped to (e.g. `field` → `Field` only, `field-group` → `FieldGroup` only). This screen offers no remap control at all. Explicit, High. Source: [OBS-004](#obs-004). *(↩ used by [BR-005](#br-005))* Registry: [BUSINESS-RULE-REGISTRY.md](../../../../registries/BUSINESS-RULE-REGISTRY.md) / [full record](../../business-rules/business-rule-kind-constrains-remap-BRULE-001.md).

##### BRULE-002
Only one row may be in edit mode at a time. Explicit, High. Source: [OBS-010](#obs-010). *(↩ used by [BR-007](#br-007))* Registry: [BUSINESS-RULE-REGISTRY.md](../../../../registries/BUSINESS-RULE-REGISTRY.md) / [full record](../../business-rules/business-rule-one-edit-at-a-time-BRULE-002.md).

##### BRULE-003
A page or section may be deleted only when it has no children. Explicit, High. Source: [OBS-017](#obs-017). *(↩ used by [BR-012](#br-012))* Registry: [BUSINESS-RULE-REGISTRY.md](../../../../registries/BUSINESS-RULE-REGISTRY.md) / [full record](../../business-rules/business-rule-delete-only-when-empty-BRULE-003.md).

##### BRULE-004
A Section is visible only if it has a matching row or its own heading matches; a Page is visible only if it has a visible Section. Explicit, High. Source: [OBS-013](#obs-013). *(↩ used by [BR-004](#br-004))* Registry: [BUSINESS-RULE-REGISTRY.md](../../../../registries/BUSINESS-RULE-REGISTRY.md) / [full record](../../business-rules/business-rule-hierarchical-filter-visibility-BRULE-004.md).

##### BRULE-005
Table view and Card view must show identical filtered/grouped data and share all state. Explicit, High. Source: [OBS-003](#obs-003). *(↩ used by [BR-003](#br-003) -- kept as the modeling constraint for whenever Card view is built)* Registry: [BUSINESS-RULE-REGISTRY.md](../../../../registries/BUSINESS-RULE-REGISTRY.md) / [full record](../../business-rules/business-rule-table-card-parity-BRULE-005.md).

##### BRULE-006
The confidence-review elements (stat tiles and confidence filter) appear only for a workflow whose structure came from an extraction step -- PDF conversion in this phase. A manually created workflow uses the same screen without them. Explicit, High. Source: [OBS-031](#obs-031), [OBS-019](#obs-019), [OBS-021](#obs-021). *(↩ used by [BR-015](#br-015))* Registry: [BUSINESS-RULE-REGISTRY.md](../../../../registries/BUSINESS-RULE-REGISTRY.md) / [full record](../../business-rules/business-rule-pdf-path-only-BRULE-006.md).

##### BRULE-007
Structural edits (add page/section/field, delete empty page/section, reorder) never require confirmation; deleting a mapped field is the one exception. The add part applies only if adding happens on this screen ([DEC-006](#dec-006)). Explicit, High. Source: [OBS-012](#obs-012), [OBS-017](#obs-017), [OBS-029](#obs-029). *(↩ used by [BR-008](#br-008), [BR-009](#br-009), [BR-010](#br-010), [BR-011](#br-011), [BR-012](#br-012), [BR-013](#br-013))* Registry: [BUSINESS-RULE-REGISTRY.md](../../../../registries/BUSINESS-RULE-REGISTRY.md) / [full record](../../business-rules/business-rule-no-confirmation-except-unlink-BRULE-007.md).

##### BRULE-008
Below roughly 900px, the mapping table uses horizontal scroll -- never a stacked-card row layout. Human Provided, High. Source: [OBS-020](#obs-020), [OBS-023](#obs-023). *(↩ used by [BR-002](#br-002), [BR-004](#br-004), [BR-006](#br-006))* Registry: [BUSINESS-RULE-REGISTRY.md](../../../../registries/BUSINESS-RULE-REGISTRY.md) / [full record](../../business-rules/business-rule-horizontal-scroll-mobile-BRULE-008.md).

##### BRULE-009
In a manually created workflow, every row's source is shown as "manual" -- no field in it can be LLM-sourced. Explicit, High. Source: [OBS-031](#obs-031). *(↩ used by [BR-015](#br-015))* Registry: [BUSINESS-RULE-REGISTRY.md](../../../../registries/BUSINESS-RULE-REGISTRY.md) / [full record](../../business-rules/business-rule-manual-workflow-source-manual-BRULE-009.md).

### Assumptions

##### ASM-001
The Mapping Report is entered from the Dashboard's workflow list by opening a workflow whose creation source is PDF. Inferred from the README's Dashboard section; confirmed in substance by [OBS-021](#obs-021) -- the PDF-conversion entry path exists, alongside two others (reopening an existing mapping; starting a new workflow from scratch). Status: **Confirmed**. Impact if false: N/A, confirmed. Owner: Business Owner.

##### ASM-002
Today's Mapping Report is a flat table with pagination, so the hierarchy replaces it rather than arriving as a new screen. Basis: README only ([OBS-034](#obs-034)); the design file shows only the new screen. Impact if false: "Existing vs. new experience" misdescribes what changes for current users. Owner: Business Owner. Status: **Open**.

### Decisions

##### DEC-001
What is the navigation trigger into the Mapping Report from elsewhere in the product? Raised as [GAP-001](#gap-001) (the README never states this). **Resolved 2026-09-08** -- see [OBS-021](#obs-021). Three entry paths: PDF conversion, reopening an existing mapping for review, and starting a new workflow from scratch.

##### DEC-002
Is there a defined empty state for a workflow with no mappings at all (as opposed to an individual empty page or section)? Raised as [GAP-002](#gap-002). **Resolved 2026-09-08** -- see [OBS-022](#obs-022), [BR-016](#br-016). New workflow: Workflow Settings → Save → lands on this screen with no structure, starts by adding a page. How the add step appears depends on [DEC-006](#dec-006).

##### DEC-003
Should the mapping table, below roughly 900px, scroll horizontally (matches desktop, simpler) or collapse each row into a stacked card (better mobile UX, more work)? The source deferred this explicitly ([OBS-020](#obs-020)). **Resolved 2026-09-08** -- see [OBS-023](#obs-023), [BRULE-008](#brule-008). Horizontal scroll.

##### DEC-004
Does reviewing or editing a workflow's mapping require a specific org role or permission, given the shared header shows org-level Members/Billing controls? **Resolved (deferred) 2026-09-08** -- see [OBS-024](#obs-024). No permission layer now; revisit when a login capability is scoped.

##### DEC-005
What measurable signal would tell the team this feature is working (e.g. less time spent correcting extractions, or fewer downstream data-quality issues traced to a bad mapping)? The source states no success criteria for this feature. **Open**, owner: Business Owner.

##### DEC-006
Where does the reviewer add pages, sections, and fields -- on the Mapping Report, or elsewhere (for example the Workflow Page Editor, where field editing now happens)? Why it matters: it decides whether [BR-009](#br-009)-[BR-011](#br-011) exist for this screen, how a new workflow starts here ([BR-016](#br-016)), and whether [JRN-003](#jrn-003) is a journey on this screen. Affected: [CAP-006](#cap-006), [BR-009](#br-009), [BR-010](#br-010), [BR-011](#br-011), [BR-016](#br-016), [BRULE-007](#brule-007). Evidence: the README describes add controls here ([OBS-014](#obs-014)-[OBS-016](#obs-016)) and the Business Owner described starting a new workflow here by adding a page ([OBS-022](#obs-022)); the dark design file has no add controls ([OBS-030](#obs-030)). See [GAP-006](#gap-006). Proposed owner: Business Owner, with the Producing Designer. **Open**.

##### DEC-007
Is inline editing of descriptions and custom labels part of this phase? Why it matters: the design offers it only in Card view ([OBS-027](#obs-027)), and this phase builds Table view only ([OBS-025](#obs-025)), whose rows have no edit control in the design -- so as designed, nothing on this screen is editable inline this phase. Affected: [CAP-004](#cap-004), [BR-006](#br-006), [BR-007](#br-007), [BR-014](#br-014). Possible directions, none chosen here: leave inline editing out until Card view is built; or carry it into Table view, which the design doesn't show. Proposed owner: Business Owner. **Open**.

##### DEC-008
What does "Delete field" remove: only the link between the PDF element and its workflow field, or the field itself from the workflow? Why it matters: deleting a workflow field is a larger and, per the dialog, irreversible change. Affected: [CAP-005](#cap-005), [BR-008](#br-008), [JRN-002](#jrn-002). Evidence: the README calls the action "unlink" and describes "removing the mapping" ([OBS-009](#obs-009)); the dark file labels it "Delete field" and its dialog says the field will be removed "from the workflow" ([OBS-029](#obs-029)). See [GAP-007](#gap-007). Proposed owner: Business Owner. **Open**.

### Gaps

##### GAP-001
Unclear Behavior. The README never states how the reviewer reaches the Mapping Report or leaves it. Leaving: the design file shows a "Back to dashboard" link ([OBS-032](#obs-032)). Entering: inferred as [ASM-001](#asm-001); **Resolved 2026-09-08** via [DEC-001](#dec-001) -- Human Provided evidence ([OBS-021](#obs-021)).

##### GAP-002
Missing Source. The README describes no state for a workflow with no mappings at all (only per-page and per-section empty states); the design file shows only its generic "No mappings match the current filter." message ([OBS-030](#obs-030)). **Resolved 2026-09-08** via [DEC-002](#dec-002) -- Human Provided evidence ([OBS-022](#obs-022)).

##### GAP-003
Conflict, Human Provided evidence vs. README. The README's Scope note says manually created workflows get no report at all ("Don't build one"); [OBS-021](#obs-021) describes this screen as also the starting point for building a workflow from scratch. **Resolved 2026-09-08** -- per PRODUCT-SOURCE-MATERIAL-SPEC.md section 6, a direct Business Owner clarification on product behavior takes precedence over the design document's own scope text. The dark design file agrees: a manually created workflow renders this screen without the stat tiles or confidence filter ([OBS-031](#obs-031)). [BR-015](#br-015) covers the confidence elements only; [BR-016](#br-016) covers the new-workflow start.

##### GAP-004
Scope narrowing, Human Provided evidence vs. design source. The design presents Card view ([OBS-003](#obs-003), [OBS-007](#obs-007)) as a second rendering on equal footing with Table view; [OBS-025](#obs-025) scopes the *build* to Table view only for this phase. **Resolved 2026-09-08** -- same authority basis as [GAP-003](#gap-003). Card view is deferred, not rejected; [BR-003](#br-003) narrowed rather than removed; [BRULE-005](#brule-005) kept as the modeling constraint for whenever Card view is picked up.

##### GAP-005
Conflict, README vs. design file -- editing. The README puts an edit control on every row in both views, with a Label and Field type editor for a field and a Label, per-item list, and Min/Max items editor for a list. The dark file has no edit control in Table view; in Card view it offers editing only for descriptions and custom elements, and sends field and list editing to the Workflow Page Editor ([OBS-027](#obs-027), [OBS-028](#obs-028)). **Resolved** -- per CLAUDE-DESIGN-READING-SPEC.md section 4 the dark design file is the source of truth for behavior, so the README's field and list editors are not recorded as requirements. The consequence for this Table-only phase is [DEC-007](#dec-007). *(↩ used by [BR-017](#br-017), [BR-006](#br-006))*

##### GAP-006
Conflict, README and Human Provided evidence vs. design file -- adding structure. The README describes add-page, add-section, and add-field controls on this screen ([OBS-014](#obs-014)-[OBS-016](#obs-016)), and the Business Owner described a new workflow starting here by adding a page ([OBS-022](#obs-022)); the dark file contains no add controls ([OBS-030](#obs-030)). Not resolved by source authority, since Business Owner input supports the README's account -- recorded as [DEC-006](#dec-006). **Open**. *(↩ used by [BR-009](#br-009), [BR-010](#br-010), [BR-011](#br-011))*

##### GAP-007
Conflict, README vs. design file -- deleting a field. The README calls the action "unlink" and says its dialog "names the sub-field cost"; the dark file calls it "Delete field", says the field will be removed "from the workflow", and states a sub-field count rather than names ([OBS-009](#obs-009), [OBS-029](#obs-029)). The dialog content follows the dark file. What is removed is recorded as [DEC-008](#dec-008). **Open**. *(↩ used by [BR-008](#br-008))*

##### GAP-008
Conflict, README vs. design file -- creation method. The README describes a demo "Created from" control (PDF / LLM / Manual) in the first filter row, and filters that share a "source filter"; the dark file has neither -- the creation method comes from the workflow and shows as a tag ([OBS-002](#obs-002), [OBS-031](#obs-031)). The README itself calls its toggle illustrative. **Resolved** -- recorded as the dark file shows. *(↩ used by [BR-015](#br-015))*

##### GAP-009
Known limitation, flagged by the source. Three user-facing issues are listed as unresolved in the design: no reminder of which field or section is being edited after the reviewer scrolls; compact target type labels with no explanation for first-time users; and low-confidence rows that don't stand out beyond a muted color ([OBS-033](#obs-033)). The source suggests possible remedies but designs none, so none is recorded as a requirement. Owner: Business Owner, with the Producing Designer. **Open**.

### Technical Unknowns

##### TECH-001
Business behavior known: each mapping arrives with a `kind` and a confidence score, extracted from the PDF before the reviewer sees the report. Technical question: what extraction mechanism produces `kind` and confidence, and where does that processing happen? Related: [CAP-001](#cap-001). For the Technical Agent stage -- not a business decision.

##### TECH-002
Business behavior known: reordering keeps an explicit per-level override list, falling back to the original order for unmoved items ([OBS-018](#obs-018)). Technical question: how are these override lists stored and kept in sync, and how do they interact with items added or deleted later? Related: [BR-013](#br-013). For the Technical Agent stage -- not a business decision.

##### TECH-003
Business behavior known: the screen's content and behavior as recorded above. The README adds framework and repository guidance, preserved here because it cites facts about the target engineering repository:
- "I looked at your repo (`pdf-workflow/workflow-manager`) and found matching real components already scaffolded: `src/app/features/dashboard/dashboard.component.ts`, `src/app/features/mapping-report/mapping-report.component.ts`."
- "**Important mismatch to resolve first:** the existing Angular components are built with **Angular Material + Tailwind, light theme** ... These new designs are in **Nocturne**, a dense dark UI system ... Decide up front whether: 1. Nocturne becomes the new global theme ... or 2. These are just references for a future restyle and current Material components stay as-is for now."
- State management: "`mappings: MappingEntry[]` (already exists per `ApiService`/`MappingEntry`) — group client-side into Page → Section → Field for render; don't refetch per level."
- "Section→Field ownership: ... each field is owned by the nearest preceding Section in the target list ... confirm this matches how sections/fields are actually modeled in `WorkflowStore` before implementing."
- Known UX issue 6: the Table and Card edit panels are duplicated in the reference -- "extract this once ... so future edits to the edit panel don't need to land twice."
- Theming architecture, component architecture, testing, and the suggested implementation order (step 4: rebuild the existing component's table as the accordion).

Technical question: how to apply this guidance, including the theme decision, which the README asks to settle before anything else. For the Technical Agent stage.

##### TECH-004
Business behavior known: the screen's layout and interactions as recorded above, drawn at desktop width. The README lists additions it says a production build needs: accordion toggles exposing their expanded state to screen readers, "Changes saved"-style messages announced to assistive technology, visible focus on every control, labels on icon-only buttons, contrast checked to WCAG AA in both themes, and reduced-motion support; and responsive guidance for this screen -- stat tiles wrapping to two per row below about 900px and one per row below about 480px, the search field going full width below about 640px, and a suggested breakpoint scale. Technical question: how these are met, and which become acceptance criteria. For the Technical Agent stage.

---

## Quality Checklist

- [x] Exact source path, branch/commit, and version are recorded.
- [x] `## Problem`, `## Goals`, and `## Success Metrics` are each present and either grounded in the source or recorded as a Decision Required.
- [x] `## Information users see or provide` and `## Existing vs. new experience` are filled in, each saying what the source doesn't describe.
- [x] `## Not built yet` separates out-of-scope items from **Potentially related** areas.
- [x] The narrative reads without resolving an evidence link, classification tag, or Gherkin block; "What this is" has zero IDs.
- [x] No commentary about this document's own revision history appears in its content -- that lives in [Review history](#review-history).
- [x] Every requirement has evidence, a classification, and a confidence level -- linked, not just named.
- [x] Every Requirement links to its Capability and source Observations; every Business Rule links to its source Observations; Capability records carry their own evidence. `Related Epic` / `Related Stories` read `Pending` until the Business Agent stage.
- [x] Acceptance criteria live with their requirement in `## Requirements`.
- [x] The feature-area narrative contains no `##### BR-XXX` headings.
- [x] Strong inferences are labeled `Strongly Implied`; human-supplied answers are labeled `Human Provided`; README-only claims the design file doesn't confirm are labeled `Assumption`.
- [x] Every open Decision is visible near the top; resolved ones say how and on what evidence.
- [x] "Not built yet" is present, and nothing is silently dropped.
- [x] Technical implementation choices are excluded or recorded as Technical Unknowns.
- [x] Every ID-only heading in the Evidence section has at least one "used by" back-link, and every "Evidence:" link resolves.

## Review history

| Review Item | Outcome | Reviewer | Date | Notes |
| --- | --- | --- | --- | --- |
| Design Analysis v2.0 | Draft, awaiting review | Design Analysis Agent | 2026-10-06 | Re-read `SRC-003` directly, treating the dark `Mapping Report.dc.html` as the source of truth per CLAUDE-DESIGN-READING-SPEC.md, and brought the document up to the current DESIGN-ANALYSIS-SPEC.md and template. Major revision (REQUIREMENTS-VERSIONING-SPEC.md section 9) -- the v1.1 approval no longer applies. Added the "Information users see or provide" and "Existing vs. new experience" sections, "How the screen adapts to how a workflow was created", "Potentially related" scope, and a Source reviewed list. Corrected requirements the dark file contradicts: [BR-006](#br-006) (field and list editing moved to the Workflow Page Editor; inline editing only in Card view), [BR-008](#br-008) (dialog states a sub-field count and says the field leaves the workflow), [BR-015](#br-015) (confidence elements hidden only for manual workflows), [BR-005](#br-005) (no remap control on this screen). Reclassified [BR-009](#br-009)-[BR-011](#br-011) as Assumptions, absent from the dark file. Added [BR-017](#br-017), [BR-018](#br-018), [OBS-027](#obs-027)-[OBS-035](#obs-035), [ASM-002](#asm-002), [DEC-006](#dec-006)-[DEC-008](#dec-008), [GAP-005](#gap-005)-[GAP-009](#gap-009), [TECH-003](#tech-003), [TECH-004](#tech-004), [CAP-009](#cap-009), and [BRULE-009](#brule-009); restated [BRULE-006](#brule-006). Analysis Version `1.1` → `2.0`; Status `Approved` → `Draft`. |
| Problem/Goals/Success Metrics added | Editorial addition | Business Agent | 2026-09-25 | `DESIGN-ANALYSIS-SPEC.md` sections 4.14-4.16 added these as required sections. Problem and Goals grounded in [OBS-026](#obs-026) (Strongly Implied -- the source never states either directly); Success Metrics has no source basis, recorded as [DEC-005](#dec-005), Open, owner Business Owner. Analysis Version `1.0` → `1.1`; no existing requirement changed. |
| Design Analysis v1.0 | Approved -- 16/16 requirements, after one revision | Manali | 2026-09-08 | `PR #17` merged with 15/16 requirements checked directly; `BR-003` was left unchecked with an inline note ("For now work on table view") -- incorporated as [OBS-025](#obs-025), `BR-003` narrowed to Table view only ([GAP-004](#gap-004)), Card view kept as deferred, not rejected. [DEC-001](#dec-001)-[DEC-004](#dec-004) were resolved via `PR #17`'s review comments, incorporated as Human Provided evidence. v1.0 was produced from the README's Mapping Report sections; the 2026-09-10 reading rules (dark `.dc.html` as source of truth) post-date it. |
| Business Requirements | Not started | -- | -- | Awaiting this Design Analysis's review outcome. |
