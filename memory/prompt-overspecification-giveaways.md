---
name: prompt-overspecification-giveaways
description: "Prompt send-back patterns: rule P4 (opening ~900 chars carries state/country, what the requester does, the reader's purchasing experience, never a persona; one task rejected on this alone 2026-09-02), P5 (no file-purpose glosses beyond one or two unclear distinctions; the id was P2 until 2026-09-04), no deliverable outlines, pitfall warnings or derived parameters; coded in autoeval_check.py"
metadata:
  type: feedback
---

Feedback on one submitted prompt (received 2026-08-17): the prompt was sent back as over-specified — "rewrite it as a plain handoff." Four giveaway patterns were flagged:

1. **Purpose hints on input files** — "you'll want that one when you decide which of the big hits are real demand" tells the solver how a file enters the analysis. Name the file and its contents only.
2. **Outlining a deliverable component's sections** — the front-tab briefing outline (commitments/approvals/exposures) had to go; component + audience is enough.
3. **Data-pitfall warnings** — "the movement file has plenty that isn't demand" and "the stretch looks nothing like our average month" gave away rubric-graded reasoning.
4. **Derived parameters stated as givens** — "to carry us to the first Searcy receipts" handed over the coverage horizon the solver should compute.

Also structural: file names belong woven into the opening narrative, not in a separate "system pulls" paragraph.

Third confirmation — an earlier rejected build: the reviewer cut the disposition-option enumeration (returns/transfers/clearance/scrap — "hands over the disposition order the policy file should teach") and the cap-math detail line ("tips off that a cap binds"). Also required ALL input file names in the opening paragraph — a separate "system pulls" paragraph is not acceptable even when every file is named. Notably this reviewer left the front-tab briefing outline and the two data warnings intact, so those are not universally cut — apply reviewer feedback as given rather than pre-emptively stripping them.

Confirmed on a second task (2026-08-17): the reviewer cut the briefing-tab section list (pattern 2 — "the shape of the golden solution handed over in the prompt") and the "sixty-day window" stated outright (pattern 4 — a deadline an input file carries must be worked out, not read off the prompt; reviewer: "let the agreement carry that"). Fix wording accepted: "a briefing tab she can read in five minutes and defend when Gene questions it."

**Why:** Reviewers grade whether difficulty lives in the input files and cross-file reasoning; any prompt line that pre-solves a graded step is a send-back, echoing the "Overspecification kills difficulty" rule in docs/submission/workflows/02-prompt-writing.md (I added these concrete patterns to that section).

**How to apply:** Before submitting any prompt, sweep it for these four patterns: strip purpose clauses from file mentions, deliverable-section outlines, pitfall warnings, and computed horizons/cutoffs/scopes stated as facts. Keep: all input file names, the single output file name, hard scenario facts, scope items, and process rules (live formulas, source-precedence like "believe the rep"). See also [[rubric-anchoring-and-landing]].


**The platform now scores pattern 1 mechanically (a Prompt human voice check, 2026-08-31).** A prompt the check itself called "notably natural" FAILed because ten of ten input files carried an individual gloss ("Janet's memo from June 3 is pricing_memo_0603.docx", "the item file with both costs on it (item_file_extract_0819.xlsx)"); the ruling names glossing most or all files a STRONG structural tell that overrides the voice. Passing shape: one natural run naming every file, then a sentence or two for the one or two distinctions the names do not carry (a revision date, which of two costs a file holds), and any people-and-thread narrative kept as narrative rather than pinned to a filename. Coded as **P5** in tools/gcheck/prompt_inputs/prompt_frame.py (P2 until the 2026-09-04 split; P2 now means the prompt names no input source) (three or more files named, half or more in the "X is <file>" / "<file> is|holds|carries" / "X (<file>)" forms), proven 10-of-10 on the failed paragraph and silent on the rewrite; 11 other prompts in the catalog carry the habit.

## The prompt must frame the US setting and the reader's role (2026-09-02, a REJECTION)

**One task was rejected on prompt quality alone**, after eight AutoEval rounds and
five reviews: "The task itself, input files, golden solution, and rubric are otherwise strong,
but the prompt does not explicitly establish that the work is U.S.-based and does not clearly
frame the analyst's professional role or assumed purchasing expertise level. Add a brief opening
that identifies the requester/analyst as U.S.-based and states the expected procurement or
purchasing experience."

Both halves came from the guidelines of the desk this repo was built from and neither was being
written: a workflow "in the United States", and no job outside the US. **This desk's guidelines
PDF and form say neither (checked 2026-09-21)**, so the US-setting half is carried over and not
confirmed here; the role and expertise half survives on its own, because the form requires "a named role, organization, and a
reason this work is happening today" (checklist item 1). A sweep found **15 of 16 in-flight prompts missing at
least one half, 6 missing both** - this was a portfolio-wide authoring habit, not one task's slip.

The two halves, and what does NOT satisfy them:

- **US setting.** Name the state ("a wholesaler in north central Illinois"). Town names alone do
  not carry it; a reviewer is not required to know where Kewanee is. Hazy states no such rule,
  so treat this as cheap insurance rather than a gate.
