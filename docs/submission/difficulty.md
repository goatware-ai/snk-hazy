# Making a task hard

What the desk learned from every hardening return between 2026-09-22 and 2026-10-01: three
`difficulty_check` FAILs on first builds, the reviewer's bulk "please make this task harder"
note of 2026-09-29 on all eight tasks in review, and the numbered "How to harden the task"
lists that followed it (ten lists across seven tasks). This page is the general shape. The
per-task cases, with figures, are in `memory/difficulty-check-lessons.md` and in each task's
`feedback-log.md`.

Read it at ideation (`workflows/01-ideation.md`), before calling a build done, and on any
return that asks for a harder task (`prompts/revise-task.md`).

---

## Two bars, and the reviewer's is higher

**The automated check.** `difficulty_check` runs two weak models (glm-5.2 and qwen3.6-27b) four
attempts each against the rubric. One PASS on any attempt fails the task: two of four failed one
build, one of three valid attempts failed two more. No PASS on four valid attempts is a pass. No
PASS on fewer than four valid attempts is INCOMPLETE, a runner error rather than a finding, and the
package goes back unchanged (`tools/fetch_feedback.py` prints the per-model attempts).

**The reviewer.** On 2026-09-29 every task in review got the same one-line note, including tasks
whose difficulty check had already passed with every attempt on both models failing. Itemised
lists followed, five to seven numbered arms each, and kept coming after the difficulty check
passed again. Four tasks were accepted after the bulk note and at most one list; the four still in
review on 2026-10-02 had taken one or two lists each on top of it. A strong-model blind
solve (Sonnet, prompt and inputs only) reproduced every graded figure of one task at twelve and
again at sixteen claims; it first missed graded figures at seventeen, when the asks had become
exact figures that each rested on several reconciliations at once.

**So build for the reviewer.** Passing `difficulty_check` is the floor. A build is hard enough
when a careful strong reader still has to get several independent calls right to reach each
graded figure, and a missed call moves a figure the rubric pins.

## Why the first builds were easy

Every first build failed on one or more of these. Each has a fix the reviewers accepted.

| Root cause | What it looked like | Fix | Check |
| --- | --- | --- | --- |
| The trap is labelled | An EXCEPTIONS column quoting the exception and the ITB section it breaks | Put the condition in the record's own prose (a bidder's cover letter) and keep the tabulation to what the form boxes carry | L7 |
| A legend states the disposition | "H = holding time exceeded, result not valid for compliance use" | The legend defines what was observed; the solver computes the hold from the dates and makes the call | L8 |
| Every exception is a two-file mismatch | Thirteen freight exceptions, each a difference between two tidy CSVs a script reproduces | A rule that turns on a document or a written act, exercised on both arms with a look-alike | PR22 |
| A derived quantity is typed in | Daily flows, age at test, cylinder area, a hold-days column | Give the raw record: totalizer readings, two measured diameters, collected and analysed timestamps | design read |
| A document narrates the answer | A manager's email confessing the missed calls; a memo narrating the incomplete set; a field book's conclusions; a transmittal line "No inspector is named"; an addendum Q&A that answers each exception | Rewrite as facts, particulars or a question; replace pre-deciding answers with harmless ones that keep the citation forms | design read |
| The verdict is far from its threshold | A six-month share at 38.5 percent against a 33 percent line, so no misread moved it | Set the figure on or a hair from the line, so the decisive read flips it | design read |
| A rule is stated once and applied once | Contract clauses on inspection certificates, certified tickets and written confirmations that no record exercised | Exercise every numbered rule and every arm of it | PR21, PR22 |
| Rubric weight sits on arithmetic | 24 of 33 positive points on figures a tidy read gives; the strict row on a count the trap does not move | Weight follows judgment (see the rubric section below) | design read |

## The design read

Do this before a build is called done and again on every hardening note. Write the answers into
the task's `clause-map.md` notes or the build log; they are what the next revision starts from.

1. **List every decision the golden makes:** each verdict, inclusion, exclusion, ranking and
   figure the rubric grades.
2. **For each, name where the solver learns the fact it turns on.** It fails the read if the
   answer is a column that names the rule, the sentence that states the rule, a legend that
   states the consequence, a memo or email that narrates it, or a column that has already done
   the computation.
3. **For each numbered rule in every input, and each test or arm inside it, name the record
   that holds and the record that fails.** A rule with three tests where only one ever fails, or
   a five-year rule whose refiling arm nothing exercises, is free difficulty left on the table.
