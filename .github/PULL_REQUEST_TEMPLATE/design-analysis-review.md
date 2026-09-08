<!--
Template for a standalone Design Analysis review PR (diff = a Design Analysis
file only, no Business Requirements/Epic/Story/Business PR yet -- per
BUSINESS-AGENT-WORKFLOW.md section 4.1's review pause).

Note: GitHub's own Review button (Approve / Request changes / Comment) can't
be used on these PRs -- GitHub never lets a PR's author approve their own PR,
and every PR in this repo is opened under the same account. The checkbox
below is the actual mechanism; it's read and applied into the Design
Analysis's own section 19 by hand (or by a future automation, not built yet).
-->

**Design Analysis:** `DA-<id>` -- `<path to the file>`

**Summary:** `<one or two sentences: what this analysis covers, and anything unusual about it>`

**Open Decisions needing your input, if any:** `<list Decision IDs, or "None">` -- leave inline comments on the specific rows in the "Files changed" tab to answer them; see the file's own section 12.

---

## Review Outcome

Check exactly one:

- [ ] **Approved**
- [ ] **Changes Requested** -- leave inline comments on what needs to change
- [ ] **Rejected**
- [ ] **Blocked** -- note the blocker below

## Notes

`<anything you want recorded against this decision -- optional>`

---

- [ ] **Business Owner sign-off (ROLE-001):** I have reviewed this Design Analysis and the outcome above is final.
