---
name: rubric-negatives
description: "Every rule for a negatively weighted criterion: R67's four critical classes (safety, privacy, inverted top-level decision, INVENTED fabrication) and what is never critical, the two-negatives bar with R61 non-blocking, the in-sentence defect frame (E1/W18/R84, 'although <source> documents no X'), single negation (R53), closed class not open scope (R77), condition not subject, threshold vs verdict cell (R37/R40), no membership or narrated-defect negatives (R52), mirrors and double jeopardy (R15/R69/R104) (to 2026-09-10)"
metadata:
  type: feedback
---

Open before writing or respending any negative. Siblings: [[rubric-liveness-criteria]],
[[rubric-anchoring-and-landing]], [[rubric-coverage-and-completeness]], [[rubric-criterion-count]].
Narratives: docs/reference/reviewer-feedback-corpus.md Part 5 (tasks 07, 08, 12, 15, 16, 18, 23,
37, 39, 40, 41, 44, 35).

## 1. What a penalty may be spent on (R67, since 2026-08-27)

- The platform's Rubric penalty scope check reserves negative weight for CRITICAL commissions:
  safety harm, a privacy leak (PII/PHI/CUI or a confidential release), an inverted or prohibited
  TOP-LEVEL decision (release/hold, fund/deny, approve/defer, legally ineligible, a prohibited
  disposition such as "scrapped although the memo sends it to the return list", "planned although
  the March cut disqualified it"), or FABRICATION. Everything else (a cadence past a ceiling, a
  bracket credit below its floor, a wrong denominator, a miscalculation, a wrong causal
  conclusion) is an ordinary miss and belongs to an affirmative positive. R67 is an ALLOWLIST
  because the rejected class has no vocabulary of its own.
