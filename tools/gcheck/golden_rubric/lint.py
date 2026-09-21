"""Lint rubric CSV files for wording patterns that fail the AutoEval oracle judge.

Every check below corresponds to a failure actually observed on this portfolio
(tasks 06/07/08, 2026-08-18). Run before every submission:

    .venv/bin/python tools/rubric_lint.py                          # lint every rubric under submissions/
    .venv/bin/python tools/rubric_lint.py path/to/rubric-{task-name}-{uid8}.csv

Exit code 1 if any finding is open. Findings are binary: every check below
corresponds to a platform failure observed on this portfolio.

Checks:
  E1 negative-polarity pin   Negative-weight criterion lacks an explicit polarity
                             marker. Bare defect statements drew
                             ambiguous_negative_polarity on 3/3 oracle runs.
                             Accepted markers: defect-frame words (incorrectly,
                             violating, beyond what X supports, contradicts) or
                             the legacy meet-style pin ("met only when ...") —
                             but see W9: prefer the defect-frame; the platform's
                             Agentic Rubric Quality Review misreads meet-style
                             pins as inverted polarity (task 07
                             needs_improvement, 2026-08-19, all four pinned
                             negatives flagged major). The "... is not this
                             defect" carve-out no longer counts and no longer
                             belongs anywhere: the platform's negative polarity
                             check fails it as scoring scaffolding (tessendorf
                             pre-submission, 2026-08-26; autoeval R18).
  E2 any-quantifier          Negative-weight criterion states the defect over a bare
                             plural subject ("Key outputs ... are ...") instead of
                             "At least one ..." / "any ..." — quantifier ambiguity.
  W1 zero-qty rows           "appears on no ... line"-style wording breaks when the
                             golden keeps the item visible as a zero-quantity row.
                             Prefer "no <sheet> claims any units of X" + a carve-out.
  W2 relative window         A relative time window (preceding/trailing/last N
                             months) with no absolute date in the criterion — anchor
                             it ("invoices dated 08/06/2023 through 08/06/2026").
  W3 csv re-sum              Criterion asks the judge to re-derive an aggregate from
                             a raw input file ("sum ... over every ... in x.csv") —
                             drew unverifiable_from_deliverable. State the figures as
                             facts checkable in the deliverable instead.
  W4 chain acceptance        Formula-liveness criterion rejects constants but does not
                             say reference chains count — judges flag ='Tab'!A1 links
                             as typed. Add "or a chain of cell references ...".
  W5 unpinned carve-out      A "may be typed" carve-out that names no dollar value —
                             judges miss unpinned carve-outs; name the exact figure
                             and source file.
  W6 liveness-mirror         Negative-weight formulas-vs-constants criterion. Judges
                             cannot verify the universal negative ("no key output
                             anywhere is typed") and deduct it deterministically —
                             a polarity pin does NOT save it (proven on task 07 run 2,
                             5/120 lost on all 3 runs). Drop it: positive liveness
                             criteria already cover this. Only a tightly scoped
                             single-column check has a chance of surviving.
  W7 counterfactual          Criterion asks the judge to simulate a dynamic behavior
                             ("removing/changing X recomputes Y") on a static file —
                             flaky 1-2 of 3 runs (marathon C32 run 3, hartwell C3/C9
                             run 4, deadstock C18 run 3 — whose "re-quantifying ...
                             re-sorts ... without manual edits" slipped the first
                             regex, all 2026-08-19). Reword to the answer-keyed static
                             form: name the golden cells/columns, disclaim look-alike
                             intermediate columns, accept rounding above exact targets.
  W8 sibling-cost spot-check A positive criterion pins a dollar value to a net/invoice/
                             landed cost (or a specific price level) but carries no
                             answer-key anchor — no golden cell reference, no arithmetic
                             chain, no look-alike-column disclaimer. On rows carrying
                             several cost-like columns the oracle judge reads a sibling
                             column 1-in-3 runs and fails a correct golden (hartwell C2
                             run 3, C3/C9 run 4, C8/C35 run 5, each a different criterion
                             per run — passing 3/3 once is NOT evidence of stability).
                             Anchor it: "(golden reference: Tab!Cell)", the multiplication
                             chain, and "does not answer this criterion" on the siblings.
  W10 chain-journey         Positive liveness criterion frames verification as a
                             reference chain or hop endorsement ("chain", "hop")
                             without telling the judge no tracing is needed. Flaked
                             a different way each oracle run on marathon C29 even
                             with every hop pre-endorsed (run 4 sheet-stat misread,
                             run 5 arithmetic-hop stall, run 6 value-mode read of
                             the SUMIFS range reported "not_observed", all
                             2026-08-19). Anchor the decision to the aggregation
                             range's stored formulas ("'Tab'!C3:C30 each store a
                             SUMIFS"), state that displayed numbers there are
                             cached formula results, and carve out downstream
                             cells with "pass; no tracing needed".
  W18 unframed negative      Negative criterion whose defect sentence carries no
                             defect-frame word, leaning on a trailing "is not this
                             defect" carve-out alone. The Agentic Rubric Quality
                             Review then reads the defect sentence as what a correct
                             deliverable does and reports the whole negative block as
                             inverted polarity (task 20, 2026-08-23, -16 exposure).
                             The frame handles polarity and is the only marker
                             left: the carve-out itself is banned as scoring
                             scaffolding (2026-08-26, autoeval R18), and count
                             pins already fail a misclassifying solver.
  W19 ambiguous defect verb  Negative criterion whose MAIN verb (counts / shows / lists /
                             reports / tracks / identifies / records / flags) names something
                             a COMPLIANT deliverable also does. A defect frame does not save
                             it: task 28 C29 read "The demand base counts invoice lines
                             carrying a job number ... in violation of policy 4.2" and the
                             Agentic Rubric Quality Review still rated the polarity inverted
                             [critical], -4 exposure (2026-08-24), answering that a correct
                             base counts those lines too (it shows them in a column of its
                             own). W18 passed it, because the frame was present. Name the
                             prohibited ACT: includes / is left with / is counted inside /
                             is incorrectly taken. Scoped to the leading clause, since the
                             same verbs are harmless in a subordinate evidence clause.
  W9 meet-style pin          Negative criterion pins polarity with "met only when /
                             does not meet" language. The oracle scores it correctly,
                             but the Agentic Rubric Quality Review parses "does not
                             meet" as "compliant responses lose points" and rates the
                             rubric needs_improvement (task 07, 2026-08-19). Reword to
                             the defect-frame: state the fault with incorrectly /
                             violating / beyond-what-X-supports / contradicts, with no
                             carve-out sentence (banned 2026-08-26, autoeval R18).
  W11 universal-sweep positive A positive criterion sweeps "every/all <items/prices/
                             rows>" with no answer-key anchor. The judge cannot verify
                             the sweep exhaustively and flakes: hartwell run 6 failed
                             the 47-SKU completeness sweep (judge re-derived the count
                             and tripped on FROZEN/DEFERRED rows) and the rounding-grid
                             sweep (judge misread trailing-zero display 47.5 / 37 as
                             off-grid) 1/3 each — both had passed 3/3 twice before.
                             Anchor it: state the exact qualifying count with the
                             exclusion arithmetic inline, name golden reference rows/
                             cells and a worked example, pin display quirks (no
                             trailing zeros), carve out held/excluded rows.
                             Extended 2026-08-20 (hollenbach run 2): the criterion-
                             initial quantifier now includes "Each ..." and the noun
                             list "action" — "Each action the plan calls for carries
                             an owner and a date" swept unstructured prose across the
                             whole workbook and failed 3/3 oracle runs; the fix is a
                             named table the sweep can be read off (a briefing action
                             list with a stated row count), not a reword. Mid-text
                             "each" stays unmatched: "each line carried at a whole
                             multiple" inside an anchored figures criterion is a
                             per-row qualifier, not a sweep (hollenbach C11 passes
                             3/3 with it).
  W12 golden-schema imposition Criterion cites a golden Sheet!Cell reference or a
                             named column ("the New Landed column", or the header token
                             directly: "carries 101 under ORDER PT" -- added 2026-08-24,
                             task 28 run 6, same imposition in a form the "... column"
                             pattern missed; "under INV-4 8.3" is a policy clause and is
                             excluded). The Agentic
                             Rubric Quality Review rates this needs_improvement as
                             misaligned_or_unjustified_rigidity when the prompt never
                             specifies that schema (hartwell 2026-08-19: 11 criteria,
                             ~31 pts — the very "(golden reference: Repricing!R48)"
                             anchors added for oracle stability). Resolution that
                             satisfies BOTH judges: keep the numeric answer key and
                             full arithmetic chain (those fixed the oracle flakes;
                             C2 stable 6 runs on arithmetic alone), disambiguate
                             sibling figures by VALUE ("the pre-surcharge 4.74 …
                             not the landed cost"), name no sheets/columns unless
                             the prompt mandates them (a prompt-required briefing
                             tab is fine to name). Fix a W12 BEFORE submission even
                             on oracle-proven wording: deadstock C17 passed the
                             oracle 3/3 with its golden refs, was left standing per
                             the don't-trim-proven-wording stance, and the quality
                             review then failed it (2026-08-19) — a standing W12 is
                             a live platform-FAIL pattern, unlike judge-legibility
                             reports (W7/R7), which proven wording may override.
  W17 rule-application negative
                             Negative criterion whose defect is that a named rule,
                             clause or article was APPLIED (or not applied) to a
                             record: "X is carried onto Y", "X is reset under
                             Article 5", "which <doc> does not support/reach".
                             The oracle flags these ambiguous_negative_polarity
                             whatever the pin, the same as the W6 liveness mirrors
                             and the W15 method sweeps (bergendahl run 1,
                             2026-08-21: two such negatives flagged, rewards
                             [0.0, 0.0, 1.0], while the two content-fact negatives
                             on the same rubric passed clean). The judge has to
                             decide both what the deliverable did AND whether the
                             rule permitted it, which is two verdicts inside one
                             negative. Drop them where positives already pin the
                             correct values, or restate the defect as a content
                             fact about a quantity or a value in the deliverable.
  W15 method-sweep negative Negative criterion whose defect is HOW a figure was
                             computed or WHICH source column it came from ("compared
                             against the last cost", "computed by applying X in place
                             of Y", "taken from ... rather than ..."). The oracle
                             flags these ambiguous_negative_polarity regardless of
                             pinning, the same way it does the formulas-vs-constants
                             mirrors in W6 (wamhoff run 1, 2026-08-20: two such
                             negatives flagged 3/3 and routed to manual review while
                             the content-fact negatives on the same rubric passed
                             clean). Drop them when positive criteria already pin the
                             correct values, or restate the defect as a content fact
                             about a quantity or value in the deliverable.
  W14 stacked negations      Negative criterion carrying 3+ negation tokens outside its
                             "is not this defect" pin. The oracle flags it
                             ambiguous_negative_polarity and routes it to manual review
                             rather than scoring it (dillman's briefing negative, 3/3
                             runs 2026-08-19). Every negative in the catalog that scored
                             cleanly sits at 0-2. submission.md already requires negatives
                             worded affirmatively ("[-5] The deliverable has X issue",
                             never "does not contain"); this enforces it.
  W13 absence-as-observable  Positive criterion asserts blankness/absence as a thing
                             to observe ("its new L1-L4 prices are blank or absent").
                             The judge's search tools grep cached values; absence
                             greps to nothing and the tool reports not_observed even
                             while quoting the surrounding evidence (hartwell C14/C35
                             run 7 — the judge quoted the frozen row note AND the
                             briefing bullet, then failed both criteria 1/3). Recast
                             in the C16 shape (3/3 stable): lead with the grep-able
                             positive fact, state that blank/absent/unchanged fields
                             all SATISFY the criterion, and end "fails only if
                             <positive evidence of the defect>". If the row shows
                             look-alike sibling values (current prices beside the
                             blank new-price fields), name them in the criterion as
                             not-new-assignments — hartwell run 9 flaked C35 when
                             the judge read current prices 6.25/5.35/4.8/4.45 as
                             "new L1-L4 prices assigned" (run-9 refinement; not
                             separately lintable without workbook data).

Folded into gcheck on 2026-09-04; tools/rubric_lint.py is the command.
"""
import re
import sys
from pathlib import Path

