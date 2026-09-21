---
description: Revise a submitted Hazy task, under the same model that built it
argument-hint: <task-uid>
model: inherit
---

## Session setup

**Task UID for this revision:** `$1`

First action of this session, before reading anything else, set the session title to that UID:

```bash
printf '\033]0;%s\007' "$1" > /dev/tty 2>/dev/null || true
```

If the title cannot be set, say nothing about it and carry on. If no UID was passed, stop and
ask for one; this command revises exactly one identified task.

## Find the task and the model that built it

```bash
python3 tools/build_model.py uid "$1"        # UID -> submissions/{NN}-{task-name}
python3 tools/build_model.py read <folder>   # that folder's metadata.json built_with
```

If `uid` finds nothing, stop and say the UID is not in `submission-list.md`.

If `read` finds nothing (a task built before the model was recorded), recover the builder from
the session transcripts and carry on:

```bash
python3 tools/build_model.py stamp <folder> --infer
```

## Route to that model, and do nothing else this turn

A task is revised by the model that built it: the golden solution, the rubric wording and the
input fabric were one model's interlocking judgment calls, and a different model re-deciding a
slice of them leaves the artifacts disagreeing with each other.

- `built_with` is a `claude-fable-*` id: invoke the skill **`revise-task-fable`**.
- `built_with` is a `claude-opus-*` id: invoke the skill **`revise-task-opus`**.

Pass the UID through as the skill's argument. Feedback is never passed on the command line; I
supply it when the skill stops and asks, and nothing is fetched from the platform (see
`prompts/revise-task.md`).

**Invoke the skill and stop.** Do not read the task files, diagnose, or edit anything in this
turn: the model override is adopted at the turn boundary, so the revision has to begin in the
turn *after* the routing. The skill verifies the model before it touches anything.
