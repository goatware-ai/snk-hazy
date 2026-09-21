---
name: revise-task-opus
description: Revise a Hazy task under Opus 5. Invoked by /revise-task; do not call directly.
model: opus
user-invocable: false
---

# Revise the task under Opus 5

You are running under the `claude-opus-5` family (`tools/build_model.py current` prints `claude-opus-5`, context-window suffixes ignored). This skill's argument is the Taskboard UID.

## 1. Confirm the model actually switched

The model override this skill carries is adopted at a turn boundary, so verify it took:

```bash
python3 tools/build_model.py check $(python3 tools/build_model.py uid <uid>)
```

It must report **OK**. On MISMATCH, **stop before touching anything** and tell me to run
`/model opus` and re-invoke the command. Never work around the check and never edit
`built_with` to match the model you happen to be.

## 2. Do the work

Read `prompts/revise-task.md` in full and follow it; this skill has verified the model, so its
model step is already done. Its first two steps are the whole of this turn: verify the folder, then stop and ask me
for the feedback.
