# Common task tooling

> **Ported from Geranium 2026-09-21.** The gate changed with the project: R67's negative
> allowlist was deleted, R11 and R12 were rebanded, M1-M3 were rewritten around Hazy's
> closed domain/occupation lists, and M4-M6, R135 and R136 are new. `../docs/RULE-DELTAS.md`
> is the record. `../docs/rules.md` is generated from this tree and must be regenerated
> (`autoeval_check.py --rules`) after any check change.

Generic, task-agnostic tools. Per-task build scripts are NOT kept in the repo —
each task's data generators live and die with the session that built it; any
later revision is applied by editing the delivered files directly.

## Environment (recreate on any machine)

    uv venv .venv
    uv pip install --python .venv/bin/python openpyxl python-docx

`.venv/` is gitignored; submissions/, accepted/, archived/, and memory/ are
tracked. Claude's persistent memory lives at `memory/` in the repo root — the
path `~/.claude/projects/-Users-aladdin-projects-snk-hazy/memory` is a
symlink to it; recreate that symlink after moving to a new machine.

## Tools (run from repo root with .venv/bin/python)

- **gate_families.py** `[RULE-ID]` — the consolidation layer over the coded checks.
  Every check id in gcheck is mapped to one of
  **35 generalized rules** grouped under the reports the platform actually returns in
  EVALUATION_PENDING: the golden solution check (GOLD-LAND / LIVE / KEY / NEG / FID),
  the LLM authorship check (AUTH-PKG / FAB / NUM), rubric quality (RUB-ATOM / OBJ /
  POL / DUP / COVER / FORM), and the adjacent gates (DATA / SKILL / LEAK / UNIQ).
  Run bare to list the rules, or with a rule id for the full statement plus the coded
  checks that implement it. It also carries the flake-exposure model — P(all 3 oracle
  runs at 1.0), fitted to this portfolio's own 23 logged oracle rounds. autoeval_check
  imports it; a coded check missing from the map is reported as a hole on every run,
  so new checks cannot silently fall out of the consolidated view.
