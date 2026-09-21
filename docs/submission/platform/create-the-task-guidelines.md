# Create the Task — Guidelines

> Captured 2026-09-21 from the project's "Create the Task" guidelines PDF. Verbatim
> material; the `platform/` folder marks captured-not-authored documents either side.
> Paired with [platform-submission-form.md](platform-submission-form.md), which captures
> the live form. **Where the two disagree, the form wins** — it is what blocks submission.
> The known disagreement is recorded in section 0 below.

---

## 0. Known conflict — the completed solution

This document says, three times, that the task creator does **not** produce a solution:

- "Expert 1 creates a new task (including task instruction, input files, and rubric). Do
  not complete the task in this workflow. Another expert will complete the task you create."
- "Your role in this workflow is to author the task package, not to produce a
  gold-standard solution."
- Before Submitting: "You have not uploaded a reference output or completed solution in
  this task-creation workflow."

The live form contradicts all three. It carries a **required** `Completed Task Upload`
under a section that reads: "Now that you've updated your Task Instruction and Input
Files, complete the task yourself — the way the qualified professional you described in
your instruction would actually do it. This is your ground truth and what you will build
your rubric off of."

**This desk builds the solution.** The form cannot be submitted without it, the rubric is
explicitly derived from it, and a rubric rule below ("pull every exact value straight from
your own reference files and ground-truth answer — never estimate") only makes sense if the
solution exists. Raise the contradiction with the project if it ever matters; until then
the form is authoritative.

---

## Project goal

The project creates high-quality, expert-level benchmark tasks that evaluate the ability of
AI systems to perform realistic professional work. Contributors develop authentic work
scenarios from their own professional experience and provide supporting reference
materials. Other experts then complete the task, either on their own or with AI assistance.

Each submission is a task package: task instructions, reference files, and an evaluation
rubric. Tasks should require meaningful reasoning, judgment, reconciliation of information
across multiple sources, and production of concrete professional outputs such as reports,
spreadsheets, presentations, or other business documents.

The benchmark emphasizes:

- Real-world professional workflows rather than artificial exercises.
- Multi-step reasoning and expert judgment rather than simple information extraction.
- Use of multiple supporting files that contain distributed, messy, or conflicting
  information requiring analysis.
- Objectively verifiable outputs with clear success criteria.
- Comprehensive evaluation through detailed rubrics that measure correctness, quality, and
  handling of complex scenarios.

## Task creation

Create a realistic, expert-level task that another qualified professional can complete
independently and would take them **~5-10 hours**. The task is used in the Human Only and
Human + AI workflows, where another expert completes it without and with AI assistance.

> ### The key rule
>
> These prompts need to be hard. They should take someone at least 5-10 hours in their
> day-to-day life to complete, and **a model should not be able to produce a good answer by
> reading the instructions alone without the input files.** Difficulty should come from
> source materials and the reasoning required to reconcile them, not from making the
> prompts themselves long or prescriptive.
>
> Examples: <https://huggingface.co/datasets/openai/gdpval/viewer/default/train>, filtered
> to your sector.

## General guidelines

- Use only files you are authorized to share. No confidential, proprietary or
  IP-restricted material.
- Use the same task instruction, rubric, input filenames and expected output filenames
  across all relevant tabs and uploaded archives.
- Tasks must reflect realistic professional work and require reasoning across the supplied
  files.

## 1. Select the O*NET domain and sector

Select the domain and sector that best match your professional expertise. **If a domain or
sector is no longer visible, it is not available.** Choose a topic you know well enough to
create an authentic assignment.

The platform presents a fixed list of domains and occupations rather than free O*NET
selection. Both lists are captured in
[domains-and-occupations.md](domains-and-occupations.md).

- **O*NET Occupation:** <https://www.onetonline.org/find/all> — select the occupation your
  prompt falls under (e.g. Accountants and Auditors). The form's own header points at
  <https://www.onetonline.org/find/industry> instead.
- **O*NET Occupation Code:** paste the code from the same page (e.g. 13-2011.00).

## 2. Write the task instruction

The task instruction is based on an expert's day-to-day working, requires one or more
reference files, and has a deliverable or outcome in mind. It provides context around who
is doing the work. Write as if briefing a skilled colleague on a real assignment: describe
the context, the required work product, and the source files they must use. Focus on what
they need to produce and why. **Do not prescribe every step of how they should do it.**

Requirements:

- **Grounded in real work.** Based on things you have actually done. Sanitized real
  documents beat invented ones.
- **Specific expert context.** Role, organization or client, business trigger, and intended
  audience. Not "you are a lawyer" but "you are the General Counsel for a mid-sized public
  agency reviewing an employee leave request under DC FMLA."
- **Multi-step reasoning (at least 3 steps).** Judgment, reconciliation or inference, not
  reading and copying.
- **Concrete deliverable.** State the required deliverable(s), including file format and
  essential structural requirements. A specific output file (.docx, .xlsx, .pptx, .pdf).
- **Input files must be necessary.** Name every input file and briefly state what it
  contains. If the task could be answered from the instruction alone, it is probably too
  easy. **Do not reveal values, findings or decisions that can only be derived from the
  files.**
- **Self-contained.** Solvers will not see the rubric. No proprietary systems or personal
  accounts. Web searches that do not require logins are OK.
- **Objectively verifiable.** The output must be checkable, not a matter of opinion.
- **Relevant constraints.** Dates, budgets, thresholds, policies, stakeholder requirements.
- **Your own voice.** Not LLM-generated. Practitioner-level language.

> ### Most common mistake: overspecification of "HOW"
>
> If your instruction reads like a template to fill in rather than a task to perform, it is
> too prescriptive. Dictating every step, column name and exact phrase leaves no room for
> expert judgment and makes the task easy for models. **Tell them WHAT to produce, not
> HOW.**

## 3. List and upload input files

**Minimum 2 files; 3+ strongly preferred.** Formats: .docx, .pdf, .xlsx, .pptx, engineering
files (STEP, STL, GERBER), multimedia. No proprietary or IP-encumbered content.

List every file required to complete the task, then upload. **The filenames and formats
must exactly match the entries in the Input File List.**

- Use at least two input files when practical; three or more strongly preferred.
- Make files necessary: the task should not be answerable from the prompt alone.
- Build difficulty through distributed information, inconsistencies, missing data,
  conflicting sources, and mixed file types where appropriate.
- Do not use source materials that require a private login unless the task explicitly
  provides access.

### Using AI to create input files

An AI assistant may help draft or structure input files. You are responsible for reviewing
and editing every file before submission so it reads and behaves like a real workplace
document created by someone in your field.

- Start from authentic documents or workflows whenever possible.
- Use specific, realistic names, dates, identifiers, figures and formatting appropriate to
  the sector. **Numbers should reconcile across files and should not look artificially
  clean or consistently round.**
- Keep normal workplace context and imperfections where appropriate: corrections, notes,
  conflicting source records, version differences. **Do not introduce inconsistencies in
  core facts** such as the entity, date range, currency or jurisdiction.
- Do not submit unedited AI-generated content. Replace generic wording, placeholders,
  overly polished summaries, generic section headers, default formatting, and other
  language or design that does not reflect how professionals in the field actually work.
- **Input files must never contain the answer**, a pre-computed result, or a conclusion the
  solver is expected to derive. Remove executive summaries, key findings, totals,
  recommendations, or other content that shortcuts the required analysis.
- **Do not include any reference to the project, task, prompt, rubric, benchmark,
  evaluation, golden solution or AI assistance** in file contents, filenames, comments,
  notes, hidden tabs, revision history, speaker notes or metadata.
- Verify all load-bearing facts, calculations, citations and cross-file references.
- Before uploading, review visible and hidden content: spreadsheet tabs, hidden rows and
  columns, comments, document properties, tracked changes, slide notes, embedded objects,
  filenames.

If you identify and correct AI-generated tells while preparing the inputs, record them in a
separate tell log only when required by the submission workflow.

## 4. Define expected output files

List every file the solver is expected to produce, with exact filenames and formats
wherever they matter. Outputs should be concrete professional work products: a spreadsheet,
report, presentation, design file or revised document.

## 5. Write task rubrics

The rubric is how model responses are evaluated, and writing a good one matters as much as
writing a good instruction. The platform can generate an initial rubric; use it as a
starting point, then review and revise every criterion.

**This document says "at least six criteria." The form says a minimum of 3 and expects
20-60+.** See the form capture; this desk works to the form's range.

Each criterion assesses one objective, observable aspect of the final deliverable.

- **Atomic** (one thing), **affirmative** ("The report identifies..." not "does not
  omit..."), non-overlapping, objectively verifiable, and focused on the **final output,
  not the process**.
- Test important results: calculations, decisions, edge cases, handling of conflicts,
  required file structure, evidence-based findings.
- **Do not merely mirror the instruction.** A criterion should help distinguish a correct
  result from a plausible but incomplete one.
- Keep rubric details out of the task instruction when they would give away the answer.

| Score | Meaning | When to use |
|---|---|---|
| +4 to +5 | Critical | Core deliverable correct and complete |
| +2 to +3 | Important | Correct structure, format or key finding |
| +1 | Minor positive | Specific detail, label or edge case |

The form extends this range downward to **-5**, for penalising specific unwanted outcomes.

> ### Most common rubric mistake: mirroring the instructions
>
> If your instruction says "include a summary tab with total revenue" and your rubric says
> "+2 The workbook includes a summary tab with total revenue", that is not good enough.
> That just checks if the model read the instruction. Good criteria test concrete, specific
> things like the correct dollar value of total revenue, and other non-obvious patterns and
> edge cases.

Example criteria:

```
[+3] Where data conflicts between source files, the contract value is used and the
     discrepancy is noted
[+2] The analysis identifies the delay pattern is concentrated in a specific segment,
     not treated as uniform
[+1] Cancelled engagements are correctly distinguished from active ones. Cancelled
     engagements include…; active ones include…
```

**What to test:** file presence and format, numeric values (within tolerance), structural
requirements (sheet count, word count), content checks (specific entity or date appears),
deduplication.

## 6. Record the human time estimate

Estimate the **active** time, in minutes, a qualified professional would need to complete
the task **without AI**. Exclude time spent learning missing domain knowledge, waiting for
others, breaks, unrelated distractions, and web research unless the prompt explicitly
requires it.

| Platform field | What to enter or do |
|---|---|
| Input File List | Every required source file, listed exactly as uploaded. |
| Output File List | Every expected deliverable, with exact name and format when relevant. |
| Task Prompt Quality Checks | Review that files exist, the task is unique, and the instruction is free of spelling and grammar errors. |
| Time to Complete This Task | Estimate minutes for reading, using reference files, performing the work, and QA/final review. |
| Tools Used | List any non-AI tools a solver would reasonably use for the task. |

The form splits this into four minute fields plus a total in hours. See the form capture.

## Before submitting

- The instruction, rubric, file lists and uploaded files match exactly.
- The task requires real professional reasoning across the supplied materials.
- The deliverables are concrete and evaluable.
- The rubric has at least six clear criteria.
- ~~You have not uploaded a reference output or completed solution in this task-creation
  workflow.~~ **Superseded by the form's required Completed Task Upload. See section 0.**