from ..common import MONTHS_RE, load_rows, split_clauses


# "not this defect" came out of the accepted markers 2026-08-26: the platform's negative
# polarity check now fails the carve-out as scoring scaffolding (autoeval R18, tessendorf),
# so it can no longer be the pin a negative leans on. The frame words W18 already accepts
# (contrary to / although / despite and kin) joined the list in the same pass, since a
# negative pinned by its frame word alone used to ride E1 on the carve-out.
PIN_RE = re.compile(
    r"met only|does not (meet|fail)|不"
    r"|incorrectly|wrongly|in violation|violat\w+|beyond what|contradicts"
    r"|contrary to|although|even though|despite", re.I)
MEET_PIN_RE = re.compile(r"met only when|do(es)? not meet", re.I)
QUANT_RE = re.compile(r"^(at least one|any |a |an |the (deliverable|plan|workbook|response|settlement)\b)", re.I)
NO_LINE_RE = re.compile(r"appears? on no|on no .*(line|row)|no .* appears", re.I)
REL_WIN_RE = re.compile(r"(preceding|trailing|last|prior)[ -](?:\w+[ -])?(twelve|thirty|\d+)[ -]?(month|day|week|year)", re.I)
ABS_DATE_RE = re.compile(r"\d{1,2}/\d{1,2}/\d{2,4}|\b(" + MONTHS_RE + r")\b.{0,15}\d{4}", re.I)
RESUM_RE = re.compile(r"(sum|total)\b.{0,40}\b(over|of) (every|all|each)\b.{0,80}\.csv", re.I)
LIVENESS_RE = re.compile(r"(formula|live)", re.I)
LIVENESS_DEMAND_RE = re.compile(
    r"\bformulas?\b|\bcell references?\b|stored as [^.;]{0,40}\breferences?\b|"
    r"\blive (?:formula|cells?|math)\b|rather than (?:being )?typed|typed constants?", re.I)
