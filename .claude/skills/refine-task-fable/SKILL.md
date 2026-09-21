---
name: refine-task-fable
description: Refine a Hazy-Refinement task under Fable. Invoked by /refine-task; do not call directly.
model: fable
user-invocable: false
---

# Refine the task under Fable

You are running under the `claude-fable-5` family (`tools/build_model.py current` prints `claude-fable-5` or a point release such as `claude-fable-5-1`; `require` and `check` fold both to the family). This skill's argument is the refinement task UID.

## 1. Confirm the model actually switched

The model override this skill carries is adopted at a turn boundary, so verify it took:

```bash
python3 tools/build_model.py require fable
```

It must report **OK**. On MISMATCH, **stop before touching anything** and tell me to run
`/model fable` and re-invoke the command. Never work around the check and never edit
`built_with` to match the model you happen to be.

## 2. Do the work

Read `prompts/refine-task.md` in full and follow it; this skill has verified the model, so its
model step is already done. End with the deliverables block that prompt specifies and stop; the stamp command is
its last step.