- **Role and expertise.** Say what the requester does and what the reader is expected to already
  know ("I buy the mechanical line ... whoever picks this up should have a few years of
  purchasing behind them"). **"my desk" does not count** - the rejected prompt carried it and the
  reviewer still found no role framed, which is why the coded detector rejects that form.

Write both in the requester's own voice. The guidelines' own banned example is the opposite
shape, "You are a financial analyst. Utilizing your expertise ...", so this is a plain opening
sentence or two, never a persona instruction. It pairs with P5 (do not gloss the input files)
and PRE-SOURCES (name at least one real source), so the opening carries the person and the place
while the file names stay bare.

**The rule's name is P4 ("prompt frame"), and it has four parts** - quote the code in any
session and the whole rule comes back:

- **P4a** the place: the state named, or the country said plainly.
- **P4b** the role: what the requester does ("my desk" does not count).
- **P4c** the expertise: what the reader is expected to already know, in the terms of the task's
  own occupation (purchasing on a buying task, dosing on a clinical one; the wording is the
  occupation's, not one trade's).
- **P4d** not a persona: never "You are a ... Utilizing your expertise", the guidelines' own
  banned example.

All three of a/b/c must land in the OPENING - the first whole paragraphs making up ~900
characters - because the reviewer asked for "a brief opening"; a state named four paragraphs
down frames nothing.

Coded as **P4** in `tools/gcheck/prompt_inputs/prompt_frame.py` (`check_prompt_role_and_locale`, run by autoeval_check.py), family
PRE-PROMPT in `tools/gate_families.py`, and written into the two files a fresh session reads
before authoring: `prompts/submission.md` (hard constraints) and
`docs/submission/workflows/02-prompt-writing.md` ("The opener" plus its final screen). Proven
to fire on all three parts of the rejected prompt and to go silent once the model opening is
prepended; a sweep on 2026-09-02 had all 27 prompts in the repo missing at least one part.

Check-writing trap found while tightening it: a case-INSENSITIVE `\bUS\b` matches the pronoun
"us", so the first cut passed prompts that never mentioned the country ("the bills start
running out on us"). The country test is case-sensitive; a state name only counts behind a
locational cue ("in ... Illinois", "Kewanee, Illinois") so a surname does not satisfy it; and
a bare "should have" is not an expertise clause ("the claim should have been filed").

## The P4 frame must not be a self-introduction to a coworker (rule P6, a REJECTION, 2026-09-05)

**A task was rejected at its first human review** on the paragraph that
satisfied P4 the literal way. It opened by naming the speaker's employer, the trade that
employer is in and the town it sits in, then gated the reader ("whoever picks this up should
have a few years behind them") - all addressed to a colleague at that same company. The note
back: "Why would you say this
to someone who works with you at the same company? They are your coworker. They know what the
company is and what you do... Remove the entire first paragraph which contains no useful info and
sounds LLM generated. If that info is needed for the LLM then include it, naturally, in the
conversation prompt."

Both rejections stand, so P4 and P6 hold together: the state rides on a place the work touches
("the pipe yard here in Chattanooga, Tennessee"), the role is ownership of the problem ("the
trucks are mine to settle"), the experience is the reason for the handoff addressed to the reader
("you have a few years of distribution operations behind you, so the schedules will not need
walking through"), and every event the opening names says in the same sentence why it matters to
the work (the reviewer asked what "Tamika's work schedule has to do with a new equipment
proposal"). Coded **P6** beside P4 in `tools/gcheck/prompt_inputs/prompt_frame.py`: the
"I <run> <thing> for <Company>, a <trade> <business> in <Town>, <State>" sentence and the
"whoever picks this up should" gate each fire; P4c now also accepts the woven "you have ... years
... behind you" form. The first sweep fired on 22 of 24 prompts in submissions/ and drafts/,
because every prompt had been rewritten to the old P4 example, which itself carried the gate
("whoever picks this up should have a few years of purchasing behind them") - that example is
replaced in `docs/submission/workflows/02-prompt-writing.md`. See [[first-round-rejection-lessons]].
- 2026-09-15 (a leakage round): an input footnote stating the finding the prompt asks for ("Freight calculated on gross order value per the standard freight policy") is an ANSWER_LEAKED verdict. Remove it and leave the finding in the figures. When the figures then derive the finding only to within a rounding slip ($659.14 against 3.2 percent of list, $659.13), correct the input so the arithmetic ties exactly. Also P4b matches only a fixed role grammar: "I'm a <role>" or "I buy/run/handle the|our|a ...". "I sell for <company>" and "I handle contractor accounts" both fail.
- 2026-09-15 (a rejection, coded P8): a prompt due date and the golden's Date line sit at least 21 days after the build (first commit of instruction.md), or the prompt gives no due date; a September 8 deadline on a September 1 build read as an impossible timeline at review.
- 2026-09-16 (an adjudication round 2): a competitor quote built on the requester's own price list is ANSWER_LEAKED. It carries the requester's unit prices, list, discount and net, which the rubric grades the solver to derive, and site-tagged subtotals leak the allocations too. Give every third-party document its own prices and re-derive every comparison figure (verify_golden.py asserts the competitor's freight basis).