CONSTANT_RE = re.compile(r"(typed|pasted|hard.?coded|constant)", re.I)
CHAIN_RE = re.compile(r"chain|cell reference|reference[sd]? (into|ending)", re.I)
CARVEOUT_RE = re.compile(r"may (appear as |be )typed|only quoted", re.I)
DOLLAR_RE = re.compile(r"\$\d")
SIBLING_COST_RE = re.compile(r"\b(landed|net|invoice)\s+cost|\bnew L[1-4]\b[^.]{0,20}\$\d", re.I)
ANCHOR_RE = re.compile(
    r"golden reference|do(es)? not (answer|meet) this criterion|upstream intermediate"
    r"|\bx\s*[01]?\.\d|[×÷]|times the|between \$|/\s?\(1\s?-|not the (landed|net|invoice) cost", re.I)
SCHEMA_REF_RE = re.compile(r"(?:'[^']+'|\b[A-Za-z_][A-Za-z0-9_]*)![A-Z]{1,3}\d+")
SCHEMA_COL_RE = re.compile(r"\bthe ['\"]?[A-Z][\w /-]{0,25}['\"]? column\b")
# W12 extension (2026-08-24, task 28 run 6): the "the X column" form is not the only way a
# criterion imposes the golden's schema. Naming the header token directly -- "carries 101
# under ORDER PT", "the 620 under ADJ UNITS" -- cites exactly the same private column name
# and reads the same way to the Agentic Rubric Quality Review. Hyphenated / numbered tokens
# are excluded because "under INV-4 8.3" is a POLICY clause, not a header (yankton C45, the
# only false positive the unguarded pattern produced portfolio-wide).
SCHEMA_HDR_RE = re.compile(r"\bunder\s+([A-Z]{2,}(?:\s+[A-Z]{2,})*)\b(?![-\d])")

