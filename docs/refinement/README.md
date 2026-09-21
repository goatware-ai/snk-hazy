# Refinement

> **Inherited from the Geranium desk, not confirmed for Hazy.** This document describes
> the refinement (Refinery) loop. Hazy has no Refinery node, and no refinement
> assignment has been seen. It is kept for reference and was NOT updated in the 2026-09-21 port; treat
> anything it says about sector, rubric bands or platform checks as Geranium's, not
> this project's. See `../RULE-DELTAS.md`.

Documentation for **Hazy Refinery** (platform node: *Hazy-Refinement*): previously
completed tasks that come back needing targeted fixes to their prompt, inputs, golden
solution, or rubrics. Tiered payment on acceptance.

`platform/` holds pages captured verbatim from Snorkel's own guidelines. **Those captures
are authoritative** — on any conflict with a workflow page, a tool, or anything else in
this repo, the capture wins.

## Layout

```
refinement/
├── README.md                          ← this file
└── platform/
    └── submission-guidelines.md       the Refinery submission page, step by step (2026-09-10)
```

## Run it

```
/refine-task <task-uid> [0=fable|1=opus]
```

The command routes to `refine-task-fable` / `refine-task-opus`, which follow
`prompts/refine-task.md`. The task is fetched by `tools/fetch_refinement.py` into
`refinements/<uid>/` (one flat folder; the hand-over survives as `original-prompt.md` and `feedback.md`)
and `refinements/<uid>/` (the revision, in submission-folder shape so the whole gate
runs on it, plus `change.log` recording what changed and `review-comment.md` carrying the Section 3 paragraph; tracked). The run ends with the completed
prompt, rubric, inputs and golden ready to enter, plus the Section 3 change summary the form
requires.

## Our own tasks in the pipeline

## The loop in one paragraph

Open the task, download the inputs and golden from the right panel, read the whole
**Feedback to Improve Task** field on the left (Correction Feedback, failed AutoEvals,
evaluations not yet run), fix exactly what it asks for, re-upload inputs and golden as
zips, paste every rubric criterion from the left panel into the right-panel textboxes with
the requested edits applied, and submit. The task reruns every in-platform evaluation, then
goes to a reviewer who confirms the required changes were made.

## Rules that bite

- **Do not touch the prompt unless the feedback asks for it.** The capture says this twice.
- **Input file names are frozen.** Modify contents if required, but re-zip under the same
  per-file names.
- **Run the Input Files Quality Check and Prompt Quality Check** before moving to Section 2.
- **Rubric criteria must be re-entered by hand.** The right-panel criterion textboxes start
  empty; copy each criterion from the left panel, then apply the feedback's edits.
- **Evaluations "not yet run" still gate acceptance.** Treat the listed checks (e.g.
  `GOLDEN_SOLUTION_LEAKAGE_CHECK`) as if they had already failed and pre-clear them.
- **Every checker a submission runs, runs here.** The refined folder is in submission
  shape on purpose: `autoeval_check.py` (whole catalog), `rubric_lint.py`, `prompt_check.py`,
  `audit_task.py`, `fix_floats.py scan`, `fix_metadata.py`, `package_sweep.py` all run on
  `refinements/<uid>` to zero errors before the round is called done, and the golden
  is scored against the final rubric criterion by criterion in `change.log`.
- **A failed AutoEval is a hard block.** The task cannot be accepted until that check passes
  on resubmission. Note the "Hazy" project-name leakage preflight is a deterministic
  hard fail on the Dataset Quality Check.

## Related

- `../submission/platform/auto-eval-feedback-guide.md` — how to read each AutoEval and rebut
  a flag.
- `../submission/platform/platform-submission-form.md` — field limits that still apply
  (500-char criteria, weight bands, 3,000-char prompt).
