# Project Geranium Reviewer Guidelines (V5.1)

> Project Geranium — GDPVal++ · Reviewer Guidelines · Version 5.1 · 2026
>
> Transcription of the "Reviewers guidelines" doc from the Reviewers' Hub
> (Geranium-Production → how to task). This is the **review** rule set; the authoring
> rule set is `../../submission/platform/project-guidelines-v5.1.md`. Section numbering follows the source.

---

## What's New in V5.1 (update 7/27 to rubric review)

Three checks to enforce on top of the V5.0 review update. **Style and formatting criteria must be
fewer than half of all criteria and no more than a quarter of the total reward. Every task must
include at least two negative weighted criteria. When the prompt names exact file names, the rubric
must include a criterion that checks the delivered file uses them.**

Bounded subjective criteria and reasoning validity checks are now valid. Do not send a criterion
back for being subjective when it names the conditions a sound answer must meet and scores the
reasoning. Do send back prompts or criteria written in the LLM pattern of stacked adjectives
followed by failure conditions. The earlier time based fix thresholds remain in effect.

**Operational updates.** Record your review time in the new platform field. It is used for payment,
so enter it accurately, and it can be verified against completed work.

Reviews generally take 30 minutes to 2 hours. If a review will take longer than 2 hours, send the
task back to the EC with feedback based on your review, and complete any fixes you can reasonably
make within the 2 hour window. This replaces the earlier per element time thresholds.

Validate the majority, 75 to 100 percent, of the rubric criteria for V5.1 compliance, and confirm
the golden solution both matches the rubric and is grounded in the input files. A new review option,
**Suspected Duplicate or Template**, flags a task that appears to reuse a previous task or template,
even when it is otherwise acceptable.


# Section 1: Prompt and Input Files

## Prompt

Ask yourself: does this sound like a real person handing off a real task, or like a prompt someone
generated to meet the requirements?

- **Natural practitioner voice with specific expert context.** There should be a role, a situation
  and stakes. "You are a lawyer" is not enough. "You are outside counsel reviewing a commercial
  lease dispute in Cook County" is stronger. Watch for generic role framing, step by step
  instructions masquerading as a task, clinical phrasing like "utilizing your expertise", vague
  stakes with no named audience or deadline, and a total absence of friction or messiness. Real
  tasks have constraints and context. LLM generated prompts read like clean textbook problems. If an
  LLM wrote it, send it back. See the submission guidelines for the full prompt comparison examples.
- **LLM adjective pattern.** Prompts must not use two stacked adjectives followed by a noun and a
  list of failures, for example "clear, well structured analysis, not vague or incomplete".
- **Real difficulty.** The task should target 5+ hours of manual work, with 3 hours the absolute
  floor. If a capable model could nail it on the first try, it is not hard enough.
- **Concrete input files and deliverable.** The prompt must name the input files by their actual
  file names, and give a specific output file type and file name.

## Input Files

Open every file. You do not need to read them cover to cover, but you must verify they are real,
substantial and necessary. See the Task Examples pages for additional context.

- **Substantial content.** Each file should contain enough material to represent real world
  documentation. A half page doc with a few paragraphs is not enough.
- **Not 100% LLM generated.** If every file is clearly fabricated (generic company names, round
  numbers, placeholder text), reject the task. Sanitized real documents, original work, and LLM
  assisted input files are fine, but LLM assisted inputs should not feel artificial in any way.
- **No paywalled or restricted content.** Flag anything that looks like it came from behind a
  paywall: Substack articles, copyrighted stock media, proprietary employer work products.
- **Clean packaging.** No subfolders in the zip. No empty files. File names match what the prompt
  references. No double extensions. Files open cleanly, with no corruption or repair prompts.

---

# Section 2: Golden Solution and Rubric

## Golden Solution

This is the answer key. If it is wrong, the whole task is worthless, because we score models against
it. You do not need to redo the task from scratch, but you do need to verify the solution is
correct, complete and polished. Confirm two things: the golden solution matches the rubric, and it
is grounded in the input files.

