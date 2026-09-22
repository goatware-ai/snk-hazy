# Creating Input Files

> **Carried over from the desk this repo was built from and not yet confirmed here.** This
> document describes how to build input files that are authentic and do not leak the answer.
> It is kept because the guidance is domain-agnostic, but nothing in it has been checked
> against Hazy's own platform. Where it disagrees with `platform-submission-form.md` or `../house-rules.md`, those win.

How to build input files that are authentic to your domain, free of LLM tells, and never leak the answer.

You can now use an LLM to help you build input files. The bar for the files themselves has not changed. Each input file has to look and behave like a real document a practitioner in the domain would work from, it has to be free of the machine-generated fingerprints that get a task sent back, and it must never contain the answer the task is meant to produce. This guide shows how to get the assist without leaving those fingerprints, in a way that carries across any domain you work in.

The reason this matters is practical. Inputs that read as fabricated or machine-written, or that leak the answer, get returned or rejected, which slows the task down. Authentic, clean inputs move through review faster. The guidance below is what separates the two.

---

## 1. The standard: real documents, not clean ones

The single test to hold every input file against is this: would this file exist, in this form, in a real workplace in this domain. Real work is specific, sourced, owned by named people and systems, and a little messy. Files that read as generic, round, and frictionless are the ones that get flagged.

There are two ways an input file fails that test, and you want to avoid both. The first is synthetic content: fabricated data, generic names, round numbers, placeholder text. The second is machine-authored content: the tells an LLM leaves when its output ships unedited. The strongest inputs start from real structure. Base a file on a document type you know from the domain, an invoice layout, a case file, a lab report, a support ticket thread, a maintenance log. If you sanitize a real document, keep its structure and its rough edges rather than smoothing them into something clean.

## 2. Make it authentic and domain-representative

Aim for these qualities in every file, whatever the sector.

- **Specific named entities.** Use realistic names, identifiers, dates, and places that fit the domain and region. Avoid "Company A," "Vendor 1," and "John Doe."
- **Numbers that are not suspiciously round and that reconcile.** Real figures carry odd cents and off-round values, and they add up. Subtotals should sum to totals, and cross-references between files should agree.
- **Real structure and sector-appropriate formatting.** Lay the file out the way that document type really appears. A bare white page with generic headers reads as machine output.
- **A human voice with ownership.** Name the authors, approvers, and systems. Include first-person notes, a correction, a caveat, a late revision. Real documents show that a person made them.
- **Authentic messiness the task can reconcile.** Two systems reporting different figures, a superseded version, a note that does not match the log, keep this kind of conflict when it is the sort the work really produces and the model can reconcile it from the files. One thing must stay consistent across all files though: the period, entities, currency, and jurisdiction the task is set in have to agree everywhere. That kind of mismatch is an error, not authentic mess.
- **Spreadsheets that behave like real ones.** Use multiple tabs when the data is multi-faceted, and formulas where a real workbook would compute rather than hard-coded results.

## 3. The fingerprints to keep out

These are the machine-generated tells reviewers are trained to catch. The way to avoid them is to source and edit authentically, not to run a find and replace. Any single strong tell tends to get a file returned, and a couple of smaller ones stacking in the same file has the same effect, so when something feels off, fix it. The categories below carry across domains.

| Tell category | What it looks like | What fixes it |
| --- | --- | --- |
| Language and prose | Hedged, non-committal phrasing; passive voice that avoids taking a position; sentences that describe what a section does instead of doing it; stacked adjectives followed by a list of failures; no named actor | Write in the practitioner's voice, take positions, name who did what |
| Structure and headers | Generic section headers, no hierarchy, bare paragraphs on a white page | Use the real document type's structure and layout |
| Visual and color | The blue palette LLM tools default to, for example hex values near #1F4E79, #2E75B6, and #1C3557; default gray table headers; no sector styling | Style the file the way a real one in that domain would be styled |
| File naming and metadata | A file that names or describes itself, or a subtitle that reads like a deliverable label | Name and title files the way a real workplace file is named |
| Spreadsheet | Round, clean numbers throughout; a single tab for multi-faceted data; hard-coded values where formulas belong | Use realistic figures, real tabs, and real formulas |
| Presentation | Data shown as text bullets instead of charts; plain white slides | Use the visuals a real deck in that domain would use |

