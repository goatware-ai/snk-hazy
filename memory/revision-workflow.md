---
name: revision-workflow
description: "How a submitted task is revised under /revise-task: the revision fetches its own feedback with tools/fetch_feedback.py (verify model and folder, then fetch; stb is read-only, never create/update/sync) (the pasted feedback and live parts), the platform's four independent parts and the per-part re-upload check, salvages that live only on the platform, debt that cannot shelter a re-entered rubric, the authorship check's two gates, and review-comment.md left untouched on AutoEval rounds (2026-09-11)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 12ee6dd7-5e9b-4059-aab3-83e9dc851d57
  modified: 2026-09-22T08:08:24.791Z
---

> **Caveat:** the platform behaviour below is carried over from the desk this repo was built
> from. Returns have since been seen on this project, so the parts a fetched
> `feedback-<uid8>.md` confirms can be trusted; the rest has not been re-checked. The
> read-only-stb rule and the operator-submits rule are house policy and stand regardless.

## The revision fetches its own feedback (2026-09-22, replaces the no-stb rule)

`/revise-task` takes only the UID. The first turn verifies the task folder (UID via
metadata.json) and the build model (`tools/build_model.py check`, [[model-routing]]), then
FETCHES the feedback rather than asking for it:

    .venv/bin/python tools/fetch_feedback.py <uid>

It wraps `stb submissions fetch-task` and `stb submissions feedback`, writes
`feedback-<uid8>.md` into the task folder and prints it. Read it before diagnosing.

`stb` is read-only in a revision: fetch only. Never `submissions create` or `update`, never a
status sync, never an upload. Submitting stays the operator's, on the platform.

Two things the fetch is for, beyond the verdict. **The notes are often empty** - a return can
carry a header and nothing else - and the real signal sits in the JSON under
`eval_revision_notes` and the per-check notes in `evaluations[].overall_evaluation_result`,
which is why the note's silence is not a failed fetch. And it **diffs the platform against the
folder**: prompt text, rubric row count and every criterion. An edit made on the platform after
submission never comes back here, so where they disagree the platform is the fact and the
folder is what needs correcting. Observed 2026-09-22: a fill that stopped part-way left the
platform holding 23 of 29 criteria while the CSV had all 29, invisible until the two were
compared.

Encoded in prompts/revise-task.md step 2, both revise-task skills and
.claude/commands/revise-task.md.

## The platform holds four independent parts

Prompt, rubric criteria form, input zip and solution zip are stored and updated independently:
re-uploading `i-{name}.zip` does not touch the rubric form, and a revision that changed criteria
is not delivered until they are re-entered by hand (one task was once submitted to another's UID
and only the input zip was replaced, which survived by luck). Before resubmitting, list which
parts changed and update each deliberately; confirm the criterion COUNT on the form matches the
task's rubric CSV as the last check ([[repo-layout-and-tooling]]). Feedback re-finding a defect
the repo already fixed (a stale core.xml) means a per-part re-upload never landed: compare the
platform copy before re-repairing, and when the form action is a zip re-upload say so twice
and ask for confirmation it took. The oracle deficit is the only read-back of entered weights,
and the form can carry figures the CSV never held ([[rubric-liveness-criteria]] section 7); the
fix is verbatim re-entry with tools/hazy-helper and a spot check. A note can have been written
against an earlier version, so check that the filenames and tabs it cites exist.

**The input widget keeps every upload (2026-09-14, PR14 / L5).** A task reached adjudication with
its own deliverable workbook among the platform's input files while the repo's i- zip held only
the seven sources: an s- zip dropped in the input widget at a resubmission ships the golden as an
input, and nobody before the adjudicator said so. Before resubmitting, read the fetch-task JSON's
input_files list back against the i- zip's members; L5 catches a staged copy.

## Salvages live on the platform only

The platform side may salvage a task (an amendment input added, the prompt rewritten to cite it,
a 40-criterion rubric, a rebuilt golden) and accept it, leaving the repo two weeks stale; later
AutoEval then runs on the salvaged package and quotes tabs the repo never had. Before diagnosing
any feedback, diff the live prompt and criteria against the folder: ask the operator to paste
`stb submissions fetch-task <uid>` (the JSON carries the stored `prompt`, the full `criteria`
list with weights, `input_files.filename` plus `uploadedAt`, every eval report and
`criteria_breakdown[].evidence_snippet`). A mismatch means the platform holds a version the repo
does not: sync the repo to the live parts and rebuild what the feedback names. A golden built on
the platform side is not exempt from the authorship catalog (fix_floats, A2 datetime cells, A13
calcChain, A14, A5 tab share); the same pre-zip gates apply when it is resubmitted.

