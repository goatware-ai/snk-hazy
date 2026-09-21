# Brief: build a batch of Hazy draft tasks

Read this together with `prompts/submission.md`, which carries the build rules, the folder
layout and the Package sequence. This file states only where a batch of drafts differs.

**How many:** the count passed to the invoking skill (default 1).

**Target folder:** `drafts/{seq}-{task-name}/`, never `submissions/`. The layout is the one
`prompts/submission.md` specifies; the rubric stays `rubric-{task-name}.csv` because a draft has
no UID. `drafts/` is gitignored; do not `git add` it.

Build them **strictly one at a time**: task 1 is finished and verified (every file on disk,
both zips built, `autoeval_check.py` at 0 errors, its report printed) before any work on task 2
begins. Never plan, design or build several tasks concurrently, and never spawn subagents to
parallelise them; each task is only distinct if it is designed with the earlier ones already
finished on disk in front of you. Set the session title to each task's folder name as you start
it, with the command in `.claude/commands/create-task.md`.

## What a draft does not have

- **No `submission-list.md` row.** It is owned by `/fetch-status`, covers submitted tasks only,
  and promotes a draft on its own once the draft's `metadata.json` UID matches a live submission.
- **No Taskboard UID.** Leave `"taskboard_uid": null`; a null UID is what marks a folder as
  unsubmitted. Do not invent, request or fill one.
- **No promotion.** Stop at the finished draft; moving a folder into `submissions/` is the
  operator's step.

## What a draft records

- `feedback-log.md` opens with one build entry, `{today} · source: build · verdict: DRAFT`, no
  UID line, naming the model that built it (the value `tools/build_model.py current` prints).
- **The building model**, as the last step once the folder is otherwise final:

  ```bash
  python3 tools/build_model.py stamp drafts/{seq}-{task-name}
  ```

  It writes `built_with` into `metadata.json` from the session transcript. Local bookkeeping
  only, never part of the platform form; `/revise-task` routes a revision back to that model,
  so a batch is only worth building under the model you intend to maintain it with.

## Uniqueness across the batch

The uniqueness gate (U1, U2) runs against `submissions/`, `accepted/`, `archived/` **and every
draft already built in this session**, including the ones built minutes ago. Two drafts from one
batch sharing a reasoning path is the most likely failure: read the existing
`drafts/*/prompt.md` before designing each new one and pick a different core workflow if
anything is close.

## Per-task verification

Each task clears the full gate before you move on: run the Package sequence
(`prompts/submission.md`) with `{target}` set to `drafts`, `clause-map.md` and `verify_golden.py`
written in the draft folder first (R134, G43), ending in `autoeval_check.py` at 0
errors on the packaged files.

## Reporting

Follow the "do not narrate" rule while working. After **each** task finishes, print that task's
deliverables block (file tree, `unzip -l` for both zips, the prompt in one fenced block, the
rubric in one fenced block, the metadata block), then start the next. When the batch is done,
print one closing list of the draft folders built and anything genuinely broken or unresolved in
any of them; if nothing is broken, say nothing beyond the list.
