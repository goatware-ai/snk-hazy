# Workflow 05 — Rubric: atomic, specific, weighted criteria

The rubric is how model outputs are scored against your golden solution. The platform
states the rules in two places: the count, the weight range, the negative-weight licence,
the values-from-ground-truth rule and the mandatory closing line in
`../platform/platform-submission-form.md#4-task-rubrics`; the criterion properties, the
weighting meanings and the mirroring mistake in
`../platform/platform-submission-form.md#4-task-rubrics`. This page holds what the
house adds on top; every coded rule carries its id, and `../../rules.md` states each in one
line.

Write the rubric **after** the golden solution, off the golden solution. Every value in it
is read from the ground truth, never estimated.

## How many criteria

| Band | Verdict |
| --- | --- |
| Under 6 | Not submittable as designed. The guidelines' floor is six clear criteria |
| 6 to 19 | Submittable, but under the form's expected range. Cover more of the task |
| 20 and up | The form's stated expectation: "somewhere in the 20-60+ range depending on complexity" |

There is **no ceiling**. The form says 20-60+, so a rubric past 60 rows is not a defect if
every row earns its place. R11 codes the floor and the recommendation.

The count is a symptom, not a target. The real rule is checklist item 9: enough criteria to
genuinely cover the task's complexity. Build the count by mapping every prompt clause and
every action the golden takes to a row (R4, R13, R101, R102), not by splitting rows to hit
a number.

## Weighting scale

| Score | Meaning | When to use |
| --- | --- | --- |
| +4 to +5 | Critical | Core deliverable correct and complete |
| +2 to +3 | Important | Correct structure, format, or key finding |
| +1 | Minor positive | Specific detail, label, or edge case |
| −1 to −2 | Minor penalty | A small, specific unwanted outcome: a stray extra item, a wrong label |
| −3 to −5 | Serious penalty | A specific unwanted outcome that damages the deliverable: page limit blown, wrong file type, a fabricated figure, an unsafe or privacy-breaching statement |

Any non-zero integer from −5 to +5 is accepted; there is no gap around −1 and −2 (R12).
Weights go in the numeric field only, **never in the criterion text**. At least one core
criterion must sit at +4/+5; flat weighting is a known defect (R99).

## Negatives: any specific unwanted outcome

Negative weight is not reserved for a class of catastrophes. The form's own instruction is
"use negative weights where useful, to penalize specific unwanted outcomes", and its three
examples are ordinary quality misses: extra items included that shouldn't be, page limit
exceeded, wrong file type.

What still constrains a negative is its **shape**, not its subject:

