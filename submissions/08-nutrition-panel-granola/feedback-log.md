# Feedback log: nutrition-panel-granola

## 2026-09-21 · source: build · verdict: DRAFT

Built under claude-fable-5-1 by /create-task 4 0, task 2 of 4. Occupation Food Scientists and Technologists (19-1012.00), domain Life, Physical, and Social Science. Concept: a Nutrition Facts panel, ingredient statement and claims check for a granola bar computed from the frozen formula, the supplier nutrient specifications (one stated per serving rather than per 100 g), the pilot batch yield, a compound ingredient whose added sugars come from its own specification, and the company's rounding and claim rules, with the brand manager's proposed claims each tested on the unrounded figure per reference amount and per serving.

**Findings** none yet; the gate was run on the packaged files and closed at 0 errors before the draft was called built.

**Actions taken** package sequence run (office_resave --force, fix_floats, fix_metadata, zips, autoeval_check); clause-map.md, verify_golden.py, form-lists.md, form-payload.json and the rubric written off the Excel-recalculated golden.

**Form actions** none; a draft carries no Taskboard UID.

## 2026-09-28 · Auto-eval · input_sufficiency FAIL, difficulty INCOMPLETE · NEEDS_REVISION

Platform note (eval_revision_notes, 2026-09-23T00:51Z), fetched with tools/fetch_feedback.py: "input_sufficiency: FAIL ... the ingredient statement requires sub-ingredient declarations for compound ingredients per SOP 4.1, and sub-ingredient information is provided only for the dried cherries ... most critically crisp rice (RM-1187) ... and potentially brown rice syrup, vanilla extract, and roasted almond butter", plus "Agent Runner Error ... Hazy difficulty: INCOMPLETE". The JSON's difficulty child: glm-5.2 FAIL x4 (solved false), qwen3.6-27b INCOMPLETE, FAIL, FAIL, FAIL (3 valid, solved null); no PASS on seven valid attempts, so the INCOMPLETE is the runner error already read on title-exam-cedarbrook-lot12 the same day and asks for no change. Repo and platform agreed on every part before the revision (prompt, 23 criteria, five inputs, one output, times 15 / 60 / 240 / 60 at 6.25 h). The offer had expired 4.9 h before the fetch with further_revision_requests_allowed true.

**Findings**
1. The judge is right on the inputs and the golden is worse than the judge saw: the golden printed "crisp rice (rice flour, sugar, salt)" from no input at all, dropped "tart" from the cherries' listed sub-ingredients, and renamed the formula's vanilla extract "natural vanilla flavor" against SOP 4.1's own "declared common name on the formula", then hedged the renaming in the note. Root cause: the first build let the golden's ingredient statement carry facts and name choices the inputs never stated, and the rubric's row 12 graded them.
2. The three "potentially compound" ingredients the judge named had no input stating that they are single-ingredient purchases.

