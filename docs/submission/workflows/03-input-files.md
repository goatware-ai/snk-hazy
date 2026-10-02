# Workflow 03 — Input Files: authentic, substantial, distributed

The input rules live in three places: the standard, the fingerprints to keep out, the
leakage hard line, the LLM-assist workflow and the tell log in
`../platform/creating-input-files.md` (a carried-over capture); the list-versus-upload
matching rule in `../platform/platform-submission-form.md#input-file-list`; and the desk's
count and formats in `../house-rules.md`. This page holds the house additions the checks
code and the packaging shape the tools expect.

## How many files

**Minimum 2. Three or more strongly preferred. No upper bound.** Below 2 the task cannot be
submitted as designed; at 2 it is submittable but thin, and the form's Sources check reads
how many files the task draws on
(`../platform/platform-submission-form.md#task-instruction-checks-optional`).

The count is not the point on its own: every file has to be load-bearing, and the answer
must be unreachable from any one of them. Two genuinely conflicting sources beat six that
say the same thing. Accepted formats are .docx, .pdf, .xlsx, .pptx, engineering files
(STEP, STL, GERBER) and multimedia; the uploader takes ZIP or TAR.GZ to 100GB and loose
audio to 200MB.

## The name match is a hard gate

Three places have to agree character for character, including case and extension: the file
name inside the ZIP, the entry in the Input File List, and every mention in the task
instruction. The form calls a mismatch, a missing file or a listed-but-never-uploaded file
"one of the most common reasons a submission gets sent back", and checklist item 7 makes it
a submit-blocking confirmation. H5 codes it.

Each Input File List entry is written as the file name, a dash, then a brief note on what
the file contains. Write those entries from the ZIP's own directory listing, never from the
build plan, and keep them in `form-lists.md` at the task root, outside both zips, beside the
Output File List entry and the times and tools. Use a plain hyphen between the name and the
note, never the em dash the form's placeholder shows (A6).

## Content and authenticity (cite, do not restate)

- Substantial, real or indistinguishable from real, nothing paywalled or
  employer-proprietary: `../platform/creating-input-files.md#1-the-standard-real-documents-not-clean-ones`
  and `#3-the-fingerprints-to-keep-out`,
  `../platform/creating-input-files.md`. Checklist item
  8 is the authorization confirmation: only files you may share, nothing confidential,
  proprietary or IP-restricted.
- **The package-provenance stop is a house rule the captures do not state.** Batch
  construction evidence (a python library named as the writing application, one shared
  write instant across files, identical docx components, shared rsids) is a rejection, not
  a cleanup (A14, G2b, `tools/gcheck/authorship/package.py`). A genuine Office
  re-save is the only sanctioned remedy: `07-pre-submission-audit.md#package-sequence`.
- **Tells the authorship screen fires on that the style guide does not list:**
  floating-point dust in stored data cells (F1), 555-prefix phone numbers (H2), calendar-
  false weekday/date pairs (H3), number series without variance (A15), round-number figures
  where real records carry odd ones, company names from the LLM-favoured lexicon, placeholder
  entries, the default LLM blue fills (A1), em dashes (A6), and the prose shapes of
  `../../reference/llm-prose-tells.md` (A10). One isolated tell is usually forgiven; two or
  more in one file compound. Authorship is the highest-severity gate: one HIGH tell returns a
  task without a full review.
- No 'notes' columns or annotations that give away issues the solver should deduce (L1,
  L3).
- **Occupation-specific exposure.** Several of the 64 occupations are clinical,
  counselling or laboratory work. No input file may carry anything that reads as real
  patient data, a real identifiable individual's record, or a practice that is unsafe if
  copied (`../platform/domains-and-occupations.md#what-this-means-for-task-design`).

## No answer leakage (cite, do not restate)

`../platform/creating-input-files.md#4-no-answer-leakage` is the rule and the list of
hiding places. The house codes it: project or evaluation vocabulary anywhere in content,
names or metadata (N1, H1); hidden sheets, hidden rows and columns, comments, tracked
changes, speaker notes (L2); an input paragraph that enumerates the golden's answer set
(L1), hands over a verdict a criterion scores (L3) or names the members of a listed set a criterion scores (L4);
a firm-price or validity date in
an input the golden never carries (R23); a snapshot dated before records it references, or
a stated balance an input reproduces only without the date cutoff (G22: pick the cutoff
first and clamp every record date to it). Remove any executive summary, key finding, total,
recommendation or conclusion that shortcuts the analysis the task asks for.

**Tell log:** `../platform/creating-input-files.md#6-the-tell-log-only-when-tells-are-found`.
The house check is T1: a standalone file, never inside an input or either zip.

## Build in difficulty

`../difficulty.md` is the method; run its design read on the inputs before the golden is
built. The input-side rules it rests on: give the raw record rather than a computed column,
let no memo, email or addendum narrate the call, label no trap (L7, L8), exercise both arms
of every rule with a look-alike (PR22), and set the decisive figure on its threshold. Beyond
those:

- **Every planted inconsistency is one the golden resolves and the rubric credits.**
- **Mixed file types** that must be reconciled (a contract PDF against a pricing
  spreadsheet against email correspondence) are the cheapest source of real difficulty.
- **A status, flag, base-period or effective-date column** that a solver skims is a good
  home for a step of the answer, and real extracts carry such columns anyway. It reports a
  state ("Superseded", "Open", "preliminary"); it never states the consequence (L8).
- **Do not introduce inconsistencies in core facts** such as the entity, date range,
  currency or jurisdiction. Conflicts are planted in the figures and the records, never in
  what the task is about.
- **Mind the preview windows.** The platform previews the first 25 and last 15 lines of a
  CSV and about the first 25 rows of a workbook sheet. A long CSV goes into side-by-side
  panels (H7), and every row the golden cites sits inside the window (H8).

## Packaging rules

- One flat `.zip` named `i-<task-name>.zip`; no subfolders; no empty files; no spaces in
  the zip name or any file name; no double extensions (H4). The form takes a single archive,
  so a flat zip is also what it wants.
- File names match the prompt and the Input File List exactly, and every file either one
  names exists (H5).
- Build it with the package sequence (`07-pre-submission-audit.md#package-sequence`); the
  zip holds exactly the files of `inputs/` (H10).

## Final screen before moving on

Unzip your own archive once and check:

- [ ] At least 2 files, preferably 3 or more; every file load-bearing
- [ ] No missing or duplicate files; no subfolders; no empty files; no spaces or double
      extensions (H4)
- [ ] Names match the prompt and the Input File List exactly, including case and extension;
      every named file present (H5)
- [ ] No half-cut-off presentations or low-character-count files (A11, A12)
- [ ] Every file real or indistinguishable from real; no batch-construction evidence
      (A14, G2b); nothing paywalled, confidential or employer-proprietary
- [ ] Nothing that reads as real patient or personal data
- [ ] No answer leakage anywhere, including the hiding places (N1, L1, L2, L3, L4, R23, G22)
- [ ] Tell log (if any) standalone, outside both zips (T1)

Next: `04-golden-solution.md`
