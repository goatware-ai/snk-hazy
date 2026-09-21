---
name: rubric-anchoring-and-landing
description: "How a positive criterion lands on the cell the judge greps: unique tokens and stored forms (R50/R56/R94/R51/R27/R43/R65), read-head and companion cells, counts (R26/R66/R70), stages and directions (R60/R62/R28/R31/R64/R80), objectivity and grader-instruction wording (R19/R25/R18/W12), named members and scoped claims (R34/R33), Rubric Quality Review derivation-in-sentence, discoverability and the deliverable-first fix (R108 citation names, to 2026-09-11)"
metadata:
  type: feedback
---

Open before writing or repairing any positive criterion that pins a figure, a date, a name or a
fact. Siblings: [[rubric-liveness-criteria]] (formula rows and the reward model),
[[rubric-negatives]], [[rubric-coverage-and-completeness]] (what has to be scored),
[[rubric-criterion-count]] (shape and weight), [[golden-fidelity]] (the golden against its
sources).

## 1. The judge greps values: cite what literally sits in a cell

- A citation claim lands only on the file name (R108, 2026-09-11): "each cited where its figures are
  used" beside Diesel_Retail_Price_History.xlsx failed 3/3 on a memo that said "the price history";
  the judge greps the file name at the sentence that uses the figure. Before scoring a row, search
  the golden for every name it promises; a score-table claim is not a search.
- Cite the unique token column A carries (item code, account number, invoice number, order and
  line). Plain-English names ("the 3/4 vacuum breaker") miss trade shorthand (VAC BREAKER 3/4); a
  spot value alone is not an anchor unless it is unique in the workbook (yankton C17 landed on
  another item with the same requirement). A criterion naming a line states exactly ONE number
  (R27 counts an item code's own digits as a figure; hyphenated tag suffixes are exempt).
- Quote money and quantities as STORED, never as formatted (R50): 10.8 not 10.80, 67.3 not
  67.30; a padded form exists only in the number format and the miss is deterministic. The
  stored form is necessary and not sufficient: pair it with a SECOND anchor, a sheet name or a
  row key, or the judge lands on the prose that spells the padded form (R94, run 8).
  A percentage stated as "85.3 percent" where the cell holds 0.853 (R48) and a spelled "September
  4" against a stored 09/04 (R56) are the same miss; a date pinned to a row key needs both on one
  sheet in the stored form. Currency notation: a money figure carries the $ mark and the cents
  (R82, reviewer fix on a task).
- The figure must be UNIQUE on its row (R51, quantities as well as money): a credit mirrored into
  OVERBILLED on the same row flaked three submissions under three wordings; no rewording removes a
  twin, re-key onto a figure that stands once or delete the twin cell. A total twinned across two
  blocks of one tab (897 summed by month and by group) is R59: delete one total.
- Lead a criterion with its most unique figure, and every sheet that carries the pinned figure
  must carry the rest of the chain (R43); R35 names the sheet. A cause attribution on a named line
  needs a word of the cause on the row itself (R58: "DWV never keyed" against a row reading pg2
  stalled 1/3); re-anchor on the row's own figures and leave the class to the cause-table rows.
- State the NEW value alone beside the row key (R65): "moves to 17.95 from 12.95" flaked when the
  row key stood on more than one sheet and the judge read the Items row that carries neither.
- Use the CELL'S words, not a paraphrase ("referred to the Ottawa branch" failed 1/3 against
  "branch call, Ottawa"); uncoded because no regex separates a damaging paraphrase from
  legitimate restatement. Reword onto the workbook's own nouns and the figure the judge quoted in
  its evidence, which the feedback hands you for free.
