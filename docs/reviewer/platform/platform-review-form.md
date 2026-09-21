# Platform Review Form — field-by-field reference

> **Inherited from the Geranium desk, not confirmed for Hazy.** This document describes
> Geranium's reviewer rules. Hazy offers no review assignments. It is kept for reference and was NOT updated in the 2026-09-21 port; treat
> anything it says about sector, rubric bands or platform checks as Geranium's, not
> this project's. See `../../RULE-DELTAS.md`.

> Captured from the live review UI (August 2026 screenshot). This is the exact shape of
> what you submit at the end of a review. Where this page adds detail the reviewer
> guidelines do not state, this page wins — it reflects the running form.

The review UI shows the task read-only in sections 1 to 3 (prompt, input files, golden
solution and rubric). Everything you enter is in **Section 4**.

## Section 4 — Review

| Field | Control | Rule |
| --- | --- | --- |
| Decision | Radio, one of **Accept** / **Reject** / **Needs Revision** | Decide before you edit anything |
| Error categories | Multi-select, the nine values below | At least one; six is the practical ceiling |
| Notes | Free text | **Required on all three decisions**, Accept included |
| How long did this review take? | Minutes | Entered for payment and verifiable against the work |

## The nine categories

Six are error classes and map one-to-one onto the guidelines' send-back labels:

| Category | Fires on |
| --- | --- |
| `Prompt Quality` | Voice, missing expert context, unnamed files, too easy, answerable without the inputs |
| `Input File Quality` | Thin, irrelevant, malformed, or hard-coded where it should compute |
| `LLM-Generated: Input Files` | Fabricated feel, generic names, round numbers, generator strings in docProps |
| `LLM-Generated: Golden Solution` | Unedited model output, generic headers, hedged prose |
| `Golden Solution Quality` | Fails a criterion, contradicts the inputs, not presentation ready |
| `Rubric Quality` | Atomicity, unbounded wording, weight caps, missing negatives, missing file-name criterion |

Three are not error classes:

| Category | Rule |
| --- | --- |
| `Suspected duplicate or template` | Scenario or structure reused from a prior task. May sit **alongside an Accept** when the task is otherwise fine |
| `No Issues - Recommend EC as Reviewer` | Exceptional across all four components. **Accept only** |
| `Adjudication Ready` | No errors, but not exceptional. **Accept only** |

Select the classes matching corrections **you made yourself**, too — the category set
records what was wrong with the task as submitted, not what remains after your edits.

## Notes field

Three parts, no exceptions: *what is wrong* (name the exact criterion number, row, cell
or file), *why it is wrong* (one sentence), *what to do about it* (a concrete path to
acceptance). Two short paragraphs is the ceiling.

Match the note to the decision:

- **Needs Revision** — every blocker in one pass. The EC has two attempts; surfacing one
  problem now and another next round burns one of them for nothing.
- **Reject** — state the reason plainly, and do not imply a revision path that no longer
  exists.
- **Accept** — say what you fixed, so the EC can see it.

The note must be yours, in your own words, from your own review. See
`feedback-best-practices.md`.
