# Workflow 01 — Ideation: pick a task worth building

Everything downstream — prompt, files, solution, rubric — inherits the quality of this
decision. A weak concept cannot be rescued by good packaging. The platform's bar is stated
once in `../platform/project-guidelines-v5.1.md#the-quality-bar`; this page adds the house
reading of it and what the sector map says about crowding.

## The three gates every concept must clear

1. **The 3-hour floor, aim for 5.** By hand, without an LLM, from genuine analytical work,
   never padding (`../platform/project-guidelines-v5.1.md#the-quality-bar`). Enter the
   estimate in hours (`06-metadata.md`).
2. **A frontier model cannot do it perfectly today.** The difficulty check passes only when
   the worst-agent accuracy is at or under 80%
   (`../platform/auto-eval-feedback-guide.md#the-difficulty-check-accuracy-percentages`).
   If a model drafts the golden correctly on the first try with no meaningful edits, the
   task is not hard enough. Test this before file production, not after.
3. **Difficulty lives in the files, not the prompt.** If the task can be answered without
   opening the attachments, the files are decoration and the task is sent back
   (`../platform/project-guidelines-v5.1.md#your-prompt`).

## Judgment is what makes a task hard. Volume is not.

- **Row count buys build effort, not difficulty.** A 300-row task whose policy files hand
  over every formula was solved perfectly by both platform models; a 9-series task beat
  both. Before scaling a concept up, ask what decision the extra rows force that the first
  twenty did not; if none, keep it small and spend the effort on the decision.
- **Give them a candidate set to eliminate.** Put several candidates in front of the solver
  where each wrong one carries a different disqualifying property discoverable only in the
  files. The difficulty is in the set, not in the volume of any member, and it is cheaper
  to build than cross-referencing.
- **Prefer real published data where the sector offers it.** Real data carries its own
  ambiguity, discontinued series, revision flags and withheld cells; a fabricated pack has
  to invent that friction, and reviewers notice when it has not (all-whole-dollar cost
  figures, A15).

history:
`../../reference/workflow-history.md#reviews-of-other-contributors-tasks-2026-09-04-to-09-05`.

## What makes a concept strong

- **Distributed information.** No single file gives the full answer; the solver must
  cross-reference several sources and reconcile conflicts between them.
- **Realistic messiness.** Duplicates, inconsistent naming, cancelled records, competing
  priorities, missing information — the friction real work carries.
- **A real decision at stake.** Someone specific needs the output to decide something
  now: a vendor recommendation, a filing, a board deliverable, a compliance position.
- **Objectively verifiable.** There is a known correct answer (or, for genuine judgment
  calls, nameable conditions any sound answer must meet) that a rubric can grade against.

## Check the sector uniqueness map first

`../platform/wholesale-trade-uniqueness-map.md` is the platform's own running map of
accepted analytical asks for this sector: per-occupation crowding counts, fresh-idea
lists, and the 27 analytical-ask categories with the accepted asks under each. Steer
toward an ask, or an occupation, not yet covered — and remember the uniqueness diff also
runs against this contributor's own prior tasks (U1, U2), so cross off anything this
portfolio has already built even if the map lists it as fresh.

Pick the concept as an **ask-category × occupation cell**, not just an occupation. The
crowded categories, the near-empty ones and the per-occupation tag counts are in
`../platform/wholesale-trade-uniqueness-map.md#category-index`; read them fresh each time
rather than from a copy here. Test the candidate's dimension-2 sentence (what the solver
does, in one line) against the spent paths in `memory/task-uniqueness-check.md` before
building.

## Concepts to discard early

- Anything answerable from general knowledge or the prompt text alone.
- Workflows outside the US (unless a US company working internationally).
- Anything requiring proprietary tools, logins, or paywalled/restricted source material.
- Single-document summarization or reformatting dressed up as analysis.
- A workflow you have not personally done — the field-authenticity tells will surface it.

## Output of this stage

One selected concept, held to this shape before moving on:

1. The scenario: who needs the output, for whom, why now.
2. The deliverable: the one output file you can name.
3. The input files you will build and what each contributes to the answer.
4. Where the 3–5+ hours of manual work actually go.
5. Why a frontier model fails it on the first pass.

Next: `02-prompt-writing.md`
