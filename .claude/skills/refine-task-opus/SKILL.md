---
name: refine-task-opus
description: Refine a Hazy-Refinement task under Opus 5. Invoked by /refine-task; do not call directly.
model: opus
user-invocable: false
---

# Refine the task under Opus 5

You are running under the `claude-opus-5` family (`tools/build_model.py current` prints `claude-opus-5`, context-window suffixes ignored). This skill's argument is the refinement task UID.

## 1. Confirm the model actually switched

The model override this skill carries is adopted at a turn boundary, so verify it took:

```bash
python3 tools/build_model.py require opus
```

It must report **OK**. On MISMATCH, **stop before touching anything** and tell me to run
`/model opus` and re-invoke the command. Never work around the check and never edit
`built_with` to match the model you happen to be.

## 2. Do the work

Read `prompts/refine-task.md` in full and follow it; this skill has verified the model, so its
model step is already done. End with the deliverables block that prompt specifies and stop; the stamp command is
its last step.
