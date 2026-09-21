# Submission — Guidelines (Geranium Refinery)

> Captured verbatim from the Snorkel Geranium-Refinement submission page (screenshots,
> 2026-09-10). Marked "Snorkel AI | Proprietary & Confidential | Not for Distribution".
> This is an AUTHORITATIVE platform capture — on any conflict with a workflow page, a tool,
> or anything else in this repo, this page wins.

## What you'll be doing

1. You'll receive a task with an existing prompt, input files, golden solution, and rubrics.
2. Review the feedback note in the left panel to identify required changes.
3. Make the updates and submit the task.
4. The task will rerun through all in-platform evaluations. Revise and resubmit if any
   evaluations fail.
5. After passing all evaluations, the task enters review to confirm the required changes
   were completed.
6. Once approved, the task is accepted and eligible for payment.

## Overview

Geranium Refinery tasks are previously completed tasks that need targeted refinements to
their prompt, inputs, golden solution, or rubrics. Review the feedback and AutoEval
guidance, make all required updates, and submit the task for reevaluation and review. Once
all checks pass and the updates are confirmed, the task is accepted and eligible for payment
based on its assigned tier.

Each Submission within Geranium-Refinery is composed of the following essential components:

- Prompt
- Input file zip
- Golden Solution Zip
- Rubrics

The Submission lifecycle begins by opening the task itself and carefully working through the
steps listed below, in order, then clicking **Submit**. Your Submission will then go through
Snorkel's quality assurance process involving a Peer Review and a series of programmatic
evaluations where it will eventually either be **Accepted**, **Rejected**, or returned to you
with actionable feedback for specific **revisions**.

---

## Creating a Submission — Step by step

Start by initiating a new submission form for Geranium-Refinement via the Snorkel Platform:

1. Log in to the Snorkel Platform and search for Geranium-Refinement within the homepage
   search bar.
2. Click *Start* on the **Submission** node for Geranium-Refinement to begin a new
   submission.

### 1. Begin Submission

You will receive a task that already includes a prompt, input files, golden solution, and
rubrics. Your role is to refine the task using the feedback provided.

These materials are located on the right-hand side of the browser window under
**Section 1 - Prompt and Input Files**. The user prompt will be visible in the prompt
section, while you can download the input files and golden solution to access them
off-platform. This step is vital.

Screenshot (right-hand panel):

> **Download Input File**
> Here are the input files you will download to inspect and make neccesary corrections to
>
> **Section 2 - Golden Solution and Rubric**
> **Provided Golden Solution File Download**
> **Provided Golden Solution File Download \***

### 2. Feedback and Provided Rubrics

Navigate to the section titled — **Feedback and Provided Rubrics** — on the left-hand side
of the browser window to access **both** the provided feedback to improve the task and the
provided rubrics.

All correction feedback is listed in the left column, while the rubrics are listed in the
right column.

Screenshot (left-hand panel, two columns):

> **Feedback and Provided Rubrics**
> Guidance to improve the task before submission
>
> | Feedback to Improve Task | Provided Rubrics |
> | --- | --- |
> | **Correction Feedback:** 1. The golden states "Ciro has multiple retail operations where he sells fireworks" (paragraph 10) but no input mentions retail operations. Delete the clause or replace with record-supported phrasing, e.g., "Ciro sold these inherently dangerous fireworks to a seventeen-year-old and was convicted of that offense." | **Rubric** — Criterion 1 — weight 1: The final deliverable is a Word document. Criterion 2 — weight 5: Argues that Sandy Cane qualifies as a victim under the Best Dakota Crime Victim's Rights Act (BDCVRA). Criterion 3 — weight 5: Argues that Victor Cane qualifies as a victim under the Best Dakota Crime… |

### 3. Feedback to Improve Task

Navigate to the section titled, **Feedback to Improve Task**.

Read the full Feedback to Improve Task field. It may include:

- **Correction Feedback**
  - Specific corrections that are required in order to get this submission to an accepted
    state
- **AutoEval Feedback**
  - A list of previously failed AutoEvals along with descriptions detailing failure reasons
