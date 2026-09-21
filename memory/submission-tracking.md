---
name: submission-tracking
description: "How a task moves from drafts/ to submissions/ to accepted/ or archived/ and how submission-list.md is kept: /fetch-status owns every automation (ordinary moves, vanished-UID reject+archive, draft promotion, ACCEPTED zip and unzip, payments, reviews chart) and hand-edits cover only 'Needs attention'; the three platform gates behind two pending states; the six-section table format (to 2026-09-01)"
metadata: 
  node_type: memory
  type: project
  originSessionId: bb88f2dc-2539-40b9-a79c-6c7db83eb568
  modified: 2026-09-17T16:17:26.803Z
---

## The pipeline

A Hazy submission passes three gates: **1. AutoEval** (ten named post-submission evals:
golden_solution_check = 3 agents all at 1.0000; difficulty_check = Easy only when the worst
agent exceeds 80%; llm_authorship_check NEEDS_REVISION below mean 3.5; dataset_quality,
agentic_rubric_quality, audit, self_containment, golden_solution_leakage,
rubric_golden_alignment, geranium_safety; five feedback boxes 60-120 minutes after submission),
**2. Reviewer** (caps at 5 human reviews, then only accept or reject), **3. Adjudication** (one
exhaustive programmatic pass whose returned minor fixes go back to adjudication directly,
bypassing human review, the cheapest revision loop). Rebuttals of wrong auto-eval flags go as a
threaded reply to the daily Eval & Review Comments Slack post with the Task/Submission ID. The
platform exposes only two pending states, so `REVIEW_PENDING` means either with the reviewer or
with adjudication; `ACCEPTED` means only that the platform says so. The platform stores prompt,
criteria, input zip and solution zip as independent parts ([[revision-workflow]]).

## Folders

