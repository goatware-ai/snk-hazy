# Feedback log: lien-analysis-larkspur

## 2026-09-28 · source: build · verdict: DRAFT

Built under claude-fable-5-1 by /create-task 2 0, task 1 of 2. Occupation Paralegals and Legal Assistants (23-2011.00), domain Legal. Concept: seven claims of mechanics lien recorded against a completed California retail building, each worked under the firm's practice note from the recorder's copies, the owner's notice and waiver logs, the direct contractor's check ledger, and the close-out correspondence. Each claim turns on a different fact the solver has to find in a record: a thirtieth day that falls on a Saturday, a claim recorded the day after the extended last day, a preliminary notice served on the direct contractor alone, a late preliminary notice that reaches back only twenty days, an unconditional waiver signed and never paid, a conditional waiver resting on a stopped check, and a lien whose ninety days to sue ran out before the index search. The deliverable states each claim's standing, its enforceable amount, the release bond at 125 percent of the recorded claim, and the open points, including the direct contractor's own window to record.

**Findings** none yet; the gate was run on the packaged files and closed at 0 errors before the draft was called built.

**Actions taken** package sequence run (office_resave --force, fix_floats, fix_metadata, zips, autoeval_check); clause-map.md, verify_golden.py, form-lists.md and the rubric written off the Excel-recalculated golden.

**Form actions** none; a draft carries no Taskboard UID.

## 2026-09-28 · source: Auto-eval · difficulty_check · NEEDS_REVISION (verdict INCOMPLETE, runner error)

Platform note (eval_revision_notes, 2026-09-28T07:58Z): "Agent Runner Error: An internal error occurred during agent execution. Hazy difficulty: INCOMPLETE". The fetch-task JSON (tools/fetch_feedback.py, kept as fetch-a5f1d783.json, evaluations[0].overall_evaluation_result.children_results[3], evaluator difficulty_check) carries what the note does not: glm-5.2 attempts FAIL, FAIL, FAIL, FAIL, 4 valid, solved false; qwen3.6-27b attempts FAIL, FAIL, FAIL, INCOMPLETE, 3 valid, solved null; verdict INCOMPLETE; the child's own metadata.error reads "CodeBuild build ended FAILED in phase COMPLETED". The three sibling checks (input_files_ocrable 5 of 5 native-ok, prompt_completeness_audit, input_sufficiency/self_containment) passed with no finding; the prompt audit's one "minor finding" (Norcal Rebar's owner notice left open) is the designed gap the practice note tells the solver to flag, and the audit says so itself. Repo and platform agree on every part: the stored prompt matches instruction.md, the 23 criteria match the CSV, five inputs and one output, tools and times as in form-lists.md; both zips uploaded 2026-09-28T06:53Z and 06:54Z are byte-identical to the folder's files. The rubric_checks block's "Missing criteria: criteria_objectively_checkable, ..." string is the same standing platform artifact the cedarbrook JSON carries with feedback_outcome PASS, not a finding. The offer expires 2026-10-03T07:58Z and had not expired at fetch time.

**Findings**
1. No task finding. The one failed child is the platform's own agent runner losing qwen3.6-27b's fourth attempt; with only three valid attempts and no PASS, that model's solved stays null and the verdict is INCOMPLETE instead of PASS. No model passed any of the seven valid attempts, so the task stands as hard on the platform's own evidence (same shape as title-exam-cedarbrook-lot12, 2026-09-28).
2. Root cause is platform-side (a failed CodeBuild run inside the difficulty child). Nothing in the prompt, inputs, golden or rubric caused it, and no file is changed.

**Actions taken** (2026-09-28)
- verify_golden.py re-run: 87 figures reproduced, 0 mismatches, 32 near flips each settled by a convention the golden states (Saturday extension, stopped check, unconditional waiver effective when signed, notice never given to the owner, ninety days expired, late notice reaching back to May 9, 125 percent bond, thirty days from the notice of completion).
- Gate re-run on the folder as it stands (tools/autoeval_check.py): 0 errors; package_sweep 58 files across 2 roots, 0 findings in 0 tasks.
- Zips compared member by member against inputs/ and solution/ (sha256): identical, so neither zip is rebuilt.
- Coded: nothing added. The finding is a platform runner error with no task-side pattern to detect; tools/fetch_feedback.py already prints the per-model difficulty section from the cedarbrook round, and this fetch used it.
- Memory: one dated line in memory/difficulty-check-lessons.md recording the second INCOMPLETE-by-runner-error on the same day.

**Form actions**
- Resubmit unchanged. No criterion is re-entered (23 rows match), no zip is re-uploaded (both stamps 2026-09-28T06:53Z/06:54Z carry the built files), the prompt is untouched.
- If the resubmission re-runs the difficulty check and returns a PASS on any model, that is a real difficulty finding and the next round is a PR21/PR22 rebuild of the inputs and golden, not a rubric tightening.
