"""Consolidation layer over the coded checks, organised by the task lifecycle.

`autoeval_check.py` grew one coded check per platform finding — 83 of them across three
tools, each named for the task and run that motivated it. That is the right way to
*capture* a lesson and the wrong way to *apply* one. Two problems follow from a flat list
of rule ids, and this module fixes both.

**Generalization.** R20, R21, R26, R31, R32, R35, R43 and R47 were each born from a
different task's oracle failure, and they are all ONE rule: every figure a criterion
asserts has to land on a single cell the judge can grep. Someone who learns the rule stops
producing all eight defects. Someone handed eight regexes fixes the eight shapes they match
and invents the ninth. So the coded checks stay as the mechanical detectors, and each is
mapped to the generalized rule it serves.

**Timing.** A finding is only useful if you know when you can still act on it. The gates
fire at four different moments, and they are not interchangeable:

  STAGE 1  PRE-SUBMISSION   platform checks run before the task is submitted at all.
                            1a prompt, O*NET occupation / tasks / skills
                            1b the rubric
                            Everything here is free to fix — nothing has been spent yet.

  STAGE 2  AUTOEVAL         the task is submitted, sits in EVALUATION_PENDING for hours,
                            and comes back NEEDS_REVISION carrying:
                            2a Golden solution check      (oracle, 3 runs, all at 1.0)
                            2b LLM generated files check
                            2c Rubric Quality Check
                            Each round costs a submission cycle, so this is the stage
                            worth spending prevention effort on.

  STAGE 3  HUMAN REVIEWER   a person reads the whole task. Mostly judgement, but the
                            recurring mechanical findings are coded here — above all
                            LLM-style prose: invented idiom, slogans, the three-beat
                            sentence rhythm. A reviewer who sees one stops trusting the
                            rest of the task, so these never ship.

  STAGE 4  ADJUDICATION     one final, exhaustive programmatic pass
                            (docs/submission/platform/task-lifecycle.md names its ten checks:
                            golden accuracy, input leakage, omissions/conflicts, prompt
                            verbosity, coherent task contract, rubric coverage,
                            over-constrained rubric, mechanical defects, solvability,
                            safety-critical content). Its returned minor fixes go back
                            to adjudication directly, bypassing human review — the
                            cheapest revision loop in the pipeline. Task-specific
                            findings still land in that task's feedback-log.md;
                            findings matching one of the ten documented checks feed the
                            coded rules here like any other stage's.

Findings are binary. There is no advisory tier: a check either proves a defect and errors,
or it does not exist — a check no feedback log ties to a real platform failure is deleted
rather than demoted.

Structure
---------
STAGES    lifecycle stage -> (name, when it fires, what it costs)
REPORTS   platform report -> (stage, its name on the platform)
RULES     generalized rule -> (report, the rule, why it decides the gate)
PRIMARY   coded check -> the generalized rule it implements (exactly one)
ALSO      coded check -> further rules it also predicts (display only, never counted)

`unmapped()` reports any coded check with no rule, so a check added later cannot silently
fall out of the consolidated view.
"""

# Stage names follow docs/submission/platform/task-lifecycle.md (captured 2026-08-26): seven
# in-app pre-submission checks, ten named post-submission evals, human review capped
# at 5 total reviews, then one programmatic adjudication pass whose returned minor
# fixes go back to adjudication directly, bypassing human review.
STAGES = {
    "PRE":   ("Stage 1 · In-app pre-submission checks",
              "before submitting", "free to fix"),
    "AUTO":  ("Stage 2 · Post-submission evals (EVALUATION_PENDING → NEEDS_REVISION)",
              "60-120 min after submitting", "costs a submission cycle"),
    "HUMAN": ("Stage 3 · Human reviewer (max 5 total reviews, then accept/reject only)",
              "after the evals clear", "costs a review round and reviewer trust"),
    "ADJ":   ("Stage 4 · Adjudication (programmatic pass; fixes bypass human review)",
              "final gate", "cheapest revision loop — automated round-trip"),
}

# platform report -> (stage, the platform's own name for the check)
REPORTS = {
    "PRE-PROMPT": ("PRE",   "1a Prompt / O*NET / Name in-app checks"),
    "PRE-RUBRIC": ("PRE",   "1b Rubric Quality Check (structure, objectivity, polarity, "
                            "near-identical, requirement mapping, full-credit completeness)"),
    "GOLDEN":     ("AUTO",  "2a golden_solution_check (3 agents, must score "
                            "1.0000/1.0000/1.0000)"),
    "LLMFILES":   ("AUTO",  "2b llm_authorship_check (mean < 3.5 → NEEDS_REVISION)"),
    "RUBRICQ":    ("AUTO",  "2c agentic_rubric_quality_check (grounding, coverage, "
                            "atomicity, objectivity, redundancy, unjustified rigidity)"),
    "DATASET":    ("AUTO",  "2d dataset_quality_check / self_containment_check / "
                            "golden_solution_leakage_check"),
    "REVIEWER":   ("HUMAN", "3 Human reviewer findings"),
}