**Actions taken**
- New sixth input supplier_spec_s1187_crisp_rice.docx (Brekke Cereal Ingredients, S-1187 revision 7, python-docx then Word resave, Verdana body with its own heading colour, in-world creator and November 2025 stamps): Ingredients as supplied "Rice, sugar, barley malt extract, salt" with proportions in that order, the nutrition table per 30 g serving matching the CSV row exactly (the basis the CSV already cites), an allergen line on both arms of SOP 4.2 (barley malt extract is a gluten source but no major food allergen is present; the packing line also runs a wheat flake cereal with a swab between runs) and a superseded revision 6 that listed "rice, sugar, salt and malt flavor". The brief's supplier paragraph now says purchasing pulled S-1187 and that the cherries and the crisp rice are the only compound items, every other raw material bought as a single ingredient under the specification the nutrient sheet cites (A20-safe sentences).
- Golden: Formula!E4:E16 are =LOWER(Bn) (the common name on the formula, water row annotated as before), F6 and F8 carry the two specifications' sub-ingredient lists in their stated order, A20 states the sources; the statement now reads "Whole grain rolled oats, brown rice syrup, crisp rice (rice, sugar, barley malt extract, salt), clover honey, infused dried cherries (tart cherries, sugar, sunflower oil), roasted almond butter, sliced almonds, high oleic sunflower oil, vanilla extract, ground cinnamon, sea salt, soy lecithin." with Contains almonds and soy unchanged; the Ingredient Statement note, Claims G8 and the note's paragraphs A6, A8 and A9 rewritten (the barley malt arm, the crisp rice sugar under the no added sugar claim, the shared-line advisory as Priya's third decision, the "confirm the basis in writing" item dropped because the specification now states it). In-world core.xml stamps restored at zip level before each Excel resave (703 caches recalculated), fix_floats, fix_metadata.
- verify_golden.py derives the ingredient statement and the Contains statement from the formula names and the "Ingredients as supplied" row of every supplier_spec_*.docx and checks them on the Panel, the declared count and the note: 57 figures reproduced, 29 near flips settled by golden phrases.
- Rubric 25 rows, positive 33 (unchanged cap, one +5 strict row), negative -12: row 12 keeps the order and the cherries' sub-ingredients at +2; new row 13 (+1) the crisp rice sub-ingredients in S-1187's order; new row 24 (-2) wheat or barley carried into the allergen declaration; later rows renumbered, formatting row last at +2. A "common names under SOP 4.1" row was tried and dropped at the gate (W12, R20, R22 mirror of the water negative); the negative was re-subjected off "Contains" (R41) and re-verbed off "lists" (W19). metadata.json rubric, task_instruction, input_files (6) and times (15 / 70 / 240 / 60, 6.5 h) resynced; form-lists.md likewise; clause-map.md renumbered with a Revised line; struck-phrases.md created (six entries).
- Coded check: skipped. The finding is "a golden statement carries a fact no input states", which is the REV-TRACE hand walk (PR21) and the model-in-the-loop input_sufficiency check; a mechanical rule over parenthesised lists in golden text would fire on tab-name lists and every cross-reference, so it stays a hand rule. Recorded in memory instead.
- Gate: 0 errors on the packaged folder; zips byte-identical to inputs/ and solution/; package_sweep clean.

**Form actions**
1. Prompt: re-enter the stored prompt from instruction.md (the file list now names supplier_spec_s1187_crisp_rice.docx between the cherries specification and the brief).
2. Input File List: six entries from form-lists.md, the new one added in that position.
3. Re-upload i-nutrition-panel-granola.zip (six members) and s-nutrition-panel-granola.zip; confirm both uploadedAt stamps moved on a re-fetch, and read the input_files list back for exactly six members (PR14).
4. Re-enter the rubric: 25 criteria from the CSV, positive 33 / negative 12, formatting row last; confirm the count on the form reads 25.
5. Times 15 / 70 / 240 / 60, total 6.5; tools, domain and occupation unchanged.
6. Section 3 unchanged (AutoEval feedback).
7. The offer expired 2026-09-28T00:51Z; confirm on the platform that the resubmission is still accepted before re-entering anything (the pretreatment task's expired offer took its resubmission the same morning).

## 2026-09-29 · Reviewer · "please make this task harder" · NEEDS_REVISION

Reviewer note (revision_notes, 2026-09-29T16:34Z), fetched with tools/fetch_feedback.py: "please make this task harder". The evaluation of the 2026-09-28 resubmission had passed all four checks (difficulty PASS, no model passing any of eight attempts; input_sufficiency PASS on six files), and the platform's zips, prompt and 25 criteria matched the folder. The operator's direction: keep the task and make it a little more difficult and bigger than the build. Offer expires 2026-10-04T16:34Z.

**Findings**
1. No specific defect named. Read against PR21 and PR22, three answers were still labelled or safe: the nutrient sheet stated the crisp rice serving weight in two columns, no claim verdict sat near its threshold, and the cherries' revision in force agreed with the nutrient sheet row.

**Actions taken**
- Inputs, now seven. ingredient_nutrient_specs.csv: BASIS_G replaced by SPEC_BASIS ("100 g" or "serving"), the serving weight left to the specifications; the crisp rice source cell no longer states it; the almond butter row restated per serving; the cherries row left on S-3301 revision 4 (total sugars 58.00, added sugars blank). New supplier_spec_s3120_almond_butter.docx (Tresler Nut Company, revision 2, per 2 tablespoons of 32 g, a single ingredient, a peanut line statement as the second look-alike for SOP 4.2). formula_ocb_26_03.xlsx: sea salt 0.72 to 0.81 kg and water 6.00 to 5.91 kg, batch total unchanged at 120. SOP 1.2 gains the sentence that the specification in force governs where the nutrient sheet differs. The brief names the almond butter supplier and specification.
- Golden: sodium 142.7292 mg per serving and 135.9 mg per reference amount, declared 140 mg at 6 percent; low sodium now Not supported (three claims supported, three not), and reading the per serving rows as per 100 g or skipping the yield each flips that verdict; the Specs tab converts S-3120 from 32 g (55.625 g fat per 100 g) and carries the cherries at revision 5, where the nutrient sheet row would print added sugars at 7 g; the note's paragraphs on the inputs, the cherries, the claims and the decisions rewritten (five decisions, the salt cut to 0.79 kg giving 139.7 mg); Formula percentages rounded to five places (A8).
- verify_golden.py reads each basis and the values in force from the specification documents, adds the nutrient-sheet-cherries variant, and parenthesises only a multi-item list: 57 figures, no mismatch, 43 near flips settled by golden phrases.
- Rubric 29 rows, positive 33, negative 15: new rows 10 (almond butter conversion, +2), 19 (cherries at the revision in force, +1), 22 (almond butter read as per 100 g, -2), 28 (peanuts in the allergen declaration, -1); row 2 on 142.7292, row 5 on 140 mg, row 17 low sodium not supported at +2; rows 3, 6, 7 and the formatting row cut to +1 to hold 33. Gate findings on the first draft fixed in place (R27, R94, R132 on rows 17 and 19; A11 and A20 on the new document). metadata.json, form-lists.md (times 15 / 90 / 300 / 60, 8.0 h), clause-map.md and struck-phrases.md resynced.
- Coded check: skipped; the note names no mechanical defect, and the difficulty judgment stays with the platform's models and the reviewer.
- Gate: 0 errors on the packaged folder; zips byte-identical to the folder; package_sweep clean for this task, with one finding on another task reported and left untouched (06-tract7-boundary-retracement, tract7_boundary_analysis.xlsx docProps names Openpyxl).

**Form actions**
1. Prompt: re-enter from instruction.md (the file list now also names supplier_spec_s3120_almond_butter.docx).
2. Input File List: seven entries from form-lists.md; the nutrient sheet entry is reworded.
3. Re-upload i-nutrition-panel-granola.zip (seven members) and s-nutrition-panel-granola.zip; confirm both uploadedAt stamps moved and read the input file list back for exactly seven members (PR14).
4. Re-enter the rubric: 29 criteria from the CSV, positive 33 / negative 15, formatting row last; confirm the form count reads 29.
5. Times 15 / 90 / 300 / 60, total 8.0; tools, domain and occupation unchanged.
6. Section 3: a human reviewer owns this round, so say in one or two sentences what was made harder, without naming the answers.

## 2026-09-30 · Reviewer · six hardening arms · NEEDS_REVISION

Reviewer note (revision_notes, 2026-09-30T22:15Z), fetched with tools/fetch_feedback.py: "How to harden the task" with six numbered arms (fiber knife-edge between the bases, whole grain on the yield, a vanilla extract specification that makes it a compound ingredient, crisp rice revision control, a minerals boundary under SOP 2.6, a working-sheet discrepancy running the other way on sodium). The 2026-09-30T01:42Z evaluation of the previous resubmission had passed all four checks; the platform's zips (uploaded 01:39Z), prompt and 29 criteria matched the folder. Offer expires 2026-10-05T22:15Z.

**Findings** the six arms, applied as written; option (b) taken on the vanilla (natural flavors only, the claim passes, the statement expands and the added sugars move); the optional non-whole-grain oat fraction not taken.

**Actions taken**
1. Fiber: oats fiber 10.10 to 11.40 g per 100 g on the nutrient sheet; the bar carries 2.815 g per serving (10.1 percent) and 2.681 g per reference amount (9.6 percent), the claim fails on the reference amount alone and the panel still prints 3 g at 11 percent.
2. Whole grain: SOP 5.3 floor 8 to 15 g; 15.5 g yield-correct against 13.86 g on 42 g of formula; a new -1 on testing it at 13.86 g.
3. Vanilla: new supplier_spec_s5020_vanilla_extract.docx (Beaumont Flavor Company, revision 2, two-fold with sugar and a natural flavor, natural vanillin only, added sugars 12.7 g per 100 g against the sheet's revision 1 at 0); the statement prints "vanilla extract (vanilla bean extractives in water and alcohol, sugar, natural flavor)"; the brief's "only compound items" line left standing and the note calls it wrong; added sugars 7.929 g unrounded, still 8 g.
4. Crisp rice revision control: the brief's receiving line puts 1,800 kg of launch inventory in September 2025 lots and 4,200 kg in November and December with the pilot on the later lots; S-1187 now states the revision 6 proportions and that pre-October lots carry the revision 6 declaration; the wrapper prints revision 7 and the note makes the September lots Priya's third decision; a new -1 on printing the revision 6 list.
5. Calcium boundary: almond butter 111 to 65 mg per 32 g (specification and sheet), almonds 269 to 200, oats 52 to 45; the bar carries 25.7069 mg, 1.98 percent, declared 0 mg at 0 percent under SOP 2.6, which now states the 2 percent test is made on the unrounded amount; rounded first it would print 30 mg at 2 percent (a new -1).
6. Sodium the other way: new supplier_spec_s2210_brown_rice_syrup.docx (Lindqvist Grain Sweeteners, revision 3, sodium 2 mg per 100 g after a plant move, against the sheet's revision 2 at 43); sodium 139.9362 mg per serving and 133.3 per reference amount, declared 140 mg at 6 percent, low sodium Supported; on the sheet row the serving exceeds the ceiling.
- SOP: clause headings restyled to "1.3 ..." with section cross-references (1.1, 2.6, 3.1, 5.1, 5.4) so the golden's "section N.N" citations are the inputs' own form (G36, which fires once any input uses the noun). Golden: Specs rows for oats, syrup, almond butter, almonds and vanilla, Parameters B14 15, Formula F13, the Claims basis cells, the Ingredient Statement note and the note's paragraphs A4 to A9 rewritten; core.xml restored before each resave. verify_golden.py reads the whole grain floor from the SOP, adds the syrup-from-sheet, vanilla-from-sheet and minerals-rounded-first variants: 57 figures, no mismatch, 41 near flips.
- Rubric 39 rows, positive 33 / negative 19; negatives reworded without "although" clauses (the in-app atomic read); gate findings fixed in place (R27 on the inventory row, R20 25.7069 as stored, R50 15.5, R132 "clearing", A20). Nine inputs; metadata.json, form-lists.md (times 15 / 100 / 330 / 60, 8.5 h), clause-map.md and struck-phrases.md resynced ("Low sodium is supported" removed from the ledger because the verdict is reinstated by design).
- Coded check: skipped; the note is a hand-designed set of arms.
- Gate: 0 errors on the packaged folder; zips byte-identical to the folder; package_sweep clean across 59 files with no findings in any task.

**Form actions**
1. Prompt: re-enter from instruction.md (nine files named).
2. Input File List: nine entries from form-lists.md.
3. Re-upload i-nutrition-panel-granola.zip (nine members) and s-nutrition-panel-granola.zip; confirm both uploadedAt stamps moved and read the input file list back for exactly nine members (PR14).
4. Re-enter the rubric: 39 criteria from the CSV, positive 33 / negative 19, formatting row last; confirm the form count reads 39.
5. Times 15 / 100 / 330 / 60, total 8.5; tools, domain and occupation unchanged.
6. Section 3: a human reviewer owns this round; say that all six arms were applied and name the two specifications added, without stating the verdicts.
