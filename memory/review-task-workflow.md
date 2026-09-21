---
name: review-task-workflow
description: "/review-task end to end: reviews-list.md lookup first (a new round carries a NEW Task UID), tools/fetch_review.py stages reviews/<id>/ with the JSON and both zips (2026-09-10, zips never fetched by hand), the fetch-task JSON schema, the fidelity re-derivation step, the Note standard (numbered actionable items, 25-sentence ceiling, plain phrasing, --lint-note, generator strings reported never instructed) and the design lessons taken from fifteen reviews"
metadata:
  type: feedback
---

One review path, pinned to Opus ([[model-routing]]). The full procedure is
docs/reviewer/workflow.md with prompts/review.md and .claude/commands/review-task.md; this file
holds the rulings behind it. The golden read it applies is [[golden-fidelity]]; the rubric rules
are the four rubric files. Narratives: docs/reference/reviewer-feedback-corpus.md Part 5 ("Task
38" and "Desk review 6da90c8b").

## 1. Before the fetch: reviews-list.md

`reviews-list.md` at the repo root logs every task this desk has reviewed (columns Req number,
Task UID, Status, Rounds, Note), the counterpart of submission-list.md. Look the task up by Task
UID and, failing that, by the zip prefix in the folder listing plus the scenario in the Note,
because **a task returning for another round carries a NEW Task UID**. Where found, tell the
operator the Req number, the decision and the note left before reviewing; `revision_notes` in
the fetched JSON carries the previous note verbatim. After the worksheet, append a Req row and
refresh the totals. The Task UID is the command argument and the payload's `task_id` (distinct
from `assignment_id` and `submission_id`). The zip filename prefix is an observed grouping that
spans unrelated tasks and matches no labelled field; never present it as naming a contributor.
The S3 key's middle folder is the per-task lineage, stable across rounds.

## 2. Staging (operator, 2026-09-10)

`tools/fetch_review.py <review-id>` fetches the assignment JSON with `-o reviews/<id>` and pulls
BOTH zips beside it, creating the folder if absent, saving under the platform's own filenames,
leaving a folder that already holds a zip alone (`--force` re-pulls). The zips are byte-identical
to browser downloads; zips are never fetched by hand. `stb reviews download` cannot serve a review
packet (its widget matcher wants `upload_a_zip_file` or a lowercase `s3fileuploader-` prefix and
returns on the first widget); the tool asks the platform for a presigned GET on the ordinary
authed session, like tools/fetch_refinement.py. Never start the read with a zip missing: re-run
the stager, and where it cannot produce both, stop and tell the operator. `stb reviews accept`,
`revise` and `skip` are forbidden; the operator submits. `-o` is mandatory because
`review_check.py` globs `review_*.json` inside the folder it is given, silently. `reviews/` is
gitignored. `/review-task` runs in two phases and stops between them, because a model may only be
a second pass over a manual review.

**The JSON** (~10 MB, everything under `task_documents[0].submission_document`): `prompt`;
`criteria` (form rows `textarea-criterion` + `numeric-weight`, take by NAME);
`criteria_breakdown` (per criterion `oracle_pass_count`/`oracle_run_count`, `oracle_fail_rate`,
`oracle_stability`, `evidence_snippet`, `matched_file`; a row passing on some runs is a Rubric
Quality finding no aggregate reveals); the eval summaries (`self_containment_text_summary`,
`golden_solution_leakage_summary`, `dataset_quality_text_summary`,
`llm_authorship_text_summary`, `oracle_passed`, `oracle_reward`, `difficulty`,
`all_agent_stats`); `input_files.filename` and `s3FileUploader-*.filename`;
`eval_revision_notes` / `revision_notes`. Top level: `evaluation_display_results` (dedupe by
name), `blocking_check_enums`. Zip roles are decided by CONTENT (`_find_zips()`: the zip holding
`criteria_breakdown[].matched_file` weighted by criterion count is the solution, the one
holding the reference files is the inputs); the embedded upload timestamp does NOT identify the
role. Nothing else is needed: no prompt.md, no rubric CSV.

**`evaluations[*]` carries the judge's stated findings (2026-09-17, req 60).** A failed
`GDPVal judge: MAJOR (NEEDS_REVISION)` in `evaluation_display_results` is a display string only;
the findings are under `evaluations[*].overall_evaluation_result.children_results[]` where
`evaluator_name == "reference_soundness_check"`, in `metadata.agent_result` (`ec_summary`,
`axes[*].findings` with severity, evidence and cited lines). The same children hold the
self-consistency and entity-grounding `output_data`. The harness does not print them. Read every
`passed=False` child there before calling a judge result unexplained: on req 59 the display row
was reported as carrying no finding when the JSON held a Major the note then missed, and on
req 60 the judge found two real defects in a golden this desk had accepted three times. Same rule
as the hold entry in [[platform-hidden-return-hold]], applied to the review path.

## 3. The read

