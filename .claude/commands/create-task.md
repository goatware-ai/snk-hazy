---
description: Build N accept-on-submit Hazy draft tasks under a chosen model (0 = Fable, 1 = Opus)
argument-hint: [count] [0=fable|1=opus]
model: inherit
---

## Arguments

- `$1`: how many tasks to build. Empty, missing, or not a positive integer: build **1**.
- `$2`: which model builds them: **`0` = Fable**, **`1` = Opus 5**. Empty: whichever model is
  already running this session (`python3 tools/build_model.py current`).

## Route to that model, and do nothing else this turn

This command cannot switch its own model, so it hands the build to the skill that carries the
model override:

- `$2` is `0`: invoke the skill **`create-task-fable`** with `$1` as its arguments.
- `$2` is `1`: invoke the skill **`create-task-opus`** with `$1` as its arguments.
- `$2` is empty: invoke whichever of the two matches `build_model.py current`.
- `$2` is anything else: stop and say the model flag is `0` (Fable) or `1` (Opus).

**Invoke the skill and stop.** Do not read the docs, design a task, or touch a file in this
turn: the override is adopted at the turn boundary, so the build has to begin in the turn
*after* the routing, or it runs under the old model and gets stamped wrong. The skill verifies
the switch before it builds.

## What the skill then does

Builds `$1` tasks one at a time into `drafts/{seq}-{task-name}/` per
`prompts/create-task-brief.md` and `prompts/submission.md`, and records the building model in
each task's `metadata.json` (`built_with`). At the start of each task it sets the session title
to that task's folder:

```bash
printf '\033]0;%s\007' "drafts/{seq}-{task-name}" > /dev/tty 2>/dev/null || true
```

If the title cannot be set, it says nothing and carries on. Drafts carry no Taskboard UID, get
no `submission-list.md` row, and are gitignored; promoting one into `submissions/` is mine to do
by hand.
