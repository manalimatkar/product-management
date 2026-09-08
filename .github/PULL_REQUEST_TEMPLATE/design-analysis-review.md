<!--
Template for a standalone Design Analysis review PR (diff = a Design Analysis
file only, no Business Requirements/Epic/Story/Business PR yet -- per
BUSINESS-AGENT-WORKFLOW.md section 4.1's review pause).

Note on the table below: GitHub does not render "[ ]" inside a table cell as
a clickable checkbox (verified directly -- it stays literal text, unlike a
plain list item's "- [ ]"). Mark a row by editing its cell directly -- change
"[ ]" to "[x]" in whichever column applies -- the same way you'd edit any
other cell in this table. This is the standard model for every review PR
template in this repo going forward, not just this one.
-->

**Design Analysis:** `DA-<id>` -- `<path to the file>`

**Summary:** `<one or two sentences: what this analysis covers, and anything unusual about it>`

**Open Decisions needing your input, if any:** `<list Decision IDs, or "None">` -- leave inline comments on the specific rows in the "Files changed" tab to answer them; see the file's own section 12.

---

## Review Outcome

Mark exactly one column per row -- `[x]` in **Approved** or **Needs Changes**, not both:

| Requirement | Statement | Approved | Needs Changes |
| --- | --- | :---: | :---: |
| `BR-<id>` | `<short statement>` | [ ] | [ ] |

<!-- Duplicate the row above for every Business Requirement. -->

If any row is marked **Needs Changes**, also leave an inline comment on that requirement's section in "Files changed" explaining what needs to change.

## Notes

`<anything worth recording -- optional>`

---

- [ ] **Business Owner sign-off (ROLE-001):** I have reviewed this Design Analysis. If every row above is Approved, this is my acceptance of the whole analysis; if any are marked Needs Changes, this confirms I've recorded all the feedback I have for this pass.
