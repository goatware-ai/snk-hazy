# Reviewer Workflow (orientation)

> **Inherited from the Geranium desk, not confirmed for Hazy.** This document describes
> the reviewer workflow. Hazy offers no review assignments: `stb reviews list` and
> `stb adjudications list` both return "no available task" for this project. It is kept for reference and was NOT updated in the 2026-09-21 port; treat
> anything it says about sector, rubric bands or platform checks as Geranium's, not
> this project's. See `../RULE-DELTAS.md`.

A review is this desk's gate on another contributor's task before it enters the Hazy
dataset: one submission, read in full, ending in a decision (Accept, Needs Revision, Reject),
one or more error categories, a note the contributor can act on, and a time figure. Assigned
sector: **Wholesale Trade**.

**The procedure is `prompts/review.md`.** It is the one description of the steps, the decision
rules and the note standard; `/review-task <review-id>` loads it and runs it in one pass,
pinned to Opus. Nothing here restates it.

## Where the rules live

`platform/` holds the live captures, and they win on any conflict with anything else in the repo:

| Capture | What it settles |
| --- | --- |
| `platform/reviewer-guidelines-v5.1.md` | what a reviewer must check and may fix |
| `platform/reviewer-rubric.md` | how LLM tells convert to a verdict |
| `platform/feedback-best-practices.md` | the note standard as the Hub wrote it |
| `platform/platform-review-form.md` | the fields the review form takes |
| `platform/task-example-omnichannel-routing.md` | the Hub's own finished golden |

House additions on top of the captures (no platform edits, the form-only worksheet, the
note shape and its 25-sentence ceiling, the harness tiers) are stated once in
`prompts/review.md`. Check ids it cites are listed in `docs/rules.md`.

## Where the work lands

- `reviews/<review-id>/`: the fetched JSON, both zips unrenamed, the harness's staged
  `_task/`, and `worksheet.md` holding only the form data. Gitignored: the files are another
  contributor's, marked Not for Distribution.
- `reviews-list.md` (repo root): one row per review, so a task coming back under a new Task UID
  is recognised as this desk's own send-back returning.

## Tools

- `tools/fetch_review.py <review-id>`: stages the JSON and both zips.
- `tools/review_check.py reviews/<review-id>`: the evidence harness, run before the read; it
  prints [BAR], [HOUSE] and [CONTEXT] tiers, and only [BAR] can justify a send-back.
- `tools/review_check.py --lint-note reviews/<review-id>`: the note linter, cleared before
  hand-over.

Submitting (`stb reviews accept` / `revise` / `skip`) is the operator's step, after reading the
worksheet.
