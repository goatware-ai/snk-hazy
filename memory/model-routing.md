---
name: model-routing
description: "Sessions in this repo run on Opus 5 by default (user, 2026-08-24); each task's metadata.json built_with pins the model its revisions run under (Geranium's 01-11 fable / 12-onward split did not port, Hazy starts empty); tools/build_model.py current/attribute/stamp/check/require/read/resolve/uid; slash commands route through per-model skills because a command cannot switch its own model; /review-task pinned to opus, /fetch-status to sonnet"
metadata:
  type: user
---

**Session default: Opus 5** (`claude-opus-5`). The user set it with `/model default` on 2026-08-24
and asked for it "forever"; treat Opus as the standing default. A model cannot switch itself, so
if a session is not on Opus, say so and let the user run `/model`; do not silently proceed on a
smaller model for substantive work, and do not pass a cheaper `model:` override to subagents
unless asked.

**Build attribution is separate from the session default.** Every task folder records its
builder in `metadata.json`'s `built_with` ([[task-metadata]]), and revisions run under that same
model: a Fable-built task is revised under Fable via the per-model skills whatever the session
default. The 01-11 fable / 12-onward opus split is Geranium's catalog, which did not come across
in the 2026-09-21 port; Hazy starts empty, so `built_with` is whatever the first builds stamp. Only two models author here: **Fable = flag `0`, Opus 5 =
flag `1`**. An archived folder is reduced to prompt.md and has no metadata, so its model lives in
submission-list.md's Model column and is recoverable with `attribute`.

**`tools/build_model.py`** owns both records:

- `current` reads `$CLAUDE_CODE_SESSION_ID` and pulls the model from that session's transcript at
  `~/.claude/projects/-Users-aladdin-projects-snk-hazy/<sid>.jsonl`; the model id is recorded
  per assistant message, so this is ground truth rather than self-report.
- `attribute` recovers the builder of any past task by scanning transcripts for turns that WROTE
  the folder (plain mentions credited the reader; uniqueness diffing opens archived prompts and
  flipped task 11 to the wrong model until the filter went in).
- `stamp <folder> [--infer]` writes `built_with`; `check <folder>` exits non-zero when the running
  model differs from it; `require <model>` exits non-zero unless THIS session is that model;
  `read`, `resolve <0|1>` and `uid <taskboard-uid>` are the lookups the command files use.

**A slash command cannot switch its own model.** The `model:` frontmatter is static and an
override is adopted at a turn boundary, so `/create-task`, `/revise-task`, `/refine-task` and
`/revise-refinement` are thin routers: resolve the model, invoke the per-model skill
(`.claude/skills/<command>-{fable,opus}/`, each `user-invocable: false` with a `model:` override),
and do nothing else that turn. Each skill re-checks `build_model.py current` before working and
stops if the switch did not take. `/review-task` carries `model: opus` in its command frontmatter
(user, 2026-09-01): one review path, no per-model variants, because nothing on the platform form
records the reviewing model; leave that line alone unless asked. `/fetch-status` runs under
Sonnet (`model: sonnet` in the skill frontmatter, then `require sonnet`, stopping on MISMATCH
because the script writes to submission-list.md, [[submission-tracking]]).

- 2026-09-14 (twincreek-bid-worksheet refinement 1d928008, round 3): the operator may re-assign a refinement to another model ("please use opus, please change the metadata"). On that explicit direction, re-stamp with `tools/build_model.py stamp <folder>` from the new session (it also rewrites build_session), confirm `check` reports OK, and record the switch in change.log; without it the MISMATCH stop stands.

- 2026-09-15 (pick-module-reslot, task 44): the operator switched a submitted TASK to Opus mid-revision ("please continue with this model"). The refinement rule applies unchanged: stamp, confirm check reports OK, record the switch in the task's feedback-log.md, and update the model column in submission-list.md.

- 2026-09-17 (rademacher-service-review, task 20, submitted task in NEEDS_REVISION since 2026-08-26): the operator re-assigned a task from Opus 5 to Fable ("please work with fable") to modernize it against the current gates. Same procedure as pick-module-reslot: stamp from the new session, check OK, the switch logged in feedback-log.md, the Model column in submission-list.md updated, and .model-name rewritten to match built_with.
