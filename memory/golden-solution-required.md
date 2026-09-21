---
name: golden-solution-required
description: "The D0 conflict on Hazy: the Create the Task guidelines PDF says three times that the task creator does NOT produce a solution, while the live form carries a REQUIRED Completed Task Upload and builds the rubric off it. The form wins because it is what blocks submission, so this desk builds a golden solution for every task and keeps all golden-solution tooling. Open whenever a doc, prompt or session says no solution is needed"
metadata:
  type: project
---

Open the moment anything says the creator does not produce a solution. It is wrong, and the
mistake is expensive: the form cannot be submitted without the upload, and the rubric has nothing
to be derived from.

**The conflict (recorded 2026-09-21).**

The guidelines PDF (`docs/submission/platform/create-the-task-guidelines.md`) says it three times:

- "Expert 1 creates a new task (including task instruction, input files, and rubric). Do not
  complete the task in this workflow. Another expert will complete the task you create."
- "Your role in this workflow is to author the task package, not to produce a gold-standard
  solution."
- Before Submitting: "You have not uploaded a reference output or completed solution in this
  task-creation workflow."

The live form (`docs/submission/platform/platform-submission-form.md`) contradicts all three. Its
section 3 carries a **required** `Completed Task Upload` under this text: "Now that you've updated
your Task Instruction and Input Files, **complete the task yourself** ... **This is your ground
truth and what you will build your rubric off of.**" Section 3 also requires an Output File List
whose names must match the upload exactly.

**The rule: the form wins.** It is what blocks submission, and two other form rules only make
sense if the solution exists: "Pull every exact value straight from your own reference files and
ground-truth answer, never estimate what a criterion should check", and checklist item 13,
"Nothing in my rubric asserts a fact that isn't actually derivable from the input files I'm
providing."

**How to apply.**

- Build a golden solution for every task. All the golden-solution tooling and rules stay in
  force: [[golden-fidelity]], `tools/golden_verify.py`, `verify_golden.py` at task-folder root.
- The rubric is derived from the golden, never from the prompt. Every pinned value is read off the
  golden and traced back to an input.
- A doc sentence claiming no solution is produced gets **corrected with a pointer to this file**,
  not deleted. The guidelines capture is verbatim platform material and is left as captured, with
  the conflict noted in its own section 0.
- The solution zip is still `s-{task-name}.zip` and is still one of the platform's four
  independent parts ([[repo-layout-and-tooling]], [[revision-workflow]]).
- Raise the contradiction with the project if it ever costs a cycle. Until a project answer
  arrives, the form is authoritative.

**This is the general rule, not a one-off.** Where the guidelines PDF and the form disagree on
anything, the form wins. The other disagreements on file today are the rubric criterion floor
(PDF at least six, form minimum 3 expecting 20-60+, see [[rubric-criterion-count]]) and the time
estimate (PDF one figure in minutes, form four minute fields plus a total in hours, see
[[task-metadata]]).
