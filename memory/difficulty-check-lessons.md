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

**A reviewer's "please make this task harder" after a difficulty PASS (nutrition-panel-granola, 2026-09-29).**
The same one-line note landed on at least two tasks one second apart, so it reads as a bulk note. The
operator's direction was to keep the task and make it a little harder and bigger than the build, NOT to
re-run the creation workflow (a first attempt to open the creation docs was stopped). Shape that fit: a
basis column reduced to a status word with the weights in the specifications, a second per-serving
ingredient with its own specification, a claim verdict moved onto its threshold by a small formula change
(passes per reference amount, fails per serving, panel prints the ceiling), and the working sheet left on a
superseded revision with the rule doc saying the specification in force governs.

- 2026-09-29 (the same bulk note on concrete-acceptance-review, difficulty PASS on both models beforehand): rebuilt as 5 to 8 inputs and 22 to 27 rows, keeping the task. Shape that fit: the break record carries two measured diameters, loads and break times but no age or area (the solver computes both; the procedure's nominal areas and calendar-day ages are the look-alikes); a field log from two technicians' books, one on the 12 hour clock, with a delivery ticket keyed with two digits turned so two sets are one sample; a spec whose sampling rule is judged on the day's total of a mixture, whose age tolerance runs in hours, and whose set-aside needs the engineer's written direction (the contractor's void request is the arm that fails it, the engineer's letter the arm that holds); a July transmittal whose figure a later correction letter changes, so the carried-forward average decides a criterion (a) call; a memo whose expectations the records contradict in five places, each stated on the note tab. verify_golden.py lists 91 near flips settled by conventions the Parameters tab states. Session trap: the rebuild session hit its usage limit after the edits and before packaging, and the gate passed the folder at 0 errors beside the old zips (H10 since 2026-09-29, [[package-hygiene-pipeline]]).

- 2026-09-30 (the same bulk note on freight-invoice-audit, difficulty PASS on both models beforehand): kept the task and grew it from 38 to 46 freight bills. Shape that fit: a late-August pickup billed in September on the wrong week beside one billed right (the bulletin's August rows finally decide something), a redelivery confirmed in writing beside one refused (the schedule line with no BOL flag, both arms), a requested liftgate billed above the schedule rate (the 6.1 flat-rate clause), a pro number with two digits turned that only the shipment's own facts match to its bill of lading (a Pro Matches tab in the golden, a criterion worded by property because R107 rejects a record id past the 28-row window), and a bill on which the carrier applied the deficit rule correctly as the look-alike; the transmittal's self-describing lines ("No inspector is named", "No weighmaster signature") rewritten as a clerk's particulars. Pipeline: 46 rows push a CSV past the 25+15 preview, so both CSVs went into two side-by-side panels, the golden copies them block for block, and the duplicate test is one two-dimensional COUNTIFS (R16 rejects COUNTIF+COUNTIF and COUNTIF-COUNTIF; COUNTIFS with a "<>" criterion is one call).

- 2026-09-30 (the same bulk note on lien-analysis-larkspur, after a 2026-09-29 rebuild to twelve claims that two
  blind solves on Sonnet and Opus then cleared in full): kept the task and grew it from 12 to 15 claims, each new one a
  threshold arm of a rule already in play. Shape that fit: a supplier whose copy of the notice of completion went out
  one day late beside one on the last day and one never sent (section 8190, three arms); a supplier whose own
  statement of account shows a first delivery 21 days before its notice while the claim and the owner's log both recite
  the notice-form date (one day late, the first invoice falls out) beside one at exactly 20 days; a subcontractor
  served at the address on the building permit (holds) beside the one served on the direct contractor (fails); an
  unapproved change order request in a claim beside an approved change order in another, the approval read off the
  subcontractor list's CHANGE_ORDERS column; completion moved so the notice of completion sits on its fifteenth day;
  the September 25 "court holiday" label stripped, the close-out file stating only an all-day office closure and the
  practice note carrying CCP 12b; six approved change orders so the money held turns on the adjusted contract sum;
  surety line and held figure reset so both answers stay within about $3,000 of their thresholds. Pipeline: openpyxl
  overwrites wb.properties.modified at save (A3 fires when created is later), so the in-world stamp goes back at zip
  level before office_resave; G18 reads a bare two-word company name ("Ferguson Enterprises") as a person and a name
  carrying "Distributors" or "Supply" as a role, so fictional claimant names take a comma suffix and avoid those words;
  a struck literal "CED" matches inside "Procedure", so short struck forms go in as /\bCED\b/; a rubric figure on a
  cell storing a tenth is caught between R50 and R82, so the row grades the basis or is dropped in favour of its
  negative.

- 2026-09-30 (pretreatment-smr-q3-2026, operator direction "make this task more difficult and bigger" on top of the
  09-29 reviewer rebuild, which passed difficulty on 09-28 before the reviewer's bulk note): kept the task and added
  five look-alike arms of rules already in play, no new rule and no new deliverable. Shape that fit: a City grab at
  the outfall manhole beside the City composites (a metals grab is not collected as 2.1 requires; counted, it is the
  fifth result over the threshold at 33.3 percent, so the copper verdict turns on it); a totalizer register replaced
  mid-July with the new one at zero, every later register shifted and the day read against zero (a difference taken
  across the replacement is a five-million-gallon negative); a contained overflow pumped back to treatment beside the
  bypass; a test-kit reading at the outfall beside the clarifier weir grab (2.5's method arm and its point arm); a
  designation letter filed with another agency beside the filed-with-the-Coordinator arm. Rubric held at +39 by
  cutting figure rows the golden still states. Pipeline: openpyxl insert_rows does not move formulas, so a row goes
  in by translating each lower row down with openpyxl.formula.translate.Translator and widening every closed
  $5:$22 range by regex; a session that fails after saving its docx edits must restore them from the backup before
  the rerun (the build script asserts on the pre-edit text).

- 2026-09-30 (title-exam-cedarbrook-lot12, operator direction "make this task harder and more complex" on top of the
  09-29 reviewer rebuild, which had passed difficulty on 09-28 with FAIL x4 on both models): kept the task and added
  three arms of rules already in play, no new rule and no new file. Shape that fit: a 1999 mortgage older than twenty
  years with no enforcement action but a 2029 maturity (guideline 6.3's second test, which neither open mortgage had
  failed on) beside the 1994 one that meets all three tests; a 2010 certificate kept alive by three refilings each inside
  five years of the last, with a docket payment, in force on all three pieces of the land across the 2014 conveyance,
  beside a 2016 certificate never refiled that ran out in 2021 (the five-year rule's third arm) and the existing timely
  and late refilings; the amendment abstract reciting the renewal date so the golden's November 3, 2026 is input-carried
  (G20 had fired on the derived date). Rubric 57 rows at +107/-24; every "although" negative and "because" positive
  rewritten to one defect or one verdict with the record inside the predicate, ahead of the form's atomic check. Pipeline:
  restore docProps/core.xml at zip level after every python-docx or openpyxl save, before office_resave; a new sentence
  with a colon and three commas reads as four clauses to A20, split it first.

- 2026-09-30 (tract7-boundary-retracement, the same 2026-09-29 bulk note after a difficulty PASS on both models): the
  09-29 rebuild session had hit its limit with the inputs, golden, rubric and verify script rewritten but nothing packaged
  (zips from 09-21, no caches, clause map untouched, no log entry); this session read the rebuild against the inputs and
  finished it. Shape that fit: a notes file of 31 shots with a leg shot twice to the county's PK nail (0.28 foot, firm
  standard 1.1's disagreeing-pair arm beside a leg whose pairs agree), a tie recorded from the wrong station and two point
  numbers exchanged against their codes, prism constants and a taped offset only in the field book, an annexation that
  takes in the parcel after the field dates beside one already in force on the other side of the road, 1994 and 2008
  plat notes that class every mark (two original, three later, one of them past the 0.50 foot and set again on the
  adjoiner's line), the rotation line between two non-adjacent original monuments computed through the calls that join
  them with the call in error left out, and the 1978 deed of trust carrying the untransposed distance. Pipeline: the
  DMS bearing-text formulas nested 3600 (R89 fires on /3600 as an operand, not on MOD(x,3600)); R29 fires only on
  two-decimal figures, so gated "a formula rather than a keyed figure" clauses went on the rotation text, a count, a
  three-decimal acreage and a one-decimal deed perimeter total (which also answers R74 with "total ... is a formula");
  the record research's "parcels are Parcels" was A10 and its two-clause fix A20, recast as one clause with a "with"
  phrase; `echo =====` fails under zsh (equals expansion), quote it.

- 2026-09-30 (carton-bid-evaluation, operator direction "make this task harder and more complex" on top of the 09-29
  reviewer rebuild, not yet uploaded): kept the task and grew it from ten to eleven bids with three arms of rules already in
  play, no new rule and no new file. Shape that fit: a bidder that offers item 4 only as an alternate with no price on the
  item as specified, FOB origin from one plant (4.4 and 5.2 beside the alternate-alongside bid; 5.4's single-plant arm
  beside the two-plant one), lowest in the file if taken as a bid; the passed-over bidder's envelope logged at the due
  minute (3.1 "by 10:00" beside the 10:22 return); a telephone price change logged at 09:35 that 3.4's signed-writing rule
  excludes, and which hands the award to the caller if applied. The 09-29 session's generator (data.py, build_docs.py,
  build_xlsx.py, gen_golden.py) was recovered from its scratchpad and patched, so the package regenerates from one bidder
  list. Pipeline: office_resave rolls an unchanged docx back and leaves Word's ~$ owner file in inputs/, which breaks every
  zip-reading check and rides into the zip; delete it before zipping. R55 reads "Co." as a sentence end, so a bidder named
  "X Container Co." is written "X Container" in a criterion. form_payload.py is gone; sync_metadata.py embeds the
  instruction, file lists and rubric into metadata.json, and M7 fires when the rubric changes without a re-sync.
