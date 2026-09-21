---
name: repo-layout-and-tooling
description: "Repo conventions: {NN}-{task-name} folders with bare names in zips (i-/s-{task-name}.zip, flat) and on the platform; rubric-{task-name}-{uid8}.csv with NUMBER/CRITERION/WEIGHT; .venv tooling with the formulas engine installed; prompts/ templates per slash command; the tools/gcheck/ @check registry (2026-09-04), renamed ids, and the rules for writing and proving a new check"
metadata:
  type: project
---

## Folders and names

Task folders are `{NN}-{task-name}` in creation order under `submissions/`, `drafts/`,
`accepted/` (as zips) and `archived/` ([[submission-tracking]]). The prefix exists ONLY on the
folder: zips are **`i-{task-name}.zip`** (inputs) and **`s-{task-name}.zip`** (solution), flat,
files at the root with no wrapper folder (`cd inputs && zip ../i-<task-name>.zip *`);
`metadata.json`'s task_name and the platform name stay bare. Each folder carries prompt.md,
inputs/, solution/, metadata.json ([[task-metadata]]), feedback-log.md
([[feedback-log-convention]]) and the rubric CSV.

**Rubric CSV:** `rubric-{task-name}-{uid8}.csv` in `submissions/` ({uid8} = first eight
characters of the Taskboard UID), `rubric-{task-name}.csv` in `drafts/` until promotion; never
rubric.md, never bare rubric.csv, no sequence prefix (2026-08-26; the file's own name is what
`tools/rubric-filler`'s popup can read). Columns `NUMBER, CRITERION, WEIGHT`: integer
weights (4 / -3), UTF-8 with BOM, fields quoted by the csv writer (a comma added to an unquoted
field breaks the row)...), which the completeness check sums
([[rubric-coverage-and-completeness]]). Generate the CSV from the criterion list, never
hand-transcribe; on revisions insert, reorder and renumber 1..N freely (the old append-at-end
rule is dead). The platform dropped the per-criterion Objectivity and Content radio groups
(2026-08-19). Tools glob `rubric-*.csv`; `gcheck.common.rubric_path` derives the name from the
UID only when no file exists.

## Environment

- Run every tool from the repo: `.venv` at the root (`uv venv .venv && uv pip install --python
  .venv/bin/python openpyxl python-docx formulas`, Python 3.14). The `formulas` package (1.3.4)
  is the recalculation engine the cache procedures in [[package-hygiene-pipeline]] rely on.
- Keep only common tooling in `tools/` (see tools/README.md); per-task generators are session
  work product written in the scratchpad and never committed. Later revisions edit the delivered
  files directly (zip-level XML edits, office resave).
