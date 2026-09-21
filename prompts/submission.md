# Prompt: build one accept-on-submit Hazy task

You are authoring **one** submission for Snorkel's Project Hazy (GDPVal++), the benchmark of
economically valuable, real-world professional workplace tasks. `./docs/submission/` is the
authoring rule set: `platform/` holds the live GitBook captures and they win on any conflict;
`workflows/` is the working decomposition, one stage per file, and is the build order. Every
check id cited here is defined in `docs/rules.md` and run by `tools/autoeval_check.py`.

**Assigned sector:** Wholesale Trade (confirm on the platform at submission time).
**Practitioner profile to write as:** purchasing and inventory analyst at a mid-sized regional
distributor (plumbing/HVAC, electrical, or food-service supplies: 3,000 to 5,000 SKUs, a few
branch locations). Day to day: supplier cost-increase letters, sell-price files against margin
floors, landed-cost calculations, reorder-point and safety-stock planning, dead-stock reviews,
supplier rebate reconciliation. Deliverables go to the purchasing manager and branch GMs.

**Occupation.** Pick only from `docs/submission/platform/platform-wholesale-trade-occupations.md`,
and pick against the prompt's actual requested work, the object it names and the whole sentence
of each task pick (M1, M2). Quote task and skill selections exactly as the form lists them.

## Read before designing anything, in this order

1. `docs/submission/platform/project-guidelines-v5.1.md` (in full, especially "What's New in V5.1")
2. `docs/submission/platform/task-lifecycle.md` (every gate the submission must clear)
3. `docs/submission/platform/creating-input-files.md`
4. `docs/submission/workflows/01-ideation.md` through `07-pre-submission-audit.md`
5. `docs/submission/platform/platform-submission-form.md`: only the section headed
   "Verified dropdown contents" (the O*NET task picks, quoted verbatim)
6. `docs/submission/platform/wholesale-trade-uniqueness-map.md`: only the subsection under
   "Fresh task ideas for this sector" for the chosen occupation, plus the category you land in
   under "Analytical-ask categories already accepted"
7. `docs/submission/platform/style-guide-llm-tells.md`: on demand, when A10 fires or a
   sentence reads generated

## Objective

The only thing that decides anything is **whether this submission is accepted on the first
pass**. The floor is a hard gate in both directions: under a 3-hour manual workflow is sent
back (target 5+ hours so an unsympathetic estimate clears); a frontier model producing the golden
correctly on the first try is sent back as too easy; difficulty living in the prompt instead of
the input files and cross-file reasoning is sent back as decoration. Build something genuinely
hard for a model, grounded in real practitioner work, and land it cleanly on every packaging and
rubric gate the first time.

The pipeline (`task-lifecycle.md`): seven in-app pre-submission checks, ten post-submission
evals (the golden_solution_check needs all three agents at 1.0000; the difficulty_check sends
the task back as Easy when the worst-agent accuracy exceeds 80%, so design for both models well
under; the llm_authorship_check; leakage, self-containment and safety audits), human review
(maximum 5 total reviews), then an adjudication pass whose minor fixes bypass human review.

## Hard constraints (any miss is a send-back)

**Prompt**
- A professional workflow from the sector, US-based, grounded in work the profile actually does.
- The opening frames the state, the requester's role and the reader's experience, woven into the
  handoff and never as a self-introduction to a coworker (P4, P6;
  `docs/submission/workflows/02-prompt-writing.md`).
- Sentence mechanics in the prompt, every input document, every golden text cell and the rubric:
  comma before a clause-joining conjunction, never three clauses in one sentence, serial comma
  (A20 codes the first two; the comma splice and the serial comma are a read).
- Natural practitioner voice, no "You are a ..." opener, no step-by-step procedure, no stacked
  adjectives, no vague stakes (A10, P7). It names exactly one output file by exact name (two
  co-equal deliverables fail the Prompt Quality Check; fold companions into the one artifact),
  names every input file without purpose glosses (P5), is self-contained, and cannot be answered
  without the inputs. It says **what** to produce, never **how**: no dictated steps, columns or
  formulas, no derived parameters (P0 to P3).
