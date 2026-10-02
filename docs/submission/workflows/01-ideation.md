# Workflow 01 — Ideation: pick a task worth building

Everything downstream (prompt, files, solution, rubric) inherits the quality of this
decision. A weak concept cannot be rescued by good packaging. The desk's standing bar is in
`../house-rules.md` and what makes a task hard is in `../difficulty.md`; this page turns
both into a concept.

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
   never padding (M4, `../house-rules.md#difficulty`). The estimate is entered as four minute
   fields plus a total in hours (`06-metadata.md`), so decide now where each block goes.
2. **Unanswerable from the instruction alone, and not one-shot by a frontier model.** If a
   model drafts the golden correctly on the first try, the task is not hard enough. Test
   this against a sketch of the inputs before building files, not after.
3. **Difficulty lives in the files, not the prompt.** It comes from the source material and
   the reasoning needed to reconcile it, never from a longer or more prescriptive prompt.

## Judgment is what makes a task hard

`../difficulty.md` is the whole method: the reasons first builds came back too easy, the
design read, and the catalog of shapes reviewers asked for. At this stage it means:

- **Design the decisions before the files.** Name each decision the golden will make, the
  rule arm on each side of it, the look-alike, and the misreading that moves a graded figure.
  A concept that cannot carry five or six such decisions is too thin to build.
- **A candidate set beats volume.** Several candidates, each wrong one disqualified by a
  different property found only in the files, cost less to build than row count and are
  harder to solve. Extra rows that force no new decision buy build effort, not difficulty.
- **Build for the reviewer, not the check.** The platform's difficulty check is the floor;
  the reviewer returned every task in review as too easy on 2026-09-29, passed checks
  included.
- **Prefer real published data where the occupation offers it.** Real data carries its own
  ambiguity, discontinued series, revision flags and withheld cells; a fabricated pack has
  to invent that friction, and the absence shows (all-whole-dollar cost figures, A15).

## What makes a concept strong

- **Distributed information.** No single file gives the full answer; the solver must
  cross-reference several sources and reconcile conflicts between them. At least 2 input
  files, 3 or more strongly preferred (`03-input-files.md`), and the concept has to justify
  every one of them.
- **Realistic messiness.** Duplicates, inconsistent naming, cancelled records, competing
  priorities, missing information: the friction real work carries.
- **A real decision at stake.** Someone specific needs the output to decide something
  now: a vendor recommendation, a filing, a board deliverable, a compliance position.
- **Objectively verifiable.** There is a known correct answer (or, for genuine judgment
  calls, nameable conditions any sound answer must meet) that a rubric can grade against.

## Uniqueness

The platform publishes no map of accepted asks for this project, so uniqueness is checked
against this portfolio only (U1, U2). Before building, test the candidate's one-line
statement of what the solver does against every prompt in `submissions/`, `accepted/`,
`archived/` and `drafts/` (a batch's own earlier drafts included). Treat the occupation as
part of the identity: the same analytical ask under a different occupation is still the same
task when the solver's work is the same.

## Concepts to discard early

- Anything answerable from general knowledge or the prompt text alone.
- Workflows outside the US (unless a US company working internationally).
- Anything requiring proprietary tools, logins, or paywalled/restricted source material.
- Single-document summarization or reformatting dressed up as analysis.
- A workflow you have not personally done; the field-authenticity tells will surface it.
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
6. Why a frontier model fails it on the first pass: the decisions it turns on, each with the
   rule arm that holds, the look-alike that fails, and the misreading that moves a graded figure
   (`../difficulty.md#the-design-read`).

Next: `02-prompt-writing.md`
