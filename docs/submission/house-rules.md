# House rules

Standards this desk holds itself to, beyond what the submission form states.

[platform-submission-form.md](platform/platform-submission-form.md) is the authority: it is
what blocks submission, and where it speaks it governs. The rules here cover what it leaves
unsaid. They are this desk's own, adopted because they have earned their place, and any of
them can be changed by deciding to change it. None of them is a platform requirement.

Checks cite this file as their source where no form section carries the rule.

---

## Input files

**At least two, three or more preferred.** One input is not a task: the difficulty is
supposed to come from reconciling information held in different places, and a single file
cannot distribute anything. Two is the floor; three or more is where a task starts being
worth building.

Enforced by **M6**, which errors below two and recommends below three.

Formats are whatever a practitioner in the occupation would actually work from: `.docx`,
`.pdf`, `.xlsx`, `.pptx`, engineering files such as STEP, STL and GERBER, and multimedia.
Mixed types are a strength, not a complication.

## Difficulty

**A model must not be able to produce a good answer from the instruction alone.** This is
the sharpest single test of whether a task is worth submitting. If the instruction can be
answered without opening the inputs, the inputs are decoration and the task measures
nothing. Difficulty comes from the source material and the reasoning needed to reconcile it,
never from making the instruction longer or more prescriptive.

**Target five to ten hours of a qualified professional's time**, without AI. The form's own
check wants more than three hours; three is the floor below which a task reads as too easy,
and five is where this desk aims so that an unsympathetic estimate still clears it.

Enforced by **M4**, which errors under three hours and recommends under five, and by the
`frontier_resistance` row of the pre-submission audit.

## Prompt shape

**Tell the solver WHAT to produce, not HOW.** An instruction that reads like a template to
fill in leaves no room for judgment and makes the task easy for a model. Dictating every
step, column name and exact phrase is the most common way a prompt is spoiled.

**No persona openings.** "You are a lawyer" and its relatives are a tell, not context. Set
the professional situation instead: the role, the organization, the trigger, the audience,
in the requester's own voice. Enforced by **P4** and **P6**.

**US setting.** Tasks are written for a workflow in the United States. Enforced by **P4**.

## Rubric

**At least six criteria.** The form allows three. Six is this desk's floor, kept because a
rubric that short has never covered a task worth submitting. The form expects 20 to 60 or
more anyway, so the floor is nowhere near the binding constraint; lower it if it ever stops
being true. Enforced by **R11**, which also recommends under 20.

**No flat weighting.** A rubric where every criterion carries the same weight tells a grader
nothing about what matters. At least one core criterion belongs at +4 or +5.

**At most 500 characters per criterion.** No platform rule sets this. A criterion past 500
characters is reliably bundling several checks into one line, which the form does forbid.
Enforced by **R1**.