- Fabrication means something INVENTED: a credit, a cost, a citation, a benefit the documents do
  not grant. An internal contradiction is NOT fabrication (the check reversed itself one round
  later on inbound-consolidation: "a contradicted total is a wrong calculation / consistency
  problem"), and "contrary to the dock log and unsupported by it" does not convert an analytical
  error into fabrication (dock-to-stock). R67's allowlist dropped contradicts / inconsistent /
  disagrees, and weak fabrication forms with a computed-quantity SUBJECT ("beyond what ...
  support" on a tier calculation) are non-critical.
- The token list is literal: "policy 2.3 bars" does not match, "prohibits" does; safety needs
  hazardous / unsafe / safety / certifi / licens / lift. A MEMO rubric that writes "The memo
  concludes / finds / attributes ..." hides the signature, so R67 fails any negative whose main
  verb is a conclusion verb with no strong critical token.
- Write the fabrication CLASS into the sentence, not just the frame word: "booked for a vendor
  whose printed terms document no bracket, in violation of the March letter that grants the one
  percent to Kesselring alone" passed twice verbatim ("an invented benefit").
- The binding bar is at least two negatives, each -3 to -5, inside the classes. R61's 20 percent
  penalty share is NON-BLOCKING by team manager ruling (2026-09-02): a recommendation printed
  through `recommend()`, never a send-back in either direction. Build two fabrication negatives
  from the start on different invented things (a credit not granted, a cost at a rate no terms
  carry) when the task supports them; cutting the positive denominator raises the share for free.
- A reviewer's suggested negatives can be platform-banned (movement contradictions, per-line fee
  misses): honour the intent with the critical classes the task supports and say so in the log.
  Never paste the penalty scope check's suggested positive rewrite; it restates a figure another
  row scores (subsumption) and re-adds liveness wording R17 caps. Where the read-through and the
  figure are already scored, DROP the row and spend its weight on a legal negative.

- A per-record QUALIFICATION call is QA, not a decision (rossville Refinery pre-submission,
  2026-09-11): "at least one line is incorrectly shown as qualifying on the strength of the item
  file's origin field" FAILed the penalty scope check as an ordinary misclassification while the
  split-line (prohibits) and premium-to-the-contractor (approval) negatives passed. "qualif" only
  counts when the subject is the deliverable's verdict; coded as R67's fourth arm. Drop such a
  negative, the count and basis positives already fail the solver.

## 2. The frame

- One sentence, at most 45 words (R55), with the defect frame INSIDE it: incorrectly / violating /
  in violation of / contradicts / contrary to / although / even though / despite / wrongly /
  beyond what (E1's PIN_RE, W18's frame words). A negative with no frame word in the defect
  sentence reads as "what a correct deliverable does" to the Rubric Quality Review (task 20,
  -16 exposure).
- The carve-out sentence ("... is not this defect") is DEAD (platform negative polarity check,
  tessendorf 2026-08-26, R18): it reads as scoring scaffolding, the same as "does not count as
  this error". Any scope boundary that truly needs stating becomes an affirmative fact. Every
  pre-2026-08-26 rubric carried it; a rubric reopened for other reasons re-gates its negatives on
  first contact. The human reviewer's rewrite shape carries the boundary inside the defect
  ("open quantity due that CAUSES its post-plan position to exceed thirteen weeks").
- No trailing ", in violation of ... / contrary to ..." clause (R84, reviewer send-back
  2026-09-02: "remove trailing clauses that bring negatively weighted items into negative
  language"). State the act once and carry the frame as the act's condition: "... although
  <source> documents no <thing>", which E1, W18, R67 and the reviewer all accept. An R84 rewrite
  must keep the R67 critical token inside the act clause ("places hazardous stock in a floor bin
  ... although the item master carries the item with a hazmat class") or R67 fires next.
- ONE negation per criterion (R53): "not / never / no / without / rather than / instead of /
  fails to" twice and the judge cannot tell which way it points (oskaloosa: the identical frame
  passed on the row that spent its single negation on the carve-out). State the defect
  positively ("trimmed in quantity", "stock beyond what the records carry").
- The judge grades each criterion as a true/false statement, so a bare plural negation of a
  nearby positive ("Key outputs are constants") draws `ambiguous_negative_polarity` 3/3. The
  any-quantifier subject ("At least one ...") or the verdict-cell form ("The workbook's count of
  <verdict cell label> stands above zero, at least one ...") reads cleanly. The old meet-pin
  style ("met only when ...; X does not meet it") was retired 2026-08-19 as inverted polarity.
- Defect frames other than "incorrectly" pass E1/W18 when a reviewer objects to the adverb.
- A negative grades a VISIBLE workbook field, never a timing fact: "billed ahead of the
  signature" fails the outcome-focus check, "the standing column is marked for billing" passes.
- Negatives are exempt from R49 (they must name the class members they fire on) and carry the
  same R82 currency notation as positives.
- The although-frame alone can still be read backwards (packaging-consolidation Rubric Quality Review,
  2026-09-11, two [critical] misaligned_or_unjustified_rigidity): "approves an award of one category to
  one bidder and another to the other" and "cites a tier price for an item that neither schedule lists"
  were both read as describing a compliant workbook. Name the defect class inside the act clause ("an
  award that splits the consolidated categories", "an invented price") and keep the frame. Not coded:
  every house negative passes the probe, the misread was the two sentences' shape.

## 3. What the object must be

- **A CLOSED class the golden plainly lacks** (R77), never an open scope: "cites a reference
  figure, bank balance or ledger entry beyond what the replies and the register document" makes
  the judge confirm EVERY figure and fired 1/3 on a verbatim register entry (wanasek). Write
  "cites a credit bureau report or score ..., although no file in the record carries one" or
  "cites a policy section number, although the policy has no such section". Prefer an
  although-clause the deliverable's own content proves ("although WH-2 ends at section 10", the
  memo cites 3 to 9) over one naming what the INPUTS lack ("although no carrier billing is among
  the inputs"), which came back unverifiable 3/3 (dock-to-stock). Answer-key the sibling negative
  in the same pass even when it passed.
- **The policy's CONDITION, not its subject** (hollenbach run 7, -5 in all three runs): "VP
  approval whenever a re-costed line is committed" fired on two lines the policy tests and lets
  through (only a line under the 12 percent floor goes to the VP). Quote the trigger or respend.
- **An act no source supports**, never a category the golden's correct line belongs to under one
  source: "written against a superseded model number although the letter prohibits it" fired on
  ZC-224, superseded per the pages and correct per the rep's override (boettcher). Let a positive
  carry the precedence call.
- **A two-column comparison read off one row, or better ONE verdict cell**, never a THRESHOLD the
  judge reasons about: "beyond thirteen weeks of supply" fired on a correctly-cancelled row at
  14.4 weeks (R37); naming two column headers made the judge pair sixty rows and it drifted one
  column (R40). Put the whole comparison's verdict in one cell of the golden (a SUMPRODUCT count
  of failing rows standing at nil) and quote that cell's label (20+ characters; a shorter string
  is a header). A verdict cell's heading must avoid function tokens and note words (CEILING read
  as the Excel function under R6; "ceiling"/"thirteen" shared with the page note under R52).
- **A figure that appears NOWHERE in the workbook**, never a value that sits legitimately
  elsewhere on the row it points at (task 20's governing date lived correctly in the CONFIRMED
  column beside the governing one). The judge greps it, finds nothing, and the defect is absent
  deterministically.
- **Not a membership claim** ("is counted as mispriced", R52) and never over a defect class the
  golden itself narrates (exception logs, correction tables, before-and-after prose): the judge
  quotes the golden's own explanation of a near miss as the defect (june-price-review run 9,
  open-order run 1). The count pins already fail a misclassifier; drop the negative. An
  exceptions/corrections tab is good for positives and poison for negatives.
