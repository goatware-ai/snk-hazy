> **Superseded 2026-09-11 by `docs/rules.md`** (generated from the check registry, one line per id). Kept as the archived rationale text of the 2026-09-04 monolith; ids and wording here may be stale.

# autoeval_check.py check catalog (archived 2026-09-04)

The module docstring of the monolithic gate as it stood when the checks moved into
`tools/gcheck/`. Kept verbatim for the per-check rationale; the live catalog is
`tools/autoeval_check.py --catalog` and the rule map is `tools/gate_families.py`.
Check ids renamed in the split: A10 (as-of) -> A18, R31 (percentage basis) -> R87,
R32 (nested money literal) -> R89, R39 (function tokens) -> R90, R39 (carries N) -> R91,
R46 (grouping coverage) -> R92, R57 (month fragment) -> R93, R58 (stored form) -> R94,
P2 (file glosses) -> P5, R12 (total twins) -> R95.

```text
One-command pre-flight for a task folder, against the platform's documented pipeline.

The platform runs (docs/submission/platform/task-lifecycle.md, captured from the live GitBook
2026-08-26 — the authoritative source, with docs/submission/platform/project-guidelines-v5.1.md
for the authoring rules):

  1. Seven in-app pre-submission checks (O*NET compliance x2, input files quality,
     prompt quality, golden solution files quality, rubric quality, name check).
  2. Ten post-submission evals: golden_solution_check (3 agents, must score
     1.0000/1.0000/1.0000), dataset_quality_check, difficulty_check (Easy =
     worst-agent accuracy > 80% -> NEEDS_REVISION), llm_authorship_check (mean
     < 3.5 -> NEEDS_REVISION), agentic_rubric_quality_check, audit_check,
     self_containment_check, golden_solution_leakage_check,
     rubric_golden_alignment_check, geranium_safety_check.
  3. Human review (maximum 5 total reviews, then accept-or-reject only).
  4. Adjudication: one exhaustive programmatic pass (golden accuracy, input
     leakage, omissions/conflicts, prompt verbosity, task contract, rubric
     coverage, over-constraint, mechanical defects, solvability, safety);
     returned minor fixes go back to adjudication, bypassing human review.

This gate codifies every failure class observed on this portfolio (feedback-log.md
entries, Aug 2026) plus the mechanically checkable rules from docs/submission/platform/, and
chains the single-purpose tools, so a task is checked against the full catalog
before submission:

    .venv/bin/python tools/autoeval_check.py submissions/NN-task-name
    .venv/bin/python tools/autoeval_check.py               # every folder in submissions/
    .venv/bin/python tools/autoeval_check.py --no-caches submissions/NN-...   # skip cache scan

Sections and their AutoEval source:

  1. Rubric — golden-solution oracle + platform rubric checks
     - all rubric_lint.py rules (E1/E2 polarity+quantifier, W1-W12; W11 added
       2026-08-19 after hartwell run 6 — un-anchored universal-sweep positives
       flake; W12 added 2026-08-19 after hartwell's Rubric Quality Review —
       golden Sheet!Cell refs / named columns in criteria read as golden-only
       schema imposition, keep numeric answer keys + arithmetic instead; W8 added
       2026-08-19 after hartwell run 5 — un-anchored sibling-cost spot-checks
       flake a different criterion each oracle run; W10 added 2026-08-19 after
       marathon run 6 — chain/hop-framed liveness criteria flake a different
       way each run, anchor on the aggregation range + no-tracing carve-out)
     - R1 ERROR criterion text over the 500-char form cap (01/03 fixes sized to it)
     - R2 ERROR process-ordering clause ("before any X is sized") — the "Rubric
                final outcome focus check" FAIL on task 07 C20; date-vs-date
                comparisons written in the deliverable are fine and not flagged
     - R24 ERROR the full-credit completeness hole: a workbook with every figure
                right but keyed by hand keeps >=90% of positive weight. The
                platform counts only criteria such a workbook FAILS, and failed
                task 20 on 2026-08-21. Fix by cutting the positive denominator
                (10 liveness points need a total <=99) and by gating substantive
                figures on their own cell being derived
     - R25 ERROR an evaluative term ("consistently", "properly", "adequately")
                with no number, precision or quoted source in the same sentence.
                The Rubric objectivity check treats one such word as failing the
                whole dimension, and it is separate from R19's hedge family
     - R26 ERROR a count stated in a positive criterion ("18 short and 31 late",
                "4 of them never acknowledged") that no solution cell holds. The
                oracle judge recounts off the deliverable and quotes the golden's
                own footer back; task 20 went 0/3 on one stale count. R20 misses
                these because its figure regex wants a decimal or four digits.
                Presence only: a small integer that happens to sit in an unrelated
                cell still passes, so recount rather than trust a clean run
     - R70 ERROR a positive criterion pins a row count ("all 72 ... one row each") and
                no single table in the golden docx has that many data rows; the judge
                sums across tables unreliably (po-conformance-review C26, 2 of 3 runs)
     - R71 ERROR a universal deadline pin ("every action ... before September 22") while
                a golden schedule table's By/Due column carries a later date
                (po-conformance-review C30, 3 of 3 runs)
     - R77 ERROR an OPEN-SCOPE fabrication negative ("cites a <figure / balance / entry /
       deadline / window / clock> beyond what <sources> document"): the judge must confirm
       every such figure against the sources and any it cannot match reads as fabricated
       (wanasek run 1, 2026-08-31, fired on an NSF entry the register carries as 11/24/25)
     - R80 ERROR an AGENTLESS COMPARATIVE in a positive criterion ("Invoice X has its
       surcharge rated on the net linehaul rather than the base charge"): the subject is
       the audited object, so the judge can read the comparison as either party's act
       (dfl-freight-audit C6, 2026-09-02, 1/3 on the golden)
     - R81 ERROR a positive criterion fixes an action's OWNER to a named person ("assigns
       Hector Ybarra the classing ..."): [major] rigidity in the Rubric Quality Review even
       for names the prompt carries (dfl-freight-audit C23-25, 2026-09-02)
     - R86 ERROR two positive rows put a per-item quantifier on the same attribute with no
       shared figure (a field-list row and a 'one of the codes on each claim' row): the
       platform's near identical criteria check reads subsumption (dfl-freight-audit 2026-09-03)
     - R27 ERROR (4 or more, and 3) separate figures asserted in one positive
                criterion. The Agentic Rubric Quality Review calls this non_atomic
                and rated task 20 needs_improvement on six of them. Split
                weight-neutrally: divide the parent's weight among the children,
                never add, or the completeness denominator grows and the loop in
                memory/rubric-criterion-count.md starts. Blind to non-numeric
                bundles (a layout plus two counts, item codes plus a total), and
                deliberately so: clause-structure heuristics were calibrated twice
                against reviewer labels and do not separate bundled from accepted
                (the note at the end of this docstring has the numbers). Hollenbach's
                second atomicity round (2026-08-24) named ten criteria R27 could not
                see, and every one matched a shape below. Check these by hand:
                  * a conjoined second predicate: "reproduce the published ceilings,
                    AND the variance is zero"; "totals 66 units, AND all of it falls
                    in October"; "is flagged below the floor, AND is put up for
                    approval"
                  * two dimensions swept at once: "reads 0 in every month for BOTH
                    constrained groups" - split per group or per month
                  * two subjects sharing one verb: "the ceiling control lines AND the
                    money summary reach their values through ..."
                  * a column list standing in for a table-shape claim: "each line
                    showing the item, the branch, the month AND the reason"
                  * a list of like figures under one measurement: the six briefing
                    summary figures. This one is defensible as ONE criterion until a
                    reviewer calls it, so weigh it rather than reflex-split
                Splitting stays weight neutral: a +2 parent divides into two +1
                children, never two +2s, because R24 caps the positive denominator
                (liveness has to hold 10 percent of it)
     - A9 ERROR a cached value the cell's own formula does not reproduce. The
                build injects rounded money into the cache while the formula stays
                unrounded, so the workbook changes on open and a rubric figure
                pinned to the stored value moves (task 20's 1,097.90 became
                1,097.89 downstream and the oracle failed it). Round in the
                formula, never in the cache
     - a task may record a finding that predates its own submission in
       submissions/NN-x/.gate-debt (see load_debt); everything else is an ERROR
       one line per finding ("C17 R43 = why"), reported as DEBT and not counted.
     - R39 ERROR a positive liveness criterion names a spreadsheet function token, which
                the judge's value-grep can never find in a formula (branch-stocking-reset
                run 5). Claim a read-through with plain cell references instead.
     - R38 ERROR a strict-liveness criterion names a sheet that holds no reference-chain
                cell and no sole-call formula matching a head function it names, so the
                judge opens compound wrappers and reads them as typed (branch-stocking-
                reset run 2, C5 flaked 1/3).
     - R35 ERROR a positive criterion asserts a value with no digit and no row key
                anywhere in it, leaving the judge nothing to grep (branch-stocking-
                reset run 1: the class-holdback claim failed 1/3, judge quoted a tab
                with no class column). Spelled-out numbers do not count.
     - R54 ERROR a positive criterion carrying a second scorable turn: a second
                sentence, a trailing so/including clause, a parenthetical with its
                own figures, a three-parameter rule, or a value beside its own
                derivation. An AUTHORING constraint, not a classifier (it also hits
                rows the reviewer did not name, each the same shape as one he did);
                the repair is to fold the turn in or give it its own row
     - R49 ERROR a positive criterion carrying two subjects a grader scores apart:
                two or more item codes under one predicate, two or more account
                numbers under one predicate, or a count of things beside a money
                total. The yankton-branch-opening reviewer sent the task back on
                thirteen of these (2026-08-24) and R27 saw two, because the rest
                carried two figures or none. Split, and split the parent's weight
     - R56 ERROR a criterion pins a DATE to a row key ("September 4 ... on order
                44243") and no single sheet carries both as written. R43 for
                money, in tokens R43 cannot see; date form counts, so a spelled
                date and the stored 09/04 are different anchors (open-order-
                cleanup run 5, 2/3: the briefing spelled the date without the
                order, the row the judge read carried the order without a date)
     - R48 ERROR a positive criterion ASSERTS a figure as a percentage ("is 97.1
                percent") where the cell holds 0.971 under a percent format. The
                judge greps cached values, so the percentage is unfindable
                (task 20 run 8: "[no matches for pattern '97.1' across 9 sheet(s)]").
                Name the stored decimal in the criterion as well
     - R40 ERROR a negative stating its defect as a COMPARISON of two quantities
                without quoting the label of a single verdict cell. The judge has
                to align two columns down the table and drifts by one
                (open-order-cleanup run 4: a negative naming OPEN ALLOWED fired on
                the neighbouring OPEN CORRECTED column, -4). Put a count of the
                failing rows in a cell and quote that cell's label
     - R37 ERROR a negative criterion carrying a THRESHOLD ("beyond thirteen weeks")
                where a golden cell under a column of that unit already sits past
                it. The judge lands on the cell and fires the negative for its full
                weight without reading the clause meant to exclude that row
                (open-order-cleanup run 3, a deadstock row at 14.4 weeks with nil
                open quantity, -4). Key negatives on a two-column comparison
     - R34 ERROR a positive criterion states a rule over an UNNAMED member of a
                class with a causal clause ("Two order lines ... are closed
                because ...", "An order more than ninety days old ... is kept
                where ..."). The judge picks its own rows: open-order-cleanup
                run 2 lost the first 2/3 to the short-close rows and the second
                1/3 to an order cancelled for a different reason. Name the order
                or line the golden means
     - R33 ERROR a positive criterion asserts a property "throughout the workbook"
                that the golden itself falsifies. Hollenbach C44 claimed no negative
                quantity workbook-wide and failed 3 of 3 oracle runs on a correct
                net-of-returns cell (-17) two tabs away from the order columns it
                meant. The judge reads every tab, so scope the claim to the columns
                it is about rather than the whole file
     - R28 ERROR a criterion states "X rather than Y" where a solution cell states
                "Y rather than X". The judge quotes that cell back as the
                contradiction (task 20 C41, 1/3). Say both in the deliverable:
                the term as written and the change being asked for
     - R30 ERROR a strict liveness criterion naming no head function and no plain
                cell reference (vondrak run 1, C23 over compound ROUND cells, 1/3)
     - R32 ERROR a money-sized literal (1,000 or more, not a year) nested inside a
                stored golden formula on a row whose visible cells carry a
                different figure. The judge greps cached values and head
                functions only, so a base that lives solely inside
                ROUND(D5*393900,2) is invisible; vendor-terms-program run 1
                failed its Selzer negative (1/3) because the row showed 456,300
                of purchases and no 393,900 anywhere the judge could land. Give
                the figure its own cell and reference it
     - R47 ERROR the same decimal figure is stated by two POSITIVE criteria — the
                platform's near-identical-criteria check reads the weaker row as
                subsumed and FAILs (june-price-review pre-submission, 2026-08-24:
                "3,356.41 reported as absorbed" was subsumed by the reconciliation
                row "tying to the 3,356.41 absorbed"). Give each positive criterion
                a figure no other positive states; restating a figure in a NEGATIVE
                is the allowed mirror the check itself exempts
     - R46 ERROR the prompt demands a grouped/batched presentation ("batched by
                account", "grouped by vendor") but no positive criterion grades that
                grouping — the platform's Rubric requirement mapping check FAILs on
                exactly this (june-price-review pre-submission, 2026-08-24: "batched
                by account so the branches can make their calls" had no mapped
                criterion; invoice-level and total-level criteria do not count as
                coverage). Add one dedicated criterion for the by-group organization
     - R44 ERROR a strict liveness criterion whose target is a range STORING a
                named function (SUMIFS, COUNTIFS, ...) rather than plain =Tab!Cell
                read-throughs — flaked 2/3 on june-price-review run 3 even with W4
                chain acceptance, W10 no-tracing anchoring and the head function
                named (the judge read the range in value mode, the marathon run-6
                stall). The shape proven across nine oracle runs on that task is
                the briefing read-through (hollenbach): grade cells that HOLD a
                plain reference, splitting disjoint cell sets to carry the weight
     - R39 ERROR a positive criterion says the deliverable "carries/runs/lists N
                <things>" while also asserting the count stands in a cell — the judge
                sometimes recounts the list instead of reading the count cell and
                flakes on section headers and note rows (june-price-review run 2, C24:
                "carries 91 matrix cells to re-key" went 1/3 with the judge quoting
                the very cell holding 91 as not_observed). Point the claim at the
                count cell itself: "closes with its count, N, computed in a cell"
     - R31 ERROR a positive criterion places a count IN A CELL ("standing in a
                cell", "beside", "in the cell below") but the workbook carries that
                count only inside a sentence (june-price-review run 1, C2 +5: "332
                ... in a cell beside the 987 extracted lines" failed 1/3, the judge
                finding 987 only in briefing prose). R26's prose escape is for counts
                a criterion merely states; once the criterion promises a cell, the
                number has to be a numeric cell value
     - R29 ERROR a criterion states how a figure is derived while that figure sits
                in more than one cell. The summary tab reads every headline figure
                through from the tab that computes it, so the judge can land on the
                reference copy and fail the criterion (task 20 lost one criterion to
                this shape in three of four oracle rounds). Leave derivation to the
                two liveness criteria, which grade a tab rather than one figure
     - R31 ERROR a criterion states a percentage basis that does not reproduce the
                figure it pins. Task 20 pinned 1,097.90 as "two percent of the
                purchases that leave", which computes to 1,097.89; the golden
                subtracts two separately rounded rebates. State the path the
                deliverable takes, or accept both cents
     - R32 ERROR a criterion pins an exact count of the figures on a summary page.
                The prompt fixes no such count, so a solver carrying eleven or
                thirteen useful figures up front fails. Grade that each NAMED
                summary figure is formula derived instead
     - R39 ERROR a positive strict-liveness criterion sweeping a whole tab ("the X
                tab's figures stand as stored formulas") while that tab also holds
                typed numeric constants among its cells. The judge sweeps every
                cell it can see and quotes the constants back as the violation:
                vendor-terms-program run 1 failed C19 (+5, 1/3) on Program!C4
                60000, C11 1456.3, C12 16115, the keyed line, repayment and
                unclaimed figures a program tab legitimately carries. R30 and R38
                had both reported the criterion without proving it an error
                because a reference-chain cell on the sheet rescued it. Name the
                read-through cells and anchor their cached values instead of
                sweeping the tab
     - R41 ERROR a negative criterion sharing a distinctive proper-noun subject with a
                positive criterion outside its own carve-out sentences. The Agentic
                Rubric Quality Review rated vendor-terms-program needs_improvement
                (2026-08-24) on four positive/negative mirror pairs (Heitkamp
                letter terms scored +4 and -3, Selzer base +4 and -3, the bank
                test +5 and -4, the credit line +5 and -4), reading each pair as
                double-counting one requirement even with polarity pins in place.
                Keep the positive, spend negatives on failures no positive scores
     - R45 ERROR a strict liveness criterion whose value anchor is a figure another
                criterion already scores. The near-identical check reads it as
                subsumption and FAILs the rubric (task 20 twice). R9 wants a value
                beside the liveness clause; pick one nothing else states
     - R46 ERROR a strict liveness criterion anchored on a COUNTIF over a text
                pattern many cells match. The judge reads the matched rows and
                quotes them back instead of reaching the count (task 20 lost the
                same criterion two rounds running on one column)
     - R4 ERROR prompt demands "every/all <items>" but no criterion pins a
                completeness count — reviewer gap on tasks 01/03, fixed on 10
     - R5 ERROR answer-key drift: a 'Sheet'!range key cited in a criterion does
                not resolve against the task's workbooks — sheet missing, range
                outside the used area, an asserted function (e.g. "stores a
                SUMIFS") absent from a keyed cell, or a quoted golden formula
                differing from the stored one. Answer-keyed criteria (the
                pattern that fixed task 06 C29/C32) are only as good as their
                keys; marathon run-4 showed the judge takes stated keys at face
                value, so a stale key would fail oracle runs deterministically.
                Keys may use quoted or unquoted sheet names (unquoted added
                2026-08-19 after deadstock run 4 — the quoted-only regex had
                skipped Torbeck_RGA!D11:D20-style keys entirely).
     - R6 ERROR judge-invisible function token: a criterion cites a function
                that no stored solution formula uses, or that appears only
                NESTED inside wrappers (e.g. IFERROR(LARGE(...))). The oracle
                judge's search_xlsx greps cached values, never formula text,
                and its formula summary surfaces head functions only —
                deadstock run 4 failed C18 on 3/3 runs with "no matches for
                pattern 'LARGE'" against 6 stored LARGE formulas. Cite head
                functions only, or key on displayed values.
     - R12 ERROR criterion weight outside the platform's bands: positives +1..+5,
                negatives -3..-5, integers only (-1 and -2 are rejected outright).
                The platform's Rubric Structure Check FAILs on this. Added
                2026-08-19 after dillman set a briefing criterion to +8, following
                an AutoEval completeness suggestion that read "e.g., 8-10 points" -
                the two platform checks contradict each other, and the way to give
                a requirement 10%+ of positive weight without breaching +5 is more
                in-band criteria covering it, not one heavier criterion.
     - R11 ERROR criterion count outside 15-60 (docs/submission/platform/project-guidelines-v5.1.md
                "Require a minimum of 15 criteria and maximum 60", target 15-25;
                docs/submission/workflows/07-pre-submission-audit.md lists it as E1
                criterion_count). Added 2026-08-19 after a Rubric Quality Review
                asked for 12 bundled criteria to be atomised and the split pushed
                task 11 to 54 rows with nothing in the gate objecting. Atomising
                and the cap pull against each other: a list of like items under one
                measurement is ONE criterion (that reviewer accepted a seven-item
                and a ten-item sweep), so merge those back before deleting anything
                a criterion actually grades. Only the platform band is checked;
                conflict can only be resolved by a human: task 11 was submitted at
                52 on the user's call 2026-08-19, the atomicity instruction taking
                precedence over the cap, after AutoEval enumerated all 54 rows of
                the pre-merge rubric and raised no count objection. Every other task
                in the catalog sits inside the range (34, 37, 38), so a hit here is
                rare and worth reading rather than routine noise.
     - R10 ERRORanswer-key overlap between two criteria: one keys a cell the other's
                key already covers. The platform's "near identical criteria" check
                reads that as redundancy by subsumption and FAILS (dillman
                2026-08-19: C31 keyed 'First Order'!M43 for the order total while
                liveness C49 keyed K5:M43 and restated the same total, so passing
                C49 necessarily passed C31; Economics!C27:C29 vs C27/C28/C29 was
                the same shape, unflagged). Note the trap: the C49 anchor came from
                satisfying R9, so R9 now stands down when a liveness criterion
                explicitly disclaims value matching ("credit here is for the stored
                formulas ... scored by the criteria that state them"). Liveness
                criteria stay value-free; answer criteria own the numbers.
     - R8 ERROR answer-key value drift: a criterion states a numeric answer and
                keys a single golden cell, but that cell's cached value is not
                among the numbers stated. R5 proves the key resolves; R8 proves
                it still says what the criterion claims. Added 2026-08-19 after
                dillman rebuilt its settings and usage tabs under an already
                finished rubric; the judge takes a stated key at face value, so
                drift fails every oracle run. Liveness criteria are exempt: they
                cite a cell to show where a formula lives and state no value.
     - R7 ERROR compound-formula function key: a criterion asserts every cell
                of a range stores <FUNC>, but the stored formulas are compound
                (the function plus further terms). Judges verified pure
                single-call ranges on all 7 marathon oracle runs yet misread
                the compound =SUMIFS(...)+IF(...) Usage Rollup column as typed
                values in runs 4, 6, and 7 (run 7: 3/3 deterministic, after
                four wording attempts — wording cannot fix it). Anchor liveness
                criteria on pure-function ranges, simplify the golden formula,
                or drop the criterion (marathon C29 was dropped, 2026-08-19).
     - R9 ERROR formula-only liveness positive: a criterion whose satisfaction
                rests entirely on reading stored formulas (live formulas / not
                typed constants / stored cell formulas) with no displayed-value
                answer key beside it. Judge formula extraction is variance-
                prone even on pure head-call single-function ranges — deadstock
                C8 flaked 1/3 in oracle runs 3 AND 5 across two wordings while
                the values+formula-clause C18 passed 3/3 (added 2026-08-19,
                run 5; C8 dropped per the 2-flaky-runs house rule). Pair every
                liveness clause with cached-value anchors the judge can verify
                without formula tools, or expect flakes. Hollenbach run 3
                (2026-08-20) sharpened the picture: value anchors REDUCE but do
                not eliminate the risk — a value-anchored pure-SUMIFS pull
                criterion flaked 1/3 with the judge quoting the very anchor
                values it then failed (same class as kolterman C25), while the
                two REFERENCE-CHAIN liveness criteria (=Tab!Cell read-throughs,
                briefing pulls) passed every oracle run across three rounds.
                When a liveness criterion must exist, key it on reference
                chains the formula summary renders trivially, not on
                cross-sheet SUMIFS extraction; and drop an observed flaker
                early when a proven-pass criterion can carry the weight.
     - R13 ERROR (measured over the whole coverage BLOCK, not the single biggest
                criterion: omitting the requirement fails every criterion covering
                it, and splitting into independent failure modes is the prescribed
                fix since R12 caps any one criterion at +5. Both platform checks
                have now suggested a weight past that cap - "8-10 points" for the
                briefing, "8-15 point range" for the coverage table - so read those
                as "give this requirement ~10% of the rubric", never as a literal
                weight.)
     - R13 ERRORthe prompt demands "every/all <items>" and a completeness-count
                criterion exists (R4 satisfied) but carries under 10% of the
                positive weight — the platform's "Rubric full credit
                completeness check" computes what a solver retains after
                omitting the core coverage table from POSITIVE weight alone,
                and FAILs at ~90%+ retained (dillman 2026-08-19: the 138-row
                settings table sat at C2 w3 of 101 = 97% retained despite
                omitting the prompt's central deliverable; raised to w12 →
                98/110 = 89.1%). Sizing rule: retained = rest/(rest+w) < 0.90
                → w must be at least rest/9. Negatives do not help — the
                check ignores them (its own briefing analysis proves it).
                Note: on tasks whose prompt spreads the core
                deliverable over many criteria (deadstock's plan sections)
                a small completeness criterion for ONE section can be
                legitimate; judge the hit, don't auto-inflate weights.
     - R12 ERRORthe same dollar figure is asserted as a scored total (total/
                gross/equals/sum wording within 40 chars) in two POSITIVE
                criteria — the platform's "near identical criteria" check
                reads that as redundancy by subsumption and FAILs (deadstock
                2026-08-19: C3 "total gross credit value equals $7,283.04"
                vs C17 "authorized gross credit of $7,283.04"; the $7,283.04
                stayed in C17 because the quality reviewer's own suggested
                wording included it — the two platform checks pull against
                each other, and the near-identical one wins on totals).
                One total, one criterion: sibling criteria keep the
                mechanics/composition and may reference the figure only as
                context (allowance caps, subtraction operands are fine —
                trigger words are what fire). Negatives exempt.
     - R20 ERROR a criterion states a figure that no solution CELL carries as a
                value. The oracle judge verifies by grepping cached cell values, so a
                number that only appears inside a briefing sentence reads as absent
                (wamhoff C11, 2026-08-20: "Hongli's minimum of 40 cartons is 8,000
                pieces" failed 1/3, evidence "not excluded due to a 40 carton / 8,000
                piece minimum constraint in the deliverable", while 8,000 sat only in
                prose; fixed by adding a MIN PCS column).
     - R21 ERROR no single sheet carries all the figures a criterion states, so the
                judge must assemble the chain across tabs (wamhoff C4, 2026-08-20:
                the coverage-cap derivation lived on the demand tab while 57 cartons
                and 45,600 pieces lived on the order tab; failed 1/3 with the judge
                quoting the order tab row it landed on). Co-locate on one row.
     - R36 ERROR a liveness criterion describes the SPAN of the range it says is
                summed ("a stored SUM across the twelve monthly columns") while the
                cell carrying the value it states sums a range of a different width.
                luebbert run 2 (2026-08-20): C28 described the branch rows, whose
                P column stores =SUM(D5:O5) over twelve monthly cells, but pinned
                1,050, which lives on the kit TOTAL row storing =SUM(P5:P7) over
                three branch subtotals. The judge landed on the cell holding the
                value, found a SUM of the wrong width, and reported "displays 1050
                as a typed numeric value without a SUM formula" — 1 of 3 runs, the
                only thing between 0.9868 and a pass. R5 could not catch it (no
                'Sheet'!range key) and R6 could not (SUM is a head function and is
                stored). Fix at the source so every cell that can carry the stated
                value has the described shape, or restate the span. Judges land on
                the cell holding the number, not the cell you had in mind.
     - R22 ERROR a negative criterion restates a numeric literal that a POSITIVE
                criterion already scores, so the two read as a mirrored pair. Two
                gates punish this at once (luebbert run 1, 2026-08-20): the oracle
                DEDUCTED the -3 tankless margin negative on 3/3 runs, quoting the
                golden's own briefing sentence ("returns 27.6 percent at the 52.75
                it sells for now") as evidence the defect was present, because a
                golden that narrates the pre-remedy condition it then fixes hands
                the judge a true reading of the defect; and the Rubric Quality
                Review independently raised redundant_or_double_counted_criteria on
                that pair plus the Meramec pair (C6/C33) and the bench-hours pair
                (C4/C34), which had drawn ambiguous_negative_polarity 3/3 apiece.
                The fix in both directions is the same and matches the hollenbach
                run-1 rule (R15): keep the positive, drop the negative mirror, and
                spend the remaining negatives on failure modes no positive scores.
                Document identifiers (26-Q-4187) are not literals for this purpose.
     - R19 ERROR unanchored hedge-like qualifier ("where relevant / as
                appropriate / where judgment is exercised / everywhere the
                workbook touches it"): the platform's Rubric objectivity check
                FAILs the whole dimension on a single hedge because it defers
                scope to unspecified judgment (hollenbach C24 pre-submission,
                2026-08-20 — failed on the qualifier even though the criterion
                enumerated four concrete rules after it). Delete the qualifier
                and state the checkable conditions directly; "as required by
                <named policy>" is exempt, the source anchors it.
     - P1 ERROR deliverable filename not explicitly named in the prompt: every
                solution/ file must appear in prompt.md with a naming cue
                (saved as / named / call it / file name) in the preceding 80
                chars. The platform's "Prompt output filename check" FAILed
                deadstock 2026-08-19 on "One workbook back:
                yearend_deadstock_plan.xlsx" — the elliptical construction was
                read as referencing a PRIOR workbook, not the output name
                (same class as the "counter day Friday" grammar flag: trade
                shorthand parses wrong). Fixed to "Send me one workbook back,
                saved as yearend_deadstock_plan.xlsx". A creation-verb
                apposition ("Build me one workbook, X.xlsx", "Send me back
                one workbook, X.xlsx") also passes — the verb blocks the
                prior-file misparse; only the verbless "One workbook back:
                X.xlsx" form is known to FAIL.
     - info: positive/negative weight totals (deficit-arithmetic diagnostic:
             reward shortfall x total positive weight = failed criteria weights)

  2. LLM-authorship check — solution files (detect side)
     - F1 ERROR float-repr cached values, all xlsx (fix_floats.scan; HIGH tell,
                failed tasks 01, 06, 08)
     - A1 ERROR blue-family fills in solution xlsx (confirmed tells 1F3864,
                26374A, 3E5871, 1F3B57 — early reviewer feedback; use gray + warm accents)
     - A2 ERROR datetime-formatted cells in solution xlsx (extract as
                "2025-12-02 00:00:00" and dominated an early task's flagged chunks;
                store dates as text in the source CSV format)
     - A3       docProps: missing/tool creator, missing title, created ==
                modified (single-instant), created after modified, two files
                sharing one created stamp (per-document plausibility feedback +
                twincreek run-2 humanization)
     - A5       raw-paste wall dominating a solution workbook's extracted text (three
                signals: letterless or long-string walls, a dominant word-anchored tab,
                and a verbatim input extract over 30% of the text):
                a sheet with 100+ data rows carrying over 35% of the workbook's
                extracted characters. ERROR when a 250+-row wall is letter-free
                (letters under 15% of sheet chars — twincreek run-4 numeric wall,
                5% letters, detect 0.06 vs 27-43% on every detector-passing big
                tab), and ERROR when rows average a 45+-char longest string
                (dillman run 1, 2026-08-19: 141 settings rows each carrying a
                ~50-char templated reason sentence, mean longest 59.4, detect
                0.20 against the ~0.36 needed; the 250-row gate had let both of
                its walls through). Fires at a 25+-char longest string (the
                desc-column wall that failed twincreek runs 1-3 at detect 0.04-
                0.08; passing tabs sit at 8-23). Fix structurally: keep the raw
                transaction paste in the inputs, carry only a rollup in the
                solution (twincreek run-4 surgery), or anchor rows with short
                real-word columns like vendor/branch (deadstock, marathon).
                Run-5 calibration: wall removal alone moved detect only 0.06 ->
                0.18 (needs ~0.36) — the remaining AI-read texture was
                Title-case comma-phrased catalog descs and round-number-only
                money columns; hartwell's detect=1.00 rows are ALL-CAPS
                shorthand dense with full-precision decimals. Run-6 falsified
                the tab-local texture levers: shorthand descs + one ratio
                column moved detect 0.18 -> 0.14 (noise). Package internals
                are also ruled out — marathon/deadstock passed with the same
                openpyxl app.xml + inline-string structure. Twincreek was
                retired 2026-08-19 per user after six FAILs (a run-7 revision
                — hartwell-register briefing, extract tab dropped, pre-round
                build-up columns — was built but never graded). Standing
                design guidance for NEW tasks: no mechanical signature ever
                separated twincreek from a passing workbook, so treat
                deliverable SHAPE as the lever — a workbook whose honest
                fabric is tidy 2-dp money tables plus terse-fragment prose
                (bid worksheets) fights this detector; shapes that naturally
                carry flowing memo prose, word-anchored data rows, or
                high-precision working decimals (hartwell/marathon/deadstock)
                pass it.
     - A10      LLM prose tells in prompt.md, input .docx text and solution
                workbook text cells: tautologies ("committed work is committed",
                "policy 6.3 is still policy", "paragraph 8 is the whole story"),
                aphorism/slogan sentences ("September is use it or lose it",
                "Chestnut Ridge is where the money hurts"), idiom standing in for
                a quantity ("where we are naked", "not quietly dropped"), and
                compressed first-person filler ("I pulled the rest"); plus, over
                EVERY string cell and sheet title of the solution workbooks, the
                three classes the platform's authorship phrasing judge names in
                each FAIL report: self-describing titles ("Golden Solution: ..."),
                roadmap sentences ("the sections that follow") and pre-counted
                lists ("there are three key drivers") (pbw-rebate-reconciliation,
                2026-08-31, llm-only 3/5 on a reviewer-salvaged golden). The task 12
                reviewer (2026-08-22) named the structure: "messy workplace detail
                --> artificial shorthand/idioms ---> analytical requirement ...
                It is not how most people really speak at work." The full flagged
                history and the fix pattern per class live in
                docs/reference/llm-prose-tells.md. ERROR on a tautology (the highest
                confidence shape, three flagged in one task); also on the rest,
                since a single idiom in a document reads human and only the
                density is damning. Reads the GOLDEN's prose under the same rule
                as the inputs: task 12's briefing was flagged as hard as its memo.
     - A6       em-dash density in docx text (inputs + solution): the repeated
                "clause — clause" construction reads as LLM punctuation
                (reviewer fail on deadstock inputs 2026-08-19: memo 4 dashes /
                191 words, rep emails 9 / 506). ERROR at >=4 dashes and >=12
                per 1000 words; fires at >=3 and >=8. The task's natural docs
                sat at <=2 dashes (2.9-8.2 per 1000). Also fires on ANY em
                dash in prompt.md / the rubric CSV — house rule (user, 2026-08-19)
                after the portfolio-wide scrub: platform-entered text carries
                zero em dashes; use commas/colons/semicolons/parentheses.

     - A1 extended 2026-08-26 per docs/submission/platform/style-guide-llm-tells.md: the
                AI-blue range #1C3557-#2E4A6B is a named, trained-for rejection
                signal, in INPUT files as well as the solution, and in Word
                body shading and pptx fills as well as xlsx (docx styles.xml is
                deliberately not scanned - Word's latent default styles carry
                heading blues in every hand-made file).
     - N1 ERROR project/evaluation vocabulary in a shipped file's content, name
                or metadata ("rubric", "golden solution", "AutoEval", "GDPVal",
                "AI-generated", ...) and category/AI-status file names
                (golden_solution.xlsx, ai_output.pptx). Both an authenticity
                tell and a form of leakage
                (docs/submission/platform/creating-input-files.md section 4; the in-app
                Name Check covers only the literal project name).
     - L2 ERROR hidden-content leakage locations: hidden/veryHidden sheets,
                hidden rows/columns, cell comments, Word tracked changes and
                comments, input-deck speaker notes - the places leakage hides
                that the visible page never shows
                (docs/submission/platform/creating-input-files.md section 4).
     - T1 ERROR a tell log inside inputs/, solution/ or either zip - the tell
                log is standalone by rule, so meta content cannot
                cross-contaminate the task
                (docs/submission/platform/creating-input-files.md section 6).

  3. Golden cache presence — empty-cache scan on solution xlsx (judges read
     cached values; empty caches get misread). Pure XML scan: flags formula
     cells with no cached <v>. Recompute caches by opening the workbook in a
     spreadsheet app and saving (the in-repo formulas-engine injector was
     removed 2026-08-19 per user). Skipped with --no-caches.

  4. Task hygiene — audit_task.py sweeps (canary, 555 phones, weekday/date
     validity, zip hygiene, prompt file refs, future dates).

  5. Metadata
     - M1 ERROR occupation 13-1022 paired with a customer-facing bid/quote prompt
                (O*NET Compliance Check FAIL on task 08; use 41-4012.00).
     - M3 ERROR occupation 13-1022 paired with a prompt whose requested work
                reads as another domain's job (insurance claim preparation,
                litigation support, an audit engagement, a creditor's
                bankruptcy exposure and covenant workup) rather than as
                merchandise work. The platform's "Occupation prompt relevance"
                check FAILed frankfort-storm-claim 2026-08-21 on exactly this:
                the occupation and the picks were defensible but the prompt
                asked for "a property-loss claim workbook" and the check read
                the purchasing duties as "only a limited part of the requested
                work". Fix by reframing the ask around the merchandise work the
                deliverable actually carries (condition of the stock,
                replacement cost off the current supplier pages, mark-downs,
                the covering transfers and the replacement buy) and letting the
                other domain enter as the rules the values are written on, not
                as the job. The deliverable file name is part of what the check
                reads.
     - M2 ERROR an O*NET task pick whose duty has no signal anywhere in
                prompt.md. The platform's "Skills prompt relevance check" reads
                every pick against the prompt text and FAILs the whole section
                when the picks lean on standard occupation duties the prompt
                never asks for (task 13, 2026-08-20: negotiation, budget
                consultation and trend forecasting were picked for a recall
                reconciliation and claims prompt; only the specification pick
                survived). Pick tasks off the work the prompt actually asks for,
                not off the occupation's headline duties, and never reuse the
                previous task's block unchanged — the same four-pick block had
                been pasted into tasks 06, 11 and 12.

Not automatable, still manual: invented proper names vs inputs, source-document
sufficiency, symmetric-event rubric mirroring, verbatim pasted-source tabs,
answer-key sufficiency of stated totals, ONE CRITERION = ONE ASSERTION, and
cross-tab narrative consistency — every prose claim in an action list or briefing
(who gets what, how many, from which source) must be re-derived from the
quantitative tabs whenever the plan changes. Hollenbach run 2 (2026-08-20): a
leftover Coverage action row said Klinger accepts 224 Fegley breakers on Penn
Street while the Jobs tab planned those 224 from Hollenbach with classified 0 —
the platform's golden/rubric alignment audit caught the contradiction; the
mapping from job id to job name lived only in the inputs, so no repo-side regex
can. Sweep the text rows against the tables by hand after any replan.

Two more authoring rules from the kolterman reviewer (2026-08-20), neither
codeable here. (1) POST EVENT EXPOSURE: when the scenario turns on a dated
trigger and the input data runs past that date, the golden has to identify the
transactions on the far side of it and say what to do about them. Kolterman's
trace counted 76 affected units invoiced between the stop sale on 08/10/2026 and
the stock date of 08/18/2026 inside its 2,318 unit total and never separated
them, so the accounts that took product after the branches should have caged it
were treated the same as accounts served in March. No repo-side check finds this:
the rows were present, dated and correctly valued, and the ledger already carried
their dates, so nothing is missing or inconsistent in any mechanical sense. Ask
of every dated scenario: what happened between the event and the data cut, and
who has to be called first. (2) BASIS DEPENDENT PINS: when one criterion lets the
response choose a basis ("or at another horizon that carries the branches past
the first receipt"), every later criterion whose figures fall out of that choice
has to allow the same, or a justified alternative loses points twice. Kolterman
pinned 176 Renner pieces and 76 uncovered units against a three month horizon its
own coverage criterion left open. Keyword and adjacency heuristics do not find
the coupling (the dependent criteria share no distinctive token with the flexible
one - they name Renner and the substitute rule, not the horizon), so trace it by
hand: for each figure in the rubric, ask which assumption produces it, and tag
every figure that moves when the assumption moves.

The bundling rule is an authoring rule, not a check. The Rubric Quality Review
called 12 of task 11's 37 criteria bundled (2026-08-19) and asked for each item
split into its own atomic criterion. Calibrated against those 12 labels and the
25 the same reviewer accepted, clause-structure heuristics do not separate the
two: clause count (splitting on ';', ':', ', and', ' - ', parentheticals and
carve-outs stripped) has median 2 on BOTH sets, giving 9/12 recall at 15/25 false
positives, or 4/12 recall at zero. The reviewer's own boundary is semantic and
not self-consistent either - C29's three branch cycles and C37's three dates were
called bundled while C17's seven-position sweep, C23's "clears the minimum and
ships prepaid" and C34's "order points and line points" were not. Write criteria
atomic by construction instead: one measurement per row, derivation chains and
carve-outs inline (those are not extra assertions), and a list of like items
under a single measurement kept as one criterion.

Exit code 1 if any finding is open. Findings are binary: every check here proves
a defect. A finding that predates the check reporting it is recorded per task in
.gate-debt and reported as DEBT (see load_debt), never silently dropped.

```