# generalized rule -> (report, the rule, why it decides the gate)
RULES = {
    # ---- Stage 1a: prompt, occupation, O*NET --------------------------------------
    "PRE-FRAME": ("PRE-PROMPT",
        "The prompt's opening frames the US setting, the requester's role and the expertise the reader brings, in the requester's own voice.",
        "open-order-cleanup was rejected on prompt quality alone (2026-09-02) with its inputs, golden and "
        "rubric called strong, for an opening that framed none of the three, and lift-truck-fleet-plan was "
        "rejected at first review (2026-09-05) for writing the frame as a self-introduction to a coworker. "
        "Before this family existed P4 and P6 mapped to the report heading and never reached docs/rules.md."),
    "PRE-OCC": ("PRE-PROMPT",
        "The domain, occupation and the form's own metadata fields are all on the platform's closed lists and agree with each other.",
        "Rewritten 2026-09-21 for Hazy (docs/RULE-DELTAS.md D1, D7-D9). The form offers a "
        "CLOSED list of 14 domains and 64 occupations, so three things are mechanical and "
        "certain: an occupation off the list cannot be submitted at all, a domain that "
        "disagrees with the occupation's own O*NET job family is a form a reviewer bounces, "
        "and the required time, tool and input-count fields are either there or they are "
        "not. The four First-Line Supervisor rows are the standing trap: they sit in four "
        "different job families and none of them is Management. Pick only from "
        "docs/submission/platform/domains-and-occupations.md, and confirm the code in "
        "docs/submission/platform/onet-codes.md - eight of the 64 are detail codes ending "
        ".01 to .04."),
    "PRE-FILES": ("PRE-PROMPT",
        "The prompt names the deliverable file it expects, explicitly.",
        "V5.1 requires that when a prompt names exact file names, a criterion checks the "
        "delivered files use them. A prompt that never names its own output leaves the "
        "file-name criterion ungrounded and the platform's own check fails it."),
    "PRE-SOURCES": ("PRE-PROMPT",
        "The prompt names at least one concrete input source.",
        "The platform's 'Prompt input files reference check' FAILs a prompt that gestures "
        "at 'the folder': the uploaded archive's own filename does not count and the "
        "deliverable is an output, not a source. It pairs with the Prompt human voice "
        "check, which FAILs the opposite end for glossing nearly every file, so the two "
        "form a band - name the source whose precedence or governance changes the answer, "
        "name nothing else, and never pair a filename with a description of its contents."),
    "PRE-VERBOSE": ("PRE-PROMPT",
        "The prompt does not catalogue its inputs.",
        "The 'Prompt human voice check' FAILs per-file glossing on its own - 'nearly every "
        "referenced file is paired with an explanation of what it contains ... sufficient to "
        "fail by itself' - and stage 4 adjudication lists input cataloguing among its "
        "prompt-verbosity tells. It is the far end of PRE-SOURCES' band, and the repair "
        "overshoots into that check unless at least one source is kept "
        "(frankfort-stock-recovery failed both, in that order, 2026-08-31)."),
    "PRE-UNIQ": ("PRE-PROMPT",
        "The prompt does not reuse a prior task's reasoning path.",
        "The platform diffs each new prompt against the contributor's own prior tasks on "
        "scenario, reasoning path, constraints, input kit and deliverable. Task 21 was "
        "retired for reusing task 18's authored narrative moves, 7 of 7 markers."),
    "PRE-PACK": ("PRE-PROMPT",
        "Both zips are flat, every name is clean, no file is empty, and every file the prompt "
        "names exists.",
        "The in-app input-files and golden-files quality checks read packaging first: a "
        "subfolder, a space, a double extension or an empty member fails them before any "
        "content is judged, and a prompt naming a file the packet lacks fails the reference "
        "check. Coded from tools/audit_task.py's sweeps when they joined the registry "
        "(2026-09-04)."),
    "PRE-NAME": ("PRE-PROMPT",
        "No project or evaluation reference anywhere in the shipped package.",
        "The in-app Name Check verifies the literal project name is absent across the "
        "fields; docs/submission/platform/creating-input-files.md goes further — no mention of a "
        "task, prompt, rubric, golden, eval or benchmark in any shipped file's content, "
        "file name, or document metadata. A file that points at the project is both an "
        "authenticity tell and a form of leakage."),

    # ---- Stage 1b: the rubric, before it is ever submitted -------------------------
    "PRE-OBJ": ("PRE-RUBRIC",
        "Criteria state checkable facts — no evaluative words, hedges, grader "
        "instructions, or golden-only cell references.",
        "The objectivity check treats ONE unanchored word ('consistently', 'where "
        "judgment is exercised') as failing the whole dimension."),
    "PRE-POL": ("PRE-RUBRIC",
        "Negatives carry a polarity pin and frame the defect affirmatively.",
        "A bare plural subject and stacked negations draw ambiguous_negative_polarity on "
        "all 3 oracle runs; 'does not meet it' reads to the quality review as inverted."),
    "PRE-SCOPE": ("PRE-RUBRIC",
        "A penalty is spent only on a critical commission.",
        "The Rubric penalty scope check allows a negative weight on four classes and no "
        "others: safety harm, a privacy leak, an inverted or prohibited top-level decision, "
        "and fabrication. A cadence, threshold or rate misapplied is an ordinary planning "
        "miss, belongs to an affirmative positive, and FAILs the dimension where it is "
        "written as a penalty (inbound-consolidation-plan, 2026-08-27)."),
    "PRE-DUP": ("PRE-RUBRIC",
        "No criterion scores what another criterion already scores.",
        "Mirrored positive/negative pairs and repeated figures fail the near-identical "
        "check, and the quality review reads them as double-counted even when pinned."),
    "PRE-COVER": ("PRE-RUBRIC",
        "Completeness is pinned, and full credit is unreachable without the derivation.",
        "The most common human-reviewer finding in this portfolio AND a platform check: "
        "the prompt demands every item, the rubric spot-checks a few, and a partial "
        "submission passes. Its machine twin is the full-credit completeness hole — a "
        "hard-coded workbook that still collects 90%+ of positive weight."),
    "PRE-FORM": ("PRE-RUBRIC",
        "The submission form's own bands are respected.",
        "500-char criteria, weights outside +1..+5 / -3..-5, and criterion count outside "
        "15-60 are rejected by the form or its structure check "
        "(Geranium's project-guidelines-v5.1.md, deleted in the 2026-09-21 port; Hazy's form "
        "and guidelines state no US-setting rule, so this is house practice now - see "
        "docs/RULE-DELTAS.md)."),
    "PRE-FOCUS": ("PRE-RUBRIC",
        "Criteria grade the finished file, not the order the work was done in.",
        "A delivered file carries no drafting timeline, so a process-ordering clause "
        "('before any X is sized') cannot be observed. Failed task 07 C20."),

    # ---- Stage 2a: the golden solution check ---------------------------------------
    "GOLD-LAND": ("GOLDEN",
        "Every figure a criterion asserts lands on ONE cell the judge can grep.",
        "The oracle greps cached values and head functions. A figure that lives only in "
        "prose, nested inside a formula, or split across two tabs gives the judge nothing "
        "to land on, and it returns unverifiable_from_deliverable — on a workbook whose "
        "numbers are all correct."),
    "GOLD-LIVE": ("GOLDEN",
        "Liveness is anchored on a cached value; it is never asserted on its own.",
        "The single largest flake source in this portfolio ('liveness' appears 36 times "
        "in the golden-check FAIL entries). The judge normalises compound formulas, loses "
        "nested calls, and refuses to trace chains. Pair every derivation clause with the "
        "value it produces, or drop the criterion after 2 flaky runs."),
    "GOLD-KEY": ("GOLDEN",
        "Answer keys resolve exactly, and once, to the delivered workbook.",
        "A key citing a sheet, range or value the workbook does not carry fails "
        "deterministically in all 3 runs — the one golden-check failure class that is "
        "never judge variance."),
    "GOLD-NEG": ("GOLDEN",
        "A negative names one verdict cell — never a comparison, threshold or sweep.",
        "Told to compare two columns the judge aligns them itself and drifts by a row; "
        "given a threshold it fires on any cell past the line whatever the clause says. "
        "Put the failing-row count in a cell and quote that cell's label."),
    "GOLD-FID": ("GOLDEN",
        "The golden's own fabric agrees with itself across every tab.",
        "The fidelity pass re-derives the action plan end to end. A computed status "
        "contradicted by a typed CHANGE cell, arrival dates that ignore the planned order "
        "dates, or a superlative the neighbouring table does not support, is a hard fail "
        "no arithmetic check would ever see. Every ranking word in a solution cell is a "
        "claim, and it has to be checked against the rows it summarises."),

    # ---- Stage 2b: the LLM generated files check ------------------------------------
    "LLM-PKG": ("LLMFILES",
        "Package metadata reads as something a person made in Excel and Word.",
        "docProps creator, one shared write instant, identical docx components and shared "
        "rsids are package-level proof of generation. This is a stop, not a cleanup."),
    "LLM-SHAPE": ("LLMFILES",
        "Deliverable SHAPE, not word choice, decides this check.",
        "A raw-paste wall dominating the solution fabric fails it in any form — "
        "description-heavy and letterless-numeric both did. Design tasks whose honest "
        "fabric is flowing memo prose and word-anchored rows; the measured signature is "
        "mean longest string per row on the dominant tab (pass band 8-23, dillman failed "
        "at 59.4). Raw data stays in the inputs; the solution carries the rollup."),
    "LLM-NUM": ("LLMFILES",
        "Numeric residue is human-scale.",
        "openpyxl float-repr tails and cells storing more precision than they display are "
        "machine residue. An injected cache the formula does not reproduce is worse: it "
        "moves a pinned figure the moment the grader opens the file."),

    # ---- Stage 2c: the Rubric Quality Check ------------------------------------------
    "RUBQ-ATOM": ("RUBRICQ",
        "One measurement per criterion.",
        "The Agentic Rubric Quality Review rates a rubric needs_improvement on bundled "
        "criteria. Split WEIGHT-NEUTRALLY — divide the parent's weight among the children. "
        "Adding rows and weight together grows the completeness denominator and starts the "
        "bloat loop (32 to 50 criteria at an unchanged +98 is the shape that works)."),
    "RUBQ-SCHEMA": ("RUBRICQ",
        "The rubric grades the answer, not the golden's own layout.",
        "Citing a golden Sheet!Cell reference or a named column reads as imposing the "
        "golden's schema on any correct response. Keep numeric answer keys and the "
        "arithmetic instead."),
    "RUBQ-GROUND": ("RUBRICQ",
        "Every id and figure a criterion pins is readable inside the review's input window.",
        "The Agentic Rubric Quality Review reads each input sheet through a window of about "
        "28 rows and rates the rubric needs_improvement (ungrounded_verification, critical) "
        "when a criterion pins a record id, quantity or status that sits only past it: "
        "hathi-replenishment-order-decision 2026-09-11, eleven rows citing transaction and "
        "adjustment ids at rows 122 to 407 of the logs, 'could not be verified in the "
        "agent-visible source files'. A fact from a docx input or the prompt is always in "
        "view; a workbook fact past the window is scored as the deliverable's own property "
        "(cites the records by id, states their status) without the id (PR1, R107)."),
    "RUBQ-WEIGHT": ("RUBRICQ",
        "A core deliverable's cluster is weighted like a core deliverable, and no two strict rows score one total.",
        "The Agentic Rubric Quality Review reads a deliverable's share on its DIRECT rows only "
        "(strict and gated liveness rows counted apart as 'live-calculation') and rates a rubric "
        "needs_improvement (miscalibrated_weighting, major) when a core requirement's cluster is "
        "many rows at +1 each (weldon-bridge-plan 2026-09-11: eight rows, 8 of 39, 'failing the "
        "transition order retains ~79%'; rossville 2026-09-11: six requirements at 1 to 3 points). "
        "It also reads two +5 strict rows on one order's unit count and dollar total as "
        "redundant_or_double_counted. Answer inside 39: +2 on the decision rows, a policy spot "
        "check, the strict pair on two different deliverables' outputs."),
    "RUBQ-RIGID": ("RUBRICQ",
        "Exact-number and exact-ID criteria stay under 80% of the rubric.",
        "The Agentic Rubric Quality Review rates a rubric needs_improvement when rigid "
        "checks with no tolerance pass 80% of the criterion count, and arguing the task "
        "is deterministic does not spare the rating (tessendorf, 2026-08-26: 22 of 25). "
        "Hand-count it: the review's classification is semantic (a named-item outcome "
        "check counts as exact-ID with no digit in sight), so no digit proxy survives "
        "probing - 60-83% by digits across rubrics the review has passed. Re-probed "
        "2026-08-31 against a second labelled point (frankfort-stock-recovery, the review "
        "counting 36 of 40 = 90%) and the proxy still does not separate: that rubric "
        "measures only 85% by digits and 77.5% by money/quantity literals, under "
        "boettcher's passing 90.6% and beside june-price-review's passing 83.0%. The "
        "review sees a class the digits cannot. Do not code this. The repair is "
        "converting count-anchored single facts to method/coverage wording (an action "
        "list naming an owner and a date against each thing to be done; items showing "
        "counter movement held under the rule), never touching the liveness pair or the "
        "figure answer keys the oracle needs."),

    # ---- Stage 2d: dataset quality and leakage ---------------------------------------
    "DATA-SUFF": ("DATASET",
        "Every input file carries enough substance to stand on its own.",
        "Per-file floors on words (prose docs) and populated cells (xlsx/csv). Thin files "
        "lean on the aggregate carve-out and the dataset quality check names them."),
    "DATA-OPEN": ("DATASET",
        "Every shipped package opens in the tooling a solver would reach for.",
        "A malformed part (docProps missing its namespace declarations) makes openpyxl and "
        "pandas refuse the whole file: the solver's first command crashes, and this gate's "
        "own loaders skip what they cannot read, so every content check on that file goes "
        "silent. Both times it has happened the broken part was hiding a real finding "
        "(pavelka 2026-08-26 and inbound-consolidation-plan 2026-08-27, each masking a "
        "thin-input failure)."),
    "DATA-BUDGET": ("DATASET",
        "The deliverable fits in the reviewing agent's context.",
        "The Agentic Rubric Quality Review reads the whole deliverable and every input "
        "before it reads the rubric. Kolterman's review evicted the rubric itself from "
        "context at 260k chars and never actually ran."),
    "DATA-TIME": ("DATASET",
        "Dates are absolute and genuinely prospective.",
        "A relative window with no anchor drifts between the criterion and the workbook; "
        "a term date in the past contradicts the scenario."),
    "DATA-JOIN": ("DATASET",
        "Records the golden cites join across the inputs on the keys they carry.",
        "The dataset quality check's cross-document consistency axis hard-fails at 2 when a "
        "cited record's related-id field names a record no input holds; quantities that tie "
        "by inference do not count as a join (hathi-replenishment-order-decision 2026-09-13, "
        "every cited adjustment's Related Transaction ID absent from the transaction log)."),
    "DATA-LEAK": ("DATASET",
        "No input passage enumerates the golden's own answers.",
        "The leakage check verdicts ANSWER_LEAKED on a single passage listing the chosen "
        "replacements. Rulings stay on categories and procedure, never on products."),

    # ---- Stage 3: what human reviewers actually flag -----------------------------------
    "REV-PROSE": ("REVIEWER",
        "No LLM-style prose: invented idiom, slogans, or the three-beat sentence rhythm.",
        "The highest-trust finding a reviewer can make against a task, and the one the "
        "user has called out explicitly. Reviewers do not flag a word list — they flag the "
        "rhythm (workplace detail, idiom, analytical ask), tautologies, slogans, idiom "
        "standing in for a quantity, and first-person filler. Task 07 was failed on "
        "em-dash density alone. One tell costs the reviewer's trust in everything else, "
        "so these never ship. Full flagged history in docs/reference/llm-prose-tells.md."),
    "REV-REGISTER": ("REVIEWER",
        "The prose is desk register throughout — the prompt, the inputs AND the golden.",
        "Comma splices, a missing comma before a coordinating conjunction, punchy headers, "
        "sentences doing two things at once, and plural-noun-singular-verb are all "
        "send-backs. The rubric itself is held to the same standard."),
    "REV-CREDIBLE": ("REVIEWER",
        "Names, dates and document metadata survive being checked.",
        "Reviewers verify them: fabricated surnames the inputs never carry, weekday/date "
        "pairs that are not real calendar days, and document metadata that is not "
        "operationally credible have each blocked a task."),
    # Hand rule, no detector (2026-09-10, tessendorf-channel-split adjudication note). The
    # adjudicator reads every basis the golden states against the input that states it, and
    # every numbered rule in an input memo against the rubric. Two send-backs on one note that
    # no regex can model: "the two case-pack items" for PK-212 and TW-440 (only TW-440 is
    # case-pack; PK-212 is a bulk spool the rep removed because it will not carton), and the
    # BD-780's weight exclusion attributed to the program's 25 lb caps when the memo's 10 lb
    # rule is what excluded it. The same note found the memo's rule 7 (shelf prices hold)
    # graded by no criterion. Read the golden's prose one basis at a time, and tick the memo's
    # numbered rules off against the rubric, before submitting.
    "REV-TRACE": ("REVIEWER",
        "Every basis the golden states is the input's own basis, and every numbered rule in an input memo is graded.",
        "The adjudication pass traces every claim to its exact input source and flags "
        "substituted terms and wrong cross-references (task-lifecycle.md section 4.a.i), and "
        "grades every prompt requirement, the memo's numbered rules included (4.a.vi). A "
        "collective label that fits one item of a pair, a rule basis borrowed from the wrong "
        "document, and a memo rule no criterion penalises breaking each came back from "
        "adjudication on tessendorf-channel-split (2026-09-10)."),
}

