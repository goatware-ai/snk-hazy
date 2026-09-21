# Auto-Eval Feedback Guide

> **Inherited from the Geranium desk, not yet confirmed for Hazy.** This document was
> captured on a different project and describes Geranium's post-submission auto-eval feedback boxes. It is kept because the guidance is
> domain-agnostic, but nothing in it has been checked against Hazy's own platform. Where it
> disagrees with `create-the-task-guidelines.md` or `platform-submission-form.md`, those win.

After you submit your golden solution and rubric, the platform automatically runs quality checks called **auto-evaluations** (auto-evals). They run in the background — you don't trigger them. Allow **60–120 minutes** after submission before checking results.

> Auto-eval build codes no longer overwrite human reviewer feedback. You'll see a separate, **date-labeled human reviewer feedback box** and a separate **auto-eval feedback box**.

## Step 1 — Where to find auto-eval feedback

Your first signal is a build code or message like *"AutoEval Execution Summary: AutoEval execution failed. Build status: FAILED..."* in the reviewer feedback box on the left.

All five auto-eval feedback boxes live in **Section 2: Golden Solution and Rubric**. Scroll past the Golden Solution file uploader and the file quality check to find:

1. Auto-Evaluation Golden Solution Submission Feedback
2. Auto-Evaluation Dataset Quality (Input/Output) Check Submission Feedback
3. Auto-Evaluation LLM Generated Files Check Submission Feedback
4. Auto-Evaluation Difficulty Submission Feedback
5. Auto-Evaluation Rubric Quality Check Submission Feedback (optional)

> ⚠️ These boxes only populate after the auto-evals finish. If one looks empty, check back after 60–120 minutes. If your status is **Needs Revision** with no reviewer notes beyond build codes, these boxes are your primary diagnostic.

## Step 2 — How to read each check

### The three standard checks (Pass / Fail)

Golden Solution, Dataset Quality, and LLM Generated Files each show **PASSED** or **FAILED** in the first 1–2 lines. If **FAILED**, expand the box for axis scores, the exact issues flagged, and suggested next steps.

When reading an expanded failure report: note which **axis score** drove the failure; address **HIGH** issues before **MEDIUM**; treat suggested next steps as guidance — you remain responsible for the accuracy of every edit.

### The Difficulty check (accuracy percentages)

Shows **Best Agent Accuracy** and **Worst Agent Accuracy** on line 2.

- **PASS:** at least one percentage is **80% or below** (a model found your task genuinely hard).
- **FAIL:** both are above 80% (all tested models solved it easily — not challenging enough).

### The Rubric Quality check (rating)

Returns an overall rating — **needs_improvement**, **good**, or **excellent**. Aim for good or excellent. It's **non-blocking today** (a reviewer confirms a needs_improvement before returning a task), but expect it to become blocking. When you see needs_improvement, expand the box and use its feedback as your revision checklist.

## Quick reference

| Check | What to look for | Pass condition |
| --- | --- | --- |
| Golden Solution | First 1–2 lines: PASSED/FAILED | PASSED |
| Dataset Quality (Input/Output) | First 1–2 lines: PASSED/FAILED | PASSED |
| LLM Generated Files | First 1–2 lines: PASSED/FAILED | PASSED |
| Difficulty | Best/Worst agent accuracy % | At least one ≤ 80% |
| Rubric Quality | Rating near the top | good or excellent |

## Step 3 — What to do when a check fails

**Revise.** Use the suggested next steps as a starting point, apply your own judgment, and make genuine, human-verified corrections against your source files. For a needs_improvement rubric rating, expand the box and treat its feedback as your checklist.

**Submit a rebuttal (only if you believe a flag is wrong).** Post it as a **threaded reply** to the daily *Eval & Review Comments* post in Slack — not a new thread or DM.

Each rebuttal must include at least one of: a screenshot of the relevant auto-eval feedback, or your **Task ID / Submission ID** (not a link).

A strong rebuttal: states specifically what you believe is correct and why; references the exact criterion or guideline section; provides evidence from your input files or golden solution; acknowledges what was flagged, then explains why your submission satisfies the requirement.

> ⚠️ **These won't move forward:** "I disagree" (no evidence); "The platform evals passed it before I submitted" (pre-submission evals are a floor check, not a final gate); "I used the platform-generated rubric criteria" (never paste those directly — criteria must be rewritten with human-verified values).

## Auto-eval review checklist

- Wait 60–120 minutes after submission before checking.
- Go to **Section 2: Golden Solution and Rubric**.
- Check the first 1–2 lines of each standard box for PASSED/FAILED.
- For Difficulty, confirm at least one accuracy value is ≤ 80%.
- If a check failed, expand and read the full report; fix HIGH-severity items first.
- Open the Rubric Quality box; if needs_improvement, expand and read the fixes.
- To rebut, reply in the daily Slack thread with a screenshot and/or Task/Submission ID.