4. **For each decision, name the misreading a careless solver makes and confirm it moves a
   graded figure.** `verify_golden.py` carries it as a variant reading; a variant that moves
   nothing means the decision is not graded difficulty. Hardened tasks carried 40 to 400 such
   near flips.
5. **Check that the traps interact.** The strongest builds had two or more independent misreads
   each flipping the same headline (the award, the approver, the verdict, the claim total), so a
   solver has to get all of them right at once.

## The hardening catalog

These are the shapes the reviewers asked for, in the order they recur. A good round applies three
to six of them, each as a new arm of a rule already in the package. The frame they hang on is a
**candidate set**: several bids, bills, claims or samples, each wrong one disqualified by a
different property found only in the files, so each missed trap changes the headline.

### 1. Both arms, with a look-alike

Every rule that decides something is exercised on the arm that holds and the arm that fails,
with records that look alike. Put a look-alike on the *holding* side as well, where the pull of
the decoy says it should fail.

- A signed inspection certificate for one reclass beside a system notice with no inspector.
- A preliminary notice served at the permit address (holds) beside one served on the direct
  contractor (fails).
- A carrier that applied the deficit rule correctly, beside the bills where it did not.

### 2. Knife-edges and thresholds

Put the decisive figure on its threshold or within a hair of it, and set thresholds between the
naive figure and the correct one so the naive reading flips the verdict.

- A certified ticket 4.6 percent over against a 5 percent tolerance; a cyanide hold outside 336
  hours by 3 h 50 m beside one inside by 20 minutes.
- A notice 21 days after first delivery beside one at exactly 20; a notice of completion copy
  sent a day late beside one on the last day.
- An award $79 over the approval line, under it only if the discount is credited correctly.
- A mineral at 1.98 percent that declares as zero on the unrounded amount; a whole-grain floor
  of 15 g against 14.80 g correct and 21.61 g with the syrup wrongly counted.

### 3. Derive, don't state

Give the record a practitioner works from, not the figure they would compute from it. Hours, not
days, where the rule runs in hours.

- Totalizer register readings, so a day's flow exists only as a difference; a register replaced
  mid-month and restarted at zero.
- Two measured diameters and a break time, no area and no age column.
- Collected and analysed timestamps, no hold column; "collected" defined as the end of the
  composite period.

### 4. Strip the signposts

No input narrates, concludes or confesses. Memos, field books, title abstracts, addenda and
transmittals state facts; the call is the solver's.

- A confession ("I have not been calling her") becomes a question, and the proof moves to a
  telephone log in another file.
- A closure is stated once, in a separate notice the solver has to find, not in the memo.
- An expectations memo that the records contradict in five places, each one graded.

### 5. Which document governs

Give two versions of the truth and a rule that says which one controls.

- A superseded specification revision beside the one in force, made numerically consequential
  (inventory lots split by date, an explicit ask whether the deliverable holds for all of it).
- A working sheet left on a stale revision while the rule document says the specification governs;
  a stale sheet that errs in the other direction on a second nutrient.
- A bulletin that misprints a week against the tariff table the contract subordinates it to.
- A transmittal figure a later correction letter changes; a withdrawn bill beside its marked
  corrected bill; a search whose "current through" date, not its run date, decides expiry.

### 6. Identity and record matching

Make the solver match records across files on more than a clean key.

- A hold registered under a trade name at the bid form's address, with a same-surname decoy on
  open hold at another address.
- A pro number or delivery ticket with two digits turned, matched only by the shipment's own facts;
  two survey point numbers exchanged against their codes.
- A clearance notice naming only a lot and a plant, resolved through a register note.

### 7. Timing, windows and written acts

- A bid logged at the due minute beside one returned late; a withdrawal and resubmission that
  re-times a bid.
- A confirmation in writing before delivery, one the day after, and a request from the consignee
  rather than the shipper.
- A ninety-day window that closes four days before the report date; a holiday or office closure
  stated once in a separate notice; a twelve-hour clock in one technician's book.

### 8. Stated conventions that flip a result

State the convention in the rules, then set the figures so the wrong convention gives a different
answer.

- Rounding per claim against rounding the total, with a cap set so the two disagree.
- Rounding order per line (linehaul, discount, net, surcharge), with one half-cent the carrier
  rounded the other way.
- Credits applied to accrued interest first; a test made on the unrounded amount; a day-count and
  due-day rule for a penalty.