**Debt cannot shelter a rubric going back through the form.** The platform re-judges the rubric
under its CURRENT rules on every resubmission, so an old acceptance is not evidence: R24/R22
findings are fixed before resubmitting; debt is reserved for judge-landing lints (R29/R50/R51,
W4/W12) on wording the oracle passed 3/3 against labels the golden still carries. A rubric the
platform has already passed on is not re-entered for a nicety ([[rubric-criterion-count]]).

## The authorship check has two gates

The LLM-authorship check FAILs when llm-only < 3.5/5 on any file OR when combined = 0.7 x detect
+ 0.3 x llm-only < 0.55. Clearing the phrasing tells lifts llm-only to 1.0, after which detect
must reach about 0.36; composition (prose mass, tab share, number series) is the only lever for
detect ([[package-hygiene-pipeline]]). A platform-passed check is evidence against a coded
heuristic: a P5/A5 finding on a prompt and workbook the platform's own battery passed is debt,
not churn. An in-app finding on a form field (occupation, picks, prompt) is never debt.

## review-comment.md on an AutoEval round (2026-09-11)

On a revision driven by AutoEval feedback (golden solution check, alignment, penalty scope and
the other automated reports), leave `review-comment.md` (the form's Section 3 paragraph) exactly
as it stands; rewrite it only when the feedback owner is a human (operator, 2026-09-11). The
round still goes into `change.log` and `feedback-log.md` ([[feedback-log-convention]]); the
form-actions list says "Section 3 unchanged (AutoEval feedback)".

**Section 3 names (2026-09-14, PR11):** the adjudication trace reads review-comment.md as a claim
source; a person named there whom the deliverable does not name comes back as the next round's
finding even when every file is clean. Describe such a person by role, never by name.

- 2026-09-14 (a round 3): the trace reads EARLIER rounds' Section 3 paragraphs too. Round 1's
  paragraph named a removed title and two removed branch names; two rounds later adjudication
  returned both as items quoting the clean deliverable ("no input file gives Marcy a title.
  Briefing row 4 addresses 'Marcy; Branch GMs - ...'"). An item that quotes the deliverable's
  current text and says the inputs carry no support for a claim the deliverable no longer makes
  is a closed-item trace: change nothing, answer in Section 3 by describing the cell's shape, and
  never restate removed wording in any Section 3.

- 2026-09-14 (an adjudication note after a resubmission): "a fully-populated copy of the
  deliverable workbook is present among the files ... a Major leak if shipped as a contributor
  input" is real on the platform side even when the repo i- zip is clean at every commit; it is
  PR14's input-widget residue, answered on the form (delete the workbook from the input list,
  read input_files back), never by a repo change or a rebuttal. Feedback pasted under an
  "Adjudication Note" title is Stage 4: the fixes go back to adjudication and bypass human review.

- 2026-09-14 (an adjudication note, PR17): an adjudication note can lag the platform's own copy.
  The note asked for an addressee row and (b)/(f) dollar rows and named an author, while the
  folder restored from the platform at 04:03 the same morning already carried all three rows (C2,
  C17, C28) and a role-only From line; the person called fabricated is in one of the input
  documents. Before changing anything on such a note, compare each cited item against the live
  copy; an item the live copy answers is trace lag: change nothing, confirm the form rows,
  resubmit, log it.

- 2026-09-14 (a second adjudication note the same day, PR17 second instance): the note described a
  PO chronology defect in an input docx quoting two strings ("Entered Friday, acknowledged Monday
  morning", "the cancellation is dated yesterday") that appear nowhere in the platform's current
  copy or the delivered i- zip; the exchange had been moved to the 08/17 and 08/18 messages on
  2026-09-02, and the folder restored from the platform the same morning carries that repair,
  which is itself the proof the platform serves the fixed file. Two instances in one day: check
  the cited STRINGS, not just the claim, and treat a restored-from-platform folder as the
  authority.

- 2026-09-14 (a Stage 4 note): an adjudication note's weight read-back ("5/39") can come from the
  evaluation layer's criteria snapshot (`evaluations[*]` "Positive-weight pool = 39; total
  criteria = 21") rather than the live form (22 at 42): diff BOTH against the CSV. Its two items
  named text the current package does not contain (a front-page mandate C4 never had; a
  10/09/2026 no XML, serial or cached cell carries, equal to the s-zip upload date plus thirty)
  with `reviewer_revision_requested_at` after the uploads: a misread of the live package, answered
  on the form by describing the cells' shape, never by a golden edit. What did need fixing was the
  form itself at 42 positive (R24), found only because the JSON was read.

- 2026-09-14 (an adjudication return): PR17's lag can include the FIX itself - the restored live
  rubric already carried the criterion the note asked to add, pasted in the adjudicator's own
  phrasing as a third strict-liveness row at an appended +1 (positive 40, single-loss firing on
  both +5 rows). Diff the live criteria against the note before adding anything; reword an
  adjudicator-applied row to the gated house shape on the workbook's noun and fund it back inside
  +39 rather than accepting the appended weight.

- 2026-09-14 (a panel with unlabelled findings): a panel can carry "Where:" lines with no finding
  text under the stated findings. Each is still a finding; map its citations with a line-numbered
  extraction (the platform's input numbering ran about three lines ahead of pypdf's) and fix what
  the cited golden lines get wrong. Here they were an unsupported carrier claim and an unsupported
  storage check.

- 2026-09-14 (a round 4, PR18): the form's zip re-uploads did not go up for round 3 while the
  criteria did, and the next adjudication note was written against round 2's golden and round 1's
  inputs (it cited a lot no golden ever carried). Every zip-upload form action says "confirm the
  uploadedAt moved" and the round is closed only after a re-fetch shows both stamps on the day of
  the round; `stb submissions fetch-task <uid> -o <file>` is the operator's command, and
  evaluations[*].reference_soundness_check.metadata.agent_result.axes carries the judge's full
  findings when the note is garbled.

- 2026-09-14 (a round 3): the auto-mode permission check refuses one chained command that
  overwrites tracked inputs and deletes a zip and an untracked .gate-debt as irreversible local
  destruction. Back up to the scratchpad first, install each file in its own step, build a zip
  under a scratchpad name and mv it over the tracked one, and move a retired .gate-debt to the
  scratchpad instead of deleting it.

- 2026-09-15 (a round 3): the operator pasted only the golden solution check ("[0.0000, 1.0000,
  1.0000], no EC-actionable failures") and the first diagnosis was "collapsed run, resubmit
  unchanged". The fetch JSON for the same evaluation carried five more blocking results: an
  adjudication Major (Section 5.4 recipients missing), attribution FAIL 1/64, entity grounding,
  numeric grounding and self-consistency. A pasted note is one report of many: before concluding
  that nothing needs changing, ask for or run the fetch and list every `evaluations[-1]` child
  with `passed=False`; the blocking set is outcome NEEDS_REVISION or FAIL.

- 2026-09-15 (a rejection, PR19 PR20): from the third return a revision rebuilds from
  clause-map.md and dates its Rebuilt line (checked by R134); every struck phrase or removed claim
  goes into struck-phrases.md the same day as a literal or /pattern/ (searched by G42).

- 2026-09-17 (an operator-directed modernization, "update this task to meet our current gates and
  rules"): a modernization of an old NEEDS_REVISION task is a PR19 rebuild with no platform
  feedback; the gate's own findings are the feedback (51 errors from checks coded after the last
  entry). Sequence that worked: verify_golden.py first from the inputs, then prompt frame, O*NET
  picks, rubric to the +39 two-strict shape with critical-class negatives, golden date and prose
  repairs, input comma repairs, clause map and struck ledger, then the Package sequence; the H8
  preview window on a copied source tab is cleared by relaying the INPUT into side-by-side blocks.

- 2026-09-22 (the desk's first return, a difficulty FAIL): the note carried one sentence and no
  findings, and the session ran the fetch itself. That is now the standing behaviour rather
  than an exception: `tools/fetch_feedback.py <uid>` wraps the read-only calls and every
  revision starts with it. The JSON's difficulty child carried the per-model attempts the note did not
  ([[difficulty-check-lessons]]). /fetch-status had already moved the row to NEEDS_REVISION
  before the revision started, so step 7's list move was a no-op.

- 2026-09-17 (a second operator-directed modernization the same day): the sequence above held
  (stamp, gate as feedback, verify_golden.py first, prompt frame, picks, rubric to +39, golden
  repairs, clause map and struck ledger, Package). Four pipeline traps on a pre-September golden
  edited with openpyxl: re-pointing a moved column must rewrite BOTH ends of every range or SUMIFS
  returns #VALUE!; a figure copied from a formula-mode load is formula text; MINIFS/MAXIFS need the
  _xlfn. prefix written before office_resave or the tool rolls the file back as changed content;
  Excel's save stamps modified with today, so the in-world stamp goes back at zip level before
  fix_metadata. Diff every Excel-recalculated cell against a snapshot of the delivered file before
  trusting any of it (10,304 cells, zero drift). An H8 finding on a long CSV can be the golden's
  typed copy of it: dropping the typed money column and re-basing the figure on a visible
  item-file column cleared both CSV hits without relaying either file. An integer-dollar total is
  written with the mark and no cents ($12,473) so R50 and R82 both hold.