- **Item-code negatives test a VALUE, not a state**: once every detail tab lists the full row set,
  every code appears everywhere and presence proves nothing. "is incorrectly given an opening
  quantity above zero", plus an ORDERED / NOT ORDERED label on every row so a code search lands
  on the word (yankton run 3).
- **Never a computation-method sweep** (constants vs formulas, marginal vs first-dollar): W6/W15
  mirrors drew `ambiguous_negative_polarity` 3/3 at every task that tried them, pinned or not, and
  the completeness check's own suggested typed-constant negative is that trap. Content-fact sweeps
  bounded to checkable data survive.
- **Subject and verb distinct from every positive** (R69): a negative with the same subject and
  verb as a positive ("the discount is taken at ...") is DUAL POLARITY. Negatives naming a
  prohibited act with their own verb (stepped up past the cap, written against a superseded
  number, goes out) pass.

## 4. Mirrors and double jeopardy

- Delete the mirror, keep the positive (R15, Agentic Rubric Quality Review 2026-08-19): a positive
  and its negative scoring one behaviour is redundant_or_double_counted. Back only requirements
  no positive already scores. The requirement mapping check may suggest mirrored pairs; it accepts
  non-mirrored dedicated criteria, so keep those.
- A positive rewarding the ABSENCE of a defect a negative penalises (contract zero-charges +2 vs
  contract-charge -4) is double jeopardy in adjudication: keep the negative, re-scope the
  positive to a different property of the same tab (delivery-zone 2026-09-04).
- A positive and a negative anchored on ONE rule, even in instance form ("March-cut items held"
  +1 vs "March-cut item planned drop-ship" -5), is double jeopardy (R104, tessendorf
  2026-09-10): drop the positive, keep the negative, spend the freed weight inside the cluster.
- Reviewers read a negative as a reversal when a positive states the same rule: drop the
  mirroring POSITIVE or restate it as the instance, so negatives sit over defect classes no
  positive asserts (open-order 2026-08-24).