- `submissions/`, `accepted/`, `archived/` and `memory/` are git-tracked; `drafts/`, `reviews/`
  (other contributors' Not-for-Distribution files), `.venv/`, `__pycache__/` and `.DS_Store` are
  ignored. `memory/` is symlinked from `~/.claude/projects/-Users-aladdin-projects-snk-hazy/memory`;
  recreate the symlink on a new machine.
- Package order before every zip build: `office_resave.py` (`--force` after any python-docx edit)
  -> `fix_floats.py fix` -> `fix_metadata.py` -> build both zips -> gate (`autoeval_check.py`,
  `audit_task` H1-H5 at 0 failures). Detail in [[package-hygiene-pipeline]].

## prompts/ and commands

Reusable operator prompt templates live in `prompts/`, one per slash command: `submission.md`
(`/create-task`, with `create-task-brief.md` as the per-task brief), `revise-task.md`
(`/revise-task`), `review.md` (`/review-task`), `refine-task.md` (`/refine-task`),
`revise-refinement.md` (`/revise-refinement`). Commands in `.claude/commands/` route to
per-model skills ([[model-routing]]); `/fetch-status` is a skill ([[submission-tracking]]).

## tools/gcheck/ (since 2026-09-04)

`tools/autoeval_check.py` and `tools/review_check.py` are thin commands over one package,
`tools/gcheck/`, in four groups: `prompt_inputs/` (prompt_frame, occupation, input_quality),
`golden_rubric/` (rubric_form, negatives, landing, liveness, fidelity, leakage, sourcing),
`authorship/` (prose, package, workbook_shape), `packaging/` (hygiene). `core.py` holds
emit/recommend/debt and the `@check(codes, rules, needs, params)` registry; `driver.py` runs
submissions, `review.py` runs reviews. The five check tools (rubric_lint, prompt_check,
audit_task as H1-H5 under PRE-PACK, originality_check U1/U2 and G2a-G2d needing `originality`,
package_sweep) are shims with unchanged output; repair tools (fix_*, office_resave) stay
separate, the package only reads. Design record: docs/reference/tools-refactor-plan.md; old
docstrings: docs/reference/autoeval-check-catalog-archive.md.

- A new check is one `@check` function in the group that matches what it reads, with a NEW id
  (the registry refuses an owned id; ids are portfolio-shared across sessions, so check
  `gate_families.py` before numbering) and a `gate_families.PRIMARY` mapping. Never append to a
  shim. Renamed ids: A18 as-of date (was A10), R87 percentage basis (R31), R89 nested money
  literal (R32), R90 function token in liveness (R39), R91 'carries N' count (R39), R92
  grouped-presentation coverage (R46), R93 month-fragment landing (R57), R94 stored-form anchor
  (R58), R95 same total scored twice (R12), P5 file glosses (P2, until 2026-09-04; P2 now means
  the prompt names no input source). Older logs cite old ids by meaning.
- `needs` decides where a check runs: review packets supply prompt, rubric, inputs and solution
  only, so checks needing metadata, rubric_req or `folder` skip in review and the run reports
  it. `'folder'` in `needs` means the BUILD folder, which review never stages; declaring it opts
  the check out of review silently (it lands in `skipped`). Declare only what you read and test
  against all four packet shapes (both zips, input zip only, golden zip only, JSON-only). Review
  tiers come from `gate_families.REVIEW_TIER` (BAR for rules the reviewer guidelines state, else
  HOUSE).
- **A check is only done when it has been shown to FIRE on the artifact that motivated it** and
  stay silent on the fixed one (`git show HEAD:path` for the pre-fix artifact). G1 and R58 were
  born dead (a swallowed NameError from a bare openpyxl call; any-key row matching), R74 twice (a
  non-raw `'''` string turned `\b` into backspaces; a sheet name matched as an aggregate). Write
  rule blocks with `r'''...'''`; function-local `import openpyxl` is the convention.
- **Probe every candidate rule against rubrics already watched passing** before coding: four
  provenance-of-a-number rules, a prose-twin rule (13 passing rows), a negatives-only-subject
  rule (68 negatives on 15 rubrics) and a figure-free-positive rule (58 rows) all lit up passing
  work and were written down instead. A rule that cries wolf teaches people to ignore the gate;
  a rule that forbids what another check mandates is not a rule; narrowing a check IS writing it
  (R59's first cut flagged eleven 1.0 rows).
- Regexes that key on figures try `-value` too (house style quotes shortages and credits
  unsigned), keep money digits out of row-key patterns (`(?<![\d.,])\d{4,}(?![\d,]*\.\d)`), strip
  trailing zeros only after a decimal point, read labels straight off sheets (a 40-char cap hid
  a verdict label), and render figures the way the judge does (raw stored form beside the
  comma-formatted one). Print what a check names and diff it against what the platform named
  before trusting it.
- `.gate-debt` keys on (criterion number, rule): void every criterion-keyed line when a rubric is
  renumbered, and drop a file-level line the moment the rewrite closes it. `.gate-accepted`
  records a settled warning ("R11 = why"), warnings only, never errors.
- Regression method for any tool change: freeze a copy of tools/, capture sorted
  ERROR/DEBT/REC/NOTE lines per folder over submissions/ plus the accepted zips unpacked, change,
  re-run, diff. Set-order nondeterminism in R51 and R22 messages is pre-existing.

**The rubric CSV has no REQ column (operator, 2026-09-14).** It was a house-only tag column in
a file that otherwise mirrors the platform form, and it has been stripped from all 52 CSVs and
from every writer. The two checks it fed are deleted with it: the per-requirement cluster share
and the core-cluster weighting read. The platform's own full-credit completeness check still
exists and still fails on thin clusters, so that has to be judged by reading the rubric against
the prompt's requirements now, with no local arithmetic behind it.
- 2026-09-15 (rule-catalog cleanup): the selfcheck now fails a first docstring line that opens with an id, stops mid-sentence or runs under 30 characters, a PRIMARY family that is not a RULES key, and a PR id cited in memory, prompts, docs or .claude that procedural.py does not register; a crashing check is an ERROR and the rest still run; .gate-debt lines matching no finding print a NOTE; atomicity reports one finding per criterion and R20/R43/R50 wait for atomic criteria; tools/fixture_suite.py runs the planted-defect fixtures in tools/check_fixtures/ and prints catalog coverage, so add a fixture with every new check; G2a, G2c and G2d retired; P4 and P6 now map to PRE-FRAME.
