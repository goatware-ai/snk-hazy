---
name: create-task-opus
description: Build Hazy draft tasks under Opus 5. Invoked by /create-task; do not call directly.
model: opus
user-invocable: false
---

# Build the batch under Opus 5

You are running under the `claude-opus-5` family (`tools/build_model.py current` prints `claude-opus-5`, context-window suffixes ignored). The count of tasks to build arrives as this skill's arguments (default 1 if empty).

## 1. Confirm the model actually switched

The model override this skill carries is adopted at a turn boundary, so verify it took:

```bash
python3 tools/build_model.py require opus
```

It must report **OK**. On MISMATCH, **stop before touching anything** and tell me to run
`/model opus` and re-invoke the command. Never work around the check and never edit
`built_with` to match the model you happen to be.

## 2. Do the work

Read `prompts/create-task-brief.md` and `prompts/submission.md` in full and follow them; this skill has verified the model, so its
model step is already done. When a task is otherwise final, stamp it:

```bash
python3 tools/build_model.py stamp drafts/{seq}-{task-name}
```