- Ordering rows name ONE object that comes first and pin its place ("whose first paragraph
  states ..."); "leads with the decomposition and the recovery figure" flaked 1/3 (R105).

## 2. Read-head and companion cells: fix the deliverable first

- A graded fact past the first sentence of a long prose cell fails on read-head (yankton run 4:
  752-char cell, date 600 chars in; commission-review C7: ten bonuses at the tails of six
  900-char paragraphs, 0/3, R103). Keep prose cells ~200-500 chars and give every figure the
  rubric grades a companion cell in a labelled table, one value per cell; a per-item enumeration
  needs a row per item on the tab the criterion names, verdicts as formulas off the computing tab.
- Discoverability is a first-class variable: give a graded table its own tab named for what the
  criterion asks ('Short at Opening', not a block under 'Purchase Orders'), and state a graded
  census in BOTH the briefing prose and a cell block so either search path lands (yankton run 1).
- Before rewording a flaky criterion, look for the cell it needed: put the count, the period end
  date and the total where the judge lands and let the wording stand (one rubric, run 1). Statement
  decomposition splits on paragraphs: three actions across two paragraphs failed, a named action
  table (action / owner / by when) fixed it.
- A count needs a cell that reports it (COUNTA under a plain label turns a 41-row tally into one
  grep) and the exact count LEADING ("carries all 41 items", not "carries every item ... reporting
  41", which W11 reads as a sweep). A count clause inside a positive is a second thing to verify;
  drop it unless the count is the point. Never make the judge re-sum detail lines: quote the label
  beside the total. A pinned N that the rows are spread over seven schedules needs ONE
  consolidated table whose data-row count IS the number (R70).
- Stale counts fail 3/3 and drift in packs after a data retune (R26): when one is stale, recount
  them all from the delivered inputs. A judge fails a count it can read differently on the landing
  row ("2,318 units across 41 accounts" beside "40 accounts and the counter", R66): put the
  criterion's own count on the row that holds the pinned figure, live, and align the prose beside
  it. A bare count the workbook repeats (three eighteens) needs a deliverable sentence saying what
  the count is, and the criterion cites that sentence.
- A universal deadline pin ("each fix before September 22") fails on ONE later-dated row (R71):
  date the item's pre-deadline step inside the bound.
- Two criteria naming the same quantity at different figures is a [critical] contradiction even
  when both are right steps of one bridge (R60): name the STAGE in the workbook's own row label,
  never delete one. A direction claim on a magnitude the golden holds with both signs needs the
  row that holds the figure to carry the direction verb in the criterion's words (R62). A
  criterion asking for a CHANGE against a deliverable describing the term AS IT STANDS gives the
  judge the same nouns in opposite order (R28): carry a WHAT IT SAYS NOW / WHAT WE WANT pair in
  the golden and keep the inverted phrasing out of the prose. Where the golden performs a reading
  everywhere and states it nowhere (what a date code IS), say it in the tab the criterion names.
- A positive whose SUBJECT is the audited object and turns on "rather than" is agentless and
  inverts for the judge (R80): make the deliverable the subject and name who did what ("The memo
  claims 292.60 on invoice X, where DFL applied the surcharge to the base charge instead of the
  573.72 net linehaul"); re-subject sibling "Invoice X rates ..." rows in the same pass.
- A dated criterion copies the golden's ROLE for the date (May 15 as the LAST single-receiver day,
  not the first); the honest runs fail it and the lenient run passes it, which is the flake
  signature. Use the deliverable's own word for a date's role (claim deadline vs
  filing date).
- A stated basis has to reproduce the figure to the cent (R31/R64): when a figure is one rounded
  amount less another, say so; a one-step paraphrase is a different computation, and a percent
  of a base whose components span sheets gets re-derived by the review. Prefer restating the path
  over accepting two cents.
- A criterion proving an ABSENCE ("kept rather than cancelled for age", "as material that is not
  coming") flakes: re-key onto a cell that only exists if the thing survived ("still converts at
  12019.23", the backlog row's own phrases). Blank-or-absent fields are recast as the positive
  observable the golden carries (the flag, the marking, the zero), and look-alike siblings beside
  the blank are named as not-new-assignments with failure pinned to values DIFFERING from them.

## 3. Wording the objectivity and polarity checks accept

- One hedge fails the whole objectivity dimension (R19): "where judgment is exercised",
  "everywhere the workbook touches it", and any vague intensity on a MAGNITUDE (roughly /
  approximately / about / around / nearly / some / or so before a number). Buy flexibility with a
  computable rule (whole months of usage to the first confirmed receipt plus one month), never a
  fuzzy quantity; a hedge quoting a source is exempt only when the source actually hedges.
- One bare evaluative word fails it too (R25): consistently / appropriately / properly /
  accurately / thoroughly / adequately / sufficiently / suitable / meaningful / comprehensive /
  thin, and any subjective-sounding word beyond the list. The anchor must sit in the SAME
  sentence; a neighbour's anchor does not carry over. "as required by <named policy>" is fine.
  Vague scope nouns get enumerated ("headline figures" -> name them) and "references the detail"
  becomes a mechanism.
- Criterion text states a fact about the artifact, never a grader instruction (R18): "fails only
  if", "any response meets this if", "is a pass", "counts as met", "judge from", "verify by",
  "decide from", "do not answer this criterion", "scored by their own criteria", "credit here is
  for". The checker's own fix (restate the defect at positive weight) INVERTS the criterion;
  restate what the compliant deliverable does.
- No golden sheet or column names unless the prompt mandates them (W12, the quality review's
  rigidity finding); the wording that satisfies both the oracle and the review is a numeric answer
  key plus the full arithmetic chain, with sibling figures disambiguated by VALUE ("the
  pre-surcharge 4.74 and pre-adder 5.02 are upstream intermediates"). Naming the golden's column
  headers in a coverage row draws W12; word it functionally ("the program side and the shelf side
  standing in columns of their own"). Headers the prompt requires may be named.
- A rule over an UNNAMED member of a class hands the judge its own choice of rows (R34): before
  writing "an X is treated this way where Y", search the golden for a row satisfying Y treated
  differently; a definite subject ("Line 2 of order 44121 ...") is the whole fix. The same shape
  without a causal clause stays uncoded and is fixed the same way.
- Scope a property claim to the columns it is about (R33): "throughout the workbook no quantity
  is negative" failed on a correct net-of-returns figure two tabs away.
- `unverifiable_from_deliverable` means the wording is on the INPUT side ("the suppliers'
  shipping paper", "at the cost on the file") or a counterfactual ("would fall short without
  Sedlacek's lines"): name the deliverable's own column or page as the place the comparison is
  made, and state the standing fact. A cross-workbook consistency row that re-derives an aggregate
  over 53 rows is fixed by four adjacent cells that add up.
- Never make the judge re-derive a big aggregate from an input file; anchor relative windows to
  absolute dates; "X appears on no line" breaks when a zero-quantity row for X exists.
- The oracle awards partial credit per atomic statement, so cutting statement count raises the
  score directly; a five-statement scope row failed with the right ten codes listed.

## 4. What the Rubric Quality Review reads

- Every figure carries its input-side derivation in the sentence ("the sum over the 320 items of
  pick lines times the current bin's walk distance in the location master, is 7358662"); a bare
  computed value reads as "derived from the golden solution rather than independently verifiable
  from agent-visible inputs" on workbooks AND docx memos. Every judgment word (busiest, nearest,
  safety, same order) gets a rule, a section or an input column as its anchor, never a second
  figure. Section numbers drop where a row already holds two figures.
- A presence row over a computed figure is BLOCKING (R119, 2026-09-11): "the branches tab shows the
  spend staying with the branches ... for each branch" drew "rubric does not verify computed values";
  the row names the total the figures reach or the source rows they reconcile to.
- "First page" is the first worksheet to the judge (R120, 2026-09-11): "stated on the first page" failed 2/3
  with the figure on a sixth-tab Summary behind five reference tabs. The summary is the first tab; the
  September batch (52 to 56) built it last.
- An ALLOCATION task's outputs (bins, move counts, walk indices from a rank-based allocation)
  read as re-solve-to-verify whatever the wording (three rounds): score constraints checkable row
  by row against the inputs with one worked example each, keep only the two R9 strict keys, and
  rebut with the fidelity axis's own confirmation of the figures.
- Rigid-value composition cap ~80%: 22 of 25 exact-number rows rated miscalibrated. Convert
  count-anchored single facts to method/coverage wording at unchanged weight (an action list
  naming an owner and a date against each thing to be done, without the count cell); never touch
  the liveness pair or figure answer keys. Hand check (RUBQ-RIGID), a digit proxy misreads it.
- Never pin a presentation count (twelve summary figures, "8 actions in all", five rows) or a
  layout the prompt never fixes (R32); a data-row count the inputs fix is fair. Never pin a date
  the prompt or inputs do not set or derive ("filed by September 15" was the golden's own planning
  choice, an invented deadline); pin the RULE the date must satisfy ("a Friday after the
  08/28/2026 plan date") so every honest choice passes. Test every value-pinning row against the
  PROMPT and inputs alone: could a solver who never saw the golden reach this number
  (peer-statistic IQRs under an unstated CSV filter could not)?
- "appears nowhere in the table" overclaims when the value sits at another key; write "not the
  row this key points to". A method summary keeps each rule's test on its own object.
- A criterion the reviewer disputes on a figure that is actually right shows a grading hole: add
  the criterion that states the inference (one rubric's 125 under a "per register" header).
- Do not paste a checker's suggested rewrite without testing it against the other checks (R21,
  the near-identical check, W12 have each failed a suggested wording).
- Owner and date wording is bounded on both sides ([[rubric-coverage-and-completeness]], R81/R100).

- 2026-09-11 (a revision round): W8 fires on a $ figure in a sentence that also says "new L1..L4" or "landed/net/invoice cost" with no answer-key anchor; write "SKU X's L1 price on the Repricing tab is set at $23.75 …" and keep "cost" out of a strict row's cell label. R74 reads a prompt saying "keep the math live" as a recalculation contract and wants a strict row's subject to carry "total" or "sum of" (label the cell "Total …"). The completeness check counts only gated rows as the LIVE cluster's direct weight, so two strict +5 rows still need gated rows worth over 7% of the positive total plus one.

- 2026-09-11 (a round 2, Rubric Quality Review [major] x3): a bare golden tab name in criterion prose ("The Bridge_Buy tab carries", "on the ROP_SS_Reset tab", the strict-row shape "plain cell references into the Bridge_Buy tab") is misaligned_or_unjustified_rigidity unless the prompt or an input mandates the name; W12 never saw the prose form. Name what the tab IS (the transition order, the reset, the front tab, its open order row) and keep the answer key. Coded as R112 (exempts names the prompt or any input carries).

- 2026-09-12 (a round 6, coded R121): a positive that names an answer as "one acceptable answer" is the answer key to the Rubric Quality Review whatever the softener (misaligned_or_unjustified_rigidity, major, after two rounds of hedging); score the structure the row tests and leave validity to sibling rows. Same round, uncoded: a row asking for a "before-and-after table" flaked 1/3 on a table holding after values beside deltas; the golden table carries the current and after-move columns literally and the row uses the table's own nouns.

- 2026-09-12 (a round 3, adjudication, uncoded): when an input table lists several options that meet the requirement (five 480 V wye standby windings, all above the 1,200 kVA inrush), a positive that pins the golden's pick or its figure (B601-2, 3,866 kVA) is over-constrained; grade the property of whichever option the report calls out and ask for its identifier from the table. RUBQ-RIGID by hand, no detector.

- 2026-09-12 (a round 3, adjudication, coded R122): a positive that opens on a disposition verb and names the alternative ("holds the bid ... rather than cancelling it") mandates one business choice where the prompt invites any evidence-led conclusion, so a defensible proceed-and-flag answer loses the row; score that a disposition is stated and the finding it rests on, and leave the choice to the solver. RUBQ-RIGID; quiet on fact-versus-wrong-explanation contrasts ("attributes X to Y rather than to Z").

- 2026-09-12 (a round 4, golden check 0.9825 in 1/3, coded R123): an identifier borrowed from an input (B601-2, ADS-311) is written in the input's exact hyphenated form; "B601 2" sent the judge to a hand read of the PDF table, where it misread the row. Name the sibling rows the golden rejects with their figures so the judge can match the table.

- 2026-09-14 (a round 5, golden check 0.9825 x 2, uncoded): the judge's PDF table extraction can shift a column (it read B601-2 as 600 V in every run of two rounds) and the misread is stable, so a hyphen fix makes it worse by making the token findable. When the golden borrows one row from a PDF table of near-identical rows and the rubric accepts any qualifying row, call out the row whose tokens the judge's read agrees on (B600-2 at 3,313 kVA) and state no column the read may shift (temperature rise). Coded checks cannot see this; read the judge's reason text for the table it believes in.

- 2026-09-14 (a round 2, golden check 0.9895 in 1/3, PR16): a "which of the items are X" row is met by a per-row Yes/No marker column beside the items in the golden, never by a prose list above the table; the judge reads the table for the per-row attribute and missed the prose list one run. Word the row per item ("for each item, whether it is ...").

- 2026-09-14 (an adjudication, coded R128): a positive that prescribes one spreadsheet function as the mechanism ("computed ... by a COUNTA over the item column") or the exact words of a label ("the words matrix cells to re-key beside it") is returned as over-constraint; the adjudicator's remedy is "any formula-driven count ... or equivalent, with any label that identifies the count". Name the thing counted and pin its value ("91 cells to re-key, the count a formula over the list rather than a keyed figure"): R126 still wants the sheet's labelled footer graded and R118 allows only one figure-less formula row, so an unpinned count fails the gate both ways. R76 and R90 were silent on the prescription grammar.
- 2026-09-14 (a round 2, golden check 0.98 on 3/3, coded R130): a positive that cites "Section N.N" is graded by that number, so the golden must name the section where the point is made; C14 cited Section 3.2 and the golden had only Section 3.1, though its figures already applied the rule. Round 1's golden-versus-rubric table recorded a landing sentence that never existed: score that table by reading the golden, never from the rubric.
- 2026-09-14 (a round 2, golden check 0.98 on 3/3, coded R131): a positive citing a section ("PM-4 3.3") on the front page fails when the front page states the rule only mid-way through long prose cells (character 251 of 876, 464 of 854), even with the same rule in short cells on a later tab; the judge reads the sentence around the first hit as the whole claim. Open the cell on the cited rule with the members named, and word the row on the tags (WC-1 and MV-1), never "the two lines".
- 2026-09-14 (a round 2, adjudication, uncoded): a prompt asking the solver to "challenge one quantity that looks useful but should not be used" was graded by a row naming only the GS-18 lot G903 overage; the adjudicator named two equally grounded held quantities (60 FL-150 sets, 6 revision C valves) that would score zero. When the prompt says "one X" and the inputs hold several qualifying X, the row grades the structure (a quantity that looks usable, and the receipt control that bars it) and the golden states that control in the paragraph. Check the sensitivity row the same way: it may stay pinned only when a single document release changes the outcome.
- 2026-09-15 (a revision round): R64, R47 and R21 interlock on share rows. A percent row must state its base figure inline (R64). The base must sit on the same tab as the percent (R21), so a total kept only on another tab fails. If several rows state only that shared base (percents are not counted as figures), R47 fails every one of them. The shape that clears all three puts the base on the graded tab as a plain reference and restates share rows as "N of the BASE cases", each with its own second figure. A note row then scores a non-figure fact from the note.
- 2026-09-15 (a round 3, adjudication, coded R133): a pinned decimal whose unrounded value is a tie at its printed places (29.75 x 0.942 - 28.75 = -0.7255 pinned as -0.725), or that the golden reaches by rounding cells already rounded to the same places, is returned as failing a correct single-rounding solver. Pin a figure the chain reaches exactly; where the chain is exact (eighths times three-place factors) carry it unrounded under a 0.000### format, because ROUND at each step and four-place intermediates both fail: Excel's float ROUND breaks exact ties in both directions.
