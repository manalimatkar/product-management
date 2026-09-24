# Design Analysis: <Feature Name>

<!--
TEMPLATE GUIDANCE ONLY -- delete this whole comment block once the sections below are filled
in. None of it belongs in a real, generated Design Analysis; a reader of a finished analysis
needs the product's story, not this template's own authoring rules or revision history.

The one rule that makes links survive a rewrite: every linkable item (BR-, CAP-, OBS-, GAP-,
DEC-, ASM-, TECH-, BRULE-) gets its own heading containing only the ID -- "##### BR-003", never
"##### BR-003: Some Descriptive Title". GitHub's auto-generated anchor is built from the whole
heading text, so an ID-only heading keeps its anchor (#br-003) permanently, even after the bold
title on the next line gets reworded later. Put the descriptive title as bold text on the line
right after the heading, not in the heading itself. Each ID's heading exists in exactly one
place in the document -- a BR-XXX heading lives in "## Requirements" only, never duplicated in
the narrative above it.

Reading or writing a CAP-, JRN-, or BRULE- ID? Those three describe the product, not just this
one analysis -- unlike a BR-/OBS-/GAP-/DEC-/ASM-/TECH- ID, which is scoped to this document
alone. Each has a real registry: JOURNEY-REGISTRY.md, CAPABILITY-REGISTRY.md,
BUSINESS-RULE-REGISTRY.md, under ../registries/. Check the registry before minting a new one --
cite an existing entry and link to its record if the analysis is genuinely describing the same
Journey/Capability/Business Rule. See ARTIFACT-RELATIONSHIP-MODEL.md section 3.1 for the full
model, including why a Capability's realness is proven by which Journeys actually depend on it,
not by its description alone.

This template's own format history -- why it's shaped this way, including the 2026-09-21 pass
that moved every Business Requirement's Gherkin/Evidence detail out of the narrative into a
dedicated "## Requirements" register -- lives in DESIGN-ANALYSIS-SPEC.md section 11 and
EVIDENCE-SPEC.md section 10. A real Design Analysis should never carry its own
"Format revised..." paragraph -- that's this template's history, not the product's, and belongs
in the spec, not repeated at the top of every instance.

No HTML anywhere else in a generated analysis, per this repository's standing format preference
-- every cross-reference is a real markdown link to a heading, never a collapsible block. This
comment is the one template-authoring exception, and it gets deleted before publishing anyway.
-->

> `<One sentence, plain language, describing what this document is about -- not who or what produced it or how. E.g. "Describes what the Mapping Report feature does and why, based on its design source. It does not define technical implementation.">`

---

| Field | Value |
| --- | --- |
| Analysis ID | `DA-<number>` |
| Feature | `<feature name>` |
| Source Material | `<repository path or link -- branch/path/commit for a design-branch source, per ARTIFACT-STORAGE-SPEC.md section 10>` |
| Source Version | `<version, or Not Versioned>` |
| Analysis Version | `<version>` |
| Created By | `<Business Agent run or author -- keep this factual, a name/identifier, not a narrative sentence>` |
| Created At | `<timestamp>` |
| Status | `Draft` / `In Review` / `Approved` / `Superseded` / `Rejected` |
| Related Epic | `<Epic reference, or Pending -- created at the Business PR stage>` |
| Related Stories | `<Story references, or Pending>` |
| Business Owner Approval | `<approval reference, or Pending>` |

`<If this analysis supersedes, corrects, or replaces a prior one, say so here in one short paragraph -- what happened and why, once, right under the metadata table. Don't repeat the same lineage explanation again inside "What this is" below; that section is for the product, not this document's own history.>`

## What this is

`<Two or three sentences, plain language: what does this feature do, who is it for, what business problem or outcome does it address. No IDs in this paragraph, and no links -- someone who has never seen the feature should be able to read only this and understand the point of it. State source limitations as plain prose here too if useful context, without linking out to the requirement that resolves them -- save the link for where the resolution is explained.>`

## `<Feature area 1, named the way a person would recognize it -- not "Capability CAP-001">`

`<Prose. Explain how this part of the feature works, in the order a user would experience it. Weave in the reasoning -- why a rule exists -- rather than just stating the rule. This prose IS the primary description of each requirement in plain language -- don't just restate a BR-XXX's statement here, actually explain it. Link to a "## Requirements" entry only where there's a real reason beyond restating the rule -- pointing at a scope decision, a deferral, or where the exact acceptance detail matters (`see [BR-005](#br-005) for the exact label format`) -- not mechanically once per requirement. A Journey (`JRN-`), if one belongs in this feature area, stays embedded here as its own ID-only heading -- it already reads as plain narrative and carries no Evidence tag.>`

<!-- Duplicate this "## Feature area" heading + prose for every area of the feature. No `##### BR-XXX` heading belongs here -- every Business Requirement's full detail lives in "## Requirements" below, once. -->

## `<Feature area 2>`

`<...>`

## Requirements

*Every Business Requirement's full statement, acceptance criteria, and evidence classification -- grouped in the same order the feature-area narrative above introduces them, not flat ID order, so this stays "coherent by area" rather than a table to reassemble. Click a `BR-XXX` reference from the narrative to jump straight here.*

##### BR-001
**`<Short, outcome-oriented title>`**

`<The requirement statement, in one or two sentences.>`

```text
Given <starting condition>
When <user action or business event>
Then <observable product behavior>
```
`<Add Validation / Loading / Empty / Success / Error / Permissions / Recovery cases here only if the source actually represents them -- say "Not represented in source" rather than omitting the case silently.>`

Evidence: [OBS-001](#obs-001). `<Explicit / Strongly Implied / Assumption / Human Provided>`, `<High / Medium / Low>` confidence.

<!-- Duplicate the ID-only heading + title + statement + acceptance criteria + evidence line above for every requirement, in the order its feature area appears above. If a requirement's evidence line needs to explain a revision (e.g. narrowed after review feedback) AND that same story is already told by a GAP-/DEC- entry in Evidence and Traceability below, don't repeat the full explanation here -- write one line pointing at it instead: "**Narrowed <date>, not removed** -- see [GAP-00X](#gap-00x) for the full review history." -->

## Open Decisions

`<A short, scannable list. If a Decision is resolved, say so in one line with its evidence link -- don't make the reader hunt for the resolution. If genuinely still open, say what's blocking it and who owns it. Only give a Decision its own full entry in the Evidence section below if there's enough nuance (a real conflict, a narrowed requirement) that one line here isn't enough.>`

- `<DEC-001>`: `<question>` -- **Resolved**, see [OBS-00X](#obs-00x). / **Open**, owner: `<role>`.

## Not built yet

`<A short, flat list of what's explicitly out of scope or deferred -- LLM/future paths named in the source but not built, anything a Business Owner explicitly deferred, technical questions handed to the Technical Agent. This is often the first thing a new team member needs, so keep it near the top of the document, not buried at the end.>`

- `<item>` -- `<why: deferred by direct decision, out of scope per the source, or a Technical Agent question>`.

---

## Capabilities

`<Only include this section if the capabilities genuinely need their own entry point distinct from the feature-area narrative above -- e.g. a capability spanning multiple feature areas, or one a Story will need to reference directly. Most features won't need this section at all; the feature-area headings above already are the capabilities, just named for a human instead of numbered. This section is reference material, like Evidence and Traceability below it -- not needed to understand the feature, needed as a stable entry point for the Business Requirements stage.>`

**Group by the Journey that proves each Capability is real -- never a flat ID-ordered list.** A Capability's realness comes from the Journey that needs it (`ARTIFACT-RELATIONSHIP-MODEL.md` section 3.1) -- so the section that lists Capabilities should show that relationship, not hide it behind a "used by" line a reader has to go looking for. One `###` subheading per Journey, its Capabilities underneath; a closing subsection for anything identified but not yet tied to a real Journey, stated honestly, not smoothed over. Each Capability entry links to its own full record (per the registry note above) -- that record already carries its own Evidence section, so don't repeat an `Evidence: [OBS-...]` clause here too. **Before dropping or omitting an Evidence clause on a Capability/Business Rule entry, rerun `verify_design_analysis.py` and confirm every `OBS-` it would have cited still has at least one inbound link from somewhere else in the document (typically a `BR-` Evidence line) -- otherwise that Observation becomes orphaned.**

### Serving Journey `<JRN-001>` -- `<journey name>`

`<One sentence: what this journey needs and why these capabilities serve it.>`

##### CAP-001
**`<name>`.** `<business purpose, one sentence>`. Registry: [CAPABILITY-REGISTRY.md](../registries/CAPABILITY-REGISTRY.md) / [full record](<link to the Capability's own file>).

<!-- Duplicate the "### Serving Journey ..." subheading for every Journey that has Capabilities, with its own Capabilities nested under it. -->

### Not yet tied to a Journey

`<Capabilities identified from the source, but no recorded Journey walks through them end to end yet. A real, honest gap -- not hidden, not force-fit into a Journey that doesn't actually need it.>`

##### CAP-00X
**`<name>`.** `<business purpose, one sentence>`. Registry: [CAPABILITY-REGISTRY.md](../registries/CAPABILITY-REGISTRY.md) / [full record](<link>).

## Evidence and Traceability

*Reference material. Each entry below is what an "Evidence" link above jumps to -- not needed to understand the feature, needed to audit a specific claim. Every entry ends with a "used by" link back to whatever cited it, so this section is navigable in both directions.*

##### OBS-001
`<What was observed, and where -- file, section, or a direct quote if the evidence is Human Provided.>` `<Classification>`, `<Confidence>`. *(↩ used by [BR-001](#br-001))*

<!-- Duplicate for every Observation. Give each Business Rule, Gap, Assumption, and Technical Unknown its own ID-only heading here too, in whichever grouping (Observations / Business Rules / Gaps / Assumptions / Technical Unknowns) it belongs to -- same pattern, same "used by" back-link. -->

##### GAP-001
`<Conflict or missing information. What sources conflict, or what's missing. State the resolution here if one exists -- who decided, and on what authority (e.g. a direct Business Owner clarification outranking the design document's own text) -- don't leave a reader to guess whether this was silently resolved.>` *(↩ used by [BR-00X](#br-00x))*

##### ASM-001
`<Provisional interpretation, and why it's not yet a confirmed requirement.>` Status: `Open` / `Confirmed` / `Rejected`.

##### TECH-001
`<Business behavior that's clear, paired with the technical question it raises -- for the Technical Agent stage, not a business decision here.>`

---

## Quality Checklist

- [ ] Exact source path, branch/commit, and version are recorded.
- [ ] The whole document -- not just "What this is" -- reads as a first-time target reader would read it: the narrative needs no evidence link, classification tag, or Gherkin block resolved to be understood. "What this is" itself has zero IDs.
- [ ] No commentary about this document's own revision history appears in its content -- format changes, prior drafts, review-round corrections belong in `DESIGN-ANALYSIS-SPEC.md` section 11's changelog, never repeated here. This is easy to reintroduce even while fixing it -- check explicitly.
- [ ] Every requirement has evidence, a classification, and a confidence level -- linked, not just named.
- [ ] Every Requirement/Capability/Business Rule links upstream to its source, and -- once they exist -- downstream to its Story/Epic; `Related Epic`/`Related Stories` in the metadata table are updated, not left `Pending` once known (`BUSINESS-AGENT-WORKFLOW.md` section 4.4).
- [ ] Acceptance criteria live with their requirement in `## Requirements`, not scattered in a separate section.
- [ ] The feature-area narrative contains no `##### BR-XXX` headings -- each exists exactly once, in `## Requirements`.
- [ ] Strong inferences are labeled `Strongly Implied`; human-supplied answers are labeled `Human Provided`, not `Explicit`.
- [ ] Every open Decision is visible near the top, resolved ones say how and on what evidence.
- [ ] "Not built yet" is present and honest -- nothing silently dropped.
- [ ] Technical implementation choices are excluded.
- [ ] Every ID-only heading in the Evidence section has at least one "used by" back-link, and every "Evidence:" link above resolves to a real heading below.
