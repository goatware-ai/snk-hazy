# Hazy Helper

A Chrome extension that fills the task submission form from a finished task package.
It never touches file uploads.

## Install

1. Open `chrome://extensions` and turn on **Developer mode**.
2. **Load unpacked**, and pick this folder (`tools/hazy-helper`).
3. Pin it, so the popup is one click from the form.

It asks for `activeTab`, `scripting` and `storage`. It runs only on the tab you have open
when you press a button, talks to nothing off your machine, and stores only the payload you
last pasted, so it survives closing the popup.

## Use

```bash
.venv/bin/python tools/form_payload.py drafts/01-my-task
```

That writes `drafts/01-my-task/form-payload.json` and prints a short report: how many inputs
and criteria it found, the rubric's positive and negative totals, and anything it could not
fill in. Then:

1. Open the submission form. The extension opens each section itself, so you do not need
   to expand them first.
2. Open the popup, **Load JSON**, pick that file.
3. Press **Scan page** first. Read what it found.
4. Press **Fill all**, or fill one section at a time.
5. Attach both zips yourself, and read the form before you submit.

To fill only the rubric, skip the generator and **Load rubric CSV** with the task's
`rubric-*.csv` directly. It reads the repo's own `NUMBER,CRITERION,WEIGHT` format.

## What it fills, and how much to trust each part

| What | How it is found | Confidence |
|---|---|---|
| The five sections | `data-testid="section-<heading>"`, open state from bare `data-open` / `data-closed` | **Verified** |
| Domain, Occupation | `field-radio-domain` / `-occupation`, then `radio-option-container-<label>` | **Verified** |
| Task Instruction | `field-task-prompt` > `textarea#task-prompt` | **Verified** |
| Input File List | `field-repeatabletextarea-input_file_list` | **Verified** |
| Task Rubrics rows | `data-testid` on each repeatable row | **Verified** |
| Output File List, Tools | their own `field-repeatabletextarea-...` containers | **Verified** |
| The five times | `field-textarea-time_...`, one testid each | **Verified** |
| The 14 checkboxes | `field-multiselect-confirm_...`, `role="checkbox"` per box | **Verified**, opt-in |
| File uploads | never touched | n/a |

Every section is verified against a capture of the live form. Scan is still worth pressing
first: it reports each section's state and what it found, without writing anything.

**The repeatable lists do not all start the same way.** The input and output file lists
arrive with no rows at all: a place for them, an Add button, nothing else. Tools arrives with
one row already there. So rows are counted inside the field container and created only as
needed, which avoids both writing nothing and leaving a stray empty row.

**The two repeatable components mark their rows differently.** The rubric numbers rows as
`-instance-N`; the file and tool lists use `field-repeatable-textarea`. Both count as a row.

**The rubric arrives with three rows, but only the first is open.** Rows 2 and 3 have no
panel in the DOM at all, so they carry no description and no weight field. Rows are counted
by their containers, which exist either way, and every row is expanded before anything is
written. Counting only rows that already show a field sees one row, then adds a fresh row
per criterion on top of the three you already had.

**Expanding never clicks a dialog trigger.** The "Show criteria" buttons in sections 2 and 3
also carry `aria-expanded="false"`, so the expand pass skips anything with `aria-haspopup`.

**The checklist boxes are not checkboxes.** Each is a div with `role="checkbox"` and its
whole text in `aria-label`, with no `<label>` wrapper, so `aria-checked` is the only record
of state. Every tick is read back, and any box that would not tick is named rather than
counted. Scan lists the ones still off, by their text.

**The five time fields are textareas with `maxlength="5"`,** not number inputs. A total of
`10.25` fits exactly and anything longer is truncated by the browser without a word, so every
write is read back and a value that did not fit is reported. The helper also checks the
form's own arithmetic before you submit: the total must be at least the four minute figures
converted to hours, and over the three-hour difficulty floor.

Two things about section 1 are worth knowing, because both would be easy to get wrong. The
element you can click is the `button[role="radio"]`; the `<input type="radio"><` beside it is
`aria-hidden` and clipped to a 1px box. And the domain arrives with an option **already
selected**, so "it is checked" is no evidence that the helper checked it. Every pick is
confirmed by reading the group back, and the popup prints what the form actually holds
rather than what was asked for.

An option can also be matched through its slug. Each option's button carries
`value="<label lowercased, every run of non-alphanumerics turned into one underscore>"`, so
`Healthcare Practitioners / Support` is `healthcare_practitioners_support`. That makes
matching survive a difference in punctuation or spacing between your payload and the form.

