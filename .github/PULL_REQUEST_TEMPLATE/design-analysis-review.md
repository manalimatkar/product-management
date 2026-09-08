<!--
Template for a standalone Design Analysis review PR (diff = a Design Analysis
file only, no Business Requirements/Epic/Story/Business PR yet -- per
BUSINESS-AGENT-WORKFLOW.md section 4.1's review pause).

GitHub blocks a PR's author from submitting an "Approve" review on their own
PR -- confirmed directly (PR #1/#2). "Request changes" and "Comment" are NOT
blocked for the author, only "Approve" is -- so use GitHub's real Review
button for those two. Only "Approved" (and the two states GitHub's Review
button doesn't offer at all, "Rejected"/"Blocked") need the checkbox below.
-->

**Design Analysis:** `DA-<id>` -- `<path to the file>`

**Summary:** `<one or two sentences: what this analysis covers, and anything unusual about it>`

**Open Decisions needing your input, if any:** `<list Decision IDs, or "None">` -- leave inline comments on the specific rows in the "Files changed" tab to answer them; see the file's own section 12.

---

## Review Outcome

**If you want changes made:** use GitHub's own **Review changes** button (top right of the "Files changed" tab) -> **Request changes**, with your inline comments attached. That's a real, native GitHub review -- not blocked for the PR's own author, only "Approve" is.

**If you're approving, rejecting, or the analysis is blocked on something outside this PR:** GitHub won't let you submit a native "Approve" review on your own PR, so record it here instead -- check exactly one:

- [ ] **Approved**
- [ ] **Rejected**
- [ ] **Blocked** -- note the blocker below

## Notes

`<anything you want recorded against this decision -- optional>`

---

- [ ] **Business Owner sign-off (ROLE-001):** I have reviewed this Design Analysis and the outcome above is final.
