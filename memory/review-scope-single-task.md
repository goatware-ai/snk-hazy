---
name: review-scope-single-task
description: "Originality, authorship and rubric gates run only on the task folder being built or revised, named explicitly, never as a portfolio sweep (user, 2026-08-22); the one carve-out is the mechanical, report-only tools/package_sweep.py on every revision (2026-09-02), fix only the named task"
metadata:
  type: feedback
---

After task 21 was sent back (2026-08-22) I ran the new originality and authorship checks across the
whole catalogue and reported that every task folder failed the forensic gates and that six prompts
reused the signature narrative moves. The user retired task 21 and said: "I don't want you make
this kind of review anymore in other tasks."

**Why:** the finding was solicited for the task under review, not for the back catalogue. Turning
one send-back into a portfolio-wide failure report is unasked-for work that puts every other task
in question at once, including accepted ones, and it is the user's call how and when to raise that
with the team.

**How to apply:** run originality, authorship and rubric gates **on the task folder being built or
revised**, named explicitly. Do not sweep `submissions/*` and do not report verdicts on other tasks
unless asked. `tools/originality_check.py` has had its catalogue-wide mode removed for this reason
and now requires a folder argument. If a check happens to reveal something about another task, note
it once at most and leave it alone. Related: [[package-hygiene-pipeline]].

**Carve-out, 2026-09-02 (user decision): a MECHANICAL sweep runs every revision, report-only.**
`tools/package_sweep.py` scans every task folder for package-level facts about the bytes -
python generator strings in docProps, the absPath Excel stamps into workbook.xml, a synthetic
calcChain real Excel refuses to open, the codename canary - and has no repair mode. The rule
this carves out of is unchanged in substance: what was ruled out is portfolio-wide JUDGMENT
work (originality, authorship, rubric quality), which is expensive, subjective, and drags
unrelated tasks into a revision. A deterministic byte check is neither. Fix only the task named
in the revision; report the rest by name and leave it alone. Wired into step 6 and step 8 of
prompts/revise-task.md. Why it exists: A14 debt sat unpaid on seven tasks for a week because
nothing looked past the folder in hand. See [[package-hygiene-pipeline]].
