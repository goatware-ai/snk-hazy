---
name: difficulty-check-lessons
description: "The desk's three difficulty_check FAILs (carton-bid-evaluation and freight-invoice-audit, 2026-09-22; pretreatment-smr-q3-2026, 2026-09-28) and one INCOMPLETE that was a runner error, not a finding (title-exam-cedarbrook-lot12, 2026-09-28): what the platform measures (per-model PASS/FAIL attempts in the fetch JSON; two PASS of four, and ONE PASS of three valid, each fail the task), why each task was easy (every trap labelled in a tidy column; every exception a two-file mismatch a script reproduces), and the rebuild shapes that answered them (a candidate set with a decoy per trap, conditions in prose letters, a status column; a rule with a document or written-act condition exercised on both arms, a look-alike record that fails it, a bulletin the contract subordinates to its table; a lab flag unlabelled and the decisive record left unflagged, with the verdict figure on the threshold)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 12ee6dd7-5e9b-4059-aab3-83e9dc851d57
  modified: 2026-09-22T08:24:19.654Z
---

Open on any "Hazy difficulty: FAIL" or "Hazy difficulty: INCOMPLETE" note, and before calling a new build hard enough.

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


**Third FAIL (pretreatment-smr-q3-2026, fetched 2026-09-28).** glm-5.2 went PASS, FAIL, FAIL, INCOMPLETE
(`solved: true`, 3 valid), qwen3.6-27b FAIL x4; verdict FAIL. The offer had expired (expiry_time
2026-09-28T00:45Z, read at 05:08Z) with further_revision_requests_allowed true; the operator checks
whether the platform still takes the resubmission.

**Why it was easy.** A permit's computation rules stated once and applied once to a tidy lab table:
the lab's qualifier legend read "H = holding time exceeded, result not valid for compliance use" and the
chain-of-custody note "nickel result qualified H" (the Section 2.3 call typed beside the flag); the
plant manager's email confessed the missing Section 3.2 calls ("I have not been calling her"); the
daily flows were typed in the log with the 47,300 day annotated; the six-month copper share sat at
38.5 percent, far from the 33 threshold, so no misread moved the verdict.

**What fixed it (PR21 relocations, PR22 both arms, no rubric-only tightening).**
- The flag legend defines U, J, NS only; the lab log carries analysis dates and factual notes ("digestate
  lost ... re-digested and analyzed 08/06"), the holding periods in its footer, and the solver computes
  the days. The decisive instance is the one the lab never flagged at all: the July 7 sample's metals at
  30 days, which drops the copper denominator from 13 to 12 and moves the TRC share from 30.8 (clear) to
  33.3 (significant noncompliance), so the verdict Gordon does not expect turns on that one read. Both
  arms: a 27-day metals run and a 13-day cyanide run stand; a 34-day nickel and the 30-day metals fall.
- The Coordinator's telephone log ("your calls of September 10 and September 17") establishes the missing
  copper notices; the manager's email asks a question instead of confessing. The 09/17 excursion is called
  in at 15:20 and reported in writing (the Section 3.2 arm met), beside the overflow's late call.
- The log carries totalizer register readings, not daily flows; 47,300 exists only as a difference. A
  6.0 in-line low on 09/11 is the in-range look-alike for the 5.8 excursion (a -2 for listing it).
- Golden: validity is a formula over the chain-of-custody dates (DATE(VALUE(...)) serial helpers and
  _xlfn.DAYS, which R42 now reads as one call), Flow Sep differences the register, the note names the
  30.8-versus-33.3 hinge. Rubric 31 rows at +33/-9 (R129 non-live cap), the +5 strict row on "exactly 4".
- Coded: L8 in leakage.py (an input xlsx/csv cell stating a record's compliance disposition beside its
  flag), fixture labelled-disposition-legend; a permit docx stating the rule in the same words is out of
  scope by design.

**Pipeline traps this round.** openpyxl's save stamps dcterms:modified with today and office_resave
restores that stamp, so the in-world core.xml goes back at zip level before the resave; Excel writes DAYS
as _xlfn.DAYS and office_resave rolls the file back as changed content unless the prefix is written first
(the MAXIFS/MINIFS rule again); R42's pure-call regex had no room for the prefix (fixed).

**An INCOMPLETE verdict is a runner error, not a task finding (title-exam-cedarbrook-lot12, fetched
2026-09-28).** Note text "Agent Runner Error: An internal error occurred during agent execution. Hazy
difficulty: INCOMPLETE", outcome NEEDS_REVISION. JSON: glm-5.2 FAIL x4 (4 valid, `solved: false`);
qwen3.6-27b FAIL, INCOMPLETE, FAIL, FAIL (3 valid, `solved: null`); verdict INCOMPLETE. So the rule
set reads: a PASS anywhere fails the task; no PASS on four valid attempts is `solved: false`; no PASS
on FEWER than four valid attempts leaves `solved: null`, and a null with no model solved gives
INCOMPLETE rather than PASS. Zero of seven valid attempts passed, so the task was hard and nothing was
changed: gate 0 errors under the newer checks, zips byte-identical to the folder, resubmit unchanged,
offer already expired (same as the pretreatment round). `tools/fetch_feedback.py` now prints the
difficulty child per model and an EXPIRED header line, so the JSON dive is no longer needed.

**Same task, second return the same day (2026-09-28, after the rebuild above).** Resubmitted on the
rebuilt package: run one INCOMPLETE (glm FAIL x4, qwen one attempt lost), resubmitted unchanged, run two
FAIL (glm PASS, FAIL, FAIL, FAIL). One pass in eight valid glm attempts on a package with the trap
unlabelled. Two rubric reasons, both design reads with no detector:
- **The strict +5 row must anchor on a figure the central trap moves.** It anchored on the count above
  the threshold ("exactly 4"), identical whether or not the invalid sample is dropped; re-anchored on the
  measurement count ("exactly 12", a pure COUNTIFS).
- **Weight follows judgment, not arithmetic.** 24 of 33 positive points sat on figures a tidy read of the
  lab table gives; a solver that missed every judgment still cleared most of the weight. Cut the
  trap-independent figure rows, fund the judgment rows (+3 for the exclusion, +2 each for the frequency
  call and the two August findings).
- **Supply the file the prompt says is missing.** input_sufficiency failed the July and August logs'
  absence even though the prompt said "Luis's log is September only". Supplying them also turned the
  manager's attestation into a written claim the records contradict (PR22): 08/13 over the flow limit by
  register difference, 08/20 pH band high 9.2, with July look-alikes at 44,880 and 9.0.
- Pipeline: deleting a sheet leaves formulas pointing at it; Excel rewrites them to #REF! and office_resave
  rolls the file back as changed content, so grep every formula for the old sheet name first.

**Second INCOMPLETE-by-runner-error, same day (lien-analysis-larkspur, fetched 2026-09-28).** Same note
text, glm-5.2 FAIL x4 (solved false), qwen3.6-27b FAIL, FAIL, FAIL, INCOMPLETE (3 valid, solved null),
verdict INCOMPLETE; the difficulty child's `metadata.error` reads "CodeBuild build ended FAILED in phase
COMPLETED", which is the runner-side signature to look for. Zero of seven valid attempts passed; gate 0
errors, zips byte-identical, resubmit unchanged, offer still open (expires 2026-10-03). The
`rubric_checks` block's "Missing criteria: criteria_objectively_checkable, ..." string appears in every
fetch JSON with `feedback_outcome: PASS` and is a platform artifact, not a finding.
