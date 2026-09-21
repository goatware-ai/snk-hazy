# Prompt: refine one Hazy-Refinement task

- **Task UID:** {TASK_UID} (the submission id on the Hazy-Refinement node)
- **Model:** the one the invoking skill carries; recorded into `built_with` at the end

A Refinery task is somebody's previously completed task that came back with targeted feedback.
The work is a revision, not a build: read what the platform asks for, find the root cause of
each item, fix it, clear the full gate, and hand back the finished prompt, rubric, inputs and
golden ready to enter. `docs/refinement/platform/submission-guidelines.md` is the platform's
own page for this node and is authoritative; read it first, every time.

---

**Scope, hard limit:** only `refinements/{TASK_UID}/` may be modified. Never edit any
folder under `submissions/`, `accepted/`, `archived/`, `drafts/` or another refinement, even
when a check surfaces the same defect there; report it in the summary instead. Never edit `original-prompt.md` or
`feedback.md` inside it: those two are the platform's hand-over, kept verbatim so the round's
changes can be read against what arrived. A change to `tools/` is re-run portfolio-wide as read-only
reporting, never as a license to fix other tasks.

**`stb`, one allowed use:** `python3 tools/fetch_refinement.py {TASK_UID}` is the only way the
platform is touched, and only in step 2. No other `stb` command, ever. The submission itself is
entered in the browser by the operator.

**Frozen by the platform** (the guidelines page, steps 7 and 1):
- the prompt, unless the feedback names it; then the smallest edit that answers it;
- every input file's name, and the deliverable's name as criterion 1 or the prompt fixes it;
- the number and order of criteria may change, but each criterion pasted is the full text from
  the rubric CSV, so the CSV is the rubric: no rubric.md, no side notes in it.

**Third-party material:** the inputs and golden are another
contributor's files, Not for Distribution. The whole refinement folder is tracked;
never copy anything from them into `submissions/` or `drafts/`, never let a phrase of them into
a task of ours.

## What the submission rules still require of a refinement

The guidelines page says the task **reruns every in-platform evaluation** after resubmission
(`docs/submission/platform/task-lifecycle.md`), so the refinement is judged by the same rule
set as a build, and the feedback panel is only the part of it the platform already tripped on.
Read before diagnosing: `docs/refinement/platform/submission-guidelines.md`,
`docs/submission/workflows/07-pre-submission-audit.md`, and the workflow doc for each area the
feedback names (`02-prompt-writing.md`, `03-input-files.md`, `04-golden-solution.md`,
`05-rubric.md`; `docs/submission/platform/auto-eval-feedback-guide.md` for reading an
AutoEval item). Skip `01-ideation.md` and the uniqueness map: the concept is not ours to choose.
Every check id below is defined in `docs/rules.md`.

Every row of `07-pre-submission-audit.md` is walked in step 4 against the refined package, with
this stance per section:

| Section | Stance in a refinement |
| --- | --- |
| A concept and difficulty | Judge, do not redesign. The `difficulty_check` reruns; if the task reads Easy, the sanctioned lever is a denser, more exacting rubric and a golden the rubric pins tightly, never a new scenario. |
| B prompt | Frozen unless the feedback names it **or** a check it faces fails on it (P4, P6, A20, one named deliverable, every input referenced by name, 3,000 characters at most). Then the smallest edit, recorded in `change.log`; everything else found goes under "Not changed, and why". |
| C inputs | Names frozen. Contents may change when the feedback or an eval requires it: leakage (L1 to L4), tells at HIGH or two MEDIUMs in one file (A10), float dust (F1), 555 numbers, period / entity / currency disagreement, the provenance stops (G2b, A3, A14). Every edit goes through the Package sequence. |
| D golden | Fully in scope, deliverable name frozen. Answers every part of the prompt, scores ~100, live formulas with cached values (A9, A17), opens from the zipped copy (A16), client-ready, and survives the reviewer's read (G8, G9, G10, G22; `04-golden-solution.md`, "The reviewer's read"). |
| E rubric | Fully in scope, and where most refinements are won: 15 to 60 rows (R11), one measurement each (R55), values the golden states (R20, R21), every prompt ask covered (R4, R13), the Rubric Quality Review's shape (core cluster 12 to 15 direct points with +2 on decision rows, the strict pair on two deliverables and two sheets R114/R117, one bare gated row R118, no presence-only computed rows R119, active-voice negatives R111, no golden-only tab names R112), at least two negatives worded as the defect committed and scoped to the rows they penalise (R67), style rows under half the count and a quarter of the weight, the filename row (R83), weights in band with a +4/+5 core row and no flat weighting (R12, R99), 500 characters each, and the rubric fails the golden's own defects. Never several record ids in one row. |
| F metadata | Only what the Refinery form shows: the multimodal boolean from the zip (a PDF-only set is NOT multimodal: the Input Files Quality Check FAILed boiler-replacement-recommendation on Yes, 2026-09-12; images, pptx and media are), the LLM-starting-point radio, the minutes estimate. O*NET occupation, tasks and skills are hidden on this form and stay as the platform holds them; `metadata.json` carries the resolved occupation for the gate and empty task/skill lists. |
| G program-wide | The Hazy string (N1) and no-contradiction rows are absolute and re-checked by the Name Check and the golden check. LLM authorship reruns at the highest severity: nothing written into an input or the golden may read as generated (A10). Uniqueness is not yours to test: never pass `--originality`. |
| H lifecycle | All apply: no project or evaluation reference in any shipped file (N1), no hiding places (L2), a tell log outside both zips (T1; for a refinement it is `change.log`), safety (a golden that normalises an unsafe act fails on content), self-containment (rebuild the answer path touching only shipped files). |

