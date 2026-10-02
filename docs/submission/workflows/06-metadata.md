# Workflow 06 — Metadata and the platform form

The live form is `../platform/platform-submission-form.md`; the domain and occupation lists
are `../platform/domains-and-occupations.md`. The repo records only the values, in each
task's `metadata.json` and `form-lists.md`; the reasoning behind a pick belongs in the build
summary and the feedback-log entry, never in the metadata file.

## metadata.json

The build writes these keys, in this order. `tools/sync_metadata.py` later adds the form's
copies (`input_files`, `output_files`, `task_instruction`, `rubric`) from `form-lists.md`,
`instruction.md` and the rubric CSV; that full shape is in `08-fill-the-form-and-submit.md`.

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
rationale. Never hand-edit the synced copies; re-run the sync (M7).

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
The pair, and the domain that matches the occupation's job family, is chosen at ideation,
before the prompt is written (`01-ideation.md`).

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

Next: `07-pre-submission-audit.md`
