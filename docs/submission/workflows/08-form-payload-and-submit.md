# Workflow 08 — Form Payload and Submit

The last stage. The package is built and the audit in
[07-pre-submission-audit.md](07-pre-submission-audit.md) passes. What remains is getting it
onto the form without transcription errors, and submitting.

Everything on the form except the two file uploads is filled from one JSON file. Browsers
will not let a page set a file input from a path, so the two zips are attached by hand.

```bash
.venv/bin/python tools/form_payload.py drafts/NN-task-name
```

That reads the task folder and writes `form-payload.json` **inside that same folder**, next
to `instruction.md` and `metadata.json`. It works the same way on a promoted task in
`submissions/`. Then it prints what it found and anything it could not fill.

Three things about where it lands, all checked:

- **It is never zipped.** The two archives are flat builds from `inputs/` and `solution/`
  (`cd inputs && zip ../i-<task-name>.zip *`), and the payload sits above both, so it cannot
  reach the platform.
- **The gate ignores it.** The N1 leakage check walks only files directly inside `inputs/`
  and `solution/`; everything else is skipped. That matters because the payload contains the
  whole rubric, which is exactly what N1 exists to keep out of shipped files.
- **It is gitignored.** It is regenerated from the folder it sits in, so committing it would
  only create a second copy of the rubric that can go stale. Regenerate it rather than
  editing it; a hand-edit is lost the next time anyone runs the generator.

Load that file in the Hazy Helper extension (`tools/hazy-helper`, see its README to
install), press **Scan page**, then **Fill all**.

---

## Where each field comes from

The generator reads the task folder. Nothing is invented: a value it cannot source is left
empty and named in its report.

| Payload key | Read from | Fills |
|---|---|---|
| `domain` | `form-lists.md` → Domain and occupation | Section 1, Domain |
| `occupation` | `form-lists.md` → Domain and occupation | Section 1, Occupation |
| `occupation_code` | `form-lists.md` → O*NET code | nothing; carried for your reference |
| `task_instruction` | `instruction.md`, verbatim | Section 2, Task Instruction |
| `input_files[]` | `form-lists.md` → Input File List | Section 2, Input File List |
| `output_files[]` | `form-lists.md` → Output File List | Section 3, Output File List |
| `times.*` | `form-lists.md` → Times and tools | Section 3, the five time fields |
| `tools[]` | `form-lists.md` → Tools, split on `;` | Section 3, Tool list |
| `rubric[]` | `rubric-*.csv`, one row per criterion | Section 4, one rubric row each |

**`form-lists.md` is the source.** Someone wrote those entries for the form, in the form's
own shape, so the generator copies them rather than inferring anything. `metadata.json` is
only a fallback for a field `form-lists.md` does not carry, and the two disagreeing is
reported: the form gets `form-lists.md`.

`occupation_code` is the one key the extension never reads. The form asks for the
occupation by name, not by code, so the code rides along only so you can check it against
[onet-codes.md](../platform/onet-codes.md) without opening another file.

## The shape

```json
{
  "domain": "Management",
  "occupation": "Purchasing Managers",
  "occupation_code": "11-3061.00",
  "task_instruction": "I run the outbound freight desk here, and ...",
  "input_files": [
    "rate_pages.xlsx - the carrier's published rates for the period",
    "bills_q2.csv - every invoice paid in the quarter"
  ],
  "output_files": ["freight_audit_q2.docx"],
  "times": { "read": 25, "files": 85, "work": 240, "qa": 40, "total_hours": 6.5 },
  "tools": ["Excel", "Adobe Acrobat"],
  "rubric": [
    { "description": "The memo is addressed to the requester and covers the quarter.", "weight": 1 },
    { "description": "Overall formatting and style of the deliverable.", "weight": 5 }
  ]
}
```

Rules the extension relies on:

- **Every key is optional.** A missing key means that part of the form is left alone, which
  is how the per-section buttons work. An empty `rubric` writes no criteria rather than
  clearing the ones already there.
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
2. Load `form-payload.json` in the popup.
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
| `N row(s) beyond the M supplied were left untouched` | The form had more rubric rows than your rubric. Delete the extras by hand, or the formatting-and-style criterion is no longer last. |
| `N row(s) would not expand` | A rubric row stayed collapsed, so its fields could not be reached. Open it and fill that one by hand. |
| `total Xh is below the four parts` | Your own arithmetic does not hold. Fix the metadata, not the form. |
| `N of M entries are a bare file name with no description` | The popup is filling from a payload you loaded before regenerating the file. Press Load JSON again. |
| `found N boxes, expected 14` | The checklist changed. Read it, and update the capture in [platform-submission-form.md](../platform/platform-submission-form.md). |

## After submitting

Record the Taskboard UID in `metadata.json` and move the folder from `drafts/` to
`submissions/`. `/fetch-status` reconciles the rest.