- **Answers the prompt.** Does it address every part of what was asked, with full accuracy? Missing
  sections or skipped requirements are grounds for revision. Pick 2 to 3 calculations or data points
  and verify them against the input files. Models get these wrong regularly, and submitters
  sometimes trust the model output without checking. If the numbers do not match, send it back.
- **Human edited, not a raw LLM dump.** Look for signs of unedited model output: generic phrasing,
  no domain specific voice, overly hedged language, perfect formatting that looks templated.
- **Clean packaging and presentation ready formatting.** No subfolders, no empty files, no double
  extensions, clean names. All files open with no XML errors or repair prompts. Spreadsheets use
  dynamic formulas, not hard coded values. Presentations need backgrounds, charts or tables, not
  plain white slides. Documents should look polished and client ready. No broken charts, no low
  resolution images.

**The client test:** would you hand this to a client or present it to your manager? If not, it is not
ready. That is the bar for golden solutions.

## Rubric

The rubric determines how we grade model outputs. A vague rubric makes the whole evaluation
unreliable. This is where we saw the most issues in the first review cycle.

- **Each criterion is atomic.** One check per criterion. If a criterion says "identifies the three
  key vendors AND calculates the correct totals AND formats the summary tab", that is three checks
  crammed into one. Send it back to be split.
- **Criteria are specific with correct answers,** and do not simply repeat the prompt instructions.
  "The memo reconciles conflicting information" is not specific enough. It needs to say which
  conflicts and what the correct reconciliation is, ideally with numbers. Correct values should be
  human calculated, not copied from the model output.
- **Rubric matches the golden solution.** Pick 2 to 3 criteria and verify the golden solution
  actually satisfies them. If the rubric expects a specific number and the golden solution has a
  different one, something is wrong.
- **Bounded subjective criteria are allowed.** Some tasks have more than one defensible answer. A
  criterion that names the conditions a sound answer must meet and scores the reasoning is correct,
  not vague, and should not be sent back for being subjective. Only send back unbounded criteria,
  meaning those that name no conditions and leave a grader unable to tell whether a response passes.
- **Reasoning is tested, not just the result.** Where a wrong method could still reach the right
  answer, criteria should test how the answer was derived. A right answer reached by faulty logic
  should not score full marks.
- **Cap style and formatting criteria.** They must be fewer than half of all criteria and must not
  exceed a quarter of the total reward. Send back a rubric that lets presentation dominate.
- **At least two negative criteria.** Most tasks should carry two negatively weighted criteria. Send
  back a rubric with fewer.
- **File name criterion when names are given.** If the prompt names exact file names, the rubric must
  include a criterion checking the delivered file uses them. Send it back if that check is missing.

---


## Reviewer order of operations

1. **Determine the overall decision first.** Decide whether the task is Accept, Needs Revision or
   Reject before you start editing. This locks your direction and prevents over investing in a task
   that should be rejected, or under correcting one that needs a full revision.
2. **Fix all correctable elements, regardless of the overall decision.** Even if the task is going
   back for Needs Revision, fix everything across the other elements that falls within the time
   limits. Do not skip fixable issues just because the task is not being accepted.
3. **Submit.**

## Time threshold reference

Illustrative, not exhaustive. Use these to calibrate your judgment on edge cases.

- **Prompt, under 10 minutes:** correcting a typo or grammatical error; adjusting a vague word or
  phrase, such as replacing "analyze the data" with "calculate the year over year variance"; adding a
  missing output file name or extension; fixing a minor tone issue, such as EC voice appearing where
  the model role should be.
- **Prompt, over 10 minutes:** rewriting a prompt that is overspecified or step by step to the point
  that the model has no reasoning to do; revising a prompt so underspecified that the expected output
  is unclear; reframing a prompt that can be answered without opening the input files.
