---
name: rubric-liveness-criteria
description: "How a formula-liveness criterion survives the oracle judge and the completeness check: what the judge can and cannot see, the reference-chain and tab-gestalt shapes, anchor selection (R9/R42/R45/R46/R51/R59/R72/R98/R106), the two-row cap and drop rules (R17/R24), the gated tier (R29/R73/R76/R96/R109), golden-side design for live decisions, the solved reward model and judge-side artifacts (to 2026-09-11)"
metadata:
  type: feedback
---

Open before writing, re-anchoring or dropping any criterion that scores stored formulas. The
sibling files: [[rubric-anchoring-and-landing]] (how any criterion lands on a cell),
[[rubric-negatives]], [[rubric-coverage-and-completeness]], [[rubric-criterion-count]] (the
weight arithmetic these rules live inside), [[golden-fidelity]].

## 1. What the judge can see

- The oracle judge greps CACHED VALUES. `search_xlsx` never reads formula text, so any function
  name in a criterion, head call or nested, is a string it searches the values for and fails to
  find (C18 nested LARGE 3/3, C44 head COUNTIF 3/3). Never name a function
  token in a criterion; R6 and R90 flag them. R30's old ask for a named head function is settled
  in .gate-accepted where it conflicts; the oracle wins.
- `xlsx_formula_summary` surfaces column-dominant formulas and plain reference chains. A single
  footer cell (=COUNTIF, =SUM) is invisible to it (C24 3/3). A compound cell
  (=SUMIFS(...)+IF(...), =A53+A54, =MIN(B9,B13), =B5-B15) reads as typed to one judge in three
  (C29, a task run 6, C-strict); a boolean-product SUMPRODUCT
  ((range="x")*range) reads the same way (R96).
- A judge also reads sheet-level typed-share statistics and infers "the rollup is typed" without
  opening a cell (a run 4), and it stalls at an arithmetic hop when tracing a chain
  (a run 5: R3 -> E3 =C3*D3 -> C3 SUMIFS rejected at the multiplication).
- A verdict aggregation over one cell's stored content is a coin flip; a TAB's uniform formula
  picture is verified reliably (chemical-lot rounds 3-7: single-cell claims flaked six times,
  the page-level claim passed 16/16 with no anchor).
- A row sweep ("each of the N rows draws its quantity by cell reference") multiplies W11's sweep
  flake with the extraction misread and one misread row sinks it (C29 2/3); with no
  landing cell the judge may INVENT the formula it expected and fail the golden against its own
  guess (792-row zone claim, a VLOOKUP nowhere in the workbook).
- A counterfactual ("removing an item recomputes ...") cannot be executed on a static file and
  fails (a run 3).

## 2. The shapes that hold

- **Reference chain.** The front page's figures stored as `=Tab!Cell` reading through to the tabs
  that compute them. This is the only liveness shape the judge has verified from its own evidence
  (it quoted formula='=Impact!I60' beside the displayed value). It has never flaked when the
  criterion is worded on a NAMED SET of same-tab cells that are uniformly pure references, names
  only tabs (no row-binding hop like "to the lot's row"), and carries one "exactly N" value anchor
  for R9. Two +5 unanchored front-page read-throughs are the strict shape with the longest clean
  history (a task nine of nine, a task, a task).
- **Assert on the READING cell, not the link** (C5): name the cell that reads through
  by its column header plus its row key, and say what it reads. "The usage page holds the formula
  and the position page reads through" lets the judge quote the source and deny the link.
- **The subject cell must be the shape the row names** (R98): a strict row's own subject cell is
  `=Tab!Cell` or one aggregation call. Same-sheet arithmetic over live cells reads as "calculated
  within the sheet rather than through a cell reference" to one judge in three. R72 resolves each
  strict reference-claiming row's pinned decimal to its golden cells and errors when none is a
  plain reference or a pure single call; the words "cell references" satisfy R30 while the cell is
  a =ROUND(arithmetic), which is exactly the R72 case.