Sections matter more than they sound. Every write opens its own accordion first and then
searches only inside it, which is what stops a label as generic as "File" from matching in
the wrong section. **Scan page** reports each section as open, closed or not found, followed
by every labelled field it can see, without writing anything. Press it first.

The checklist heading contains an em dash. Matching falls back to comparing text with all
dash characters folded together, so a capture that turns it into an en dash or a hyphen
still matches; the difference is invisible on screen and would otherwise be a silent miss.

## After you regenerate a payload, press Load JSON again

The popup keeps the last payload you loaded in browser storage and restores it when you
reopen it. That is convenient and it is also the one trap in this tool: regenerating
`form-payload.json` on disk does **not** change what the popup holds. The file and the popup
drift apart, and the fill still succeeds, just with the old values.

Three things now make that visible rather than silent:

- Opening the popup prints a one-line summary of the payload it restored.
- Loading a file prints the same summary for the new one.
- Filling either file list warns when entries are bare file names with no description.

If any of those mention bare file names, press **Load JSON** and pick the file again.

**Changing the extension's own code needs a reload too.** Edits to `page.js` or `popup.js`
do not reach a loaded unpacked extension until you press the reload arrow on its card at
`chrome://extensions`.

## The checklist is deliberately separate

The fourteen boxes in the last section are statements about your package: that the
instruction is self-contained, that no rubric criterion asserts something the inputs do not
support, that every listed file was uploaded. Ticking them is an attestation, so it is never
part of **Fill all**. It is its own button, it asks for confirmation, and you should read the
boxes rather than trust it.

## Why uploads are excluded

A page cannot put a file into an upload field from a path. Browsers forbid it, and that is a
security boundary rather than a limitation worth working around. Attach `i-<task>.zip` and
`s-<task>.zip` by hand, and check the names inside each match the lists you just filled.

## When the form changes

The rubric selectors are read out of `page.js` by the test, so the two cannot drift:

```bash
.venv/bin/python tools/hazy-helper/test_selectors.py
```

It walks `rubric-sample.html` and checks every rule `page.js` relies on for the rubric: that
instance containers exist, that each row yields exactly one description textarea and one
weight input bounded to -5..+5, that the add-a-row button is findable by its text, and that
the fallback path finds the same rows as the primary one.

It then walks `sections-sample.html` and checks the accordions: that every entry in the
`SECTIONS` map is found, that open and closed are read from bare attributes rather than
values, and that the checklist heading still matches with an en dash or a hyphen in place of
its em dash.

It walks `section1-sample.html`: both radio groups, the option containers, that each option's
clickable control is a button and its paired input is `aria-hidden`, that every option's
`value` matches the slug rule, and that a domain arrives pre-selected.

It walks `section2-sample.html` and checks that the `FIELD` map in `page.js` still names the
testids the form carries, that the instruction textarea is `#task-prompt` and required, that
the uploader is a real file input so it gets skipped, and above all that the Input File List
is reachable **while it holds no rows**.

It walks `section3-sample.html`: that all five entries in `TIME_FIELD` resolve, that
each is a textarea carrying `maxlength="5"`, that Tools arrives with exactly one row marked
`field-repeatable-textarea`, that the output list arrives with none, and that one time label
really does appear three times in that section, which is the reason none of it is matched on
label text.

It also asserts the thing that shapes the whole design: **the description and weight ids are
duplicated across rubric rows**, so `getElementById` returns the first row every time. Every
lookup is scoped to a row's own instance container instead. If that test starts failing, the
form has moved. Re-capture the view into `rubric-sample.html` and fix the selectors at the
top of `page.js`.

To promote a section's fields from inferred to verified, capture that view into this folder
the same way and add cases to the test. Until then, Scan is the check.

## Files

| File | What it is |
|---|---|
| `manifest.json` | MV3 manifest |
| `popup.html` / `popup.js` | the panel, payload handling, CSV parsing, rendering |
| `page.js` | everything that touches the form, injected into the tab |
| `test_selectors.py` | proves the section and rubric selectors still match the captures |
| `rubric-sample.html` | the rubric section with every row expanded |
| `section4-sample.html` | the same section on arrival: three rows, only the first open |
| `section5-sample.html` | the fourteen checklist boxes, as role="checkbox" divs |
| `sections-sample.html` | the five section accordions, with the heading's dash written three ways |
| `section1-sample.html` | the domain and occupation radio groups, as the form renders them |
| `section2-sample.html` | the instruction, the empty input file list, and the uploader |
| `section3-sample.html` | the five time fields, the pre-populated tools row, the output list |
| `icons/make-icons.py` | regenerates the icons |
