# Workflow 06 — Metadata and the platform form

The live form is `../platform/platform-submission-form.md`; the field-by-field guidance is
`../platform/create-the-task-guidelines.md#1-select-the-onet-domain-and-sector` and
`#6-record-the-human-time-estimate`. The repo records only the values, in each task's
`metadata.json`; the reasoning behind a pick belongs in the build summary and the
feedback-log entry, never in the metadata file.

## metadata.json

Keys in this order:

```json
{
  "task_name": "transfer-station-closure-packet",
  "taskboard_uid": null,
  "domain": "Life, Physical, and Social Science",
  "onet_occupation": {
    "code": "19-2041.00",
    "title": "Environmental Scientists and Specialists"
  },
  "input_file_count": 4,
  "output_file_count": 1,
  "tools": ["Microsoft Excel", "Adobe Acrobat"],
  "time_read_minutes": 20,
  "time_files_minutes": 75,
  "time_work_minutes": 240,
  "time_qa_minutes": 45,
  "total_time_hours": 6.5,
  "built_with": "claude-fable-5",
  "build_session": "f26c2b60"
}
```

**Values only.** No justification prose, no alternates kept on file, no occupation
rationale; that reasoning goes in the build summary and the task's feedback-log.md.

`taskboard_uid` is always present and null until the operator fills it after submission; a
missing key and a null one are not the same thing. `built_with` and `build_session` follow
the house convention (`memory/task-metadata.md`, `memory/model-routing.md`).

There is no `sector` field. The form has no sector, and no task carries one.

## The fields, one at a time

### domain and onet_occupation

Both are single-select radio lists on the form, and an entry not visible on the form is not
available (`../platform/platform-submission-form.md#1-select-the-domain-and-sector`). The
14 domains and 64 occupations are in `../platform/domains-and-occupations.md`; the verified
code for each occupation is in `../platform/onet-codes.md#the-table`.

- `domain` is the form's spelling of the domain, verbatim.
- `onet_occupation.title` is the form's spelling of the occupation, verbatim, which is
  sometimes shorter than the official O*NET title.
- `onet_occupation.code` is the O*NET-SOC code confirmed on that occupation's own
  onetonline.org page. Eight of the 64 are detail codes ending `.01` to `.04`, and the four
  First-Line Supervisor titles are officially hyphenated
  (`../platform/onet-codes.md#four-traps`).
- Pick the domain that matches the occupation's O*NET job family, and avoid
  `Healthcare Practitioners / Support` unless nothing else fits.

The pair is chosen at ideation, before the prompt is written (`01-ideation.md`).

### input_file_count

The number of files inside the inputs zip, counted from the zip and not from the build
plan. Minimum 2, 3 or more preferred (`03-input-files.md`). It has to equal the number of
entries in the form's Input File List.

### tools

At least one entry, and at least one of them a non-AI tool the solver would reasonably use:
Excel, Photoshop, DaVinci, SolidWorks, LabVIEW
(`../platform/platform-submission-form.md#please-insert-any-tool-used-for-this-task`). Name
the real application, not a category ("Microsoft Excel", not "spreadsheet software"). The
list should be the tools the task genuinely needs; if the only honest entry is a text
editor, the deliverable is probably too thin.

### The five time values

Four integer minute fields plus a total in hours
(`../platform/platform-submission-form.md#times`):

| Key | Form field |
| --- | --- |
| `time_read_minutes` | Time to read and understand the prompt and requirements |
| `time_files_minutes` | Time to open, skim/search, and use the reference files |
| `time_work_minutes` | Time to perform the required work |
| `time_qa_minutes` | Time for verification/QA and final review |
| `total_time_hours` | Total time, decimals, at least the sum of the four converted |

These five key names are the ones `tools/gcheck/prompt_inputs/occupation.py` (M4) reads; any other spelling fails the gate as a missing field.

Rules that bind:

- All five are estimates for a qualified professional working **without any AI assistant**,
  from the prompt and the reference files.
- The four minute fields are integers. The total is a decimal number of hours and must be
  **at least** their sum converted; it may be higher.
- The total must be **over 3 hours**, which the form's Difficulty check reads. Under 5 is
  short of the guidelines' 5-to-10 target and worth a redesign rather than a rounding up.
- Exclude: learning missing domain knowledge, waiting on other people or approvals, breaks
  and unrelated distractions, and web research unless the prompt explicitly requires it.
- The values must be consistent with where `01-ideation.md` said the hours go. Inflating
  one field to clear the floor produces a profile that reads as padding.

## Final screen

- [ ] `domain` and `onet_occupation.title` spelled exactly as the form lists them
- [ ] `onet_occupation.code` confirmed on the occupation's own O*NET page
- [ ] Domain matches the occupation's job family
- [ ] `input_file_count` matches the zip and the Input File List
- [ ] At least one tool, named as a real application
- [ ] Four integer minute fields; total in hours ≥ their sum; total > 3
- [ ] `taskboard_uid` present and null until submitted
- [ ] No `sector` key anywhere
- [ ] `form-lists.md` at the task root carries the Input File List entries, the Output File List entry, the five time values, the tools, and the domain and occupation, with the same numbers as `metadata.json`

## House notes on the live form

Observations from building against the live form; the form facts themselves are in the
capture.

### Form fields

- The Input File List, the Output File List and the file names inside both zips are checked
  against the prompt's own wording. Write every list from the zip's directory listing.
- Weights go in the numeric field, never in the criterion text. Any non-zero integer from
  −5 to +5 is accepted, so a minor penalty can be authored at −1 without being rejected
  (R12).
- Fold companion outputs into the one deliverable (a briefing tab, an appendix). Mark a
  second file optional only if it truly is, and then the rubric must not require it (P1).
- The three in-form check panels (Task Instruction, Completed Task, Task Rubric) are
  advisory and state that they do not submit or block anything. The 14-box checklist in
  section 5 is what blocks. Each section still ends in **Run Evaluations and Continue** and
  the form ends in **Run Evaluations and Submit**, so evaluations do run at submit time.

### Judge behaviour observed on this desk

Carried over from earlier submissions and **not yet re-confirmed against this project's own
evaluations**. Treat them as precautions rather than as platform rules.

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
- **The llm-only axis is dragged by co-occurring tells:** floating-point
  dust in stored data cells (`34.04799999999999` in a cost column; long decimals in cached
  formula cells are normal) (F1), 555-prefix phone numbers (H2), and invented company names
  drawn from the LLM-favored lexicon (corroborating only). One isolated tell
  gets sole-signal suppression; two or more compound.
- **Judges decompose each criterion into atomic statements and verify every one inside the
  deliverable.** A criterion pairing a method with a value (a policy tier plus one item's
  reorder point) failed 1 of 3 runs with "Statement 4 was completely omitted" although the
  value sat in a 66-row table. One verifiable statement per criterion (R54, R55); say where
  in the deliverable the value can be checked, in deliverable-neutral words; give dense tabs
  a parameters legend and one worked example row so the judge confirms the rule and the
  number without re-deriving them.
- **A criterion enumerating several independent record IDs reads as non-atomic** (one
  criterion listing six SKUs that could each pass or fail). Phrase the check over the class
  or split one criterion per item (R27, R85).

Next: `07-pre-submission-audit.md`
