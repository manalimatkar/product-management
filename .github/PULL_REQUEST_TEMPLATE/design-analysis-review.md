<!--
Template for a standalone Design Analysis review PR (diff = a Design Analysis
file only, no Business Requirements/Epic/Story/Business PR yet -- per
BUSINESS-AGENT-WORKFLOW.md section 4.1's review pause).

Review Outcome below is a plain task list -- one real, clickable checkbox per
requirement, text right next to it. (GitHub can't render a clickable checkbox
inside a table cell -- verified directly, twice -- so this deliberately
isn't a table.) This is the standard model for every review PR template in
this repo going forward, not just this one.
-->

**Design Analysis:** `DA-<id>` -- `<path to the file>`

**Summary:** `<one or two sentences: what this analysis covers, and anything unusual about it>`

**Open Decisions needing your input, if any:** `<list Decision IDs, or "None">` -- leave inline comments on the specific rows in the "Files changed" tab to answer them; see the file's own section 12.

---

## Review Outcome

Check off each requirement once approved. Leave one unchecked -- and leave an inline comment on that requirement's section in "Files changed" explaining what needs to change -- for anything that needs changes.

- [ ] `BR-<id>`: `<short statement>`

<!-- Duplicate the line above for every Business Requirement. -->

## Notes

`<anything worth recording -- optional>`

---

- [ ] **Business Owner sign-off (ROLE-001):** I have reviewed this Design Analysis. If every requirement above is checked, this is my acceptance of the whole analysis; if any are left unchecked, this confirms I've recorded all the feedback I have for this pass.
