# Workflow 07 — Pre-Submission Audit

One row per gate. Walk every row against what you actually built, in order, and fix
failures before submitting, since a failed gate means the submission is sent back. Modeled
on `../platform/platform-submission-form.md#5-before-you-submit--task-creation-checklist`
and `../platform/platform-submission-form.md#5-before-you-submit--task-creation-checklist`; on any conflict, the form
wins.

The **Check** column names the registry id that codes the row (one line per id in
`../../rules.md`; the code is under `tools/gcheck/`), or **MANUAL** when no check codes it
and the row is a read. A coded row is not a substitute for the read: the checks are pattern
nets, and every MANUAL row is a rejection that has happened.

Sections A to H are the house audit. Section I is the platform's own checklist, and it is
the gate: all of its boxes must be checked before the form will submit.

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
| MANUAL | `domain_occupation_picked` | Domain and occupation are entries on the form's closed lists, and the domain matches the occupation's job family | `01-ideation.md#start-by-picking-the-domain-and-the-occupation`; codes in `../platform/onet-codes.md#the-table` |
| MANUAL | `three_hour_floor` | The task takes over 3 hours by hand without an LLM; 5 to 10 is the target | Recount where each of the four time blocks goes; under 3 → redesign |
| MANUAL | `frontier_resistance` | A model cannot produce a good answer from the instruction alone, and cannot draft the golden correctly on the first try with no meaningful edits | Run the prompt through a model before building files; harden the task where it succeeds |
| MANUAL | `difficulty_in_files` | Difficulty comes from input files + reasoning, not the prompt | Confirm the task is unanswerable without opening the attachments |
| L7, PR21, PR22 | `traps_not_labelled` | No decision the golden makes turns on an input column that names the rule, or on the sentence that states it; a numbered rule an input carries is applied somewhere, and a rule that turns on a document or a written act is exercised on both arms with a look-alike that fails it | Walk each golden decision to the input fact it turns on (PR21); L7 errors on an exceptions/deviations column citing the section a record breaks; PR22 is the both-arms walk. The platform's difficulty check failed a task built the other way (2026-09-22) and a rating audit whose exceptions were all two-file mismatches (2026-09-22) |
| MANUAL | `occupation_fit` | The prompt's actual work is the selected occupation's work, named in its vocabulary | `02-prompt-writing.md#the-prompt-has-to-fit-the-occupation-you-selected`; if it drifted, change the selection |
| P4 | `us_grounding` | The opening names the state or the US, the requester's role, and the expertise the reader brings | `02-prompt-writing.md#the-opening-frame-p4-p6` |

## B. Prompt

| Check | Gate | What it verifies | How to pass |
| --- | --- | --- | --- |
| A10, P7 | `natural_voice` | Written by you; none of the flagged prose shapes; no three sentences opening on the same stem | Read aloud; `../../reference/llm-prose-tells.md` |
| P6 | `expert_context` | The P4 frame is woven into the ask, never a self-introduction to a coworker | `02-prompt-writing.md#the-opening-frame-p4-p6` |
| MANUAL | `named_context` | A named role, a named organization, and a stated reason the work is happening today | Checklist box 1 |
| A20 | `comma_rules` | A comma before a clause-joining conjunction; never three clauses in one sentence | `02-prompt-writing.md#sentence-mechanics-a20`; the serial comma is a read |
| P1 | `output_named` | One output file named, with its format and every length or structural requirement stated | Checklist box 3; name it exactly as the solution zip delivers it |
| P2, P3 | `inputs_referenced` | Every input file named in the narrative; no inventory paragraph | Checklist box 2; weave the names into the opening paragraph |
| P5 | `no_file_glosses` | At most one or two files carry a purpose gloss | Name what each file contains, not what it is for |
| MANUAL | `constraints_present` | Real scenario constraints stated: budget, deadline, headcount, threshold | Checklist box 4; these are wanted, not a leak |
| MANUAL | `no_derived_findings` | No number, name or finding that can only come from working the input files | Checklist box 5; move it to the rubric |
| MANUAL | `not_overspecified` | No pitfall warnings, derived parameters, section outlines or decision frameworks from an input | `02-prompt-writing.md#overspecification-giveaways-beyond-step-by-step` |
| MANUAL | `self_contained` | Complete without the rubric; no proprietary tools or logins required | Checklist box 6; replace or remove any such dependency |
| MANUAL | `verifiable` | Objectively gradable against a known correct answer | If no correct answer (or nameable conditions) exists, redesign |
| MANUAL | `prompt_language` | No spelling or grammar errors | Spell-check |

## C. Input files

