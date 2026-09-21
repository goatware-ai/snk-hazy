---
name: review-optional-slot
description: The optional item in a review note opens "Optional:", never "Not blocking:", and only two kinds of thing may go in it
metadata:
  type: feedback
---

The optional last item in a review note opens **"Optional:"** on both Accept and Needs Revision.
"Not blocking:" is retired (operator, 2026-09-11), as is the older "Optional, not why this is
going back:". `tools/gcheck/review.py` bans both openers and `--lint-note` fails on them.

**Why:** "Not blocking" names what the item is *not*, so it still reads to the EC as a fault they
are expected to fix, which is the opposite of what the slot is for. The operator asked plainly:
if it is non-blocking, call it optional. It matters most on an Accept, where a flagged deficiency
muddies the verdict, and on a last round where `further_revision_requests_allowed` is false and
there is no attempt left to spend.

**The slot is narrower than our house convention suggested.** The platform's own
`docs/reviewer/platform/feedback-best-practices.md` has no non-blocking slot at all. Its optional
second paragraph allows exactly two things, "what you corrected yourself, so the EC can see it,
and at most one pattern to carry into the next submission. Nothing else." So an optional item
that is neither of those is **cut, not relabelled**. A pattern worth keeping is phrased as one
("keep the counterfactual figures in criterion 3 and the four like it, because ..."), not as a
deficiency that happens not to block.

**How to apply:** write the item as "Optional: ...", keep the anchor, and before writing it ask
which of the two permitted kinds it is. If it is neither, delete it and put the observation in the
chat report instead. Related: [[review-task-workflow]].