`/create-task [count]` builds N tasks, one at a time, into gitignored **`drafts/{seq}-{name}/`**
with no UID and no submission-list.md row. Sequence numbers continue the global max across
`submissions/`, `accepted/`, `archived/` and `drafts/`. Run the uniqueness diff against drafts
built earlier in the same batch, not only the submitted catalog ([[task-uniqueness-check]]).
`autoeval_check.py` with no argument sweeps `submissions/*` only, so drafts are checked by
explicit path. The operator submits and writes the UID into the draft's metadata.json
([[task-metadata]]); the next `/fetch-status` promotes the folder to `submissions/{seq}-{name}/`
and adds the row. Accepted tasks are zipped whole into `accepted/{seq}-{name}.zip` (feedback-log
and built zips inside) and the folder removed; a rejected or retired task is reduced to
`archived/{seq}-{name}/prompt.md` (kept for uniqueness diffing only, never as a design
reference; task 04's archive was removed 2026-08-19 and only its prompt kept). A task rejected by
platform system error may be recreated as a FRESH task with the next number and a reset log
(05 -> 07 yearend-deadstock-plan). `archived/` also holds task 04 while it is ACCEPTED, so an
archived folder does not by itself imply rejection. Layout conventions: [[repo-layout-and-tooling]].

## submission-list.md

One table per status section, ordered `## ACCEPTED`, `## REVIEW_PENDING`,
`## EVALUATION_PENDING`, `## NEEDS_REVISION`, `## OFFERED`, `## REJECTED` (finished work first,
then what is moving, then what is parked). No Status cell: a status change is moving the row.
Columns `Seq | Task name | Taskboard UID | Updated | Model` (Created dropped 2026-09-11), plus `Note` under
NEEDS_REVISION only (a pointer; the record is the task's feedback-log.md, and a row leaving the
section drops its note). `Model` is `built_with` for a folder that exists, otherwise persisted in
the table ([[model-routing]]). `Updated` is US Eastern (EST/EDT), `-` for rows predating the
column. `fetch_status.parse_submission_list` reads each row against its own section header.

## /fetch-status owns the automations

`.claude/skills/fetch-status/fetch_status.py` points at Hazy-Production
(`cda2e943-8524-45f0-a966-469903337102`, the Hazy_Task_Creation node), runs under Sonnet, resolves UIDs through
submission-list.md, and syncs EVERY unequal local/platform pair on every run with no
confirmation step (`--no-apply` reports without writing):

- **Ordinary progress**: a row whose section disagrees with the platform's Assignment State
  moves, Updated re-stamped.
- **A vanished UID** (absent from `stb submissions list`, download refused) is a rejection: the
  row moves to REJECTED and the folder is reduced to `archived/{seq}-{name}/prompt.md`.
  Idempotent.
- **A matched draft**: an OFFERED/EVALUATION_PENDING submission with no row is matched against
  every `drafts/*/metadata.json` taskboard_uid and promoted; no match leaves it under "Needs
  attention" as `?`.
- **An accepted task** is zipped into `accepted/` and its folder removed; **a task leaving
  ACCEPTED** (adjudication send-back) is unzipped back into `submissions/` and the zip deleted
  (added 2026-08-27 after 04, 10 and 22 sat as zips); a restored folder is frozen at the shape it
  was accepted in and gets re-fitted to current conventions.
- **Reviews** are charted from `stb reviews list -p <project>` (OFFERED and REVIEW_PENDING
  labelled "To review"; REVIEW_PENDING means the opposite thing in the two charts). **Payment
  status** is charted for both, the actionable line being accepted-with-no-payout; snapshots
  predating the field count as no baseline.

Hand-edit only what it reports under "Needs attention" (no matching draft, an unrecognised
state, an unreadable section), using the six headings exactly and stamping Updated in Eastern
time. `/set-status` and `tools/set_status.py` were removed 2026-08-24. The `stb` CLI
version-gates itself; see [[stb-cli-upgrade]] when every command errors as outdated.

## refinement-list.md (2026-09-11)

Refinements are submissions on their own project node. Hazy has no Refinery node yet, so `REFINE_PROJECT_ID` is unset and the refinement block is skipped.
`/fetch-status` charts them as a third block and syncs **refinement-list.md** at the repo root.

**One table**, not one per status (operator): columns `Task UID | Task name | Status |
Updated | Note`, grouped in the STATUSES order then by UID. **Note** is the original task's
name when the refinement's `origin_submission_id` resolves against submission-list.md, and
`-` when it does not - i.e. Note is the "this is my own task" marker, since most refinements
handed out are other contributors' work (5 of 13 were ours on 2026-09-11).

Task name comes from `refinements/<uid>/metadata.json`, so an unfetched refinement
still gets a row and is reported under "Not fetched yet" with the `/refine-task <uid>` that
fetches it. A row the platform stops listing is reported and **left alone**: refinements have
no archive/promote automation.

Two gotchas if this is extended. `split_row`/`header_columns` are submission-specific
(numeric Seq cell, literal "Seq" header); the refinement file needs
`refine_split_row`/`refine_header_columns`, which key off a UID cell and the "Task UID"
header, or it re-reads as empty and every row is re-added every run. And the parser must skip
`## ` lines when collecting the preamble, or the renderer's own heading doubles on each write.

## No refinement pipeline status (2026-09-11)

`REFINEMENT_PIPELINE` and `refinement-candidates/` were removed entirely (operator). A vanished
UID is archived again, the old way: row to **REJECTED**, folder reduced to
`archived/{seq}-{name}/prompt.md`. What the row keeps is a **Note**, so REJECTED now carries one
alongside NEEDS_REVISION: a row that had reached ACCEPTED before vanishing did not fail, it went
to the refinement pipeline and still pays out, so its Note reads `Payout submitted; went to
refinement`. The payment half comes from the prior snapshot, since a vanished UID cannot be
queried. The 10 parked packages were archived and the folder deleted on 2026-09-11.

## Archived then re-listed: restore the folder (2026-09-14)

A UID that vanishes is archived (folder reduced to `archived/{seq}-{name}/prompt.md`). When the
platform re-lists it as NEEDS_REVISION the row moves back but the package does not, so
`/revise-task` finds a row and no folder. **`python3 tools/restore_submission.py <uid>` or
`--all-needs-revision`** rebuilds it from `stb submissions fetch-task` (download does not work:
"has no uploaded file to download"). 17 rows were restored this way on 2026-09-14.

Costs that do not come back: build_session and any feedback-log history. A restored
old task also gates against today's rules, so expect a large error count that is pre-existing
drift, not restore damage - 01-hartwell came back at 152 errors, mostly R55/R54/R18, against 38
on a never-archived control of similar age.

## "ARCHIVE FAILED: no submissions/ folder found to archive" is often benign (2026-09-17)

When a vanished UID that had already reached ACCEPTED goes through the reject/archive routine,
the script looks for a `submissions/{seq}-{name}/` folder to move into `archived/` and reports
ARCHIVE FAILED if none exists. For an already-ACCEPTED row this is expected, not data loss: the
folder was already zipped into `accepted/{seq}-{name}.zip` and removed when it first reached
ACCEPTED, so there is nothing left under `submissions/` to archive. **Check `accepted/` for the
zip before treating this as a problem** - confirmed on 2026-09-17 for tasks 23, 32, 37, 38, 39,
41 after 13 submissions vanished from the platform in one 15-minute /fetch-status cycle (the
largest single-cycle drop seen this session); all six had their accepted/ zip intact and the
ARCHIVE FAILED messages were false alarms.

## Orphan UID 5a02fddb is task 05, not task 07 (2026-09-17)

`/fetch-status` repeatedly flags `5a02fddb` under "Needs attention" (NEEDS_REVISION, no
submission-list.md row, no matching draft). This is **not** a UID that changed under task 07 -
it is task 07's *predecessor*, task 05 (also `yearend-deadstock-plan`), rejected 2026-08-18 by
an AutoEval infrastructure failure with no substantive finding. Per the reset-and-recreate
convention (Folders section above, "05 -> 07"), the identical package was resubmitted fresh as
**task 07** under a **new** UID `872f01f2-...`, and task 05's row/history was deliberately
closed and never carried forward (confirmed in the old feedback-log.md provenance note,
recovered via `git log -S`). Task 07 is correctly tracked today: ACCEPTED, zipped at
`accepted/07-yearend-deadstock-plan.zip`. The `5a02fddb` orphan is just the platform's own
leftover record of the abandoned task 05 attempt - safe to leave unmatched, never add it as a
row.
- **2026-09-17 (detention-claim-audit on 12's UID 9266b8e2):** when a retired task's form is reused for a
  fresh draft, the platform UID re-enters as EVALUATION_PENDING and /fetch-status moves the OLD row
  (12 -> EVALUATION_PENDING at 19:23) instead of promoting the draft, because the UID already has a
  row. Re-point by hand: move the draft to submissions/, suffix the rubric with the uid8, replace the
  old row with the draft's seq, name and built_with, leave the retired seq in archived/ with no row.
  The automation has no case for a matched draft whose UID already has a row.

