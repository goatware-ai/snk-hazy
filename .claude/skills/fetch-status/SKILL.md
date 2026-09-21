---
name: fetch-status
description: Fetch current Hazy submission counts from the Snorkel platform, reconcile them against submission-list.md, and report how they changed since the last check. Use when the user runs /fetch-status or asks about submission status, how many tasks are accepted, what's in review, or whether anything moved in the queue.
model: sonnet
---

# fetch-status

Reports Hazy-Production submission counts, what moved since the previous check, and reconciles the repo's own `submission-list.md` against the platform — including rows the platform has moved past, UIDs it has dropped entirely, and drafts that were just submitted.

## Confirm the model switched — first action, before running anything

This skill's `model: sonnet` frontmatter carries the override, so an invocation should already
be running Sonnet. Confirm it took:

```bash
python3 tools/build_model.py require sonnet
```

It must report **OK** naming `claude-sonnet-5`. On **MISMATCH or UNKNOWN, stop immediately**:
report what it printed, ask for `/model sonnet`, and end the turn. Do not call the platform,
do not read `submission-list.md`, and above all do not run the script without `--no-apply` — it
moves rows, archives folders and promotes drafts on its own, so a run under the wrong model is
not a read-only mistake.

The override is adopted at a turn boundary, so a MISMATCH means the switch did not take and
nothing in this turn is running under Sonnet. Never work around the check.

## Run

```bash
python3 .claude/skills/fetch-status/fetch_status.py
```

Run it from the hazy repo root (`/Users/aladdin/projects/snk/hazy`). If invoked elsewhere, use the absolute path: the script resolves history, `submission-list.md`, `submissions/`, `drafts/` and `archived/` relative to its own location, so it works from any cwd.

> **Refinery node not configured.** The production node is set and verified against the
> platform (`Hazy_Task_Creation`). Hazy has no Refinery node configured yet, so the
> refinement chart and `refinement-list.md` are skipped on every run. Set
> `REFINE_PROJECT_ID` in `fetch_status.py` (and below) if and when one is assigned.

The script does everything: calls `stb submissions list -p "cda2e943-8524-45f0-a966-469903337102"`, tallies the Assignment State column, diffs against the last snapshot, appends a new snapshot to `history.jsonl` in this directory, reconciles `submission-list.md` (see below), and prints the report. All timestamps it prints or writes are US Eastern (EST/EDT, follows DST).

Add `--no-apply` to see what it would do to `submission-list.md` and the filesystem without doing it.

## Report

Present the script's output to the user as-is; it is already formatted. Then add a one- or two-line read of what actually moved, for example that a task cleared evaluation into review, that the revision queue grew, or that nothing changed since the last check. Do not restate the numbers the table already shows.

