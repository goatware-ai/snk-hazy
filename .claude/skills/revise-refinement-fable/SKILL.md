---
name: revise-refinement-fable
description: Revise an already-fetched Hazy refinement under Fable. Invoked by /revise-refinement; do not call directly.
model: fable
user-invocable: false
---

# Revise the refinement under Fable

You are running under the `claude-fable-5` family (`tools/build_model.py current` prints `claude-fable-5` or a point release such as `claude-fable-5-1`; `require` and `check` fold both to the family). This skill's argument is the refinement task UID.

## 1. Confirm the model actually switched

The model override this skill carries is adopted at a turn boundary, so verify it took:

```bash
python3 tools/build_model.py check refinements/<uid>
```

It must report **OK**. On MISMATCH, **stop before touching anything** and tell me to run
`/model fable` and re-invoke the command. Never work around the check and never edit
`built_with` to match the model you happen to be.

On MISSING, stop and ask me which model did the earlier round; do not infer it and do not stamp
a guess.

## 2. Do the work

Read `prompts/revise-refinement.md` in full and follow it; this skill has verified the model, so its
model step is already done. Its first two steps are the whole of this turn: verify the folder, then stop and ask me
for the feedback.