# coded check -> the generalized rule it implements (exactly one)
PRIMARY = {
    # Stage 1a
    "M1": "PRE-OCC", "M2": "PRE-OCC", "M3": "PRE-OCC",
    # Added 2026-09-21 in the Hazy port (docs/RULE-DELTAS.md D7-D9): the form's
    # required time breakdown, non-AI tool list and input-file count.
    "M4": "PRE-OCC", "M5": "PRE-OCC", "M6": "PRE-OCC", "P1": "PRE-FILES", "P2": "PRE-PROMPT",
    "P2": "PRE-SOURCES", "P3": "PRE-VERBOSE", "P4": "PRE-FRAME", "P0": "PRE-FILES",
    "P5": "PRE-VERBOSE",    # file glosses (was P2 until 2026-09-04; a branch of check_prompt_rules since 2026-09-11)
    # P6: the P4 frame written as a self-introduction to a coworker - lift-truck-fleet-plan was
    # REJECTED at first human review on that paragraph (2026-09-05).
    "P6": "PRE-FRAME",
    "P7": "PRE-VERBOSE",   # repetitive sentence openers (harlow-route-rebalancing-proposal, 2026-09-10)
    "H1": "PRE-NAME",       # codename anywhere in a shipped file (audit_task canary)
    "H2": "REV-CREDIBLE",   # 555-prefix phone number
    "H3": "REV-CREDIBLE",   # weekday/date pair that is calendar-false
    "H4": "PRE-PACK",       # name, extension, empty-file and zip-member hygiene
    "H5": "PRE-PACK",       # a file the prompt names that the folder lacks,
    "H6": "PRE-PACK",       # a placeholder or dummy phrase in an input file, PDFs read too (2026-09-12)
    "U1": "PRE-UNIQ", "U2": "PRE-UNIQ",
    # N1: project/eval vocabulary in shipped files, names or metadata (the in-app
    # Name Check plus docs/submission/platform/creating-input-files.md section 4, 2026-08-26)
    "N1": "PRE-NAME",
    # Stage 1b
    "R18": "PRE-OBJ", "R19": "PRE-OBJ", "R25": "PRE-OBJ",
    "E1": "PRE-POL", "E2": "PRE-POL", "W9": "PRE-POL", "W14": "PRE-POL",
    "W15": "PRE-POL", "W17": "PRE-POL", "W18": "PRE-POL",
    # W19: a negative whose main verb a compliant deliverable also performs reads as
    # inverted polarity (task 28 run 6 quality review; drafts 2026-08-24).
    "W19": "PRE-POL",
    # R67 (what a penalty may be spent on) was DELETED 2026-09-21 in the Hazy port: it
    # reserved negatives for four critical classes, and the Hazy form explicitly invites
    # negatives on ordinary quality misses. See docs/RULE-DELTAS.md D4.
    "R69": "PRE-SCOPE",
    "R104": "PRE-SCOPE",  # a positive and a negative sharing one rule anchor score the same disposition both ways (tessendorf adjudication, 2026-09-10: C15 held vs C29 planned, "merge or remove one")
    "R10": "PRE-DUP", "R15": "PRE-DUP", "R22": "PRE-DUP", "R41": "PRE-DUP",
    "R47": "PRE-DUP",
    "R60": "PRE-DUP",
    "R57": "PRE-DUP",
    "R95": "PRE-DUP",       # same dollar total scored twice (was R12's second arm in check_total_twins)
    "R92": "PRE-COVER",     # grouped presentation demanded, no criterion pins it (was R46's second arm)
    "R4": "PRE-COVER", "R13": "PRE-COVER", "R126": "PRE-COVER", "R132": "PRE-COVER", "R24": "PRE-COVER", "R73": "PRE-COVER", "R74": "PRE-COVER", "R76": "PRE-COVER",
    "E0": "PRE-FORM", "R1": "PRE-FORM", "R11": "PRE-FORM", "R12": "PRE-FORM",
    # Added 2026-09-21 in the Hazy port (docs/RULE-DELTAS.md D5, D6): the form's
    # mandatory closing formatting-and-style criterion, and its ban on hedged figures.
    "R135": "PRE-FORM", "R136": "PRE-FORM",
    # R61: the 20% penalty share (negative weight against positive) — pure weight
    # arithmetic, so it sits with the other band checks, but it is NON-BLOCKING as of the
    # team manager's ruling of 2026-09-02 ("a nice to have and not a blocking requirement
    # to submit or get an accepted task ... should never be the main reason to send a task
    # back"). autoeval_check.py routes it through recommend(), so it prints and is never
    # counted; it stays mapped here only so the code still resolves to its family.
    "R61": "PRE-FORM",
    "R2": "PRE-FOCUS",
    # Stage 2a
    "R20": "GOLD-LAND", "R21": "GOLD-LAND", "R26": "GOLD-LAND", "R31": "GOLD-LAND",
    "R32": "GOLD-LAND", "R35": "GOLD-LAND", "R43": "GOLD-LAND", "R63": "GOLD-LAND", "R64": "GOLD-LAND", "R48": "GOLD-LAND", "R50": "GOLD-LAND", "R51": "GOLD-LAND", "R58": "GOLD-LAND",
    "R56": "GOLD-LAND", "R66": "GOLD-LAND",
    "R70": "GOLD-LAND", "R71": "GOLD-FID",
    "R58": "GOLD-LAND",
    # ids split out of colliding checks on 2026-09-04 (merged back into their parent checks 2026-09-11)
    "R87": "GOLD-LAND",     # percentage basis that does not reproduce (was R31 in check_stated_basis)
    "R91": "GOLD-LAND",     # 'carries N' count (was R32; a branch of check_presentation_counts)
    "R93": "GOLD-LAND",     # month-fragment landing (was R57; a branch of check_date_key_colocation)
    "R94": "GOLD-LAND",     # stored-form anchor (was R58; a branch of check_padded_figures)
    # holes the old gate reported on every run (NOTE lines), closed 2026-09-04
    "R78": "GOLD-LAND",     # plan counts pinned in a criterion
    "R79": "GOLD-LAND",     # placement claims (a figure said to sit in a named place)
    "W5": "GOLD-LAND", "W8": "GOLD-LAND", "W13": "GOLD-LAND",
    "R6": "GOLD-LIVE", "R7": "GOLD-LIVE", "R9": "GOLD-LIVE", "R16": "GOLD-LIVE", "R72": "GOLD-LIVE", "R96": "GOLD-LIVE", "R97": "GOLD-LIVE",
    "R17": "GOLD-LIVE", "R30": "GOLD-LIVE", "R36": "GOLD-LIVE", "R38": "GOLD-LIVE",
    "R39": "GOLD-LIVE", "R42": "GOLD-LIVE", "R44": "GOLD-LIVE", "R45": "GOLD-LIVE",
    "R46": "GOLD-LIVE",
    "R89": "GOLD-LIVE",     # nested money literal in a formula (was R32 in check_nested_literals)
    "R90": "GOLD-LIVE",     # function token in a liveness criterion (was R39; a branch of check_named_functions)
    "R59": "GOLD-LAND", "R62": "GOLD-LAND", "R65": "GOLD-LAND", "W4": "GOLD-LIVE", "W7": "GOLD-LIVE", "W10": "GOLD-LIVE",
    "W11": "GOLD-LIVE", "W16": "GOLD-LIVE",
    "R5": "GOLD-KEY", "R8": "GOLD-KEY",
    "R28": "GOLD-NEG", "R33": "GOLD-NEG", "R34": "GOLD-NEG", "R37": "GOLD-NEG",
    "R40": "GOLD-NEG", "R53": "GOLD-NEG", "W1": "GOLD-NEG", "W3": "GOLD-NEG", "W6": "GOLD-NEG", "R52": "GOLD-NEG",
    "R77": "GOLD-NEG",
    # R80: an agentless comparative lands on the wrong party (dfl-freight-audit C6).
    "R80": "GOLD-LAND",
    # R81: a criterion fixing an action's owner to a named person (dfl-freight-audit C23-25).
    "R81": "RUBQ-RIGID",
    "R128": "RUBQ-RIGID",  # one named function or the exact label words prescribed on a positive (june-price-review adjudication, 2026-09-14)
    "R129": "RUBQ-RIGID",  # formula and cell-reference criteria over a quarter of positive weight under a prompt with no live-formula demand (hx4180 adjudication, 2026-09-14)
    # R86: per-item quantifier on one attribute in two positives, no shared figure (dfl 2026-09-03).
    "R86": "PRE-DUP",
    # R124: an exact-count row and a figure-free closed-set row on one tab (recall-response 2026-09-14).
    "R124": "PRE-DUP",
    # R99: no positive at +4/+5, a flat rubric; R100: an owner/date clause the prompt never asked
    # for (dfl-freight-audit adjudication note, 2026-09-09).
    "R99": "PRE-FORM", "R100": "RUBQ-RIGID",
    # R114: the Rubric Quality Review's weighting read (weldon-bridge-plan, 2026-09-11).
    "R114": "RUBQ-WEIGHT",
    "R115": "PRE-COVER",    # a prompt asking for a figure by X and Y has a criterion cueing both dimensions (packaging-consolidation adjudication, 2026-09-11)
    "R117": "GOLD-LIVE",    # two strict rows resolve to one sheet (packaging-consolidation Rubric Quality Review, 2026-09-11)
    "R118": "GOLD-LIVE",    # a second formula-only gated row (same review)
    "R119": "PRE-OBJ",      # presence-only row over a computed figure (computed-values BLOCKING finding, same day)
    "R120": "GOLD-LAND",    # a first-page row needs the summary as the first worksheet (packaging-consolidation oracle 2/3, 2026-09-11)
    "R101": "PRE-COVER",   # a labelled front-page block no criterion scores
    "R102": "PRE-COVER",   # prompt names the addressee, no criterion grades it (po-conformance-review 2026-09-10)
    "R82": "RUBQ-ATOM",
    # R85: stacked absolute clauses / example hung off a liveness clause (pick-module-reslot).
    "R85": "RUBQ-ATOM",
    # R84: a negative ending in a trailing rule-breach clause (", contrary to ...") - the
    # flyer-program-review gate-2 reviewer sent the rubric back on the shape (2026-09-02).
    "R84": "REV-REGISTER",
    # R111: a negative opening in the passive voice ("<object> is incorrectly <done>") - the Rubric
    # Quality Review read it as inverted polarity twice on inbound-consolidation-plan (2026-09-11).
    "R111": "GOLD-NEG",
    "G1": "GOLD-FID", "G2": "GOLD-FID", "G3": "GOLD-FID", "R29": "GOLD-FID",
    # G6: a Params row cites a section that states a different figure (pick-module-reslot).
    "G6": "GOLD-FID",
    # G7: a docx table total row that does not equal its rows (dfl-freight-audit 2026-09-02).
    "G7": "GOLD-FID",
    # G8-G10: the reviewer's literal read of the golden (lift-truck-fleet-plan REJECTED 2026-09-05):
    # no signature line when the prompt says the deliverable is signed; actions dated before the
    # deliverable's own date; a cited identifier no input carries.
    "G8": "GOLD-FID", "G9": "GOLD-FID", "G10": "GOLD-FID",
    # G11-G13 + R97: the golden read against the SOURCES it cites (hollenbach-allocation-plan REJECTED 2026-09-05):
    # a deadline attributed to a source that never gave one; the inputs' own conditions and
    # prohibitions ledger; one item carrying two unit costs; a month split no criterion scores.
    "G11": "GOLD-FID", "G12": "GOLD-FID", "G13": "GOLD-FID",
    # G14: the golden's dispute tab adjudicates an account no correspondence input names
    # (commission-review-q2 AutoEval golden_source_fidelity 2/5, 2026-09-05).
    "G14": "GOLD-FID",
    # G34: a prose direction to a tab for a column label another tab carries (commission-review-q2 reviewer round 5, 2026-09-14).
    "G34": "GOLD-FID",
    "G37": "GOLD-FID",      # an identifier two inputs share, cited in a golden paragraph or cell that names neither owner (standby-generator round 7, 2026-09-14)
    # R103: a positive enumerating N>=5 items on a prose tab with fewer than N short cells to count
    # (commission-review-q2 golden check 0/3 on C7, 2026-09-10).
    "R103": "GOLD-LAND",
    # R105: a positive ordering claim ("leads with") coordinating two determiner-led objects,
    # two verdicts in one row (freight-audit-review refinement golden check 2/3, 2026-09-11).
    "R105": "RUBQ-ATOM",
    # G15: a person the golden assigns an action to whom no input and not the prompt names
    # (dfl-freight-audit adjudication note, 2026-09-09: "Hector Ybarra").
    "G15": "GOLD-FID",
    "G16": "GOLD-FID",   # a memo author line / docProps creator no input and not the prompt names (po-conformance-review 2026-09-10)
    "G17": "GOLD-FID",   # a header line gives a named person a title no input and not the prompt carries (dock-to-stock-review adjudication, 2026-09-10)
    "G18": "GOLD-FID",   # an owner-dated golden row carrying a date no input and not the prompt states (tessendorf-channel-split adjudication, 2026-09-10)
    "G19": "GOLD-FID",   # a prose "X's quarter moves up/down" claim the correction column's sign contradicts (commission-review-q2 review round 3, 2026-09-10)
    "G20": "GOLD-FID",   # a full date a golden prose cell states that neither the prompt nor an input carries (commission-review-q2 review round 4, 2026-09-10)
    # S1 sits here, not with the prose rules: a superlative in a solution cell is a
    # CLAIM the fidelity axis re-derives from the neighbouring table, and vondrak run 2
    # failed it 2/5 because "cheapest of the four" named the wrong counter. The remedy
    # is verifying the claim against its own numbers, not deleting the sentence.
    "S1": "GOLD-FID",
    # Stage 2b
    "A1": "LLM-PKG", "A2": "LLM-PKG", "A3": "LLM-PKG",
    # originality_check.py's package-provenance codes: a generator string, one shared
    # write instant, identical docx components, a shared Word rsid. Package-level proof
    # of generation, and a stop rather than a cleanup.
    "G2b": "LLM-PKG",       # G2a, G2c and G2d retired 2026-09-15 (see check_input_authorship)
    # A13: a formula workbook shipped without xl/calcChain.xml reads as all-values-
    # hard-coded to the extractor's package scan (june-price-review, 2026-08-24)
    "A13": "LLM-PKG",
    # A14: an Openpyxl generator string in docProps is the same package-provenance
    # tell surfacing at gate 2 - a reviewer reads file properties (june-price-review)
    "A14": "LLM-PKG", "A19": "LLM-PKG",
    "A5": "LLM-SHAPE",
    # A15: machine-generated number series in input CSVs (strict cycling, near-uniform
    # amount distributions) — the same statistical detector, reading the inputs.
    "A15": "LLM-SHAPE",
    "A8": "LLM-NUM", "A9": "LLM-NUM", "F1": "LLM-NUM",
    # Stage 2c
    "R27": "RUBQ-ATOM", "R49": "RUBQ-ATOM", "R54": "RUBQ-ATOM", "R55": "RUBQ-ATOM", "W12": "RUBQ-SCHEMA",
    # R112: a bare golden-only tab name in criterion prose (weldon-bridge-plan Rubric Quality Review, 2026-09-11).
    "R112": "RUBQ-SCHEMA",
    # Stage 2d
    "A11": "DATA-SUFF", "A12": "DATA-SUFF", "A16": "DATA-OPEN", "A7": "DATA-BUDGET",
    "R23": "DATA-TIME", "W2": "DATA-TIME", "A18": "DATA-TIME", "L1": "DATA-LEAK",
    # L2: hidden-content leakage locations (hidden sheets/rows, comments, tracked
    # changes, input-deck speaker notes); T1: a tell log shipped inside a package.
    # Both from docs/submission/platform/creating-input-files.md (2026-08-26).
    "L2": "DATA-LEAK", "L3": "DATA-LEAK", "L4": "DATA-LEAK", "L5": "DATA-LEAK", "T1": "DATA-LEAK",
    "L6": "DATA-LEAK",      # a conclusion word in a note on an input row the golden cites
    # Stage 3
    "A6": "REV-PROSE", "A10": "REV-PROSE",
    # A20: a missing comma before a clause-joining conjunction, or three or more clauses in one
    # sentence - the two mechanical shapes of the sentence rule the lift-truck-fleet-plan reviewer
    # wrote out by hand and rejected on (2026-09-05). REV-REGISTER stays in NO_DETECTOR because the
    # serial comma, the comma splice and the rest of the rule are still a read.
    "A20": "REV-REGISTER",
    "G5": "GOLD-FID",       # a prose "X of the Y" count the golden's own tab contradicts
    "A17": "LLM-PKG",       # a formula cell carrying more than one cached <v>
    # mapped 2026-09-11 (repo rules audit): five codes that fired with no family
    "G4": "GOLD-FID",       # an under-agreement register line missing from the golden's correcting table
    "G21": "GOLD-FID",      # docx table figures that do not multiply out as printed
    "G22": "DATA-TIME",     # a snapshot input referencing later-dated records / an unfiltered as-of balance
    "R83": "PRE-COVER",     # the deliverable basename quoted in no positive criterion (filename format coverage)
    "R127": "PRE-COVER",    # a golden verdict column (TEST/CHECK/FLAG/VERDICT/CALL header) no positive criterion names
    "R98": "GOLD-LIVE",     # a strict liveness row's own subject cell is not the shape the row claims
    "R106": "GOLD-LIVE",    # a strict liveness anchor labelled by a bare noun the sentence uses for another quantity
    "R107": "RUBQ-GROUND",  # a positive pins a record id that sits only past row 28 of an input sheet
    "R108": "GOLD-LAND",    # a citation-by-file-name claim whose file name the golden never states
    "R109": "GOLD-LIVE",    # a gated "formula rather than a keyed date" clause over TEXT()-rendered dates
    "R125": "GOLD-LIVE",    # a gated count clause on a lone COUNT footer under a column of another head (twincreek 2026-09-14)
    "R110": "RUBQ-GROUND",  # a citation claim for a key whose records some input sheet holds only past row 28
    "A21": "REV-PROSE",     # a document whose sentences are half or more the status-report skeleton
    "G23": "GOLD-FID",
    "G38": "GOLD-FID",      # a second location the golden records never appears as a move-list from-location
    "G24": "GOLD-FID",      # a typed column that mirrors an input CSV aggregate drifts from it on some keys      # a spelled month-day date supported only by a workbook date cell
    "G25": "GOLD-FID",      # an organisation or facility name in a golden docx body, header or footer that no input and not the prompt carries
    "G27": "DATA-JOIN",     # a related-record id on a golden-cited input row that no input holds
    "G26": "GOLD-FID",      # a standard number, or a class/type/level/tier beside a standard, in the golden that no input and not the prompt carries
    "G28": "GOLD-FID",      # a prompt description title-cased into an organisation name in the golden (2026-09-14)
    "G29": "GOLD-FID",      # a banded input table with a shared endpoint, no inclusion rule, data on the line (2026-09-14)
    "G30": "GOLD-FID",      # a money column directly after a Yes/No column headed with a charge's name (kesselring refinement, 2026-09-14)
    "G31": "GOLD-FID",      # an open status claimed for every key with no source beside it while another input closes one
    "R115": "PRE-COVER",    # mapped 2026-09-11 for a check another session registered without a family
    "L4": "DATA-LEAK",      # mapped 2026-09-11 for a check another session registered without a family
    "R116": "PRE-DUP",      # the same "all N <noun>" completeness phrase on two positives
    "A22": "LLM-NUM",       # a duration column holding only multiples of 2 or 5
    "A23": "LLM-NUM",       # a money column holding only multiples of 500
    "A24": "LLM-NUM",       # a name column mostly on the nature-word + feature + trade pattern
    "A25": "REV-PROSE",     # a note or comment column filled on nearly every row from a dozen or fewer phrases
    "A27": "LLM-NUM",       # a date column with eight in ten dates on one fixed non-month-end day
    "A28": "LLM-NUM",       # one line-name vocabulary carried by three or more competing brands
    "A29": "LLM-NUM",       # a date column carrying one date on nineteen in twenty rows
    "A30": "LLM-NUM",       # a quantity column drawing a hundred values from seven or fewer figures
    "A55": "LLM-NUM",       # a cents-bearing money column whose per-key totals are whole dollars
    "A31": "LLM-NUM",       # a key column stepping by a constant stride larger than one
    "A32": "REV-PROSE",     # two or more generic report headings in one solution docx
    "A26": "REV-PROSE",     # a solution free-text column carrying one identical line on every populated row
    "R121": "RUBQ-RIGID",   # a positive presenting a named answer as "one acceptable answer" or "for example"
    "G33": "GOLD-FID",      # a prose superlative record count over a long CSV
    "G40": "GOLD-FID",      # a read-through label pointing the opposite way from its source row's label (tessendorf adjudication, 2026-09-15)
    "G39": "GOLD-FID",      # two docx tables keyed on the same rows with a like-named value column carrying different figures (crandall 2026-09-15)
    "G36": "GOLD-FID",      # a citation form (policy 4.1, ITB 5) no input uses (twincreek 2026-09-14)
    "R122": "RUBQ-RIGID",   # a positive scoring one business disposition against a named alternative (freight-audit-review adjudication, 2026-09-12)
    "H7": "PRE-PACK",       # a chronological reference CSV longer than the adjudication preview window (freight-audit-review, 2026-09-14)
    "H8": "PRE-PACK",       # a golden-cited id's input row in the hidden middle of a sheet longer than 40 rows
    "H9": "PRE-PACK",       # an input CSV field containing a comma, split naively by adjudication (dfl-freight-audit, 2026-09-15)
    "R134": "PRE-COVER",    # every prompt ask mapped to a golden anchor and a positive rubric row in clause-map.md (dfl-freight-audit rejection, 2026-09-15)
    "G41": "GOLD-FID",      # an action row defers an asked-for artifact, or one schedule stands in for one form per record (dfl-freight-audit rejection, 2026-09-15)
    "G42": "GOLD-FID",      # a phrase recorded in struck-phrases.md back anywhere in the package (dfl-freight-audit rejection, 2026-09-15)
    "G43": "GOLD-FID",      # verify_golden.py missing, failing, or a near flip the golden never settles (dfl-freight-audit rejection, 2026-09-15)
    "P8": "REV-CREDIBLE",   # a prompt due date or golden Date line under 21 days after the build (dfl-freight-audit rejection, 2026-09-15)
    "R130": "GOLD-FID",     # a positive criterion citing a numbered section no solution file names (crandall-program-allocation refinement, 2026-09-14)
    "R123": "GOLD-LAND",   # an identifier borrowed from an input written with a space or dash variant for its hyphen (standby-generator round 4, 2026-09-12)
    "R131": "GOLD-LAND",   # a positive criterion's section cite the golden states only past the read head of long prose cells (rempel-buyout-plan refinement round 2, 2026-09-14)
    "R133": "GOLD-LAND",   # a pinned decimal on a rounding tie or a rounded-first chain the single rounding disagrees with (hx4180-fa26-spec-rev3 adjudication, 2026-09-15)
}

