# Feedback log: title-exam-cedarbrook-lot12

## 2026-09-21 · source: build · verdict: DRAFT

Built under claude-fable-5-1 by /create-task 2 0, task 1 of 2. Occupation Title Examiners, Abstractors, and Searchers (23-2093.00), domain Legal. Concept: a title examination report for a residential closing in Licking County, Ohio, where the chain carries a deed that describes less land than the grantor held, an unreleased mortgage, a dower defect, a name variance, a judgment lien on the seller, a judgment on a similar name that does not attach, delinquent taxes with penalty, and a tax proration to the closing date.

**Findings** none yet; the gate was run on the packaged files and closed at 0 errors before the draft was called built.

**Actions taken** package sequence run (office_resave --force, fix_floats, fix_metadata, zips, autoeval_check); clause-map.md, verify_golden.py, form-lists.md and the rubric written off the resaved golden.

**Form actions** none; a draft carries no Taskboard UID.

## 2026-09-28 · source: Auto-eval · difficulty_check · NEEDS_REVISION (verdict INCOMPLETE, runner error)

Platform note (eval_revision_notes, 2026-09-23T00:52Z): "Agent Runner Error: An internal error occurred during agent execution. Hazy difficulty: INCOMPLETE". The fetch-task JSON (tools/fetch_feedback.py, evaluations[0].overall_evaluation_result.children_results[3], evaluator difficulty_check, kept as fetch-b34c9335.json) carries what the note does not: glm-5.2 attempts FAIL, FAIL, FAIL, FAIL, 4 valid, solved false; qwen3.6-27b attempts FAIL, INCOMPLETE, FAIL, FAIL, 3 valid, solved null; verdict INCOMPLETE. The three sibling checks (input_files_ocrable, prompt_completeness_audit, self_containment) passed with no finding. Repo and platform agreed on every part: the stored prompt matched instruction.md, the 27 criteria matched the CSV, four inputs and one output, tools and times as in form-lists.md; both zips uploaded 2026-09-21T22:27Z are byte-identical to the folder's files. The offer's expiry_time (2026-09-28T00:52:54Z) had passed when the feedback was fetched (05:43Z) with further_revision_requests_allowed true.

**Findings**
1. No task finding. The one failed child is the platform's own agent runner erroring on qwen3.6-27b's second attempt; with only three valid attempts and no PASS, that model's solved stays null and the verdict is INCOMPLETE instead of PASS. No model passed any of the seven valid attempts, so the task stands as hard on the platform's own evidence.
2. Root cause is platform-side (a 500 from the runner, as the sibling input_sufficiency child also logged one InternalServerError on its first request before succeeding on its second). Nothing in the prompt, inputs, golden or rubric caused it, and no file is changed.

**Actions taken** (2026-09-28)
- Gate re-run on the folder as it stands under the checks coded after the 2026-09-21 build (L8, PR21, PR22, the H1 feedback-file skip): 0 errors; G43 reproduced 14 figures with 6 near flips each settled by a stated convention; package_sweep clean, 0 findings in 0 tasks.
- Zips compared member by member against inputs/ and solution/: identical, so neither zip is rebuilt.
- Coded: tools/fetch_feedback.py now prints a "Difficulty check" section (per-model attempts, valid attempts, solved, verdict, runner errors) and an EXPIRED header line when expiry_time has passed at fetch time; tools/README.md updated. No tools/gcheck/ check is added because the finding is a platform runner error with no task-side pattern to detect.
- Memory: one dated line in memory/difficulty-check-lessons.md on the INCOMPLETE verdict semantics.

**Form actions**
- Resubmit unchanged. No criterion is re-entered (27 rows match), no zip is re-uploaded (both stamps 2026-09-21T22:27Z carry the built files), the prompt is untouched.
- The offer had expired before this revision; confirm the platform still takes the resubmission under further_revision_requests_allowed. If it re-opens as a fresh submission, the same package goes up and the new UID goes into metadata.json.

