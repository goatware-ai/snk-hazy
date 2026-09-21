"""Group 2: rubric form, coverage, duplication, objectivity and atomicity (PRE-* and RUBQ-* rules).

Generated 2026-09-04 from autoeval_check.py; every check body is verbatim.
"""
import re
from pathlib import Path
from .lint import lint_file
from ..common import (LIVENESS_STRICT_RE, RANGE_KEY_RE, _FIGURE_RE, _YEAR_RE, _col_num, _weights, _without_cell_refs,
                      load_rows, rubric_path, solution_files, split_clauses, workbook)
from ..core import check, emit, recommend, REPORT, OPTIONS


PROCESS_ORDER_RE = re.compile(
    r"\b(before|after|prior to)\s+(any|each)\b[^.;]{0,60}?\b(is|are)\s+\w+(ed|wn)\b"
    r"|\bthe worker\s+(first|then)\b",
    re.I)


R100_PROMPT_ACTION_RE = re.compile(
    r"who does what|action (?:list|plan|items)|next steps|what has to happen|name and a date"
    r"|owner and a date|who (?:owns|does) (?:what|each)|who(?:'s| is) responsible", re.I)


R100_ACTION_RE = re.compile(
    r"action (?:list|plan|items?)\b|\bactions?\b|owner and a date|name and a date"
    r"|who does what|next steps|to be done"
    # a memo's action plan is written one fix at a time ("assigns the Green River window to
    # purchasing, with a completion date"), which the front-page vocabulary above never saw
    # (dock-to-stock-review, 2026-08-31). The date token is required: an assignment with no
    # date is not one of the "owned, DATED action rows" the check counts, and without it
    # "assigns each late receipt to the first step that missed" would be credited too
    r"|assign(?:s|ed)\b[^.]{0,200}?\b(?:completion date|due date|target date|with a date)", re.I)


# TIER ONE IS WORTH LESS THAN THIS CODE CREDITS IT (frankfort-stock-recovery, 2026-08-31).
# R24 counts strict and gated together and assumes a hard-coded workbook fails both. The
# platform's Rubric full credit completeness check does not: it FAILed a rubric this file
# scored clean at +39 with two strict criteria and no gated ones, reasoning that "a solver
# can satisfy those two links while hard-coding the underlying claim recap, yard total,
# loss schedules, salvage calculations, coverage-limit splits, transfers, purchases and
# fulfillment results ... retaining all 39/39 positive points". R9 and R30 FORCE each
# strict criterion onto one named cell, so two live cells in an otherwise typed workbook
# collect the full +10 and the workbook-wide demand costs nothing to omit.
#
# So when the prompt demands live formulas across the workbook, tier one is worth ZERO
# against that requirement and only the GATED tier below carries it. The repair is weight
# neutral: attach a derivation phrase to the substantive value criteria (loss quantities,
# replacement cost, markdown and salvage credits, limit splits, transfers, purchases,
# landed costs, unmet-order determinations) so hard-coding fails them outright. Frankfort
# went from 10 gated of 39 (retaining 74.4% by this file's model, 100% by the platform's)
# to 19 of 39, retaining 51.3% under either.
#
# The second FAIL landed 2026-08-31 (inbound-consolidation-plan round 2: "a solver can
# satisfy those two 5-point checks with references while hard-coding every other cost,
# saving, freight, bracket, and calendar result ... still earns all 39/39") and the rule
# is now coded as R73, scoped to prompts that themselves demand live formulas so the
# nine carriers without that prompt demand stay quiet where the evidence is thinner.
#
# tier two: a value criterion whose own figure is asserted to be derived, inseparably
LIVENESS_GATED_RE = re.compile(
    r"rather than (?:a )?(?:keyed|repeating|a figure keyed)"
    r"|(?:adds|sums|summed|summing) (?:the|across)[^.]{0,80}rather than"
    r"|is a formula|are formulas|a formula (?:dividing|summing|adding)", re.I)


FORMULA_DEMAND_RE = re.compile(r"stored (?:cell )?formulas?|live formulas?|typed constants?|hard-?coded", re.I)




VALUE_ANCHOR_RE = re.compile(r"\$\d|\bexactly \d|\b\d[\d,]*(?:\.\d+)? units\b|\bequals \$?\d", re.I)


LIVENESS_DISCLAIM_RE = re.compile(
    r"credit (here )?is for the (stored )?formulas?|scored (by|elsewhere)|not for matching any particular", re.I)


COMPLETENESS_RE = re.compile(r"\bexactly once\b|\b(every|each|all)\b[^.;]{0,90}?\b\d{1,4}\b", re.I)


# Extended 2026-08-31 (po-conformance-review, platform Rubric full credit completeness check
# FAIL): the prompt demanded "every purchase order that does not conform listed", no
# criterion required the schedule to be complete, and a solver omitting most exception
# rows kept 96.9% of positive credit. "purchase order" / "exception" / "invoice" / "receipt"
# were not in this noun list, so R4 never asked for the completeness criterion.
PROMPT_EVERY_RE = re.compile(r"\b(every|all)\s+(stocked\s+)?(qualifying\s+)?(affected\s+)?(nonconforming\s+)?"
                             r"(item|sku|branch|line|tag|product|combination|purchase order|order|exception|"
                             r"invoice|receipt|lot|account|delivery)", re.I)


# R76 (2026-08-31, inbound-consolidation-plan round 6, Rubric full credit completeness
# check): a strict liveness criterion that prescribes ONE formula tactic is a "gold-only
# implementation ... optional-tactic lock": "the prompt requires live formulas throughout,
# but it does not require the specific gold-only implementation of plain cell references
# ... a valid workbook using SUMIFS, XLOOKUP, or a direct aggregation formula could lose
# 10/39". Two +5 rows worded "through plain cell references ... rather than typed
# constants" (the shape delivery-zone and boettcher cleared with) failed the bar here.
# Name the mechanism the golden uses AND admit any live alternative in the same sentence.
_R76_LOCK_RE = re.compile(r"\bplain cell references?\b|\bdirect cell references?\b", re.I)


_R76_OPEN_RE = re.compile(r"\balike\b|\bor an?y?\b[^.]{0,60}\b(?:formula|aggregation|count|lookup)\b|\bany live\b|\bwhether\b", re.I)


@check(codes=['R76'], rules=['PRE-COVER'], needs=['rubric'], params=['rows'])
def check_tactic_lock(rows):
    """A strict liveness criterion names the golden's mechanism and admits any live alternative in the same sentence, never plain cell references alone.

    Since: 2026-08-31 (inbound-consolidation-plan round 6).
    Source: the platform's Rubric full credit completeness check ('gold-only implementation ... optional-tactic lock').
    """
    for num, text, weight in rows:
        if weight > 0 and LIVENESS_STRICT_RE.search(text) and _R76_LOCK_RE.search(text) \
                and not _R76_OPEN_RE.search(text):
            emit("ERROR", f"C{num} [R76] prescribes plain cell references as the only live mechanism - the "
                          "Rubric full credit completeness check reads that as a gold-only tactic lock "
                          "('a valid workbook using SUMIFS, XLOOKUP, or a direct aggregation formula ... "
                          "could lose 10/39', inbound-consolidation-plan, 2026-08-31). Keep the value "
                          "anchor and the strict idiom, name the golden's mechanism, and admit any live "
                          "alternative in the same sentence ('... or an aggregation over the same "
                          "orders alike')")


# R128 (2026-09-14, june-price-review adjudication): a positive that prescribes ONE named
# spreadsheet function as the way a figure is produced ("computed ... by a COUNTA over the
# item column") or fixes the exact words of a label ("the words matrix cells to re-key beside
# it") was returned as over-constraint: "reword the criterion to accept any formula-driven
# count of the corrections (COUNTA, ROWS, COUNT, or equivalent) with any label that
# identifies the count". R76 covers the plain-cell-reference lock and R90 the function token
# on a strict liveness row; neither fired on this wording, because it named the function as a
# prescription rather than a landing. Name the thing counted and the value; admit any formula
# and any label.
_R128_FUNCS = (r"SUM|SUMIFS?|SUMPRODUCT|COUNT|COUNTA|COUNTIFS?|COUNTBLANK|ROWS|AVERAGE|AVERAGEIFS?"
               r"|MAX|MIN|LARGE|SMALL|INDEX|MATCH|VLOOKUP|HLOOKUP|XLOOKUP|LOOKUP|IFERROR|ROUND")
_R128_FUNC_LOCK_RE = re.compile(
    r"\b(?:by|with|using|via|through|from|as) (?:a|an|the|one|a single|a plain)\s+(?:" + _R128_FUNCS + r")\b"
    r"|\b(?:" + _R128_FUNCS + r") (?:over|across|on|of) (?:the|its|a|an|every|each|all)\b")
_R128_LABEL_LOCK_RE = re.compile(
    r"\bthe (?:exact )?words? [^.;]{3,80}?\b(?:beside|next to|alongside|above|under|below|in the cell|in the label)\b"
    r"|\blabell?ed (?:exactly|verbatim|with the words?)\b"
    r"|\b(?:label|caption|header|heading|title) (?:reads|reading|of exactly|exactly|worded)\b"
    r"|\bthe exact (?:label|wording|caption|heading|words?)\b"
    r"|\bexactly the (?:words?|label|caption|heading)\b", re.I)
_R128_OPEN_RE = re.compile(
    r"\bor equivalent\b|\bor an?y?\b[^.]{0,60}\b(?:formula|aggregation|count|lookup|function|label|wording|words)\b"
    r"|\balike\b|\bany (?:live|formula|label|wording|equivalent)\b|\bwhatever (?:the )?(?:label|wording|function|formula)\b"
    r"|\bin any words\b|\bunder any label\b|\bhowever (?:labelled|worded)\b", re.I)


@check(codes=['R128'], rules=['RUBQ-RIGID'], needs=['rubric'], params=['rows'])
def check_function_or_label_lock(rows):
    """A positive names the thing counted or summed and its value, never one spreadsheet function as the required mechanism nor the exact words of its label, unless the same sentence admits any equivalent.

    Since: 2026-09-14 (june-price-review adjudication: criterion 15 required a COUNTA and the words 'matrix cells to re-key').
    Source: the adjudicator's own remedy, 'any formula-driven count ... (COUNTA, ROWS, COUNT, or equivalent) with any label that identifies the count'.
    Drift-notes: R76 is the plain-cell-reference lock on strict liveness rows; R90 is the function token the judge cannot grep. This is the prescription grammar ('by a COUNTA', 'the words X beside it') on any positive.
    """
    for num, text, weight in rows:
        if weight <= 0 or _R128_OPEN_RE.search(text):
            continue
        m = _R128_FUNC_LOCK_RE.search(text)
        if m:
            emit("ERROR", f"C{num} [R128] prescribes one spreadsheet function as the required mechanism "
                          f"(\"{m.group(0)}\") - the june-price-review adjudicator returned a COUNTA "
                          "requirement as over-constraint (2026-09-14) and asked for 'any formula-driven "
                          "count ... or equivalent'. Name the thing counted and its value, and say 'a "
                          "formula over the list rather than a keyed figure' or admit the alternative in "
                          "the same sentence")
        m = _R128_LABEL_LOCK_RE.search(text)
        if m:
            emit("ERROR", f"C{num} [R128] mandates the exact words of a label (\"{m.group(0)[:60]}\") - "
                          "the june-price-review adjudicator returned 'the words matrix cells to re-key "
                          "beside it' as over-constraint (2026-09-14) and asked for 'any label that "
                          "identifies the count'. Describe what the label identifies, never its wording")


# R81 (2026-09-02, dfl-freight-audit Rubric Quality Review, [major]
# misaligned_or_unjustified_rigidity): three positive criteria fixed the OWNER of a corrective
# action to a named person ("assigns Hector Ybarra the classing ...", "assigns Arlen Kracht a
# paid pro number check ...", "asks Trina Boesch for written confirmation ...") while the prompt
# only asked for the actions. The review called it rigidity a valid alternative assignment
# loses six points to, and it did not matter that two of the three names were visible in the
# prompt and inputs: the prompt never mandated the assignment. Score the action, the fact of an
# owner and the date; never the person: "The memo assigns an owner and a completion date to
# classing fiberglass tub and shower kits at class 125 on the bill of lading."
# "names Pine Grove Creamery" (semrad C5) is a company, not an owner: the verb set is the
# assignment verbs only, and a name ending in a business word is not a person.
_R81_NAMED_OWNER_RE = re.compile(
    r"\b(?:assigns|assigned to|tasks|hands|directs|asks|owned by|owner is)\s+"
    r"(?:[A-Z][a-z]+(?:'s)?\s+){1,2}[A-Z][a-z]+\b")


_R81_BUSINESS_RE = re.compile(
    r"\b(?:Creamery|Supply|Supplies|Inc|LLC|Co|Company|Corp|Freight|Lines|Foods|Distributors?"
    r"|Wholesale|Brothers|Bank|Mutual|Group|Sanitary|District|Plumbing|Electric|Industries"
    r"|Manufacturing|Hardware|Logistics|Trucking|Transport|Express|Partners|Associates)\b$")


@check(codes=['R81'], rules=['RUBQ-RIGID'], needs=['rubric'], params=['rows'])
def check_named_owner(rows):
    """A positive action row never fixes the owner to a named person, and it scores that an owner is named and a date only when the prompt asks who and by when (R100 forbids both otherwise).

    Since: 2026-09-02 (dfl-freight-audit Rubric Quality Review, [major] rigidity).
    Source: reviewer ruling that a valid alternative assignment must not lose points, even when the name sits in the prompt.
    Drift-notes: this is the lower bound. R100 (2026-09-09 adjudication) is the upper bound: when the prompt never asks
    for owners or dates, a row must not score them at all. The memory wording "a named person as owner and a calendar
    date" from reviewer round 3 applies only when the prompt itself asks who and by when.
    """
    for num, text, weight in rows:
        if weight < 0:
            continue
        m = _R81_NAMED_OWNER_RE.search(text)
        if not m or _R81_BUSINESS_RE.search(m.group(0)):
            continue
        emit("ERROR", f"C{num} [R81] fixes an action's owner to a named person (\"{m.group(0)}\"): "
                      "the Rubric Quality Review rated this [major] rigidity when the prompt asked "
                      "for the actions and not the assignments (dfl-freight-audit C23-25, "
                      "2026-09-02), and a name being visible in the prompt or inputs does not save "
                      "it. Score the action, that an owner is named, and the date - 'assigns an "
                      "owner and a completion date to <action>' - never the person")




# R74 (2026-08-31, open-order-cleanup pre-submission): the completeness check's THIRD
# axis. R24 measures how much WEIGHT the strict liveness criteria carry, and the
# each requirement's cluster SHARE; both passed a rubric the platform still failed, because
# neither looks at what a liveness criterion actually SCOPES. Criteria 5 and 6 held 10 of 39
# points (25.6%) and pinned two individual cells, so "a solver can satisfy both criteria with
# the two required references while hard-coding all line conversion dollars, commitment
# totals, variance, and briefing totals ... the workbook can fail the explicit requirement
# that totals 'update on their own' while retaining all 39/39 positive points."
#
# So where the PROMPT sells a dynamic-recalculation contract, at least one positive has to
# put a formula demand on an AGGREGATE - a total, a converting total, a commitment or a
# variance - and not only on individual read-through cells. Two named cells are lineage
# checks; they are not proof of the chain. The repair is cheap and adds no weight: hang an
# inseparable formula clause on the totals criteria the rubric already carries ("Ottawa's
# converting total ... is a formula over the line detail's plan value column, standing at
# 39795.46"), which a hard-coded workbook fails outright.
_R74_PROMPT_RE = re.compile(
    r"update on (?:their|its) own|updates? on (?:their|its) own|totals? need to update"
    r"|keep the math live|live in the cells|recalculat\w+|update automatically"
    # semrad-date-recovery, 2026-08-31: the platform's completeness check FAILed on exactly
    # this axis while R74 stayed silent, because the prompt sells the contract as "keep it on
    # live formulas, because Dale will move a date Thursday and the plan has to move with
    # him" - a dynamic-recalculation promise in the house's own register that named neither
    # "recalculate" nor "update on their own"
    r"|keep (?:it|them|the \w+) on live formulas?|has to move with|have to move with", re.I)


_R74_FORMULA_RE = re.compile(
    r"\bis a formula\b|\bare formulas\b|stored formulas?|live formulas?|formula derived"
    r"|reach(?:es)? (?:its|their) values?\s+(?:from|through)|rather than (?:being )?typed"
    r"|typed constants?", re.I)


_R74_AGG_RE = re.compile(
    r"\btotals?\b|\bcommitment\b|\bvariance\b|\bconverting\b|\bconverts?\b|\bsubtotal\b"
    r"|\bsum of\b|\bbalance\b", re.I)


