# Prompt: build one accept-on-submit Hazy task

You are authoring **one** submission for Snorkel's Project Hazy (GDPVal++), the benchmark of
economically valuable, real-world professional workplace tasks. `./docs/submission/` is the
authoring rule set: `platform/` holds the platform captures, of which
`create-the-task-guidelines.md` and `platform-submission-form.md` are authoritative and the
form wins where the two disagree; `workflows/` is the working decomposition, one stage per
file, and is the build order. Check ids cited here are defined in `docs/rules.md` and run by
`tools/autoeval_check.py`; where this file states a count, a band or a weight range, this file
and the platform section it names govern over `docs/rules.md`.

## Domain and occupation

There is no assigned sector. Section 1 of the form is two single-select radio lists, 14 domains
and 64 occupations, and a domain or occupation not visible on the form is not available
(`docs/submission/platform/platform-submission-form.md`, "1. Select the Domain and Sector").
Both lists are in `docs/submission/platform/domains-and-occupations.md`; the verified O*NET code
for each occupation is in `docs/submission/platform/onet-codes.md`, "The table". Pick the pair
before writing a line of prompt, because the occupation is what makes the scenario authentic and
what constrains the day-to-day work the prompt may depict.

- **Pick the occupation first, then the domain that matches its O*NET job family.** The domain
  radio is in practice the occupation's job family (`onet-codes.md`, "Why the domain list is what
  it is"). Treat `Healthcare Practitioners / Support` as a duplicate to avoid unless nothing else
  fits. Confirm the code on the occupation's own onetonline.org page before recording it: the form
  abbreviates several titles and eight entries are `.0x` detail codes rather than `.00`
  (`onet-codes.md`, "Four traps").
- **Favour occupations where a written work product is genuinely part of the job.** Most of the 64
  are hands-on. Phlebotomists, Machinists and Home Health Aides do not spend the day producing a
  document, and the deliverable still has to be a concrete file, so the supervisory, managerial,
  analytical and licensed-professional entries carry a task best: the four First-Line Supervisor
  rows, the manager rows, the scientist rows and the legal rows
  (`domains-and-occupations.md`, "What this means for task design"). Choosing a hands-on
  occupation and then inventing paperwork for it is the fastest route to a task that reads
  fabricated.
- **Clinical, counselling and laboratory occupations raise the safety and privacy bar.** They put
  real patient-safety and PHI exposure in scope. Nothing in the package may teach materially
  unsafe practice, and no input file may carry anything that reads as a real patient record,
  a real identifier or real clinical data.
- **Write as that occupation's practitioner.** The role, the organization, the trigger and the
  reader all come from the occupation's own work, and the prompt reads as the person in that seat
  handing the work off.

Record the domain, the occupation title and the code in `metadata.json`.

## Read before designing anything, in this order

1. `docs/submission/platform/create-the-task-guidelines.md`, in full
2. `docs/submission/platform/platform-submission-form.md`, in full: it is what blocks submission,
   and its section 5 checklist is the gate every box of which must be true
3. `docs/submission/platform/domains-and-occupations.md` and `onet-codes.md`, before any concept
   work
4. `docs/submission/platform/creating-input-files.md`
5. `docs/submission/workflows/01-ideation.md` through `07-pre-submission-audit.md`
6. `docs/submission/platform/style-guide-llm-tells.md`: on demand, when A10 fires or a
   sentence reads generated

Where a workflow page or a capture disagrees with those two platform documents, the form
wins, then the guidelines.

## Objective

The only thing that decides anything is **whether this submission is accepted on the first
pass**. The floor is a hard gate in both directions: the form's Difficulty check wants estimated
manual effort over 3 hours and the guidelines target 5 to 10, so build for 5 or more and an
unsympathetic estimate still clears; a frontier model producing the golden correctly on the first
try is too easy; difficulty living in the prompt instead of the input files and cross-file
reasoning is decoration. Build something genuinely hard for a model, grounded in real
practitioner work, and land it cleanly on every packaging and rubric gate the first time.

The form has five sections, each ending in **Run Evaluations and Continue** and the last in **Run
Evaluations and Submit**. The three "Checks (optional)" panels (Task Instruction, Completed Task,
Task Rubric) are advisory and state that they do not submit or block anything, so a clean panel
proves nothing. What blocks is the fourteen-box **Before You Submit** checklist: every box must be
checked to submit, so every box must be true of the package before it is.

## Hard constraints (any miss is a send-back)

