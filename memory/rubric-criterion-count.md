---
name: rubric-criterion-count
description: "Rubric size and weight rules for Hazy: ERROR under 6 criteria, RECOMMEND under 20, NO ceiling (the form says 20-60+); any non-zero integer weight in -5..+5; the last row is the general formatting-and-style line; R24's single-loss cap on positive weight (inherited from Geranium, unverified here), one atomic sentence per row (R55/R54), weight-neutral splits (R27/R49/R85), never a checker's suggested weight, rebuild rather than patch a rubric that sat between rounds"
metadata:
  type: feedback
---

Open before sizing, splitting or reweighting a rubric. Detail on what the rows must cover is in
[[rubric-coverage-and-completeness]]; liveness rows in [[rubric-liveness-criteria]]; negatives in
[[rubric-negatives]]; wording in [[rubric-anchoring-and-landing]]. History of the older
positive-at-99 and positive-at-66 arithmetic is in docs/reference/reviewer-feedback-corpus.md
Part 5 (tasks 11, 18, 20, 34); those ceilings are superseded.

**Count (2026-09-21, the Hazy port).** There is no upper band. The form
(docs/submission/platform/platform-submission-form.md) asks for "a minimum of 3 criteria; expect
somewhere in the 20-60+ range depending on complexity", and checklist item 9 repeats the 3 with
"most real tasks need well more than 3". The guidelines PDF
(docs/submission/platform/create-the-task-guidelines.md) sets a higher floor twice, "at least six
criteria" / "The rubric has at least six clear criteria". So: **ERROR under 6** (the PDF floor,
which also clears the form's 3), **RECOMMEND under 20** (the bottom of the form's expected range),
**no ceiling**: a rubric past 60 is not a defect, because the form's own range is open-ended.
Geranium's 15-60 band and its aim-for-15-25 advice are dead and were deleted with
project-guidelines-v5.1.md; do not reinstate either from an old rubric.

**Weights (2026-09-21).** Any **non-zero integer in -5..+5**. The form states the range twice
("Weight -5 to +5", checklist item 11) with no gap around -1 and -2, so Geranium's split band
(+1..+5 positive, -3..-5 negative) is gone. Weight by how central the item is to a correct
deliverable, never by habit.

**The last row is the formatting-and-style line (2026-09-21).** The form: "End with a general
'Overall formatting and style of the deliverable' line (commonly ~+5)", and checklist item 12
makes confirming it a submit-blocking box. ERROR when it is absent; ERROR when it is present but
not last. It is a general polish row and is exempt from the anchoring rules that want a figure.

**The weight ceiling is R24 (since 2026-08-26, tessendorf; inherited from Geranium and
unverified for Hazy, since nothing confirms Hazy runs the full credit completeness check).**
The full credit completeness check quantifies hard-coding ONE liveness-anchored figure while the
other chain stays live, and its own addition drifts by a point, so EACH strict liveness criterion alone must cost more than 10%
of positive weight plus a one-point cushion. At the +5 platform cap that pins **positive weight
at 39 or under**; R24 errors when a hand-keyed workbook would retain 85% or more. The denominator
is the only lever: the checker's suggestions (raise the pair, add a third liveness row, add a
mirrored negative) are each closed (R17 caps formula-only rows at two, mirrors draw ambiguous
polarity 3/3).

**The shape that fits +39.** One +1 file row (R83); two +5 strict liveness read-throughs anchored
on two different requirements' own outputs; every other positive at +1, with +2 kept for
multi-step decisions; gated "the cell a formula rather than a keyed figure" clauses on value rows
tagged +LIVE until LIVE holds roughly half the positive weight (R73 needs over 15%). No coverage
cluster takes more than 12.5% plus a point (the completeness check), which affords about five to
seven clusters. The reference rubrics are delivery-zone-reset (+39/-8) and june-price-review run 11
(26 rows, +39/-8). At 20-plus rows the +1 default is what keeps positive inside the cap; the
formatting-and-style closer at ~+5 is funded from inside it, not on top of it.

