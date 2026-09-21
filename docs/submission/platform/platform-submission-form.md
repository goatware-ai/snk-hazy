# Submission form — Hazy_Task_Creation

> Captured 2026-09-21 from the live form (submission `aa146ff6-4558-4117-9a35-68ce26d6233c`,
> task UID `d2aa8273-c67c-49f0-ac97-9f6b515cbdae`) on
> `experts.snorkel-ai.com/projects/cda2e943-8524-45f0-a966-469903337102`.
> **This file is authoritative.** Where the guidelines PDF
> ([create-the-task-guidelines.md](create-the-task-guidelines.md)) disagrees, the form wins:
> it is what blocks submission.

Form header: "Please select the closest occupation to this task using the list here:
<https://www.onetonline.org/find/industry>. All form questions are required unless marked
as optional."

The form has five sections, each ending in **Run Evaluations and Continue**, with the last
ending in **Run Evaluations and Submit**.

1. Select the Domain and Sector
2. MetaData — task instruction, input file list, file uploader
3. Completed Task — output file list, completed upload, times, tools
4. Task Rubrics
5. Before You Submit — Task Creation Checklist

---

## 1. Select the Domain and Sector

Two single-select radio lists, **Domain** and **Occupation**, both "Please select one based
on your area of expertise". Neither is free text, and the guidelines note that a domain or
sector not visible is not available. Both lists are captured in
[domains-and-occupations.md](domains-and-occupations.md).

## 2. MetaData

### Task Instruction

"Below, please write the instructions for a task in your selected domain above. Write it as
if you're briefing a skilled colleague on a real assignment."

- Set specific context: your role, your organization, and what's prompting this work today.
- Name every input file you're uploading and what it contains.
- State the exact deliverable: file format, and any length or structural requirements (page
  limit, number of tabs, required columns, naming convention).
- Include real scenario numbers and constraints where they belong — budgets, deadlines,
  headcounts, thresholds. These are fine and expected.
- **Leave out any number, name, or finding that the reader can only get by actually working
  through your input files** — those are what the exercise is testing, so save them for
  your rubric, not your instructions.
- Be fully self-contained: whoever completes this task, including an AI model, will not see
  your rubric. Everything needed to produce a correct, complete answer must be here.

Placeholder text in the field:

```
e.g. "You are the [role] at [company]. [What's prompting this task today]. Using the
attached [file name], which contains [what it contains]..., produce a [file format] that
[what it should show/recommend], no more than [length/structure limit]."
```

### Input File List

- List each input file, using the **exact file name it will have when uploaded** (same
  spelling, capitalization and extension).
- Start each entry with the file name, then a dash, then briefly note what it contains.
- "This list is checked against your actual upload — a mismatched name, a missing file, or
  a file listed here that never gets uploaded is **one of the most common reasons a
  submission gets sent back**. If you're referencing the file by name anywhere in your Task
  Instruction, make sure it matches this list exactly too."

Placeholder: `e.g. "Q3_Regional_Sales.xlsx — monthly sales by region, includes conflicting
totals between the summary tab and the raw data tab"`

> House note (2026-09-21): the desk writes each entry with a plain hyphen between the file name and the note, never the em dash the placeholder shows, and keeps the entries in the task's `form-lists.md`.

Entries are added with **+ Add Another Input File**.

### File Uploader (required)

"Compress all of your input files into a single ZIP before uploading here. Each file name
inside the ZIP must exactly match an entry in the Input File List above — this is what
confirms your task package is complete before it moves forward."

Accepts ZIP, TAR.GZ to 100GB; MP3, M4A, AAC, WAV to 200MB.

### Task Instruction Checks (optional)

Advisory only — "This feedback is advisory and does not submit or block anything." Reviews:

- *Task Instruction* — long enough to stand on its own, and names every file in the Input
  File List
- *Input File List* — populated, with each entry starting with a real file name
- *Sources* — advisory note on how many input files the task draws on

## 3. Completed Task

"Now that you've updated your Task Instruction and Input Files, **complete the task
yourself** — the way the qualified professional you described in your instruction would
actually do it. **This is your ground truth and what you will build your rubric off of.**"

### Output File List

"List every file your completed task produces, using the exact file name and format you
specified in your Task Instruction's deliverable requirements." Added with **+ Add Another
Output File**.

### Completed Task Upload (required)

"Upload your completed deliverable(s) here. File names must exactly match the Output File
List above, including extension." Same size limits as the input uploader.

### Times

Five fields. The first four are minutes, the fifth is hours.

