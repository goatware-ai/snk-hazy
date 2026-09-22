"""Procedural rules: house rules no check can test mechanically, registered here so they
carry an id the docs, prompts and memory can cite the way they cite a check code.

`autoeval_check.py --rules` writes them into docs/rules.md under "Procedural rules (not
mechanically checked)". Add a rule as one dict; keep the statement to one sentence.
"""

PROCEDURAL = [
    {"id": "PR1",
     "statement": "Keep every worked example inside the first 25 data rows of an input and never "
                  "pin a count a partial read cannot reproduce: the Rubric Quality Review reads "
                  "inputs through a 28-row window (28 observed, 25 prescribed, a cushion of 3); the "
                  "record-id arm is coded as R107, counts and quantities stay by hand.",
     "source": "memory/rubric-coverage-and-completeness.md (2026-09-01; 2026-09-03)"},
    {"id": "PR2",
     "statement": "Run no stb command in a revision; accept, revise or skip is never issued from "
                  "this desk.",
     "source": "memory/revision-workflow.md"},
    {"id": "PR3",
     "statement": "Package in this order: tools/office_resave.py --force, then fix_floats, then "
                  "fix_metadata, then build the zips, then run the gate.",
     "source": "memory/package-hygiene-pipeline.md (2026-09-02)"},
    {"id": "PR4",
     "statement": "A revision runs under the model recorded in the task's metadata.json built_with.",
     "source": "memory/model-routing.md"},
    {"id": "PR6",
     "statement": "When a golden's figures are totals over an input longer than the review window, the "
                  "deliverable carries a per-key ledger (account, route) whose rows sum to the stated "
                  "totals and names the record ids behind any single-account figure, so a partial read "
                  "can still trace them (2026-09-11: a grader read about forty of "
                  "117 log rows and called every route total fabricated).",
     "source": "memory/golden-fidelity.md (2026-09-11)"},
    {"id": "PR7",
     "statement": "The prompt's experience sentence (P4c) is written fresh for the task: the portfolio's "
                  "stock phrasings ('a few years of X behind you/them', 'this is coming to you because') "
                  "sit in sixteen prompts, and a re-entered prompt carrying them failed the platform's "
                  "in-app prompt uniqueness check where the task's earlier wording had passed "
                  "(2026-09-11).",
     "source": "house rule since 2026-09-11. Uniqueness is checked by hand against this desk's own drafts, submissions and accepted work, with the occupation counting as part of a task's identity"},
    {"id": "PR9",
     "statement": "A criterion grading a computation an input clause defines names every factor the "
                  "clause states (rate, base and period alike): a row naming fewer factors credits a "
                  "formula the clause forbids, and adjudication reads the row against the clause "
                  "(2026-09-12: 'the order total at the policy "
                  "carrying rate' let a flat 18% formula earn the point where policy 7.2 halves the "
                  "coverage period).",
     "source": "memory/rubric-liveness-criteria.md (2026-09-12)"},
    {"id": "PR10",
     "statement": "Every person the prompt names carries their role beside their name in an input (a "
                  "signature line, an addressee line, 'Gail, my purchasing manager'); a role the reader "
                  "joins across two sentences or two documents is inferred, and adjudication traces it "
                  "as unsourced whether or not the golden states the title (2026-09-11 to 09-14: "
                  "on one task the title was removed in an early round and the trace returned twice "
                  "more until the email stated the role beside the name). "
                  "G17 catches the title on a header line; the untitled inference is read by hand.",
     "source": "memory/golden-fidelity.md (2026-09-14)"},
    {"id": "PR8",
     "statement": "A deliverable byline names only the recipient an input establishes and the plan "
                  "date; it carries no preparer clause, by person or by department, unless an input "
                  "assigns that role, because adjudication traces the clause to the one person the "
                  "inputs place in that department (2026-09-12: 'Prepared for purchasing' was read "
                  "back to a person the terms sheet names only as its checker).",
     "source": "memory/golden-fidelity.md (2026-09-12)"},
    {"id": "PR11",
     "statement": "The Section 3 paragraph (review-comment.md) never introduces a person the deliverable "
                  "does not name: the adjudicator's trace reads it as a claim source and quoted the "
                  "submitter's own sentence about the terms sheet's checker back as a finding after the "
                  "workbook itself was clean (2026-09-14); "
                  "describe such a person by role.",
     "source": "memory/revision-workflow.md (2026-09-14)"},
    {"id": "PR12",
     "statement": "A single-key figure the golden builds from a few rows of a long CSV (an account's own "
                  "drive and selling minutes over eight visits) has those rows inside adjudication's "
                  "preview window, the first 25 and last 15 lines, by relaying the file into side-by-side "
                  "panels or one row per key, never by moving the key's rows to the top: a lead block "
                  "hands the solver the scope decision by file order (2026-09-15), and cited ids "
                  "alone are called untraceable when the rows are hidden (2026-09-14). "
                  "H8 codes the cited-row arm; a broad rule over "
                  "every register id lit up seven goldens that cite ids legitimately deep in their CSVs.",
     "source": "memory/golden-fidelity.md (2026-09-14, 2026-09-15)"},
    {"id": "PR13",
     "statement": "A rubric row grades only an action inside the scope the prompt sets for actions "
                  "(\"what we change on our own dock\"), never a planning choice the golden adds on its "
                  "own (a filing date ahead of a meeting, a written confirmation asked of the carrier): "
                  "adjudication reads those rows as grading operational choices the prompt never requests "
                  "(2026-09-14). The golden may still carry the choice as "
                  "content; the rubric may not score it. Fuzzy to code: the scope phrase differs per prompt.",
     "source": "memory/rubric-coverage-and-completeness.md (2026-09-14)"},
    {"id": "PR14",
     "statement": "Before every resubmission the platform's input file list holds exactly the i- zip's "
                  "members and never the deliverable: the input widget keeps every upload it was ever "
                  "given, and an s- zip dropped there ships the golden as an input; the fetch-task "
                  "JSON's input_files list is the read-back (an adjudication, 2026-09-14; L5 catches "
                  "a staged copy, nothing in the repo can see the widget).",
     "source": "memory/revision-workflow.md (2026-09-14)"},
    {"id": "PR15",
     "statement": "A hedged per-item finding in the golden ('if one request is a duplicate, 110 units stay "
                  "unexplained') is restated elsewhere only in the same hedged form: no later sentence turns it "
                  "into a definite position or direction (a 'true position', 'would overstate the need'); the "
                  "internal-contradiction check reads every summary-level claim against the detail and lists the "
                  "pair.",
     "source": "a late revision round's feedback log (2026-09-14)"},
    {"id": "PR16",
     "statement": "A rubric row that asks which items of a schedule fall in a class ('which of the "
                  "corrective actions are changes to a procedure rather than re-approvals') is met in "
                  "the golden by a per-row marker column beside the items (a Yes/No 'Procedure change' "
                  "column), never by a prose sentence listing the members above the table: the oracle "
                  "judge reads the table for the per-row attribute and failed the prose form 1 of 3 runs "
                  "(2026-09-14). The rubric row is "
                  "worded per item ('for each item, whether it is ...'). One hit portfolio-wide, so it "
                  "stays procedural.",
     "source": "memory/rubric-anchoring-and-landing.md (2026-09-14)"},
    {"id": "PR17",
     "statement": "An adjudication or review note can be written against a version the platform no "
                  "longer holds: before changing anything, read the note's cited content (population "
                  "figures, names, counts, criteria it says are missing) against the live copy "
                  "(a pasted fetch-task JSON). An item the live copy "
                  "already answers is a trace-lag item: change nothing for it, confirm on the form "
                  "that the rows and files are there, and say so in the feedback log. "
                  "(An adjudication, 2026-09-14: the note asked for three rubric "
                  "rows and named an author that the platform's live copy "
                  "already carried and had already dropped.)",
     "source": "memory/revision-workflow.md (2026-09-14)"},
    {"id": "PR18",
     "statement": "Every zip-upload form action tells the operator to confirm the upload's uploadedAt moved, "
                  "and a round closes only after a re-fetch shows both zip stamps on the round's day: "
                  "one revision round (2026-09-14) had its criteria re-entered while the zips "
                  "never went up, and the next adjudication note was written against an earlier "
                  "round's golden and the first round's inputs.",
     "source": "memory/revision-workflow.md (2026-09-14)"},
    {"id": "PR19",
     "statement": "From a task's third return, the revision rebuilds the package from clause-map.md: "
                  "every prompt ask is re-read against the golden and the rubric, every finding from "
                  "earlier rounds is re-checked in every file, and only then are the items the new note "
                  "names fixed; patching the named items alone let one task carry an unmet ask "
                  "through eleven rounds to rejection (2026-09-15). R134 checks the map's Rebuilt date.",
     "source": "memory/revision-workflow.md (2026-09-15)"},
    {"id": "PR20",
     "statement": "Every phrase a reviewer or check strikes, and every claim a fix removes, is recorded the "
                  "same day as a bullet in the task's struck-phrases.md, as a literal in double quotes or a "
                  "/pattern/ that also catches the claim reworded, followed by its source and date; G42 then "
                  "searches the whole package for it (2026-09-15: a struck Appendix B "
                  "claim survived in a table cell).",
     "source": "memory/revision-workflow.md (2026-09-15)"},
    {"id": "PR21",
     "statement": "Before a build is called done, list every decision the golden makes and name where a "
                  "solver learns the fact it turns on; a fact that sits in a column naming the rule, or "
                  "in the sentence that states the rule, is relocated into a record's own prose, a "
                  "second file that must be reconciled, or a status column a reader can skip, and a "
                  "numbered rule an input carries that the golden never applies is made to decide "
                  "something (2026-09-22: the desk's first difficulty_check FAIL, two of four weak-model "
                  "attempts clearing a rubric whose every trap was labelled). L7 catches the labelled "
                  "exception column; the rest is read by hand.",
     "source": "memory/difficulty-check-lessons.md (2026-09-22)"},
    {"id": "PR22",
     "statement": "A numbered rule an input carries that turns on a supporting document or a written act "
                  "(a certificate attached, a certified scale ticket, a confirmation in writing before "
                  "delivery, a bulletin the contract subordinates to its table) is exercised on both arms "
                  "in the inputs, with a record that satisfies it and a look-alike that does not (an "
                  "unsigned notice, a dock readout, a ticket inside the tolerance, a request refused after "
                  "delivery), so that the golden's call on each turns on reading the record and never on "
                  "the two-file mismatch alone (2026-09-22: the desk's second difficulty_check FAIL, a "
                  "rating audit whose every exception was a mismatch between two tidy CSVs that a script "
                  "reproduces; one weak-model attempt in three cleared it).",
     "source": "memory/difficulty-check-lessons.md (2026-09-22)"}
]