Adjudication then re-runs its ten programmatic checks (lifecycle §4): every golden claim traced
to an input with the arithmetic recomputed, leakage, input omissions and conflicts, prompt
verbosity, coherent task contract, rubric coverage, over-constrained rubric, mechanical rubric
defects, solvability, safety. Its findings return as minor fixes that bypass human review, so
pre-clearing them is the cheapest round: the families with no detector (`tools/gate_families.py`:
REV-TRACE, REV-REGISTER, REV-CREDIBLE, RUBQ-RIGID) are read by hand.

## Steps

1. **Model.** The command set the session title and the invoking skill verified the model
   (first round: `require`; a later round: `check` against `built_with`). Never edit
   `built_with` to match the running model.

2. **Fetch and stage.** One command, and the only platform access in the whole run:

   ```bash
   python3 tools/fetch_refinement.py {TASK_UID}
   ```

   It writes `refinements/{TASK_UID}/` as ONE flat folder in the exact shape of a submission
   folder (`prompt.md`, `inputs/`, `solution/`, `rubric-<task-name>.csv`, `metadata.json`,
   `feedback-log.md`, both flat zips) plus `change.log` and `review-comment.md` skeletons, and
   keeps two things from the hand-over verbatim: `original-prompt.md` (the prompt as it
   arrived) and `feedback.md` (the panel). There is no `original/` and no `refined/`. Print the
   tree it reports. On a later round it re-downloads the hand-over, rewrites those two files,
   says whether the feedback changed, and leaves everything you edit alone. If the fetch fails,
   stop and show the error; do not build the folder by hand.

4. **Diagnose as a reviewer, then as a reviser.** The original author's judgment is not yours.
   - Run `.venv/bin/python tools/autoeval_check.py refinements/{TASK_UID}` on the
     untouched package first, so you know what it sees.
   - Read `prompt.md`, every input, the golden, the rubric CSV. Apply the reviewer's read
     (section D above) and the read in `prompts/review.md` step 4: re-derive every figure the
     rubric or golden pins from the inputs with `verify_golden.py` in the folder root (started
     from `tools/templates/verify_golden.py` and kept, since the gate runs it as G43), and read
     the golden against
     itself (count words against tables, convention sentences against every section, states
     against the input column that records them).
   - Walk `07-pre-submission-audit.md` row by row with the stance table above, with particular
     attention to the rows with no coded check (natural voice, authentic files, frontier
     resistance, no contradictions, safety, self-containment, the rubric alignment rows).
     Score the golden against the rubric and fix whichever side is wrong if it lands under
     ~100. A row that fails and cannot be fixed inside the frozen-name rules goes into
     `change.log` under "Not changed, and why" with the row id.
   - Write `clause-map.md` (R134): every prompt ask mapped to the golden's quoted anchor and a
     positive rubric row, which is where an ask the golden never meets shows up. Seed
     `struck-phrases.md` with every phrase the panel strikes (PR20, G42).
   - For each feedback item find the root cause, not the symptom, and check for the same
     defect elsewhere in the task. Where your recomputation disagrees with the golden, cite the
     input rows and the golden's own line; the fix is whichever side is wrong.

