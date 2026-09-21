---
name: rubric-negatives
description: "What a negatively weighted criterion may penalise (any specific unwanted outcome, R67's critical-only allowlist deleted 2026-09-21) and the shape rules that survive: one thing per line (R55), single negation (R53), affirmative phrasing of the defect (E1/W18/R84/R111, no carve-out sentence R18), a closed class not an open scope (R77), the policy's condition not its subject, objectively checkable off one verdict cell (R37/R40/R52), derivable from the inputs, and no double jeopardy with a positive (R15/R69/R104)"
metadata:
  type: feedback
---

Open before writing or respending any negative. Siblings: [[rubric-liveness-criteria]],
[[rubric-anchoring-and-landing]], [[rubric-coverage-and-completeness]], [[rubric-criterion-count]].

## 1. What a penalty may be spent on (rewritten 2026-09-21)

**Any specific, observable unwanted outcome.** The form
(docs/submission/platform/platform-submission-form.md) reads: "Use negative weights where useful,
to penalize specific unwanted outcomes (extra items included that shouldn't be, page limit
exceeded, wrong file type)." All three of its own examples are ordinary quality misses, so there
is no critical class and no permission question left to answer.

**R67 is DELETED (2026-09-21).** Its allowlist reserved negative weight for safety harm, a
privacy leak, an inverted or prohibited top-level decision, and fabrication, and rejected
everything else as an ordinary miss. That rule came from a Rubric penalty scope check nothing
shows this platform runs, and the form states the opposite rule in its own words. Every
R67 arm goes with it: the literal token list, the conclusion-verb signature, the
classification-is-not-a-decision ruling, the methodology-whatever-the-verb ruling, the weak
fabrication forms. Do not answer a "can this be a negative?" question from an old rubric or an
old feedback log.

**No floor and no count.** The old bar of at least two negatives, each -3 to -5, is gone with
the allowlist. Weight is any non-zero integer in -5..+5 ([[rubric-criterion-count]]), and a rubric
with one negative, or with none where nothing specific is worth penalising, is legal. R61's 20
percent penalty-share figure survives only as a NON-BLOCKING recommendation (team manager ruling
2026-09-02, printed through `recommend()`, never a send-back in either direction) and is carried
over and not yet confirmed here.

What is left is shape, and the shape rules below are unchanged: a negative still has to be one
thing, readable in one direction, bounded, and checkable against the inputs and the golden.

## 2. One thing per line

- One sentence, one main verb, one scorable claim, at most 45 words (R55), the same bar a
  positive takes. The form's checklist item 10 says it too: "Each criterion tests exactly one
  thing - no line bundles two separate checks with 'and'."
- Negatives are exempt from R49 (they must name the class members they fire on) and carry the
  same R82 currency notation as positives.

## 3. Single negation, and the defect stated affirmatively

- **ONE negation per criterion (R53):** "not / never / no / without / rather than / instead of /
  fails to" twice and the judge cannot tell which way the row points (on one rubric the identical
  frame passed on the row that spent its single negation on the carve-out). State the defect
  positively ("trimmed in quantity", "stock beyond what the records carry").
