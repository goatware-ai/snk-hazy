# Workflow 06 — Metadata and the platform form

The platform states the metadata fields once, in
`../platform/project-guidelines-v5.1.md#input-files` (the O*NET metadata block), and the
live form is `../platform/platform-submission-form.md`. The repo records only the values,
in each task's `metadata.json`; the reasoning behind a pick belongs in the build summary
and the feedback-log entry, never in the metadata file.

## House rules on top of the capture

- **Occupation:** pick only from `../platform/platform-wholesale-trade-occupations.md`,
  the table the sector match uses, and route by prompt type per
  `02-prompt-writing.md#house-notes-on-platform-wholesale-trade-occupationsmd` (M1, M3).
- **Tasks:** 3 to 5, each traceable to a clause of the prompt (M2). Name the clause in the
  build summary; if that sentence is hard to write, the pick is wrong.
- **Skills:** 3 to 5 from the Skills section. Several occupations' dropdowns carry no
  Mathematics (41-4012, 11-3071, 43-4041); the routing table says which.
- **Multimodal:** Yes if any input is a .pdf or .pptx (the form counts them as images).
  Decide from the zip, not the plan.
- **Input-file count:** the files inside the inputs zip. Record it and both booleans in
  `metadata.json`.
- **Time:** hours, by hand without an LLM, 3+ and consistent with `01-ideation.md`.

## Final screen

- [ ] Occupation is on the sector table and passed for this prompt type (M1, M3)
- [ ] 3–5 tasks, each named to a prompt clause (M2)
- [ ] 3–5 skills, from the Skills section (not Technology Skills)
- [ ] Multimodal boolean matches file contents (pdf/pptx = Yes)
- [ ] Web-search boolean matches the prompt
- [ ] Input-file count matches the zip
- [ ] Time estimate reflects 3+ hours of manual work

## House notes on platform-submission-form.md

Observations from building against the live form; the form facts themselves are in the
capture.

### Form fields

- Draft the prompt against the 3,000-character cap from the start; keep every rubric
  criterion under 500 characters (R1).
- Author every failure-mode criterion at −3 from the start; the form rejects −1 and −2 and
  an empty weight (R12).
- The Objectivity and Content tags are gone: never author or carry them anywhere.
- Fold companion outputs into the one deliverable (a briefing tab, an appendix). Mark a
  second file optional only if it truly is, and then the rubric must not require it (P1).
- Answer the "what LLM as a starting point" question truthfully; it asks about the golden.

### Oracle and quality-check behaviour observed live

- **Judges read spreadsheets with tools.** A formula cell without a cached value shows
  them only the formula string; a judge estimated `=1-H5/E5` at ~7.6% when it computes to
  11.7% and fired a contradiction penalty against the golden itself. Ship every xlsx with
  real cached values in each formula cell (generator libraries leave them empty) plus
  `fullCalcOnLoad`, so formulas stay live and readers see numbers (A9, A13, A17).
- **Negatives must scope exactly to the rows they should penalize.** A universal negative
  ("any populated price below floor") was legitimately TRUE on rows the golden correctly
  held unchanged (deferred families, frozen items whose margins already sat below floor)
  and fired against the golden. Evaluate every negative against every row class of the
  golden and carve out the classes that are supposed to violate it (R33, R37, R52).
- **The llm-only axis (≥ 3.5/5 per file) is dragged by co-occurring tells:** floating-point
  dust in stored data cells (`34.04799999999999` in a cost column; long decimals in cached
  formula cells are normal) (F1), 555-prefix phone numbers (H2), and invented company names
  from the LLM-favored lexicon ("Hartwell"-class, corroborating only). One isolated tell
  gets sole-signal suppression; two or more compound.
- **Judges decompose each criterion into atomic statements and verify every one inside the
  deliverable.** A criterion pairing a method with a value (a policy tier plus one item's
  reorder point) failed 1 of 3 runs with "Statement 4 was completely omitted" although the
  value sat in a 66-row table, scoring 0.9681 and failing the 3/3-at-1.0 rule. One
  verifiable statement per criterion (R54, R55); say where in the deliverable the value can
  be checked, in deliverable-neutral words; give dense tabs a parameters legend and one
  worked example row so the judge confirms the rule and the number without re-deriving them.
- **The Rubric Quality Review flags a criterion enumerating several independent record IDs
  as non-atomic** (one criterion listing six SKUs that could each pass or fail). Phrase the
  check over the class or split one criterion per item (R27, R85).

Next: `07-pre-submission-audit.md`
