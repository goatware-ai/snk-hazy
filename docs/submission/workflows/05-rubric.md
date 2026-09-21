# Workflow 05 — Rubric: atomic, specific, weighted criteria

The rubric is how model outputs are scored against your golden solution. The platform
states the rules once, in `../platform/project-guidelines-v5.1.md#rubric`: the 15 to 60
band (aim for 15 to 25), rigid versus subjective criteria, the weighting scale, the hard
rules, affirmative wording of negatives, and the common mistakes. This page holds what the
house adds on top; every coded rule carries its id, and `../../rules.md` states each in one
line.

## Weighting scale, with the house reading of the penalty row

| Score | Meaning | When to use |
| --- | --- | --- |
| +4 to +5 | Critical | Core deliverable correct and complete |
| +2 to +3 | Important | Correct structure, format, or key finding |
| +1 | Minor positive | Specific detail, label, or edge case |
| −3 to −5 | Critical penalty | Only the four classes the platform's penalty scope check allows (R67): a safety harm, a privacy leak, an inverted or prohibited top-level decision, or a fabrication. A wrong answer, wrong method, or omission is never a penalty; score it as a positive the deliverable fails |

At least one core criterion must sit at +4/+5; flat weighting is a known defect (R99).
Positive weight is capped by the completeness check (R24): a workbook keyed by hand must lose more than 15% of positive weight, and with strict liveness capped at 10 points that pins the positive total at or under 39. Add coverage by displacing +1 rows, never by adding liveness rows.
Weights go in the numeric field only, **never in the criterion text**; the form accepts +1..+5 and −3..−5 (R12).

## House rules on top of the capture

- **One simple atomic sentence per criterion** (R55; the bundle shapes are R27, R49, R54,
  R85). The rubric quality review reads several record IDs in one criterion as a bundle:
  phrase over the class or split one per item.
- **Negatives:** at least two, each spent on one of the four R67 classes, framed inside the
  sentence ("although <source> documents no X"), never as a trailing "in violation of"
  clause (R84), one negation only (R53), and scoped to exactly the rows the golden would
  violate (R33, R37, R52). Affirmative polarity is the platform's rule; E1 and W18 code it.
- **The file-name criterion is never droppable coverage:** the platform's filename
  coverage check fails without the exact basename in a criterion, and the row grades
  content around the basename ("The memo, <basename>, is addressed to X") (R83).
- **Owner rows** score an owner or a date only when the prompt asks who and by when (R100).
  When it does, write "with a named person as owner and a calendar date", never the person's
  name and never a bare "an owner" (R81); when it does not, the row ends on the action.
- **Every figure carries its input-side derivation in the sentence** and every judgment
  word an anchor, or the Rubric Quality Review reads the value as unverifiable from inputs
  (R20, R21, R29, R82).
- **Liveness rows** land on a pure read-through or one aggregation call, never same-sheet
  arithmetic (R98, R9, R72); summary counts and conditional sums are COUNTIF/SUMIFS, not
  boolean SUMPRODUCT (R96).
- **A rubric that would pass the golden's own errors is the rejection that survives a
  0-error gate.** Pin the facts a reviewer verifies: each cited identifier, the
  deliverable's date, the signature line, the closed status of every policy class, the
  partial-period cost, the successor for a departing asset. Then ask of every row: if the
  golden had this wrong, would the row fail it? history:
  `../../reference/workflow-history.md#lift-truck-fleet-plan-rejected-at-first-human-review-2026-09-05`.
- **Every prompt clause and every golden action row maps to a criterion** (R4, R13,
  R101, R102); a reviewer builds that map before reading anything else.

## Final screen before moving on

- [ ] 15–60 criteria (R11); every prompt requirement covered (R4, R13)
- [ ] Each criterion one atomic sentence with explicit values (R55); answers human-calculated
- [ ] Rigid criteria state exact values; subjective criteria name their conditions (R19, R25)
- [ ] ≥2 negative criteria, affirmative (E1), critical-class only (R67), framed inside the
      sentence (R84), scoped to the golden's row classes
- [ ] Style/formatting share and weight under the platform's caps
- [ ] File-name criterion present with the exact basename (R83)
- [ ] Positive weight at or under the R24 cap; at least one +4/+5; no flat weighting (R99)
- [ ] Golden solution scores ~100
- [ ] Each fact the reviewer's read verified (`04-golden-solution.md`) has a row that would
      fail if the golden had it wrong
- [ ] **Run the platform's Rubric Quality Check before submitting**

Platform note: the form caps each criterion at 500 characters and carries only text plus a
numeric weight; the oracle's judges decompose each criterion into statements and the Rubric
Quality Review reads ID lists as bundles. The observed behaviour and the house mitigations
are in `06-metadata.md#house-notes-on-platform-submission-formmd`.

Next: `06-metadata.md`
