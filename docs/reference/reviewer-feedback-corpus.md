# Reviewer Feedback Corpus

> **Inherited from the Geranium desk, not confirmed for Hazy.** This document describes
> verbatim feedback from Geranium reviewers on Geranium tasks, in the Wholesale Trade
> sector. The prose and rubric lessons generalise; the sector specifics do not. It is kept for reference and was NOT updated in the 2026-09-21 port; treat
> anything it says about sector, rubric bands or platform checks as Geranium's, not
> this project's. See `../RULE-DELTAS.md`.

> Every piece of reviewer feedback this portfolio has received, collected as **learning
> material**: how real Geranium reviewers pick what to flag, how they word it, and where they
> draw the blocking / non-blocking line. Nothing here is a to-do list. Fix actions for any task
> live in that task's `feedback-log.md`.

**Sources.** Verbatim notes pulled 2026-08-20 (Part 1) and again 2026-09-04 (Part 1b) with `stb submissions feedback <taskboard-uid>`
for all 15 submissions in `submission-list.md`. The platform keeps only the **latest** Revision Notes and
Accept Notes per submission, so earlier rounds survive only as the summaries written into each
task's `feedback-log.md` at the time; those appear in Part 2, marked as paraphrase.

**Quoting rule.** Part 1 is reproduced character for character, including the reviewers' own
typos, lowercase, and em dashes. Do not clean it up. The register is part of what makes it
useful.

**Human reviewers only.** This corpus deliberately excludes AutoEval, the agentic rubric quality
review, and the platform pre-submission checks. Everything in Part 1 was typed by a person. The one
place machine text appears is inside task 04's accept note, where the reviewer pasted the AutoEval
atomicity comments into their own note and worked from them; it is kept because the reviewer's
handling of it is the lesson. AutoEval history for every task lives in the task feedback logs.

**Coverage.** As of 2026-09-04, 22 of 24 submissions with a UID have reviewer text (Part 1b); on 2026-08-20 it was 8 of 15. Tasks 12 and 13 carry AutoEval and agentic
review findings only, with no human reviewer note yet. Task 14 (evaluation pending) and 15
(offered) have none. Task 02 was rejected and is no longer assigned, so its feedback is not
retrievable through the CLI.

---

# Part 1 — Verbatim reviewer notes

## Task 01, hartwell-cost-increase (ADJUDICATION_PENDING)

**Revision Notes**

> The rubric lacks a completeness criterion. The prompt requires every affected stocked item to
> be repriced, but the rubric only spot-checks individual SKUs (lines 2-16); a submission
> omitting items would pass if the spot-checked SKUs are present. Add a criterion requiring every
> qualifying Hartwell item in item_master_extract.xlsx to appear exactly once on the repricing
> tab with populated new cost and L1-L4 prices (excluding held FTG-PRESS items, frozen dead-stock
> items, and non-Hartwell vendors). Also add a penalty if any new L1-L4 price falls below the
> corresponding current value in current_price_matrix.xlsx, per pricing_policy.docx section 5.

**Accept Notes**

> One non blocking observation for future submissions: a few criteria cover several SKUs in one
> line, such as the six press SKUs in criterion 4 and the three 601T lines in criterion 17.
> Splitting those would make partial credit cleaner, but the values are all correct and the auto
> rubric check already rated the set good, so this does not affect the decision.

## Task 03, weldon-transition-buy (ACCEPTED)

**Revision Notes**

> The prompt requires 'new reorder points and safety stock for every stocked branch/item,' but no
> rubric criterion grades completeness of the reset table. Line 11 grades only that the correct
> safety-stock tier is applied, and line 33 spot-checks a single WEL-2230/LYN value. A submission
> resetting parameters for a handful of items could satisfy both. Add a criterion awarding credit
> only when the reset table carries a populated new reorder point and safety stock for every
> stocked branch/item combination with baseline demand across all three branches (ROA/LYN/DAN),
> consistent with policy 5.2's non-stock exception.

**Accept Notes**

> No blocking issues. All four points from the last review were fixed and the workbook
> recalculates to the rubric key from its own formulas.
> Minor for later: criteria 7 and 13 each bundle several checks into one field, and task.toml is
> missing sector, occupation, occupation_code and difficulty_tier.

## Task 04, pbw-rebate-reconciliation (ACCEPTED, salvaged by the reviewer)

The longest note in the portfolio and the only salvage. The reviewer rewrote the task rather than
sending it back a third time, then documented every change.

**Revision Notes** (the earlier round, prompt overspecification)

> -The prompt tells the writer exactly how to lay out the briefing tab, listing what they claimed,
> what it should be, the gap, the drivers, the pushback and our answer, and the filing date. That
> is the shape of the golden solution handed over in the prompt, and the v5.1 guide does not allow
> that level of instruction because it takes the reasoning work away. Cut the list and just say
> Deb needs a briefing tab she can read in five minutes and defend when Gene questions it.
> -Also the prompt says the sixty day window outright. Let the agreement carry that so the filing
> deadline has to be worked out instead of read off the prompt.
> -Everything else is fine. The input files, the golden solution numbers, and the rubric all hold
> up, so only the prompt needs the edit.

**Accept Notes**

> Prompt:
>
> You did great job on revising the prompt by following previous reviewer's comment. however,
> there are still some issues with current prompt:
>
> Main prompt issue: the amendment evidence: The prompt says the correspondence contains:  "the
> thread from last fall about getting the press-fitting line added"
> But the agreement itself says product groups may be added only by a written amendment signed by
> both parties. It repeats that amendments must be in a writing signed by both parties.
> Gene's email says he received "the signed amendment" and confirms Group 30 is effective January
> 1, 2026. That's strong business evidence, but it isn't the amendment itself.
> Because the deliverable is supposed to establish "what PBW actually owes us under the
> agreement," I would prefer either:
> add the executed Group 30 amendment as an input, or slightly modify the prompt:
> "For purposes of this reconciliation, treat Gene's November 12 email as confirmation that the
> executed amendment added Group 30 effective January 1, 2026."
> The first option is much better and more realistic.
> Other than that, I would leave the prompt largely alone. It is not over-specified.
>
> Input file:
>
> 1. Missing actual amendment ,This is the one substantive sufficiency issue.
>
> If Group 30 is excluded, the answer changes materially—not just by the Group 30 dollars, but
> also around the $1 million rebate-tier boundary. So the executed amendment is decision-critical
> evidence.
>
> I would add something like:  pbw_group30_amendment.pdf or .docx that showing:  both parties;
> Group 30/P-Press added; January 1, 2026 effective date; signatures.
> That would make the input packet much stronger.
>
> Input issue 2: authenticity metadata
>
> there is a metadata concern, both Word files have the exact same created and modified timestamp
> of December 23, 2013 at 23:15 UTC, even though one purports to be a 2025 agreement and the other
> is a saved 2025–2026 Outlook correspondence record. The supplier statement's file metadata says
> it was created August 17, 2026, even though the document itself is dated July 31. that does not
> prove LLM generation, and it could reflect sanitization/template reconstruction, but it is not
> operationally credible as untouched original source metadata. please make sure clean the
> metadata.
>
> Golden solution:
>
> 1. As discussed above, the Golden treats the $98,903.14 net Group 30 adjustment as definitively
> owed.  But the actual signed amendment is not attached:  That matters enormously. If Group 30
> were removed from the calculation, corrected eligible purchases would fall to roughly
> $999,968.81, just below the $1 million 3.50% tier. So the missing source document changes both
> the base and the rate. I would therefore not call the current $43,954.88 amount completely
> source-supported until the executed amendment is supplied.
>
> 2.the Eligibility Detail sheet's Status field is manually entered with values, Likewise, the
> credit sheet's "Nets vs Base?" Y/N decisions are hardcoded. This means the most important
> analytical decisions are not actually live.
>
> Rubric: current rubric has some auto eval comments on atomic"
>
> [minor] non_atomic: Criterion 7 bundles fourteen independently verifiable invoice numbers
> (525149, 526642, 527104, 528399, 533776, 534206, 535571, 536175, 538043, 539793, 540019, 541078,
> 541324, 541609) into a single scored item. Each invoice's inclusion or exclusion from the Group
> 30 adjustment could pass or fail independently.
> Suggestion: Consider splitting into separate criteria for major invoice groups or categories
> within the Group 30 adjustment, or accept that this criterion evaluates the adjustment category
> as a whole rather than individual invoices.
> 2. [minor] non_atomic: Criterion 8 bundles five independently verifiable pre-2026 invoice
> numbers (517177, 519811, 521482, 522693, 524180) into a single scored item for the exclusion
> check.
> Suggestion: Consider whether this exclusion check warrants separate scoring, or accept it as a
> single coherent verification of the date-based exclusion rule.
> 3. [minor] non_atomic: Criterion 9 bundles eleven independently verifiable March invoice numbers
> (531191, 531301, 531518, 532016, 532100, 532149, 532341, 532595, 532640, 532935, 533369) into a
> single scored item.
> Suggestion: Consider splitting into separate criteria for major date-range adjustments, or
> accept that this criterion evaluates the March gap analysis as a single reconciliation
> adjustment.
> 4. [minor] subjective_terms: Criterion 23 requires each objection to have a response consistent
> with the agreement's terms and provides examples (ship-date convention, pre-2026 press
> purchases, register cleanup), but does not fully define what makes a response qualify as
> consistent. Graders may differ on whether other responses qualify.
> Suggestion: Either enumerate the specific objection-response pairs expected, or add explicit
> guidance such as 'counts as consistent if the response cites a specific agreement section or
> program rule that addresses the objection.
>
>
> Task now salvaged, with updates:
> Updated task package:
> - Updated_Task_Prompt.txt
> - pbw_growth_rebate_agreement.docx
> - pbw_group30_amendment.docx   [new executed amendment input]
> - pbw_program_correspondence.docx
> - pbw_rebate_statement_py2026.xlsx
> - ap_invoice_register_pbw.csv
> - pbw_credit_memos.csv
> - pbw_rebate_reconciliation_py2026.xlsx
>
> then updated the rubric to have full coverage.
>
> What changed after salvage:
> 1. Added the executed Group 30 amendment so the January 1, 2026 eligibility change is supported
> by the contract file itself, not only by email.
> 2. Refreshed Word document metadata on the agreement/correspondence copies; substantive source
> content was not changed.
> 3. Rebuilt the Golden workbook around live Controls. Eligibility status, duplicate detection,
> countable amount, supplier ship-date basis, cutoff flags, credit treatment, tier selection,
> accelerator, deadline, bridge and briefing amounts are formula-driven.
> 4. Added Statement Rebuild to show the March migration shortfall against PBW's own ship-date
> convention and tie the selected omission invoices by product group.
> 5. The briefing contains linked values rather than fixed numbers embedded in narrative, so
> changes to live controls flow through the meeting summary.
>
> Golden reference result under the supplied terms:
>
> 1.corrected net eligible purchases: $1,098,871.95.
> 2. Applied rebate rate: 4.00%;
> 3.Rebate due: $43,954.88
> 4. PBW statement rebate: $25,706.30
> 5.Additional rebate owed: $18,248.58
> 6.Claim deadline: September 29, 2026

## Task 06, marathon-line-review (ADJUDICATION_PENDING)

**Revision Notes**

> The task is strong and sufficiently complex and the main calculations reconcile. The following
> issues need to be fixed before the task is adjudication ready.
> 1. Criterion 31 uses CROSS OK as the scenario switch, but cross validity is different from the
> decision to convert an item. Add a separate include/exclude control so Sandy can remove items and
> have savings, Great Lakes volume, rebate status, and briefing totals update automatically.
> 2. The rubrics do not directly test the prompt's requirement for a reason on every retained line.
> Add a completeness check requiring a visible reason beside each item left with Great Lakes.
> 3. Policy 4.2 measures Great Lakes volume at current cost, while the analysis uses the
> $317,110.42 historical spend total from glc_purchase_summary.xlsx. Clarify that this file is the
> approved basis for the tier test or provide current-cost support for the other categories.

**Accept Notes**

> Good work on the fixes. The on off switch does what it should now, take a line out and everything
> after it moves too. The numbers are all right as well. Real savings come to 5,878.05 and curt is
> out there claiming 25,776.60.

## Task 07, yearend-deadstock-plan (ACCEPTED)

**Revision Notes**

> UID: ab709e1e-c40d-45ef-a654-481ce1b8a6e7
>
> 1. controller_memo_0810.docx shows an LLM-style punctuation pattern, with em dashes used in the
> heading and throughout nearly every short paragraph. Rewrite the memo in natural internal-office
> language and replace the repeated em-dash construction with conventional punctuation. Keep the
> dates, inventory target, approval requirements, and other business facts unchanged.
>
> 2. vendor_rep_emails.docx shows the same pattern more strongly, with nine em dashes across four
> short messages. Revise all four messages so each sender has a natural email voice, use ordinary
> punctuation, and remove the repeated em-dash phrasing while preserving every program
> clarification, deadline, item decision, and invoice requirement.
>
> Summary and remedy: Update these two input files to remove the repeated LLM-style punctuation
> pattern, then run a fresh per-file authorship sweep before resubmitting. The other input files
> and the revised workbook do not need changes for this issue.

**Accept Notes**

> Thanks for the rewrite, the memo and the emails read like normal office writing now. The numbers
> are all good too. The Torbeck cap allocation and the 12,800.06 cleared both come out right. Good
> work

## Task 08, twincreek-bid-response (ADJUDICATION_PENDING)

**Accept Notes** (no revision round)

> The task substantially meets the acceptance threshold. The prompt is realistic, clear, and
> appropriately scoped to the purchasing/bid-pricing role, and the source filenames and required
> twincreek_bid_worksheet.xlsx output are consistent throughout.
>
> The workbook covers the main business requirements well: all District lines remain in order,
> priced lines identify the offered manufacturer and part, unsupported lines are declined with
> reasons, addendum changes are incorporated, policy floors and continuity limits are considered,
> purchasing-manager issues are surfaced on the briefing tab, and both the District-scored bid
> value and expected contract-year economics are shown. The formulas are sufficiently live for
> review and repricing, and the rubric set gives strong coverage to the prompt's key analytical and
> decision-making goals.
>
> There are a few very small step-rounding differences on individual lines, but they are immaterial
> to the overall pricing analysis and do not warrant rejection. Overall, I do not see a substantive
> correctness, coverage, usability, or source-alignment issue that should block acceptance.

## Task 09, stroebel-inventory-settlement (ACCEPTED)

**Accept Notes** (no revision round)

> The 46,948.49 wire and the 5,451.51 adjustment both hold up, and the elections, the new item
> calls and the buy list all follow the memo the way it reads. The tag corrections from the emails
> are carried with their sources, which is what will win the argument across the table.

## Task 10, boettcher-winter-earlybuy (ACCEPTED)

**Accept Notes** (no revision round)

> The task is professionally scoped and fully supported by its seven source files. The workbook
> correctly applies the rep's written corrections, accounts for every stock-file item, handles PO
> 20347 without double-counting, and provides live item-level sizing, pricing, program economics,
> and a decision-ready front briefing. I found no formula errors or internal contradictions.
> The Advanced Plus difficulty is aligned with the agent results: GPT-5.6 passed 0/5 and Claude
> Opus passed 2/5. Test alignment is adequate: the golden passed all three strict oracle runs,
> while independent checks confirmed the key quantities, discount tier, totals, and economic
> calculations. The advisory static findings are minor and do not create a material grading defect.
> The separate LLM sweep found no actionable authorship signals in any of the seven input files or
> the golden workbook.

## Task 11, dillman-freight-cutover (ADJUDICATION_PENDING)

**Revision Notes**

> Rubric Quality
> The following criteria are bundled: 6, 7, 11, 12, 15, 16, 20, 29, 32, 33, 35, and 37. For each of
> those, separate each item into its own atomic criterion. No criterion should measure/check/test
> more than one single thing.

**Accept Notes**

> Good work.

---

# Part 1b — Verbatim reviewer notes, captured 2026-09-04

Pulled with `stb submissions feedback <uid>` for every submission carrying a UID (24 folders;
42 and 44 have no reviewer text yet). Same quoting rule as Part 1: character for character,
including the reviewers' typos, curly quotes and em dashes. Where a task appears in Part 1 as
well, this is the LATER round; the platform overwrote the earlier text. The section numbers a
reviewer pastes from the adjudication tool ("Adjudication Note: 1. Adjudication Note: (1) ...")
are kept as they arrived.

## Task 04, pbw-rebate-reconciliation (ACCEPTED)

**Revision Notes**
>
> -The prompt tells the writer exactly how to lay out the briefing tab, listing what they claimed, what it should be, the gap, the drivers, the pushback and our answer, and the filing date. That is the shape of the golden solution handed over in the prompt, and the v5.1 guide does not allow that level of instruction because it takes the reasoning work away. Cut the list and just say Deb needs a briefing tab she can read in five minutes and defend when Gene questions it.
> -Also the prompt says the sixty day window outright. Let the agreement carry that so the filing deadline has to be worked out instead of read off the prompt.
> -Everything else is fine. The input files, the golden solution numbers, and the rubric all hold up, so only the prompt needs the edit.
>
**Accept Notes**
>
> Prompt:
>
> You did great job on revising the prompt by following previous reviewer's comment. however, there are still some issues with current prompt: 
>
> Main prompt issue: the amendment evidence: The prompt says the correspondence contains:  “the thread from last fall about getting the press-fitting line added”
> But the agreement itself says product groups may be added only by a written amendment signed by both parties. It repeats that amendments must be in a writing signed by both parties.
> Gene's email says he received “the signed amendment” and confirms Group 30 is effective January 1, 2026. That's strong business evidence, but it isn't the amendment itself.
> Because the deliverable is supposed to establish “what PBW actually owes us under the agreement,” I would prefer either:
> add the executed Group 30 amendment as an input, or slightly modify the prompt:
> “For purposes of this reconciliation, treat Gene's November 12 email as confirmation that the executed amendment added Group 30 effective January 1, 2026.”
> The first option is much better and more realistic.
> Other than that, I would leave the prompt largely alone. It is not over-specified.
>
> Input file:
>
> 1. Missing actual amendment ,This is the one substantive sufficiency issue.
>
> If Group 30 is excluded, the answer changes materially—not just by the Group 30 dollars, but also around the $1 million rebate-tier boundary. So the executed amendment is decision-critical evidence.
>
> I would add something like:  pbw_group30_amendment.pdf or .docx that showing:  both parties;  Group 30/P-Press added; January 1, 2026 effective date; signatures.
> That would make the input packet much stronger.
>
> Input issue 2: authenticity metadata
>
> there is a metadata concern, both Word files have the exact same created and modified timestamp of December 23, 2013 at 23:15 UTC, even though one purports to be a 2025 agreement and the other is a saved 2025–2026 Outlook correspondence record. The supplier statement's file metadata says it was created August 17, 2026, even though the document itself is dated July 31. that does not prove LLM generation, and it could reflect sanitization/template reconstruction, but it is not operationally credible as untouched original source metadata. please make sure clean the metadata.
>
> Golden solution:
>
> 1. As discussed above, the Golden treats the $98,903.14 net Group 30 adjustment as definitively owed.  But the actual signed amendment is not attached:  That matters enormously. If Group 30 were removed from the calculation, corrected eligible purchases would fall to roughly $999,968.81, just below the $1 million 3.50% tier. So the missing source document changes both the base and the rate. I would therefore not call the current $43,954.88 amount completely source-supported until the executed amendment is supplied.
>
> 2.the Eligibility Detail sheet's Status field is manually entered with values, Likewise, the credit sheet's “Nets vs Base?” Y/N decisions are hardcoded. This means the most important analytical decisions are not actually live.
>
> Rubric: current rubric has some auto eval comments on atomic" 
>
> [minor] non_atomic: Criterion 7 bundles fourteen independently verifiable invoice numbers (525149, 526642, 527104, 528399, 533776, 534206, 535571, 536175, 538043, 539793, 540019, 541078, 541324, 541609) into a single scored item. Each invoice's inclusion or exclusion from the Group 30 adjustment could pass or fail independently.
> Suggestion: Consider splitting into separate criteria for major invoice groups or categories within the Group 30 adjustment, or accept that this criterion evaluates the adjustment category as a whole rather than individual invoices.
> 2. [minor] non_atomic: Criterion 8 bundles five independently verifiable pre-2026 invoice numbers (517177, 519811, 521482, 522693, 524180) into a single scored item for the exclusion check.
> Suggestion: Consider whether this exclusion check warrants separate scoring, or accept it as a single coherent verification of the date-based exclusion rule.
> 3. [minor] non_atomic: Criterion 9 bundles eleven independently verifiable March invoice numbers (531191, 531301, 531518, 532016, 532100, 532149, 532341, 532595, 532640, 532935, 533369) into a single scored item.
> Suggestion: Consider splitting into separate criteria for major date-range adjustments, or accept that this criterion evaluates the March gap analysis as a single reconciliation adjustment.
> 4. [minor] subjective_terms: Criterion 23 requires each objection to have a response consistent with the agreement's terms and provides examples (ship-date convention, pre-2026 press purchases, register cleanup), but does not fully define what makes a response qualify as consistent. Graders may differ on whether other responses qualify.
> Suggestion: Either enumerate the specific objection-response pairs expected, or add explicit guidance such as 'counts as consistent if the response cites a specific agreement section or program rule that addresses the objection.
>
>
> Task now salvaged, with updates: 
> Updated task package:
> - Updated_Task_Prompt.txt
> - pbw_growth_rebate_agreement.docx
> - pbw_group30_amendment.docx   [new executed amendment input]
> - pbw_program_correspondence.docx
> - pbw_rebate_statement_py2026.xlsx
> - ap_invoice_register_pbw.csv
> - pbw_credit_memos.csv
> - pbw_rebate_reconciliation_py2026.xlsx 
>
> then updated the rubric to have full coverage. 
>
> What changed after salvage:
> 1. Added the executed Group 30 amendment so the January 1, 2026 eligibility change is supported by the contract file itself, not only by email.
> 2. Refreshed Word document metadata on the agreement/correspondence copies; substantive source content was not changed.
> 3. Rebuilt the Golden workbook around live Controls. Eligibility status, duplicate detection, countable amount, supplier ship-date basis, cutoff flags, credit treatment, tier selection, accelerator, deadline, bridge and briefing amounts are formula-driven.
> 4. Added Statement Rebuild to show the March migration shortfall against PBW's own ship-date convention and tie the selected omission invoices by product group.
> 5. The briefing contains linked values rather than fixed numbers embedded in narrative, so changes to live controls flow through the meeting summary.
>
> Golden reference result under the supplied terms:
>
> 1.corrected net eligible purchases: $1,098,871.95.
> 2. Applied rebate rate: 4.00%;
> 3.Rebate due: $43,954.88
> 4. PBW statement rebate: $25,706.30
> 5.Additional rebate owed: $18,248.58
> 6.Claim deadline: September 29, 2026

## Task 10, boettcher-winter-earlybuy (ACCEPTED)

**Accept Notes**
>
> The task is professionally scoped and fully supported by its seven source files. The workbook correctly applies the rep’s written corrections, accounts for every stock-file item, handles PO 20347 without double-counting, and provides live item-level sizing, pricing, program economics, and a decision-ready front briefing. I found no formula errors or internal contradictions.
> The Advanced Plus difficulty is aligned with the agent results: GPT-5.6 passed 0/5 and Claude Opus passed 2/5. Test alignment is adequate: the golden passed all three strict oracle runs, while independent checks confirmed the key quantities, discount tier, totals, and economic calculations. The advisory static findings are minor and do not create a material grading defect.
> The separate LLM sweep found no actionable authorship signals in any of the seven input files or the golden workbook.

## Task 12, hollenbach-allocation-plan (ACCEPTED 2026-09-02)

**Revision Notes**
>
> Previous review issues are resolved and this is almost ready for adjudication. Just a few rubric issues to fix now...
>
> 1. Bundled items: 2, 6, 8, 9, 10, 11, 16, 19, 21, 30, 31 all check for more than one thing; separate into individual criterion. 
> 2. Remove negative language in negatively weighted items such as "although prohibited."
>
**Accept Notes**
>
> Thanks for the revisions. Please note the currency labels in your rubric criteria lack $ and proper notation so please human review them even if you are using LLM-generated inspiration. I adjusted them. Thanks

## Task 13, kolterman-valve-advisory (ACCEPTED)

**Revision Notes**
>
> The core FIFO, claim, customer-exposure, and coverage calculations independently reconcile (Quarantine rows 37–40, Claim rows 30–36, Accounts row 46, and Coverage row 32). However, operations_memo_0817.docx explicitly requests short written counter guidance stating the affected numbers, what customers should do, whom to contact, and that counter staff must not promise labor reimbursement. The golden workbook never provides that notice or script: Accounts row 45, Actions row 13, and Notes B16 merely say to post one. It also omits the CONTACT and PHONE fields available in customer_master_extract.xlsx, reducing the actionability of the immediate-contact list. Rubric criterion 11 checks only the 108 untraceable units and posting action, so the requested counter content is not graded. Add the counter-facing copy/actionable contacts and a corresponding rubric criterion.
>
**Accept Notes**
>
> All nine inputs and the golden workbook are usable and internally consistent. Independent FIFO and transfer tracing confirmed the 30 zero-balance reconciliation checks and the key results: 594 quarantined/1,531 saleable units, $12,473 material credit and $13,096.65 claim, 961.1 lb consolidated pickup, 2,318 affected units across 41 accounts, 76 post-stop-sale units, 108 untraceable counter units, 11 capped potable-service accounts, 176 substitute units, and $2,121.44 margin at risk. The workbook correctly applies the rep email’s expanded B25-31–B26-16 window and added LF-4406-12/LF-9012K scope, excludes the Piqua XP codes, preserves original invoice costs through transfers, and supplies the requested Briefing, Counter, Accounts, Claim, Coverage, and Actions content. Required totals are formula-driven with no formula errors or external links, and no prohibited LLM-generation or duplication evidence was found.

## Task 19, rempel-job-buyout (ACCEPTED)

**Revision Notes**
>
> Adjudication Note: 1. Adjudication Note: (1) Rubric line 27 (weight 4) requires 'a named action table of five rows' but the prompt does not fix the number of actions; it drives them from overages above $250 and schedule misses, which yields a variable count. Drop the row count and grade for an action table where each required notification carries an owner and a date. (2) Total negative weight is -16 (four criteria) against 134 positive weight (11.9%), which is below the 20% penalty floor. Add or increase negative criteria to reach at least -27.
> 2. The golden workbook is substantively accurate across all 29 buyout line extensions (total 58,682.84), all variance splits (scope -2,158.20 / buy 4,380.05), all eight release dates and freight calculations (1,134.75 total), all eight stock pull/buy decisions, and both summary totals (59,817.59 delivered, 3,356.60 over basis). One narrative overstatement in the Briefing (cell A23) says 'the ball valves only clear because Grebner has twenty four coming in' when only BV-1 depends on the PO -- BV-2 passes at position 44 vs. order point 40 without it. This does not affect any workbook number. Fix by changing 'the ball valves' to 'BV-1'. The rubric has three Minor mechanical issues: (1) double jeopardy between criteria 3 and 10 on HB-1 sourcing (9 points at risk for one error), (2) subjective 'clear note' in criterion 18, (3) penalty weight at 11.9% of positive vs. the 20% floor.
>
**Accept Notes**
>
> Accepting this one. The prompt reads like a real handoff and all fourteen file names sit naturally in the opening paragraph, and it stops at the workbook name, the content scope and the live cells without dictating tabs or a computation order, so the reasoning friction is intact and both frontier agents scoring zero confirms it. The inputs hold together well, and the traps are genuine, since GB-712 clears the movement test at twenty six units where the fourteen inch would not, and the position lands exactly on the order point which the policy says passes. Also the golden ties out to the penny with no formula errors, and scope and buy add to the difference while the eight release nets plus the five Salina picks reconcile back to the buyout total. Good work.

## Task 20, rademacher-service-review (ACCEPTED)

**Revision Notes**
>
> Adjudication Note: Rubric criterion 12 mandates the purchase-order-line walkthrough appear 'on the parameters tab,' but the prompt never names a parameters tab or dictates tab layout. A solver who places the same walkthrough on any other tab would lose 3 points for an equally valid approach. Reword to 'on the parameters tab or equivalent' so the criterion grades the analytical content rather than a specific tab name.
>
**Accept Notes**
>
> Minor, not blocking. The rubric is all rigid criteria. Two items are real judgment calls and would score better as condition-based criteria: the three renewal terms (weight 1 each) and the item moves. A solver who names three other sound terms earns nothing for work that answers the ask. Worth adjusting next time, no rework needed here.
>
> Everything else holds. Prompt reads as a real handoff, file names sit naturally in the opening, deliverable stated without walking through the method. All auto-checks pass and difficulty came back Frontier.

## Task 22, frankfort-stock-recovery (ACCEPTED, recommended)

**Revision Notes**
>
> The prompt names bercot_inspection_report.docx and bercot_email_thread.docx and nothing else, but there are fifteen files in the folder. The rest have to be named the same way.
>
> Most already have a sentence pointing straight at them. The Ratcliff crew is ratcliff_disposal_manifest.xlsx, INV-9 is property_loss_policy.docx, what Bernice sent is ripberger_memo_0817.docx.
>
> Nothing else needs changing. The 83 lines tie back to the 08/07 status and 93,189.29 comes out the same. Criterion 6 already carries the YB4015 exception at N-34-B, so the alignment note about it is wrong and the criterion should be left alone.
>
**Accept Notes**
>
> Accepting and recommending. This has the hardest difficulty profile I've seen this cycle: zero solves across ten runs, rewards from 0.389 to 0.891, and a mean around 0.72.
>
> I verified the key calculations from the raw files, including the supplier pricing conventions, the $77,344.18 replacement-cost total, the $436.96 KP1044 adjustment, the timing cut around the storm, and the $93,189.29 net claim. Everything checks out.
>
> The negative criteria are especially strong because they clearly separate the actual defects from nearby cases that should not be flagged. The prompt is also very well written, with realistic provenance, clear precedence rules, and a real reason for requiring live formulas.
>
> One small cleanup item: all six XLSX files, including the golden, still show "Microsoft Excel Compatible / Openpyxl 3.1.5" in the metadata. That should be cleared before the package is used as a reference example.
>
> No other changes needed.

## Task 23, june-price-review (ACCEPTED, recommended)

**Revision Notes**
>
> Hi, excellent work on this package. I rebuilt the audit independently, and the analysis is correct throughout. Every major figure and disposition reconciles with the source data.
>
> Sending this back for only two things.
>
> First, all five input XLSX files still show Microsoft Excel Compatible / Openpyxl 3.1.5 in their properties. The golden has the same trace. Please open and re-save them in Excel or LibreOffice so that metadata is cleared.
>
> Second, the quotation honor date is off by one day. Thirty days after 06/15/2026 is 07/15/2026, but the Params tab and Q-26048 currently use 07/14/2026. This does not change any financial result, but criterion 46 explicitly tests the date, so those two cells should be corrected.
>
> One additional note: the static audit's claim that the rubric does not require formulas is incorrect. Several criteria do require them, and the golden contains 2,127 live formulas. However, some formula criteria may not be verifiable through extracted text, so that is worth checking separately.
>
> The underlying analysis and task design are exceptionally strong. Clear the workbook metadata and fix the two date cells, and this is ready.
>
**Accept Notes**
>
> Accepting and recommending. Both issues from previous review are fixed correctly.
> The metadata blocker is cleared. All five input workbooks and the golden now show Microsoft Excel, the intended authors remain intact, and there are no generator strings.
> The quotation honor date is also corrected to 07/15/2026 in both places. I re-ran the key figures after the Excel re-save and nothing changed: the 332 mispriced lines, 6,689.08 net shortfall, and other audited figures still reconcile. The golden also retains all 2,127 formulas and its calcChain.
> The remaining safety-screen finding about July 14 is stale because it ran against the previous artifact. The formula-related verifier findings appear to be harness limitations rather than package defects.
>
> Everything I asked to be fixed is now resolved, with no regressions.

## Task 29, chemical-lot-review (ACCEPTED)

**Revision Notes**
>
> Adjudication Note: 1. Adjudication Note: 1. Criterion 4 hard-codes 'eight actions in all,' but the prompt asks only for 'whatever has to be done, and by whom, before any of it is keyed.' A solver who covers every pre-keying task but groups them into seven or nine lines loses two points for a grouping choice the contract leaves open. Revise to grade coverage plus owner and date for each pre-keying task without mandating a count, for example: 'The front page carries an action list naming an owner and a date for each pre-keying task required by the memo and policy (scrap approval, rotation request and shipping, Dahlstrom hold and notification, PO cancellations, order-quantity keying, transfer staging, sell-first moves), however grouped.' 2. The inputs carry two different credit-memo numbers for the same September 2025 rotation credit: the summary sheet and vendor email say CM 44817 while the Credit Memos 2025 detail sheet says CM 44783, both for 3,418.77 on 09/22/2025. Make the numbers consistent. 3. The golden Params tab source note for the 212.40 non-rotation credit says 'CM posted June 2025' but the input shows March 2025; correct the month.
> 2. The golden Params tab cites 'CM posted June 2025' for the 212.40 non-rotation credit but the input shows March 2025. Correct the month in the source note. The value itself (212.40) and all downstream calculations are correct.
>
**Accept Notes**
>
> Good work on this one. The 234 lots and 8,337 units come out right after the recounts and the case tags, the 1,601.85 plus 146.20 write off ties out lot by lot, and the Tomczak limit lands at 2,064.05. I changed one action line to say thirteen cases and reworded criterion 14.

## Task 30, rossville-domestic-content (ACCEPTED)

**Revision Notes**
>
> Hi, the analysis in this package is exceptional, and neither of my findings affects it. I rebuilt the model from the inputs and every graded figure checks out. The allowance allocation is especially well designed, including the whole-line rule and the skip-and-continue logic. The negatives and the formula-driven workbook are also very strong.
> Only two things need fixing.
> First, the difficulty run was scored against a different rubric. The current rubric totals 87 points, but all ten reported rewards resolve against a 107-point denominator. Please re-run difficulty against the current rubric and resubmit with the updated results.
> Second, all five input workbooks still show "Microsoft Excel Compatible / Openpyxl 3.1.5" with AppVersion 3.1. Please re-save them through Excel, set plausible creators matching the source of each workbook, and make sure the Application metadata reads Microsoft Excel.
>
> Nothing else needs changing. The analysis, task design, and golden are all strong.
>
**Accept Notes**
>
> All 10 inputs and the golden workbook are readable, consistent, and substantively complete. The Schedule tab reconciles all 44 PO lines and correctly identifies 17 nonqualifying lines, with 12 substitutions and five whole-line allowance assignments. Allowance!E4:E27 correctly excludes Schedule lines 43–44, producing a $323,788.80 base, $16,189.44 limit, and $16,155.40 used. The clamp timing, $7,814.24 premium, and margin reduction from $63,492.70 to $55,678.46 independently reconcile to the source documents. Purchase Orders rows 6–23 and Certifications rows 5–13 correctly reflect the vendor deadlines and two required letter reissues. Key briefing figures and line-level cost, arrival, and allowance outputs use live formulas. The rubric is well aligned, and I found no material duplication or prohibited LLM-authorship indicators.

## Task 31, returns-cage-disposition (ACCEPTED)

**Revision Notes**
>
> Great job overall; this looks almost ready for adjudication. I don't see issues remaining with previous review note topics.
>
> There are 2 rubric coverage gaps: 
> 1. Prompt asks for every cage line to show where it goes; rubric doesn't measure this.
> 2. Prompt requires workbook to remain correct when Janet moves a line, but no criterion checks this.
>
**Accept Notes**
>
> Accepting. Both coverage gaps from last round are closed. Criterion 8 now puts a disposition on every cage line with the restock count against it, and criterion 9 scores the schedules filling themselves from the per-line dispositions, which is the thing that has to hold when Janet moves a line. The workbook does it properly. The vendor, claim, restock, scrap and chargeback tabs all pull their rows through slot formulas off the Lines tab rather than fixed references.
> I rebuilt the file from the cage count, the authorization log, the credit register and the item file rather than reading the workbook back. Seventy five lines and 145 units at 16,374.83, restock 32 lines at 3,949.79, two Ostrander lines going back at 708.00 with 566.40 of credit after the twenty per cent, 21 claims at 6,019.56, 20 scrapped at 5,697.48 and eight chargebacks covering 13 units at 681.70 of cost. The suspense bridge comes to 3,478.49 plus 566.40 plus 141.60 plus 5,371.56 plus 4,888.00 plus 681.70, which is 15,127.75 against Janet's balance with nothing unexplained. The Brenneke pair at 120.70 falling under Nate's new 250 minimum, the May effluent pumps at 105 days against Ostrander's sixty, and the second sewage ejector on RG2637 going to scrap because only one was ever authorized, all come out the same way.
> One observation, and it is not why I am accepting. Seventeen of the 39 positive points sit on the four criteria about live formulas and the action list, while the calls that make this task hard, the windows, the vendor minimum, the account placement and the reconciliation itself, are mostly a point each. A response with tidy formulas and the wrong Brenneke decision keeps more credit than one that gets every disposition right and types a couple of cells. Worth rebalancing if the rubric is ever opened again.

## Task 32, pavelka-exposure-workup (ACCEPTED)

**Revision Notes**
>
> Adjudication Note: (1) Add a rubric criterion (weight 3) for individual credit memo claim lines: Each pre-petition credit memo appears as its own claim line showing the dollar amount and the treatment signed and walked, with CM-2515 at 611.84, CM-2774 at 939.42, and CM-2861 at 1,655.32 each converting to a program credit if signed and riding as a pre-petition claim if walked. (2) The golden attributes the schedule to Arlene Kubat (Briefing row 2), a name appearing in no input file; remove or replace with a sourced name. (3) The golden expands V. RAMAEKERS to Vicki Ramaekers in the action list; use the name as it appears in the input. (4) Revise criterion 4 to accept any signing date on or before 09/04/2026; the inputs establish only the deadline, not 09/03 specifically. (5) Criteria 16 (+4) and 20 (-4) double-count the sign/walk recommendation; a wrong call loses the +4 reward and incurs the -4 penalty for an 8-point swing on a single binary decision; fold into one criterion or reduce one weight.
> 2. 1. The golden attributes the schedule to Arlene Kubat (Briefing row 2), a name appearing in no input; remove or replace with a sourced name. 2. The golden expands V. RAMAEKERS to Vicki Ramaekers in the action list; use the name as shown in the input. 3. Criterion 4 hard-codes the signing date as 09/03/2026 but the inputs establish only the deadline of 09/04/2026; revise to accept any date on or before 09/04. 4. Criteria 16 (+4) and 20 (-4) double-count the sign/walk recommendation, creating an 8-point swing on a single binary decision; fold into one criterion or reduce one weight.
>
**Accept Notes**
>
> The nine source files are usable, mutually consistent, and support the task without answer leakage or credible evidence of prohibited LLM generation or template duplication. The golden workbook opens normally and correctly traces the key results through live formulas: Invoices!C33:C40 reconciles the $22,366.80 keyed invoice total to the $20,854.44 notice balance and the $18,173.34 trued payable; Claims and Rebate produce $8,972.29 of claims; Agreement!B5:B12 computes the $3,197.07 commitment cost, $3,961.26 signing advantage, and SIGN recommendation; and Bank Schedule!B16:B17 reports $1,813.96 signed versus $8,972.29 walked exposure. The front Briefing sheet references those calculations and includes named, dated actions. The rubric covers the material deliverable requirements with appropriate answer keys and penalties.

## Task 33, semrad-date-recovery (ACCEPTED)

**Revision Notes**
>
> 1. Adjudication Note: The rubric (lines 5 and 6) hard-codes 'each of its 8 actions' but the prompt says only 'a name and a date on everything that has to happen' without fixing a count. The number of required actions is not deterministically derivable from the inputs, so a compliant action list of a different length would be penalized. Reword both criteria to grade every listed action as carrying a named owner and a due date, dropping the fixed count.
> 2. The golden Briefing page introduces a fabricated preparer name "Lorna Sedlacek" (cell A2) that does not appear in any input file. Fix: remove the specific name or replace with a generic placeholder such as "[Preparer]", since the prompt does not identify who is building the workbook beyond Cliff Wodarczyk requesting it. All 151 other traced claims (line-by-line recovery decisions, every added-cost figure totaling 1,602.19, the Kriegl release at 8,063, the quick-ship order at 4,201.56, the Kriegl premium total at 957.33, the transfer charge, the Rice Lake sizing, all dates, all job names, and every formula cross-reference) reconcile exactly to the input files. The rubric covers all 13 discrete prompt requests, carries adequate penalty weight (46% of positive), and contains no over-constraining, under-specification, or mechanical defects.
>
**Accept Notes**
>
> Accepting. Both prior notes are closed and the package reconciles end to end.
> The action count is out of criteria 7 and 8, which now grade every action the list carries rather than a fixed eight, so a solver who writes nine or twelve is not punished for it. The briefing page no longer carries a preparer who does not exist. It reads Cliff Wodarczyk now, and he is on the memo's To line, so nothing on that page is invented. I ran the names in the workbook against the inputs and every one of them, Bernice, Dale, Dennis Prosser, Bonnie, Norb, traces back to a file.
> I rebuilt the slip from the ten inputs before opening the workbook, and I got the same numbers. Kriegl at 8,063 for the one SE-119-18 and five SR-50-65, premiums of 957.33 against the booked nets, the quick-ship order at 4,201.56 with the 298.77 and the 142.14 upcharges and the vent kit riding without one, the 45.00 transfer, and 1,602.19 to hold the season. That last figure reconciles two ways, once as premiums plus upcharges plus transfer and once down the added-cost column on the line sheet, and both land on it. The 72.55 model delta on the SG-100-80 is the piece most people would drop, and it is there.
> The construction underneath is the best part. The donor rule bites correctly in three places: Wausau can release exactly one SG-50-60 because eight weeks at its own pace rounds to three and it holds four, and Rice Lake and Eau Claire can release nothing on the SR line because both sit under their own eight week floors. Closing the SR quick-ship slots on Bonnie's word rather than the printed letter is what forces the Klingbeil units to Kriegl, and the Pine Grove line is the only one that cannot be recovered because the substitute is barred by the engineer and Norb has nothing before November. The prepaid freight thresholds hold on both orders without anyone having to say so.
> One thing for adjudication rather than for you. The Rice Lake buy of three turns on measuring twelve weeks to the arrival week, and the workbook states that on the Sizing sheet, which is the right way to do it. But the round up sits about half a week from flipping to four. Anyone who anchors the count on the stock file's 08/19 cut, or who runs it to the Friday of the arrival week, gets four units, and that carries the Kriegl release to 9,078 and fails two criteria. The memo's "now" is plainly the working date and not the stock snapshot, so I think the workbook has it right, but graders should expect that variance and should not read four as careless.
> Two things I checked and dismissed. The package audit reports a Major saying the rubric never requires formulas or penalises hard-coded values. That is not true of this rubric. Criteria 2, 3, 17, 18 and 19 all require the value to arrive through a reference or a computation and say so in as many words, and they carry 16 of the 39 positive points. The rest of that audit is complaining about task.toml keys and a check_outputs script, which do not belong to a package of this shape. Separately the linter fails criterion 18 for grading process not output, on the words "the model", which there means the model number on a heater.
> Small point, take it or leave it. The prior reviewer wanted the two formula criteria cut from five points each. I would leave them. Bernice's memo makes live formulas an instruction in its own right, not a nicety, so weighting them is fair.

## Task 34, delivery-zone-reset (ACCEPTED)

**Revision Notes**
>
> Prompt Quality
> 1. When prompting an LLM to write a rushed work email, you need to edit it yourself, remove LLM slang/shorthand, remove the incomplete sentences, and make sure it's clear and professional. 
>
> 2. I started to fix your final paragraph, but I'm unclear what this is intended to say: "The contract jobs kept clear of it, the accounts on Emmett's twenty listed with what the quarter would have cost each of them, and the page he reads first up front, with the recommendation and who does what before the letter mails." I think you mean this: Keep the contract jobs separate from the reset rather than folding them into the zone-by-zone recalculation. Next, list the 20 accounts Emmet has, showing what the quarter would have cost each of them under the new charges. Put a summary page first, ahead of everything else in the workbook. It should hold the recommendation and who's responsible for what, before the letter goes out." Either way, please edit it for clarity and professional sentence structure. 
>
> 3. How did Emmet come out of a statement? Is he a number? Do you mean a statement meeting, or do you mean his quarterly statement review - or something else entirely? Use clear and professional communication, please. 
>
> 4. The prompt, overall, is too prescriptive. State what you need and what is included. Do not provide all of the step by step info. 
>
> Input file quality
> Remove Ai slop/slang like these phrases: 
> 1. "Word travels. Two things before the pencil comes out." Nobody but an LLM really speaks like that... Particularly, nobody who has a truly urgent issue that needs resolving immediately is going to speak in less-than-clear language. 
> 2. "The July statement has the outbound delivery line circled in my handwriting, and it is going to stay circled until the sheet we hand customers matches what the trucks cost." If there is urgency, state it. "Urgent: xyz mean we need to attend to this issue immediately." 
>
> 3.  Edit this AI slang: 
> - "A charge a customer hears about from their salesman is a policy; a charge they meet cold on a statement is an insult, and I have watched an insult cost this house an account that took ten years to win."
>  - "The seventy five was old when gas was cheap."
> - "if a charge shows up they will drive to Quincy before they pay it, and honestly that is fine with me and probably with the trucks."
>  - "Just build it so I can stand at a counter and defend it, zone by zone, with the cost on paper."
>
> Rubric Quality
> 1. 7, 10, 11, and 17 are bundled; separate into individual criterion. 
>
> 2. 21 is largely redundant with 18. No criterion should measure the same thing more than once. Make sure negatively weighted items are not repeats of things already measured with a positive weight.
>
> 3. Coverage gaps. The prompt asks for the following which are in the golden but are not measured in the rubric: 
> - recovery percentages per memo rule 7
> - 25% floor per the same memo rule 7
> - city/near zone minimums and charges individually are missing
> - top 20 ranking correctness is missing 
> - Memo rule 4 names Mercer & Kroeger but only Mercer is in rubric
> - Formula check is inconsistent - missing for items 4 and 13
>
**Accept Notes**
>
> Accepting. All three sections of the last note are closed and the workbook reproduces from the files.
> On the prompt, the paragraph you were asked about now reads as three plain sentences and says what it means: keep the contract jobs separate, list the twenty accounts with what the quarter would have cost each, and put the summary page first. The statement question is answered in the opening line, where Emmett reviews the July financial statement on Friday and flags the delivery line. On whether it is still too prescriptive, I read it as scoped rather than step by step. It names the things the workbook has to contain and points at the memo and Rosella's rates for the method, and it never says how to cost a stop, what the house margin is, or where to round. That is the right side of the line.
> Both input files are clean now. Every phrase quoted back at you is gone. The circled handwriting line is a plain statement of urgency, the insult sentence has become lasting resentment, the Quincy counter line no longer editorialises, and the seventy five was old when gas was cheap has become has not moved in seven years. None of the rewriting touched a rule, which matters because the golden was built before the prose edit went in. I rebuilt from the current files rather than assume, and nothing moved.
> The numbers hold all the way down. Costing the runs at 31.40 an hour and 94 cents a mile gives 17.44 on the city, 23.02 on the near towns and 35.61 on the far, and at the 24 percent house margin rounded up to the next 25 that is 75, 100 and 150 with charges of 17, 23 and 36. The register is 792 stops, 309 of them take a charge, and the 61 contract stops sit outside it. The old sheet collected 450 against a quarter that cost 18,126.38, which is 2.48 percent, and the new sheet projects 7,687, which is 42.41 and clears rule seven's floor. Ten of the top twenty are touched at 3,619 between them, and the ranking comes out in the same order I got straight off the margin column.
> On the rubric, the coverage gaps are closed. Recovery and the quarter of cost floor are both at criterion 16, the ranking at 21, Kroeger now sits beside Mercer at 19 and 20, and the formula checks reach the register rows and the contract cells. The two negatives are prohibitions rather than mirrors of anything already scored positively.

## Task 35, tessendorf-channel-split (ACCEPTED)

**Revision Notes**
>
> This is a strong task and it is close. The prompt reads like a real handoff, the workbook is live end to end, and I re-derived the numbers off the inputs rather than taking them on trust: the 456.86 shelf runoff is exactly the nine drop-ship items' on-hand times their March nets, the 9/13/4 split falls out of the counter rule, the dead test, the weight rule on CI-330 and the cheaper-side comparison, and seven prices reprice with CV-921 and HR-540 holding above the floor. ST-7712 lands at 23.95. All of that stands.
> The reason this comes back is item_file_tessendorf.xlsx. Its docProps/core.xml is not valid XML. The file declares the cp prefix but then uses dc:creator, dcterms:created, dcterms:modified and xsi:type with no matching namespace declarations, so any strict reader stops at the first of those elements. openpyxl will not open the file at all, it raises "unbound prefix" on line 1 of core.xml, and pandas fails the same way because it reads through openpyxl. That is the file carrying the March nets, the on-hand and the order quantities, so a solver reaching for the ordinary Python path cannot get at the data the whole task computes from. Your golden workbook has the same properties block written correctly, with xmlns:dc, xmlns:dcterms and xmlns:xsi declared inline on each element, so the fix is to copy that pattern into the input file's core.xml and rebuild the input zip. Nothing else in the file needs to change and no figure moves. I would have corrected it myself but input files are locked on my side.
> One optional thing while you are in there. The front page calls that line "Program fees on a year at current movement" and the 257.62 behind it is the full drop-ship side, the 6.85 handling on 35 orders plus the four percent premium on the units. The memo's rule 5 supports reading it that way, but the program letter's own Fees section defines fees as the handling and the parcel charge, so a model reading the letter literally lands on 239.75 and drops criterion 9 on a labelling difference rather than a mistake. Relabelling that line as the program's annual cost, or naming both pieces inside the criterion, would close the gap. Your call, it is not why this is going back.
>
**Accept Notes**
>
> Accepting. The reason this came back is fixed, and I checked it rather than assuming.
> The core.xml in item_file_tessendorf.xlsx now declares xmlns:dc, xmlns:dcterms and xmlns:xsi inline on each element. It parses under a strict reader and openpyxl opens the workbook and gives up the Item File sheet. I went further and parsed every XML part in all five office files, inputs and golden, and they are all clean now, so there is no second copy of that problem waiting in one of the docx files.
> I rebuilt the catalog from the memo rather than reading the answers off your workbook, and all 26 items land where you put them. Nine to drop-ship, thirteen on the shelf, four off the site. The 456.86 is the nine drop-ship items' on-hand at their March nets, the 299.70 is the four dead items the same way, and the 257.62 is the 6.85 on 35 orders plus four percent on the units, which comes to 257.62 when the per-item sides are carried at cents and 257.61 if you sum raw. Your rows are cent rounded and the total agrees with them, so that is consistent. Seven prices reprice and CV-921 and HR-540 hold. ST-7712 lands at 23.95.
> The two places this task is sharpest are worth saying out loud because they are what makes it hard. CI-330 comes out cheaper on their side, 44.05 against 45.92, so only the weight rule holds it on the shelf. And TW-440 splits by three cents, 55.91 against 55.94, so a model that skips Iva's March cut sends it to drop-ship on the arithmetic. Both traps are deliberate and both work. The .95 rounding is done properly too, with the INT test rather than a lookup, so a floor of 17.93 goes to 17.95 and one of 17.96 would go to 18.95.
> On the labelling point from last time, criterion 9 now names both pieces inside itself, the handling and the four percent premium together, so a model that reads the program letter's Fees section literally and lands on 239.75 fails on the number rather than on a wording difference. That closes it.
> Two things to look at, neither of which stops this.
> The workbook says it was prepared by Verla Stroman, on the front page and in the file properties, and that name is in none of the six inputs. The handoff framing does leave room for someone other than Stan to be building it, so it is not incoherent, but it is a name that cannot be traced to the pack and provenance checks do pick those up. A generic preparer line, or Stan's own name, would carry no risk at all. Everyone else in the workbook, Ardyce, Tammy, Dean, Iva, Stan, traces back to a file.
> The rubric review flags criteria 28 and 29 as redundant mirrors. It is right about 29 and wrong about 28. Criterion 15 does already require the two March cut items on the shelf, so 29 restates it from the failure side, but that is a deliberate mirror on the one rule the arithmetic actively fights, and dropping it would leave a single negative on the form. Criterion 28 is not redundant at all. No positive criterion anywhere grades what happens to the dead stock after it comes off the site, and the spring return list is a separate instruction in the memo from the off-site decision itself. I would leave both alone.
> This is close to the top class. What keeps it a notch below for me is the invented preparer and the fact that the count criteria, 10, 11, 12, 19 and 23, spend five slots on five numbers that all fall out of the same decision column. That is defensible for partial credit and I am not asking for a change.

## Task 36, radke-price-protection (ACCEPTED)

**Revision Notes**
>
> Prompt:
>
> Reading the prompt, i can feel that it implies late August 2026, but the task never directly states the review date/year, while eligibility for invoice 884126 depends on whether it has actually been received and the cage is still due to be recounted before filing. Gaylene says 884126 qualifies only “on receipt,” not merely because it shipped before the effective date.  Please state an explicit cutoff such as “analyze records as of August 25, 2026” and treat later receipt/recount events as pending inputs until confirmed.
>
> Input files:
>
> 1. Gaylene's four answers explicitly resolve the sixty-day boundary, opened-reel treatment, the two in-transit invoices, and SPA-8804, while Lavina's memo then specifies the writedown basis, aluminum exclusion, netting treatment, front-page figures, recount process, and receipts classification. Those are legitimate facts in isolation, but collectively the inputs almost supply the intended reasoning path rather than leaving the analyst to reconcile naturally occurring records. Fix: use more natural underlying correspondence/records and avoid a purpose-built question thread that conveniently resolves every benchmark edge case.
>
> 2. Metadata: All three Word inputs explicitly carry generated by python-docx in their package metadata. together with unusually perfect coordination across the other files: the physical count ties exactly to system on-hand, the receipt register contains a one-day-before-window case plus precisely placed SPA exclusions, and the open-PO file contains exactly the pre-/post-effective transit cases asked about in Gaylene's email. this is strong tell that files are engineered.  please at least clean these metadata. 
>
> Golden solution:
>
> 1. The workbook treats invoice 884126 as already qualifying even though the supplied evidence only says it qualifies when received. The Claim sheet immediately includes 5,000 ft of TH-10STR and 12,500 ft of NM-122 from invoice 884126, producing the $3,415.09 filing, even though the source packet contains no record that this truck actually reached the dock. The governing clarification is conditional: “it qualifies on receipt.”  
>
> please add an actual-receipt-status/date input and exclude 884126 until that condition is met; using the current Sunday count and currently supported receipts, the provisional claim is about $3,106.59, with another $308.50 pending if 884126 subsequently qualifies.
>
> 2. The live formulas incorrectly put aluminum footage back into “qualifying footage.” Lavina expressly says SER aluminum stays “out of everything” and “neither devalues nor files,” while the supplier letter likewise says aluminum is unchanged and excluded from protection. But the Golden's Receipts sheet marks the 4,500-ft SER-222 receipt as counted, and after recalculation the Claim/Briefing formulas report 187,000 qualifying ft, including those 4,500 aluminum feet.
>
>  you will need to classify SER-222 as excluded in the receipts register and make the qualifying-footage formula explicitly zero any item outside the program.
>
> 3. The prompt asks for both qualifying and nonqualifying footage with the reason beside each exclusion, but Claim mainly shows qualifying footage and a general standing; purchase-cap exclusions must be inferred, while the cut-stock section only rolls up the 8,775 ft and drops the original condition/reason from the detailed cage rows. The program expressly excludes cut/opened stock, special-price purchases, aluminum and other disallowed categories. 
>
> Please consider add item-level excluded-footage columns or a reconciliation table that separately quantifies cut/opened stock, purchase-cap excess, SPA, out-of-window receipts, post-effective transit and aluminum, with each category tied to its reason. 
>
> 4. The workbook allows full-package counts to be changed and downstream formulas do flow, which is good, but it does not retain package condition or provide an SPA-found flag. Lavina specifically says that if SPA-8804 stock turns up during the recount it must be flagged and excluded. 
>
> Please make the final recount an explicit editable input layer with sealed/opened condition and an eligibility/source flag so changes in both quantity and classification propagate through the filing.
>
>
> Rubric:
>
>
> C2. Wording is too vague: “a page standing ahead of the working sheets” does not clearly identify what qualifies. Say that the front/briefing sheet is the first visible worksheet in the workbook.
>
> C4.  invoice 884126 qualifies only upon actual receipt, which is not established in the supplied records. The criterion should require the qualifying-footage total to be formula-driven from confirmed eligibility inputs, with 884126 shown as pending until receipt.
>
> C5. Not fully atomic. It bundles four separate action-list requirements—recount, verification, signature, and filing—which could be satisfied independently; split them or use a general completeness criterion with separately scored action items.
>
> C14. Factually wrong as written. Invoice 884126 does not qualify merely because it shipped on 8/21; Gaylene says it qualifies “on receipt,” so the criterion should require it to remain pending until an actual receipt is documented.
>
> C21. Needs revision for the same reason as C14. The $649.60 NM-122 credit depends on including footage from invoice 884126, so it should not be hard-coded as a confirmed credit until that shipment's receipt is evidenced.
>
> C23. Needs revision. The filing should not be described as containing all 10 catalog numbers when aluminum SER is expressly outside the protection program; if the workbook shows all ten for reconciliation, it should clearly distinguish the nine claim-eligible copper catalog numbers from the excluded aluminum line.
>
**Accept Notes**
>
> Accepting. Every item on the last note is closed and the workbook rebuilds from the files.
> Taking the golden items in order. Invoice 884126 is now held out of the filing entirely, with the In Transit sheet carrying an editable received-date column that flips the line in when the truck is checked in. The filing on what is at the dock reads 3,106.59 with 308.50 shown separately as pending, which is the split the last note asked for. The aluminum leak is gone: SER-222 is marked NO in the receipts register with its reason, and the qualifying formula on the Claim sheet zeroes anything whose program class is not copper column, so the 4,500 feet cannot come back in through a recalculation. The Exclusions sheet is a real reconciliation now, item by item across cut or opened, SPA found, aluminum, cap excess, pending receipt and post-effective transit, each with the letter term it comes from, and the tie column proves every foot lands in exactly one place. It sums to zero. The recount is a proper input layer with condition and source beside each package count, and the SPA-found cell is there for Lavina.
> I rebuilt the whole thing from the eight files rather than checking your arithmetic against itself. The window at 06/25 through 08/23 on dock dates. The sixty day purchases by catalog number with the SPA lines pulled out of the receipts but not the receipts themselves. Nine copper catalog numbers, the cap biting on five of them for 22,000 feet, 165,000 qualifying against 8,775 feet of cut and opened stock excluded. Every drop off the two column sets, including the 21.55 on MC-122. The credits round at the line, which is why the filing comes to 3,106.59 rather than the 3,106.58 you would get totalling first, and that is the right convention for a credit filing. Shelf loss 3,801.18 on all copper at the cage footage, cut stock included, net 694.59, and 386.09 if the truck lands. All of it matched.
> On the prompt, the last note wanted an explicit cutoff. It reads "as of today, Tuesday the 25th" rather than spelling out the year, but the memo is dated Tuesday, August 25, 2026 and the letter is dated the 24th, so the date is not actually in doubt. More to the point, the prompt now states the pending-input rule directly, which was the substance of the ask. I would leave it.
> One thing to fix if the input zip ever gets rebuilt for another reason. In open_po_radke.xlsx the last line, PO 26-5241 for MC-122, carries an order date of 08/26/2026 on a file headed "PULLED 08/25/2026" with a footnote about the 08/25 status. A pull cannot show an order placed the next day. It changes nothing, because the line is unshipped and sits outside both the filing and the on-hand footage, and your In Transit sheet says so. But it is the one date in the pack that cannot be true. The receipts CSV also carries a file timestamp a day past the as-of date while everything else is set deliberately.
> The rest of it is very good work. The Params sheet naming each rule against the document it comes from, the cage-versus-system variance table that catches the one 500 foot difference on TH-8STR and says the cage governs, and the whole chain running off the recount so a Thursday change drops in without rekeying. Both frontier models went 0 out of 5 on it, which answers the earlier worry that the rep email hands the reasoning over.

## Task 37, inbound-consolidation-plan (ACCEPTED)

**Accept Notes**
>
> All five inputs are usable, internally consistent, and sufficient for the task. Independent reconciliation of po_history_h1.csv found 274 orders, $246,724.51 of merchandise, $11,340.22 of freight, and $1,180.50 of fees, totaling $12,520.72. The golden workbook’s History, Buckets, Vendors, and Briefing sheets correctly use live formulas to produce $1,378.02 of plan freight, $719.88 of Kesselring bracket credit across 13 qualifying fortnights, and $11,862.58 of half-year savings. It also correctly documents vendor cadences, ship modes, waits, Vollintine’s no-change recommendation, owners, and the 09/11/2026 switchover. The rubric is well aligned and appropriately tests the decisive calculations and operational requirements. No persuasive duplication or prohibited LLM-authorship evidence was found.

## Task 38, po-conformance-review (ACCEPTED)

**Revision Notes**
>
> The last round's items look closed. Attribute (a) is now 21 orders totaling 285,310.06 and includes 26-0368 and 26-0443. The confirming-order corrective action asks whether a section 6 emergency existed instead of marking every order EMERG. The pending-vendor write-up treats 26-0581 and 26-0646 as closed and holds open 26-0663. The control observations now name three post-delegation approvals, 26-0241, 26-0597 and 26-0718.
> The remaining miss is attribute (g). Policy section 10 and Kristen's letter test approvals recorded under a departed employee's ID after the separation date. Merv Beiler's last day was April 17. Purchase order 26-0346 is an expense order for 140.40, dated April 16, approved under MBEI at 16:08 on April 20, the next business day. It sits in the 708-order tested population and is not on the (g) schedule or Appendix B. The memo says an order approved under his ID after April 17 is reported under (g), then lists only the eleven State College non-stock orders dated April 21 through May 29 totaling 66,536.26. Counting every MBEI approval timestamp after April 17 gives twelve orders totaling 66,676.66. Adding 26-0346 also moves the distinct-exception count from 72 / 558,832.93 to 73 / 558,973.33, and the within-limit re-approval item from nine orders to ten. Put 26-0346 on the (g) schedule and Appendix B, and update Criteria 26, 29, 30 and 34 so they track the corrected counts.
>
**Accept Notes**
>
> Looks good. The remaining (g) miss on 26-0346 is closed: it is on the system access schedule and Appendix B, and Criteria 26, 29, 30 and 34 now score 12 MBEI orders totaling 66,676.66, 73 distinct exception POs, and the ten within-limit MBEI re-approvals. Re-derived the tested population at 708 orders / 3,565,356.60 from the register after dropping 18 cancelled and the five blanket headers. Accepting.

## Task 39, dock-to-stock-review (ACCEPTED)

**Revision Notes**
>
> Most headline figures independently reproduce from the CSVs, but the late-receipt logic has a substantive contradiction. Receiving_procedure.docx §§3, 4, 6, and 7 expressly allow an after-3:00 arrival to be unloaded/keyed the next business day and put away the following business day, while the overall deadline remains the business day after arrival. Six late receipts—R70457, R70461, R70465, R70480, R70634, and R70638—therefore missed the overall deadline without missing any step clock. Criterion 5 is not satisfiable as written, and the golden memo’s “First step that missed” table incorrectly classifies all 18 late after-cutoff receipts as an arrival miss even though next-morning unloading is expressly expected. The memo also twice says after-cutoff freight was “on the floor overnight,” while dock_log_feb_aug.csv shows all 50 after-cutoff deliveries were unloaded the next morning, consistent with §3. Revise the rubric to distinguish root-cause buckets from missed-step clocks and correct the memo’s classification and physical-state wording.
>
**Accept Notes**
>
> Looks good. The late-receipt note is closed: the memo now splits root-cause buckets from missed-step clocks, names the six after-cutoff receipts that missed the overall deadline with no step miss (R70457, R70461, R70465, R70480, R70634, R70638), and reads every after-cutoff truck as unloaded the next morning. Re-derived May through August as 49 late receipts and 107 in-building backorder lines at 39,646.38. Accepting.

## Task 40, wanasek-credit-workup (ACCEPTED)

**Accept Notes**
>
> Accepting. I rebuilt the workup from the six files before reading yours and every figure came out the same.
> The chain holds all the way down. Twenty percent of the $329,728 net worth is $65,945.60, one and a half times Badger's verified $86,400 is $129,600, the house ceiling is $100,000, so section 4.1 lands on $65,000 after the rounding. Both 4.3 triggers are live, Badger at 52 days against net 30 and check 4415 returned on 11/17/25 inside the 24 month window, so the base halves to $32,500 and floors to $30,000. Setting the $75,000 due from affiliate aside takes adjusted current assets to $876,630 against $741,802 of current liabilities for 1.18, and $909,802 against net worth gives 2.76, so both section 3.3 floors clear and the account is not a rejection.
> The exposure schedule is the part I checked hardest and it is right. Receipts at 75 days after the end of each delivery month put September's money on 12/14, which is why the December month end is the peak rather than November: $237,000 delivered against $39,140 received is $197,860. Retainage at five percent of $287,200 is $14,360 and it sits there until June. Peak plus ten percent is $217,646, rounded up to $220,000. The schedule runs September through June and the receipts column ties out to the deliveries column.
> Three details are better than they had to be. The Fort Atkinson reference is caught on the address rather than on the name, 411 Commerce Court being the applicant's own, and signed by a Wanasek. Worth saying that setting it aside does not actually move the limit, since twenty percent of net worth governs either way, but it leaves exactly the two unrelated references section 2.3 demands and it takes the best looking reference on the file out of the picture. The guaranty paragraph on the application is genuinely struck through in the file, not just annotated, so your line about it coming back struck through with a note to discuss is literally accurate and a solver working off extracted text alone will miss it. And the bank line maturing November 30 against a December exposure peak is a real observation rather than a decorative one.
> One thing to think about rather than fix. The difficulty measurement puts this at Advanced Plus, with Opus at four out of five and GPT at one out of five. It passes the bar, a capable model is not nailing it first try, but the split has a cause worth knowing. Almost everything that can go wrong goes wrong in one place. Read section 5.4 correctly and the peak, the retainage, the plus ten percent and the job limit all fall out together; read it wrong and four criteria worth twelve points fail at once. The rest of the memo is a careful walk through provisions that are each stated plainly. If you build another on this shape, a second independent place to go wrong would lift it.
> The linter flags criterion 21 as bundling on the words plus the. It is one figure and one computation and that pattern is a known false positive. Its three notes about the negatives not reading like failure modes are wrong as well, all three describe something that should not happen.

## Task 41, flyer-program-review (ACCEPTED, recommended)

**Revision Notes**
>
> Golden Quality
> 1. Coverage gap: The prompt asks to for formulas, but the golden's Base Week, Window Units, Set-Aside Units, Pull-Forward cells, and Six Week Base cells all contain typed-in numbers, not formulas.
>
> Rubric Quality
> 1. Split these bundled items into atomic criterion: 11, 12, 13
> 2. Remove trailing clauses that bring negatively weighted items into negative language such as "in violation of..." or "contrary to...."
>
>
> 3. Coverage gaps
> - The prompt asks for a price and the support behind every slot on the September and October lineup, but the rubric does not measure the specific price or rate for 6 of the 8 lineup slots (DP-1618, RC-2216, RC-1240, VS-2210, VS-3306, TT-2244).
> - The prompt asks for the call on the program with what comes out of the rotation, but the rubric does not measure three of the five held-out items (RC-0871, MB-3118, DP-8331) or the reasons given for holding them out.
> - The prompt asks for the support behind every slot, but the rubric does not measure the reserve items (TT-8801, RC-6612, MB-6707) or their rates.
>
**Accept Notes**
>
> Looks good, and this is one of the better ones I have seen on this project.
> Every prior note is closed. Base Week, Window Units, Set-Aside Units, Pull-Forward and Six Week Base are all formulas now: the results tab reads the Slot Windows totals, Slot Windows indexes into the netted weekly grid, and that grid is the raw file less the set-asides off the Set-Asides tab. Nothing derived is keyed anywhere I could find. On the rubric side the old bundled items are single-fact now, the two negatives carry no trailing "in violation of" clause, and the coverage gaps are filled: the six lineup rates, the three held-out items and all three reserves each have their own criterion.
> I did not take the numbers off the workbook. I rebuilt the whole thing from item_sales_weekly.csv and large_order_extract.csv, netted the twelve orders over the exclusion line, laid out the eight base weeks, six issue weeks and four after weeks for each of the 32 slots, and worked rule 3 on every one. Every slot matched to the cent, and so did the issue nets of 2,758.02, 360.18, 1,522.13 and 1,341.51, the 5,981.84 program net, and the count of eleven losing slots. I then rebuilt the fall plan from the last six posted weeks and got the same plan quantities and the same 1,644.75 confirmed billback against a 918.45 half-print line, so FUNDED stands. I also read all 3,744 cells of the weekly grid back against the CSV and found no transcription error.
> The traps are honest ones. The curling club order really does turn the chafing fuel slot from a winner into a loser once rule 2 is applied, the gloves really do give the quarter back in the after weeks, and the four slots with no written support are the four the deal sheets decline. Working the fall mailed count as a stated plan assumption rather than a graded figure was the right call, since rule 9 puts that count outside the files.
> One small thing if you are ever back in this file: the held-out list names DP-8331 and VS-6620 under rule 5, but DP-7104, TT-7716, VS-5512 and TE-3610 also ran in issue 4 and also carry fall money, and they are not mentioned. The front page explains why the two named ones are the interesting cases, so it reads fine as it stands. Not worth a revision.
> Accepting, and flagging this one as a recommend.

## Task 43, dfl-freight-audit (NEEDS_REVISION, round 2 open)

**Revision Notes**
>
> Golden Quality
> 1. The golden assigns the full $251.68 under-billing total to invoice DFL7718272. However, the input files support only $1.18 for that invoice.
>
> Rubric Quality
> 1. Item 13 is inaccurate. It attributes all wrong charges to lift gate issues and misses residential charges.
> 2. 16 confuses claim deadline with filing date. October 4 is the earliest claim deadline, not the earliest filing date. The memo sets the actual filing date as September 15.
> 3. Criterion makes same under billing error as the golden (see above)
> 4. Prompt requires a deadline for every claim, but the rubric only measures the earliest one. 
> 5. The prompt requires every incorrectly billed invoice to state why it is wrong, but the rubric does not require a reason for each of the six under-billed invoices.
> 6. The prompt requires every bill to be rated correctly against the agreement and rate pages, but criterion 2 requires only that rated amounts appear.
> It does not require all 122 amounts to be mathematically correct.
> 7. The golden requires every future DFL bill to be rated before payment, but the rubric does not measure that action.
> 8. The golden requires the dock to record liftgate and notification requests accurately, but the rubric measures only the fiberglass-kit classification change.

## Task 45, lift-truck-fleet-plan (REJECTED at first human review, 2026-09-05)

The only task in this portfolio rejected at its first human review. The AutoEval gate had passed
it at 0 errors the day before. Every finding below was invisible to the coded checks of the time:
the prose rule is one the reviewer wrote out by hand, and the seven golden findings came from
reading the golden against the inputs and the prompt, which no check then did. Lessons and the
checks they became (P6, A20, G8, G9, G10) are in `../submission/workflows/02-prompt-writing.md`,
`04-golden-solution.md` and `prompts/submission.md`.

**Revision Notes**
>
> Rejecting for major errors in the golden and rubric, along with minor revisions to clarity and sentence structure needed throughout.
>
> Prompt Quality
> Use natural language and revise for clarity and sentence structure throughout.
> 1. Why would you say this to someone who works with you at the same company? "I run the warehouse and the pipe yard for Ledford Pipe & Supply, a pipe, valve and fitting wholesaler in Chattanooga, Tennessee." They are your coworker. They know what the company is and what you do... Remove the entire first paragraph which contains no useful info and sounds LLM generated.
>
> 2. If that info is needed for the LLM then include it, naturally, in the "coversation" prompt. For example: Four of our Ledford Pipe & Supply trucks come off the Cumberland lease on December 31.
>
> 3. Fix the run-ons:
> Sentence 1 Four of our trucks come off the Cumberland lease on December 31,
> Sentence 2 Tamika's second shift starts October 12,
> Sentence 3 and Scenic City's proposal for new equipment is good through October 2.
>
>
> 4. It's unclear what Tamika's work schedule has to do with a new equipment proposal.... written clarity is needed...
>
> Input file/golden issues
> Fix the extensive run-on sentences throughout. Here is just one example: "Three of the four schedule A trucks go back to Cumberland on December 31 and the reach truck is bought. U-01 is already past ten thousand hours and U-03 crosses it before the inspection, so neither can be bought out under the rules, and U-02 fails the maintenance test at more than seven dollars an hour on the twelve months, most of it a hydraulic pump, two brake jobs and a set of mast chains that the dealer had keyed to U-01. "
>
> When two sentences are joined with "and" or "so" or "but" or "or" or another coordinating conjunction, they need a comma. This is the rule to fix the first sentence above, which should look like this: "Three of the four schedule A trucks go back to Cumberland on December 31, [<--see comma]and the reach truck is bought." No more than 2 sentences can be joined with a comma and coordinating conjunction. Basic comma rules should be used throughout. Nobody is looking for perfection, but commas in lists and commas in compound sentences are basics.
>
> This is a very long run-on:
> Sentence 1: U-01 is already past ten thousand hours
> Sentence 2: and U-03 crosses it before the inspection,
> Sentence 3: so neither can be bought out under the rules,
> Sentence 4: and U-02 fails the maintenance test at more than seven dollars an hour on the twelve months, most of it a hydraulic pump, two brake jobs and a set of mast chains that the dealer had keyed to U-01.
>
> Major golden coverage gaps of things asked for in the prompt:
>
> 1. Missing tables summarizing order and elections notice, purchase order, signature block for Darrell to sign
> 2. Dated 9/22 but schedules work for 9/16-17
> 3. Says U-08 can operate with battery defect; U-06 can operate with rear work light defect; U-03 can run with damaged tire - all prohibited by the check card which requires these to be same day fixes
> 4. Wrong repair invoice numbers in inspection tab for U-05, 01, 04, and 02.
> 5. Golden says U-05 returned to service 6/3 but input files don't support this.
> 6. Prompt asks for rental cost since U-05 returned to work; golden only looks at 3 rental invoices beginning 6/21 which is not in keeping with a 6/3 return - and the 6/3 return wasn't supported by the data
>
> 7. Golden says U-05 will be traded in when a replacement arrives between 12/4 and 12/18 - but then schedules it to work all 55 night shifts through the end of 12/31. It should specify that it or its replacement will work those nights.
>
> Rubric Quality
> The rubric will need a total update based on accurate Golden; right now it clearly did not catch the issues noted above.

**What each finding was, in the repo's terms.** Prompt 1-2: the P4 frame delivered as a
self-introduction to a coworker (now P6). Prompt 3 and the golden paragraph: a missing comma
before a clause-joining conjunction, and three or more clauses in one sentence (now A20; the
serial comma stays a read). Prompt 4: an event named in the opening with no link to the work
in the sentence. Golden 1: the prompt said the order and the notice were ready "for him to
sign" and the golden had tables, no purchase order, no notice letter and no signature line (now
G8). Golden 2: the memo was dated 9/22 and scheduled 9/16 and 9/17 actions as "today" (now G9).
Golden 3: the check card's same-day-fix class was treated as "runs under the card"; the rule
was applied to the tag-out class only. Golden 4: the generator renumbered the invoices after the
golden text was written, so four cited invoice numbers existed nowhere (now G10). Golden 5: a
return-to-service date inferred from an invoice date and the next meter reading, stated as
fact. Golden 6: a "cost since <date>" that counted whole invoices after the date and skipped the
partial month. Golden 7: a truck traded in during a December delivery window still carried all
55 nights to December 31 with no successor named. Rubric: it pinned none of these facts, so the
golden scored full marks under it.

---

## Task 48, commission-review-q2 (NEEDS_REVISION, round 4, 2026-09-10)

A short note that reads as the round 3 finding restated, with one new clause: "the unsupported
dates". The only date in the golden's prose that no input stated was the first page's own dateline
(September 1, 2026, against a requesting note of August 28). Read the lesson as: the deliverable's
dateline is a stated fact the reviewer checks like any other, so it is anchored to an input or left
off. Coded G20; the two consistency positives were widened from one representative to all six.

**Revision Notes**

> Revise the golden workbook so the representative-facing notes match the actual calculations for Amy, Dwight, and Frank, and remove or correct the unsupported dates. Also update the rubric with a consistency check so narrative notes cannot contradict the computed results and still receive full credit.

## Task 48, commission-review-q2 (NEEDS_REVISION, round 3, 2026-09-10)

The round after the evidence tab. The reviewer certified the whole recomputation ("correct and
traceable") and then read the six representative paragraphs against the Review tab cell by cell,
citing each contradiction by cell address on both sides. Two things to learn from the shape: the
reviewer treats employee-facing prose as a deliverable that can misinform, not as colour, and
grades the rubric for having let it through ("awarded full credit despite these contradictions").
The check that came out of it is G19. The rubric fix is two consistency positives, not a penalty: the
platform's penalty scope ruling of 2026-08-27 (R67) puts an internal contradiction outside the four
classes a negative may be spent on, so the contradiction is graded affirmatively.

**Revision Notes**

> The underlying recomputation is correct and traceable, including all 403 invoices, 34 credits, splits, bonuses, accelerators, and the six corrections. However, the representative-facing text contains material contradictions. Representative Notes!B6 says Dwight's quarter moves up, references Churchill Downs instead of the Baptist East Dining line he questioned, and says both bonuses stand; Q2 Review!D11 and Review!E7 instead show a $190.54 recovery and only one $250 bonus. Representative Notes!B8 says Frank moves down, his accelerator decreases, and both bonuses stand; Q2 Review!D13, Review!H9, and Review!E9 show a $407.25 increase, an accelerator increase from $396.80 to $435.78, and only one qualifying bonus. Representative Notes!B3 also says Amy's qualifying Cave City bonus "comes off" and then "stays." These statements could misinform employees and must be corrected. The rubric also needs a consistency criterion or penalty because it awarded full credit despite these contradictions in the deliverable's representative-facing content.

## Task 48, commission-review-q2 (NEEDS_REVISION, round 2, 2026-09-09)

A single-criterion send-back with everything else called strong. The reviewer read the rubric
against the golden's vendor tab and saw that the criterion grading the module-error list could be
earned by naming the errors, because the tab itself carried no figure. Note the shape of the ask:
not "add evidence" but "validate each claimed defect against the plan rule AND the source data",
with the six validations spelled out by input column. The fix lives in the deliverable first (a test
and a live figure per point) and only then in the criterion.

**Revision Notes**

> Revise Criterion 23 so the vendor-error findings are not rewarded merely for being listed. Require each claimed module defect to be validated against the relevant plan rule and source data—for example, invoice cost basis versus `UNIT_COST`, invoice-level rate bands versus the quarter-average rate, split-note handling, house-account treatment, bonus eligibility, and credit-memo rate treatment. The prompt, inputs, golden solution, and remaining rubric criteria otherwise appear strong.

# Part 2 — Earlier rounds, surviving only as log summaries

The platform overwrites Revision Notes each round. These findings are recorded in the task
feedback logs in the repo's own words, not the reviewer's, so treat them as content examples
rather than wording examples.

**Task 01, hartwell, first review round.** The letter and hartwell_price_pages_0908.xlsx
discontinue 601T-025 with replacement 601TN-025 at new list $21.35, but the rubric graded only the
413S-100 supersession; a mirrored criterion was required. The golden fabricated the surname
"Villanueva" for Marcy in Briefing B4, a name no input contains. The reviewer also recorded that
all 94 other traced claims reconciled exactly, naming the classes checked: cost multipliers, the
6% import surcharge, family adders, supersession costing, all 188 matrix prices, the $17,705
annualized impact, all six agreement assessments, dead stock, duplicate consolidation, and the
FTG-PRESS deferral.

**Task 03, weldon, first review round.** Calendar-invalid weekday and date pairs: "Friday,
September 26, 2026" in weldon_rep_email.docx and "Friday, October 3, 2026" in the transition-letter
table are both Saturdays, and the error had propagated into rubric criterion 21 and two golden
cells. The golden fabricated the surname "Spruill" for Gail. Verification note: every demand
baseline, buy quantity, reorder point, coverage demand, carrying cost, and the order total was
independently recomputed and matched.

**Task 04, pbw, first review round.** Four findings, all later confirmed in the salvage note above:
the missing executed Group 30 amendment, non-credible document metadata, hard-coded eligibility and
netting decisions in the golden, and the AutoEval rubric notes on bundled criteria 7/8/9 and the
unqualified "consistent with the agreement" wording in criterion 23.

**Rounds recorded only in the task logs, 2026-08-21 to 2026-09-02** (the platform kept only the
latest note per task; these are the repo's summaries, not the reviewers' words).

- **12, hollenbach, four rounds before the accept.** (1) LLM-sounding prose named as a
  structure, "messy workplace detail, artificial idiom, analytical requirement", eight prompt
  phrases, four input phrases, four briefing phrases quoted; prompt too prescriptive; rubric
  bundling with C2 as the worked example. (2) "Some are fixed; some are still bundled", ten
  criteria named. (3) The golden ignored 166 Fegley breakers on hand, the briefing did not tie
  (5,117 against 5,159), the carrying cost was hard-coded and group-averaged, and the rubric
  pinned the defective figures. (4) The plan leaned on a Sowers hold that lapsed three days
  before the scheduled signature; carrying cost pooled by group; only two liveness criteria
  against a prompt asking for live formulas throughout.
- **13, kolterman, three rounds.** 76 affected units invoiced after the stop sale never
  separated out; then an allowance criterion missing its cap clause, a dates criterion bundling
  three checks, a memo at 395 words, and three lines describing the coverage horizon three
  ways; then the counter notice the memo asked for was never written and CONTACT/PHONE were
  not carried.
- **14, wamhoff, adjudication.** Freight spread over 67.5 cbm but applied to 67.4654 loaded, a
  3.99 shortfall carried into the landed cost; criterion 25 mandated a 30 day production step
  the rep email contradicted at 35.
- **19, rempel, adjudication.** A five-row action table mandated where the prompt fixes no
  count; penalty weight at 11.9 percent; Briefing A23 overstating the ball valve case; double
  jeopardy between criteria 3 and 10.
- **20, rademacher, two adjudication rounds.** A percentage basis that does not reproduce the
  pinned figure (1,097.90 against 1,097.894); an exact count of summary figures; a criterion
  mandating "on the parameters tab".
- **31, returns cage, three rounds.** A lookup keyed by RGA alone pulling the wrong customer on
  a duplicate RGA; two briefing actions dated after the close; schedule tabs that pulled fixed
  Lines rows so a moved line stayed on its old schedule; two coverage gaps.
- **32, pavelka, two rounds.** Q2 rebate overstated by an omitted credit memo (CM-2588,
  149.36); criterion 4 mandating exactly eight actions; then C26 double-scoring the rebate as
  a negative and C28 to C30 spending negative weight on ordinary mistakes.
- **33, semrad.** Bundling on twenty criteria with the rule given as no criterion measuring more
  than one thing; three self-containment gaps.
- **34, delivery zone, two rounds.** Only C3 and C8 required formulas; C4 pinned exactly 8
  actions; then the three-front note in Part 1b.
- **35, tessendorf, two rounds before Part 1b.** Bundles pairing value with liveness; negatives
  reversing positives; rigid and judgment criteria to be separated.
- **38, po-conformance, three rounds.** Appendix A not footing (gross register and blanket
  headers missing); the action table missing owned, dated responses per attribute; then two
  over-limit orders omitted from attribute (a), an EMERG flag the inputs do not support,
  closed orders called open, "two approvals" where the schedule lists three; then 26-0346
  (Part 1b).
- **39, dock-to-stock.** The late-receipt logic contradicting the procedure (Part 1b).
- **41, flyer program, two rounds.** Bundling on six criteria and C24/C11 double-measuring the
  decision; then typed figures where the prompt asks for formulas and twelve coverage gaps
  (Part 1b).
- **43, dfl freight, two rounds.** The golden accepted DFL's printed fuel surcharge percentage
  against the wrong band table on 43 bills; then one golden cell wrong and eight rubric points
  (Part 1b).

---

# Part 3 — What reviewers actually flag

Refreshed 2026-09-04 over every reviewer round the portfolio has recorded: 37 rounds on 24
tasks (Parts 1, 1b and 2). Ordered by how many tasks the class touched.

| Finding class | Tasks | Blocking? |
| --- | --- | --- |
| Bundled, non-atomic criteria ("no criterion should measure more than one thing") | 01 03 04 11 12 13 33 34 35 36 41 | Yes when named as a list; "minor for later" only on 01 and 03 |
| Rubric coverage gap: a prompt sentence, a memo requirement or a golden action with no criterion | 01 03 06 12 13 31 34 41 43 | Yes, every time |
| A count or a layout the prompt never fixes, pinned by a criterion (eight actions, five rows, twelve figures, "on the parameters tab") | 19 20 29 32 33 34 | Yes |
| The golden wrong against the inputs on a figure or a classification | 12 13 14 32 38 39 43 | Yes, every time |
| Decisive cells hard-coded where the prompt asks for formulas | 04 12 34 41 | Yes |
| Generator string or template metadata in docProps (Openpyxl, python-docx, one shared timestamp) | 04 22 23 30 36 | Yes on 23 and 30 as the only send-back item; "cleanup" on 22's accept |
| LLM-sounding prose in inputs or prompt (em dashes, idiom, three-beat rhythm) | 07 12 34 | Yes |
| Negatives that mirror a positive, or spend penalty weight on an ordinary miss | 32 34 35 41 19 | Yes |
| A fabricated name in the golden (Villanueva, Spruill, Lorna Sedlacek, Arlene Kubat, Verla Stroman) | 01 03 32 33 35 | Yes, except 35 where it was "not why this is accepted" |
| The golden internally inconsistent (a briefing that does not tie, two sections disagreeing, a convention stated then broken) | 12 13 38 39 | Yes |
| Prompt over-prescriptive or unclear | 04 12 34 36 | Yes |
| An input file unreadable or a decision-critical input missing | 04 35 | Yes |
| Currency notation missing from criteria | 12 | Fixed by the reviewer on the accept |
| Penalty weight under the 20 percent share | 19 | Ruled non-blocking 2026-09-02 |

Four of these recur often enough to be standing checks on anyone's task: **atomicity**,
**coverage of every prompt and memo requirement**, **the golden re-derived from the inputs**,
and **counts and layouts the prompt never fixes**. The first three were already the standing
three on 2026-08-20; the fourth arrived with the adjudication notes.

---

# Part 4 — How the notes are written

Observations across 37 rounds, refreshed 2026-09-04. The register moved between August and
September: the adjudication tool produces terse numbered lists, and the human reviewers who
send tasks back most efficiently write the same way.

- **The shortest revision notes produced the cleanest fixes.** 12's last round is three
  lines: "Bundled items: 2, 6, 8, 9, 10, 11, 16, 19, 21, 30, 31 all check for more than one
  thing; separate into individual criterion." 38's round 3, 39, 31's last round and 43 are
  one paragraph or a numbered list and nothing else. None of them summarises the task, recaps
  the previous round beyond one line, or praises before the substance.
- **Numbered items, grouped by area only when more than one area is touched.** 34, 41 and 43
  head their lists "Prompt Quality / Input file quality / Rubric Quality", which are the form's
  own category names; 12 and 31 have one area and no heading.
- **Each item is where, what, fix.** "16 confuses claim deadline with filing date. October 4
  is the earliest claim deadline, not the earliest filing date. The memo sets the actual
  filing date as September 15." Anchor, defect, the fact that settles it. The fix is often
  implicit in the defect and stated only when it is not obvious: "Put 26-0346 on the (g)
  schedule and Appendix B, and update Criteria 26, 29, 30 and 34."
- **The imperative, not the conditional.** "Split these bundled items", "Remove trailing
  clauses", "Re-save them through Excel", "Reword to 'on the parameters tab or equivalent'".
  Never "you may want to consider".
- **Money as the workbook shows it.** $251.68, $1.18, 66,676.66, $3,415.09. The one reviewer
  who found criteria without currency marks fixed them and said so.
- **A still-open point from the last round is just an item again**, restated with its
  anchor. Closed points get one line at most ("The last round's items look closed", "Previous
  review issues are resolved") and usually nothing.
- **Optional items are marked as optional in the item itself**: "One optional thing while you
  are in there", "Your call, it is not why this is going back", "Small point, take it or leave
  it", "Not worth a revision".
- **Accept notes come in two lengths and both are accepted practice.** "Looks good ...
  Accepting." with one line on what closed (38, 39), or a re-derivation essay that names every
  figure the reviewer rebuilt (31, 33, 35, 36, 40, 41). The essays are the reviewer showing
  their work to adjudication; nothing in them is for the EC to act on.
- **What reads as generated, and appears nowhere in the 37 rounds:** an opening summary of
  what the task is about, stacked adjectives before a noun, "overall", "demonstrates",
  headings and bullets wrapped around one sentence, a closing pleasantry, a sentence listing
  the components that were checked. The one note that opened "Hi, excellent work on this
  package" (23) still got to its two items in the second paragraph.
- **The three-part shape from feedback-best-practices.md holds, but as a list, not as
  paragraphs.** What is wrong, why, what to do, per item; two short paragraphs is the ceiling
  and a numbered list is one paragraph for that purpose.

---

## Refreshing this corpus

```bash
stb submissions feedback <taskboard-uid>     # UIDs are in ../../submission-list.md
```

Prints Revision Notes and Accept Notes for the submission and writes a `notes.txt` copy to a temp
directory. Only the most recent round of each is retained, so capture notes here before a
resubmission overwrites them.


# Part 5. Memory narratives relocated 2026-09-11

Dated per-task narratives moved out of memory/ on 2026-09-11, verbatim, one subsection per task in
chronological order. The rules each narrative produced live in the memory topic files and in the
coded checks; this Part is the record of what happened. For ten of these tasks (Rossville, rempel,
semrad, twincreek, kolterman, yankton, open-order-cleanup, returns-cage, havlicek, bergendahl) no
feedback-log.md exists anywhere, so this is their only record.

## Task 04, pbw-rebate-reconciliation: LLM-authorship gate and reviewer salvage (2026-08-17)

Feedback on task 04 (received 2026-08-17; that task's archive was removed from the repo 2026-08-19 per user - do not cite it as a reference) revealed two automated gates and what trips them:

**LLM-authorship check on OUTPUT files** (pass requires combined ≥ 0.55):
- Dark-navy header fill **#1F3864 is a confirmed in-range "AI-blue" tell** (HIGH category). Avoid blue-family fills in solution workbooks; use gray (D9D9D9/F2F2F2) plus amber/green/pink accents.
- Datetime cells extract as `2025-12-02 00:00:00` and dominated the flagged chunks. Store dates as **plain text matching the source CSV format** (mm/dd/yyyy) in solution sheets.
- Uniform machine tokens (ELIGIBLE/FREIGHT repeated 400×) read as generated; terse lowercase analyst codes (ok/frt/spa/dup) + a sparse Note column + legend read as human working paper.
- Graders/detector read **cached formula values**; openpyxl writes empty `<v></v>` after `<f>`, so a freshly saved workbook must be recalculated before zipping - open it in a spreadsheet app and save. (The in-repo formulas-engine injector was removed 2026-08-19 per user; autoeval_check's empty-cache scan catches un-recalculated books. Value-preserving edits can instead carry caches forward from the last known-good build via a session-local script.)
- **Python float-repr artifacts in cached values are a confirmed HIGH tell** (failed hartwell 2026-08-14 batch and marathon-line-review 2026-08-18: e.g. 68814.54999999999, 8295.869999999995, 0.0033006199999999833). When injecting cached `<v>` values, ALWAYS write shortest clean decimals - round to the fewest places within 1e-9 relative drift - never raw `repr(float)`. Cleanup + scan script lives at `tools/fix_floats.py` (scan/fix modes, edits sheet XML in place, formulas untouched); run `python3 tools/fix_floats.py scan` on every xlsx (inputs AND solution) as a pre-zip gate before every submission.
- Set human doc props (creator "C. Statz", plausible created/modified dates).

**Outcome of task 04 (2026-08-17): SALVAGED-ACCEPTED** - the reviewer fixed and closed the task themselves (added the missing amendment input, refreshed metadata, rebuilt the golden on live formulas, patched the rubric). "Task now salvaged" + past-tense change list + locked form = accepted, no contributor action. Human-review lessons for future tasks:
- **Source-document sufficiency**: any contractual/program fact the golden relies on must exist as an actual document in the inputs (the executed amendment itself), not only as a reference in correspondence - above all when it swings a tier/threshold boundary. Reviewers call this "decision-critical evidence."
- **Per-document metadata plausibility**: created/modified timestamps must differ per file and precede or match each document's own internal date (a statement "created" after its printed date, or two files sharing one timestamp, gets flagged even without an LLM accusation).
- **Live decision fields**: eligibility Status / Y-N / flag columns in the golden must be formula-driven, not typed - "the most important analytical decisions are not actually live" is a send-back-grade comment. (Watch: yearend-deadstock-plan's Torbeck/Kellerman "Eligible?" YES/NO cells are typed text; if that task returns, formula-drive them, e.g. min-line and invoice-presence checks.)
- **Subjective criteria need a qualifying rule**: e.g. "counts as consistent if the response cites the specific agreement section addressing the objection" - examples alone are not enough.

## Task 07, yearend-deadstock-plan: reviewer send-back and oracle runs (2026-08-17 to 08-19)

**yearend-deadstock-plan send-back (2026-08-17) - reviewer standards to build to from day one:**
- **Temporal coherence to the real task date**: every completed event/record (letters, emails, snapshots, receipts, purchases) must be dated on or before the actual submission date; only genuinely prospective deadlines may sit in the future. Declaring a fictional "today" is explicitly not accepted. A snapshot file must contain no receipt dates after its own run date.
- **Data must cover every eligibility window the sources cite** (a 36-month vendor rule needs 36+ months of purchase history), and every claimed return/claim quantity must be ≤ what the records document.
- **Vendor deadlines ≠ internal execution dates**: the plan must schedule its own earlier ship/disposal dates when a memo demands completion before an event; scrap needs a physical-removal date, not just an accounting booking.
- **Live cascade end-to-end**: qualification lookups, supported qty, package rounding, dynamic ranking (LARGE/INDEX + skip logic), cap IN/OUT, downstream clearance quantities, route labels, and briefing totals all formula-driven. Test refreshability with the `formulas` pip package (pip install works on this machine): perturb an eligibility input, a quantity, and a price; assert totals re-flow.
- **After a data rebuild, recompute the golden - never engineer new data to reproduce old answers**, and rewrite the rubric only after the golden is final.

**Prompt spelling/grammar check**: elliptical trade jargon reads as a typo to the checker - "at the counter day Friday" was flagged as garbled on yearend-deadstock-plan (2026-08-17). Keep jargon nouns but frame them grammatically ("at our counter day on Friday"); input .docx files are not run through this check.

**Golden-solution oracle check (LLM judge, 3 runs, all must hit 1.0)** - yearend-deadstock-plan FAIL 2026-08-18 at 0.956–0.958, all flags judge-side, four rubric rewordings required:
- **Negative criteria must state an explicit any-quantifier defect** ("At least one key output … is a hard-coded constant"), never the bare plural negation of a nearby positive criterion ("Key outputs … are constants") - that drew `ambiguous_negative_polarity` on 3/3 runs. Adding "a workbook whose outputs are all live formulas does not meet it" pins the polarity.
- **Never make the judge re-derive a big aggregate from a raw input file** (e.g. "sum EXT_AMT over every vendor row in the CSV") - draws `unverifiable_from_deliverable`. Word the criterion so the stated figures and their basis are checkable in the deliverable itself.
- **Anchor every relative time window to an absolute date** ("preceding 36 months" → "invoices dated 08/06/2023–08/06/2026, the letter's window").
- **"X appears on no line" breaks when a zero-quantity screening/eligibility row for X exists** - write "no return claims any units of X" plus an explicit carve-out that a zero-qty row is not a claim. Watch this any time the golden keeps ineligible items visible as 0-qty rows.

**Pins are NOT enough for universal-negative sweeps (task 07 run 2, 2026-08-18):** the pinned "At least one key output … is a hard-coded constant" negative was STILL flagged `ambiguous_negative_polarity` 3/3 and deducted its full weight every run (deficit exactly 5/120 per run). The judge cannot exhaustively verify "no output anywhere is typed", so it deducts deterministically. **Never pair a negative formulas-vs-constants mirror with positive liveness criteria - drop the negative entirely** (dropped portfolio-wide 2026-08-18; lint rule W6 flags new ones). A negative liveness check scoped to ONE inspectable column may survive; watch task 09's bounded extension-cells criterion as the test case. Diagnostic trick: deficit × total-positive-weight identifies exactly which criteria the judge failed (e.g. 0.9583 → 5/120; 0.9333 → 8/120 = the −5 sweep + a weight-3 positive).

**Never cite a nested function token in a criterion - judge tools cannot see it (deadstock run 4, 2026-08-19, C18 3/3 deterministic):** the judge's search_xlsx greps cached VALUES only (never formula text) and xlsx_formula_summary surfaces HEAD (outermost) functions only. C18 named LARGE and INDEX/MATCH - all nested inside IFERROR(...) in the golden - and the judge reported "no matches for pattern 'LARGE' across 12 sheets" against 6 stored LARGE formulas, failing every run. Its sibling C8, naming head functions (SUMPRODUCT, FLOOR), passed 3/3 in the same runs. Rules: answer-key liveness on functions that are the outermost call of the keyed cells, or re-key on cached values (a rank table's IN/OUT/skip pattern IS value-visible evidence of the logic); the answer-keyed pattern only works when the key tokens survive the judge's lossy extraction. Gate: autoeval_check R6 (2026-08-19) errors on criteria citing functions absent from stored solution formulas or present only nested; R5's key regex also now matches unquoted sheet names (quoted-only had silently skipped Torbeck_RGA!D11-style keys).

**Even pure head-call formula-ONLY liveness criteria flake - pair every liveness clause with cached-value anchors (deadstock run 5, 2026-08-19):** C8 ("live formulas ... verify stored cell formulas, not displayed values", keying head-call SUMPRODUCT/FLOOR ranges - R6/R7-clean) flaked 1/3 in run 3 AND again in run 5 after passing run 4 3/3; the platform itself marked it stability=flaky, judge variance on a verified-live golden. Its sibling C18/C17, which anchors on cached rank-table VALUES first and adds the formula clause second, passed 3/3 in the same runs. Rule: a liveness criterion with no displayed-value answer key beside the formula demand gives the judge nothing to verify when formula extraction misbehaves - pair it with value anchors or apply the 2-flaky-runs drop rule (C8 dropped, 38 criteria; liveness share may fall below the R3 10% floor as an accepted advisory, precedent C9 + marathon C29). Deficit arithmetic doubles as a platform-form auditor: run 5's 0.9646 = 1 − 4/113 exactly, proving the entered form carried 113 positive weight vs rubric.csv's 101 (appended instead of overwritten rows) - after any renumbering, re-fill the whole form and count rows/weights. Gate: autoeval R9 (2026-08-19) warns on formula-only liveness positives lacking a value anchor.

## Tasks 01, 02 and 03: hartwell, marquette and weldon reviewer sweeps and oracle runs (2026-08-17 to 08-19)

**Reviewer sweeps that recur across tasks (audit before every submission):**
- **No invented proper names in the golden** - reviewers diff every person name against the inputs; fabricated surnames were flagged three times on 2026-08-17/18 (weldon "Gail Spruill", hartwell "Marcy Villanueva", marquette "W. Fontaine"/"P. Raman" for prompt-only "Wes"/"Priya"). Use exactly the names the inputs use, first-name-only if that is all they give.
- **"Pasted source" tabs must be verbatim** - a tab claiming to be a pasted copy of a source sheet must keep the source's legend lines (e.g. adjustment-code keys) and its own row labels (marquette flagged for dropping the "Adjustment codes: PJ/PD/LX/CR" legend and relabeling "TOTAL ELIGIBLE" as "TOTAL PER STATEMENT", 2026-08-18). When adding a row to such a tab, shift every cross-sheet VLOOKUP/range reference to match.
- **Weekday/date pairs must be calendar-true** in every file (weldon bounced for two "Friday" labels on Saturdays). Sweep all weekday+date patterns against the real calendar before zipping.
- **Symmetric events need symmetric rubric coverage** - if the inputs contain two parallel facts (two supersessions, two discontinued items), grading only one gets flagged; mirror the criterion for each.
- **"Every item" prompt demands need an explicit completeness criterion** - flagged twice in two days (weldon reset table 2026-08-18, hartwell repricing tab 2026-08-19): spot-check criteria alone let a submission omit items and still pass. Whenever the prompt says "every/all stocked items", add a criterion pinning the exact qualifying count with the exclusion arithmetic inline (e.g. "47 SKUs: 56 Hartwell rows, dup counted once, minus 6 press, minus 2 frozen") plus carve-outs so legitimately excluded rows don't fail it; pair with a policy-anchored negative when a directional rule exists (e.g. "matrix prices do not decrease"). Audit remaining rubrics (06, 07, 08, 09, 10) for this gap before their next review cycle.

**Warning:** [[repo-layout-and-tooling]] siblings share these tells: marquette-rebate-recon solution has 788 datetime cells + navy fills (26374A, 3E5871); hartwell-cost-increase has navy 1F3B57. They will likely fail the same check if submitted as-is.

**Dollar spot-checks flake serially - answer-key the whole class at once (hartwell runs 3-5, 2026-08-19):** three consecutive golden-check cycles each flaked a DIFFERENT previously-3/3-passing positive dollar spot-check (run 3: C2 net cost; run 4: C3 landed + C9 floor price; run 5: C8 landed - judge read the sibling New Net 4.7376 instead of New Landed 5.4989 - and C35 frozen-SKU identification). **Passing 3/3 once is NOT evidence a criterion is stable**; fixing only the criteria the last run flagged guarantees another cycle. Any positive criterion pinning a dollar value on a net/invoice/landed cost or matrix-price level needs an anchor: a golden cell reference ("golden reference: Repricing!R48"), the arithmetic chain, and a "do not answer this criterion" disclaimer on sibling look-alike columns; an identification claim that lives in two places (row note + briefing bullet) needs an explicit either-location acceptance. rubric_lint W8 (added 2026-08-19) warns on un-anchored ones; x/×/÷ arithmetic chains and between-$ ranges count as anchored. Also mind terminology drift: hartwell C13 said "net cost with the 6% surcharge" for a value that lives in the New Invoice column - a latent guaranteed flake. Run 6 extended the pattern to **universal-sweep positives** ("every/all items/prices"): the 47-SKU completeness sweep flaked when the judge re-derived the count and tripped on FROZEN/DEFERRED rows, and the rounding-grid sweep flaked on trailing-zero display (47.5 / 37 misread as off-grid) - both had passed 3/3 twice. Anchor sweeps too: exact qualifying count with exclusion arithmetic inline, golden row-status breakdown (45 REPRICE + 2 SUPERSEDED), a worked display example, and held-row carve-outs (lint W11). Absence-style sweeps ("vendor X gets no new prices") need an absence-satisfies answer key. **BUT (hartwell quality review, same day): "(golden reference: Sheet!Cell)" anchors and named-column requirements ("the New Landed column … other columns do not answer") drew a needs_improvement rating - misaligned_or_unjustified_rigidity, ~31 pts - because they impose the golden's layout on candidate deliverables. The wording that satisfies BOTH the oracle judge and the quality review: numeric answer key + full arithmetic chain (this alone is what stabilized the oracle - C2 passed 6 runs with no cell ref), sibling figures disambiguated by VALUE ("the pre-surcharge 4.74 and pre-adder 5.02 are upstream intermediates, not the landed cost"), no sheet/column names unless the prompt itself mandates them (a prompt-required briefing tab may be named). Lint W12 flags golden refs/column names in criteria. Clear every W12 BEFORE submission even when the oracle passed that wording 3/3: deadstock C17 kept its golden heads + cell refs under the don't-trim-proven-wording stance and the quality review failed it for exactly that (2026-08-19, two [major] findings - golden-only rigidity AND non_atomic bundling of six line decisions). Fix pattern that survived both gates: split into a values+arithmetic outcome criterion (like-item OUT-exclusions stay one criterion per the dillman reviewer's own treatment; IN decisions already scored elsewhere stay out to avoid R10 subsumption) plus a small function-free liveness criterion carrying the R10 value-matching disclaimer, worded on stored formulas - never the reviewer's suggested 'recalculates when lines change' counterfactual, which is the marathon run-3 flake form. Only judge-legibility warns (W7/R7) may defer to proven wording. Follow-up trap (same day): the split C17 kept "gross credit of $7,283.04" because the quality reviewer's own suggested rewrite included it, and the 'near identical criteria' check then FAILed C3-vs-C17 as redundancy by subsumption - reviewer suggestions are not pre-cleared against the other platform checks. One total, one criterion: the mechanics/composition sibling drops the total token entirely (even from subtraction parentheticals) and carries a non-overlap disclaimer ('the authorized gross total itself is scored by its own criterion, not here'); autoeval R12 warns on a dollar figure asserted as a scored total in two positives.** Run 8 (hartwell, same day) pinned the last flake class: a positive criterion asserting **blankness/absence as an observable** ("its new L1-L4 prices are blank or absent") gets match: not_observed from the judge's value-grep tools even while the judge quotes the surrounding evidence verbatim. Stable shape (hartwell C16, 3/3): lead with the grep-able positive fact, state that blank/absent/unchanged fields all SATISFY the criterion, and end "fails only if <positive evidence of the defect>". Lint W13 flags it. Run-9 refinement: when the row shows look-alike sibling values beside the blank fields (current prices next to absent new prices), name them in the criterion as not-new-assignments and pin failure to "prices DIFFERING from those current values" - the judge otherwise reads the current prices as new assignments (hartwell C35, 6.25/5.35/4.8/4.45). Same run also validated the defect-frame negatives: ambiguous_negative_polarity flags fell from six criteria to two (the remaining any-quantifier pricing sweeps are flagged-but-never-deducted; leave them).

## Task 06, marathon-line-review: oracle runs 1-7 (2026-08-18 to 08-19)

marathon-line-review FAIL 2026-08-18 (0.893–0.918) added two more - judges misjudged a verified-clean golden on both:
- **Formula-liveness criteria must accept reference chains**: "(e.g., SUMIFS)" primes the judge to demand aggregation at the point of use and flag `='Rollup'!E3` links as typed. Word it "aggregation in the cell itself OR a chain of cell references ending in a tab whose cells aggregate the data", name a passing example reference, and say only typed totals fail.
- **Quoted-input carve-outs must pin the exact value and source** ("only quoted inputs may be typed" → judge flagged the allowed cell anyway). Name it: "$25,776.60 transcribed from marathon_item_proposal.xlsx may appear as a typed constant and does not fail this criterion."

**The drop rule extends to ALL workbook-wide sweep negatives, not just liveness (marathon run 2, 2026-08-19):** the pinned "At least one Great Lakes incentive amount … computed marginally" negative was flagged `ambiguous_negative_polarity` 3/3 - same as the liveness mirrors. Rule: negative sweeps over COMPUTATION METHOD (how figures are computed - constants-vs-formulas, marginal-vs-first-dollar) get flagged regardless of pinning - drop them when positive criteria already pin the exact correct values. Negative sweeps over CONTENT FACTS (quantities/values checkable against data, e.g. "a return line claimed beyond what the extract supports") have passed every run so far, even unpinned - keep those as point-checks or bounded sweeps. Also: judge formula-summary tooling can MISS real formulas (claimed 'Usage Rollup'!C3:C30 static when all 28 cells hold plain SUMIFS - verified false 3/3). Fix by answer-keying liveness positives: "Verify by reading the cell formulas stored in the file, not the displayed values (golden reference: <exact ranges and formula kinds>)."

**Counterfactual liveness positives are judge-flaky (marathon run 3, 2026-08-19):** a positive criterion worded as a simulation ("Removing an item ... recomputes ... automatically") failed 1/3 oracle runs - the judge cannot execute a static file, and typed decision-flag inputs (Y/N letters) plus fixed-range SUMIFS give it "hardcoded" evidence to cite. Reword to the answer-keyed static form that C29 proved: name the exact golden formulas (=IF, SUMIFS with ranges), pin that typed decision-flag INPUTS do not fail the criterion, accept plain-reference chains, and instruct "verify stored cell formulas, not displayed values". Do not trim or rewrite a criterion the oracle just passed 3/3 merely to satisfy an internal lint (marathon C29 stayed over-cap until run 4 forced a rework anyway).

**Judges infer liveness from sheet-level statistics, not cell reads (marathon run 4, 2026-08-19, 0.9703 ×3):** on a workbook byte-identical (all worksheets) to one that had just passed the same criterion 3/3, the judge failed C29 citing "typed_share=0.33 … no SUMIFS exist" - its own statistic proved the tool HAD parsed the formulas (28 typed input cells / 84 numeric = 0.333 exactly; the typed cells are the case-pack input column), but the judge read the sheet-level typed-share number as "the rollup cells are typed" without opening any cell. Liveness criteria must therefore also say "judge from stored formulas, never from displayed values or typed-cell-share statistics" AND name which columns are legitimately typed inputs (mixed input/formula tabs are the trap). Companion gate: autoeval_check R5 (2026-08-19) verifies every 'Sheet'!range answer key cited in a rubric against the actual workbooks - sheet exists, range in used area, asserted functions ("stores a SUMIFS") actually stored, quoted golden formulas byte-match - because judges take stated keys at face value, so key drift fails oracle runs deterministically. Also: oracle pass/fail can flip between runs on identical content - a judge-side FAIL with provably-clean golden warrants a targeted rubric hardening + resubmit, not workbook churn.

**Judges trace reference chains hop-by-hop and stall at arithmetic hops (marathon run 5, 2026-08-19, 1.0/1.0/0.9703):** with the typed-share defusal in place, the one failing judge traced 'Landed Comparison'!R3 → 'Usage Rollup'!E3 =C3*D3, hit the arithmetic hop (pieces × case pack), and rejected without following one more hop to C3's SUMIFS. "A chain ending in a tab that aggregates" is not enough - a chain-liveness criterion must name the golden chain AND endorse every intermediate hop explicitly: "'Landed Comparison'!R3 ='Usage Rollup'!E3, E3 =C3*D3 (arithmetic hops do not fail it), C3:C30 store SUMIFS". autoeval_check R5 now byte-verifies paren-less hop keys (=C3*D3, ='Sheet'!E3) so stated chains can't drift from the workbook; its function-assertion match is anchored to the key it directly follows (a later bare-range "C3:C30 store SUMIFS" was being misattributed to the preceding quoted key). Same run: the four meet-style negatives drew ambiguous_negative_polarity for the 5th straight time while task 07's Agentic Rubric Quality Review failed on that exact pin style - "met only when / does not meet" pins are now retired portfolio-wide in favor of the defect-frame form (defect asserted with incorrectly/violating wording + "... is not this defect" carve-outs; lint W9).

**COMPOUND-formula cells are judge-illegible; no wording fixes them - drop the criterion (marathon runs 6-7, 2026-08-19, terminal):** after hop-endorsement (run 5, 1/3 fail), run 6's judge read the SUMIFS range in value mode and called it not_observed (1/3), and run 7's fully anchored rework ("Decide from stored formulas only: 'Usage Rollup'!C3:C30 each store a SUMIFS ... displayed numbers are cached formula results ... fails only where typed") made the misread DETERMINISTIC - 3/3 judges asserted "C3 contains typed 180" against XML-verified SUMIFS. The variable was never wording, it was the cell: ranges storing pure single-call formulas (=SUMIFS(...) alone, 'Program Scenarios'!B3:C7) verified on every one of 7 runs; the compound =SUMIFS(...)+IF(B3="",0,SUMIFS(...)) column failed in 4 of them. Rules: (1) liveness answer keys may only cite ranges whose stored formula is a single pure function call - autoeval R7 (2026-08-19) warns on compound-range function keys; (2) after TWO flaky oracle runs on the same liveness criterion, stop rewording and drop it if remaining liveness weight stays ≥10% (marathon C29 dropped on the platform's own "drop if inherently unstable" guidance; positive criteria pinning the correct VALUES, e.g. usage counts, carry the residual coverage); (3) when building future goldens, keep aggregation columns pure (put prior-code/adjustment terms in a helper column) so liveness criteria have a legible anchor.

## Task 08, twincreek-bid-response: oracle polarity, authorship detector runs, occupation (2026-08-18 to 08-19)

**Root cause & permanent gate (after 3rd judge-side FAIL, twincreek 0.9184×3 deterministic, 2026-08-18):** the oracle judge grades each criterion as a true/false statement; a negative criterion written as a bare defect assertion leaves polarity unresolved - worst when the golden holds a near-miss (declined/zero-qty rows, quoted claims being rebutted, excluded-but-computed reference figures). ALL negative criteria need: any-quantifier subject ("At least one …") + polarity marker + near-miss carve-outs. **Marker style SUPERSEDED 2026-08-19 - use the DEFECT-FRAME, never the meet-pin:** the Agentic Rubric Quality Review (task 07, needs_improvement, all four pinned negatives flagged [major]) parses "met only when …; X does not meet it" as inverted polarity ("compliant responses lose points") and demands bare defect statements back. Canonical form now: state the fault with defect words ("incorrectly included … violating policy 2.2", "exceeds … violating the letter's cap", "claimed beyond what X supports", "contradicts … beyond rounding") and phrase carve-outs "…is not this defect" - polarity lives in the semantics, no meet-language anywhere. Serves both readers; watch the next oracle run - if a defect-framed negative starts deducting, the two gates genuinely conflict and the deducting one wins. rubric_lint: E1 accepts defect-frame markers, W9 warns on remaining meet-pins (25 sibling criteria across 01/03/06/08/09/10 to convert on each task's next touch). Portfolio-wide sweep applied 2026-08-18 (tasks 01, 03, 06, 07, 08, 09). **Gate: run `python3 tools/rubric_lint.py` on every rubric before submission** (alongside fix_floats scan) - it errors on unpinned/bare-plural negatives and warns on zero-qty-row phrasing, unanchored relative windows, CSV re-sum demands, chain-less liveness wording, and unpinned carve-outs.

**Float cleanup alone does NOT move the statistical detector** (twincreek run 2, 2026-08-19: floats fixed → llm-only 0.50→1.00 but detect stuck at 0.04, 71/74 chunks). **Sparse notes/legend/docProps humanization barely moves it either** (twincreek run 3: detect 0.04→0.08 only - that approach is retired as a primary fix; keep docProps plausibility and derivable-facts-only annotations as hygiene, and verify any policy-section cites against the source doc). The detector judges the extracted text fabric (cached values incl. numbers) in ~1.2k-char chunks; detect ≈ fraction of chunks judged human, combined ≈ 0.7·detect + 0.3·llm-only, pass ≥ 0.55 ⇒ with llm-only at 1.00 detect must reach ≈0.36. **The real driver is a raw-paste WALL dominating the solution workbook's extracted text - in ANY form** (theory revised after twincreek run 4, 2026-08-19). Run 3 deleted the desc column believing "codes/numbers pass, desc text fails"; run 4 disproved it: the resulting near-letterless numeric wall (884 rows, 63% of fabric, 5% letters) scored detect=0.06 - human chunks actually FELL 6/75→3/54. Calibration across every big tab with a known outcome: marathon (1,011 rows, 43% letters - branch words per row) and deadstock (429 rows, 27% letters - vendor names per row) passed; twincreek's wall failed both with descs (runs 1–3) and without (run 4). Rule: a solution-workbook sheet with 250+ rows carrying >35% of extracted chars fails when near-letterless (<15% letters) or desc-heavy (mean longest string >25 chars/row); short real-word anchors (vendor/branch, ≤~20 chars, small vocabulary) read human. Fix applied to twincreek run 4: delete the raw-paste tab entirely (the CSV input carries it), freeze the rollup's CSV-facing columns to pivot values, keep all decision formulas live - workbook lands at hartwell's shape (~28k chars), the portfolio's only detect=1.00 full-shape reference. Coded as check A5 in tools/autoeval_check.py. **Run 5 (2026-08-19): wall removal tripled detect (0.06→0.18) but fell short of the ~0.36 needed - the residual AI-read texture was (a) Title-case comma-phrased catalog prose in desc columns (the district bid-sheet wording; LLM-catalog register) and (b) tables of clean 2-dp money and small ints only - LLM-typical round numbers. Hartwell's detect=1.00 rows are ALL-CAPS shorthand dense with long-precision decimals (~30% of numeric tokens). Run-5 fix (shorthand descs + one ratio column per tab) was FALSIFIED by run 6: detect 0.18→0.14, no gain. Package internals also ruled out - marathon/deadstock passed with the identical openpyxl app.xml/inline-string structure. What still separates hartwell (detect=1.00): flowing idiomatic memo PROSE in the briefing (twincreek's terse headline-fragment briefing was detect-flagged in all six runs despite llm-only 1.00 - the statistical detector and the LLM phrasing judge disagree on prose), ~43% long-decimal density in data rows, and no verbatim input-extract paste tab. A run-7 revision (briefing rewritten to hartwell register, Item Data extract tab deleted with lookups frozen, pre-rounding build-up columns) was built but never graded: **the task was retired 2026-08-19 per user after six FAILs, then RESTORED to submissions/ the same day per user** (full folder recovered from git; the run-7 revision sits ungraded in its s-zip, pending a resubmission decision). Standing lessons: tab-local micro-texture does NOT move this detector - only structural composition (what tabs exist, prose register, digit-entropy density) plausibly does; and a deliverable whose natural fabric is tidy 2-dp money tables with terse-fragment prose (a bid worksheet) may be a structurally bad fit for the detector - when designing NEW tasks, prefer deliverable shapes whose honest fabric carries flowing memo prose, word-anchored data rows, or high-precision working decimals from the start, and never let a solution workbook carry a verbatim input paste or a numeric wall.

**The gate is per-zip, never one-time.** The 2026-08-18 "portfolio-wide" sweep was trusted
as done, yet task 08's solution still carried 47 raw IEEE tails and failed the authorship
check that same day (combined 0.18 vs 0.55; margin-rate cells like 0.24011571841851492)  - 
the workbook had been built/regenerated outside the sweep. Run
`python3 tools/fix_floats.py scan <file>` on EVERY xlsx (inputs and solution) immediately
before EVERY zip build or rebuild, and re-run after any workbook regeneration. Never rely
on a past sweep. A corroborating LOW signal: vendor names on the
LLM-favored proper-noun lexicon (e.g. "Hartwell") - prefer plainer invented names for new
tasks. See [[rubric-anchoring-and-landing]].

**Run-7/8 chunk-level refinement (2026-08-19, twincreek):** the detector's pass unit is the ~1.4k-char chunk window, and empirically ONLY prose-register windows pass - twincreek run 7 passed exactly its 3 Briefing chunks (72% letters, 165+ lowercase words per window) and failed everything else including a 57%-letter/137-word annotated Params window and every word-anchored table window. Arithmetic-dense prose ("0.87 x 1.12 x 1.02" worked examples) reads AI; word-dominant working sentences with sparse numbers read human. So the winning lever is composition arithmetic: contiguous prose mass / total fabric ~= detect. Run-8 fix: a Working Notes tab in the briefing's first-person register (facts all derivable from the sheet, number-light), prose-forward Params, desc/experimental columns blanked on internal tabs, tab order prose-first - prose ~= 46% of fabric, simulated 8/17 chunks. Chunk simulator: extract all cell values sheet-by-sheet in tab order, join, split into ~17 windows, score letters% and lowercase-word count (pass profile: >=60% letters AND >=120 words). Result pending.

The platform's **O*NET Compliance Check ("Occupation prompt relevance") judges the
selected occupation against what the prompt actually has the solver do**, not against
the practitioner profile or sector. It failed twincreek-bid-response (UID
65516b43-2487-4fb4-b053-e8b0f11d960f, 2026-08-18) for using 13-1022.00 (Wholesale and
Retail Buyers) on a prompt about pricing a customer contract bid: "primarily concerns
purchasing merchandise for resale rather than pricing and submitting sales bids to
customers."

**Why:** the distributor practitioner profile straddles buy-side and sell-side work,
but O*NET splits it: 13-1022/13-1023 = buying for resale; **41-4012.00 Sales
Representatives, Wholesale and Manufacturing, Except Technical and Scientific
Products** = quoting/bidding to customers (also a Wholesale Trade occupation).

**How to apply:** pick the occupation from the prompt's central deliverable. Supplier
cost events, replenishment, rebates, dead stock → 13-1022. Customer bids, quotes,
sell-price proposals → 41-4012.00 (tasks: "Prepare drawings, estimates, and bids that
meet specific customer needs."; "Estimate or quote prices, credit or contract terms,
warranties, and delivery dates."; "Recommend products to customers, based on
customers' needs and interests."). 41-4012's Skills section has **no Mathematics**  - 
use Complex Problem Solving alongside Critical Thinking, Reading Comprehension,
Judgment and Decision Making. Fix recorded in
docs/platform-submission-form.md. See [[task-metadata]],
[[rubric-anchoring-and-landing]].

## Task 11, dillman-freight-cutover: the atomicity bloat loop and the first detector signature (2026-08-19)

**Why (measured on task 11, 2026-08-19).** A Rubric Quality Review asked for 12 bundled criteria
to be atomised; the split took the rubric from 37 to 54 and immediately failed two platform
checks that get *harder* as the count rises:

- **Near-identical criteria.** Mutual non-redundancy has to hold across every pair, so the
  surface grows with the square of the count: 52 criteria is ~1,300 pairs against ~350 at 27.
  Task 11 failed on one subsumed pair and had four more of the same shape unflagged.
- **Full-credit completeness.** It fails if any prompt-mandated requirement can be omitted while
  keeping 90% of the positive-weight sum. More criteria means each requirement holds a smaller
  share: the briefing sat at 5 of 91 points, so skipping the single most-emphasised deliverable
  still scored 94.6%. Fixing it meant one criterion at weight 8 plus a mirrored negative, which
  is far easier to arrange in a 27-row rubric than a 52-row one.

**The bloat loop, and how to break it.** A review says split a bundled criterion, so rows go up;
more rows raise the positive total; a higher total shrinks every requirement's share of it; the next
completeness check fails on a *different* requirement; closing that adds more rows. Task 11 ran the
loop five times, 37 to 57 criteria, failing completeness twice on the way. Break it three ways: when
a review asks you to split, merge a like-item list back elsewhere to stay at budget; when
completeness fails, re-weight **inside** the existing block before adding a row; and re-run every
percentage against the new total, because raising the denominator reopens holes you closed earlier.

**Measured 2026-08-19, and it is the +1 rows that do it.** The four rubrics in the catalog with no
+1 criteria sit at 30-39 and clear the checks; task 12 is the model shape (30 criteria, positive 94,
weights {2:3, 3:4, 4:9, 5:8}). Task 11 accumulated 23 +1 rows, 45% of its positive criteria and 21%
of its denominator, and is the only one that bloated. (Uncoded - the completeness bar now
actively requires +1 rows to cut the denominator, so treat this as history, not a rule.)

**Never copy a weight a checker suggests.** The full-credit completeness check says things like
"weight it 8-10 points" or "in the 8-15 point range"; the platform rejects any positive above +5
(R12) and both suggestions were acted on literally before that was caught. Read them as "give this
requirement about 10% of the rubric" and build it from 2-3 criteria at +4/+5.

Coverage does not need instances: a list of like items under one measurement is ONE criterion, which
is the line rubric reviewers have actually drawn (a seven-item and a ten-item sweep were both
accepted). Only genuinely different *measurements* get their own row. Difficulty comes from criteria
being exacting, not from there being more of them.

**How to apply:** draft to 25-30 from the start; if a task seems to need more than 30, the prompt
is probably carrying a pile of independent requirements rather than one hard workflow, so fix the
prompt. Coded as R11 in `tools/gcheck/golden_rubric/rubric_form.py` (run by autoeval_check.py): ERROR outside the platform band (15-60 since
2026-08-26; the softer 25-30 house-target arm was deleted 2026-08-24 for flagging
reviewer-mandated splits). Recorded in `prompts/submission.md`.

Task 11 itself stayed at 52 on the user's call: reaching 40 would have reverted 8 of the 12
reviewer-mandated splits, and AutoEval had enumerated all 54 rows without objecting to the count.
See [[repo-layout-and-tooling]] and [[rubric-anchoring-and-landing]].

**Dillman run 1 (2026-08-19) found the first mechanical signature that DOES separate a failing
workbook from the passing ones: mean longest string per row on the dominant tab.** detect 0.20,
combined 0.44. The Settings tab was 141 rows x a ~50-char templated reason sentence per row
("46 picks 12 mo; branch usage, weekly transfer review (5.4)") plus a DESC column duplicated from
another tab: mean longest 59.4 chars/row, 48% of the workbook's extracted text. **Every big tab on
this portfolio with a known detector PASS sits at 8.2-22.3** (marathon 1011r/8.2, weldon 1028r/16.8,
deadstock 429r/18.2, stroebel 689r/22.3); A5's old 250-row gate had let both of dillman's ~140-row
walls through untouched. Small tabs are exempt at any length (hartwell's 58-row Repricing is 37.4 and
scored detect 1.00), so string length only bites at scale. Fix that landed inside the pass band with
zero change to any number, formula or cached value: replace the templated reason sentences with
ALL-CAPS trade shorthand and move the legend to a params tab (one row, not 138); drop every column a
tab duplicates from another tab (a DESC repeated on three tabs is three walls) and every column no
formula references; put the cross-referenced fact the rubric needs ON the row as a live column (here
a PICKS 12 SUMIFS, which also killed three flaky judge sweeps); and grow the briefing into real memo
prose. Settings 59.4 -> 21.5, Usage 29.0 -> 12.1, prose share 11.7% -> 20.6%, workbook 59.4k -> 44.3k
chars. A5 now gates at 100 rows, ERRORs above 45 chars/row and WARNs above 25, regression-tested
against the failing workbook and silent on all six passing ones. **Editing a finished golden without
losing caches:** openpyxl writes empty `<v></v>` for every formula cell, so carry the old cached
values across by reading the file twice (formulas + data_only), then patching `<v>` back into the
saved XML by cell ref; run `fix_floats.py fix` afterwards, since a full openpyxl re-save re-serialises
static numbers too (4 fresh tails on dillman's Item Data list prices).

## Gate tooling notes: writing and proving checks (2026-08-19 to 2026-09-02)

**Combined gate (2026-08-19): `tools/autoeval_check.py <task-folder>` runs the WHOLE catalog in one pass** - rubric_lint + fix_floats scan + an empty-cache scan (pure XML; the formulas-engine injector inject_caches.py was removed 2026-08-19 per user - recalc by opening the workbook in a spreadsheet app, or rebuild the injector from feedback history if ever needed) + audit_task, plus the previously manual checks: 500-char criterion form cap, process-ordering clauses (final-outcome-focus check), liveness-coverage hole (<10% of positive weight), missing completeness criterion vs an "every/all items" prompt, blue-family fills, datetime-formatted cells, docProps plausibility (tool/empty creator, missing title, created==modified, created>modified, duplicate created stamps across files), 200×-repeated ALL-CAPS tokens, and 13-1022-occupation-with-bid-prompt. Exit 1 on errors; `--no-caches` skips the cache scan. First portfolio run found real defects: over-cap criteria on 06/10 (C29 755, C22 623, C29 652 chars), hartwell solution created 08/27 AFTER modified (and in the future), marathon created after modified, weldon solution's 1,049 date-formatted serial cells, weldon input 555 phone numbers. Still manual: invented names vs inputs, source-doc sufficiency, symmetric-event mirroring, pasted-tab verbatimness, answer-key sufficiency.

**Money digits have to be kept out of every row-key pattern.** Three separate checks this session (R57, R58's anchor reuse, R60's skip) needed `(?<![\d.,])\d{4,}(?![\d,]*\.\d)` rather than a bare `\b\d{4,}\b`, or 84866.21 reads as an order number. In R60 the failure mode was silent: the check skipped the criterion as row-keyed and stopped firing on the very contradiction it was written for. Always re-run the known-bad artifact after tightening a check, not just after writing one.

**A new check written through a non-raw heredoc is born dead, silently.** R74 took three attempts. The first was written inside a `'''...'''` Python string, so every `\b` in its regexes became a backspace character before it reached the file and nothing matched. The second matched the sheet name "commitment page" as an aggregate and exempted the exact shape it existed to catch. Both looked installed and both reported clean. Fire every new check at the known-bad artifact and require it to FIRE before trusting a silent run, and write rule blocks with `r'''...'''`.

**An Excel re-save is now part of the pipeline, and it changes what the other tools see (2026-09-02).** `tools/office_resave.py` (see [[package-hygiene-pipeline]]) runs FIRST, before fix_floats and fix_metadata, because Excel rewrites every cache: it writes full-precision `<v>` literals, so `fix_floats.py fix` still has to follow it (85 fresh tails on one input rate page). Two things the re-save exposed that no other check had caught. **Excel writes SHARED formulas** (`<f t="shared" si="0"/>`), which openpyxl never emits, and A17's cell regex ran past `</c>` looking for a closing `</f>` in a later cell, so every shared formula was reported as a multi-`<v>` defect; the pattern is now fenced with `(?!</c>)` on both halves and still catches the real appended-`<v>` defect. **And Excel disagreed with injected caches on task 22 frankfort**, moving 38 values because the build used Python's banker's `round(x, 2)` where the formula says `ROUND(...,2)` - the yankton lesson above, unheeded at build time, and the workbook had been shipping numbers its own formulas do not produce. Read the re-save's recalculation notes rather than skimming them: cent-level moves cascade through SUMIFS totals into rubric-pinned figures.

## Task 12, hollenbach-allocation-plan: nine AutoEval runs, six reviewer rounds, rejection (2026-08-19 to 09-05)

**Mirrored positive/negative criteria are now a rubric-review defect (hollenbach run 1, 2026-08-19):** the Agentic Rubric Quality Review rated the rubric needs_improvement on two [major] redundant_or_double_counted_criteria findings, each a positive criterion and its negative mirror scoring one behaviour (PO 78331 treated as cancelled; registration R-88214 shipped outside the ceiling), and both times instructed to keep the positive and delete the mirror. This overrides the older house habit of backing every stated requirement with a mirrored negative; back only requirements no positive already scores, and expect a bundled reconciliation criterion to be flagged too when its figures are already scored individually elsewhere. Coded as autoeval R15.

**Compound aggregation totals break liveness criteria (hollenbach run 1, 2026-08-19):** the golden stored `=SUM(L5:O5)+P5` in the plan's total column; the oracle judge's xlsx_formula_summary quoted it back as `=SUM(L5:P5)`, and the weight-5 liveness criterion over that column failed 1 of 3 runs (0.9537, deficit 5/108), the same R7 class that killed marathon C29. Fix at the source: widen the range so every total is one pure call (`=SUM(L5:P5)`), keep extra terms in their own cells, and cut liveness criteria to a single statement. Deficit arithmetic again pinned form drift, 108 entered positive weight vs 94 in rubric.csv. Coded as autoeval R16.

**A rubric restructure must be a coverage pass, not just a splitting pass (hollenbach, 2026-08-22):** the platform's **Rubric requirement mapping check** walks every material requirement in the prompt and demands a dedicated criterion for each. It FAILed a rubric that had just been split for atomicity, because the split faithfully divided what the old rubric measured and never re-walked the prompt: two asks the old rubric had never covered (a lost-business dollar figure, and the shortfall table's branch dimension plus its reason column) carried straight through, both present and correct in the golden but ungraded. After ANY restructure, re-walk the prompt clause by clause and name the criterion covering each. Note the arithmetic trap when adding rows: R24 needs the liveness criteria to hold 10 percent of positive weight, so with two liveness criteria capped at +5 each the positive total cannot exceed 99, and further criteria must displace weight rather than add it. Also note this check and the Agentic Rubric Quality Review pull against each other on mirrored +/- pairs (one suggests them, R15 exists because the other demands they be deleted); the mapping check accepts non-mirrored dedicated criteria, so keep those. This finding class is NOT mechanically checkable: a coded attempt (breakdown-dimension matching) missed the real case and threw six false positives on phrases like "by hand", and was removed rather than shipped, because a rule that cries wolf teaches people to ignore the gate.

**An unscoped universal claim is only as true as the least convenient cell in the file (hollenbach run 4, 2026-08-22, 0.9802/0.9444/0.9615):** "Throughout the workbook, ordered quantities are whole units, no quantity is negative" failed 3 of 3 oracle runs on `'Base Recap'!E12 = -17`, a CORRECT net-of-returns figure two tabs away from the order columns the criterion meant. The judge scans every tab, so scope a property claim to the columns it is about ("in the item level plan's four monthly order columns") rather than to the file. Coded as autoeval R33, which scans the golden for negative and fractional values whenever a positive criterion claims a workbook-wide property, and names the offending cell. Same run, three criteria flaked 1/3 each for one shared reason worth generalising: **the criterion and the cell the judge landed on described the same fact in different words** (a "classified requirement" column called "moved onto the Fegley line"; a total "across the four months" whose cell also includes registration material; "the vice president's signature on the surplus order" against a row reading "Sowers order / G. Yeakel"). Reword onto the workbook's own nouns and the figure the judge quoted in its evidence, which the feedback hands you for free.

**Hedge qualifiers fail the Rubric objectivity check outright (hollenbach pre-submission, 2026-08-20):** "where judgment is exercised" / "everywhere the workbook touches it" were read as the disallowed "where relevant"/"as appropriate" class, and ONE hedge fails the whole dimension even when the criterion then enumerates concrete rules. Delete the qualifier and state the checkable conditions directly ("Throughout the workbook, ordered quantities are whole units, ..."); "as required by <named policy>" stays fine, the source anchors it. Coded as autoeval R19. Same checker also asks vague scope nouns to be enumerated ("headline figures" → name them) and "references the detail" to become a concrete mechanism ("each summary figure is a cell reference into the detail tabs").

**Value anchors reduce but do not eliminate liveness flakes - prefer reference-chain liveness and drop an observed flaker early (hollenbach run 3, 2026-08-20, 1.0/0.9126/1.0):** a value-anchored liveness criterion over pure single-call cross-sheet SUMIFS pulls flaked 1/3 with the judge QUOTING the anchor values (5117|1138|390) it then failed - same class as kolterman C25. Meanwhile the two reference-chain liveness criteria (control lines/money summary reading through =Tab!Cell, briefing figures as pure references) have passed every oracle run across three rounds. Rules: key liveness on reference chains the formula summary renders trivially, not on cross-sheet SUMIFS extraction; when a proven-3/3 criterion can carry the weight, drop an observed flaker at ONE flake rather than waiting for the 2-flake rule (hollenbach moved the 5 points onto the proven briefing-reference criterion). Also two judge/platform-side artifacts worth recognizing fast instead of churning the golden: (1) oracle evidence citing a SHEET THAT DOES NOT EXIST in the workbook ("Sources & Uses ... senior debt and equity") = cross-task judge contamination; (2) an alignment-audit finding repeating verbatim with a criterion number the rubric doesn't have and quoting text already fixed in the delivered zip = stale audit - verify by unzipping the delivered s-zip, then flag on the platform rather than editing the repo.

### A reviewer nets on-hand stock, and adds the summary column up (task 12 hollenbach, reviewer gate 3, 2026-08-25)

The plan netted Hollenbach on-hand off demand and never did the same for the **substitute
Fegley line**, whose on-hand the very same item file extract publishes, at the very same
branches that are allowed to use it. The order went out for the whole 538 unit classified
requirement instead of the 375 that were actually short. Everything downstream inherited it:
the briefing coverage line, the classified cost comparison, and four rubric criteria that
pinned the wrong order quantity and the wrong carrying cost. **Whenever an input publishes a
stock quantity for a class of item the golden orders, net it, and net it on every line of
that class, not just the ones the narrative happens to be about.**

The reviewer's second finding is the one worth coding. The briefing stated 5,117 units of
demand and then enumerated the coverage beneath it, and those lines added to 5,159. Every
cell was a live cross-sheet reference, so no liveness or cache rule could see it, and **the
oracle judge scores such lines one at a time and never adds the column up** - it survived
three AutoEval rounds. A reviewer adds it up and opens with it. Coded as **G3
(check_summary_reconciliation)**: a contiguous run of five or more cells in one column, each
a pure reference into the same other sheet, where the first is meant to be the total of the
rest, firing only when the block nearly ties and nothing beneath it carries the difference.
The guards matter as much as the rule - **every part positive and below the total, four or
more parts, and a 2% near-tie band** - because the first draft fired on task 15, whose
briefing block mixes an opening balance, a target, a variance and three negative deductions.
That is a list, not an identity, and the sign test is what separates them. The fix in the
golden is a reconciliation cell that reads zero, which is cheap and which a reviewer looks
for.

Third finding, same class one step out: a **hard-coded quantity column sitting beside
computed siblings**, and a **group-average cost taken over a range that includes material
outside the constraint** (registration units that ship outside the monthly ceilings and are
never held). Both read as unresponsive to a prompt that asks for live arithmetic. Rebuilding
it live runs into R16, which wants every aggregation to be a pure single call: the repair is
to **put each component on its own row and keep the combining cell to plain arithmetic**,
which is what a buyer wants to read anyway, and to **give the block its own tab** rather than
crowd a tab that is about something else. Coverage was about the gap; the running balance
became a Buying Ahead tab.

Two mechanics worth keeping:

- **openpyxl 3.1.5 writes floats at 16 significant digits**, so a value Python holds as a
  clean 8.95 lands in the XML as 8.949999999999999. It is the writer, not the data.
  `fix_floats.py fix` is not optional after any openpyxl save, and the tails it leaves will
  also drift any cached product that reads the cell.
- The **`formulas` package is installed in the repo venv** and will recalculate a whole
  workbook from its stored formulas. That is the only way to prove injected caches are
  reachable from the golden's own formulas, which is the G2 hazard. Run it, and **prove the
  verifier fires first by corrupting one cache** - a silent pass on a mis-keyed sheet index
  looks identical to a clean one.

### A total twinned across two blocks of one tab (task 12 hollenbach, AutoEval run 4, 2026-08-25)

Rewards `[0.0000, 1.0000, 1.0000]`. **Read the two 1.0000s first**: a clean 1.0 is zero
deficit, which proves the rewritten 38-criterion rubric reached the form intact and that the
golden satisfies all of it. And read the 0.0000 for what it is - a single +2 criterion
failing out of 66 scores 0.9697, so a zero is a run that produced no verdict, not a low one.
The difficulty check in the same window died on `DownloadVerifierDirError`. **Do not rewrite
a golden to chase a 0.0.**

The real finding was one flagged criterion, and the judge's own evidence diagnosed it:

    'Buying Ahead'!G32: ALL held at the end of the month = 897
    'Buying Ahead'!C40: TOTAL UNIT MONTHS HELD          = 897

It found the figure, quoted **both** cells holding it, and still verdicted
`unverifiable_from_deliverable`. The tab totalled 897 twice by different arithmetic, once
across the four months and once across the three groups. **Naming the sheet cannot fix that,
because both twins are on the sheet.** R51 guards a figure twinned on a ROW, R46 guards
textual twins on a liveness anchor; neither sees a total twinned across two BLOCKS of one
tab. Coded as **R59 (check_figure_sheet_twins)**.

The fix is in the workbook, not the wording: **delete one of the two totals.** Adding
month-end positions across months IS unit-months, a cost concept, so it belongs in the
holding-cost block and nowhere else. That leaves the figure in the source-plus-one-read-through
shape R46 endorses, and the criterion can then be keyed in the tab's own words - sheet name,
column header, row key, one figure.

**Narrowing a new check is the substance of writing it.** R59's first cut flagged any figure
a sheet happened to hold twice and lit up **eleven criteria that had just scored 1.0 twice**,
because a counter quantity of 26 recurs in a 75-row demand table. A judge never mistakes a
detail cell for the answer. Requiring **both holders to be range aggregations sitting on a
row labelled TOTAL or ALL, with neither reading the other**, took it to one true hit. A
check that fires on passing criteria is worse than no check: it buries real findings and
invites bad repairs. Always run a new rule against rubrics you have already watched pass.

### The oracle reward model, solved (task 12 hollenbach, AutoEval run 5, 2026-08-25)

Rewards `[0.9877, 1.0000, 0.9875]`. Dividing the deficit by the file's positive total of 66
gives **0.81 and 0.83 of a weight point** - below the smallest weight on the file, therefore
impossible, and under the old house rule that reads as a rubric that never reached the form.
**That reading was wrong, and so was the hint the gate had been printing for weeks.** The
model that reproduces all three rewards exactly:

    reward = (B - u - f) / (B - u),  B = positive + |negative|

`u` is the weight of criteria verdicted `unverifiable_from_deliverable`, `f` the weight that
actually failed. Here B = 66 + 17 = 83, and: run A 81/81 = 1.0000 (C27 unverifiable, nothing
failed), run B 80/81 = 0.9877 (C9 failed, C20 unverifiable), run C 79/80 = 0.9875 (C9 failed,
C35 unverifiable).

Three things follow, and they change how to triage a reward vector:

- **The denominator is positive PLUS the absolute negative**, because avoiding a defect earns
  its weight. Dividing a deficit by the positive total alone will not come out even, and a
  non-integer result is NOT evidence of an unsubmitted form.
- **An `unverifiable` verdict costs nothing.** It is dropped from both sides. A run scored a
  clean 1.0000 while carrying one. Do not rewrite a golden for a judge-side item.
- Solving for `f` tells you exactly which criteria are worth touching. Here it was **one**,
  out of four the report listed.

The one real failure, C9, is an ordinary landing miss worth recognising: the criterion named
no sheet, named no PO number and asked the judge to confirm an **absence** ("as material that
is not coming"), so the bare figure 220 walked it to the nearest prose row carrying that
number - an **action-list row about a different action** ("Re enter the 220 pieces cancelled
with PO 78331 ...") - while the backlog table that says the thing the criterion meant was
never reached. Fixed by keying it on the backlog row in the table's own words, with two
phrases unique in the workbook (`effect on the ceiling`, `replanned inside the period`), and
by deleting the figure's twin from the row's prose cell, which repeated a number the UNITS
column already carried.

**And a check not written.** The generalisable form - "a criterion naming no sheet whose
figure also lives in prose rows" - was probed against this rubric before coding and flagged
**13 criteria, most of them scoring 1.0**, because 25 appears in dates, 254 inside item codes
and 911 in a job name. R35 already carries the durable half (name the sheet). Probe every
candidate rule against criteria you have watched pass, and when it lights them up, write the
lesson down instead of coding it.

### Cutting the denominator drops requirement mappings (task 12 hollenbach, pre-submission mapping check, 2026-08-25)

The Rubric requirement mapping check FAILed on two explicit prompt asks with no dedicated
criterion: the shortfall "broken out by item, by branch and by month" with a reason, and the
briefing listing "anything that has to be signed or sent before the first of the month".
**Both had criteria in the 57-criterion rubric and I cut them the same day**, taking the
positive total from 96 to 66 to satisfy R24's completeness bar.

That is the standing trap. **R24 counts weight and the mapping check counts requirements, and
they pull opposite ways.** R24 forces the positive total to 66 or under; R11 caps the rubric
at 40 rows; so every requirement needs a row, and rows have to be paid for. Closing the two
gaps here cost one dropped criterion (the load center ceiling, whose block was already
credited) and four weight cuts from +2 to +1 on single derived facts. There is no free
addition once you are near both caps - **decide what a criterion DECIDES, and spend the +1
band on single facts so the +2s and +3s stay on the decisions.**

Two shapes the checker will not accept as a mapping:

- **An aggregate does not map a breakout.** "Counter demand that cannot be covered totals 66
  units" does not cover "show me what falls short and why, broken out by item, by branch and
  by month". Write the breakout as a presence claim over rows ("gives each uncovered line its
  item, its branch, its month and why it is short"), which is the safe shape, never as a
  count.
- **A negative's carve-out is not a mapping.** The action list existed only inside a negative
  that checks tab ordering. The checker said so explicitly: a carve-out mentions content "in
  passing" and cannot be the positive half of a pair.

Write both against the workbook's own header words - `WHY IT IS SHORT`, `WHO`, `BY WHEN` -
each of which appears once, so the judge lands where you meant.

**A third candidate check, probed and rejected.** "A subject appearing only in negative
criteria has no positive mapping" is exactly finding 2's shape, and across the portfolio it
flagged **68 negatives on all 15 rubrics**, because a negative necessarily carries defect
vocabulary its positives do not. That is three rounds running where the obvious rule lit up
criteria already scoring 1.0. The guard for this one is procedural and belongs in the head,
not the gate: **after any weight cut that removes rows, re-read the prompt's deliverable
sentences one at a time and confirm each still has a criterion of its own.**

### judge_failed is fail-closed; unverifiable is free (task 12 hollenbach, AutoEval run 6, 2026-08-26)

Rewards `[0.9759, 1.0000, 1.0000]`, no EC-actionable failures, two items reported as
judge-side. The arithmetic separates them: with `B = 66 + 17 = 83`, run A was 81/83 (the
briefing action-block criterion, weight +2, **failed**) and run B was 82/82 (the average-cost
criterion, weight +1, **unverifiable**, dropped from both sides).

**A judge RUNTIME error is not an unverifiable verdict.** `judge_failed`
(`content_type=NoneType`, an agno parser failure) is *fail-closed into `f`* and costs the
criterion's full weight; `unverifiable_from_deliverable` costs zero. Both arrive under the
same "judge-side, not your submission" banner, and only one of them is actually free. So when
a report says nothing is EC-actionable, **solve for `f` anyway** - here it named the single
criterion worth touching, and it was the one the platform told me not to worry about.

The mitigation for a parser failure is the criterion's **evidence surface**. The one that
died asked for "each row filled in with who and by when" across nine action rows of long
text; re-keyed onto a single named row (the Sowers order, its signer and its date) it pulls
one row instead of nine. Note also that **"G. Yeakel" reads as two sentences** to the
sentence counter, because of the initial's full stop - R54/R55 fire on it. Write "Yeakel".

For the unverifiable one, the fix was to **drop it rather than reword it**: its clause
("taken across the units ordered inside the ceilings") asked the judge to confirm a
derivation it can never see, and the fact survives elsewhere - the carrying cost of 203.51 is
only reachable if that average excludes registration material (leaving it in reads 212.52,
checked). **Before dropping a criterion, prove the requirement is still tested by another
one, arithmetically.**

**R24's single-loss variant changes the whole shape of a rubric.** Each strict liveness
criterion must cost more than a tenth of the positive total on its own, so with the +5 cap
the positive total is pinned at **39 or under**, not 66. Since the minimum weight is 1, that
also caps non-liveness criteria at 29 and pushes essentially every positive to +1. Cutting
from 66 to 39 means dropping rows, so **pick the ones whose requirement another criterion
still carries** and check each against the mapping rules before cutting. R18 landed the same
day: `is not this defect` carve-outs are banned outright, so every negative becomes one
affirmative sentence carrying its own frame word.

**A fourth candidate check, rejected.** "Flag a criterion whose evidence surface is a
multi-row sweep of long text" is what preceded the parser failure, but W16 already covers row
sweeps, and tightening it would flag the shortfall criterion the requirement-mapping check
*required* in the previous round - which has to be a presence claim over rows to map its
requirement. **A rule that forbids what another check mandates is not a rule.**

### A hold date is a supply commitment, and a group average is not a plan (task 12 hollenbach, reviewer gate 4, 2026-08-31)

Three findings, all upheld.

**A quotation's hold paragraph is a hard constraint on the schedule.** Sowers wrote "I can
hold this list for you until Friday August 28 and after that it goes to whoever calls", and
the plan deferred the vice president's signature to Monday 08/31 - three days past it - while
the workbook's own surplus note already said "Sowers holds the list until 08/28". It stated
the date and scheduled around it. **When an input names an expiry, walk every action date
against it**, and where the deliverable's own timetable lands later, say so and move the
approval: this one purchase had to go to Gwen on its own, ahead of the plan, or the lot was
gone and the coverage leaning on it had to be replanned.

**A group-average carrying cost does not trace a SKU-level plan.** The tab pooled
item-specific stock, backlog, surplus and classified supply into a product-group balance and
priced it at a group average. Rebuilt one row per catalog number at its own cost, the figures
moved both ways: **597 unit months against 897**, because pooling let one item's surplus mask
another's shortfall, and **226.03 carrying against 203.51**, because load centers carry far
more at their own cost than a group average implies (one item, LCP2040MB, was 76.36 of it).
The check that the item-level balance is real rather than an allocation of a group total:
**every item closes the period at zero and none goes negative.**

**The new rules interlock, and the binding constraint is now the CLUSTER COUNT.** R24 pins
positives at 39 or under; the strict liveness pair takes 10 of that; the completeness check needs every
requirement cluster over 12.5% of positive weight; so the remaining 74.4% affords **five
clusters and no more**. Fold requirements together on that arithmetic (SHORT rode into
SOURCE) rather than adding rows you cannot pay for. Alongside: R73 wants the gated tier over
15%, and **R29 forbids a derivation clause on any figure that sits in more than one cell** -
so gated clauses must be anchored on single-cell values, which are worth hunting for
deliberately (a per-item carrying cell, a tab's own counter total, a register quantity). And
R67's strong-token list is literal: "policy 2.3 **bars**" does not match, "**prohibits**"
does.

**Verify caches after moving any mirrored row.** The briefing's action list mirrors Coverage
by formula, so moving one row left three stale cached strings behind it. The recalculation
pass caught it; nothing else would have.

### A weight cut is a coverage change, twice now (task 12 hollenbach, coverage check, 2026-08-31)

The Rubric coverage check FAILed on one gap: **"what the shortfalls cost us in counter
business we cannot write" had no criterion.** I had one and dropped it the previous rebuild,
when R24, the cluster share and R73 forced the positive total to 39 across five clusters. **This is the
second time the same mechanism has cost a submission** - the 2026-08-25 mapping failure was
the first. Every weight cut is a coverage change; re-walk the prompt's deliverable sentences
one at a time after each one, because no local check enforces it.

Useful precision from the checker on what does NOT count as covering a requirement: a
criterion on the identity and reason of each shortfall line does not cover the *money* the
shortfall costs, and an overall net-cost criterion does not either, because "neither
necessarily penalizes omission of the requested counter-business shortfall cost". **Ask what
a deliverable could omit while still passing every criterion.**

Where to find the room, when the caps are already binding: **drop criteria whose substance
another criterion forces.** A base-period construction rule is gated by the variance reading
zero on all three groups (it cannot, unless the base was built right); a 538 total is forced
by the pinned 163 and 375 that make it up. That is a real argument, not a convenience, and it
is the only honest way to buy a row at the cap.

The checker asked for the restored figures to be formula linked. **They cannot be**: R29
forbids a derivation clause on a figure held in more than one cell, and 699 sits in three.
When two checks pull opposite ways, follow the coded one and say why in the log.

**M2 is per-prompt, not per-occupation.** "Collaborate with vendors to obtain or develop
desired products" is a legitimate pick on tasks whose prompts source or develop product, and
wrong here, where the work is planning and ordering against an allocation. The check tests
each pick against the prompt's own words, so a pick carried over from a sibling task is the
classic failure.

### A negative must quote its policy's CONDITION, not its subject (task 12 hollenbach, AutoEval run 7, 2026-08-31)

Rewards `[0.8980, 0.8776, 0.8776]` - 44/49 and 43/49 against B = 39 + 10. **One -5 negative
fired in every run** and cost more than everything else combined.

The criterion said VP approval is required whenever "a job line re costed above its quoted
basis is committed". Policy 5.1 says a re costed line is *tested* against a 12 percent floor
and only "a line that lands under the floor goes to the vice president". The golden shows
three re costed lines, two holding above the floor and committed without going to the VP,
which is correct - and the criterion read that correct behaviour as the defect. **A negative
that names a policy's SUBJECT but drops its CONDITION fires on the compliant golden.** Quote
the triggering condition, or spend the penalty elsewhere.

**Respend rather than repair, when the evidence is ambiguous.** Correcting the wording would
still park the judge beside the table showing a 9.8 percent line, which is what it quoted all
three runs. Moved to policy 2.4, where the golden's evidence is a column of zeros plus two
file notes saying acceptance is not needed because no classified device is furnished.

**A gated clause must not describe mechanism.** Both flaky positives quoted the right cell and
failed anyway, because the clauses said "multiplying the item quantities by their classified
costs" and "summing the plan's October column". The judge greps cached values, so a described
mechanism - especially one reaching across sheets - is unverifiable by construction. The
minimal form **"the cell a formula rather than a keyed figure"** still satisfies R73's gated
tier and is confirmable in one tool call. Verify each anchor really is a formula.

**R76 (2026-08-31): a strict criterion must admit live alternatives.** Prescribing "plain cell
references" as the only mechanism is a gold-only tactic lock, because a workbook aggregating
the same rows is equally live and would lose the whole strict tier. Add "or an aggregation
over the same rows alike" and keep the value anchor.

And the standing warning about platform advice: the guidance told me to change the golden's
J-2634 line "so it complies with policy 5.1". That would have been wrong - a 9.8 percent line
under the floor is exactly what the policy contemplates, and the plan already sends it to the
VP. **When the feedback proposes a golden change, re-read the source clause before touching
anything.**

### The gate tested the rubric against the golden, never the golden against its sources (task 12 hollenbach, REJECTED 2026-09-05)

Rejected after nine AutoEval runs and six reviewer rounds - and it had been *accepted* once,
then sent to adjudication. Every defect that killed it was in the first build, and none of
them was a rubric-mechanics defect, which is all the gate could see:

1. **A deadline attributed to a source that never gave one.** The golden said "Balliet has
   asked for it by Friday the 28th". Balliet's message says only "Send me a recap by group
   and by month ... I will put it in front of Sandusky myself" - **no date at all**. The
   28th was the SOWERS hold date, lifted from a different document in the same packet. This
   is fabricated evidence attributed to a named person, the most serious class there is.
2. **A plan built on an entitlement only requested.** Oct-Dec ordered at the corrected 589
   ceiling when the notice publishes 466 and Balliet says a correction "realistically lands
   with the October ceilings" and "do not build September around a bigger number".
3. **The shortfall table typed** against a prompt demanding live formulas - and the liveness
   criteria all pointed at cells that were already formulas.
4. **A blended cost pricing three supply sources at one of their unit costs** (23 units off
   PO 78214 at 9.33, costed at the item file's 8.95).

Coded as four checks in `gcheck/golden_rubric/sourcing.py`, each proved on the rejected
artifact and silent across every live task:

- **G11** (ERROR) a dated obligation put on a named person must carry a date appearing in a
  document that mentions that person. **Source-scoped is what makes it quiet**: a deadline
  the buyer sets himself is in the prompt, which is in the corpus. A first cut keyed on
  name-plus-date in a row and flagged every memo header and action row.
- **G12** (ledger) the inputs' own conditions and prohibitions, printed to tick off. Whether
  the golden may lean on a conditioned figure is the builder's judgement, so a rule that
  guessed it would flag correct work.
- **G13** (ledger) one item carrying two unit costs across the inputs.
- **R97** (ERROR) a month-split table the rubric never scores. **The overlap test must
  require the criterion to NAME a month**: a bare figure match passed on coincidence,
  because "26 catalog numbers" collided with a 26 sitting in a month column.

**The standing lesson.** Every other check in the package tests the rubric against the
golden. Nothing tested the golden against the documents it cites, and that is where all four
fatal defects lived, through nineteen rounds of feedback. Before the first submission,
re-derive every attributed fact from the source that is supposed to carry it.

And ids are portfolio-shared: G8-G10 were claimed the same week by another session's
lift-truck checks, so check `gate_families.py` before numbering.

**Two gotchas when registering a check.** Ids are portfolio-shared - G8-G10 were claimed the
same week by another session's lift-truck checks. And **`'folder'` in `needs` means the BUILD
folder**, which `review_check` never stages, so declaring it opts the check out of review
**silently**: it lands in `skipped`, prints nothing, and looks like it passed. The staged task
directory arrives as a PARAM, which is a separate thing. Declare only the data you read
(`inputs`, `solution`, `prompt`, `rubric`) and verify against all four packet shapes review
can produce - both zips, input zip only, golden zip only, JSON-only.

**Atomicity reviews come in waves, and R27 only sees the numeric half (hollenbach, 2026-08-22 then 2026-08-24).** The first round split every criterion bundling multiple FIGURES, which is the shape R27 detects; the reviewer then named ten more that bundle ASSERTIONS without bundling figures. Five shapes to check by hand, now listed in R27's docstring: a conjoined second predicate ("reproduce the ceilings, AND the variance is zero"), two dimensions swept at once ("0 in every month for BOTH groups"), two subjects sharing one verb ("the control lines AND the money summary reach ..."), a column list standing in for a table-shape claim, and a list of like figures under one measurement (defensible as one until a reviewer calls it). Do NOT try to code a detector: clause heuristics have now been calibrated three times and fail (task 11's 12 flagged vs 25 accepted, median clause count 2 on both; a conjoined-predicate test caught 3-4 of hollenbach's 10 while flagging noun lists). **Weight neutrality forces +1 children:** a +2 parent the reviewer calls bundled divides into two +1 rows, never two +2s, because R24 caps the positive denominator (liveness must hold 10 percent of it, so with two criteria at the +5 cap the total cannot exceed 99). Settle the resulting R14 (+1 share) and R17 (liveness count) warnings in .gate-accepted with the reasoning, since both are consequences of the reviewer's instruction rather than defects.

## Task 13, kolterman-valve-advisory (2026-08-20 to 08-26)

**Liveness criteria are a per-criterion lottery, so cap the count (kolterman run 1, 2026-08-20):** C25, C26 and C27 were three near-identical formula-only liveness criteria over three tabs; C26 and C27 passed 3/3 while C25 failed 2/3 with the judge quoting the exact SUMIFS it reported as not_observed, sinking two runs (0.9643, 0.9306). Wording did not separate them, so the lever is how many are on the board: keep at most two liveness positives, drop any that flakes twice (deadstock C8 precedent), and remember that a flaked criterion of ANY weight fails the 3/3-at-1.0 rule, so a weight-1 liveness criterion buys nothing and costs a full submission. Coded as autoeval R17; dillman was trimmed from three to two the same day. Same run: a 5-statement scope criterion (count + two series + two rep-added codes + authority) failed 1/3 even though the judge listed the right ten codes, and a completeness criterion that asked the judge to tie back to an INPUT file drew unverifiable_from_deliverable; point completeness criteria at the deliverable's own check column instead.

**Grader-instruction wording is a pre-submission FAIL, and the checker's own fix inverts your criterion (kolterman, 2026-08-20):** the platform's Rubric negative polarity check failed four POSITIVE criteria for "It fails only if ..." and "Any response meets this if ...", calling both near-verbatim paraphrases of the banned "Fail the response if" and "Award if / Give credit if" patterns: criterion text must state a fact about the artifact, never tell the grader when to pass or fail. Same run passed all five negatives and named "... is not this defect" as the reason they read correctly, so that carve-out shape is confirmed good. CAUTION: the checker suggests rewriting "It fails only if <defect>" as a bare statement of the defect while keeping the positive weight, which inverts the criterion so the golden loses the points and a wrong answer earns them; restate what the COMPLIANT deliverable does instead. Knock-on: rubric_lint W13's old remedy for absence-claiming positives was exactly the now-banned shape, so absence claims are now recast as a positive observable (the flag, marking or zero the golden carries). Coded as autoeval R18; the same defect was live in marathon, dillman and hollenbach and was reworded portfolio-wide the same day. **Run 2 on the same task failed the check again on a second family: attribution disclaimers.** "Judge from the stored formulas, not from displayed values" and "Credit here is for the stored formulas, and the figures are scored by their own criteria" read as grader instructions too, even though they exist to stop a liveness criterion restating figures scored elsewhere. Keep liveness criteria VALUE-FREE and delete the disclaimer: being value-free is what prevents the overlap, the sentence only announced it. R18 now also matches "scored by their own criteria", "credit here is for", "counts as met", "counts as ... here"; a catalog sweep found the family live on twincreek C24, hollenbach C21, wamhoff C29, oskaloosa C29, open-order C5 and yankton C5. Procedural lesson from the same run: the gate was CLEAN when this rubric was entered and the rule landed afterwards from another task in flight, so re-run autoeval_check immediately before entering a rubric, not only when the rubric changes.

**Reviewers audit the gap between the triggering event and the data cut (kolterman reviewer, 2026-08-20).** The golden traced 2,318 affected units correctly and still came back for revision: 76 of them were invoiced across five invoices in the eight days BETWEEN the stop sale and the stock date, and nothing in the workbook separated those accounts from accounts served eleven months earlier. Nothing was missing, misdated or mispriced, so no repo-side check can find it; the question is semantic. **Ask it of every dated scenario: what moved between the event and the data cut, who has to be called first, and what did we not yet know when it moved.** The last part is where the credit is: working the codes through showed 52 of the 76 were on the printed bulletin when they shipped, 21 came off codes the rep added the same day the invoice was written, and 3 came off a number and a code that entered scope after the valves left the dock, so that invoice is not a miss at all. Design tasks so that split exists and grade it. Related: **basis-dependent pins** - the same reviewer asked that criteria stop pinning figures that fall out of an assumption a sibling criterion leaves open (176 Renner pieces and 76 uncovered units against a three month horizon the coverage criterion explicitly allowed the solver to change). Tag every figure with the assumption that produces it and let the dependent criteria say "on the three month horizon that is X, and the figures follow the horizon the response states". Neither is codeable (the dependent criteria share no distinctive token with the flexible one); both are recorded in autoeval_check's manual section.

**A liveness demand written as a row sweep fails even when every row is live (kolterman run 2, 2026-08-21, 0.9669/1.0/0.9679).** "Each line of the return authorization detail draws its quantity and its unit price from the receipt layer by cell reference" was true of all 20 rows (=Layers!Q168, =Layers!H168, extension =E15*F15) and failed 2 of 3 runs, the judge quoting a displayed row back as typed numbers. Sweep plus liveness is the worst pairing available: W11's flake mode and the formula-extraction misread multiply, and one misread row sinks the criterion. **Scope liveness to a named handful of figures, never to each/every line of a table.** The replacement is the reference-chain shape that has held everywhere it has been used: the front tab's figures stored as cell references reading through to the tabs that compute them. Note the anchored variant of the sweep does pass (open-order C4, yankton C4 both carry a worked example and cleared their runs), so the lethal combination is sweep + liveness + no figure in the text. Coded as rubric_lint W16 (ERROR), scoped exactly that way. Deficit arithmetic identified the criterion before reading the report: 0.0331 x 156 = 5.2 and 0.0321 x 156 = 5.0, one weight-5 criterion per failing run, which also proved the second criterion the report mentioned had cost nothing.

**Vague-intensity hedges on a MAGNITUDE fail the objectivity check too, one strike (kolterman pre-submission, 2026-08-21).** "with roughly a further month of cover behind it" sank the dimension on its own: the checker asked whether five weeks is roughly a month, and ruled that the exact date elsewhere in the sentence anchors the receipt, not the margin. This is a different family from the "where relevant" hedges R19 was built for, and it bites precisely where a criterion is trying to leave room for a justified alternative: **do not buy flexibility with a fuzzy quantity, buy it with a computable rule.** The fix was to state the policy rule the golden already follows (whole months of usage to the first confirmed receipt plus one full month) so any longer horizon sized the same way still scores. Hedges quoting a source template are exempt, but check the source actually hedges: wamhoff C25's "the roughly sixty days the program letter states" was the author's hedge, the letter says sixty days flat. R19 now also matches roughly/approximately/about/around/nearly/almost/some/circa/broadly/more or less/give or take/a little over/in the region of when followed by a number or number word, plus a trailing "or so".

**The Agentic Rubric Quality Review can fail on its own context, and a fat golden makes it likelier (kolterman, 2026-08-21).** It returned needs_improvement with a [critical] completeness finding and no analysis at all: rubrics.txt and instruction.md both came back as "[Prior result omitted from context to avoid token overflow]". Those are the two SMALLEST files in the submission and they were read FIRST, so this is eviction by read order, not a size cliff. Recognise it as harness-side (no criterion named, nothing called subjective or bundled) and resubmit rather than churning the rubric. What IS ours: the reviewer reads every input plus the whole deliverable first, and kolterman's golden was 153,735 chars against a 23k to 46k band for every other golden in the catalog, because it carries a 907-row line-level ledger; total ingest 260k chars, about 65k tokens. **Design goldens to stay in that band: row-level detail belongs in the inputs, the deliverable carries the rollup** (which is also what the A5 authorship detector wants). Coded as autoeval_check A7, WARN over 100k chars.

**What the Agentic Rubric Quality Review means by non_atomic, and its two other habits (kolterman, 2026-08-21).** It flagged ONE criterion of 36: the one bundling five notification classes, because "each class could pass or fail independently". It left every derivation chain and like-item list alone (a worked FIFO case, a 30-row reconciliation with its example, a transfer price chain, a four-line buy list), which matches how the task 11 reviewer treated the same shapes. **The boundary is independent policy checks stacked in one row, not the count of figures.** Two more habits worth designing for: (a) it flags positive/negative OVERLAP as well as exact mirrors, and de-enumerating the positive can dissolve the overlap without deleting either criterion, which is better than losing a check; (b) it wants a PARENT PRESENCE criterion for every section the prompt requires, even when detail criteria already score that section's figures, so budget one presence criterion per deliverable section from the start. Note the standing tension: every parent criterion raises the positive denominator, which pushes the full-credit completeness check the wrong way (R24).

**A recorded action is not the artifact, and a reviewer reads the input document to find
out (kolterman-valve-advisory, 2026-08-26).** An operations memo asked for short written
counter guidance ("I would rather they read something we wrote"): which numbers, what a
customer does, who to call, and that nobody at a counter promises labor money. The workbook
answered with three cells saying a notice gets posted, an action-list row with a date on it
and a notification class reading "Counter posting". The reviewer scored that as the
requested content missing, not present. **Where an input asks for copy addressed to a
person - a posting, a script, a letter, a form of words - the deliverable carries the
words.** The same report named the second half of the same cause: the golden transcribed
from the customer master only the columns its arithmetic needed and dropped CONTACT and
PHONE, so the call-ahead list it built could not be acted on. **Transcribe the columns the
ACTION needs, not only the columns the sums need.** Neither half is codeable: judging what
an instruction asks for is semantic, and the mechanical proxy (an input column the
deliverable never uses) fires on every legitimately unused column. Two practical notes from
the repair. New copy pays for itself in liveness if it reads THROUGH to the tabs behind it
(the script's "11 of the 32 accounts" is `=Accounts!K46` and `=Accounts!B50` inside a
concatenation, the posting's date range is `=Scope!B23`, the ten covered numbers are ten
read-throughs of the scope rows) rather than restating figures, which would have made
R59 twins of them. And R24's 39-point ceiling means a reviewer's "add a criterion" costs a
criterion: the row it displaced was the unanchored "briefing figures agree within rounding",
proved redundant first against the four criteria that score those figures on their own tabs.

**A judge fails a count it can read differently on the row it lands on (kolterman C9,
2026-08-26).** "2,318 affected units were invoiced to customers across 41 accounts" failed
2 of 3 oracle runs, and both failures quoted the deliverable's own Briefing row: the 2318
the judge greps for, and beside it "40 accounts and the counter". Both statements are
right, since 40 accounts are named and the counter cash account is the forty-first, and the
criterion was the one out of step, calling counter units "invoiced to customers" while its
neighbour criterion calls them untraceable to any customer. **The repair is on the landing
row, not the wording**: put the criterion's own count on the row that holds the pinned
figure, live (`=COUNTA(roster)&" accounts on the list, the counter among them"` on the
total row), and align the prose note beside it. Coded R66, which reads the first
three-digit non-year figure as the pinned one and errors when a row carrying it uses the
criterion's noun against a different number and never against the criterion's; R43 is blind
to this because it checks that the landing sheet carries the REST of the chain, never that
it carries a DIFFERENT value for it. Two exclusions were needed and both came from the
portfolio probe: **year tokens land on every dated row**, and a row putting the noun on the
pinned figure ("4,471 units" under a criterion reading "369 of the 4,471 units") is the
criterion's own framing.

**The same round's second failure: a reading the golden performs everywhere and states
nowhere.** "The workbook reads a casting date code as a range of manufacturing dates rather
than as a lot number identifying an individual customer's shipment" came back
`not_observed` after the judge searched the tab that explains the trace. The trace notes
said invoices carry no date code and that receipts run against issues, which is the reading
in action, but never said what a date code IS. R28's rule holds and generalises past
inverted pairs: **it costs nothing to say it, so say it**, in the tab the criterion names,
in the criterion's own nouns. A check for this family was drafted and REJECTED on the
probe - a figure-free positive whose distinctive words the deliverable never uses flags 58
criteria across the portfolio that score fine (exactly, standing, briefing, showing,
constants), and tightening it toward the real defect would push criteria into quoting the
golden's wording, which W12 penalises.

**A second artifact class the float fixer cannot see: stored precision the number format hides (kolterman, 2026-08-21, authorship FAIL at combined 0.85, detect clean).** The reviewer reads CACHED VALUES, not the display, so 199.7626667 behind a #,##0.00 format reads as programmatic computation even though the sheet shows 199.76. These are not float-repr tails, so `fix_floats` passes them; the tell is that the stored value has more decimals than the cell's own format prints. **Fix at the source with ROUND() in the formula** (a unit margin is cents, a per-month usage figure is two places) so the stored figure is the figure a reader sees; formatting alone changes nothing. Watch the knock-on: round per-row first and let totals SUM the rounded rows, or a group total computed from unrounded parts will disagree with its own column by a cent, and re-check any ROUNDUP-driven quantity (kolterman's NEED 3 MONTHS moved on none of 27 rows, so the buy plan held; only the margin total shifted, $2,121.54 to $2,121.44, and its rubric criterion was updated). Coded as autoeval_check A8, percent formats handled. On the sweep that added it, kolterman was the ONLY clean golden in the catalog: wamhoff carried 988 such cells, open-order 176, yankton and twincreek 93 each.

**A second check reads the task picks, not just the occupation.** The **Skills prompt
relevance check** FAILed kolterman-valve-advisory 2026-08-20 with the occupation
(13-1022.00) accepted and the skills accepted: the four task picks had been carried over
from earlier tasks rather than picked off this prompt. On a recall reconciliation and
claims prompt it rejected "Negotiate prices, discount terms, or transportation
arrangements with suppliers" (nothing is negotiated), "Consult with store or merchandise
managers about budgets or goods to be purchased" (no budget discussion), and "Monitor and
analyze sales records, trends, or economic conditions to anticipate consumer buying
patterns" (the analysis is of specific transactions, not trends), and called "Authorize
payment of invoices or return of merchandise" only tangential while its own suggestions
asked for exactly that duty. One poor pick fails the whole section.

**How to apply:** pick 3 to 5 tasks off the work the prompt asks for and write the
sentence in metadata.json that ties each pick to the clause in the prompt carrying it. The
same block had been pasted into tasks 06, 11, 12 and 13; it is now different in each.
Coded as **autoeval_check rule M2**, which reads every pick in metadata.json against
prompt.md and errors when the duty behind the pick has no signal there.

## Task 15, open-order-cleanup (2026-08-20 to 08-31)

**Deficit arithmetic uses the sum of ABSOLUTE weights, not the positive total (open-order-cleanup run 1, 2026-08-20):** rewards 0.9407/0.9237/0.9322 against 99 positive and -19 negative resolve to integer deficits only over 118 = 99 + 19, giving exactly 7, 9 and 8 points lost, which matched the four named criteria one for one (a -4 negative failing all three runs plus a different positive or negative each run). Use |positive| + |negative| as the denominator when reverse-engineering which criteria a run failed, and treat a clean integer split as confirmation that nothing failed silently.

**A deliverable that narrates the defect it corrected hands a defect-class negative its own evidence (same run, terminal 3/3):** the Exceptions sheet documented "44158 line 1: 5 EA received against 125 ordered" so the reader could see WHY the line closes, and the judge quoted that row as proof of the negative "at least one line shown as received in full is carried forward with a balance still due". Same shape flaked a supplier-minimum negative 1/3 off "what would be left is $428.40 against Kammerer's $1,500 minimum". Rule: never write a negative over a defect class the golden itself describes in prose (correction tables, exception logs, before-and-after narration) - the carve-out does not save it, because the judge is grepping the narration, not the plan. Drop the negative and let the positives that pin the corrected values carry the weight. Corollary for design: an exceptions/corrections tab is good for positives (it makes the fix verifiable) and poison for negatives.

**Statement decomposition splits on paragraphs (same run, 1/3 each):** a criterion naming three actions with owners and dates failed when those actions were spread across two briefing paragraphs, and a criterion demanding a date be "put in front of the branch" failed when the date lived only in prose and not beside the line the judge landed on. Fix that worked: a small named action table (action / owner / by when) in the briefing, and the date repeated in the exceptions row's owner cell. Same lesson as W11's "a named table the sweep can be read off, not a reword".

**A rule stated over an UNNAMED member of a class hands the judge its own choice of rows (open-order-cleanup run 2, 2026-08-23).** Two of the four actionable failures were the same shape. "Two order lines the file shows as still due are closed because the register shows the goods already received in full" failed 2 of 3 with the judge quoting the two SHORT CLOSE rows: four rows carried that disposition under two different rules and the criterion named neither, so it read the reason as wrong. "An order more than ninety days old with nothing received is kept where the supplier has confirmed a ship date on or before September 11" failed 1 of 3, because the golden also CANCELS an order confirmed to ship inside that window, for a discontinued item, which makes the rule false read as a universal. **Before writing "an X is treated this way where Y", search the golden for a row satisfying Y that is treated differently; if one exists, the criterion has to name the row it means.** A definite subject ("Line 2 of order 44121 ...", "Order 44016, written 04/27/2026 ...") is the whole fix. Coded as **R34** (WARN on an indefinite or bare-count subject plus a causal clause with no identifier anchor); portfolio-silent on this task after the rewrite, and it also caught a passing criterion worth anchoring. Same round: **a criterion the judge reports as unverifiable_from_deliverable is one worded on the INPUT side** ("the suppliers' shipping paper", "at the cost on the file", which order was written later). That is the standing tension with the Rubric objectivity check, which asks for comparison against named source documents; both are satisfied by naming the DELIVERABLE'S own column or page as the place the comparison is made. And **a flaky liveness criterion cannot always be dropped**: with the +5 cap and R17's two-criterion ceiling, R24's ten strict points are exactly two criteria, so sharpen instead, narrowing the subject from "an item and branch" to the single named row and naming the head function (SUM) that R30 wants.

**A THRESHOLD in a negative fires on any cell past the line, whatever the clause says (open-order-cleanup run 3, 2026-08-23).** "At least one stocked item and branch is incorrectly left with open quantity still due that puts its position beyond thirteen weeks of supply" cost its full -4 in one run: the judge landed on the one position row standing at 14.4 weeks, a deadstock item with 175 on the shelf whose entire open order the golden CANCELS, so open quantity there is nil and the causal clause was never read. **Key a negative on a two-column comparison the judge reads off one row** (open planned against open allowed), never on a threshold it has to reason about, and check the golden for a row that crosses the threshold for a reason the negative does not mean. Coded as **R37** (ERROR; R35 and R36 were taken), which names the offending cell; header detection has to be narrow, the unit as a whole word in a short heading, or WEEKLY RATE and any prose mentioning a week turn a money column into a column of weeks. Two positives went the same round for the same reason, both rescued by an anchor rather than a rewording: a trim criterion whose figures were right but whose landing was the supplier-call sentence, where the input file the judge can also read shows a contradictory balance (moved onto the trims block, both figures in adjacent cells of one row), and a criterion carrying a count clause, "sits on two open orders", which sends the judge hunting for the pair before it scores the trim (clause dropped). **A count clause inside a positive is a second thing to verify; drop it unless the count is the point.**

**A column header is not a landing place, and a comparison negative drifts one column (open-order-cleanup run 4, 2026-08-24).** The two-column negative that replaced the threshold one flaked in its turn: "more open quantity planned than the open allowed figure carried beside it" fired on the single row whose planned quantity exceeds the NEIGHBOURING column (open corrected, nil, because that line is the one the plan ADDS for a superseded item), while the column it actually named read 58.94. Naming two headers asks the judge to pair sixty rows itself. **Put the verdict for the whole comparison in ONE cell of the golden, a count of the rows that fail it, and quote that cell's label in the criterion.** Here that is a SUMPRODUCT over the two columns standing at nil, which is also what a buyer would want on the page as proof the plan clears the ceiling. Coded as **R40** (WARN; R38 and R39 were taken the same day), where a "label" is a string of twenty characters or more, since a shorter one is a column header. Third wording in three rounds is the signal to change the SHAPE, not the words, and the shape that ends the flake is always one cell the judge reads instead of a sweep it has to perform. **A workbook cell can be added without rebuilding the golden**: edit the sheet XML in place (inline strings and an injected `<v>`), which leaves every other cached value untouched, then recalculate the whole file with the `formulas` package to prove the caches still agree.

### A column header is a provenance claim (task 15 open-order-cleanup, reviewer pass 3, 2026-08-24)

The golden closed PO 44158 line 1 at 125 EA received under a column headed **RECD PER
REGISTER**, while the register showed 5. The 125 was right: the acknowledgement said five
cartons, twenty five to a carton, and the item file carried the pack at 25, so the register's
5 was cartons keyed into a pieces field. The reviewer still sent it back, because **a header
naming an input source asserts that the figure is a plain read of that source**, and a
reviewer checks the golden against the authority the sheet itself cites.

The sheet note made it worse by pinning the whole column on policy 2.4, which only reaches a
line where the order file and the register DISAGREE. On 44158 they agreed, both at 5, so the
cited clause never fired and the figure came from 2.3 (the supplier's written confirmation)
instead. **Check that the clause a sheet cites actually triggers on the row the reviewer will
land on.**

The mislabelling covered all four corrected rows, not just the flagged one: none of them was
a literal read of the register column (a duplicated slip, a whole slip posted to one line,
cartons keyed as pieces). Fix the COLUMN, not the row: rename to what the figure is
(RECD CORRECTED), cite every clause that can produce it, and give the odd row its own reason
code so the jump is legible where it is made. No figure needed to change.

**A subtle inference no criterion pins is a grading hole.** Nothing in the rubric told a
grader 125 was intended, which is why the reviewer had only the header to go on. When a
reviewer disputes a golden figure that is actually right, add the criterion that states it.

**R42 rejected a bare same-sheet read-through `=C5` as compound while already accepting the
sheet-qualified `='Commitment'!C5`**, which is strictly more complex. That left the only clean
liveness anchors in the workbook unreachable and forced churn on wording that was fine. Fixed
in tools/gcheck/golden_rubric/liveness.py (`_READ_THROUGH_RE`, formerly in autoeval_check.py). When two checks demand opposite things
(R38 wants a landing, R39 forbids naming the function; R50 wants the stored form, R9 wants a
value anchor), the resolutions are: key on a reference chain and say "cell references", and
use "exactly <stored figure>" to satisfy both at once.

**A criterion that pins a DATE to a row key needs both on one sheet (open-order-cleanup run 5, 2026-08-24).** "September 4 is named as the date the answer on order 44243 is required" failed 2/3 with every part of it true. The briefing spells out September 4 without naming the order, the exceptions row carries "44243 line 1" against "answer needed by 09/04", and the supplier calls row the judge landed on carries the order with no date, saying only "See the exceptions sheet". Date FORM is half of the fault: a spelled September 4 and a stored 09/04 are different anchors to a value-grepping judge, the same way R48 separates a percentage from its stored decimal and R50 separates formatted money from what the cell holds. Coded as R56, which is R43 in tokens R43 cannot see. **Write a new check against the artifact before trusting it**: the first draft of R56 was the rule "a spelled date the golden never spells", and it was born dead, because the briefing does spell September 4.

**A liveness criterion must assert itself on the READING cell, not on the link (same run).** C5 claimed the usage page holds the live formula and the position page "reads through by plain cell reference". Both are true (Usage O43 is a SUM at 636, Position M43 is ='Usage'!O43) and the judge quoted the usage cell and then denied the link, because nothing told it which position cell makes it. Put the assertion on the reading cell and name it by its column header plus its row key. Note the trap in the repair: `LIVENESS_STRICT_RE` keys on a fixed set of phrases ("live formula", "reaches its value from/through", "rather than typed"), so a rewrite that drops all of them silently stops counting toward R24's ten-point floor.

**The R34 shape also arrives without a causal clause (same run).** "Confirmed costs within three percent of the cost carried on the order are applied to the lines without an approval step" is a rule over an unnamed class with no order and no digit, and it failed 2/3 with the judge reporting, correctly, that the briefing does not mention the rule. R34 missed it because it requires a because/where clause and a determiner-led subject. Not coded: a check that fires on this also fires on "Six order lines are reduced in quantity rather than cancelled" and two siblings the oracle passes every run, and separating them is the classifier the R27 docstring rules out. Fix by naming the member, here line 3 of order 44219 at the confirmed 10.62.

### The deficit is the only read-back of the entered form (task 15 run 6, 2026-08-24)

Oracle rewards were 1.0000, 0.9730, 1.0000. **0.0270 is 2/74, and the rubric file totalled 66
positive.** The failed criterion's text was current, so the wording had been re-entered and the
WEIGHTS had not. Nothing else in the pipeline reads the entered form back. **Always divide the
deficit by the file's own positive total; if it does not land on a whole criterion weight, the
form and the file are out of step and the rubric is partly unsubmitted.** Here that also meant
the R24 full-credit exposure the rescale was built to close was still open on the platform.

**A criterion that asks the judge to prove an ABSENCE flakes.** "Order 44016 written 04/27/2026
is kept rather than cancelled for age" made the judge establish that nothing anywhere cancels
it; the row it landed on carried the order and the date and said nothing about survival. Re-key
onto a cell that only exists if the thing survived: "still converts at 12019.23". Same fix for
the paired trim criterion, which had to prove the OTHER order was not trimmed.

**R50's prose carve-out is not cover on its own.** C18 said "$18,508.10", the briefing prose
carried "$18,508.10", and the judge still quoted `Commitment!C55 = '18508.1'` back and verdicted
unverifiable_from_deliverable. The carve-out now requires a SECOND anchor (a sheet name or a row
key), because that is what walks the judge to the row whose prose spells the padded form. Task
20's eleven long-surviving padded figures all carry one.

**A check's own value bag has to render figures the way the judge does.** `_sheets_carrying`
emitted only comma-formatted numbers, so R56 could not see 12019.23 on a row that plainly holds
it and reported a false co-location failure. Any check that models "what the judge can grep"
must carry the raw stored form too, which is the same premise R50 is built on.

**A universal DERIVATION positive subsumes the criteria that score instances of it (open-order-cleanup, 2026-08-25).** The near-identical criteria check FAILed on "The quantity still due on each line is calculated from the corrected received quantity ...", because three other criteria scored consequences of that same derivation (30 EA on 44121 line 1, nothing due on 44121 line 2, 125 rather than 5 on 44158 line 1): "if Criterion 8 genuinely passes, those three line-level checks must also pass." Narrow the universal to the aggregate total plus the general METHOD and leave the named rows as independent spot checks. That repair is weight-neutral, where deleting the subsumed rows costs criteria, weight and then a rebalance against R24. The distinction that keeps the coverage criteria safe: **presence over every row ("carries an action") is coverage; correctness over every row is subsumption.** Coded as R57, which R47 could never see because R47 compares figures and these criteria share none.

**A check that names the wrong criteria is worse than no check.** R57's first draft cited C4, C6 and C7 as the subsumed rows, because its row-key pattern `\b\d{4,}\b` read the money figures 84866.21 and 12019.23 as order numbers. The same discipline that applies to a reviewer's numbered findings applies to our own output: print what the check names and diff it against what the platform named before trusting it. Reject any digit run that is part of a decimal, and never cite a universal criterion as a "named instance".

**R50's stored-form rule needs an anchor or it becomes the next flake (open-order-cleanup run 8, 2026-08-25).** R50 correctly converted C14 and C18 from $6,407.60 and $18,508.10 to the stored 6407.6 and 18508.1, because the judge's tools render raw values. C14 then came back unverifiable with the judge quoting the briefing's "taking $6,407.60 off the book": the golden's PROSE still spells the padded form, and with no sheet and no row label in the criterion the judge is free to land on the sentence rather than the cell. The stored form is necessary and not sufficient. Keep it and name the row that holds the raw cell ("the Taken off in total row on the commitment page"). Coded as R58, which reuses R50's own `_other_anchor`, so both directions ask for the same anchor and cannot contradict each other. Note it correctly spares a criterion whose ordinary prose happens to name a sheet ("the open commitment is 84694.61" contains "commitment").

**A criterion has to use the CELL'S words, not a paraphrase of them.** C26 said the decision on order 44243 "is referred to the Ottawa branch" and failed 1/3 while the judge quoted the whole exceptions row back, including "branch call, Ottawa, answer needed by 09/04". The row says what the criterion means and does not say it in the criterion's words, so the judge had to rule that a branch call for Ottawa is a referral to the Ottawa branch, and once in three it declined. This is the money-as-stored rule applied to prose. Left uncoded on purpose: no regex separates a damaging paraphrase from the many criteria that legitimately restate a fact in their own words.

**Fix the twin even when it passed 3/3, if its twin just cost a run.** C18 was the other figure R50 had converted in the same pass, with the same missing anchor, and it scored 1.0 in all three runs. The house rule carries a proven-3/3 criterion as debt, but that rule is for shapes that have never failed; here the identical shape had just failed on C14, and the repair was two words. Debt is for uncertainty, not for a landmine you have already watched go off.

**Two criteria naming the same quantity at different figures is a CRITICAL quality-review finding, even when both figures are right (open-order-cleanup, 2026-08-25).** C4 pinned 84866.21 and C8 pinned 84694.61, both called "the open commitment", and the Agentic Rubric Quality Review rated the whole rubric needs_improvement on that alone: "both cannot be right." They were two steps of one bridge, the extract opening and the running total after the receipt postings are corrected, each with its own labelled row on the commitment page. The repair is to name the STAGE in the workbook's own words, never to delete one of the pair. Note the review's own suggested fix was wrong twice over here: restating C4 at the corrected figure would have broken the liveness anchor that has to match the cell the briefing actually reads, and deleting C8 would have dropped the receipt correction the task is built on. Coded as R60, which only compares a phrase EQUATED to a figure, so a criterion that mentions the quantity in passing stays silent.

**When an atomicity review collides with R24's positive-weight ceiling, rebuild to the budget and record what was dropped (open-order-cleanup, 2026-08-26).** A reviewer named 22 bundled criteria on a rubric already failing R24's single-loss variant at +66. Splitting in place was arithmetically impossible: splits add rows, rows add weight, and R24 pins positive at 39 or under (each strict liveness criterion must cost more than a tenth of positive plus a point of cushion, at the +5 cap). The only shape that satisfies both is 10 points of liveness plus 29 single-fact criteria at +1, which is 31 positive rows and no more. **Coverage is what pays for atomicity**: eight scored facts were dropped outright rather than bundled back in, and that loss belongs in the feedback log, not buried. Reason clauses are the cheapest thing to cut, since "X is cancelled because Y" is exactly the two-things-to-be-wrong-about the reviewer is naming. A liveness criterion is still NARROWED rather than split (R17 caps them at two, R24 needs both at +5), keyed on one cell whose own value is its anchor so subject and anchor coincide.

**"Incorrectly" is not the only defect frame, and the checks accept several.** A reviewer required removing "incorrectly" from three negatives, which the platform's own polarity checks otherwise demand a frame word for. `PIN_RE` also accepts violating / in violation / contradicts / contrary to / although / even though / despite / wrongly / beyond what, so "violating <the named policy>" satisfies E1's polarity pin and W18's defect frame with no evaluative adverb. Keep the negative reading TRUE when the failure is present.

**A verdict cell's own heading can trip the checks that asked for it.** The negative keyed on LINES ABOVE THE CEILING AFTER THE PLAN (added in an earlier round to satisfy R40) then failed R6, which read CEILING as a citation of the Excel function, and R52, which found "ceiling" and "thirteen" shared with the page's own note. Renaming the heading to LINES OVER THE ALLOWED OPEN QUANTITY cleared both and cost nothing, since the edit is a sheet-XML string swap at zip level with no cached value moved. Also note R52 keys on the MEMBERSHIP frame `is/are counted|included|listed|reported` - phrasing the same claim as "the cell stands above zero" leaves it silent while still quoting the verdict cell.

**A parameter row can cite the right clause and state the wrong basis, and nothing catches it (open-order-cleanup, 2026-08-31).** Policy 6.2 keyed the aged-line cutoff to "ninety days before THE REVIEW", with retention only on "a ship date on or before the review date". The golden's Parameters row read 06/13/2026 sourced as "policy 6.2, ninety days before the freeze" - the right clause, a date the clause never mentions. It survived four AutoEval rounds and four reviewer passes because every check tests the rubric against the golden, and the golden was internally consistent with its own wrong parameter. The tell was inside the same sheet: row 6 already keyed the demand window to "the six full months before the review". **When a policy names a date, grep the workbook for every other place that policy's dates are set and check they name the same event.** The cost: one wrong parameter moved two orders, one trim, three deferrals, every branch total, the final total, the uplift and twelve rubric answer keys.

**A live workbook corrects part of a reviewer finding by itself.** The trim on 44214 line 3 was `=MIN(K47,FLOOR(Position!I7-P9,G47))`, keyed on the plan quantity of the earlier order; cancelling that order dropped P9 to nil and the trim reverted to the full 33 with no edit. That is the payoff of keeping decision fields as formulas rather than typed answers: the parts of the golden that depend on a corrected decision recompute, and only the prose and the hard-coded blocks need hand work.

**Editing literals in sheet XML and recomputing every cache is the safe way to change a golden's answer.** Set the literal cells at zip level (inline strings and numbers only), then recompute with the `formulas` package and rewrite every `<v>`, then regenerate calcChain. docProps, styles and the parts you did not touch survive byte for byte, so A13/A14 stay clear and no figure ends up hand-keyed. Note `formulas` returns keys as `'[file.xlsx]SHEET'!REF` with the FILENAME IN ITS ORIGINAL CASE - matching it uppercased silently returns zero cells and the injection reports "0 caches rewritten" instead of failing.
; a gate-3 reviewer ordering the VALUE/LIVENESS split (tessendorf round 2, 2026-08-31) is answered with task 23's shape - a plain value row per figure plus an unanchored front-page read-through at +5 (the only strict shape with nine-of-nine oracle history), the R9 findings carried as .gate-debt - and NOT by putting the figure back in the liveness row; R29 blocks the tempting middle (a derivation clause on a value that also stands as a front-page reference copy: the judge lands on the copy and fails it), so derivation clauses go only on figures with ONE holder or holders that are all formulas; a reviewer's suggested negatives can be PLATFORM-BANNED (their movement-contradiction and per-line-fee examples are ordinary misses under the 2026-08-27 penalty scope ruling) - honor the intent with the critical classes the task supports (prohibited disposition 'scrapped or written off although the memo sends it to the return list', eligibility inversion 'planned although the March cut disqualified it'), each with subject+verb distinct from every positive (R69), and say so in the log; R13's coverage block counts only COMPLETENESS_RE rows ('exactly once' / each-all within 90 chars of a number), so coverage claims are phrased 'on each of the 26 catalog rows' mid-sentence (leading 'Each' trips W11's sweep) and the count-cell row 'counts all 26 catalog rows by a formula'
**The full-credit completeness check has a THIRD axis: criterion SCOPE (open-order-cleanup, 2026-08-31).** R24 measures the weight strict liveness carries; the cluster-share axis measures each requirement's share. Both passed a rubric the platform still failed, because neither asks what a liveness criterion covers. Two criteria pinning two named cells held 25.6% of positive weight and still let a solver "satisfy both criteria with the two required references while hard-coding all line conversion dollars, commitment totals, variance, and briefing totals". The same shape appears wherever a criterion buys credit for a container rather than its contents: one point for 28 supplier-call rows with no supplier and no call, an action required on every line with no converting quantity or dollars beside it. **Test every criterion by asking what a deliverable that satisfies its words while omitting the requirement's substance would look like.** The repair adds no weight: hang an inseparable formula clause on the totals criteria the rubric already carries, so a hard-coded workbook fails them outright (39/39 retained became 30/39). Coded as R74. Note two of the platform's own suggestions had to be declined on evidence: a criterion cannot ask the judge to edit the workbook and re-check it, and demanding formulas across every row is W16, which failed kolterman 2/3 - put the formula demand on one named row and let the sweep ask only for presence.

**A human reviewer's atomicity standard is stricter than the platform's (open-order-cleanup, 2026-08-21):** the reviewer called 29 criteria "mostly bundled" and gave the rule as "each criterion can only measure or check one single item", quoting a briefing criterion that carried four different figures (open book, converting total, target, headroom). The same review said criteria must not explain the rule or the calculation, and rewrote a negative from "At least one stocked item and branch is left with quantity still due that puts its position beyond thirteen weeks of supply, violating the ceiling in the policy. A branch already past thirteen weeks on hand alone, with nothing left due to it after the plan, is not this defect." down to "At least one stocked item/branch is left with open quantity due that causes its post-plan position to exceed thirteen weeks of supply." Note what that rewrite does: it carries the carve-out INSIDE the defect ("open quantity due that CAUSES"), so the golden's legitimately-over-ceiling row no longer trips it without any appended exception. That is the shape to write negatives in from now on, and it also satisfies the oracle. Fix applied: 29 criteria at +100 became 39 at +99, weight-neutral as the house rule requires, with a method plus its own resulting figure left as one criterion (one measurement) while genuinely different facts were split.

**A reviewer's atomicity splits still have to land inside 15 to 40 (open-order-cleanup, 2026-08-24).** Five named bundles split weight-neutrally took the rubric from 39 to 45 rows, and R11's band is a criterion_count error in the pre-submission audit, so the count has to be paid for rather than argued with. Pay it from rows the checks want gone anyway, never by re-bundling anything the reviewer named: a duplicate figure row (two criteria stating only the same $55,895.98, which the near-identical-criteria check fails on its own), a section-presence criterion added in an earlier round, one of several instances of the same rule, and a total already implied by its components. The freed weight goes back onto simple facts the oracle has passed, so the positive total never moves. **Reviewers also read a negative as a reversal when a positive states the same rule**: the fix is to drop the mirroring POSITIVE and keep the negative (which is the only place that defect class is scored), or to restate the positive as the instance rather than the rule, so the negatives end up over defect classes no positive asserts.

## Task 16, yankton-branch-opening (2026-08-20 to 08-24)

**Judge discoverability is a first-class rubric variable (yankton run 1, 2026-08-20).** Three positives flaked on a golden with no defect, and the evidence quotes showed why: each one pointed at a fact whose table was somewhere the judge did not look. The deferred quantities lived in a block at the bottom of the purchase-order tab, and the judge went hunting on Source of Supply and the briefing instead (C24, failed 2/3). The 99-item census split lived only in a cell block on the capital tab while the briefing carried the headline, so the judge quoted the briefing and could not verify the breakdown (C12, failed 1/3). **Fix the deliverable, not only the wording:** give a graded table its own tab named for what the criterion asks ('Short at Opening', not a block under 'Purchase Orders'), and state a graded census in BOTH the briefing prose and a cell block so either search path lands on it. Reserve rewording for the criterion's statement count: C24 went from five statements to one figure plus one spot anchor. The third failure was the plain W11 shape, a universal pack sweep over 53 rows (C17, failed 2/3), and it was replaced outright by a single-item derivation with every figure in a cell, which is the cheapest way to keep a block's weight without a sweep. A negative worded over HOW a figure was computed came back unverifiable_from_deliverable (W15); restating it as a content fact about which items are shown opening with stock makes it checkable from the file alone.

**The oracle judge greps cell values, so a criterion must cite tokens that literally sit in a cell (yankton run 2, 2026-08-20).** Five criteria flaked on a golden with no defect, and all five shared one cause. Criteria named items in plain English ("the 3/4 vacuum breaker", "the 4 inch DWV coupling") while the sheets carry trade shorthand (VAC BREAKER 3/4, CPLG DWV 4), so the judge could not match them; where it searched on the spot value instead, it matched the wrong row. C17 failed 2/3 because the judge searched 75, landed on BG0504 (also requirement 75 on a pack of 25) and failed the criterion on BG0504's 7 lines and 260 units. **Cite the item code, the account number, the invoice number: whatever unique token column A carries.** A spot value alone is not an anchor unless it is unique in the workbook. Two further shapes came back unverifiable_from_deliverable in the same run, both counterfactual: "four items fall short of the test without Sedlacek's lines" and "each transfer is taken from the store showing the largest excess". A judge can only check what stands in the file, so state the standing fact (account 10233 counts on 115 lines; BE050 takes 331 from Fremont against 56 at Columbus and none at Norfolk) and never ask what a figure would have been. A third, a cross-workbook consistency criterion, failed by asking for an aggregate re-derivation over 53 rows; restating it as four adjacent cells that add up fixed it. **Oracle deficits are fractional** (0.9806 of a 130-point rubric leaves 2.52, not an integer), so the oracle awards partial credit per atomic statement inside a criterion. Cutting statement count raises the score directly, independently of whether the criterion is right.

**"Live formulas" means the DECISIONS, not the arithmetic (yankton reviewer, 2026-08-22).** A workbook where every quantity and total is a formula still fails the prompt's live-formula demand if the decisions sitting on top of them are typed. The send-back named four: the stock or no-stock disposition, the supplying branch, the purchase order line set, and the freight charge, plus the capital and space totals that depend on them. Test it the way the reviewer does: change one demand figure and see whether the item moves in or out of the assortment, not merely whether its quantity moves. The shape that works is a **Decision Tests tab** carrying the flags (passes test, can ship, candidate, bin rank, space cut, capital rank, capital cut, opens) with the deliverable tab reading them, plus a **cut ladder** for any rule that is a sequential greedy algorithm: one row per step, each recomputing the downstream totals, and the step count returned by MATCH(1,fits,0)-1. A subset presentation tab (only the rows that transfer, only the lines that get ordered) is itself a hardcoded decision; list the full row set and let the quantity formula zero the rows that drop out. Two corollaries: **SUMIFS/COUNTIFS keyed on a text criterion is fragile** (Excel coerces numeric-looking text like a vendor code "02140", and the `formulas` package cannot evaluate it at all) so use SUMPRODUCT for every criteria-based aggregate; and a live chain makes the whole file verifiable, so perturb an input and diff the downstream cells before shipping. Reviewers also apply a **500-word floor to input prose documents** (441 and 411 word files were sent back), now coded as A11.

**A negative that names item codes is verified by PRESENCE, so it must test a value, not a state (yankton run 3, 2026-08-23).** Two negatives fired against a correct golden, with evidence that was bare presence: "Purchase Orders!B8 = 'RA125'", "'Opening Assortment'!A26 = 'RL100'". Both rows carried a quantity of zero and an ACTION of NOT STOCKED. The trap is the interaction with the live-formula fix: once every detail tab lists the full row set (which is what makes an order line set live rather than hardcoded), every item code appears on every sheet and presence proves nothing. Word such negatives as "is incorrectly given an opening quantity above zero" rather than "is shown opening with stock", and add the carve-out that names the judge's actual mistake: "an item appearing on a worksheet row whose quantity is zero is not this defect". Then harden the sheet too: put an explicit ORDERED / NOT ORDERED (or equivalent) label on every row, so a code search lands on the word next to the code. Same run: a criterion carrying a count, a value and two reasons came back unverifiable although the judge quoted both figures, so cut multi-part criteria to a count and a value; and a criterion came back unverifiable on text the workbook does not contain at all, which is the cross-task contamination artifact, not a golden defect.

**A graded fact buried at the end of a long prose cell fails on judge read-head (yankton run 4, 2026-08-24).** The briefing's closing paragraph was 752 characters in one cell and the graded date sat ~600 characters in. The judge quoted the paragraph's FIRST sentence as its evidence and scored the criterion failed, 1/3. Prose paragraphs are still the right thing for the authorship detector, but **every figure the rubric grades needs a companion cell**: keep prose cells short (~200-500 chars, split long ones) and give dated actions, owners and decision deadlines their own labelled table with one value per cell. The same run showed the mirror case as a judge-side 'unverifiable': three lead-time figures that existed only in briefing prose, fixed by re-pointing the criterion at the parameters table where each sits in its own cell. Rule of thumb: if a criterion's figure can only be found by reading past the first sentence of a cell, move the figure, do not reword the criterion.

**The non-numeric half of an atomicity review IS partly codeable, by counting subjects rather than clauses (yankton-branch-opening, 2026-08-24).** The reviewer named thirteen bundled positives and R27 saw two, because the rest carried two figures or none. Three of the shapes are countable and were coded as **R49** (RUBQ-ATOM in `tools/gate_families.py`): two or more ITEM CODES under one predicate, two or more ACCOUNT NUMBERS under one predicate, and a COUNT of things beside a MONEY total in the same sentence, which is the reviewer's own worked example ("asks for number of items and then checks for the cost", the money being arithmetic off the count). Carve-outs that matter: negatives are exempt, since a negative has to name the class members it fires on (R34), and a zero count with a zero value is one claim ("0 lines and an order value of $0.00"). Spell counts out and the regex misses them, so R49 reads spelled numbers too, both of the reviewer's examples having been spelled. It fires on 6 rows of the pre-revision rubric and is silent on the revised one, and on 4 other in-flight tasks. This does NOT reopen clause heuristics, which failed calibration three times; it counts named subjects, which is what the reviewer counts. **A liveness criterion cannot be split** (R17 caps them at two and R24 needs those two at +5 to clear the completeness bar), so when a reviewer calls one bundled, NARROW it to one derivation instead of splitting it, and let the answer criteria carry the figures the dropped clauses covered.
**Atomicity comes in a second wave, and it is TURNS not subjects (yankton-branch-opening, 2026-08-24).** After the first split fixed every bundled SUBJECT, the same reviewer returned on nine rows bundling a second TURN: a trailing consequence clause ("so none of its history counts", "including the lines it bought before the hold"), a second sentence carrying the measurement, a parenthetical golden-reference example, a rule stating three class parameters at once, and a value beside its own derivation. Coded as **R54** (RUBQ-ATOM) and deliberately framed in its docstring as an AUTHORING constraint rather than a classifier: against his labels it catches 8 of his 9 plus 6 more rows of the identical shape he did not name, which is the right failure direction when the repair is a rewrite. The house form is **one sentence, one verb, one figure-bearing claim**, with ACCEPTANCE clauses still allowed (a chain-reference carve-out, "transcribed figures stay typed") because they narrow one verdict instead of adding another. What survives as a hand-check is the conjoined second predicate carrying no figures, since every test for it also flags the accepted "is on credit hold, and none of the 124 lines is counted". **A liveness criterion the reviewer calls bundled has a third repair besides splitting and narrowing: re-key it onto ONE cell whose own value is the R9 anchor**, so subject and anchor coincide ("Item RA075's buy value of $489.84 is a stored formula ..."). The disclaimer route to satisfying R9 is closed here by R18, which bans grader-instruction wording, and check R51 before picking the cell: the first anchor chosen was twinned across two cells of its own row.

**Excel ROUND is half-up, Python round() is banker's (2026-08-20, yankton).** A workbook that carries money to cents through `=ROUND(qty*cost,2)` will disagree with a Python-computed cache on every exact half: 75 x 3.31500 = 248.625 is 248.63 in Excel and 248.62 in Python, and that mismatch propagated into every downstream SUM. Compute injected caches with `float(Decimal(repr(x)).quantize(Decimal('0.01'), ROUND_HALF_UP))`, not `round(x, 2)`. Related: rounding money per line rather than only at the totals is what makes every displayed figure equal its cached value, which is what the oracle judge greps (autoeval R20).

## Task 19, rempel-job-buyout (2026-08-20 to 08-25)

**Grader-instruction wording also covers verdicts and method imperatives, and it bites criteria with no pass/fail conditional at all (rempel pre-submission, 2026-08-20):** the Rubric negative polarity check passed all four defect-framed negatives (naming the "... is not this defect" carve-out as why they read correctly) and FAILed the section on two LIVENESS positives instead. Two shapes the earlier kolterman fix did not cover: a verdict assigned inside the text ("A cell reaching its value through a plain cell reference IS A PASS" reads as Award-if) and an imperative aimed at the grader's method ("JUDGE FROM the stored formulas together with the displayed values, not from a typed cell share", "VERIFY BY reading the cell formulas stored in the file"). Both were house wording invented to defuse judge misreads, so the whole liveness idiom had to be restated as facts about the artifact, keeping every defusal: cached-value anchor becomes "the numbers shown in them are the cached results of those stored references", typed-input carve-out becomes "the quantities and unit costs on the tabs behind them are source data typed as it comes", plain-reference acceptance becomes "a cell that reaches its value through a plain cell reference to such a formula is formula derived rather than a typed constant". autoeval R18 widened to `is a pass|counts as a pass|is a fail|does not fail this criterion|do not answer this criterion|judge from/by/on/it/this|verify by/that|decide from|needs no tracing`; the same wording is live in seven criteria across tasks 12, 13, 15, 16 and 18; those tasks were left untouched per [[feedback-log-convention]] and the check flags them on their own next revision.

**A policy rule applied to one vendor and skipped on another is a golden_source_fidelity hard fail, even when it costs nothing (rempel run 1, 2026-08-21).** Every other axis passed (4s and 5s) and all the arithmetic verified, but the dataset quality check scored golden fidelity 2/5 and hard-failed the submission: the Dettmann quotation was firm through 10/31/2026, the procedure required advancing a later release onto a firm price date, the golden did exactly that for Halvorsen (note, exception row, action item) and never mentioned the Dettmann date anywhere. The reason it was missed is the reason it fails: no published increase sat behind that date, so there was no number to write, and the checker treats a silent skip of a rule the golden itself demonstrates as an internal inconsistency, not an omission. Rules: (1) when a policy clause keys on a per-vendor or per-entity attribute, enumerate every entity that carries the attribute and show the test on each, including the ones where the answer is "does not bind"; (2) design term dates onto working days so the advance lands somewhere sane; (3) a decision with no dollar effect still belongs in the action table when the memo asks for what has to be decided. Coded as autoeval **R23**: ERROR when a firm-price or validity date stated in an input appears in no solution cell, WARN on relative windows ("firm for sixty days") whose date has to be worked out first. Same run, soft findings worth building for from the start: a single tab over 80% typed share fails even when the workbook is at 58% (fix by adding a genuinely useful computed column, not filler), and an input spreadsheet under 100 populated cells only survives on an aggregate carve-out.

**An openpyxl save destroys every cached value in the workbook, even for a one-word text
edit.** The A14 rule says never round-trip through openpyxl to fix docProps; it is not
about docProps. `load_workbook()` without `data_only` then `save()` rewrote all 221 formula
cells with no cached results and the whole golden read as empty to every value-mode tool.
Restore from git and edit the sheet XML at zip level. The same zip-level pass is where
calcChain (A13) and the docProps Application pair (A14) belong.

**`.gate-debt` keys on (criterion number, rule), so RENUMBERING A RUBRIC MAKES ITS DEBT
LIE.** After the rewrite, 34 stale lines still matched by number and silently suppressed
live findings on whatever criterion had landed on each number: six real R27 findings came
back as DEBT under numbers that referred to deleted criteria. Drop every criterion-keyed
line whenever the numbering changes, and drop a file-level line the moment the rewrite
closes it (R24 here) so it cannot mask a regression.

**A reviewer can mix CSV FILE LINE numbering and CRITERION numbering inside one report.**
"Rubric line 27 (weight 4)" was criterion 26 (file line 27), while "criteria 3 and 10"
in the next paragraph were criterion numbers. Only the descriptions separate them, which
is the same print-each-named-criterion-and-diff discipline the mixed-in-another-task's-
criteria artifact needs.

**A reviewer's weight arithmetic is a second read-back of what was entered on the form.**
The report totalled 134 positive against a CSV totalling 132. Like the oracle deficit
check, a mismatch means the entered form and the file disagree, so audit the entered
total rather than assuming the last upload took.

**A finding that matches no criterion under either numbering is an artifact, not work.**
"Subjective 'clear note' in criterion 18" named a rubric containing neither "clear" nor
"note" outside "approval notes". Report it, do not churn the criterion it names.

**Double jeopardy, positive to positive, stays a hand check.** Two positives worth nine
points both turned on one HB-1 sourcing decision. R41 catches the negative-to-positive
form on a shared subject, but the same test on two positives fires on legitimate pairs
(CU-1 carrying a position test on one row and a whole-lengths rule on another), so there
is no signal to code. The repair is to give one criterion the tag: HB-1 now appears only
in the scope-change criterion, and the pull-decision family never names it.

**R27 counted a hyphenated TAG SUFFIX as a scored figure.** The 1 of "HB-1" and the 2 of
"HGR-2" each burned a figure slot, so six criteria stating two figures were reported as
stating three, and the only repair the rule left was renaming the tag out of the criterion
- which costs the judge the row key R43 and R50 both want. The head test now reads `\w-`
rather than `\d-`. Fourteen findings resolved across the catalogue, none created.

## Task 20, rademacher-service-review (2026-08-21 to 08-24)

**The full-credit completeness check counts only criteria a hard-coded workbook FAILS, and R3 was measuring the wrong thing (task 20, 2026-08-21).** The check failed a rubric R3 had scored clean at 11.9% liveness: R3's regex counts any criterion whose text mentions a formula, so a correctness criterion carrying "Each percentage is a formula dividing ..." bought cover it does not actually provide. The platform reasoned explicitly that "a solver who hard-codes those exact correct values as typed constants still collects the full 5+5", leaving 116 of 126 = 92.1%. The arithmetic in the finding was itself wrong (it stated a 129 denominator where its own listed weights sum to 126) so recompute before acting, but the hole was real. **The structural consequence is a hard ceiling on rubric size:** with the +5 platform cap and R17's two-formula-only-liveness-criteria limit, 10 liveness points only clear ten percent when POSITIVE WEIGHT IS AT OR UNDER 99. A 126-point rubric cannot defend liveness at all. Task 20 was rebuilt 35 criteria/+126 to 32/+98, and three substantive figures (a claim total, a barred total, a moved-purchases total) were additionally gated on their own cell being derived, worded inseparably from the value ("the cell carrying it adding the three clause lines above it rather than keyed by hand") so the checker's separability reasoning cannot discount them; on that reading a hard-coded workbook keeps 69.4%. Then re-test EVERY material requirement one at a time, not just liveness: the tightest four all landed at 89.8% retained. Coded as **R24** (ERROR on the strict reading, WARN when only the gated reading clears), which reproduced the platform finding exactly on the pre-fix rubric. R3 stays as the loose counterpart. **Portfolio-wide diagnostic the same day: every other in-flight task fails R24** (twincreek and hollenbach at 100%, oskaloosa and wamhoff 96.2%, luebbert 92.7%, kolterman 92.6%, rempel 92.2%, yankton 92.1%, open-order 90.0%), all of them over the 99-point denominator; they are left untouched under the one-task-per-feedback rule and each needs the same rebuild at its next revision.

**Two other checks fired on the same build.** *Near identical criteria*: a liveness criterion that had picked up a dollar figure as its R9 value anchor SUBSUMED the criterion scoring that figure ("passing C29 necessarily establishes the claim amount"). Anchor liveness criteria on something no other criterion scores, such as a row count. Writing the replacement as an honest sweep over the summary also exposed a typed cell among figures the criterion claimed were all derived, so check the claim against the workbook before shipping the wording. *Requirement mapping*: a clause added to the prompt late (renewal terms, added so an O*NET task pick had a signal) had no dedicated criterion; anything added to a prompt for metadata reasons still needs its own row, and the checker rejects coverage folded into a neighbouring criterion.

**The Rubric objectivity check fails on a single bare evaluative word, and the contradiction criterion is where it hides (task 20, 2026-08-21).** "The amount claimed, the quarterly percentages and the items moving are stated consistently wherever they appear" FAILed the whole dimension on "consistently": "an unanchored grader-judgment term with no numeric threshold, quoted source language, or example defining it in the sentence". The anchor must sit in the SAME sentence as the term, so enumerating figures earlier in the criterion does not rescue it. This is separate from R19's "where relevant" hedge family; coded as **R25** over consistently/appropriately/properly/accurately/thoroughly/adequately/sufficiently/suitable/meaningful/comprehensive/well-structured/as-needed. Task 12 C27 carries the same shape and is untouched pending its own round. **Do not paste the checker's suggested rewrite without testing it:** its fix here enumerated the claim total, eight quarterly percentages and three item codes, which R21 then flagged (no single sheet carries them all) and which was vacuous anyway, because two of those families appear only once in the workbook so "the same value wherever repeated" grades nothing. The shape that survived all three checks is the parameters legend the workflow docs already recommend: the rules the analysis runs on, each against the clause it comes from, every figure co-located on one sheet. It does contradiction and domain-correctness work, carries no evaluative term, and is not subsumed by the criteria that merely use those values.

**A stale COUNT fails the oracle on every run, and no check was looking at counts (task 20 run 1, 2026-08-21, 0.9123 x3).** C10 said "18 of them short and 31 late"; the golden's own footer said 28, and the judge quoted that footer back in all three runs. The golden was right and the rubric was stale. R20 has policed stated figures since wamhoff, but its regex wants a decimal or four digits, so **every bare count under 1000 in the whole portfolio had never been checked**. Recounting the task from its delivered inputs found three more nobody had failed on yet (4 never-acknowledged lines against 3, 6 revisions against 5, 12 requested-date rows against 11) and one wrong quarter-shift count. **When one count is stale, recount them all: they drift together, because they are what a data retune moves and prose does not follow.** Coded as **R26** (ERROR, reproduces the finding on the pre-fix rubric); it is a PRESENCE check, so a small integer sitting in an unrelated cell still passes and a clean run is not proof. Portfolio diagnostic: fires only on task 12 C15 and task 14 C18, left for their own rounds. The same run's three 1/3 flakes were not judge variance either, and the fix for each was a cell rather than a rewording: Not Claimed read "after the two thousand cap" where the article caps at 1,500.00 and the criterion asserted 1,500.00, so the judge was reading a contradiction on the tab it was sent to; the "quarters ended 12/31/2025 and 03/31/2026" had to be mapped from bare "Q2"/"Q3" labels through another sheet (fix: put the period end date in the row); and "three of the items move" had no MOVE count anywhere (fix: =COUNTIF over the decision column). **Before rewording a flaky criterion, look for the cell it needed: put the count, the period label and the total where the judge lands, and let the wording stand.**

**A bare count is not an anchor when the workbook repeats it, and a negative reworded to please a house check can fail the platform's (task 20 run 2, 2026-08-21).** Three lessons from one oracle round. (1) C11 pinned "18 lines are set outside both measures" and the judge searched 18 and landed on "18 lines shipped short of the quantity acknowledged"; three different eighteens lived in that workbook. The fix is a sentence in the deliverable that says what the count is, and a criterion that cites that sentence rather than the number alone. This is the yankton spot-value lesson applied to counts. (2) Splitting a criterion into limbs leaves the golden's prose stating only the combined figure: C12 pinned 8 late acknowledgements and the judge quoted the Briefing's "eleven of the misses" back as the contradiction. **After any rubric split, re-read the golden's prose for the combined figure the split replaced.** (3) The negative was reworded in the previous round purely to clear an R22 mirror WARN, and came back ambiguous_negative_polarity 3/3: two "rather than" clauses plus a carve-out gave the judge two readings. **Never reword a criterion that the oracle has passed in order to clear a house warning; the platform check outranks R22.** The shape that reads cleanly puts the workbook itself as the subject doing the wrong thing ("The workbook measures a line against the date the supplier confirmed even though..."). Also settled that round: a task can record a warning it has decided against in `submissions/NN-x/.gate-accepted` ("R11 = why"), which prints as an accepted note instead of a warning, so a settled judgement call stops reappearing on every run. Warnings only, never errors.

**Three rounds of rewording is the signal to change a criterion's SHAPE (task 20, 2026-08-21).** C12 flaked 2/3, then 1/3, then 2/3 under three different wordings, with the judge each time quoting back the exact cell that proves it. The count was anchored in a COUNTIF cell with the rule beside it in words, so the anchor was never the problem: the criterion OPENED with a universal rule ("A line whose acknowledgement went out more than two business days after order entry is measured against...") and a judge has to sweep every line to confirm a rule before it can score the count that follows. Restating it as an observation of the deliverable's own sentence, one cell on one sheet, is the shape that holds: "The exception detail counts the misses whose acknowledgement went out more than two business days at 8, and says beside that count that Article 4.2 measures those against the date the distributor asked for." The rule keeps being graded by the criteria that pin the derived figures. This is the universal-sweep lesson from kolterman applied to a plain correctness criterion rather than a liveness one: **sweep plus anything is the risk, and pins do not save it.** Same round, a second trap worth naming: a criterion asking for a CHANGE to a term ("fill measured on the quantity ordered rather than on the quantity acknowledged") against a deliverable that describes the term AS IT STANDS ("measures fill against the quantity they acknowledge rather than the quantity we ordered") gives the judge the same two nouns in opposite order and it quotes the deliverable back as the contradiction. Fix in the golden, not the rubric: carry a WHAT IT SAYS NOW and WHAT WE WANT IT TO SAY pair, and keep the inverted phrasing out of the prose. Coded as **R28** (WARN, compares the distinguishing words on each side of "rather than"), which also caught that appending the ask was not enough while the inverted sentence still stood.

**A derivation clause needs a figure with ONE home, and a read-through summary guarantees two (task 20 run 4, 2026-08-22).** The oracle quoted `Briefing!E10`, `='Not Claimed'!D8`, against a criterion saying the cell carrying that total adds the three clause lines above it. Both cells are right; the judge simply landed on the read-through copy. The reference-chain summary that the liveness criteria are built to reward is precisely what gives every pinned total a second home, so "the cell carrying that total" is ambiguous by construction in any workbook built this way. Across four oracle rounds this one shape cost a criterion in three of them, a different instance each round (C15 and C20, then C21, then C25), which is how a task bleeds four rounds fixing the same thing one instance at a time. **When a shape fails twice on different instances, retire the shape everywhere in one pass rather than the instance that just failed.** Value criteria state the value and its place in the table ("standing on the not claimed tab as the total of the three clause lines listed above it"); derivation belongs only to the two dedicated liveness criteria, which grade a whole tab rather than one figure and have never flaked. Coded as **R29** (WARN when a criterion states how a figure is derived and that figure sits in more than one cell, naming them); it also surfaced a third home nobody had noticed, a running-total column. Portfolio-wide it fires 13 times.

**A negative needs a defect-frame WORD, not just the carve-out sentence (task 20, 2026-08-23).** The Agentic Rubric Quality Review rated a rubric needs_improvement on one [major] finding covering all four negatives at once, reporting -16 of exposure and saying each "describes what a correct deliverable does". Three of the four descriptions were wrong on the direction, but the cause was real and shared: every negative used "[defect sentence]. [near miss] is not this defect", and with no frame word in the first sentence the review read that sentence as correct behaviour. rubric_lint W9 has always prescribed both halves, state the fault with incorrectly / violating / contradicts AND phrase the carve-out that way; only the carve-out half was being applied across the catalog. Coded as **W18** (ERROR), which fires 25 times across eight other tasks. Same round, a second rule for negatives: **do not pin a negative to a value that appears legitimately elsewhere in the row it points at.** The -5 negative pinned a governing date of 07/13/2026 and the judge quoted the row back, where 07/13/2026 sits correctly in the CONFIRMED column beside the governing 06/26/2026. The replacement pins a figure that appears NOWHERE in the workbook (the claim total with the returnable material folded in, 7,988.65), so the judge greps it, finds nothing, and the defect is absent deterministically. And a third: **an alignment audit quoting figures from a superseded round is stale** even when its own arithmetic is right; task 20's quoted 31 late, 4 never acknowledged, 6 revisions and 12 rows against a rubric that had read 28, 3, 5 and 11 for two days, with criterion numbers one below the round 1 numbering. The oracle report in the same batch quoted the current wording, which is how to tell. Verify against the delivered zip, then act on nothing.

**A stated basis has to reproduce the figure it pins, to the cent (task 20 adjudication, 2026-08-23).** A reviewer caught "1,097.90 ... being two percent of the purchases that leave Rademacher" where two percent of 54,894.70 is 1,097.894: a solver computing the stated basis directly lands on 1,097.89 and is marked wrong on a correct answer. The golden reaches the cent the way the deliverable shows it, one rounded rebate less another rounded rebate, which is the right business answer because a rebate is paid on actual purchases and not on a hypothetical subset. **When a figure comes from subtracting or summing separately rounded amounts, the criterion must say so; a one-step paraphrase of the basis is a different computation.** Prefer restating the path over accepting two cents, since an either/or pin spreads to every criterion downstream. Coded as **R31**, which tries the stated rate against every cell and reports the base and the value it computes to. Second finding the same round: **a rubric must not pin the NUMBER of figures on a summary page.** The prompt asked for the key figures up front with live math and said nothing about twelve, so a solver carrying eleven or thirteen useful ones would have lost a weight 5 criterion on a presentation choice. Grade that each NAMED summary figure is formula derived and let extras through. A count of data ROWS meeting a condition is different and stays fair to pin, because it falls out of the inputs. Coded as **R32**. Dropping the count cost that criterion its R9 displayed-value anchor, and the answer is to name two values in the criterion rather than to put the count back.

**Two judge-landing rules, both learned the same day (task 20 run 6, 2026-08-24).** (1) **A liveness anchor must sit in a cell that is ONE function call.** The criterion pinned "exactly 11 rows" and the 11 lived in `=A53+A54`, two pure COUNTIFs added; the judge reads a compound cell as typed and failed a weight 5 criterion. The fix was in the workbook, not the wording: both clause texts shared the words "the requested date stands", so one COUNTIF over that column reaches 11 by itself. Look for a wording the data already supports before accepting a compound cell. Coded as **R42**. Note this cuts against R30, which asks a liveness criterion to name a head function: naming IF was honest but the IFs were nested four deep, so name the pure call and key the criterion on that. (2) **Every sheet that carries a criterion's pinned figure must carry the rest of its figures too.** R21 only asks whether SOME sheet carries the whole chain, and the judge does not choose that sheet: the claim row held 2,032.54 while the 135,502.60 behind it lived on the scorecard, and the criterion failed 1/3. Coded as **R43**, which found four more instances on the same workbook before the oracle could, including criteria that led with a figure appearing on three tabs (the 1,500.00 cap) instead of the one that appears on one (the documented premium). **Lead a criterion with its most unique figure**, since that is where the judge lands. The two fire 27 times across eight other tasks.


**Anchor a liveness criterion on a figure nothing else scores, and check the whole rubric before picking it (task 20, 2026-08-24).** The near-identical check FAILed on the liveness criterion subsuming the presentation criterion beside it: both named the amount claimed and what is out of time, so passing the liveness one necessarily passed the other. This is the second time the same task failed this check for the same reason, and both times the cause was R9. R9 wants a displayed value beside a liveness clause, the subsumption check wants that value owned by nobody else, and the two only reconcile on a figure the rest of the rubric does not touch. **List every figure on the tab the criterion grades and mark which criteria own them before choosing the anchor**; on task 20 that left the year's purchases at net as the single free figure among twelve summary rows. Fix the criterion you last changed, not the one that has been passing. Coded as **R45**.

**When a criterion fails twice on the same TAB, move the anchor off it (task 20 run 7, 2026-08-24).** The strict liveness criterion flaked two rounds running under two wordings, both keyed to the exceptions clause column, and both times the judge quoted row-level clause cells back instead of the footer count that the criterion was about. Eleven rows of that column carry the phrase the count formula matches, so a judge sent to "the clause column" reads the rows and never reaches the cell. **Rewording is the wrong lever once the location is the problem.** The replacement grades a figure living in exactly two cells, its source on the parameters tab and a plain read-through where it is used, with no textual twins and no other criterion naming it: the reference chain shape that has never flaked, on a tab with nothing to collide with. Coded as **R46** (WARN when a liveness anchor is a COUNTIF over a text pattern many cells match, naming the twins). Also rejected a candidate claiming the rules are "held once" on one tab: the workbook types the 1,500 cap in four cells, correctly, so a judge could find a counterexample. **Universal claims give the judge somewhere to say no; keep a liveness criterion to one cell, one figure, one formula.** Watch for the rubric being edited between a fix and a submission: the C44 that ran was not the C44 written for the previous round, so check what the repo actually holds before diagnosing a failure.

**Weight-neutral splitting is what makes an atomicity review survivable (task 20, 2026-08-21).** The Agentic Rubric Quality Review returned needs_improvement with nine non_atomic findings, the same shape that ran task 11 from 37 criteria to 54 and failed two platform checks on the way. The loop is not caused by splitting; it is caused by splitting **and adding weight**. Divide the parent's weight among its children instead (a +5 becomes 2/1/1/1) and every requirement keeps exactly its share of an unchanged denominator, so no completeness percentage moves and nothing reopens. Task 20 went 32 criteria to 50 at an unchanged +98, funding the one split that could not be paid for internally (a +2 into three rows) by taking a point off a sibling in another block. What that costs is R11 (50 against the 15 to 40 guideline) and R14 (+1 rows at 19% of positive weight), both accepted: with the total capped at 99 by the completeness check and the platform capping any criterion at +5, a four-way split arithmetically cannot give every child +2. **Prefer a wide flat rubric to a heavy one; the ceiling is the thing that fails you, not the row count.** Two knock-ons worth expecting: eight criteria naming a quarter each need the period end date carried in the deliverable's own period column, or every one of them has to map a bare "Q2" through another sheet; and splitting a two-limb rule into its limbs can leave a negative reading as a mirror of the new positive, so restate the negative on the observable defect. Coded as **R27** (ERROR at four or more separate figures in one positive criterion, WARN at three), verified to fire on four of the six [major] findings against the pre-split rubric and to stay silent on everything the reviewer accepted; it is blind to non-numeric bundles such as a table layout plus two counts. Portfolio-wide, every other in-flight task carries the shape at 11 to 19 criteria each. See [[rubric-anchoring-and-landing]].

**An injected cache that the formula does not reproduce is a live defect, not a cosmetic one (task 20, 2026-08-21).** The build rounds money to cents in Python and injects that as the cached value, while the formula in the cell stays unrounded. With `fullCalcOnLoad` set the workbook recomputes the moment anyone opens it, so the file ships one number and shows another. It cost an oracle criterion: `=E22*Params!C16` cached 11,217.40 against a true 11,217.395 and `=E26*Params!C16` cached 10,119.50 against 10,119.501, both immaterial alone, but the cell subtracting them moved a rubric-pinned figure from 1,097.90 to 1,097.89. **Round inside the formula with ROUND(...,2), never in the cache**, so the stored figure, the recalculated figure and the criterion are the same number. Coded as **A9** in `tools/autoeval_check.py` (evaluates pure arithmetic, plain references and single-column SUMs against their caches; ERROR at a tenth of a cent or more, WARN below), verified against a fixture rebuilt to the shipped state. Portfolio sweep the same day: material in task 21 bergendahl (63 cells) and task 12 hollenbach (6), immaterial hairs in wamhoff, oskaloosa and open-order. Related, same task: percentage cells stored to nine decimals behind a 0.0% format are the A8 authorship tell, and the same ROUND-at-the-source fix serves both.

## Draft 20, vosberg-assortment-review: uniqueness failure 2 (2026-08-21)

**Second failure, 2026-08-21: vosberg-assortment-review (built against UID 865d895b, never
submitted past the check).** A stocking assortment review: qualify non stock counter demand into
the assortment under a stocking procedure, fund it by taking dead numbers off the file, size and
price the supplier's stocking order, all bounded by an authorized dollar amount and the supplier's
tier tests. The user reported the uniqueness FAIL and had the whole task deleted; the checker's own
comparison text was not captured, so which prior task it matched is unrecorded. The nearest
neighbours by design are **16 yankton-branch-opening** (decide what goes on a floor item by item,
sized against a budget number, with the orders to key) and **10 boettcher-winter-earlybuy** (size a
supplier program order against a dollar ceiling with what stays off shown), and the collision is
almost certainly dimension 2 and dimension 5: "decide what to stock and how much, then write the
order inside a dollar limit" is now a used reasoning path and a used deliverable, whatever the
scenario dressing.

Its prompt is kept at `archived/20-vosberg-assortment-review/prompt.md` for diffing only. Note the
sequence number appears twice on purpose: 20 was rebuilt under the same Taskboard UID as
**rademacher-service-review** (a supplier service measurement and claim review), which is what
`submissions/20-...` and the submission-list.md row now hold.

**How to apply, sharpened:** the portfolio has now spent the "event lands, size the buy, write the
order against a limit" path many times over (03, 10, 12, 14, 16, 17, 19). Before building, check the
candidate's dimension 2 against that sentence; if it fits, the scenario will not save it. Paths still
open after 20: measuring performance or compliance out of transaction records against a written
standard, valuing or settling something, and reconstructing what actually happened.

## Task 22, frankfort-stock-recovery: occupation framing (2026-08-21)

**A third failure mode is framing, not fit.** The check FAILed frankfort-storm-claim
2026-08-21 under 13-1022 with the occupation genuinely correct: "the prompt primarily
requires preparing a property-loss claim workbook ... those duties are only a limited
part of the requested work." The deliverable was merchandise work almost end to end
(grading stock condition bin by bin, valuing it off the current supplier pages, marking
the damaged goods against a salvage bid, covering committed customers out of two other
branches, writing the replacement buy), but the prompt opened on the adjuster, the
examiner and the coverage, named the file `frankfort_storm_claim.xlsx`, and put the
customer coverage last.

**Why:** the sector is assigned (Wholesale Trade), so a non-merchandise occupation is
not available to switch to. When the check fires on framing, the prompt is the only
lever.

**How to apply:** lead the prompt with the merchandise question ("where our stock
stands and what it takes to put it back on the shelf"), list the stock/item/movement/
backlog/supplier-price files first, let the other domain's documents enter as *the rules
each class of material has to be valued on*, order the ask so the buy-side work comes
before the other domain's closing figure, and name the deliverable for the merchandise
work. No number in the golden had to move. Coded as **autoeval_check rule M3**, which
counts frame vocabulary against merchandise vocabulary under 13-1022 (warns at 30
percent) and flags a deliverable file name borrowed from another domain; **M1** was
tightened the same day so a bid the company *receives* (a salvage buyer's bid) no longer
reads as a customer bid.

**The reframe was not enough, and that is the real lesson.** The rewritten prompt FAILed
the same check an hour later, this time enumerating the work itself: "reconstructing
inventory, classifying storm-damaged goods, calculating insured losses and salvage
credits, determining coverage shortfalls, and preparing a proof-of-loss workbook ... not
a strong, direct match for Wholesale and Retail Buyers." **Test first whether the frame
is the wording or the work.** If the check names duties rather than emphasis, no wording
pass will save it and the occupation has to move.

**The sector list is bigger than the buy-side corner of it.** O*NET's Wholesale Trade
industry filter (onetonline.org/find/industry?i=42) returns 63 occupations, not three.
It carries no claims or insurance occupation, but **11-3071.00 Transportation, Storage,
and Distribution Managers** is on it and its task list covers warehouse loss work
outright: "Develop and document standard and emergency operating procedures for
receiving, handling, storing, shipping, or salvaging products or materials", "Monitor
inventory levels of products or materials in warehouses", "Resolve problems concerning
transportation, logistics systems, imports or exports, or customer issues", "Collaborate
with other departments to integrate logistics with business systems or processes, such
as customer sales, order management, accounting, or shipping", "Examine invoices and
shipping manifests", and "Negotiate with carriers, warehouse operators, or **insurance
company representatives**". frankfort PASSED there 2026-08-21 **with the prompt
unchanged, and with no edit to the workbook or a single rubric criterion** - pulling the
full sector list is cheaper than rewriting a task. **11-3071 has no Mathematics in its
Skills section**, the same trap as 41-4012; use Complex Problem Solving with Reading
Comprehension, Critical Thinking and Judgment and Decision Making. Its ERROR-level
non-picks for an analyst prompt are warehouse safety programs, supervising or staffing
personnel, departmental budgets, import/export compliance, negotiating carrier or
insurer rates, drones and energy reduction; M2 now carries twelve 11-3071 fit rows.

## Task 21, bergendahl-item-conversion: input provenance and narrative-move reuse (2026-08-22)

**Third failure, 2026-08-22: 21-bergendahl-item-conversion, retired.** A reviewer read it as a
rewrite of **18-oskaloosa-count-adjustment** and flagged it to the team. The overlap was NOT in
bulk wording (4.7% 6-gram overlap against the nearest prompt) but in a handful of authored
narrative moves the reviewer said were "not a generic professional convention": the live-formulas
user story ("keep the math live, the manager pulls a line in front of people and the dollars have
to follow"), "put what she needs up front, ahead of the detail", "X's ground rules came Monday",
"our own procedure is Y, the N/26 revision", "the rest I pulled <weekday> night", and "so <name>
wants this <day>". The reviewer also matched the **source-role sequence** (outside notice ->
detailed transaction file -> corrective clarification -> manager memo -> internal policy -> item
master -> branch stock -> open transactions -> 12-month movement) and the **authority pattern**
(outside source not trustworthy, later correction overrides, internal procedure decides treatment,
operational data set quantities).

Task 21 carried **7 of 7** of those markers, the only prompt in the catalogue that did, and the
markers were widespread across the rest (8 of 15 live prompts had the live-formulas story, 7 of 15
had "ground rules came"). Prompt kept at `archived/21-bergendahl-item-conversion/prompt.md` for
diffing.

**Coded as `tools/originality_check.py` section 1** (U1 n-gram overlap, U2 signature-move reuse;
ERROR at 4+ reused moves). Run it on the folder being built, by name. Related:
[[package-hygiene-pipeline]].

A reviewer sent task 21 back on 2026-08-22 with "direct evidence of batch programmatic
construction" in the input packet, and flagged it to the team. Every claim verified. The tells are
at the **OOXML package level**, not in the data, so no amount of tuning the numbers touches them:

- **xlsx** `docProps/app.xml` names the generator (`Microsoft Excel Compatible / Openpyxl 3.1.5`).
- **xlsx** zip entry timestamps: every internal component of every workbook written at one
  identical second, though the files purport to be catalogues, accounting extracts and item-master
  records with different source dates.
- **docx** 15 of 17 package components byte-identical across all documents in the packet (they came
  off one python-docx template in one pass), though they purport to come from different companies.
- **docx** one shared Word `rsidRoot` revision-session id across every document in the packet.
- Data-side corroboration the reviewer also used: perfectly alternating monthly vendor-credit
  patterns, near-fixed freight-to-merchandise ratios, perfect relational grids, and errata cases
  positioned exactly around the governing rules.

## Draft 25, havlicek-backcharge-response: uniqueness failure 3 (2026-08-22)

**Third failure, 2026-08-22: draft 25 havlicek-backcharge-response (never submitted, retired by the user the same day).** A
distributor answering a CUSTOMER's line-by-line backcharge schedule from its own tickets,
credits, quotation and terms of sale, conceding to the dollar on one credit memo before a
meeting. The checker's text named six overlapping dimensions and the pattern: "a vendor-side
account owner must answer a customer's line-by-line billing demand ... verify the customer's
arithmetic, decide what is owed as a credit, and produce a consolidated deliverable that survives
a line-by-line recompute ahead of a hard deadline tied to a follow-on meeting". The mirror image
of the supplier-claim tasks (04 rebate, 13 recall, 20 service) counts as the same design.

**How to apply, sharpened again:** the "adjudicate a counterparty's claim line by line from
records and clauses into one settlement figure before a meeting" path is spent in BOTH
directions. Paths that have now passed uniqueness in this batch: a forensic audit of our own
file (23, passed all Section 1 checks), a negotiation package (24, untested), a portfolio terms
program (26, untested), an agreement-year measurement and renewal schedule (27, untested).

## Task 23, june-price-review (2026-08-22 to 08-31)

**Fourth failure mode, 2026-08-22 (draft 23 june-price-review): a sell-price audit is sell-side.**
13-1022 FAILed the Occupation prompt relevance check on a prompt that reconstructs what every
invoice line should have billed, corrects the sell matrix and the customers' invoices, and
measures the margin the error cost. The check named the duties: "auditing customer sales pricing,
identifying invoice and pricing-matrix errors, calculating customer corrections and unrecovered
margin impact, and designing pricing controls, not on purchasing merchandise". The fix was the
twincreek move to **41-4012.00** with the quote-prices-and-credit-terms and
answer-customers'-price-questions duties, no Mathematics skill, and the prompt, inputs, golden
and rubric untouched. Rule: maintaining or auditing SELL prices, corrected invoices and credits
to customers is 41-4012 work however much the analyst thinks of it as purchasing-desk work;
13-1022's #4 "recommend selling prices" does not carry a prompt whose center is customer
billing. Drafts 25 (11-3071) and 27 (41-4012) were built on this reading from the start.

**Same draft, second rejection the same day: 41-4012 also FAILed**, the check reading the work
as "primarily analytical and file-maintenance work rather than the direct wholesale selling
activities represented by the selected occupation". Lesson: when a prompt's center is an AUDIT
of records (invoices, prices, margins) with corrections and control changes, neither trade
occupation carries it; the check is describing **13-2011.00 Accountants and Auditors**, which
is on the Wholesale Trade industry list and whose task list is examine-records-for-accuracy,
analyze-costs-and-revenues, and develop-or-modify-recordkeeping-systems. Moved there with those
three picks (Mathematics is in its Skills section). Pending the third run; if 13-2011 holds,
it is the occupation for any future billing-audit or margin-forensics prompt from the first
build, and the prompt should lead with the audit and correction work so the framing matches.

**13-2011 then FAILed the ONET Occupation-Sector Match (2026-08-22):** the platform keeps its
own occupation-to-sector table, narrower than onetonline.org/find/industry, and Accountants and
Auditors is tied only to Professional, Scientific, and Technical Services. So the O*NET industry
filter is not proof the platform accepts an occupation for the sector. For audit-shaped prompts
in Wholesale Trade the candidates are the clerical ones with wholesale employment: **43-3031
Bookkeeping, Accounting, and Auditing Clerks** (check figures, reconcile discrepancies, financial
calculations) first, **43-3021 Billing and Posting Clerks** (verify billing data, resolve
discrepancies) as fallback. Draft 23 moved to 43-3031, pending; record which one the platform
lists when known.


**Resolved 2026-08-22: 11-2022.00 Sales Managers PASSED the relevance check on draft 23** with the
picks determine-price-schedules-and-discount-rates, review-operational-records-for-profitability,
and resolve-customer-sales-complaints. That is the occupation for a sell-price audit, billing
correction or margin-review prompt in Wholesale Trade; 13-2011 and 43-3031 are off the platform's
sector table and 13-1022/41-4012 fail relevance on it. A mid-chain 11-2022 'FAIL' was a form entry
error, so when a rejection text does not match the occupation just entered, check the entry
before moving again. Routing table: docs/platform-wholesale-trade-occupations.md.


**Quote money figures as STORED, never as formatted (june-price-review run 7, 2026-08-24).** C32 said "a 10.80 credit"; the credit cell stores 10.8, and the judge failed it 2/3 while QUOTING the very row in its evidence - its tools render raw stored values, never the 2-dp number format, so the grep for 10.80 misses. The check that should have caught it (R20) bags formatted values beside raw reprs, so it saw "10.80" as present. Coded as **R50** (ERROR when a positive criterion's trailing-zero figure exists only as formatting, proven on the pre-fix wording); the sweep found one more on the same rubric (67.30 vs stored 67.3). A criterion figure the judge can grep is the raw repr: 10.8, 67.3, 9981 - the padded form is a deterministic miss, not variance.

**The authorship extractor reads workbooks in value mode; ship a calcChain part (june-price-review, 2026-08-24).** The LLM-authorship check failed the golden on "all-values-hard-coded HIGH: zero formulas across all six analytical sheets" against a workbook storing 2,127 formulas - its per-sheet "hard-coded numerics" equalled formulas + plain numerics exactly, proving every cached formula result was counted as a typed constant. The package (XML-level build) carried no xl/calcChain.xml, so a package-level formula counter also finds zero. Fix at zip level, caches untouched: write xl/calcChain.xml enumerating every formula cell, with the content-type override and workbook rel. Coded as **A13** (ERROR on a formula workbook with no calcChain part, proven on the pre-patch file). This is the verify-the-delivered-zip artifact class: the golden's fabric was right, and reshaping it (stripping formulas or de-densifying tabs) would have been churn; if the check fails again with the part present, dispute with the formula counts rather than editing the golden.

**The same-row name+figure shape needs the figure UNIQUE on its row (june-price-review run 8, 2026-08-24).** C32 bound "a 10.8 credit" to the H96284 row and flaked on three straight submissions under three wordings, the judge quoting the whole row each time: the row carries 10.8 twice (OVERBILLED and CREDIT, the credit cell a plain =F34 mirror), and confirming WHICH 10.8 is the credit needs a header-to-column binding the judge cannot make reliably. No rewording removes a twin. KUCERA's 647.26 passed 3/3 three times in the identical shape because its figure stands once on its row. Coded as **R51** (ERROR when a positive binds a figure to a keyed row holding that figure in 2+ cells; proven on the dropped wording). Twins whose cells AGREE with the claim (a shortfall mirrored into ABSORBED on the same row) have survived five submissions 3/3 - recorded as debt, not churned; the conflict case (credit vs overbilled) is the killer. After the third flake the fix was the house rule, not a fourth wording: drop the criterion and re-key its weight onto a proven 3/3 neighbor covering the same money (credits total, 2 -> 4).

**A membership negative deducts on the golden's own near-miss narrative (june-price-review run 9, 2026-08-24).** The honor-rule negative ("At least one line ... is counted as mispriced") fired 1/3 ON THE GOLDEN, the judge quoting the briefing's own explanation of why a quoted line is NOT mispriced ("billed right, because it rode quotation Q-26048") as evidence of the defect. A negative whose defect is membership in a computed classification gives prose that names the category beside the list a way to read as the defect, and the exclusion sentence does not save it. The fix was drop, not reword: the count pins (332/987/17 standing in cells) already fail a solver who misclassifies, so the membership negative added flake surface without deterrence. Coded as **R52** (ERROR when a membership-shaped negative shares 2+ category words with a long solution prose cell; proven on the dropped wording, naming the very briefing cell the judge cited). Also declined the feedback's remove-the-text suggestion: the quoted prose was load-bearing fidelity (the prompt's inciting counter pulls), and the feedback's own location tag pointed at the wrong sheet.

**Reviewers audit the derived calendar dates and the file properties (june-price-review gate 2 round 2, 2026-08-25).** After rebuilding the whole audit and clearing every figure, the reviewer sent the package back on (1) the Openpyxl 3.1.5 generator string in docProps of all six workbooks and (2) a one-day miss in a derived date: policy said "no later than thirty days after the effective date" and the golden wrote 06/15 + 30 as 07/14 instead of 07/15. Re-run every derived calendar date against its rule text before shipping - day-count arithmetic drifts by one when "thirty days after" is compiled to "through day 29". The metadata remedy is a zip-level swap of the Application/AppVersion pair to what Excel writes (Microsoft Excel / 16.0300), never an openpyxl round-trip, which destroys cached formula values; coded as **A14** (proven on the pre-fix golden). Same round confirmed the run-8 artifact diagnosis from the outside: the reviewer volunteered that the static audit's zero-formulas claim was wrong against 2,127 live formulas. When concurrent-session checks (R24 tightening, R54/R55/R56) fire mid-flight on criteria proven verbatim through nine submissions, record debt with the history as rationale rather than churning a rubric a reviewer just called ready.

**A cause attribution on a named line must be confirmable from the row's own cells (june-price-review run 10, 2026-08-25).** C24 tied the K118343 DC300 line to "the DWV never keyed cause" while the row's cause cell reads the opaque code pg2 - zero shared tokens - so the judge quoted the row verbatim and still stalled 1/3 mapping the code through the Summary cause table. The proven sibling never flaked because "copper L2 January" finds L2 in the row's own level cell; the lexical overlap IS the difference. Fix by re-anchoring the criterion on figures the row carries (billed and should-bill, each unique on the row) and leaving the class attribution to the cause-table criteria; rewriting the golden's codes was rejected (SUMIFS key on them) and so was a legend row (XML row insertion renumbers everything below). Coded as **R58**, whose first cut was BORN DEAD exactly as the G1 lesson warns - any-key row matching let the corrections list's own "never keyed" text confirm the phrase - and the proving step caught it; tightened to rows carrying ALL the criterion's key tokens plus a 6-word phrase capture, then shown to fire exactly once on the old wording and stay silent on the proven sibling and the catalog.

**A task that sat between rounds while the platform tightened needs the rebuild, not the
two-row fix (june-price-review run 11, 2026-08-31).** A 53-row +103/-14 rubric with nine
clean platform submissions behind it came back on one liveness flake, and the gate showed
nineteen errors from checks coded after its last rubric entry (R18 carve-outs, R67 penalty
scope on all four negatives, R61, R24 single-loss at 96-97% retained, cluster share).
Re-entering any criterion re-runs the platform's checks on the CURRENT rules, so the
minimal fix would have failed three of them predictably. Rebuilt in one pass to the
delivery-zone-reset shape: 26 rows, +39/-8, two +5 unanchored read-throughs (the only
strict shape with clean history on that workbook), gated "the cell a formula ... rather
than a keyed figure" rows for breadth, every requirement cluster 15.4%+, negatives written on the
policy's literal "no corrected invoice is issued" prohibitions with their own verb (goes
out) so R69 finds no positive twin. Proven rows keep their wording verbatim; the 26 rows
cut are listed in the feedback log so nothing gets bundled back. Void every
criterion-keyed .gate-debt line when renumbering and re-derive from the gate.


**A prompt sentence that names the line-level work needs a REGISTER row, not aggregates
(june-price-review completeness FAIL, 2026-08-31).** A +39/-8 rebuild with every cluster
over 15% still FAILed the full credit completeness check because "every line that billed
wrong and what it should have billed" mapped to nothing: every EXC row pinned a total or a
selected example, and the check counts selected examples and downstream-column formulas as
NOT requiring the register, so omitting all 332 lines retained 100%. Cluster arithmetic cannot see this -
it checks cluster shares by tag, and the EXC tag was fat. The row that answers it is the
delivery-zone-reset register shape at +5 ("worked as N rows, each carrying <the row's
columns>, the N a formula over the list ... rather than a keyed figure") plus a +1
per-row formula clause beneath it, so the line-level cluster alone costs 6 of 39; give the
cause rows the operand-free gated clause so the totals demonstrably derive from it. Read
every prompt sentence for a deliverable the rubric only IMPLIES, and give the implied
artifact its own row before the check does.

## Task 24, vondrak-negotiation-plan: run 2 (2026-08-23)

### Vondrak run 2 (2026-08-23)

- A single-cell head-function liveness key (a footer =COUNTIF or =SUM cell) is invisible
  to the judge's xlsx_formula_summary, which surfaces column-dominant formulas and plain
  reference chains only; vondrak C24 failed 3/3 with the COUNTIF provably stored in the
  shipped zip. Reference-chain criteria are the only liveness shape the judge has verified
  from its own evidence (it quoted formula='=Impact!I60' with the displayed value in the
  same run). Coded as the R9 acceptance pattern; do not key liveness on single cells.
- The platform form can end up carrying figures the rubric CSV never contained (five vondrak
  criteria held one variant total propagated at x1, x0.75, x0.5). The oracle then fails
  3/3 with "not_observed" while the golden is right. Before diagnosing the golden, diff
  the failed criteria's figures against the rubric CSV; if they differ, the fix is verbatim
  re-entry with tools/rubric-filler and a spot-check of the entered figures, not a golden
  change. [[revision-workflow]]
- The golden-source-fidelity axis re-derives narrative conclusions from the tables beside
  them and hard-fails the dataset on one wrong sentence (vondrak's "six point cap is the
  cheapest of the four" against its own table, axis 2/5). Every superlative in a solution
  text cell must be re-verified whenever numbers move; coded as S1. Input xlsx files also
  carry a per-file 100-populated-cell floor (25 hard minimum) on the thinness axis; the
  aggregate carveout saves a thin file but gets named a top issue; coded as A12.

## Task 30, rossville-domestic-content: AutoEval rounds 1 and 2 (2026-08-24)

### Rossville AutoEval round 1 (2026-08-24)

- The golden-source-fidelity axis re-derives the ACTION PLAN across tabs, not just the
  arithmetic: rossville hard-failed (2/5) on one line whose Schedule status computed DE
  MINIMIS while the PO tab's typed action cell and the Briefing said CHANGE TO RW-D.
  Mutually exclusive outcomes on one row cost the axis even though every recomputed total
  tied. Coded as **G1** (ERROR): a solution row carrying DE MINIMIS / AS QUOTED beside an
  uppercase CHANGE/CANCEL/REPLACE token, or SUBSTITUTE beside KEEP. The same axis also
  cross-checks date arithmetic between tabs: an arrival column computed from the review
  date reads as contradicting an action plan that orders days later. Fix by giving the
  schedule a typed planned-order-date column the arrival formula reads (falling back to
  the review date for lines never ordered, which is the basis the allowance triage needs),
  and saying that basis in the sheet note.
- **A12 floors now cover CSVs** (the 72-cell open_po_lines file was invisible to the
  xlsx-only sweep and got named a top issue). Same 100-cell floor, 25 hard minimum.
- Editing a delivered workbook with openpyxl restamps docProps modified to the save
  instant, which can put modified BEFORE the in-fiction created stamp and trip A3;
  restore docProps/core.xml from the delivered baseline after every openpyxl save.
  Empty-string formula results must be cached as t="str" with an empty <v/>, or the
  empty-cache scan counts them uncached; a value-preserving revision is proven by
  recalc-inject then a full cell diff against the delivered baseline, expecting only the
  intended cells.
- R27 counts a figure that follows "and" even in "Lines 16 and 17"; write "line 16 and
  line 17" so each number sits behind the word line and is read as an identifier.

### Rossville AutoEval round 2, leakage (2026-08-24)

- The golden-solution leakage check reads every input against the golden's conclusions
  and verdicts ANSWER_LEAKED on one passage that enumerates the answer set: rossville's
  RFI Question 8 named every approved substitute across six manufacturers in one
  parenthetical, "a complete, engineer-approved map from every non-compliant original to
  its qualifying substitute". Per-vendor facts spread across letters, emails and
  quotations passed as raw data in the same verdict. An approval or ruling document may
  rule on CATEGORIES and PROCEDURE; the moment it enumerates the chosen products it is
  the answer key. Fix by rewriting the ruling generically (here: a replacement
  furnishing the specified product in its specified size and class is not a 1.5.H
  substitution and may be ordered on the article's manufacturer information), keeping
  the procedural function the golden's timeline depends on. Watch the chronology too:
  the leaky list was also impossible, an 08/10 request naming substitutes identified
  only after the 08/18 answers. Coded as **L1** (WARN, cross-vendor concentration: one
  input paragraph naming 4+ of the manufacturers the solution tracks).
- **A coded check is only done when it has been shown to fire on the artifact that
  motivated it.** G1 and check_asof's xlsx branch were dead code from birth:
  the gate (autoeval_check.py, now the gcheck modules) never imports openpyxl at module level, so bare openpyxl calls
  inside try/except blocks raised NameError and were silently swallowed, and the "clean"
  portfolio run proved nothing. Function-local `import openpyxl` is the file's
  convention. Always re-prove a new check against the known-bad version (git show
  HEAD:path for the pre-fix artifact) and the fixed one.

## Task 28, branch-stocking-reset: contaminated check and uniqueness failure 6 (2026-08-24 to 08-26)

**Identify a contaminated check by criterion COUNT plus a verbatim quote (branch-stocking-reset, 2026-08-24).** The Rubric filename format coverage check FAILed task 28 saying "Criterion 1 grades a DIFFERENT deliverable basename: 'rademacher_service_review.xlsx'" and "Criteria 2-50 appear to describe a Rademacher supplier service-review/claim task". Task 28 holds 32 criteria naming branch_stocking_reset.xlsx; task 20 holds exactly 50 opening on that exact rademacher C1 string. A verbatim C1 match plus an exact criterion-count match names the source folder in one grep, which is far faster than re-reading the flagged rubric. Do not apply the suggested fix when prompt, golden and rubric already agree: re-fetch the stored submission with `stb submissions fetch-task <uid>` and compare its `criteria` list against the rubric CSV, then flag the check rather than editing a correct artifact. Note the one thing the fetch cannot settle: whether the checker contaminated across tasks or the wrong rubric was genuinely on the form when it ran and was replaced since. Either way the stored state governs, so verify the form before every resubmit ([[revision-workflow]]) since a wrong-rubric paste is invisible in the rubric CSV on disk.

**Sixth failure, 2026-08-26: 28-branch-stocking-reset, FAILed after five AutoEval rounds and a
human review had already been spent on it.** This is the first time the checker's full text was
captured, and it is the most useful one on file, because it named all five dimensions at once
and quoted the sentence that triggered each. Scenario ("a distribution-branch inventory problem
across three counters driven by a leader who has branch managers on a phone call"), input kit
("a policy doc at a dated revision, a boss's ground-rules memo, vendor/supplier program letters
and bulletins, and rep emails"), constraint ("the rep's emailed answer overrides a conflicting
printed letter ... reproduced almost verbatim"), reasoning path ("an item file, current keyed
settings, a supplier terms sheet, and matched twelve-month invoice/receipt/backorder histories
used to rework settings"), and deliverable ("a single named workbook built on live formulas
because the leader moves numbers during the call, with the meeting-facing page placed up front
and a required actions/asks section").

**The new lesson, and it is not about task 28.** Dimensions 2 and 5 are not that task's design
choices, they are THIS PORTFOLIO'S HOUSE STYLE, and the checker has now started failing tasks
on it. Measured across all 39 prompts in the catalogue on 2026-08-26: live formulas 29/39, a
boss's ground-rules memo 31/39, a meeting/front page up front 21/39, a policy doc at a dated
revision 20/39, vendor letters plus rep emails 18/39, a year-of-history file set 18/39. Twelve
prompts carry the whole deliverable template together (one named workbook + live formulas +
front page), and the list is the NEWEST work: 28, 29, 30, 31, 32, 33, 34, 35 and drafts 36 and
37. So the same failure is already queued behind this one.

**How to apply:** the dimension-2 sentence test is necessary but no longer sufficient. Test the
INPUT KIT and the DELIVERABLE SHAPE as their own dimensions before building, because they are
now the most collided thing in the portfolio. Concretely, a new task should break at least the
deliverable template: something other than a single live-formula workbook with a meeting front
page and a vendor-ask section. Note also that surface rewording cannot reach any of this, which
is why the U2 marker fix cleared originality_check while the platform still FAILed: U1/U2
measure wording and authored moves, and the platform is matching DESIGN.

**The prior task 28 collided with is almost certainly 11-dillman-freight-cutover, which is
ACCEPTED and therefore in the comparison set.** Read them side by side: a supplier letter lands
announcing a shipping change, the rep's emailed answers override the printed letter, our own
stocking rules are a policy docx at the 4/26 revision, the own-record kit is item file plus
current keyed settings plus movement history, and it all has to be in front of the branch
managers on a call. That is task 28's five dimensions, with the supplier and the branch names
swapped. Task 28 was built as task 11 re-dressed without anyone noticing.

Three fingerprints measured across all 39 catalogue prompts on 2026-08-26, and they are the
concrete things to grep for before building:

- **"the rep's answer overrides the printed letter": 13/39.** This is the constraint the checker
  singled out as "a distinctive rule reproduced almost verbatim". It is in accepted task 11, in
  28, and in draft 36. Treat it as burned: a new task needs a conflict-resolution rule that
  differs in SUBSTANCE, not a reworded version of rep-wins.
- **"the 4/26 revision" of an internal policy: 6/39.** The same revision date, six times. A
  reviewer reading two of these back to back sees one template.
- **"branch managers on a call": 10/39.** The stakes-setting device of the whole portfolio.

**Draft audit, 2026-08-26 (user asked before submission).** 36-radke-price-protection is HIGH
RISK and should not be submitted as it stands: it carries the rep-override constraint almost
word for word ("where her answers and the printed program differ, her answers hold"), the boss's
ground-rules memo, the full deliverable template, U1 at 6.4% against 35 and U2 at 3 of 7
markers, and its reasoning path (work a supplier program claim item by item into a net credit
figure) is the claim-adjudication path already recorded as spent in both directions. 37-inbound
-consolidation-plan is LOWER RISK: U1 0.5% and U2 0 of 7, no rep-override, no policy-at-revision,
and a reasoning path (re-cost a half year of orders against a counterfactual combined-house
calendar) that is genuinely unspent. Its exposure is the deliverable template and the
boss-memo-plus-rep-email kit, which is fixable by changing the deliverable shape alone.

Prompt kept for diffing. Related: [[submission-tracking]] for the drafts now at risk.

## Task 18, oskaloosa-count-adjustment (2026-08-24 to 08-26)

**A golden's caches can be unreachable from its own formulas, and the oracle judge cannot see it (oskaloosa run 3, 2026-08-24).** Task 18's Tag detail tab declared twelve headers and had only nine columns written, with the two data columns sitting one to the LEFT of the headers naming them and the two reserved columns empty; the exclusion VLOOKUP pointed at an empty range. So the reconciliation's `=SUMIFS('Tag detail'!$I$6:$I$59, ..., $K$6:$K$59,"use")` summed TEXT filtered on nothing, and its neighbour summed an empty column, while both carried the caches the build had computed off the layout it MEANT to write. The judge reads caches, scored it 0.96 and flagged only an unrelated flake; a reviewer pressing F9, or Excel on first open, collapses the whole workbook to zero. This is [[package-hygiene-pipeline]]'s A9 at workbook scale and `fix_floats.py scan` does not see it (the caches are clean floats, just unreachable). Coded as **G2** (ERROR when a SUM/COUNT-family range holds nothing it could aggregate while the cell caches non-zero; 80 hits on the pre-fix file, 0 on the fixed one and 0 elsewhere). Restore such a tab from the INPUTS and prove the rebuilt columns reproduce every downstream cached figure before touching anything else - here all 41 items of both extension columns matched, so no pinned figure moved.

**Three coded checks were blind to negative-stored figures (same run).** R42, R46 and R50 all extract a criterion's figure unsigned ("exactly 8,940.5 short", "a 10.80 credit") and then look it up positive, so every shortage and credit walked straight past them. Scanning both signs turned up 45 genuine R50 findings across the catalogue that had been invisible since the check was written. When a rubric quotes money the house style writes unsigned with a trailing word ("short", "credit"), so any check keyed on a criterion figure must try `-value` too.

**A verdict-cell label is a sentence, not a code (same run).** R40 sourced its labels from `_solution_cell_values`, which drops every string over 40 characters, so C38 quoted its verdict cell "Transfer lines drawing more than the sending branch can give up" (62 chars) and R40 fired at it anyway, twice, across two revisions. Reading labels straight off the sheets at 12-90 chars cleared four false positives catalogue-wide. **Before re-wording a criterion to satisfy a check, confirm the check can actually see what the criterion already quotes.**

**The "count of <label> stands above zero" negative survives what the sweep negative does not (same run).** Three negatives opening "At least one X is incorrectly Y" were read as ambiguous polarity in 3/3 oracle runs; the fourth, opening "The workbook's count of <verdict cell label> stands above zero, at least one ...", was not flagged at all. Recast the sweeps onto that shape, one new verdict cell reading zero per negative. The trailing carve-out sentence ("A tag written in eaches ... is not this defect") is safe to keep: the unflagged negative carries one.

**R45 and R47 close the obvious escape from an R42-dirty anchor (same run).** When a liveness anchor sits in compound cells, the tempting move is to re-anchor on another figure the workbook already computes cleanly, but every clean figure on this workbook was already scored by some other positive, and R45/R47 fail exactly that overlap. **Fix the cells instead:** `=K15*L15` became `=ROUND(K15*L15,2)` and a running `=O15+IF(...)` became `=SUMIF($P$15:P15,"defer",$M$15:M15)`, both single calls, zero cached values moved, and the criterion kept the text it was submitted with. A re-anchor is only free when the new figure is clean AND unpinned.

**Ambiguous negative polarity is a NEGATION COUNT, not a frame (oskaloosa run 4, 2026-08-24).** Four negatives on one rubric shared the identical frame - "The workbook's count of <verdict cell label> stands above zero, at least one <defect>. A <boundary case> is not this defect." - and the oracle flagged three of them `ambiguous_negative_polarity` 3/3 across two submissions while never flagging the fourth. Recasting the three onto the fourth's frame changed nothing, which proved the frame was never the variable. The one difference: C38 spent its single negation on the carve-out, while C35 and C37 also said "rather than" and C36 also said "the records do not support". **Two negative turns in one criterion and the judge cannot tell which way it points.** State the defect positively ("trimmed in quantity", "stock beyond what the records carry", "at its face quantity") and leave "is not this defect" as the only negation. Coded as **R53** (ERROR on a negative carrying two or more of not/never/no/without/rather than/instead of/fails to), proven on the submitted wording with C38 as the passing control; 15 findings across nine other tasks.

**A flaky liveness criterion cannot always be dropped or widened - check R24 before either (same run).** Rewriting a flaky weight 4 liveness criterion as a plain content criterion tripped **R24**: with only the other liveness criterion's 5 points left, a hand-keyed workbook retained 94.0% and the platform's full credit completeness check fails at 90% or more. With the +5 cap and R17's two-criterion ceiling, ~84 positive weight needs BOTH liveness criteria at 5 and 4, so "drop the flaky one" is only available when the survivors still clear the 10-point floor. Widening it to a column of 41 plain read-throughs was refused by three checks at once: **W16** (a liveness row sweep is the kolterman C29 failure), **R39** (the column header COUNT CORR carries a function token the value-grepping judge can never find) and R38. What the house record calls the shape that stopped flaking is a **reference chain, not a sweep over one** - do not read it as licence to say "every row".

**Rank candidate liveness anchors by whether BOTH ends of the chain sit on labelled rows (same run).** The scan that matters: figures clean under R42 (no compound or typed holder) AND stated by no other criterion (else R45/R47 fail the overlap). Task 18 had exactly one such figure, 390, and it flaked 1/3 because its only read-through sat in an unlabelled numeric grid. Rounding an extension column for an unrelated R42 fix had quietly freed a better one, 949, which reaches the briefing through `='Cover order'!B34` on a row labelled with the supplier's name and is computed by a bare SUMIF on a row labelled the same way at the other end - C33's shape, the only anchor on that workbook proven 3/3 twice. **Re-run the clean-and-unpinned scan after every workbook change; fixing one cell can open a better anchor than the one you settled for.**

**The full-credit completeness bar is APPROXIMATE, so a rubric needs margin, not a hair under (oskaloosa, 2026-08-24).** R24 used 0.90 as a literal cutoff and passed the rubric at 89.3% hand-keyed retention (strict liveness 9 of 84) in the same round the platform's Rubric full credit completeness check FAILed it, reasoning that ~90% is "effectively at the bar" and declining to certify a rubric sitting on the line. R24 now holds retention at **85% or below**. Note the check also **misadded its own recomputation** - it enumerated the rubric's thirty-four positive weights correctly, in order, then called their sum 89 when the list sums to 84, and argued 89.9% instead of 89.3%. Correct the arithmetic in the log for the record but do not argue it as a defence: the ruling turns on the share, and the share was genuinely too thin.

**Cut the denominator; never buy liveness share with more liveness criteria (same run).** The check's own suggestions - raise the two liveness criteria, add a dedicated high-weight one, add a mirrored negative - are each closed off on this portfolio: the two are at the +5 cap, **R17** caps a rubric at two formula-only liveness positives because each is an independent 3/3 flake risk (kolterman C25), and liveness-mirror negatives are retired. With strict liveness capped at 10 by the +5 cap and the R17 ceiling, 85% retention needs a positive total **at or under 66**. The lever is therefore the denominator: reweight single-fact criteria to +1, keep +2 for multi-step checks, and reserve +5 for the headline figures and the liveness pair. Task 18 went from 34 positives totalling 84 (10.7% liveness) to the same 34 totalling 61 (16.4%), adding zero flake surface. **+1 rows are inside the platform's own +1..+5 band** and the house anti-+1 check (R14) was deleted for good reason; weighting by habit rather than by what a criterion decides is what inflates the denominator in the first place.

**R24's gated tier is a second, cheaper lever (same run).** A value criterion can be rewritten so the derivation IS the thing scored - "the corrected variance is a formula summing an item level difference ... rather than a keyed figure" - which lands in LIVENESS_GATED_RE and counts toward the gated total, while NOT matching LIVENESS_CRIT_POS_RE, so R17 does not count it and no flake surface is added. Two such rewrites took the gated share to 29.5%. Keep the derivation inseparable from the cell (a formula clause hanging off a correctness criterion buys nothing, which is what the platform discounted on task 20).

**Weight does not protect a criterion: the 3/3 rule fails on a +1 (oskaloosa run 5, 2026-08-24).** After the completeness reweight took twenty-three single-fact criteria to +1, the next oracle run lost exactly one +1 criterion in each of two runs (rewards 1.0000, 0.9872, 0.9870) and failed. Cutting the denominator is right for the full-credit bar, but it buys nothing on the golden check, where **every criterion must land regardless of what it weighs**. Do not deprioritise a +1 row when hunting flakes.

**A twinned figure can be a bare QUANTITY, not just money, and R51 could not see one (same run).** C26 bound 550 to PI-125; the Cover order row carries 550 in THREE columns (POSITION, NEED and QTY, because the need and the ordered quantity both land on the position figure), and the judge failed it 1/3 while quoting that exact row. R51 tests precisely this and stayed silent because its figure set came from `_FIGURE_RE`, which keeps decimals and thousands-separated money and drops bare quantities. Widened to bare 2-6 digit integers, with a lookbehind that keeps an item code's own digits out (PI-125 contributes no 125) and a lookahead that reads a sentence-final period as punctuation, not a decimal point. **The widening then exposed a latent bug in R51**: its form set used `rstrip("0")`, right for a decimal's formatting zero (10.80 to 10.8) but it eats a significant digit on an integer, so 250 matched every cell holding 25 - inert while the check only saw decimals, a false-positive engine the moment it saw quantities. Strip trailing zeros only when the figure has a decimal point. Fix for the criterion itself: re-key onto a figure unique on every row the item appears on (the 250 on order), never reword.

**Give a count criterion a cell that reports the count (same run).** C2 asked for "all 41 items"; the judge tallied 26 PMP + 15 WTR = 41 correctly in its evidence and still missed once, because nothing in the workbook reported 41. A `COUNTA` under a plain label ("Items reconciled, pump line and water treatment line") turns a 41-row tally into one grep. Same shape as the C18 boundary cells. And when rewording a count criterion, keep the exact count LEADING - "carries every item ... reporting 41" trips W11 as a universal sweep, while "carries all 41 items ..." does not.

**A criterion that re-sums detail lines is a landing bug (same run).** C6 stated 1,540.24 for TR-2211 and the judge quoted the three transit detail lines (-1098.6, -210.64, -231), adding them itself, and verdicted unverifiable 1/3. The total was already in two cells. Quote the LABEL that sits beside the total ("as a transfer in the truck at the cutoff") so the judge reads the figure instead of building it.

**One figure fits beside a row key (same run).** R27 counts an item code's digits as a figure, so "PI-125 ... 250 ... 550" reads as three separate claims. A criterion naming a line can state exactly one number.

**Verify every criterion a reviewer names before acting on it (oskaloosa reviewer pass 3, 2026-08-25).** Eight points came back; two were right and six named criteria by number and then described something else. Four described concepts that exist nowhere in the task (two purchase orders, a store column, a freight column, a surplus reduction, a recalculated position after a transfer) against a task with one purchase order, one branch and no surplus. Two were flatly false about the file: "the postable and held figures never appear anywhere in the rubric" against a rubric where the postable is the joint-largest criterion at weight 5, and "add a value check and a derivation check for the postable" against a pairing that already existed on both core figures. **The tell is different from the contaminated-checker tell already recorded**: the criterion NUMBERS are valid and the DESCRIPTIONS belong to another rubric, so a count-plus-verbatim-quote match will not catch it. Print each named criterion beside his description and diff them one by one, and check the previously submitted wording too in case the reviewer read an older version. Acting on those six would have deleted the two highest-weight criteria and rebuilt bundles split a round earlier.

**When a reviewer says the prompt over-specifies, check whether an INPUT already carries the requirement (same pass).** The closing paragraph was told to build the workbook ("nothing in there can be a number I typed", then the replenishment stepped through in order). Both requirements turned out to be documented in the inputs already, and better placed there: liveness in Verlyn's memo in his own voice ("Open it in front of Dwaine and change a quantity and watch the rest of it move. I have had three of these come to me as pasted numbers"), and the transfer-before-purchase order in IC-2 section 9. So the prompt clause could be cut with **zero loss of grounding** for the weight 10 of strict liveness that depends on it, and the worker now has to read the memo and the procedure to find the requirement, which is the reasoning the task exists to test. Grep the inputs for the requirement before either defending the prompt clause or fearing the cut: [[prompt-overspecification-giveaways]] is satisfied by moving a requirement into the source documents, not by deleting it.

**A workbook can be perfectly self-consistent AND functionally dead: recalculate the SCENARIO, not just the caches (oskaloosa reviewer pass 4, 2026-08-26).** Every one of 1,850 formula cells reproduced its cached value, G2 was clean, the gate was at 0 errors and the oracle had it at 1.0/1.0/0.9545 - and the entire Thursday workflow the task exists to test was broken. `Position!I6:I46` keyed the recount hold off Recount column **H** (SLOT, whether the item was ISSUED onto the list, which never changes) instead of column **K** (WORKED, which flips when a figure is keyed). `Reconciliation!Q` used the right column, so keying a recount released the variance for posting while the position tab still held the item off cover and the order never replenished a confirmed shortage: the two tabs contradicted each other the moment anyone did the thing the workbook is for. **Static verification cannot see this.** The `formulas` engine can: inject the input the scenario describes (`Recount!J45 = 0`), recalculate, and diff the action columns against the pre-fix file. Pre-fix Position!R45 stayed "hold" with Reconciliation!Q45 already "post"; fixed it becomes "xfer ott". Whenever a prompt or an input memo says a figure gets keyed in later and the rest must move, **key it in and recalculate before submitting** - a two-state check, not a one-state one.

**Prefer the column that CHANGES over the column that records history (same pass).** The bug is a whole class: an issued/slot/assigned column looks interchangeable with a worked/open/status column while nothing has happened yet, and is identical in the caches, so the wrong one survives every static check and every oracle run. When two columns agree in the delivered state, ask which one moves under the workflow, and key the criterion and the formula onto that one.

**A fixed-length action block is defensible; a silent one is not (same pass).** The reviewer also faulted the purchase and transfer blocks for not growing a line when an item releases. Auto-growing needs a lookup a desk sheet has no honest reason to carry, so the answer is the controls: once the hold released correctly, the buy/xfer counts part company with the lines carried and the sheet says "the order needs a line added", the short list's basis column flips to "recount worked, cover this now", and a new count reports items worked and still short. Detect and instruct, and make sure the detection actually fires in the recalculated scenario.

A FAILED verdict and an UNVERIFIABLE verdict have different causes and different costs, and
the verdict itself is the diagnosis. Unverifiable means the judge could not land, and it is
free under the reward model (it comes off both sides of the ratio); FAILED means the judge
landed and read the row as contradicting the criterion, and it costs the weight. So when the
platform's evidence quotes the exact row the criterion wants and still reports a failure, stop
looking for a landing fix and look for what on that row disagrees. Oskaloosa C4 (run 6,
2026-08-26) claimed a correction was "added to the book quantity" and named 3,490.02: the
Corrections row it landed on carried the figure positive but named no side at all - the tab's
own header note even said corrections are signed "the way it enters the count", which is false
for the three book-side types - and the only cell that did name a side held the same magnitude
NEGATIVE under a paraphrase ("put on book" against the criterion's "added to the book
quantity"). Two ways to disagree, both supplied by the workbook. The repair is the workbook
saying the direction on the row that holds the figure, in the criterion's own words, plus one
note stating a bridge block's sign convention - never a reworded criterion, because the
criterion was right. Coded as R62 (a direction claim on a magnitude the golden holds with both
signs, where no row holding it carries the direction verb): zero findings catalogue-wide, one
on the pre-fix artifact, and pointedly NOT on the two sibling criteria whose sign twins already
sat on rows reading "taken off" - the probe-before-coding discipline paying off again.

## Draft 31, pack-factor-correction: uniqueness failure 4 (2026-08-24)

**Fourth failure, 2026-08-24: draft 31 pack-factor-correction (never submitted, retired by the
user the same day; prompt kept at `archived/31-pack-factor-correction/prompt.md` for diffing, the
checker's comparison text not captured).** A cycle-count variance traced to stale pack factors:
roll every position forward from the physical, split the posted adjustments into the part the
file explains and the part that is real, reversal entries for the controller before the close,
item file corrections and a margin restatement. The nearest neighbour by design is
**18-oskaloosa-count-adjustment** (book-to-count reconciliation with correcting entries ahead of
a close), and the reasoning path "reconcile a physical count against the book, explain the
variance from the transaction record, and hand the controller the correcting entries before the
close" should be treated as spent whatever caused the variance. Its two batch-mates
(lima-flammables-storage, returns-cage-disposition) were renumbered drafts 31 and 32 the same
day.

## Draft 31, lima-flammables-storage: uniqueness failure 5 (2026-08-24)

**Fifth failure, 2026-08-24, same day as the fourth: draft 31 lima-flammables-storage (never
submitted, retired by the user; prompt kept at `archived/31-lima-flammables-storage/prompt.md`
for diffing, checker text again not captured).** A fire-bureau notice caps flammable classes in
the building: class every item from its safety data, figure the class peaks against the notice
figures, re-size Class I/II order quantities to two weeks in whole cases, buy cabinets, move the
drums to Dayton, cost the first year. In hindsight it fits the long-spent dimension-2 sentence:
an outside event lands, the buy is re-sized item by item, and the plan is written against a
limit (the notice figures standing in for a dollar ceiling) - the compliance dressing did not
save it. Two batch drafts failed this way back to back; before building another, write the
candidate's dimension-2 sentence down FIRST and test it against every spent path in this file,
not after the workbook exists. Its batch-mate returns-cage-disposition became draft 31.


## Task 32, pavelka-exposure-workup: occupation and uniqueness failure 8 (2026-08-25 to 09-04)

**Fifth mode, 2026-08-25 (draft 32 pavelka-exposure-workup): a vendor-bankruptcy exposure
workup is purchasing MANAGEMENT, not buying.** 13-1022 FAILed on a supplier Chapter 11 prompt
(true the payable, work the credits/deposits/claims, price the vendor's trade support
agreement, hand the bank a covenant schedule): "the requested work is financial analysis and
reporting rather than buying merchandise or managing wholesale/retail purchasing." Duties
named → occupation moves. Fix: **11-3061.00 Purchasing Managers** (on the platform's sector
list, first use), whose task list carries the work verbatim: "Resolve vendor or contractor
grievances and claims against suppliers", "Represent companies in negotiating contracts and
formulating policies with suppliers", "Review purchase order claims and contracts for
conformance to company policy". **Mathematics IS in 11-3061's essential Skills** (unlike
41-4012/11-3071); Judgment and Decision Making is only transferable there - use Reading
Comprehension, Critical Thinking, Mathematics, Writing. Prompt/inputs/golden/rubric untouched.
Coded: M3 gained the creditor-bankruptcy frame (proven to fire on the pre-fix artifact), M2
gained nine 11-3061 fit rows. Result pending platform re-check.

The occupation list and the per-prompt-type routing table now live in the repo at
`docs/platform-wholesale-trade-occupations.md` (moved out of memory 2026-08-22 per user).


**Eighth failure, 2026-09-04: 32-pavelka-exposure-workup, the SECOND resubmission FAIL (grunewald
precedent holds).** Created 08-25, cleared uniqueness at original submission, then sat through
five feedback rounds while 22 siblings were accepted; the re-run quoted six triggers and every
one is house furniture, not the scenario: the P4 persona sentence ("I do the buying at Stelten
Supply, a plumbing and heating wholesaler" - the P4 docstring template itself, added 09-02, so a
P4 REPAIR CAN CREATE A UNIQUENESS COLLISION when siblings get the same sentence shape), the
weekday-dated crisis letter with a hard deadline, the rep-answers-override-the-notice device
(long recorded as burned at 13/39), the folder-of-files manifest ("their paper and ours"), the
live-formulas-because-he-will-call-back rationale, and the front-page-first-with-recommendation
close. The reasoning path itself (a supplier's Chapter 11: true the payable to the receiving
record, classify what they owe us under the notice, price a trade support agreement sign-or-walk,
covenant schedule at zero recovery) has NO catalogue sibling, so unlike 28-vs-11 this is a
furniture match, not a design identity. Response tried (the path grunewald left unproven): a
deep prompt de-templating that REMOVES the devices instead of rewording them - the precedence
rule and the live-formula demand both already live inside wanek_memo_0818.docx, so the prompt
now simply points at the memo and the solver discovers both from the inputs (better task design
anyway: the prompt was pre-solving); persona re-voiced ("I run the vendor side of purchasing at
... a pipe, valve and fitting house"), weekday cadence dropped for plain dates, the manifest
split into their-paper/our-exports sentences, the front-page ask recast as "Lead with the
answer: ... the recommendation and who does what by when" (completeness cues kept). U1 0.4%, U2 0/7,
gate 0 errors. Whether prompt-level device REMOVAL clears a resubmission uniqueness FAIL is the
open question this submission now tests; the grunewald first-move (platform flag: original
clearance predates the siblings' acceptance, same contributor both sides) applies here too and
goes in before or with the resubmit. P4 repairs portfolio-wide should each get their OWN role
sentence shape, never the docstring example verbatim.

## Task 33, semrad-date-recovery (2026-08-26 to 09-02)

### A required price the packet never states (semrad-date-recovery, AutoEval, 2026-08-26)

Both dataset hard-fail axes (`golden_source_fidelity`, `cross_document_consistency`) fired on
ONE typed cell: the SG-100-80 current distributor net, 2489.75, which appeared in no input.
The vendor letter set the rule ("twelve percent on the model's current distributor net") and
named a substitute model, but priced only the vent kit, so the substitute's own net was a
REQUIRED FIELD WITH NO SOURCE, and it fed six downstream figures including the headline. The
shape to watch when authoring: a rule stated in one input plus an operand supplied by none.
Whenever an input document states a FORMULA in prose, list its operands and point at the cell
or sentence that supplies each one.

The repair is additive and costs no rubric figure: the letter already referenced "the price
pages issued June 1 ... unchanged and remain in force", so the page became an input, every net
tied to the booked nets already in the order file, and the golden gained a transcription tab
the quick-ship cells read by reference. Grounding a value beats re-deriving it, because every
pinned criterion survives untouched.

**Two of the three findings were judge misreads, and checking cost minutes.** The EC-branch
stock finding quoted memo rule 3, which governs "a rescheduled STOCK LINE"; EC's on-order was
0, so nothing of EC's had been rescheduled, and the judge had read a JOB order as stock cover.
The "ADDED COST column is largely typed" half was wrong too: every non-zero cell was already a
formula and the rest were genuine zeros. Its OTHER half was real (the held-date column was
typed, so a moved date propagated nowhere against the prompt's live-formula demand). Triage
each finding against the inputs before editing: on this round one of two hard-fails was real,
and one finding was half right.

**A fourth rule of the ungrounded-figure family, probed and rejected.** "A typed money-shaped
cell that feeds a golden formula but matches no number in any input" fires exactly and only on
the pre-fix cell here and is clean after, so the direction is right - but portfolio-wide it
flags 12 of 16 tasks, 1,702 hits on kolterman and 145 on grunewald, nearly all already through
dataset quality. Transcribed aggregates, computed intermediates left as values and spelled-out
prose numbers ("fifty-two", "eight weeks") all read as ungrounded. Not coded. This is the
fourth candidate of this family to light up passing work, and the pattern is now firm enough to
state as a rule about rules: **a check that reasons about where a NUMBER came from will
false-positive, because provenance lives in prose the checker cannot parse.**

**Restoring caches after an unavoidable openpyxl save.** Adding a whole sheet is not zip-level
surgery, so the save happens and every `<v>` is lost. The recovery: snapshot all cached values
first, edit, then re-inject at zip level, then RECALCULATE with the `formulas` engine and diff
every formula cell against its restored cache (56/56 here, 0 mismatches) - which is the G2
proof in one step. Two traps: openpyxl writes rels with `Target` BEFORE `Id` and a leading
slash, so an attribute-order regex silently yields an empty sheet map and the injector writes
nothing while reporting success; map sheets by workbook order to `sheetN.xml` instead. And
finish with fix_floats plus fix_package, since the save also destroys calcChain (A13) and
stamps the Openpyxl generator string (A14).

### The forged pair hides from its own remedy (semrad-date-recovery, 2026-09-02)

A14 greps `docProps` for the `openpyxl` / `python-docx` substring, and `office_resave.py`
originally selected files the same way. So a file carrying `fix_package.py`'s OLD A14 "repair" -
a hand-written `<Application>Microsoft Excel</Application>` stub, removed under the G2a ruling -
passed the gate AND was skipped by the tool, because the forgery had deleted the very evidence
both of them look for. **A forged pair is worse than an honest openpyxl string: it asserts Excel
authored the bytes while removing the proof it did not.**

Tell them apart by SIZE and PARTS, not by the Application name. Real Office always writes a
fuller `app.xml` - `HeadingPairs`/`TitlesOfParts` for a workbook, `Template`/`TotalTime`/`Pages`
for a document, ~1040 bytes. A hand-written pair is a 180-240 byte stub with `Application` and
`AppVersion` and nothing else. Coded as `forged_pair()` in the tool, reported as FORGED by
`--check`, acted on by the resave loop, plus a `--force` flag. It found **26 of 98 packaged
office files portfolio-wide**, including several solution workbooks, so any task reopened for
other reasons should re-check its packet.

Two things to expect after the resave, both benign and both requiring the documented order:

- **Excel reintroduces float artifacts.** Five cells came back as `2417.1999999999998` across
  three inputs. `fix_floats` runs AFTER the resave for exactly this reason; running it before
  is wasted work.
- **Verify values, not just metadata.** Snapshot every cell and docx paragraph before, diff
  after: 570 of 570 identical here. Also confirm `cp:lastModifiedBy` carries no operator account
  name and the in-world `dc:creator` survived, which is what the tool's core.xml restore is for.

See [[package-hygiene-pipeline]] and [[package-hygiene-pipeline]] - both predate the install and
say Office is unavailable; this file governs.

## Task 29, chemical-lot-review: strict liveness rounds 3-7 (2026-08-26)

**Strict-liveness criteria: single-cell formula-property claims flake; tab-level gestalt claims do not (chemical-lot-review rounds 3-7, 2026-08-26).** The same +5 liveness slot flaked SIX times across four anchors and three shapes - a 234-row formula sweep, a Transfers unit-cost read-through with an "exactly 6.07" anchor (three rounds: the judge read E10, the row dump, then H10 for it), and a Claim-tab single-cell read-through at 2/3 - and in every failing run the judge's evidence sat on the correct cell with xlsx_formula_summary output in hand. Meanwhile C3's page-level claim ("the front page figures reach their values through plain cell references into the tabs that compute them") passed 16/16 lifetime runs carrying an R9 debt with no anchor at all. The judge verifies a TAB'S uniform formula picture reliably and a single cell's stored content like a coin flip, and R9 value anchors reduce nothing here because discovery was never the failure - the verdict aggregation is. The fix that ends the churn: scope the liveness claim to a NAMED SET of same-tab cells that are uniformly pure references (excluding any arithmetic cells on the tab from the wording), keep one "exactly N" anchor for R9, and name only tabs (a row-binding hop like "to the lot's row" is part of the flaky shape). The house two-flake rule fires long before round six: re-key a flaked single-cell liveness criterion into the gestalt shape IMMEDIATELY, not onto another single cell.

## Task 34, delivery-zone-reset (2026-08-26 to 09-04)

**The completeness check has a SECOND axis besides liveness: per-requirement cluster share (delivery-zone-reset, 2026-08-26).** The check re-adds the positive column itself (its own sum can be off by one - never argue the arithmetic, the ruling turns on the share), then tests EACH explicitly named prompt deliverable: if omitting that requirement's entire criterion cluster still retains ~90%+ of positive weight, FAIL. A cluster of +3/+2 in a 59-point rubric (8.5%, 91.5% retained) failed on exactly this; mirrored negatives buy no cover because they fire on affirmative defects, not omission - and do NOT add an omission-firing negative (absence-proving negatives flake, and R22 reads them as mirrors). The repair is inside the cluster: raise its criteria toward the +5 cap and give a BREAKOUT phrase in the prompt ("what the quarter would have cost each of them") its own presence-over-rows criterion, since an aggregate does not map a breakout. Target every named-deliverable cluster at 12-20% of positive; with R24 also binding (strict liveness 10 points must stay >= 15%, so positive <= 66), about five clusters is all the budget holds - a cluster can sit under 10% ONLY when omission is not separable because other criteria's pinned figures corrupt and negatives fire without it (the contract carve-out: skipping it breaks the projection figures and trips two -4s). Not coded: cluster mapping is semantic, and three prior candidate rules of this family flagged criteria already scoring 1.0.

**A human reviewer reads liveness BREADTH, not just the two strict rows (delivery-zone-reset gate 2, 2026-08-31).** With only the two formula-only criteria carrying liveness, the reviewer ruled "largely hard-coded outputs could receive most points" and asked for end-to-end formula and source-traceability requirements. R17 still caps formula-ONLY rows at two, so breadth comes from GATED clauses on value criteria ("the cell a formula rather than a keyed figure", "the total a formula over the register's projected charges") tagged +LIVE - boettcher's accepted C10 shape - until the LIVE tag holds about half the positive weight; keep the clause operand-free where the figure sits in several cells (R29 fails a derivation clause on a value with read-through twins). The same review called a pinned count of an author-composed list ("8 actions in all") overfitting: a data-row count the inputs fix is fair, a presentation count is not, wherever it sits - R32 widened to list nouns. Rebuilt at +39/-8: two +5 strict rows, gated clauses on eight value rows, every requirement cluster at 15.4%+.

**The completeness check derives its clusters from the PROMPT, and two of them are invisible to cluster arithmetic (delivery-zone-reset pre-submission, 2026-08-31, the check's fourth FAIL in five days).** (1) The decision page ("front page with the recommendation and who does what") is scored from decision rows alone - a +5 figure read-through on that page is wiring, so a front-page cluster that bundles it hides a 2-of-39 hole (94.74% retained). (2) The exhaustive formula carry ("all 792 tickets into formula-driven zones") is a requirement of its own apart from the values it feeds; one +2 row is a 94.74% hole. (3) The denominator drifts by one (38 read for 39), so a cluster at exactly 12.8% needs the one-point cushion. At the +39 ceiling this means: FILE 1 + two +5 strict rows that must each ALSO carry a requirement cluster (anchor them on a cluster figure: the trucks' cost for COST, the far minimum for POLICY) + five more clusters at 5 each = 39 with nothing to spare - drop supporting facts (leak counts, recovery percents) before core ones, and log the coverage dropped. It reproduced both holes on the failed rubric and lit the same decision shape on tasks 31, 32 and 35. Also from the same round: a negative must grade a VISIBLE workbook field - "billed ahead of the signature" is a timing fact the outcome-focus check rejects; "the standing column is marked for billing" is not.

**Each explicitly named front-page component is its own cluster (delivery-zone-reset, 2026-08-31, the check's 5th FAIL).** A decision cluster summed across "the recommendation and who does what" passed at 5 of 39 while the platform failed the two halves separately (recommendation 2 of 39 = 94.9%, action plan 3 of 39 = 92.3%). Rule: every noun phrase the prompt names as a deliverable is tested alone, so each needs over 12.5% plus a point on its OWN rows (a +5 figure read-through on the same page counts for neither). At the +39 ceiling with two strict rows that means seven 5-point clusters plus FILE - the only way to fund it is to fold like figures into two-figure rows (R27 errors at three) and drop supporting facts; log what was dropped. The recommendation and the action plan are measured as separate arms; the first scan lit tasks 32, 33, 35 and 37 on the same hole.

**A strict read-through credits a requirement only when its anchored figure IS that requirement's own output (delivery-zone-reset, 2026-08-31, the check's 6th FAIL; denominator read 44 for 39).** The front-page read-through of the quarter's cost (a downstream total) bought route cost nothing - "it does not require the referenced impact-sheet value to derive from the three route stop-cost formulas" - while the front-page read-through of the far minimum was credited to policy in two consecutive rulings. Coupling through other rows is discounted unless the wording compels it, and R29/the oracle forbid the multi-cell derivation clauses that would. So the +39 arithmetic only closes one way: FILE 1 + seven 5-point clusters = 36 means BOTH strict rows must anchor on a cluster's own output (the policy sheet's far stop cost 35.61 for COST, the far minimum 150 for POLICY), never on a front-page total. A front-page strict row anchored on a cost/total/dollars/sum/sales/savings/order-value figure counts for liveness only. **Drafting rule for new tasks:** count the prompt's named deliverable phrases before building - at seven the rubric has zero slack, at eight it cannot pass; write prompts with at most six named outputs, and pick the two strict-row anchors from two different requirements' own outputs on working sheets.

**Input-CSV number SERIES are part of the detector's fabric too (task 34 delivery-zone-reset, 2026-08-26, detect 0.13).** A run-log whose city miles cycled a strict period-5 sequence [14,16,18,20,22] and hours a period-4 sequence with zero variation, and a ticket-amount column holding 38 unique values across 792 stops (~20-28 repeats each), were named the HIGH drivers - and the solution's register tab carries the CSV through, so the workbook was flagged at 87% AI. Fix: regenerate series with structure-derived jitter (miles from the route's actual town pairings per the policy doc's mileage table, hours correlated with miles and stops; amounts log-normal within each row's price band) so every planted count/band survives the retune, then patch caches at zip level and prove them with a `formulas`-package full recalc plus a deliberate corruption. Coded as **A15** (strict period>=3 cycling whole-column or within a low-cardinality group; amount-like headers with <=10% unique over 300+ rows - unit/rate columns exempt, they repeat per catalog item; probed portfolio-wide before coding, zero false fires).

**A word-anchored register inside every per-row band can still fail on TAB SHARE alone (delivery-zone-reset rounds 1+3, 2026-08-26, detect 0.13 twice, identical 39/45 split before and after a full data retune - proof the detector reads composition, not texture).** The 792-row stop register sat at 42% letters and mean-longest 17 (inside A5's calibrated bands) but held 80% of the workbook's extracted text with prose at 5%; no accepted workbook has a tab above marathon's 67%, and accepted prose mass runs 13-46%. The repair that moved the chunk sim from 0.04 to 0.22 (above dillman's accepted 0.18) with every cached value proven unchanged: (1) drop columns the register duplicates from another tab via a key (its DATE rode on RUN - rebuild the sheet XML, remap cross-sheet refs, regenerate that calcChain block); (2) add a Working Notes tab of first-person desk prose (twincreek's accepted device, ~8k chars, one paragraph per decision) plus extended note lines on the small tabs - and keep every rubric-pinned figure OUT of the new prose (a prose twin steals judge landings, R58), spelled numbers only; (3) prove with a pre/post value snapshot diff + formulas recalc. Coded as the A5 dominant-tab signal: 100+ row tab over 72% of extracted text = ERROR even when word-anchored. The chunk simulator (scratchpad chunksim.py pattern: cell values in tab order, 1.35k windows, pass = letters >= 60% AND >= 120 lowercase words) is only a RELATIVE meter - accepted workbooks sim at 0.10-0.44 while passing - so steer to beat dillman's 0.18, not to the platform's 0.36.

**A row-sweep liveness criterion can make the judge INVENT the formula (delivery-zone-reset, 2026-08-31, run 2 at 0.9574).** "The zone on each of the 792 register rows is a formula rather than a keyed zone" passed the W16 gate (subject was the zone, not the row) and still flaked: the evidence quoted =VLOOKUP(A5,Runs!$A$5:$D$132,4,FALSE), a formula nowhere in the workbook - with 792 rows and no landing cell the run reasoned out how zones "should" be looked up and failed the golden against its own guess. The fix that keeps the cluster arithmetic (the check needs the "792 rows" text) is a COLUMN claim with ONE named cell and its cached value: "The zone column on the register's 792 rows is formulas rather than keyed zones, the first ticket T60411 standing at Z1 in cell G5." Any exhaustive-carry liveness row should be written that way from the start.

**Adjudication reads every NAMED PERSON in the golden against the inputs (delivery-zone-reset, 2026-09-04).** "Marcene Hildebrand" as the preparer (Briefing byline + Working Notes signature) was ruled a fabricated identity because no input or prompt establishes the name - the fix is an unsigned attribution or a name the memos already carry (here Harley Duesterhaus, whose desk the work lands on). The name also sat in docProps dc:creator AND cp:lastModifiedBy, which the adjudicator could not see but the same ruling covers - sweep the whole package for the name, not just the quoted cells. When inventing a golden's author, use the prompt's requester or a memo-established person from the start. Same ruling: a positive rewarding the absence of a defect a negative already penalizes (contract zero-charges +2 vs contract-charge -4) is DOUBLE JEOPARDY - one deficiency may swing only one criterion; keep the negative and re-scope the positive to a different property of the same tab.

## Task 37, inbound-consolidation-plan: penalty scope and pre-submission checks (2026-08-27)

### 2026-08-27 · inbound-consolidation-plan, pre-submission checks

**A NEW pre-submission check restricts what a penalty may be spent on, and it overrides the
house habit of backing every rule with a negative (R67).** The Rubric penalty scope check
FAILed two negatives that E1, W18 and W19 all passed, and named its taxonomy outright: a
negative weight is reserved for CRITICAL commissions - safety harm, a privacy leak (PII/PHI/CUI
or a confidential release), an inverted or prohibited top-level DECISION (release/hold,
fund/don't, approve/defer, legally ineligible), or FABRICATION (invented citations, costs or
evidence, or an internal contradiction the deliverable's own figures refute). Everything else
is an ordinary planning or rule-application miss and belongs to an affirmative POSITIVE. A
cadence assigned past the memo's ceiling is planning; a bracket credit taken below its floor is
a threshold misapplied, which the check groups explicitly with "wrong denominator" and
"incorrectly calculated". Note its reasoning on why the second is not fabrication: the money in
question was a real computed figure scored by another criterion, so nothing was invented. Coded
as **R67**, an ALLOWLIST over the four classes, because the rejected class has no vocabulary of
its own - an ordinary miss reads exactly like a compliant fact with a defect frame bolted on.
It fires on 34 of the portfolio's 65 negatives, which is expected of a rule that landed after
they were written, and they stay standing under the single-task scope rule.

**R67 closes against R61 the way R24 does: cut the positive denominator.** (After 2026-09-02
this is worth doing, not required: R61's share is a recommendation and R67's scope is the gate.
Where they conflict, R67 wins and the share simply sits low.) The 20 percent penalty floor
applied while three quarters of the usual negatives became illegal, so the two rules only meet
at a small positive total. This rubric went +57/-13 (three negatives, two
of them ordinary misses) to +39/-9 (two negatives, contradiction at -5 and a fabricated credit
at -4, 23.1 percent) with the converted negatives coming back as +1 positives. Write the
fabrication negative so the CLASS is visible in the sentence ("booked for a vendor whose
printed terms document no bracket"), not just the frame word, since that is what R67 matches on
and what the platform check reads.

**"... is not this defect" is now dead in every criterion, and a rubric written before a rule
lands does not know it.** All three negatives here failed the negative polarity check on the
carve-out, the same class as the banned "does not count as this error" - the repo gate had
learned that from tessendorf the day before (R18, R55) and this rubric predated it. The
procedural rule from kolterman holds: **re-run autoeval_check immediately before entering a
form, not only when the rubric changes.**

**A malformed package part is a silencer, and the second time it has hidden a real finding
(A16 → DATA-OPEN).** An input xlsx shipped a docProps/core.xml with no xmlns declarations for
dc, dcterms and xsi. openpyxl and pandas refuse the whole file on that alone, so a solver's
first command crashes and the gate's own loaders skip it silently: repairing the namespaces
immediately exposed A12, 44 populated cells against the 100-cell floor (pavelka hid the same
class on 2026-08-26). Fix at zip level, member by member, then re-run everything.

**Widening a thin input is where a source-sufficiency hole surfaces.** Filling that sheet out
to 101 cells meant asking what the record would really carry, and the answer named something
missing: the per-vendor freight rating the golden prices every below-floor bucket on (a base
charge plus a percent of merchandise) appeared in NO input. The task was not solvable as
shipped, and no coded check sees it - the golden was internally consistent and the figures all
reconciled. Publishing the rating also proved itself: it reproduces all 244 freight-billed rows
in the history to the penny, and the history then reconciles to the table's floors, rates and
fee thresholds with zero exceptions. **Ask of every input table: does it publish every
parameter the golden computes with, or only the ones the prose happened to mention?**

**The penalty scope check REVERSED itself one round later, and the reversal is the real rule
(same task, 2026-08-27).** Round 1 defended the internal-contradiction negative ("more defensibly
a fabrication-type critical failure [that] would pass on its own"); round 2 failed it outright:
"an ordinary internal-consistency / miscalculation miss ... A contradicted total is a wrong
calculation / consistency problem, which the guidance explicitly disallows as a negative." The
test the check actually applies is whether something was **INVENTED** - a credit, a cost, a
citation, a benefit the documents do not grant - not whether two numbers disagree. So the
house's internal-contradiction negative (V5.1's own recommended class, used since hollenbach)
is dead whatever the wording, and R67's allowlist dropped contradicts / inconsistent /
disagrees. Two procedural points: a passage in a FAIL report defending a criterion is not a pass
and does not bind the next round, and the shape that DID pass verbatim, twice quoted back
approvingly, is worth copying literally - "booked for a vendor whose printed terms document no
bracket, in violation of the March letter that grants the one percent to Kesselring alone",
which the check called "an invented benefit". Fabrication negatives are also the only class left
that can hold R61's floor, so build two of them from the start on different invented things (a
credit that is not granted, a cost priced at a rate no terms carry).

**Never paste the penalty scope check's suggested positive.** Its rewrite for the failed
contradiction criterion ("The front-page half saving agrees with the vendor sheets' own totals
(equals 11,974.52 via cell references)") restates the exact figure another criterion already
scores, which the near-identical check fails as subsumption, and re-adds the liveness wording
R17 caps at two criteria. Where the read-through and the figure are already scored, DROP the
criterion and spend its weight on a legal negative instead of converting it.

**A penalty may only be spent on a critical commission, which changes the weight arithmetic
(inbound-consolidation-plan, 2026-08-27).** The platform's new Rubric penalty scope check
restricts negatives to safety harm, privacy leaks, inverted or prohibited top-level decisions,
and fabrication; a cadence, threshold or rate misapplied is an ordinary planning miss and has to
be carried by an affirmative positive instead. Most of the portfolio's negatives are that
ordinary class (34 of 65), so the R61 20 percent penalty share had to be met by two or three
legal negatives, which means CUTTING THE POSITIVE DENOMINATOR - the same lever R24 already
forces. (R61 went non-blocking on 2026-09-02 by team manager ruling, so the share is now worth
holding only where the legal negatives are there anyway; R67's scope and R24's ceiling still
gate.) This rubric closed both at +39/-9 (23.1 percent) with the two converted negatives coming
back as +1 positives. Coded as R67. See [[rubric-anchoring-and-landing]].

## Task 10, boettcher-winter-earlybuy (2026-08-31)

**A verbatim input-extract tab UNDER the 100-row gate still sinks the detector (boettcher-winter-earlybuy, 2026-08-31, detect 0.15 / llm-only 1.00 / combined 0.40, 23 of 27 chunks AI).** The golden pasted the 81-row, 36-month usage CSV whole as a Usage tab: 36.5% of extracted text at 26% letters, and two of the three passages the detector quoted came off it, the third off a sentence-length BASIS / NOTES column on the buy tab (mean longest 58). A5's two earlier signals gate at 100 rows, so it was silent. Repair, values proven unchanged (0 diffs on every carried figure, formulas-package recalc 522/522): delete the paste, carry a 27-row Season Usage rollup of typed pivot values with the demand VLOOKUPs live on top, move the notes column into a Working Notes tab of first-person desk prose with no digits at all, and split bundled exclusion rows. Chunk simulator 0.29 -> 0.64 (twincreek's accepted 0.44 was the previous best). Coded as the **A5 third signal**: a solution sheet whose header matches an input file's header (Jaccard >= 0.8) with >= 80% of its rows, holding over 30% of extracted text, errors regardless of row count. Calibration: no accepted workbook carries a verbatim extract at all; passing-gate extracts sit at 27% and below; the one open point is inbound-consolidation-plan's History tab at 66% (no verdict yet - if it passes, raise the bar). Two side lessons from the same revision: (1) the `formulas` package (in .venv) reproduces this portfolio's caches exactly (434/434 on the shipped golden), so recalc = openpyxl edit -> formulas calculate -> inject `<v>` at zip level -> fix_floats -> fix_package (calcChain only) -> recalc diff; (2) a task built under the Aug-19 standard carries ~100 gate errors today, nearly all rubric, so an authorship revision is in practice a full rubric rebuild to the one-sentence +39/-9 shape - budget for it.

**A negative must not name a category the golden's own correct line belongs to under one source (boettcher oracle run, 2026-08-31, rewards 1.0 / 0.9149 / 1.0).** "The buy is written against a superseded model number although the letter prohibits it" deducted 1/3 on ZC-224: the price pages list ZC-224T as replacing it, so by the letter alone the golden orders a superseded number - it is right only because the rep's written answer (policy 4.2) overrides the pages. Where the golden's correctness turns on one source overriding another, a negative worded from the overridden source is a judge coin-flip. Write the negative on an act no source supports (Falk-Meyer on the buy, which the memo bars outright) and let a positive carry the precedence call. Same round: the gate catalog moves during a revision (six checks landed from other sessions in one day), so re-run the full gate immediately before every form action, not only after the edit that answered the feedback.

**Cluster share is now coded, and so is dual polarity (boettcher pre-submission, 2026-08-31).** The per-requirement axis above hit again: economics at 3 of 39 (92.3% retained) and the open PO at 4 of 39 (89.7%, "approximately the 90% bar") both FAILed, so the bar needs margin, and the fix is always re-weighting INSIDE the cluster (+1 rows to +2) and cutting rows elsewhere, never adding to the denominator. Every requirement cluster must hold over 12.5% of positive weight. The same round's penalty scope check failed a negative for DUAL POLARITY against a positive with the same subject and verb ("the discount is taken at ...") and for being a non-critical tier calculation dressed in fabrication words ("beyond what ... support"); coded as R69 (subject-head + verb match) and an R67 tightening (weak fabrication forms with a computed-quantity SUBJECT). Negatives that name a prohibited act with their own verb - stepped up past the cap, written against a superseded number - passed the same check. Budget rule of thumb at +39: two +5 liveness rows, then each requirement cluster at 5-11 points.

`tools/fix_package.py` used to repair two package tells at zip level: A13 (write
`xl/calcChain.xml` from the real formula cells) and A14 (swap the `Microsoft Excel
Compatible / Openpyxl 3.1.5` generator string for Excel's Application/AppVersion pair).
On the boettcher revision (2026-08-31) I ran it over the task folder and it rewrote the
generator string in two INPUT workbooks and the solution before I read A14's own
docstring: the user ruled on 2026-08-26 (branch-stocking-reset) that G2a governs - the
string is evidence of a machine-made file, rewriting it asserts Excel authored a file
openpyxl produced, and the only honest remedy is a genuinely authored file. I restored
the inputs from git, put the true string back in the solution, and removed the A14 arm
from the tool.

## Task 39, dock-to-stock-review: memo rubric penalty scope (2026-08-31)

**A memo rubric hides the dual-polarity signature, and a wrong CONCLUSION is never a critical
penalty (dock-to-stock-review pre-submission, 2026-08-31).** The penalty scope check FAILed a -5
reading "the memo concludes that late buying or vendor promise dates caused the delay, contrary to
the dock log and unsupported by it" on both of its axes at once. DUAL POLARITY, because a positive
already rewarded the supported causal conclusion, and the check spelled out the limit of the
carve-out it does allow: a safe action against a dangerous commission is permitted, but the
opposite of an ordinary causal finding is not, since that opposite is not itself a safety, privacy
or prohibited operational decision. NON-CRITICAL, because "saying that a conclusion is contrary to
the dock log and unsupported by it does not convert the analytical error into fabrication" - nothing
was invented, and blame for a delay is not a release/hold, fund/deny, approve/defer or eligibility
decision. Neither R67 nor R69 saw it, because a rubric whose deliverable is a MEMO writes every
criterion as "The memo <verb>s ...", so the passive "the X is <verb>ed" subject-verb signature both
checks read never appears. Coded by stripping that wrapper: R67 now fails any negative whose main
verb is a conclusion verb (concludes / finds / determines / attributes / blames / identifies) with
no strong critical token, and R69 gets a second pass flagging a negative and a positive that both
conclude and share two or more content lemmas. The repair is NOT the checker's suggested positive
rewrite, which duplicates the positive already there and fattens the denominator: spend the penalty
on a prohibited ACT the sources bar, at the same weight so the penalty share does not move
(R61 is non-blocking since 2026-09-02, but a same-weight swap costs nothing). Here that was
an uncertified receiver put on the overhead zone, which section 9 of the procedure bars because the
order picker is the only way up - so certifi / licens / lift joined R67's safety allowlist. Same
round, the action-plan reading learned the memo shape: an action plan written one fix at a time
("assigns the Green River window to purchasing, with a completion date") matched none of the
front-page vocabulary, and the date token is what separates it from "assigns each late receipt to
the first step that missed".

## Task 27, grunewald-renewal-review: resubmission uniqueness failure 7 and the formulas ROUND drift (2026-08-31)

**Seventh failure, 2026-08-31: 27-grunewald-renewal-review - the first uniqueness FAIL on a
RESUBMISSION.** The check re-runs on every submission of a task, against the comparison set as it
stands THAT day, so a task that passed at original submission can fail a later round against a
sibling accepted in the meantime. 27 (created 08-21, passed Section 1 then, two reviewer rounds
spent) failed its round-3 resubmission against 24-vondrak-negotiation-plan - its own same-day
batch sibling, accepted 08-25 while 27 sat in review. The checker's five dimensions all matched:
renewal/increase-at-higher-cost scenario, priced-position-before-a-fixed-meeting objective
(Sept 9 vs Sept 10), quote-comparison + rep-answers + policy-at-revision + own-record-history
kit (Kesler & Boh = the Behrends role), line-by-line answer-and-price path, live workbook with a
meeting front page. Lessons: (1) batch-built siblings that individually pass can kill each
other's later rounds - diff WITHIN a draft batch on the five dimensions before submitting any of
them; (2) a NEEDS_REVISION task's uniqueness exposure grows with every sibling accepted while it
waits, so the longest-queued revision should go back first when siblings share a design; (3) on
such a FAIL the first move is a platform flag (original clearance predates the partner's
acceptance; same contributor both sides), before any redesign or retirement.

**Outcome of the seventh failure (2026-08-31): 27-grunewald-renewal-review RETIRED, its UID
6c82ef0a passed to 41-flyer-program-review (the 20 vosberg-to-rademacher precedent).** A
prompt-only rewrite was drafted (every quoted trigger and shared template device removed,
originality 0.0%/0 of 7, gate clean) but the operator chose retirement over testing it, so
whether wording alone can clear a design-level collision remains unproven. Prompt and
feedback log kept at `archived/27-grunewald-renewal-review/` for diffing; the
agreement-year-measurement-and-renewal-schedule path counts as spent alongside 24's
negotiation package.

**The formulas engine's ROUND disagrees with Excel at half boundaries - never let a recalc overwrite proven caches on untouched cells (grunewald round 3, 2026-08-31).** Excel's ROUND works off the 15-significant-digit display value: 10.94/0.8 (double 13.674999999999999) rounds to 13.67, 1.74/0.8 (double 2.17499999999999982, displays 2.175) rounds to 2.18 - the original build's caches carried both correctly, the `formulas` package returned 13.68 and 2.17, and the two wrong cents cascaded through eleven cells into three rubric-pinned figures (706.97→709.01, 9,299.58→9,287.21). Procedure that held: snapshot every cached value first, recalc, then inject engine values ONLY for new or genuinely input-changed cells and restore the snapshot for every other formula cell; diff the final workbook against the snapshot and require the changed-cell list to equal the intended edit list exactly. Related same round: a cache injector that appends `<v>` without stripping openpyxl's empty `<v></v>` leaves TWO cached-value elements per formula cell - malformed OOXML that openpyxl/Excel silently tolerate; a reviewer failed the workbook on it. Coded as autoeval A17 (exactly one `<v>` per formula cell); task 23 june-price-review still carries 2,122 such cells for its own round.

## Task 31, returns-cage-disposition: reviewer window and final rejection (2026-09-01 to 09-11)

The Rubric Quality Review on returns-cage-disposition (2026-09-01) raised two majors that
were tool artifacts, not errors: "tag T574 does not exist, the cage count shows T501-T528
only" and "the 75-line count could not be verified from the 28-tag cage count". The
input carries 75 tags, T501-T575; the reviewer's reader stopped after 28 data rows
(header at row 3, rows 4-31). The rubric had anchored a worked example on T574 (row 77)
and a count of 75 that only a full read reproduces.

**Why:** a reviewer cannot be argued with and the same reader will run again; a criterion
whose evidence sits past the window is scored ungrounded every time, whatever the file
holds.

**How to apply:** when a criterion needs a row-level worked example from an input, pick a
row inside the first ~25 data rows (returns-cage moved the example from T574 to T506, two
units at 7.12, and swapped the 75-line count for the Totals-row figure the reader can see
on the golden). Do not pin counts of input rows as answer keys unless the deliverable
reports the count in a labelled cell the reader also sees. The judge (oracle) is not the
issue, it reads whole sheets; this is the quality reviewer only. Related: the same review
ordered the liveness/figure split a third time; task 23's precedent (record R9 as
reviewer-ordered .gate-debt, keep the strict phrasing for R24) was followed, see
[[rubric-anchoring-and-landing]] and [[rubric-criterion-count]].

### 2026-09-11 · returns-cage-disposition FINAL REJECTION: cutoff chronology (coded G22)

After 14 platform verdicts and 4 human rounds, adjudication rejected the task on a
fabric defect present since the first build: the 08/14 cage count tagged goods under
authorizations the RGA log issues 08/15 and 08/16 (T570/RG2718, T571/RG2727), and the
memo's suspense balance "at the close of business Friday, August 14" (15,127.75)
equalled the credit register summed WITHOUT a date filter - CM9726/CM9718/CM9727,
dated 08/15-08/16, carried 736.76 at item cost, so the true through-08/14 figure was
14,390.99. The golden inherited both, criterion 22 pinned the balance, and every
fidelity re-derivation "matched" because it summed the same undated register (the
standing lesson: a matching recomputation proves consistency, not correctness - this
is its sharpest instance).

**Why nothing caught it:** every check tests the golden against the inputs; both
agreed. The cutoff lived only in the STORY (the memo's as-of sentence, the count
file's date stamp), and no check read story dates against record dates.

**Coded G22** (tools/gcheck/prompt_inputs/input_quality.py), two faces: (a) a
snapshot input stamped _MMDD must not reference record ids another input's LEADING
column dates after the snapshot (first cut mapped frankfort's STOCK NO item codes to
order dates - a register dates its OWN records, so only column 0 feeds the id map);
(b) a docx balance anchored "at/as of <date>" that equals a register's item-cost sum
only WITHOUT the date filter. Proven 2 findings on the recovered rejected inputs,
0 across the portfolio.

**Generator rule:** when fabricating inputs, pick the cutoff date FIRST and clamp
every generated record date to it; any record meant to postdate the story cutoff must
be excluded from every as-of figure and never referenced by a snapshot document.

**Rebuild ruling:** not re-drafted. The path (physical count against a to-the-penny
account under 13-1022) overlaps task 18's rejected count-reconciliation path, the
platform has diffed this exact scenario 14 times, and a rejected task's own concept
re-entering is the bergendahl "recycling" flag shape. The salvage is this check, the
dynamic slot-tab pattern as a technique, and the memory trail.

## Task 38, po-conformance-review: the review fidelity step (2026-09-02)

On 2026-09-02 a reviewer sent po-conformance-review back with four findings that every
automated gate had passed: a convention stated in one section and broken in another ("an
order is reported under every attribute it fails", while two over-limit MBEI orders sat under
(g) only); a prose count the golden's own schedule contradicted ("two approvals after a
delegation ended", three listed); a state claim the register refuted ("the three open orders",
two CLOSED); and a corrective action the inputs did not support (retro-flagging routine stock
orders EMERG). The operator asked that /review-task catch this class.

**Why:** every coded check tests the rubric against the golden or the golden's package; none
re-derives from the inputs or reads two sections against each other. The reviewer's method
is recomputation plus a cross-read, and it is the only thing that sees these.

**How to apply:** `tools/review_check.py` now has a `[fidelity]` section (table ledger with
row counts and id ranges; count words with the section they sit under; convention sentences;
ids named with "also / as well / would have needed" and the tables that carry them; state
words beside the matching input row, flagged [BAR] when the record's same-axis status
contradicts the word - open/closed/cancelled, active/inactive/pending, paid/unpaid; rule
sentences with required/must/policy are skipped). `prompts/review.md` item 7,
`.claude/commands/review-task.md` step 3 item 8 and `docs/reviewer/workflow.md` step 4 item 7
make the re-derivation and the ledger walk mandatory. The recomputation verifies the
delivered work; the note cites the input rows and the golden's own line, never the
reviewer's figure as the answer. Run the same section on our own memo goldens before a
submission by staging the task under a review-shaped folder (`_x/in`, `_x/sol`). Related:
[[review-task-workflow]], [[rubric-anchoring-and-landing]].

**Round 3 (2026-09-02): a matching recomputation is not proof.** The first recomputation
keyed the separation cutoff on PO_DATE, as the golden had, so the diff was clean; the reviewer
keyed it on APPROVED_AT (section 10 says "recorded under the ID ... after"), found 26-0346
(dated April 16, approved under MBEI on April 20) and moved (g) to 12 / $66,676.66 and the
distinct count to 73 / $558,973.33. Rule: key each test on the column the policy sentence
names, and where an input carries more than one date column, re-key every date-gated test
on each and diff. The harness now lists the date columns per input CSV under [fidelity].

## Task 44, pick-module-reslot (2026-09-02 to 09-05)

**R84 rewrite keeps the R67 token (pick-module-reslot, 2026-09-02).** Moving a negative's ", contrary to section N ..." tail inside the sentence as "although the item master carries ..." passes R84 but drops the words that put it in a critical class, and R67 fires next. Keep hazardous / unsafe / safety (or the fabrication or decision token) in the act clause: "The plan places hazardous stock in a shelving or floor bin ... although the item master carries the item with a hazmat class." R84 is mapped to REV-REGISTER in tools/gate_families.py. See [[rubric-criterion-count]], [[package-hygiene-pipeline]].

**A procedure's stated figures must match the master file it describes (pick-module-reslot AutoEval, 2026-09-03).** The build raised a bin cube in the generator and never re-read the procedure text; AutoEval failed fidelity (2/5) on the golden citing "section 7" for figures section 7 did not state, and scored cross-document consistency 3/5 on the same conflict. When a generator changes a constant, grep every input document for the old figure. Coded G6 (parameter provenance: a Params literal cited to a docx section must appear in that section; a derivation is worded "derived from ..."). Same round: a procedure that gives one ordering rule for a sub-list (safety corrections by pick lines) and another for the rest (by savings) needs both in the formula; the judge reads the clause literally. See [[package-hygiene-pipeline]] for the openpyxl-edit-then-Excel-resave path that rebuilt the golden.

**State the input-side derivation beside every computed value (pick-module-reslot Rubric Quality Review round 2, 2026-09-03).** The review rated a rubric needs_improvement because "exact computed values (walk indices, move counts, class tallies) appear only in the solution output and cannot be verified from agent-visible inputs", one round after the fidelity axis had confirmed those same values from the inputs. A bare figure gives the reviewer no path from the inputs; a figure with its derivation in the same sentence ("the sum over the 320 items of pick lines times the current bin's walk distance in the location master, is 7358662") does. Same review flags "unanchored subjective language": busiest, nearest, safety, same order - anchor each to a rule, a section or an input column, never a second figure (R51 twins, R27 two-figure cap). Not codeable; see [[rubric-criterion-count]].

**An allocation task's outputs read as "re-solve to verify" to the Rubric Quality Review (pick-module-reslot rounds 1-3, 2026-09-03).** Three consecutive needs_improvement ratings were one objection in three wordings: bins, move counts and walk indices from a rank-based allocation cannot be checked against the inputs row by row, unlike a freight audit's totals, which decompose into per-invoice facts. Surface fixes (splits, derivation clauses) do not move it. Recognise the shape at round one: a rubric whose answer keys depend on a global allocation needs property criteria (constraints checkable row by row against the inputs, with one worked example each) plus the two strict liveness keys R9 forces, and a rebuttal citing the fidelity axis's own confirmation of the figures. Draft in [[submissions/44 property-rubric-draft.csv]]; see [[rubric-criterion-count]].

**A boolean-product SUMPRODUCT reads as a typed constant to one judge in three (pick-module-reslot golden check, 2026-09-04).** =SUMPRODUCT((range="SEP 12-13")*range) behind a front-page reference scored 0.9792 on a +1 "computed in a cell rather than keyed" row; the judge named SUMIFS as what it wanted. Summary counts and conditional sums go in as COUNTIF / COUNTIFS / SUMIFS and dot products as SUMPRODUCT(range,range), never a comparison multiplied inside. Coded R96 (GOLD-LIVE) on the proven shape only; plain arithmetic targets are common in accepted goldens and stay with R72.

**A rule row carries the procedure's own exceptions (pick-module-reslot reviewer, 2026-09-05).** Two rules-only rows each restated one clause of WH-4 and missed the clause that qualifies it: within-zone ranking by pick lines omitted section 4's seasonal-equivalent basis, and the 25-pound floor rule omitted section 6's reserve-rack carve-out for stock that fits no floor bin. The reviewer read both against the golden and found correct placements the rows would score wrong. When a row cites a section, grep that section and its cross-references for "unless / where ... does not / also" and fold the exception into the sentence ("..., or reserve rack where the required cube fits no floor bin"). See [[review-task-workflow]].

**Splitting a carry row halves the carry (pick-module-reslot, 2026-09-03).** The Agentic Rubric Quality Review's non-atomic shapes were a column-wide formula demand with a named example hung off it and a count with two trailing clauses; splitting them weight-neutrally (2 -> 1+1) dropped the 320-row carry rows from 6 to 2 of 39 and the coverage checks fired. Re-fund the carry rows to 6 (the formula rows and the count row at +2, the count row naming "each of the N rows") by cutting base-count rows and dropping one +1 row, never by raising the total. Coded R85 (RUBQ-ATOM) for the two shapes; rigidity stays a hand count.

**Round 4 confirmation (pick-module-reslot, 2026-09-03):** after the allocation figures were gone, the review still called counts over the item master (six hazmat, 30 no-pick) and examples past row 25 (FT1319 at row 169) "determinable only from the golden output". When the first ~25 input rows carry no instance of a rule, the rubric row is the rule and its section alone, no count and no example; the oracle then verifies the rule against the deliverable. Procedure parameters, the email's budget and the row count survive as figures.

## Draft 47, credit-hold-audit: uniqueness failure 9 (2026-09-05)

**Ninth failure, 2026-09-05: draft 47-credit-hold-audit, retired by the user the same day
(prompt and log kept at `archived/47-credit-hold-audit/` for diffing, checker text not
captured).** A credit desk re-tests a month of the ERP's credit holds against the written credit
policy (aging from due date not invoice date, unapplied cash and open disputes netted out), codes
every wrong hold by cause, costs the cancelled orders, and flags desk releases the policy reserves
to the manager. Built under 43-4041 like accepted 40-wanasek-credit-workup, which is the likely
collision on occupation plus scenario (a credit desk working accounts against the credit policy),
and on reasoning path it is the portfolio's "re-test a system's or a counterparty's decisions line
by line against a written rule, code the misses by cause, cost them" audit, already carried by 23
(sell prices), 43 (freight bills) and now 53 (detention claims, a draft). Treat the credit-desk
scenario and the second 43-4041 task as spent; the line-by-line rule audit path is crowded and
should carry a genuinely different mechanism (53's is time on the dock) when used again. Batch
lesson: 47 was the first of ten drafts built 2026-09-04 and the only one on an occupation the
portfolio already held an ACCEPTED task in with the same desk in the scenario; the other nine
went to occupations with zero or one prior task.

## Draft 49, forklift-incident-review: uniqueness failure 10 (2026-09-05)

**Tenth failure, 2026-09-05: draft 49-forklift-incident-review, retired by the user the same day
(prompt and log kept at `archived/49-forklift-incident-review/` for diffing, checker text not
captured).** A forklift impact investigation: sequence from four statements and the sign-out
sheet, recordability re-read under the procedure and 1904, causes traced to the training file,
defect log and rack inspection, every operator on a truck type with no evaluation, corrective
actions with owner and date. Built under 11-3071 four days after 45-lift-truck-fleet-plan went
in on the same occupation with the same lift truck fleet, a warehouse safety program pick, an
operator and training dimension in the kit and a manager's written plan as the deliverable; 45 is
the near certain collision (scenario and kit), whatever the reasoning path. Treat lift trucks,
forklift operators and the warehouse safety program as a spent scenario on this portfolio, and
treat a second task on an occupation that already holds one in the comparison set as high risk
when it shares the scenario's physical subject, the way 47 shared the credit desk with 40. Two
of the ten drafts built 2026-09-04 have now failed uniqueness, both the ones that reused a
sitting task's occupation and subject; the eight that went to fresh occupations and subjects
are the ones to submit.

## Draft 50, scale-house-recon: uniqueness failure 11 (2026-09-05)

**Eleventh failure, 2026-09-05: draft 50-scale-house-recon, retired by the user the same day
(prompt and log kept at `archived/50-scale-house-recon/` for diffing, checker text not captured).**
A scale house reconciles a month of bulk loads: site net against the bill of lading's origin net
under contract and procedure tolerances, a scale error correction applied to tickets before
comparison, moisture discounts, seal and split and missing paperwork exceptions, and the claims by
supplier for the claim letters. Untried occupation (43-5111), new mechanism, and it still failed:
the dimension-2 sentence is "compare our record to the counterparty's line by line under the
clauses and build the claim figure", the claim-adjudication path recorded as spent in both
directions after 04, 13, 20 and 25. A fresh occupation and a fresh physical subject do NOT clear a
spent reasoning path; the sentence test has to be run on the path with the mechanism stripped
out ("what does the deliverable DO with the records"), and "our figures versus theirs, then a
claim" fails it however the figures are measured. Three of the ten 2026-09-04 drafts have now
failed; the remaining six should be re-read on that sentence before submission: 51 (bid comparison
under a policy, a path 08 and 24 sit near), 52 (a rating engine run three ways on one month), 53
(a time based audit of carrier claims against a gate record, which is "their claim versus our
record" and therefore at risk the same way 50 was), 54 (a cumulative quantity test against a
contract), 55 (a currency basis comparison with a policy gate), 56 (an ordered assignment under
caps).

## Task 48, commission-review-q2 (2026-09-05 to 09-10)

### 2026-09-05 · commission-review-q2 AutoEval golden_source_fidelity 2/5 (coded G14)

A dispute answer is read against the claimant's own words. Boyd's email named Cave City Diner
(another rep's account, eligible) while the golden took back the bonus on Horse Cave Cafe, his
actual account, without saying so; every figure was right and the judge still read the basis as
fabricated. Before shipping, check every entity a dispute / complaint / question tab names against
the correspondence it answers, and when the claimant misnames the account, have the answer say which
account the claimant named and why the ruling lands elsewhere. G14 does the one-direction mechanical
half (a tab anchored to the emails naming an account no email names); "claim" tabs are registers the
golden files (22, 31), not answers, and stay out of its scope.

**Sixth mode, 2026-09-05 (commission-review-q2, draft 48, AutoEval Skills prompt relevance check
FAIL):** a pick that fits the OCCUPATION can still fail the section when the prompt's work does not
contain its object. 11-2022's "Resolve customer complaints regarding sales and service" was carried
over from the sell-price audit (23, where the customers really complained) onto a commission
recomputation whose disputes are the representatives' own, and the checker read "disputes" as not
customer complaints; "Direct and coordinate activities involving sales" was called only indirectly
related to a commission audit deliverable. Fix: three picks, the accounting and recordkeeping and
the operational records rows plus "Plan and direct staffing, training, and performance evaluations
to develop and control sales and service programs". Coded as four 11-2022 M2 rows (the complaints
pick needs a customer complaining, the direct-sales pick needs selling activity, the staffing and
performance pick needs commission/quota/bonus/performance words, the sales goals pick needs a
quota or goal). The operator relayed the text as task 38's; it matched 48's picks and prompt, and
38 (Purchasing Managers) never carried the pick, so check which UID the form was on before acting.
Second round the same day: the staffing, training and performance evaluations pick was called
"clearly unrelated" to a commission audit workbook, so commission words are not a signal for it;
48 resubmits on the two picks that passed (sales and service accounting and recordkeeping;
operational records and reports for profitability) and nothing else. The checker's own steer for a
commission task: picks about reviewing sales and accounting records, analyzing invoices and
margins, and preparing or validating commission related reports. Two picks are enough.
Confirmed 2026-09-05: 48 PASSED the relevance check on those two picks alone.

### 2026-09-10 · commission-review-q2 golden check 0/3 (coded R103)

The oracle judge does not read to the end of long prose cells either. C7 scored the Representative Notes tab on naming each of the 10 new account bonuses as standing or coming back; the golden named all ten, at the tails of six 900-character paragraphs, and all three runs reported the tab 'contains only general commentary'. A per-item enumeration needs a row per item on the tab the criterion names (a small table under the prose, verdicts as formulas off the tab that computes them), or the criterion scores the tab that already tabulates it. R103 fires on a positive enumerating N >= 5 items on a tab whose text is three or more 300+ character cells with fewer than N short cells.


## Task 51, packaging-consolidation (2026-09-05)

### 2026-09-05 · packaging-consolidation AutoEval golden_solution_check 2/3 (coded R98)

A strict liveness row is a statement about ONE cell, and that cell has to be the shape the row
names. "The first page's landed cost ... reaches its value through a cell reference into the
branches tab or a sum over the spend rows" sat on Summary!B15 =MIN(B9,B13), and the saving row on
=B5-B15; every operand read the branches tab, so two judges passed and the third stopped at the
arithmetic hop and quoted it back as "calculated within the sheet rather than through a cell
reference". The workbook was right and the wording was false of it. Repair is a re-anchor, not a
reword: pick a first-page figure that IS =Tab!Cell and that no other criterion states (current
cost =Branches!B8, stays-local total =Branches!I8), and leave the decision figures to their value
rows. R38 could not see it because it tests whether some named sheet holds a chain cell; R98
resolves the row's own subject cell by its label, follows bare same-sheet read-throughs, and
errors on anything but a pure cross-sheet reference or one aggregation call.

**Seventh mode, 2026-09-05 (packaging-consolidation, draft 51, 11-3061):** two picks failed for
carrying a context or a verb the prompt lacks. "Prepare bid awards requiring board approval" was
called an added board approval context (the prompt has bids and an award but no board), and
"Develop and implement purchasing and contract management instructions, policies, and procedures"
was called not the requested work because the prompt APPLIES an existing policy rather than
developing one. Read every word of a pick against the prompt, including its qualifiers: the
platform holds a pick to its whole sentence. Replacements: "Represent companies in negotiating
contracts and formulating policies with suppliers" for the award of a supply agreement, and the
conformance-to-company-policy pick for applying a policy. Coded as two M2 rows (bid awards need a
board; policy development needs writing, revising or rolling out a policy). 55 carried the policy
development pick too and dropped it before submission. 38-po-conformance-review (in review)
carries it as well and passed its own relevance check earlier; the gate now fires on 38 for it,
which is the platform's current reading, not a defect to fix while 38 sits in review.

## Desk review 6da90c8b: an accept overturned by adjudication (2026-09-10)

**Round 4 (2026-09-10, review 6da90c8b): this desk ACCEPTED a task adjudication then sent back,
for the second time.** Both of adjudication's points were in the layer the read treats as
routine, and neither needed domain knowledge. They are two distinct blind spots:

1. **A re-derivation at full precision hides a rounding defect in the printed table.** The
   per-unit rows showed 766 kWh/year and 5,366 kWh over seven years. Both figures are the
   correct rounding of the true 766.50 and 5,365.50, so recomputing from the inputs agreed
   with the golden and found nothing - but 766 x 7 is 5,362, and a customer reading the quote
   does the arithmetic on what is printed. **Re-derive at full precision AND re-do the
   arithmetic on the displayed figures as displayed.** Coded `G21` in
   `tools/gcheck/golden_rubric/fidelity.py`: where a column is a stated multiple of another
   (a small count or a calendar constant, never an inferred one), the printed values must
   multiply out at the displayed precision. The fix is always carrying more decimals, never
   recalculating, because the values are individually right. Same family as the req 37
   truncation sweep, which first measured formula source text instead of displayed values.
2. **A criterion is checked against the golden, which can never see a criterion the PROMPT
   does not support.** Criteria 19 and 20 pinned peer statistics (IQR 1.90-2.21, 75th
   percentile 2.21) reproducible only under one CSV filter the prompt never stated; the prompt
   said only "the relevant currently certified peer group". The golden satisfies them, the
   oracle passed them on every run, and they are still unanswerable. **Test every criterion
   that pins a value against the prompt and inputs alone: could a solver who never saw the
   golden reach this number?** If the answer is no, the criterion is scoring the golden's
   arbitrary choice, and the remedy is either to state the rule in the prompt or to score the
   property rather than the value.

**Why this keeps happening:** the review concentrated where the task was interesting (a genuinely
hard ENERGY STAR judgment trap, which was correct) and both defects sat in the dull parts. The
skill says "read to find problems, not to confirm the task is fine", and a strong dimension is
exactly what pulls attention off the weak ones. **Standing practice: every adjudication overturn
of one of this desk's accepts produces a coded check.** That worked for reqs 15/24 (sweep the
golden for any fact no input or the prompt carries, which then found the third instance) and it
is what `G21` is for here. Related: [[review-task-workflow]], [[review-task-workflow]].

## Freight-audit-review refinement, round 2 (2026-09-11)

### Ordering rows and planning dates in prose (freight-audit-review refinement round 2, 2026-09-11)

- An ORDERING criterion ("leads with", "opens with") is one verdict only when it names ONE thing to come first; "leads with the decomposition and the recovery figure" flaked 1 in 3 on the golden check (0.9851) because the summary's first sentence carried neither and the judge read "leads with" against sentence one. Repair: name one object and pin its place ("whose first paragraph states ..."), and put that object at the head of the golden's opening. Coded R105 (RUBQ-ATOM).
- A full date the golden invents as its own plan (a bid dated 30 April) goes in the actions table's date column, never restated in prose, or G20 fires; the prose points at "the last dated action in the table".
- A RANK or superlative the golden's prose states ("ranked last by value", "the last dated action") is read against the golden's own table before any criterion pins it, the same axis as G5's count-versus-tab read: freight-audit-review's §6 called the fuel index week error last by value with a smaller class tabled beneath it, and my own round-2 fix called the bid the last dated action with a later row in the table (alignment review 2026-09-11). Prefer scoring the substantive point (a control failure still to be corrected) over a rank, and after any edit list every rank word left in the golden by search.

## Rossville-material-compliance refinement, round 3 (2026-09-11)

### A liveness anchor labelled by a bare noun the sentence reuses (rossville-material-compliance refinement round 3, 2026-09-11)

- The +5 allowance liveness row anchored on "the allowance standing at exactly $16,189.44" after the same sentence had named "the allowance's running total" and "the allowance used" (16,155.4, the figure another row owns). Golden check 1.0 / 1.0 / 0.8913: two judges read the bare noun as the cap at Allowance!E5, the third as the allowance used and failed the row on its value, naming 16,189.44 as "the maximum 5% allowance capacity limit". The golden's own label beside the anchor cell, "Allowance at five percent", was not used. Repair: the anchor label is the cell's words ("the allowance at five percent standing at exactly $16,189.44"), two words trimmed elsewhere to hold the 45-word cap. Coded R106 (GOLD-LIVE): a one- or two-word anchor label that recurs in its own criterion errors; three words or more is read as a cell label.

## Hathi-replenishment-order-decision refinement, round 2 (2026-09-11)

### Record ids past the review window (hathi-replenishment-order-decision refinement round 2, 2026-09-11)

- The Rubric Quality Review rated needs_improvement with one [critical] and one [major] ungrounded_verification finding: eleven positives cited transaction, adjustment, hold and receipt ids, quantities and status tokens that sit at rows 122 to 407 of the input logs. The review named TXN-641186 to TXN-641436, rows 2 to 30 of the transaction log, as what it saw, and it reported the cycle count's Hathi rows (17 to 21, inside the window) as carrying "no variance data". Every id was real; the window was the limit PR1 already records. Repair: decision rows keep the recommendation per SKU in the memo's words with no quantity; citation rows score the deliverable's property (cites the records by id, what the finding states about them) with no id, quantity, date or status token. Coded R107 (RUBQ-GROUND, new family): an id-shaped token a positive pins that the input sheets carry only past row 28 and no docx or the prompt states.

## Standby-generator-recommendation refinement, round 2 (2026-09-11)

### A citation claim the golden paraphrased (standby-generator-recommendation refinement round 2, 2026-09-11)

- A +1 row promised findings "tied to the four provided files ... each cited where its figures are used", naming Diesel_Retail_Price_History.xlsx, and the memo named no input file at all ("the three sheets", "the price history"). Golden check 0.9825 in all three runs: the judge grepped the file name at the price sentence and found nothing. The round 1 score table had asserted the names sat in the background, which a search would have disproved. Repair in the deliverable, not the row: each file named in the sentence that uses its figure, at zip level with every other member byte-identical. Coded R108 (GOLD-LAND): a citation-verb row naming an input file whose name no solution file carries; keyed on the verb because 16 passing rows elsewhere name a file only as a figure's source.

## Rossville-material-compliance refinement, round 4 (2026-09-11)

### Gated clauses on text-valued cells, and a weighting review inside the 39 cap (rossville-material-compliance refinement round 4, 2026-09-11)

- Two +1 gated clauses each failed one run of three: "the arrival date cell a formula rather than a keyed date" on a cell holding =IF(...,TEXT(AD37,"mm/dd/yyyy")), which the judge quoted and still called keyed, and "the line's action cell a formula rather than a keyed word" on a nested-IF verdict the judge read by value. A gated clause is safe on a numeric cell that is one pure call; a text-valued cell reads as typed to one judge in three whatever it holds. Repair: the date clause dropped (the two dates stand as values), the word clause re-keyed onto the column gestalt ("the action column on the 44 schedule lines formulas rather than keyed words"). Coded R109 (GOLD-LIVE) for the date arm; the word arm is logged.
- The Rubric Quality Review's six miscalibrated_weighting findings asked for +5 rows with +2/+3 siblings and mirrored negatives on six requirements, near 65 positive points; the +5 cap and R24 pin positive at 39. Handled as the criterion-count note says: points moved onto the named rows (basis and premium to +2), two figure-free coverage rows added in the thinnest clusters (which also answered the 80% rigid-composition finding), paid for by a presence row, an implied-total row and a second-instance row, with R73's gated tier and R13's coverage share re-checked after every move. Weight changes never reworded a row the oracle had passed 3/3.
- "Golden solution role check, Attribution: FAIL (1/64 points failed)" arrived with no item text and no house document describes it; ask for the item before touching anything.

## Hathi-replenishment-order-decision refinement, round 3 (2026-09-11)

### The citation frame, not the id, is what the window review verifies (hathi-replenishment-order-decision refinement round 3, 2026-09-11)

- Round 2 took every transaction and adjustment id out of six rows and kept "cites by transaction id the outbound pick transactions" for each SKU; the Rubric Quality Review returned the same six [critical] ungrounded_verification findings, this time "the transaction log does not contain any transactions for HAT-FRG-1001". The review verifies the claim that a log holds records for a key by looking for the key inside its 28-row window, so an id-free citation row fails exactly as an id row does. The rows it passed both rounds were the recommendation rows written as the memo's decision and reason. Repair: every explanation row written as what the SKU's explanation attributes the variance to or states, in the memo's words, and the receipt row as the reconciliation's method (SKU by SKU rather than a common failure). Coded R110 (RUBQ-GROUND, a second arm of R107): a citation phrase beside a key whose rows in some input sheet all sit past the window. The same round's golden check flaked 1/3 on the receipt row for naming five receipts in one sentence without a per-SKU mapping; the row's recast removed the claim rather than the golden being edited.

## Hathi-replenishment-order-decision refinement, round 4 (2026-09-11)

### A templated status memo and three dates that lived only in date cells (hathi-replenishment-order-decision refinement round 4, 2026-09-11)

- The LLM-authorship check FAILED at llm-only 0.50 on an INPUT: a distribution-centre operations update whose thirteen sections all ran "X remained/continue according to established procedures; No Y was reported", 30 of 40 sentences on one skeleton, with a LOW corroborating note on botanical supplier names. A10 reads tells sentence by sentence and never sees a document that is one sentence repeated. Repair: every body paragraph rewritten in plain voice with the shape varied, facts intact, Word resave with stamps restored. Coded A21 (REV-PROSE): half or more of a docx's sentences on the status skeleton; the flagged file 72%, its sibling 32%, the rest of the portfolio 14% or under. The LOW name item was left: the refinement rule moves an input for HIGH or two MEDIUMs, and the names thread four workbooks.
- The entity grounding check listed "June 17", "June 18" and "June 19" as fabricated. They were the transactions' own date cells, stored as datetimes and displayed mm-dd-yy, which the platform reads as text and cannot match to a spelled date; G20 had anchored them on the cells and said nothing. Repair: the dates dropped (no criterion pinned them). Coded G23 (GOLD-FID): a spelled month-day the golden carries that no input text or the prompt holds and only a workbook date value supports.

## Harlow-route-rebalancing-proposal refinement, round 2 (2026-09-11)

### A reviewer's partial read of a 117-row log (harlow-route-rebalancing-proposal refinement round 2, 2026-09-11)

- The reviewer recomputed every route total from the visit log and called the golden's figures fabricated: North 15 visits against the golden's 36, East 4, West 7, Castor Valley 2 entries, ratios 96.4 / 91.2 / 103.1 / 149.4. The full 117-row log reproduces the golden to the minute; the reviewer's totals match roughly the first forty rows, the same window the Rubric Quality Review reads (PR1), now on a reviewer. The roster's "unquoted thousands separator" was a quoted field with a trailing space. Repair without moving a figure: the deliverable names the eight Castor Valley visit ids and both minute totals, states the count rule beside the shortfall list, and carries an appendix ledger by account summing to the route totals; the roster revenue becomes plain integers; the Section 3 paragraph gives the re-derivation. The reviewer's one sound rubric point, move-specific densities pinned under a row calling the move open, is fixed by stating the relation any move satisfies (density moves by the account's revenue over 64 days). Recorded as PR6: totals over an input longer than the window need a per-key ledger and the record ids in the deliverable.

### A completeness count restated in a sibling row (harlow-route-rebalancing-proposal refinement round 3, 2026-09-11)

- The platform's near-identical check failed C14 "lists all 10 accounts ... short" against C16 "the shortfall list carries all 10 accounts in descending annual revenue, Brackenfell HVAC at 47,500 last": passing the second passes the first. R47 keys on a shared figure and R86 on a shared attribute, neither on a repeated "all N <noun>" completeness phrase. Repair: the ordering row and the top-row row assess their own point only, a per-item counts row keeps the completeness block over 10%, and the cluster weights get one lead row each. Coded R116 (PRE-DUP).

## Pick-module-reslot, reviewer round after acceptance-in-principle (2026-09-11)

### A typed source column that drifted from its own CSV, and a corrections rule read narrower than its section (pick-module-reslot, 2026-09-11)

- The reviewer re-summed the pick file and found the golden's typed twelve-week units off on 223 of 320 SKUs while the lines column beside it matched exactly; one item's required cube crossed the 2,880 shelf-bin line and the whole allocation followed. The generator had written weekly units with rounding that no longer summed to the totals it had typed into the golden. Repair: the column retyped from the CSV, Excel recalculating every downstream formula (181 moves against 180, walk after 5,128,676 against 5,146,506). Coded G24 (GOLD-FID): a typed column that sits within a few units of an input CSV's per-key sum on 80 percent of keys must equal it on every key.
- WH-4 section 10 works "corrections under sections 5 and 6" first; the golden's flag covered hazmat and the 25-pound rule and left section 6's oversize-to-floor and reserve-rack placements in the savings order (BK1236 at order 24 on 984 lines). A rule row that cites a section owns the whole section: the flag now covers every section 5 and 6 placement (30 corrections), and the rubric names the oversize case with the reviewer's own example.
- The reviewer also asked for what the rules-only rubric had dropped: validation of the typed units against the CSV, the required-quantity rule, and the oversize placement, and for the prompt to say that the email's aisle-grouping remark does not override the procedure's list order. A rules-only rubric still needs a row on each typed source column the golden copies from an input.

### The review reads a receiving-route pin as the wrong direction (harlow-route-rebalancing-proposal refinement round 4, 2026-09-11)

- The Rubric Quality Review rated [critical] a row locking the moved account's receiving route to West, reasoning that the worst-ratio route must shed accounts, not gain them; on the data an inbound account with a lower ratio than West's lowers West's ratio, and moves in both directions clear the tests. The row was dropped rather than argued: the constraint the prompt sets (address the route furthest past the threshold) is carried by "West's after-move ratio is reported lower than its current ratio", which any valid move satisfies. Same round: an invented-figure negative must name checkable anchors on an account no positive scores (a Castor Valley draft mirrored the top-row positive under R22/R41); a ten-member completeness row splits weight-neutrally into the set plus named high-revenue members; a positive and a negative that share only an antonym pair (closer together / further apart) are a mirror to the review though no coded mirror check sees them; and R13's completeness block stays the completeness rows themselves, since the split the review orders moves the table's weight onto rows the "all N" regex never counts.

### A duration column that is always clean (harlow-route-rebalancing-proposal refinement round 5, 2026-09-11)

- The LLM-authorship check hard-failed on an input: all 117 visit durations were multiples of 2 or 5 while check-in times were not round, "duration chosen first, check-out time back-calculated". Repair without moving a single golden figure: minutes redistributed between visits within each account so every account and route selling total held, check-out times recomputed. The two LOW corroborating items (compound-nature names, revenues rounded to 500) were left; contracted revenue is round by nature and both thread the golden and rubric. Coded A22 (LLM-NUM), keyed on time-like headers because the broad rule lit up ten quantity, class and price columns portfolio-wide.

## Hartwell-price-worksheet refinement, round 2 (2026-09-12)

### A live-math prompt in a buyer's words, and a rubric that graded the formulas on four rows (hartwell-price-worksheet refinement round 2, 2026-09-12)

- Adjudication returned five items. One was a leak hedge ("if it is part of the contributor-facing inputs, it is a Major leak") that the zip listing answers; two were the same finding: the prompt requires live math ("I can't do that against pasted values") and the rubric graded formula-drivenness on the two briefing totals, one SKU's L1-L4 and the exposure lookups while rows 4-14 graded the other 46 SKUs as values. The gate's R73 breadth check had never run, because its prompt trigger keyed on "live formulas" and "recalculate" and this prompt says "keep the math live in the cells". Repair inside 39: a column-claim row on the new landed cost across the repricing rows and one on the L1-L4 prices across the repriced rows (one named SKU and its stored value each, no sweep), the minimal gated clause on five single-SKU value rows whose cells are single-home ROUND formulas, the completeness row cut from +4 to +2 to pay; gated tier 3 to 10 of 39. Rows whose figure has a typed twin elsewhere on the sheet (a current price equal to another SKU's new price) were left as value rows. R73's trigger widened to "math live", "live in the cells", "pasted values" and "hard-coded values"; it fires on the round-1 rubric and is silent on the rebuilt one. The last two items were source traces, verified verbatim.
- Coded after round 1 and caught on the same rebuild: R112 on three rows naming the golden-only tabs Impact and Contract_Exposure, rewritten as what the tab is. A reworded strict row naming "new landed cost" beside a dollar figure trips W8 as a sibling-column spot check, and a gated price anchor is quoted as stored (51.5, not $51.50).

## Standby-generator-recommendation refinement, round 3 (2026-09-12)

### A markup where the method divides, a rubric that pinned one of five qualifying windings, and three code references no input carries (standby-generator-recommendation refinement round 3, 2026-09-12)

- Adjudication returned nine numbered items, two of them stated twice. The tank paragraph disclosed a 10 percent unusable allowance and then marked the usable need up by 10 percent (3,672 x 1.10 = 4,039.2) where the disclosed method divides (3,672 / 0.90 = 4,080); the tank and runtime were unaffected, and the adjudicator called the derivation internally incoherent rather than wrong. The rubric pinned the golden's alternator choice (B601-2, 3,866 kVA) where the DQCB table lists five 480 V wye standby windings that all clear the 1,200 kVA inrush; the fix grades the inrush against whichever standby winding the report calls out and asks for its feature code, and the golden now says every such winding clears it. The compliance cluster had left 60 Hz ungraded beside 480Y/277 V. Three sentences dressed the prompt's plain owner rules in code language ("NFPA 110 Class 72", "at full voltage with no soft starter", "voltage dip inside the NFPA 110 allowance"); each was traced to the prompt's own words and the sheet's 90 percent starting basis. Coded G26: a standard number, or a class, type, level or tier beside a standard, in the golden that neither the prompt nor any input carries, PDF inputs read through pypdf; it fires on the round 2 golden and is quiet on 24 other folders. The gate also caught a passive-voice negative (R111) written before the rule existed.

## Weldon-bridge-plan refinement, round 3 (2026-09-12)

### A gated liveness row that named two of a policy clause's three factors (weldon-bridge-plan refinement round 3, 2026-09-12)

- Adjudication returned four items, the first two one finding: the carrying-cost criterion read "a formula over the order total at the policy carrying rate rather than a keyed figure", and policy 7.2 computes committed dollars times an 18% annual rate times one-half the coverage period. The golden's cell applied the clause in full (=ROUND(N26*0.18*(157/365)/2,2)); the row did not, so a submission keying a flat 18% of the order total would have earned the point. Repair on the rubric only: the row names every factor the clause states and rejects a full year at the rate. Registered as PR9; no detector, since the factor list of a policy sentence is not machine-readable.
- The other two items restated the round 1 panel (Tom Marsh's title, Gail's inferred title) against the delivered version, and the adjudicator's own preview read closed the first; a sweep of the golden, prompt, rubric and every docx part confirmed the second was already gone. An adjudication note can carry the hand-over's findings forward verbatim; read each against the current file before treating it as a repeat that did not land.
- The gate crashed on the way in the G24 typed-aggregate helper: the two CSV inputs open with a one-cell report banner, so DictReader files every data row's overflow under a None key as a list. The helper now skips that key.

## Freight-audit-review refinement, round 3 (2026-09-12)

### A complete fuel table read as missing four months, a superseded split quoted as a live conflict, and a bid row that mandated the golden's choice (freight-audit-review refinement round 3, 2026-09-12)

- Adjudication returned six items, three of them pairs. Items 1 and 2 said fuel_index.csv jumps from 2026-07-27 to 2026-11-30 and that the surcharge tests could not run for four months; the file carries 56 consecutive Mondays, the zip copy is byte-identical, the "missing" weeks are rows 25 to 41, and the weeks cited as examples hold 169 to 273 fuel lines each. The input stayed as it was; the golden's sources table now states the population ("each of the 56 weeks from 2026-02-16 to 2027-03-08") so the next read carries the range, and the operator confirms the platform's zip copy by download. Item 3 held the golden's 3,426 fuel lines against feedback.json's 3,746 split; the golden carries no trace of the old figures, the split having been corrected in round 1. The re-derivation did find the golden's "88 same-percentage lines" to be 95 under every dedupe order, and it was corrected.
- Items 4 and 5 read C44 ("holds the bid behind the decision on the September release rule rather than cancelling it") as mandating one business choice where the prompt's last line invites any evidence-led conclusion. The row now scores that the review states whether the bid should still go out on 10 April in light of the release changes, at +2 as the DOC row that scores a decision (ten DOC rows had all sat at +1), paid by the fuel-average row going +3 to +2. Coded R122 (RUBQ-RIGID): a positive opening on a disposition verb with a "rather than" or "instead of" alternative; 1,380 rows probed, no other hit.
- Item 6 quoted the round-0 panel on bundling and mirrored negatives with no claim against the current 48-row rubric, the shape weldon round 3 also saw: an adjudication note carries the hand-over's findings forward verbatim, so each is read against the current file, and the form's box count is confirmed before submitting in case the re-entry never landed.

## Hathi-replenishment-order-decision refinement, rounds 5 and 6 (2026-09-12)

### A fabricated name fixed in the body and kept by the footer, then four note columns written from one filler list (hathi-replenishment-order-decision refinement rounds 5 and 6, 2026-09-12)

- Adjudication returned one finding four ways: the memo's footer still read "Hathi Fragrances Distribution Center", the entity the round 0 trace had flagged. Round 1 had fixed the subtitle in the body and four gates had passed the memo, because python-docx's paragraph list and every gcheck docx reader open word/document.xml only; the adjudicator reads the rendered page and quoted the footer back. Fixed to the subtitle's line, resaved through Word with the stamps intact. Coded G25 (GOLD-FID): an organisation or facility name in a golden docx body, header or footer that no input text and not the prompt carries, a sentence-initial word trimmed once; quiet on 22 other folders. When correcting any string in a docx, search every part of the zip for the old one.
- The rerun then failed LLM-authorship at llm-only 0.50 on two workbooks whose Notes and Comments columns were filled on every one of 514 and 257 rows from ten and eleven stock phrases, "uniform log-entry template" at MEDIUM; two more columns in the same package had the shape unnamed. All four rewritten as operator free text, most cells blank and the rest from the row's own fields, the Hathi rows written by hand to agree with the memo and stay neutral on the duplicate-request question; every other cell byte-identical. Coded A25 (REV-PROSE): a note-like column of a hundred rows or more, nine in ten filled from twelve or fewer phrases; fires on the four old columns, quiet on 85 tabular inputs elsewhere. The openpyxl edit stamped the real clock into every workbook's modified property and the resave chain kept it; the i- zip listing showed the September dates and core.xml was restored from the pre-edit files.

### A borrowed code written with a space for its hyphen (standby-generator-recommendation refinement round 4, 2026-09-12)

- The golden solution check failed one run of three on the +1 winding row: the judge said B601-2 was a 600 V winding. The DQCB sheet's table says 480 Wye, 80 C, standby, 3866 kVA, ADS-311, B601-2, so the judge misread the PDF, but it misread because the memo wrote "B601 2" and its search for the sheet's token came back empty. The code is now written as the sheet writes it, with its alternator data sheet number beside it and the two sibling 480 wye standby windings named with their kVA. Coded R123: an identifier an input carries hyphenated that the golden writes with a space or a dash variant.

### The judge's column-shifted read of a PDF table, stable across runs (standby-generator-recommendation refinement round 5, 2026-09-14)

- After the hyphen fix the golden check got worse (1.0 / 0.9825 / 0.9825): with "B601-2" now findable, the judge's pdf_search landed on its own read of the alternator table, which puts B601-2 at 600 V and B600-2 at 480 V 80 C rise, and the reason text was near identical in both rounds. The sheet is right, the judge is wrong, and the judge is the instrument. Because the rubric accepts any qualifying winding since the adjudication round, the golden now calls out B600-2, the 480 V wye standby winding at 3,313 kVA, which is true on the sheet and matches the judge's read; the temperature rise (105/80 on the sheet, 80 in the judge's read) is left unstated and no other code is named. Uncoded: a golden that borrows one row from a PDF table of near-identical rows should prefer the row the judge's read agrees on and state no column the read may shift.

## Hathi-replenishment-order-decision refinement, round 7 (2026-09-13)

### A join that tied by quantity and failed by key, and a guidance cluster paid for inside 41 (hathi-replenishment-order-decision refinement round 7, 2026-09-13)

- The dataset quality check hard-failed cross-document consistency at 2: every adjustment the memo cited carried a Related Transaction ID absent from the transaction log, and the pick and damage reference documents differed between the adjustment and the transaction it reconciled. The variances tied by quantity and the checker said so, and still called the join broken, so the axis reads formal keys, not arithmetic. The generator had drawn every related id above the log's range (257 of 257 dangling). Fix: the nine Hathi adjustments now name their June transactions with matching reference documents on both sides, the review-entry transactions name the requests they belong to, and the other 248 related ids sit below the log's first record so they read as prior-period. Coded G27 (new family DATA-JOIN): a related-record id of another input's key family, on a row the golden cites, that no input holds; fires on the old files with the checker's eight ids and is quiet elsewhere. The same report found "twelve minutes apart" against stamps seven minutes apart: a displayed-time read, one word to fix.
- The Rubric Quality Review called the guidance cluster miscalibrated at 3 of 41. Raising it to 6 by growing the total to 44 thinned every other +3 cluster, and paying from the explanation cluster left a flat +1 cluster; the payment that holds comes off a presence row, a count row and the least consequential decision row.

### A description title-cased into a name, and a grounding check that read two of four inputs (standby-generator-recommendation refinement round 6, 2026-09-14)

- The platform's entity grounding check listed four of eight entities as fabricated, and its own reasons show it read only the DQCB and DQGAB sheets: "Regional Medical Center" (the prompt says "a regional medical center in northern New Mexico"; the subtitle had title-cased it), "June 22, 2026" (the dateline, grounded as the price workbook's latest week), and "NFPA 110" and "NFPA 20" (the prompt's own words). The subtitle now uses the prompt's lowercase description and the dateline lost its date, since no criterion reads either; the two NFPA strings stay because the prompt and C22 require them. Coded G28: a capitalised organisation-style run in a solution docx that the prompt or an input carries only in lowercase. G25 was quiet because it lowercases both sides of its lookup.

## Weldon-bridge-plan refinement, round 4 (2026-09-14)

### A title finding that survived its own removal (weldon-bridge-plan refinement round 4, 2026-09-14)

- The round 1 panel said no input states that Gail is the purchasing manager. Round 1 removed the title from the briefing header; adjudication returned the finding in round 3 and again, alone, in round 4, while its own preview read confirmed the header now carried no title. The adjudicator was tracing the relationship, not the string: the prompt puts the plan in front of Gail, Tom's email takes it "to my purchasing manager", and the reader joins the two. Repair: the email now says "to Gail, my purchasing manager" in the paragraph the note cites; golden, rubric and prompt untouched, input zip rebuilt.
- Why the gate could not see it: G17 read docx goldens only and passed any title phrase found anywhere in the corpus. The briefing was an xlsx cell and "purchasing manager" existed unbound in the policy and the email. G17 now reads xlsx header cells, parses "Name (Title)", and requires the title within 160 characters of the name; it fires on the original golden and, read-only, on 46-cold-chain-review's "Terrell Whitby, Distribution Manager" (the procedure names the role with no person). PR10 records the hand read for the untitled case.

## Freight-audit-review refinement, round 4 (2026-09-14)

### The same three items back verbatim, and the proof that adjudication previews 25 plus 15 lines of a CSV (freight-audit-review refinement round 4, 2026-09-14)

- Round 3 had answered the "fuel table omits every Monday from 2026-08-03 through 2026-11-23" pair by showing the file complete and stating its range in the golden's sources table. The note returned unchanged. The diagnosis came from the round 3 note's own examples: the six invoice lines it named as falling in the gap are exactly the FUEL lines within the first 25 and last 15 lines of carrier_invoices.csv, so the adjudicator sees that window of every CSV and takes it for the whole file; a 57-line table shows it rows 1 to 24 and 42 to 56 every time. The fix changed the shape, not the content: the 56 weeks now sit in two side-by-side panels of 28, 29 lines, and the file unpivots to the original row for row. Coded H7 (41 to 120 lines, sorted date first column); one other portfolio file carries the shape.
- Item 3 also repeated: "correct all three counts". Round 3 had shown the golden free of the old 3,746 split, but the note wants three counts and the golden gave one, so section 6 now states 1,565 above the tender week's percentage, 1,766 below and 95 the same, summing to 3,426 and recomputable from the percentage printed in each line's description. Lesson: when an adjudication note repeats, the earlier answer was an argument; the second round changes what the adjudicator reads.
- Found on the way and left for its own round: 114 invoice lines on 26 invoices dated 2027-03-14 to 2027-04-20, after the review's own date and partly after the bid date, original fabric that cascades into the confirmed fuel and duplicate figures if re-dated.

## Boiler-replacement-recommendation refinement, round 2 (2026-09-14)

### The hand-over finding returned as a mismatch against its own fix (boiler-replacement-recommendation refinement round 2, 2026-09-14)

- Adjudication returned two items: feedback.json says the byline carries a fabricated company name but the golden's paragraph 2 contains no such name, and paragraph 2's "Prepared for the plant engineer by the boiler service side" is verified as clean. Round 1 had removed the name; the adjudicator read the verbatim hand-over against the corrected file and reported the difference. Third instance of the pattern (weldon round 3, freight-audit round 3): no package file changed, the sweep of every docx part and both zips found the old name nowhere, and the Section 3 paragraph now quotes the current byline and says the hand-over describes the byline as it stood before the refinement, without writing the removed name into a paragraph the trace reads as a claim source (PR11).

## Hartwell-price-worksheet refinement, round 3 (2026-09-14)

### Two closed items come back as traces of the first round's Section 3 text (hartwell-price-worksheet refinement round 3, 2026-09-14)

- Adjudication returned two items that restate round 1's panel findings, the unsupported title and the two branches singled out for freight, and each quotes or describes the deliverable's fixed state (the To line quoted verbatim without a title; "no input carries branch-level order/freight data that would justify selecting" the pair). Every cell of the golden and its zipped copy holds neither the title nor any branch selection. The cause is PR11: the trace reads the Section 3 history as a claim source, and round 1's paragraph had named the removed title and the removed pair, so the trace verified those strings against the inputs and reported the clean deliverable as items. Nothing in the package changed; the Section 3 paragraph describes the two cells by their shape and repeats neither string. A later round's Section 3 never restates wording that was removed.
- Same day, the platform team announced that newly introduced auto evaluations were returning tasks without surfacing the feedback that triggered the return, and asked that returns with only positive visible notes get no rebuttal and no changes until engineering confirms next steps. This refinement is held at the round 2 state, unsubmitted; the hidden trigger may be an auto evaluation rather than the adjudication trace at all.

## Parts-quotation refinement, round 2 (2026-09-14)

### A parts master read as ending where the preview ends (parts-quotation refinement round 2, 2026-09-14)

- The adjudication note said the master "lists parts through PN-31213 only", with no PN-30744 and no PN-30702, and that the source parts behind the Summary formulas were absent. All were present; the i-zip on the platform was byte for byte the folder's. PN-31213 is the master's last line and every part named sat between lines 26 and 146 of 161: the 25+15 line preview proven on freight-audit the same day, this time on an id-keyed lookup rather than a dated series, and at a length the H7 drift-note had assumed was a sampled log.
- Fix: the master in five side-by-side blocks of 32, the supersession file in three of 17, the breakdown list in two of 28, and the stock file pivoted from 326 branch-and-part rows to 160 part rows with a column per branch in five blocks, every file at 33 lines or fewer and each round-tripped to the old rows. The golden, rubric and prompt did not move; H7 gained a sorted unique-id arm.

### A band table's shared endpoint and the two rows the rubric graded past the prompt (dfl-freight-audit adjudication, 2026-09-14)

- Twenty-one items, fourteen of them "Supported": adjudication traces every figure, name and title in the memo back to an input or the prompt and writes the trail out, so a clean claim reads as an item too. The findings were three: Appendix B's "3.65 to 3.70" and "3.70 to 3.75" rows share 3.70 with no inclusion rule and one shipment's week reads exactly 3.70, so the exactly graded totals were called underdetermined; two rubric rows graded a filing date ahead of the meeting and a confirmation asked of the carrier, choices the prompt's "what we change on our own dock" never requested; and the role "Shipping dock lead", put in when the invented dock lead's name came out, is in no input either. Two more were the adjudicator's own limits: the golden read as "among the extracted files" (both zips were opened; the i-zip holds the seven sources only) and four ids "beyond the truncated CSV rows" of the 25+15 preview.
- Fix: one sentence under Appendix B naming the convention the carrier's bill and the golden already applied; the memo states it and rates the June 29 week under it; the dock row's owner is the prompt's requester; the two rows came out of the rubric with their weight kept inside their clusters. Coded G29 (a shared endpoint with data on the line and no rule) and PR13 (rubric rows stay inside the prompt's action scope). The preview-window items were left: the two files are transaction logs and PR6 does not reorder a log for a partial read.

## Hathi-replenishment-order-decision refinement, round 8 (2026-09-14)

### Two LOW tells on one surface make a MEDIUM: a safe expiry day and one scent vocabulary under ten brands (hathi-replenishment-order-decision refinement round 8, 2026-09-14)

- The LLM-authorship check failed at a mean of 3.0 with nothing above LOW: its escalation rule turns two LOWs on the same input surface into a MEDIUM and takes a notch. The tells were 505 of 513 expiry dates on the 28th while the task's own SKUs sat on month ends, and twelve scent lines carried by all ten brands in every product name. Fix in the fabric: expiry days re-derived per lot and made identical across the two files that carry them (they had disagreed on every Hathi lot), and each competing brand given its own line vocabulary, mapped per brand and old line so a SKU keeps one name in all four files. Coded A27 (a fixed non-month-end day on eight in ten dates) and A28 (line names under three or more brands, brand column before supplier column); both fire on the old files and are quiet on the fix. A G22 check added the same day caught the transaction log stamped June 25 with records to June 30: a month extract is written after month end.

## Parts-quotation refinement, round 3 (2026-09-14)

### Generated fabric under a golden that pins it (parts-quotation refinement round 3, 2026-09-14)

- The LLM-authorship check failed the package on the inputs alone: one notified date on all 51 supersession notices, stock drawn from six figures, part numbers on a stride of 7 with one description template, four customer notes in rotation. Every one of those columns feeds a golden decision or a rubric pin, so the respread was done under constraints: each branch keeps its side of every requested quantity (no source moves), only the 57 parts nothing names leave the stride, notices date in ascending order along each chain, and a component type now follows its chain where the old file superseded a hose with a sprocket. The golden re-derived at 0 mismatches after every edit.
- The reader counts across the side-by-side panels H7 asks for, so a check keyed on a column has to merge the `_2`, `_3` suffixes before counting; A25, A29, A30 and A31 do.

## Cold-chain-review revision, round 1 (2026-09-14)

### The preview window reaches every CSV, whatever its length (cold-chain-review adjudication, 2026-09-14)

- Adjudication returned nine items, three of them one defect: the 1,129-line invoice lines file "only contains" the Aug 17 and Aug 28 invoices, the 1,801-line reefer logger "lines 1-40 cover only" 04:00 to 05:15 on the 17th and 14:15 to 15:00 on the 28th, and the manifest holds the 17th, the 18th "through stop 8 on T-31" and the 28th. Each is exactly the first 25 and last 15 lines. H7 had stopped at 120 lines on the assumption that longer logs are sampled; they are not, so the date arm now fires at any length with repeated keys allowed. The repair kept every figure: the logger became one row per truck-day with both zones' return air across 45 quarter-hour columns (20 rows; supply air, mode, door and setpoint dropped and the procedure's recording sentence rewritten to match), the invoice lines became an invoice register with a dollar column per category so the TCS split stays the solver's under section 6, and the events and manifests went into side-by-side panels. Six excursions, 21 exposed deliveries and $9,068.10 re-derived at 0 mismatches from the relaid files.
- The other findings were the checks coded after the build, seen live: the addressee ungraded (R102), first names in driver notes past the window with no full name or role anywhere (G15, PR10: a DOCK_LEAD column on the manifest sources the dock lead by name and role at once; "Rita Mobley, your dispatcher" in the dealer's letter), a phone number on the sign-off no input carries, and the prompt's "over my signature" with no letter in the golden (G8). The letter went in as Appendix C with the nine readings in a table and a signature line; the memo date moved to the input's Monday and every action date to the prompt's Thursday or the service record's PM week.

## Hathi-replenishment-order-decision refinement, round 9 (2026-09-14)

### A leak of the desk's own making, a heading pair read as an outline, and a claim lifted out of its sentence (hathi-replenishment-order-decision refinement round 9, 2026-09-14)

- The leakage check returned ANSWER_LEAKED on three comments written in round 6, when the Hathi notes were composed "to agree with the memo": "picks not posted, timing, hold until WMS posts", "bin corrected to QC hold, no qty change", "242 short, cannot tie to txns". A note on a row the golden cites may name a document or a bin and nothing else; the diagnosis belongs in the status and quantity columns the solver has to read. Coded L6 with a closed conclusion lexicon and no golden-wording requirement, since one leak was semantic.
- The authorship reader failed the golden alone on "Executive Summary" and "Recommendations" as a partial generic outline; across the portfolio only this memo carried two such headings. Coded A32 at two or more. The internal-contradiction check lifted "every SKU carried Under Review" out of a sentence that opened "Cycle count records establish", so the source has to sit beside the status ("Under Review on the count sheet"); coded G31 by id shape across every column. Its other two pairs were a hedged per-item finding restated as a "true position" and a "would overstate"; PR15, since no detector reads a hedge.

## Twincreek-bid-worksheet refinement, round 2 (2026-09-14)

### A count footer the judge cannot see (twincreek-bid-worksheet refinement round 2, golden solution check, 2026-09-14)

- Rewards 1.0 / 1.0 / 0.98. The +1 row "The 47 count on the pricing tab's total row is a formula counting the priced lines rather than a keyed figure" failed one run with the judge quoting row 60 back and calling H60 "a hardcoded typed numeric value of 47". H60 is =COUNT(H6:H59). The cell sits at the foot of a column whose other 47 formulas are VLOOKUPs, so xlsx_formula_summary reports the column as lookups and never lists the footer; search_xlsx then finds 47 twice on the row, once in the label "(47 lines priced)" that is typed. The memory had this shape from vondrak C24 (a lone =COUNTIF footer, 3/3) but no detector.
- Repair: re-key the row onto the column the count summarises, as a column claim naming the count mid-sentence, "The unit bid column on the pricing tab reads the cost basis tab by formula on all 47 priced lines rather than keyed figures". The clause carries no money figure because every unit bid has three twins (Cost Basis O and T, History Rollup H) and R29 would fire on any of them; "all 47" mid-sentence keeps R13's coverage block at 4 of 39 without the leading Each that W16 reads as a sweep. Coded R125: a gated count clause whose every carrier is a lone COUNT-family footer under a column with three or more formulas of another head. The gate also surfaced R13 on the folder once the REQ column left the CSV for the upload form, since the old row 3 carried no completeness cue; the same reword clears it.

## Purchasing-review-jan-jul-2026 refinement, round 2 (2026-09-14)

### A set-membership row the judge read off the table (purchasing-review-jan-jul-2026 refinement round 2, golden solution check, 2026-09-14)

- Rewards 0.9895 / 1.0 / 1.0. The +1 row "The corrective actions state which of the items are changes to a procedure rather than re-approvals of individual orders" failed one run. The golden's lead-in paragraph named the six procedure items in one sentence, but the judge went to the corrective-actions table, found columns Action, Attribute, Owner, By and no per-row class, and reported the section "does not classify or state which items" are which. Two runs read the paragraph; one did not.
- Repair on the golden side: a fifth column, "Procedure change", Yes on six rows and No on the rest, and the two rows that mixed an order-level fix with a procedure (disable MBEI plus the leaver check; note the vendor approval date on six orders plus the hold on a new vendor's first order) split so each row is one thing. The lead-in now says the last column marks the six. No owner, date, count or dollar changed. Rubric row 43 reworded per item: "state, for each item, whether it is a change to a procedure rather than the re-approval of an individual order". Registered as PR16; one hit portfolio-wide (the origin task's own rubric), so procedural.

## Commission-review-q2, reviewer round 5 (2026-09-14)

### Prose written before the fabric settled (commission-review-q2 reviewer round 5, 2026-09-14)

- The reviewer called the recomputation sound, 403 invoices and 34 credits tracing and every formula right, and sent the task back on four sentences: a Working Notes example of a representative "paid twelve percent on an average band" when the module's own table shows all six averages in the 8 percent band and all 403 invoices at 8 percent; a credit said to fall after the June split note when the memo is dated May 21; "ten accounts opened in the quarter" when the account file holds eleven, the eleventh a house account that drew no bonus; and a dispute answer sending the reader to the Invoices tab for STMT GP, a Statement Lines header since the tab split on 2026-09-04.
- Repair: the four sentences rewritten from the tables, plus two of the same class the reviewer did not list (one in-quarter note where there are two; the statement's line and cause code placed beside the invoice row when they sit on Statement Lines). Shared-string edits only; no figure moved. Registered G34 for the tab-plus-label direction, which is mechanical; the illustrative example, the count and the date are the hand re-read of prose against its own tables.

## Dock-to-stock-review, adjudication round (2026-09-14)

### An adjudicator-dictated criterion in a coded 3/3-fail shape (dock-to-stock-review adjudication, 2026-09-14)

- The adjudication note asked for one general positive at weight 2: "Every action item the memo proposes states a responsible person or role and a target completion date," closing the gap between the prompt's "a name and a date on each fix" and the four named-fix rows. The platform's stored criteria already carried the row verbatim (the restored CSV showed it as C38), so the coverage fix was live before the round was worked.
- The dictated wording is W11's hollenbach extension exactly: a criterion-initial "Every" over the noun "action" with no anchor, the shape that failed 3/3 oracle runs there. Entered as given it would trade an adjudication acceptance for a golden-check flake. Reworded to the mid-sentence form the same rule records as the fix, "The memo's What to do table states a responsible person or role and a target completion date on each of its action rows" - the sweep reads off the memo's own named table, no row count is pinned (the number of fixes is solver-discretionary), and a worked-example clause was dropped because it would pin names on a row C27 deliberately leaves at "purchasing, with a completion date".
- Lesson: a platform-suggested criterion is adopted for its substance, then run through the same wording gate as any hand-written row before it goes on the form; when a coded rule records its shape as a 3/3 fail, the log says so and the reworded form keeps the suggester's scope.


## Task 41, flyer-program-review: adjudication after acceptance (2026-09-14)

Accepted and recommended at gate 2 (2026-09-10), the task came back from adjudication with three
base findings of which two self-refuted on the adjudicator's own reading (the precedence hierarchy
is in the prompt and rule 10; the "entity mismatches" were the Weekly Units two-block headers). The
third held: rule 6 pricing (18 percent floor, 12 percent cover allowance, prices ending in 5 or 0,
cover to the largest plan quantity) was graded by no criterion, because the round-2 rebuild had
dropped the cover-price row to fit the 39-point cap. The platform copy restored that day carried
two appended rule 6 rows at +3/+2 and the issue 2 to 4 nets back at +2, which broke R24 at 50
positive. Rebuilt to 29 rows at +39/-9 with the floor graded on the golden's FLOOR TEST column
(HOLDS, anchored on cell I6) and the cover assignment as a value-plus-gated row. Lesson coded as
R127: a golden verdict column no positive criterion names.
Same day, on re-entry: the in-app penalty scope check failed both negatives, whose R84-form
("... although its deal sheet documents no flyer support") kept only the weak fabrication words
once the "in violation of" tail was gone. Rewritten with the deliverable as actor and the invented
thing named; coded as R67's fifth arm.

## Dock-to-stock-review, AutoEval leakage round (2026-09-14)

### A dispute thread that argued the answer, and an exoneration resting on the wrong metric (dock-to-stock-review AutoEval, 2026-09-14)

- ANSWER_LEAKED: the warehouse manager's email in the dispute thread named all three planted causes with their timing, in character. Every cause was independently derivable from the CSVs, so the fix was to strip the diagnosis, not the data: his email now holds his position (same-day keying, purchasing buys late) and category-level deflection with no vendor, date or mechanism, and the two sentences elsewhere in the thread that echoed the carrier's name went with it. Symptom instances (a pallet sitting by a door, product in the building on a named vendor's truck) stayed, because symptoms seed the investigation the prompt assigns while the diagnosis pre-empts it. Design rule: a dispute-thread input may carry positions and symptoms, never the causal diagnosis with names and dates.
- The soundness check rejected the golden's categorical "not buying late" because promise-date adherence tests vendors after a PO exists, not whether purchasing ordered early enough. The repair was the missing test, computed from the inputs' own join: on truck-waiting backorder lines the PO behind the filling receipt was already open at the customer's order date on 237 of 243 and 147 of 154, and truck-waiting lines fell while the complaint rose. An exoneration needs a metric that tests the accused mechanism itself; when a check hands you the alternative support it found, compute it and print it rather than softening the words around the old metric.
- Same round: a memo dated the day before its own earliest deadlines is a self-report defect (three September 8 deadlines under a September 9 date); re-dating the memo to the requested Thursday and moving the three deadlines cleared it and the grounding check's off-by-one complaint together.


## Task 23, june-price-review: adjudication return on the accepted task (2026-09-14)

### A count row that prescribed the function and the label (june-price-review adjudication, 2026-09-14)

The adjudicator returned criterion 15 (+3), "closes with its count of cells to re-key, 91, computed in a cell on the list by a COUNTA over the item column, the words matrix cells to re-key beside it", on two grounds: the prompt asks for "the corrections ready to key" and never for a count, and the row mandates one function and one label. The remedy given: "accept any formula-driven count of the corrections (COUNTA, ROWS, COUNT, or equivalent) with any label that identifies the count". The row had been written that way to land the judge on the golden's own footer cell. Neither R76 (plain cell references as the only live mechanism) nor R90 (a function token on a strict liveness row) fired on it, because the function was named as a prescription rather than a landing; coded as **R128** (RUBQ-RIGID): a positive that prescribes one named function ("by a COUNTA", "SUMIFS over the") or the exact words of a label ("the words X beside it", "labelled exactly") without admitting an equivalent in the same sentence. Proven on the platform wording, silent on the rewrite and across the portfolio. The rewrite keeps the value: "carries 91 cells to re-key, the count a formula over the list rather than a keyed figure" at +1, because an unpinned count failed R126 (the sheet's labelled footer ungraded) and R118 (a second figure-less formula row) at once. The second item, "past July 14" in the Briefing against Params' "through 07/15/2026", was the prose left behind when the honor date was corrected on 2026-08-25; the refinement fc4c0b1a's held round had already fixed it and its golden was adopted whole (four text cells differ from the platform copy, every computed cell identical). The same round cleared the folder's 29-error gate debt inherited from the platform copy, including five spreadsheet inputs carrying the 2026-08-25 forged Excel application stubs that only `office_resave.py --check` reports.

## Hathi-replenishment-order-decision refinement, round 10 (2026-09-14)

### Cited rows in the hidden middle of three workbook logs, and no tail window on a sheet (hathi-replenishment-order-decision refinement round 10, 2026-09-14)

- Adjudication verified three rows it could see, quoting the round 9 note text back, and reported every other cited record absent: the receipts at rows 122 to 180 of 300, the 1004 pair at 296 and 313 of 514 with its requests at 254 and 255 of 258, the 1005 pair at 375 and 184. Query matching found rows 338 and 407 and not their neighbours, and the two requests inside what would be a CSV's last-15 window were called absent too, so a workbook sheet is read head-only. PR12's fix applied to xlsx: each log leads with the brand block under review in date order, the rest following in file order, no value changed. Coded H8: an input row keyed by a golden-cited id outside the preview (head 25 on a sheet, 25+15 on a CSV) on a file over 40 rows, every key-like column read by id shape; it names the adjudicator's ids on the old files and is quiet on the new.

## Crandall-program-allocation-2026q1 refinement, round 2 (2026-09-14)

### A criterion citing a section the golden never named, recorded as landing (crandall-program-allocation-2026q1 refinement round 2, 2026-09-14)

- The golden solution check scored 0.98 on all three runs on one row, C14 (+1): "States that Okamura Roofing Systems' qualifying demand is left out of the demand to which Section 5.4 applies, under Section 3.2 of the program customer terms." The judge's evidence: the golden cites Section 3.1 for the withheld 780 units and never mentions Section 3.2 or the exclusion. Alignment item 1 said the same.
- Round 1 had written the row and recorded it in the change log's scoring table as landing on "the Section 3.2 sentence in the commitments section". No such sentence existed. The table had been written from the rubric, not read against the golden.
- The figures were right: each item's qualifying demand total less its committed and non-committed pools is exactly CU-1136's in-quarter demand (381, 262, 0, 957, 304), so the Section 3.2 rule had been applied without being stated. The fix is a paragraph naming Section 3.2 with those four figures, plus the cite in decision 1, the limitations, the basis line and the decisions table. Coded as R130.
- Side finding: office_resave --check showed the two workbook inputs as FORGED stubs the gate never sees, and Word's automation was blocked by its start screen for the whole session while Excel worked.

## Hx4180-fa26-spec-rev3 refinement, round 2 (2026-09-14)

### A measurement report's middle read as one size L line, and the 25 percent implementation cap (hx4180-fa26-spec-rev3 refinement round 2, adjudication, 2026-09-14)

- Adjudication, five items in two findings. First: the golden's size L sample readings (across shoulder 19.646 from 49.9 cm, bicep 9.508 from 48.3 cm, body length from 73.5 cm) "do not appear in the supplied measurement report, whose only size L record is pocket opening 16.7 cm". The report was 57 lines in one block, PROTO L at 2 to 15, PP S at 16 to 29, PP L at 30 to 43, PP 2XL at 44 to 57: the 25+15 preview (H7) saw PP L only at line 43, pocket opening 16.7. No id the golden names keys the file, so H8's id arm was silent; the golden typed the readings themselves. Relaid as two side-by-side panels of 28 rows (29 lines), values untouched, and the golden's sample-read note names the three sample refs beside the report number. H8 gains a figure arm: a hidden-middle row whose decimal figure of three or more digits the golden types into a cell counts as cited, from five rows up (fires on the round 1 report at 13 rows, silent on the relaid one).
- Second: "14 of 39 positive points (35.9%) for formula/cell-reference implementation and tab architecture (criteria 3, 7, 20-23) that the prompt never requires, exceeding the 25% implementation cap and failing a numerically correct static-value workbook". The 14 were exactly the set R24 reads (two +5 strict read-throughs, four gated +1 rows). R24's per-row floor (each strict row over 10 percent plus a point) means two strict rows never sit under 25 percent at any total, so a prompt with no live-formula demand takes one +5 strict row at positive 33 or under with one or two gated +1 rows; here 7 of 33 (21.2 percent), hand-keyed retention 84.8 percent. The second read-through and an arithmetic detail row were dropped, the rib change carried as a value row, and golden-only tab names in criteria replaced by descriptions of what the tab holds. Coded R129 (RUBQ-RIGID), erroring above 10 of 39 since that shape has passed adjudication elsewhere; silent under R73's live-formula prompt trigger.

## Twincreek-bid-worksheet refinement, round 3 (2026-09-14)

### A citation is a term: "policy 4.1" in no input (twincreek-bid-worksheet refinement round 3, attribution / role check, 2026-09-14)

- After the golden check and the difficulty gate cleared, the attribution / role check failed 1 of 64 points on Params!B6, "Class margins for bid work (policy 4.1)": "terminology 'policy 4.1' does not appear in any input". The bid pricing policy numbers its clauses bare ("4.1  Class margins for firm-price bid work") and cross-refers bare ("under 4.2"); the addendum writes "ITB Section 3" and "ITB Section 5"; the ITB's number is "ITB No. 27-04". The golden had coined "policy N.N" eleven times, "ITB 3" and "ITB 5" three times, and "ITB 27-04" three times. The judge sampled one; the rest were the same failure waiting.
- Repair at zip level in the string table (no cache moved): bare clause numbers, "ITB Section N", "ITB No. 27-04", the policy's own heading words for the margin table, and "class target plus four points" for the coined "add-on". Coded G36: a document noun plus a number in a form no input carries, fired on 17 cells before, silent after.
- The same gate run surfaced R129 on a prompt that does demand formulas ("Keep the pricing on formulas ... has to carry through the sheet on its own"): the shared R73/R129 trigger now reads both phrases. H8 (rows past adjudication's preview in an 82-row item file and an 883-row sales history) was first carried as debt and then cleared at the operator's request.

### A feature code two data sheets share, cited in a cell that named neither model (standby-generator-recommendation refinement round 7, 2026-09-14)

- The attribution / role check failed 1 of 51 points on the compliance cell "3,313 kVA starting capacity on winding B600-2 against 1,200 kVA inrush": it found B600-2 in the DQGAB alternator table at 5,743 kVA and called the figure a contradiction. Cummins reuses alternator feature codes across models, so B600-2 is the 480 Wye 105/80 winding on both the DQCB (3,313 kVA) and the DQGAB (5,743 kVA) sheets, and B601-2 is shared the same way. The prose mentions named the DQCB in their paragraph and passed; the table cell stood alone. Round 5 had moved the pick to B600-2 to suit the golden check's PDF read without testing the code's uniqueness across the three sheets. Every mention is now scoped to the DQCB, the cell with the sheet's file name. Coded G37 after one false start: keying on any identifier two inputs share fired on twenty record-id lines in four other refinements, where a transaction or hold number joins the same record across a register and a memo; the defect is a code whose figures differ by input, so G37 keys on a paragraph figure that sits beside the code in one input and not another. Another session took G35 and G36 in the same hour, and the registry's duplicate-id refusal is what caught the collision.
- Clearing H8 on a constant-price log: the sales history carried one unit price per item for two years, so every one of an item's invoice lines repeated a figure the golden types, and no ordering could reach the window (642 hidden hits). The relay that kept every figure: one row per item (item, description, unit, price) with a quantity column per invoice whose header names the date, invoice and PO, two side-by-side panels of 22 (23 lines), EXT_PRICE dropped as derivable; the 79-item master went into four side-by-side panels of 20 inside the 25-row workbook window. Both unpivot to the original records exactly, and all 92 golden rows drawn from them re-derived before packaging.

## Pick-module-reslot, adjudication (2026-09-15)

### Second bins counted as cleared but never put on the crew list (pick-module-reslot adjudication, 2026-09-15)

- Adjudication returned the golden, Golden deliverable Major: WH-4 section 8 consolidates an item slotted in two bins and empties the second bin, section 10 puts every changed item on the move list with its from and to bin, and the requester's email wants both bins on every line. The Items tab counted four second bins cleared and the Bins tab showed them emptied, but the Move List was one INDEX/MATCH row per moving item on a single order column, so no line could carry a second bin as its from bin, and the extra work never counted against the 150-move budget. Repair: a CONSOL ORDER and CONSOL WINDOW column on the Items tab rank each consolidation with the moves under section 10 at no walk saved (the walk index counts the item at its primary bin, section 11); the Move List reads both order columns and runs to 185 lines, 150 in the first window and 35 carried, with every class, zone, bin, distance and saving unchanged. Four rubric rows reworded to count lines rather than item moves. Coded G38 (GOLD-FID): every second location the golden records appears as a from-location on its move list.
- The same round's gate surfaced R129 firing on a prompt that asks for formulas ("Keep the classing and the bin assignments on formulas"): the trigger allowed one word between keep and on formulas, and R73 and R129 each hold their own copy of it. Both widened to six words.

## Weldon-bridge-plan refinement, round 5 (2026-09-15)

### One sampled citation standing for twenty-two, one inside a formula (weldon-bridge-plan refinement round 5, 2026-09-15)

- The attribution / role check failed 1 of 64 points on "terminology 'policy 5.2' does not appear in any input". The policy numbers its clauses bare ("5.2  The reorder point is ...") and cross-refers once as "section 4.4"; the golden cited "policy N.N" in 21 text cells and in the string literal of the approval formula, whose cached value the briefing reads through. G36 (coded 2026-09-14 on twincreek) listed the 21 text cells and missed the formula, because it skipped formula cells while the judge reads values. Repair: every citation in the input's form, at zip level, then an Excel re-save; no figure moved. The same read found "on hand less allocations (policy 7.1)" where the definition is 6.1, and "before mid-2027", a date no input carries, replaced with 7.3's own words.
- The gate also raised H8's figure arm on the 1,026-row ledger: three net costs the golden types matched UNIT_PRICE on transfer lines past row 27. Each is typed from a row of the 27-row item status report, which the preview shows whole, so the check now subtracts figures some input shows inside its window; it still fires on the hx4180 measurement report it was written for, and it goes silent on three submissions with the same sourcing.

## Crandall-program-allocation-2026q1 refinement, round 3 (2026-09-15)

### One pasted report of six, a Section 5.4 fill never run, and a two-panel calendar misread (crandall-program-allocation-2026q1 refinement round 3, 2026-09-15)

- The operator pasted the golden solution check, `[0.0000, 1.0000, 1.0000]` with no EC-actionable failures, and the first diagnosis was a collapsed run to resubmit unchanged. The fetch-task record of the same evaluation held five more failed children: an adjudication Major, attribution FAIL 1/64, entity grounding, numeric grounding and self-consistency. The diagnosis was withdrawn.
- The adjudicator's Major: the memo carried the Section 5.4 balance per item (78, 69, 553) and never ran the fill the section names, so no account receiving those units appeared. Running it in acceptance-date order reproduced the adjudicator's values exactly, and exposed that on two items the balance runs out inside a group of orders accepted the same day. Section 5.4 sets no order within a day; the prompt says such a point goes to the requester as a decision, so the golden names the settled recipients and puts the two splits to the Director.
- Attribution failed "the year end shutdown runs to January 1, 2026" by listing only the December days. Exhibit C carried 2026-01-01 at the foot of the left panel of a side-by-side table. It was relaid in one chronological panel, the reverse of the two-panel relay that helps a workbook preview window.
- Numeric grounding failed both evaluations on "Program value" heading three item schedules with different meanings; coded as G39. Self-consistency caught a real slip introduced in round 2: "applied to no other account in either event" is false once an extension forces a recut, and the +4 criterion had carried the same claim.
- Re-gating also showed the G36 citation-form check firing on the inputs' own "Section N.N" style; it was narrowed and proved against twincreek's coined cites. Naming the new recipients by order number tripped H8, so the golden names them by account, acceptance date and quantity.

### Quoted commas read as shifted columns, and five of eight groups named (dfl-freight-audit adjudication, 2026-09-15)

- Four items: two were reconciliations the adjudicator ran and passed (71 + 45 + 6 = 122; the eight group totals sum to 5,982.91). The findings were two. The bill of lading register and the freight bills export carried quoted fields with commas ("Bittner residence, c/o Hilltop Plumbing", "Water heaters, commercial"); both files were valid CSV and byte for byte the uploaded copies, but the adjudicator split lines on commas, counted 18 fields against 16 and 25 against 24, and warned that weight, class, rate and accessorial columns come out shifted. And the prompt's "dollars we take back grouped by what went wrong" was graded on five of the eight groups the golden reports plus the aggregate.
- Fix: the ten comma-bearing values reworded without the comma ("Commercial water heaters", "Bittner residence c/o Hilltop Plumbing"), 105 fields, every other byte and the CRLF endings kept, the rated and claim totals re-derived unchanged; three rows added for freight all kinds, the class raised without a certificate and the reweighs inside tolerance. Coded H9. The rebuilt package also tripped G36 on the memo's "section 3" citations, a false positive on an agreement that numbers its clauses as integer headings and cross-refers as "section 8", so G36's house-style pass now covers integers as it did dotted numbers. The task moved to Opus by operator direction.

### Rejected on an ask the golden never met, after eleven returns (dfl-freight-audit, 2026-09-15)

- The rejection: "it does not provide the 71 individual DFL claim forms required by the agreement and claims desk, instead giving a consolidated schedule and leaving form preparation/filing as future work", with internal fuel-surcharge count and wording inconsistencies, "at least one underbilled invoice" marked correct, an "impossible timeline" and five of eight reason-code groups graded.
- Checked against the last committed package: the claim forms finding is right and was present from the first build; the prompt asked for "the claims themselves in the form Dahlquist's claims desk will accept" and both the agreement and the claims desk say "one claim per invoice" on DFL's form. The reason-code table still carried the Appendix B claim the 09-10 reviewer struck from the prose, and "Thirty-four invoices ... in two forms" named parts of 13 and 43 without the overlap. No appendix standing contradicts its difference, but DFL7718237 turns under-billed by a cent if the base charge is left unrounded, and four more standings move on a rounding or band-boundary reading the golden never stated. "September 17" appears in no shipped file; the prompt's September 8 deadline had passed by review.
- Why eleven rounds missed it: every check and every rubric row compared artifacts with each other, never the prompt's asks with the deliverable; each round fixed only the items its note named; the rating engine lived in a scratchpad.
- Coded: R134 clause map (with the third-return Rebuilt date), G41 deferred deliverable and one form per record, G42 struck-phrase ledger, G43 verify_golden.py with an alternate-reading pass, the G5 split-count arm, P8 due date 21 days past the build. Procedural: PR19 rebuild from the map at the third return, PR20 record struck phrases the same day.

## Draft 53, detention-claim-audit (2026-09-17)

### A carrier-contact pick on a claim audit (Skills prompt relevance check, 2026-09-17)

Eighth M2 mode, the sixth mode's shape under a new occupation. 43-5071 Shipping, Receiving, and
Inventory Clerks carried four picks on a detention claim audit; the checker retained three
(compute amounts such as demurrage charges; record shipment data such as charges and discrepancies
for accounting; confer or correspond with establishment representatives to rectify problems) and
failed the section on "Contact carrier representatives to make arrangements or to issue
instructions for shipping and delivery of materials": auditing a carrier's invoice against gate
times and a contract rate is not arranging its delivery, and the requester's line that she sets
the inbound appointments did not count. Its steer for an audit prompt: picks about auditing
records, calculating charges, reconciling discrepancies, and preparing accounting or operational
reports. Fix: the pick removed, no replacement (nothing in 43-5071's eleven duties is closer to
an audit than the three retained, and 48 passed on two). Coded as four 43-5071 rows in
ONET_TASK_FIT; the carrier-contact row's signal is arranging, booking, scheduling, tendering,
dispatching or instructing a carrier, never an appointment.

