# Rule deltas — Geranium to Hazy

Working document for the 2026-09-21 port. Every rule below changed when this desk moved
from Project Geranium (Wholesale Trade, golden-solution benchmark) to Hazy_Task_Creation.
Authoritative sources are `docs/submission/platform/platform-submission-form.md` (the live
form, which blocks submission) and `docs/submission/platform/create-the-task-guidelines.md`
(the guidelines PDF). **Where they disagree, the form wins.**

Delete this file once every row is applied and the first Hazy submission has come back.

---

## D0. The solution is still required

The guidelines PDF says the creator does not produce a solution. The live form has a
**required** `Completed Task Upload` whose section text says "complete the task yourself
... This is your ground truth and what you will build your rubric off of."

**Applied rule:** the desk builds a golden solution for every task. All Geranium
golden-solution tooling stays. Any doc sentence claiming no solution is produced is wrong
and must be corrected, not deleted, with a pointer to this conflict.

## D1. Sector is gone; domain plus occupation replaces it

| Was | Now |
|---|---|
| One fixed sector, "Wholesale Trade" | One of **14 domains**, chosen per task |
| O*NET occupation free-chosen from onetonline | One of **64 occupations** on a closed platform list |
| 6 occupation codes hardcoded in the gate | Domain and occupation vary per task |

Lists: `docs/submission/platform/domains-and-occupations.md`. Codes:
`docs/submission/platform/onet-codes.md`.

**Applied rule:** no document, prompt, skill or check may assert a single sector. Any
sentence of the form "assigned sector: Wholesale Trade" is deleted, not reworded. Metadata
carries `domain` and `onet_occupation` and the task picks them per task.

Geranium's per-occupation prompt-fit tables (O*NET task-pick matching, the M1-M3 checks)
were built from six Wholesale Trade codes and predict nothing here. They are deleted rather
than ported: a check that cannot fire is indistinguishable from a broken one.

## D2. Rubric criterion count

| Source | Says |
|---|---|
| Geranium (deleted) | minimum 15, maximum 60, aim 15-25 |
| Hazy form | "minimum of 3 criteria; expect somewhere in the 20-60+ range depending on complexity" |
| Hazy form checklist item 9 | "at least 3 criteria, and enough to genuinely cover the task's complexity (most real tasks need well more than 3)" |
| Hazy guidelines PDF | "at least six criteria" / "The rubric has at least six clear criteria" |

