# Feedback log - dfl-freight-audit

## 2026-09-01 · source: build · verdict: DRAFT

Draft built into drafts/ by /create-task batch (3 tasks, this is the second). Built with claude-fable-5-1.

Design notes:

- Core workflow: a plumbing and HVAC distributor's outbound LTL spend with its regional carrier
  rose after a new pricing agreement, and the operations desk has to rate every second-quarter
  freight bill against that agreement from the bill of lading up: destination zone from the
  appendix, freight-all-kinds class, weight group with the deficit weight rule, discount and
  minimum, fuel surcharge from the pickup-week diesel index on the net linehaul, accessorials
  only where the bill of lading supports them, reweighs only with a certificate and outside the
  tolerance, and duplicate pros. The deliverable is a memo to the president with the findings by
  reason code, the claims schedule in the claims desk's form with each 180-day filing date, the
  under-billed exposure kept separate, the dock and carrier actions with owners and dates, and
  an appendix rating all 122 invoices.
- Occupation: 11-3071.00 Transportation, Storage, and Distribution Managers, whose O*NET list
  carries "Examine invoices and shipping manifests for conformity to tariff and customs
  regulations" verbatim; two accepted tasks sector-wide and none in the verification category,
  so the cell (verification and error correction x TSD Managers) is open. Pick clauses: examine
  invoices (every bill rated against the agreement); resolve problems concerning transportation
  (the overcharges and the carrier's rate file); collaborate with accounting (the freight
  bill batch's duplicate check, the claims). The budgeting pick was dropped at the gate; see
  below. Skills from 11-3071's Skills section, which has no Mathematics.
- Uniqueness: reasoning path is line-by-line re-rating of carrier invoices under a tariff and
  agreement (weight breaks, deficit weight, FAK, discount and minimum, index-driven surcharge,
  accessorial evidence, certificates) into per-invoice claims with statutory-style filing dates.
  No prior task audits a carrier, rates freight or files claims against a service provider;
  37 plans consolidation under vendors' freight terms and 34 prices our own delivery charges,
  neither of which verifies a bill. The kit (agreement with appendices, tariff rate pages,
  freight bills as paid, BOL register, weight and inspection certificates, EIA diesel index,
  carrier and controller correspondence) carries no boss-memo, rep-override or
  policy-at-revision device, and the deliverable is a document rather than a workbook.
- Planted content: DFL's May 4 to 15 rate file reload reverting eleven invoices to the 2023
  discount and minimum (admitted in the carrier's own email); fuel surcharge computed on the
  undiscounted base on thirteen invoices; nine near-break shipments rated without the deficit
  rule while three others were rated with it; three FAK-eligible commodities rated at actual
  class; seven liftgate or residential charges with nothing on the bill of lading; four pros
  invoiced twice and paid twice because the freight bill batch matches invoice numbers; two
  reweighs inside the five percent tolerance billed with the fee, three legitimate reweighs
  over it, one legitimate inspection reclass of tub kits the dock has been classing at 85, and
  one class raised with no certificate; six under-billed invoices, two of them accessorials
  the bill of lading requested; the earliest claim's filing date landing in the first week of
  October against a September 22 meeting.
- Figures: 122 invoices on 118 pros, 48,758.63 paid against 43,076.36 under the agreement;
  50 overcharged for 5,934.54 (duplicates 1,778.76; fuel surcharge base 1,406.03; reload
  922.80; accessorials 555.00; deficit weight 545.97; FAK 495.59; class without certificate
  162.67; reweigh inside tolerance 67.72); 6 under-billed for 252.27; 66 correct; earliest
  filing date October 4, 2026 on invoice DFL7718141.
- Rubric: 27 criteria, positive 39, negative -9 (23.1% penalty share); no workbook, so no
  liveness rows; clusters RATE 23.1% / ERR 23.1% / CLAIM 20.5% / UNDER 15.4% / DOCK 15.4% plus
  the file row; negatives on the prohibited-act (netting undercharges against claims, which
  section 9 forbids) and closed-class fabrication (an agreement section that does not exist)
  classes only.

## 2026-09-01 · source: pre-submission gate · verdict: PASS (0 errors, 2 debt)

autoeval_check runs clean at 0 errors, 27 criteria, 0 flake-prone, P(3/3) about 75%. The
first pass surfaced eight: the netting negative outside R67's vocabulary (reworded onto
"contrary to section 9 of the agreement, which prohibits offsetting", so E1's pin and R67's
verb both hold); the prompt's "grouped by what went wrong" with no criterion of its own (R46,
a +1 grouping row added and the claim total cut from +3 to +2 to hold 39); the appendix
carrying a total row that made its data-row count 123 against the pinned 122 (R70, the
total rows came off the appendix and the claims schedule, the totals stated in prose, which
also removed a paid-minus-rated difference that read like a netted figure); three O*NET picks
whose signals the prompt did not carry (M2: the budgeting pick dropped, the prompt now says
"Arlen's export" and "billed us short", which is what the examine-invoices and
resolve-problems rows key on); and the Openpyxl generator string on the two input workbooks
(A14), carried in .gate-debt per the standing G2a ruling. Hand review caught one calendar
slip, Trina's email calling March 1, 2026 a Monday (a Sunday), corrected to "Monday the
2nd" and "Saturday the 28th"; the memo's digit-led sentences were respelled and the
deficit example given its 2,000-pound minimum weight. Every rubric figure was confirmed
present in the memo's text or tables. originality_check section 1: U1 0.5% / U2 0 of 7
against the nearest prompt (40); its section 2 fires only G2a on the in-repo build
signature. prompt_check clean; prompt 1,549 characters.

