# Claude Design Reading Specification

## 1. Purpose

This document defines how to read a **native Claude Design export** accurately -- which parts of it to trust, which to treat as reference only, and how to avoid the specific failure modes this repository has already hit once for real (`DA-003`'s first draft, built from README prose that a more literal source directly contradicted).

**This is a tool-specific document, deliberately separated from the generic methodology.** How to interpret *any* design source -- understand the end-to-end user flow first, then decompose into capabilities, requirements, and rules -- is the same regardless of which tool produced the source, and lives in [DESIGN-ANALYSIS-SPEC.md](DESIGN-ANALYSIS-SPEC.md) and [EVIDENCE-SPEC.md](EVIDENCE-SPEC.md) section 3.1. What differs per tool is *where the ground truth actually lives in that tool's specific output* -- that's what this document is for. A sibling document (e.g. a future `FIGMA-READING-SPEC.md`) would cover the same questions for a different tool's actual file shapes, without needing to restate the generic methodology -- each tool gets its own reading spec; the analysis method stays common.

## 2. Relationship to Other Artifacts

- [EVIDENCE-SPEC.md](EVIDENCE-SPEC.md) section 3.1 states the generic, tool-agnostic rules (read the most literal representation, cross-check a descriptive document against it, locate actual data not just logic, never trust an unverified verification technique). This document is that section's concrete application to one specific tool's output.
- [DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md](DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md) section 6.2 defines *where* a native Claude Design export is stored and its format (the `design` branch, folder shape, `_cover-sheet.md`, versioning, intake gates). That document is storage and format; this document is reading technique. Neither restates the other -- section 6.2's own Scope (section 3) explicitly excludes interpretation, which is what this document fills in.
- [DESIGN-ANALYSIS-SPEC.md](DESIGN-ANALYSIS-SPEC.md) Business Agent Activity 1 ("Understand the Design") points here for the concrete technique when the source is this tool's output.
- `.claude/agents/business-agent.md` reads this document as part of its standing instructions whenever the source is a native Claude Design export.

## 3. Scope

This specification covers only how to read the actual content of a native Claude Design export -- the `README.md`, `PARITY_RULE.md`, and `designs/*.dc.html` files described structurally in `DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md` section 6.2. It does not cover:

- the generic order of analysis (user flows before capabilities before requirements) -- see [DESIGN-ANALYSIS-SPEC.md](DESIGN-ANALYSIS-SPEC.md) section 4
- storage location, versioning, or intake gates -- see `DESIGN-HANDOFF-BUNDLE-FORMAT-SPEC.md` section 6.2
- evidence classification vocabulary -- see [EVIDENCE-SPEC.md](EVIDENCE-SPEC.md)

## 4. Reading Rules

These rules come from auditing what a real export actually contains in depth (four real versions of one export compared directly, `pdf-workflow/workflow-manager/design/`) and testing two candidate reading techniques against real content -- not assumed.

**The dark `designs/*.dc.html` file -- both its markup and its inline `<script type="text/x-dc" data-dc-script">` block -- is the sole source of truth for a screen's functionality.** That script is not a rendering afterthought; it is a real, complete class: actual state, actual methods (e.g. `toggleSection`, `moveField`, `confirmUnlink`), actual conditional logic, and exact copy text (confirmation-dialog wording, computed labels). Read it directly for every screen in scope. Within it, **explicitly locate and read the seed/mock data definition** (typically a constant such as `SEED` assigned to the initial state, e.g. `mappings: SEED`) -- this is where real field-level content actually lives (exact text, exact confidence values, exact source attribution per entry), separate from the methods that operate on it. Reading the methods without finding this data gives an incomplete picture even though the file was technically read in full.

**Never read, cite, or trust the light (`(Light).dc.html`) variant for behavior.** It is excluded from functional analysis entirely -- not ranked below the dark file, simply not used. Reason: the Claude Design agent producing these exports is not reliable about propagating a behavioral change to both theme variants even under explicit, repeated instruction (`PARITY_RULE.md` exists precisely because this does not happen automatically) -- so the light file's script cannot be assumed current, and there is currently no verified-accurate technique for checking it (see the rendering note below). This does not make theme support itself invisible to the analysis -- if light/dark mode is genuinely a product capability, that fact may still be recorded, sourced from `PARITY_RULE.md` or the README, never from reading the light file's own script.

**`README.md` is reference material, not an authoritative source.** It's genuinely useful for business framing, screen purpose, and naming -- but per `EVIDENCE-SPEC.md` section 3.1, every functional/behavioral claim it makes must be verified against the actual `.dc.html` before being recorded as `Explicit`. Where the README and the `.dc.html` disagree, the `.dc.html` wins outright; the README's claim gets downgraded or recorded as a Gap, not trusted at face value. This is not a close call between two comparably reliable sources -- the README has already been found, directly, to omit or misstate details the `.dc.html` gets right (see `CLAUDE.md`'s history of the retracted `DA-002`, built from a version where the README's own text briefly contradicted itself).

**Read the entire README, not only the feature's numbered subsection under "Screens."** Its structure is stable and predictable (confirmed identical section order across four real versions): Overview, About the design files, Fidelity, Screens, Known UX issues, **Interactions & behavior**, **State management**, Theming, Design tokens, Assets, Responsive behavior, Accessibility, then framework-conversion guidance, UI architecture, Files, and a suggested implementation order. The two bolded sections are flat and unlabeled -- they mix rules from every screen in the drop with no per-screen markers, so a rule relevant to the feature-slice being analyzed can appear there without ever naming that screen. The "Files" section, despite reading as bookkeeping, has been found to carry a real, otherwise-undocumented business rule as an aside -- read it in full, not just as a manifest to skim.

**Treat framework-conversion guidance as technical input, not business content.** The README's later sections (e.g. "Converting these designs to Angular," "UI architecture," "Suggested implementation order") are pre-supplied technical opinions the design tool volunteers unasked -- sometimes grounded in real, scanned facts about the actual target engineering repository (specific file paths, a real detected mismatch between the existing app's theme system and the new design's theme). Exclude all of it from the Design Analysis's business content (`DESIGN-ANALYSIS-SPEC.md`'s business/technical boundary, section 1) -- but do not silently drop it either. Record it as a Technical Unknown for the Technical Agent stage, preserved verbatim where it references real repository facts.

**A rendered screenshot of a `.dc.html` file is not currently a reliable verification technique for this format, and must not be used to override the source code.** Tested directly: a bare headless-Chrome screenshot of a real, content-populated screen rendered its data cells empty, twice, under different flags, with zero console errors -- while the same file's own source plainly contained the real seed data all along. The failure was in the rendering technique, not the source. Do not treat an empty or unexpected rendered element as evidence that content is missing from the design -- check the source's seed/mock data definition first, per the paragraph above. If a verified-accurate rendering or interaction technique (e.g. proper browser automation, independently confirmed against a known case per `EVIDENCE-SPEC.md` section 3.1 item 6) becomes available later, this note should be revisited -- until then, source-code reading is the sole method.

**Verify shared infrastructure is present; never analyze its content.** `designs/support.js`, `designs/image-slot.js` (when present), and `designs/_ds/<system>-<uuid>/{styles.css,_ds_bundle.js}` are identical across every screen in a drop and, confirmed across four real versions, stable across versions too (same design-system UUID every time). Their presence is a structural completeness check (already covered by `design_branch_gate.py`); their content is infrastructure, never a source of business evidence.

## 5. Open Decisions

- No sibling reading spec exists yet for any other tool (a bare Figma link, a written spec, or a future tool). When one is needed, it should follow this document's shape (Purpose / Relationship / Scope / Reading Rules), not be folded into this file -- keeps each tool's real, concrete quirks from accumulating into one unbounded document.

## 6. Revision History

| Date | Section | Change |
| --- | --- | --- |
| 2026-09-10 | 4 | This document created, closing gaps `DA-003`'s first draft had hit (see `CLAUDE.md`). |