**Prompt**
- A professional workflow the chosen occupation actually performs, US-based, with a real decision
  at stake for a named reader.
- The opening frames the state of play, the requester's role and the reader's experience, woven
  into the handoff and never as a self-introduction to a coworker (P4, P6;
  `docs/submission/workflows/02-prompt-writing.md`).
- It sets specific context (a named role, a named organization, and what is prompting this work
  today), names every input file by the exact name it will carry in the Input File List and the
  zip and without purpose glosses (P5), states the exact deliverable with its file format and any
  length or structural requirement (page limit, tab count, required columns, naming convention),
  and carries the real scenario constraints that belong in a brief: budgets, deadlines,
  headcounts, thresholds (form checklist 1 to 4).
- It **leaves out every number, name and finding the reader can only get by working through the
  inputs** (form checklist 5): those are what the exercise tests and they belong in the rubric. It
  is self-contained, because whoever completes it never sees the rubric (checklist 6), and it
  cannot be answered from the instruction alone.
- Sentence mechanics in the prompt, every input document, every golden text cell and the rubric:
  comma before a clause-joining conjunction, never three clauses in one sentence, serial comma
  (A20 codes the first two; the comma splice and the serial comma are a read).
- Natural practitioner voice, no "You are a ..." opener, no step-by-step procedure, no stacked
  adjectives, no vague stakes (A10, P7). Prefer **one** named output file and fold companion
  material into it as a tab or an appendix; the Output File List does accept several, so name
  each one exactly when the work genuinely produces more than one, and never leave a second
  deliverable half-specified. It says **what** to produce, never **how**: no dictated steps,
  columns or formulas, no derived parameters (P0 to P3). Overspecification of HOW is the most
  common prompt defect the guidelines name.
- Length is not difficulty. Brief the colleague and stop; the capture records no character cap on
  this form, so do not read one as headroom.