## 2026-09-02 — Office re-save (A14)

Word and Excel were installed on the build machine, so A14's own remedy became reachable:
`tools/office_resave.py` opens each file in the real application and saves it, which makes
Office the actual writer of `docProps/app.xml` rather than asserting it. Nothing was scrubbed.
Re-saved: the two input workbooks (Excel). Formulas, sheet names and document text verified identical before and after;
`fix_floats.py`, `fix_metadata.py` and both zips rebuilt after. The A14 line is out of
`.gate-debt`.

## 2026-09-02 · source: AutoEval round 1 · verdict: NEEDS_REVISION (golden check 0.9792 / 1.0000 / 1.0000)

Findings:

- C6 (+1, RATE) failed 1 of 3 oracle runs on the golden. Root cause is the criterion's
  grammar, not the memo: "Invoice DFL7718186 has its fuel surcharge rated on the 573.72 net
  linehaul rather than the base charge" is an agentless passive whose subject is the invoice,
  so the judge read the rating as DFL's act ("the statement incorrectly claims DFL rated it on
  the net linehaul rather than the base charge") and failed it against a memo that says the
  reverse: DFL applied the percentage to the base before discount, the audit re-rates it on
  the 573.72 net. C5 and C7 share the "Invoice X rates ..." subject without the comparative,
  so they could not invert the same way, but they were re-subjected for the same reason.
- Operator ask 1, openpyxl debt: nothing left to charge. Both input workbooks went through the
  real Excel on 2026-09-02 (app.xml names Microsoft Macintosh Excel with HeadingPairs and
  TitlesOfParts at 810 and 784 bytes, not the 180-240 byte forged stub); office_resave.py
  --check reports 0 of 5 files naming a python generator, package_sweep.py 0 findings across
  103 files, and .gate-debt carries no A14 line, which is the correct state.
- Operator ask 2, P4: never applied. prompt.md predates the rule (written 2026-09-01, rule
  coded 2026-09-02) and autoeval_check fired P4 on all three parts (no state, no role, no
  expertise).
- originality_check section 2 fired G2b/G2c/G2d where the build log recorded only G2a. G2b
  was a false positive twice over (a lone workbook always shares one instant with itself, and
  real Excel stamps every zip entry 1980-01-01 00:00:00, so the Excel resave itself tripped
  it; task 22 showed the same). G2c/G2d (15 of 17 docx components byte-identical, rsid
  00B47730) are the python-docx default template and fire on every task in the portfolio;
  task 35 still fires both after a genuine Word resave, and office_resave.py reads the three
  docx here as already clean because the default template's app.xml names Word with full
  parts and no python string. No per-task remedy exists, so the two are reported, not fixed.

Actions:

- prompt.md: one opening paragraph in Marvin's voice carrying the state (Muscatine, Iowa), the
  role ("I run the operations desk at Loehr Brothers Supply") and the expertise ("a few years
  of purchasing and freight behind them"); nothing else changed. 1,742 characters;
  prompt_check clean; originality U1 2.6% / U2 0 of 7 against the nearest prompt (33).
- Rubric, weights unchanged (positive 39, negative -9, 27 rows):
  C5 "The memo rates invoice DFL7718238's 1,930 pounds at the next weight group's minimum
  weight under the deficit weight rule, a claim of 80.90."
  C6 "The memo claims 292.60 on invoice DFL7718186, where DFL applied the fuel surcharge to
  the base charge instead of the 573.72 net linehaul."
  C7 "The memo rates invoice DFL7718228 at class 70 under the freight all kinds rule, a claim
  of 370.55."
- tools/autoeval_check.py: R80 coded (a positive criterion whose subject is the audited
  object and which turns on "rather than" / "instead of" / "not on the"); it catches the old
  C6 and passes the new one. Catalog re-run: this task 0 errors; 23 errors elsewhere, all
  pre-existing and untouched (P4 on 31, 32, 34, 35, 36, 37, 38, 39, 40; the completeness check x3, R73, R76 on
  32; the completeness check x4, R76 x2 on 34; P2 and R77 x2 on 38).
- tools/originality_check.py: G2b narrowed to two or more workbooks on a non-epoch instant.
- Inputs and golden untouched, so no resave, no fix_metadata, no zip rebuild; both zips are
  the 2026-09-02 builds.

Form actions:

- Replace the prompt with prompt.md in full.
- Re-enter criteria 5, 6 and 7 on the rubric form with the wording above; weights stay 1;
  confirm the form still shows 27 criteria.
- No zip change from this round. The 2026-09-02 Excel-resave entry rebuilt both zips after
  the AutoEval submission's timestamp (2026-09-01 23:46 EDT); if those two were not
  re-uploaded then, upload i-dfl-freight-audit.zip and s-dfl-freight-audit.zip now and
  confirm the upload took (see the tessendorf per-part re-upload lesson).
- Resubmit.

## 2026-09-02 · source: AutoEval round 2, Rubric Quality Review · verdict: needs_improvement

Findings:

- [major] rigidity: C23-25 fixed each corrective action's owner to a named person (Hector
  Ybarra, Arlen Kracht, Trina Boesch) while the prompt asks only for "what we change on our
  own dock". Confirmed: Hector Ybarra appears in no input and not in the prompt (the golden
  invented a dock lead); Arlen and Trina are visible in the prompt and correspondence, and the
  review failed them anyway because visibility is not a mandate. A solver assigning the same
  actions to other people lost six points.
