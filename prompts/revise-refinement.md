# Prompt: revise a refinement based on new feedback

> **Inherited from the Geranium desk, not ported to Hazy, and unverified.** It is a later round
> of `prompts/refine-task.md`, and Hazy has no Refinery node and no refinement assignment, so the
> refinement workflow does not exist here yet (delta D12). Everything below was written for the
> Wholesale Trade sector and the single-sector rules that went with it, neither of which Hazy
> has, and none of it has been checked against Hazy's own platform. Do not treat a rule in it as
> current until a refinement assignment confirms the workflow exists.

- **Refinement task UID:** {TASK_UID}
- **Feedback owner:** {AutoEval | Reviewer}
- **Feedback:** {paste the full feedback text / verdict / scores below}

---

**Scope, hard limit:** only `refinements/{TASK_UID}/` may be modified. Never edit
`original-prompt.md` or `feedback.md` inside it: those two are the platform's hand-over, kept
verbatim as the fixed point this round is read against. Never touch another refinement or a task folder under
`submissions/` or `drafts/`, even if a check surfaces the same defect there; report it instead.

**No `stb` CLI, hard limit:** never run any `stb` command, and never run
`tools/fetch_refinement.py`: that fetcher belongs to `/refine-task` and would move the baseline
mid-revision. Everything from the platform arrives pasted by the operator; when you need a live
part, ask.

**What is frozen stays frozen.** This is a later round of the same refinement, so every
platform rule in `prompts/refine-task.md` still binds: input file names, the deliverable name,
and the prompt unless the feedback names it or a check it faces fails on it. Read that prompt's
"What the submission rules still require of a refinement" table before changing anything.

## Steps

1. **Locate and verify the refinement.** The folder is `refinements/{TASK_UID}/`,
   addressed by UID directly. Confirm it exists and that its `metadata.json` carries that UID;
   if it does not exist, stop and say the refinement has not been fetched and that
   `/refine-task {TASK_UID}` is round 1. The invoking skill has already verified that the model
   running now is the one recorded in `built_with`.

   Read `change.log` before anything else: it records what the earlier round changed
   and, under "Not changed, and why", what it deliberately left alone. A finding that reappears
   may be one this log already answered, in which case the question is whether that reasoning
   survives the new feedback, not whether to patch it.

2. **Stop and ask for the feedback.** End the turn: report the folder, the recorded model, the
   round the change log is on and the gate result, then ask for the feedback: owner (AutoEval
   or Reviewer) and the full text, verdicts and scores, plus any live part the platform may now
   hold.

3 to 8. **Same as `prompts/revise-task.md` steps 3 to 8, with these substitutions:**

- The files are `prompt.md`, `rubric-{task-name}.csv`,
  `feedback-log.md` and `change.log`; the Package sequence runs on the folder
  and the package sweep is fixed only for **this** refinement.
- In step 3, say for each item whether it is **new** or a **repeat** of something the earlier
  round addressed; a repeat means the earlier fix did not land, and that is what to diagnose.
- In step 4, every edit stays inside the frozen-name rules; a row that fails and cannot be fixed
  inside them goes into `change.log` under "Not changed, and why".
- In step 5, a one-off is recorded in `change.log`, not the feedback log.
- `clause-map.md`, `struck-phrases.md` and `verify_golden.py` sit in the refinement folder root
  beside `change.log`, outside both zips; steps 3, 4 and 6 apply to them unchanged, and the round
  counts returns from `feedback-log.md` for PR19 the same way, the hand-over panel included.
- In step 6, after the gate, score the golden against the final rubric criterion by criterion
  and confirm it lands ~100.
- In step 7, append a new round section to `change.log` (date, round number, feedback
  category, one entry per item with root cause and change, and for a repeat why the earlier
  fix did not hold, the "Not changed, and why" list, the golden-versus-rubric table) and the
  round's entry to `feedback-log.md`. `review-comment.md` (the form's Section 3
  paragraph) is rewritten **only** when the feedback owner is a Reviewer; on AutoEval feedback
  it is left exactly as it stands. A refinement has no `submission-list.md` row.
- In step 8, the summary also says which items were new and which repeats, the golden's score,
  and "no Section 3 change" on AutoEval feedback.
