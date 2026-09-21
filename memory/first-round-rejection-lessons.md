---
name: first-round-rejection-lessons
description: "A task that gated at 0 errors was REJECTED outright at its first human review 2026-09-05 and the operator ruled learn-not-fix: the prompt frame woven never a self-introduction (P6), the comma rules (A20), the literal read of the golden against the inputs (G8/G9/G10 and the hand reads, detail in golden-fidelity), and a rubric that must fail the golden's own defects; a second task rejected at adjudication 2026-09-11 on cutoff chronology (G22); a third rejected after eleven returns 2026-09-15"
metadata:
  type: feedback
---

**What happened.** A task passed `autoeval_check.py` at 0 errors on 2026-09-04 and was rejected
outright at its first human review on 2026-09-05: "major errors in the golden and rubric, along
with minor revisions to clarity and sentence structure needed throughout." The operator's
instruction: do not fix it; learn the lesson so no future task is rejected at a first-round
review. The task stayed REJECTED and archived. On 2026-09-11 a second task was rejected at
adjudication after 14 platform verdicts and 4 human rounds on a fabric defect present since the
first build (a count cited authorizations issued after its own date, and a memo's as-of balance
equalled the undated register sum); the rule is G22 in [[golden-fidelity]].

**Why the gate missed all of it.** Every coded fidelity check tested the rubric against the
golden or the golden against itself. The reviewer did three reads none of the checks did: the
prompt as a coworker would hear it, every sentence for basic comma rules, and the golden claim by
claim against the inputs and the prompt.

**The lessons, and where each lives now:**

1. **P4 woven, never a self-introduction (P6).** "I run the warehouse ... for a pipe, valve and
   fitting wholesaler ... Whoever picks this up should have ..." reads as LLM to a reviewer
   ("They are your coworker. They know what the company is"). Carry the state on a place the work
   touches, the role as ownership of the problem, the experience as the reason for the handoff
   addressed to the reader, and say in the same sentence why each named event matters to the
   work. Coded P6 (`tools/gcheck/prompt_inputs/prompt_frame.py`). See
   [[prompt-overspecification-giveaways]].
2. **Comma rules (A20).** Comma before and/but/so/or joining two independent clauses; never a
   third clause in a sentence; serial comma in every list; prompt, inputs, golden text cells and
   rubric alike. Coded A20 (`tools/gcheck/authorship/prose.py`, REV-REGISTER) for the
   bare-conjunction and three-clause shapes; the rest is a read. See [[prose-standard]].
3. **The reviewer's read of the golden**, a standing step in
   `docs/submission/workflows/04-golden-solution.md` and `prompts/submission.md`, run before the
   rubric is drafted: every cited identifier exists in an input (G10); a stated date is written
   in an input or derived by a stated rule, never inferred from adjacent records; the deliverable
   is dated no later than any action it schedules as done (G9); "ready to sign" means the
   signable document with a signature-and-date line (G8); every policy class applied to every
   record it governs, no invented status; a "cost since <date>" covers the partial period; no
   duty on an asset after the day it leaves, successor named. The full list is [[golden-fidelity]].
4. **The rubric must fail the golden's own defects.** Pin the facts a reviewer verifies
   (identifiers, the document date, the signature line, each policy class closed) so a wrong
   golden loses points under its own rubric; "the rubric clearly did not catch the issues" was the
   closing line. See [[rubric-coverage-and-completeness]].

**How to apply.** Both build skills say it: before a draft is called built, do the reviewer's read
and the comma read. The first sweep of the new checks fired P6 on 22 of 24 prompts and A20 on
every task in submissions/ and drafts/ (report only, per [[gate-scope-single-task]]); those were
authoring habits, fixed task by task when each is next touched, never in a portfolio pass.
A rejected task's own concept re-entering is the "recycling" flag shape, so a rejected task is
not re-drafted. This desk has no uniqueness map and no accepted-asks map, so keep the
no-recycling habit by hand.

- 2026-09-15: a third task was REJECTED after eleven returns and a 0-error gate. Central finding:
  the golden gave one claims schedule where the prompt and the claims desk required a form per
  invoice. Also a struck claim left in a table cell, an unstated rounding convention a reviewer
  read differently, and a due date already past. Coded R134 G41 G42 G43 P8 and the G5 split arm;
  PR19 PR20.