## 4. No answer leakage

This is the one hard line. Input files carry the raw material the model reasons over, and they must never carry the answer or anything that shortcuts to it. A leaked answer invalidates the whole task.

Keep these out of every input file:

- **The solved output.** Do not include the final figures, conclusions, or deliverable the task is meant to produce, anywhere in the inputs.
- **Pre-computed results the task asks the model to derive.** Provide the source rows and records and let the model do the reconciliation, calculation, or synthesis. If the task is to compute a total, the inputs supply the line items, not the total.
- **Meta residue that points at the task or the answer.** Notes or labels such as a comment that a value matches the prompt, or a cell reading like a marker for the intended solution, are defects. Scrub them.
- **Any reference to the project or the evaluation.** Input files are ordinary workplace documents, so they must not name the project or mention a task, prompt, rubric, golden, eval, or benchmark anywhere in the content, the file names, or the document metadata. Do not label a file or its properties with the project name. A file that points at the project is both an authenticity tell and a form of leakage, so keep every such reference out of the files.

LLM assistance makes leakage more likely, so watch for it specifically. When you ask a model to generate an input, it often adds a helpful summary, an executive overview, a key-findings box, or a grand total, which is frequently the exact thing the task wants derived. Remove those before the file ships.

Check the places leakage hides, not just the visible page:

- Extra or hidden worksheet tabs, and hidden or filtered rows and columns
- Cell comments and notes, and tracked changes or revision history
- Document properties, author fields, and other metadata
- Slide speaker notes and embedded objects
- The file names themselves

A fast self-check for each input file: does this file hand the model any part of the answer it is supposed to work out, or point at the project in any way. If the answer is yes, take that part out.

## 5. Using an LLM without leaving fingerprints

The workflow that keeps the assist invisible is straightforward. Use the model to scaffold and draft raw material, then edit it as the domain expert you are. The human edit is what removes the tells; unedited output is itself the tell.

- Prompt toward realism. Give the model the real document type, real entity names, and real constraints, and ask for specificity and messiness rather than a clean summary.
- Never ask it to produce or include the answer, the totals, or the conclusions the task will test.
- Replace generic names, round numbers, and placeholder text with specific, domain-real values.
- Read every file end to end after generating it, including the hidden places listed above.
- Verify the facts. Models invent plausible but false specifics, a citation that does not exist, a rate that is out of date, a standard that was never issued, numbers that do not reconcile. Every load-bearing fact in an input has to be true and internally consistent, because a plausible but wrong input quietly breaks the task even when it reads well.

## 6. The tell log, only when tells are found

If you notice that you introduced a tell while building your inputs, keep a short record of it in a tell log. Create this log only when you found tells. If your inputs are clean, there is nothing to log and no file to create.

The tell log is a standalone file. Do not place it inside an input file, and do not embed it as a tab, a comment, or a note within any deliverable, so that no meta content cross-contaminates the task. Keep it simple, with one row per tell:

| Input file | Tell type | Where it appeared | How you resolved it |
| --- | --- | --- | --- |
| example_invoice.xlsx | Spreadsheet, round numbers | Line items on the charges tab | Replaced with realistic off-round figures from the source |

Save it as its own file, for example a plain CSV or text file named as a tell log, kept separate from the input files. Follow the current submission instructions for where to place it when you submit.

## 7. Quick check before you submit your inputs

- Each file is something a practitioner in this domain would really work from.
- Named entities, dates, and identifiers are specific, with no generic placeholders.
- Numbers are realistic and reconcile, and are not suspiciously round.
- The file uses real document structure and sector-appropriate styling, with none of the default LLM blues.
- Spreadsheets use real tabs and formulas where a real one would.
- The files carry a human voice and ownership, with authentic messiness and consistent framing across files.
- No language, structure, visual, naming, spreadsheet, or presentation tells remain.
- No answer leakage anywhere, including hidden tabs, comments, notes, metadata, and file names.
- No project name or evaluation reference anywhere, including the file contents, file names, and metadata.
- Every load-bearing fact is verified true and internally consistent.
- A tell log exists only if you found tells, as a separate standalone file.
