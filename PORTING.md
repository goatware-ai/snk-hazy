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

**b. Assigned sector.** Everything ported says Wholesale Trade, because that is Geranium's
assignment. If Hazy is assigned a different sector, these are the files that state it
outside the verbatim platform captures:

| File | Line | What it says |
|---|---|---|
| `.claude/commands/review-task.md` | 2 | `(Wholesale Trade)` in the command description |
| `prompts/review.md` | 8, 99 | assigned sector, and the prompt-read test |
| `prompts/submission.md` | 9 | assigned sector |
| `memory/task-metadata.md` | 15 | the `sector` field of the metadata template |
| `memory/onet-occupation-routing.md` | 3, 8 | the occupation routing table |
| `docs/reviewer/workflow.md` | 6 | assigned sector |
| `docs/README.md` | 12 | assigned sector |
| `docs/submission/workflows/02-prompt-writing.md` | 115 | the industry filter |

**c. Re-capture the platform docs.** See section 4.

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

## 4. The platform captures still say Geranium, on purpose

Everything under `docs/submission/platform/`, `docs/reviewer/platform/`,
`docs/refinement/platform/` and `docs/reference/` is captured verbatim from the Snorkel
platform and from real reviewer feedback. Rewriting a verbatim capture would falsify the
record, so those eleven files were left exactly as captured:

```
docs/submission/platform/{welcome,project-guidelines-v5.1,task-lifecycle,
                          style-guide-llm-tells,platform-submission-form,
                          wholesale-trade-uniqueness-map}.md
docs/reviewer/platform/reviewer-guidelines-v5.1.md
docs/refinement/platform/submission-guidelines.md
docs/reference/{autoeval-check-catalog-archive,llm-prose-tells,
                reviewer-feedback-corpus}.md
```

Re-capture them from Hazy's own platform pages. Until then they are Geranium's rules, which
are probably close but are not authoritative for this desk. The uniqueness map in
particular is a list of asks already accepted **in Geranium**, so it cannot tell you
whether a Hazy task is unique.

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
