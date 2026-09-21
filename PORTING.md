# Porting notes — Hazy desk, forked from Geranium

Ported 2026-09-21 from `../geranium`. This file records what came across, what was
deliberately left behind, what was rewritten, and the short list of things that must be
settled before the desk is used. Delete it once the desk is live and the open items below
are closed.

---

## 1. Open items

**a. Project node ids — production resolved 2026-09-21, Refinery still open.**
`PROJECT_ID` is set to `cda2e943-8524-45f0-a966-469903337102`, verified against the
platform as `Hazy_Task_Creation`. A dry run of `/fetch-status` reached it and charted the
one OFFERED submission on the board, so the submissions, reviews and reconciliation paths
all work.

The Refinery node is a separate question and is **still open**:

```python
REFINE_PROJECT_ID = "TODO-HAZY-REFINEMENT-PROJECT-ID"
```

Hazy has no Refinery node that this account can see, and `stb projects list` shows only
Geranium-Production, since it lists just the projects enabled for AI credentials. So the
placeholder is left in place and the behaviour was changed to match: only `PROJECT_ID`
blocks the run now, and while `REFINE_PROJECT_ID` is unset `run_refinements_cli()` returns
early, so the refinement chart and `refinement-list.md` are skipped rather than failing.
Set it if and when a Refinery node is assigned. Nothing else needs to change.

Note that `/refine-task` and `/revise-refinement`, and `tools/fetch_refinement.py`, address
a refinement by its own UID and do not read `REFINE_PROJECT_ID`, so they work without it.

**b. Assigned sector — RESOLVED 2026-09-21.** Hazy has no fixed sector. The form offers a
closed list of **14 domains and 64 occupations**, chosen per task. Both lists are captured
in `docs/submission/platform/domains-and-occupations.md`, and every code was verified
against onetonline.org in `onet-codes.md`. Only two of Geranium's six Wholesale Trade
occupations survive, so most Geranium task ideas cannot be resubmitted here.

**c. Re-capture the platform docs — DONE for the two that matter.** The guidelines PDF
and the live form are now captured. Four Geranium documents remain inherited and
unverified; see section 4.

---

## 2. What came across

| Folder | Contents |
|---|---|
| `.claude/` | 5 slash commands, 9 skills, `settings.json` permissions |
| `docs/` | 34 documents: the three workflows, platform captures, reference material |
| `prompts/` | the 6 authoring, review, refinement and revision prompts |
| `tools/` | the full gate: 48 modules, `gcheck/` check packages, 5 fixtures, the rubric-filler extension |
| `memory/` | 27 memory files plus `MEMORY.md` |
| `requirements.txt` | new — pins the 13 direct dependencies to the versions Geranium ran |

Empty working folders were created because the tooling resolves paths against them:
`submissions/`, `accepted/`, `archived/`, `drafts/`, `refinements/`, `reviews/`.

`memory/` is symlinked from `~/.claude/projects/-Users-aladdin-projects-snk-hazy/memory`,
matching Geranium's convention, so the ported memory is live in this project's sessions.

**Verified after porting:** 48 of 48 tool modules import, all 5 gate fixtures pass, and
every CLI entrypoint responds.

```
5 of 5 fixtures pass; 12 of 257 check codes carry a fixture assertion
```

## 3. What was left behind

No task material came across, per the porting request: `accepted/`, `archived/`,
`drafts/`, `refinements/`, `reviews/`, the three tracking lists (`submission-list.md`,
`refinement-list.md`, `reviews-list.md`), `.tmp-office/`, `.venv/`, `.git/` and
`fetch-status/history.jsonl`. The tracking lists are written by `/fetch-status` itself
from a built-in skeleton, so they will appear on the first successful run.

This folder is not a git repository. `.gitignore` came across ready for one, but
initialising and committing is left to you.

## 3b. The 2026-09-21 rules pass

The two source documents were captured and every rule they changed was applied across the
docs, prompts, memory and the gate. `docs/RULE-DELTAS.md` is the record, D0 to D13, and is
the reference for anything that still reads as Geranium's.

The one finding worth knowing before anything else: **the guidelines PDF and the live form
contradict each other on whether the author writes a solution.** The PDF says three times
that they do not. The form has a required Completed Task Upload and builds the rubric from
it. The form blocks submission, so the form wins and this desk builds a golden solution.
Recorded in `create-the-task-guidelines.md` section 0 and `memory/golden-solution-required.md`.

What changed in the gate:

| Check | Change |
|---|---|
| R67 | **Deleted.** It reserved negative weight for four critical classes; the form invites negatives on ordinary quality misses. |
| R11 | Rebanded: floor 6, recommend 20, **no ceiling** (was 15-60). |
| R12 | Weights are any non-zero integer -5..+5 (was +1..+5 or -3..-5, with -1 and -2 rejected). |
| M1-M3 | Rewritten around the closed domain/occupation lists (was a 200-line Wholesale Trade prompt-fit table). |
| M4-M6 | **New:** the form's five time values, its non-AI tool list, and the 2-file input minimum. |
| R135 | **New:** the rubric must END with the "Overall formatting and style of the deliverable" criterion. |
| R136 | **New:** no hedged figures; values come from the ground truth. |
| R24/R73/R129 | Kept, but their absolute point totals were Geranium arithmetic and are gone; the bars are shares, which survive a 20-60+ rubric. Marked unverified. |
| P4/P6 | Expert-context vocabulary widened from wholesale-only to all 13 occupation families. |

