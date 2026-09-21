# Workflow 07 — Pre-Submission Audit

One row per gate. Walk every row against what you actually built, in order, and fix
failures before submitting, since a failed gate means the submission is sent back. Modeled on
the checklists in `../platform/project-guidelines-v5.1.md#pre-submission-checklist` and
the lifecycle in `../platform/task-lifecycle.md`; on any conflict, the platform captures
win.

The **Check** column names the registry id that codes the row (one line per id in
`../../rules.md`; the code is under `tools/gcheck/`), or **MANUAL** when no check codes it
and the row is a read. A coded row is not a substitute for the read: the checks are pattern
nets, and every MANUAL row is a rejection that has happened.

## Package sequence

Run once, in this order, after every file is final and before every zip build:

1. `.venv/bin/python tools/office_resave.py <folder> --force` (a genuine Word/Excel save
   replaces the python library's application stamp; `--force` because a python-docx
   default app.xml reads as already clean)
2. `.venv/bin/python tools/fix_floats.py fix <workbook>` on every workbook (Excel
   reintroduces float artifacts on save, so this runs after the resave)
3. `.venv/bin/python tools/fix_metadata.py <folder>` (syncs stamps and mtimes after the
   content is final)
4. Rebuild `i-<task-name>.zip` and `s-<task-name>.zip`
5. `.venv/bin/python tools/autoeval_check.py <folder>`

Step 5 is the audit: it runs every coded row below and prints the findings by family. Any
row it cannot see is MANUAL here. Record a check the operator has ruled non-blocking in the
folder's `.gate-debt`, never by editing the check.

## A. Concept & difficulty

| Check | Gate | What it verifies | How to pass |
| --- | --- | --- | --- |
| MANUAL | `three_hour_floor` | Workflow takes ≥3 hours by hand without an LLM | Design for 5+; recount where the hours go; below 3 → redesign |
| MANUAL | `frontier_resistance` | The difficulty check passes only when the worst-agent accuracy is ≤ 80% (`../platform/auto-eval-feedback-guide.md#the-difficulty-check-accuracy-percentages`) | Run the prompt through a model; if output needs no meaningful edits, harden the task; aim both models under 80 |
| MANUAL | `difficulty_in_files` | Difficulty comes from input files + reasoning, not the prompt | Confirm the task is unanswerable without opening the attachments |
| P4 | `us_grounding` | The opening names the state or the US, the requester's role, and the expertise the reader brings | `02-prompt-writing.md#the-opening-frame-p4-p6` |

## B. Prompt

| Check | Gate | What it verifies | How to pass |
| --- | --- | --- | --- |
| A10, P7 | `natural_voice` | Written by you; none of the reviewer-flagged prose shapes; no three sentences opening on the same stem | Read aloud; `../../reference/llm-prose-tells.md` |
| P6 | `expert_context` | The P4 frame is woven into the ask, never a self-introduction to a coworker | `02-prompt-writing.md#the-opening-frame-p4-p6` |
| A20 | `comma_rules` | A comma before a clause-joining conjunction; never three clauses in one sentence | `02-prompt-writing.md#sentence-mechanics-a20`; the serial comma is a read |
| P1 | `output_named` | One output file named, with a naming cue that makes it the deliverable | Name it exactly as the solution zip delivers it |
| P2, P3 | `inputs_referenced` | Every input file named in the narrative; no inventory paragraph | Weave the names into the opening paragraph |
| P5 | `no_file_glosses` | At most one or two files carry a purpose gloss | Name what each file contains, not what it is for |
| MANUAL | `not_overspecified` | No pitfall warnings, derived parameters, section outlines or decision frameworks from an input | `02-prompt-writing.md#overspecification-giveaways-beyond-step-by-step` |
| MANUAL | `self_contained` | No proprietary tools or logins required | Replace or remove any such dependency |
| MANUAL | `verifiable` | Objectively gradable against a known correct answer | If no correct answer (or nameable conditions) exists, redesign |
| MANUAL | `prompt_language` | No spelling or grammar errors; under 3,000 characters | Spell-check; count |