- **Input files:** no direct edits permitted. Input files are locked in the platform, so all input
  file issues route to Needs Revision regardless of time. That covers LLM generated content,
  decorative or placeholder files, thin or sparse content, corrupted files, IP concerns, and file
  names that do not match the prompt.
- **Rubric, under 10 minutes:** fixing a typo in a criterion; tightening the wording of 1 to 2
  criteria without changing what is being tested; adding one missing criterion when the correct
  answer is clear from the golden solution and input files; removing a score weight embedded in
  criterion text and confirming it is in the numeric field.
- **Rubric, over 10 minutes:** splitting a bundled criterion into two or more atomic criteria and
  recomputing weights; rewriting multiple vague criteria that lack specific values or verifiable
  answers; rewriting criteria that simply restate the prompt instructions; adding more than one
  missing criterion; rewriting criteria that conflict with or are not satisfied by the golden
  solution.
- **Golden solution, under 10 minutes:** correcting a clear factual typo, such as a single wrong
  number, a date off by one digit, or an obvious copy paste error where the correct value is
  immediately verifiable from the input files; fixing a file naming error such as a wrong or double
  extension.
- **Golden solution, over 10 minutes:** correcting a solution that does not fully answer the prompt;
  fixing wrong data across multiple fields or calculations; rewriting content that reads as unedited
  LLM output; rebuilding a solution that fails multiple rubric criteria; reformatting a solution that
  does not meet the client test.

## Selecting error and recommendation classes

When submitting a review decision you must select at least one class, with a maximum of six.

**Reviewer Recommend** is reserved for work that is exceptionally high quality across all components,
where the prompt, input files, golden solution and rubric all meet or exceed the bar and the
submission stands as a model example of what Geranium tasks should look like. Select it on an Accept
decision only. **N/A** applies when a task has no errors and you are accepting it, but the work does
not rise to the Reviewer Recommend threshold.

Error classes usually apply to any task receiving Needs Revision or Reject. Occasionally, when edits
are minor enough that you can make them and then accept, still select the categories that best align
with the corrections you made. Multiple classes may apply to a single task and should all be selected
when they do.

- **LLM-Generated: Input Files** and **LLM-Generated: Golden Solution** flag components that read as
  unedited or lightly edited model output rather than genuine expert produced work.
- **Input File Quality** covers any input file problem that is not LLM generation: files that are thin
  or lacking the depth needed for a complex workflow, content misaligned with the prompt's domain or
  task, broken formatting, hard coded spreadsheet values, or files that would not pass the client
  ready standard.
- **Golden Solution Quality** applies when the solution fails one or more rubric criteria, contains
  data errors or mismatches with the input files, includes unedited model output, or is not formatted
  to a presentation ready standard a client or manager could act on.
- **Rubric Quality** flags any rubric that departs from Geranium guidelines: vague or subjective
  criteria, criteria that simply restate prompt instructions, missing atomic structure, weights
  embedded in criterion text rather than the numeric field, or a rubric that does not align with what
  the golden solution delivers.
- **Prompt Quality** applies when the prompt is missing any required element: a specific expert role
  and situational context, explicit references to input files by exact filename, a concrete output
  file type and name, sufficient task complexity, or a practitioner voice that does not read as LLM
  generated.

---

## Writing Good Feedback

Your revision notes are the only thing the EC sees. If the notes are vague, they will guess at what
you meant and submit something that still does not work. Be direct, reference specific files and
criteria, and tell them exactly what needs to change. Every revision note should have three things.

- **What is wrong.** Name the specific item. "Criterion 3", not "the rubric". "The revenue figure on
  row 14 of the golden solution", not "the numbers look off".
- **Why it is wrong.** Explain the problem. "This criterion bundles three separate checks into one
  field, which breaks our automated scoring" is more useful than "rubric needs work".
- **What to do about it.** Give a clear path to acceptance. "Split this into three separate criteria,
  each testing one thing: (1) the correct vendor count, (2) the total contract value, (3) whether
  cancelled contracts are excluded" tells the EC exactly what to submit next.