| Check | Gate | What it verifies | How to pass |
| --- | --- | --- | --- |
| MANUAL | `input_count` | At least 2 input files; 3 or more preferred; every one load-bearing | Add a genuinely necessary source, never filler |
| A11, A12 | `substantial_files` | Prose inputs clear the word floor; no thin or placeholder file | Grow or cut thin files |
| G2b | `authentic_files` | No package-level batch-construction evidence (generator string, one shared write instant, identical docx components, shared rsids) | Rebuild from sanitized real material; the Office re-save in the package sequence |
| A15, F1, H2, H3, A1, A6 | `no_fabrication_tells` | No number series without variance, float dust, 555 phones, calendar-false weekday/date pairs, LLM-blue fills, em dashes | Inject real variance; use plausible specific values; `../platform/creating-input-files.md#3-the-fingerprints-to-keep-out` |
| MANUAL | `rights_clean` | No paywalled, copyrighted, restricted, confidential or employer-owned content | Checklist box 8; remove or replace with material you may distribute |
| MANUAL | `no_real_personal_data` | Nothing that reads as a real patient record, a real identifiable individual, or unsafe practice | Re-key or fictionalize; `../platform/domains-and-occupations.md#what-this-means-for-task-design` |
| L1, L3, L4 | `no_giveaways` | No input paragraph enumerating the answer set, handing over a verdict a criterion scores, or naming the members of a listed set; no notes columns revealing what the solver should deduce | Delete them |
| R23 | `term_dates_carried` | A firm-price or validity date stated in an input is carried by the golden | Carry it or remove it |
| G22 | `cutoff_chronology` | No snapshot dated before records it references; no stated balance an input reproduces only without the date cutoff | Re-key every date-gated figure on the input's own date column |
| H4 | `zip_hygiene_inputs` | Single flat zip; no subfolders, empty files, spaces, or double extensions | Unzip once and inspect before submitting |
| H5 | `names_match_prompt` | Input File List, prompt mentions and zip member names agree character for character, including case and extension | Checklist box 7; fix names on whichever side is wrong |
| A14, A3, A13 | `package_provenance` | docProps names the application that really wrote the file, never a python library; plausible creator and stamps; a calcChain Excel would write | The package sequence above; the generator string is evidence, cleared only by a genuine save (`memory/package-hygiene-pipeline.md`) |

## D. Golden solution

| Check | Gate | What it verifies | How to pass |
| --- | --- | --- | --- |
| MANUAL | `solution_uploaded` | A completed deliverable exists and is uploaded; the form will not submit without it | `04-golden-solution.md` |
| MANUAL | `complete_answer` | Every part of the prompt answered; fact-checked | Walk the prompt line by line against the deliverable |
| MANUAL | `scores_100` | Golden solution scores ~100 on the rubric | Fix the solution or the rubric, whichever is wrong |
| MANUAL | `human_edited` | Mostly human-edited | If a model draft needed no meaningful edits, the task fails `frontier_resistance` too |
| A1, A2, A5, A6, A10 | `client_ready` | No LLM-blue fills, datetime-formatted date cells, paste walls, em dashes or flagged prose shapes | `../platform/style-guide-llm-tells.md` |
| A9, A13, A17 | `live_formulas` | Formulas live, every cache reproducible by its own formula, calcChain present | Rebuild calculations as formulas; `06-metadata.md#house-notes-on-the-live-form` |
| G8 | `signable_document` | When the prompt says a document is signed, the golden carries it with a signature line | Add the document, not a table about it |
| G9 | `dateline_before_actions` | The deliverable is not dated later than an action it schedules as done | Date the deliverable the day the work is done |
| G10 | `cited_identifiers` | Every invoice, PO, serial or work-order id the golden cites exists in a shipped input | Look each one up in the input at the moment of writing |
| G18, G20 | `dates_anchored` | Every owner-dated action row and every full date in the prose is written in an input or the prompt | Carry the date in an input, show the derivation, or leave it off |
| G19 | `direction_claims` | Every "X moves up/down" claim agrees with the correction column | Re-read per-person prose against the tabs |
| G1, G5, G7, G21 | `internal_consistency` | No stays-as-placed status beside a change; prose counts match the tabs; docx total rows tie; displayed ratios re-derive from displayed figures | Cross-read all three side by side; one mismatch is a send-back |
| G11, G12, G13, G14, G15, G16, G17 | `sourced_from_inputs` | Attributed dates, input conditions, unit costs, dispute entities, owner and author names and header titles all stand in an input or the prompt | Re-derive every figure and name from the shipped inputs |
| H5 | `output_name_match` | Output file name matches the prompt and the Output File List, including extension | Fix whichever side is wrong |
| A16 | `opens_cleanly` | Every package parses; no XML errors, repair prompts, or corruption | Re-open every file from the zipped copy |
| H4 | `zip_hygiene_solution` | Flat zip; no subfolders or empty files; no spaces or double extensions | Unzip once and inspect |
| L2 | `no_revision_residue` | No tracked changes, comments, hidden sheets, rows or columns | Unhide, review, strip |

