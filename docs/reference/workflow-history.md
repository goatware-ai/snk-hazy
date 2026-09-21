# Workflow history: the dated build lessons behind the workflow rules

> Dated narratives relocated from `docs/submission/workflows/01-07` on 2026-09-11 so the
> workflow pages carry only the rules. Each section is one task (or one review batch), in
> the order the workflows cited it. The rule each story taught stands in the workflow page
> as a checklist line with its check id; this file is the evidence. Nothing here is a rule
> on its own: when a story and a check disagree, the check (`docs/rules.md`) wins.
> Reviewer notes in full are in `reviewer-feedback-corpus.md`.

## open-order-cleanup (rejected on prompt quality, 2026-09-02)

Taught: P4, the opening frame. Cited from `../submission/workflows/02-prompt-writing.md`.

`open-order-cleanup` was **rejected on prompt quality alone** (2026-09-02) after eight
AutoEval rounds and five reviews, with its inputs, golden solution and rubric all called
strong: "the prompt does not explicitly establish that the work is U.S.-based and does not
clearly frame the analyst's professional role or assumed purchasing expertise level. Add a
brief opening that identifies the requester/analyst as U.S.-based and states the expected
procurement or purchasing experience."

The rejected prompt carried "my desk" and the reviewer still found no role framed; it
named a town (Kewanee) and the reviewer did not take that as a state. The repair that
passed:

> "Four of our trucks come off the Cumberland lease on December 31, and Darrell wants the
> whole fleet settled before then. I run the warehouse and the pipe yard here in Chattanooga,
> Tennessee, so the trucks are mine to settle, and I am handing this to you because you have a
> few years of distribution operations behind you and will not need the lease schedules walked
> through."

## lift-truck-fleet-plan (rejected at first human review, 2026-09-05)