## C. Input files

| Check | Gate | What it verifies | How to pass |
| --- | --- | --- | --- |
| A11, A12 | `substantial_files` | Prose inputs clear the word floor; no thin or placeholder file | Grow or cut thin files; every file load-bearing |
| G2b | `authentic_files` | No package-level batch-construction evidence (generator string, one shared write instant, identical docx components, shared rsids) | Rebuild from sanitized real material; the Office re-save in the package sequence |
| A15, F1, H2, H3, A1, A6 | `no_fabrication_tells` | No number series without variance, float dust, 555 phones, calendar-false weekday/date pairs, LLM-blue fills, em dashes | Inject real variance; use plausible specific values; `../platform/creating-input-files.md#3-the-fingerprints-to-keep-out` |
| MANUAL | `rights_clean` | No paywalled, copyrighted, restricted, or employer-owned content | Remove or replace with material you may distribute |
| L1, L3, L4 | `no_giveaways` | No input paragraph enumerating the answer set, handing over a stay verdict or naming the members of a listed set; no notes columns revealing what the solver should deduce | Delete them |
| R23 | `term_dates_carried` | A firm-price or validity date stated in an input is carried by the golden | Carry it or remove it |
| G22 | `cutoff_chronology` | No snapshot dated before records it references; no stated balance an input reproduces only without the date cutoff | Re-key every date-gated figure on the input's own date column |
| H4 | `zip_hygiene_inputs` | Single flat zip; no subfolders, empty files, spaces, or double extensions | Unzip once and inspect before submitting |
| H5 | `names_match_prompt` | Every file the prompt names exists with that exact name | Fix names on whichever side is wrong |
| A14, A3, A13 | `package_provenance` | docProps names the application that really wrote the file, never a python library; plausible creator and stamps; a calcChain Excel would write | The package sequence above; the generator string is evidence, cleared only by a genuine save (`memory/package-hygiene-pipeline.md`) |

## D. Golden solution

| Check | Gate | What it verifies | How to pass |
| --- | --- | --- | --- |
| MANUAL | `complete_answer` | Every part of the prompt answered; fact-checked | Walk the prompt line by line against the deliverable |
| MANUAL | `scores_100` | Golden solution scores ~100 on the rubric | Fix the solution or the rubric, whichever is wrong |
| MANUAL | `human_edited` | Mostly human-edited | If a model draft needed no meaningful edits, the task fails `frontier_resistance` too |
| A1, A2, A5, A6, A10 | `client_ready` | No LLM-blue fills, datetime-formatted date cells, paste walls, em dashes or flagged prose shapes | Apply the formatting standards in `../platform/project-guidelines-v5.1.md#golden-solution` |
| A9, A13, A17 | `live_formulas` | Formulas live, every cache reproducible by its own formula, calcChain present | Rebuild calculations as formulas; `06-metadata.md#house-notes-on-platform-submission-formmd` |
| G8 | `signable_document` | When the prompt says a document is signed, the golden carries it with a signature line | Add the document, not a table about it |
| G9 | `dateline_before_actions` | The deliverable is not dated later than an action it schedules as done | Date the deliverable the day the work is done |
| G10 | `cited_identifiers` | Every invoice, PO, serial or work-order id the golden cites exists in a shipped input | Look each one up in the input at the moment of writing |
| G18, G20 | `dates_anchored` | Every owner-dated action row and every full date in the prose is written in an input or the prompt | Carry the date in an input, show the derivation, or leave it off |
| G19 | `direction_claims` | Every "X moves up/down" claim agrees with the correction column | Re-read per-person prose against the tabs |
| G1, G5, G7, G21 | `internal_consistency` | No stays-as-placed status beside a change; prose counts match the tabs; docx total rows tie; displayed ratios re-derive from displayed figures | Cross-read all three side by side; one mismatch is a send-back |
| G11, G12, G13, G14, G15, G16, G17 | `sourced_from_inputs` | Attributed dates, input conditions, unit costs, dispute entities, owner and author names and header titles all stand in an input or the prompt | Re-derive every figure and name from the shipped inputs |
| H5 | `output_name_match` | Output file name matches the prompt | Fix whichever side is wrong |
| A16 | `opens_cleanly` | Every package parses; no XML errors, repair prompts, or corruption | Re-open every file from the zipped copy |
| H4 | `zip_hygiene_solution` | Flat zip; no subfolders or empty files; no spaces or double extensions | Unzip once and inspect |
| L2 | `no_revision_residue` | No tracked changes, comments, hidden sheets, rows or columns | Unhide, review, strip |