- 3,000 characters at most (the form's field cap).

**Input files**
- 1 to 20 files, 30 MB at most, 2+ strongly preferred. Real, or indistinguishable from real
  (`creating-input-files.md`): an LLM may assist, the result must read as a document the
  practitioner works from. No PII, nothing paywalled. Substance over decoration (A11, A12).
- No round-number giveaways, no generic or LLM-lexicon company names, no 555 phone numbers, no
  placeholder entries, no notes column that reveals what the solver should deduce; stored values
  at field precision (F1), no arithmetic series in a data column (A15). Period, entities,
  currency and jurisdiction agree across files; realistic messiness (duplicates, inconsistent
  naming, cancelled records) is fine, a mismatch on those four is an error.
- Every snapshot input references only records dated on or before its own date, and any "as of"
  balance re-derives from the registers date-filtered (G22): pick the cutoff first and clamp
  record dates to it.
- A deliverable date the prompt gives ("I need it ...") and the golden's Date line fall at least 21
  days after the build, or the prompt gives no due date (P8): review runs weeks after the build,
  and a deadline already past reads as an impossible timeline.
- **No answer leakage**: inputs never carry the solved output, pre-computed results the task asks
  for, or meta residue (L1, L2, L3, L4), including hidden tabs, hidden or filtered rows and columns,
  comments, tracked changes, document properties and file names. No project or evaluation
  reference anywhere in any shipped file's content, name or metadata, and the word "Hazy"
  appears nowhere (N1). A tell found and fixed while building goes in a standalone tell log,
  never inside an input or either zip (T1).
- **Package provenance is a stop, not a cleanup:** batch generator strings, one shared write
  instant, identical docx components, shared rsids (G2b, A3, A14) read as generated
  inputs and are a rejection without a revision cycle.

**Golden solution**
- Answers every part of the prompt, fact-checked, client-ready: documents polished, spreadsheets
  on live formulas with a cached value in every formula cell (A9, A17), output names matching the
  prompt exactly, every file opening cleanly (A16). Summary counts and conditional sums are
  COUNTIF/COUNTIFS/SUMIFS, dot products SUMPRODUCT(range,range) (R96).
- It survives the reviewer's literal read against the inputs and the prompt before the rubric is
  drafted (G8, G9, G10, G22; `docs/submission/workflows/04-golden-solution.md`, "The reviewer's
  read"): every cited identifier exists in a shipped input, no action is dated before the
  document's own date, a signed document is carried with its signature line, and every dated
  claim is written in an input or derived by a stated rule.
- It never contradicts the prompt or the rubric, even by one number (G1, G5, G7, G21), and it
  scores ~100 on the rubric.
- Nothing in the task teaches materially unsafe practice: the safety check fails a golden that
  normalises an unsafe act even when every number is right.

**Rubric**
- 15 to 60 criteria (R11), one simple atomic sentence each (R55), explicit values the golden
  actually states (R20, R21), every prompt instruction covered (R4, R13). Rigid criteria state the exact answer; judgment calls score the
  reasoning and name the conditions any sound alternative meets. Never several record ids in one
  criterion; phrase over the class or split.
- Weights +1 to +5 and -3 to -5 in the numeric field only (R12), at least one core row at +4/+5,
  no flat weighting (R99); each criterion 500 characters at most.
- At least two negatives, worded as the defect committed, critical-only (safety, privacy, an
  inverted decision, fabrication: R67), each scoped to exactly the rows it should penalise and
  tested against every row class of the golden (R28, R33, R37, R52); the penalty share is a
  recommendation, never a bar (R61).
- Style and formatting rows under half the count and a quarter of the reward; one criterion
  carrying the exact output basename (R83); a contradiction check and a domain-correctness
  clause. No single liveness criterion may carry more than the completeness cap (R24), and owner
  rows never name the person (R81) and score an owner or a date only when the prompt asks who
  and by when (R100).
- **The shape the Rubric Quality Review expects** (three needs_improvement ratings on gate-clean
  rubrics, 2026-09-11): the core deliverable's cluster holds 12 to 15 DIRECT points of 39, +2 on
  the rows that decide something, never six or more rows all at +1; the two +5 strict rows
  sit on two different deliverables' outputs, never a unit count beside the dollar total of one
  order (R114) nor two cells of one page (R117), and the page a row calls first is the
  workbook's first worksheet (R120); one formula-only gated row at most, every other
  gated clause riding on a value row (R118); a row over a computed figure names its value or its
  reconciliation, never presence alone (R119); an "each item ... N items" row is written as the count row plus separate spot
  checks; negatives put the deliverable in the actor's seat ("The workbook wrongly books ...",
  R111); no golden-only tab name in any criterion, name what the tab is (R112).
- **The rubric must fail the golden's own defects:** pin the facts a reviewer verifies (each
  cited identifier, the document's date, the signature line, the closed status of every policy
  class), so an error in the golden loses points under its own rubric.

**Package, metadata, uniqueness**
- Both zips flat: no subfolders, no empty files, no spaces, no double extensions, accepted
  formats only, input names, prompt references and output names agreeing exactly (H1 to H5).
