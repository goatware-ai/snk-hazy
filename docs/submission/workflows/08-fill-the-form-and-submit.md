# Workflow 08 — Fill the Form and Submit

The last stage. The package is built and the audit in
[07-pre-submission-audit.md](07-pre-submission-audit.md) passes. What remains is getting it
onto the form without transcription errors, and submitting.

Everything on the form except the two file uploads is filled from the task's own
`metadata.json`. Browsers will not let a page set a file input from a path, so the two zips
are attached by hand.

```bash
.venv/bin/python tools/sync_metadata.py drafts/NN-task-name
```

That folds the form's fields into the folder's `metadata.json`, leaving `task_name`,
`taskboard_uid`, `built_with` and `build_session` untouched, then prints what it found and
anything it could not fill.

`metadata.json` is the only file the helper needs. It already carried the build record; it
now carries the form's fields too, so there is no second file to keep in step.

**It holds copies.** `task_instruction` copies `instruction.md`, and `rubric` copies the
rubric CSV. That duplication is deliberate, because the helper can only be handed one file,
and it is why check **M7** exists: it errors when a copy stops matching its source. Re-run
the sync after editing either source, and never hand-edit the copies.

Load `metadata.json` in the Hazy Helper extension (`tools/hazy-helper`, see its README to
install), press **Scan page**, then **Fill all**.

---

## Where each field comes from

The generator reads the task folder. Nothing is invented: a value it cannot source is left
empty and named in its report.

| metadata.json key | Read from | Fills |
|---|---|---|
| `domain` | `form-lists.md` → Domain and occupation | Section 1, Domain |
| `onet_occupation.title` | `form-lists.md` → Domain and occupation | Section 1, Occupation |
| `onet_occupation.code` | `form-lists.md` → O*NET code | nothing; carried for your reference |
| `task_instruction` | `instruction.md`, verbatim | Section 2, Task Instruction |
| `input_files[]` | `form-lists.md` → Input File List | Section 2, Input File List |
| `output_files[]` | `form-lists.md` → Output File List | Section 3, Output File List |
| `time_*_minutes`, `total_time_hours` | `form-lists.md` → Times and tools | Section 3, the five time fields |
| `tools[]` | `form-lists.md` → Tools, split on `;` | Section 3, Tool list |
| `rubric[]` | `rubric-*.csv`, one row per criterion | Section 4, one rubric row each |

**`form-lists.md` is the source.** Someone wrote those entries for the form, in the form's
own shape, so the generator copies them rather than inferring anything. Where `form-lists.md` and the existing metadata disagree on domain or occupation, the
sync takes `form-lists.md` and reports the change.

`occupation_code` is the one key the extension never reads. The form asks for the
occupation by name, not by code, so the code rides along only so you can check it against
[onet-codes.md](../platform/onet-codes.md) without opening another file.

## The shape

```json
{
  "task_name": "carton-bid-evaluation",
  "taskboard_uid": "bd686eba-...",
  "domain": "Management",
  "onet_occupation": { "code": "11-3061.00", "title": "Purchasing Managers" },
  "input_files": [
    "rate_pages.xlsx - the carrier's published rates for the period",
    "bills_q2.csv - every invoice paid in the quarter"
  ],
  "output_files": ["freight_audit_q2.docx - the audit memo"],
  "input_file_count": 2,
  "output_file_count": 1,
  "tools": ["Microsoft Excel", "Microsoft Word"],
  "time_read_minutes": 25,
  "time_files_minutes": 85,
  "time_work_minutes": 240,
  "time_qa_minutes": 40,
  "total_time_hours": 6.5,
  "task_instruction": "I run the outbound freight desk here, and ...",
  "rubric": [
    { "description": "The memo is addressed to the requester and covers the quarter.", "weight": 1 },
    { "description": "Overall formatting and style of the deliverable.", "weight": 5 }
  ],
  "built_with": "claude-fable-5-1",
  "build_session": "afce3ffb"
}
```

Rules the extension relies on:

- **Every key is optional.** A missing key means that part of the form is left alone, which
  is how the per-section buttons work. An empty `rubric` writes no criteria rather than
  clearing the ones already there.
