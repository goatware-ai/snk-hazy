"""Group 2: negative-criterion polarity, scope and wording (GOLD-NEG, PRE-POL, PRE-SCOPE, REV-REGISTER).

Generated 2026-09-04 from autoeval_check.py; every check body is verbatim.
"""
import re
from ..common import _without_cell_refs, workbook
from ..core import check, emit, recommend, REPORT, OPTIONS


# R69 second wave (2026-08-31, a pre-submission check): a rubric whose
# deliverable is a memo writes every criterion as "The memo <verb>s ...", so the passive
# subject-verb signature both checks read never appears. _R70_WRAPPER_RE strips that
# wrapper, and R70_CONCLUSION_VERBS is the set of verbs that make the criterion an
# ANALYTICAL CONCLUSION rather than a reported fact or a prohibited act.
_R70_WRAPPER_RE = re.compile(
    r"^\s*(?:the|a|an)\s+(?P<subj>[\w'\-]+(?:\s+[\w'\-]+){0,2}?)\s+(?P<verb>[a-z]+s)\b"
    r"(?:\s+that)?", re.I)


R70_CONCLUSION_VERBS = {
    "concludes", "finds", "determines", "decides", "attributes", "blames", "identifies",
    "judges", "asserts", "claims", "argues", "reasons", "infers",
}


_R70_STOP = {
    "the", "that", "this", "and", "for", "with", "from", "into", "than", "then", "when",
    "which", "while", "have", "has", "had", "been", "being", "are", "was", "were", "not",
    "its", "their", "them", "they", "it", "on", "in", "of", "to", "as", "at", "by", "or",
    "an", "a", "is", "still", "also", "any", "each", "every", "one", "two", "memo",
    "report", "workbook", "deliverable", "analysis", "summary", "page", "tab", "sheet",
    "contrary", "unsupported", "incorrectly", "wrongly", "instead", "rather", "over",
    "under", "against", "about", "because", "does", "own",
}


def _r70_wrapper(text):
    """("memo", "concludes", "rest of the criterion") for "The memo concludes that ..."."""
    m = _R70_WRAPPER_RE.match(text)
    if not m:
        return None
    return m.group("subj").split()[-1].lower(), m.group("verb").lower(), text[m.end():]


def _r70_lemmas(text):
    out = set()
    for w in re.findall(r"[a-z]{4,}", text.lower()):
        if w in _R70_STOP:
            continue
        for suf in ("ing", "ed", "es", "s"):
            if w.endswith(suf) and len(w) - len(suf) >= 3:
                w = w[: -len(suf)]
                break
        if len(w) > 3 and w.endswith("e"):
            w = w[:-1]
        out.add(w)
    return out


_R69_SV_RE = re.compile(
    r"^\s*(?:at least one|the|a|an)\s+(?P<subj>[\w'\-]+(?:\s+[\w'\-]+){0,4}?)\s+(?:is|are)\s+"
    r"(?:(?:incorrectly|wrongly|still|also|then)\s+)?(?P<verb>[a-z]+)", re.I)


# R77 (2026-08-31, an oracle run, golden check 0.9444 / 1.0 / 1.0): an
# OPEN-SCOPE fabrication negative. "The workup cites a reference figure, bank balance or
# ledger entry beyond what the reference replies and the account register document" fired
# 1/3 ON THE GOLDEN, the judge quoting the NSF sentence (check 4415 returned November 17,
# made good by cashier's check November 24 with the bank charge) that the register carries
# verbatim as 11/17/25 rtn / 11/17/25 svc / 11/24/25 cc 118220. The frame is legal
# fabrication, but its object is a whole CLASS of figures: the judge has to
# confirm every such figure in the deliverable against the named sources, and one it fails
# to match (a CSV date written 11/24/25, a derived deadline, a monthly average the source
# does not literally carry) reads as cited beyond the record. It is R47's universal-sweep
# surface on the penalty side, and it flakes the same way. A fabrication negative needs a
# CLOSED class of invented content the golden plainly lacks (a credit bureau report, a
# section number the policy has no heading for), never "any figure of kind X".
_R77_FRAME_RE = re.compile(
    r"\bbeyond what\b|\b(?:do|does) not (?:support|document|show|carry)\b", re.I)


_R77_OBJECT_RE = re.compile(
    r"\b(?:figure|balance|entry|entries|amount|total|date|deadline|window|time|clock|limit"
    r"|tolerance|period|average|rate|count|quantity|quantities|days|hours|percent(?:age)?"
    r"|price|cost|value)s?\b", re.I)


@check(codes=['R77'], rules=['GOLD-NEG'], needs=['rubric'], params=['rows'])
def check_open_scope_fabrication(rows):
    """A fabrication negative names a closed class of invented content, never an open class of figures the judge must confirm one by one.

    Since: 2026-08-31 (an oracle run, 1/3 on the golden).
    Source: the oracle.
    """
    for num, text, weight in rows:
        if weight >= 0:
            continue
        frame = _R77_FRAME_RE.search(text)
        if not frame:
            continue
        # the object is what the deliverable is said to cite or state, ahead of the frame
        obj = _R77_OBJECT_RE.search(text[:frame.start()])
        if obj:
            emit("ERROR", f"C{num} [R77] open-scope fabrication negative: its object is a class of "
                          f"figures ({obj.group(0)}) and its frame (\"{frame.group(0)}\") sends the judge "
                          "to confirm EVERY such figure in the deliverable against the sources; one it "
                          "cannot match (a CSV date, a derived deadline, a computed average) reads as "
                          "cited beyond the record and the negative fires on the golden "
                          "(2026-08-31, 1/3 on an NSF entry the register carries as 11/24/25). Narrow it "
                          "to a CLOSED class of invented content the golden plainly lacks ('cites a "
                          "credit bureau report or score, with no such report in the file'; 'cites a "
                          "policy section number with no such section in the policy')")