261 coded checks, up from 257. Five Geranium documents and two memory files were deleted as
superseded or unfirable. `docs/rules.md` was regenerated.

Two things to settle when the first Hazy result comes back:

1. Whether Hazy runs Geranium's ten named post-submission auto-evals at all. Nothing
   confirms it. R24, R73 and R129 depend on one of them and should be dropped if it does
   not run.
2. Whether the prompt-length and criterion-length caps Geranium's form enforced exist here.
   Neither Hazy source mentions them, so they were removed rather than assumed.

## 4. The platform captures still say Geranium, on purpose

Everything under `docs/submission/platform/`, `docs/reviewer/platform/`,
`docs/refinement/platform/` and `docs/reference/` is captured verbatim from the Snorkel
platform and from real reviewer feedback. Five were deleted in the rules pass as superseded
or sector-wrong: Geranium's welcome page, its project guidelines v5.1, its Wholesale Trade
occupation table, its Wholesale Trade worked example, and its uniqueness map.

What remains from Geranium now carries a banner saying it is inherited and unverified:

```
docs/submission/platform/{creating-input-files,style-guide-llm-tells,
                          task-lifecycle,auto-eval-feedback-guide}.md
docs/reviewer/**                     (Hazy offers no review assignments)
docs/refinement/**                   (Hazy has no Refinery node)
docs/reference/{autoeval-check-catalog-archive,reviewer-feedback-corpus,
                workflow-history}.md
prompts/{review,refine-task,revise-refinement}.md
.claude/commands/{review-task,refine-task,revise-refinement}.md
```

The first four are domain-agnostic craft guidance and the Hazy documents restate their
rules, so they are safe to work from. The rest describe workflows that do not exist on this
project yet. Do not trust any of it on sector, rubric bands or platform checks.

Four names correctly keep the Geranium spelling everywhere, because they belong to
Snorkel's side rather than to this repo: the Slack channel `#ec-geranium-project`, the
autoeval check `geranium_safety_check`, the same check as `geranium_safety` in a results
list, and the expert-docs URL `expertdocs.snorkel-ai.com/geranium-production-1`. Confirm
each still applies to Hazy.

## 5. Code changes made during the port

**The codename canary now screens both names.** The platform's Name Check forbids the
programme codename anywhere in a shipped package. Three modules each carried their own
`geranium` regex; they now share one pattern defined in `tools/gcheck/common.py`:

```python
CODENAME_PATTERN = r"geranium|(?<![a-z])hazy(?![a-z])"
```

Both names are screened because this desk carries Geranium vocabulary through every ported
doc, prompt and worked example, so an author echoing one of them leaks the old codename
just as fatally as the new one. The lookarounds are used instead of `\b` so that
`HAZY_TASK_CREATION` trips while `hazier` does not. `tools/gcheck/packaging/hygiene.py`,
`tools/gcheck/golden_rubric/leakage.py` and `tools/gcheck/authorship/package.py` import it.

Two caveats. If Hazy is not in fact the platform-side codename, drop that alternative in
`common.py` and nowhere else. And `hazy` is an ordinary English word, so a genuine
"hazy finish" in a coating spec will trip H1; that is the intended trade, since a false
positive costs a reword and a false negative costs a platform cycle.

**`GERANIUM_ROOT` is now `HAZY_ROOT`**, renamed together across its one setter
(`gcheck/golden_rubric/conformance.py`) and four readers (`tools/golden_verify.py`,
`tools/templates/verify_golden.py`, two fixtures) so the pair still agrees. The variable
appears in the `verify_golden.py` that sits at task-folder root; `.py` is not in the H1
sweep's suffix list, so it was never a canary risk either way.

**Local identity renamed Geranium to Hazy** across commands, skills, prompts, tool
docstrings, `tools/README.md`, `memory/`, `docs/README.md`, `docs/reviewer/workflow.md`
and `docs/refinement/README.md`, with the four platform names in section 4 masked out of
the rename. This includes the session and memory paths, which now read
`-Users-aladdin-projects-snk-hazy`.

## 6. Worth knowing

The occupation checks in `tools/gcheck/prompt_inputs/occupation.py` are keyed to six
O*NET codes, all Wholesale Trade:

```
11-2022.00  11-3061.00  11-3071.00  13-1022.00  41-4012.00  43-5071.00
```

Each check fires only when the task's metadata carries its code. Under a different sector
they stay silent rather than failing wrongly, so the gate degrades safely, but M1 through
M3 will protect nothing until the table is rebuilt for Hazy's occupations. The same
applies to the prompt-frame vocabulary in `tools/gcheck/prompt_inputs/prompt_frame.py`.

The gate fixtures under `tools/check_fixtures/` are built from a Wholesale Trade freight
audit. They test the checking machinery rather than the sector, so they stay valid and
passing whatever Hazy's sector turns out to be.
