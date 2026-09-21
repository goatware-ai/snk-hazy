# Workflow 04 — Golden Solution: the perfect, client-ready answer

The golden solution is the correct answer to your prompt — the deliverable you would
actually put in front of a client or your manager. It is both the reference the rubric
grades against and proof the task is doable.

**It is required.** Section 3 of the form carries a required `Completed Task Upload` under
the instruction to complete the task yourself, "the way the qualified professional you
described in your instruction would actually do it", and states that it is "your ground
truth and what you will build your rubric off of"
(`../platform/platform-submission-form.md#3-completed-task`). The guidelines PDF says three
times that the creator does not produce a solution; the form wins, and the contradiction is
recorded in `../platform/create-the-task-guidelines.md#0-known-conflict--the-completed-solution`.
Build the solution before drafting a single criterion: every rubric value is read off it
(`05-rubric.md`).

## The Output File List

The form asks for every file the completed task produces, by exact file name and format,
and the upload must match that list including extension
(`../platform/platform-submission-form.md#output-file-list`). Those names are the ones the
prompt already committed to, so all three (prompt, Output File List, uploaded file) have to
agree character for character. H5 codes it. Outputs are concrete professional work
products: a spreadsheet, report, presentation, design file or revised document
(`../platform/create-the-task-guidelines.md#4-define-expected-output-files`).

## A shape to model when the deliverable is a document

When the ask is an assessment rather than a model, the evaluation memo is the shape worth
copying: executive summary, then numbered findings each carrying a stated rule, an impact
count and one fully worked example, then an overall assessment and a remediation list.
Every figure in it reconciles exactly, which is the standard a golden solution is held to.

## Say what the work does not settle

Give the deliverable a short closing section naming what its own analysis cannot answer. The
strongest golden built on this desk closes on three: it prices the steel and not the other 38
per cent of the job, the published index is not the mill price actually paid, and the backtest
is one three-year window chosen from a series that has ranged far wider.

Nothing in that task's rubric scored the section, and it was still the clearest thing
separating that golden from every other one read. It is what evidentiary depth means in
practice, and it is the difference between a deliverable that answers the question and one
a manager can act on knowing the edges. Three sentences is enough; each one names a limit
and why the files cannot close it.

## Never let the file describe itself

The deliverable must not name its own category or production method — anywhere
(`../platform/style-guide-llm-tells.md`, all HIGH-severity tells; coded as N1):

- **File name:** never `golden_solution.xlsx`, `ai_output.pptx`, `model_response.pdf`
  — the prompt names the deliverable, and that name is what ships.
- **Body/headings:** no "Golden Solution", "AI-generated", "As requested, this
  document provides", no watermarks referencing AI or draft status.
- **Title slides:** a real professional title ("Q3 Operations Review: Midwest
  Region"), never the file category ("Output File: Strategic Analysis").

## The literal read: the golden against the inputs and the prompt

The coded fidelity checks read the rubric against the golden or the golden against itself.
The literal read is yours: go through the golden against the inputs and the prompt, one
claim at a time. Do that read before the rubric is drafted, and write the rubric so that each of these would lose
points (`05-rubric.md`):

- Every identifier the golden cites (invoice, PO, serial, work order) exists in a shipped
  input (G10).
- Every date the golden states is written in an input or derived by a stated rule; the
  deliverable's own dateline is a stated date too, so date it to the note it answers or
  leave it off (G18 for owner-dated action rows, G20 for every full date in the prose).
- The deliverable's date is not later than an action it schedules as done (G9).
- When the prompt says a document is to be signed, the golden carries that document with a
  signature-and-date line, not a table about it (G8).
- Every rule class in a policy input is applied to every record it governs, and no status
  the policy does not name is written (a read).
- A cost "since <date>" covers the partial period from that date (a read).
- An asset that leaves carries no duty after it leaves (a read).
- Every paragraph addressing one person restates that person's row: direction and amount,
  each bonus standing or coming back, splits, house lines (G19 codes the "X's quarter moves
  up/down" form; the rest is a hand read). Grade it with positives: a self-contradiction is
  diffuse, and a negative criterion has to name a specific observable outcome.
- Every displayed ratio and total re-derives from the displayed figures as displayed (G21,
  G5, G7).
- Comma rules held in every text cell and paragraph (A20, `02-prompt-writing.md`).

Write down, as you go, the exact value behind every claim you will later grade. The rubric
quotes those values verbatim and is never allowed to estimate them
(`05-rubric.md`), so a running list of figure-to-cell pairs saves a rebuild later.

## Packaging rules

- One flat `.zip` named `s-<task-name>.zip`; no subfolders; no empty files; no spaces or
  double extensions (H4). Output file name matches **exactly** what the prompt says to name
  the deliverable and what the Output File List says (H5).
- Every file **opens cleanly**: no XML errors, repair prompts, or corruption (A16). Open
  each one from the zipped copy before submitting.
- No revision residue: no tracked changes, no comments, no hidden sheets (L2).
- Every formula cell carries its cached value and the workbook is formula-live (A9, A13,
  A17); the reason is in `06-metadata.md#house-notes-on-the-live-form`.
- Run the package sequence in `07-pre-submission-audit.md#package-sequence` before zipping.

## Final screen before moving on

- [ ] Every part of the prompt answered; fact-checked; would score ~100 on the rubric;
      mostly human-edited
- [ ] Output File List written from the delivered files, matching the prompt exactly (H5)
- [ ] Client/manager-ready aesthetics; spreadsheets use live formulas with cached values
      (A9, A13, A17); no default LLM blues (A1); no paste walls (A5); no em dashes (A6)
- [ ] File name matches the prompt exactly (H5); opens cleanly (A16); flat zip (H4)
- [ ] **The literal read done:** G10, G18, G20, G9, G8, G19, G21 and the three hand reads
      above
- [ ] Comma rules held in every text cell and paragraph (A20)
- [ ] A list of every figure the rubric will cite, with the cell or paragraph it comes from

Platform note: judges read spreadsheets with tools and decompose each criterion
into statements they must find in the deliverable; the observed behaviour and the house
mitigations are in `06-metadata.md#house-notes-on-the-live-form`.

Next: `05-rubric.md`