## E. Rubric

| Check | Gate | What it verifies | How to pass |
| --- | --- | --- | --- |
| R11 | `criterion_count` | At least 6 criteria; 20 or more expected; no upper bound | Cover more of the task rather than splitting rows to hit a number |
| R55, R27, R49, R54, R85 | `atomic_specific` | One simple atomic sentence per criterion; no bundles, stacked clauses or second subjects | Checklist box 10; split bundles |
| R20, R21, R82 | `figures_land` | Every stated figure lands on the golden, written to the cent with a $ mark | Add the exact correct values where the golden holds them |
| MANUAL | `values_from_ground_truth` | No hedged magnitude ("approximately", "roughly", "about", "~") in front of an asserted figure; nothing asserted that the inputs cannot produce | Checklist box 13; read every value off the golden |
| R4, R13, R101, R102 | `coverage` | Every prompt instruction, front-page block and addressee has a criterion | Map prompt requirements → criteria; fill gaps |
| R18, R19, R25 | `rigid_vs_subjective` | No grader instructions, unanchored hedges or evaluative terms; subjective rows name their conditions | Reclassify and rewrite any vague criterion |
| MANUAL | `two_negatives` | ≥2 negatives, each naming a specific observable unwanted outcome | `05-rubric.md#negatives-any-specific-unwanted-outcome` |
| R84, R53 | `negative_shape` | The defect is framed inside the sentence, one negation only, never a trailing "in violation of" clause | Rewrite the clause |
| E1, W18 | `affirmative_negatives` | Negative criteria read TRUE when the failure is present | Remove "does not / fails to / is missing" phrasing |
| R33, R37, R52 | `negatives_scoped` | No universal, threshold or membership negative the golden's own rows violate | Test each negative against every row class of the golden |
| MANUAL | `closing_criterion` | The **last** row is a general "Overall formatting and style of the deliverable" criterion | Checklist box 12; add it, or move it to the end |
| MANUAL | `style_share` | Specific style and formatting rows stay a minority of the count, the closing criterion aside | Cut or down-weight style rows |
| R83 | `file_name_criterion` | A criterion carries the deliverable's exact basename | Add it, grading content around the basename |
| R5, R6, R7, R8, R72, R98, R96 | `liveness_lands` | Every liveness row keys a cell of the shape it claims; no function names a grader cannot see; read-throughs, not same-sheet arithmetic | `05-rubric.md#house-rules-on-top-of-the-capture` |
| R12, R99 | `weights_clean` | Every weight a non-zero integer in −5..+5; at least one +4/+5; no flat weighting | Checklist box 11; re-tier weights; weights never in the text |
| R81, R100 | `owner_rows` | Action rows score "a named person as owner and a calendar date", never the person | Rewrite the owner clause |
| MANUAL | `not_prompt_restatement` | Criteria check outcomes, not the prompt's wording | Rewrite offenders against the golden solution |
| MANUAL | `rows_fail_the_golden` | Each fact the literal read verifies (`04-golden-solution.md`) has a row that would fail if the golden had it wrong | `05-rubric.md#house-rules-on-top-of-the-capture` |

## F. Metadata

| Check | Gate | What it verifies | How to pass |
| --- | --- | --- | --- |
| MANUAL | `domain_on_list` | `domain` is one of the 14, spelled as the form spells it | `../platform/domains-and-occupations.md#domain-14` |
| MANUAL | `occupation_on_list` | `onet_occupation.title` is one of the 64, spelled as the form spells it | `../platform/domains-and-occupations.md#occupation-64` |
| MANUAL | `onet_code_verified` | The code is confirmed on the occupation's own onetonline.org page, detail suffix included | `../platform/onet-codes.md#the-table` |
| MANUAL | `input_file_count` | Matches the zip and the Input File List; ≥2 | Count from the zip, not the plan |
| MANUAL | `tools_logged` | At least one tool, named as a real non-AI application | `06-metadata.md#tools` |
| MANUAL | `time_fields` | Four integer minute fields; total in hours at least their sum; total over 3 | `06-metadata.md#the-five-time-values` |
| MANUAL | `no_sector_key` | No `sector` field anywhere in metadata, prompts or build notes | Delete it |

## G. Program-wide checks

