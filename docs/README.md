# Project Hazy: Documentation

Local documentation for **Hazy_Task_Creation**, Snorkel's task-authoring project
(`cda2e943-8524-45f0-a966-469903337102`). The desk's job here is to **author** task
packages: an instruction, input files, a completed solution and a rubric. There is no fixed
sector: each task picks one of 14 domains and one of 64 occupations from a closed list
(`submission/platform/domains-and-occupations.md`).

## What governs, in order

1. **The platform captures** in `submission/platform/`, led by
   `platform-submission-form.md`. The form is what blocks submission, and where it speaks it
   governs. Two captures, `creating-input-files.md` and `style-guide-llm-tells.md`, carry a
   banner: they were carried over from the desk this repo was built from and are not yet
   confirmed here, so their guidance is used but their specifics yield to the form.
2. **`submission/house-rules.md`**: this desk's own standards for what the form leaves
   unsaid. None of them is a platform requirement, and each can be changed by deciding to.
3. **`submission/difficulty.md`**: how a task is made hard enough for the reviewer.
4. **`submission/workflows/`**: the build order, one stage per file. Each topic has one home
   there and other pages point to it rather than restating it.
5. **`rules.md`**: one line per coded check, generated from `tools/gcheck/`. Cite check ids
   from here; where a workflow page states a count, a band or a weight range, the page
   governs.

The build and revision prompts that drive a session are in `../prompts/`: `submission.md`
(one task), `create-task-brief.md` (a batch of drafts) and `revise-task.md` (a return).

## How the platform judges a task

- **In the form.** Each of the five sections ends in **Run Evaluations and Continue** and
  the last in **Run Evaluations and Submit**. The three "Checks (optional)" panels (Task
  Instruction, Completed Task, Task Rubric) are advisory and block nothing, so a clean panel
  proves nothing. What blocks is the fourteen-box **Before You Submit** checklist: every box
  must be true of the package before it is checked (`workflows/07-pre-submission-audit.md`,
  section I).
- **After submitting.** The evaluations seen on this project's returns, read with
  `tools/fetch_feedback.py`, are a file-readability pass, `prompt_completeness`,
  `input_sufficiency` and the Hazy difficulty check (two weak models, four attempts each; one
  PASS on any attempt fails the task; an INCOMPLETE with no PASS is a runner error and goes
  back unchanged). The visible note is often one sentence or empty; the fetched JSON carries
  the detail.
- **The reviewer.** A human reviewer reads the task after the evaluations, and holds a higher
  difficulty bar than the automated check (`submission/difficulty.md`).

## Layout

```
docs/
├── README.md                        ← this file
├── rules.md                         ← GENERATED from the check registry: one line per check id
├── submission/                      ← authoring a task (the whole job)
│   ├── platform/                    ← AUTHORITATIVE captures
│   │   ├── platform-submission-form.md      the live form, section by section: TOP AUTHORITY
│   │   ├── domains-and-occupations.md       the closed 14-domain / 64-occupation lists
│   │   ├── onet-codes.md                    verified codes, job families, and the four traps
│   │   ├── creating-input-files.md          authenticity, LLM-assist policy, leakage (carried over)
│   │   └── style-guide-llm-tells.md         severity-keyed LLM tell tables (carried over)
│   ├── house-rules.md               ← this desk's own standards beyond the form
│   ├── difficulty.md                ← making a task hard: root causes, design read, hardening catalog
│   └── workflows/                   ← the build order, one stage per file
│       ├── 01-ideation.md           domain, occupation, a concept worth building, uniqueness
│       ├── 02-prompt-writing.md     the prompt: the form's six asks, the P-rules, overspecification
│       ├── 03-input-files.md        authenticity, tells, leakage, input-side difficulty, packaging
│       ├── 04-golden-solution.md    the ground truth, the literal read, verify_golden.py, live caches
│       ├── 05-rubric.md             count, weights, negatives, rubric shape, how judges read
│       ├── 06-metadata.md           metadata.json, the domain/occupation fields, tools, times
│       ├── 07-pre-submission-audit.md   THE package sequence, the audit table, the 14 boxes
│       └── 08-fill-the-form-and-submit.md   filling the form from metadata.json, submitting
└── reference/                       ← this repo's own corpora, not platform documents
    └── llm-prose-tells.md           prose classes the style guide lacks (feeds check A10)
```

## Reading order for a new task

1. `submission/platform/platform-submission-form.md`, in full.
2. `submission/house-rules.md` and `submission/difficulty.md`.
3. `submission/platform/domains-and-occupations.md` and `onet-codes.md`: pick the
   occupation, then the domain, then confirm the code.
4. `submission/workflows/01-ideation.md` through `08-fill-the-form-and-submit.md`.

## What is generated, and from where

Each task's `metadata.json` carries the submission form's fields as well as the build
record, folded in by `tools/sync_metadata.py` from `form-lists.md`, `instruction.md` and the
rubric CSV. It is the one file the browser helper fills the form from; its shape is in
`submission/workflows/08-fill-the-form-and-submit.md`.

`rules.md` is regenerated from `tools/gcheck/` by `autoeval_check.py --rules`. Regenerate it
after any check or family change, or it will state a band the gate no longer enforces. Tool
usage is documented in `../tools/README.md`.

## Open questions

1. **Several coded checks were written for evaluations seen on the earlier desk and not yet
   seen here.** `rules.md` stage 2 lists a three-run `golden_solution_check` and an
   `llm_authorship_check`; neither has appeared in this project's fetched returns. The checks
   built for them (R24, R73, R129 and the GOLD-* and LLM-* families) still run and still
   protect a sound package, but a finding from them is evidence of an earlier platform's
   rule, not this one's.
2. **No prompt-length or criterion-length cap is documented.** Neither platform document
   mentions one. R1 rejects a criterion over 500 characters as a house rule; raise or drop
   that number freely, the reason to keep it being that the form asks for one thing per line.