# a check that also predicts another gate; shown, never double-counted
ALSO = {
    "R10": ["GOLD-KEY"],      # overlapping keys also double-score in the oracle
    "R22": ["GOLD-NEG"],      # the mirrored negative is also deducted by the oracle
    "R47": ["GOLD-LAND"],
    "W17": ["GOLD-NEG"],
    "R29": ["GOLD-LAND"],
    "A9":  ["GOLD-FID"],      # a cache the formula does not reproduce moves a pinned figure
    "A3":  ["REV-CREDIBLE"],  # reviewers check document metadata by hand too
    "G17": ["REV-CREDIBLE"],  # a title on a named person is a claim the adjudicator traces by hand
    "G18": ["REV-CREDIBLE"],  # an unanchored action date is a date that fails being checked
    "G19": ["REV-CREDIBLE"],  # a direction claim the signed figure contradicts is prose that fails being checked
    "G20": ["REV-CREDIBLE"],  # an unanchored dateline is a date that fails being checked
    "G25": ["REV-CREDIBLE"],  # the adjudicator reads the rendered page, footer included, and traces every named entity
    "G27": ["GOLD-FID"],      # a golden claim of consistent documentation rests on the join
    "G26": ["REV-CREDIBLE"],  # a code reference is a claim the adjudicator traces to the prompt or an input
    "G28": ["REV-CREDIBLE"],  # the grounding check reads a capitalised run as a name and traces it
    "G37": ["REV-CREDIBLE"],  # the attribution check matches an unscoped shared identifier to the wrong source
    "G29": ["REV-CREDIBLE"],  # adjudication calls an exactly graded total underdetermined on a shared band endpoint
    "A6":  ["LLM-SHAPE"],     # em-dash density feeds the machine check as well
    "A10": ["LLM-SHAPE"],
    "A25": ["LLM-SHAPE"],     # the authorship reader reads a stock-phrase column as generated fabric
    "A26": ["LLM-SHAPE"],     # the same reader on a golden tab, at any row count
    "A32": ["LLM-SHAPE"],     # the authorship reader lists generic headings as a MEDIUM on the output file
}

