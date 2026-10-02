# Prompt: build one accept-on-submit Hazy task

You are authoring **one** submission for Snorkel's Project Hazy (GDPVal++), the benchmark of
economically valuable, real-world professional workplace tasks. `docs/README.md` explains how
the rule set is organised and which document wins a conflict: the platform captures in
`docs/submission/platform/`, led by `platform-submission-form.md`, govern; `house-rules.md`
holds this desk's own standards; `difficulty.md` is how a task is made hard; `workflows/` is
the build order, one stage per file. Check ids cited anywhere are defined in `docs/rules.md`
and run by `tools/autoeval_check.py`; where a workflow page states a count, a band or a weight
range, it and the platform section it names govern over `docs/rules.md`.

This file states the objective, the non-negotiables, the folder and the process. The detail
behind each item is in the page it points to; do not work from this summary alone.

## Read before designing anything, in this order

1. `docs/submission/platform/platform-submission-form.md`, in full: what blocks submission,
   and its section 5 checklist, every box of which must be true
2. `docs/submission/house-rules.md` and `docs/submission/difficulty.md`, in full
3. `docs/submission/platform/domains-and-occupations.md` and `onet-codes.md`, before any
   concept work
4. `docs/submission/platform/creating-input-files.md`
5. `docs/submission/workflows/01-ideation.md` through `07-pre-submission-audit.md`
6. `docs/submission/platform/style-guide-llm-tells.md`: on demand, when A10 fires or a
   sentence reads generated

## Objective

The only thing that decides anything is **whether this submission is accepted with as few
returns as possible**. Three things have to be true at once: the task takes a qualified
professional 5 or more hours without AI (the form's floor is 3); it is genuinely hard for a
model, with the difficulty in the input files and the reasoning across them rather than in
the prompt, built to the reviewer's bar and not only the platform's difficulty check
(`difficulty.md`); and it lands cleanly on every packaging and rubric gate the first time.

## Non-negotiables (any miss is a send-back)

**Concept** (`01-ideation.md`)
- The occupation is picked first, then the domain matching its O*NET job family; both are
  entries on the form's closed lists, and the code is confirmed on its onetonline.org page.
- One US workflow that occupation actually performs, with a real decision at stake for a
  named reader, unique against every task in this portfolio (U1, U2).
- Clinical, counselling and laboratory occupations: nothing teaches unsafe practice and
  nothing reads as a real patient record.

**Difficulty** (`difficulty.md`)
- The design read is done before the build is called done: every golden decision traced to
  the input fact it turns on (PR21), every rule exercised on both arms with a look-alike
  (PR22), no labelled trap (L7, L8), and a named misreading behind each decision that moves a
  graded figure.
- The package already carries the recurring shapes reviewers ask for: raw records rather than
  computed columns, no input that narrates the call, the decisive figure on its threshold, a
  stated convention that flips a figure, exact figures rather than Yes/No answers.

**Prompt** (`02-prompt-writing.md`)
- The requester's voice: the P4 frame (place, role, the reader's expertise) woven into the
  handoff, never a persona or a self-introduction (P4, P6); named role, organization and
  trigger; real scenario constraints.
- Every input file named by its exact Input File List name, at most half glossed (P5); every
  output file named exactly with its format and structural requirements (P1).
- What, never how; no number, name or finding that comes only from working the inputs; any
  due date at least 21 days after the build (P8).

**Input files** (`03-input-files.md`, `creating-input-files.md`)
- At least 2, 3 or more preferred, each load-bearing; names identical in the Input File
  List, the prompt and the zip (H5).
- Real or indistinguishable from real; no authorship tells, no batch-construction evidence
  (a stop, not a cleanup: G2b, A3, A14); no answer leakage anywhere, hidden places included
  (L1 to L4, N1, R23, G22).

**Golden solution** (`04-golden-solution.md`)
- Built in full before the rubric; answers every ask; client-ready; live formulas with
  cached values; survives the literal read; never contradicts the prompt or the rubric.
- `verify_golden.py` reproduces it from the inputs with every alternate reading named (G43).

**Rubric** (`05-rubric.md`)
- At least 6 criteria and usually 20 or more, no ceiling; one atomic sentence each; every
  value read off the golden, never hedged; weights non-zero integers in -5..+5 with at least
  one +4 or +5; weight on the calls the traps decide; negatives on specific observable defects,
  shaped per 05; the last row is the general formatting-and-style criterion.
- Every prompt ask mapped in `clause-map.md` to a golden anchor and a positive row (R134).

**Metadata and form** (`06-metadata.md`, `form-lists.md`)
- Domain, occupation and code; at least one non-AI tool; four integer minute fields and a
  total in hours at least their sum and over 3 (M4).

**Everywhere:** no spelling or grammar errors, no em dashes (A6), the comma rules (A20), no
project codename or evaluation vocabulary (N1).

## Process

Do all of this work and do **not** narrate it: no candidate write-ups, no checklist
walkthroughs, no status commentary.

1. Read the docs in the order above, pick the occupation and domain, consider a few concepts
   internally, and pick the one that is hard and lands cleanly. Do not present the
   alternatives.
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
   ├── metadata.json        the build keys in 06-metadata.md, plus the form copies
   │                        sync_metadata.py adds (08-fill-the-form-and-submit.md)
   ├── form-lists.md        what gets typed into the form: one Input File List entry per input
   │                        (exact name, a plain hyphen, what it contains), the Output File List
   │                        entry, the five time values, the tools, the domain and occupation
   ├── feedback-log.md      chronological log: date, source, verdict, then findings /
   │                        actions / form actions; one entry per piece of feedback
   ├── clause-map.md        every prompt ask -> quoted golden anchor -> positive rubric rows (R134)
   ├── verify_golden.py     re-derives the golden's figures from inputs/ alone, with its
   │                        alternate-reading pass (G43; start from tools/templates/)
   ├── <generator scripts>  optional: the scripts the package is regenerated from, kept so a
   │                        hardening revision rebuilds rather than patches (difficulty.md)
   └── struck-phrases.md    only once something is struck: one quoted phrase or /pattern/
                            per bullet, with source and date (PR20, G42)
   ```

3. Real, working content in every file: no placeholders, no `TODO`, no thin files;
   spreadsheets on live formulas; documents to client-ready standard.
4. Verify, quietly. Run the design read (`difficulty.md`). Do the literal read of the golden
   (`04-golden-solution.md`) before the rubric is final. Score the golden against the rubric
   criterion by criterion and fix whichever side is wrong if it lands under ~100. Write
   `verify_golden.py`, then `clause-map.md` last. Walk
   `docs/submission/workflows/07-pre-submission-audit.md` row by row, with particular attention
   to the MANUAL rows, and run its **package sequence** to 0 errors on the packaged files.
5. Walk the form's fourteen-box checklist (`platform-submission-form.md`, "5. Before You
   Submit"; mapped in section I of the audit), one box at a time against the built package,
   and fix anything that is not already true.

## Deliverables, exactly these

1. **The task directory** on disk, complete, printed once as a file tree.
2. **`i-<task-name>.zip` and `s-<task-name>.zip`** with `unzip -l` output for each.
3. **The prompt text** and **the rubric**, each in one fenced block ready to paste.
4. **The metadata block** printed from `metadata.json`: domain, occupation with its code, input
   and output file counts, the tools list, the four minute values and the total in hours.
5. **The `sync_metadata.py` report** from the package sequence, with every hole it named
   fixed.

Then stop. The only addition allowed is a short list of anything genuinely broken or unresolved
that the operator must act on before submitting; if there is nothing, say nothing.