- **autoeval_check.py** `[--no-caches] [--brief] [--record-debt] [--originality] [--catalog] [--selfcheck] [--rules] [task-folder ...]` —
  one-command AutoEval pre-flight. No args = every folder in submissions/. Exit 1 on any
  error. Run before every submission/resubmission. Since 2026-09-04 this file is only the
  command: the checks live in **gcheck/**, one registered function per check, grouped by
  the artifact under test and the platform report that judges it:

      gcheck/prompt_inputs/   group 1  prompt_frame (P0-P7), occupation (M1-M6),
                                       input_quality (A7 A11 A12 A16 A18 G22 R23), uniqueness (U1 U2)
      gcheck/golden_rubric/   group 2  rubric_form (form, coverage, subsumption, atomicity),
                                       negatives (polarity, scope, the mirror family), landing,
                                       liveness, fidelity (G1-G21), sourcing (G11-G13 R97),
                                       leakage (L1-L3 N1 H1 T1), lint (the E/W oracle-wording rules),
                                       conformance (R134 clause map, G41 deferred deliverables,
                                       G42 struck phrases, G43 golden verification)
      gcheck/authorship/      group 3  prose (A6 A10 A20), package (A3 A13 A14 A19 G2b),
                                       workbook_shape (A1 A2 A5 A8 A9 A15 A17 F1)
      gcheck/packaging/       group 4  hygiene (H2-H5, the audit_task sweeps)
      gcheck/core.py          emit/recommend/debt, the @check registry, run_checks, selfcheck,
                              the docs/rules.md generator
      gcheck/state.py         TaskState: the task folder as a Path carrying every parse the run
                              has made (workbooks in both modes, documents, rubric rows, prompt,
                              metadata, input texts, formula cells), opened once per run
      gcheck/common.py        the one home for each shared helper: load_rows, input_texts,
                              package_texts, generator_of, split_sentences/split_clauses, the
                              month table, the solution value bags
      gcheck/procedural.py    PR1-PR4, house rules with no detector, registered so they have an id
      gcheck/driver.py        the submission runner; gcheck/review.py the review runner

  Every check declares its ids, its generalized rules and its `needs` (prompt, rubric,
  rubric_req, inputs, solution, metadata, folder, originality) and carries a structured
  docstring: first line the canonical one-sentence rule (a `Codes:` block gives one line per
  id when a check emits several), then `Since:`, `Source:` and `Drift-notes:`. Checks run
  grouped (core.GROUP_ORDER) in registration order inside each group; there is no separate
  order table. Families that read one property (the mirror detectors R15/R22/R41/R69/R104,
  the subsumption detectors R10/R47/R57/R60/R86, the atomicity detectors
  R27/R49/R54/R55/R85/R105) are one walk each, and the 2026-09-04 carve-out twins
  (R90 R44 R91 R94 R93 R92 R38 P5 A18) are branches of their parent checks again; every
  id is kept, so `.gate-debt` files, memory and docs cite the same codes as before.

  **Registry hygiene runs before every gate** (`--selfcheck` runs it alone, exit 1 on a
  failure): every check has its rule statement, every `[CODE]` a check's source emits is
  declared, every module's code literals belong to a check in that module, and every
  check's `rules` agree with gate_families.PRIMARY. `--catalog` prints every check with
  its ids, rules, needs and rule. `--rules` regenerates **docs/rules.md**, every id under
  its gate_families stage, family and rule with the canonical statement, plus the
  procedural rules; regenerate it after any check or family change.

  **Findings are binary.** There is no advisory tier (removed 2026-08-24): a check either
  proves a defect and errors, or it does not exist. The one side channel is `recommend`,
  reserved for findings the programme has ruled non-blocking in terms (R61).

  **Pre-existing findings** — a check added after a task was submitted — are recorded per
  task in `submissions/NN-x/.gate-debt`, reported as DEBT and not counted, so an in-flight task
  still gates clean while anything NEW errors. Debt is per finding, never per rule. Generate
  one with `autoeval_check.py --record-debt <task-folder>`.

  Every run ends with the **consolidated gate view** from gate_families: a per-stage
  FAIL/debt/ok verdict stated as generalized rules, and for the golden solution check the
  criterion count, the flake-prone count and the odds of clearing all three oracle runs.
  `--brief` prints only that view; multi-folder runs add a rollup.

- **review_check.py** `reviews/<review-id>` — the review harness. Reads the fetch-task JSON
  and the two zips, stages them as a task-shaped folder (`_task/`), and runs every
  registered check whose needs that folder satisfies through the same `core.run_checks`
  and TaskState the gate uses, tiered by `gate_families.REVIEW_TIER`: [BAR] for rules the
  reviewer guidelines state, [HOUSE] for this repo's own conventions, never a send-back.
  Platform verdicts, zip role matching, the fidelity ledgers and the package sweep stay
  review-only, and so do its four hand sections (packaging, rubric_structure,
  golden_vs_rubric, inputs_substance): they print context lines and reviewer-bar findings
  the registry does not reproduce (an input the prompt never names, a criterion figure
  absent from cells and prose alike, a golden with no formulas). Checks needing
  metadata.json or the build folder skip themselves there and the run
  says which.

- **restore_submission.py** `<uid> [...] [--all-needs-revision] [--dry-run]` — rebuilds a
  `submissions/{seq}-{name}/` folder from the platform. Needed because a UID that drops off
  `stb submissions list` is archived (folder reduced to `archived/{seq}-{name}/prompt.md`), and
  when the platform later re-lists it as NEEDS_REVISION the row comes back but the package does
  not, so `/revise-task` has a row and nothing to revise. `stb submissions download` cannot help
  ("has no uploaded file to download"); everything comes from `stb submissions fetch-task` —
  prompt and criteria as text, the input and golden zips as S3 URIs pulled through stb's
  presigned-get helper under stb's own interpreter. Rebuilds prompt.md, inputs/, solution/, both
  flat zips, the rubric CSV, metadata.json from the form's own values, and a feedback-log entry;
  then removes the archived/ folder. **What cannot come back:** build_session and any feedback-log
  history the archive discarded. `built_with` comes from submission-list.md's Model column. Plain
  `python3`, no .venv needed.

- **fetch_refinement.py** `<uid> [--name task-name] [--force]` — pulls a Hazy-Refinement
  task off the platform into `refinements/<uid>/`, ONE flat folder in the exact shape of a
  submission folder (prompt.md, inputs/, solution/, rubric-<task-name>.csv, metadata.json with the O*NET code resolved from the form's dropdown, feedback-log.md,
  both flat zips, and change.log / review-comment.md skeletons for what changed and the Section
  3 paragraph), so every gate above runs on `refinements/<uid>` unchanged. Two pieces of the
  hand-over are kept verbatim beside it, `original-prompt.md` and `feedback.md`; the rest is
  downloaded to a scratch directory and removed. There is no `original/` and no `refined/`
  (2026-09-11). `stb submissions download` cannot do this (it only serves the zip you
  uploaded); the seed zips are S3 URIs inside the fetch-task JSON, fetched through stb's
  presigned-get helper under stb's own venv. Re-running re-downloads the hand-over, rewrites
  those two files and says whether the feedback changed. Plain `python3`, no .venv needed. The one `stb` use
  `/refine-task` permits.

- **rubric_lint.py**, **prompt_check.py**, **audit_task.py**, **originality_check.py**,
  **package_sweep.py** — since 2026-09-04 these are commands over code that lives in gcheck,
  kept for fast single-purpose iteration and for the workflows that name them:
  - `rubric_lint.py [rubric.csv ...]` — the E/W oracle-wording rules, now
    `gcheck/golden_rubric/lint.py` (its docstring is their catalog); the gate runs them
    through `check_rubric_lint`.
  - `prompt_check.py <task-folder ...>` — P0-P3, now in `gcheck/prompt_inputs/prompt_frame.py`
    beside P4 and P5. P2 and P3 are a BAND on the same dial: naming no input fails the
    platform's "Prompt input files reference check", glossing nearly every input fails its
    "Prompt human voice check".
  - `audit_task.py <task-folder>` — the hygiene sweeps, now `gcheck/packaging/hygiene.py`
    with ids H1 canary, H2 555 phones, H3 calendar-false weekday, H4 name/extension/empty
    and zip-member hygiene, H5 a prompt-named file the folder lacks. The gate emits each
    as its own finding; the command still prints FAIL lines and the future-date count.
  - `originality_check.py <task-folder>` — U1/U2 prompt recycling
    (`gcheck/prompt_inputs/uniqueness.py`) and G2b input packet forensics
    (`gcheck/authorship/package.py`). Inside the gate they run only with `--originality`
    (a build-time gate for the task being built; G2c and G2d, retired 2026-09-15, held portfolio-wide on the
    python-docx template and are not per-task debt), in review_check always. The command
    keeps its single-folder contract and the G2 rule stays a STOP, never a cleanup.
  - `fixture_suite.py [fixture...]` — planted-defect fixtures in `check_fixtures/`: each one asserts
    which codes fire and which stay silent on a temporary copy, then the run prints how many
    catalog codes carry a fixture. Add a fixture with every new or narrowed check.
  - `package_sweep.py [root...]` — the portfolio-wide, report-only sweep; `inspect()` lives
    in `gcheck/authorship/package.py` and review_check calls it there.

- **fix_floats.py** `scan|fix <xlsx...>` — rewrite float-repr tails in cached
  values (`34.04799999999999`) to shortest clean decimals. The LLM-authorship
  check flags these HIGH. Run `scan` on every xlsx (inputs AND solution)
  immediately before every zip build.
- **audit_task.py** `<task-folder>` — pre-zip sweeps: Hazy canary (incl.
  embedded metadata), 555 phone numbers, calendar-false weekday/date pairs,
  zip hygiene (flat/no spaces/no double extensions/no empty files), prompt
  file-name references, and a review list of future dates (each must be a
  genuinely prospective deadline).

## Standard pre-zip sequence for any task

    # 1. Recalculate formula caches: open the solution workbook in a spreadsheet
    #    app and save (openpyxl leaves cached <v> values empty; judges misread
    #    empty caches). The in-repo formulas-engine injector was removed
    #    2026-08-19 per user — rebuild from feedback history if ever needed.
    .venv/bin/python tools/fix_floats.py    fix  <all xlsx>
    .venv/bin/python tools/autoeval_check.py     <task folder>   # 0 errors
      # (runs fix_floats scan, empty-cache scan, audit_task, rubric_lint
      #  and the authorship/rubric/metadata catalog checks in one pass)