**One simple atomic sentence per criterion (R55, 2026-08-24).** One sentence, one main verb,
one scorable claim, at most 45 words, positive or negative alike. A colon or semicolon
introducing a clause, a comma-and second predicate, a second sentence, and R54's second turns
(a trailing so/including clause, a parenthetical carrying figures, a three-parameter rule, a
value beside its own derivation) are all a second claim. Acceptance clauses that narrow the one
verdict stay legal ("with book quantity left as typed source data", "a cell reaching it through
a plain cell reference counts too"). The repair folds the second turn into a participial or
prepositional phrase or drops it; a split to a new row must stay weight-neutral. "G. Yeakel"
reads as two sentences to the counter; write "Yeakel".

**Splits are weight-neutral (R27/R49/R54/R85).** A reviewer's atomicity split divides the
parent's weight among its children (a +2 becomes two +1s), never adds rows and weight together,
which is the bloat loop that ran task 11 from 37 to 57 rows. R27 errors at four separate figures
in one positive (WARN at three); R49 counts subjects (two item codes or account numbers under
one predicate, a count beside a money total); R54 counts turns; R85 covers the carry-row shapes,
and a split carry row is re-funded to its old weight by cutting base-count rows. A liveness row
is narrowed, never split. A human reviewer's standard is stricter than the platform's ("each
criterion measures one single item", "criteria must not explain the rule or the calculation"),
and a like-item list under one measurement is one criterion until a reviewer calls it. When a
split has to be paid for, pay from rows the checks want gone (a duplicate figure row, a
section-presence row, a second instance of one rule, a total implied by its components), never
by re-bundling what the reviewer named. Rebuild to the budget and log the coverage dropped
rather than bundle back.

**Negatives (rewritten 2026-09-21).** R67's critical-only allowlist is DELETED. The Hazy form
says "Use negative weights where useful, to penalize specific unwanted outcomes", so a negative
may sit on any specific, observable unwanted outcome at any non-zero weight down to -5. There is
no minimum number of negatives. R61's 20 percent penalty share is NON-BLOCKING (team manager
ruling 2026-09-02, a recommendation printed through `recommend()`, never a send-back in either
direction). The shape rules that survive are in [[rubric-negatives]].

**Never copy a weight a checker suggests.** "Weight it 8-10 points" is rejected by the +5 ceiling
(R12); read it as "give this requirement its share" and fund it inside the cluster. An
adjudicator's "raise these nine rows to 4 or 5" would need positive near 62 and reopen the
single-loss FAIL the same platform issued on the same task: move what a freed point allows onto
the named rows and rebut with the cluster share (tessendorf 2026-09-10).

**A rubric that sat between rounds while the platform tightened gets the one-pass rebuild, not
a two-row fix.** Re-entering any criterion re-runs the platform's checks on the CURRENT rules
(june-price-review run 11 showed nineteen gate errors from checks coded after its last entry).
Keep proven rows verbatim, list every cut row in the feedback log, and void every
criterion-keyed `.gate-debt` line when renumbering, since debt keys on (criterion number, rule).
A rubric the platform has already passed to the reviewer is NOT re-entered for an optional
nicety; post-dated coded findings on it go into `.gate-debt` with the pass history.
Re-run the gate immediately before every form action, because the catalog moves daily.

- 2026-09-11 (stroebel refinement): the gate's R27 figure count includes four-digit tag or record ids (0157, 0193) and small integers (1, 2, 6), and a hyphenated suffix such as FR-100 is the only exempt form; a tag-heavy row therefore carries one tag id and one money figure at most, naming the second tag by its description.
- 2026-09-11 (rossville refinement round 4): the Rubric Quality Review's miscalibrated_weighting finding
  (six core requirements at 1 to 3 points, "raise to +5 with siblings and mirrored negatives") is the
  same arithmetic as the adjudicator's: answer inside 39 by moving points onto the named rows, adding
  figure-free coverage rows in the thinnest clusters (they also cut the rigid share), and paying with
  presence, implied-total and second-instance rows; re-run R73 (gated over 15%) and R13 (coverage
  cluster over 10%) after every move, since both tripped on the first cut.
- 2026-09-11 (weldon-bridge-plan refinement round 2, Rubric Quality Review needs_improvement): the review reads a core deliverable's share on its DIRECT rows only, counting strict and gated rows apart as "live-calculation", so eight +1 rows on the transition order (21%) drew miscalibrated_weighting [major] and 12 to 15 direct points of 39 is its bar; the two +5 strict rows on one order's unit count and dollar total drew redundant_or_double_counted, so the strict pair sits on two different deliverables' outputs (order total, reset count cell) from the start; an "each item ... N items" row is non_atomic, write the count row and separate spot checks. Funded at 39 by +2 on the decision rows, a policy spot check, and the completeness row cut to +2 with the count-cell strict row carrying R13 through "all ... rows ... 61".
- 2026-09-11 (coded, same day): the Quality Review's weighting read errors on a cluster of six or more direct rows all at +1 under a quarter of positive weight (the review's "token-underweighted" signature; 8 portfolio rubrics carry it, the looser under-25% form hit 24 and was not coded); R114 errors when two strict rows' figures sit on one total row of one sheet (landing-based). The "each item ... N items" bundle is NOT coded: it is the register-row shape the coverage checks mandate, so it stays a hand rule. prompts/submission.md and refine-task.md now state the shape.
- 2026-09-14 (harlow refinement round 10, Rubric Quality Review [major] miscalibrated_weighting): the row carrying a prompt's explicitly named identification ("the route furthest past the threshold called out plainly") at +2 of 45 drew "96 percent retained if wrong"; fund it to +3 or more inside the budget from the figure rows beneath it (the identified route's own ratio back to +1, a merged relation row to +3), never a mirrored negative. Not coded: verdict rows at +1 sit on accepted rubrics.
- 2026-09-14 (hx4180-fa26-spec-rev3 refinement round 2, adjudication, R129): the +39 two-strict shape is for prompts that demand live formulas; a prompt with no such demand is capped at a quarter of positive on formula rows, which two +5 strict rows always exceed (10 of 39 is 25.6%). The non-live shape is +33 or under with ONE +5 strict row and one or two gated +1 rows; fund the freed points nowhere, cut the denominator (drop the second read-through and an arithmetic detail row).
- 2026-09-15 (inbound-4582 refinement round 3, Rubric Quality Review [major] miscalibrated_weighting x2): a prompt-named side deliverable ("one sensitivity", "challenge one quantity") at +2 and +1 of 39 drew 95 and 97 percent retained; the review's own remedy was 3 or 4. Funded both to +3 inside 39 from rows whose figure other rows imply (a shipment total the per-SKU rows sum to, a shortfall equal to requested less released, a hold row the +4 decision and a negative also carry), keeping the register rows the coverage check needs. Check every prompt-named ask for a +1 or +2 sole row before submitting.
