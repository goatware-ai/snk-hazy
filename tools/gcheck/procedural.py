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
     "source": "memory/rubric-coverage-and-completeness.md (returns-cage 2026-09-01; pick-module-reslot "
               "round 4, 2026-09-03)"},
    {"id": "PR2",
     "statement": "Run no stb command in a revision; a review may fetch (tools/fetch_review.py), and "
                  "accept, revise or skip is never issued from this desk.",
     "source": "memory/revision-workflow.md; memory/review-task-workflow.md"},
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
                  "can still trace them (harlow refinement, 2026-09-11: a reviewer read about forty of "
                  "117 log rows and called every route total fabricated).",
     "source": "memory/golden-fidelity.md (2026-09-11); refinements/baac9089-8d6c-498a-859a-c4f9bbc42294/change.log"},
    {"id": "PR7",
     "statement": "The prompt's experience sentence (P4c) is written fresh for the task: the portfolio's "
                  "stock phrasings ('a few years of X behind you/them', 'this is coming to you because') "
                  "sit in sixteen prompts, and a re-entered prompt carrying them failed the platform's "
                  "in-app prompt uniqueness check where the task's earlier wording had passed "
                  "(pick-module-reslot, 2026-09-11).",
     "source": "memory/task-uniqueness-check.md (2026-09-11); submissions/44-pick-module-reslot/feedback-log.md"},
    {"id": "PR9",
     "statement": "A criterion grading a computation an input clause defines names every factor the "
                  "clause states (rate, base and period alike): a row naming fewer factors credits a "
                  "formula the clause forbids, and adjudication reads the row against the clause "
                  "(weldon-bridge-plan refinement round 3, 2026-09-12: 'the order total at the policy "
                  "carrying rate' let a flat 18% formula earn the point where policy 7.2 halves the "
                  "coverage period).",
     "source": "memory/rubric-liveness-criteria.md (2026-09-12); refinements/53be0f9b-2e98-40f2-a3f6-681e48981466/change.log"},
    {"id": "PR10",
     "statement": "Every person the prompt names carries their role beside their name in an input (a "
                  "signature line, an addressee line, 'Gail, my purchasing manager'); a role the reader "
                  "joins across two sentences or two documents is inferred, and adjudication traces it "
                  "as unsourced whether or not the golden states the title (weldon-bridge-plan "
                  "refinement rounds 1 to 4, 2026-09-11 to 09-14: the title was removed in round 1 and "
                  "the trace returned twice more until the email stated the role beside the name). "
                  "G17 catches the title on a header line; the untitled inference is read by hand.",
     "source": "memory/golden-fidelity.md (2026-09-14); refinements/53be0f9b-2e98-40f2-a3f6-681e48981466/change.log"},
    {"id": "PR8",
     "statement": "A deliverable byline names only the recipient an input establishes and the plan "
                  "date; it carries no preparer clause, by person or by department, unless an input "
                  "assigns that role, because adjudication traces the clause to the one person the "
                  "inputs place in that department (inbound-consolidation-plan refinement round 3, "
                  "2026-09-12: 'Prepared for purchasing' was read back to Adele Brakhane, whom the "
                  "terms sheet names only as its checker).",
     "source": "memory/golden-fidelity.md (2026-09-12); refinements/a784d07d-e579-42d5-8b51-0d3cfab07811/change.log"},
    {"id": "PR11",
     "statement": "The Section 3 paragraph (review-comment.md) never introduces a person the deliverable "
                  "does not name: the adjudicator's trace reads it as a claim source and quoted the "
                  "refiner's own sentence about the terms sheet's checker back as a finding after the "
                  "workbook itself was clean (inbound-consolidation-plan refinement round 4, 2026-09-14); "
                  "describe such a person by role.",
     "source": "memory/revision-workflow.md (2026-09-14); refinements/a784d07d-e579-42d5-8b51-0d3cfab07811/change.log"},
    {"id": "PR12",
     "statement": "A single-key figure the golden builds from a few rows of a long CSV (an account's own "
                  "drive and selling minutes over eight visits) has those rows inside adjudication's "
                  "preview window, the first 25 and last 15 lines, by relaying the file into side-by-side "
                  "panels or one row per key, never by moving the key's rows to the top: a lead block "
                  "hands the solver the scope decision by file order (recall-response refinement, "
                  "2026-09-15), and cited ids alone are called untraceable when the rows are hidden "
                  "(harlow refinement round 8, 2026-09-14). H8 codes the cited-row arm; a broad rule over "
                  "every register id lit up seven goldens that cite ids legitimately deep in their CSVs.",
     "source": "memory/golden-fidelity.md (2026-09-14, 2026-09-15); refinements/baac9089-8d6c-498a-859a-c4f9bbc42294/change.log"},
    {"id": "PR13",
     "statement": "A rubric row grades only an action inside the scope the prompt sets for actions "
                  "(\"what we change on our own dock\"), never a planning choice the golden adds on its "
                  "own (a filing date ahead of a meeting, a written confirmation asked of the carrier): "
                  "adjudication reads those rows as grading operational choices the prompt never requests "
                  "(dfl-freight-audit adjudication, 2026-09-14). The golden may still carry the choice as "
                  "content; the rubric may not score it. Fuzzy to code: the scope phrase differs per prompt.",
     "source": "memory/rubric-coverage-and-completeness.md (2026-09-14); submissions/43-dfl-freight-audit/feedback-log.md"},
    {"id": "PR14",
     "statement": "Before every resubmission the platform's input file list holds exactly the i- zip's "
                  "members and never the deliverable: the input widget keeps every upload it was ever "
                  "given, and an s- zip dropped there ships the golden as an input; the fetch-task "
                  "JSON's input_files list is the read-back (commission-review-q2 adjudication, "
                  "2026-09-14; L5 catches a staged copy, nothing in the repo can see the widget).",
     "source": "memory/revision-workflow.md (2026-09-14); submissions/48-commission-review-q2/feedback-log.md"},
    {"id": "PR15",
     "statement": "A hedged per-item finding in the golden ('if one request is a duplicate, 110 units stay "
                  "unexplained') is restated elsewhere only in the same hedged form: no later sentence turns it "
                  "into a definite position or direction (a 'true position', 'would overstate the need'); the "
                  "internal-contradiction check reads every summary-level claim against the detail and lists the "
                  "pair.",
     "source": "refinements/58c17e52-7d6b-4e16-b3e0-4ea51b3eb66f/feedback-log.md (round 9, 2026-09-14)"},
    {"id": "PR16",
     "statement": "A rubric row that asks which items of a schedule fall in a class ('which of the "
                  "corrective actions are changes to a procedure rather than re-approvals') is met in "
                  "the golden by a per-row marker column beside the items (a Yes/No 'Procedure change' "
                  "column), never by a prose sentence listing the members above the table: the oracle "
                  "judge reads the table for the per-row attribute and failed the prose form 1 of 3 runs "
                  "(purchasing-review-jan-jul-2026 refinement round 2, 2026-09-14). The rubric row is "
                  "worded per item ('for each item, whether it is ...'). One hit portfolio-wide, so it "
                  "stays procedural.",
     "source": "memory/rubric-anchoring-and-landing.md (2026-09-14); refinements/ad4181ea-8946-4ba5-b724-c47f03c2a55e/change.log"},
    {"id": "PR17",
     "statement": "An adjudication or review note can be written against a version the platform no "
                  "longer holds: before changing anything, read the note's cited content (population "
                  "figures, names, counts, criteria it says are missing) against the live copy "
                  "(tools/restore_submission.py or a pasted fetch-task JSON). An item the live copy "
                  "already answers is a trace-lag item: change nothing for it, confirm on the form "
                  "that the rows and files are there, and say so in the feedback log. "
                  "(po-conformance-review adjudication 2026-09-14: the note asked for three rubric "
                  "rows and named an author that the platform's copy, restored the same morning, "
                  "already carried and had already dropped.)",
     "source": "submissions/38-po-conformance-review/feedback-log.md (2026-09-14); memory/revision-workflow.md"},
    {"id": "PR18",
     "statement": "Every zip-upload form action tells the operator to confirm the upload's uploadedAt moved, "
                  "and a round closes only after a re-fetch shows both zip stamps on the round's day: "
                  "recall-response refinement round 4 (2026-09-14) had its criteria re-entered while the zips "
                  "never went up, and the next adjudication note was written against round 2's golden and "
                  "round 1's inputs.",
     "source": "memory/revision-workflow.md (2026-09-14)"},
    {"id": "PR19",
     "statement": "From a task's third return, the revision rebuilds the package from clause-map.md: "
                  "every prompt ask is re-read against the golden and the rubric, every finding from "
                  "earlier rounds is re-checked in every file, and only then are the items the new note "
                  "names fixed; patching the named items alone let dfl-freight-audit carry an unmet ask "
                  "through eleven rounds to rejection (2026-09-15). R134 checks the map's Rebuilt date.",
     "source": "memory/revision-workflow.md (2026-09-15); archived/43-dfl-freight-audit, feedback-log.md in git c2c5874"},
    {"id": "PR20",
     "statement": "Every phrase a reviewer or check strikes, and every claim a fix removes, is recorded the "
                  "same day as a bullet in the task's struck-phrases.md, as a literal in double quotes or a "
                  "/pattern/ that also catches the claim reworded, followed by its source and date; G42 then "
                  "searches the whole package for it (dfl-freight-audit, 2026-09-15: a struck Appendix B "
                  "claim survived in a table cell).",
     "source": "memory/revision-workflow.md (2026-09-15)"},
]
