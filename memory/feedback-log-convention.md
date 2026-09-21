---
name: feedback-log-convention
description: "Every task folder keeps feedback-log.md (inside the accepted/ zip once accepted); each feedback entry also adds or tightens a coded check whose FIRST DOCSTRING LINE is the canonical rule, then `autoeval_check.py --rules` regenerates docs/rules.md and memory gets one dated line (registry flow since 2026-09-11); feedback for one task changes that task only"
metadata:
  type: feedback
---

Each task folder carries `feedback-log.md` (user instruction 2026-08-18). Entry format,
appended chronologically (oldest first):

```
## YYYY-MM-DD · Reviewer | Auto-eval · <check name> · <verdict>
**Findings** (numbered, as given)
**Actions taken** (what was changed, with dates)
**Form actions** (what the user must re-upload / re-enter)
```

**Why:** feedback was scattered across chat sessions; the user wants a per-task paper
trail that survives sessions - auto-eval check failures AND reviewer send-backs both go in.

**How to apply:** whenever the user relays feedback for a task UID, append the entry to
that task's log as part of handling it (and create the log if missing). Accepted tasks keep their
log INSIDE `accepted/{seq}-{name}.zip` (the whole folder is zipped by /fetch-status, see
[[submission-tracking]]); a task leaving ACCEPTED is unzipped back with its log. New tasks get the file at
build time with an empty-log placeholder. `prompts/submission.md`'s folder spec lists it.
Exception (user instruction 2026-08-18): RETIRED tasks are stripped to prompt.md only,
moved to `archived/{seq}-{task-name}/` - log, inputs, solution, zips, metadata deleted.

**Gate must learn from every AutoEval feedback (user instruction 2026-08-19):** handling
AutoEval feedback is not done until the check module under `tools/gcheck/` (see
[[repo-layout-and-tooling]]; `tools/rubric_lint.py` for oracle-wording rules) is updated to catch the newly observed failure class - add or
tighten a check when a new pattern appears, and fix the check when feedback proves a rule
wrong or a threshold off (false positive/negative). Then re-run the gate portfolio-wide
and record the tool change in the task's log entry alongside the content fixes. Checks
too fuzzy to automate go in the tool's "still manual" docstring list instead.
**Feedback for one task changes that task only (user instruction 2026-08-20):** when
feedback arrives for a task UID, edit and log that task's files and nothing else. The
portfolio gate run stays diagnostic: report what it finds in other tasks in chat, leave
their prompt, inputs, solution, rubric, log and `submission-list.md` row untouched, and fix each
one when its own feedback round comes (the gate keeps flagging them until then). The
user reverted a same-day rubric sweep across three tasks on 2026-08-20 and asked
for this separation twice: first for the logs, then for the file changes, and a THIRD time
the same day after one R18 sweep touched five task folders at once. The rule means: run the checker over everything,
never edit what it flags elsewhere. Check `git status` before touching any file outside the
task in hand.

**Tightened 2026-08-22:** the diagnostic portfolio run is now off too. After one task was
sent back I ran the new originality and authorship gates across the catalogue and reported
in chat that every task folder failed them; the user retired that task and said not to make
that kind of review on other tasks again. So: still code every lesson into the gate, but
re-run it on the task in hand, named explicitly, and do not report verdicts on other
folders. `tools/originality_check.py` has no catalogue-wide mode for this reason.

**Registry flow (repo-wide cleanup, 2026-09-11):** a rule lives in exactly one place, the
check's docstring in `tools/gcheck/`, whose first line is the canonical one-sentence
statement (then optional `Since:`, `Source:`, `Drift-notes:` lines). `autoeval_check.py
--selfcheck` fails on a registered check without one or on an emitted code it does not
declare, and runs before every gate. `autoeval_check.py --rules` regenerates `docs/rules.md`
(stage, family, code, statement); uncoded procedural rules sit in `tools/gcheck/procedural.py`
as PR-ids so they appear there too. Handling feedback is therefore: log entry in the task's
feedback-log.md, then the check (new or tightened, docstring first), then `--rules`, then ONE
dated line in the owning memory topic file citing the id, then prompts and docs cite the id.
Never restate a rule in words in more than one layer: the 2026-09-11 audit found 4 to 9
wordings per rule and five that contradicted the gate (R67, R81, R24, P2/P5, revision count).
Dated per-task narrative stays in that task's own `feedback-log.md`, never in a rule file or a
prompt template.

Related: [[repo-layout-and-tooling]], [[rubric-anchoring-and-landing]],
[[gate-scope-single-task]].
