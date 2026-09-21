---
name: platform-hidden-return-hold
description: "Platform announcement 2026-09-14: new auto evaluations return tasks without showing the triggering feedback; a return whose visible notes are all positive gets no rebuttal and no changes until the team confirms next steps (boiler-replacement-recommendation refinement held at round 2)"
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

**How to apply:** when pasted feedback for a return contains only confirmations
(the adjudication note that carries a hand-over finding forward and verifies it clean,
as on boiler-replacement-recommendation refinement round 2, 2026-09-14), log a HOLD entry
in that task's feedback-log.md and change.log, leave any prepared form actions
unsubmitted, and say so in the summary. Resume with the ordinary revision flow
([[revision-workflow]]) once the operator relays the team's resolution. Tasks held under
this rule as of 2026-09-14: refinement b9c2dfc3-a18c-4b4e-8318-a11c07d51826
(boiler-replacement-recommendation), round 2 prepared locally, nothing submitted. Added 2026-09-14: refinement fc4c0b1a-285d-422d-8c74-5cdf47c67089 (june-price-review, own task 23), whose panel is an all-positive auto-eval trace naming two unstated Briefing findings; round 1 prepared locally (gate 0), nothing submitted.
Same-shape returns the same week, whose logs prepared a Section 3 change and a resubmit
before the announcement (confirm with the operator whether they went out): hartwell-price-worksheet
590fc77f (round 3, two repeats already fixed, no package change), inbound-consolidation-plan
a784d07d (round 4, note reports no defect, no package change), tessendorf-channel-split
submissions/35 (2026-09-11 adjudication note describing the task's correct state, no form action).
- 2026-09-14: task 23's own UID 7373c89f came back from adjudication with a STATED finding (criterion 15's COUNTA and label lock, the July 14 prose), so it was revised in the ordinary flow under /revise-task, adopting the held refinement round's golden and inputs; the refinement fc4c0b1a stays held and its prepared round is superseded if task 23 resubmits.
- 2026-09-14: refinement f35f9e96-4dab-4360-b15c-f12edd9aad9a (recall-response) held at round 4: the note's one stated finding (lot P2-26-163 on Affected_Lots row 12) is false against every copy of the golden, its second item says no defect, its third compares without stating one; a fix for the total-row reading of item 3 is written in change.log, not applied.
- 2026-09-14, later the same day: recall-response f35f9e96 hold LIFTED. The fetch JSON carried the trigger the note did not: evaluations[2].reference_soundness_check (GDPVal judge) Major with two fully stated findings, and the uploadedAt stamps showed the round 3 zips had never been uploaded (solution 09-12, inputs 09-11), so the note was written against a mixed package. Before holding any return, fetch the JSON and read (1) every evaluations[*] child with passed=False and its agent_result.axes[*].findings, (2) input_files.uploadedAt and the golden uploader's uploadedAt against the round that was meant to ship. A hold is for a return whose JSON also shows nothing; a garbled note over a stated judge finding is revised normally.
- 2026-09-15: refinement 253bad46-a09a-4d29-9d72-e2674cfd4c72 (rfq-response, third-party) HELD at offer. Its only note (category Golden Solution) confirms the golden and states no defect. The fetch JSON was read first, per the rule above: evaluations empty, every revision, eval, rebuttal and accept note null, seed zips one coherent upload (2026-08-24). fetch_refinement.py deletes its scratch JSON, so read it with fetch_refinement.fetch_task_json(uid, dir) into a kept folder. Nothing prepared; the untouched gate's 81 errors are listed in change.log for a later round. The offer's expiry_time was 2026-09-15T08:11Z, so a hold can let a refinery offer lapse; say so to the operator.
- 2026-09-15, later: rfq-response 253bad46 hold LIFTED on operator direction ("Feedbacks are in feedback.md"). A positive note can still carry actionable items it frames as acceptable, here golden details no input sources and rubric rows grading them. Before holding, read the note for anything it calls unsupported, not stated in any input, or the bidder's own assertion; those are fidelity findings, not praise, and the round proceeds.
- 2026-09-17: task 24 vondrak-negotiation-plan 27bd8e87 came back with no feedback text, only the rubric as JSON. On operator direction ("no feedback actually ... check all rules, validations, gate and update it to meet our docs") it was treated as a full rules pass under /revise-task rather than a hold: the untouched folder gated at 23 errors (47 once the misnamed rubric CSV was found), rebuilt to 0, resubmission left to the operator.