- **Admit live alternatives** (R76): "reaches its value through a plain cell reference into the
  branches tab, or an aggregation over the same rows alike". A row that prescribes plain
  references alone is a gold-only tactic lock and the completeness check discounts it ("a valid
  workbook using SUMIFS could lose 10/39"). Do not name a sheet in the alternative ("over the
  history" reads as a sheet key to R38).
- **No grader instructions** (R18): "judge from stored formulas", "verify by reading the cell
  formulas", "is a pass", "does not fail this criterion", "credit here is for", "scored by their
  own criteria" all fail the platform's negative polarity check. State facts about the artifact:
  "the numbers shown in them are the cached results of those stored references", "the quantities
  on the tabs behind them are source data typed as it comes", "a cell reaching its value through a
  plain cell reference to such a formula is formula derived rather than a typed constant". Keep
  liveness rows VALUE-FREE apart from the one R9 anchor, so no disclaimer is needed.
- **Never a single-cell formula-property claim, never "every row", never a function name, never
  a counterfactual.** After one flake on a single-cell liveness row, re-key it into the gestalt
  shape immediately, not onto another single cell.
- LIVENESS_STRICT_RE keys on fixed phrases ("live formula", "reaches its value from/through",
  "rather than typed"); a rewrite that drops them all silently stops counting toward R24. Check
  the R24 output after every reword.

## 3. Choosing the anchor

The R9 value anchor beside a liveness clause has to satisfy four checks at once, so scan before
choosing and re-scan after every workbook change (fixing one cell can free a better anchor):

- **Owned by no other criterion** (R45/R47): the near-identical check fails a liveness row whose
  anchor figure another row scores, because passing one proves the other. List every figure on
  the graded tab and mark which criteria own them; anchor on the one free figure (a row count, a
  year's net purchases), and fix the criterion you last changed, not the one that has been passing.
- **Clean under R42**: the holder is one pure function call or a plain reference, never
  `=A53+A54`. Fix the cells rather than re-anchoring (`=K15*L15` -> `=ROUND(K15*L15,2)`, a running
  `=O15+IF(...)` -> `=SUMIF($P$15:P15,"defer",$M$15:M15)`); a re-anchor is only free when the new
  figure is clean AND unpinned. R42 accepts a bare same-sheet `=C5` as well as `='Tab'!C5`.
- **No twins**: not a COUNTIF over a text pattern many cells match (R46, the judge reads the rows
  and never reaches the footer), not repeated on its own row (R51, quantities as well as money),
  not totalled twice in two blocks of one tab (R59, delete one total), not sitting in an
  unlabelled numeric grid. Rank candidates by whether BOTH ends of the chain sit on labelled rows
  (a task's 949: SUMIF on a supplier-labelled row, read through on a row labelled the same way).
- **A count anchor needs one cell that reports it**: look for a wording the data already supports
  so one COUNTIF reaches the number by itself (a task's "the requested date stands").
- **Label the anchor in the cell's own words** (R106, 2026-09-11): "the allowance standing at exactly
  $16,189.44" in a sentence that had already used "allowance" for the running total and the
  allowance used sent one run in three to the other figure (one revision round, 0.8913 on a
  +5). A one- or two-word label that recurs in its own criterion errors; write the label beside
  the cell ("the allowance at five percent").
- **Both ends on one sheet with the rest of the chain** (R43): every sheet carrying the pinned
  figure must carry the rest of the criterion's figures too, since the judge picks the sheet.
- When the same criterion fails twice on the same TAB, move the anchor off the tab; rewording is
  the wrong lever once the location is the problem (a task run 7).
- Twins whose cells AGREE with the claim have survived five submissions and stay as .gate-debt;
  the conflict case (credit beside overbilled) is the killer.

## 4. How many, and when to drop

- **At most two formula-only liveness positives** (R17): each is an independent 3/3 flake risk
  (C25/C26/C27 identical wording, one failed 2/3). Both sit at +5 because R24 needs each
  alone to cost over 10% of positive plus a one-point cushion ([[rubric-criterion-count]]).
- **Weight does not protect a row**: the 3/3 rule fails on a +1 (one run 5 lost one +1 in
  two runs). Hunt flakes regardless of weight.
- **Drop at ONE flake when a proven 3/3 row can carry the weight** (a run 3); after TWO
  flaky runs on the same row stop rewording and change its SHAPE (C29, C8).
  Three rewordings in three rounds is the same signal. When a shape fails twice on different
  instances, retire the shape everywhere in one pass (one task bled four rounds fixing one
  instance each).
- **A flaky liveness row often cannot be dropped or widened**: R24 needs both +5 rows, widening to
  a column is W16 (row sweep) plus R90 (a function token in the header), so SHARPEN instead:
  narrow the subject to one named cell whose own value is the anchor, or re-key onto the gestalt.
- A liveness row a reviewer calls bundled is never split: narrow it to one derivation, or re-key
  it onto one cell whose own value is the R9 anchor so subject and anchor coincide.
- Never reword a row the oracle just passed 3/3 to clear a house warning; settle the warning in
  `.gate-accepted` instead. Debt is for shapes that have never failed, not for a twin of a row
  that just cost a run (fix the twin even at 3/3).

## 5. The gated tier

Breadth comes from GATED clauses on value rows, tagged +LIVE, not from more strict rows:

- The minimal form is "the cell carrying it a formula rather than a keyed figure" (or "the cell
  carrying the FUNDED verdict holds a formula rather than a keyed word"). A clause that DESCRIBES
  the mechanism ("multiplying the item quantities by their classified costs", "comparing the
  billback to the half-print line") is unverifiable to a value-grepping judge and flaked at
  two tasks' later runs. Verify each gated anchor really is a formula.
- Only on NUMERIC cells (R109, 2026-09-11): a gated "formula rather than a keyed date" clause on a
  TEXT()-rendered date failed 1/3 with the judge quoting the formula and calling it keyed, and a
  "keyed word" clause on a nested-IF verdict failed 1/3 read by value (a round 4). Drop
  the clause or re-key a word column onto the column gestalt; never gate a text-valued cell.
- Only on figures that live in ONE cell (R29): a derivation clause on a total mirrored by a
  front-page read-through gives the judge a second home and it lands on the copy. Hunt
  single-cell anchors deliberately (a per-item carrying cell, a tab's own counter total).
- Only where the stored formula is a pure single call (R72); summary counts and conditional sums
  are COUNTIF/COUNTIFS/SUMIFS and dot products SUMPRODUCT(range,range) (R96), never a comparison
  multiplied inside SUMPRODUCT.
- Never as an each-vendor sweep when one row legitimately holds zeros (W11).
- R73: a prompt demanding live formulas needs the gated tier over 15% of positive; a human
  reviewer reads liveness BREADTH and ruled a rubric with only the two strict rows "largely
  hard-coded outputs could receive most points", so push LIVE toward half the positive weight.
- When the prompt promises a rerun on refreshed inputs, the ROW-LEVEL chain needs per-row formula
  criteria in the register shape ("the program side on each of the N rows is a formula over its
  row's movement, net and rate cells rather than a keyed figure") weighted 5+, or a selective
  hard-coder who keys the imported figures and every dependent row result while leaving formulas
  in the checked cells retains 39/39 (a round 3). An exhaustive-carry row is a COLUMN
  claim with ONE named cell and its cached value ("the zone column on the register's 792 rows is
  formulas rather than keyed zones, the first ticket T60411 standing at Z1 in cell G5"), which
  keeps the "N rows" text without a sweep. Typed source-data columns stay typed and are never
  asserted live. See [[rubric-coverage-and-completeness]] for R74 (a liveness row must cover the
  requirement's substance, not a container).

## 6. Golden-side design for liveness

- "Live formulas" means the DECISIONS, not the arithmetic (yankton reviewer): stock/no-stock,
  supplying branch, the order line set, freight, and the totals on top must move when a demand
  figure changes. Shape: a Decision Tests tab of flags (passes test, can ship, candidate, rank,
  cut, opens) that the deliverable reads, a cut ladder for any sequential greedy rule (one row per
  step, step count by MATCH(1,fits,0)-1), and the FULL row set on every detail tab with the
  quantity formula zeroing rows that drop out; a subset presentation tab is itself a hard-coded
  decision. A typed shortfall table under a live-formula prompt with the liveness rows pointing at
  already-live cells is one of the four defects that got one task rejected.
- Keep aggregation columns pure (R7/R16): one component per row, the combining cell plain
  arithmetic, on its OWN tab, so liveness has a legible anchor; widen a `=SUM(L5:O5)+P5` into one
  call rather than keep the extra term.
- A live chain makes the whole file verifiable: perturb an input and diff the downstream cells
  before shipping. Where a prompt or memo says a figure gets keyed in later and the rest must
  move, INJECT that input and recalculate with the `formulas` engine, diffing the action columns
  (one rubric keyed the recount hold off the SLOT column that never changes instead of the WORKED
  column, and 1,850 self-consistent caches hid a dead workflow). Prefer the column that CHANGES
  over the one that records history when two agree in the delivered state. A fixed-length action
  block is defensible when a control cell says "the order needs a line added".
- A live workbook corrects part of a reviewer finding by itself (one golden's trim reverted when
  the earlier order was cancelled); only prose and hard-coded blocks need hand work.
- A hard-coded quantity column beside computed siblings, or a group-average cost over a range
  that includes material outside the constraint, reads as unresponsive to a live-formula prompt.
- Cache mechanics (fix_floats, formulas recalc, calcChain, Excel re-save) are in
  [[package-hygiene-pipeline]].

## 7. Reading a reward vector

- reward = (B - u - f) / (B - u), B = positive + |negative|, u = weight verdicted
  `unverifiable_from_deliverable`, f = weight that failed. Avoiding a defect earns its weight, so
  a deficit does not divide evenly into the positive total and a non-integer is NOT evidence of an
  unsubmitted form. An `unverifiable` verdict costs nothing; `judge_failed` (a parser error) is
  fail-closed and costs the full weight even under the "judge-side, not your submission" banner,
  so solve for f every time and touch only those rows.
- A clean 1.0000 means zero deficit: the form matches the file and the golden satisfies all of
  it. A 0.0000 is a collapsed run, not a low score (one +2 failing out of 66 scores 0.9697); never
  rewrite a golden to chase it.
- The deficit is the only read-back of the entered form: when it does not land on a whole
  criterion weight against the file's own totals, the wording was re-entered and the WEIGHTS were
  not (a task run 6, 2/74 against a file at 66). The form can also carry figures the CSV never
  held (one variant total propagated); diff the failed rows' figures against the CSV
  before diagnosing the golden, and re-enter verbatim with tools/rubric-filler
  ([[revision-workflow]]).
- A FAILED verdict quoting the exact row the criterion wants means the row disagrees with the
  criterion (a magnitude with no side named, a paraphrase); stop looking for a landing fix.
- Shrink a row's EVIDENCE SURFACE to survive a parser failure: one named row instead of nine
  action rows of long text.

## 8. Judge-side artifacts to recognise instead of churning

- Evidence citing a SHEET THAT DOES NOT EXIST, or text the workbook does not contain at all, is
  cross-task judge contamination.
- An alignment-audit finding repeating verbatim with a criterion number the rubric lacks, or
  quoting figures from a superseded round, is a stale audit; the oracle report in the same batch
  quotes the current wording, which is how to tell. Verify against the delivered zip, then flag
  on the platform and act on nothing.
- A check naming another task's criteria: a verbatim C1 match plus an exact criterion-count match
  names the source folder in one grep. Re-fetch the stored submission and compare its criteria to
  the CSV before editing a correct artifact.
- A reviewer can describe another rubric under valid criterion numbers (six of eight items on
  one report), mix CSV line numbers with criterion numbers in one report, or name a finding that
  matches no criterion under either numbering. Print each named criterion beside the description
  and diff before acting; a reviewer's weight arithmetic is a second read-back of the entered
  form (134 read against a 132 file). The platform's own suggested rewrites are not pre-cleared
  against its other checks (a suggested figure re-adds a subsumption; a suggested typed-constant
  negative is the W6/W15 mirror that draws ambiguous polarity 3/3).
- A difficulty check dying on `DownloadVerifierDirError` and a harness that returns
  "[Prior result omitted from context]" for the two smallest files (eviction by read order on a
  fat golden) are resubmit-and-wait, not rubric work; keep goldens in the 23k-46k char band (A7
  warns over 100k, row-level detail belongs in the inputs).

## 8. Dated lines

- 2026-09-11 (Rubric Quality Review, [major] x2, coded R117/R118): two strict rows
  reading two first-page cells are one traceability requirement scored twice, so the pair sits on two
  SHEETS (R117 resolves the subject cells through R98's locator; 53 to 56 carry the same pair); two
  formula-only gated rows ("is a formula multiplying ...", "is a formula over ...") are one live-formula
  property scored twice, so a rubric gets one bare gated row and the rest ride on value rows (R118; 44 and
  48 carry it). The strict row's new home was the by-vendor table's own cell (a ROUND(SUMIFS) over the
  register), which R98 accepts as a cross-sheet aggregation.
- 2026-09-12 (a round 2, adjudication): a prompt saying "keep the math live in
  the cells ... I can't do that against pasted values" is R73's live-formula demand in a buyer's words; the
  trigger now reads "math live", "live in the cells", "pasted values" and "hard-coded values". Adjudication
  reads liveness breadth exactly as R73 does ("lines 4-14 grade the remaining ~46 SKUs ... as values"), so the
  gated tier goes over 15% before the first submission: a column-claim row per derived column (one named SKU,
  its value as stored, no sweep) plus the minimal clause on single-SKU value rows whose cell is a single-home
  ROUND, never on a figure with a typed twin on the sheet.
- 2026-09-12 (a round 3, adjudication, PR9): the minimal gated clause is not enough
  when an input clause DEFINES the computation; "a formula over the order total at the policy carrying rate"
  named two of policy 7.2's three factors and adjudication ruled that a flat 18% formula would earn the
  point where the clause halves the coverage period. Name every factor the clause states in the row
  ("applying the policy 7.2 annual carrying rate to the order total for one-half the coverage period,
  rather than a full year at that rate or a keyed figure"); leave a numeral out when no cell holds it
  as a value, and do not pin the result when a front-page read-through gives it a second home (R29).

- 2026-09-14: a strict +5 anchor must be a value whose EVERY carrier cell is a plain reference or a typed constant; R42 fires on any carrier reaching it by arithmetic (=E8+F8) and R72 on ROUND(a/b,3) shapes even when a pure-reference twin exists, and R9 does not read a leading minus as a figure. Before wording the strict pair, scan the workbook for values carried only by pure refs and typed cells (openpyxl formulas vs data_only, classify per value) and pick two on different sheets; a wired factor cell and a looked-up prior figure both qualify.
- 2026-09-14 (a round 2, golden check 1.0 / 1.0 / 0.98, coded R125): a gated count clause ("the 47 count ... is a formula counting the priced lines") landed on a lone =COUNT footer beneath a column of 47 VLOOKUPs, and one judge read the cached 47, typed again in the label beside it, as hard-coded. A count footer under a data column of another head is never a liveness anchor (C24 was the 3/3 case). Re-key onto the column the count summarises as a column claim naming the count mid-sentence ("reads the cost basis tab by formula on all 47 priced lines rather than keyed figures"): no money figure when the column's values have twins (R29), no leading Each (W16), and the "all N" keeps R13's block and the gated tier.
- 2026-09-14 (a round 2, adjudication, coded R129): "14 of 39 positive points (35.9%) for formula/cell-reference implementation and tab architecture (criteria 3, 7, 20-23) that the prompt never requires, exceeding the 25% implementation cap and failing a numerically correct static-value workbook". The 14 were exactly R24's strict-plus-gated set. Under R24 each strict row alone must cost over 10% plus a point, so TWO strict rows sit at 25.6% or more at any positive total; a prompt with no live-formula demand takes ONE +5 strict row at positive 33 or under plus one or two gated +1 rows (7 of 33, 21.2%, hand-keyed retention 84.8%). The +39 two-strict shape stays for R73 prompts. R129 errors above 10 of 39 (that shape has passed adjudication); golden-only tab names in liveness rows ("into the bulk projection tab") are described instead ("into the tab carrying the released Rev 2 pattern"), R112's reading.

- 2026-09-15: R73 and R129 each hold their OWN copy of the live-formula prompt trigger in rubric_form.py; widen both together. "Keep X on formulas" now reads up to six words for X ("Keep the classing and the bin assignments on formulas" was read as static and R129 fired on a formula-demanding prompt).
- 2026-09-15 (a round 5): R129 fired on a rubric built under the +39 two-strict shape for a prompt with no live-formula demand (15 of 39 on formula rows). Applied the non-live shape without re-funding: dropped the second strict row (Affected_Lots read-through) and a range row the exact-count row already fixed, stripped the formula clauses from two value rows, kept one +5 strict and two gated +1 (7 of 33, hand-keyed retention 84.8%).

- 2026-09-17 (a draft, gate update): once a prompt carries the live trigger, R74 wants a formula clause whose SUBJECT is a total and whose verb R74 reads ("is a formula", not "rather than a keyed figure"), and R29 then wants that total in ONE cell. The headline total fails R29 whenever a breakdown tab carries its own total row (Summary, Cartons Used and Packers all held $15,043.66); land the clause on a single-home pure-sum total instead (the N2-added charges, a ROUND(SUM) only the Summary holds), replacing a +1 method row the value rows already enforce. "each figure live" alone matched neither R73 nor R129; "live in the cells" matches both. MINIFS written as _xlfn.MINIFS survives the Excel resave and the formulas engine, so a smallest-fitting-carton decision column can be live without array entry.
- 2026-09-17 (rules pass): R85 rejects a named example hung off a column claim ("... rather than a keyed figure, the CH0050 clevis landing at $1.81"); the gated column claim carries its count instead ("The Kesler landed price on all 48 quoted lines is a formula ..."), and R74 reads a totals row only in the "The line total ... is a formula summing ..." subject form, not as a trailing participial. R114 treats two SUM footers on ONE row of one sheet (P60 and S60) as one total line, so the second strict anchor moved to another sheet's footer read through to the front page.