_R84_TRAILING_RE = re.compile(
    r",\s*(?:in violation of|violating|contrary to|against (?:the|its|their|rule|policy|section|"
    r"paragraph)|in breach of|in conflict with|contradicting)\b[^.]*\.?\s*$", re.I)


@check(codes=['R84'], rules=['REV-REGISTER'], needs=['rubric'], params=['rows'])
def check_negative_trailing_clause(rows):
    """A negative states its prohibited act once with the frame inside the sentence, never ending on a trailing rule-breach clause such as 'in violation of' or 'contrary to'.

    R84 (2026-09-02, a gate-2 reviewer): 'Remove trailing clauses
    that bring negatively weighted items into negative language such as "in violation
    of..." or "contrary to...."'. A negative should state the prohibited act once; a comma
    clause at the end that restates it as a rule breach is the author arguing the case, and
    the judge then has a second claim to confirm. E1/W18 accept those words as polarity
    frames, which is how the tails got there. Put the frame inside the sentence as the
    act's condition instead: 'booked for a slot although its deal sheet documents no
    flyer support' passes E1, W18 and the reviewer together."""
    for num, t, w in rows:
        if w >= 0:
            continue
        m = _R84_TRAILING_RE.search(t.strip())
        if m:
            emit("ERROR", f'C{num} [R84] negative ends in a trailing rule-breach clause "{m.group(0).strip()[:50]}" '
                          "- a gate-2 reviewer (2026-09-02) sent the rubric back on "
                          "exactly this shape ('remove trailing clauses ... such as in violation of / contrary "
                          "to'). State the act once and carry the polarity frame inside the sentence as its "
                          "condition ('... although <source> documents no <thing>'), which E1 and W18 "
                          "all accept")


# R111 (2026-09-11, Rubric Quality Review rated needs_improvement): "Bracket money is
# incorrectly booked for a vendor on an invented bracket, although the March letter grants
# the one percent to one vendor alone" and "Plan
# freight is incorrectly priced at an invented rate, although no vendor's printed terms carry
# it" were both read as INVERTED POLARITY at critical ("the sentence describes what a correct
# deliverable does ... a fully compliant deliverable satisfies this sentence and loses 4
# points"). The same review had called the earlier passive form of the same two rows
# ("Bracket money is booked for a vendor whose printed terms document no bracket, in violation
# of the March letter ...") inverted as a minor on 2026-08-31, so the frame word (in violation
# of / although) is not what the review reads: it is the PASSIVE opening that puts the wronged
# object in the subject slot and lets the sentence parse as a state the workbook is in. Both of
# the platform's suggested rewrites put the deliverable in the actor's seat with a transitive
# verb ("Books bracket money for a vendor other than the named one, inventing a bracket ...";
# "Prices plan freight at a rate not found on any vendor's printed terms sheet"). The fix that
# passed the gate: "The workbook wrongly books bracket money for ..., inventing a bracket
# where ...". Narrowed to the adverb-carrying passive ("X is incorrectly <participle>") so the
# verdict-cell shape "the standing column is marked for billing" (rubric-negatives memory,
# accepted) stays clear; probed 2026-09-11 over 28 rubrics and 67 negatives: 4 hits in 3
# other rubrics, all this shape, none yet judged by the review.
_R111_PASSIVE_RE = re.compile(
    # NOT widened to adverb-less passives (probed 2026-09-14 on a penalty scope FAIL):
    # dropping the adverb fired on 27 negatives across the portfolio,
    # most of them the proven "At least one line is bought ..." any-quantifier shape. That
    # day's ruling was about the fabrication class.
    r"^\s*(?:the |a |an )?[\w'.,/ -]{2,70}?\s+(?:is|are)\s+(?:incorrectly|wrongly)\s+"
    r"(?:\w+ed|\w+en|built|kept|sent|put|set|held|bought|sold|paid|split|cut|met|spent|left|"
    r"lost|made|shown|taken|given|written|drawn|found)\b", re.I)


@check(codes=['R111'], rules=['GOLD-NEG'], needs=['rubric'], params=['rows'])
def check_negative_passive_opening(rows):
    """A negative names the deliverable as the actor of the defect; a passive opening ("<object> is incorrectly <done>") reads to the Rubric Quality Review as a description of a correct deliverable and is failed as inverted polarity.

    Since: 2026-09-11
    Source: the Rubric Quality Review (two critical misaligned_or_unjustified_rigidity
    findings on C25 and C26, both passive); the same review read the earlier passive form of
    the same rows as inverted on 2026-08-31.
    Drift-notes: narrowed to the adverb-carrying passive so the accepted verdict-cell shape
    ("the standing column is marked for billing") and bare passives stay clear; widen only
    on a second platform reading."""
    for num, t, w in rows:
        if w >= 0:
            continue
        m = _R111_PASSIVE_RE.search(t)
        if m:
            emit("ERROR", f'C{num} [R111] negative opens in the passive voice ("{m.group(0).strip()[:60]}") '
                          "- the Rubric Quality Review read exactly this shape as INVERTED polarity twice on "
                          "one package (minor 2026-08-31, critical 2026-09-11): with the wronged "
                          "object in the subject slot the sentence parses as a state a correct deliverable is "
                          "in. Put the deliverable in the actor's seat with a transitive verb and keep the "
                          "a fabrication token inside the act ('The workbook wrongly books bracket money for a vendor "
                          "other than the named one, inventing a bracket where ...')")


