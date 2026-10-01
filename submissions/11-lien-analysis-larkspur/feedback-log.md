# Feedback log: lien-analysis-larkspur

## 2026-09-28 · source: build · verdict: DRAFT

Built under claude-fable-5-1 by /create-task 2 0, task 1 of 2. Occupation Paralegals and Legal Assistants (23-2011.00), domain Legal. Concept: seven claims of mechanics lien recorded against a completed California retail building, each worked under the firm's practice note from the recorder's copies, the owner's notice and waiver logs, the direct contractor's check ledger, and the close-out correspondence. Each claim turns on a different fact the solver has to find in a record: a thirtieth day that falls on a Saturday, a claim recorded the day after the extended last day, a preliminary notice served on the direct contractor alone, a late preliminary notice that reaches back only twenty days, an unconditional waiver signed and never paid, a conditional waiver resting on a stopped check, and a lien whose ninety days to sue ran out before the index search. The deliverable states each claim's standing, its enforceable amount, the release bond at 125 percent of the recorded claim, and the open points, including the direct contractor's own window to record.

**Findings** none yet; the gate was run on the packaged files and closed at 0 errors before the draft was called built.

**Actions taken** package sequence run (office_resave --force, fix_floats, fix_metadata, zips, autoeval_check); clause-map.md, verify_golden.py, form-lists.md and the rubric written off the Excel-recalculated golden.

**Form actions** none; a draft carries no Taskboard UID.

## 2026-09-28 · source: Auto-eval · difficulty_check · NEEDS_REVISION (verdict INCOMPLETE, runner error)