@check(codes=['R74'], rules=['PRE-COVER'], needs=['prompt', 'rubric'], params=['rows', 'folder'])
def check_chain_scope(rows, folder):
    """A prompt that sells dynamic recalculation has formula criteria reaching past single cells to the chains that recalculate."""
    prompt = folder / "prompt.md"
    if not prompt.exists() or not _R74_PROMPT_RE.search(prompt.read_text(encoding="utf-8")):
        return
    live = []
    for n, text, w in rows:
        if w <= 0:
            continue
        m = _R74_FORMULA_RE.search(text)
        if m:
            live.append((n, text, m.start()))
    if not live:
        return                                  # R24 already owns "no liveness at all"
    # the aggregate has to be what the criterion is ABOUT, so only the subject counts:
    # "reaches its value through a cell reference into the commitment page" names a sheet,
    # not a total, and read whole-text it would exempt the very shape this rule catches
    for _, text, at in live:
        subject = re.sub(r"\b(commitment|line detail|position|usage)\s+(page|sheet|tab|column)\b",
                         " ", text[:at], flags=re.I)
        if _R74_AGG_RE.search(subject):
            return
    emit("ERROR", f"[R74] the prompt sells a dynamic-recalculation contract but every formula "
                 f"demand (C{', C'.join(n for n, _, _ in live)}) sits on an individual cell, none on "
                 "a total, converting total, commitment or variance - a solver satisfies them with "
                 "those references and hard-codes every downstream total, keeping full credit while "
                 "failing the requirement that the totals update on their own (open-order-cleanup, "
                 "2026-08-31: two lineage criteria at 10 of 39 and the completeness check FAILed "
                 "anyway). Hang an inseparable formula clause on the totals criteria already in the "
                 "rubric; it adds no weight and a hard-coded workbook fails it outright")


# R25 (2026-08-21, task 20): the Rubric objectivity check also rejects a bare evaluative
# term, separately from R19's "where relevant" hedge family. It failed a contradiction
# criterion on the single word "consistently": "an unanchored grader-judgment term with no
# numeric threshold, quoted source language, or example defining it in the sentence. It
# requires the grader to subjectively decide what counts as consistent." The anchor has to
# sit in the SAME sentence as the term, so a criterion that enumerates its figures earlier
# and then says "and these are stated consistently" still fails.
JUDGMENT_TERM_RE = re.compile(
    r"\b(consistent(?:ly)?|appropriate(?:ly)?|proper(?:ly)?|accurate(?:ly)?|thorough(?:ly)?"
    r"|reasonabl[ey]|adequate(?:ly)?|sufficient(?:ly)?|suitabl[ey]|meaningful|comprehensive"
    r"|well[- ]structured|as needed)\b", re.I)


JUDGMENT_ANCHOR_RE = re.compile(r"\d|\"[^\"]+\"")


# Magnitude descriptors (2026-08-31, inbound-consolidation-plan round 5): the objectivity
# check FAILed "the fortnights its combine stays thin" on "thin" while the sentence carried
# 713.02, ruling that a total "does not define which fortnights qualify as thin through a
# threshold, comparison, quoted source phrase, named category, or example" and that a
# sibling row's "under the floor" does not carry over. A digit is therefore NOT an anchor
# for a categorical descriptor; the sentence itself must carry the comparison.
JUDGMENT_MAGNITUDE_RE = re.compile(r"\b(thin(?:ly)?|lean|scant|hefty|sizeable|modest|marginal)\b", re.I)


JUDGMENT_COMPARISON_RE = re.compile(
    r"\b(?:under|below|above|over|beneath|short of|past|at least|at most|no more than|no fewer than"
    r"|less than|more than|fewer than|within|floor|threshold|ceiling|cap|minimum|maximum)\b|\"[^\"]+\"", re.I)


HEDGE_RE = re.compile(
    r"\b(?:where|wherever|when|whenever|if|as)\s+(?:relevant|applicable|appropriate|needed|necessary|sensible|suitable|possible)\b"
    r"|\bas required\b(?!\s+by\b)"
    r"|\bwhere judgment\b|\bjudgment is (?:exercised|applied|used)\b"
    r"|\b(?:everywhere|wherever|anywhere) the \w+ touches\b"
    r"|\bwhere it matters\b|\bas judged\b"
    # OPEN-ENDED SUBSTITUTE (task 20 pre-submission, 2026-08-25): an adjudicator asked for
    # "on the parameters tab or equivalent" so the criterion would grade the analytical
    # content rather than a tab name, and the objectivity check FAILed the whole dimension
    # on the phrase: "it leaves undefined what counts as an acceptable substitute tab, with
    # no in-sentence criterion, label, or example defining equivalence", ranking it with the
    # banned "as appropriate". The remedy is not a hedge but the removal of the mandate: say
    # what the deliverable must SHOW and drop the location, or enumerate the acceptable
    # places by name. A reviewer's own suggested wording is not exempt from this check.
    r"|\bor (?:its |an |any )?(?:equivalent|equivalents|similar|comparable)\b"
    r"|\b(?:or|and) the like\b"
    # vague-intensity hedges on a MAGNITUDE (kolterman pre-submission, 2026-08-21):
    # "with roughly a further month of cover behind it" failed the objectivity check on
    # its own - the checker asked whether five weeks is roughly a month. A quantity in a
    # criterion has to be exact or bounded; the one-strike rule kills the dimension.
    r"|\b(?:roughly|approximately|about|around|nearly|almost|some|circa|broadly|"
    r"more or less|give or take|a little (?:over|under)|in the region of)\s+"
    r"(?:a|an|one|two|three|four|five|six|seven|eight|nine|ten|half|\$?\d)"
    r"|\d[\d,.]*\s+or so\b"
    # vague intensity COMPARATOR on a magnitude relation (twincreek C23 pre-submission,
    # 2026-08-21): "far above the account's actual buying" failed the objectivity check
    # as "a vague intensity comparison with no defined numeric threshold" even though the
    # sentence supplied all three figures (300 vs 26/48) - the boundary for "far" is
    # undefined. State the numeric relation bare ("exceeds", "is more than 6x") instead.
    r"|\b(?:far|well|way|much|considerably|significantly|substantially|markedly|vastly|"
    r"dramatically|sharply|slightly|somewhat|marginally|modestly|comfortably)\s+"
    r"(?:above|below|over|under|higher|lower|more|less|greater|smaller|larger|bigger|"
    r"beyond|past|short of|exceed\w*|outpac\w*)\b", re.I)


@check(codes=['R19'], rules=['PRE-OBJ'], needs=['rubric'], params=['rows'])
def check_hedges(rows):
    """A criterion carries no unanchored hedge-like qualifier that defers its scope to unspecified judgment.

    R19: an unanchored hedge-like qualifier defers the criterion's scope to
    unspecified judgment, and the platform's Rubric objectivity check FAILs the
    whole dimension on a single one.

    Hollenbach pre-submission (2026-08-20): C24 opened "Domain reasoning holds
    where judgment is exercised, everywhere the workbook touches it" and the check
    FAILed on exactly those two clauses as functioning like the disallowed "where
    relevant"/"as appropriate", even though the criterion then enumerated four
    concrete rules. The same run accepted the other 27 criteria on their numeric
    anchors. Fix by deleting the qualifier and stating the checkable conditions
    directly ("Throughout the workbook, ordered quantities are whole units, ...");
    "as required by <named policy>" stays exempt because the source anchors it.
    """
    for num, text, _ in rows:
        m = HEDGE_RE.search(text)
        if m:
            emit("ERROR", f'C{num} [R19] hedge-like qualifier "{m.group(0)}" — the platform\'s Rubric '
                          "objectivity check FAILs the dimension on one unanchored hedge (hollenbach C24 "
                          "pre-submission, 2026-08-20); delete the qualifier and state the checkable "
                          "conditions directly")


GRADER_INSTRUCTION_RE = re.compile(
    r"fails? only if|fail the response if|meets? this(?: criterion)?\b|does not meet it|"
    r"met only if|earns? (?:this criterion|full credit)|satisfies this(?: criterion)?\b|"
    r"also satisfies|award (?:if|credit)|give credit if|"
    # verdict assigned inside the text (rempel pre-submission, 2026-08-20)
    r"is a pass\b|counts as a pass\b|is a fail\b|does not fail this criterion|"
    r"do not answer this criterion|"
    # imperatives directing how the grader should evaluate (same run)
    r"\bjudge (?:from|by|on|it|this)\b|\bverify (?:by|that)\b|\bdecide from\b|"
    r"\bneeds no tracing\b|"
    # attribution disclaimers: the scoping note that keeps a liveness criterion from
    # restating figures scored elsewhere reads as grader instruction too (kolterman
    # pre-submission run 2, 2026-08-20 - the negatives passed, these two positives did not)
    r"scored by (?:their|its) own criteri|(?:scored|graded|counted) (?:here|elsewhere)\b|"
    r"credit here is for|counts? as met\b|counts as [^.;]{0,40}\bhere\b|"
    # the negatives' exclusion carve-out, banned by the same platform check on
    # tessendorf-channel-split pre-submission (2026-08-26) - see the docstring
    r"(?:is|are) not this (?:defect|error)|"
    r"do(?:es)? not count as this (?:defect|error)|"
    r"do(?:es)? not (?:satisfy|answer) this criterion", re.I)


@check(codes=['R18'], rules=['PRE-OBJ'], needs=['rubric'], params=['rows'])
def check_grader_instructions(rows):
    """A criterion states a fact about the deliverable, never an instruction telling the grader when to pass or fail.

    R18: criterion text that tells the grader when to pass or fail instead of stating
    a fact about the deliverable.

    The platform's Rubric negative polarity check FAILED kolterman pre-submission
    (2026-08-20) on four positives: "It fails only if ..." on C3 and C28 and "Any
    response meets this if ..." on C12 and C18, calling them near-verbatim paraphrases
    of the banned "Fail the response if" and "Award if / Give credit if" patterns. Note
    the checker's own suggested rewrites invert a positive criterion into a statement of
    the defect while keeping its positive weight; restate the compliant fact instead.

    The negatives' "... is not this defect" carve-out passed that kolterman run and was
    exempt here until tessendorf-channel-split pre-submission (2026-08-26) FAILed the
    same check on both carve-outs as scoring scaffolding, "functionally identical" to
    "does not count as this error": grader-facing language defining what does NOT
    trigger the penalty rather than a fact about the artifact. The repair is to DROP
    the carve-out sentence outright - the violation clause fully specifies the defect -
    and it costs nothing against the rest of the gate: W18 keys on the defect-frame
    word in the violation sentence, not the carve-out, and R53 fires only on a second
    negation. If a scope boundary genuinely needs stating, it goes in as an affirmative
    fact ("The two held prices sit at or above the floor"), never as an exclusion.

    Extended after rempel pre-submission (2026-08-20), which FAILed the same check on two
    LIVENESS positives that carried no pass/fail conditional at all. Two further shapes
    count as grader instruction: a verdict assigned inside the text ("A cell reaching its
    value through a plain cell reference is a pass") and an imperative aimed at the
    grader's method ("Judge from the stored formulas together with the displayed values",
    "Verify by reading the cell formulas stored in the file"). Both were house wording for
    defusing judge misreads, and both have to be restated as facts about the artifact: the
    displayed numbers are the cached results of the stored references, a cell reached
    through a plain reference is formula derived rather than a typed constant.
    """
    for num, text, _ in rows:
        m = GRADER_INSTRUCTION_RE.search(text)
        if m:
            emit("ERROR", f'C{num} [R18] grader-instruction wording "{m.group(0)}" — the platform\'s Rubric '
                          "negative polarity check FAILs this as scoring scaffolding (kolterman pre-submission "
                          "2026-08-20; carve-outs added tessendorf pre-submission 2026-08-26). State the fact "
                          "about the artifact instead: drop an \"is not this defect\" carve-out outright, never "
                          "invert a positive into a statement of the defect, and restate any needed scope "
                          "boundary as an affirmative fact")


_GROUPED_BY_RE = re.compile(r"\b(?:batch(?:ed)?|group(?:ed)?)\s+by\s+(\w+)", re.I)


# R57 (2026-08-25, open-order-cleanup pre-submission): the platform's near-identical
# criteria check FAILs a rubric where a positive quantifies a DERIVATION over every row and
# other positives score named instances of that same derivation. C8 read "The quantity still
# due on each line is calculated from the corrected received quantity, which follows the
# receipt register ... giving an open commitment of 84694.61", and C9, C10 and C11 checked
# three specific consequences of it (30 EA still due on 44121 line 1, nothing left due on
# 44121 line 2, 125 and not 5 on 44158 line 1). The ruling: "If Criterion 8 genuinely passes
# against the fixed source files, those three line-level checks must also pass." R47 could
# not see it, because it compares FIGURES and these criteria share none.
#
# Narrow on three counts at once, which is what keeps it off the coverage criteria the
# reviewers ask for: the quantifier has to range over ROWS (each line, every row), the
# predicate has to be a derivation rather than presence ("carries an action" is coverage and
# stays silent), and some other positive has to name a member of that class by row key. The
# repair is the checker's own: narrow the universal to the aggregate total plus the general
# method and leave the named rows as independent spot checks, which costs no weight.
_R57_UNIVERSAL_RE = re.compile(
    r"\b(?:each|every)\s+(?:open\s+|order\s+|single\s+)?(?:line|row|item|order|entry)\b", re.I)


_R57_DERIV_RE = re.compile(
    r"\b(?:calculated|computed|derived|recalculated|reconciled|follows|reflects"
    r"|based on|taken from|priced at|valued at)\b", re.I)


# a row key, not a money figure: 84866.21 and 12019.23 must not read as order numbers,
# or the finding names the wrong criteria and sends the next author to the wrong rows
_R57_MEMBER_RE = re.compile(r"(?<![\d.,])\d{4,}(?![\d,]*\.\d)|\bline \d+\b", re.I)


# R60 (2026-08-25, open-order-cleanup Agentic Rubric Quality Review): two positives equated
# the same named quantity to different figures and the review rated the rubric
# needs_improvement on it alone - "Criteria 4 and 8 state contradictory open commitment
# figures (84866.21 vs 84694.61) ... Both cannot be right." Both figures were right and the
# NAMES were wrong: 84866.21 is the Open on the 08/19 extract row and 84694.61 is the running
# total after the receipt postings are corrected, two steps of one bridge. A rubric that calls
# both "the open commitment" gives the grader no way to tell which it is scoring.
#
# Narrow by construction: it only looks at a phrase EQUATED to a figure (is / reads / stands
# at / totals), so a criterion that merely mentions the quantity in passing stays silent - C14
# says an amount is removed "from the open commitment" and carries 6407.6, and must not fire.
# Generic tail nouns are stripped so "the open commitment figure" and "the open commitment"
# are one name. The repair is never to delete a criterion: name the STAGE each figure belongs
# to, using the row label the workbook already carries.
_R60_EQUATE_RE = re.compile(
    r"\b(?:the\s+)?((?:[a-z][a-z']*\s+){1,3}[a-z][a-z']*)\s+"
    r"(?:figure\s+)?(?:there\s+)?"
    r"(?:is|reads|reading|stands\s+at|totals?|comes\s+to)\s+"
    r"(?:exactly\s+)?\$?(\d[\d,]*\.\d+)")


# a row key, never a money figure: 84866.21 must not read as an order number
_R60_KEY_RE = re.compile(r"(?<![\d.,])\d{4,}(?![\d,]*\.\d)|\b[A-Z]{2,}[0-9][\w-]*\b")


_R60_TAIL = {"figure", "figures", "total", "totals", "value", "amount", "row", "cell",
             "page", "block", "line", "sum", "balance"}


_R60_STOP = {"the", "a", "an", "of", "on", "in", "at", "to", "and", "that", "which", "it",
             "there", "here", "its", "their", "this", "those", "these", "for", "from",
             "with", "by", "as", "is", "are", "be", "been", "under", "over", "before",
             "after", "per", "into", "within", "above", "below", "against", "across"}


def _r59_name(phrase):
    words = [w for w in phrase.lower().split() if w not in _R60_STOP]
    while words and words[-1] in _R60_TAIL:
        words.pop()
    return " ".join(words[-2:]) if len(words) >= 2 else ""


_R83_BASENAME_RE = re.compile(r"\b([\w\-]+\.(?:xlsx|docx|csv|pdf|pptx))\b", re.I)


# R86 (2026-09-03, dfl-freight-audit Rubric near identical criteria check FAIL): subsumption
# with NO shared figure. C16 listed the fields every claim carries ("each carrying the pro,
# the invoice, ... and the reason code the claims desk's instructions require") and C20
# scored "one of the claims desk's eight reason codes on each claim"; passing C16 passed
# C20, and R10/R12/R45/R47 saw nothing because the pair shared no figure and no cell. The
# shape is two positive rows that each put a per-item quantifier (each, every, one per, on
# each) on the same attribute noun. Give the second row a DISTINCT property of the attribute
# (a reconciliation: "the schedule's reason codes reconcile to the grouped summary's counts,
# 34 coded OC-FSC on both") or drop it.
_R86_ATTR_RE = re.compile(
    r"\b(reason code|deadline|due date|completion date|owner|status|standing|class|zone|bin|"
    r"pro number|invoice number|bill of lading|ship date|amount paid|amount claimed|"
    r"unit cost|unit price|lead time|vendor|supplier|location|quantity|weight)s?\b", re.I)


