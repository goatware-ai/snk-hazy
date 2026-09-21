---
name: platform-expertdocs
description: "docs/{submission,reviewer}/platform/ are the authoritative GitBook captures (2026-08-26) of both the authoring and reviewer rule sets: rubric 15-60, difficulty = worst agent <=80%, LLM-assisted inputs OK, reviewer spot-checks, two revisions before reject, locked input files, checks N1/L2/T1 and A1 extended; the omnichannel golden example is reviewer-side"
metadata:
  type: reference
---

The live GitBook expert docs (https://expertdocs.snorkel-ai.com/geranium-production-1, behind
the Snorkel portal login - not fetchable; the user screenshots pages and they are transcribed)
are mirrored under **docs/submission/platform/** (welcome, project-guidelines-v5.1,
style-guide-llm-tells, creating-input-files, task-lifecycle, auto-eval-feedback-guide,
task-example-wholesale-trade) and **docs/reviewer/platform/** (captured 2026-08-26; the
`platform/` subfolder name marks captured-verbatim material either side).
**On any conflict, the platform captures win** - over the 2026-08-14
announcement and every older local copy.

Corrections the capture forced (all propagated into tools + workflows + prompts 2026-08-26):

- **Rubric band 15-60** (the local copy had carried a narrower band); R11 updated, and R24's
  positive-weight cap is the real ceiling, see [[rubric-criterion-count]].
- **difficulty_check passes when worst-agent accuracy ≤ 80%** (fails as Easy only when both
  models exceed 80) - not "both under 80".
- **golden_solution_check = 3 agents, all must score 1.0000** - the [x, y, z] triples in oracle
  feedback are this check's raw scores.
- **LLM assistance on input files is now permitted** when the result is indistinguishable from
  a real document, tell-free and leak-free (creating-input-files.md) - supersedes the
  sanitization-only rule; the batch-provenance stop ([[package-hygiene-pipeline]]) still stands.
- New coded checks from the capture: **N1** (project/eval vocabulary in shipped
  content/names/metadata), **L2** (hidden sheets/rows, comments, tracked changes, input speaker
  notes), **T1** (tell log must be standalone, never in a package), **A1 extended** (named
  AI-blue hex range #1C3557-#2E4A6B, inputs + docx/pptx too).
- **geranium_safety_check**: nothing may teach materially unsafe professional practice  - 
  relevant if a task ever touches dosing, held parts, rigging.
- Human review caps at 5; adjudication fixes bypass human review ([[submission-tracking]]).
- The platform's own worked example (docs/submission/platform/task-example-wholesale-trade.md) contains a negative worded
  "does not contain" - contradicting its own affirmative-wording rule; imitate its MOQ pair
  (matched +4 universal / -4 existential, both affirmative) instead.

## The reviewer-side captures live here too (moved 2026-08-26)

`reviewer-guidelines-v5.1.md`, `reviewer-rubric.md`, `feedback-best-practices.md`,
`platform-review-form.md` and `task-example-omnichannel-routing.md` (an unannotated example golden,
filed reviewer-side because the Hub publishes it there) live in **docs/reviewer/platform/**. The guidelines were re-verified section by section against a fresh
capture on 2026-08-26 and matched verbatim, so there has been no drift since the 2026-08-20
transcription.

What the reviewer set states that the authoring docs do not:

- A reviewer **spot-checks only 2 to 3 rubric criteria** against the golden, so a mismatch anywhere
  else is a coin flip they may or may not catch. It is not a full verification.
- The EC gets **2 revision attempts**; a third failure is a reject.
- Reviewers may fix small things themselves (10 minutes per element, 30 if only one element needs
  changes) but **input files are locked in the platform and can never be edited**, so EVERY input
  problem routes to Needs Revision regardless of size. Input defects are therefore the most
  expensive class to ship.
- A **Suspected Duplicate or Template** flag exists for a task that reuses a prior task or template
  even when it is otherwise acceptable ([[task-uniqueness-check]]).
- **Bounded subjective criteria are explicitly valid** and a reviewer is told NOT to send one back
  for being subjective when it names the conditions and scores the reasoning. Only unbounded
  criteria come back.
- Reviewers do **not** review O*NET metadata; the evals team owns it (the M1/M2/M3 checks answer to
  that team, not to the reviewer).
- Six error classes drive the send-back label: LLM-Generated Input Files / Golden Solution, Input
  File Quality, Golden Solution Quality, Rubric Quality, Prompt Quality.