## E. Rubric

| Check | Gate | What it verifies | How to pass |
| --- | --- | --- | --- |
| R11 | `criterion_count` | 15–60 criteria (target 15–25; band per `../platform/project-guidelines-v5.1.md#rubric`) | Split or merge to range |
| R55, R27, R49, R54, R85 | `atomic_specific` | One simple atomic sentence per criterion; no bundles, stacked clauses or second subjects | Split bundles |
| R20, R21, R82 | `figures_land` | Every stated figure lands on the golden, written to the cent with a $ mark | Add the exact correct values where the golden holds them |
| R4, R13, R101, R102 | `coverage` | Every prompt instruction, front-page block and addressee has a criterion | Map prompt requirements → criteria; fill gaps |
| R18, R19, R25 | `rigid_vs_subjective` | No grader instructions, unanchored hedges or evaluative terms; subjective rows name their conditions | Reclassify and rewrite any vague criterion |
| R67, R84, R53 | `two_negatives` | ≥2 negatives, each on a critical class (safety, privacy, inverted decision, fabrication), framed inside the sentence, one negation | `05-rubric.md#house-rules-on-top-of-the-capture` |
| E1, W18 | `affirmative_negatives` | Negative criteria read TRUE when the failure is present | Remove "does not / fails to / is missing" phrasing |
| R33, R37, R52 | `negatives_scoped` | No universal, threshold or membership negative the golden's own rows violate | Test each negative against every row class of the golden |
| MANUAL | `style_caps` | Style/formatting criteria < half of count and ≤ ¼ of total reward | Cut or down-weight style rows |
| R83 | `file_name_criterion` | A criterion carries the deliverable's exact basename | Add it, grading content around the basename |
| R9, R24, R73 | `liveness_completeness` | A hand-keyed workbook loses more than 15% of positive weight; strict liveness ≤ 10 points; positive total ≤ 39 | Displace +1 rows, never add liveness rows |
| R5, R6, R7, R8, R72, R98, R96 | `liveness_lands` | Every liveness row keys a cell of the shape it claims; no function names the judge cannot see; read-throughs, not same-sheet arithmetic | `05-rubric.md#house-rules-on-top-of-the-capture` |
| R12, R99 | `weights_clean` | Weights in the platform bands; at least one +4/+5; no flat weighting | Re-tier weights; weights never in the text |
| R81, R100 | `owner_rows` | Action rows score "a named person as owner and a calendar date", never the person | Rewrite the owner clause |
| MANUAL | `not_prompt_restatement` | Criteria check outcomes, not the prompt's wording | Rewrite offenders against the golden solution |
| MANUAL | `contradiction_domain` | A contradiction row and a domain-correctness row considered (recommended), both as positives | Add both unless there's a reason not to; never as penalties (R67) |
| MANUAL | `rows_fail_the_golden` | Each fact the reviewer's read verifies (`04-golden-solution.md`) has a row that would fail if the golden had it wrong | `05-rubric.md#house-rules-on-top-of-the-capture` |
| MANUAL | `platform_quality_check` | Platform Rubric Quality Check run before submitting | Run it; resolve findings |

## F. Metadata