# W19 (2026-08-24, task 28 run 6 Agentic Rubric Quality Review, [critical]
# misaligned_or_unjustified_rigidity): a negative can carry a defect frame and STILL be read
# as inverted when its main verb is one a compliant deliverable also performs. Task 28 C29
# read "The demand base counts invoice lines carrying a job number as replenishment demand,
# in violation of policy 4.2 ..." -- W18 passed it, because "in violation of" is present, but
# the review answered that a correct base also "counts" those lines (it tracks them in a
# column of their own) and rated the rubric needs_improvement on -4 of exposure. The fix is
# the verb: "includes ... as replenishment demand" is something only a wrong base does.
# Scoped to the criterion's MAIN clause: the same verbs are harmless in a subordinate
# evidence clause ("on a row that also shows ...", "the price its sheet lists"), which is
# where all four portfolio occurrences sit.
AMBIG_DEFECT_VERB_RE = re.compile(
    r"^\s*(?:The|A|An)\s+[\w' ]{2,40}?\s+"
    r"(counts|shows|lists|reports|tracks|identifies|records|flags)\s+", re.I)
ABSENCE_CLAIM_RE = re.compile(
    r"\b(are|is|left)\s+(blank|empty|absent)\b|\bcarr(y|ies) no\b|\breceives? no\b"
    r"|\bhas no\b|\bcontains? no\b"
    # luebbert C16 (2026-08-20): "shown with no purchase price available after 11/01/2026"
    # drew unverifiable_from_deliverable 1/3 while the judge quoted the very row carrying the
    # withdrawal marker. Same class as the blank-cell claims: the absence greps to nothing.
    r"|\b(shown|listed|marked|left|stands?|standing)\s+with no\b"
    r"|\bno\s+\w+(\s+\w+)?\s+(available|shown|carried|present|listed)\b", re.I)
