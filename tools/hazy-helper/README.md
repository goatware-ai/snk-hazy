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

1. Open the submission form and expand the section you are about to fill.
2. Open the popup, **Load JSON**, pick that file.
3. Press **Scan page** first. Read what it found.
4. Press **Fill all**, or fill one section at a time.
5. Attach both zips yourself, and read the form before you submit.

To fill only the rubric, skip the generator and **Load rubric CSV** with the task's
`rubric-*.csv` directly. It reads the repo's own `NUMBER,CRITERION,WEIGHT` format.

## What it fills, and how much to trust each part

| Section | How fields are found | Confidence |
|---|---|---|
| Task Rubrics | data-testid on each repeatable row | **Verified** against a capture of the live form |
| Domain, Occupation | option text on radio inputs | Inferred |
| Task Instruction | label text | Inferred |
| Input / Output File List | the row's "Add another ..." button | Inferred |
| Times, Tools | label text | Inferred |
| The 14 checkboxes | every checkbox on the page | Opt-in only |
| File uploads | never touched | n/a |

Only the rubric is verified. When this was written, the rubric view was the only part of the
form whose DOM had been captured, so everything else is matched on the label text recorded
in `docs/submission/platform/platform-submission-form.md`. That is why **Scan page** exists
and why you should press it first: it lists every labelled field it can see, without writing
anything, so you can tell whether a section will match before you let it fill.

If a section comes back empty, the usual cause is that its accordion is collapsed. The
extension expands what it can, but open the section yourself and scan again.

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

It walks `rubric-sample.html`, a capture of the live rubric view, and checks every rule
`page.js` relies on: that instance containers exist, that each row yields exactly one
description textarea and one weight input bounded to -5..+5, that the add-a-row button is
findable by its text, and that the fallback path finds the same rows as the primary one.

It also asserts the thing that shapes the whole design: **the description and weight ids are
duplicated across rubric rows**, so `getElementById` returns the first row every time. Every
lookup is scoped to a row's own instance container instead. If that test starts failing, the
form has moved. Re-capture the view into `rubric-sample.html` and fix the selectors at the
top of `page.js`.

To extend coverage to the other sections, capture one of those views into this folder the
same way and add cases to the test. Until then, treat Scan as the check.

## Files

| File | What it is |
|---|---|
| `manifest.json` | MV3 manifest |
| `popup.html` / `popup.js` | the panel, payload handling, CSV parsing, rendering |
| `page.js` | everything that touches the form, injected into the tab |
| `test_selectors.py` | proves the rubric selectors still match the captured DOM |
| `rubric-sample.html` | the captured rubric view; the only record of the real DOM |
| `icons/make-icons.py` | regenerates the icons |
