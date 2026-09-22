# Prompt: revise a task based on new feedback

- **Task UID:** {TASK_UID}

The feedback is fetched from the platform, not pasted. Step 2 does it.

---

**Scope, hard limit:** only the task resolved from the UID above may be modified. Do not edit
any other task folder (instruction.md, the rubric CSV, workbooks, zips, feedback-log.md,
metadata.json) even if a check or diagnosis surfaces the same defect there; report such
findings in the summary instead. A change to `tools/` is re-run portfolio-wide as read-only
reporting, never as a license to fix other tasks in this run.

**`stb` is read-only here, hard limit:** the only platform call a revision makes is
`tools/fetch_feedback.py`, which wraps `stb submissions fetch-task` and
`stb submissions feedback`. Never run `stb submissions create` or `update`, never sync
status, never upload. Submitting the revision is the operator's, on the platform.

## Steps

1. **Locate and verify the task.** Resolve the UID via `submission-list.md` to its
   `submissions/{NN}-{task-name}/` folder and confirm the folder's `metadata.json` carries that
   UID. If the UID resolves to nothing, stop and say so. The invoking skill has already
   verified that the model running now is the one recorded in `built_with`; never edit
   `built_with` to match the model you happen to be.

2. **Fetch the feedback.** Do not ask for it; the platform has it.

   ```bash
   .venv/bin/python tools/fetch_feedback.py <uid>
   ```

   That writes `feedback-<uid8>.md` into the task folder and prints it. Read all of it before
   diagnosing anything. Four parts matter:

   - **Outcome and the revision notes.** `eval_revision_notes` is the auto-eval's verdict,
     `revision_notes` a reviewer's. Either can be absent.
   - **The per-check list.** Each check's own text, with the failures marked. A check that
     passed still tells you what the grader read.
   - **Platform vs repo.** The prompt and every rubric row, compared. The platform's copy is
     what was graded, so where they disagree, the platform is the fact and the folder is the
     thing to correct. An edit made on the platform after submission never came back here.
   - **What the platform holds.** Domain, occupation, file counts, times, tools. Check these
     against `metadata.json` and `form-lists.md`.

   A return whose notes say nothing is normal, not a failure to fetch: the JSON usually
   carries the trigger the note does not. If the report is thin, the failing check's text and
   the drift section are what you have; say so plainly rather than inventing a cause.

   Fetching also refuses to guess. If no folder carries the UID it says so and writes nothing;
   resolve the folder first rather than working on the wrong task.

3. **Diagnose.** Read the folder's `instruction.md`, `rubric-{task-name}-{uid8}.csv`,
   `feedback-log.md`, and the files the feedback names. Determine the root cause of each
   finding rather than the symptom it names, and check whether the same defect exists
   elsewhere in this task (other criteria, other tabs, other files); fix every occurrence. Run
   `verify_golden.py` before trusting any figure the feedback questions. Count the returns in
   `feedback-log.md`: from the third, the revision is a rebuild from `clause-map.md` (PR19), every
   prompt ask re-read against the golden and the rubric and every earlier finding re-checked in
   every file before the named items are fixed, and the map's `Rebuilt:` line is dated when that is
   done (R134).

4. **Apply the revision.** Update the rubric CSV, the solution or input files, and/or
   `instruction.md` as the feedback requires, following the existing conventions:
   - Rubric edits: one simple atomic sentence per criterion (R55), negatives worded as the
     defect committed with a polarity pin (R84), no CSV re-sums, absolute date windows, no
     liveness-mirror negatives (R15, R22). Weights stay non-zero integers from -5 to +5, with
     no gap around -1 and -2, and a negative may penalise any specific, observable unwanted
     outcome, not a restricted class of them (`docs/submission/platform/platform-submission-form.md`,
     "4. Task Rubrics"). When feedback asks for coverage, add rows freely: the floor is 6
     criteria, 20 or more is the expected range and there is no ceiling. Every value a new or
     edited criterion asserts is pulled from the golden and the inputs, never estimated and
     never hedged ("approximately", "roughly", "about", "~"). After any addition, renumbering
     or deletion, the general **Overall formatting and style of the deliverable** row is still
     the last row of the CSV.
   - File and metadata edits: if an input or output file is added, removed or renamed, the
     Input File List, the Output File List, every mention in `instruction.md` and the member names
     inside the rebuilt zip all have to match again, exactly, case and extension included; a
     mismatch there is one of the most common reasons a submission comes back. If the scope of
     the work changed, revisit the five time values (four minutes fields plus the total in
     hours, the total at least their sum and over 3) and the tools list in `metadata.json`.
   - Workbook and document edits: no blue fills or datetime cells (A1, A2), decision fields
     stay live formulas, then run the Package sequence (`prompts/submission.md`) on every
     touched file. Rebuild the affected `i-`/`s-` zips (flat, bare task name) only if their
     contents changed.
   - Record every phrase the feedback strikes, and every claim a fix removes, in
     `struck-phrases.md` the same day: a quoted literal, or a /pattern/ that also catches the
     claim reworded, then source and date (PR20); G42 searches every file for it, table cells
     and rubric rows included.
   - Keep `verify_golden.py` and `clause-map.md` current: a moved figure, a new convention, a
     new ask landing or a renumbered rubric row changes them in the same revision.

5. **Coded check.** If the finding is generalizable beyond this task and mechanically
   checkable, add or tighten the check in `tools/gcheck/` (the group module that reads what
   the check reads, with a new id; see `tools/README.md`) and re-run it portfolio-wide as
   reporting. If it is a one-off, say so in the feedback log rather than
   silently skipping.

6. **Gate.** The Package sequence ends in `tools/autoeval_check.py` at zero errors on the folder
   as it will be uploaded; if any file is touched after it, the sequence runs again from the
   top. The gate runs `verify_golden.py` (G43) and reads `clause-map.md` (R134) and
   `struck-phrases.md` (G42), so a revision is not done while any of them fails. Then run
   `.venv/bin/python tools/package_sweep.py`, the mechanical read-only sweep of
   every task folder (no repair mode by design): fix only what it reports against the task
   named in this revision; everything else goes in the step 8 report and is left untouched.

7. **Record.** Append an entry to the task's `feedback-log.md` (newest last: date, source,
   verdict, then Findings / Actions / Form actions); the log holds the detail, including what
   remains to be done on the platform (which criteria to re-enter, which zips to re-upload,
   resubmit). In `submission-list.md` move the row into the section matching the single
   applicable state (OFFERED, NEEDS_REVISION, EVALUATION_PENDING, REVIEW_PENDING, ACCEPTED or
   REJECTED); the section is the status, there is no Status cell.

8. **Report.** End with a summary: root cause, files changed, coded check added or explicitly
   skipped with the reason, gate result, and the exact platform form actions the operator must
   perform. Add a **Package sweep** line: "clean across N tasks", or the other tasks carrying
   findings, named. Never fold those into this revision.
