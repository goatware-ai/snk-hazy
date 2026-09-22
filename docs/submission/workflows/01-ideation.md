# Workflow 01 — Ideation: pick a task worth building

Everything downstream — prompt, files, solution, rubric — inherits the quality of this
decision. A weak concept cannot be rescued by good packaging. The platform states its bar in
`../house-rules.md`; this page adds the house reading
of it.

## Start by picking the domain and the occupation

There is no assigned sector. Section 1 of the form is two single-select radio lists, 14
domains and 64 occupations, and a domain or occupation not visible on the form is not
available (`../platform/platform-submission-form.md#1-select-the-domain-and-sector`). Both
lists are in `../platform/domains-and-occupations.md`; the verified O*NET code for each
occupation is in `../platform/onet-codes.md#the-table`.

Pick the pair **before** writing a line of prompt, because the occupation is what makes the
scenario authentic and constrains what counts as day-to-day work:

- **Pick the occupation first, then the domain that matches its O*NET job family.** The
  domain radio is, in practice, the occupation's job family
  (`../platform/onet-codes.md#why-the-domain-list-is-what-it-is`). Treat
  `Healthcare Practitioners / Support` as a duplicate to avoid unless nothing else fits.
- **Watch the four traps** in `../platform/onet-codes.md#four-traps`: the four First-Line
  Supervisor rows are not Management, Inspectors and Machinists are Production, eight
  entries are `.0x` detail codes, and EMTs and Paramedics are separate occupations.
- **Favour occupations where a written work product is genuinely part of the job.** Most of
  the 64 are hands-on. Phlebotomists, Machinists and Home Health Aides do not spend the day
  producing an .xlsx. The four First-Line Supervisor rows, the manager rows, the scientist
  rows and the legal rows carry real document deliverables
  (`../platform/domains-and-occupations.md#what-this-means-for-task-design`).
- **Clinical, counselling and laboratory occupations raise the safety and privacy bar.** A
  task must never teach unsafe practice, and no input file may carry anything that reads as
  real patient data.

Record the pair in `metadata.json` (`06-metadata.md`).

## The three gates every concept must clear

1. **Over 3 hours by hand, aim for 5 to 10.** Without an LLM, from genuine analytical work,
   never padding. The form's Difficulty check wants estimated manual effort over 3 hours
   (`../platform/platform-submission-form.md#completed-task-checks-optional`) and the
   guidelines target 5 to 10 (`../house-rules.md`).
   The estimate is entered as four minute fields plus a total in hours (`06-metadata.md`),
   so decide at this stage where each of the four blocks of time actually goes.
2. **A frontier model cannot do it perfectly today.** The guidelines' key rule: a model
   should not be able to produce a good answer by reading the instructions alone without the
   input files. If a model drafts the golden correctly on the first try with no meaningful
   edits, the task is not hard enough. Test this before file production, not after.
3. **Difficulty lives in the files, not the prompt.** If the task can be answered without
   opening the attachments, the files are decoration and the task is sent back
   (`../platform/platform-submission-form.md#2-metadata`). Difficulty
   comes from source materials and the reasoning required to reconcile them, never from
   making the prompt longer or more prescriptive.

## Judgment is what makes a task hard. Volume is not.

- **Row count buys build effort, not difficulty.** A 300-row task whose policy files hand
  over every formula was solved perfectly by both platform models; a much smaller one built
  on a single hard decision beat both. Before scaling a concept up, ask what decision the
  extra rows force that the first twenty did not; if none, keep it small and spend the effort on the decision.
- **Give them a candidate set to eliminate.** Put several candidates in front of the solver
  where each wrong one carries a different disqualifying property discoverable only in the
  files. The difficulty is in the set, not in the volume of any member, and it is cheaper
  to build than cross-referencing.
- **Never label the trap.** A column that states a record's exception with the section it
  breaks, or a flag that names the rule, hands the graded call to the solver; the platform's
  difficulty check failed a four-bid evaluation built that way on 2026-09-22 (two of four
  weak-model attempts cleared the rubric). Put the condition in the record's own prose, in a
  second file that has to be reconciled, or under a status column a reader can skip, and make
  every numbered rule an input carries decide something (L7 for the labelled column, PR21 for
  the walk; `memory/difficulty-check-lessons.md` carries the case).
- **Prefer real published data where the occupation offers it.** Real data carries its own
  ambiguity, discontinued series, revision flags and withheld cells; a fabricated pack has
  to invent that friction, and the absence shows (all-whole-dollar cost figures, A15).

## What makes a concept strong

- **Distributed information.** No single file gives the full answer; the solver must
  cross-reference several sources and reconcile conflicts between them. At least 2 input
  files, 3 or more strongly preferred (`03-input-files.md`), and the concept has to justify
  every one of them.
- **Realistic messiness.** Duplicates, inconsistent naming, cancelled records, competing
  priorities, missing information — the friction real work carries.
- **A real decision at stake.** Someone specific needs the output to decide something
  now: a vendor recommendation, a filing, a board deliverable, a compliance position.
- **Objectively verifiable.** There is a known correct answer (or, for genuine judgment
  calls, nameable conditions any sound answer must meet) that a rubric can grade against.

## Uniqueness

The platform publishes no map of accepted asks for this project, so uniqueness is checked
against this portfolio only (U1, U2). Test the candidate's dimension-2 sentence (what the
solver does, in one line) against the paths this desk has already spent
before building, and treat the occupation as part of the identity: the same analytical ask
under a different occupation is still the same task if the solver's work is the same.

## Concepts to discard early

- Anything answerable from general knowledge or the prompt text alone.
- Workflows outside the US (unless a US company working internationally).
- Anything requiring proprietary tools, logins, or paywalled/restricted source material.
- Single-document summarization or reformatting dressed up as analysis.
- A workflow you have not personally done — the field-authenticity tells will surface it.
- Anything that cannot be reached from one of the 14 domains and 64 occupations. The list
  is closed: there is no free-text alternative, so a concept that does not fit an entry
  cannot be submitted at all.

## Output of this stage

One selected concept, held to this shape before moving on:

1. The domain and occupation, with the occupation's O*NET code.
2. The scenario: who needs the output, for whom, why now.
3. The deliverable: the one output file you can name.
4. The input files you will build (at least 2, 3+ preferred) and what each contributes to
   the answer.
5. Where the four blocks of manual time actually go, and the total in hours.
6. Why a frontier model fails it on the first pass.

Next: `02-prompt-writing.md`