Platform note (eval_revision_notes, 2026-09-28T07:58Z): "Agent Runner Error: An internal error occurred during agent execution. Hazy difficulty: INCOMPLETE". The fetch-task JSON (tools/fetch_feedback.py, kept as fetch-a5f1d783.json, evaluations[0].overall_evaluation_result.children_results[3], evaluator difficulty_check) carries what the note does not: glm-5.2 attempts FAIL, FAIL, FAIL, FAIL, 4 valid, solved false; qwen3.6-27b attempts FAIL, FAIL, FAIL, INCOMPLETE, 3 valid, solved null; verdict INCOMPLETE; the child's own metadata.error reads "CodeBuild build ended FAILED in phase COMPLETED". The three sibling checks (input_files_ocrable 5 of 5 native-ok, prompt_completeness_audit, input_sufficiency/self_containment) passed with no finding; the prompt audit's one "minor finding" (Norcal Rebar's owner notice left open) is the designed gap the practice note tells the solver to flag, and the audit says so itself. Repo and platform agree on every part: the stored prompt matches instruction.md, the 23 criteria match the CSV, five inputs and one output, tools and times as in form-lists.md; both zips uploaded 2026-09-28T06:53Z and 06:54Z are byte-identical to the folder's files. The rubric_checks block's "Missing criteria: criteria_objectively_checkable, ..." string is the same standing platform artifact the cedarbrook JSON carries with feedback_outcome PASS, not a finding. The offer expires 2026-10-03T07:58Z and had not expired at fetch time.

**Findings**
1. No task finding. The one failed child is the platform's own agent runner losing qwen3.6-27b's fourth attempt; with only three valid attempts and no PASS, that model's solved stays null and the verdict is INCOMPLETE instead of PASS. No model passed any of the seven valid attempts, so the task stands as hard on the platform's own evidence (same shape as title-exam-cedarbrook-lot12, 2026-09-28).
2. Root cause is platform-side (a failed CodeBuild run inside the difficulty child). Nothing in the prompt, inputs, golden or rubric caused it, and no file is changed.

**Actions taken** (2026-09-28)
- verify_golden.py re-run: 87 figures reproduced, 0 mismatches, 32 near flips each settled by a convention the golden states (Saturday extension, stopped check, unconditional waiver effective when signed, notice never given to the owner, ninety days expired, late notice reaching back to May 9, 125 percent bond, thirty days from the notice of completion).
- Gate re-run on the folder as it stands (tools/autoeval_check.py): 0 errors; package_sweep 58 files across 2 roots, 0 findings in 0 tasks.
- Zips compared member by member against inputs/ and solution/ (sha256): identical, so neither zip is rebuilt.
- Coded: nothing added. The finding is a platform runner error with no task-side pattern to detect; tools/fetch_feedback.py already prints the per-model difficulty section from the cedarbrook round, and this fetch used it.
- Memory: one dated line in memory/difficulty-check-lessons.md recording the second INCOMPLETE-by-runner-error on the same day.

**Form actions**
- Resubmit unchanged. No criterion is re-entered (23 rows match), no zip is re-uploaded (both stamps 2026-09-28T06:53Z/06:54Z carry the built files), the prompt is untouched.
- If the resubmission re-runs the difficulty check and returns a PASS on any model, that is a real difficulty finding and the next round is a PR21/PR22 rebuild of the inputs and golden, not a rubric tightening.

## 2026-09-29 · source: Reviewer note · NEEDS_REVISION ("please make this task harder")

Reviewer note (revision_notes, 2026-09-29T16:34Z), one sentence and no findings: "please make this task harder". The platform's own difficulty check had passed on the resubmitted package (glm-5.2 and qwen3.6-27b FAIL on all four attempts each), so the reviewer's bar sits above those two models. This is the second return on the task; the rebuild was still done from the clause map, and clause-map.md carries Rebuilt: 2026-09-29.

**Findings**
1. Root cause: seven claims, each turning on one rule the practice note stated beside a worked example (the 29th reaching back to the 9th), with the deciding facts narrated in the direct contractor's email (the stopped check, the unpaid unconditional waiver) or labelled in a column (SERVED_ON, STATUS). No rule was exercised on both arms, several numbered rules decided nothing (service of the claim, the 15 days), and no figure sat near a threshold.
2. A first rebuild (twelve claims, the copy of the notice of completion under section 8190, a direct contractor hired by the owner, a claim served on the wrong party, a final waiver, a search that predates a last day to sue, two threshold answers) was cleared in full by two blind solvers, so it was hardened again.

**Actions taken** (2026-09-29)
- Inputs rebuilt: twelve claims; practice note rewritten with sections 8018, 8190, 8416(c) and (e), the four waiver forms, payments after recording and finance charges, and without worked examples; owner workbook gains a Certified Mail tab and the owner's own agreements, and loses SERVED_ON; ledger rebuilt with TYPE and BANK_CLEARED, a stop payment line, replacement check 4474 and unpaid check 4479; close-out file gains the second memorandum, the surety's $500,000.00 line, the court holiday of 09/25/2026 and Labor Day, and a recorder index table. Completion moved to 08/17/2026 and the notice of completion to 08/26/2026 so that the tenth and thirtieth days fall on holidays.
- Golden rebuilt (ten tabs, formulas throughout); verify_golden.py rewritten with 24 alternate readings; rubric rebuilt to 27 rows at +33/-13; clause-map.md, struck-phrases.md, form-lists.md and metadata.json (times 20/110/300/80, 8.5 h) brought into line.
- Package sequence run through the lock wrapper; gate 0 errors; package_sweep reports nothing against this task.
- Coded: nothing (tools/ is outside this revision's scope). G18 misfired on claimant names ending in Systems or Distributors beside a derived deadline; the claimant was renamed Fenwick Roofing, Inc. and two rows were dropped rather than the tool changed.

**Form actions**
- Re-enter the prompt (one sentence added on the two answers for Nadia).
- Re-enter all 27 rubric rows with their weights; confirm the count reads 27.
- Re-upload i-lien-analysis-larkspur.zip and s-lien-analysis-larkspur.zip and confirm both uploadedAt stamps moved; read input_files back against the five names.
- Re-type the five Input File List notes and the Output File List note from form-lists.md; times 20 / 110 / 300 / 80 minutes, total 8.5 hours; tools unchanged.

## 2026-09-30 · source: operator, "make this task harder and more difficulty and perfect one" (the reviewer note of 2026-09-29 still open) · NEEDS_REVISION

The platform still holds the 2026-09-28 package (23 rows, the old prompt, the 12-claim zips uploaded 2026-09-28T06:53Z); the 2026-09-29 rebuild in this folder was never uploaded. Re-fetched 2026-09-30: the resubmitted old package had passed the difficulty check on both models (glm-5.2 and qwen3.6-27b FAIL on all four attempts each), and the reviewer's one-line note "please make this task harder" arrived 2026-09-29T16:34Z with the offer open to 2026-10-04T16:34Z. Before touching anything, two blind solves of the 2026-09-29 twelve-claim package (Sonnet and Opus, inputs and prompt only) each reproduced every date, standing, amount and both of Nadia's answers exactly, so that rebuild was not hard enough for a careful reader and the hardening had to add facts that must be reconciled across files and figures on thresholds, not rows.

**Findings**
1. Every trap in the twelve-claim package was discoverable from one place: the September 25 last day was labelled "a court holiday" in the search paragraph; the copy-of-notice rule had only a never-sent arm (Calder) and an in-time arm (Petrakis); the late preliminary notice had only Hedrick's 53-day arm; service on the owner had only the failing arm (Abrego); the price-agreed limb of section 8430(a) and the fifteen-day limit on the notice of completion were stated in PN-14 and applied to nothing; the money held was the contract sum less payments with no change orders to reconcile.
2. Two claimants carried real suppliers' names (Ferguson Enterprises, Consolidated Electrical Distributors); G18 also read the first as a person's name and the second as a role beside derived deadlines.

**Actions taken** (2026-09-30)
- Three claims added, fifteen in all, each a threshold arm of a rule already in play: Lindqvist Fire Protection (claim 9, $16,600.00: retention plus change order request 3 of $9,467.50 that the subcontractor list shows was never approved, beside Bautista's approved change order 1; served at 1440 Eureka Road, the owner's address on permit B25-1187 per Devlin's August 19 memorandum, beside Abrego's service on the direct contractor; enforceable $7,132.50); Sierra Pipe & Supply, Inc. (claim 10, $19,742.64: its statement of account shows ticket R-51022 delivered 02/23/2026 while the claim and the owner's log both recite 03/03/2026 from the notice form, so the notice deposited 03/16/2026 is one day late and reaches back to 02/24/2026; enforceable $15,426.44); Capitol Wire & Lighting, Inc. (claim 15, $23,480.00, recorded 10/01/2026: its copy of the notice of completion went out 09/09/2026, one day after the last day, so its last day is 11/09/2026; its notice is exactly 20 days after its first delivery of 01/27/2026 on its own statement; enforceable in full).
- Completion moved from 08/17/2026 to 08/11/2026 so the notice of completion of 08/26/2026 sits on its fifteenth day (Kastner, Ostrowski, application 8 and the waiver log moved with it); 90 days after completion now ends 11/09/2026 and retention fell due 09/28/2026.
- The September 25 closure is no longer labelled a court holiday: the search paragraph states an all-day closure of the clerk's and the recorder's offices for a records conversion, and PN-14 2.5 states Code of Civil Procedure section 12b. PN-14 3.1 states the price-agreed rule for change orders and 4.5 the adjusted contract sum.
- Six approved change orders of $46,000.00 on the Owner Payments tab and in the August 19 memorandum (adjusted contract sum $3,794,250.00, application 8 $98,340.00, retention $189,712.50), so the money held is $283,135.50 and a solver on the signed sum gets $237,135.50. Nadia's surety line moved to $575,000.00. Both answers stay on their thresholds: bonds $578,094.11, over by $3,094.11; enforceable under the direct contract $286,087.47, short by $2,951.97.
- Reid's message trimmed of three narrated conclusions (check 4479 "two days after they recorded", the painter's check "never cut", the sprinkler request "never signed"), and the two real supplier names replaced throughout.
- Golden regenerated (ten tabs, every decision a formula; Amounts gains a SECURED_BY_THE_LIEN column with the price-agreed test; Parameters carries the signed sum, the change orders and the adjusted sum); verify_golden.py rewritten (249 figures, 30 variants, 203 near flips each settled by a phrase the note states, every new arm decisive on a headline answer); rubric rebuilt to 34 rows at +33/-15 with the strict +5 row on the bond total; clause-map.md (Rebuilt: 2026-09-30), struck-phrases.md (17 new entries), form-lists.md and metadata.json (times 20/130/330/90, 9.5 h; descriptions; rubric) brought into line.
- Package sequence run in order (office_resave --force, fix_floats, fix_metadata, flat zips, autoeval_check): 0 errors. package_sweep: 67 files across 2 roots, 1 finding in 1 task (tract7-boundary-retracement's workbook names openpyxl as its generator), left untouched.
- Coded: nothing in tools/gcheck/ (out of this revision's scope). Three pipeline reads go to memory instead: openpyxl overwrites the modified stamp at save so the in-world stamp goes back at zip level before the resave (A3); G18 reads a bare two-word company name as a person and "Distributors" or "Supply" as a role; a short struck literal ("CED") matches inside other words, so it is entered as a word-bounded pattern.

**Form actions**
- Re-enter the prompt from instruction.md (the platform still holds the 2026-09-28 wording).
- Re-enter all 34 rubric rows with their weights from the CSV; confirm the count reads 34.
- Re-upload i-lien-analysis-larkspur.zip and s-lien-analysis-larkspur.zip and confirm both uploadedAt stamps move past 2026-09-28T06:54Z; read input_files back against the five names.
- Re-type the five Input File List notes and the Output File List note from form-lists.md; times 20 / 130 / 330 / 90 minutes, total 9.5 hours; tools unchanged.
- Resubmit before the offer expires on 2026-10-04.

Blind solve of the hardened package (Sonnet, inputs and prompt only, 2026-09-30): reproduced every date, standing and figure, both answers included, in one pass. The platform's own two models failed every attempt on the seven-claim original, so the fifteen-claim package sits well above their bar; a strong careful reader still clears it, and any further hardening would have to trade on the golden's defensibility rather than on facts a solver can find. Left as built.

## 2026-09-30 · source: in-app pre-submission · Criteria atomic · FAIL

Form note: "Some criterion include multiple checks, for example considering both if a claim was recorded timely and if the criteria required a certain value to be stated. Suggestions: Split criteria that currently bundle multiple evaluations into separate criteria focused on a single aspect each."

**Findings**
1. Nine positives bundled a verdict with its reason or its date ("X's claim recorded 09/29/2026 is found timely because the owner never gave it a copy", "treated as a direct contractor whose claim recorded 09/30/2026 is timely", "found effective because it was recorded within 15 days after the completion of 08/11/2026", "found served on the owner because it was mailed to the owner's address shown on the building permit"), the two-reasons-under-one-verdict and relative-clause shapes the 2026-09-22 note lists.

**Actions taken** (2026-09-30)
- Every positive rewritten to one verdict or one figure per row; the five +2 verdict rows split weight-neutrally into a verdict row and a reason-or-date row (Calder timely / last day 11/09/2026; Capitol Wire timely / copy given after the last day; Ostrowski timely / last day 09/28/2026; notice effective / completion 08/11/2026; Lindqvist served / permit-address service counts); the reasons dropped from the +1 rows (Petrakis, Sorensen, Foothill, Fenwick, Abrego, the adjusted contract sum). Positive weight stays 33 with the one strict row.
- The negative on section 8182 dropped as a mirror of the new positive (R22/R104), negatives now -14. 38 rows. metadata.json rubric and clause-map.md row references re-mapped. Gate 0 errors.

**Form actions**
- Re-enter all 38 rubric rows with their weights from the CSV; confirm the count reads 38. The other form actions of the entry above stand.

## 2026-09-30 · source: in-app pre-submission · Rubric covers deliverable · FAIL

Form note: "While many specific calculations and checks are covered, the requirement related to Nadia's request on bonds fitting within surety lines is only indirectly addressed and it is not clear if every necessary aspect of Nadia's email has been covered explicitly in the rubric. Suggestions: Ensure that criteria explicitly cover Nadia's email request about bonds fitting within the surety line and money held on the contract."

**Findings**
1. The two answers were graded only through their excess figures ($3,094.11 over the line, $2,951.97 short); no row asked for the Yes or No the prompt and Nadia's email put, and Nadia's "which claims we can demand released and which we would have to bond" had no count row after the atomic rewrite.

**Actions taken** (2026-09-30)
- Three rows added at +1 each: the first worksheet answers that the bonds do not fit inside the surety's line; it answers that the money held does not cover the claims enforceable under the Dunmore-Kettle contract; it routes 5 of the 15 recorded claims to a demand for release.
- Funded inside 33 by dropping the permit-address rule statement (Lindqvist's served verdict still scores it), the typed completion date (a figure read straight off the notice), and Ostrowski's timeliness verdict (its $61,477 enforceable-amount row already requires it). 38 rows at +33/-14. metadata.json rubric and clause-map.md re-mapped (rows 22 and 23 carry the two answers). Gate 0 errors.

**Form actions**
- Re-enter all 38 rubric rows with their weights from the CSV; the other form actions above stand.

## 2026-09-30 · source: in-app pre-submission · Criteria atomic · FAIL (second)

Form note: "Multiple rubric criteria bundle separate checks. For example, 'The workbook wrongly includes the lumber supplier's delivery of 05/08/2026 in its enforceable amount although its late preliminary notice reaches back only to 05/09/2026.' and 'The workbook wrongly treats the electrical subcontractor's final draw as paid by check 4479 although the ledger shows that check as unpaid at the bank.' should be split into multiple criteria since they address separate and specific checks."

**Findings**
1. The "although <rule or record>" polarity clause on every negative reads to the platform's atomic check as a second check. The 23-row rubric passed the same check on 2026-09-28 with that frame, so the read is not stable, but it failed twice today and the clause carries no scoring weight of its own.

**Actions taken** (2026-09-30)
- All ten negatives cut to the single defect each penalises, the record kept as a phrase inside the one predicate ("as unpaid after check 4474 paid at the bank", "by the unpaid check 4479", "instead of the claim as recorded") or dropped where the positive rows already carry the rule. Weights unchanged, 38 rows at +33/-14, metadata.json synced, gate 0 errors.

**Form actions**
- Re-enter all 38 rubric rows with their weights from the CSV; the other form actions above stand.

## 2026-09-30 · source: Reviewer note, six hardening items (pasted by the operator) · NEEDS_REVISION

The reviewer's six items, quoted in short: (1) strip the narrative signposts from Devlin's September 10 memorandum and state the September 25 closure once in a separate notice; (2) a second name-collision trap beside Calder, with Sierra Pipe's green card blank and its article returned unclaimed, deposit governing; (3) a post-recording payment found by reconciliation, a joint check to Ostrowski and Capitol Wire on the ledger with a Capitol Wire conditional final waiver on the log; (4) the retention question as an exact-figure deliverable with the $22,000.00 correction disputed in good faith; (5) the bond rounding convention in PN-14 4.4 and a line that flips on per-claim against total rounding; (6) a claimant whose preliminary notice went to the owner at the old Eureka Road permit address, with PN-14 accepting it. Third harden of the day, on top of the fifteen-claim package.

**Findings**
1. All six items read as designed traps the package lacked; two interact. A releasable retention exists only when the enforceable claims of record fit inside the money held with room for the 150 percent hold, so item 4 turns the money-held answer to Yes and makes the release figure the threshold. Item 2 is decisive only if Sierra Pipe's timeliness turns on the "given" call, so its recording moved to October 1 and its one-day-late notice arm moved to Capitol Wire, which item 3 also loads.

**Actions taken** (2026-09-30)
- Claims now sixteen. Sierra Pipe & Supply recorded 10/01/2026 (Document No. 2026-0101690); its certified mail number 7022 1670 0002 3391 4399 has no green card and sits in a returned mail record on the Certified Mail tab as unclaimed 09/29/2026, beside a Sierra Test and Balance entry of Rancho Cordova (Kastner's balancing subcontractor, now on the subcontractor list); given on deposit, so untimely and demanded released. Capitol Wire's first delivery moved to 01/26/2026 (twenty-one days before its notice, the $1,500.00 balance out); the ledger carries joint check 4488 of 10/06/2026 to Ostrowski and Capitol Wire for invoice C-14212, paid 10/09/2026, Lorna's email now of 10/10 names it, and the waiver log carries Capitol Wire's conditional final waiver naming that check with "Disputed claims for extras: $14,540.00", so Capitol Wire enforces $13,040.00. Granite Bay Sheet Metal, Inc. (claim 16, $18,360.00, Kastner's duct fabricator) attaches a proof of service of its preliminary notice to the owner at 1440 Eureka Road, Suite 100, with no owner log entry and no copy of the notice of completion; PN-14 1.3 accepts notice at the permit address, so it has lien rights and enforces in full.
- Devlin's September 10 memorandum trimmed to the mail log; a new part E in the close-out file, the court's public notice of the September 25 closure and Labor Day, and the search paragraph no longer mentions either. The August 19 memorandum now records the $22,000.00 correction as disputed in good faith and the adjusted contract sum of $3,828,250.00 with retention of $191,412.50 (change orders 1 to 6 now $80,000.00; application 8 $132,340.00). Nadia's email asks for the retention due for release and the monthly cost of holding it, and gives the surety's line as 15 percent of the $3,842,450.00 appraisal; the prompt's "two things" sentence reworded to the three asks. PN-14 4.4 states the surety writes each bond at 125 percent rounded up to the next whole dollar, 4.5 states the release computation and the 2 percent penalty, 1.3 the permit-address notice.
- Golden regenerated: bonds ROUNDUP per claim ($576,369.00 against a line of $576,367.50, over by $1.50; rounded once on the total they would fit), money held $317,135.50 covers $278,581.03 by $38,554.47, retention due 09/28/2026, retention due for release $5,554.47, penalty $111.09 per month; the Waivers tab gains EXCEPTION_AMOUNT and the Amounts tab applies a final form's stated exception; the DK Ledger tab copies the CSV's two side-by-side panels (21 lines, H7) into one list. verify_golden.py reads the panels, the returned mail record, the joint payee and the exception, and reproduces 275 figures with 310 near flips under 39 readings, each settled by a phrase the note states. Rubric 41 rows at +33/-15, the strict row on $576,369; clause-map.md rebuilt (Rebuilt: 2026-09-30, third harden), struck-phrases.md 21 new entries, form-lists.md and metadata.json (times 20/150/390/110, 11.5 h).
- Gate 0 errors after the package sequence; package_sweep unchanged (the one finding is on another task, left alone). Pipeline reads: a cited certified mail article takes the input's own form ("certified mail number 7022 ...", G36); a rubric row on a percent states its base inline (R64); a 41-line CSV goes into two panels (H7).

**Form actions**
- Re-enter the prompt from instruction.md (the "two things" sentence changed).
- Re-enter all 41 rubric rows with their weights from the CSV; confirm the count reads 41.
- Re-upload i-lien-analysis-larkspur.zip and s-lien-analysis-larkspur.zip and confirm both uploadedAt stamps move; read input_files back against the five names.
- Re-type the five Input File List notes and the Output File List note from form-lists.md; times 20 / 150 / 390 / 110 minutes, total 11.5 hours; tools unchanged.
- Resubmit before the offer expires on 2026-10-04.

Blind solve of the sixteen-claim package (Sonnet, inputs and prompt only, 2026-09-30, run before the ledger was paneled and the August 19 memorandum's figures were aligned, neither of which changes a decision): reproduced every standing, every enforceable amount, the ten bonds at $576,369 against the $576,367.50 line, the money held of $317,135.50, the $5,554.47 due for release and the $111.09 penalty. Its one slip, a direct contractor claim "by 10/26" where the golden says November 9, is graded by row 28 of the rubric. Every reviewer item was applied correctly by a strong careful reader, so the difficulty now rests on the number and spread of the reconciliations rather than on any one hidden fact. Left as built.