Taught: P6 (the frame woven in, never a self-introduction), A20 (comma rules), G8, G9,
G10 (the reviewer's read of the golden), and the rubric rule "a row for every fact the
reviewer verifies". Cited from `../submission/workflows/02-prompt-writing.md`, `../submission/workflows/04-golden-solution.md`,
`../submission/workflows/05-rubric.md`.

### The prompt: P6

`lift-truck-fleet-plan` was rejected at its first human review on the paragraph that
satisfied P4 the literal way. The paragraph read: "I run the warehouse and the pipe yard for
Ledford Pipe & Supply, a pipe, valve and fitting wholesaler in Chattanooga, Tennessee, and
the lift trucks are mine to keep running and to replace. Whoever picks this up should have a
few years of distribution operations behind them and be able to read a lease schedule and a
service history without help." The reviewer: "Why would you say this to someone who works
with you at the same company? They are your coworker. They know what the company is and what
you do... Remove the entire first paragraph which contains no useful info and sounds LLM
generated. If that info is needed for the LLM then include it, naturally, in the
conversation prompt. For example: Four of our Ledford Pipe & Supply trucks come off the
Cumberland lease on December 31."

Both rejections (this one and open-order-cleanup's) are real, so P4 and P6 hold together.
The frame is carried by sentences that do other work:

- The place rides on something the work touches: "the pipe yard here in Chattanooga,
  Tennessee", "Cumberland's yard on the Tennessee side". Never "a <trade> wholesaler in
  <Town>, <State>" told to a colleague who works there.
- The role is ownership of the problem: "the trucks are mine to settle", "the lease is mine
  to answer". Never a job description.
- The experience is the reason for the handoff, addressed to the reader: "you have a few
  years of distribution operations behind you, so the schedules will not need walking
  through". Never "whoever picks this up should have ...", which gates a stranger instead of
  talking to a coworker.
- Every event the opening names carries its link to the work in the same sentence. The same
  reviewer asked what "Tamika's work schedule has to do with a new equipment proposal": a
  second shift is a fleet matter only once the prompt says it puts trucks on nights and
  needs batteries the yard does not have.

### The sentences: A20

The same rejection rewrote the prompt's opening sentence into three and a golden paragraph
into four, then stated the rule: "When two sentences are joined with 'and' or 'so' or 'but'
or 'or' or another coordinating conjunction, they need a comma ... No more than 2 sentences
can be joined with a comma and coordinating conjunction. Basic comma rules should be used
throughout. Nobody is looking for perfection, but commas in lists and commas in compound
sentences are basics." It applies to the prompt, every input document, every golden text
cell, and the rubric ("Fix the extensive run-on sentences throughout").

- Wrong: "Three of the four trucks go back to Cumberland on December 31 and the reach truck is
  bought." Right: "... on December 31, and the reach truck is bought."
- Wrong: "U-01 is already past ten thousand hours and U-03 crosses it before the inspection, so
  neither can be bought out under the rules, and U-02 fails the maintenance test ..."
  Right: four sentences. A third independent clause always starts a new sentence.
- Wrong: "Four of our trucks come off the lease on December 31, Tamika's second shift starts
  October 12, and Scenic City's proposal is good through October 2." Three clauses, and the
  first join is a comma splice. Right: three sentences, each saying why the event matters.
- Wrong: "a hydraulic pump, two brake jobs and a set of mast chains". Right: "a hydraulic
  pump, two brake jobs, and a set of mast chains" (the serial comma, every list).

A20 codes the two mechanical shapes (a bare conjunction opening a new subject and verb;
three or more clauses in one sentence). The serial comma, the comma splice, and compound
sentences inside a subordinate clause are a read.

### The golden: the reviewer's read

The gate passed the task at 0 errors; the reviewer rejected it the next day with seven
golden findings. Every coded fidelity check read the rubric against the golden or the golden
against itself. The reviewer read the golden against the inputs and the prompt, one claim at
a time.

1. **Every identifier the golden cites exists in the shipped input.** Four invoice numbers
   on the inspection tab existed nowhere: the generator had renumbered the invoices after
   the golden text was written. Coded G10.
2. **A date the golden states as fact is written in an input or derived by a stated rule.**
   "U-05 returned to service June 3" was inferred from an invoice dated June 2 and a meter
   that moved on June 5. The reviewer: "input files don't support this." Coded G18 for
   owner-dated action rows and G20 for every full date in the golden's prose.
3. **The deliverable's own date is not later than an action it schedules as done.** A memo
   dated September 22 scheduled the rental pickup and two tag-outs for September 16 and 17.
   Coded G9.
4. **When the prompt says a document is to be signed, the golden carries that document.**
   "The order and the notice ready for him to sign" needs a purchase order (vendor, ship-to,
   reference, lines, totals) and a notice letter (addressee, schedule, election per unit),
   each with a signature-and-date line, and a first-page block for the signer. Tables about
   them are not them. Coded G8.
5. **Every rule class in a policy input is applied to every record it governs.** The check
   card had two classes: tag-out defects and same-day-fix defects. The golden applied the
   first and invented a "runs under the card" status for the second, which the card never
   allows. A read.
6. **A cost "since <date>" covers the partial period from that date.** Three whole invoices
   billed after June 21 do not answer "what the rental cost us since June 3"; the eighteen
   days of the month already billed count too. A read.
7. **An asset that leaves carries no duty after it leaves.** A truck traded in during a
   December delivery window cannot also work all 55 nights to December 31. A read.

Then the sentences: the reviewer quoted one golden paragraph as "a very long run-on" and
broke it into four numbered sentences (A20 again).

### The rubric: a row for every fact the reviewer verifies

The reviewer found the seven golden defects above (wrong invoice numbers, a memo dated after
its own "today" actions, no signature block, a policy class left unapplied) and closed with
"the rubric ... clearly did not catch the issues noted above"; the task was rejected
outright. The rubric had no row that would have failed the golden on any of them.

## weldon-transition-buy (reviewer feedback, August 2026)

Taught: the overspecification giveaways subtler than step-by-step instructions (P3, P5 and
three reads). Cited from `../submission/workflows/02-prompt-writing.md`.

Patterns the reviewer sent back:

- **Saying what a file is for.** Name it and what it contains; how it enters the analysis is
  the solver's discovery ("the project quote register", not "you'll want that one when you
  decide which of the big hits are real demand"). Coded P5.
- **Outlining sections of a deliverable component.** Naming the component and its audience
  is enough ("a briefing tab Gail can walk the GMs through"); listing its sections dictates
  structure.
- **Warning about data pitfalls.** If spotting bad rows, non-demand spikes, or an atypical
  period is graded, a warning to "watch out for X" hands it over.
- **Stating derived parameters.** A coverage horizon, cutoff, or scope the solver should
  compute from scenario facts must not appear as a given.
- Structurally, **all** input file names belong in the opening paragraph, woven into the
  narrative; a separate "here are the pulls" inventory paragraph gets flagged even when
  every file is named. Coded P3.

## yearend-deadstock-plan (reviewer feedback, August 2026)

Taught: never enumerate the decision framework an input file teaches. Cited from
`../submission/workflows/02-prompt-writing.md`.

Listing the disposition options (return / transfer / clearance / scrap) in the prompt handed
over the policy file's decision order; asking for line items with "the right detail" that
names a cap or charge tips off that it binds.

## commission-review-q2 (NEEDS_REVISION rounds 2-4, 2026-09-09 to 09-10)

Taught: G20 on the deliverable's own dateline, and the per-person prose re-read (G19).
Cited from `../submission/workflows/04-golden-solution.md`.

The deliverable's own dateline is a stated date too: the first page said "Tuesday,
September 1, 2026" with the requesting note dated August 28, and the reviewer asked to
"remove or correct the unsupported dates". Date it to the note it answers or leave the date
off.

The task went back twice on per-person notes written against an earlier data generation:
paragraphs addressing one representative did not restate that person's row (direction and
amount of the correction, each bonus standing or coming back, splits, house lines,
accelerator). G19 codes the "X's quarter moves up/down" form; the rest is a hand read.
Grade it with positives, never a penalty (R67 puts contradictions outside the penalty
classes).

## Reviews of other contributors' tasks (2026-09-04 to 09-05)

Taught: "row count buys effort, not difficulty", "give them a candidate set to eliminate",
and "prefer real published data". Cited from `../submission/workflows/01-ideation.md`.

Observed across fifteen reviews, scoring the two frontier models the platform runs:

| Task | Scale | Model rewards |
|---|---|---|
| Steel escalator from published PPI series | 9 series | 0.55 / 0.66 |
| Census e-commerce line read | 20 rows | 0.56 / 0.49 |
| VA Ohio coverage plan | 373 items over 2,793 actions | 0.42 / 0.31 |
| Q4 liquidation and procurement plan | 300 rows | **1.00 / 1.00** |
| Import landed-cost closeout | 7 shipments | 0.92 to 1.00 |

The task with the most rows was solved perfectly by both models, because its policy files
handed over every formula algebraically. The task with the fewest beat both. Before scaling
a concept up, ask what decision the extra rows force that the first twenty did not. If the
answer is none, keep it small and spend the effort on the decision instead.

**The candidate set.** The strongest task reviewed puts nine candidate price indexes in
front of the buyer and asks which to write into a contract. Six are wrong, and wrong for six
different reasons: two stopped publishing, one is the seasonally adjusted twin whose history
gets restated, three measure the industry's own output price rather than its input cost, one
is aluminium, one is scrap. Nothing in the prompt hints at any of it. The difficulty is in
the set, not in the volume of any member, and each wrong candidate needs one disqualifying
property discoverable only by reading the files.

**Real published data.** Correlation rather than proof: the three tasks the models scored
lowest on all used real published data (BLS producer price indexes, Census annual wholesale
figures, USAspending contract actions). The two they solved used synthesized data. Real data
was never designed to be clean, so its ambiguity, discontinued series, revision flags and
withheld cells come free and survive scrutiny. A fabricated pack has to invent that
friction, and reviewers can tell when it has not: one task went back because all 350 of its
cost figures were whole dollars.

## O*NET occupation and task-pick checks (twincreek, frankfort, kolterman, drafts 23 to 40, task 45; August to September 2026)

Taught: M1, M2, M3 and the per-prompt-type routing table. Cited from
`../submission/workflows/02-prompt-writing.md#house-notes-on-platform-submission-formmd`. Relocated from the
`platform-submission-form.md` and `platform-wholesale-trade-occupations.md` captures on
2026-09-11.

- **Buy-side versus sell-side (M1).** twincreek-bid-response FAILed the Occupation prompt
  relevance check under 13-1022 because the prompt priced a bid to a customer; it passed
  under 41-4012.00. "Prepare drawings, estimates, and bids that meet specific customer
  needs." fits a bid response but FAILed the Skills prompt relevance check on an agreement
  renewal prompt (draft 27, 2026-08-22) as bid and drawing work.
- **Framing, not fit (M3).** frankfort-storm-claim FAILed under 13-1022 with the occupation
  correct and the deliverable merchandise work end to end, because the prompt was written as
  an insurance job: "the prompt primarily requires preparing a property-loss claim workbook
  ... those duties are only a limited part of the requested work." Reframed to lead with the
  merchandise question, it failed a second time with a DUTIES reading ("reconstructing
  inventory, classifying storm-damaged goods, calculating insured losses and salvage credits
  ... not a strong, direct match for Wholesale and Retail Buyers"). It PASSED under
  11-3071.00 Transportation, Storage, and Distribution Managers with the prompt, workbook
  and rubric untouched.
- **Sector match.** 13-2011 Accountants and Auditors and 43-3031 Bookkeeping, Accounting,
  and Auditing Clerks both FAILed the ONET Occupation-Sector Match on draft 23 (2026-08-22)
  as "Professional, Scientific, and Technical Services" only, even though the relevance
  reading had accepted the audit framing. 11-2022 Sales Managers then passed on the same
  sell-price audit prompt after 13-1022 ("not on purchasing merchandise or performing
  wholesale/retail buyer duties") and 41-4012 ("primarily analytical and file-maintenance
  work rather than the direct wholesale selling activities") had failed relevance; a
  recorded 11-2022 rejection on that prompt turned out to be a form entry error.
- **Task picks (M2).** kolterman-valve-advisory failed the Skills prompt relevance check with
  the occupation and the skills both accepted: on a recall reconciliation and claims prompt
  it rejected #2 (nothing is negotiated), #11 (no budget discussion) and #7 (the analysis is
  of specific transactions, not trends). The same four-pick block had been pasted into tasks
  06, 11, 12 and 13 before the check caught it; all four now differ.
- **11-3071 on a backcharge dispute** failed (draft 25): delivery records as evidence do not
  make it distribution work; 11-2022 was the fallback. 13-1022 failed task 18's count
  reconciliation prompt naming "verifying inventory counts, maintaining inventory records,
  or determining stock levels/reorder points" as duties it does not carry, and failed draft
  32 pavelka as "financial analysis and reporting rather than buying merchandise or managing
  wholesale/retail purchasing" (11-3061 Purchasing Managers pending). 43-4041 Credit
  Authorizers, Checkers, and Clerks passed draft 40 wanasek-credit-workup on occupation and
  tasks/skills.
- **53-1047.00** is listed on the O*NET industry page but DISABLED there (2026-09-04), and
  the platform's task and skill dropdowns for it are empty; task 45 lift-truck-fleet-plan
  was built on it and moved to 11-3071.00 at the form.

## Rule-catalog cleanup (2026-09-15)

An audit of the gate against 68 folders (16 submitted tasks, 22 accepted, 30 refinements) found
three rules that contradicted each other, stale entries, and heavy duplicate reporting. Changed:

- **Conflicts.** E1's message suggested "This criterion is met only when ...", the pin W9 and R18 ban;
  it now points at the in-sentence defect frame. The submission and rubric templates told authors to
  write "a named person as owner and a calendar date" unconditionally against R100; both now score an
  owner or date only when the prompt asks, and R81's statement says the same. H8 and PR12 prescribed
  moving cited rows to the top of a log while the latest adjudication lesson rejected a lead block;
  both now prescribe a relay into side-by-side panels or one row per key.
- **Stale entries.** PR18 registered. P4 and P6 moved from a report heading to a new PRE-FRAME rule
  family, so docs/rules.md lists them. Sixty checks whose first docstring line was an id stub or a
  dated story cut mid-sentence got a rule sentence. G2a (a duplicate of A14), G2c and G2d (unclearable
  on python-docx inputs, permitted under the 2026-09-04 ruling) retired; G2b stays.
- **Duplicate reporting.** Atomicity reports one finding per criterion with the other reasons listed,
  R55 leaves a grader-instruction carve-out sentence to R18, and R20, R43 and R50 wait until a criterion
  is atomic. Across the 16 submitted tasks error lines fell from 800 to 642 with no code gaining a line
  (R20 16 to 3, R43 31 to 2, R50 43 to 11, R54 41 to 3, R27 45 to 17, R55 84 to 70).
- **Runner.** A crashing check is an ERROR and the rest of the gate still runs; the packaging sweep
  reports an unreadable file or zip instead of raising; .gate-debt lines matching no finding print a
  NOTE (14-wamhoff's R39 lines, 24-vondrak's R9 lines, left for each task's own revision).
- **Selfcheck** fails a first docstring line that opens with an id, stops mid-sentence or runs under 30
  characters, a PRIMARY family that is not a RULES key, and a PR id cited in memory, prompts, docs or
  .claude that procedural.py does not register.
- **Fixtures.** tools/fixture_suite.py runs planted-defect fixtures in tools/check_fixtures/ in a
  temporary copy and prints catalog coverage. Seeded with five (dfl-freight-audit as rejected, fixed, and
  with its verification script; rubric shapes; an unreadable prompt), all passing, covering 12 of 257
  codes.
- **Left as is, on purpose.** H9 fires on 9 of 22 accepted tasks but stays an ERROR: emit() has no
  warning tier and only a program ruling moves a finding to recommend(). R24's liveness floor and
  R129's cap form a 16 to 25 percent band, and R81 and R100 are documented bounds, so neither pair
  changed beyond R81's statement.
