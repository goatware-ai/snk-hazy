---
name: reviewer-recovery-bridge-and-coverage
description: "Reviewer lessons from task 23 june-price-review (2026-08-24): credits are refunds, never added into a recovered figure, the bridge must tie; rubrics need named-line and named-cell criteria across causes, and the correctly-billed remainder must name its ordinary class in cells with a tie row"
metadata:
  type: feedback
---

Reviewer send-back on task 23 june-price-review (2026-08-24), analysis otherwise reconciled:

1. A money summary that adds customer credits to corrected invoices and calls the sum
   "recovered" is wrong; a credit refunds money. Net recovery = corrected invoices minus
   credits, and the bridge shortfall - corrected + credits = absorbed must be shown and tie.
2. Rubric coverage: cause-total criteria (N lines short by X) do not verify any line's
   identity or expected price; the reviewer wants named-line criteria (invoice, item, level,
   billed vs should-bill vs short) across causes, and named-cell criteria on the corrections
   list, not just the count plus one worked example.
3. The remainder accounting ("the other 655 billed right") must name the ordinary class
   (466 plain matrix lines) alongside the special ones (pre-effective, sheet, quote) and put
   the counts in cells with a tie row.

**Why:** the reviewer reconciles the golden independently and reads the rubric for whether a
wrong-line or wrong-cell answer could still score full marks.
**How to apply:** at build time, write the bridge row and the billed-right block into the
summary, and spend 3 to 5 criteria on named lines and cells, each stating one figure unique on
its row. Keep the rubric inside R24's positive-at-39 cap by funding those rows at +1 from rows
whose substance another criterion forces ([[rubric-criterion-count]],
[[rubric-coverage-and-completeness]]); the line-level cluster itself is the REGISTER row shape.
