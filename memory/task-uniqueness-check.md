---
name: task-uniqueness-check
description: "The platform's prompt uniqueness gate: five design dimensions diffed against the contributor's prior tasks on EVERY submission (a resubmission can fail against a sibling accepted meanwhile), the spent reasoning paths and burned house devices as of 2026-09-05 after eleven failures (02, 20, 25, 21, 31, 31, 28, 27, 32, 47, 49, 50), the dimension-2 sentence test before building, U1/U2, and the sector uniqueness map pointer"
metadata:
  type: project
---

The platform compares each submission against the contributor's existing work and FAILs it when
the core design tracks a prior task, whatever the companies, numbers and files. It is re-run on
EVERY submission against the comparison set as it stands that day, so a task that cleared at
first submission can fail a later round against a batch sibling accepted meanwhile (27 against
24, 32 after 22 siblings were accepted). The eleven failures are narrated in
docs/reference/reviewer-feedback-corpus.md Part 5; the reviewer-side flag "Suspected Duplicate or
Template" exists as well ([[platform-expertdocs]]).

## The five dimensions (checker's own taxonomy, marquette vs task 04, 2026-08-18)

1. **Framing scenario**: the premise and its urgency.
2. **Central task / reasoning path**: e.g. "invoice-level reconciliation building to a
   clause-supported dollar claim".
3. **Distinctive constraints**: e.g. "net in amounts favoring the vendor".
4. **Input kit in kind and role**: e.g. "program letter + AP register + invoice line extract".
5. **Deliverable spec**: e.g. "single named live-formula workbook with a five-minute front
   briefing tab".

All five must differ from every prior task; the checker matches DESIGN, so surface rewording
cannot reach it (the U2 marker fix cleared originality_check while the platform still failed 28).

## Before building: the sentence tests

- Write the candidate's dimension-2 sentence with the mechanism stripped out ("what does the
  deliverable DO with the records") and test it against the spent paths below BEFORE the
  workbook exists. A fresh occupation and a fresh physical subject do NOT clear a spent path (50).
- Test the input kit and the deliverable shape as their own dimensions: they are the most
  collided things in the portfolio (measured 2026-08-26 across 39 prompts: live formulas 29,
  a boss's ground-rules memo 31, a front page up front 21, a policy doc at a dated revision 20,
  vendor letters plus rep emails 18, a year of history 18). A new task should break the
  deliverable template (something other than one live-formula workbook with a meeting front page
  and a vendor-ask section).
- Diff WITHIN a draft batch on the five dimensions before submitting any of them; batch-built
  siblings that individually pass can kill each other's later rounds, and the longest-queued
  revision goes back first when siblings share a design.
- A second task on an occupation that already holds one in the comparison set is high risk when
  it shares the scenario's physical subject or desk (47 shared the credit desk with 40, 49 shared
  lift trucks with 45); the drafts that went to occupations with zero or one prior task are the
  ones to submit.
- Check `docs/submission/platform/wholesale-trade-uniqueness-map.md` first: the platform's own
  per-occupation accepted-task counts, fresh-idea lists and the 27 ask categories. The 13-1022
  crowding is largely this portfolio and roughly 10 of its 16 "fresh" buyer ideas are spent here;
  pick concepts as an ask-category x occupation CELL, steering to thin occupations (Supply Chain
  Managers, Order Clerks, Logistics Analysts, Logisticians) and near-empty categories
  (optimization under constraint, verification, evidence synthesis, root cause, gap/feasibility,
  data-quality reconciliation, audit/controls). Steering tables: docs/submission/workflows/01-ideation.md.
- Diff against `archived/{seq}-{name}/prompt.md` for every retired or rejected task (kept for
  diffing ONLY, never as a design reference) and against every prompt in submission-list.md.

## Spent paths and burned devices (as of 2026-09-05)

- "An event lands, size the buy item by item, write the order against a limit" (03, 10, 12, 14,
  16, 17, 19; vosberg 20 and lima 31 failed on it, compliance dressing included).
- "Adjudicate a counterparty's claim line by line from records and clauses into one settlement
  figure before a meeting", in BOTH directions (04, 13, 20; havlicek 25 as the mirror; scale-house
  50 as "our record vs theirs, then a claim"); 53's carrier claim audit carries the same risk.
