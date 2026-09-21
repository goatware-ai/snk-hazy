# Validation tooling refactor plan

The plan shipped on 2026-09-04: checks live in `tools/gcheck/` by group under a `@check` registry, with `tools/autoeval_check.py` and `tools/review_check.py` as the drivers (the one-line rule per check id is `docs/rules.md`). Sections 1 to 6 (the pre-refactor read of the monolith, the proposed shape, the registry contract, the migration order and the regression diff) were removed on 2026-09-11; the execution record below is what remains because tool docstrings cite this file.

## 7. Execution record (2026-09-04)

Done in one session, with the regression diff of section 6 run against two baselines: the
15 live folders under `submissions/` and the 20 accepted zips unpacked into a scratch corpus.

- **Package name** is `gcheck` (`tools/gcheck/`), laid out as in section 2 with two
  simplifications: `gate_families.py` stays where it is (memory and docs cite the path) and
  gains `REVIEW_TIER`; the repair tools stay flat under `tools/` for the same reason.
- **The hubs were split first** (`check_rubric` into 14 functions, `check_authorship` into 11)
  by line-range surgery on the monolith, then a generator carved every top-level definition
  into its module by usage. Helpers used by more than one module went to `common.py`;
  everything else followed its sole user. Check bodies are verbatim.
- **Order** is preserved by `_order.py`, generated from the monolith's call sequence. The
  one deliberate change: `check_chain_scope` was called twice and its R74 findings printed
  twice; it now runs once.
- **Id collisions resolved**: A18, R87, R89, R90, R91, R92, R93, R94, R95 and P5 as listed
  in the archive header. The registry now refuses a shared id at import time (A6 is the one
  allowed exception, one rule on two surfaces). One `.gate-debt` line changed
  (39-dock-to-stock-review, P2 to P5). A hidden shadowing also surfaced: `_MONTHS` was
  defined twice in the monolith, a string for R71 and a dict for R23, and only import
  order kept both working; the R71 form is now `_R71_MONTHS`.
- **Rule-map holes closed**: R78, R79, G5 and A17 printed as unmapped on every run of the
  old gate and are mapped now.
- **Review harness**: `review_check.py` stages `_task/` and runs the registry; its own
  copies of R11, the file-name criterion, the generator-string and unreadable-workbook
  checks were deleted. Kept review-only: platform verdicts, zip role matching, two
  negatives, style caps, weight-in-text, evaluative wording, the zero-formulas bar, the
  broad figure sweep, the fidelity ledgers and the package sweep.
- **Regression**: the gate's sorted findings match both baselines except the renamed ids,
  the de-duplicated R74 lines, the closed NOTE holes, and two messages (R51, R22) whose
  wording depends on set iteration order and differed run to run before the refactor.
- **`needs` recomputed from code**: the first derivation read comment text, so A14 read
  "metadata" in a comment and skipped itself in review; ten decorators changed.
- **Satellites folded (same day, on request)**: rubric_lint became
  `golden_rubric/lint.py`; prompt_check's P0-P3 joined `prompt_inputs/prompt_frame.py`;
  audit_task became `packaging/hygiene.py` with ids H1-H5 and a new PRE-PACK rule, so its
  findings now carry ids and reach the consolidated view (before, one anonymous error for
  any number of failures); originality_check split into `prompt_inputs/uniqueness.py`
  (U1 U2) and `authorship/package.py` (G2a-G2d); both carry the `originality` need,
  which the gate supplies only with `--originality` (G2c/G2d fire on 14 of 15 live
  submissions and are a portfolio-wide condition by the 2026-09-02 ruling, not debt) and
  review supplies always;
  package_sweep's `inspect()` moved beside A14 in `authorship/package.py`. All five CLIs
  remain as shims with byte-identical output on the sampled folders. The repair tools stay
  separate by the operator's decision: the package only reads.
- **Not done**: `--catalog` prints the registry but the per-check rationale still sits in
  the archived docstring and the function comments rather than a `source=` field.