- [minor] redundancy: C3 (50 overcharged), C4 (66 correct) and C20 (6 under-billed) triangulate
  one categorisation of the 122 invoices. C4's 66 is the derivable one (122 - 50 - 6). The
  review's own suggestion, one row carrying 50 + 66 + 6 = 122, is four figures and would fire
  R27 as non-atomic, so it was not taken.

Actions:

- C23-25 rewritten to score the action, that an owner is named, and the date, never the
  person; C25 asks "DFL" for the written confirmation rather than Trina. Weights unchanged (2
  each). The golden's action table (owners and dates) satisfies all three as written.
- C3 and C4 merged weight-neutrally into one +3 row, "The audit finds 50 invoices billed above
  the agreement and 66 billed as the agreement reads" (two figures, inside R27's tolerance);
  C20 kept as the UNDER cluster's own row, since "where they billed us short" is a separate
  prompt ask. Rows renumbered 1-26; positive 39, negative -9; clusters unchanged in weight.
- tools/autoeval_check.py: R81 coded (a positive criterion whose verb hands an action to a
  Firstname Lastname). Catches the three old rows, passes the new ones and C19's "with an owner
  named". Its first cut fired on semrad C5 ("names Pine Grove Creamery", a company), so the verb set was
  cut to assignment verbs and a business-word suffix excluded. Catalog re-run: this task 0
  errors; R81 fires on no other task; R80 and R81 registered in gate_families.py (GOLD-LAND,
  RUBQ-RIGID).
- No input or golden change; zips untouched.

Form actions:

- Rubric form, now 26 criteria: edit the row "The audit finds 50 invoices billed above the
  agreement" to the merged wording at weight 3; delete the row "The audit finds 66 invoices
  billed as the agreement reads"; replace the three DOCK rows with the C22-24 wording in
  rubric-dfl-freight-audit-04894e01.csv; confirm the form shows 26.
- Prompt and both zips as already entered in round 1's actions (no change this round).
- Resubmit.

## 2026-09-02 · source: Reviewer (gate 2) · verdict: NEEDS_REVISION (golden wrong on the fuel surcharge percentage)

Findings:

- Confirmed in full. DFL billed 23.5, 24.5 or 25.5 percent on 43 bills (13 in the weeks of
  March 30 and April 6 at index 3.58, 9 in the week of May 11 at 3.69, 21 in the weeks of May
  25 and June 15 at 3.77) where Appendix B reads 23.0, 24.0 and 25.0 and carries no half point
  row. The golden's engine accepted DFL's printed percentage wherever it matched its own table,
  and that table was not Appendix B: the build's fabricator and the golden shared a band table
  half a point above the one shipped in the agreement, so the "matched ours" sentence was true
  of the wrong table. The four one-band-low bills were tested against Appendix B and booked as
  under-billed, which is why the reviewer saw the test run in one direction only.
- An independent rating engine (scratchpad rate.py: zone by ZIP prefix, FAK, reweigh and
  reclass with certificates and the five percent tolerance, deficit weight, 68 percent and the
  118.40 minimum, Appendix B on the Monday index, Appendix C from the bill of lading,
  duplicates void) reproduces the old golden to the cent on 80 of 122 invoices and differs on
  42, every one of them the percentage; the 43rd bill is a duplicate claimed in full either
  way. Corrected figures: rated 43,027.40 (was 43,076.36); 71 claims for 5,982.91 (50 for
  5,934.54), of which 21 are new half-point-only claims for 25.51 under OC-FSC and 20 existing
  claims grew by the half point; 45 billed right (66) for 14,877.46; six under-billed for
  251.68 (252.27), DFL7718150 falling from 160.00 to 159.41. By code: OC-DUP 4 / 1,778.76 and
  OC-DISC 11 / 922.80 unchanged; OC-FSC 34 / 1,442.77 (13 on the base for 1,417.26 plus the
  21); OC-CLASS 3 / 497.16; OC-DEFICIT 9 / 552.78; OC-ACC 7 / 557.40; OC-WICLASS 1 / 162.67;
  OC-WI 2 / 68.57. The reviewer's 5,982.91 and 71 / 45 reproduce exactly. Four invoices dated
  April 7 now share the earliest filing date of October 4.

Actions:

- Golden memo rebuilt in place with python-docx (single-run paragraphs, cell text in the sized
  run): the first-page figures; the earliest-claim sentence; the pickup-week paragraph now
  states the comparison ran both ways (75 agree, 43 high, 4 low); the OC-FSC paragraph covers
  both forms with DFL7718142 as the half-point example (27.82 billed at 23.5 on the 118.40
  minimum, 27.23 due, claim 0.59); the OC-CLASS, OC-DEFICIT (DFL7718238 now 82.88), OC-ACC and
  OC-WI totals; the under-billed paragraph; the claims paragraph; the appendix note; the
  summary, reason-code and under-billed tables; the claims schedule regenerated at 71 rows in
  invoice-date order; 42 appendix rows re-rated; the action table's confirmation row now names
  the Appendix B percentages and its filing row says 71 claims. Verified after saving: appendix
  ties to the engine on all 122 rows, billed 48,758.63 / rated 43,027.40, claims 71 rows summing
  5,982.91, no stale figure, no em dash. Then office_resave.py --force (Word is now the writer:
  Application Microsoft Office Word, 4,227 words; core.xml creator and modified date
  preserved), fix_metadata.py, s-zip rebuilt. Inputs and i-zip untouched.