| Field | Note |
|---|---|
| Time to read and understand the prompt and requirements | minutes |
| Time to open, skim/search, and use the reference files | minutes |
| Time to perform the required work (analysis, writing, calculations, coding, spreadsheet edits, formatting) | minutes |
| Time for verification/QA and final review | minutes |
| **Total time (in hours)** | decimals; 90 minutes is 1.5 hours |

"This should be at least the sum of the four figures above, converted to hours. It may be
higher."

Estimates are for completing the task **without any AI assistant**, based on the prompt and
reference files. Exclude: time learning missing domain knowledge, waiting on other people
or approvals, breaks or unrelated distractions, and web research unless explicitly required
by the prompt (default: do not assume browsing).

### Please Insert Any Tool Used For this Task

"e.g., Excel, Photoshop, DaVinci, SolidWorks, LabVIEW". At least one, added with **+ Add
Another Tool**.

### Completed Task Checks (optional)

Advisory only. Reviews:

- *Output File List* — populated
- *Times* — all five fields are numbers, and the total is at least the sum of the four parts
- *Tools* — at least one tool logged
- ***Difficulty* — estimated manual effort is over 3 hours**

## 4. Task Rubrics

"List your criteria one by one — most tasks will need a **minimum of 3 criteria; expect
somewhere in the 20-60+ range depending on complexity.** Each line should test exactly one
thing: a specific number, name, date, format requirement, or structural detail — not a
bundled description."

- **Weight -5 to +5** based on how central the item is to a correct deliverable.
- **Use negative weights where useful, to penalize specific unwanted outcomes** (extra
  items included that shouldn't be, page limit exceeded, wrong file type).
- **Pull every exact value straight from your own reference files and ground-truth answer —
  never estimate what a criterion should check.**
  - Bad (estimated): `[+2] The workbook states total damage revenue as approximately $15,000.`
  - Good (from the actual data): `[+2] The workbook states total damage revenue as $15,170.`
- **End with a general "Overall formatting and style of the deliverable" line** (commonly
  ~+5) to catch polish and presentation.

Each rubric row has a **Rubric Description** (marked optional) and a **criteria weight -5 to
+5** (marked optional). The form opens with Rubric 1, 2 and 3 and a **+ Add a New Rubric**
control.

### Task Rubric Checks (optional)

Advisory only. Reviews:

- *Rubric rows* — every criterion has a description and a weight between -5 and +5
- *Scoring* — at least one weight is positive, so a correct deliverable can score
- *Depth* — advisory note on whether the rubric covers the task's complexity

## 5. Before You Submit — Task Creation Checklist

"Confirm each item below applies to your submission before you check it off. **All boxes
must be checked to submit.**" **Fourteen** boxes, in four labelled groups:

**Task Instruction**

1. My instruction sets specific context: a named role, organization, and a reason this work
   is happening today.
2. I named every input file I'm uploading and briefly described what each one contains.
3. I stated the exact deliverable format (file type), plus any length or structural
   requirements (page limit, tab count, required columns, naming convention).
4. I included real scenario constraints where they belong (budget, deadline, headcount,
   threshold).
5. I did not include any number, name, or finding that can only come from actually working
   through the input files — those live in the rubric, not here.
6. My instruction is fully self-contained: someone with no rubric access could read it and
   my input files and have everything they need to produce a complete, correct answer.

**Input Files**

7. Every file I listed is actually uploaded, and every file I uploaded is listed — names
   match exactly, including extension and case.
8. I'm only using files I'm authorized to share — no confidential, proprietary, or
   IP-restricted material.

**Task Rubric**

9. I have at least 3 criteria, and enough to genuinely cover the task's complexity (most
   real tasks need well more than 3).
10. Each criterion tests exactly one thing — no line bundles two separate checks with "and."
11. Each criterion's weight (-5 to +5) reflects how central that item actually is to a
    correct deliverable.
12. My rubric ends with a general "Overall formatting and style of the deliverable" line.
13. Nothing in my rubric asserts a fact that isn't actually derivable from the input files
    I'm providing.

**Final Check**

14. If someone with real expertise in this domain — but no access to my rubric — read only
    my instruction and files, they could produce work that passes my rubric.

The boxes are unnumbered on the form and carry their group name as a prefix instead. The
numbering above is this capture's, for citation: 1-6 Task Instruction, 7-8 Input Files,
9-13 Task Rubric, 14 Final Check. Counted from the 2026-09-21 screen capture; if the live
form ever shows a box not listed here, add it rather than assuming this list is complete.