**Applied rule:** ERROR below **6** (the PDF's floor, which also satisfies the form's 3).
RECOMMEND below **20** (the bottom of the form's expected range). **No ceiling** — the form
says "20-60+", so a rubric above 60 is not a defect.

## D3. Rubric weights

| Was | Now |
|---|---|
| Integer in +1..+5, or -3..-5 for a negative | Integer in **-5..+5**, zero excluded |

The form states the range twice ("Weight -5 to +5", checklist item 11) with no gap around
-1 and -2.

**Applied rule:** accept any non-zero integer in -5..+5.

## D4. Negative weights are no longer an allowlist

Geranium's R67 reserved negative weight for four critical classes only: safety harm,
privacy leak, an inverted top-level decision, and fabrication. Everything else was a
rejected negative.

The Hazy form says the opposite: "**Use negative weights where useful, to penalize specific
unwanted outcomes** (extra items included that shouldn't be, page limit exceeded, wrong
file type)." All three of its own examples are ordinary quality misses that R67 would have
rejected.

**Applied rule:** R67's allowlist is **deleted**. Negatives may penalise any specific,
observable unwanted outcome. The remaining constraints still hold because they are about
criterion shape, not permission: one thing per line, affirmative phrasing of the defect,
objectively checkable, derivable from the inputs.

## D5. New mandatory closing criterion

The form: "End with a general '**Overall formatting and style of the deliverable**' line
(commonly ~+5)." Checklist item 12 makes it a submit-blocking confirmation.

**Applied rule:** new check. The rubric's **last** row must be a general formatting-and-style
criterion. ERROR when absent; ERROR when present but not last.

## D6. Rubric values come from the ground truth

The form: "Pull every exact value straight from your own reference files and ground-truth
answer — never estimate what a criterion should check." Bad: "approximately $15,000". Good:
"$15,170". Checklist item 13: "Nothing in my rubric asserts a fact that isn't actually
derivable from the input files I'm providing."

**Applied rule:** unchanged in spirit from Geranium's anchoring and landing rules, which
stay. Add a check for hedged magnitudes in a criterion ("approximately", "roughly", "about",
"~") where a figure is asserted.

## D7. Input file count

| Was | Now |
|---|---|
| Large packages, ten-ish inputs typical | **Minimum 2, 3+ strongly preferred** |

Formats now include engineering files (STEP, STL, GERBER) and multimedia alongside the
Office set. Upload is a **single ZIP** whose member names must match the Input File List
exactly.

**Applied rule:** ERROR below 2 inputs, RECOMMEND below 3. No upper bound. Filename
matching between the list, the prompt and the ZIP stays a hard check; the form calls a
mismatch "one of the most common reasons a submission gets sent back".

## D8. Time estimate is five fields, not one

| Was | Now |
|---|---|
| `manual_time_hours`, a single number; AHT tracked nowhere | Four **minute** fields plus a **total in hours** |

The four: read and understand the prompt; open, skim/search and use the reference files;
perform the required work; verification/QA and final review. Total in hours, decimals, and
**at least the sum of the four**, converted.

The form's advisory Difficulty check wants estimated manual effort **over 3 hours**. The
guidelines PDF targets **5-10 hours**.

**Applied rule:** metadata carries all five. Check that the four are integers, that the
total is at least their sum in hours, and that the total is over 3. RECOMMEND when under 5.

## D9. Tools used

New required field, at least one non-AI tool (e.g. Excel, Photoshop, DaVinci, SolidWorks,
LabVIEW).

**Applied rule:** metadata carries a `tools` list, at least one entry.

## D10. The pre-submit checklist is a gate

The form's "Before You Submit — Task Creation Checklist" has 15 boxes and **all must be
checked to submit**. It is reproduced in the form capture.

**Applied rule:** the pre-submission audit ends by walking the checklist, one row per box.

## D11. In-form checks are advisory

The three "Checks (optional)" panels (Task Instruction, Completed Task, Task Rubric) state
"This feedback is advisory and does not submit or block anything." Each section still ends
in **Run Evaluations and Continue**, and the form ends in **Run Evaluations and Submit**, so
evaluations do run at submit time.

**Applied rule:** do not model the optional panels as blocking. Geranium's post-submission
auto-eval and adjudication documents are kept but banner-marked unverified, because nothing
confirms Hazy runs the same ten named checks.

## D12. No reviewer or refinement workflow on Hazy, yet

`stb reviews list` and `stb adjudications list` both return "no available review/
adjudication task" for this project, and there is no Refinery node. Geranium's reviewer and
refinement material is kept and banner-marked rather than deleted, since an assignment may
arrive later.

**Applied rule:** the reviewer and refinement stacks are out of the main path. They are not
updated for Hazy and must not be trusted until an assignment confirms the workflow exists.

## D13. What carries over unchanged

These Geranium rules are domain-agnostic and the Hazy documents restate them, so they stay
as they are:

- No project, eval, rubric, benchmark, golden-solution or AI reference anywhere in a
  shipped file: content, filename, metadata, hidden tabs, speaker notes. (The codename
  canary now screens both "Geranium" and "Hazy".)
- Inputs never contain the answer, a pre-computed result or a conclusion to be derived.
- No unedited AI-generated content; the LLM-tell catalogue still applies.
- Overspecification of HOW is the most common prompt defect.
- Numbers reconcile across files and must not look artificially clean or round.
- Criteria are atomic, affirmative, non-overlapping, objectively verifiable and about the
  final output rather than the process.
- Do not mirror the instruction in the rubric.
- Package hygiene: real Office provenance, no placeholder text, no impossible dates.
