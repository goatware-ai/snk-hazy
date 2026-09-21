# Reviewer Rubric

> Style Guide Section 1: Recognizing LLM-Generated Files. Evaluation and outcome logic for
> reviewers.
>
> Transcription of the "Reviewer Rubric" page from the Reviewers' Hub. It governs how LLM tells are
> counted and converted into an outcome. The companion review rule set is
> `reviewer-guidelines-v5.1.md`.

---

## The Severity Escalation System

Tells escalate. Convert them before deciding an outcome.

- **2 LOWs = 1 MEDIUM.** Two LOW tells in the same file convert to one effective MEDIUM.
- **2 MEDIUMs = 1 HIGH.** Two effective MEDIUM tells convert to one effective HIGH.
- **Convert in order.** Apply LOWs to MEDIUMs first, then MEDIUMs to HIGHs. Never skip a step.
- **Remainders count.** Leftover tells after conversion still carry weight in the outcome.
- **Evaluate each file separately.** Tells do not pool across files in a submission.

### Conversion reference

- 2 LOW tells become 1 effective MEDIUM. Effective HIGH count: 0, not yet HIGH.
- 2 MEDIUM tells become 1 effective HIGH. Count: 1.
- 4 MEDIUM tells become 2 effective HIGHs. Count: 2.
- 1 MEDIUM plus 2 LOWs becomes 2 MEDIUMs, then 1 effective HIGH. Count: 1.
- 2 HIGHs plus 2 MEDIUMs becomes 2 HIGHs plus 1 effective HIGH. Count: 3, which is a REJECT.
- 5 MEDIUMs becomes 2 effective HIGHs plus 1 remaining MEDIUM. Count: 2 plus 1 MEDIUM, which is a
  send back.
- 6 MEDIUMs becomes 3 effective HIGHs. Count: 3, which is a REJECT.

---

## Outcome Decision Logic

- **ACCEPT.** 0 effective HIGHs, 0 effective MEDIUMs, and 0 or 1 LOW. A single isolated LOW tell is
  acceptable and needs no action.
- **SEND BACK.** 0 effective HIGHs but 1 or more effective MEDIUMs, or 1 to 2 effective HIGHs.
- **REJECT.** 3 or more effective HIGHs.

### Worked Examples

- **1 HIGH** (AI-blue header). 1 effective HIGH. **SEND BACK.** One revision allowed. Flag the
  specific header fill and hex range.
- **2 MEDIUMs** (em dash density plus generic headers). 1 effective HIGH. **SEND BACK.** Same
  threshold applies after conversion.
- **1 MEDIUM** (passive voice throughout). 1 effective MEDIUM, no HIGHs. **SEND BACK.** A single
  MEDIUM alone triggers send-back, no conversion needed.
- **2 LOWs** (uniform visual hierarchy plus gradient fills). 1 effective MEDIUM. **SEND BACK**, not
  accept.
- **1 LOW** (uniform visual hierarchy only). No conversion. **ACCEPT.** A single isolated LOW is the
  one acceptable tell combination.
- **2 HIGHs plus 2 MEDIUMs** (AI-blue, self-naming, em dash, generic headers). 3 effective HIGHs.
  **REJECT.**
- **1 HIGH plus 3 MEDIUMs** (AI-blue, hard-coded values, round numbers, single-tab). 2 effective
  HIGHs plus 1 remaining MEDIUM. **SEND BACK.**

---

## Send-Back Process

**Revision limit: one revision only, no exceptions.**

Every send-back note uses the three-part format: **what is wrong**, naming the specific tell and
where it appears; **why it is wrong**, tying it to the severity rating and the tell category; and
**what to do about it**, giving a concrete fix the EC can act on.

Number the tells so the EC can see the full scope, for example "Tell 1 of 2: AI-blue color scheme,
HIGH, Visual and Color Tells" followed by "Tell 2 of 2: Em dash overuse, MEDIUM, Prose and Language
Tells".

---

## Resubmission Review Standard

The bar tightens on resubmission. Anchor your review to the tells you flagged, but any new tell
counts too.

- **0 tells of any severity remaining: ACCEPT.** All flagged tells resolved.
- **1 LOW tell remaining, none previously unflagged: ACCEPT.** A single isolated LOW is acceptable,
  consistent with the first-submission standard.
- **Any 1 MEDIUM tell found, whether previously flagged or new: REJECT.**
- **Any 1 HIGH tell found, whether previously flagged or new: REJECT.**

---

## Flagging LLM Rejections in the Daily Thread

Flag any first-submission rejection where the effective HIGH count reaches 3 or more, and any
resubmission rejection where a MEDIUM or HIGH tell is found. **Do not flag send-backs.** Only
rejections require a daily thread entry.

Copy this template into the thread: Task ID, file or files affected with type, file context (input
file or golden solution), submission type (first or resubmission), primary tell category, all tells
found with severity, effective HIGH count, and any pattern notes such as the same tell recurring from
a prior rejection.

---

## Quick Reference

| Tells found | Outcome |
| --- | --- |
| 0 HIGHs, 0 MEDIUMs, 0 to 1 LOWs | **ACCEPT.** No revision applicable. |
| 0 HIGHs, 1 or more MEDIUMs | **SEND BACK.** One revision, whole task. |
| 1 to 2 effective HIGHs | **SEND BACK.** One revision, whole task. |
| 3 or more effective HIGHs | **REJECT and FLAG.** No revision. |
| Resubmission with any MEDIUM or HIGH | **REJECT and FLAG.** No revision. |
| Resubmission with 0 MEDIUMs or HIGHs and at most 1 LOW | **ACCEPT.** |

**If you are unsure, document and escalate rather than guess.** If a file has tells that do not
clearly map to a severity rating in the style guide, or a combination you have not seen before, write
it up and raise it rather than forcing a rating.

---

## Provenance

Transcribed 2026-08-20 from screenshots of the Reviewers' Hub "Reviewer Rubric" page. The page is
Section 1 of the reviewer style guide and covers evaluation and outcome logic only. The tell catalog
it references (categories such as Visual and Color Tells and Prose and Language Tells, and which
specific tells are LOW, MEDIUM or HIGH) lives in the rest of the style guide and was not part of the
captured pages.