5. **Apply the revision.** The smallest set of changes that resolves every root cause and
   pre-clears the not-yet-run checks; do not restyle, re-plot or re-author what the feedback did
   not touch.
   - Rubric: one measurement per criterion (R55), checkable facts, negatives framed as the
     defect committed with a polarity pin (R84), no CSV re-sums, absolute dates, no
     liveness-mirror negatives (R15, R22), weights in band (R12), 500 characters at most; a
     criterion pins a figure only if the golden states it (R20, R21).
   - Documents and workbooks: text-only docx/xlsx fixes go in at zip level so `app.xml` and
     `core.xml` stamps stay byte-identical (assert each fragment occurs once, watch run splits);
     anything structural goes through the Package sequence (`prompts/submission.md`). Decision
     cells stay live formulas. "Hazy" appears nowhere (N1).
   - Rebuild `i-<task-name>.zip` / `s-<task-name>.zip` flat only if their contents changed; an
     unchanged zip is re-uploaded as the platform's original.

6. **Coded check.** If a feedback item is generalizable and mechanically checkable, add or
   tighten the check in `tools/gcheck/` (new id, group module that reads what the check reads;
   see `tools/README.md`) and re-run it portfolio-wide as reporting. If it is a one-off, say so
   in the feedback log rather than silently skipping.

7. **Gate.** Run the Package sequence (`prompts/submission.md`) on
   `refinements/{TASK_UID}` exactly as it will be uploaded; `autoeval_check.py` runs the
   rubric lint, the prompt checks, the audit and the whole `gcheck/` catalog in one pass, and
   zero errors is the bar. Never pass `--originality`. Then:

   ```bash
   R=refinements/{TASK_UID}
   .venv/bin/python tools/fix_floats.py scan $R/inputs/*.xlsx $R/solution/*.xlsx   # must be clean
   .venv/bin/python tools/package_sweep.py refinements/{TASK_UID}                  # 0 findings; fix only this task's
   python3 tools/gate_families.py                                                  # read: the hand-checked families with no detector
   ```

   If any file is touched after the gate, the sequence runs again from the top. Then read the
   round against what arrived: `git diff` the folder (it is tracked, so the diff is the round),
   and read `prompt.md` against `original-prompt.md`. Every hunk traces to a ledger line, and
   every ledger line to a hunk or a written reason.

   Finally score the golden against the final rubric **criterion by criterion**, quoting for
   each positive the golden sentence or cell that satisfies it and for each negative the reason
   it does not fire; the table goes into `change.log`. A criterion with no quotable landing is
   rewritten or dropped; a golden sentence a criterion needs but cannot find is added to the
   golden. The golden scores 100 or the round is not done.

8. **Record and stamp.** Fill `change.log`: one entry per feedback item (what it pointed
   at, the root cause, the change), the files changed with one line each, what was not changed
   and why, and the golden-versus-rubric table. Write `review-comment.md`, the paragraph
   for the form's Section 3 and nothing else, the way a contributor writes one: 60 to 120 words,
   plain first person, fragments allowed, what changed and what was left alone with the reason,
   no rule ids, no check names beyond the one that failed, no figures unless the reviewer needs
   them; hold it to A10 and A20. Append the round's entry to `feedback-log.md` (newest last:
   date, source, verdict, then Findings / Actions / Not done and why / Form actions). Then:

   ```bash
   python3 tools/build_model.py stamp refinements/{TASK_UID}
   ```

## Deliverables, exactly these

The completed artifacts, whole, ready to enter, not a changelog (the form's Section 3 asks for
the summary separately; it is item 6).

1. **File tree** of `refinements/{TASK_UID}/`.
2. **`unzip -l`** of both zips, and for each whether it is rebuilt or the platform's original.
3. **The prompt**, complete, in one fenced block, with one line above it saying "unchanged,
   leave the pre-populated field" or "changed, replace the field".
4. **The rubric**, complete and in final order, in one fenced block, `N. (+w) text` per
   criterion, including the untouched ones.
5. **The golden and inputs**: the path of each file under `solution/` and `inputs/` and whether
   it changed. Word documents are described by the sections a reviewer will open, not pasted.
6. **Section 3 text**, in one fenced block, in the contributor's voice, 60 to 120 words, nothing
   the feedback did not raise: `review-comment.md` verbatim.
7. **The form facts**: multimodal Yes/No, input file count, LLM starting point, the Section 4
   minutes estimate.
8. **Form actions**, as a checklist: which zips to re-upload or leave, which criteria textboxes
   change, which in-app checks to run before Section 2, and "submit".

Then stop. The only addition allowed is a short list of anything genuinely unresolved the
operator must act on before submitting; if there is nothing, say nothing.
