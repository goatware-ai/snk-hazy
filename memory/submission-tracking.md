---
name: submission-tracking
description: "How a task moves from drafts/ to submissions/ to accepted/ or archived/ and how submission-list.md is kept: /fetch-status owns every automation (ordinary moves, vanished-UID reject+archive, draft promotion, ACCEPTED zip and unzip, payments) and hand-edits cover only 'Needs attention'; the three platform gates behind two pending states; the six-section table format"
metadata: 
  node_type: memory
  type: project
  originSessionId: bb88f2dc-2539-40b9-a79c-6c7db83eb568
  modified: 2026-09-17T16:17:26.803Z
---

## The pipeline

A submission passes three gates: **1. AutoEval** (post-submission evals, of which
`golden_solution_check` = 3 agents all at 1.0000 and `difficulty_check` = Easy only when the
worst agent exceeds 80% are the two whose arithmetic matters here, plus an
`llm_authorship_check` that returns NEEDS_REVISION below mean 3.5; feedback boxes land 60-120
minutes after submission), **2. Reviewer** (caps at 5 human reviews, then only accept or
reject), **3. Adjudication** (one exhaustive programmatic pass whose returned minor fixes go
back to adjudication directly, bypassing human review, the cheapest revision loop). The full
eval list is carried over from the desk this repo was built from and not yet confirmed here;
[[platform-expertdocs]] holds what is known of it. Rebuttals of wrong auto-eval flags go as a
threaded reply to the daily Eval & Review Comments Slack post with the Task/Submission ID. The
platform exposes only two pending states, so `REVIEW_PENDING` means either with the reviewer or
with adjudication; `ACCEPTED` means only that the platform says so. The platform stores prompt,
criteria, input zip and solution zip as independent parts ([[revision-workflow]]).

## Folders

`/create-task [count]` builds N tasks, one at a time, into gitignored **`drafts/{seq}-{name}/`**
with no UID and no submission-list.md row. Sequence numbers continue the global max across
`submissions/`, `accepted/`, `archived/` and `drafts/`. Run the uniqueness diff by hand against
drafts built earlier in the same batch as well as the submitted catalog; this desk has no
accepted-asks map (2026-09-21).
`autoeval_check.py` with no argument sweeps `submissions/*` only, so drafts are checked by
explicit path. The operator submits and writes the UID into the draft's metadata.json
([[task-metadata]]); the next `/fetch-status` promotes the folder to `submissions/{seq}-{name}/`
and adds the row. Accepted tasks are zipped whole into `accepted/{seq}-{name}.zip` (feedback-log
and built zips inside) and the folder removed; a rejected or retired task is reduced to
`archived/{seq}-{name}/instruction.md` (kept for uniqueness diffing only, never as a design
reference). A task rejected by platform system error may be recreated as a FRESH task with the
next number and a reset log; an archived folder does not by itself imply rejection, since a
resubmitted-fresh predecessor is archived while its successor is live. Layout conventions:
[[repo-layout-and-tooling]].

## submission-list.md

One table per status section, ordered `## ACCEPTED`, `## REVIEW_PENDING`,
`## EVALUATION_PENDING`, `## NEEDS_REVISION`, `## OFFERED`, `## REJECTED` (finished work first,
then what is moving, then what is parked). No Status cell: a status change is moving the row.
Columns `Seq | Task name | Taskboard UID | Updated | Model` (Created dropped 2026-09-11), plus `Note` under
NEEDS_REVISION only (a pointer; the record is the task's feedback-log.md, and a row leaving the
section drops its note). `Model` is `built_with` for a folder that exists, otherwise persisted in
the table ([[model-routing]]). `Updated` is US Eastern (EST/EDT), `-` for rows predating the
column. `fetch_status.parse_submission_list` reads each row against its own section header.

A REJECTED row also carries a Note, because a row that had reached ACCEPTED before its UID
vanished did not fail. The payment half of such a Note comes from the prior snapshot, since a
vanished UID cannot be queried.

## /fetch-status owns the automations

`.claude/skills/fetch-status/fetch_status.py` points at Hazy-Production
(`cda2e943-8524-45f0-a966-469903337102`, the Hazy_Task_Creation node), runs under Sonnet, resolves UIDs through
submission-list.md, and syncs EVERY unequal local/platform pair on every run with no
confirmation step (`--no-apply` reports without writing):

- **Ordinary progress**: a row whose section disagrees with the platform's Assignment State
  moves, Updated re-stamped.
- **A vanished UID** (absent from `stb submissions list`, download refused) is a rejection: the
  row moves to REJECTED and the folder is reduced to `archived/{seq}-{name}/instruction.md`.
  Idempotent.
- **A matched draft**: an OFFERED/EVALUATION_PENDING submission with no row is matched against
  every `drafts/*/metadata.json` taskboard_uid and promoted; no match leaves it under "Needs
  attention" as `?`.
- **An accepted task** is zipped into `accepted/` and its folder removed; **a task leaving
  ACCEPTED** (adjudication send-back) is unzipped back into `submissions/` and the zip deleted
  (added 2026-08-27 after three tasks sat as zips); a restored folder is frozen at the shape it
  was accepted in and gets re-fitted to current conventions.
- **Payment status** is charted, the actionable line being accepted-with-no-payout; snapshots
  predating the field count as no baseline.

Hand-edit only what it reports under "Needs attention" (no matching draft, an unrecognised
state, an unreadable section), using the six headings exactly and stamping Updated in Eastern
time. `/set-status` and `tools/set_status.py` were removed 2026-08-24. The `stb` CLI
version-gates itself; see [[stb-cli-upgrade]] when every command errors as outdated.

## "ARCHIVE FAILED: no submissions/ folder found to archive" is often benign (2026-09-17)

When a vanished UID that had already reached ACCEPTED goes through the reject/archive routine,
the script looks for a `submissions/{seq}-{name}/` folder to move into `archived/` and reports
ARCHIVE FAILED if none exists. For an already-ACCEPTED row this is expected, not data loss: the
folder was already zipped into `accepted/{seq}-{name}.zip` and removed when it first reached
ACCEPTED, so there is nothing left under `submissions/` to archive. **Check `accepted/` for the
zip before treating this as a problem** - confirmed on 2026-09-17 for six rows after 13
submissions vanished from the platform in one 15-minute /fetch-status cycle; all six had their
accepted/ zip intact and the ARCHIVE FAILED messages were false alarms.

## An orphan UID under "Needs attention" can belong to an abandoned predecessor

A UID that keeps coming back under "Needs attention" (NEEDS_REVISION, no submission-list.md row,
no matching draft) is not necessarily a UID that changed under a live task. It can be the
platform's leftover record of an abandoned predecessor: a task rejected by an infrastructure
failure with no substantive finding, resubmitted fresh under a new sequence number and a NEW
UID, with the old row and history deliberately closed and never carried forward. Such an orphan
is safe to leave unmatched; never add it as a row.

## A reused form's UID moves the old row instead of promoting the draft (2026-09-17)

When a retired task's form is reused for a fresh draft, the platform UID re-enters as
EVALUATION_PENDING and /fetch-status moves the OLD row (to EVALUATION_PENDING) instead of
promoting the draft, because the UID already has a row. Re-point by hand: move the draft to
submissions/, suffix the rubric with the uid8, replace the old row with the draft's seq, name and
built_with, leave the retired seq in archived/ with no row. The automation has no case for a
matched draft whose UID already has a row.