ABSENCE_OK_RE = re.compile(
    r"fails only if|absence[^.]{0,60}satisf|satisf\w+[^.]{0,60}absence|not this defect", re.I)
METHOD_SWEEP_RE = re.compile(
    r"compared against|computed by (applying|taking)|is computed by|taken from[^.]{0,40}"
    r"rather than|in place of the [a-z ]{0,20}(cost|rate|value|price)|"
    r"rather than the (current|actual|stated) [a-z ]{0,20}(cost|rate|value|price)", re.I)
RULE_APPLY_RE = re.compile(
    r"\bis (?:carried|converted|moved|mapped|posted|keyed|assigned) (?:onto|to|under|against)\b"
    r"|\bis (?:reset|reopened|claimed|credited|counted|measured|applied|excluded|retired|waived)"
    r"\s+(?:under|against|beyond|outside)\b"
    r"|which (?:the )?[a-z][\w .-]{0,40}?(?:does not|do not|cannot)\s+"
    r"(?:support|reach|allow|permit|cover|extend)\b", re.I)
NEG_TOKEN_RE = re.compile(
    r"\b(no|not|never|omits?|lacks?|fails? to|cannot|without|missing|absent|neither|nor)\b", re.I)
DEFECT_FRAME_RE = re.compile(
    r"\b(incorrectly|wrongly|in violation of|violating|contradicts?|contrary to|against "
    r"(?:the|policy|bulletin|paragraph|article)|beyond what|which [a-z ]{0,20}does not "
    r"(?:support|reach|allow|permit)|although|even though|despite|with no |carrying no )", re.I)
PIN_STRIP_RE = re.compile(r"(is|are) not this defect", re.I)
CHAIN_JOURNEY_RE = re.compile(r"\b(chain|hop)s?\b", re.I)
NO_TRACE_RE = re.compile(r"no tracing|without tracing|need not (be )?trac|not (be )?traced", re.I)
SWEEP_RE = re.compile(
    r"^(every|each|all)\b|\b(every|all)\s+(populated|qualifying|affected|new\s+)?"
    r"(item|price|row|line|sku|figure|total|action)s?\b", re.I)