**Input files**
- **At least 2 files, 3 or more strongly preferred** (`create-the-task-guidelines.md`, "3. List
  and upload input files"), each one necessary to the answer, with no upper bound. Accepted
  formats include .docx, .pdf, .xlsx, .pptx, engineering files (STEP, STL, GERBER) and
  multimedia. The uploader takes a single ZIP or TAR.GZ to 100GB and standalone audio to 200MB,
  so size is never the constraint: substance over decoration is (A11, A12).
- **The names must match in three places**: the Input File List entry, every mention in the
  prompt, and the member name inside the ZIP, exactly, including case and extension. The form
  calls a mismatch one of the most common reasons a submission gets sent back.
- Real, or indistinguishable from real (`creating-input-files.md`): an LLM may assist, the result
  must read as a document the practitioner works from. No PII, no patient-identifiable content,
  nothing paywalled or IP-restricted.
- No round-number giveaways, no generic or LLM-lexicon company names, no 555 phone numbers, no
  placeholder entries, no notes column that reveals what the solver should deduce; stored values
  at field precision (F1), no arithmetic series in a data column (A15). Period, entities,
  currency and jurisdiction agree across files; realistic messiness (duplicates, inconsistent
  naming, cancelled records) is fine, a mismatch on those four is an error.
- Every snapshot input references only records dated on or before its own date, and any "as of"
  balance re-derives from the registers date-filtered (G22): pick the cutoff first and clamp
  record dates to it.
- A deliverable date the prompt gives ("I need it ...") and the golden's Date line fall at least 21
  days after the build, or the prompt gives no due date (P8): the package is read weeks after
  the build, and a deadline already past reads as an impossible timeline.
- **No answer leakage**: inputs never carry the solved output, pre-computed results the task asks
  for, or meta residue (L1, L2, L3, L4), including hidden tabs, hidden or filtered rows and columns,
  comments, tracked changes, document properties and file names. Remove any executive summary, key
  finding, total, recommendation or conclusion that shortcuts the required analysis. No project or
  evaluation reference anywhere in any shipped file's content, name or metadata, and no
  project codename appears in any shipped file (N1). A tell found and fixed while building goes in
  a standalone tell log, never inside an input or either zip (T1).
- **Package provenance is a stop, not a cleanup:** batch generator strings, one shared write
  instant, identical docx components, shared rsids (G2b, A3, A14) read as generated
  inputs and are a rejection without a revision cycle.

**Golden solution**
- **Required, and the rubric is built from it.** The guidelines PDF says three times that the
  creator does not produce a solution. The live form carries a required **Completed Task Upload**
  under "complete the task yourself ... This is your ground truth and what you will build your
  rubric off of", and the form wins (`create-the-task-guidelines.md`, "0. Known conflict"). Build
  it in full, before the rubric, and **pull every exact value in the rubric straight from it and
  from the input files, never estimated** (`platform-submission-form.md`, "4. Task Rubrics").
- The Output File List names every file the task produces, with the exact names the prompt
  specified, and the completed upload matches that list exactly, extension included.
- Answers every part of the prompt, fact-checked, client-ready: documents polished, spreadsheets
  on live formulas with a cached value in every formula cell (A9, A17), output names matching the
  prompt exactly, every file opening cleanly (A16). Summary counts and conditional sums are
  COUNTIF/COUNTIFS/SUMIFS, dot products SUMPRODUCT(range,range) (R96).
- It survives the literal read against the inputs and the prompt before the rubric is
  drafted (G8, G9, G10, G22; `docs/submission/workflows/04-golden-solution.md`, "The literal
  read"): every cited identifier exists in a shipped input, no action is dated before the
  document's own date, a signed document is carried with its signature line, and every dated
  claim is written in an input or derived by a stated rule.
- It never contradicts the prompt or the rubric, even by one number (G1, G5, G7, G21), and it
  scores ~100 on the rubric.
- Nothing in the task teaches materially unsafe practice: a golden that normalises an unsafe act
  fails on safety even when every number is right, and in the clinical and laboratory occupations
  that is the likeliest way to lose an otherwise correct task.

**Rubric**
- **At least 6 criteria** (`create-the-task-guidelines.md`, "Before submitting", which also
  satisfies the form's minimum of 3), and in practice **20 or more**: the form expects "somewhere
  in the 20-60+ range depending on complexity" and its checklist says most real tasks need well
  more than 3. **There is no ceiling**: a rubric above 60 rows is not a defect if the task earns
  them. One simple atomic sentence each (R55), no line bundling two checks with "and", explicit
  values the golden actually states (R20, R21), every prompt instruction covered (R4, R13). Rigid
  criteria state the exact answer; judgment calls score the reasoning and name the conditions any
  sound alternative meets. Never several record ids in one criterion; phrase over the class or
  split.
- **Weights are any non-zero integer from -5 to +5**, in the numeric field only, with no gap around
  -1 and -2 (`platform-submission-form.md`, "4. Task Rubrics" and checklist item 11). At least one
  core row at +4 or +5, no flat weighting (R99); each criterion 500 characters at most.
- **Negatives penalise any specific, observable unwanted outcome.** There is no restricted class:
  the form's own examples are ordinary quality misses ("extra items included that shouldn't be,
  page limit exceeded, wrong file type"). Carry a negative wherever the deliverable has an
  unwanted outcome worth naming, and hold the shape rules, which are about the criterion and not
  about permission: one thing per line, the defect stated affirmatively as committed, objectively
  checkable, derivable from the inputs, scoped to exactly the rows it should penalise and tested
  against every row class of the golden (R28, R33, R37, R52). The penalty share is a
  recommendation, never a bar (R61).
- **Every exact value comes from the ground truth.** Never estimate what a criterion should check,
  and never hedge a magnitude: "approximately $15,000" is a defect where "$15,170" is the check.
  Nothing in the rubric asserts a fact that is not derivable from the input files being provided
  (form checklist 13).
- **The last row is mandatory and general:** the rubric ends with an overall formatting and style
  of the deliverable criterion, commonly around +5 (form checklist 12). It is the final row, not
  merely present somewhere.
- Style and formatting rows otherwise under half the count and a quarter of the reward; one
  criterion carrying the exact output basename (R83); a contradiction check and a
  domain-correctness clause. No single liveness criterion may carry more than the completeness cap
  (R24), and owner rows never name the person (R81) and score an owner or a date only when the
  prompt asks who and by when (R100).
- **Do not mirror the instruction.** A criterion that repeats what the prompt already demanded
  ("+2 the workbook includes a summary tab with total revenue") only checks that the solver read
  the instruction. Test the value, the reconciliation, the edge case and the non-obvious pattern.
- **Rubric shape:** +2 on the rows that decide something, never six or more rows all at +1; the
  two strictest rows sit on two different deliverables' outputs, never a unit count beside the
  dollar total of one order (R114) nor two cells of one page (R117), and the page a row calls
  first is the workbook's first worksheet (R120); one formula-only gated row at most, every other
  gated clause riding on a value row (R118); a row over a computed figure names its value or its
  reconciliation, never presence alone (R119); an "each item ... N items" row is written as the
  count row plus separate spot checks; negatives put the deliverable in the actor's seat ("The
  workbook wrongly books ...", R111); no golden-only tab name in any criterion, name what the tab
  is (R112).
- **The rubric must fail the golden's own defects:** pin the facts the literal read verifies (each
  cited identifier, the document's date, the signature line, the closed status of every policy
  class), so an error in the golden loses points under its own rubric.

**Package, metadata, uniqueness**
- Both zips flat: no subfolders, no empty files, no spaces, no double extensions, accepted
  formats only, input names, prompt references and output names agreeing exactly (H1 to H5).
- Metadata: the domain, the occupation title and its verified O*NET code, the input file count,
  the tools list and the five time values.
- **Times are five fields**: four integers in minutes (reading and understanding the prompt;
  opening, skimming or searching and using the reference files; performing the required work;
  verification, QA and final review), plus a total in hours as a decimal that is **at least the
  sum of the four converted**. The total must clear 3 hours for the form's Difficulty check, and 5
  to 10 is the guidelines' target. The estimate is for a qualified professional working **without
  any AI assistance**, and excludes learning missing domain knowledge, waiting on other people,
  breaks and web research the prompt does not require.
- **Tools: at least one non-AI tool** a solver would reasonably use, named as the form names them
  (Excel, Photoshop, DaVinci, SolidWorks, LabVIEW).
- No spelling or grammar errors anywhere, no em dashes anywhere (A6).
- **LLM authorship is the highest-severity gate:** the prompt is human-authored, and inputs and
  golden read as human work (A10; one HIGH tell is a return without full review, and two
  MEDIUMs in one file compound to a HIGH).
- **The task is unique** (U1, U2). The platform publishes no map of accepted asks for this
  project, so uniqueness is checked against this portfolio: test the candidate's one-line sentence
  of what the solver actually does against every prompt already in `submissions/`, `accepted/`,
  `archived/` and `drafts/` before building, and against the uniqueness note in `memory/` if one
  is present for this desk. Treat the occupation as part of the identity: the same analytical
  ask under a different occupation is still the same task when the solver's work is the same.

## Design targets

1. **Concept.** One workflow the chosen occupation unambiguously owns, with a real decision at
   stake. Discard anything answerable from general knowledge, template-shaped, or outside what
   that occupation actually does.
2. **Difficulty.** How much has to be true simultaneously across the files: reconciling
   conflicting sources, inferring the method from domain evidence, producing a native
   professional artifact. Not volume or obscurity. Pressure-test before building files: if a
   frontier model one-shots the answer from the prompt plus a sketch of the inputs, harden now.
3. **Files.** Could someone who never worked in this field have produced this layout? If yes,
   rebuild it with the conventions a real practitioner document carries. Each planted
   inconsistency is one the golden resolves and the rubric credits.
4. **Rubric.** Drafted alongside the prompt and finalised against the golden: everything graded is
   stated in the prompt or is ordinary professional standard, and everything the prompt requires is
   graded. Every ask in the prompt is mapped in `clause-map.md` to where the golden delivers it and
   a positive row that fails without it (R134), and the golden produces each asked-for artifact
   itself, in the form any input prescribes (one claim form per invoice means one form per
   invoice), never an action row that says to make it later (G41).

## Process

Do all of this work and do **not** narrate it: no candidate write-ups, no checklist
walkthroughs, no status commentary.

1. Read the docs in the order above, pick the occupation and domain, consider a few concepts
   internally, pick the one that is hard and lands cleanly. Do not present the alternatives.
2. Pick a task name: lowercase kebab-case, 4 words at most, descriptive of the workflow (e.g.
   `rebate-reconciliation-q2`). The **target folder** is `{target}/{seq}-<task-name>/`, where
   `{target}` is `drafts` under `/create-task` (see `prompts/create-task-brief.md`) and
   `submissions` only when the operator asks for a submission build directly; `{seq}` is the
   next number after the highest `{NN}-` prefix across `submissions/`, `accepted/`, `archived/`
   and `drafts/`. Never write into a previous task's folder. `submission-list.md` is owned by
   `/fetch-status`: a build never edits it.

   ```
   {target}/{seq}-<task-name>/
   ├── instruction.md       the task instruction exactly as pasted into the platform
   ├── inputs/              every input file, final names
   ├── i-<task-name>.zip    flat zip of inputs/
   ├── solution/            the golden file(s), final names
   ├── s-<task-name>.zip    flat zip of solution/
   ├── rubric-<task-name>.csv         columns NUMBER, CRITERION, WEIGHT; UTF-8 with BOM;
   │                                  renamed rubric-<task-name>-<uid8>.csv once a Taskboard UID
   │                                  exists (<uid8> = its first eight characters); no rubric.md
   ├── metadata.json        form values only: task_name, taskboard_uid (null until submitted),
   │                        domain, onet_occupation {code,title}, input_file_count,
   │                        output_file_count, tools[], time_read_minutes, time_files_minutes,
   │                        time_work_minutes, time_qa_minutes, total_time_hours, built_with,
   │                        build_session (the five time keys are the ones the M4 check reads)
   ├── form-lists.md        what gets typed into the form: one Input File List entry per input
   │                        (exact name, a plain hyphen, what it contains), the Output File List
   │                        entry, the five time values, the tools, the domain and occupation
   ├── feedback-log.md      chronological log: date, source, verdict, then findings /
   │                        actions / form actions; one entry per piece of feedback
   ├── clause-map.md        every prompt ask -> quoted golden anchor -> positive rubric rows (R134)
   ├── verify_golden.py     re-derives the golden's figures from inputs/ alone, with its
   │                        alternate-reading pass (G43; start from tools/templates/)
   └── struck-phrases.md    only once something is struck: one quoted phrase or /pattern/
                            per bullet, with source and date (PR20, G42)
   ```

3. Real, working content in every file: no placeholders, no `TODO`, no thin files; spreadsheets
   on live formulas; documents to client-ready standard.
4. Verify, quietly. Walk `docs/submission/workflows/07-pre-submission-audit.md` row by row
   against what you built and fix every failing gate, with particular attention to the rows
   with no coded check (natural voice, authentic files, frontier resistance, the rubric
   alignment rows). Do the literal read of the golden (Golden solution, above) before the
   rubric is final. Score the golden against the rubric criterion by criterion and fix whichever
   side is wrong if it lands under ~100. Write `verify_golden.py` from
   `tools/templates/verify_golden.py`: it reads only `inputs/`, reproduces every figure the golden
   states, and lists every other reading the figures admit (rounding at each step, band
   boundaries, tolerances) with the phrase the golden uses to settle it, and the golden's method
   text states each of those phrases (G43). Write `clause-map.md` last, from the final prompt, golden
   and rubric (R134). Then run the Package sequence.
5. Walk the form's fourteen-box checklist
   (`platform-submission-form.md`, "5. Before You Submit"), one box at a time against the built
   package, and fix anything that is not already true. Every box must be checked to submit, so a
   box that is not true is a defect, not a formality.

## Package sequence

Run it once the files are final, and again from the top whenever any file is touched afterwards,
because only the last step judges the result:

```bash
T={target}/{seq}-<task-name>
.venv/bin/python tools/office_resave.py $T --force                          # real Excel/Word write the bytes (A14); read its recalculation notes
.venv/bin/python tools/fix_floats.py fix $T/inputs/*.xlsx $T/solution/*.xlsx  # Excel writes float artifacts back (F1)
.venv/bin/python tools/fix_metadata.py $T                                   # immediately before the zips: de-batch stamps, sync mtimes
# rebuild i-<task-name>.zip and s-<task-name>.zip, flat
.venv/bin/python tools/autoeval_check.py $T                                 # 0 errors, on the packaged files
```

The order matters: the re-save verifies only that content survived, Excel recalculates every
cache on the way (its ROUND disagrees with Python's on exact halves and can move a rubric-pinned
figure by a cent) and reintroduces float dust that `fix_floats` removes, `fix_metadata` must see
the final bytes, and the gate on the zipped files is the only verification. `docProps/app.xml`
is never hand-edited: a generator string is cleared by really saving in Office, never by editing
the Application pair. Unzip both archives once and inspect them.

## Deliverables, exactly these

1. **The task directory** on disk, complete, printed once as a file tree.
2. **`i-<task-name>.zip` and `s-<task-name>.zip`** with `unzip -l` output for each.
3. **The prompt text** and **the rubric**, each in one fenced block ready to paste.
4. **The metadata block** printed from `metadata.json`: domain, occupation with its code, input
   and output file counts, the tools list, the four minute values and the total in hours.

Then stop. The only addition allowed is a short list of anything genuinely broken or unresolved
that the operator must act on before submitting; if there is nothing, say nothing.
