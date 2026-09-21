---
description: Revise an already-fetched Hazy refinement, under the same model that refined it
argument-hint: <task-uid>
model: inherit
---
> **INHERITED FROM GERANIUM, NOT VERIFIED FOR HAZY.** Hazy has no Refinery node, so there is no fetched refinement for this command to revise. The procedure below
> still describes Geranium's Wholesale Trade rules and was not updated in the
> 2026-09-21 port. See `docs/RULE-DELTAS.md` D12.


## Session setup

**Refinement task UID for this revision:** `$1`

First action of this session, before reading anything else, set the session title to that UID:

```bash
printf '\033]0;%s\007' "$1" > /dev/tty 2>/dev/null || true
```

If the title cannot be set, say nothing about it and carry on. If no UID was passed, stop and
ask for one; this command revises exactly one identified refinement.

## Find the folder and the model that refined it

A refinement is addressed by its UID directly; there is no index to resolve it through.

```bash
ls -la refinements/$1                              # the tracked revision
python3 tools/build_model.py read refinements/$1   # its metadata.json built_with
```

If `refinements/$1` does not exist, **stop** and say the refinement has not been fetched
yet, and that `/refine-task $1` is the command that fetches and does round 1. Never create the
folder here.

If `read` finds nothing, stop and ask which model did the earlier round rather than guessing: a
refinement carries no transcript-recoverable history the way a task folder does.

## Route to that model, and do nothing else this turn

A refinement is revised by the model that refined it, for the same reason a task is revised by
the model that built it: the golden, the rubric wording and the input fabric were one model's
interlocking judgment calls, and the earlier round's reasoning in `change.log` is
extended coherently only by its author.

- `built_with` is a `claude-fable-*` id: invoke the skill **`revise-refinement-fable`**.
- `built_with` is a `claude-opus-*` id: invoke the skill **`revise-refinement-opus`**.

Pass the UID through as the skill's argument. Feedback is never passed on the command line; I
supply it when the skill stops and asks, and nothing is fetched from the platform (see
`prompts/revise-refinement.md`).

**Invoke the skill and stop.** Do not read the refinement files, diagnose, or edit anything in
this turn: the model override is adopted at the turn boundary, so the revision has to begin in
the turn *after* the routing. The skill verifies the model before it touches anything.

## How this differs from `/refine-task`

`/refine-task <uid>` is round 1: it fetches the hand-over and stages `refinements/<uid>/`
from it. `/revise-refinement <uid>` is every round after that: the
folder already exists, nothing is fetched, and the work is driven by feedback I paste.