| Check | Gate | What it verifies | How to pass |
| --- | --- | --- | --- |
| M1, M3 | `onet_occupation` | Occupation is on the sector table and fits the prompt's requested work as framed | `02-prompt-writing.md#house-notes-on-platform-wholesale-trade-occupationsmd` |
| M2 | `onet_tasks` | 3–5 tasks, each with a duty the prompt carries | Trim to what the prompt directly exercises |
| MANUAL | `onet_skills` | 3–5 skills from the Skills section (not Technology Skills) | Re-select |
| MANUAL | `multimodal_flag` | Boolean matches actual file contents (pdf/pptx = Yes) | Set from the zip, not the plan |
| MANUAL | `websearch_flag` | Boolean matches the prompt | Set from the prompt text |
| MANUAL | `time_estimate` | Reflects a 3+ hour manual workflow | Align with `three_hour_floor` |

## G. Program-wide checks (see `../platform/task-lifecycle.md`)

| Check | Gate | What it verifies | How to pass |
| --- | --- | --- | --- |
| H1, N1 | `no_geranium_string` | "Geranium" and project vocabulary appear nowhere: prompt, file names, file contents, file metadata | Search every file and its embedded metadata; strip before zipping |
| A6, A10, A14, F1, G2b | `llm_detection` | The prompt is human-authored; inputs and golden carry no authorship tell or batch evidence (`../../reviewer/platform/reviewer-guidelines-v5.1.md`) | **Highest severity.** Package-level evidence of batch generation is a rejection with offboarding risk |
| U1, U2 | `uniqueness` | Not similar to another submitted task, this portfolio's own included | Use your own artifacts and a scenario specific to your work; `01-ideation.md#check-the-sector-uniqueness-map-first` |
| MANUAL | `model_solvability` | Worst-agent accuracy ≤ 80% (`../platform/auto-eval-feedback-guide.md#the-difficulty-check-accuracy-percentages`) | Harden the task and/or densify the rubric |
| G1, G5, G21, R60 | `no_contradictions` | Golden solution agrees with prompt and rubric in every number and sentence; no quantity equated to two figures | Cross-read all three side by side; one mismatch is a send-back |

## H. Lifecycle checks (see `../platform/task-lifecycle.md` and `../platform/creating-input-files.md`)

| Check | Gate | What it verifies | How to pass |
| --- | --- | --- | --- |
| N1 | `no_meta_references` | No project/evaluation reference in any shipped file's content, name, or metadata | Sweep and strip |
| L2 | `hidden_content` | No leakage hiding places: hidden/veryHidden sheets, hidden rows/columns, cell comments, tracked changes, speaker notes | Unhide, review, strip |
| T1 | `tell_log_standalone` | A tell log (if any tells were found) exists as a standalone file and is NOT inside either zip | Move it out of the packages |
| MANUAL | `safety_check` | Nothing in the task teaches materially unsafe professional practice; the `geranium_safety_check` screens this independently of correctness | Redesign any scenario whose golden normalizes an unsafe act |
| MANUAL | `self_containment` | Prompt + input files alone are sufficient to reproduce the golden solution | Rebuild the answer path touching only shipped files |

The reviewer's own rule set is `../../reviewer/platform/reviewer-guidelines-v5.1.md`, and
`../../reviewer/platform/reviewer-rubric.md` gives the severity math that turns LLM tells into a
verdict. Reading the rows above against those two is the closest thing to seeing the
review before it happens: a reviewer spot-checks 2 to 3 rubric criteria against the
golden, allows between one and four revision rounds depending on which capture you read (build for one), and can flag Suspected Duplicate or
Template even on an otherwise acceptable task.

When every row passes: submit. When in doubt on any row, ask in `#ec-geranium-project`
before submitting — early feedback prevents rework. After submitting, allow 60–120
minutes, then read the five auto-eval feedback boxes per
`../platform/auto-eval-feedback-guide.md`; rebut a wrong flag as a threaded reply to
the daily *Eval & Review Comments* Slack post with the Task/Submission ID.