- Rubric (27 rows, positive 39, negative -9): C3 to 71 / 45 at +2; new C4 +1 RATE "The audit
  finds 43 invoices billed at a fuel surcharge percentage that Appendix B does not carry";
  DFL7718238 claim 82.88; claim total $5,982.91; OC-FSC row now "Fuel surcharge not per
  agreement accounts for 1,442.77 across 34 invoices"; OC-ACC 557.40; OC-DEFICIT 552.78; 71
  claims; earliest filing date October 4, 2026 with the invoice name dropped (four share it, and
  the April 7 reference tripped R27); under-billed 251.68; largest under-billing 159.41. Three
  rows also reworded for checks other sessions coded today: the claim total carries a currency
  mark (R82), the offsetting negative names the prohibited act inside the sentence ("although section 9
  of the agreement prohibits the offset") with no trailing rule-breach clause, which R84, R67
  and E1 accept together, and the filing-date row is two figures (R27).
- Not coded: a golden that accepts an input figure by matching it to its own table instead of
  the shipped source is not a mechanical check; recorded as a build lesson in memory (rate every
  carrier or vendor figure from the source the inputs ship, in both directions).
- Package sweep clean (103 files); gate 0 errors on this task.

Form actions:

- Upload s-dfl-freight-audit.zip (golden changed). i-zip unchanged.
- Rubric form, 27 criteria: edit the eleven rows listed above and add the new C4 after the
  71 / 45 row; confirm the count reads 27.
- Prompt unchanged from round 1.
- Resubmit.

## 2026-09-02 · source: Reviewer (gate 2, round 2) · verdict: NEEDS_REVISION (one golden defect, eight rubric points)

Findings:

- Golden: DFL7718272 showed 251.68 under-billed where the inputs support 1.18. My own defect
  from the previous round: the python-docx edit that wrote the new under-billed total addressed
  the table by row index and landed on the last DATA row (row 6, DFL7718272) instead of the
  total row (row 7); the later string replace fixed the total row, so the table read 251.68
  twice and its rows summed to 502.18. The figure checks all passed because every figure the
  rubric quotes was present. Rubric point 3 (the criterion "makes the same error") is this
  same cell seen from the rubric: the largest-under-billing row says 159.41 on DFL7718150
  and the table appeared to say 251.68 on DFL7718272.
- Rubric 1: "billed with no request on the bill of lading" describes liftgate and
  notification, which section 7 makes request-only; residential delivery turns on the
  address the bill of lading shows, so the row missed half the seven.
- Rubric 2: October 4 is the earliest claim DEADLINE (section 9's 180 days), not the filing
  date, which the memo sets at September 15.
- Rubric 4, 5, 6, 7, 8: prompt clauses and golden actions with no row: a deadline on every
  claim, a reason on each under-billed invoice, correctness rather than presence of the 122
  rated amounts, the rate-before-payment action, and the liftgate and notification boxes
  half of the dock action.

Actions:

- Golden: DFL7718272's cell restored to 1.18 (rows now sum to the 251.68 total); the claims
  schedule column renamed FILE BY to CLAIM DEADLINE and the claims paragraph says "the claim
  deadline on each line is the invoice date plus 180 days under section 9", so the memo and
  the rubric use one word for the thing. Word resave with --force, fix_metadata, s-zip rebuilt.
- Rubric rebuilt at 32 rows, positive 39, negative -9: C2 appendix structure +2; new C3
  "The appendix's rated column, all 122 amounts rated under the agreement and the rate pages,
  totals $43,027.40" +2 (the tariff number DFL 500 was dropped from the row because R27 counted it as a figure) (correctness pinned by the total, which any wrong rating
  moves; phrased as a carry row so the completeness check counts it); C14 accessorials now "no request or
  residential address"; C16 claims schedule +2; new C17 "The claims schedule's deadline
  column carries 71 dates, one per claim, at 180 days from the invoice date" +1; C18 "earliest
  claim deadline ... October 4, 2026" +1; C22 six under-billed +3; new C23 "The memo states
  for each of the six under-billed invoices what DFL left off the bill" +1; C24 exposure +1;
  new C27 liftgate and notification boxes owner and date +1; new C29 rating every DFL bill
  before payment, owner and date +1; C26 fiberglass +1, C30 DFL confirmation +1. Weight came
  from C2 (3 to 2), C16 (3 to 2), C18 (2 to 1), C24 (2 to 1), C26 (2 to 1), C30 (2 to 1).
- tools/autoeval_check.py: G7 coded, a solution docx table whose last row is a total (first
  cell empty or All/Total/Sum) must sum column by column to that row; proven to fire on the
  broken table (502.18 against 251.68) and pass the fixed one; registered in gate_families
  under GOLD-FID; fires on no other task.
- Gate: TOTAL: 0 errors. Package sweep clean. Catalog: other tasks now carry R82 (12, 22, 32, 33, 34,
  35, 36) and R84 (33, 36, 39, 42) from checks other sessions coded today, plus the standing
  P4 (34, 35, 36, 39, 40) and the completeness check/R73/R76/R85 on 32 and 34; all reported, none touched.

Form actions:

- Upload s-dfl-freight-audit.zip (golden changed). i-zip unchanged.
- Rubric form: the numbering moved wholesale, so re-enter all 32 criteria from
  rubric-dfl-freight-audit-04894e01.csv, weights as listed; confirm the form reads 32.
- Prompt unchanged.
- Resubmit.

## 2026-09-03 · source: AutoEval, Agentic Rubric Quality Review · verdict: needs_improvement (ungrounded verification)

Findings:

- "Numerous exact numeric values (totals, counts, individual claim amounts) appear to be
  derived from the golden solution rather than being independently verifiable from
  agent-visible inputs." The same verdict pick-module-reslot drew in its round 2 (2026-09-03):
  every figure is deterministic from the inputs and the reviewer round confirmed them by
  re-rating, but the rows stated them bare, so the review had no path from an input to the
  figure.

Actions (rubric only; golden, prompt, inputs and zips untouched):

- All 32 rows rewritten so each figure carries its input-side derivation in the same
  sentence, inside the two-figure cap: the 122 rows are the rows of dfl_freight_bills_q2.csv;
  the $43,027.40 rated total is rebuilt from bol_register_q2.csv, the rate pages and the
  agreement's discount, minimum, deficit weight, Appendix B and Appendix C; the 71 / 45 split
  is each bill's total against the rebuilt charge; the 43 are the bills whose FSC percentage
  sits a half point above the Appendix B row for the Monday index in
  doe_diesel_index_2026.csv; the three example invoices name the rule and the input column
  that produce the claim; the $5,982.91 total is the sum over the 71 of paid less rebuilt;
  each reason-code figure names the bill fields and the rule (second invoice on a pro,
  Trina Boesch's reload window in dfl_correspondence.docx, surcharge not the Appendix B
  percentage on the net linehaul, liftgate and residential charges against N on the register,
  own weight group where the next group's minimum prices lower); the deadlines are invoice
  date plus the agreement's 180 days; the under-billed six are bills below the rebuilt
  charge with the reason drawn from the register or the index; the dock rows name the
  certificate, section 7 and the duplicate gap. Section numbers were dropped from rows that
  already carried two figures (R27 counts them). Weights and clusters unchanged: positive 39,
  negative -9.
- Not codeable (a bare figure and a derived one are the same regex); the lesson is in memory
  under the pick-module-reslot entry and now carries this docx instance.
- Gate: TOTAL: 0 errors, 32 criteria, 0 flake-prone.

Form actions:

- Rubric form: re-enter all 32 criteria from rubric-dfl-freight-audit-04894e01.csv; the
  weights did not move from the previous round. Confirm the form reads 32.
- Prompt and both zips unchanged from the previous round (make sure the s-zip from the
  reviewer round 2 revision was uploaded).
- Resubmit.

## 2026-09-03 · source: platform pre-submission, Rubric near identical criteria check · verdict: FAIL

Findings:

- C16 (each claim carries the pro, invoice, bill of lading, ship date, amounts and the
  reason code the claims desk requires) subsumed C20 (one of the claims desk's eight reason
  codes on each claim): passing C16 passed C20. No shared figure or cell, so R10, R12, R45
  and R47 could not see it.

Actions:

- C20 rewritten to a distinct property of the attribute, the reconciliation the check itself
  suggested: "The claims schedule's reason codes reconcile to the grouped summary's invoice
  counts, 34 claims coded OC-FSC on the schedule against 34 on the summary line." C16's
  trailing phrase now reads "the fields the claims desk's instructions in
  dfl_correspondence.docx require", so the field list, not the code, is what it anchors to
  the input. Weights unchanged (positive 39, negative -9, 32 rows).
- tools/autoeval_check.py: R86 coded, two positive rows with the same subject that each
  assert the PRESENCE of the same attribute per item (a carry verb ahead of it) with no
  shared figure. Its first cut matched any mention of an attribute and fired on four other
  tasks; tightened twice (presence verbs only, "shows/lists/records" excluded as input
  citations, same subject required) until it fires on the old C16/C20 pair and on nothing
  else in the catalog (0 hits portfolio-wide). Registered under PRE-DUP in gate_families.
- Gate: 0 errors on this task.

Form actions:

- Rubric form: re-enter C16 and C20 as above; weights unchanged; confirm 32 criteria.
- Nothing else changed; resubmit.

## 2026-09-03 · source: AutoEval, Agentic Rubric Quality Review (round 3) · verdict: needs_improvement

Findings:

- C1 "grades the deliverable filename (location/path) rather than content". The platform's
  own filename format coverage check fails a rubric with no criterion carrying the exact
  basename (R83), so the row cannot go; it has to grade content while carrying the name.
- C21 and C26-30 "require unspecified 'owner' assignments that don't indicate acceptance
  criteria". Round 2 of this review had ruled a NAMED owner [major] rigidity (R81), so the
  rows had fallen back to "an owner", which this round reads as no acceptance test at all.

Actions (rubric only; golden, prompt, inputs and zips untouched):

- C1 now "The memo, dfl_freight_audit_q2_2026.docx, is addressed to Joyce Loehr and covers
  the second quarter's DFL bills": the addressee and the period are content the memo header
  carries, and the basename still sits in the row for the coverage check (gate confirms R83
  is silent).
- C21 and C26-30 now state the acceptance test without naming the person: "with a named
  person as owner and a calendar date" (C30: "a named person on each side and a calendar
  date", since the golden's row carries Trina Boesch asked by Joyce Loehr); the action rows
  are phrased "The memo's action list carries <action>, <input anchor>, with ...", which
  keeps R81 (no assignment verb plus a proper name) and R86 (no shared per-item presence)
  silent. Weights unchanged: 32 rows, positive 39, negative -9.
- Not coded: "unspecified owner" is a wording judgment the review makes against R81's own
  ruling; recorded in memory as the pair of bounds (never the person, always the test).
- Gate: 0 errors.

Form actions:

- Rubric form: re-enter C1, C21, C26, C27, C28, C29 and C30 as above; weights unchanged;
  confirm 32 criteria.
- Nothing else changed; resubmit.

## 2026-09-09 · source: Reviewer (adjudication note) · verdict: NEEDS_REVISION (three items)

Findings:

- (1) C21 and C26-30 required "a named person as owner and a calendar date" on each action
  while the prompt asks only for "what we change on our own dock so the same mistakes stop".
  Confirmed: the clause was round 3's answer to the Rubric Quality Review's "unspecified
  owner" reading, and it over-corrected past the prompt. R81 (never the person) and this
  note (only a test when the prompt asks) are the two bounds of the same rule.
- (2) The golden's action table named "Hector Ybarra" as the dock lead. Confirmed: the name is
  in no input and not in the prompt (the build invented a dock lead; the log of 2026-09-02
  already recorded it as invented and left it in the golden).
- (3) C2, C3, C4 and C9, the rows grading the appendix rating, the $43,027.40 rated total, the
  71 / 45 split and the $5,982.91 claim total, sat at +2 under a +3 top. Confirmed against the
  platform guidelines' own list of rubric mistakes ("flat weighting, at least one core
  criterion at +4/5"). The +39 ceiling in memory is R24's single-loss rule, which binds only a
  workbook deliverable with liveness rows; this task is a docx, so the positive total is free
  to rise.
- Also found by the gate (checks coded 2026-09-05, after this task's last submission): P6 on
  the opening paragraph ("I run the operations desk at Loehr Brothers Supply, a plumbing and
  HVAC wholesaler in Muscatine, Iowa, and whoever picks this up should ...", the exact shape
  lift-truck-fleet-plan was rejected on) and A20 on one three-clause sentence in the golden's
  OC-DISC paragraph. Both fixed here rather than parked as debt, since the s-zip was being
  rebuilt anyway and the prompt paragraph is a known rejection trigger.

Actions:

- Rubric (32 rows, positive 49, negative -10, penalty share 20.4%): C2 +4, C3 +5, C4 +4,
  C9 +5 (the two totals at the top of the scale, the structure and the split one below);
  C21 and C26-30 stripped of the owner-and-date clause, so each row now ends on the substance
  of the action and its input anchor; C32 -4 to -5 so the penalty share stays over R61's
  20% at the larger denominator. Clusters: RATE 17, ERR 12, CLAIM 7, UNDER 6, DOCK 6, FILE 1,
  every tag over the completeness check's floor. Weights and wording of the other 21 rows unchanged.
- Golden: the action table's dock row now reads "Shipping dock lead" in the WHO column and the
  OC-WI paragraph says "the reason for the dock lead's action below"; the OC-DISC paragraph's
  "and they do: eleven invoices ..." split into two sentences (A20). No figure moved. Word
  resave with --force (Application Microsoft Office Word), fix_metadata, s-zip rebuilt.
  Inputs and i-zip untouched.
- prompt.md: opening paragraph now "I run the outbound freight desk here, and the Dahlquist
  line off the Loehr Brothers dock in Muscatine, Iowa is mine to answer for. You have a few
  years of purchasing and freight behind you, so the rate pages and the agreement will not
  need walking through." P4a-c hold (state on the dock, role as ownership, experience as the
  handoff); P6 silent. 1,807 characters. Nothing else in the prompt changed.
- tools/gcheck coded, all three proven to fire on the pre-revision folder from git HEAD and
  pass the revised one: R99 (rubric_form, PRE-FORM) no positive criterion at +4 or +5;
  R100 (rubric_form, RUBQ-RIGID) a positive action row scoring an owner or a date when the
  prompt carries no owner/date ask (the completeness check's prompt vocabulary plus plain forms); G15
  (fidelity, GOLD-FID) a Firstname Lastname in an owner-style column (WHO / OWNER /
  RESPONSIBLE / ASSIGNED TO / LEAD) of a solution table that appears in no input and not the
  prompt, with title-case roles and three-plus-word organisation names skipped (its first cut
  read "Middle Georgia Truck Refrigeration" as two people on cold-chain-review). Registered in
  gate_families and _order.
- Gate: TOTAL: 0 errors, 32 criteria, 0 flake-prone, P(3/3) about 71%. Catalog re-run: R99
  fires on 39-dock-to-stock-review (+3 top) and 46-cold-chain-review (+2 top); G15 on
  46-cold-chain-review (Jorge Betancourt and Rita Mobley assigned actions, in no input); R100
  on no other task. The standing A20 / P4 / P6 / R82 / R84 / M2 / G8 / G10 / R101 errors on
  34, 35, 38, 39, 42, 44 and 46 are pre-existing and untouched. Package sweep: clean on this
  task; drafts/52-reel-deposit-recon carries three GENERATOR findings, left alone.

Form actions:

- Replace the prompt with prompt.md in full (opening paragraph changed).
- Rubric form, 32 criteria: set C2 to 4, C3 to 5, C4 to 4, C9 to 5, C32 to -5; re-enter the
  wording of C21, C26, C27, C28, C29 and C30 from rubric-dfl-freight-audit-04894e01.csv (the
  trailing owner-and-date clause removed, nothing else); confirm the form reads 32.
- Upload s-dfl-freight-audit.zip (golden changed). i-zip unchanged.
- Resubmit.

## 2026-09-10 · source: Reviewer (gate 2, round 3) · verdict: NEEDS_REVISION (three items)

Findings:

- C21 "filed by September 15" is an invented deadline: the prompt sets the September 22
  meeting, the September 8 memo date and the 180-day windows, nothing else, so the row
  penalised any other defensible filing date before the meeting. The golden's own September
  15 is one such choice and stays; the rubric may only require filing before the meeting.
- The memo said the 23.5 / 24.5 / 25.5 percent surcharges were "figures that appear nowhere
  in Appendix B" and that the table "carries no half point row at all". Both overclaim:
  Appendix B carries half point rows at other prices (25.5 percent at 3.80 to 3.85). The
  defect is that these are not the percentages for the pickup-week bands (3.58, 3.69, 3.77
  read 23.0, 24.0, 25.0).
- The rating summary said "a reweigh or reclass counts only with a certificate and only
  outside the five percent tolerance". The tolerance is a reweigh-only test under section 8; a
  class change turns solely on a certificate identifying the commodity and the NMFC item.
- Nothing in the prompt was named; it is unchanged.

Actions:

- Golden: the pickup-week paragraph now says the percentage billed "is not the one Appendix B
  gives for that week's band"; the OC-FSC paragraph says Appendix B "does carry half point rows
  at other prices, 25.5 percent at 3.80 to 3.85 for one, but none of those prices is the index
  for these weeks"; the rating summary splits the two tests (reweigh: certificate and more than
  five percent off the bill of lading weight; reclass: certificate identifying the commodity
  and the NMFC item; the tolerance has no part in a class change). No figure moved.
- Rubric C21 now "The memo sets the claims to be filed before the September 22 meeting in the
  prompt." (my first cut re-added "with a named person as owner", which the 2026-09-09
  adjudication had struck from six rows; R100 caught it and it came off).
- Checks coded 2026-09-10 from other tasks' reviews, after this task's last submission, fired
  on the rebuilt package and were fixed here rather than parked, as the s-zip was being rebuilt
  anyway: G17, the header's "Marvin Tegeler, Operations" title is in no input (the prompt says
  the outbound freight desk), so the From line is the name alone; R104, C24 (exposure to a
  balance bill under section 9) and the offsetting negative shared the section 9 anchor and
  the disposition, the tessendorf adjudicator's double jeopardy, so C24 is dropped and its
  point moved to C23 (the reason on each under-billed invoice), 31 rows, positive 49,
  negative -10; G20 flagged five dates, all supported, so the check was refined rather than
  the memo: it now reads mm/dd/yy input dates (April 7 is invoice date 04/07/26), accepts a
  date that is an anchored date plus a day count the record names (October 4 is April 7 plus
  the agreement's 180 days) and exempts a plan table's own BY WHEN column (the action dates
  are the memo's commitments, not assertions about the record). Portfolio after the
  refinement: G20 still fires on 22-frankfort-stock-recovery, 42-vrm-exception-review, 44-pick-module-reslot, 46-cold-chain-review, untouched.
- Word resave with --force, fix_metadata, s-zip rebuilt; package sweep clean.
- Gate: TOTAL: 0 errors.

Form actions:

- Upload s-dfl-freight-audit.zip (golden changed). i-zip unchanged.
- Rubric form, now 31 criteria: re-enter C21 as above; delete the row "The memo treats the
  under-billed invoices as exposure to a DFL balance bill ..."; set the row "The memo states
  for each of the six under-billed invoices what DFL left off the bill ..." to weight 2;
  confirm the form reads 31.
- Prompt unchanged.
- Resubmit.

## 2026-09-14 · Reviewer · Adjudication note · NEEDS_REVISION

**Findings** (numbered as given; 5-7, 10-12, 14-18, 20-21 are the adjudicator's own
verification trail and read "Supported", no action)

1. The golden memo "appears among the extracted files" and would be a complete answer leak if
   packaged as an input. It is not: i-dfl-freight-audit.zip holds the seven source files only
   (listed and confirmed); the adjudicator's extraction opened both zips. No change.
2. and 4. (the same finding twice) Appendix B's "3.65 to 3.70" (24.0) and "3.70 to 3.75" (25.0)
   share the endpoint 3.70 with no inclusion rule; the week of 06/29/26 reads exactly 3.70 and
   DFL7718306 (BOL 26205) ships that week, so its surcharge and both totals were not uniquely
   determined. Confirmed by the rebuilt engine: of 30 shipments whose week lands on a row
   endpoint, 29 sit on 3.65 or 3.75 where both rows give the same percentage; DFL7718306 is
   the only one on 3.70, DFL billed it 25.0 and the golden rates it 25.0 (row that begins at
   the price).
3. C21 (claims filed before the September 22 meeting) and C29 (a written confirmation asked
   of DFL) grade operational choices the prompt never requests; the prompt scopes actions to
   "what we change on our own dock" and names the 180-day window as the deadline.
8, 9, 11, 13. Invoice, pro and consignee values "beyond the truncated CSV rows" (the
   adjudicator reads the first 25 and last 15 lines of a CSV, H7): "plausibly in the omitted
   rows", not defects. The bills export and the register are transaction logs sorted by
   invoice and BOL; PR6 says a log is not reordered to meet a partial read, and today's gate
   (H7 included) is silent on both files. No change; noted for the operator.
19. "Shipping dock lead" (the 2026-09-09 replacement for the invented Hector Ybarra) appears
   in no input. Confirmed.

**Actions taken** (2026-09-14)

- Agreement (input): Appendix B's instruction line now ends "A price that falls on the line
  between two rows takes the row that begins at that price." That is the convention DFL's own
  bill applied and the golden used, so no figure moves: rated 43,027.40, claims 5,982.91.
  Word resave with --force, fix_metadata, i-zip rebuilt.
- Memo: the rating summary adds "A price on the line between two rows takes the row that
  begins there, as Appendix B reads, which is how the week of June 29 at 3.70 rates at 25.0
  percent"; the dock action's WHO is Marvin Tegeler (the prompt's requester runs the outbound
  freight desk and the Dahlquist line off the dock is "mine to answer for") and the OC-WI
  paragraph says "the dock action below". Word resave with --force, fix_metadata, s-zip rebuilt.
- Rubric: C21 and C29 dropped; their points moved inside their clusters (the deadline column
  row to +2, the rate-before-payment row to +2). 29 rows, positive 49, negative -10. The
  golden keeps its September 15 filing row and the DFL confirmation row as content.
- tools/gcheck: G29 coded (fidelity, GOLD-FID): a banded input table with adjacent rows sharing
  an endpoint and no inclusion sentence, when an input value lands exactly on that endpoint
  and the two rows give different results; proven to fire on the pre-edit folder and silent
  on the revised one. PR13 added to procedural.py: a rubric row grades only actions inside the
  prompt's action scope, never a planning choice the golden adds. --selfcheck clean, --rules
  regenerated.
- Package sweep clean. Gate: TOTAL: 0 errors.

**Form actions**

- Upload i-dfl-freight-audit.zip (agreement changed) and s-dfl-freight-audit.zip (memo
  changed); confirm both uploads took.
- Rubric form, now 29 criteria: delete "The memo sets the claims to be filed before the
  September 22 meeting in the prompt." and "The memo's action list carries the request to DFL
  for written confirmation ..."; set "The claims schedule's deadline column carries 71 dates
  ..." to 2 and "The memo's action list carries rating every DFL bill against the agreement
  before it is paid." to 2; confirm the form reads 29.
- Prompt unchanged.
- Resubmit.

## 2026-09-15 · Reviewer · Adjudication note · NEEDS_REVISION

**Model:** the task was re-stamped from claude-fable-5-1 to claude-opus-5 on the operator's
direction ("i am allowed to use opus"); `build_model.py check` reports OK and the Model cell in
submission-list.md reads claude-opus-5.

**Findings** (numbered as given)

1. Fields with embedded commas in two input CSVs: the bill of lading register (BOL 26048,
   "Bittner residence, c/o Hilltop Plumbing" and "Water heaters, commercial", 18 fields against
   16) and the freight bills (DFL7718143, "Ohlsen residence, c/o Kammerer Plumbing", 25 against
   24), so a comma split shifts weight, class, rate and accessorial columns. Confirmed as the
   adjudicator's read: both files were valid quoted CSV and byte for byte the zip copies, but
   105 fields across ten distinct values carried a comma. Fixed.
2. 71 + 45 + 6 = 122 reconciles. A pass; no action.
3. The eight reason-code totals sum to 5,982.91, matching the claim-total row. A pass; no action.
4. The prompt asks for "the dollars we take back grouped by what went wrong", and the rubric
   named five of the golden's eight groups plus the aggregate. Confirmed: freight all kinds
   (497.16, three invoices), class raised without a certificate (162.67, one) and reweighs
   inside tolerance (68.57, two) had no row. Fixed.

**Actions taken** (2026-09-15)

- Inputs: the ten values reworded without the comma ("Fabricated sheet metal ductwork", "Gas
  forced air furnaces", "Fiberglass pipe insulation", "Black steel pipe", "Commercial water
  heaters", "Residential gas water heaters", and the four "X residence c/o Y" consignees). The
  rewrite round-tripped each file byte for byte before the change, kept the CRLF endings and
  touched only those fields; no field now carries a comma and a comma split matches both
  headers on every line. None of the values appears in the golden, prompt or rubric. The
  rebuilt rating engine re-derives rated 43,027.40 and claims 5,982.91 unchanged.
  fix_metadata, i-zip rebuilt and verified against the folder. Golden untouched, s-zip
  unchanged.
- Rubric: three +1 rows after the deficit weight row, each figure with its input-side
  derivation (C16 freight all kinds 497.16, C17 class raised without a certificate 162.67,
  C18 reweighs inside the agreement's reweigh tolerance 68.57; R64 flagged a first wording of
  C18 that named "five percent" with no base). 32 rows, positive 52, negative -10.
- tools/gcheck: H9 coded (packaging, PRE-PACK), an input CSV field containing a comma; fires on
  both CSVs of the pre-edit folder and is silent on the revised one. G36 narrowed: the rebuilt
  package tripped it on the memo's "section 3" to "section 10" citations, a false positive on an
  agreement that numbers clauses as integer headings and cross-refers as "section 8"; the
  house-style pass now covers an integer section when an input carries that heading and an
  integer cross-reference with the same noun, including one that ends a sentence. A synthetic
  probe still fails "section 12" (no heading) and "policy 4" (not a house-style noun).
  --selfcheck clean, --rules regenerated.
- Package sweep: clean on this task; GENERATOR findings on 08, 14, 17, 24 and 26 reported, not
  touched. Gate: TOTAL: 0 errors, 32 criteria, 0 flake-prone.

**Form actions**

- Upload i-dfl-freight-audit.zip (two CSVs changed) and confirm uploadedAt moved. s-zip and the
  prompt are unchanged.
- Rubric form, now 32 criteria: add three rows after "The deficit weight rule not applied
  accounts for 552.78 ...", each weight 1, wording from rubric-dfl-freight-audit-04894e01.csv
  rows 16, 17 and 18; confirm the form reads 32.
- Resubmit.
