---
name: revise-task-fable
description: Revise a Hazy task under Fable. Invoked by /revise-task; do not call directly.
model: fable
user-invocable: false
---

# Revise the task under Fable

You are running under the `claude-fable-5` family (`tools/build_model.py current` prints `claude-fable-5` or a point release such as `claude-fable-5-1`; `require` and `check` fold both to the family). This skill's argument is the Taskboard UID.

## 1. Confirm the model actually switched

The model override this skill carries is adopted at a turn boundary, so verify it took:

```bash
python3 tools/build_model.py check $(python3 tools/build_model.py uid <uid>)
```

It must report **OK**. On MISMATCH, **stop before touching anything** and tell me to run
`/model fable` and re-invoke the command. Never work around the check and never edit
`built_with` to match the model you happen to be.

## 2. Do the work

Read `prompts/revise-task.md` in full and follow it; this skill has verified the model, so its
model step is already done.

Do not ask me for the feedback. Step 2 fetches it:

```bash
.venv/bin/python tools/fetch_feedback.py <uid>
```

That writes `feedback-<uid8>.md` into the task folder and prints it, including a comparison of
what the platform holds against what the folder holds. Read it, then carry straight on into
the diagnosis. Stop and ask only if the fetch fails, if no folder carries the UID, or if the
report leaves a finding genuinely ambiguous.