# Rules that .gate-debt may never cover. LLM-style prose is the finding a human reviewer
# trusts least and generalizes from hardest: one invented idiom or slogan costs their
# confidence in the whole task. It is also always cheap to fix — it is words, not fabric —
# so there is no case for carrying it. Per user, 2026-08-24.
NON_DEBTABLE = ("REV-PROSE",)

# Rules with no detector: nobody can automate them, and pretending otherwise is worse
# than saying so. They are printed on every run as a standing human check.
# REV-CREDIBLE has H2/H3 since 2026-09-04 but stays listed: names and metadata are still
# a human read.
NO_DETECTOR = ("REV-REGISTER", "REV-CREDIBLE", "RUBQ-RIGID", "REV-TRACE")

# --- review tiering ------------------------------------------------------------------
# How review_check.py tiers a registry finding on ANOTHER contributor's task. BAR rules
# are the ones docs/reviewer/platform/reviewer-guidelines-v5.1.md states in terms (file
# names and inputs named, substantial and readable inputs, golden accuracy, no answer
# leakage, no programme vocabulary, clean provenance, atomic and objective criteria, the
# rubric's form). Everything else is this repo's own authoring convention: it predicts an
# oracle flake or a platform check that is the submitter's problem, never a send-back.
# A rule absent here reads as HOUSE.
REVIEW_TIER = {
    "PRE-FILES": "BAR", "PRE-SOURCES": "BAR", "PRE-NAME": "BAR", "PRE-PACK": "BAR",
    "PRE-FORM": "BAR", "PRE-OBJ": "BAR",
    "GOLD-FID": "BAR", "DATA-LEAK": "BAR", "DATA-SUFF": "BAR", "DATA-OPEN": "BAR",
    # LLM-PKG was BAR until the team ruling of 2026-09-04 in #ec-geranium-project. ECs are
    # allowed to use an LLM to assist with inputs and goldens, so an openpyxl or python-docx
    # string is usually an artifact of permitted use, and the library is in any case a
    # legitimate way to load data faster than typing it. It is reviewer discretion, "not a
    # blanket or hard bounce back", and on some tasks the string is even appropriate to
    # leave. A generator string alone is therefore HOUSE on another contributor's task and
    # goes in the note as an observation, never as the reason it is going back.
    "LLM-PKG": "HOUSE",
}
# Per-code overrides where a rule's checks straddle the line: R27 (three or more figures in
# one criterion) is the atomicity shape the guidelines describe, the other RUBQ-ATOM shapes
# are house; R18 (grader-instruction wording) is a platform pre-check, not reviewer bar.
# A19 is the one LLM-PKG code that stays BAR: the team ruled on 2026-09-04 that a docProps
# creator or lastModifiedBy left as a placeholder such as the literal word "generated" is an
# automatic send-back, because it asserts nothing about who authored the file, which is a
# different thing from a tool name that records how it was written.
REVIEW_TIER_CODE = {"R27": "BAR", "R18": "HOUSE", "A19": "BAR"}


