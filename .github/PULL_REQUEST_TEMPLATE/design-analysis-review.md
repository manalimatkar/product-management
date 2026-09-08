<!--
Template for a standalone Design Analysis review PR (diff = a Design Analysis
file only, no Business Requirements/Epic/Story/Business PR yet -- per
BUSINESS-AGENT-WORKFLOW.md section 4.1's review pause).

GitHub does not render a clickable checkbox inside a table cell -- verified
directly (POST /markdown: "[ ]" in a <td> stays literal text, never becomes
<input type="checkbox">). Only a plain list item ("- [ ]") renders as a real,
clickable checkbox. So this uses a table for the readable overview, paired
with a real checklist right under it -- one Approved/Needs Changes pair per
row, matching the table by ID. This is the standard model for every review
PR template in this repo going forward, not just this one.
-->

**Design Analysis:** `DA-<id>` -- `<path to the file>`

**Summary:** `<one or two sentences: what this analysis covers, and anything unusual about it>`

**Open Decisions needing your input, if any:** `<list Decision IDs, or "None">` -- leave inline comments on the specific rows in the "Files changed" tab to answer them; see the file's own section 12.

---

## Review Outcome

One row per Business Requirement this analysis produced:

| Requirement | Statement |
| --- | --- |
| `BR-<id>` | `<short statement>` |

<!-- Duplicate the row above for every Business Requirement. -->

For each requirement above, check exactly one -- same order as the table:

- [ ] `BR-<id>`: Approved
- [ ] `BR-<id>`: Needs Changes

<!-- Duplicate the checkbox pair above for every Business Requirement. -->

If any requirement is marked **Needs Changes**, also leave an inline comment on that requirement's section in "Files changed" explaining what needs to change.

## Notes

`<anything worth recording -- optional>`

---

- [ ] **Business Owner sign-off (ROLE-001):** I have reviewed this Design Analysis. If every requirement above is Approved, this is my acceptance of the whole analysis; if any are marked Needs Changes, this confirms I've recorded all the feedback I have for this pass.
