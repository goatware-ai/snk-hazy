# Project Hazy — Documentation

Local documentation for **Hazy_Task_Creation**, Snorkel's task-authoring project
(`cda2e943-8524-45f0-a966-469903337102`). The desk's job here is to **author** task
packages: an instruction, input files, a completed solution and a rubric.

Inside `submission/`, the `platform/` subdirectory holds documents captured from Snorkel's
own pages. **Those captures are authoritative** — on any conflict with a workflow page, a
tool, or anything else in this repo, the capture wins. Everything outside `platform/` is
this repo's own derived working material.

Two things govern above everything else:

1. **The live form beats the guidelines PDF.** The form is what blocks submission. The one
   known disagreement between them is whether the author produces a solution; the form
   requires one. See `submission/platform/create-the-task-guidelines.md` section 0.
2. **There is no fixed sector.** Each task picks one of 14 domains and one of 64
   occupations from a closed list. See `submission/platform/domains-and-occupations.md`.

The pipeline is short: fill the form's five sections, tick its fourteen-box checklist,
submit. Two captures, `creating-input-files.md` and `style-guide-llm-tells.md`, carry a
banner saying they were carried over from the desk this repo was built from and are not yet
confirmed here; their guidance is domain-agnostic, but do not treat their specifics as this
project's rules until an assignment confirms them.

---

## Layout

```
docs/
├── README.md                        ← this file
│
├── submission/                      ← authoring a task (the whole job)
│   ├── platform/                    ← AUTHORITATIVE captures
│   │   ├── platform-submission-form.md      the live form, section by section — TOP AUTHORITY
│   │   ├── create-the-task-guidelines.md    the guidelines PDF; §0 holds the solution conflict
│   │   ├── domains-and-occupations.md       the closed 14-domain / 64-occupation lists
│   │   ├── onet-codes.md                    verified codes, job families, and the four traps
│   │   ├── creating-input-files.md          authenticity, LLM-assist policy, leakage
│   │   └── style-guide-llm-tells.md         severity-keyed LLM tell tables
│   └── workflows/                   ← our decomposition, one stage per file
│       ├── 01-ideation.md           pick a domain, occupation and a task worth building
│       ├── 02-prompt-writing.md     house prompt rules (P4/P6/A20)
│       ├── 03-input-files.md        authenticity, distributed difficulty, leakage, packaging
│       ├── 04-golden-solution.md    the ground truth the rubric is built from
│       ├── 05-rubric.md             6 minimum / 20+ expected; weights −5..+5; the closing row
│       ├── 06-metadata.md           the form's fields: domain, occupation, times, tools
│       ├── 07-pre-submission-audit.md   package sequence, then the form's 14-box checklist
│       └── 08-form-payload-and-submit.md the payload schema, filling the form, submitting
│
├── rules.md                         ← GENERATED from the check registry: one line per check id
│
└── reference/                       ← this repo's own corpora, not platform documents
    └── llm-prose-tells.md           prose classes the style guide lacks (feeds check A10)
```

## Reading order for a new task

1. `submission/platform/domains-and-occupations.md` — pick the occupation, then the domain.
2. `submission/platform/onet-codes.md` — confirm the code. Eight are detail codes ending
   `.01` to `.04`, and the four First-Line Supervisor rows are not Management.
3. `submission/workflows/01-ideation.md` through `08-form-payload-and-submit.md`.
4. `submission/platform/platform-submission-form.md` — the 14-box checklist, before you
   submit anything.

## What is generated, and from where

`form-payload.json` is generated per task by `tools/form_payload.py` from that task's own
metadata, prompt, rubric and folders. It is what the Hazy Helper extension fills the form
from; its schema is in `submission/workflows/08-form-payload-and-submit.md`.

`rules.md` is regenerated from `tools/gcheck/` by `autoeval_check.py --rules` and is the
place to cite a check id from. Regenerate it after any check or family change, or it will
state a band the gate no longer enforces. Tool usage — the package sequence, the gate, the
harnesses — is documented in `../tools/README.md`, not here.

## Open questions

Two things the captures do not settle. Both are open until an assignment or a platform page
answers them.

1. **Nothing confirms that this project runs an automated evaluation after submission.**
   The form's three in-form check panels are advisory and block nothing, and each section
   ends in a Run Evaluations button, so evaluations run at submit time; what happens to a
   submission afterwards is not documented anywhere available to this desk. Three checks
   (R24, R73, R129) only make sense against a post-submission auto-eval and should be
   dropped if there is none.
2. **No prompt-length or criterion-length cap is documented.** Neither platform document
   mentions one. R1 still rejects a criterion over 500 characters, but it now says so as a
   house rule rather than citing a form cap that no capture carries. Raise or drop that
   number freely; the reason to keep it is that the form asks for one thing per line.