**Tone matters.** These ECs are domain experts donating real knowledge. Be direct and specific, but
not dismissive. A note like "This is fixable, here is what to change" keeps people engaged. "This is
wrong" with no guidance makes people disengage.

Examples, bad then good:

- "Prompt is too easy." Better: "The prompt asks for a summary of info already organized in the PDF,
  which is not complex enough for a 3+ hour workflow. Add more input sources the model must
  reconcile."
- "Rubric needs work." Better: "Criteria 2 and 4 both check whether the workbook has a summary tab.
  Merge them, or rewrite criterion 4 to test the specific total revenue value ($1.43M per the input
  data)."
- "Golden solution looks off." Better: "Row 14 of the golden solution shows Q3 revenue as $412K but
  the Austin P&L (cell D14) shows $389K. Please verify against the source file and correct."
- "Criterion text has weights in it." Better: "Criteria 1 and 5 have the score written in the text
  field. Remove the score prefix from the criterion text. The weight should only appear in the
  numeric weight field."

---

## Edge Cases

- **Debatable interpretation.** If it is a minor interpretive difference that does not affect rubric
  grading, accept it. If it materially changes how a model would be scored, send it back for
  revision.
- **Disagreement with the submitter.** If an EC disputes your feedback after a revision, adjudication
  is case by case.

---

## Review Checklist

### Prompt

- Clear, natural practitioner voice, with no LLM adjective pattern
- Sets concrete expert context: role, situation, stakes
- Requires multi step reasoning, roughly 5+ hours of work
- Specifies a concrete output file with an exact file name
- References input files explicitly by name
- Cannot be completed from the instructions alone, and requires using the files
- Not overspecified, so expert judgment is still needed

### Input files

- All files open cleanly, with no corruption, errors or repair prompts
- Substantial and necessary, with no placeholders or irrelevant files
- Clean packaging: no subfolders, empty files or messy names
- File names match prompt references exactly
- Not fully LLM generated, and no restricted or paywalled content

### Golden solution

- Fully answers the prompt, with no skipped sections
- Fact checked: 2 to 3 data points verified against the input files, and any mismatch means send it
  back
- Clearly human edited, not raw LLM output
- Presentation ready, passing the client test, with polished formatting and no errors
- Spreadsheets use formulas, not hard coded values
- Slides and documents include real visuals, not barebones content
- Files open cleanly, with correct naming and packaging

### Rubric

- Minimum 15 criteria
- Each criterion is atomic, testing one check only
- Criteria are specific and verifiable, with exact answers and values
- Tests reasoning, not just task completion
- Aligned with the golden solution: spot check 2 to 3 criteria, and any mismatch means send it back
- Subjective criteria name the conditions a sound answer must meet and score the reasoning, and are
  not sent back for being subjective
- Reasoning is tested where a wrong method could reach the right answer
- Style or formatting criteria are fewer than half of all criteria and at most a quarter of total
  reward
- At least two negative weighted criteria
- A file name criterion is present when the prompt names exact file names

**When in doubt, flag.** If you are unsure whether something meets the quality bar, or you spot a
pattern across multiple submissions, flag it in `#ec-geranium-project` on Slack. Surfacing edge cases
early improves the guidelines for everyone.

---

## Provenance

Transcribed 2026-08-20 from screenshots of the Reviewers' Hub "Reviewers guidelines" page
(Geranium-Production → how to task → Reviewers' Hub). Headings and section numbers are reproduced as
they appear in the source, which jumps from Section 2 to Section 4; no Section 3 heading appeared in
the captured pages.

**Re-verified 2026-08-26** against a fresh capture of the same page, section by section: every
heading, rule and checklist line matches, including the V5.1 rubric checks, the 2 hour review
window, the Suspected Duplicate or Template option, the six error classes and the Section 2 to
Section 4 jump. No content changed. Filed under `docs/reviewer/platform/` alongside the reviewer rubric and the
feedback standard.