| Check | Gate | What it verifies | How to pass |
| --- | --- | --- | --- |
| H1, N1 | `no_codename_string` | Neither programme codename nor project vocabulary appears anywhere: prompt, file names, file contents, file metadata | Search every file and its embedded metadata; strip before zipping |
| A6, A10, A14, F1, G2b | `llm_detection` | The prompt is human-authored; inputs and golden carry no authorship tell or batch evidence | **Highest severity.** Package-level evidence of batch generation is a rejection with offboarding risk |
| U1, U2 | `uniqueness` | Not similar to another submitted task, this portfolio's own included | `01-ideation.md#uniqueness` |
| MANUAL | `model_solvability` | A model reading the instruction alone, without the input files, cannot produce a good answer | Harden the task and/or densify the rubric |
| G1, G5, G21, R60 | `no_contradictions` | Golden solution agrees with prompt and rubric in every number and sentence; no quantity equated to two figures | Cross-read all three side by side; one mismatch is a send-back |

## H. Package and safety checks

| Check | Gate | What it verifies | How to pass |
| --- | --- | --- | --- |
| N1 | `no_meta_references` | No project/evaluation reference in any shipped file's content, name, or metadata | Sweep and strip |
| L2 | `hidden_content` | No leakage hiding places: hidden/veryHidden sheets, hidden rows/columns, cell comments, tracked changes, speaker notes | Unhide, review, strip |
| T1 | `tell_log_standalone` | A tell log (if any tells were found) exists as a standalone file and is NOT inside either zip | Move it out of the packages |
| MANUAL | `safety_check` | Nothing in the task teaches materially unsafe professional practice; clinical, counselling and laboratory tasks carry the highest exposure | Redesign any scenario whose golden normalizes an unsafe act |
| MANUAL | `self_containment` | Prompt + input files alone are sufficient to reproduce the golden solution | Rebuild the answer path touching only shipped files |

The three in-form check panels are advisory and block nothing, but each section ends in
**Run Evaluations and Continue** and the form ends in **Run Evaluations and Submit**, so
evaluations do run at submit time. Read the panels' findings, and treat a finding you
disagree with as a prompt to re-read the row above rather than as a verdict.

## I. The platform's checklist: all boxes must be checked to submit

This is the gate. Walk it last, one row at a time, against what is actually uploaded rather
than against what you intended to upload
(`../platform/platform-submission-form.md#5-before-you-submit--task-creation-checklist`).

**Task Instruction**

| # | The box | Where this audit verified it |
| --- | --- | --- |
| 1 | Specific context: a named role, organization, and a reason this work is happening today | B `named_context`, A `us_grounding` |
| 2 | Every input file named and briefly described | B `inputs_referenced`, C `names_match_prompt` |
| 3 | Exact deliverable format stated, plus length and structural requirements | B `output_named` |
| 4 | Real scenario constraints included where they belong | B `constraints_present` |
| 5 | No number, name or finding that can only come from working the input files | B `no_derived_findings` |
| 6 | Fully self-contained: instruction + files are enough, with no rubric access | B `self_contained`, H `self_containment` |

**Input Files**

| # | The box | Where this audit verified it |
| --- | --- | --- |
| 7 | Every listed file uploaded and every uploaded file listed; names match exactly, including extension and case | C `names_match_prompt`, C `zip_hygiene_inputs` |
| 8 | Only files you are authorized to share; nothing confidential, proprietary or IP-restricted | C `rights_clean`, C `no_real_personal_data` |

**Task Rubric**

| # | The box | Where this audit verified it |
| --- | --- | --- |
| 9 | At least 3 criteria, and enough to genuinely cover the task's complexity | E `criterion_count` (house floor 6, 20+ expected) |
| 10 | Each criterion tests exactly one thing; no line bundles two checks with "and" | E `atomic_specific` |
| 11 | Each weight (-5 to +5) reflects how central that item is | E `weights_clean` |
| 12 | The rubric ends with a general "Overall formatting and style of the deliverable" line | E `closing_criterion` |
| 13 | Nothing in the rubric asserts a fact that is not derivable from the input files | E `values_from_ground_truth`, E `figures_land` |

**Final Check**

| # | The box | Where this audit verified it |
| --- | --- | --- |
| 14 | Someone with real expertise but no rubric access, reading only the instruction and files, could produce work that passes the rubric | A `frontier_resistance`, B `self_contained`, D `scores_100` |

The form states fourteen boxes and the capture reproduces fourteen. Read the live checklist
before checking anything off, and add the missing box to the capture if it appears; do not
assume this table is complete.

When every row and every box passes, build the form payload and fill the form:
[08-fill-the-form-and-submit.md](08-fill-the-form-and-submit.md).

```bash
.venv/bin/python tools/sync_metadata.py drafts/NN-task-name
```

Its report is the last gate. Anything it says it could not source is a hole in the package,
not a quirk of the generator: an input with no description, a missing time value, an empty
tools list. Fix those here rather than typing around them on the form.
