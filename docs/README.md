# Project Hazy — Documentation

Local documentation for **Snorkel's Project Hazy (GDPVal++)**, organised by the three
jobs this repo does: **submitting** tasks, **reviewing** other contributors' tasks, and
**refinement**.

Inside `submission/` and `reviewer/`, the `platform/` subdirectory holds documents captured
verbatim from Snorkel's own pages. **Those captures are authoritative** — on any conflict
with a workflow page, a tool, or anything else in this repo, the capture wins. Everything
outside `platform/` is this repo's own derived working material.

Assigned sector: **Wholesale Trade** (both for authoring and for review assignments).

---

## Layout

```
docs/
├── README.md                        ← this file
│
├── submission/                      ← authoring a task
│   ├── platform/                    ← AUTHORITATIVE captures (live GitBook, 2026-08-26)
│   │   ├── welcome.md                       program overview and quality bar
│   │   ├── project-guidelines-v5.1.md       the authoring rules (rubric band 15–60)
│   │   ├── creating-input-files.md          authenticity, LLM-assist policy, leakage, tell log
│   │   ├── style-guide-llm-tells.md         severity-keyed LLM tell tables + self-checks
│   │   ├── task-lifecycle.md                in-app checks → evals → review → adjudication
│   │   ├── auto-eval-feedback-guide.md      reading auto-eval results; the rebuttal process
│   │   ├── task-example-wholesale-trade.md  annotated good/bad example (workbook deliverable)
│   │   ├── wholesale-trade-uniqueness-map.md    accepted asks, crowding, fresh ideas
│   │   ├── platform-submission-form.md      the live submission form, field by field
│   │   └── platform-wholesale-trade-occupations.md   O*NET table + per-prompt routing
│   └── workflows/                   ← our decomposition, one stage per file
│       ├── 01-ideation.md           pick a task worth building; difficulty & the 3-hour floor
│       ├── 02-prompt-writing.md     house prompt rules (P4/P6/A20); O*NET routing house notes
│       ├── 03-input-files.md        authenticity, distributed difficulty, leakage, packaging
│       ├── 04-golden-solution.md    client-ready deliverables; formatting standards
│       ├── 05-rubric.md             15–60 criteria; weights; rigid vs subjective; negatives
│       ├── 06-metadata.md           metadata values; house notes on the submission form
│       └── 07-pre-submission-audit.md   package sequence; one row per gate keyed to check ids
│
├── reviewer/                        ← reviewing other contributors' tasks
│   ├── platform/                    ← AUTHORITATIVE captures (Reviewers' Hub)
│   │   ├── reviewer-guidelines-v5.1.md   the review rule set and decision authority
│   │   ├── reviewer-rubric.md            severity math: how LLM tells become a verdict
│   │   ├── feedback-best-practices.md    the revision note standard
│   │   ├── platform-review-form.md       the live review form, field by field
│   │   └── task-example-omnichannel-routing.md  the golden-solution standard reviewers judge against
│   └── workflow.md                  orientation only; the review procedure is prompts/review.md
│
├── refinement/                      ← fixing a returned task (Hazy Refinery)
│   ├── README.md                    the loop, and the rules that bite
│   └── platform/                    ← AUTHORITATIVE captures (Refinery page, 2026-09-10)
│       └── submission-guidelines.md     step-by-step submission guide
│
├── rules.md                         ← GENERATED from the check registry: one line per check id
│
└── reference/                       ← this repo's own corpora, not platform documents
    ├── llm-prose-tells.md           prose classes the style guide lacks (feeds coded check A10)
    ├── reviewer-feedback-corpus.md  verbatim reviewer notes, tasks 01–48
    ├── workflow-history.md          dated build lessons relocated from workflows 01-07 (2026-09-11)
    ├── tools-refactor-plan.md       execution record of the 2026-09-04 gcheck refactor
    └── autoeval-check-catalog-archive.md   archived monolith docstring, superseded by rules.md
```

Tool usage (the package sequence, the gate, the review harness) is documented in
`../tools/README.md`, not here; `rules.md` is regenerated from `tools/gcheck/` and is the
place to cite a check id from.

## Where to start

### Submitting

| If you want to… | Read |
| --- | --- |
| Understand the program and the quality bar | `submission/platform/welcome.md`, then `project-guidelines-v5.1.md` |
| See every gate a submission must clear | `submission/platform/task-lifecycle.md` |
| Decide what to build | `submission/workflows/01-ideation.md` |
| Check an idea for uniqueness | `submission/platform/wholesale-trade-uniqueness-map.md` |
| Build prompt / inputs / golden / rubric / metadata | `submission/workflows/02`–`06` |
| Screen files for LLM tells | `submission/platform/style-guide-llm-tells.md` |
| Self-audit before submitting | `submission/workflows/07-pre-submission-audit.md` |
| Read auto-eval feedback or rebut a flag | `submission/platform/auto-eval-feedback-guide.md` |

### Reviewing

| If you want to… | Read |
| --- | --- |
| Know what you are actually required to check | `reviewer/platform/reviewer-guidelines-v5.1.md` |
| Convert LLM tells into a verdict | `reviewer/platform/reviewer-rubric.md` |
| Write the revision note | `reviewer/platform/feedback-best-practices.md` |
| Run a review end to end | **`/review-task <review-id>`** — `prompts/review.md` (+ `tools/review_check.py`); `reviewer/workflow.md` is orientation only |
| Know exactly what the form asks for | `reviewer/platform/platform-review-form.md` |
| See the standard a golden solution is judged against | `reviewer/platform/task-example-omnichannel-routing.md` |

### Refining

| If you want to… | Read |
| --- | --- |
| Run a refinement end to end | **`/refine-task <uid>`** — `prompts/refine-task.md`, `refinement/README.md` (+ `tools/fetch_refinement.py`) |
| Know what the Refinery page requires, step by step | `refinement/platform/submission-guidelines.md` |
| See the rules that most often trip a refinement | `refinement/README.md` |

## Key facts

**Authoring.** Rubric band 15–60 criteria (aim 15–25), per
`submission/platform/project-guidelines-v5.1.md#rubric`. The difficulty rule (pass when the
worst-agent accuracy is ≤ 80%) is stated in
`submission/platform/auto-eval-feedback-guide.md#the-difficulty-check-accuracy-percentages`;
cite it there rather than restating it. The golden solution check runs three agents and needs
1.0000 from all three. LLM assistance
on input files is permitted, provided the result is indistinguishable from a real workplace
document, carries no style-guide tell, and never leaks the answer.

**Review.** A reviewer spot-checks only 2–3 rubric criteria against the golden. The captures
disagree on how many revision rounds an EC gets (one in reviewer-rubric.md, four in
feedback-best-practices.md, five total reviews in task-lifecycle.md), so build as if the
first review is the only one. Reviewers may fix small things themselves, but **input
files are locked and can never be edited**, so every input defect routes to Needs Revision
regardless of size. Bounded subjective criteria are explicitly valid and must not be sent
back for being subjective.
