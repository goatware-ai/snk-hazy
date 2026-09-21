# Workflow 03 — Input Files: authentic, substantial, distributed

The platform states the input rules once: the standard, the fingerprints to keep out, the
leakage hard line, the LLM-assist workflow and the tell log in
`../platform/creating-input-files.md`; the count and size limits, the field-authenticity
test and the packaging rules in `../platform/project-guidelines-v5.1.md#input-files`. This
page holds the packaging shape the tools expect and the house additions the checks code.

## Content and authenticity (cite, do not restate)

- Substantial, real or indistinguishable from real, nothing paywalled or
  employer-proprietary: `../platform/creating-input-files.md#1-the-standard-real-documents-not-clean-ones`
  and `#3-the-fingerprints-to-keep-out`, `../platform/project-guidelines-v5.1.md#input-files`.
- **The package-provenance stop is a house rule the captures do not state.** Batch
  construction evidence (a python library named as the writing application, one shared
  write instant across files, identical docx components, shared rsids) is a rejection, not
  a cleanup (A14, G2b, `tools/gcheck/authorship/package.py`). A genuine Office
  re-save is the only sanctioned remedy: `07-pre-submission-audit.md#package-sequence`.
- **Tells the platform's authorship screen fires on that the style guide does not list:**
  floating-point dust in stored data cells (F1), 555-prefix phone numbers (H2), calendar-
  false weekday/date pairs (H3), number series without variance (A15), the default LLM
  blue fills (A1), em dashes (A6), and the prose shapes of
  `../../reference/llm-prose-tells.md` (A10). Detail in
  `06-metadata.md#house-notes-on-platform-submission-formmd`.
- No 'notes' columns or annotations that give away issues the solver should deduce (L1,
  L3).

## No answer leakage (cite, do not restate)

`../platform/creating-input-files.md#4-no-answer-leakage` is the rule and the list of
hiding places. The house codes it: project or evaluation vocabulary anywhere in content,
names or metadata (N1, H1); hidden sheets, hidden rows and columns, comments, tracked
changes, speaker notes (L2); an input paragraph that enumerates the golden's answer set
(L1), hands over a stay verdict a criterion scores (L3) or names the members of a listed set a criterion scores (L4); a firm-price or validity date in
an input the golden never carries (R23); a snapshot dated before records it references, or
a stated balance an input reproduces only without the date cutoff (G22).

**Tell log:** `../platform/creating-input-files.md#6-the-tell-log-only-when-tells-are-found`.
The house check is T1: a standalone file, never inside an input or either zip.

## Build in difficulty

- **Distributed information** and **realistic messiness** as `01-ideation.md` defines them;
  every planted inconsistency is one the golden resolves and the rubric can credit.
- **Mixed file types** that must be reconciled (a contract PDF against a pricing
  spreadsheet against email correspondence).
- **Put a step of the answer in a metadata column.** A status, flag, base-period or
  effective-date column that most solvers skim is where difficulty hides cheaply, and it is
  the kind of column real extracts carry anyway. The best task reviewed to date derives its
  whole contract mechanism, a five-month reference lag, from a `preliminary` flag and the
  revision cycle it implies.
- **Keep worked examples inside the first ~25 data rows** of an input; the reviewer's
  tooling reads inputs through a window of about 28 rows (`memory/rubric-coverage-and-completeness.md`).

## Packaging rules

- One flat `.zip` named `i-<task-name>.zip`; no subfolders; no empty files; no spaces in
  the zip name or any file name; no double extensions (H4). Limits and accepted formats:
  `../platform/project-guidelines-v5.1.md#input-files`.
- File names match the prompt exactly, and every file the prompt names exists (H5).
- Run the package sequence in `07-pre-submission-audit.md#package-sequence` before zipping.

## Final screen before moving on

Unzip your own archive once and check:

- [ ] No missing or duplicate files; no subfolders; no empty files; no spaces or double
      extensions (H4)
- [ ] Names match the prompt exactly; every named file present (H5)
- [ ] No half-cut-off presentations or low-character-count files (A11, A12)
- [ ] Every file is load-bearing
- [ ] Every file real or indistinguishable from real; no batch-construction evidence
      (A14, G2b); nothing paywalled or employer-proprietary
- [ ] No answer leakage anywhere, including the hiding places (N1, L1, L2, L3, L4, R23, G22)
- [ ] Tell log (if any) standalone, outside both zips (T1)

Next: `04-golden-solution.md`