- **The helper reads metadata's own shape.** The occupation nested under `onet_occupation`,
  the times as flat `time_*_minutes` keys. A flat `occupation` / `times` object still works,
  so a hand-written payload is still a valid thing to paste.
- **`input_files` and `output_files` are plain strings**, one per row, not objects. The form
  wants `name - what it contains`, so that whole line is one string.
- **`times` values are numbers**, minutes for the first four and decimal hours for the
  total. The form's fields cap at five characters, so a total of `10.25` fits and anything
  longer is truncated by the browser; the extension reads each value back and reports one
  that did not fit.
- **`rubric[].weight` is a non-zero integer from -5 to +5.** A blank weight is allowed and
  leaves that row's weight empty, which the form permits and the audit does not.
- **Order is meaningful in `rubric`.** Rows are written in array order, and the form
  requires the general formatting-and-style criterion to be **last**, so it must be the last
  element. The generator preserves CSV order.

## What it checks while it reads

**The file lists against the folders.** Every name in the Input File List must be a file in
`inputs/`, and every file in `inputs/` must be named in the list. Same for outputs and
`solution/`. The form calls a mismatch here one of the most common reasons a submission gets
sent back, and it is invisible until the platform rejects it, so both directions are
reported.

**`form-lists.md` against `metadata.json`.** They are written separately and can drift. A
disagreement on domain, occupation or code is reported.

**The arithmetic.** The total must be at least the four minute figures converted to hours,
and every time value must fit the form's five-character fields.

**The last criterion.** Rows are typed in array order, so the general formatting-and-style
line has to be last in the CSV.

## When there is no form-lists.md

The generator falls back to naming the files in `inputs/` and `solution/` and hunting
`instruction.md` for a sentence that describes each input **on its own**. A sentence naming
several inputs is a file list, not a description, so it is rejected; every input would
otherwise get the same meaningless line. Anything it cannot source comes out bare and is
named in the report. Writing `form-lists.md` is the better answer.

## Filling

1. Open the submission form. The extension opens each section itself.
2. Load the task's `metadata.json` in the popup.
3. **Scan page.** It reports every section as open, closed or not found, what section 1
   currently has selected, how many rubric rows exist, and how many checklist boxes are
   ticked. Nothing is written. Read it before going further.
4. **Fill all**, or one section at a time while you are still learning to trust it.
5. Attach `i-<task-name>.zip` to the Section 2 uploader and `s-<task-name>.zip` to the
   Section 3 uploader.
6. Read the form top to bottom against the payload.
7. Work the checklist in Section 5 yourself. The extension can tick all fourteen, behind a
   confirmation, but each box is a statement about your package and ticking it here does not
   make it true. Section I of the audit maps every box to the check that verified it.
8. **Run Evaluations and Submit.**

## What the fill reports, and what to do about it

The popup prints one line per section, and any problem under it. These are the ones worth
knowing before you see them:

| It says | It means |
|---|---|
| `domain reads back as "X", not "Y"` | The click landed on the wrong option, or the form rejected it. Section 1 arrives with a domain already selected, so this check exists precisely because "something is selected" proves nothing. |
| `"10.255" did not fit (maxlength 5)` | The field truncated your value. Round the total and regenerate. |
| `N removed` on the rubric line | The form held more rows than your rubric has criteria, and the surplus was deleted from the end. Expected on a revision that drops criteria. |
| `N row(s) would not open: 4, 7, 9` | Those rubric rows stayed collapsed and could not be written. Open them on the form and fill those by hand. |
| `total Xh is below the four parts` | Your own arithmetic does not hold. Fix the metadata, not the form. |
| `N of M entries are a bare file name with no description` | The popup is filling from a payload you loaded before regenerating the file. Press Load JSON again. |
| `found N boxes, expected 14` | The checklist changed. Read it, and update the capture in [platform-submission-form.md](../platform/platform-submission-form.md). |

## After submitting

Record the Taskboard UID in `metadata.json` and move the folder from `drafts/` to
`submissions/`. `/fetch-status` reconciles the rest.
