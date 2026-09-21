---
name: golden-coverage-and-recovery
description: "Golden and rubric design for a recovery or shortfall analysis (2026-08-24): credits are refunds and are never added into a recovered figure, the bridge must tie, the correctly-billed remainder names its ordinary class in cells with a tie row, and the rubric spends 3 to 5 criteria on named lines and named cells across causes rather than cause totals alone"
metadata:
  type: feedback
---

Open when a golden nets credits into a recovered figure, or when a rubric scores causes without
naming the lines and cells they rest on (2026-08-24).

1. A money summary that adds customer credits to corrected invoices and calls the sum
   "recovered" is wrong; a credit refunds money. Net recovery = corrected invoices minus
   credits, and the bridge shortfall - corrected + credits = absorbed must be shown and tie.
2. Rubric coverage: cause-total criteria (N lines short by X) do not verify any line's
   identity or expected price. Spend criteria on named lines (invoice, item, level, billed vs
   should-bill vs short) across causes, and on named cells of the corrections list, not just
   the count plus one worked example.
3. The remainder accounting ("the other 655 billed right") must name the ordinary class
   (466 plain matrix lines) alongside the special ones (pre-effective, sheet, quote) and put
   the counts in cells with a tie row.

**Why:** whoever checks the package reconciles the golden independently and reads the rubric for
whether a wrong-line or wrong-cell answer could still score full marks.

**How to apply:** at build time, write the bridge row and the billed-right block into the
summary, and spend 3 to 5 criteria on named lines and cells, each stating one figure unique on
its row. Keep the rubric inside R24's positive-at-39 cap by funding those rows at +1 from rows
whose substance another criterion forces ([[rubric-criterion-count]],
[[rubric-coverage-and-completeness]]); the line-level cluster itself is the REGISTER row shape.
