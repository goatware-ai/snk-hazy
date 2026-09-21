---
description: Refine a Hazy-Refinement task from its UID, under a chosen model (0 = Fable, 1 = Opus)
argument-hint: <task-uid> [0=fable|1=opus]
model: inherit
---

## Arguments

- `$1`: the refinement task UID (the submission id on the Hazy-Refinement node). Missing:
  stop and ask for one; this command refines exactly one identified task.
- `$2`: which model does the work: **`0` = Fable**, **`1` = Opus 5**. Empty: if
  `refinements/$1/metadata.json` exists and carries `built_with`, the model recorded
  there (a later round goes back to the model that did the first); otherwise whichever model is
  already running this session (`python3 tools/build_model.py current`).

## Session setup

First action, before reading anything else, set the session title to the UID:

```bash
printf '\033]0;%s\007' "$1" > /dev/tty 2>/dev/null || true
```

If the title cannot be set, say nothing about it and carry on.

## Route to that model, and do nothing else this turn

- resolved model is Fable: invoke the skill **`refine-task-fable`** with `$1` as its argument.
- resolved model is Opus: invoke the skill **`refine-task-opus`** with `$1` as its argument.
- `$2` is anything else: stop and say the model flag is `0` (Fable) or `1` (Opus).

**Invoke the skill and stop.** Do not fetch, read, diagnose or edit anything in this turn: the
model override is adopted at the turn boundary, so the refinement has to begin in the turn
*after* the routing. The skill verifies the model before it touches anything.

## What the skill then does

Follows `prompts/refine-task.md` end to end: fetches the task with `tools/fetch_refinement.py`
into `refinements/$1/` as one flat folder (the hand-over survives as `original-prompt.md` and
`feedback.md`, beside the tracked revision with its `change.log` and `review-comment.md`), reads
the platform's feedback panel, diagnoses each item to its root cause, revises within the platform's
frozen-name rules, runs the Package sequence to zero errors, scores the golden against the
final rubric criterion by criterion, logs the round, stamps `built_with`, and returns the
completed artifacts ready to enter.
