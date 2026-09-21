---
name: revise-refinement-opus
description: Revise an already-fetched Hazy refinement under Opus 5. Invoked by /revise-refinement; do not call directly.
model: opus
user-invocable: false
---

# Revise the refinement under Opus 5

You are running under the `claude-opus-5` family (`tools/build_model.py current` prints `claude-opus-5`, context-window suffixes ignored). This skill's argument is the refinement task UID.

## 1. Confirm the model actually switched

The model override this skill carries is adopted at a turn boundary, so verify it took:

```bash
python3 tools/build_model.py check refinements/<uid>
```

It must report **OK**. On MISMATCH, **stop before touching anything** and tell me to run
`/model opus` and re-invoke the command. Never work around the check and never edit
`built_with` to match the model you happen to be.

On MISSING, stop and ask me which model did the earlier round; do not infer it and do not stamp
a guess.

## 2. Do the work

Read `prompts/revise-refinement.md` in full and follow it; this skill has verified the model, so its
model step is already done. Its first two steps are the whole of this turn: verify the folder, then stop and ask me
for the feedback.
