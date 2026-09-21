---
name: platform-hidden-return-hold
description: "Platform announcement 2026-09-14: new auto evaluations can return a task without showing the triggering feedback, so a return whose visible notes are all positive gets no rebuttal and no changes until the team confirms next steps. Open before holding anything: the JSON usually carries the trigger the note does not, and a garbled note over a stated judge finding is revised normally"
metadata:
  type: project
---

On 2026-09-14 the platform team announced that recently introduced auto evaluations may
send a task back for revision or rejection without showing the feedback that actually
triggered it, and that engineering is investigating. Instruction: when a task is returned
and the visible reason is not valid or clear (every reviewer note and auto-eval note is
positive or says it passed), do NOT submit a rebuttal and do NOT make changes yet; wait for
the team's next steps.

**Why:** the visible note is not the trigger in these cases, so a revision aimed at it
spends a submission cycle on nothing and may touch a file the hidden check passed.

**How to apply:** when pasted feedback for a return contains only confirmations - an
adjudication note that carries a hand-over finding forward and verifies it clean - log a HOLD
entry in that task's feedback-log.md and change.log, leave any prepared form actions
unsubmitted, and say so in the summary. Resume with the ordinary revision flow
([[revision-workflow]]) once the operator relays the team's resolution. The rule is the platform
team's, so it is assumed to hold here; nothing is on hold on this desk today.

**Read the JSON before holding anything (2026-09-14).** A hold is for a return whose JSON also
shows nothing. One held return was lifted the same day: the fetch JSON carried the trigger the
note did not - a `reference_soundness_check` (GDPVal judge) Major with two fully stated findings
- and the `uploadedAt` stamps showed that round's zips had never been uploaded, so the note had
been written against a mixed package. Before holding any return, fetch the JSON and read
(1) every `evaluations[*]` child with `passed=False` and its `agent_result.axes[*].findings`, and
(2) `input_files.uploadedAt` and the golden uploader's `uploadedAt` against the round that was
meant to ship. A garbled note over a stated judge finding is revised normally, as is a return
with a stated finding on the task's own UID.

**An empty-evaluations JSON is readable, and an offer expires (2026-09-15).** Where a return's
only note confirms the golden and states no defect, and the JSON shows evaluations empty with
every revision, eval, rebuttal and accept note null, the hold is correct - but say so promptly,
because an offer carries an `expiry_time` and a hold can let it lapse. Read such a JSON into a
kept folder rather than a scratch dir that gets deleted.

**A positive note can still carry actionable items (2026-09-15).** Before holding, read the note
for anything it calls unsupported, not stated in any input, or the bidder's or author's own
assertion. Those are fidelity findings, not praise, and the round proceeds.

**No feedback text at all is not automatically a hold (2026-09-17).** One return came back with
no feedback text, only the rubric as JSON. On operator direction ("no feedback actually ... check
all rules, validations, gate and update it to meet our docs") it was treated as a full rules pass
under /revise-task rather than a hold: the untouched folder gated at 23 errors (47 once the
misnamed rubric CSV was found) and was rebuilt to 0, with resubmission left to the operator.