- **The defect frame goes INSIDE the sentence:** incorrectly / violating / in violation of /
  contradicts / contrary to / although / even though / despite / wrongly / beyond what (E1's
  PIN_RE, W18's frame words). A negative with no frame word in the defect sentence reads as "what
  a correct deliverable does" (one rubric, -16 exposure). Frames other than "incorrectly" pass
  E1/W18 when a reviewer objects to the adverb.
- **No trailing ", in violation of ... / contrary to ..." clause (R84,** reviewer send-back
  2026-09-02: "remove trailing clauses that bring negatively weighted items into negative
  language"). State the act once and carry the frame as the act's condition: "... although
  <source> documents no <thing>", which E1, W18 and the reviewer all accept.
- **The carve-out sentence is DEAD (R18,** 2026-08-26): "... is not this defect" and
  "does not count as this error" read as scoring scaffolding. A scope boundary that truly needs
  stating becomes an affirmative fact, or goes inside the defect ("open quantity due that CAUSES
  its post-plan position to exceed thirteen weeks").
- **Never open in the passive voice (R111,** a round 2, 2026-09-11): "Bracket
  money is incorrectly booked ... although ..." is read as inverted polarity whatever frame word
  it carries. Put the deliverable in the actor's seat with a transitive verb: "The workbook
  wrongly books bracket money for a vendor other than the named one ...". "absent from every ..."
  states a class with no negation, where "not found on any" draws W1.
- **A bare plural negation of a nearby positive** ("Key outputs are constants") draws
  `ambiguous_negative_polarity` 3/3, because the judge grades each criterion as one true/false
  statement. The any-quantifier subject ("At least one ...") or the verdict-cell form ("The
  workbook's count of <verdict cell label> stands above zero, at least one ...") reads cleanly.
  The old meet-pin style ("met only when ...; X does not meet it") was retired 2026-08-19.
- **The although-frame alone can still be read backwards** (2026-09-11,
  two [critical] misaligned_or_unjustified_rigidity): "approves an award of one category to one
  bidder and another to the other" and "cites a tier price for an item that neither schedule
  lists" were both read as describing a compliant workbook. Name the defect class inside the act
  clause ("an award that splits the consolidated categories", "an invented price") and keep the
  frame. Not coded: every house negative passes the probe, the misread was the two sentences'
  shape.

## 4. A closed class, never an open scope (R77)

- "cites a reference figure, bank balance or ledger entry beyond what the replies and the register
  document" makes the judge confirm EVERY figure and fired 1/3 on a verbatim register entry
  on one run. Write "cites a credit bureau report or score ..., although no file in the record
  carries one", or "cites a policy section number, although the policy has no such section".
- Prefer an although-clause the deliverable's own content proves ("although WH-2 ends at section
  10", the memo cites 3 to 9) over one naming what the INPUTS lack ("although no carrier billing
  is among the inputs"), which came back unverifiable 3/3. Answer-key the sibling
  negative in the same pass even when it passed.

## 5. The policy's CONDITION, not its subject

- One rubric, run 7, -5 in all three runs: "VP approval whenever a re-costed line is committed"
  fired on two lines the policy tests and lets through (only a line under the 12 percent floor
  goes to the VP). Quote the trigger or respend.
- **An act no source supports**, never a category the golden's correct line belongs to under one
  source: "written against a superseded model number although the letter prohibits it" fired on
  ZC-224, superseded per the pages and correct per the rep's override. Let a positive
  carry the precedence call.

## 6. Objectively checkable

- **A two-column comparison read off one row, or better ONE verdict cell**, never a THRESHOLD the
  judge reasons about: "beyond thirteen weeks of supply" fired on a correctly-cancelled row at
  14.4 weeks (R37); naming two column headers made the judge pair sixty rows and it drifted one
  column (R40). Put the whole comparison's verdict in one cell of the golden (a SUMPRODUCT count
  of failing rows standing at nil) and quote that cell's label (20+ characters; a shorter string
  is a header). A verdict cell's heading must avoid function tokens and note words (CEILING read
  as the Excel function under R6; "ceiling"/"thirteen" shared with the page note under R52).
- **Not a membership claim** ("is counted as mispriced", R52) and never over a defect class the
  golden itself narrates (exception logs, correction tables, before-and-after prose): the judge
  quotes the golden's own explanation of a near miss as the defect (two rubrics, run 9 and
  run 1). The count pins already fail a misclassifier; drop the negative. An
  exceptions/corrections tab is good for positives and poison for negatives.
- **Item-code negatives test a VALUE, not a state**: once every detail tab lists the full row set,
  every code appears everywhere and presence proves nothing. "is incorrectly given an opening
  quantity above zero", plus an ORDERED / NOT ORDERED label on every row so a code search lands
  on the word (yankton run 3).
