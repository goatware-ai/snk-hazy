---
name: difficulty-check-lessons
description: "The desk's first difficulty_check FAIL (carton-bid-evaluation, 2026-09-22): what the platform measures (per-model PASS/FAIL attempts in the fetch JSON, two PASS of four on one model fails the task), why the task was easy (every trap labelled in a tidy column, one rule applied once to four bids, nothing reconciled across files), and the rebuild shape that answered it (a candidate set to eliminate, conditions in prose letters, a responsibility register with a name variant and a decoy, a superseded drawing revision under a STATUS column)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 12ee6dd7-5e9b-4059-aab3-83e9dc851d57
  modified: 2026-09-22T08:24:19.654Z
---

Open on any "Hazy difficulty: FAIL" note, and before calling a new build hard enough.

**What the check is.** `evaluations[*].children_results[]` with `evaluator_name: difficulty_check`
carries `metadata.agent_result.models.<model>.attempts` (PASS / FAIL / INCOMPLETE per attempt),
`solved` and `valid_attempts`, then a `verdict`. On 2026-09-22 glm-5.2 went PASS, PASS, FAIL,
FAIL (`solved: true`) while qwen3.6-27b went INCOMPLETE four times (zero valid attempts), and the
verdict was FAIL, outcome NEEDS_REVISION. The visible note is one sentence; read the JSON. The
carried-over "80 percent worst-agent" rule in [[platform-expertdocs]] does not describe this.

**Why the task was easy (the root cause, not the symptom).** Four bids, five items, one
tabulation workbook. The tabulation carried an EXCEPTIONS_AND_ALTERNATES column that quoted the
exception with its ITB section and a PRICE_HOLD_STATED column restating it; the addendum flag was
"1" against "1, 2"; the discount floor, the freight rule and the extension rule were each stated
once and applied once. Nothing had to be reconciled between files, and no decision turned on a
column a solver skims. A model that reads the ITB and computes gets every figure.

**What fixed it, in the desk's own words from 01-ideation.md and 03-input-files.md.**
- *A candidate set to eliminate:* six bidders, each wrong one disqualified by a different
  property (an unacknowledged addendum and a superseded quantity; a six month price hold with an
  index in a cover letter; a full-truckload pricing condition in a cover letter that the
  addendum's Q&A makes a quantity exception; an open quality hold on the lowest responsive bid).
  Each missed trap changes the award to a different bidder, so the award figure, the margin and
  the approver all move together.
- *Conditions in prose, not in a labelled column:* the bidders' own bid forms and letters as a
  compiled docx, with the tabulation "as opened" recording only what the form boxes carry.
- *A step of the answer in a metadata column:* the item weights sheet lists drawing revision A
  (Superseded, addendum 2) and revision B (Current) for the amended item, so FOB origin freight
  moves; a hold register with a STATUS column, the bidder under its registered name variant
  ("Loken & Vik Container Corp." for "Loken & Vik Container"), a same-surname decoy also on Open,
  and the awardee's own hold Cleared.
- *A policy clause the first build never exercised:* PP-3.7 responsibility was already in the
  input; adding the register made it decide the award. Check every numbered rule in an input for
  one the golden never applies; that is free difficulty.

- 2026-09-22 (coded): L7 in leakage.py errors on an input column headed exceptions /
  deviations / qualifications / departures whose cell cites the section or policy number the
  record breaks (fires on the pre-fix tabulation, silent portfolio-wide, fixture
  labelled-exception-column); PR21 in procedural.py is the hand walk (every golden decision
  traced to the input fact it turns on; every numbered input rule applied somewhere). Cited in
  07-pre-submission-audit.md (`traps_not_labelled`), 01-ideation.md and prompts/submission.md.

**How to apply.** Before a build is called done, list each decision the golden makes and ask
where in the inputs a solver learns the fact it turns on; if the answer is "a column that names
the rule" or "the same sentence that states the rule", relocate the fact into prose, a second
file, or a status column. Two files that must agree on a name in two spellings beat one tidy
sheet. A difficulty revision is a rebuild of inputs and golden, never a rubric-only tightening;
the platform re-runs the models on the files.
