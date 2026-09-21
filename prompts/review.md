# Prompt: review one Hazy task by another contributor

> **Inherited from the Geranium desk, not ported to Hazy, and unverified.** Hazy has no
> reviewer assignment: `stb reviews list` and `stb adjudications list` both return no available
> review or adjudication task for this project, so the reviewer workflow does not exist here yet
> (delta D12). Everything below was written for the Wholesale Trade sector and the single-sector
> rules that went with it, neither of which Hazy has, and none of it has been checked against
> Hazy's own platform. Do not treat a rule in it as current until a review assignment confirms
> the workflow exists.

You are reviewing **one** submission for Snorkel's Project Hazy (GDPVal++). You are a quality
gate for the dataset: what you accept goes in, and what you send back costs another contributor
a revision attempt. This file is the whole procedure and the note standard; `/review-task`
loads it and runs it in one pass.

**Assigned sector:** Wholesale Trade.

**Rule set.** `docs/reviewer/platform/` holds the live captures and they win on any conflict:
`reviewer-guidelines-v5.1.md` (what you must check), `feedback-best-practices.md` (the note
standard), `reviewer-rubric.md` (how LLM tells convert to a verdict),
`platform-review-form.md` (the fields you fill), `task-example-omnichannel-routing.md` (the
Hub's own finished golden, the standard for presentation and evidentiary depth). Read the
first four before touching anything. Check ids cited below are listed in `docs/rules.md`.

**Scope.** Verify **every** rubric criterion against the golden, not a sample; open every input
file; trace every asserted figure to the inputs. O*NET metadata is not reviewed. Time scales to
the task: 30 minutes to confirm a clean task, 60 to 120 to review and write feedback; past 120,
send it back with what you found and say which parts went unverified.

**Boundaries.** Make no edit on the platform, even inside reviewer editing authority: every fix,
however small, goes into the note and the decision is Needs Revision. Input files are locked on
the platform, so every input defect routes to Needs Revision. Submitting is the operator's step,
after reading the worksheet. `reviews/` is gitignored and holds another contributor's files
marked Not for Distribution: never commit them, never copy them into `submissions/` or
`drafts/`, never let a phrase of them into a task of ours.

## 1. Stage the assignment

```bash
.venv/bin/python tools/fetch_review.py <review-id>       # review_<short>.json + both zips into reviews/<review-id>/
```

It creates the folder if needed and saves each zip under the platform's own filename. A folder
that already holds any zip is left as it is and only the JSON is refreshed; `--force` re-pulls.
`stb reviews fetch-task <review-id> -o reviews/<review-id>` fetches the JSON alone; `-o` is
mandatory because the harness globs `review_*.json` inside the folder it is given and reports
nothing, with no error, when the file is elsewhere.

Keep both zips **as zips and unrenamed**. The filenames do not say which is which and their
timestamps mislead; the harness matches each by content and reports the basis on its
`[packaging]` lines. If the stager cannot produce both zips, stop and tell the operator: without
the bytes there is no packaging, provenance, liveness, figure-tracing or input-substance check.

**Look the task up in `reviews-list.md`** (repo root): by Task UID first, then by the `s3Key`
prefix plus the scenario in the Note column, because a task returning for another round carries
a new Task UID. If it is there, report the Req number, the decision and the note left last time
before going further; `revision_notes` in the JSON carries that note verbatim.

## 2. Read the platform's verdicts

Under `task_documents[0].submission_document`: `prompt`; `criteria` (`textarea-criterion` +
`numeric-weight`); `criteria_breakdown` (per criterion: `oracle_pass_count`/`oracle_run_count`,
`oracle_stability`, `evidence_snippet`, `matched_file`; a criterion passing on some runs only is
a Rubric Quality signal no aggregate shows); `self_containment_text_summary`;
`golden_solution_leakage_summary`; `oracle_passed`/`oracle_reward`;
`llm_authorship_text_summary`; `dataset_quality_text_summary`; `all_agent_stats` with
`difficulty`; `input_files.filename` and `s3FileUploader-*.filename`; `revision_notes` and
`eval_revision_notes`; `evaluation_display_results`.

Report these verbatim, with no quality commentary attached. They say what is settled and where
your hours are needed. Difficulty fails as **Easy** only when **both** tested models exceed 80%.

## 3. Run the harness (measurement)

```bash
.venv/bin/python tools/review_check.py reviews/<review-id>
```

Run it before the read, so the read can walk its ledgers. It stages the packet as a task-shaped
folder (`_task/`), runs every registry check (`tools/gcheck/`) whose needs the packet supplies,
and prints three tiers, tiered by `gate_families.REVIEW_TIER`:

- **[BAR]**: the reviewer bar in `reviewer-guidelines-v5.1.md`. Can justify a Needs Revision.
- **[HOUSE]**: this repo's stricter authoring conventions. **Never** send another contributor's
  task back for one; say so each time one appears.
- **[CONTEXT]**: measurement. The `[fidelity]` ledgers (table row counts and id ranges, count
  words with their section, convention sentences, state claims beside the input record, the
  date columns each input carries) are what step 4 item 8 walks. The `[authorship]` lines (the
  package sweep and the A10 prose check, reported even when clean) are what the note's
  LLM-authorship sentence rests on: write that sentence from them, never from a read-through
  alone, and where one fires name the file and the phrase and say whether it blocks.

Registry findings carry their check id in brackets under `[prompt_inputs]`, `[golden_rubric]`,
`[authorship]`, `[packaging]`; the `[registry]` lines say how many checks ran and which needs
the packet could not supply. A `[fidelity]` line in the BAR tier is a state word the input
record contradicts; verify it against the row before citing it. Say which zip it matched to
which role.

## 4. The read: judgment the harness cannot make

**Read to find problems, not to confirm the task is fine.** The platform's evals already report
what passed; your value is the defect they missed. Test the rubric against the atomicity and
wording rules, not only against the golden; read the prompt for what it gives away; treat every
"looks fine" as a check not yet run. Unzip both archives under `reviews/<review-id>/` and open
every file. Record every finding as an anchored fact: file, criterion number, sheet, cell, figure.

1. **Prompt.** Wholesale Trade work? A practitioner handing off work, or a generated task?
   Overspecified, underspecified, or answerable without the inputs?
2. **Every input file.** Real, substantial, necessary? Round numbers, generic company names
   and a tidiness no real extract has are the tells.
3. **Hours.** Genuinely 5+ by hand, with 3 the floor?
4. **Every criterion against the golden.** Quote the evidence (sheet and cell, or paragraph);
   pass or fail each; give the weakest-looking criteria the closest reading.
5. **Every value-pinning criterion against the PROMPT and the inputs alone.** Checking against
   the golden can only show they agree; ask whether a solver who never saw the golden could
   derive the number from what the prompt states and the files carry. A criterion pinning a
   figure that needs an unstated selection rule scores the golden's own arbitrary choice; the
   fix is to state the rule in the prompt or to score the property rather than the value.
6. **Every asserted figure traced to the inputs.** Show the arithmetic.
7. **Bounded subjective criteria are valid.** A criterion that names its conditions and scores
   the reasoning does not come back for being subjective; only unbounded ones do.
8. **Re-derive the golden, then read it against itself.** Rebuild every schedule the golden
   reports from the inputs with a throwaway script and diff it against the golden's tables.
   Then walk the step 3 `[fidelity]` ledgers: every count word against the table that carries
   it, every convention sentence against every section it governs, every state word against
   the input column that records it, every corrective action against the record it relies on.
   Each contradiction is a Golden Solution Quality send-back anchored to the two lines that
   disagree. A recomputation that matches proves consistency, not correctness: key each test
   on the column the policy sentence names, and re-key every date-gated test on each date
   column the input carries before calling a schedule clean.
9. **The arithmetic again on the DISPLAYED figures, as displayed** (G21). A full-precision
   rebuild is blind to the printed table; re-check every relationship each table states
   (per-unit times periods, subtotals, rate times base) at the displayed precision. The fix is
   to carry more decimals, never to recalculate: it is a presentation defect, not a
   calculation error, and the note says so.

Script the mechanical parts (recompute a column, count keys, diff an evidence tab against its
source) so full coverage fits the window; read the prompt, the prose and the presentation by
eye. The recomputation checks the delivered work and is not a rival answer key: where it
disagrees, cite the input rows and the golden's own line, never your own figure. Anything you
found that the harness did not: verify it mechanically where it can be, and say plainly when it
cannot be.

## 5. Decide

On the complete read, then write the note:

- **Accept.** Passes all checks with nothing to fix. Stylistic differences from how you would
  have written it are fine.
- **Needs Revision.** Fails one or more checks but is fixable: an overspecified, underspecified
  or input-free prompt; decorative, synthetic, corrupted or IP-risky inputs; a golden that does
  not answer the prompt, has wrong data or reads as unedited LLM output; mostly incomplete or
  vague criteria; any change that would substantially alter the task.
- **Reject.** Fundamentally unacceptable: prompt or inputs off-sector, fully LLM generated, or
  a third failed revision.

**Penalty share is never a send-back** (R61): negative weight as a share of positive weight is
a recommendation, at most one optional line, and earns no category. The binding negative bar is
at least two negatives at -3 to -5.

**A generator string is reported, never instructed, and never a send-back alone.** Where
docProps name the writing library (`openpyxl`, `python-docx`, an `Application` naming the
library), state what the property holds and where, and stop: no re-save instruction, no
category, never a reason for the decision. It is worth one non-blocking line only when the slot
is not better spent and the scenario does not make the string appropriate; otherwise it goes in
the chat report alone. The exception is a `dc:creator` or `cp:lastModifiedBy` left as a
placeholder such as the literal "generated" (A19, BAR): a numbered item that decides. Every
other `LLM-PKG` code is HOUSE on another contributor's task.

**Categories.** At least one, six the practical ceiling: `Prompt Quality`, `Input File Quality`,
`LLM-Generated: Input Files`, `LLM-Generated: Golden Solution`, `Golden Solution Quality`,
`Rubric Quality`; `Suspected duplicate or template` may sit beside an Accept; `Adjudication
Ready` and `No Issues - Recommend EC as Reviewer` are Accept only.

## 6. The note

Required on all three decisions, and it carries only what the EC has to act on. No opening line
about the task, no praise before the substance, no sentence about what was checked and found
clean, no LLM-authorship verdict unless a tell was found, no closing line.

**Previous feedback gets a verdict.** Where the JSON carries `revision_notes` or
`eval_revision_notes`, open with one sentence naming what the last round asked for and whether
it is fixed, then the numbered items. A still-open point is also a numbered item, restated with
its anchor. Name points by subject, not round number.

**Needs Revision.** Numbered items, one per fix, most severe first. Each names the exact place
(criterion 12, Claim!C14, item_file.xlsx, the third paragraph of the memo), states the defect in
one clause, and gives the fix as an instruction. Group under the form's area names `Prompt`,
`Input files`, `Golden solution`, `Rubric` only when more than one area is touched. An LLM tell
is an item under its file, phrase quoted, severity per `reviewer-rubric.md`. A figure the EC
will touch is stated inside its item. Anything optional is one last item opening
"Optional:". Name every blocker in one pass: one now and another next round costs the EC
an attempt.

**Accept.** "Accepted." then at most one sentence of credit, then at most one line opening
"Optional:". The figures re-derived during the review go in the chat report. The platform's
`feedback-best-practices.md` allows only two things in that slot, what you fixed yourself and at
most one pattern for the next submission, so an item that is neither is cut rather than labelled.

**Reject.** The reason in one or two sentences, no revision path.

**How it reads.** Imperative instructions ("Split criterion 7 into one criterion per figure").
Money as the workbook shows it, with currency mark and cents. Criteria as "criterion 12". One
job per sentence, plain words over precise ones, no em dashes, "partially" never "partly". Each
item is one line in the worksheet, because the Note is pasted into a free-text field and a hard
wrap lands as a literal newline. **25 sentences is the hard ceiling**, around two paragraphs of a
few sentences each; no sentence over 40 words; no sentence carrying more than four figures. Dense
technical phrasing is the specific thing the core team asked reviewers to stop sending. Never
name our tooling (python-docx, openpyxl, lxml, `.venv`, "I ran a script"): state the defect as
a property of their file they can see for themselves; reporting what their own docProps say is
allowed. Never: "Overall", "demonstrates", "well-structured", two adjectives stacked before a
noun, "you may want to consider", "Hi", "Thanks", a heading or bullet wrapped around a single
sentence. Write the words yourself and read them back: every figure traced to where the review
found it, every sentence an instruction to fix rather than a summary of a finding.

Shape:

```
Golden solution
1. The under-billed table gives DFL7718272 the full $251.68 where the inputs support $1.18. Restore the cell so the six rows sum to the $251.68 total.
Rubric
2. Criterion 13 attributes every accessorial to a missing liftgate request; residential delivery turns on the address on the bill of lading. Reword it to cover both.
3. The prompt requires a deadline on every claim and the rubric measures only the earliest. Add a criterion on the deadline column of the claims schedule.
```

## 7. Worksheet, lint, bookkeeping

Write `reviews/<review-id>/worksheet.md` holding **only the submission form data**
(`docs/reviewer/platform/platform-review-form.md`):

```markdown
# Review: <review-id> (submission form data)

## Decision
Accept | Needs Revision | Reject

## Error categories
<the classes that apply>

## Note
<ready to paste, one item per line>

## Time
<minutes, estimated from the task's scale; the operator confirms the actual figure>
```

Then lint the note and clear every hit; it applies the A10 prose patterns, the banned list, the
tooling ban, the anchor on every item, the Accept shape and the sentence ceilings:

```bash
.venv/bin/python tools/review_check.py --lint-note reviews/<review-id>
```

Do not narrate the lint. What it cannot see you still settle silently: whether the EC would know
what to submit without messaging anyone, whether every sentence rests on a finding from this
review, and whether the note matches the decision and the categories.

**Append the review to `reviews-list.md`**: one Req row with the Task UID, the status, the rounds
count and a Note naming the task and, where the prior note was this desk's, which Req it was and
whether the points closed. Refresh the totals and the zip-prefix grouping below the table.

## Deliverables, exactly these

1. **The platform's verdicts**, verbatim from the JSON, no commentary attached.
2. **The harness output** in its three tiers, `[HOUSE]` findings called out as no grounds for a
   send-back.
3. **`reviews/<review-id>/worksheet.md`** as above. Everything else (anchored findings,
   re-derived figures, anything unverified) goes in the chat.

Then hand over. Submitting is the operator's step; if you see a pattern across submissions, say
so in the chat so it can be raised in `#ec-geranium-project`.