- **Post-Submission Evaluations Not Yet Run**
  - AutoEvals that were not run on the original task

### 4. Analyze Correction Feedback

Analyze all correction feedback listed under **Feedback to Improve Task**.

Example screenshot:

> **Correction Feedback:**
>
> 1. Paragraph 22 of migration_audit.docx says 'Four statements sit outside the transaction
>    block' then lists only three; reconcile by changing to 'Three' or adding the
>    CONCURRENTLY index with a carve-out note.
> 2. Add rubric criteria for three uncovered prompt requirements: per-issue file
>    attribution, per-issue fix, and identifying items that look wrong but are correct per
>    policy.
> 3. Complete or remove rubric line 14 (truncated mid-sentence at 'when a referenced co.'
>    and double-counts line 2). Remove rubric line 15 (unrelated guardrail about figures
>    citing periods/source identity that the prompt does not request).
> 4. (a) Golden paragraph 22 count/enumeration mismatch: 'Four' stated but only three items
>    listed. (b) Three prompt requirements uncovered by rubric: per-issue file attribution,
>    per-issue fix, and policy-correct items section. (c) Rubric line 14 truncated and
>    duplicative of line 2; line 15 is an unrelated guardrail with no prompt anchor.

### 5. Analyze AutoEval Feedback

Analyze all previously failed AutoEvals located directly underneath Correction Feedback. A
failed AutoEval represents a known issue in the original submission; the task cannot be
accepted until it passes after resubmission.

Example screenshot:

> **AutoEval Feedback:**
>
> **Dataset Quality Check:**
>
> Dataset quality check (LLM-authorship axis excluded) FAILED (overall mean 1.0 < threshold
> 3.5; synthetic_boilerplate score 1 <= cutoff 1).
>
> Axis scores (1-5):
>
> - Prescriptiveness: ?/5
> - Synthetic / boilerplate feel: 1/5 Hard-fail deterministic preflight found forbidden
>   "Geranium" project-name leakage in task metadata or submitted assets.
> - Domain realism: ?/5
> - Cross-document consistency: ?/5
> - Formatting quality: ?/5
> - Content thinness: ?/5
> - Hard-coded spreadsheet values: ?/5

### 6. Analyze Post-Submission Evaluations Not Yet Run

Review the list of AutoEvals that were not previously run. These checks will also need to
pass when the task is resubmitted.

Example screenshot:

> **Post-Submission Evaluations Not Yet Run**
>
> The following post-submission evaluations have not been run and will run after you submit
> this task. Please verify that the task is positioned to pass these evaluations before
> submitting, or additional AutoEval feedback may require further revision:
> **GOLDEN_SOLUTION_LEAKAGE_CHECK**

### 7. Complete Submission

After you've analyzed the entirety of the Feedback and Provided Rubrics section, you are
ready to complete this submission.

Navigate to **Section 1 - Prompt and Input Files** on the right-hand side of the browser
window.

Adjust the prompt **only if requested. Do not change this prompt unless instructed
otherwise**.

Next, if your input file(s) require a modification, update them, compress your modified
input file(s) together and upload them as a .zip file. Do not change the naming conventions
of each individual input file.

Run the **Input Files Quality Check** and **Prompt Quality Check** before moving on to
Section 2.

In **Section 2 - Golden Solution and Rubric**, start by making any requested modifications
to the output file, and upload the provided Golden Solution file as a zip.

**IMPORTANT: READ CAREFULLY**

Finally, copy/paste each rubric criterion from the left-hand side of the browser window
underneath, **Feedback and Provided Rubrics** into each corresponding criterion textbox on
the right-hand side of the browser window (these criterion textboxes are located after the
golden solution evals).

Make any necessary changes/appendages/modifications based on the provided task feedback.

### 8. Finalize Submission

Submit your completed updates. The task will then run through all post-submission
AutoEvals. If the task passes all AutoEvals, it will move to review. Reviewers will confirm
that all required changes were completed. Once the updates are confirmed, the task will be
accepted and eligible for payment.