After stating any convention, scan every record at every binding step for ties (two existing bills
landed on structural half-cent ties the moment a rounding order was stated). No pinned figure sits
on a tie (R133).

### 9. Data-integrity defects

A record that disagrees with itself or with its governing source, which only a careful read catches.

- A transposed month-end register line exposed by the operator's own reading and the next log's
  opening.
- A bar count that disagrees with the governing scale ticket; a survey leg shot twice to the wrong
  nail; a tie recorded from the wrong station.

### 10. Exact figures, not Yes/No

Turn verdict answers into linked exact figures: the amount held, the cushion, the release due, the
penalty accrued through a named date, the cheapest action that cures it. An exact figure moves
under almost every misreading; a Yes/No survives most of them. This was the change that first made
a strong-model blind solve miss.

### 11. Supply what the prompt calls missing, and use it

If the prompt says a record is absent or partial, the input-sufficiency check reads that as a gap.
Supply the file, and make it carry a contradiction the golden has to resolve (the manager's
attestation contradicted by July and August logs; a compound ingredient whose supplier specification
only arrives as its own file).

## Bigger, but only with new arms

"Harder and bigger" was the operator's direction on the bulk note, and the hardened tasks did grow:
10 to 11 bids, 38 to 46 bills, 12 to 17 claims, 5 to 10 inputs. Every new member was a new arm of a
rule already in play, a look-alike, or a decoy. Plain filler rows add effort, not difficulty; one
round dropped two clean bills to make room for two that each decided something. (On the desk this
repo came from, a 300-row task whose policy files handed over every formula was solved perfectly,
while a much smaller one built on a single hard decision was not.)

- Prefer no new rule and no new deliverable. Add a file only when an arm needs a document a
  practitioner would actually hold (a supplier specification, a transmittal, correspondence).
- Past the preview window a long CSV goes into side-by-side panels and the golden copies them block
  for block (H7, H8).
- Raise the time estimates in `form-lists.md` and `metadata.json` to match.

## The rubric for a hardened task

- **Weight follows judgment.** Cut rows on figures a tidy read of one table gives; fund the rows on
  the calls (+2 or +3 on the exclusion that decides the verdict).
- **The strict +5 row anchors on a figure the central trap moves.** A count that is the same whether
  or not the trap is caught grades nothing.
- **Each new arm takes its own row,** usually +1 or +2, and the look-alike's error takes a negative
  (-1 or -2). A silent set-aside the golden makes is graded too.
- **One verdict per row.** The in-app atomic check reads an "although" clause on a negative or a
  "because" clause on a positive as a second check.
- **Knife-edges collide with the figure checks.** A tenth (190.3) is caught between R50 and R82, a
  time or a date plus two figures trips R27: anchor on a cell storing two decimals, and on a
  time-boundary call name the call rather than the clock.

## Applying a hardening note

On a revision (`prompts/revise-task.md`, step 3):

- **The bulk one-liner** after a difficulty PASS: keep the task, harden it and grow it. Do not re-run
  the creation workflow. Run the design read, then apply three to six catalog shapes as new arms.
- **An itemised list:** apply each item as written and log it by number. Lists are written against
  the copy the platform holds, which can be older than the folder, so check each item against the
  current files first and record which were already in place, which are new, and which option was
  taken where the item offers one. Where an item leans on a fact the package has since corrected,
  apply its intent to the current mechanics (a holding-time arm moved from a struck 28-day metals
  period onto cyanide's 14 days).
- **Re-derive every answer after every arm.** Arms interact: a releasable-retention ask forced the
  money-held answer to Yes, and a second dispute only left a release if the money held rose.
- **Regenerate, don't patch.** Keep the generator in the task folder (a data model, the document and
  workbook builders, `build_golden.py`) and rebuild the package from it. Where a figure is sensitive
  to every parameter, grid-search the design model against the thresholds first.
- **Every new arm gets a `verify_golden.py` variant that flips a graded figure.**
- **A blind solve is worth running** on a hardened package: a strong model, prompt and inputs only,
  compared to the golden. A solve that reproduces every graded figure means the difficulty rests on
  spread alone; record the result in the log either way.
- **The third return is a rebuild from `clause-map.md`** (PR19), every ask re-read.
- **The Section 3 note** says which items were applied and names any file added, without stating the
  verdicts.
- **No coded check** for a design arm; PR21 and PR22 cover the shape. Say so in the log.