- Metadata: occupation as above, then 3 to 5 tasks and 3 to 5 skills chosen after it (skills
  from the Skills section, never Technology Skills); multimodal matches the zip (.pdf and .pptx
  count as images); web-search matches the prompt; the time estimate reflects the manual hours.
- No spelling or grammar errors anywhere, no em dashes anywhere (A6).
- **LLM authorship is the highest-severity gate:** the prompt is human-authored, and inputs and
  golden read as human work (A10; mean score under 3.5 is NEEDS_REVISION, one HIGH tell is a
  return without review, two MEDIUMs in one file compound to a HIGH).
- **The task is unique** (U1, U2): the platform diffs every new prompt against prior tasks on
  scenario, reasoning path, constraints, input kit and deliverable. Choose the concept as an
  ask-category by occupation cell per `01-ideation.md`, avoid the crowded categories on a
  crowded occupation, prefer a thin occupation, and test the candidate's reasoning-path sentence
  against the chosen category's accepted-ask list and this portfolio's own history before
  building.

## Design targets

1. **Concept.** One workflow, unambiguously inside the sector, with a real decision at stake.
   Discard anything answerable from general knowledge, template-shaped, or outside the profile.
2. **Difficulty.** How much has to be true simultaneously across the files: reconciling
   conflicting sources, inferring the method from domain evidence, producing a native
   professional artifact. Not volume or obscurity. Pressure-test before building files: if a
   frontier model one-shots the answer from the prompt plus a sketch of the inputs, harden now.
3. **Files.** Could someone who never worked in this field have produced this layout? If yes,
   rebuild it with the conventions a real practitioner document carries. Each planted
   inconsistency is one the golden resolves and the rubric credits.
4. **Rubric.** Drafted alongside the prompt: everything graded is stated in the prompt or is
   ordinary professional standard, and everything the prompt requires is graded. Every ask in the
   prompt is mapped in `clause-map.md` to where the golden delivers it and a positive row that fails
   without it (R134), and the golden produces each asked-for artifact itself, in the form any input
   prescribes (one claim form per invoice means one form per invoice), never an action row that
   says to make it later (G41).

## Process

Do all of this work and do **not** narrate it: no candidate write-ups, no checklist
walkthroughs, no status commentary.

1. Read the docs in the order above, consider a few concepts internally, pick the one that is
   hard and lands cleanly. Do not present the alternatives.
2. Pick a task name: lowercase kebab-case, 4 words at most, descriptive of the workflow (e.g.
   `rebate-reconciliation-q2`). The **target folder** is `{target}/{seq}-<task-name>/`, where
   `{target}` is `drafts` under `/create-task` (see `prompts/create-task-brief.md`) and
   `submissions` only when the operator asks for a submission build directly; `{seq}` is the
   next number after the highest `{NN}-` prefix across `submissions/`, `accepted/`, `archived/`
   and `drafts/`. Never write into a previous task's folder. `submission-list.md` is owned by
   `/fetch-status`: a build never edits it.

   ```
   {target}/{seq}-<task-name>/
   ├── prompt.md            the prompt exactly as pasted into the platform
   ├── inputs/              every input file, final names
   ├── i-<task-name>.zip    flat zip of inputs/
   ├── solution/            the golden file(s), final names
   ├── s-<task-name>.zip    flat zip of solution/
   ├── rubric-<task-name>.csv         columns NUMBER, CRITERION, WEIGHT; UTF-8 with BOM;
   │                                  renamed rubric-<task-name>-<uid8>.csv once a Taskboard UID
   │                                  exists (<uid8> = its first eight characters); no rubric.md
   ├── metadata.json        form values only: task_name, taskboard_uid (null until submitted),
   │                        sector, onet_occupation {code,title}, onet_tasks[], onet_skills[],
   │                        input_file_count, multimodal, web_search_allowed,
   │                        manual_time_hours, llm_starting_point, built_with, build_session
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
   alignment rows). Do the reviewer's read of the golden (Golden solution, above) before the
   rubric is final. Score the golden against the rubric criterion by criterion and fix whichever
   side is wrong if it lands under ~100. Write `verify_golden.py` from
   `tools/templates/verify_golden.py`: it reads only `inputs/`, reproduces every figure the golden
   states, and lists every other reading a reviewer could take (rounding at each step, band
   boundaries, tolerances) with the phrase the golden uses to settle it, and the golden's method
   text states each of those phrases (G43). Write `clause-map.md` last, from the final prompt, golden
   and rubric (R134). Then run the Package sequence.

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
4. **The metadata block** (occupation, tasks, skills, booleans, time estimate) printed from
   `metadata.json`.

Then stop. The only addition allowed is a short list of anything genuinely broken or unresolved
that the operator must act on before submitting; if there is nothing, say nothing.