## 2026-09-29 · source: Reviewer note · NEEDS_REVISION

Reviewer revision note (2026-09-29T16:34Z), in full: "please make this task harder". No other finding. The platform's own difficulty check on the latest run had passed (glm-5.2 FAIL x4, qwen3.6-27b FAIL x4), so the reviewer's bar sits above those two models. Read from feedback-b34c9335.md as fetched; no fetch and no stb command was run in this revision.

**Findings**
1. Root cause of the easy read: the searcher's abstracts narrated every defect ("The deed carries no reference to Lot 13", "did not sign the deed", "No satisfaction ... was found of record", "no affidavit of identity is of record"), the Names tab gave each owner's holding period so lien attachment was a lookup, the index legal column showed the omitted land as a tidy column difference, and each guideline was stated once and applied once on one arm. Seven requirements, one judgment payoff, one tax line.
2. Guidelines 6.3 (insure-over) and 10.5 were exercised on one arm only, and the 5% penalty rule in the treasurer's note decided nothing.

**Actions taken** (2026-09-29, a rebuild of inputs and golden, not a rubric tightening)
- Inputs rebuilt, six files in place of four. Abstracts give parties, recitals, description and execution as on the instrument, with no conclusion. The 2014 deed describes the north 24.25 feet of Lot 13 where every other instrument describes 42.25 feet, the index keys all of them alike, and an 18.00-foot strip stays of record in Daniel R. Pruitt. New court_records_search_hlt262214.xlsx (probate and domestic relations index runs) and location_survey_418_cedarbrook.docx (the buyers' survey, ties only).
- Both arms (PR22): a satisfaction signed by the assignor after its assignment against one signed by the assignee; a mortgage seventeen days short of twenty years against one that meets all three insure-over tests; a certificate refiled inside five years against one refiled fourteen days late; a decree of dissolution against a dismissed case and a pending case; a namesake (Daniel Robert Pruitt) on the largest certificate and on the 2019 marriage license against the owner (Daniel Ray Pruitt); Peggy A. Kessler as a second wife against the nickname guideline, with Margaret Ann Kessler's death in the probate index; a tax installment paid six days late against one unpaid; the dwelling's main wall clear of the building line against its roofed porch over it.
- Chain: the strip decides the corrective deed, which Pruitt is the owner, which certificate attaches, and where the garage and driveway stand on the survey.
- Requester beliefs the record contradicts: one loan, one missed bill, a deed signed by the seller alone.
- Golden rebuilt: fourteen requirements, a people-in-the-chain table, a docket table with reasons, specific survey exceptions, three judgment payoffs ($7,809.53, $8,543.78, $4,724.26), taxes $2,424.91, proration $3,050.94, total of record $23,502.48. Report date moved to October 21, 2026 with the prompt's due date.
- Rubric rebuilt at 49 rows, +92 / -18. The 27 earlier rows are replaced; rows kept in substance are the file row, the Muskingum Valley payoff, the two Schedule B instrument exceptions, the chain table, the loan policy mortgage, the mechanics lien, invented payoff and assessment proration negatives, and the closing style row. Dropped: the affidavit of identity row (now a negative), the $10,556.19 and $2,319.48-only figures, the search period row.
- verify_golden.py rewritten: 47 figures and standings re-derived from inputs/, 20 missed-read variants, each moving a graded result. clause-map.md rebuilt and dated, struck-phrases.md created, form-lists.md and metadata.json resynced (six inputs, times 20 / 170 / 340 / 80 minutes, 10.25 hours).
- Blind solves, solver given the prompt and inputs only: two on the first rebuild and two on the second (one Fable, one Opus each) cleared nearly every row, which is why the namesake, second-wife, late-payment and survey layers were added; the runs on the final inputs are in the revision report. A frontier model still clears most of the weight; the misses seen were the garage standing on the strip and the first-half penalty left as a question.
- Package sequence run in order on the final files; gate TOTAL: 0 errors.
- Coded check: none added in this revision (tools/ is outside its scope). Suggested for the tooling owner: a check that an input abstract or note does not state the absence of an instrument the golden makes a requirement of ("no satisfaction was found", "did not sign").

**Form actions**
- Prompt: replace with instruction.md (new file names, due date October 21).
- Input File List: six entries from form-lists.md; input zip: re-upload i-title-exam-cedarbrook-lot12.zip and confirm uploadedAt moved; remove any earlier input upload the widget still holds.
- Output File List unchanged in name; solution zip: re-upload s-title-exam-cedarbrook-lot12.zip and confirm uploadedAt moved.
- Rubric: delete the 27 rows and enter the 49 rows of the CSV with their weights; confirm the count reads 49.
- Times: 20 / 170 / 340 / 80 minutes, total 10.25 hours. Tools unchanged (Microsoft Word, Microsoft Excel). Domain and occupation unchanged.

## 2026-09-30 · Operator · "make this task harder and more complex" · NEEDS_REVISION (on the 09-29 reviewer return)

Fetched first (tools/fetch_feedback.py): outcome NEEDS_REVISION, reviewer_revision_requested_at 2026-09-29T16:34Z with the note "please make this task harder", expiry 2026-10-04T16:34Z, further revisions allowed. The JSON's two evaluations end in the 2026-09-28 run with outcome PASS (difficulty: glm-5.2 FAIL x4, qwen3.6-27b FAIL x4) on the four-input package uploaded 2026-09-21T22:27Z; the platform still holds that package, so nothing from the 09-29 rebuild had gone up. The folder as left by the 09-29 session had its zips matching but gated at 2 errors under the current checks (R27 on the amendment row's three figures; G20 on the golden's November 3, 2026 renewal date, which no input carried).

**Findings**
1. No platform finding beyond the reviewer's ask; the operator's direction is to keep the task and make it harder and more complex on top of the 09-29 rebuild. Read as a keep-and-harden round: each addition is a look-alike arm of a rule already in play, no new rule and no new deliverable.
2. Rules with an arm the file never exercised: guideline 6.3's maturity test (both open mortgages failed on the twenty-year test, and the one insured over met all three tests); guideline 7.4's five-year life had a timely refiling and a late one but no certificate that simply ran out, and no lien that survives a chain of refilings across the 2014 conveyance.

**Actions taken**
- Inputs, still six files. recorder_index_cedarbrook_lot12.csv and instrument_abstracts_hlt262214.docx gain a 1999 mortgage from the Vosses to Park National Bank at instrument 199907160122 ($61,500.00, final installment due August 1, 2029, no release of record): older than twenty years and with no enforcement action, but not matured, so it cannot be insured over and stays open. tax_and_lien_search_hlt262214.xlsx gains certificate 10JL00227 against Daniel Ray Pruitt (filed 03/12/2010 while he held all of the land, refiled 03/05/2015, 02/26/2020 and 02/19/2025, each inside five years of the last, with a $1,000.00 payment credited 06/15/2018) and certificate 16JL00541 against Robert Lee Kessler (filed 09/08/2016, never refiled, so it ran out in September 2021). The amendment abstract now recites its effect "from the renewal of the Declaration on November 3, 2026", so the golden's date is input-carried.
- Golden: the Park National mortgage in the mortgage table and the insure-over paragraph; 10JL00227 and 16JL00541 in the docket table with their reasons; requirements 6 (Park National) and 13 (10JL00227) inserted and the list renumbered to sixteen with every cross-reference re-pointed; the payoff table carries 10JL00227 in two legs ($1,435.89 to the payment, $1,115.03 after it, $124.00 costs, $5,993.47), four judgment payoffs at $27,071.04 and the of-record total at $29,495.95; 16JL00541 in the examined-and-passed table; the open-matters line names Park National as a third lender to ask. A20 repairs on the new sentences.
- verify_golden.py: 56 figures reproduced, 68 near flips; three variants added, each moving a graded standing (the maturity test skipped on an old mortgage, a never-refiled certificate read as in force, every refiling measured from the first filing), and the existing payment, lien-survival and interest variants now move 10JL00227 too.
- Rubric 57 rows at +107 / -24: positives for the Park National mortgage held open (+3), 10JL00227 in force through its refilings (+3) and its payoff (+2), 16JL00541 lapsed and passed (+2); negatives for insuring over the unmatured 1999 mortgage (-2) and requiring payment of the lapsed certificate (-2). The amendment row reworded off its three figures (R27). Every "although" negative and the two reason-clause positives ("because", "on the ground that") rewritten as one defect or one verdict with the record inside the predicate, the shape the form's atomic check accepted on lien-analysis-larkspur the same day. Gate findings on the draft fixed in place: E1 on the payoff-figure negative (now "wrongly states"), R22 on the 1999 mortgage negative (id dropped, "recorded in 1999"), A20 twice on the golden.
- struck-phrases.md extended (the three-count phrases, the two old totals, the old amendment recital, the old rubric wording); clause-map.md re-pointed to the new numbering with the Rebuilt line dated 2026-09-30; form-lists.md times 20 / 180 / 370 / 90, total 11 h; metadata.json resynced with tools/sync_metadata.py (57 criteria, six inputs). Prompt unchanged since the 09-29 rebuild.
- Coded check: none. The lesson (a rule's every arm exercised, with the decisive instance the one the file does not flag) is PR21/PR22 already; recorded in memory/difficulty-check-lessons.md as this task's keep-and-harden round.
- Gate: 0 errors on the packaged folder (office_resave --force, fix_floats, fix_metadata, zips, autoeval_check, H10 zips matching); package_sweep reports one GENERATOR finding on submissions/06-tract7-boundary-retracement (not touched).

**Form actions**
1. Replace the prompt with instruction.md (unchanged since the 09-29 rebuild, but the platform holds the 09-21 text: the two new file names, the examined-and-passed ask and the October 21 due date are new to the form).
2. Input File List: six entries from form-lists.md; remove any earlier input upload the widget still holds.
3. Re-upload i-title-exam-cedarbrook-lot12.zip (six members) and s-title-exam-cedarbrook-lot12.zip; confirm both uploadedAt stamps moved past 2026-09-21T22:27Z on a re-fetch.
4. Re-enter the rubric: 57 criteria from the CSV, positive 107 / negative 24, formatting row last; confirm the count on the form reads 57.
5. Times 20 / 180 / 370 / 90, total 11; tools, domain and occupation unchanged.
6. Section 3 unchanged (the reviewer's note carried no finding to answer). Resubmit before 2026-10-04T16:34Z.

## 2026-09-30 · Operator · a seven-item hardening list, second pass the same day · NEEDS_REVISION (same return)

The operator pasted seven hardening items written against the task as first built. Read against the current package: items 1 (abstracts stripped of conclusions), 4 (a certificate against the seller's husband, 24JL00902, with him off the no-certificates line), 5 (the 2016 dissolution decree in the domestic relations index, the 2006 open-end mortgage seventeen days inside the twenty-year line) and 7 (the plat items and the November 3, 2026 renewal in the golden) were already in place from the 09-29 rebuild and the morning's round; nothing was changed for them. Items 2, 3 and 6 were new and are built.

**Actions taken**
- Item 2, credits. title_order_hlt262214.docx now says a payment or garnishment the docket credits goes first to the interest accrued to its date and any remainder to principal, interest runs on the reduced principal, interest a credit did not cover stays due without bearing interest, and a vacated credit is left out. Docket Entries gains a $1,500.00 garnishment credited 01/15/2026 on 25JL01133. Golden: 25JL01133 in three legs ($391.95 and $1,108.05, then $98.28 and $2,551.72, then $303.84 to closing) at $6,243.07; 10JL00227's $1,000.00 credit is less than the $1,435.89 then accrued, so it goes wholly to interest and the principal stays $4,318.55, payoff $6,329.47; four judgments $25,840.58.
- Item 3, the release. The release at instrument 202310020190 now recites a lien "recorded July 12, 2023 in Official Record 3198, Page 411", no instrument in the chain, while the index still keys it to 202307210033. Golden: the lien is open (guideline 10.5, the instrument controls under 1.3), requirement 14 for a corrected release or payment of the $6,840.00, the reverse case of the mis-keyed satisfaction stated beside it, the passed-liens row dropped, a corrected-release line under open matters; the requirements renumbered to seventeen with every cross-reference re-pointed.
- Item 6, the duplicate. Tax Duplicate rebuilt with GROSS TAX, ROLLBACK (12.5%), NET TAX, SPECIAL ASSESSMENT, BILLED, PAID, PAID DATE and STATUS; gross figures moved to multiples of $0.08 so the 87.5% net is exact to the cent (2022 $1,712.32, 2023 $1,741.84, 2024 $1,768.48, 2025 $1,796.16); the second-half 2024 installment paid $1,700.00 against $1,859.92 and marked "Paid short"; a note defining the rollback. The order prorates the net tax after the rollback credits and collects the unpaid part of an installment paid short. Golden: unpaid second half $2,072.55, late-payment penalty $94.21, the short $159.92 with its $15.99 penalty $175.91, taxes $2,342.67, proration on $3,143.28 net at $2,669.64, of-record total $28,183.25.
- verify_golden.py: the interest-first rule, the net-tax and short-payment arithmetic, the release tested by the instrument's own recording; 57 figures reproduced, 75 near flips; three variants added (a credit taken off principal, the short payment read as paid, proration on the gross tax) and the index-reference variant now moves the mechanics lien too.
- Rubric 62 rows at +116 / -26: the two payoff rows re-pinned, positives for the 10JL00227 credit going wholly to interest (+2), the garnishment applied to accrued interest (+2), the short installment collected (+2), the proration on the net tax re-worded, the mechanics lien row turned from a -3 negative into a +3 release requirement; negatives for passing the lien on the index reference alone (-3) and prorating the gross tax (-2). Gate findings on the draft fixed in place: R27 on two new rows (figures trimmed), G43 on the payment variant's struck phrase, A20 on the duplicate's note and one golden sentence.
- struck-phrases.md extended (every old payoff, tax and proration figure, the old credit rule, the release's old recital, the old standing and rubric wording); clause-map.md re-pointed to the 62 rows; form-lists.md times 20 / 190 / 400 / 90, total 11.75 h, the workbook gloss extended; metadata.json resynced. Prompt unchanged.
- Coded check: none; PR21/PR22 cover the shape. Memory: one dated line in memory/difficulty-check-lessons.md.
- Gate: 0 errors on the packaged folder after the full sequence; package_sweep reports one GENERATOR finding on the lien-analysis-larkspur owner file (another session's work in progress, not touched).

**Form actions** (replace the morning's list)
1. Replace the prompt with instruction.md (the platform holds the 09-21 text).
2. Input File List: six entries from form-lists.md; remove any earlier input upload the widget still holds.
3. Re-upload i-title-exam-cedarbrook-lot12.zip (six members) and s-title-exam-cedarbrook-lot12.zip; confirm both uploadedAt stamps moved past 2026-09-21T22:27Z on a re-fetch.
4. Re-enter the rubric: 62 criteria from the CSV, positive 116 / negative 26, formatting row last; confirm the count reads 62.
5. Times 20 / 190 / 400 / 90, total 11.75; tools, domain and occupation unchanged.
6. Section 3 unchanged. Resubmit before 2026-10-04T16:34Z.