# R28 (2026-08-21, an oracle run): C41 asked for fill "measured on the quantity
# ordered rather than on the quantity acknowledged" and flaked 1/3 with the judge quoting
# the golden's own "measures fill against the quantity they acknowledge rather than the
# quantity we ordered" as its evidence. The deliverable was describing the term as it
# stands and the criterion was stating the change asked for: the same two nouns in the
# opposite order, which reads to the judge as a contradiction. It costs nothing to say
# both in the deliverable, so say both.
_STOP = {"the", "a", "an", "of", "on", "in", "to", "is", "are", "be", "it", "we", "they",
         "that", "this", "our", "their", "its", "and", "or", "at", "as", "by", "for",
         "with", "was", "were", "not", "from", "than", "rather", "shall", "should"}


def _content(words):
    """the words that carry the meaning, stemmed enough to match across inflections."""
    out = set()
    for w in re.findall(r"[a-z]+", words.lower()):
        if w in _STOP or len(w) < 4:
            continue
        for suffix in ("ing", "ed", "es", "s", "d"):
            if w.endswith(suffix) and len(w) - len(suffix) >= 4:
                w = w[: -len(suffix)]
                break
        if w.endswith("e") and len(w) > 4:     # acknowledge / acknowledged -> acknowledg
            w = w[:-1]
        out.add(w)
    return out


def _rather_pairs(text):
    """(before, after) content-word sets around each 'rather than' in a string."""
    for m in re.finditer(r"\brather than\b", text, re.I):
        before = " ".join(text[: m.start()].split()[-7:])
        after = " ".join(text[m.end():].split()[:7])
        b, a = _content(before), _content(after)
        if b and a and b != a:
            yield b, a