def review_tier(code):
    """BAR or HOUSE for a coded finding on another contributor's task."""
    if code in REVIEW_TIER_CODE:
        return REVIEW_TIER_CODE[code]
    return REVIEW_TIER.get(PRIMARY.get(code), "HOUSE")

# Criteria carrying one of these are the ones observed to flake: the oracle cannot
# reliably land on them, as opposed to criteria that are simply wrong.
FLAKE_CLASS = {r for r, rule in PRIMARY.items()
               if rule in ("GOLD-LAND", "GOLD-LIVE", "GOLD-NEG")}

# --- flake exposure -----------------------------------------------------------------
# The golden check is a PRODUCT, not an average: N criteria x 3 runs verdicts must every
# one come back 1.0. These rates were fitted to this portfolio's own history (15 tasks,
# 23 logged oracle rounds, 2026-08-19..24) by solving q = (1-p)^(3N) for the observed
# mean rounds-to-pass in each cohort: rubrics under 40 criteria took 1.4 rounds (q~0.71,
# N~32 -> p~0.35%), rubrics of 40+ took 4.5 rounds (q~0.22, N~47 -> p~1.07% blended).
# Splitting the blended rate at the ~30% flake-class share those rubrics carry gives the
# two constants below. Re-fit as the log grows; they are estimates from a small sample.
P_CLEAN = 0.0035
P_FLAKY = 0.027


