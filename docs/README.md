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

This desk was ported from Project Geranium (Wholesale Trade) on 2026-09-21.
`RULE-DELTAS.md` records every rule that changed and is the reference for anything that
still reads as Geranium's. Material inherited from Geranium and not yet confirmed against
Hazy's platform carries a banner saying so; do not trust it until an assignment confirms it.

---

## Layout

```
docs/
├── README.md                        ← this file
├── RULE-DELTAS.md                   ← what changed in the Geranium→Hazy port (D0–D13)
│
├── submission/                      ← authoring a task (the whole job, for now)
│   ├── platform/                    ← AUTHORITATIVE captures
│   │   ├── platform-submission-form.md      the live form, section by section — TOP AUTHORITY
│   │   ├── create-the-task-guidelines.md    the guidelines PDF; §0 holds the solution conflict
│   │   ├── domains-and-occupations.md       the closed 14-domain / 64-occupation lists
│   │   ├── onet-codes.md                    verified codes, job families, and the four traps
│   │   ├── creating-input-files.md          authenticity, LLM-assist policy, leakage  [inherited]
│   │   ├── style-guide-llm-tells.md         severity-keyed LLM tell tables            [inherited]
│   │   ├── task-lifecycle.md                Geranium's stages after submit            [inherited]
│   │   └── auto-eval-feedback-guide.md      Geranium's auto-eval boxes                [inherited]
│   └── workflows/                   ← our decomposition, one stage per file
│       ├── 01-ideation.md           pick a domain, occupation and a task worth building
│       ├── 02-prompt-writing.md     house prompt rules (P4/P6/A20)
│       ├── 03-input-files.md        authenticity, distributed difficulty, leakage, packaging
│       ├── 04-golden-solution.md    the ground truth the rubric is built from
│       ├── 05-rubric.md             6 minimum / 20+ expected; weights −5..+5; the closing row
│       ├── 06-metadata.md           the form's fields: domain, occupation, times, tools
│       └── 07-pre-submission-audit.md   package sequence, then the form's 14-box checklist
│
├── reviewer/                        ← INHERITED, unverified: Hazy offers no review tasks
│   ├── platform/                        Geranium's Reviewers' Hub captures
│   └── workflow.md                      orientation only
│
├── refinement/                      ← INHERITED, unverified: Hazy has no Refinery node
│   ├── README.md
│   └── platform/submission-guidelines.md
│
├── rules.md                         ← GENERATED from the check registry: one line per check id
│
└── reference/                       ← this repo's own corpora, not platform documents
    ├── llm-prose-tells.md           prose classes the style guide lacks (feeds check A10)
    ├── reviewer-feedback-corpus.md  verbatim Geranium reviewer notes            [inherited]
    ├── workflow-history.md          dated build lessons relocated from workflows 01-07
    ├── tools-refactor-plan.md       execution record of the 2026-09-04 gcheck refactor
    └── autoeval-check-catalog-archive.md   archived monolith docstring, superseded by rules.md
```

## Reading order for a new task

1. `submission/platform/domains-and-occupations.md` — pick the occupation, then the domain.
2. `submission/platform/onet-codes.md` — confirm the code. Eight are detail codes ending
   `.01` to `.04`, and the four First-Line Supervisor rows are not Management.
3. `submission/workflows/01-ideation.md` through `07-pre-submission-audit.md`.
4. `submission/platform/platform-submission-form.md` — the 14-box checklist, before you
   submit anything.

## What is generated, and from where

`rules.md` is regenerated from `tools/gcheck/` by `autoeval_check.py --rules` and is the
place to cite a check id from. Regenerate it after any check or family change, or it will
state a band the gate no longer enforces. Tool usage — the package sequence, the gate, the
harnesses — is documented in `../tools/README.md`, not here.