@check(codes=['R28'], rules=['GOLD-NEG'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_inverted_pairs(rows, folder):
    """A criterion's 'X rather than Y' pair is stated in the order the deliverable states it.

    Since: 2026-08-21 (an oracle run, C41 flaked 1/3).
    Source: the oracle, quoting the golden's reversed sentence as the contradiction.
    """
    strings = []
    d = folder / "solution"
    for path in sorted(d.glob("*.xlsx")) if d.is_dir() else []:
        try:
            wb = workbook(path, data_only=True)
        except Exception:
            continue
        for ws in wb.worksheets:
            for row in ws.iter_rows():
                for c in row:
                    if isinstance(c.value, str) and "rather than" in c.value.lower():
                        strings.append((ws.title, c.coordinate, c.value))
    if not strings:
        return
    for num, text, weight in rows:
        if weight <= 0:
            continue
        for cb, ca in _rather_pairs(text):
            for title, ref, val in strings:
                for sb, sa in _rather_pairs(val):
                    # compare on the words that DISTINGUISH the two halves; the shared
                    # ones ("quantity" on both sides of both phrases) carry no signal
                    cb2, ca2 = cb - ca, ca - cb
                    sb2, sa2 = sb - sa, sa - sb
                    # the deliverable puts the criterion's two halves the other way round
                    if ca2 & sb2 and cb2 & sa2:
                        emit("ERROR", f"C{num} [R28] states one order of a pair that "
                                     f"{title}!{ref} states the other way round — the judge "
                                     "quotes that cell back as the contradiction (one criterion "
                                     "flaked 1/3 on fill measured on the quantity ordered "
                                     "against a briefing that described the term as it stands). "
                                     "Have the deliverable say both, the term as written and "
                                     "the change asked for, in the criterion's own order")
                        return


# R33 (2026-08-22, an oracle run): a positive criterion asserting a property
# "throughout the workbook" that the golden itself falsifies somewhere. C44 read
# "Throughout the workbook, ordered quantities are whole units, no quantity is
# negative ..." and failed 3 of 3 oracle runs on 'Base Recap'!E12 = -17, which is a
# correct figure: that tab nets returns against shipments and February 2026 on the
# Reading account ran negative. The judge scans every tab, so an unscoped universal
# is only as true as the least convenient cell in the file. Scope the claim to the
# columns it is actually about, or drop it.
_UNIVERSAL_SCOPE_RE = re.compile(
    r"\bthroughout the workbook\b|\banywhere in the workbook\b|\bacross the workbook\b"
    r"|\bno quantity (?:is|may be)\b|\bno figure (?:is|may be)\b|\bno value (?:is|may be)\b"
    r"|\bevery (?:quantity|figure|number) in the workbook\b", re.I)


_CLAIM_NONNEG_RE = re.compile(r"\b(?:no|none|never|not)\b[^.;]{0,40}\bnegative\b", re.I)


_CLAIM_WHOLE_RE = re.compile(r"\b(?:whole units?|whole numbers?|integers?)\b", re.I)


@check(codes=['R33'], rules=['GOLD-NEG'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_universal_claims(rows, folder):
    """A workbook-wide property claim has no counterexample anywhere in the golden."""
    d = folder / "solution"
    if not d.is_dir():
        return
    negs, fracs = [], []
    for path in sorted(d.glob("*.xlsx")):
        try:
            wb = workbook(path, data_only=True)
        except Exception:
            continue
        for ws in wb.worksheets:
            for row in ws.iter_rows():
                for c in row:
                    v = c.value
                    if not isinstance(v, (int, float)) or isinstance(v, bool):
                        continue
                    if v < 0:
                        negs.append(f"'{ws.title}'!{c.coordinate} = {v:g}")
                    elif isinstance(v, float) and v != int(v) and abs(v) > 1:
                        fracs.append(f"'{ws.title}'!{c.coordinate} = {v:g}")
    for num, text, weight in rows:
        if weight <= 0 or not _UNIVERSAL_SCOPE_RE.search(text):
            continue
        if _CLAIM_NONNEG_RE.search(text) and negs:
            emit("ERROR", f"C{num} [R33] claims no negative value workbook-wide, but the golden "
                          f"carries {len(negs)} ({', '.join(negs[:3])}) — the judge scans every tab, "
                          "so an unscoped universal is only as true as the least convenient cell "
                          "(a criterion failed 3/3 oracle runs on a correct net-of-returns "
                          "figure, 2026-08-22). Scope the claim to the columns it is about")
        if _CLAIM_WHOLE_RE.search(text) and fracs:
            emit("ERROR", f"C{num} [R33] claims whole-unit quantities workbook-wide, but the golden "
                          f"carries fractional values ({', '.join(fracs[:3])}) — scope the claim to "
                          "the quantity columns it is about, not the whole file")


# R34 (2026-08-23, an oracle run): a positive criterion that states a RULE
# over an UNNAMED member of a class leaves the judge to choose its own rows, and it
# chooses badly. "Two order lines the file shows as still due are closed because the
# register shows the goods already received in full" failed 2 of 3 runs with the judge
# quoting the two SHORT CLOSE rows, a different rule on the same disposition. "An order
# more than ninety days old with nothing received is kept where the supplier has
# confirmed a ship date on or before September 11" failed 1 of 3, because the golden
# also cancels an order that IS confirmed to ship inside the window, for a discontinued
# item, so the rule reads false as a universal. Both were rescued by naming the order or
# the line the golden means. Fires on an indefinite or bare-count subject carrying a
# causal clause and no identifier anchor; a definite subject ("Order 44088 ...", "The
# Galesburg aquastat line ...") is exactly the fix and does not fire.
_RULE_SUBJ_RE = re.compile(
    r"^\s*(?:An?|One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten|Eleven|Twelve|Several)\s+"
    r"(?!of\b)[a-z]")


_RULE_CAUSE_RE = re.compile(r"\b(?:because|where|since|whenever|wherever|as long as|so long as)\b", re.I)


_RULE_ANCHOR_RE = re.compile(r"\b\d{4,}\b|\$\s?\d|\b[A-Z]{2,}[0-9][\w-]*\b")


@check(codes=['R34'], rules=['GOLD-NEG'], needs=['rubric'], params=['rows'])
def check_rule_anchors(rows):
    """A rule stated over a class names a member the judge can land on."""
    for num, text, weight in rows:
        if weight <= 0 or not _RULE_SUBJ_RE.match(text):
            continue
        if not _RULE_CAUSE_RE.search(text):
            continue
        if _RULE_ANCHOR_RE.search(_without_cell_refs(text)):
            continue
        emit("ERROR", f"C{num} [R34] states a rule over an unnamed member of a class with a "
                     "causal clause and no identifier to land on — the judge picks its own "
                     "rows and lands on a sibling the rule does not cover (an oracle run: "
                     "the received-in-full claim failed 2/3 on the short-close rows, "
                     "the aged-order claim 1/3 on an order cancelled for a different reason). "
                     "Name the order, line or row the golden means")


# R37 (2026-08-23, an oracle run): a NEGATIVE criterion carrying a THRESHOLD
# fires on the golden as soon as one cell crosses that threshold, whatever the causal
# clause says. C37 read "left with open quantity still due that puts its position beyond
# thirteen weeks of supply" and the judge landed on the one Position row standing at 14.4
# weeks, a deadstock item whose whole open order the golden CANCELS: open planned is zero
# there, so the clause that was meant to exclude it never got read. This is R33's shape on
# the negative side, and the negative costs its full weight when it fires. Key a negative
# on a two-column comparison the judge reads off one row (open planned against open
# allowed), never on a threshold it has to reason about.
_NEG_THRESH_RE = re.compile(
    r"\b(?:beyond|above|over|more than|past|under|below|less than)\s+"
    r"(\d+(?:\.\d+)?|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
    r"thirteen|fourteen|fifteen|twenty|thirty|sixty|ninety)\s+"
    r"(weeks?|days?|months?|percent|units?)\b", re.I)


_WORD_NUM = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
             "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
             "fourteen": 14, "fifteen": 15, "twenty": 20, "thirty": 30, "sixty": 60,
             "ninety": 90}


@check(codes=['R37'], rules=['GOLD-NEG'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_negative_thresholds(rows, folder):
    """A threshold negative has no golden cell already across its line."""
    d = folder / "solution"
    if not d.is_dir():
        return
    sheets = []
    for path in sorted(d.glob("*.xlsx")):
        try:
            sheets.extend(workbook(path, data_only=True).worksheets)
        except Exception:
            continue
    for num, text, weight in rows:
        if weight >= 0:
            continue
        m = _NEG_THRESH_RE.search(text)
        if not m:
            continue
        raw, unit = m.group(1).lower(), m.group(2).lower().rstrip("s")
        limit = _WORD_NUM.get(raw, None) if not raw[0].isdigit() else float(raw)
        if limit is None:
            continue
        unit_re = re.compile(r"\b%ss?\b" % unit, re.I)   # WEEKS AFTER, not WEEKLY RATE
        over = []
        for ws in sheets:
            for row in ws.iter_rows():
                for c in row:
                    if not isinstance(c.value, str) or not unit_re.search(c.value):
                        continue
                    # a HEADER carries the unit, prose merely mentions it: "WEEKS AFTER"
                    # is a column of weeks, "rewritten the week of go live" is a sentence
                    if len(c.value) > 30 or len(c.value.split()) > 4:
                        continue
                    for below in range(c.row + 1, ws.max_row + 1):
                        v = ws.cell(below, c.column).value
                        if isinstance(v, (int, float)) and not isinstance(v, bool) and v > limit:
                            over.append(f"'{ws.title}'!{ws.cell(below, c.column).coordinate} = {v:g}")
        if over:
            emit("ERROR", f"C{num} [R37] is a negative over a {limit:g} {unit} threshold and the "
                          f"golden already carries {len(over)} cell(s) past it "
                          f"({', '.join(sorted(set(over))[:3])}) — the judge lands on the cell and "
                          "fires the negative for its full weight, never reading the clause that "
                          "was meant to exclude that row (an oracle run lost 4 points to a "
                          "deadstock row at 14.4 weeks whose open quantity is nil). Key the "
                          "negative on a two-column comparison read off one row instead")


# R40 (2026-08-24, an oracle run): a negative whose defect is a COMPARISON of
# two quantities makes the judge align two columns across a wide table, and it drifts by
# one column. C37 read "more open quantity planned than the open allowed figure carried
# beside it" and fired on the one Position row whose planned quantity (50, a line the plan
# ADDS for a superseded item) exceeds its neighbouring OPEN CORRECTED column at nil, while
# the OPEN ALLOWED column it actually names reads 58.94. Column headers are not landing
# places: they name sixty rows. Give the sheet a cell that carries the verdict for the
# whole comparison (a count of the rows that fail it) and quote that cell's label in the
# criterion, so the judge reads one number instead of pairing sixty.
_NEG_COMPARE_RE = re.compile(
    r"\b(?:more|greater|larger|higher|longer|lower|smaller|fewer)\b[^.;]{0,60}\bthan\b"
    r"|\bexceed(?:s|ing)?\b|\bin excess of\b", re.I)


# R52 (2026-08-24, an oracle run): the honor-rule negative ("At least
# one line ... is counted as mispriced") fired 1/3 on the GOLDEN, the judge quoting
# Briefing prose about the near-miss the rule permits ("The Vondracek DWV invoice billed
# right, because it rode quotation Q-26048"). A negative whose defect is MEMBERSHIP in a
# computed classification invites the judge to read the golden's own narrative about a
# correctly-classified line as the defect: the prose names the category (quotation,
# billed) right next to the list, and one run in three takes it. The count pins already
# fail a solver who misclassifies (the 332/987/17 cells move), so the membership
# negative adds flake surface without adding deterrence. Key negatives on a two-column
# same-row comparison or a verdict cell (R37/R40), or drop them.
_MEMBER_NEG_RE = re.compile(r"\b(?:is|are)\s+(?:counted|included|listed|reported)\b", re.I)


_R52_STOP = frozenset(("contradicting", "policy", "defect", "least", "against", "other",
                       "their", "there", "because", "before", "after", "written", "dated",
                       "among", "within", "carries", "carried", "standing"))


def _r52_tokens(text):
    return {w for w in re.findall(r"[a-z]{6,}", text.lower())} - _R52_STOP


@check(codes=['R52'], rules=['GOLD-NEG'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_membership_negatives(rows, folder):
    """A membership negative never collides with the golden's own prose about that member."""
    d = folder / "solution"
    prose = []
    for path in sorted(d.glob("*.xlsx")) if d.is_dir() else []:
        try:
            wb = workbook(path, data_only=True)
        except Exception:
            continue
        for ws in wb.worksheets:
            for row in ws.iter_rows():
                for c in row:
                    if isinstance(c.value, str) and len(c.value) >= 80:
                        prose.append((f"{path.name}:{ws.title}!{c.coordinate}",
                                      _r52_tokens(c.value)))
    if not prose:
        return
    for num, text, weight in rows:
        if weight >= 0 or not _MEMBER_NEG_RE.search(text):
            continue
        ct = _r52_tokens(text)
        hits = [(where, sorted(ct & pt)) for where, pt in prose if len(ct & pt) >= 2]
        if hits:
            where, shared = hits[0]
            emit("ERROR", f"C{num} [R52] membership negative shares its category words "
                 f"({', '.join(shared[:3])}) with the golden's own prose ({where}"
                 f"{' and ' + str(len(hits) - 1) + ' more' if len(hits) > 1 else ''}) - "
                 "the judge quotes the narrative about a correctly-classified near-miss "
                 "as the defect and deducts (an honor negative, 1/3, "
                 "citing the very briefing sentence explaining why the line is NOT the "
                 "defect). Key the negative on a two-column same-row comparison or a "
                 "verdict cell, or drop it - the count pins already fail a "
                 "misclassifying solver")


# R53 (2026-08-24, an oracle run): a negative reads as ambiguous_negative_polarity once
# it carries a SECOND negation beside the carve-out. Four negatives on one rubric shared
# the identical frame - "The workbook's count of <verdict cell label> stands above zero,
# at least one <defect>. A <boundary case> is not this defect." - and the oracle flagged
# three of them 3/3 across two submissions while never flagging the fourth. The only thing
# separating them: C38 spent its single negation on the carve-out, while C35 and C37 also
# said "rather than" and C36 also said "the records do not support". Two negative turns in
# one criterion and the judge cannot tell which way it points. Say the defect positively.
# The carve-out was the licensed single negation until 2026-08-26, when the platform's
# polarity check started failing it as scoring scaffolding (R18) - a negative
# now spends its negation budget on nothing at all, with the defect frame (in violation
# of / contrary to / although) carrying the polarity.
_NEGATION_RE = re.compile(
    r"\bnot\b|\bnever\b|\bno\b|\bwithout\b|\brather than\b|\binstead of\b"
    r"|\bfail(?:s|ing|ed)? to\b|n't\b", re.I)


@check(codes=['R53'], rules=['GOLD-NEG'], needs=['rubric'], params=['rows'])
def check_negation_count(rows):
    """A negative criterion spends exactly one negation."""
    for num, text, weight in rows:
        if weight >= 0:
            continue
        hits = _NEGATION_RE.findall(text)
        if len(hits) < 2:
            continue
        emit("ERROR", f"C{num} [R53] spends {len(hits)} negations ({', '.join(sorted(set(h.lower() for h in hits)))}) "
                     "— a negative carrying a second negative turn beside its carve-out reads as "
                     "ambiguous_negative_polarity, flagged 3/3 on three negatives of one rubric across "
                     "two submissions while the fourth, identical but for spending its one negation "
                     "on the carve-out, was never flagged (2026-08-24). State the defect positively "
                     "with the frame word carrying the polarity; the carve-out that used to hold the "
                     "single licensed negation is itself banned as scaffolding since 2026-08-26 (R18)")


@check(codes=['R40'], rules=['GOLD-NEG'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_comparison_negatives(rows, folder):
    """A comparison negative lands on a single verdict cell."""
    # A verdict cell's label is a sentence fragment, not a code: one golden's "Transfer
    # lines drawing more than the sending branch can give up" runs to 62 characters, and
    # _solution_cell_values drops every string over 40, so C38 quoted its verdict cell and
    # R40 fired anyway (2026-08-24). Read the labels straight off the sheets instead.
    labels = set()
    d = folder / "solution"
    for path in sorted(d.glob("*.xlsx")) if d.is_dir() else []:
        try:
            wb = workbook(path, data_only=True)
        except Exception:
            continue
        for ws in wb.worksheets:
            for row in ws.iter_rows(values_only=True):
                for v in row:
                    if isinstance(v, str) and 12 <= len(v.strip()) <= 90:
                        labels.add(v.strip().lower())
    if not labels:
        return
    for num, text, weight in rows:
        if weight >= 0 or not _NEG_COMPARE_RE.search(text):
            continue
        low = text.lower()
        if any(lab in low for lab in labels):
            continue
        emit("ERROR", f"C{num} [R40] states its defect as a comparison of two quantities and quotes "
                     "no label of a single verdict cell, so the judge has to align two columns "
                     "down the whole table and drifts by one (an oracle run: a negative "
                     "naming OPEN ALLOWED fired on the neighbouring OPEN CORRECTED column). Put a "
                     "count of the failing rows in a cell and quote that cell's label here")


_R104_RULE_TOKEN_RE = re.compile(
    r"\b(?:rule|policy|paragraph|article|section|clause)\s+[\w.]{1,6}\b"
    r"|\bthe [\w']+(?: [\w']+)? (?:rule|test|cut|cap|floor|window)\b", re.I)
_R104_GENERIC = {"the", "a", "an", "memo", "plan", "workbook", "deliverable", "page", "sheet",
                 "list", "rule", "test", "cut", "cap", "floor", "window", "policy", "section",
                 "clause", "paragraph", "article", "under", "although", "its", "their"}


def _r104_tokens(text):
    out = set()
    for m in _R104_RULE_TOKEN_RE.finditer(text):
        words = m.group(0).lower().replace("'s", "").split()
        out.add(" ".join(words[-2:]))
    return out


def _r104_lemmas(text):
    return {w.rstrip("s") for w in re.findall(r"[a-z']+", text.lower())
            if len(w) > 3 and w not in _R104_GENERIC}


# ---- the mirror family: a negative scoring what a positive already scores, one walk ----------
MIRROR_ID_RE = re.compile(r"\b(?:[A-Z]{1,3}-\d{3,6}|PO\s?\d{4,6}|\d{5,6})\b")


# R22: DISTINCTIVE quantity/money literals only. A leading or trailing word character
# or hyphen rules out document identifiers (26-Q-4187) and item codes (WHK-40G); the
# alternation then keeps only decimals, thousands-separated figures, and integers of
# 1000 or more that are not year-like. Bare small integers, month/day fragments and
# 19xx/20xx years produced a 60% false-positive rate on the first portfolio pass
# (counts of "2", dates read as "2026, 26, 08"), which would have buried the real hits.
NUM_LITERAL_RE = re.compile(
    r"(?<![\w.-])(?:"
    r"\d[\d,]*\.\d+"          # 38.1819, 17,500.00, 0.32
    r"|\d{1,3}(?:,\d{3})+"      # 19,200, 1,050
    r"|(?!19\d{2}(?![\d])|20\d{2}(?![\d]))\d{4,}"   # 10000+, minus bare years
    r")(?![\w-])")


_R41_STOP = {"THE","A","AN","AND","OR","NOT","THIS","THAT","THESE","IS","ARE","OF","ON","IN",
             "ITS","NO","PER","PROGRAM","ARTICLE",
             "JANUARY","FEBRUARY","MARCH","APRIL","JUNE","JULY","AUGUST","SEPTEMBER",
             "OCTOBER","NOVEMBER","DECEMBER",
             "MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY","SATURDAY","SUNDAY"}


def _r41_subjects(text, strip_carveouts):
    """The distinctive capitalised tokens of a criterion's operative sentences (R41)."""
    from ..common import split_sentences
    parts = split_sentences(text)
    if strip_carveouts:
        parts = [x for x in parts if "not this defect" not in x.lower()]
    toks = set()
    for x in parts:
        for w in re.findall(r"\b[A-Z][a-z]{3,}\b", x):
            if w.upper() not in _R41_STOP:
                toks.add(w)
    return toks


def _r69_subj_verb(t):
    m = _R69_SV_RE.match(t)
    if not m:
        return None
    head = m.group("subj").split()[-1].lower().rstrip("s")
    return head, m.group("verb").lower()


# ---- rationale kept from the merged checks (mirror family) ----
# R15:
#   R15: a negative criterion scores the same behaviour a positive criterion already
#       scores, so one requirement swings twice.
#
#       One submission (2026-08-19): the Agentic Rubric Quality Review rated the rubric
#       needs_improvement on two [major] redundant_or_double_counted_criteria findings,
#       C6/C27 (PO 78331 treated as cancelled) and C7/C26 (registration R-88214 shipped
#       outside the ceiling). Its instruction both times: keep the positive, delete the
#       negative mirror. Pairs are detected on shared record IDs (PO numbers, registration
#       and agreement numbers, catalog numbers): two or more shared IDs across a positive
#       and a negative criterion is the mirror shape. Generic contradiction and
#       domain-correctness negatives carry no IDs and never trip this.
# R22:
#   R22: negative criteria that mirror a positive by restating its figures.
# R41:
#   R41: positive/negative pairs on the same named subject read as double-counting.
#
#       The quality reviewer pairs a negative with a positive by subject, not by shared
#       figures, so R22's figure test misses pairs like "Heitkamp is priced at the March
#       letter's terms" (+4) against "Heitkamp is priced at the terms file's one percent"
#       (-3). Compare the distinctive capitalized tokens of each negative's operative
#       sentences (carve-outs stripped) against every positive; a shared proper noun is a
#       mirror suspect. Spend negatives on failures no positive scores.
# R69:
#   R69 (2026-08-31, a pre-submission check): DUAL POLARITY. The penalty scope check
#   also fails a negative that scores the inverse of a positive - "Criterion 6 positively
#   rewards 'The discount is taken at the five percent tier' while Criterion 30 negatively
#   scores the mirrored error 'The program discount is incorrectly taken at a tier
#   beyond ...'". R22 only sees shared NUMBERS, and that pair shared none. The mechanical
#   signature is the same subject head and the same verb: "discount is taken" on both
#   sides. Negatives that describe a prohibited ACT with its own verb passed the same
#   check on the same rubric ("the order is stepped up", "the buy is written against"),
#   so the test is subject+verb identity, not topic overlap.
#   R69 second pass (2026-08-31, a second pre-submission check): the same dual
#   polarity ruling, on a rubric where every criterion is wrapped in "The memo <verb>s".
#   The passive signature above never appears there, so nothing fired on C20 ("the memo
#   concludes that purchasing's order timing is not a cause") against C32 ("the memo
#   concludes that late buying or vendor promise dates caused the delay"), which the
#   check failed: "it still scores the same ordinary causal finding in both correct and
#   incorrect forms". Signature: both sides state a CONCLUSION about the same subject
#   matter. Restricted to the conclusion verbs and to two shared content lemmas, because
#   a reporting verb ("states", "reports") is shared by half a memo rubric's rows.
# R104:
#   R104 (2026-09-10, a ruling): "Criteria 15 (+1, March-cut
#   items held on shelf) and 29 (-5, March-cut item planned DROP-SHIP) double-penalize the
#   same error; merge or remove one." R69's subject+verb signature never fires on the pair
#   ("items are held" vs "unit is planned") and R22 sees no shared number; what the two
#   rows share is the RULE ANCHOR ("the March cut") plus the governed objects, and the
#   dispositions they score are mutually exclusive, so one act loses the positive AND
#   incurs the penalty. The repair is the house doctrine: drop the positive and keep the
#   negative (the defect class scores once), spending the freed weight inside the same
#   cluster - instance-form wording did NOT save the pair. Probed 2026-09-10
#   across submissions/: fires on the pre-fix pair and on four other pairs across three
#   packages (section 9 exposure vs netting; section 6 floor bins vs above-floor lift;
#   exposed-delivery and claims rules) - each a pair where one act moves both scores,
#   none yet ruled on.
@check(codes=['R15', 'R22', 'R41', 'R69', 'R104'], rules=['PRE-DUP', 'PRE-SCOPE'], needs=['rubric'], params=['rows'])
def check_mirrors(rows):
    """A negative criterion never mirrors a positive: not on shared record ids, shared figures, a shared subject, the same subject-and-verb or conclusion, or one rule anchor over the same matter.

    Codes:
      R15   a negative shares no two record ids (PO, registration, catalog numbers) with a positive
      R22   a negative restates no distinctive figure a positive already scores
      R41   a negative's operative sentences share no distinctive proper noun with a positive
      R69   a negative never has a positive's subject-and-verb signature, nor a conclusion on the same subject matter
      R104  a positive and a negative never share one rule anchor over the same governed objects
    Since: R22 2026-08-19; R15 2026-08-19; R41 2026-08-24; R69 2026-08-31; R104 2026-09-10.
    Source: the oracle, the Agentic Rubric Quality Review (redundant_or_double_counted) and the platform's Rubric
    penalty scope check (dual polarity).
    Drift-notes: five detectors on one property, merged into one walk over the rubric on 2026-09-11; each code keeps
    its own 'matched on' detail.
    """
    from collections import Counter
    # one pass over the positives: every signature a negative could mirror
    pos_ids, pos_lits, pos_subj, pos_sv, pos_concl, pos_anchor = [], {}, [], {}, [], {}
    for num, text, weight in rows:
        if weight <= 0:
            continue
        pos_ids.append((num, text, MIRROR_ID_RE.findall(text)))
        for lit in NUM_LITERAL_RE.findall(text):
            pos_lits.setdefault(lit, []).append(num)
        pos_subj.append((num, _r41_subjects(text, False)))
        sv = _r69_subj_verb(text)
        if sv:
            pos_sv.setdefault(sv, num)
        wrap = _r70_wrapper(text)
        if wrap and wrap[1] in R70_CONCLUSION_VERBS:
            pos_concl.append((num, _r70_lemmas(wrap[2])))
        for tok in _r104_tokens(text):
            pos_anchor.setdefault(tok, []).append((num, _r104_lemmas(text)))
    # a token spread across 3+ positives is the task's protagonist, not a subject (R41)
    spread = Counter(tok for _, toks in pos_subj for tok in toks)
    for num, text, weight in rows:
        if weight >= 0:
            continue
        # R15: matched on shared record ids
        nids = MIRROR_ID_RE.findall(text)
        if nids:
            for pn, pt, pids in pos_ids:
                shared = set(nids) & set(pids)
                if len(shared) >= 2:
                    emit("ERROR", f"C{num} [R15] negative mirrors positive C{pn} on {', '.join(sorted(shared))} — "
                                 "the Agentic Rubric Quality Review reads a positive/negative pair scoring one "
                                 "behaviour as double counting and rates the rubric needs_improvement "
                                 "(2026-08-19, two [major] findings); keep the positive and delete the mirror")
        # R22: matched on shared distinctive figures
        shared = sorted({lit for lit in NUM_LITERAL_RE.findall(text) if lit in pos_lits},
                        key=lambda x: -len(x))
        if shared:
            owners = sorted({n for lit in shared for n in pos_lits[lit]}, key=int)
            emit("ERROR", f"C{num} [R22] negative restates {', '.join(shared[:3])}, already scored by "
                         f"positive criterion {'/'.join('C' + o for o in owners[:3])} — the pair reads "
                         "as a mirror. The oracle deducted exactly this shape 3/3 (one criterion, judge "
                         "quoting the golden's own pre-remedy sentence as evidence of the defect) and "
                         "the Rubric Quality Review flags it redundant_or_double_counted. Keep the "
                         "positive, drop the mirror, and spend negatives on failures no positive scores")
        # R41: matched on a shared distinctive subject outside the carve-outs
        neg_subj = {t for t in _r41_subjects(text, True) if spread[t] <= 2}
        for pnum, ptoks in pos_subj:
            shared = neg_subj & ptoks
            if shared:
                emit("ERROR", f"C{num} [R41] shares the subject {sorted(shared)} with positive "
                             f"C{pnum} outside its carve-outs — the Agentic Rubric Quality Review "
                             "read four such pairs on one rubric (2026-08-24) as "
                             "double-counted requirements despite polarity pins, and rated the "
                             "rubric needs_improvement. Keep the positive and spend the negative "
                             "on a failure no positive scores")
                break
        # R69: matched on the subject+verb signature ...
        sv = _r69_subj_verb(text)
        if sv and sv in pos_sv:
            emit("ERROR", f"C{num} [R69] scores the inverse of positive C{pos_sv[sv]}: both say "
                          f"\"{sv[0]} is {sv[1]}\" - the platform's Rubric penalty scope check FAILs this "
                          "as dual polarity (2026-08-31: C6 'the discount is taken at the five "
                          "percent tier' against C30 'the discount is incorrectly taken at a tier beyond "
                          "...'). Keep the positive and drop the mirror, or give the negative a prohibited "
                          "act of its own (stepped up past, written against, placed on)")
        # ... or on a conclusion about the same subject matter (the memo-rubric shape)
        wrap = _r70_wrapper(text)
        if wrap and wrap[1] in R70_CONCLUSION_VERBS:
            lem = _r70_lemmas(wrap[2])
            for pnum, plem in pos_concl:
                shared = sorted(lem & plem)
                if len(shared) >= 2:
                    emit("ERROR", f"C{num} [R69] concludes on the same subject as positive C{pnum} "
                                  f"(shared: {', '.join(shared[:4])}) - the platform's Rubric penalty scope check "
                                  "FAILs a negative that scores the same finding in its incorrect form "
                                  "(2026-08-31: C20 \"purchasing's order timing is not a "
                                  "cause\" against C32 \"late buying or vendor promise dates caused the delay\"). "
                                  "Rely on the positive, and spend the penalty on a prohibited act instead")
                    break
        # R104: matched on a shared rule anchor plus shared subject matter
        lem = _r104_lemmas(text)
        hit = None
        for tok in _r104_tokens(text):
            for pnum, plem in pos_anchor.get(tok, []):
                if lem & plem:
                    hit = (tok, pnum, sorted(lem & plem)[:3])
                    break
            if hit:
                break
        if hit:
            tok, pnum, shared = hit
            emit("ERROR", f"C{num} [R104] shares the rule anchor \"{tok}\" and the subject matter "
                          f"({', '.join(shared)}) with positive C{pnum} - one act loses the positive "
                          "and incurs the penalty, which reads as double jeopardy "
                          "(2026-09-10: 'merge or remove one'). Drop the positive and "
                          "keep the negative, the only place the defect class scores, and spend "
                          "the freed weight inside the same cluster")