_R86_PER_ITEM_RE = re.compile(
    r"\b(?:each|every|one per|per (?:claim|row|line|item|invoice|order|move|sku|bill))\b", re.I)


# the attribute counts only when the row asserts its PRESENCE per item: a carry verb (or
# "with") inside the same clause ahead of it. "rebuilt from its bill of lading" or "at the
# amount paid" use the attribute as an input, not as the thing scored.
# "shows"/"lists"/"records" are how a row cites an INPUT ("the location master shows in two
# bins", pick-module-reslot C22), so only the carry verbs count; and two rows about different
# components (the Kriegl release and the quick-ship order each carrying a quantity, semrad
# C17/C18) are not one requirement, so the rows must share their subject.
_R86_PRESENCE_RE = re.compile(r"\b(?:carr(?:y|ies|ying)|with|has|have)\b", re.I)


_R86_SUBJECT_RE = re.compile(r"^\s*(?:the|a|an|each|every)?\s*([a-z][a-z'\-]*(?:\s+[a-z][a-z'\-]*)?)", re.I)


def _r86_subject(text):
    m = _R86_SUBJECT_RE.match(text)
    return m.group(1).lower().replace("'s", "") if m else ""


def _r86_present_attrs(text):
    out = set()
    for m in _R86_ATTR_RE.finditer(text):
        clause = text[max(0, m.start() - 120):m.start()]
        clause = clause.rsplit(".", 1)[-1]
        if _R86_PRESENCE_RE.search(clause):
            out.add(m.group(1).lower().rstrip("s"))
    return out


@check(codes=['R83'], rules=['PRE-COVER'], needs=['inputs', 'prompt', 'rubric'], params=['rows', 'folder'])
def check_filename_coverage(rows, folder):
    """Every deliverable basename the prompt names appears verbatim in at least one positive criterion.

    R83 (2026-09-02, flyer-program-review pre-submission): the platform's Rubric
    filename format coverage check FAILs when the prompt names the exact deliverable
    file and no criterion quotes that basename as the workbook to produce or grade
    ("references such as 'the review's front page' are not sufficient"). The file row
    had been dropped to fit the R24 cap; it is not optional. Every deliverable basename
    the prompt names must appear verbatim in at least one positive criterion."""
    p = folder / "prompt.md"
    if not p.is_file():
        return
    prompt = p.read_text(encoding="utf-8", errors="ignore")
    inputs = {q.name.lower() for q in (folder / "inputs").glob("*")} if (folder / "inputs").is_dir() else set()
    deliverables = [m.group(1) for m in _R83_BASENAME_RE.finditer(prompt)
                    if m.group(1).lower() not in inputs]
    if not deliverables:
        return
    positive = " ".join(t for _, t, w in rows if w > 0)
    for name in sorted(set(deliverables)):
        if name not in positive:
            emit("ERROR", f"[R83] the prompt names the deliverable {name} and no positive criterion "
                          f"quotes that exact basename - the platform's Rubric filename format "
                          f"coverage check FAILs on it (flyer-program-review, 2026-09-02: 'references "
                          f"such as the review's front page are not sufficient'). Keep a +1 row of the "
                          f"form 'The deliverable is a single workbook named exactly {name}.'")


_R127_HEAD_RE = re.compile(r"\b(?:TEST|CHECK|FLAG|VERDICT|CALL)\b", re.I)


def _r127_norm(text):
    return re.sub(r"[^a-z]", "", re.sub(r"\bthe\b", "", text.lower()))


