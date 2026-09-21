# Task Lifecycle

> **Inherited from the Geranium desk, not yet confirmed for Hazy.** This document was
> captured on a different project and describes Geranium's submission, auto-eval, human review and adjudication stages. It is kept because the guidance is
> domain-agnostic, but nothing in it has been checked against Hazy's own platform. Where it
> disagrees with `create-the-task-guidelines.md` or `platform-submission-form.md`, those win.

This page describes the task lifecycle from beginning to end.

## 1. Submission

a. Your task must pass all in-app evaluations before you are able to submit:

   i. **O\*NET Compliance Check** – This check verifies that exactly one occupation is selected from the dropdown, the occupation matches the industry sector assigned, and the occupation matches the prompt content.

   ii. **O\*NET Tasks & Skills Compliance Check** – This check verifies there are between 1 and 10 O\*NET tasks are selected from the dropdown (or "N/A" if the occupation has no O\*NET reference tasks), between 1 and 10 O\*NET skills are selected from the dropdown (or "N/A" if the occupation has no O\*NET reference skills), and the selected tasks and skills are relevant to the prompt content.

   iii. **Input Files Quality Check** – This checks verifies that input files are non-empty, not too large, and contain meaningful content, have clean filenames use a flat archive structure when zipped, match filenames mentioned in the prompt, and that files are consistent with the multimodal boolean field.

   iv. **Prompt Quality Check** – This check verifies that the prompt is written in your own voice, gives specific expert context, is complex enough, requiring multiple reasoning steps and 5 hours of work minimum, contains no spelling or grammar errors, specifies a single, concrete output deliverable and a file name, and that the input files are referenced explicitly in the prompt (cannot be answered from instructions alone). It also verifies uniqueness, such that a similar prompt has not already been created.

   v. **Golden Solution Files Quality Check** – This checks verifies the golden solution files are non-empty, not too large, are well-formatted and client-ready, and are not placeholder or LLM outputs, they have clean filenames and use a flat archive structure when zipped and the files match filenames mentioned in the prompt.

   vi. **Rubric Quality Check** – This check verifies that Rubric criteria are specific and grounded in the task details, include numeric/data specifics when applicable, grade only the final answer, not hidden intermediate steps, weights are not included in the criterion text field and are only stored in the numeric weight field, and that each criterion is atomic and does not bundle multiple independent checks into one field.

   vii. **Name Check** – This check verifies there is no usage of the name Geranium across the fields.

## 2. Post-Submission Evals

a. There are several post-submission evaluations that your submission must pass before entering human review.

   i. **golden_solution_check** – This check verifies that every criteria provided is met within your golden solution. It is checked against three different agents, and the score must be 1.0000, 1.0000, 1.0000 to be considered a pass.

   ii. **dataset_quality_check** – Datapoint quality audit on a five-axis rubric (prescriptiveness, synthetic feel, realism, cross-document consistency, formatting)

   iii. **difficulty_check** – runs two models 5x each in parallel and reports on a 5-tier difficulty score (Frontier / Advanced Plus / Advanced / Core / Easy). Sends the submission to NEEDS_REVISION when difficulty resolves to Easy (worst-agent accuracy > 80%)

   iv. **llm_authorship_check** – Scores the llm_generated axis in isolation and surfaces a verdict/text summary. Mapped to PASS in the outcome map, and NEEDS_REVISION if the overall mean is below 3.5 threshold.

   v. **agentic_rubric_quality_check** – Source-aware agentic rubric quality review. Reads the prompt, weighted criteria, input files, and golden solution; checks grounding, coverage, atomicity, objectivity, redundancy, and unjustified rigidity.

   vi. **audit_check** – Audit of the task package itself rather than the deliverable: prompt/rubric alignment, input sufficiency, verifier integrity and occupational realism.

   vii. **self_containment_check** – audit of whether the submission's prompt + input files are sufficient to reproduce the golden solution, with no outside data/tools/web search required.

   viii. **golden_solution_leakage_check** – audit of whether the specific deliverables asked for in the prompt and provided in the golden solution are incorrectly leaked into the input files.

   ix. **rubric_golden_alignment_check** – Checks that the submitted rubric can actually be satisfied by the golden solution. Two judged tiers: filenames vs content.

   x. **geranium_safety_check** – Screens the task package for content that would teach materially unsafe professional practice, such as an unsafe drug administration rate, release of held aircraft parts, and a crane pick without capacity verification, independently of correctness scoring.

## 3. Human Review

a. In the human review layer, there will be a maximum of **5 total reviews** before the task can only be accepted or rejected.

## 4. Adjudication

a. The adjudication layer consists of one final, exhaustive, programmatic pass that verifies the following:

   i. **Golden accuracy:** Is every claim traced to the exact input source. Recomputes arithmetic for accuracy. This check will flag embellishments such as added names, substituted terms, and wrong cross-references.

   ii. **Input Leakage:** Inputs containing pre-computed answers, populated templates, or conclusion memos.

   iii. **Input omissions & conflicts:** Missing facts needed for conclusions and unresolved contradictions. Deliberate imperfections are permitted when a rubric criterion judges them.

   iv. **Prompt verbosity:** LLM-style tells, including excessive scene-setting, input cataloguing, and scaffolding phrases.

   v. **Coherent task contract:** The prompt names a scope, population, or date that the inputs don't pin down – meaning two professionals could answer different questions.

   vi. **Rubric coverage:** Every prompt requirement is graded by at least one criterion.

   vii. **Over-constrained rubric:** The rubric mandates one approach when valid alternatives exist.

   viii. **Mechanical defects:** Incorrect weight totals, reversed negatives, unrelated guardrails, duplicates, double-counting, or "Penalize if..." framing instead of affirmative facts.

   ix. **Task solvability:** The prompt asks for a determination that the inputs cannot support.

   x. **Safety-critical content:** The golden teaches an unsafe practice (separate escalation from scoring-only defects in safety domains).

b. If any of the above are flagged for areas of improvement, the task will be returned back to the original submitter to make the final updates. Given these checks are automated, this means **minor fixes** may be returned to the original submitter, however, once these fixes are made, the task returns to the adjudication layer, bypassing human review.