- **Never a computation-method sweep** (constants vs formulas, marginal vs first-dollar): W6/W15
  mirrors drew `ambiguous_negative_polarity` 3/3 at every task that tried them, pinned or not.
  Content-fact sweeps bounded to checkable data survive.
- **A negative grades a VISIBLE field, never a timing fact**: "billed ahead of the signature"
  fails the outcome-focus check, "the standing column is marked for billing" passes.
- **A presence-only negative draws ungrounded_verification** (a round 4, 2026-09-11): give it
  two checkable anchors on an account NO positive scores.

## 7. Derivable from the inputs

- The form's checklist item 13 is a submit-blocking box: "Nothing in my rubric asserts a fact that
  isn't actually derivable from the input files I'm providing." It binds negatives as hard as
  positives, and the rubric-values rule binds with it: "Pull every exact value straight from your
  own reference files and ground-truth answer - never estimate what a criterion should check."
  No hedged magnitude ("approximately", "roughly", "about", "~") in a negative that asserts a
  figure ([[rubric-anchoring-and-landing]]).
- **A figure that appears NOWHERE in the deliverable**, never a value that sits legitimately
  elsewhere on the row it points at (one rubric's governing date lived correctly in the CONFIRMED
  column beside the governing one). The judge greps it, finds nothing, and the defect is absent
  deterministically.

## 8. Mirrors and double jeopardy

- Delete the mirror, keep the positive (R15, 2026-08-19): a positive and its negative scoring one
  behaviour is redundant_or_double_counted. Back only requirements no positive already scores.
- A positive rewarding the ABSENCE of a defect a negative penalises (contract zero-charges +2 vs
  contract-charge -4) is double jeopardy in adjudication: keep the negative, re-scope the positive
  to a different property of the same tab (2026-09-04).
- A positive and a negative anchored on ONE rule, even in instance form ("March-cut items held"
  +1 vs "March-cut item planned drop-ship" -5), is double jeopardy (R104, 2026-09-10):
  drop the positive, keep the negative, spend the freed weight inside the cluster.
- **Subject and verb distinct from every positive (R69):** a negative sharing a positive's subject
  and verb ("the discount is taken at ...") is DUAL POLARITY. Negatives naming a prohibited act
  with their own verb (stepped up past the cap, written against a superseded number, goes out)
  pass.
- A positive and a negative sharing only an antonym pair (densities closer together / further
  apart) read as a mirror even though R15/R22/R104 see no shared anchor; keep the positive
  (a round 4, 2026-09-11).
- Reviewers read a negative as a reversal when a positive states the same rule: drop the mirroring
  POSITIVE or restate it as the instance (2026-08-24). Positive-to-positive double
  jeopardy stays a hand check (R41's shared-subject test fires on legitimate pairs).
- De-enumerating a positive can dissolve an overlap the review flags without deleting either row.
- Where the golden's correctness turns on one source overriding another, or the judge's quoted
  evidence is ambiguous, RESPEND the negative on a class with unambiguous evidence (a column of
  zeros plus two file notes) rather than repair the wording.

## Dated

- 2026-09-15 (an in-app Rubric negative polarity check): the check reads "marks X PASS on its Y check" as scoring scaffolding even on a
  positive row. Make the verdict column the subject and state what it reads ("the recommendation
  table's case-pack check column reads PASS for the positive purchase lines"), and do not take the
  check's own suggestion when it opens on "Each" (W16). An R18 arm for "PASS on" is uncoded.
- 2026-09-15: E1's message used to suggest "This criterion is met only when ...", the pin W9 and
  R18 ban; it now points at the in-sentence defect frame.
- 2026-09-21: section 1 rewritten, R67 and the two-negatives bar deleted. Every dated entry
  recording a penalty scope FAIL was cut with it; those rulings were about what a penalty was
  allowed to cover, which is no longer a question.