If the report carries an **Updated submission-list.md**, **Rejected and archived**, **Accepted and archived**, or **Promoted from drafts/** section, say so in that read: the script has already made those changes, so there is nothing left to run, but a task that landed on `NEEDS_REVISION` or `REJECTED` still needs its findings appended to that task's `feedback-log.md`, and that is worth naming.

Counts are drawn as a horizontal bar chart, one row per status, bars scaled against the largest count and drawn with partial eighth-blocks so a small state stays visible next to a large one:

```
  Accepted             ████████████████████████  18   .
  Review pending       █████████████▍            10   +1
  Evaluation pending   ██████▋                    5   -1
  Needs revision                                  0   .
  --------------------------------------------------------
  Total                                          33   .
```

Under each chart sits a **Payment** breakdown from the same CLI table, with the line that actually needs acting on:

```
  Payment
  Payout submitted     ████████████              11   .
  Pending              ████████████████████████  22   .
    8 of these are accepted with no payout submitted
```

Payment lags status, so the useful number is not how many are pending overall but how many have **finished the work and are still unpaid** — an accepted submission with no payout submitted. That is the last line, and it is the one to chase.

A payment change with no state change appears in **Movement since then** prefixed `$`:

```
    $ 33 semrad-date-recovery: payment PENDING to PAYOUT_SUBMITTED
```

Snapshots written before payment was tracked have no such field, and the script treats that as *no baseline* rather than as zero, so the first run after this change shows no deltas instead of a full-count jump.

Refinement tasks live on their own project node (`REFINE_PROJECT_ID`, unset on this desk) and, once it is set, get their own chart and their own list file:

```
  Refinements (Hazy-Refinement project)
  Review pending       ████████████████████████   6   .
  Evaluation pending   ████████████████           4   .
  Needs revision       ████                       1   .
  Offered              ████                       1   .
  --------------------------------------------------------
  Total                                          12   .
```

They are submissions on that node, so they carry the same states as ordinary submissions and are charted the same way.

**`refinement-list.md`** at the repo root is **one table**, not one per status — a refinement is addressed by its UID everywhere (`refinements/<uid>/`, and both `/refine-task` and `/revise-refinement` take the UID), so the UID leads and the status is a cell again:

```
| Task UID | Task name | Status | Updated | Note |
|----------|-----------|--------|---------|------|
| a784d07d-... | inbound-consolidation-plan | OFFERED | 2026-09-11 08:59 EDT | inbound-consolidation-plan |
| 0206a5c5-... | skylark-brookstone-proposal | REVIEW_PENDING | 2026-09-11 08:59 EDT | - |
```

Rows are grouped in the `STATUSES` order, then by UID inside each status.

**`Note` is the original task's name when the refinement is of one of ours**, resolved from the refinement's `origin_submission_id` against `submission-list.md`. A `-` means it refines another contributor's submission — which is most of them, so the column is really the "is this my own task" marker. The report ends with the count: `5 of 13 refine one of our own submissions.`

`Task name` comes from `refinements/<uid>/metadata.json`, so a refinement the platform lists but nobody has fetched appears as a row and is reported under **Not fetched yet** with the `/refine-task <uid>` that would fetch it. A row the platform stops listing is reported but **left alone** — refinements have no archive automation, unlike submissions.

If you hold review assignments, a second chart follows for them, from `stb reviews list -p <project>`:

```
  Review assignments (other contributors' tasks, assigned to me)
  To review            ████████████████████████   5   .
  (payment pending)                               5
```

Two states have been seen live: **`OFFERED`** (offered, not yet taken) and **`REVIEW_PENDING`**, labelled *To review*, meaning the assignment is yours and the review is not submitted. The full set is not documented, so any other state the platform returns is charted under its own name rather than being dropped or guessed at. `(payment pending)` counts assignments whose Payment Status is still `PENDING`.

**`REVIEW_PENDING` means opposite things in the two charts.** In the submissions chart it is your task sitting with someone else's reviewer; in the review chart it is someone else's task sitting with you. That is why the labels differ.

A reviews failure never takes the report down: if `stb reviews list` errors or you have no reviewer access, the section is simply absent.

The four states that matter day to day lead — **Accepted, Review pending, Evaluation pending, Needs revision** — followed by any of `OFFERED`, `REJECTED`, `SKIPPED` that actually hold a task, so the bars always reconcile with the total. A state the script does not recognise is listed separately under "Unrecognised states" rather than charted.

Deltas are against the previous recorded run, not a fixed window. If the last check was three days ago, that is the comparison, and the report says so. On the first ever run there is no baseline, so no deltas are shown.

## submission-list.md structure

`submission-list.md` is one table per status. The sections run `## ACCEPTED`, `## REVIEW_PENDING`, `## EVALUATION_PENDING`, `## NEEDS_REVISION`, `## OFFERED`, `## REJECTED` — finished work first, then what is still moving, then what is parked (user instruction 2026-08-26). A status change moves the row into its new section rather than rewriting a cell in place.

Every table carries **Seq | Task name | Taskboard UID | Updated | Model**, where Model is the model that built the task (`metadata.json`'s `built_with`; for an accepted or rejected task the folder is gone, so the value persists in the table and is recovered with `tools/build_model.py attribute` if it is ever lost).

**`NEEDS_REVISION` and `REJECTED` alone add a Note column**, since each is a state where something extra has to be written down: the next action for `NEEDS_REVISION`, and for `REJECTED` why the UID vanished plus its last known payment status. A row that had reached `ACCEPTED` before vanishing did not fail — the platform took it into the refinement pipeline, and it still pays out — so its Note reads `Payout submitted; refinement pipeline`. The payment status is recovered from the prior snapshot, since the vanished UID can no longer be queried directly.

## The three gates, and why REVIEW_PENDING is ambiguous

A task passes three gates before it is accepted:

1. **AutoEval review** - automated checks (`EVALUATION_PENDING`)
2. **Reviewer review** - a human reviewer (`REVIEW_PENDING`)
3. **Adjudication** - final sign-off (**also** `REVIEW_PENDING`)

Adjudication has no Assignment State of its own, so `REVIEW_PENDING` means either "sitting with the reviewer" or "reviewer cleared it, sitting with adjudication". The platform alone cannot tell them apart, and submission-list.md does not try to.

### Every unequal row is submission-list.md falling behind

Any row whose section disagrees with what the platform reports means the platform has moved past it. Since the platform is the source of truth for state, the script **moves the row into the right section** on every run and reports it under **Updated submission-list.md**, stamping Updated with the current time. Common ones:

| submission-list.md section | Platform | Moved to | Reading |
|---|---|---|---|
| `OFFERED` | `EVALUATION_PENDING` | `EVALUATION_PENDING` | Submitted, AutoEval running |
| `NEEDS_REVISION` | `EVALUATION_PENDING` | `EVALUATION_PENDING` | Resubmitted, AutoEval running |
| `NEEDS_REVISION` | `REVIEW_PENDING` | `REVIEW_PENDING` | Resubmitted and cleared AutoEval |
| `EVALUATION_PENDING` | `REVIEW_PENDING` | `REVIEW_PENDING` | Cleared AutoEval, now with the reviewer |
| `REVIEW_PENDING` | `ACCEPTED` | `ACCEPTED` | Accepted |
| `ACCEPTED` | `NEEDS_REVISION` | `NEEDS_REVISION` | It came back after acceptance |

`--no-apply` reports every such move under **submission-list.md is behind the platform on** instead of making any of them.

Two of these are more than a bookkeeping change. A move landing on `NEEDS_REVISION` or `REJECTED` prints a reminder to record the findings and the pending platform actions in that task's `feedback-log.md`; the table holds the status only.

### A UID that vanishes is rejected and archived — or routed to the refinement pipeline

A submission the platform stops listing has left `stb submissions list` for one of two reasons, and vanishing alone cannot tell them apart. The platform's own admin note on some vanished-after-acceptance tasks reads "This task has been sent to the refinement pipeline", not a rejection, and such a task can still pay out (discovered 2026-09-11, after the plain reject-and-archive path destroyed real, paid work by reducing it to `prompt.md`). So the script uses the row's prior status to route:

- **The row had already reached `ACCEPTED`**: it went to the refinement pipeline rather than failing, so its Note records that and its last known payment status. It is archived like any other vanished UID.
- **The row never reached `ACCEPTED`**: a genuine rejection. The row moves to `REJECTED`, stamps Updated, then `submissions/{seq}-{task-name}/` is reduced to just `prompt.md` under `archived/{seq}-{task-name}/`, deleting the rest of the folder (the rubric CSV, zips, metadata.json, feedback-log.md). Reported under **Rejected and archived**.

Both paths run every time and are idempotent — a row already in its target status whose move or archive didn't finish on a prior run gets the same attempt again. `--no-apply` lists what each path would do instead of doing it. If neither an `accepted/` zip, a `submissions/` folder, nor (for the reject path) a `prompt.md` can be found, the script reports the row under **Needs attention** rather than guessing.


### An accepted task is zipped into accepted/ automatically

This runs in both directions. **A row that leaves `ACCEPTED`** — it comes back as `NEEDS_REVISION`, say — has its folder restored: `accepted/{seq}-{task-name}.zip` is unpacked into `submissions/` and the zip removed, reported under **Restored from accepted/**. Without it the zip sat in `accepted/` while the row said otherwise, which is how tasks 04, 10 and 22 drifted (fixed 2026-08-27). `--no-apply` lists these under **Would restore from accepted/**.

Every `ACCEPTED` row whose `submissions/{seq}-{task-name}/` folder still exists gets archived: the whole folder is zipped into `accepted/{seq}-{task-name}.zip` (the folder itself is the zip's top-level directory, matching the hand-built zips already there) and removed from `submissions/`. This covers both a row that landed on `ACCEPTED` this run and one accepted earlier whose archive step never happened. Rows already in their steady state (zip present, no `submissions/` folder) are skipped silently. An `ACCEPTED` row with neither a `submissions/` folder nor a zip is reported under **Needs attention**. `--no-apply` lists the candidates under **Would archive into accepted/** instead of acting.

### A matched draft submission is promoted automatically

A platform submission reporting `OFFERED` or `EVALUATION_PENDING` with no submission-list.md row is checked against every `drafts/{seq}-{task-name}/metadata.json`'s `taskboard_uid`. On a match, the script moves that draft folder to `submissions/{seq}-{task-name}/` and adds a new row (Created = today, Status = whatever the platform reports) under **Promoted from drafts/**. A submission with no matching draft is reported under **Needs attention** as `?` instead — the script never invents a row for one.

The platform is the source of truth for state. Never edit the platform to match submission-list.md; correct submission-list.md.

## When something goes wrong

The script exits non-zero **without** recording a snapshot if the CLI call fails, so a failed run never poisons the next diff with a phantom drop to zero. Common causes:

- **The CLI is out of date.** `stb` version-gates itself: once a newer release ships, every
  command refuses to run with `Error: Version 2.4.8 is outdated (latest: 2.4.9). Please
  upgrade before continuing`. Nothing is wrong with the submission data; upgrade and re-run:

  ```bash
  uv tool upgrade snorkelai-stb \
    --find-links https://snorkel-python-wheels.s3.us-west-2.amazonaws.com/stb/index.html \
    --python ">=3.12"
  ```

  The script detects this case and prints the command for you.
- Not logged in or credentials expired, so run `stb login`
- `stb` missing from PATH; it lives at `~/.local/bin/stb` on this machine

Report the failure and the cause. Do not fabricate counts or reuse the previous snapshot as if it were current.

## State reference

| Status | Gate | Meaning |
|---|---|---|
| `OFFERED` | before 1 | Offer made, task not yet submitted |
| `EVALUATION_PENDING` | 1 | AutoEval checks running |
| `NEEDS_REVISION` | 1 or 2 failed | AutoEval or the reviewer requested changes |
| `REVIEW_PENDING` | 2 or 3 | With the reviewer, or with adjudication |
| `ACCEPTED` | past 3 | Adjudication complete |
| `REJECTED` | - | Task rejected |

`submission-list.md` uses these as its section headings; they mirror the platform's own Assignment States, though the sections are ordered for reading rather than by pipeline position. `/fetch-status` keeps the file in sync automatically; anything it cannot infer on its own is corrected by hand-editing the table directly.
