# Feedback Best Practices

> **Inherited from the Geranium desk, not confirmed for Hazy.** This document describes
> Geranium's reviewer rules. Hazy offers no review assignments. It is kept for reference and was NOT updated in the 2026-09-21 port; treat
> anything it says about sector, rubric bands or platform checks as Geranium's, not
> this project's. See `../../RULE-DELTAS.md`.

What every revision note must contain, how long it should be, and why it has to be.

## Why your note matters

Three constraints shape every note you write.

The EC has up to four revision attempts before a task is rejected. A vague note rarely costs only one of them, because the EC fixes what they guessed at rather than what was actually wrong, and the same issue comes back on the next pass.

Your review window is two hours, and your notes are part of it. Budget for writing, not just for reading and fixing.

You get no chance to clarify after you submit. The note has to stand on its own.

The test to apply before you submit: could the EC open your note, go straight to the file, and know exactly what to change without messaging anyone? If the answer is no, the note is not finished, no matter how long it is.

## Every revision note has three parts

This is not a style preference. A note missing any one of these is incomplete.

### What is wrong

Name the exact item. Criterion 3, not the rubric. Row 14 of the golden solution, not the numbers look off. The specific file name, not the input files.

### Why it is wrong

State the problem in one sentence. "This criterion bundles three separate checks into one field, which breaks our automated scoring" is more useful than "rubric needs work."

### What to do about it

Give a clear path to acceptance. "Split this into three separate criteria, each testing one thing: the correct vendor count, the total contract value, and whether cancelled contracts are excluded" tells the EC exactly what to submit next.

Tone matters throughout. These are domain experts contributing real knowledge. Be direct and specific without being dismissive. A note that says "this is fixable, here is what to change" keeps people engaged. "This is wrong" with no guidance makes people disengage.

## Length: two short paragraphs is the ceiling

Most strong notes run four to six sentences. Length is not thoroughness. If you find yourself writing a third paragraph, you have started explaining instead of instructing.

**Paragraph one, required.** The blockers, most severe first, each one with what is wrong, why it is wrong, and the fix. Use exact names throughout: file names, criterion numbers, cell references, row numbers.

**Paragraph two, optional.** What you corrected yourself, so the EC can see it, and at most one pattern to carry into the next submission. Nothing else.

When you need to cut, start with these. Opening summaries of what the task was about. Praise placed before the substance. Restatements of the guidelines. Anything the EC already knows because they wrote it.

## Examples

Each pair below describes the same review finding written two ways. Only one of them tells the EC what to submit next.

### Rubric finding

**Not acceptable:** "Rubric needs work. Several criteria are unclear and should be tightened up before this can be accepted."

No criterion number, no explanation of the defect, and no fix. The EC has to reverse engineer your review.

**Acceptable:** "Criteria 2 and 4 both check whether the workbook has a summary tab. Merge them, or rewrite criterion 4 to test the total revenue value of 1.43M from Q3_vendor_spend.xlsx. Criterion 7 has the weight written into the text field as a score prefix. Remove that prefix and put the weight in the numeric weight field."

Two blockers, both named, both with a specific action, in three sentences.

### Golden solution finding

**Not acceptable:** "Golden solution looks off. Please double check your numbers and make sure everything ties out before you resubmit."

This sends the EC back through the entire solution to hunt for an error you already found. Your two hours become their five.

**Acceptable:** "Row 14 of the golden solution shows Q3 revenue as 412K, but cell D14 of Austin_PL_2025.xlsx shows 389K. Correct row 14 and recheck the three totals that feed off it in rows 15 to 17."


### Prompt finding

**Not acceptable:** "The prompt is too easy and reads like it was AI generated. Needs to be more complex and sound more human."

Two real problems with zero direction. More complex and more human are not instructions anyone can act on.

**Acceptable:** "The prompt asks for a summary of information already organized in intake_packet.pdf, so a model can answer it without reconciling anything. Add a second source that conflicts with the packet, such as the billing export, so the model has to resolve the difference. Also replace utilizing your expertise in line 2 with the actual role and setting, for example a claims supervisor preparing a denial appeal."

This names the structural defect and the voice defect separately, and gives a concrete substitution for each.

## What makes a note read as machine written

- Stacked adjectives followed by a list of failures, for example "clear, well structured analysis, not vague or incomplete." This is the same pattern that gets a prompt or a criterion sent back to the EC, so hold your own writing to the bar you are enforcing.
- A summary opener, for example "Overall, the submission demonstrates a solid understanding of the task requirements."
- Headings and bullet scaffolding wrapped around four sentences of actual content.
- The praise sandwich: a compliment, a vague concern, another compliment, with no file, no number, and no action.
- Hedged instructions, for example "you may want to consider possibly revising" where the note should say "revise criterion 4 to test the 1.43M total."
- No anchors anywhere. Not one file name, cell reference, or criterion number in the whole note.

## Match the note to your decision

Select at least one error or recommendation class and no more than six, including classes that cover issues you corrected yourself.

**Accept.** Say what you fixed directly so the EC can see it, and still select the classes matching those corrections. Reviewer Recommend is reserved for exceptional work only.

**Needs Revision.** Name every blocker in one pass. Surfacing one issue now and another next round costs the EC attempts they should not have to spend.

**Reject.** State the reason plainly and do not imply a revision path that does not exist. This covers work that is off sector, has unusable input files, is fully model generated, or has exhausted its revision attempts without reaching the bar.

**Suspected Duplicate or Template.** Say what the task appears to reuse and where you saw it. This can sit alongside an Accept when the task quality itself is fine.

## The sixty second check before you submit

Run these five questions against your note. If any answer is no, the note is not ready, and fixing it now is faster than adjudicating a dispute later.

1. Did I name the exact file, criterion number, row, or cell for every issue?
2. Would the EC know what to submit next without messaging anyone?
3. Is it two paragraphs or fewer?
4. Does it match my decision and the error classes I selected?
5. Is the tone direct without being dismissive?