- Positive-to-positive double jeopardy (two rows turning on one HB-1 sourcing decision) stays a
  hand check (R41's shared-subject test fires on legitimate pairs); give ONE criterion the tag.
- De-enumerating a positive can dissolve an overlap the review flags without deleting either row.
- Where the golden's correctness turns on one source overriding another, or the judge's quoted
  evidence is ambiguous, RESPEND the negative on a class with unambiguous evidence (a column of
  zeros plus two file notes) rather than repair the wording.

- 2026-09-11 (hartwell refinement, penalty scope FAIL): a decision verb in the although-clause names the source's act, not the deliverable's, and the platform reads the row as an ordinary calculation miss ("incorrectly reprices … although the vendor deferred that group" FAILed). Put the decision in the deliverable's hands in the defect clause (incorrectly releases / approves / declares eligible) or cite a rule token in the although-clause (prohibits / barred / eligible only for), which the platform has accepted; R67 fifth arm flags the shape.

- 2026-09-11 (inbound-consolidation refinement round 2, Rubric Quality Review critical x2): a negative that OPENS in the passive voice ("Bracket money is incorrectly booked ... although ...") is read as inverted polarity whatever frame word it carries (the same rows drew the same minor on 2026-08-31 in their "in violation of" form). Put the deliverable in the actor's seat with a transitive verb and the R67 token inside the act: "The workbook wrongly books bracket money for a vendor other than Kesselring, inventing a bracket where ..."; "absent from every ..." states the class with no negation (the platform's "not found on any" draws W1). Coded as R111.
- 2026-09-11 (harlow refinement round 4): an invented-figure negative that is presence-only draws
  ungrounded_verification; give it two checkable anchors on an account NO positive scores (a Castor Valley
  draft mirrored the top-row positive under R22/R41) and keep the "invented" token for R67. A positive
  and a negative sharing only an antonym pair (densities closer together / further apart) are a mirror to
  the review even though R15/R22/R104 see no shared anchor; keep the positive.
- 2026-09-12 (recall-response refinement round 2, penalty scope FAIL on re-entry): a record's SCOPE MEMBERSHIP is a classification, not a decision, whatever rule token the although-clause cites. "A lot outside the notice's scope ... is incorrectly carried as in scope, although section 1 prohibits widening the withdrawal" (-4) FAILed as "an ordinary scope/content-classification error" and as dual polarity with the positives pinning the in-scope set (exactly the 12 combinations, plant P2 only, the three items and no other); "prohibits" in the although-clause did not save it. Drop such a negative, the set-and-count positives already fail a widened deliverable. Coded as R67's sixth arm (record subject + classify verb + "in/out of scope"); probed over 121 negatives first, one hit.

- 2026-09-14 (hx4180 fc3c5a5c, penalty scope FAIL): "incorrectly qualifies the trial finishing result as the basis for the pattern column" was ruled an ordinary methodology error although "qualifies" sat in the defect clause; the check judges the substance (which source figure to compute from), not the verb. A basis-selection or input-choice defect can only be penalized as fabrication (an invented figure no source carries) or not at all; release/hold and approve/defer decisions on the same task passed.
- 2026-09-14 (flyer-program-review re-entry, penalty scope FAIL, R67 fifth arm): once R84 strips the "in violation of <source>" tail, a weak fabrication form alone ("documents no", "carries no") is read as "not clearly framed as explicit fabrication" or "an ordinary source-row / coverage / data-validity check"; the deliverable must be the actor and name the invented thing ("The plan books an invented billback ... at a per-unit rate that no deal sheet puts in writing", "The review invents a 2026 slot result for an item the printed history never carried"). Widening R111 to adverb-less passives was probed and reverted (27 hits, mostly the proven "At least one line is ..." shape).
- 2026-09-15 (wholesale-purchasing-recommendation refinement dfa2b2d2, in-app Rubric negative polarity check): the check reads "marks X PASS on its Y check" as scoring scaffolding even on a positive row. Make the verdict column the subject and state what it reads ("the recommendation table's case-pack check column reads PASS for the positive purchase lines"), and do not take the check's own suggestion when it opens on "Each" (W16). An R18 arm for "PASS on" is uncoded because the tooling edit was blocked that session.
- 2026-09-15 (rfq-response refinement 253bad46, in-app Rubric penalty scope check): a negative for a non-conforming bid element ("incorrectly qualifies a priced line as to quantity ... although the tender treats a quantity-qualified bid as non-conforming") is an ordinary bid-content error, even though the tender rejects such a bid; non-conformance is not an inverted top-level decision. Grade it as a positive on the statement the golden makes (accepts the qualifications instructions without exception), and keep negatives to fabrication of a closed record class (an item number, a site reference); a rate or figure class fails R77.
- 2026-09-15: E1's message used to suggest "This criterion is met only when ...", the pin W9 and R18 ban; it now points at the in-sentence defect frame.
