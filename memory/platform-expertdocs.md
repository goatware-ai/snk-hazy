---
name: platform-expertdocs
description: "What the platform's expert-doc captures state beyond the live submission form: difficulty_check passes when worst-agent accuracy is 80% or under, golden_solution_check is 3 agents all at 1.0000, LLM assistance on input files is permitted when the result is indistinguishable from a real document, and the coded checks N1/L2/T1/A1-extended. Carried over from the desk this repo was built from and not yet confirmed here; on any conflict the live form wins"
metadata:
  type: reference
---

The two captures that are authoritative for this desk are
`docs/submission/platform/platform-submission-form.md` (the live form, which blocks submission)
and `docs/submission/platform/create-the-task-guidelines.md`. The supporting captures are
`creating-input-files.md`, `style-guide-llm-tells.md`, and the two list captures
`domains-and-occupations.md` and `onet-codes.md`.

**On any conflict the form wins**, then the guidelines PDF, then anything else
([[golden-solution-required]] is the worked example of that order).

Everything in this file is carried over from the desk this repo was built from and not yet
confirmed here. It is background; nothing in it blocks a submission on its own.

- ~~Rubric band 15-60~~ SUPERSEDED 2026-09-21: the form sets no ceiling and expects 20-60+, with
  an error floor of 6 from the guidelines PDF. See [[rubric-criterion-count]].
- **difficulty_check passes when worst-agent accuracy is 80% or under** (it fails as Easy only
  when both models exceed 80) - not "both under 80".
- **golden_solution_check = 3 agents, all must score 1.0000** - the [x, y, z] triples in oracle
  feedback are this check's raw scores.
- **LLM assistance on input files is permitted** when the result is indistinguishable from a real
  document, tell-free and leak-free (`creating-input-files.md`) - this supersedes the older
  sanitization-only rule; the batch-provenance stop ([[package-hygiene-pipeline]]) still stands.
- Coded checks taken from the captures: **N1** (project/eval vocabulary in shipped
  content/names/metadata), **L2** (hidden sheets/rows, comments, tracked changes, input speaker
  notes), **T1** (tell log must be standalone, never in a package), **A1 extended** (named
  AI-blue hex range #1C3557-#2E4A6B, inputs plus docx/pptx too).
- A **safety check** exists: nothing may teach materially unsafe professional practice, relevant
  if a task ever touches dosing, held parts or rigging. Whether this desk's platform runs it is
  unconfirmed.
- Human review caps at 5; adjudication fixes bypass human review ([[submission-tracking]]).
- The EC gets **2 revision attempts**; a third failure is a reject.
- **Input files are locked in the platform and can never be edited**, so EVERY input problem
  routes to Needs Revision regardless of size. Input defects are therefore the most expensive
  class to ship.
- Only **2 to 3 rubric criteria** are spot-checked against the golden, so a mismatch anywhere else
  is a coin flip. It is not a full verification.
- A **Suspected Duplicate or Template** flag exists for a task that reuses a prior task or
  template even when it is otherwise acceptable. This desk has no uniqueness map to diff against,
  so the check is by hand against its own drafts and submissions.
- **Bounded subjective criteria are explicitly valid** and are not sent back for being subjective
  when they name the conditions and score the reasoning. Only unbounded criteria come back.
- O*NET metadata is the evals team's, not the reviewer's (the M1/M2/M3 checks answer to that team).
- Six error classes drive a send-back label: LLM-Generated Input Files, LLM-Generated Golden
  Solution, Input File Quality, Golden Solution Quality, Rubric Quality, Prompt Quality.