def exposure(n_criteria, n_flaky):
    """P(all 3 oracle runs score exactly 1.0), given how many criteria are flake-prone."""
    if n_criteria <= 0:
        return None
    clean = max(n_criteria - n_flaky, 0)
    return (1 - P_CLEAN) ** (3 * clean) * (1 - P_FLAKY) ** (3 * n_flaky)


def unmapped(codes):
    """Coded checks that fired but carry no generalized rule — the map has a hole."""
    return sorted(c for c in codes if c not in PRIMARY)


def rules_for(code):
    p = PRIMARY.get(code)
    return ([p] if p else []) + ALSO.get(code, [])


# --- consolidated report ------------------------------------------------------------

def _by_rule(findings):
    """rule -> (errors, debt, criteria) for everything emitted."""
    out = {}
    for level, code, num, _msg in findings:
        rule = PRIMARY.get(code)
        if rule is None:
            continue
        e, d, crits = out.get(rule, (0, 0, set()))
        out[rule] = (e + (level == "ERROR"), d + (level == "DEBT"),
                     crits | ({num} if num else set()))
    return out


def report(findings, n_criteria, debt=(), out=print):
    """Print the lifecycle stages worst-first, as generalized rules.

    findings: (level, coded check, criterion number or None, message).
    n_criteria: rows in the task's rubric CSV, for the flake-exposure estimate.
    debt: (code, criterion) pairs carried in .gate-debt.
    """
    hits = _by_rule(findings)
    verdicts = {}
    for rep, (stage, name) in REPORTS.items():
        rules = [r for r, v in RULES.items() if v[0] == rep]
        e = sum(hits.get(r, (0, 0, set()))[0] for r in rules)
        d = sum(hits.get(r, (0, 0, set()))[1] for r in rules)
        verdicts[rep] = (stage, name, rules, e, d)

    out("  ── consolidated gate view ─────────────────────────────────────────────")
    for stage, (sname, when, cost) in STAGES.items():
        reps = [r for r, v in verdicts.items() if v[0] == stage]
        if stage == "ADJ":
            out(f"  {sname}  ({when}, {cost})")
            out("         ten documented checks (docs/submission/platform/task-lifecycle.md §4) — "
                "returned fixes go straight back to adjudication, bypassing human review")
            continue
        se = sum(verdicts[r][3] for r in reps)
        sd = sum(verdicts[r][4] for r in reps)
        flag = "FAIL" if se else ("debt" if sd else "ok")
        out(f"  [{flag:4s}] {sname}  ({when}, {cost})")
        for rep in reps:
            _s, name, rules, e, d = verdicts[rep]
            tail = ""
            if rep == "GOLDEN":
                flaky = {n for _l, c, n, _ in findings if c in FLAKE_CLASS and n}
                p = exposure(n_criteria, len(flaky))
                if p is not None:
                    tail = (f" · {n_criteria} criteria, {len(flaky)} flake-prone"
                            f" → P(3/3 clean) ≈ {p:.0%}")
            if not (e or d) and not tail:
                continue
            out(f"      {name}{tail}")
            for rule in rules:
                re_, rd, crits = hits.get(rule, (0, 0, set()))
                if not (re_ or rd):
                    continue
                cs = ("C" + ", C".join(sorted(crits, key=lambda x: int(x) if x.isdigit() else 0))
                      if crits else "")
                counts = ", ".join(x for x in (
                    f"{re_} error" + "s" * (re_ != 1) if re_ else "",
                    f"{rd} debt" if rd else "") if x)
                out(f"        {rule:13s} {counts:18s} {cs[:50]}")
                out(f"        {'':13s} {RULES[rule][1]}")
    out("         no detector, check by hand: " + ", ".join(
        f"{r} ({RULES[r][1].rstrip('.')})" for r in NO_DETECTOR if r in RULES))
    if debt:
        out(f"         carried as debt in .gate-debt: {len(debt)} findings")
    return verdicts