@check(codes=['R127'], rules=['PRE-COVER'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_verdict_column_coverage(rows, folder):
    """A golden column of verdict words under a TEST / CHECK / FLAG / VERDICT / CALL header is a rule the golden applies, and at least one positive criterion names that header or one of its verdict words.
    Since: 2026-09-14 (flyer-program-review adjudication, sound_aligned_rubric confirmed).
    Source: the Flyer 5 Plan FLOOR TEST column read HOLDS on all eight lineup rows against
    rule 6's 18 percent floor and 12 percent cover allowance, and no criterion graded margin
    compliance or the cover assignment; the adjudicator: "a solver who violates rule 6
    pricing could pass every criterion". The accepted rubric had dropped the cover-price row
    to fit the R24 cap, and the rows a later hand appended graded the percentages, not the
    golden's own verdict column, so the gap survived until adjudication.
    Drift-notes: a verdict column is three or more populated cells under the header, every
    value a short string, at most three distinct values; the header and the verdict words are
    matched with articles and punctuation stripped ("come out of the rotation" carries OUT OF
    ROTATION). A rule column the golden does not reduce to a verdict word is not seen here.
    """
    import openpyxl
    raw_positive = " ".join(t for _, t, w in rows if w > 0)
    positive = _r127_norm(raw_positive)
    if not positive:
        return
    for path in solution_files(folder, {".xlsx"}):
        try:
            wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
        except Exception:
            continue
        for ws in wb.worksheets:
            grid = list(ws.iter_rows(min_row=1, max_row=min(ws.max_row or 1, 400), values_only=True))
            if not grid:
                continue
            for r, row in enumerate(grid[:8]):
                for c, v in enumerate(row):
                    if not isinstance(v, str) or not _R127_HEAD_RE.search(v) or len(v) > 30:
                        continue
                    vals = []
                    for below in grid[r + 1:]:
                        cell = below[c] if c < len(below) else None
                        if cell is None or (isinstance(cell, str) and not cell.strip()):
                            if vals:
                                break
                            continue
                        vals.append(cell)
                    if len(vals) < 3 or not all(isinstance(x, str) and len(x) <= 20 for x in vals):
                        continue
                    words = sorted({x.strip() for x in vals})
                    if len(words) > 3:
                        continue
                    head = v.strip()
                    # a one-word verdict must be quoted in the golden's own casing (HOLDS), since
                    # the lowercase word is often a verb elsewhere in the rubric ("holds a formula");
                    # a multi-word verdict or the header matches with articles stripped
                    def named(w_):
                        if " " in w_.strip():
                            return _r127_norm(w_) in positive
                        return re.search(r"(?<![A-Za-z])" + re.escape(w_.strip()) + r"(?![A-Za-z])", raw_positive) is not None
                    if _r127_norm(head) in positive or any(named(w_) for w_ in words):
                        continue
                    emit("ERROR", f"[R127] {path.name} {ws.title}!{head}: the golden reduces a rule to the "
                                  f"verdict column {head} ({' / '.join(words)}) and no positive criterion "
                                  f"names the column or a verdict word - the flyer-program-review "
                                  f"adjudicator (2026-09-14) found rule 6 pricing ungraded this way ('a solver "
                                  f"who violates rule 6 pricing could pass every criterion'). Grade the "
                                  f"column: name its verdict on the rows that must carry it, anchored on one "
                                  f"cell")
        wb.close()


# R27 (2026-08-21, task 20 Agentic Rubric Quality Review): needs_improvement, six
# [major] non_atomic findings. A criterion carrying four quarterly percentages, or a
# total with its three components, is one scored item where the judge has four
# independent verdicts to reconcile. The reviewer's own test is "each could pass or fail
# independently". Counting numeric assertions approximates it: task 20's two worst
# offenders carried five figures each. It does NOT see a bundle of a table layout plus
# two counts, or a list of item codes plus their total, because those are not numerically
# dense — read the finding, do not trust a clean run.
#
# Splitting is not free. The bloat loop in memory/rubric-criterion-count.md is real, so
# split WEIGHT-NEUTRALLY: the parent's weight is divided among its children, never
# multiplied, or every completeness percentage is measured against a bigger denominator
# and the next check fails on a different requirement.
# a one-digit-then-dot token is a clause number in this domain (7.1, 5.4, 4.2);
# money always carries two decimals and a percentage always two or three digits
_ATOM_FIG_RE = re.compile(r"\d[\d,]*\.\d{2}\b|\b\d[\d,]{3,}\b|\b\d{2,3}\.\d\b|\b\d{1,3}\b")


_ATOM_CITE_RE = re.compile(r"^\s*(?:percent\s+)?(?:from|in|under|of)\s+(?:Article\s+)?\d|"
                           r"^\s*(?:business\s+)?day|^\s*percent\s+commitment", re.I)


_ATOM_ID_BEFORE_RE = re.compile(r"(?:purchase orders?|orders?|invoices?|quotations?|"
                                r"accounts?|lines?|items?|PU-|Article|clause)\s*$", re.I)


# R49 (2026-08-24, yankton-branch-opening human review): the reviewer named thirteen
# bundled positives and R27 saw two of them, because most carried only two figures or
# none. Their test is the same as the quality reviewer's, "one could be wrong and two
# right", and the shapes that failed it are countable rather than clausal:
#   * a list of item codes under one predicate ("Items OW075, DE040, PP050C and PP075C
#     do not open with stock")
#   * a list of account numbers under one predicate ("the history of accounts 10442 and
#     10518 ... and account 10088")
#   * a count of things and a money total in one sentence ("Seven items come off the
#     assortment ... and they come to $2,058.54"), the reviewer's own worked example:
#     the money is arithmetic off the count, so the count can stand while the money is
#     wrong. A zero count with a zero value is one claim, not two, and is exempt.
# Negatives are exempt throughout: a negative has to name the class members it fires on
# (R34), and this reviewer flagged positives only.
_R49_ITEM_RE = re.compile(r"\b[A-Z]{2,3}\d{3,4}[A-Z]?\b")


_R49_ACCT_RE = re.compile(r"\baccounts?\s+((?:\d{4,6}[,\s]*(?:and\s+)?){2,})", re.I)


_R49_MONEY_RE = re.compile(r"\$\s?(\d[\d,]*(?:\.\d{2})?)")


_R49_ONES = ("one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|"
             "fourteen|fifteen|sixteen|seventeen|eighteen|nineteen")


_R49_TENS = "twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety"


# the reviewer's own two examples spelled their counts out ("Seven items ... $2,058.54",
# "Forty-three lines ... $8,993.57"), so a digits-only count regex misses the shape
_R49_COUNT_RE = re.compile(r"\b(\d{1,4}|(?:" + _R49_TENS + r")(?:-(?:" + _R49_ONES + r"))?|(?:"
                           + _R49_ONES + r"))\s+(?:items?|lines?|orders?|accounts?|rows?|"
                           r"positions?|parts?|suppliers?|customers?|branches)\b", re.I)


# R54 (2026-08-24, yankton-branch-opening human review, second atomicity round): the same
# reviewer came back on nine rows the first split had left carrying a second scorable turn,
# none of which R27 (figure count) or R49 (subject count) can see. This is the clause-shape
# family the R27 docstring says not to build a CLASSIFIER for, and that advice stands: run
# against his labels the five signals below catch 9 of 9 but also hit six rows he did not
# name, every one of them the same shape as a row he did (a two-sentence item row beside the
# two he flagged, a parenthetical anchor beside the one he flagged). So this is not a
# classifier of bundled-vs-accepted; it is an AUTHORING constraint, fail-closed, and the
# repair is always the same and always cheap: fold the second turn into the first clause, or
# give it its own row and split the parent's weight. Positives only; a negative's shape is
# policed by W18/W19/R53, and since 2026-08-26 it carries no carve-out sentence (R18).
#
# One claim per criterion: one sentence, one verb, one figure-bearing assertion, plus
# acceptance clauses ("a cell reaching it through a plain cell reference counts too",
# "transcribed figures stay typed") which narrow one verdict rather than adding another.
_R54_SIGNALS = (
    ("a second sentence", re.compile(r"[.!?]\s+[A-Z]")),
    ("a trailing so/including clause", re.compile(r",\s*(?:so|including)\b")),
    ("a parenthetical carrying its own figures", re.compile(r"\([^)]*\d[^)]*\)")),
    ("a rule stating three parameters at once",
     re.compile(r"(?:\bclass [ABC]\b.*){3}|(?:\b(?:ten|thirteen|twenty)\b.*){3}", re.I)),
    # the derivation signal needs a FIGURE in front of it: "opens at 600 pieces, its 2,870
    # units rounded up" is a value plus its working, while "excess is on hand less committed
    # less the order point" is one definition and carries no value at all
    ("a value beside its own derivation",
     re.compile(r"\d[\d,]*(?:\.\d+)?[^.]*\b(?:its|being)\b[^.]*"
                r"\b(?:rounded|divided|multiplied)\b", re.I)),
)


# R55 (2026-08-24, standing house rule): A CRITERION IS ONE SIMPLE ATOMIC SENTENCE.
# R27 counts figures, R49 counts subjects and R54 catches five clause shapes, and between
# them oskaloosa still shipped a rubric where a colon introduced a second claim (C18, C25),
# a comma-and coordinated a second predicate (C20, C22, C34) and one criterion ran to 61
# words across four listed items plus an anchor plus an acceptance clause (C33). Each of
# those is independently right or wrong, which is exactly the reviewer's yankton complaint:
# "one could be wrong and two right". The grader scores a criterion as a single verdict, so
# a criterion that asserts two things cannot be scored, only guessed at.
#
# The rule, and it is not negotiable at authoring time:
#   one sentence, one main verb, one scorable claim.
# A NEGATIVE got a second sentence for its carve-out until 2026-08-26, when the platform's
# polarity check started failing "is not this defect" as scoring scaffolding (R18,
# tessendorf); a negative is now one sentence like everything else. An acceptance clause
# that NARROWS the one verdict ("with book quantity left as typed source data") is allowed
# because it cannot be scored on its own; a second assertion about a second thing cannot.
#
# The repair never adds weight: fold the second turn into a participial or prepositional
# phrase ("..., leaving an item still open held out of that sum"), or drop it. Splitting to
# a new row is available only under R11's 60-criterion ceiling and must stay weight-neutral.
_R55_MAX_WORDS = {True: 45, False: 45}      # one cap since the carve-out ban (2026-08-26, R18)


_R85_ABS_RE = re.compile(
    r",\s+(?:its|their|the|each|every)\s+[^,]*?\b(?:a formulas?|formulas?|standing|landing|sitting|"
    r"counted|carrying|with|reading|running|holding|keyed|typed)\b[^,]*", re.I)


_R85_ID_RE = re.compile(r"\b[A-Z]{2,4}-?\d{3,5}\b")


# R82 (2026-09-02, hollenbach-allocation-plan ACCEPT note): the reviewer accepted the task
# but adjusted every money figure in the rubric by hand - "the currency labels in your
# rubric criteria lack $ and proper notation so please human review them even if you are
# using LLM-generated inspiration". The rubric said "costs 10,958.6" and "premium of
# 2,476.8" where the workbook holds 10958.60 and 2476.80: no currency mark, and a trailing
# zero dropped so the figure reads to a tenth of a dollar. Both are mechanical.
_R82_LEAD_RE = re.compile(
    r"\b(?:costs?|priced?|premium|paid|pays|charges?|fees?|value|worth|amount|billed|"
    r"spend|spends|revenue|sales|margin|credit|balance|total(?:s|ling)?)\w*\s*"
    r"(?:of|at|to|is|are|comes?\s+to|stands?\s+at|reads?)?\s*$", re.I)


# a figure governed by a reference noun is an identifier, not money
_R82_REF_RE = re.compile(
    r"\b(?:section|policy|article|clause|paragraph|rule|ratio|tier|version|item|line|"
    r"quotation|order|invoice|account|registration|purchase\s+order|PO)\s*$", re.I)


# a figure that is a RATIO of money is not itself money ("liabilities to net worth at 2.76")
_R82_RATIO_RE = re.compile(
    r"\b(?:ratio|coverage|leverage|multiple|times)\b[^.;]{0,30}$"
    r"|\bto\s+(?:net\s+worth|equity|assets|sales|revenue)\s*(?:at|of|is|are)?\s*$", re.I)


_R82_NUM_RE = re.compile(r"(\$?)(\d{1,3}(?:,\d{3})*(?:\.\d+)?|\d+(?:\.\d+)?)")


@check(codes=['R82'], rules=['RUBQ-ATOM'], needs=['rubric'], params=['rows'])
def check_currency_notation(rows):
    """A money figure in a criterion carries a currency mark and is written to the cent."""
    for num, text, _ in rows:
        for m in _R82_NUM_RE.finditer(text):
            dollar, val = m.group(1), m.group(2)
            before = text[max(0, m.start() - 30):m.start()]
            if _R82_REF_RE.search(before) or _R82_RATIO_RE.search(before):
                continue
            # a unit noun anywhere before the next clause break makes it a quantity,
            # not money ("worth 369 additional breaker units")
            after = re.split(r"[,.;]", text[m.end():m.end() + 40])[0]
            if re.search(r"\b(?:percent|%|units?|pieces?|lines?|rows?|months?|days?|weeks?|"
                         r"cartons?|breakers?|orders?|tests?|shipments?|times|ratio)\b", after, re.I):
                continue
            money = bool(dollar) or bool(_R82_LEAD_RE.search(before))
            if not money:
                continue
            dec = val.split(".")[1] if "." in val else ""
            if not dollar:
                emit("ERROR", f"C{num} [R82] money figure {val} carries no currency mark - the "
                              "reviewer who accepted hollenbach-allocation-plan adjusted every one "
                              "of these by hand and asked for them to be read before submission "
                              "(2026-09-02). Write it as a currency amount")
            elif len(dec) == 1:
                emit("ERROR", f"C{num} [R82] money figure ${val} is written to a tenth of a dollar - "
                              "the workbook holds it to the cent, and a dropped trailing zero is "
                              "the notation the same accept note called out. Write it to two decimals")


@check(codes=['E0', 'E1', 'E2', 'W1', 'W10', 'W11', 'W12', 'W13', 'W14', 'W15', 'W16', 'W17', 'W18', 'W19', 'W2', 'W3', 'W4', 'W5', 'W6', 'W7', 'W8', 'W9'], rules=['DATA-TIME', 'GOLD-LAND', 'GOLD-LIVE', 'GOLD-NEG', 'PRE-FORM', 'PRE-POL', 'RUBQ-SCHEMA'], needs=['rubric'], params=['folder'])
def check_rubric_lint(folder):
    """Every criterion is worded so the oracle judge can verify it: framed negatives, anchored sweeps, no counterfactuals, no golden-schema imposition.

    Codes:
      E0   WEIGHT is numeric
      E1   a negative carries a polarity pin (a defect-frame word)
      E2   a negative never opens with a bare plural subject
      W1   no 'appears on no line' wording, which breaks on zero-quantity rows
      W2   a relative time window carries an absolute date anchor
      W3   the judge is never asked to re-sum an aggregate from a raw input CSV
      W4   a formula-liveness positive accepts reference chains
      W5   a 'may be typed' carve-out pins its dollar value
      W6   no negative liveness mirror (formulas-vs-constants as a penalty)
      W7   no counterfactual (recompute-on-change) wording on a static file
      W8   a dollar spot-check beside sibling cost columns carries an answer-key anchor
      W9   no meet-style polarity pin ('met only when')
      W10  a chain- or hop-framed liveness criterion says no tracing is needed
      W11  a universal sweep ('every/all ...') carries an answer-key anchor
      W12  no golden Sheet!Cell reference or private column name the prompt never mandates
      W13  a positive never asserts blankness or absence as the observable
      W14  a negative stacks at most two negations outside its pin
      W15  a negative never sweeps how a figure was computed or which column it came from
      W16  a liveness demand is never written as a row sweep
      W17  a negative's defect is never the application of a named rule to a record
      W18  a negative's defect sentence carries a defect-frame word
      W19  a negative's main verb is one a compliant deliverable never performs
    Since: 2026-08-18 (tasks 06/07/08 oracle runs), extended through 2026-08-26.
    Source: oracle verdicts on this portfolio; folded from tools/rubric_lint.py on 2026-09-04.
    """
    for _, num, level, code, msg in lint_file(rubric_path(folder)):
        emit(level, f"C{num} [{code}] {msg}")


@check(codes=['R1', 'R2', 'R25', 'R9'], rules=['GOLD-LIVE', 'PRE-FOCUS', 'PRE-FORM', 'PRE-OBJ'], needs=['rubric'], params=['rows'])
def check_form_basics(rows):
    """A criterion stays under 500 characters, anchors every evaluative term in its own sentence, states no drafting order, and pairs a formula demand with a displayed value.

    Codes:
      R1   a criterion is at most 500 characters (the form cap)
      R25  an evaluative term (consistently, appropriate, thin ...) carries a figure, quote or comparison in the same sentence
      R2   no process-ordering clause; a finished file carries no drafting timeline
      R9   a formula-only liveness criterion carries a displayed-value anchor
    Since: R25 2026-08-21 (task 20), magnitude words 2026-08-31 (inbound-consolidation-plan round 5); R9 deadstock C8.
    Source: the platform's Rubric objectivity check and final-outcome-focus check; R9 is a house rule.
    """
    for num, text, weight in rows:
        if len(text) > 500:
            emit("ERROR", f"C{num} [R1] criterion is {len(text)} chars — over the 500-char form cap")
        for sent in split_clauses(text):
            jm = JUDGMENT_TERM_RE.search(sent)
            mm = JUDGMENT_MAGNITUDE_RE.search(sent)
            if mm and not JUDGMENT_COMPARISON_RE.search(sent):
                jm = mm
            elif jm and JUDGMENT_ANCHOR_RE.search(sent):
                jm = None
            if jm:
                emit("ERROR", f'C{num} [R25] "{jm.group(0)}" is an evaluative term with no anchor in '
                              f'its own sentence - the platform Rubric objectivity check FAILs on '
                              f'exactly this (task 20, 2026-08-21, one word "consistently" sank the '
                              f'whole dimension). Put the figures, the precision or the quoted source '
                              f'language in the same sentence as the term, or drop the term and state '
                              f'the checkable fact')
        m = PROCESS_ORDER_RE.search(text)
        if m:
            emit("ERROR", f'C{num} [R2] process-ordering clause "{m.group(0)}" — a finished file carries '
                         'no drafting timeline (final-outcome-focus check); reword to observable facts')
        if weight > 0 and FORMULA_DEMAND_RE.search(text) and not VALUE_ANCHOR_RE.search(text) \
                and not LIVENESS_DISCLAIM_RE.search(text):
            emit("ERROR", f"C{num} [R9] formula-only liveness criterion with no displayed-value anchor — "
                         "judge formula extraction flakes even on pure head-call ranges (deadstock C8 "
                         "flaked 1/3 in runs 3 and 5 across two wordings; values-anchored C18 passed "
                         "3/3); pair the liveness clause with cached-value answer keys, or drop the "
                         "criterion after 2 flaky runs (house rule)")


@check(codes=['R12'], rules=['PRE-FORM'], needs=['rubric'], params=['rows'])
def check_weight_bands(rows):
    """Every weight is a non-zero integer in -5..+5.

    Source: docs/submission/platform/platform-submission-form.md section 4 ("Weight -5 to
    +5") and its checklist item 11.
    Drift-notes: rewritten 2026-09-21 in the Hazy port (docs/RULE-DELTAS.md D3). Geranium
    banned -1 and -2 outright; the Hazy form states the range as a continuous -5..+5 and
    offers page-limit and wrong-file-type penalties, which are naturally small.
    """
    for num, _, weight in rows:
        if weight != int(weight) or weight == 0 or not -5 <= weight <= 5:
            emit("ERROR", f"C{num} [R12] weight {weight:g} is outside the platform's range "
                          "(a non-zero integer from -5 to +5; platform-submission-form.md "
                          "section 4)")


@check(codes=['R11'], rules=['PRE-FORM'], needs=['rubric'], params=['rows'])
def check_criterion_count(rows):
    """The rubric carries at least 6 criteria, and 20+ for anything but a simple task.

    Source: docs/submission/platform/platform-submission-form.md section 4 ("minimum of 3
    criteria; expect somewhere in the 20-60+ range depending on complexity") and
    create-the-task-guidelines.md section 5 ("at least six criteria").
    Drift-notes: rewritten 2026-09-21 in the Hazy port (docs/RULE-DELTAS.md D2). Geranium
    required 15-60 and capped at 60; the Hazy form's range is open at the top ("20-60+"),
    so there is no ceiling any more. The floor is the guidelines' 6 rather than the form's
    3, because the guidelines are the stricter of the two and both must pass.
    """
    n = len(rows)
    if n < 6:
        emit("ERROR", f"[R11] {n} criteria - the guidelines require at least six "
                      "(create-the-task-guidelines.md section 5, restated in its Before "
                      "Submitting list). The form's checklist item 9 sets a floor of 3 and "
                      "adds that most real tasks need well more than 3")
    elif n < 20:
        recommend(f"[R11] {n} criteria - the form expects 20-60+ depending on complexity "
                  "(platform-submission-form.md section 4). Below 20 the rubric probably "
                  "leaves scoreable results untested; check coverage before submitting")


@check(codes=['R61'], rules=['PRE-FORM'], needs=['rubric'], params=['rows'])
def check_penalty_share(rows):
    """Negative weight reaches 20% of positive weight (a recommendation, never a gate).

    Since: 2026-08-25 (rempel-job-buyout adjudication note); non-blocking by team manager ruling 2026-09-02.
    Source: adjudication.
    Drift-notes: routed through recommend(), printed and never counted.
    """
    pos, neg = _weights(rows)
    # R61 (2026-08-25, rempel-job-buyout adjudication note): the penalty floor. The
    # reviewer scored the rubric's deterrence as a SHARE of what it rewards -- "total
    # negative weight is -16 (four criteria) against 134 positive weight (11.9%), which
    # is below the 20% penalty floor" -- and sent the task back to reach at least -27.
    # A rubric that pays out heavily and deducts lightly lets a solver bank the easy
    # positives and eat the penalties, so the floor is on the ratio, not on the count of
    # negatives. It is pure weight arithmetic and cannot false-positive; note that
    # CUTTING the positive denominator raises the share just as adding negatives does,
    # which is the same lever R24 already forces (task 19 went +132/-16 = 12.1% to
    # +66/-27 = 40.9% in one pass, closing both).
    if pos and abs(neg) < 0.20 * pos:
        recommend(f"[R61] negatives carry {abs(neg):g} against {pos:g} of positive weight "
                  f"({abs(neg) / pos:.1%}), under the 20% penalty share. NON-BLOCKING since the "
                  "team manager's ruling of 2026-09-02: the floor is \"a nice to have and not a "
                  "blocking requirement to submit or get an accepted task\", and it must never "
                  "be the main reason a task goes back, in adjudication or in review. Worth "
                  f"taking if it is cheap: {0.20 * pos:.1f} of negative weight, by raising "
                  "negatives on failures no positive already scores (R22/R41), or by cutting the "
                  "positive denominator, which R24 wants at "
                  "or under 66 anyway. Do not manufacture a negative to reach it")


@check(codes=['R24', 'R73'], rules=['PRE-COVER'], needs=['prompt', 'rubric', 'solution'], params=['rows', 'folder'])
def check_completeness_share(rows, folder):
    """A hand-keyed workbook must keep no more than 85% of positive weight (R24); with strict liveness capped at 10 points the positive total is therefore at most 39.

    Codes:
      R24  a workbook with every figure hand-keyed keeps under 85% of positive weight, and no single strict liveness row alone leaves 90% within a point of drift
      R73  when the prompt demands live formulas throughout (or a rerun on refreshed inputs), the gated tier alone (per-row gated rows for a rerun) holds over 15% (10% plus a point) of positive weight
    Since: 2026-08-24 (oskaloosa FAILed at 89.3%); single-loss reading 2026-08-26 (tessendorf); R73 2026-08-31.
    Source: the platform's Rubric full credit completeness check, which fails at about 90% retention and will not certify the line. INHERITED AND UNVERIFIED FOR HAZY (2026-09-21, docs/RULE-DELTAS.md D11): that check is one of Geranium's ten named post-submission evals and nothing confirms Hazy runs it. The rule is kept because the underlying defect is real - a rubric a hard-coded workbook still aces tests nothing - and because the bar is a share, so it survives the change in rubric size. Drop it if the first Hazy results show no completeness check.
    Drift-notes: only criteria a hard-coded workbook fails OUTRIGHT count as liveness; a formula clause on a correctness row buys nothing. The R73 prompt trigger also reads "math live", "live in the cells" and "pasted values" (hartwell-price-worksheet adjudication, 2026-09-12). R73 and R129 also read "keep the pricing on formulas" and "carry through the sheet" (twincreek-bid-worksheet refinement round 3, 2026-09-14, where R129 called a formula-demanding prompt static).
    """
    pos, neg = _weights(rows)
    prompt_text = (folder / "prompt.md").read_text(encoding="utf-8") if (folder / "prompt.md").exists() else ""
    has_xlsx = any((folder / "solution").glob("*.xlsx")) if (folder / "solution").is_dir() else False
    if pos and has_xlsx:
        strict = sum(w for _, t, w in rows if w > 0 and LIVENESS_STRICT_RE.search(t))
        gated = sum(w for _, t, w in rows if w > 0
                    and (LIVENESS_STRICT_RE.search(t) or LIVENESS_GATED_RE.search(t)))
        # The bar reads "about 90%", and 0.90 as a literal cutoff passed oskaloosa at 89.3%
        # (strict 9 of 84) in the same round the platform FAILed it: the check called that
        # "effectively at the bar" and would not certify a rubric sitting on the line. Its own
        # recomputation misadded the positive column (it enumerated the same 34 weights this
        # file sums to 84, called them 89, and argued 89.9%) - but the ruling turned on the
        # share, not the arithmetic, so do not argue the addition. An approximate bar needs
        # MARGIN, not a hair under: hold hand-keyed retention at 85% or below.
        if pos and (pos - strict) >= 0.85 * pos:
            emit("ERROR", f"[R24] a workbook with every figure correct but keyed by hand still "
                          f"keeps {(pos - strict) / pos:.1%} of positive weight ({pos - strict:g} of "
                          f"{pos:g}) - the platform's Rubric full credit completeness check FAILs at "
                          f"about 90% or more and will not certify the line either (oskaloosa, "
                          f"2026-08-24: FAILed at 89.3%; task 20, 2026-08-21: liveness held only 10 "
                          f"of 126 = 7.9%). Only criteria a hard-coded workbook fails OUTRIGHT count "
                          f"here, so a formula clause hanging off a correctness criterion does not "
                          f"buy cover. This is a SHARE, so it scales with the rubric: on Hazy's "
                          f"20-60+ criteria the fix is still to cut the positive denominator or "
                          f"raise the weight of the few rows a hard-coded workbook truly fails, "
                          f"not to add liveness criteria, which only adds flake surface. Any "
                          f"absolute positive total quoted in older notes was derived from "
                          f"Geranium's smaller rubrics and no longer holds (gated total here "
                          f"{gated:g}, leaving "
                          f"{(pos - gated) / pos:.1%})")
        elif pos and (pos - gated) >= 0.85 * pos:
            emit("ERROR", f"[R24] strict liveness clears the completeness bar only on the gated "
                         f"reading ({gated:g} of {pos:g}); the platform has discounted clauses it "
                         f"judged separable from the value being scored, so keep the derivation "
                         f"inseparable from the cell it describes")

        # R73 (2026-08-31, inbound-consolidation-plan AutoEval round 2): the frankfort
        # shape's SECOND platform FAIL, the re-probe trigger the LIVENESS_STRICT_RE
        # comment reserved. When the prompt itself demands live formulas throughout, the
        # full credit completeness check scores that workbook-wide requirement from the
        # gated tier ALONE: "Criteria 3 and 24 require live references only in two
        # isolated outputs ... a solver can satisfy those two 5-point checks with
        # references while hard-coding every other cost, saving, freight, bracket, and
        # calendar result; that selectively hard-coded workbook still earns all 39/39".
        # Strict read-throughs buy the requirement nothing; only value criteria whose
        # own figure is inseparably asserted as derived fail that solver. The frankfort
        # repair is weight neutral: attach derivation clauses to the substantive value
        # rows, anchored on cells storing pure single calls so the clause does not
        # trade a completeness hole for an oracle flake (R72).
        # Widened 2026-09-12 (hartwell-price-worksheet refinement, adjudication): "Keep the
        # math live in the cells ... I can't do that against pasted values" is the same
        # workbook-wide demand in a buyer's words, and the trigger never matched it, so the
        # gate passed a rubric whose gated tier held 3 of 39 and adjudication sent it back
        # ("lines 4-14 grade the remaining ~46 SKUs' landed costs and L1-L4 prices as values").
        prompt_live = re.search(
            r"\blive formulas?\b|\bformulas? (?:live|throughout)\b|\brecomputes?\b|\brecalculat"
            r"|\bmath live\b|\blive in the cells?\b|\bpasted values\b|\bhard-?coded values\b"
    r"|\b(?:keep|kept|keeps|built|build) (?:the )?[a-z]+(?: [a-z]+){0,5} on formulas?\b|\bcarr(?:y|ies) through the (?:sheet|workbook)\b",
            prompt_text, re.I)
        if pos and prompt_live and (pos - (gated - strict)) >= 0.85 * pos:
            emit("ERROR", f"[R73] the prompt demands live formulas throughout and the gated tier "
                          f"holds only {gated - strict:g} of {pos:g} positive points: a solver who "
                          f"keeps the strict read-through cells live and hard-codes everything else "
                          f"retains {(pos - (gated - strict)) / pos:.1%}, and the platform's Rubric "
                          "full credit completeness check FAILs exactly this ('that selectively "
                          "hard-coded workbook still earns all 39/39', inbound-consolidation-plan "
                          "round 2, 2026-08-31; frankfort-stock-recovery was the first). Attach "
                          "'the cell carrying it summing ... rather than a keyed figure' clauses to "
                          "the core value criteria until the gated tier alone holds over 15% of "
                          "positive weight, anchoring them on pure single-call cells (R72)")

        # R73 REFRESH-CHAIN variant (2026-08-31, tessendorf round 3): when the prompt
        # promises a RERUN on refreshed inputs, a gated tier of summary references, count
        # cells and price cells clears the 15% bar and STILL buys nothing - the checker's
        # solver keys the imported source figures and every source-dependent row result,
        # leaves real formulas in exactly the checked cells, and retains 39/39. The
        # workbook-wide contract is only failed by PER-ROW gated criteria over the working
        # rows themselves, task 23's shape ("the program side on each of the 26 catalog
        # rows is a formula over its row's movement, its net and the rate cells rather
        # than a keyed figure"), weighted so that solver lands under 90% with the drift
        # cushion: over 10% of positive plus a point. Typed source-data columns stay typed
        # and are never asserted live. Scoped to prompts carrying both the live-formula
        # demand and refresh/rerun language (task 23's prompt carries neither word and its
        # 1-point per-row row stays legal). Probed 2026-08-31: fires on the round-2
        # tessendorf rubric (per-row gated 0), silent on the round-3 one (5).
        prompt_rerun = re.search(r"\brefresh\w*|\bre-?runs?\b|\brerun\w*", prompt_text, re.I)
        if pos and prompt_live and prompt_rerun:
            per_row = sum(w for _, t, w in rows
                          if w > 0 and LIVENESS_GATED_RE.search(t)
                          and re.search(r"\b(?:on )?each (?:of the )?\d{1,4}\b[^.]{0,60}\bformula", t, re.I))
            if per_row <= 0.10 * pos + 1:
                emit("ERROR", f"[R73] the prompt promises a rerun on refreshed inputs and the per-row "
                              f"gated criteria hold only {per_row:g} of {pos:g}: a solver who keys the "
                              f"source figures and every row result while keeping formulas in the "
                              f"summary, count and price cells retains "
                              f"{(pos - per_row) / pos:.1%} (tessendorf round 3, 2026-08-31: 39/39 with "
                              "a 15.4% gated tier of exactly those cells). Pin the working rows "
                              "themselves - per-row formula criteria over the row's source and rate "
                              "cells - until they hold over 10% of positive plus a point")

        # SINGLE-LOSS variant (2026-08-26, tessendorf pre-submission): the same platform
        # check also quantifies hard-coding ONE anchored figure while the other liveness
        # chain stays genuinely live - "either single-value hard-code ... leaves at/above
        # the 90% near-full-credit line" (a true 45/50 = 90.0%, which its own addition
        # slip read as 46/51 = 90.2%). Each strict liveness criterion must therefore cost
        # more than a tenth of the positive total ON ITS OWN, and the test carries a
        # one-point cushion because the checker's sums drift by about that much (50 read
        # as 51 here; oskaloosa's 84 read as 89). With the +5 weight cap this pins the
        # positive total at 39 or under. The checker's other remedy, a typed-constant
        # negative, is ORACLE-TOXIC and must not be taken: W6/W15 formulas-vs-constants
        # mirror negatives drew ambiguous_negative_polarity 3/3 at wamhoff (2026-08-20),
        # so the denominator is the only lever.
        for num, t, w in rows:
            if w > 0 and LIVENESS_STRICT_RE.search(t) and pos - w + 1 >= 0.90 * pos:
                emit("ERROR", f"C{num} [R24] hard-coding only this criterion's figure keeps "
                              f"{(pos - w) / pos:.1%} of positive weight ({pos - w:g} of {pos:g}), "
                              f"within an addition slip of the 90% line the Rubric full credit "
                              f"completeness check FAILed tessendorf on (2026-08-26, single-value "
                              f"hard-code read as 90.2%). Cut the positive denominator until each "
                              f"strict liveness criterion alone costs over 10% plus a point of "
                              f"cushion (under {(w - 1) / 0.10:.0f} for this weight); do NOT add "
                              f"a typed-constant negative, which the oracle flags "
                              f"ambiguous_negative_polarity 3/3 (W6/W15, wamhoff 2026-08-20)")


# R129 (2026-09-14, hx4180-fa26-spec-rev3 refinement round 2, adjudication): the note counted
# "14 of 39 positive points (35.9%) for formula/cell-reference implementation and tab
# architecture (criteria 3, 7, 20-23) that the prompt never requires, exceeding the 25%
# implementation cap and failing a numerically correct static-value workbook". The 14 were
# exactly the set R24 reads (two +5 strict read-throughs and four +1 "is a formula rather than
# a keyed figure" rows), so the cap is the mirror of R24's floor: liveness has to hold more than
# 15% (R24) and, where the prompt never asks for live formulas, no more than a quarter. That
# closes the two-strict-rows +39 shape (10 of 39 is 25.6%) for such prompts; the shape that fits
# both is one +5 strict row at positive 33 or under with one or two gated +1 rows (7 of 33).
# Portfolio probe 2026-09-14: the 10-of-39 shape has passed adjudication repeatedly
# (june-price-review run 11, delivery-zone-reset), so the error line sits just above it.
_R129_PROMPT_LIVE_RE = re.compile(
    r"\blive formulas?\b|\bformulas? (?:live|throughout)\b|\brecomputes?\b|\brecalculat"
    r"|\bmath live\b|\blive in the cells?\b|\bpasted values\b|\bhard-?coded values\b"
    r"|\b(?:keep|kept|keeps|built|build) (?:the )?[a-z]+(?: [a-z]+){0,5} on formulas?\b|\bcarr(?:y|ies) through the (?:sheet|workbook)\b"
    r"|\bkeep (?:it|them|the [a-z]+) live\b", re.I)


@check(codes=['R129'], rules=['RUBQ-RIGID'], needs=['prompt', 'rubric', 'solution'], params=['rows', 'folder'])
def check_implementation_share(rows, folder):
    """Formula and cell-reference criteria, strict and gated together, hold a quarter of positive weight or less when the prompt makes no live-formula demand; adjudication reads a larger share as grading implementation the prompt never asked for and failing a numerically correct static workbook.

    Since: 2026-09-14 (hx4180-fa26-spec-rev3 refinement round 2, adjudication).
    Source: adjudication ("14 of 39 positive points (35.9%) for formula/cell-reference implementation and tab architecture (criteria 3, 7, 20-23) that the prompt never requires, exceeding the 25% implementation cap and failing a numerically correct static-value workbook").
    Drift-notes: counts every positive matching the strict or gated liveness patterns, the same set R24 reads, so with R24's 15 percent floor the band is 16 to 25 percent: one +5 strict row at positive 33 or under with one or two gated +1 rows. The 10-of-39 two-strict shape (25.6 percent) has passed adjudication (june-price-review run 11, delivery-zone-reset), so the error fires only above that share. Silent when the prompt carries R73's live-formula trigger, where the platform's completeness check demands breadth instead. Also silent on "keep it live" and "keep the X live" (vendor-terms-program refinement round 2, 2026-09-14: a prompt asking the workbook to stay live while the controller changes numbers, whose own panel returned the golden for typed decisions, read as static); R73's trigger does not take that phrase, because the platform's completeness check passed that rubric at a gated tier of 4 of 39. "Keep X on formulas" takes up to six words for X (pick-module-reslot, 2026-09-14: "Keep the classing and the bin assignments on formulas" read as static on a prompt that asks for formulas).
    """
    pos, _ = _weights(rows)
    has_xlsx = any((folder / "solution").glob("*.xlsx")) if (folder / "solution").is_dir() else False
    if not pos or not has_xlsx:
        return
    prompt = folder / "prompt.md"
    if prompt.exists() and _R129_PROMPT_LIVE_RE.search(prompt.read_text(encoding="utf-8")):
        return
    live = [(n, w) for n, t, w in rows if w > 0
            and (LIVENESS_STRICT_RE.search(t) or LIVENESS_GATED_RE.search(t))]
    share = sum(w for _, w in live)
    if not share:
        return
    names = ", ".join(f"C{n}" for n, _ in live)
    if share / pos > 10 / 39 + 1e-9:
        emit("ERROR", f"[R129] formula and cell-reference criteria ({names}) hold {share:g} of {pos:g} positive "
                      f"points ({share / pos:.1%}) and the prompt never asks for live formulas: adjudication caps "
                      f"implementation at 25% and returned hx4180-fa26-spec-rev3 at 14 of 39 (2026-09-14) as "
                      f"'failing a numerically correct static-value workbook'. Keep one +5 strict row, ride at most "
                      f"one or two gated clauses on value rows, and cut the positive denominator so R24's "
                      f"floor still holds. The cap is a share, not a point total: the '33 or under' in "
                      f"older notes was Geranium arithmetic and does not survive a 20-60+ rubric")


def _r92_grouping_coverage(rows, folder):
    """A batched-by or grouped-by presentation the prompt demands has a positive criterion of its own.

    Since: 2026-08-24 (june-price-review).
    Source: the platform's Rubric requirement mapping check.
    Drift-notes: R46's second arm until 2026-09-04.
    """
    prompt = Path(folder) / "prompt.md"
    if not prompt.exists():
        return
    for m in _GROUPED_BY_RE.finditer(prompt.read_text(encoding="utf-8")):
        noun = m.group(1).lower()
        if any(w > 0 and noun in t.lower()
               and re.search(r"\bbatch|\bgroup|\bby\s+" + noun + r"|\bper\s+" + noun, t, re.I)
               for _, t, w in rows):
            continue
        emit("ERROR", f'[R92] the prompt demands a presentation "{m.group(0)}" and no positive '
                      "criterion grades that grouping — the platform's Rubric requirement "
                      "mapping check FAILs on exactly this (june-price-review, 2026-08-24). "
                      "Add one dedicated criterion for the by-" + noun + " organization")


@check(codes=['R13', 'R4', 'R92'], rules=['PRE-COVER'], needs=['prompt', 'rubric'], params=['rows', 'folder'])
def check_prompt_every_coverage(rows, folder):
    """When the prompt demands every or all items, a completeness criterion pins the count and the coverage block carries at least 10% of positive weight; a grouped-by presentation the prompt demands has its own criterion.

    Codes:
      R4   a prompt demanding every/all items has a criterion pinning a completeness count
      R13  the coverage criteria together carry at least 10% of positive weight
      R92  a batched-by or grouped-by presentation the prompt demands has a positive criterion of its own
    Since: tasks 01/03 (reviewer gap, R4); dillman C2 2026-08-19 (R13); june-price-review 2026-08-24 (R92).
    Source: the platform's Rubric full credit completeness check and Rubric requirement mapping check.
    Drift-notes: R92 was a carve-out twin (R46's second arm), merged back 2026-09-11.
    """
    _r92_grouping_coverage(rows, folder)     # [R92] the carve-out twin, merged back 2026-09-11
    prompt = folder / "prompt.md"
    if prompt.exists() and PROMPT_EVERY_RE.search(prompt.read_text(encoding="utf-8")):
        comp = [(num, w) for num, t, w in rows if w > 0 and COMPLETENESS_RE.search(t)]
        if not comp:
            emit("ERROR", '[R4] prompt demands "every/all <items>" but no criterion pins a completeness '
                         "count — spot-checks alone let omissions pass (reviewer gap on tasks 01/03)")
        else:
            pos_total = sum(w for _, _, w in rows if w > 0)
            block_w = sum(w for _, w in comp)
            block = ", ".join("C" + n for n, _ in comp)
            if pos_total and block_w < 0.10 * pos_total:
                emit("ERROR", f"[R13] the coverage criteria ({block}) carry {block_w:g} of {pos_total:g} "
                             f"positive weight — omitting the core coverage table retains "
                             f"{(pos_total - block_w) / pos_total:.1%} of positive credit; the 'Rubric full "
                             "credit completeness check' FAILs at ~90%+ retained (dillman C2 2026-08-19, "
                             "w3/101 = 97%). Get the block over 10% with MORE in-band criteria, one per "
                             "failure mode a solver can hit independently (items missing, branches missing, "
                             "combinations repeated) — never one heavier criterion, which R12 rejects above "
                             "+5; negatives do not count toward this check")


@check(codes=['R95'], rules=['PRE-DUP'], needs=['rubric'], params=['rows'])
def check_total_twins(rows):
    """A dollar total is asserted as a scored total in one criterion only.

    Since: 2026-08-19 (deadstock C3 against C17).
    Source: the platform's near identical criteria check.
    Drift-notes: R12's second arm until 2026-09-04.
    """
    DOLLAR_RE = re.compile(r"\$\d{1,3}(?:,\d{3})+\.\d{2}|\$\d{4,}\.\d{2}")
    TOTAL_CUE_RE = re.compile(r"\b(totals?|gross|equal(s|ing)?|sums?( to)?|adds? up)\b", re.I)
    asserted = {}
    for num, text, weight in rows:
        if weight <= 0:
            continue
        for m in DOLLAR_RE.finditer(text):
            window = text[max(0, m.start() - 40):m.end() + 40]
            if TOTAL_CUE_RE.search(window):
                asserted.setdefault(m.group(0), []).append(num)
    for amount, nums in sorted(asserted.items()):
        if len(set(nums)) > 1:
            pair = ", ".join(f"C{n}" for n in sorted(set(nums), key=int))
            emit("ERROR", f"[R95] {amount} is asserted as a scored total in {pair} — the platform's "
                         "'near identical criteria' check FAILs this as redundancy by subsumption "
                         "(deadstock C3 vs C17, 2026-08-19); keep the total in ONE criterion and let "
                         "the sibling carry only mechanics/composition, citing the figure as context "
                         "at most")


@check(codes=[], rules=[], needs=['rubric'], params=['rows'])
def rubric_info(rows):
    """Print the rubric's weight totals and the oracle reward arithmetic (information only, emits nothing).

    Since: 2026-08-25 (hollenbach run 5, fitted exactly to three rewards).
    """
    pos, neg = _weights(rows)
    # Reading an oracle reward (hollenbach run 5, 2026-08-25, fitted to all three rewards
    # of [0.9877, 1.0000, 0.9875] and exact on each): the denominator is positive weight
    # PLUS the absolute negative weight, because avoiding a defect earns that weight too,
    # and any criterion the judge verdicts unverifiable_from_deliverable is dropped from
    # BOTH sides rather than scored. So reward = (base - unverifiable - failed) /
    # (base - unverifiable). Two consequences worth having in front of you before you
    # touch a golden: an unverifiable criterion costs nothing (that run scored 1.0000
    # carrying one), and a deficit will NOT divide cleanly into the positive total alone -
    # dividing by {pos} there gave 0.81 of a weight point, which is impossible, and reads
    # as an unsubmitted rubric when nothing was wrong with the form at all.
    base = pos - neg
    print(f"        info: {len(rows)} criteria, positive weight {pos:g}, negative {neg:g}")
    print(f"        info: oracle reward = (B - u - f) / (B - u) with B = {pos:g} + {-neg:g} "
          f"= {base:g}; u = weight verdicted unverifiable_from_deliverable (dropped from BOTH "
          f"sides, costs nothing), f = weight failed - and a judge RUNTIME error "
          f"(judge_failed, content_type=NoneType) is fail-closed INTO f, so it costs the "
          f"criterion's full weight where an unverifiable verdict costs zero. "
          f"One +1 criterion failing alone reads {(base - 1) / base:.4f}")




# R99 (2026-09-09, dfl-freight-audit adjudication note): the four rows grading the core
# analytical work (rating every bill, the rated total, the overcharge classification, the claim
# total) sat at +2 while the rubric's top positive was +3, and the adjudicator sent the task
# back to put them at +4 or +5: "so the central deliverable requirements are weighted at the top
# of the 1-5 scale". The platform guidelines list "flat weighting (at least one core criterion at
# +4/5)" among the rubric mistakes (Geranium's project-guidelines-v5.1.md, deleted in the
# 2026-09-21 port; Hazy's form restates the spirit as "weight by how central the item is
# to a correct deliverable"). This
# is the mechanical half: a rubric whose highest positive weight is under 4 is flat by
# construction. Which rows are the core ones is a hand read; put the top weight on the figures
# the prompt's main ask turns on, not on the file row or an example.
@check(codes=['R99'], rules=['PRE-FORM'], needs=['rubric'], params=['rows'])
def check_flat_weighting(rows):
    """At least one positive criterion carries +4 or +5.

    Since: 2026-09-09 (dfl-freight-audit adjudication note).
    Source: Hazy's platform-submission-form.md section 4 ("Weight -5 to +5 based on how central the item is to a correct deliverable"),
    which is the surviving form of Geranium's project-guidelines-v5.1 'flat weighting' mistake (that file was deleted in the 2026-09-21 port).
    """
    pos = [w for _, _, w in rows if w > 0]
    if not pos:
        return
    top = max(pos)
    if top < 4:
        emit("ERROR", f"[R99] the highest positive weight is +{top:g}: the rubric is flat. The platform "
                      "guidelines list 'flat weighting (at least one core criterion at +4/5)' as a "
                      "rubric mistake and the dfl-freight-audit adjudicator sent the task back on it "
                      "(2026-09-09), asking for the rows that grade the central deliverable (the rated "
                      "total, the classification, the claim total) at +4 or +5. Raise the core rows, "
                      "keep the file row and the examples where they are")


# R100 (2026-09-09, dfl-freight-audit adjudication note): six action rows required "a named
# person as owner and a calendar date" on each corrective action while the prompt asked only for
# "what we change on our own dock so the same mistakes stop". The adjudicator: strip the clause
# "so that credit turns on the substance of the change alone". This is the other bound of R81
# (never the PERSON): an owner-or-date test is only a test when the prompt asked for owners or
# dates. When the prompt carries no owner/date language (the action vocabulary plus the plain
# forms below), a positive action row that scores an owner or a date grades something the
# solver was never asked for.
_R100_CLAUSE_RE = re.compile(
    r"\bnamed person\b|\b(?:an|the|with an|its|each with an?) owner\b|\bowner (?:and|of|named|on)\b"
    r"|\bcalendar date\b|\bcompletion date\b|\btarget date\b|\bdue date\b|\bdate (?:for|on|against) each\b", re.I)


_R100_PROMPT_RE = re.compile(
    r"\bowners?\b|\bwho\b[^.]{0,60}\b(?:when|by when|what|does|takes|handles)\b|\bby when\b|\bdue dates?\b"
    r"|\bcompletion dates?\b|\btarget dates?\b|\bwith a date\b|\bdate(?:s|d)? (?:for|on|against|beside) each\b"
    r"|\bname (?:and|with) a date\b|\bresponsible\b|\bassign\w*\b", re.I)


@check(codes=['R100'], rules=['RUBQ-RIGID'], needs=['prompt', 'rubric'], params=['rows', 'folder'])
def check_unmandated_owner_clause(rows, folder):
    """An action row scores an owner or a date only when the prompt asked who and by when.

    Since: 2026-09-09 (dfl-freight-audit adjudication note).
    Source: adjudication.
    Drift-notes: the upper bound to R81 (never the person); together they fix owner rows to 'an owner and a date' only when asked.
    """
    prompt_text = (folder / "prompt.md").read_text(encoding="utf-8") if (folder / "prompt.md").exists() else ""
    if R100_PROMPT_ACTION_RE.search(prompt_text) or _R100_PROMPT_RE.search(prompt_text):
        return
    for num, text, weight in rows:
        if weight <= 0:
            continue
        m = _R100_CLAUSE_RE.search(text)
        if not m:
            continue
        if "named person" not in m.group(0).lower() and not R100_ACTION_RE.search(text):
            continue
        emit("ERROR", f"C{num} [R100] scores an owner or a date on an action (\"{m.group(0)}\") while the "
                      "prompt asks for the actions and never for who owns them or by when. The "
                      "dfl-freight-audit adjudicator struck the clause from six rows (2026-09-09) so that "
                      "credit turns on the substance of the change alone; a solver who lists the right "
                      "changes without a name or a date loses nothing the prompt asked for. Drop the "
                      "clause, or put the owner/date ask in the prompt if the task needs it")


# R101 (2026-09-09, frankfort-stock-recovery, Agentic Rubric Quality Review): the review
# called the two headline money figures "token weighted", and the sweep it prompted found
# worse - the golden's front page carried a whole labelled block, "WHAT WE ASK TIPTON TO
# ADVANCE NOW" (the advance and what is left to settle at the proof of loss), that NO
# criterion scored at all. A solver could omit the block entirely and lose nothing. The
# front page is the one sheet every prompt in this portfolio promises and the one the
# requester reads, so each of its labelled blocks has to be reachable by the rubric: not
# every figure under a heading, but at least one, or the heading is unscored decoration.
# Sections are delimited by the all-caps labels the goldens use as block headings.
# A block is scored either by figure (a criterion carries one of its values) or by rule: a
# positive criterion that restates one of its row labels - "the walk index as slotted today
# is the sum over the item rows of ...", "the share of the walk saved is one minus ..." -
# scores that row's figure without quoting it, which is the shape the Agentic Rubric Quality
# Review forced on pick-module-reslot (rounds 3 and 4, 2026-09-03: allocation results stated
# as their derivation, no literal). The restatement test is the label's leading phrase,
# through its third content word, appearing verbatim in a positive criterion. Shared words
# alone are not enough: the frankfort advance label ("total loss inside the building and the
# two limited items, less the deductible") shares four words with a criterion that scores a
# bin count ("41 bins inside the building are a total loss") and must still fire (2026-09-10).
_R101_HEAD_RE = re.compile(r"^[A-Z][A-Z0-9 ,.'&/()-]{6,}$")
_R101_STOP = {"with", "from", "that", "this", "than", "then", "when", "into", "over", "under",
              "each", "every", "their", "them", "they", "what", "which", "where", "after",
              "before", "both", "less", "more", "also", "only", "some", "such", "same"}


def _r101_norm(text):
    """Lowercase words, punctuation out, one space between."""
    return " ".join(re.findall(r"[a-z0-9]+", text.lower()))


def _r101_lead(label):
    """The label's leading phrase through its third content word, or None when the label
    carries fewer than two content words (a bare "Deductible" is not a restatement)."""
    words = _r101_norm(label).split()
    content = 0
    for i, w in enumerate(words):
        if len(w) >= 4 and w not in _R101_STOP and not w.isdigit():
            content += 1
            if content == 3:
                return " ".join(words[:i + 1])
    return " ".join(words) if content >= 2 else None


def _r101_plain(v):
    """A number as the rubric would spell it, commas and currency stripped."""
    if isinstance(v, bool):
        return None
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        return ("%f" % v).rstrip("0").rstrip(".")
    return None


@check(codes=['R101'], rules=['PRE-COVER'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_front_page_blocks_scored(rows, folder):
    """Every labelled block on the golden's front page is scored by at least one criterion."""
    scored = " ".join(t for _, t, w in rows if w > 0).replace(",", "").replace("$", "")
    positives = " | ".join(_r101_norm(t) for _, t, w in rows if w > 0)
    d = folder / "solution"
    for path in sorted(d.glob("*.xlsx")) if d.is_dir() else []:
        try:
            wb = workbook(path, data_only=True)
        except Exception:
            continue
        ws = wb.worksheets[0]
        heading, values, labels, wide = None, [], [], False
        blocks = []

        def close():
            # a summary block is label-and-amount rows; a row carrying several figures is
            # a detail table that happens to sit under a caps label, and its line values
            # are not headline figures the rubric owes a criterion (vrm-exception-review
            # "SALES ORDER", 2026-09-09)
            if heading and len(values) >= 2 and not wide:
                blocks.append((heading, list(values), list(labels)))

        for row in ws.iter_rows():
            label = row[0].value if row else None
            if isinstance(label, str) and _R101_HEAD_RE.match(label.strip()):
                close()
                heading, values, labels, wide = label.strip(), [], [], False
                continue
            if heading is None:
                continue
            if isinstance(label, str) and label.strip():
                labels.append(label.strip())
            in_row = []
            for c in row:
                q = _r101_plain(c.value)
                if q is None:
                    continue
                # a bare single-digit integer is a row count, not a headline figure
                if isinstance(c.value, int) and abs(c.value) < 10:
                    continue
                in_row.append(q)
            if len(in_row) > 1:
                wide = True
            values.extend(in_row)
        close()
        for heading, values, labels in blocks:
            if any(re.search(rf"(?<![\d.]){re.escape(v)}(?![\d])", scored) for v in values):
                continue
            # scored by rule: a positive criterion restates one of the block's row labels
            leads = [ld for ld in (_r101_lead(lab) for lab in labels) if ld]
            if any(f" {ld} " in f" {positives} " for ld in leads):
                continue
            emit("ERROR", f"[R101] the front page of {path.name} carries the block \"{heading}\" and no "
                          f"criterion scores any figure in it ({', '.join(values[:4])}) - a solver can "
                          "leave the whole block out and lose nothing, which is how frankfort-stock-"
                          "recovery shipped an unscored advance-to-be-requested block past nine rounds "
                          "(2026-09-09). Score at least one figure from every labelled block on the "
                          "sheet the prompt promises, or drop the block from the golden")


# R102 (2026-09-10, po-conformance-review adjudication note): the prompt said the document
# is "addressed to Doris" and the golden carried "To: Doris Leidy, Controller", but no
# criterion graded the addressee, and the adjudicator sent the task back for a structural
# criterion requiring it. Every literal ask in the prompt owes the rubric a row (the same
# note asked for the two attribute totals the prompt's "count and the dollars under each"
# had left ungraded, which no regex can pair). The addressee is mechanical: a prompt that
# names who the deliverable is addressed to must have one positive criterion on it.
_R102_PROMPT_RE = re.compile(r"\baddressed to ([A-Z][\w'-]+(?: [A-Z][\w'-]+)?)")
_R102_CRIT_RE = re.compile(r"\baddress(?:ed|ee)\b", re.I)


@check(codes=['R102'], rules=['PRE-COVER'], needs=['prompt', 'rubric'], params=['rows', 'folder'])
def check_addressee_graded(rows, folder):
    """When the prompt names who the deliverable is addressed to, a positive criterion grades the addressee."""
    prompt = folder / "prompt.md"
    if not prompt.exists():
        return
    m = _R102_PROMPT_RE.search(prompt.read_text(encoding="utf-8"))
    if not m:
        return
    if any(w > 0 and _R102_CRIT_RE.search(t) for _, t, w in rows):
        return
    emit("ERROR", f'[R102] prompt.md says the deliverable is "addressed to {m.group(1)}" and no positive '
                  "criterion grades the addressee - po-conformance-review was sent back from adjudication "
                  "for exactly this (2026-09-10): add one structural +1 row, \"The document is addressed "
                  f"to {m.group(1)}.\", spelled the way the inputs spell the name")


# R105 (2026-09-11, freight-audit-review refinement, golden check 2/3 at 1.0): C38 read
# "Opens with an executive summary that leads with the decomposition of the increase and the
# recovery figure" and one judge in three held "leads with" to the first sentence, which
# carried the total and the memo's attribution, failing the golden at 0.9851 with the
# platform's own note "possible judge variance on visual/static deliverables". An ORDERING
# claim (leads with, opens with, begins with, starts with) is one verdict only when ONE
# thing is to come first; two determiner-led objects coordinated after it ("the X ... and
# the Y") are two verdicts, and a golden's opening seldom carries both at its head. R55
# cannot see the shape (no colon, no comma-and, one sentence). The repair is to name one
# object and pin WHERE it sits ("whose first paragraph states ...") so the judge reads a
# location rather than a relative order, and to put that object in the golden's opening.
# Probed 2026-09-11 across submissions/, drafts/ and refinements/: fires on the pre-fix
# C38 only (44-pick-module-reslot C18 "opens with the cabinet and lifting corrections"
# coordinates two modifiers under one noun and does not fire).
_R105_ORDER_RE = re.compile(
    r"\b(?:leads?|opens?|begins?|starts?) with\b(?P<rest>[^.;:]*)", re.I)
_R105_PAIR_RE = re.compile(r"\b(?:the|a|an|its|their|each|every)\b[^,]*?\band (?:the|a|an|its|their|each|every)\b", re.I)


# ---- the subsumption family: two positives where passing one passes the other, one walk ------
# ---- rationale kept from the merged checks (subsumption family) ----
# R10:
#   R10: two criteria key the same golden cell, or one keys a range containing the
#       other's cell. The platform's "near identical criteria" check reads that as
#       redundancy by subsumption and FAILS the submission.
#
#       Dillman 2026-08-19: C31 keyed 'First Order'!M43 for the $13,166.52 order total
#       while the liveness criterion C49 keyed 'First Order'!K5:M43 AND restated the same
#       total as its cached-value anchor, so passing C49 necessarily passed C31. The same
#       shape sat unflagged on Economics!C27:C29 (liveness) against C27, C28 and C29
#       keyed individually by three answer criteria. The anchors came from following R9,
#       which is why R9 now carries the carve-out: never anchor a liveness criterion on a
#       value another criterion already scores. Keep liveness criteria value-free and let
#       the answer criteria own the numbers.
# R47:
#   R47: a single-figure positive criterion whose only figure another positive
#       restates is the subsumption shape the platform FAILs; multi-figure worked
#       chains and shared thresholds are the overlaps its ruling explicitly allows
#       ("distinct rows, totals, locations"), so only the weaker-row shape is flagged.
#       Clause-like tokens (7.1) and figures without cents never count.
# R124 (2026-09-14, recall-response refinement round 3, Rubric near identical criteria check
# FAIL): "lists exactly the 12 item and lot combinations in scope across the four lot codes"
# (C5) and "carries the three withdrawn item references and no other item, four lots under
# each" (C7) on the same tab - the closed-set row restates the set the exact-count row already
# fixes and adds no figure of its own, so passing C5 necessarily passes C7. The count must be
# of set members (rows, lines, combinations, items, lots ...): "exactly 199 on hand" is a
# figure and never pairs. Probed over 1,149 positives in 46 rubrics: one hit, that pair.
_R124_TAB_RE = re.compile(r"\b([A-Z][A-Za-z]+(?:_[A-Za-z]+)+|[A-Z][a-z]+) tab\b")
_R124_EXACT_RE = re.compile(
    r"\bexactly (?:the )?\d+ (?:[a-z-]+ ){0,3}?"
    r"(?:rows?|lines?|combinations?|items?|lots?|customers?|accounts?|tabs?|entries|records?|shipments?|codes?|references?)\b", re.I)
_R124_CLOSED_RE = re.compile(r"\bno other\b|\band nothing else\b|\bonly the\b", re.I)
_R124_FIG_RE = re.compile(r"\b\d[\d,.]*\b")


@check(codes=['R10', 'R47', 'R57', 'R60', 'R86', 'R124'], rules=['PRE-DUP'], needs=['rubric'], params=['rows'])
def check_subsumption(rows):
    """No two criteria score one thing twice: no overlapping answer keys, no single-figure row another restates, no universal derivation over rows other positives name, no attribute asserted per item twice, and no named quantity equated to two figures.

    Codes:
      R10  two criteria never key the same golden cell, or a range containing another's cell
      R47  a single-figure positive never states only a figure another positive also states
      R57  a positive asserting a derivation over every row never coexists with positives scoring named rows of it
      R60  one named quantity is never equated to two different figures
      R86  two positives never both assert the presence of the same attribute per item on the same subject with no shared figure
      R124 an exact-count row and a closed-set row (no other, nothing else) on the same tab never coexist when the closed row adds no figure of its own
    Since: R10 2026-08-19 (dillman C31/C49); R47 2026-08-24 (june-price-review C33/C36); R57 and R60 2026-08-25
    (open-order-cleanup); R86 2026-09-03 (dfl-freight-audit).
    Source: the platform's near identical criteria check (redundancy by subsumption) and the Agentic Rubric
    Quality Review (R60, 'both cannot be right').
    Drift-notes: five detectors merged into one walk over the rubric on 2026-09-11; R124 added 2026-09-14 (recall-response).
    """
    keys, figs, named, universal, equated, per_item = [], {}, [], [], {}, []
    for num, text, weight in rows:
        for m in RANGE_KEY_RE.finditer(text):                                        # R10, every row
            name = m.group(1) or m.group(2)
            c1, r1, c2, r2 = m.group(3), int(m.group(4)), m.group(5), m.group(6)
            keys.append((num, name, _col_num(c1), r1, _col_num(c2 or c1), int(r2 or r1),
                         f"{name}!{c1}{r1}" + (f":{c2}{r2}" if c2 else "")))
        if weight <= 0:
            continue
        body = _without_cell_refs(text)
        figs[num] = [f for f in _FIGURE_RE.findall(body)                              # R47
                     if "." in f and not _YEAR_RE.match(f.replace(",", ""))
                     and len(f.replace(",", "").split(".")[0]) >= 3]
        if _R57_MEMBER_RE.search(body) and not _R57_UNIVERSAL_RE.search(body):        # R57 named instances
            named.append(num)
        if _R57_UNIVERSAL_RE.search(body) and _R57_DERIV_RE.search(body):            # R57 universals
            universal.append(num)
        # a criterion keyed to a named row is scoped to that row and cannot contradict another
        # row's figure (june-price-review C22/C24: two lines' prices, 6.79 and 19.01, both right)
        if not _R60_KEY_RE.search(body):                                              # R60
            for phrase, fig in _R60_EQUATE_RE.findall(body):
                name = _r59_name(phrase)
                if name:
                    equated.setdefault(name, {}).setdefault(fig.replace(",", ""), []).append(num)
        if _R86_PER_ITEM_RE.search(text) and not re.search(                         # R86
                r"\b(?:reconcil\w+|ties? to|agrees? with|formula|computed)\b", text, re.I):
            per_item.append((num, text))
    # R10: overlapping keys
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            if a[0] == b[0] or a[1] != b[1]:
                continue
            if a[2] <= b[4] and b[2] <= a[4] and a[3] <= b[5] and b[3] <= a[5]:
                emit("ERROR", f"C{a[0]} [R10] answer key {a[6]} overlaps C{b[0]}'s key {b[6]} — "
                             "the platform's near-identical-criteria check reads an overlapping key "
                             "as redundancy by subsumption and FAILs (dillman C31/C49, 2026-08-19); "
                             "give each criterion a key no other criterion covers, or drop the key "
                             "from the liveness criterion and let the answer criterion own the value")
    # R47: a single-figure row subsumed by a stronger one
    for num, fs in figs.items():
        if len(set(fs)) != 1:
            continue
        f = fs[0]
        others = [n for n, ofs in figs.items() if n != num and f in ofs]
        if others:
            emit("ERROR", f"C{num} [R47] states only {f}, which C{others[0]} also states — the "
                         "platform's near-identical-criteria check reads the single-figure row "
                         "as subsumed by the stronger one and FAILs (june-price-review C33/C36, "
                         "2026-08-24). Point this criterion at a fact no other positive scores")
    # R57: a universal derivation over rows other positives name
    for num in universal:
        others = [n for n in named if n != num]
        if not others:
            continue
        emit("ERROR", f"C{num} [R57] asserts a derivation over EVERY row while "
                     f"C{'/C'.join(others[:3])} score named instances of it - the platform's "
                     "near-identical criteria check reads the named rows as subsumed and FAILs "
                     "(open-order-cleanup, 2026-08-25: \"if Criterion 8 genuinely passes, those "
                     "three line-level checks must also pass\"). Narrow the universal to the "
                     "aggregate total and the general method, and leave the named rows as "
                     "independent spot checks")
    # R60: one named quantity, two figures
    for name, fs in equated.items():
        if len(fs) < 2:
            continue
        where = ", ".join(f"C{ns[0]} says {f}" for f, ns in sorted(fs.items()))
        emit("ERROR", f"[R60] \"{name}\" is equated to {len(fs)} different figures "
                     f"({where}) - the Agentic Rubric Quality Review rates the rubric "
                     "needs_improvement on a contradiction like this and says \"both cannot "
                     "be right\" (open-order-cleanup, 2026-08-25: the open commitment at "
                     "84866.21 against 84694.61). If they are two stages of one bridge, name "
                     "the stage each belongs to with the row label the workbook carries")
    # R86: the same attribute asserted per item in two rows on one subject
    for i, (n1, t1) in enumerate(per_item):
        a1 = _r86_present_attrs(t1)
        for n2, t2 in per_item[i + 1:]:
            shared = a1 & _r86_present_attrs(t2)
            if not shared or _r86_subject(t1) != _r86_subject(t2):
                continue
            emit("ERROR", f"C{n1} and C{n2} [R86] both assert the presence of the same attribute per item "
                          f"({', '.join(sorted(shared))}) with no shared figure, which the platform's near "
                          "identical criteria check reads as redundancy by subsumption (dfl-freight-audit "
                          "2026-09-03: a field-list row 'each carrying ... the reason code' subsumed 'one of "
                          "the eight reason codes on each claim'). Score a distinct property of the "
                          "attribute in the second row (a reconciliation to the grouped summary, a rule the "
                          "value follows) or drop it")

    # R124: an exact-count row and a closed-set row on the same tab, the closed row figure-free
    pos = [(num, text) for num, text, weight in rows if weight > 0]
    for i, (n1, t1) in enumerate(pos):
        for n2, t2 in pos[i + 1:]:
            if not (set(_R124_TAB_RE.findall(t1)) & set(_R124_TAB_RE.findall(t2))):
                continue
            if _R124_EXACT_RE.search(t1) and _R124_CLOSED_RE.search(t2):
                exact, closed, ne, nc = t1, t2, n1, n2
            elif _R124_EXACT_RE.search(t2) and _R124_CLOSED_RE.search(t1):
                exact, closed, ne, nc = t2, t1, n2, n1
            else:
                continue
            if set(_R124_FIG_RE.findall(closed)) - set(_R124_FIG_RE.findall(exact)):
                continue
            emit("ERROR", f"C{nc} [R124] closes a set (\"{_R124_CLOSED_RE.search(closed).group(0)}\") that C{ne} already "
                          f"fixes by exact count (\"{_R124_EXACT_RE.search(exact).group(0)}\") on the same tab, and states "
                          "no figure of its own - the platform's near identical criteria check FAILed \"the three "
                          "withdrawn item references and no other item, four lots under each\" as subsumed by "
                          "\"exactly the 12 item and lot combinations\" (recall-response refinement, 2026-09-14). "
                          "Respend the row on a property the exact-count row does not measure (a derived column's "
                          "values, a rule each member follows) or drop it")


# ---- the atomicity family: one scored item, one verdict; six shapes, one walk -----------------
def _r27_figure_count(num, text):
    """A positive criterion asserts at most three separate figures, and three only as steps of one computation.

    Since: 2026-08-21 (task 20, six [major] non_atomic findings).
    Source: the Agentic Rubric Quality Review.
    Drift-notes: item codes, clause numbers, dates and arithmetic-chain steps are not counted; splits stay weight-neutral.
    """
    seen = set()
    for m in _ATOM_FIG_RE.finditer(text):
        tok = m.group(0)
        head, tail = text[:m.start()], text[m.end():]
        if _ATOM_ID_BEFORE_RE.search(head):
            continue                      # an identifier, not a scored figure
        if re.match(r"\s+lines?\s+\d", tail):
            continue                      # "68427 line 1" is an order, not a figure
        if _ATOM_CITE_RE.match(tail):
            continue                      # a figure quoted against its own clause
        if re.match(r"\s*(?:/|\.\d)", tail) or head.endswith("/"):
            continue                      # part of a date or a clause number
        if re.search(r"\d[.,]$", head):
            continue                      # the tail half of 7.1 or of 1,500
        # a hyphenated line or part identifier. The head test reads \w, not \d,
        # because a TAG code suffix is the commonest form of it: rempel-job-buyout
        # (2026-08-25) had R27 counting the 1 of "HB-1" and the 2 of "HGR-2" as
        # scored figures, so six criteria stating two figures were reported as
        # stating three, and the only repair the rule left was renaming the tag out
        # of the criterion - which costs the judge the row key R43 and R50 want.
        if re.search(r"\w-$", head) or re.match(r"-\d", tail):
            continue
        if re.search(r"[=x\u00d7/+*]\s*$", head) or re.match(r"\s*[=x\u00d7/+*]", tail):
            continue                      # a step inside one arithmetic chain, which
                                          # the reviewer reads as a single claim
        seen.add(tok.replace(",", ""))
    if len(seen) >= 4:
        emit("ERROR", f"C{num} [R27] asserts {len(seen)} separate figures "
                      f"({', '.join(sorted(seen)[:5])}) — the Rubric Quality Review "
                      "calls this non_atomic [major]: each one can pass or fail on its "
                      "own, so one scored item carries several verdicts. Split it, and "
                      "split the PARENT'S WEIGHT with it so the positive total does not "
                      "grow (task 20, 50 criteria at an unchanged +98)")
    elif len(seen) == 3:
        emit("ERROR", f"C{num} [R27] asserts 3 separate figures "
                     f"({', '.join(sorted(seen))}) — check each is a step of one "
                     "computation rather than three independently scorable claims, "
                     "which the Rubric Quality Review flags as non_atomic")


def _r49_bundled_subjects(num, text):
    """R49 - a positive criterion carrying two subjects the grader scores separately.
    """
    items = sorted({m.group(0) for m in _R49_ITEM_RE.finditer(text)})
    if len(items) >= 2:
        emit("ERROR", f"C{num} [R49] names {len(items)} item codes ({', '.join(items[:4])}) "
                      "under one predicate — the reviewer reads each as its own verdict "
                      "(yankton-branch-opening, 2026-08-24: \"one could be wrong and two "
                      "right\"). One item per criterion, and split the PARENT'S WEIGHT so "
                      "the positive total does not grow")
    am = _R49_ACCT_RE.search(text)
    if am and len(re.findall(r"\d{4,6}", am.group(1))) >= 2:
        accts = ", ".join(re.findall(r"\d{4,6}", am.group(1)))
        emit("ERROR", f"C{num} [R49] names the accounts {accts} under one predicate — "
                      "each account's history is scored on its own (yankton-branch-opening, "
                      "2026-08-24). One account per criterion, weight split with it")
    cm, mm = _R49_COUNT_RE.search(text), _R49_MONEY_RE.search(text)
    digits = cm.group(1) if cm and cm.group(1).isdigit() else None
    if cm and mm and (digits is None or float(digits)
                      or float(mm.group(1).replace(",", ""))):
        emit("ERROR", f"C{num} [R49] states the count \"{cm.group(0)}\" and the money figure "
                      f"${mm.group(1)} in one criterion — the money is arithmetic off the "
                      "count, so a solver can carry the count and miss the value (the "
                      "reviewer's own example on yankton-branch-opening C32, 2026-08-24). "
                      "Score the count and the value as two criteria")


def _r54_second_turn(num, text):
    """R54 - a positive criterion carrying a second scorable turn.
    """
    hits = [name for name, rx in _R54_SIGNALS if rx.search(text)]
    if hits:
        emit("ERROR", f"C{num} [R54] carries {' and '.join(hits)} — the reviewer scores each "
                      "turn separately and sent yankton-branch-opening back twice on it "
                      "(2026-08-24: \"one could be wrong and two right\"). One sentence, one "
                      "verb, one figure-bearing claim, with acceptance clauses allowed: fold "
                      "the second turn in, or give it a row and split the parent's weight")


def _r55_atomic_sentence(num, text, weight, grader=False):
    """R55 - a criterion that is not one simple atomic sentence.
    """
    t = text.strip()
    positive = weight > 0
    hits = []
    # a colon or semicolon introduces a second claim; house style needs neither
    if re.search(r"[:;]\s", t):
        hits.append("a colon or semicolon introducing a second claim")
    # house style drops the Oxford comma, so ", and" is a coordinated second predicate
    if re.search(r",\s+(?:and|but|while|whereas)\s+", t):
        hits.append("a comma-and coordinating a second predicate")
    sentences = len([m for m in re.findall(r"[.!?](?:\s|$)", t)])
    if sentences > 1 and not grader:
        # a grader-instruction carve-out sentence is R18's finding; counting it again here reported
        # every such row twice (32 of 32 R18 rows on the 2026-09-15 catalog)
        hits.append(f"{sentences} sentences where 1 is the limit (a negative's "
                    "carve-out sentence is banned since 2026-08-26, R18)")
    words = len(t.split())
    cap = _R55_MAX_WORDS[positive]
    if words > cap:
        hits.append(f"{words} words against a {cap}-word cap")
    if hits:
        emit("ERROR", f"C{num} [R55] is not one atomic sentence: {'; '.join(hits)}. A grader "
                      "returns ONE verdict per criterion, so two assertions cannot both be "
                      "scored - one could be wrong and two right (yankton, twice). Fold the "
                      "second turn into a participial or prepositional phrase, or drop it; "
                      "acceptance clauses that narrow the single verdict are fine")


def _r85_stacked_clauses(num, text):
    """R85 (2026-09-03, pick-module-reslot Agentic Rubric Quality Review, needs_improvement:
    'several criteria bundle multiple independently gradeable elements'). R27 counts figures
    and R55 counts sentences, and both passed the rows the review named: a column-wide
    liveness clause with a named example hung off it (', the busiest item FT1319 standing at
    A') and a count with a formula clause AND a per-row attribute clause (', the count a
    formula ..., each move with the bin it comes from'). Two shapes, both mechanical: a
    positive carrying two or more comma-appended absolute clauses, or a liveness clause
    plus an absolute clause that names its own identifier. One absolute clause on a value
    row ('nets $308.25, the cell carrying it a formula rather than a keyed figure') is the
    exemplar shape the review has passed and stays legal.
    """
    clauses = _R85_ABS_RE.findall(text)
    live = LIVENESS_GATED_RE.search(text) or LIVENESS_STRICT_RE.search(text)
    if len(clauses) >= 2:
        emit("ERROR", f"C{num} [R85] stacks {len(clauses)} comma-appended clauses "
                      f"(\"{clauses[0].strip()[:40]}\" ... \"{clauses[-1].strip()[:40]}\") - the "
                      "Agentic Rubric Quality Review read this as bundling independently "
                      "gradeable elements (pick-module-reslot, 2026-09-03). Keep one clause "
                      "and give the other element its own weight-neutral row")
    elif live and any(_R85_ID_RE.search(c) for c in clauses):
        emit("ERROR", f"C{num} [R85] hangs a named example ({_R85_ID_RE.search(' '.join(clauses)).group(0)}) "
                      "off a liveness clause - a column-wide formula demand and one item's value "
                      "are two measurements, and the Agentic Rubric Quality Review split them "
                      "(pick-module-reslot, 2026-09-03). Give the example its own weight-neutral row")


def _r105_ordering_pair(num, text):
    """R105 - a positive ordering claim that puts two determiner-led objects first.
    """
    m = _R105_ORDER_RE.search(text)
    if not m:
        return
    pair = _R105_PAIR_RE.search(m.group("rest"))
    if pair:
        emit("ERROR", f"C{num} [R105] orders two objects at once (\"{m.group(0).strip()[:90]}\"): "
                      "the judge reads 'leads with' against the opening sentence and returns one "
                      "verdict for two things, which flaked 1 in 3 on freight-audit-review. Name "
                      "ONE object and pin its place ('whose first paragraph states ...'), and put "
                      "that object at the head of the golden's opening")


@check(codes=['R27', 'R49', 'R54', 'R55', 'R85', 'R105'], rules=['RUBQ-ATOM'], needs=['rubric'], params=['rows'])
def check_atomicity(rows):
    """A criterion is one simple atomic sentence carrying one scorable claim.

    Codes:
      R27   a positive asserts at most three separate figures, three only as steps of one computation
      R49   a positive names one item code, one account, and never a count beside its money figure
      R54   a positive carries no second scorable turn (a second sentence, a trailing so/including clause, a figured parenthetical, a three-parameter rule, a value beside its own derivation)
      R55   a criterion is one sentence of at most 45 words with no colon, semicolon or comma-and second predicate
      R85   a positive stacks no two comma-appended absolute clauses, and hangs no named example off a liveness clause
      R105  an ordering claim ('leads with', 'opens with') names one object, never two determiner-led objects
    Since: R27 2026-08-21 (task 20); R49 and R54 2026-08-24 (yankton-branch-opening, twice); R55 2026-08-24 (house rule,
    oskaloosa); R85 2026-09-03 (pick-module-reslot); R105 2026-09-11 (freight-audit-review refinement).
    Source: the Agentic Rubric Quality Review (non_atomic) and human reviewers ('one could be wrong and two right').
    Drift-notes: six detectors merged into one walk over the rubric on 2026-09-11; splits stay weight-neutral.
    """
    from .. import core as _core
    g = globals()
    for num, text, weight in rows:
        found = []
        real = g["emit"]
        g["emit"] = lambda level, msg: found.append(msg)
        try:
            _r55_atomic_sentence(num, text, weight, grader=bool(GRADER_INSTRUCTION_RE.search(text)))
            if weight > 0:
                _r27_figure_count(num, text)
                _r49_bundled_subjects(num, text)
                _r54_second_turn(num, text)
                _r85_stacked_clauses(num, text)
                _r105_ordering_pair(num, text)
        finally:
            g["emit"] = real
        if not found:
            continue
        # One criterion, one atomicity finding: R27, R54 and R55 stacked on 62 to 80 percent of the
        # same rows (2026-09-15 catalog). A finding already carried as debt is still recorded on its
        # own code, so debt never shelters a new reason on the same criterion.
        code_of = lambda m: (re.search(r"\[([A-Z]\d+[a-z]?)\]", m) or [None, None])[1]
        debt = [m for m in found if (str(num), code_of(m)) in _core.DEBT]
        live = [m for m in found if m not in debt]
        for m in debt:
            emit("ERROR", m)
        if live:
            head = live[0]
            if len(live) > 1:
                head += " Also on this criterion: " + " | ".join(re.sub(r"^C\d+ ", "", m) for m in live[1:])
            emit("ERROR", head)


# R115 (2026-09-11, packaging-consolidation adjudication note): the prompt's first ask was
# "what we spend now by branch and vendor" and the rubric graded neither a branch-by-vendor table
# nor its total; C6 ("... stay with the branches and are reported by vendor") carried both nouns
# and covered nothing. R92 sees only "batched by" and "grouped by"; the plain "by X and Y" is
# the shape a two-way breakout is asked for in, and each dimension needs its own cue in the
# criterion (by, each, every, per, across) before the row can be said to grade the breakout.
_R115_PAIR_RE = re.compile(r"\bby\s+(?:each\s+)?([a-z]+)\s+and\s+(?:by\s+)?([a-z]+)\b", re.I)


_R115_STOP = {"then", "there", "hand", "now", "way", "itself", "name", "when", "how", "what",
              "which", "who", "them", "that", "this", "the", "one", "two", "three", "four",
              "half", "noon", "end", "default", "law", "mail", "phone", "email", "fax", "card",
              "check", "cash", "far", "large", "small", "hard", "long", "much", "more", "less"}


def _r115_cue(noun):
    stem = re.escape(noun.rstrip("s"))
    return re.compile(rf"\b(?:by|each|every|per|across)\s+(?:of\s+)?(?:the\s+)?(?:\w+\s+)?{stem}", re.I)


@check(codes=['R115'], rules=['PRE-COVER'], needs=['prompt', 'rubric'], params=['rows', 'folder'])
def check_two_way_breakout(rows, folder):
    """A prompt asking for a figure by one dimension and another has a positive criterion carrying a breakdown cue for both dimensions.

    Since: 2026-09-11 (packaging-consolidation adjudication note).
    Source: the adjudicator required a dedicated criterion for 'what we spend now by branch and vendor', which no row graded.
    """
    prompt = Path(folder) / "prompt.md"
    if not prompt.exists():
        return
    for m in _R115_PAIR_RE.finditer(prompt.read_text(encoding="utf-8")):
        a, b = m.group(1).lower(), m.group(2).lower()
        if a in _R115_STOP or b in _R115_STOP or len(a) < 4 or len(b) < 4:
            continue
        ca, cb = _r115_cue(a), _r115_cue(b)
        if any(w > 0 and ca.search(t) and cb.search(t) for _, t, w in rows):
            continue
        emit("ERROR", f'[R115] the prompt asks for a figure "{m.group(0)}" and no positive criterion '
                      f"carries a breakdown cue (by, each, every, per) for both {a} and {b}: the "
                      "adjudicator sent packaging-consolidation back on exactly this (2026-09-11, "
                      "'what we spend now by branch and vendor' graded by no row). Add one criterion "
                      "for the two-way table, anchored on its total")


# R116 (2026-09-11, harlow-route-rebalancing-proposal refinement round 3, the platform's Rubric
# near identical criteria check): C14 "lists all 10 accounts whose Q3 visits fell short" and C16
# "the shortfall list carries all 10 accounts in descending annual revenue, Brackenfell HVAC at
# 47,500 last" were ruled redundant by subsumption, "passing Criterion 16 necessarily passes
# Criterion 14". R47 keys on a shared figure and R86 on a shared attribute per item; neither saw
# a completeness phrase ("all N <noun>") restated inside a second positive that adds an ordering
# or a named member. The second row must assess its own point only.
_R116_ALL_RE = re.compile(r"\ball (\d+) (?!of\b)([a-z]+)\b", re.I)


_R126_AGG_RE = re.compile(r"^=(?:SUM|COUNT|COUNTA|COUNTIF|COUNTIFS|SUMIF|SUMIFS|SUMPRODUCT)\(", re.I)
_R126_GENERIC = {"the", "and", "onto", "with", "their", "for", "from", "into", "each",
                 "cell", "column", "row", "sheet", "tab", "page", "total", "count"}


def _r126_lemmas(text):
    return {w.rstrip("s") for w in re.findall(r"[a-z][a-z'-]+", text.lower())
            if len(w) > 2 and w not in _R126_GENERIC}


def _r126_share(a, b):
    return {x for x in a if any(x.startswith(y) or y.startswith(x) for y in b)}


@check(codes=['R126'], rules=['PRE-COVER'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_output_totals_have_positives(rows, folder):
    """Every golden aggregation total's labelled output is graded by at least one positive criterion, never by a negative alone.

    Since: 2026-09-14 (tessendorf-channel-split adjudication).
    Source: the adjudicator's rubric coverage axis - the spring-return valuation, implemented
    on the Off Site sheet with a SUM footer, was "graded only by the negative criterion", so an
    omission cost no positive points; the positive row had been cut on 2026-08-31 to fund the
    refresh-chain criteria, which is the exact trade this check now refuses.
    Drift-notes: a footer is covered when a positive shares two label lemmas (prefix-matched),
    or one lemma plus the footer's cached value as a figure; the unit is the SHEET - it fires
    only when none of a sheet's labelled totals is covered, because task 23's Summary tab
    carries deliberately ungraded per-cause subtotals beside its graded grand totals (interior
    subtotals are spot-check territory; a sheet with no graded total is an ungraded output).
    Probed 2026-09-14: fires on this task pre-fix, silent post-fix and on the task 23 exemplar.
    """
    try:
        import openpyxl
    except ImportError:
        return
    from ..common import solution_files
    pos_rows = [(num, _r126_lemmas(text), text) for num, text, weight in rows if weight > 0]
    for path in solution_files(folder, {".xlsx"}):
        try:
            wf = openpyxl.load_workbook(path, data_only=False)
            wv = openpyxl.load_workbook(path, data_only=True)
        except Exception:
            continue
        for ws in wf.worksheets:
            vs = wv[ws.title]
            footers = []
            for row in ws.iter_rows():
                agg = [c for c in row if isinstance(c.value, str) and _R126_AGG_RE.match(c.value)]
                if not agg:
                    continue
                labels = [c.value for c in row if isinstance(c.value, str) and not c.value.startswith("=")]
                if not labels:
                    continue
                lab = _r126_lemmas(labels[0])
                if len(lab) < 2:
                    continue
                cached = {str(vs[c.coordinate].value) for c in agg if vs[c.coordinate].value is not None}
                covered = any(
                    len(_r126_share(lab, plem)) >= 2
                    or (_r126_share(lab, plem) and any(re.search(rf"\b{re.escape(v)}\b", ptext) for v in cached))
                    for _, plem, ptext in pos_rows)
                footers.append((agg[0].coordinate, labels[0], covered))
            if footers and not any(c for _, _, c in footers):
                coord, label, _ = footers[0]
                emit("ERROR", f"[R126] {path.name} {ws.title}!{coord} totals a labelled output "
                              f"(\"{label}\") and none of the sheet's totals is graded by a positive "
                              "criterion - the adjudicator failed tessendorf on the spring-return "
                              "valuation being \"graded only by the negative criterion\", an omission "
                              "costing no positive points (2026-09-14). Give the output a positive row, "
                              "funded from a spot check its sweeps already cover, and never cut an "
                              "output's only positive to pay for a restructure")


@check(codes=['R116'], rules=['PRE-DUP'], needs=['rubric'], params=['rows'])
def check_repeated_completeness_phrase(rows):
    """Two positives never both carry the same "all N <noun>" completeness phrase; the second states its own point without restating the count.

    Since: 2026-09-11 (harlow-route-rebalancing-proposal refinement round 3).
    Source: the platform's Rubric near identical criteria check (redundant by subsumption).
    Drift-notes: the noun after the count must be a word other than "of"; the portfolio probe found no
    passing rubric carrying the phrase twice.
    """
    seen = {}
    for num, text, weight in rows:
        if weight <= 0:
            continue
        for n, noun in _R116_ALL_RE.findall(text):
            seen.setdefault((n, noun.lower()), []).append(num)
    for (n, noun), nums in seen.items():
        if len(nums) > 1:
            emit("ERROR", f"C{' and C'.join(str(x) for x in nums)} [R116] both carry the completeness phrase "
                         f"\"all {n} {noun}\"; the platform's near-identical check reads the second as subsuming the "
                         "first (harlow-route-rebalancing-proposal 2026-09-11, C14 and C16). Keep the count on one "
                         "row and let the other assess its own point, the ordering or the named member")


# R119 (2026-09-11, packaging-consolidation "rubric does not verify computed values", BLOCKING):
# "The branches tab shows the spend staying with the branches and the unmatched spend for each
# branch" rewarded a computed money figure for being present. The platform wants the expected value
# or a concrete correctness check (a reconciliation to source rows) in the row. Presence verbs over a
# computed money or quantity noun with neither a digit nor a check word are the signature; list
# rows ("lists the items") are out of scope because an enumeration is not a computed value.
_R119_PRESENCE_RE = re.compile(
    r"^(?:The\s+)?[\w' ]+?\b(?:tab|sheet|page|table|workbook)\b.{0,40}?\b(?:shows|states|gives|reports|presents|carries)\b", re.I)


_R119_COMPUTED_RE = re.compile(r"\b(?:spend|cost|total|amount|saving|charge|balance|variance)\b", re.I)


_R119_CHECK_RE = re.compile(r"\d|\bties\b|\breconcil|\bmatch|\bequals?\b|\bsums? to\b", re.I)


@check(codes=['R119'], rules=['PRE-OBJ'], needs=['rubric'], params=['rows'])
def check_presence_only_computed(rows):
    """A positive row over a computed money or quantity figure names the expected value or a concrete correctness check, never presence alone.

    Since: 2026-09-11 (packaging-consolidation, the platform's 'rubric does not verify computed values' BLOCKING finding).
    Source: 'rewards a computed value for being present but does not name the expected value or require a correctness check'.
    """
    for num, text, weight in rows:
        if weight <= 0 or LIVENESS_STRICT_RE.search(text):
            continue
        if _R119_PRESENCE_RE.search(text) and _R119_COMPUTED_RE.search(text) and not _R119_CHECK_RE.search(text):
            emit("ERROR", f"C{num} [R119] rewards a computed figure for being present with no expected value and "
                          "no correctness check: the platform's computed-values check BLOCKED "
                          "packaging-consolidation on exactly this row shape (2026-09-11). Name the total the "
                          "figures reach or the source rows they reconcile to")


# R121 (2026-09-12, harlow-route-rebalancing-proposal refinement round 6, Rubric Quality Review
# [major] misaligned_or_unjustified_rigidity): C19 "names one account to move together with its
# losing route and its receiving route, Castor Valley Supply from North to West being one
# acceptable answer" was read as awarding its 5 points ONLY for Castor Valley, the "one
# acceptable answer" hedge notwithstanding; the review wanted the structural test alone, with
# validity left to the sibling rows. A named answer inside a positive is the answer key to the
# review whatever softener surrounds it. Negatives are exempt: an anchor on a class the golden
# lacks is what R77 asks of them. The portfolio probe (18 CSVs plus the accepted zips) found the
# phrase on no other rubric; "such as" and "among them" are worked-example shapes on accepted
# rows and stay legal.
_R121_EXAMPLE_RE = re.compile(
    r"\b(?:one|an|the|another)\s+acceptable\s+answers?\b|\bacceptable answers?\b"
    r"|\bfor (?:example|instance)\b|\be\.g\.", re.I)


@check(codes=['R121'], rules=['RUBQ-RIGID'], needs=['rubric'], params=['rows'])
def check_named_acceptable_answer(rows):
    """A positive never presents a named answer as "one acceptable answer" or "for example"; the Rubric Quality Review reads the named answer as the row's key and every valid alternative as failing it.

    Since: 2026-09-12 (harlow-route-rebalancing-proposal refinement round 6).
    Source: the Rubric Quality Review (misaligned_or_unjustified_rigidity, major).
    Drift-notes: positives only; "such as" and "among them" are accepted worked-example shapes (kolterman,
    parts-quotation) and are not matched.
    """
    for num, text, weight in rows:
        if weight <= 0:
            continue
        m = _R121_EXAMPLE_RE.search(text)
        if m:
            emit("ERROR", f"C{num} [R121] presents a named answer as \"{m.group(0)}\"; the Rubric Quality "
                          "Review reads the named answer as the row's key and scores every instruction-faithful "
                          "alternative as failing it (harlow-route-rebalancing-proposal 2026-09-12, C19 at +5). "
                          "State the structural test the row scores (what is named, what it is checked against) "
                          "and leave validity to the sibling rows")


# R122 (2026-09-12, freight-audit-review refinement, adjudication note): C44 "Holds the bid
# behind the decision on the September release rule rather than cancelling it" was read as
# mandating one business choice where the prompt ("If the evidence points somewhere I have not
# thought of, write that instead") invites any evidence-led conclusion, so a defensible answer
# that proceeds with the bid on the unchanged rate table while flagging the profile change
# would lose the row. The shape is a disposition verb at the head of a positive plus a named
# alternative ("rather than cancelling", "instead of proceeding"). Facts contrasted against a
# wrong explanation ("attributes X to Y rather than to Z", C4) carry no disposition verb and
# stay legal. Probed 2026-09-12 across submissions/, drafts/ and refinements/: fires on the
# pre-fix C44 only.
_R122_VERB_RE = re.compile(
    r"^(?:the\s+\w+\s+(?:\w+\s+)?)?"
    r"(?:holds?|defers?|postpones?|cancels?|proceeds? with|keeps?|drops?|approves?|rejects?|delays?"
    r"|halts?|suspends?|shelves?|abandons?|continues?"
    r"|recommends? (?:holding|deferring|postponing|cancell?ing|proceeding|dropping|delaying|halting"
    r"|suspending|shelving|abandoning|continuing|keeping))\b", re.I)
_R122_ALT_RE = re.compile(
    r"\b(?:rather than|instead of|not|never) (?:cancel|proceed|defer|postpon|drop|abandon|approv|reject"
    r"|delay|hold|halt|suspend|scrap|shelv|continu|keep|wait)\w*\b", re.I)


@check(codes=['R122'], rules=['RUBQ-RIGID'], needs=['rubric'], params=['rows'])
def check_mandated_disposition(rows):
    """A positive never scores one business disposition against a named alternative; it scores that a disposition is stated and the finding it rests on, and leaves the choice to the solver.

    Since: 2026-09-12 (freight-audit-review refinement, adjudication note on C44).
    Source: adjudication (over-constrained rubric: 'mandates one business choice where the prompt invites any
    evidence-led conclusion').
    Drift-notes: positives only; needs a disposition verb at the head of the row AND a 'rather than' or
    'instead of' alternative naming a decision verb, so fact-versus-wrong-explanation contrasts (C4) do not match.
    """
    for num, text, weight in rows:
        if weight <= 0:
            continue
        if _R122_VERB_RE.search(text.strip()) and _R122_ALT_RE.search(text):
            alt = _R122_ALT_RE.search(text).group(0)
            emit("ERROR", f"C{num} [R122] scores one business disposition against its alternative (\"{alt}\"): "
                          "the freight-audit-review adjudicator (2026-09-12) read the row as penalizing a "
                          "defensible answer the prompt invites, since the prompt asks for whatever the "
                          "evidence shows. Score that a disposition is stated and the finding it rests on, "
                          "and leave the choice to the solver")


CLOSING_STYLE_RE = re.compile(r"overall\b[^.]{0,40}\b(?:formatting|style)\b", re.I)


@check(codes=['R135'], rules=['PRE-FORM'], needs=['rubric'], params=['rows'])
def check_closing_style_criterion(rows):
    """The rubric's LAST criterion is the general "Overall formatting and style of the deliverable" line.

    Source: docs/submission/platform/platform-submission-form.md section 4 ("End with a
    general 'Overall formatting and style of the deliverable' line (commonly ~+5)") and
    checklist item 12, which is one of the fifteen boxes that must be ticked to submit.
    Since: 2026-09-21 (the Hazy port; docs/RULE-DELTAS.md D5). Geranium had no such rule.
    """
    if not rows:
        return
    hits = [num for num, text, _ in rows if CLOSING_STYLE_RE.search(text or "")]
    last_num = rows[-1][0]
    if not hits:
        emit("ERROR", "[R135] no closing criterion for overall formatting and style - the "
                      "form requires the rubric to end with a general \"Overall formatting "
                      "and style of the deliverable\" line (commonly ~+5), and checklist "
                      "item 12 is a submit-blocking confirmation that it is there")
    elif last_num not in hits:
        emit("ERROR", f"[R135] the formatting-and-style criterion is C{hits[0]}, not the last "
                      f"row (C{last_num}) - the form says the rubric ENDS with it")


HEDGED_FIGURE_RE = re.compile(
    r"\b(?:approximately|roughly|about|around|circa|approx\.?|some)\s*[~]?\s*"
    r"[\$\u20ac\u00a3]?\d|~\s*[\$\u20ac\u00a3]?\d", re.I)


@check(codes=['R136'], rules=['PRE-FORM'], needs=['rubric'], params=['rows'])
def check_hedged_figures(rows):
    """No criterion asserts a hedged figure; every value is pulled exactly from the ground truth.

    Source: docs/submission/platform/platform-submission-form.md section 4 - "Pull every
    exact value straight from your own reference files and ground-truth answer, never
    estimate what a criterion should check", with its own worked pair (bad "approximately
    $15,000", good "$15,170").
    Since: 2026-09-21 (the Hazy port; docs/RULE-DELTAS.md D6).
    """
    for num, text, _ in rows:
        m = HEDGED_FIGURE_RE.search(text or "")
        if m:
            emit("ERROR", f"C{num} [R136] hedges a figure (\"{m.group(0).strip()}\") - the form "
                          "requires the exact value from the ground truth, not an estimate. "
                          "A judge cannot grade \"approximately\"")