- One thing per line, the defect named specifically enough to be observed.
- **Affirmative phrasing of the defect**: the row reads TRUE when the failure is present
  ("The workbook carries rows for the three deferred families" rather than "does not
  omit ..."). E1 and W18 code it, one negation only (R53).
- Framed inside the sentence ("although <source> documents no X"), never as a trailing "in
  violation of" clause (R84).
- **Scoped to exactly the rows the golden would violate** (R33, R37, R52). A universal
  negative ("any populated price below floor") fires against the golden itself when the
  golden correctly holds some of those rows unchanged. Test every negative against every row
  class of the golden and carve out the classes that are supposed to violate it.
- Derivable from the shipped inputs, like every other row.

Carry at least two. A rubric where nothing can go wrong grades only presence, and the
scoring check still requires at least one positive weight so a correct deliverable can
score.

## The mandatory closing criterion

The rubric's **last** row is a general
**"Overall formatting and style of the deliverable"** criterion, commonly weighted ~+5. The
form requires it and checklist item 12 is a submit-blocking confirmation of it. Absent, or
present but not last, is a defect.

It is the one row allowed to be general. Everything above it is specific, so keep the
specific formatting checks (tab count, page limit, required columns, file type) as their own
rows and let this line catch polish and presentation.

## Values come from the ground truth

"Pull every exact value straight from your own reference files and ground-truth answer —
never estimate what a criterion should check." The form's own pair:

```
Bad   [+2] The workbook states total damage revenue as approximately $15,000.
Good  [+2] The workbook states total damage revenue as $15,170.
```

- Every figure carries its input-side derivation in the sentence, and every judgment word
  an anchor, or the value reads as unverifiable from the inputs (R20, R21, R29, R82).
- No hedged magnitude where a figure is asserted: "approximately", "roughly", "about", "~"
  in front of a number means the value was estimated rather than read off the golden.
- Checklist item 13: nothing in the rubric asserts a fact that is not actually derivable
  from the input files being shipped.

## House rules on top of the capture

- **One simple atomic sentence per criterion** (R55; the bundle shapes are R27, R49, R54,
  R85). Checklist item 10 blocks on it: no line bundles two separate checks with "and".
  Several record IDs in one criterion read as a bundle; phrase over the class or split one
  per item.
- **Do not mirror the instruction.** A row that repeats what the prompt already asked for
  only checks that the model read the prompt. Grade the concrete result: the value, the
  reconciliation, the edge case, the non-obvious pattern.
- **The file-name criterion is never droppable coverage:** the filename coverage check
  fails without the exact basename in a criterion, and the row grades content around the
  basename ("The memo, <basename>, is addressed to X") (R83).
- **Owner rows** score an owner or a date only when the prompt asks who and by when (R100).
  When it does, write "with a named person as owner and a calendar date", never the person's
  name and never a bare "an owner" (R81); when it does not, the row ends on the action.
- **Liveness rows** land on a pure read-through or one aggregation call, never same-sheet
  arithmetic (R98, R9, R72); summary counts and conditional sums are COUNTIF/SUMIFS, not
  boolean SUMPRODUCT (R96).
- **Keep style and formatting rows a minority of the count**, the closing criterion aside.
  A rubric whose weight sits in presentation does not distinguish a correct deliverable
  from a plausible one.
- **A rubric that would pass the golden's own errors is the rejection that survives a
  0-error gate.** Pin the facts the literal read verifies: each cited identifier, the
  deliverable's date, the signature line, the closed status of every policy class, the
  partial-period cost, the successor for a departing asset. Then ask of every row: if the
  golden had this wrong, would the row fail it?
- **Every prompt clause and every golden action row maps to a criterion** (R4, R13,
  R101, R102); build that map before reading anything else.

## Final screen before moving on

- [ ] At least 6 criteria, 20+ preferred; every prompt requirement covered (R11, R4, R13)
- [ ] Each criterion one atomic sentence testing exactly one thing (R55); no "and" bundles
- [ ] Every value read off the golden; no hedged magnitudes (R20, R21, R82)
- [ ] Rigid criteria state exact values; subjective criteria name their conditions (R19, R25)
- [ ] No criterion asserts a fact the shipped inputs cannot produce
- [ ] Every weight a non-zero integer in −5..+5, in the numeric field only (R12)
- [ ] At least one +4/+5; no flat weighting (R99)
- [ ] ≥2 negatives, each on a specific observable unwanted outcome, affirmative (E1),
      framed inside the sentence (R84), scoped to the golden's row classes (R33, R37, R52)
- [ ] File-name criterion present with the exact basename (R83)
- [ ] **The last row is "Overall formatting and style of the deliverable"**
- [ ] Golden solution scores ~100
- [ ] Each fact the literal read verified (`04-golden-solution.md`) has a row that would
      fail if the golden had it wrong

Platform note: the in-form Task Rubric Checks are advisory and block nothing
(`../platform/platform-submission-form.md#task-rubric-checks-optional`); the checklist is
what blocks. Judges decompose each criterion into statements and read ID lists as bundles;
the observed behaviour and the house mitigations are in
`06-metadata.md#house-notes-on-the-live-form`.

Next: `06-metadata.md`
