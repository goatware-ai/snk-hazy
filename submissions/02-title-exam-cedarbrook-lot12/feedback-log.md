# Feedback log: title-exam-cedarbrook-lot12

## 2026-09-21 · source: build · verdict: DRAFT

Built under claude-fable-5-1 by /create-task 2 0, task 1 of 2. Occupation Title Examiners, Abstractors, and Searchers (23-2093.00), domain Legal. Concept: a title examination report for a residential closing in Licking County, Ohio, where the chain carries a deed that describes less land than the grantor held, an unreleased mortgage, a dower defect, a name variance, a judgment lien on the seller, a judgment on a similar name that does not attach, delinquent taxes with penalty, and a tax proration to the closing date.

**Findings** none yet; the gate was run on the packaged files and closed at 0 errors before the draft was called built.

**Actions taken** package sequence run (office_resave --force, fix_floats, fix_metadata, zips, autoeval_check); clause-map.md, verify_golden.py, form-lists.md and the rubric written off the resaved golden.

**Form actions** none; a draft carries no Taskboard UID.

## 2026-09-28 · source: Auto-eval · difficulty_check · NEEDS_REVISION (verdict INCOMPLETE, runner error)

Platform note (eval_revision_notes, 2026-09-23T00:52Z): "Agent Runner Error: An internal error occurred during agent execution. Hazy difficulty: INCOMPLETE". The fetch-task JSON (tools/fetch_feedback.py, evaluations[0].overall_evaluation_result.children_results[3], evaluator difficulty_check, kept as fetch-b34c9335.json) carries what the note does not: glm-5.2 attempts FAIL, FAIL, FAIL, FAIL, 4 valid, solved false; qwen3.6-27b attempts FAIL, INCOMPLETE, FAIL, FAIL, 3 valid, solved null; verdict INCOMPLETE. The three sibling checks (input_files_ocrable, prompt_completeness_audit, self_containment) passed with no finding. Repo and platform agreed on every part: the stored prompt matched instruction.md, the 27 criteria matched the CSV, four inputs and one output, tools and times as in form-lists.md; both zips uploaded 2026-09-21T22:27Z are byte-identical to the folder's files. The offer's expiry_time (2026-09-28T00:52:54Z) had passed when the feedback was fetched (05:43Z) with further_revision_requests_allowed true.

**Findings**
1. No task finding. The one failed child is the platform's own agent runner erroring on qwen3.6-27b's second attempt; with only three valid attempts and no PASS, that model's solved stays null and the verdict is INCOMPLETE instead of PASS. No model passed any of the seven valid attempts, so the task stands as hard on the platform's own evidence.
2. Root cause is platform-side (a 500 from the runner, as the sibling input_sufficiency child also logged one InternalServerError on its first request before succeeding on its second). Nothing in the prompt, inputs, golden or rubric caused it, and no file is changed.

**Actions taken** (2026-09-28)
- Gate re-run on the folder as it stands under the checks coded after the 2026-09-21 build (L8, PR21, PR22, the H1 feedback-file skip): 0 errors; G43 reproduced 14 figures with 6 near flips each settled by a stated convention; package_sweep clean, 0 findings in 0 tasks.
- Zips compared member by member against inputs/ and solution/: identical, so neither zip is rebuilt.
- Coded: tools/fetch_feedback.py now prints a "Difficulty check" section (per-model attempts, valid attempts, solved, verdict, runner errors) and an EXPIRED header line when expiry_time has passed at fetch time; tools/README.md updated. No tools/gcheck/ check is added because the finding is a platform runner error with no task-side pattern to detect.
- Memory: one dated line in memory/difficulty-check-lessons.md on the INCOMPLETE verdict semantics.

**Form actions**
- Resubmit unchanged. No criterion is re-entered (27 rows match), no zip is re-uploaded (both stamps 2026-09-21T22:27Z carry the built files), the prompt is untouched.
- The offer had expired before this revision; confirm the platform still takes the resubmission under further_revision_requests_allowed. If it re-opens as a fresh submission, the same package goes up and the new UID goes into metadata.json.
