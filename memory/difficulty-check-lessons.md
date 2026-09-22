---
name: difficulty-check-lessons
description: "The desk's two difficulty_check FAILs (carton-bid-evaluation and freight-invoice-audit, 2026-09-22): what the platform measures (per-model PASS/FAIL attempts in the fetch JSON; two PASS of four, and ONE PASS of three valid, each fail the task), why each task was easy (every trap labelled in a tidy column; every exception a two-file mismatch a script reproduces), and the rebuild shapes that answered them (a candidate set with a decoy per trap, conditions in prose letters, a status column; a rule with a document or written-act condition exercised on both arms, a look-alike record that fails it, a bulletin the contract subordinates to its table)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 12ee6dd7-5e9b-4059-aab3-83e9dc851d57
  modified: 2026-09-22T08:24:19.654Z
---

Open on any "Hazy difficulty: FAIL" note, and before calling a new build hard enough.

**What the check is.** `evaluations[*].children_results[]` with `evaluator_name: difficulty_check`
carries `metadata.agent_result.models.<model>.attempts` (PASS / FAIL / INCOMPLETE per attempt),
`solved` and `valid_attempts`, then a `verdict`. On 2026-09-22 glm-5.2 went PASS, PASS, FAIL,
FAIL (`solved: true`) while qwen3.6-27b went INCOMPLETE four times (zero valid attempts), and the
verdict was FAIL, outcome NEEDS_REVISION. The visible note is one sentence; read the JSON. The
carried-over "80 percent worst-agent" rule in [[platform-expertdocs]] does not describe this.

**Why the task was easy (the root cause, not the symptom).** Four bids, five items, one
tabulation workbook. The tabulation carried an EXCEPTIONS_AND_ALTERNATES column that quoted the
exception with its ITB section and a PRICE_HOLD_STATED column restating it; the addendum flag was
"1" against "1, 2"; the discount floor, the freight rule and the extension rule were each stated
once and applied once. Nothing had to be reconciled between files, and no decision turned on a
column a solver skims. A model that reads the ITB and computes gets every figure.

**What fixed it, in the desk's own words from 01-ideation.md and 03-input-files.md.**
- *A candidate set to eliminate:* six bidders, each wrong one disqualified by a different
  property (an unacknowledged addendum and a superseded quantity; a six month price hold with an
  index in a cover letter; a full-truckload pricing condition in a cover letter that the
  addendum's Q&A makes a quantity exception; an open quality hold on the lowest responsive bid).
  Each missed trap changes the award to a different bidder, so the award figure, the margin and
  the approver all move together.
- *Conditions in prose, not in a labelled column:* the bidders' own bid forms and letters as a
  compiled docx, with the tabulation "as opened" recording only what the form boxes carry.
- *A step of the answer in a metadata column:* the item weights sheet lists drawing revision A
  (Superseded, addendum 2) and revision B (Current) for the amended item, so FOB origin freight
  moves; a hold register with a STATUS column, the bidder under its registered name variant
  ("Loken & Vik Container Corp." for "Loken & Vik Container"), a same-surname decoy also on Open,
  and the awardee's own hold Cleared.
- *A policy clause the first build never exercised:* PP-3.7 responsibility was already in the
  input; adding the register made it decide the award. Check every numbered rule in an input for
  one the golden never applies; that is free difficulty.

- 2026-09-22 (coded): L7 in leakage.py errors on an input column headed exceptions /
  deviations / qualifications / departures whose cell cites the section or policy number the
  record breaks (fires on the pre-fix tabulation, silent portfolio-wide, fixture
  labelled-exception-column); PR21 in procedural.py is the hand walk (every golden decision
  traced to the input fact it turns on; every numbered input rule applied somewhere). Cited in
  07-pre-submission-audit.md (`traps_not_labelled`), 01-ideation.md and prompts/submission.md.

**How to apply.** Before a build is called done, list each decision the golden makes and ask
where in the inputs a solver learns the fact it turns on; if the answer is "a column that names
the rule" or "the same sentence that states the rule", relocate the fact into prose, a second
file, or a status column. Two files that must agree on a name in two spellings beat one tidy
sheet. A difficulty revision is a rebuild of inputs and golden, never a rubric-only tightening;
the platform re-runs the models on the files.

**Second FAIL, same day (freight-invoice-audit, 2026-09-22).** glm-5.2 went PASS, FAIL, INCOMPLETE,
FAIL (`solved: true`, 3 valid attempts), qwen3.6-27b FAIL x4; verdict FAIL. So one PASS in three
valid attempts on one model fails the task: the bar is effectively no PASS on any model.

**Why it was easy.** A month of LTL freight bills rated against a contract: every one of the 13
exceptions was a difference between two tidy CSVs (a class, a weight, a base charge, a fuel
percentage, an accessorial, a duplicate pro) and a rule the contract stated once. A script that
rates each bill and compares reproduces the whole claim. The contract carried four arms the golden
never exercised: a reclass stands on a signed inspection certificate (4.3), a reweigh stands on a
certified scale ticket more than five percent over the declared weight (4.5), an accessorial is
billable when confirmed in writing before delivery (6.1), and the tariff table governs where the
bulletin disagrees (5.3).

**What fixed it.** Two new inputs and four invoice changes, no rubric-only tightening: a Northline
billing file transmittal (docx table, "Particulars as shown on the document") listing a signed
inspection certificate for one reclass and a system reclass notice with no inspector for the other,
a certified scale ticket 7.9 percent over the declared weight (the reweigh holds) and a certified
ticket 3.6 percent over (inside the tolerance, it reverts) beside an unsigned dock readout, plus
delivery-receipt decoys; a shipping desk email printout in which a liftgate and a reconsignment are
requested in writing before delivery (both due, the reconsignment being a schedule line with no BOL
flag) and a liftgate asked about after delivery is refused; the bulletin misprints one week's
percentage against the table. Each missed reconciliation moves the claim total (nine variants in
verify_golden.py, every one flips it). The golden reads the documents into a Billing File tab
(QUALIFIES / APPLIES_TO, the auditor's call typed beside the record) and a Confirmations tab, and the
Audit tab's contract weight, contract class and accessorials due are formulas over them.

**Coded (2026-09-22).** PR22 in procedural.py: a rule that turns on a document or a written act is
exercised on both arms with a look-alike that fails it. H1 now skips the fetched feedback-<uid8>.md
(fixture fetched-feedback-not-canary), which the first gate run of a revision otherwise trips on.
Also learned: a rubric figure on a cell storing a tenth (190.3) is caught between R50 (quote as
stored) and R82 (money to the cent); anchor the row on a cell storing two decimals instead.