def explain(rule, out=print):
    """Print one generalized rule in full, with the coded checks that implement it."""
    if rule not in RULES:
        out(f"no such rule: {rule}")
        return
    rep, oneline, why = RULES[rule]
    stage, repname = REPORTS[rep]
    codes = sorted(c for c, r in PRIMARY.items() if r == rule)
    also = sorted(c for c, rs in ALSO.items() if rule in rs)
    out(f"{rule}")
    out(f"  stage : {STAGES[stage][0]}  ({STAGES[stage][1]}, {STAGES[stage][2]})")
    out(f"  report: {repname}")
    out(f"  rule  : {oneline}")
    out(f"  why   : {why}")
    out(f"  coded : {', '.join(codes) if codes else 'nothing — human check only'}")
    if also:
        out(f"  also  : {', '.join(also)} (primary elsewhere)")


def main(argv):
    if len(argv) > 1 and argv[1] in RULES:
        explain(argv[1])
        return 0
    for stage, (sname, when, cost) in STAGES.items():
        print(f"\n{sname}   ({when}, {cost})")
        if stage == "ADJ":
            print("  ten documented checks (docs/submission/platform/task-lifecycle.md §4); returned")
            print("  fixes go straight back to adjudication, bypassing human review")
            continue
        for rep, (st, repname) in REPORTS.items():
            if st != stage:
                continue
            print(f"  {repname}")
            for rule, (r, oneline, _why) in RULES.items():
                if r != rep:
                    continue
                codes = sorted(c for c, x in PRIMARY.items() if x == rule)
                print(f"    {rule:13s} {oneline}")
                print(f"    {'':13s} {len(codes)} coded: {', '.join(codes) or 'none — human check'}")
    print(f"\n{len(RULES)} generalized rules over {len(PRIMARY)} coded checks.")
    print("Run with a rule id for the full statement, e.g. gate_families.py GOLD-LIVE")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv))