Read to find problems, not to confirm: the platform evals say what passed, so hunt for the
defect they missed and test the rubric against the atomicity and wording rules, not only against
the golden. Review everything, not a sample, scripting the mechanical parts; verify the delivered
work rather than build a rival answer key. Make no direct edits on the platform even where
editing authority allows: anything needing a fix goes in the note and the decision becomes Needs
Revision. Run `review_check.py` first as measurement, then walk its `[fidelity]` ledgers (table
ledger with row counts and id ranges, count words with their section, convention sentences, ids
named with "also / as well / would have needed", state words beside the matching input row with
[BAR] on a same-axis contradiction, the date columns per input CSV). The re-derivation itself:
recompute every schedule from the inputs (limits by date, delegations, business days), diff it
against the golden, re-key every date-gated test on every date column, re-do the arithmetic on
displayed figures as displayed (G21), and test every value-pinning criterion against the prompt
and inputs alone. A matching recomputation proves consistency, not correctness. A strong
dimension pulls attention off the dull parts, which is where both adjudication overturns of this
desk's accepts sat. Every overturn produces a coded check. Run the same section on our own memo
goldens before a submission by staging the task under a review-shaped folder (`_x/in`,
`_x/sol`).

**A generator string is not a send-back on its own** (team ruling 2026-09-04, binding on
reviews): ECs may use an LLM and a library to build inputs and goldens, so an openpyxl or
python-docx string is reviewer discretion and never earns `LLM-Generated: Input Files` by
itself. The one exception: a `dc:creator` or `cp:lastModifiedBy` left as a PLACEHOLDER (the
literal "generated") is an automatic send-back, coded A19 (BAR); every other LLM-PKG code (A3,
A13, A14, G2a, G2b) is HOUSE tier in reviews. Our own submissions keep the strict house standard
([[package-hygiene-pipeline]]).

## 4. The worksheet and the Note

The worksheet is only the form data: Decision, Error categories, Note, Time. Platform verdicts,
harness tiers, re-derived figures, the reader that failed and unchecked items go in the chat
report to the operator. The Note holds only what the EC has to act on (operator, 2026-09-04):

- Needs Revision: numbered items, one per fix, most severe first, each naming the exact place,
  the defect in one clause and the fix in the imperative; grouped under the form's area names
  (Prompt, Input files, Golden solution, Rubric) only when more than one area is touched; an LLM
  tell is an item under its file with the phrase quoted; anything optional is one last item
  opening "Optional:". Accept: "Accepted." plus at most one sentence of credit and at most one
  line opening "Optional:". Reject: the reason, no revision path. See [[review-optional-slot]].
- Where the task carries `revision_notes` or `eval_revision_notes`, OPEN with one line naming
  what was asked and whether it is fixed; a still-open point is also a numbered item with its
  anchor. No narrative recap, no opener, no praise, no sentence about what was verified, no
  authorship verdict unless a tell was found, no closing line.
- A generator string is REPORTED, never instructed: state what the property holds and where,
  give NO remedy (no "re-save through Excel", no "set the author"), the only exception to every
  item carrying a fix. Never name our own tooling (python-docx, openpyxl, lxml, .venv, "I ran a
  script"); state the defect as a property of the file the EC can see. Reporting what the EC's
  own docProps say is allowed. Mention a generator string only in the scarce non-blocking slot
  and only when that slot is not better spent; otherwise it goes in the chat report.
- **25 sentences is the absolute ceiling** (core team, 2026-09-10) and density is the thing the
  team asked reviewers to stop sending ("incredibly dense", "deeply technically worded", "feels
  highly synthetic"): around two paragraphs of a few sentences, one job per sentence, only the
  figures the EC must act on, the plain word wherever it points at the same place ("the
  per-unit rows do not multiply out"), a verdict on the last round in one sentence. The last pass
  is a read of the actual words; nobody copy-pastes model feedback verbatim.
- Money as the workbook shows it with the currency mark, "criterion 12", "partially" never
  "partly" (operator), no em dashes, each item one line in the file (the Note is a paste buffer).
- `tools/review_check.py --lint-note reviews/<id>` applies the A10 prose patterns, the
  banned-phrase list, the tooling ban, the anchor check, the 25-sentence ceiling, >40-word and
  >4-figure sentence flags; clearing it is the WHOLE pre-submit step, and the six-question
  "Before you submit" walk is no longer narrated. The model is the reviewers' own shortest notes
  on our tasks 12, 22, 31, 38, 39 and 43 (corpus Part 1b and Part 4).

## 5. Design lessons taken from fifteen reviews (2026-09-04 to 09-05)

Written into docs/submission/workflows/01-04 on 2026-09-05; these are OUR build lessons, not
review criteria. **Judgment drives difficulty, row count does not** (300 rows scored 1.00/1.00
because the policy files gave every formula; 9 PPI series scored 0.55/0.66): before scaling up,
ask what decision the extra rows force. **Candidate-set elimination** is a cheap mechanism (nine
candidate indexes, six wrong for six reasons, no hint in the prompt). **Real published data**
correlated with the models failing (BLS PPI, Census AWTS, USAspending) because its friction
comes free; a fabricated pack has to invent it, and a task went back because all 350 cost
figures were whole dollars. **Hide a step in a metadata column** (a `preliminary` flag implying a
five-month lag). **Write the prompt so it invites its own bad news.** **Close the golden with
what it does not settle.**