- "Reconcile a count against the book, explain the variance, hand the controller the entries
  before the close" (18; pack-factor 31; returns-cage 31 rejected on the neighbouring path).
- "Re-test a system's or a counterparty's decisions line by line against a written rule, code
  the misses by cause, cost them" is crowded (23, 43, 47 retired, 53 draft); a new use needs a
  genuinely different mechanism.
- Agreement-year measurement and renewal schedule (27 retired against 24's negotiation package);
  the credit-desk scenario under 43-4041 (40 accepted, 47 retired); lift trucks, forklift
  operators and the warehouse safety program under 11-3071 (45, 49 retired).
- Burned house devices the checker quotes: "the rep's emailed answer overrides the printed
  letter" (13/39 prompts, "a distinctive rule reproduced almost verbatim"), "the 4/26 revision"
  of an internal policy (6/39), "branch managers on a call" (10/39), the weekday-dated crisis
  letter with a hard deadline, the folder-of-files manifest ("their paper and ours"), the
  live-formulas-because-he-will-call-back rationale, the front-page-first-with-recommendation
  close, and the P4 docstring persona sentence itself ("I do the buying at X, a plumbing and
  heating wholesaler"): a P4 repair can CREATE a collision when siblings get the same sentence
  shape, so each prompt gets its own role sentence ([[prompt-overspecification-giveaways]]). Also
  avoid the signature phrasings ("poke at the cells", "readable in five minutes", "anything we
  owe back the other way").
- Paths that have passed: a forensic audit of our own file (23), a negotiation package (24), a
  re-costing of half a year of orders against a counterfactual calendar (37), a supplier's
  Chapter 11 exposure workup (32, a furniture match rather than a design identity).

## When a FAIL arrives

- First move on a resubmission FAIL: a platform flag (original clearance predates the sibling's
  acceptance, same contributor both sides), before any redesign or retirement.
- Whether prompt-level device REMOVAL (pointing the solver at the memo that carries the
  precedence rule and the live-formula demand, better task design anyway) clears a design-level
  collision is still unproven: 27 was retired before its rewrite was tested, 32's de-templated
  resubmission is the open test.
- Retirement passes the UID to a fresh task (20 vosberg -> rademacher, 27 -> 41) and keeps the
  prompt and log in `archived/` for diffing ([[submission-tracking]]).

**Coded:** `originality_check` section 1 (U1 n-gram overlap, U2 signature-move reuse, ERROR at 4+
reused moves) runs on the folder being built, by name ([[review-scope-single-task]]); U1/U2
measure wording and authored moves, the platform matches design, so a clean U1/U2 is not
clearance. Package-level provenance tells are G2a-G2d in [[package-hygiene-pipeline]].

- **2026-09-17 (hollenbach-allocation-plan 9266b8e2 RETIRED): a design-level uniqueness FAIL on an ACCEPTED task ends it.** Operator retired it rather than redesign all five dimensions on the same UID, and brought draft 53 detention-claim-audit forward in its place. The UID DID pass: the operator submitted 53 on 12's form the same day (the 20 vosberg -> rademacher shape), so the line below stands; what does not pass is the seq, 53 kept its draft number and 12 stays in archived/ with no list row (like 05).
- **2026-09-14 (hollenbach-allocation-plan 9266b8e2): lexical rewording does NOT clear a design-level FAIL.** A re-entered prompt failed; four sentences at 0.55-0.80 difflib similarity were rewritten to worst 0.50 with every device kept in new words, and it failed AGAIN with the checker quoting all five dimensions (scenario, reasoning path, constraints, deliverable, input kit) and the burned devices by function, not wording. The match partner, by elimination, was the task's OWN accepted copy: no other prompt in the repo scores on the profile and every input role it lists maps 1:1 onto this task's files. On a re-entry FAIL read the checker's text first; if it names design dimensions, the fork is platform flag, full redesign or retirement, never rewording.
- **2026-09-11 (pick-module-reslot, PR7):** the in-app prompt uniqueness check failed a RE-ENTERED prompt whose only opening change was the stock P6 sentence ('you have a few years of X behind you ... which is why this is coming to you', in sixteen prompts, near-verbatim to frankfort). Write the P4c experience sentence fresh per task; the platform's read is sentence similarity across the contributor's prompts, not the five design dimensions alone.