COUNTERFACTUAL_RE = re.compile(
    r"\b(remov|delet|chang|edit|flipp|updat|perturb|re-?pric|re-?quantif|re-?siz)\w*\b[^.;]{0,120}"
    r"\b(re-?comput|re-?calculat|re-?sort|re-?rank|updates?|flows?|carr(y|ies) through|propagat)"
    r"|without (manual|hand) (edit|rework|re-?entry)", re.I)


def lint_file(path: Path):
    findings = []
    bad = []
    rows = load_rows(path, bad=bad)
    for num, _text, _raw in bad:
        findings.append((path, num, "ERROR", "E0", "WEIGHT is not numeric"))
    if True:
        for num, text, weight in rows:
            if weight < 0:
                # W18 (2026-08-23, task 20 quality review): the trailing carve-out is a
                # NEAR-MISS clause, not a polarity marker on its own. Four negatives whose
                # only marker was "... is not this defect" were all read as inverted, the
                # review quoting the defect sentence back as "what a correct deliverable
                # does" and scoring -16 of exposure. W9 has always said to state the fault
                # with incorrectly / violating / contradicts AND phrase the carve-out that
                # way; this enforces the first half.
                defect_sentence = PIN_STRIP_RE.split(text)[0]
                defect_sentence = split_clauses(defect_sentence, capital=True)[0]
                if not DEFECT_FRAME_RE.search(defect_sentence):
                    findings.append((path, num, "ERROR", "W18",
                                     "negative states its defect with no defect-frame word "
                                     "(incorrectly / violating / contradicts / although / "
                                     "carrying no). A trailing \"is not this defect\" carve-out "
                                     "is a near-miss clause, not a polarity marker: the Agentic "
                                     "Rubric Quality Review read all four of task 20's negatives "
                                     "as describing what a CORRECT deliverable does and scored "
                                     "-16 of exposure (2026-08-23). Put the frame in the sentence "
                                     "that states the fault"))
                else:
                    m = AMBIG_DEFECT_VERB_RE.match(defect_sentence)
                    if m:
                        findings.append((path, num, "ERROR", "W19",
                                         f'negative states its defect with the verb "{m.group(1)}", '
                                         "which a COMPLIANT deliverable also does - a correct base "
                                         "counts/shows/lists the very rows it then excludes. A defect "
                                         "frame does not save it: task 28 C29 carried \"in violation "
                                         "of policy 4.2\" and the Agentic Rubric Quality Review still "
                                         "called the polarity inverted [critical], -4 exposure "
                                         "(2026-08-24). Name the prohibited act instead - includes / "
                                         "is left with / is counted inside / is incorrectly taken"))
                pinned = bool(PIN_RE.search(text))
                if not pinned:
                    findings.append((path, num, "ERROR", "E1",
                                     'negative criterion has no polarity pin: state the defect with a defect-frame word inside the sentence '
                                     '("incorrectly", "... although <source> documents no X"), never a '
                                     '"met only when" pin (W9) or grader wording such as "meets this criterion" (R18)'))
                    if not QUANT_RE.search(text) and not re.search(r"at least one|any\b", text, re.I) \
                            and re.search(r"^\w+.*\b(are|carry|include|count)\b", text, re.I):
                        findings.append((path, num, "ERROR", "E2",
                                         'negative criterion opens with a bare plural subject — use "At least one ..."'))
            if NO_LINE_RE.search(text):
                findings.append((path, num, "ERROR", "W1",
                                 '"appears on no line" wording — breaks on zero-quantity rows; use "claims any units" + carve-out'))
            if REL_WIN_RE.search(text) and not ABS_DATE_RE.search(text):
                findings.append((path, num, "ERROR", "W2",
                                 "relative time window with no absolute date anchor"))
            if RESUM_RE.search(text):
                findings.append((path, num, "ERROR", "W3",
                                 "asks the judge to re-derive an aggregate from a raw input file"))
            if LIVENESS_RE.search(text) and CONSTANT_RE.search(text) and not CHAIN_RE.search(text) and weight > 0:
                findings.append((path, num, "ERROR", "W4",
                                 "formula-liveness wording without reference-chain acceptance"))
            if CARVEOUT_RE.search(text) and not DOLLAR_RE.search(text):
                findings.append((path, num, "ERROR", "W5",
                                 "typed-input carve-out without a pinned dollar value/source"))
            if weight < 0 and CONSTANT_RE.search(text) and LIVENESS_RE.search(text):
                findings.append((path, num, "ERROR", "W6",
                                 "negative liveness-mirror criterion — judges deduct these deterministically even when pinned; drop it (positive liveness criteria cover this) unless scoped to one inspectable column"))
            if weight > 0 and DOLLAR_RE.search(text) and SIBLING_COST_RE.search(text) \
                    and not ANCHOR_RE.search(text):
                findings.append((path, num, "ERROR", "W8",
                                 "dollar spot-check on a cost/price with sibling look-alike columns and no answer-key anchor — add a golden cell reference, the arithmetic chain, or a does-not-answer disclaimer on the siblings"))
            if weight < 0 and len(NEG_TOKEN_RE.findall(PIN_STRIP_RE.sub("", text))) >= 3:
                findings.append((path, num, "ERROR", "W14",
                                 "negative criterion stacks 3+ negations outside its polarity pin — the "
                                 "oracle reports ambiguous_negative_polarity and the criterion is sent to "
                                 "manual review (dillman's briefing negative, 3/3 runs 2026-08-19: "
                                 '"carries no ... does not surface ... cannot be run off it"). State the '
                                 "defect affirmatively (the deliverable HAS this fault) and let the pin be "
                                 "the only negation"))
            if weight < 0 and METHOD_SWEEP_RE.search(text):
                findings.append((path, num, "ERROR", "W15",
                                 "negative sweeps over HOW a figure was computed or which source "
                                 "column it came from — the oracle flags these "
                                 "ambiguous_negative_polarity regardless of pinning, the same as the "
                                 "W6 liveness mirrors (wamhoff run 1, 2026-08-20: the last-cost and "
                                 "the duty-mechanics negatives both flagged 3/3 and routed to manual "
                                 "review). Drop them where positives already pin the correct values, "
                                 "or restate the defect as a content fact about a quantity or value"))
            if weight < 0 and RULE_APPLY_RE.search(text):
                findings.append((path, num, "ERROR", "W17",
                                 "negative's defect is the APPLICATION of a named rule, clause "
                                 "or article to a record (carried onto / reset under / which X "
                                 "does not support) - the oracle flags these "
                                 "ambiguous_negative_polarity whatever the pin, the same as W6 "
                                 "and W15 (bergendahl run 1, 2026-08-21: two such negatives "
                                 "flagged, rewards [0.0, 0.0, 1.0], while the content-fact "
                                 "negatives on the same rubric passed clean). Drop them where "
                                 "positives already pin the values, or restate the defect as a "
                                 "content fact about a quantity or value in the deliverable"))
            if weight < 0 and MEET_PIN_RE.search(text):
                findings.append((path, num, "ERROR", "W9",
                                 'meet-style polarity pin ("met only when / does not meet") — the Agentic '
                                 "Rubric Quality Review reads this as inverted polarity (task 07, "
                                 "2026-08-19); reword to defect-frame (\"incorrectly/violating/beyond "
                                 'what X supports/contradicts"), with no carve-out sentence (banned '
                                 "2026-08-26, autoeval R18)"))
            if weight > 0 and LIVENESS_RE.search(text) and CHAIN_JOURNEY_RE.search(text) \
                    and not NO_TRACE_RE.search(text):
                findings.append((path, num, "ERROR", "W10",
                                 "chain/hop-framed liveness verification with no no-tracing disclaimer — "
                                 "judges flake tracing chains (marathon C29 runs 4-6, a different stall "
                                 "each run); anchor on the aggregation range's stored formulas, note "
                                 "displayed numbers are cached results, carve out downstream cells with "
                                 '"pass; no tracing needed"'))
            if weight > 0 and SWEEP_RE.search(text) and not ANCHOR_RE.search(text) \
                    and not re.search(r"golden|answer key", text, re.I) \
                    and LIVENESS_DEMAND_RE.search(text) \
                    and not re.search(r"\d[\d,]*\.\d|\d[\d,]{3,}", text):
                # W16 (kolterman run 2, 2026-08-21): a sweep over rows PLUS a liveness
                # demand is the worst of both judge failure modes. "Each line of the
                # return authorization detail draws its quantity and its unit price ...
                # by cell reference" was true of every one of the 20 rows (=Layers!Q168,
                # =Layers!H168) and still failed 2 of 3 oracle runs, the judge quoting a
                # displayed row back as typed. It had carried a standing W11 finding
                # since it was written. Scope liveness to a named handful of cells, never
                # to "each/every line".
                findings.append((path, num, "ERROR", "W16",
                                 "liveness demand written as a row sweep (each/every line ...) — the "
                                 "judge reads displayed values back as typed and fails a golden that is "
                                 "live on every row (kolterman C29, 2/3 oracle runs, weight 5). Name the "
                                 "handful of figures the criterion covers instead of sweeping the table"))
            elif weight > 0 and SWEEP_RE.search(text) and not ANCHOR_RE.search(text) \
                    and not re.search(r"golden|answer key", text, re.I):
                findings.append((path, num, "ERROR", "W11",
                                 "universal-sweep positive (every/all ...) without an answer-key anchor — judges flake on exhaustive sweeps; state the exact count with exclusion arithmetic, name golden rows/cells and a worked example, and carve out held/excluded rows"))
            if weight > 0 and ABSENCE_CLAIM_RE.search(text) and not ABSENCE_OK_RE.search(text):
                findings.append((path, num, "ERROR", "W13",
                                 "positive criterion asserts blankness/absence as an observable — judge "
                                 "search tools grep values and report not_observed on absence (hartwell "
                                 "C14/C35 run 7, judge quoted the evidence yet failed both); lead with a "
                                 "POSITIVE observable instead: the flag, marking or zero value the golden "
                                 "actually carries. The old \"fails only if <defect>\" remedy is now banned "
                                 "by the platform Rubric negative polarity check (kolterman 2026-08-20)"))
            if SCHEMA_REF_RE.search(text) or SCHEMA_COL_RE.search(text) \
                    or SCHEMA_HDR_RE.search(text):
                findings.append((path, num, "ERROR", "W12",
                                 "criterion cites a golden sheet/cell reference or named column — the Agentic "
                                 "Rubric Quality Review flags this as golden-only schema imposition (hartwell "
                                 "2026-08-19, ~31 pts, needs_improvement); reword functionally (keep the numeric "
                                 "answer key and arithmetic chain, disambiguate siblings by VALUE not column "
                                 "name), unless the prompt itself mandates that sheet/column. Fix BEFORE "
                                 "submission even on oracle-proven wording — deadstock C17 left a W12 standing "
                                 "and the quality review failed it (2026-08-19)"))
            if COUNTERFACTUAL_RE.search(text):
                findings.append((path, num, "ERROR", "W7",
                                 "counterfactual wording asks the judge to simulate a dynamic behavior on a static file — flaky; reword to answer-keyed static form (name golden cells, disclaim intermediate columns, accept rounding)"))
    return findings


def main(argv):
    root = Path(__file__).resolve().parents[3]
    if len(argv) > 1:
        targets = [Path(a) for a in argv[1:]]
    else:
        targets = sorted(root.glob("submissions/*/rubric-*.csv"))
    errors = 0
    for path in targets:
        findings = lint_file(path)
        rel = path.relative_to(root) if path.is_relative_to(root) else path
        if not findings:
            print(f"OK    {rel}")
            continue
        for _, num, level, code, msg in findings:
            print(f"{level:5s} {rel} C{num} [{code}] {msg}")
            if level == "ERROR":
                errors += 1
    return 1 if errors else 0

