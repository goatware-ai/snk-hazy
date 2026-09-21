# Workflow 02 — Prompt Writing: your voice, a real situation

The platform states the prompt rules twice and they agree: the field's own bullets and
placeholder in
`../platform/platform-submission-form.md#task-instruction`, and the required properties,
the voice and the overspecification warning in
`../platform/create-the-task-guidelines.md#2-write-the-task-instruction`. The tell list is
`../platform/style-guide-llm-tells.md` and `../../reference/llm-prose-tells.md`. This page
holds only what the house adds on top. Coded rules carry their check id; the one-line
statement of every id is `../../rules.md`.

## What the form requires, in the order it asks for it

Checklist items 1 to 6 are submit-blocking confirmations of exactly these
(`../platform/platform-submission-form.md#5-before-you-submit--task-creation-checklist`):

1. A named role, a named organization, and a reason the work is happening today.
2. Every input file named, with a phrase on what it contains.
3. The exact deliverable: file type, plus any length or structural requirement (page limit,
   tab count, required columns, naming convention).
4. Real scenario constraints where they belong: budget, deadline, headcount, threshold.
   These are wanted, not a leak.
5. **No number, name or finding that the reader can only get by working through the input
   files.** Those are what the exercise tests; they live in the rubric.
6. Fully self-contained. The solver never sees the rubric, and neither does a model.

Item 5 and item 6 pull against each other, and that tension is the craft of this page: say
everything needed to produce the answer, and nothing that is the answer.

## House rules the platform does not state

- **One primary deliverable, named** (P1). Two co-equal required output files get sent back;
  fold companion outputs into the single artifact (a briefing tab, an appendix). Mark a
  second file optional only if it truly is, and then the rubric must not require it.
- **Every input file named in the opening paragraph, woven into the narrative** (P2, P3).
  A separate "here are the pulls" inventory paragraph reads as machine-written even when
  every file is named.
- **Gloss at most one or two files** (P5). Saying what most named files are *for* fails the
  human-voice read; name them all in one run and gloss only the one or two whose
  distinction is unclear.
- **The file names in the prompt must match the Input File List and the ZIP exactly**,
  character for character including case and extension. The form calls a mismatch here one
  of the most common reasons a submission gets sent back
  (`../platform/platform-submission-form.md#input-file-list`).
- **Ask for the answer the requester does not want.** Name the adverse result the requester
  is prepared to hear and make the files capable of producing it: it gives the requester a
  real motive, forces the golden to carry a finding against interest, and gives the rubric a
  criterion a model playing along will miss.

## The opening frame (P4, P6)

The first paragraph or two, roughly the first 900 characters, must carry three things,
written as the requester talking, never as an instruction to the solver:

- **P4a the place.** The state, or the country plainly. A town name does not carry it.
- **P4b the role.** What the requester does. "my desk" does not count.
- **P4c the expertise.** What the reader is expected to already know, in the terms of the
  occupation you selected in `01-ideation.md`.
- **P4d not a persona.** Never "You are a financial analyst. Utilizing your expertise ...".

And none of it as a self-introduction to a coworker (P6):

- The place rides on something the work touches ("the two county transfer stations we run
  out of Bakersfield"), never "<Organization>, a <kind of> operation in <Town>, <State>"
  told to a colleague who works there.
- The role is ownership of the problem ("the corrective actions are mine to close"), never a
  job description.
- The experience is the reason for the handoff, addressed to the reader ("you have run
  sampling programs of your own"), never "whoever picks this up should have ...", which
  gates a stranger.
- Every event the opening names says in the same sentence why it matters to the work.

✅ "The state inspector is back on site the first week of December and the three open
corrective actions from the August visit have to be closed before then. I run environmental
compliance for the two county transfer stations we operate out of Bakersfield, California,
so the closure packet is mine to put together, and I am handing this to you because you have
run sampling programs of your own and will not need the permit conditions walked through."

P4 reads the three parts out of the opening window and fires separately on the persona
shape; P6 fires on the self-introduction sentence and the "whoever picks this up" gate. The
rest is a read. history:
`../../reference/workflow-history.md#open-order-cleanup-rejected-on-prompt-quality-2026-09-02`,
`../../reference/workflow-history.md#lift-truck-fleet-plan-rejected-at-first-human-review-2026-09-05`.

## Sentence mechanics (A20)

- A comma before and/but/so/or joining two independent clauses.
- Never a third independent clause in one sentence.
- The serial comma in every list.

A20 codes the first two shapes; the serial comma, the comma splice and compound sentences
inside a subordinate clause are a read. It applies to the prompt, every input document,
every golden text cell and the rubric. history:
`../../reference/workflow-history.md#lift-truck-fleet-plan-rejected-at-first-human-review-2026-09-05`.

## Overspecification giveaways beyond step-by-step

The guidelines call overspecification of HOW the most common mistake: if the instruction
reads like a template to fill in rather than a task to perform, it is too prescriptive.
Reviewers also send back these subtler forms:

- Saying what a file is for (P5); name it and what it contains, and let how it enters the
  analysis be the solver's discovery.
- Outlining the sections of a deliverable component; the component and its audience are
  enough.
- Warning about data pitfalls; if spotting bad rows or an atypical period is graded, the
  warning hands it over.
- Stating derived parameters; a horizon, cutoff or scope the solver computes from scenario
  facts must not appear as a given.
- Enumerating the decision framework an input file teaches (the disposition options, the
  cap that binds).
- An inventory paragraph of file names (P3).

At the same time the prompt must be complete: every requirement the rubric grades is stated
or is a thing any competent practitioner would know to do (R4, R13). Hidden requirements are
a rubric defect, not difficulty. history:
`../../reference/workflow-history.md#weldon-transition-buy-reviewer-feedback-august-2026`,
`../../reference/workflow-history.md#yearend-deadstock-plan-reviewer-feedback-august-2026`.

## The prompt has to fit the occupation you selected

Section 1 of the form is chosen before the instruction is written, and the instruction is
read against it. Write the work the selected occupation actually does, in that occupation's
vocabulary, and name the deliverable for that work. Where the occupation's O*NET job family
and the form's domain list disagree, the form's domain choice governs
(`../platform/domains-and-occupations.md#what-this-means-for-task-design`).

If the prompt drifts into a neighbouring occupation's duties while writing, change the
selection rather than the wording: a prompt whose center of gravity is somewhere else does
not become a fit through rephrasing.

## Final screen before moving on

- [ ] Reads like you talking to a colleague; passed the read-aloud test (A10, P7)
- [ ] Named role, named organization, and why this is happening today (checklist 1)
- [ ] **P4:** the opening names the state (or the US), what the requester does, and the
      expertise the reader brings, in the requester's voice
- [ ] **P6:** none of that is a self-introduction to a coworker; every event the opening
      names says in the same sentence why it matters
- [ ] **A20:** a comma before and/but/so/or joining two clauses, never three clauses in one
      sentence, a serial comma in every list
- [ ] One output file named exactly (P1), with its format and every length or structural
      requirement stated (checklist 3)
- [ ] Every input file named in the opening paragraph (P2, P3, checklist 2), at most one or
      two glossed (P5), names matching the Input File List and the ZIP exactly
- [ ] Real scenario constraints present: budget, deadline, headcount, threshold
      (checklist 4)
- [ ] No number, name or finding that can only come from working the files (checklist 5)
- [ ] Not answerable without the input files; self-contained without the rubric
      (checklist 6)
- [ ] What, not how: none of the six giveaway forms above
- [ ] No spelling or grammar errors

Next: `03-input-files.md`
