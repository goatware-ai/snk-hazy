"""Group 2: the golden read against itself and the inputs (GOLD-FID).

Generated 2026-09-04 from autoeval_check.py; every check body is verbatim.
"""
import re
import zipfile
from decimal import Decimal
from ..common import (MONTH_NAMES, MONTH_NUM, MONTHS_LOWER, MONTHS_RE, _G5_WORDS, _MONEY_RE, _docx_tables, _docx_text,
                      _xlsx_all_text as _all_text_cells, _xlsx_prose, document, formula_cells, input_texts,
                      month_number, solution_files, workbook)
from ..core import check, emit, recommend, REPORT, OPTIONS


# R29 (2026-08-22, an oracle run): a criterion that says HOW a figure is derived
# ("the cell carrying that total adding the three clause lines above it") fails whenever
# the figure sits in more than one cell, because the judge lands on whichever copy it
# finds first. The run quoted Briefing!E10, `='Not Claimed'!D8`, a plain reference, against a
# criterion about a cell that adds three lines. The summary tab reads every headline figure
# through from the tab that computes it, which is the design the liveness criteria want, so
# every pinned total has at least two homes by construction. Three of this task's four
# oracle rounds lost a criterion to this one shape, a different instance each time.
# Pin the derivation on the two dedicated liveness criteria, which grade a whole tab rather
# than one figure, and let a value criterion state the value.
_DERIV_RE = re.compile(r"\badd(?:s|ing)\b|\bsum(?:s|med|ming)\b|\brather than (?:being )?keyed\b"
                       r"|\bis a formula\b|\bare formulas\b|\bcomputed (?:in|by) the cell\b", re.I)


@check(codes=['R29'], rules=['GOLD-FID'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_derivation_anchors(rows, folder):
    """A criterion stating how a figure is derived names a figure that sits in one golden cell only.

    Since: 2026-08-22.
    Source: the oracle, landing on a read-through copy.
    """
    homes = {}
    d = folder / "solution"
    for path in sorted(d.glob("*.xlsx")) if d.is_dir() else []:
        try:
            wb = workbook(path, data_only=True)
        except Exception:
            continue
        for ws in wb.worksheets:
            for row in ws.iter_rows():
                for c in row:
                    v = c.value
                    if isinstance(v, (int, float)) and not isinstance(v, bool):
                        homes.setdefault(round(float(v), 2), []).append(f"{ws.title}!{c.coordinate}")
    if not homes:
        return
    for num, text, weight in rows:
        if weight <= 0 or not _DERIV_RE.search(text):
            continue
        for tok in _MONEY_RE.findall(text):
            where = homes.get(round(float(tok.replace(",", "")), 2), [])
            if len(where) > 1:
                emit("ERROR", f"C{num} [R29] says how {tok} is derived, but that value sits in "
                             f"{len(where)} cells ({', '.join(where[:3])}) — the judge lands on "
                             "whichever it finds first and fails the criterion when that is a "
                             "read-through copy (an oracle run quoted the briefing's plain "
                             "reference). State the value here and leave the derivation to the "
                             "liveness criteria, which grade a tab rather than one figure")
                break


SUPERLATIVE_RE = re.compile(r"\b(cheap|dear|high|low|large|small|big|costli)est\b[^.;]{0,60}?\bof the\b"
                            r"|\bthe (cheap|dear|high|low|large|small|big|costli)est (of|among)\b", re.I)


@check(codes=['S1'], rules=['GOLD-FID'], needs=['solution'], params=['folder'])
def check_superlatives(folder):
    """Every superlative in a solution text cell is re-verified against the table it summarises whenever the numbers move.

    S1 (2026-08-23): the golden-source-fidelity axis hard-failed the task
    on one sentence, a Scenarios footer naming the six point cap 'the cheapest of the four'
    while the tab's own table showed a counter at a tenth of its price. A superlative in a
    solution text cell is a conclusion the checker re-derives from the neighbouring table,
    so every one must be re-verified against the numbers whenever the numbers move, so
    the builder eyeballs each claim; record in .gate-debt once verified."""
    sol = folder / "solution"
    hits = []
    for path in sorted(sol.glob("*.xlsx")) if sol.is_dir() else []:
        try:
            wb = workbook(path)
        except Exception:
            continue
        for ws in wb.worksheets:
            for row in ws.iter_rows():
                for c in row:
                    if isinstance(c.value, str) and SUPERLATIVE_RE.search(c.value):
                        hits.append(f"{path.name}:{ws.title}!{c.coordinate}")
        wb.close()
    if hits:
        emit("ERROR", f"[S1] superlative claim(s) in solution text cells ({', '.join(hits[:6])}) — "
                     "the fidelity axis re-derives such conclusions from the neighbouring table and "
                     "hard-fails on a mismatch (2026-08-23: 'cheapest of the four' "
                     "named the wrong counter, axis 2/5). Verify each against the numbers it "
                     "summarizes, then accept as S1 with the verification stated")


_R71_MONTHS = MONTHS_RE


# the strict words may sit a few words from the date ("before the fieldwork begins on
# September 22"); bare "by" must touch the date, or "approved by Tina ... March 16" reads
# as a deadline
_R71_BOUND_RE = re.compile(
    r"\b(before|earlier than|ahead of|no later than|on or before)\b[^.,;]{0,40}?\b(" + _R71_MONTHS +
    r")\s+(\d{1,2})\b|\b(by)\s+(" + _R71_MONTHS + r")\s+(\d{1,2})\b", re.I)


_R71_UNIVERSAL_RE = re.compile(r"\b(?:each|every|all)\b", re.I)


_R71_HEADER_RE = re.compile(
    r"^(?:by|by when|due|due date|date due|deadline|target(?: date)?|complete(?:d)? by"
    r"|completion date|target completion)$", re.I)


_R71_CELL_DATE_RE = re.compile(
    r"\b(" + _R71_MONTHS + r")\s+(\d{1,2})\b(?:,\s*(\d{4}))?|\b(\d{1,2})/(\d{1,2})/(\d{4})\b", re.I)


_MONTH_NUM = MONTH_NUM


@check(codes=['R71'], rules=['GOLD-FID'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_docx_deadline_pins(rows, folder):
    """A universal deadline pin has no later-dated row in the golden's schedule."""
    tables = None
    for num, text, weight in rows:
        if weight <= 0 or not _R71_UNIVERSAL_RE.search(text):
            continue
        b = _R71_BOUND_RE.search(text)
        if not b:
            continue
        if tables is None:
            tables = _docx_tables(folder)
        if not tables:
            return
        word = (b.group(1) or b.group(4)).lower()
        strict = word in ("before", "earlier than", "ahead of")
        bound = (_MONTH_NUM[(b.group(2) or b.group(5)).lower()], int(b.group(3) or b.group(6)))
        for name, ti, body in tables:
            if len(body) < 2:
                continue
            cols = [i for i, h in enumerate(body[0]) if _R71_HEADER_RE.match(h)]
            if not cols:
                continue
            for row in body[1:]:
                for i in cols:
                    if i >= len(row):
                        continue
                    for dm in _R71_CELL_DATE_RE.finditer(row[i]):
                        if dm.group(1):
                            when = (_MONTH_NUM[dm.group(1).lower()], int(dm.group(2)))
                        else:
                            when = (int(dm.group(4)), int(dm.group(5)))
                        late = when >= bound if strict else when > bound
                        if not late:
                            continue
                        emit("ERROR", f"C{num} [R71] says {b.group(0)} for every item, but {name} "
                                      f"table {ti + 1} (header '{body[0][i]}') carries a row dated "
                                      f"{dm.group(0)}: \"{row[0][:70]}\". The judge reads the "
                                      "universal literally and failed a task's C30 "
                                      "3 of 3 oracle runs on one October 30 row under a 'before "
                                      "September 22' heading (2026-08-31). Date the item's "
                                      "pre-deadline step inside the bound or take it out of the "
                                      "schedule the criterion sweeps")
                        break


ACTION_TOKEN_RE = re.compile(r"^(CHANGE|CANCEL|REPLACE)\b")


STAY_STATUSES = {"DE MINIMIS", "AS QUOTED"}


# G2 (2026-08-24, AutoEval run 3): the golden's Tag detail tab
# was written with EACHES and the USE flag one column to the left of the headers naming
# them, and the two columns those headers reserved were never written at all. So the
# reconciliation's =SUMIFS('Tag detail'!$I$6:$I$59, ..., 'Tag detail'!$K$6:$K$59,"use")
# summed a column of TEXT filtered on a column that was empty, and its neighbour summed
# an empty $J$6:$J$59 - while both cells carried the caches the build had computed off the
# layout it meant to write. The oracle judge reads caches, so it scored the workbook 0.96
# and never saw it; the tab's own exclusion VLOOKUP pointed at an empty $K$5:$L$9 too.
# Anyone pressing F9, and Excel on first open, collapses the whole reconciliation to zero.
# This is A9 (a cache the formula does not reproduce) at workbook scale, and no check had
# ever looked at whether an aggregation's range holds anything to aggregate.
_AGG_CALL_RE = re.compile(
    r"\b(SUMIFS|SUMIF|SUM|AVERAGEIFS|AVERAGEIF|AVERAGE|COUNTIFS|COUNTIF)\s*\(", re.I)


_RANGE_ARG_RE = re.compile(
    r"^(?:(?:'([^']+)'|([A-Za-z0-9_][A-Za-z0-9_ ]*))!)?"
    r"(\$?[A-Z]{1,3}\$?\d+)(?::(\$?[A-Z]{1,3}\$?\d+))?$")


def _split_args(s):
    args, depth, cur, quoted = [], 0, [], False
    for ch in s:
        if ch == '"':
            quoted = not quoted
        if not quoted:
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
            elif ch == "," and depth == 0:
                args.append("".join(cur))
                cur = []
                continue
        cur.append(ch)
    args.append("".join(cur))
    return [a.strip() for a in args]


def _agg_calls(formula):
    """yield (func, [args]) for every aggregation call in a formula, nested included."""
    for m in _AGG_CALL_RE.finditer(formula):
        depth, end = 1, m.end()
        quoted = False
        while end < len(formula) and depth:
            ch = formula[end]
            if ch == '"':
                quoted = not quoted
            elif not quoted:
                depth += (ch == "(") - (ch == ")")
            end += 1
        if depth:
            continue
        yield m.group(1).upper(), _split_args(formula[m.end():end - 1])


def _range_cells(vwb, default_sheet, arg):
    m = _RANGE_ARG_RE.match(arg)
    if not m:
        return None
    title = m.group(1) or m.group(2) or default_sheet
    if title not in vwb.sheetnames:
        return None
    ref = m.group(3) + (":" + m.group(4) if m.group(4) else "")
    try:
        got = vwb[title][ref.replace("$", "")]
    except Exception:
        return None
    if not isinstance(got, tuple):
        return [got]
    return [c for row in got for c in (row if isinstance(row, tuple) else (row,))]


@check(codes=['G2'], rules=['GOLD-FID'], needs=['solution'], params=['folder'])
def check_unreproducible_cache(folder):
    """No aggregation's range is empty of anything it could have aggregated."""
    # one walk over the formula cells, shared with A9 (common.formula_cells)
    for fname, title, coord, f, cached in formula_cells(folder):
        if not isinstance(cached, (int, float)) or isinstance(cached, bool):
            continue
        if cached == 0:
            continue          # a zero is reproducible from an empty range
        vwb = workbook(folder / "solution" / fname, data_only=True)
        for func, args in _agg_calls(f):
            counting = func.startswith("COUNT")
            if func in ("SUMIF", "AVERAGEIF"):
                arg = args[2] if len(args) >= 3 else args[0]
            else:
                arg = args[0]
            cells = _range_cells(vwb, title, arg)
            if cells is None:
                continue
            if counting:
                live = [c for c in cells if c.value is not None]
                what = "no cell with anything in it"
            else:
                live = [c for c in cells if isinstance(c.value, (int, float))
                        and not isinstance(c.value, bool)]
                what = "not one numeric cell"
            if live:
                continue
            emit("ERROR", f"[G2] {fname} '{title}'!{coord} caches "
                          f"{cached:g} from {f}, but {arg} holds {what} — the cache "
                          "cannot be reproduced from the formula, so the figure "
                          "survives only until someone recalculates and the tab it "
                          "feeds collapses (2026-08-24: a golden shipped "
                          "with two columns written one to the left of the headers "
                          "naming them, and the oracle judge, which reads caches, "
                          "scored it 0.96). Point the formula at the range that "
                          "carries the data")
            break


# G3 (2026-08-25, a grader): the briefing stated
# "5,117 units of demand" and then enumerated the coverage beneath it, and those lines
# added to 5,159. The 42-unit gap was the classified line quoting the quantity ORDERED
# (580, rounded up to full cartons) where the identity needs the quantity APPLIED to
# demand (538), and nothing on the page reconciled the two. Every cell in the block was
# a live cross-sheet reference, so no liveness or cache rule could see it, and the oracle
# judge scores each line separately and never adds the column up. A grader does add it
# up, and called it out in the first paragraph. The shape is mechanical: a contiguous run
# of cells in ONE column, each a pure reference into the SAME other sheet, whose first
# value is meant to be the total of the rest. Fire only when the block NEARLY ties (the
# tell of a real identity, not of unrelated figures sharing a column) and when no cell
# just below it carries the difference, which is what a reconciliation line looks like.
_G3_XREF_RE = re.compile(r"^=\s*(?:'([^']+)'|([A-Za-z][A-Za-z0-9_ ]*))!\$?[A-Z]{1,3}\$?\d{1,5}"
                         r"(?:\s*[+-]\s*(?:'([^']+)'|([A-Za-z][A-Za-z0-9_ ]*))!\$?[A-Z]{1,3}\$?\d{1,5})*$")


def _g3_target(formula):
    """The single other sheet a pure cross-sheet reference chain reads, else None."""
    m = _G3_XREF_RE.match(formula.replace("\n", "").strip())
    if not m:
        return None
    names = {g for g in re.findall(r"(?:'([^']+)'|\b([A-Za-z][A-Za-z0-9_ ]*))!", formula)
             for g in (g,) if g}
    names = {a or b for a, b in re.findall(r"(?:'([^']+)'|\b([A-Za-z][A-Za-z0-9_ ]*))!", formula)}
    return names.pop() if len(names) == 1 else None


@check(codes=['G3'], rules=['GOLD-FID'], needs=['solution'], params=['folder'])
def check_summary_reconciliation(folder):
    """A front-page column of cross-sheet references whose head is the total of the lines under it ties, or carries a reconciliation cell for the difference.

    Since: 2026-08-25.
    Source: a grader.
    """
    sol = folder / "solution"
    for path in sorted(sol.glob("*.xlsx")) if sol.is_dir() else []:
        try:
            fwb = workbook(path)
            vwb = workbook(path, data_only=True)
        except Exception:
            continue
        for ws in fwb.worksheets:
            vs = vwb[ws.title]
            for col in range(1, min(ws.max_column, 40) + 1):
                run = []
                for row in range(1, min(ws.max_row, 400) + 2):
                    f = ws.cell(row, col).value if row <= ws.max_row else None
                    v = vs.cell(row, col).value if row <= ws.max_row else None
                    ok = (isinstance(f, str) and f.startswith("=")
                          and _g3_target(f) and isinstance(v, (int, float))
                          and not isinstance(v, bool))
                    if ok:
                        run.append((row, float(v)))
                        continue
                    if len(run) >= 5:
                        total, parts = run[0][1], [x for _, x in run[1:]]
                        gap = total - sum(parts)
                        # A total-and-its-parts block: every part is a positive share of one
                        # whole. One task's Briefing B14:B20 mixes an opening
                        # balance, a target, a variance and three negative deductions, and
                        # is not an identity at all - the sign test is what tells them apart.
                        # The near-tie band then keeps unrelated positives out (the gap was
                        # 42 out of 5,117, 0.8%).
                        if (total > 0 and len(parts) >= 4
                                and all(0 < x < total for x in parts)
                                and 0.0005 < abs(gap) <= total * 0.02):
                            below = [vs.cell(r, col).value
                                     for r in range(run[-1][0] + 1, run[-1][0] + 4)]
                            if not any(isinstance(b, (int, float)) and not isinstance(b, bool)
                                       and abs(abs(b) - abs(gap)) < 0.005 for b in below):
                                emit("ERROR",
                                     f"[G3] {path.name} '{ws.title}'!{ws.cell(run[0][0], col).coordinate}"
                                     f" states {total:g} and the {len(parts)} source lines under it add "
                                     f"to {sum(parts):g}, {abs(gap):g} out, with no reconciliation cell "
                                     "beneath the block - the oracle judge scores those lines one at a "
                                     "time and never adds the column up, but a grader does and opens "
                                     "with it (2026-08-25: a coverage line "
                                     "quoting the quantity ORDERED where the identity needs the quantity "
                                     "APPLIED). Carry the difference in a cell that reads zero")
                    run = []


# G4 (2026-09-01, AutoEval, golden_source_fidelity 2/5): the input
# register carried four sales-order lines billed under the agreement price, and the
# Summary's correcting-invoice table listed three - the build's shortbill pass filtered
# on "entered at the January price" where the defect class is "billed below agreement",
# so the P10453 line mis-keyed at the load (21.48 against Schedule B's 24.18) never made
# the table and the stated total understated the recovery by 44%. Every in-golden check
# passed because the golden agreed with itself: the register mirror carries no price
# column, the table's own SUM tied, and the analytics the caches were verified against
# had the same omission. AutoEval recomputes from the inputs, so this does too: join a
# billed-register input CSV (order, item, qty, uom, unit price) to the golden's
# agreement-price map, and every line billed at least a cent per unit under agreement
# must appear on some golden row that pairs the order number with the item AND carries
# the correction context (the agreement price, the per-unit gap or the extended gap) -
# a raw register mirror restating the wrong price satisfies the pair but not the context.
_G4_ITEM_H_RE = re.compile(r"^ITEM([ _]?(NO|NUMBER|#))?$", re.I)


_G4_QTY_H_RE = re.compile(r"^(QTY|QUANTITY)$", re.I)


_G4_PRICE_H_RE = re.compile(r"^UNIT[ _]?PRICE$", re.I)


_G4_UOM_H_RE = re.compile(r"^(UOM|UNIT OF MEASURE)$", re.I)


_G4_ORDER_H_RE = re.compile(r"^(SO|SALES[ _]?ORDER|ORDER)[ _]?(NO|NUMBER|#)?$", re.I)


_G4_AGREE_H_RE = re.compile(r"^AGREEMENT( PRICE)?$", re.I)


def _g4_agreement_map(folder):
    """(item, uom-or-None) -> agreement price, from any golden sheet with an
    AGREEMENT PRICE column beside an ITEM column (cached values)."""
    out = {}
    sol = folder / "solution"
    for path in sorted(sol.glob("*.xlsx")) if sol.is_dir() else []:
        try:
            vwb = workbook(path, data_only=True)
        except Exception:
            continue
        for ws in vwb.worksheets:
            for hr in range(1, min(ws.max_row, 8) + 1):
                heads = {c: str(ws.cell(hr, c).value).strip()
                         for c in range(1, min(ws.max_column, 30) + 1)
                         if isinstance(ws.cell(hr, c).value, str)}
                item_c = next((c for c, h in heads.items() if _G4_ITEM_H_RE.match(h)), None)
                agree_c = next((c for c, h in heads.items() if _G4_AGREE_H_RE.match(h)), None)
                uom_c = next((c for c, h in heads.items() if _G4_UOM_H_RE.match(h)), None)
                if not item_c or not agree_c:
                    continue
                for r in range(hr + 1, ws.max_row + 1):
                    item = ws.cell(r, item_c).value
                    price = ws.cell(r, agree_c).value
                    if (isinstance(item, str) and item.strip()
                            and isinstance(price, (int, float))
                            and not isinstance(price, bool)):
                        uom = ws.cell(r, uom_c).value if uom_c else None
                        uom = uom.strip().upper() if isinstance(uom, str) else None
                        out[(item.strip().upper(), uom)] = float(price)
                break
    return out


_G5_NUMWORD = (r"(?:\d{1,3}(?:,\d{3})*|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
               r"thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|"
               r"forty|fifty|sixty|seventy|eighty|ninety)(?:[- ](?:one|two|three|four|five|six|"
               r"seven|eight|nine))?")


_G5_CLAIM_RE = re.compile(r"\b(all |every one of )?(" + _G5_NUMWORD + r") of (?:the |its |those |these |them |"
                          r"which |our |his |her )?(" + _G5_NUMWORD + r")\b", re.I)


def _g5_int(tok):
    # thousands separators are stripped before the digit test: an earlier run
    # (2026-09-10) read "36 of 1,134" as "36 of 1" and failed a correct golden,
    # because the numword pattern stopped at the comma.
    tok = tok.lower().strip().replace(",", "")
    if tok.isdigit():
        return int(tok)
    parts = re.split(r"[- ]", tok)
    return sum(_G5_WORDS.get(p, 0) for p in parts)


_G5_SPLIT_HEAD_RE = re.compile(r"\b(" + _G5_NUMWORD + r") ([a-z]+s)\b[^.]{0,160}?\bin (two|three|four|five) "
                               r"(?:forms|ways|kinds|groups|parts|categories|shapes)\b", re.I)
_G5_SPLIT_NOT_NOUN = {"days", "weeks", "months", "years", "percents", "hours", "minutes", "pounds", "dollars"}
_G5_OVERLAP_RE = re.compile(r"\bboth\b|\boverlap\w*|\bcounted (?:once|twice)\b|\bin each\b", re.I)


def _g5_split_paragraphs(folder):
    out = []
    for x in solution_files(folder, {".xlsx"}):
        out.extend((f"{x.name} {where}", text) for where, text in _xlsx_prose(x))
    for d in solution_files(folder, {".docx"}):
        out.extend((f"{d.name} paragraph {i + 1}", p) for i, p in enumerate(_docx_text(d).split("\n")) if p.strip())
    return out


@check(codes=['G5'], rules=['GOLD-FID'], needs=['solution'], params=['folder'])
def check_narrative_count_claims(folder):
    """A count claim in the golden's prose is consistent with itself: in "X of the Y" X never exceeds Y, and the parts of a total split "in two forms" (ways, kinds, groups, parts) sum to that total or the paragraph states the overlap.

    Split arm since 2026-09-15 (a rejection): "Thirty-four invoices carry a fuel
    surcharge ... in two forms. On thirteen invoices ... On 43 invoices ..." sums to 56 against 34 with
    the overlap never stated, and the rejection named it an internal count inconsistency. The head is a
    number and a plural noun followed within the sentence by "in two|three|four|five forms|ways|kinds|
    groups|parts|categories|shapes"; the parts are the next k "number noun" runs of the same noun in the
    paragraph; an overlap is stated by "both", "overlap", "counted once|twice" or "in each".

    G5 (2026-09-02, AutoEval golden_source_fidelity 2/5): the
    golden's narrative said 'four slots ran ... with no written support, three of the
    four lost money' while its own results tab held four negative unsupported slots and
    a counter reading 4. Every other check tests the rubric against the golden, so a
    prose count that contradicts the golden's computed tab is invisible to all of them.
    This lists every 'X of the Y' count claim in the golden's prose (workbook prose cells
    and solution .docx text) for hand verification against the computed tab, and fails
    outright when X exceeds Y. A count claim the tab contradicts is the one-mismatch
    hard fail on the fidelity axis; verify each line here before every zip build."""
    claims = []
    for x in solution_files(folder, {".xlsx"}):
        for where, text in _xlsx_prose(x):
            for m in _G5_CLAIM_RE.finditer(text):
                claims.append((f"{x.name} {where}", m.group(0), m.group(2), m.group(3)))
    for d in solution_files(folder, {".docx"}):
        for m in _G5_CLAIM_RE.finditer(_docx_text(d)):
            claims.append((d.name, m.group(0), m.group(2), m.group(3)))
    for at, phrase, a, b in claims:
        x, y = _g5_int(a), _g5_int(b)
        if x > y:
            emit("ERROR", f'[G5] {at}: "{phrase}" claims more than the whole it counts from')
        else:
            # not a failure the tool can prove; the operator confirms each line by hand
            print(f'        info: [G5] {at}: count claim "{phrase}" - confirm the golden\'s '
                  "computed tab gives the same X of Y (a prose count the tab contradicts is "
                  "a fidelity hard fail, 2026-09-02)")
    for at, text in _g5_split_paragraphs(folder):
        for m in _G5_SPLIT_HEAD_RE.finditer(text):
            noun = m.group(2).lower()
            if noun in _G5_SPLIT_NOT_NOUN:
                continue
            k = _G5_WORDS.get(m.group(3).lower(), 0)
            total = _g5_int(m.group(1))
            stem = noun[:-1] if noun.endswith("s") else noun
            rest = text[m.end():]
            parts = [_g5_int(p.group(1)) for p in re.finditer(r"\b(" + _G5_NUMWORD + r") " + re.escape(stem) + r"s?\b", rest, re.I)][:k]
            if len(parts) < k or sum(parts) == total or _G5_OVERLAP_RE.search(text):
                continue
            emit("ERROR", f'[G5] {at}: "{m.group(0)[:90]}" splits {total} {noun} into parts of '
                          f'{" and ".join(str(p) for p in parts)}, which sum to {sum(parts)}, and the paragraph states no '
                          "overlap - say how many sit in both, or give parts that add to the total "
                          "(a rejection, 2026-09-15)")


# G7 (2026-09-02, a grader, Golden Quality): a docx table's total
# row did not equal its rows. A python-docx edit that addressed the total row by index landed
# on the last DATA row instead (the under-billed table: DFL7718272's 1.18 became the 251.68
# total, the real total row was fixed by a later string replace), the golden's own sum no
# longer tied, and a grader read it in one pass while every figure the rubric quotes was
# still present. Every solution docx table whose last row is a total (first cell empty or
# reading All/Total/Sum) must sum, column by column, to that row.
_G7_NUM_RE = re.compile(r"^-?\(?\$?-?[\d,]+(?:\.\d+)?\)?$")


def _g7_num(txt):
    t = txt.strip().replace("$", "").replace(",", "")
    if not t or not _G7_NUM_RE.match(txt.strip()):
        return None
    neg = t.startswith("(") and t.endswith(")")
    t = t.strip("()")
    try:
        v = Decimal(t)
    except Exception:
        return None
    return -v if neg else v


@check(codes=['G7'], rules=['GOLD-FID'], needs=['solution'], params=['folder'])
def check_docx_total_rows(folder):
    """Every solution docx table with a total row sums, column by column, to that row.

    Since: 2026-09-02 (Golden Quality).
    Source: a grader.
    """
    for d in solution_files(folder, {".docx"}):
        doc = document(d)
        for ti, t in enumerate(doc.tables):
            rows = [[c.text for c in r.cells] for r in t.rows]
            if len(rows) < 4:
                continue
            last = rows[-1]
            label = next((c for c in last if c.strip()), "")
            is_total = (not last[0].strip()) or re.match(r"^(?:all|total|sum|grand total)\b", last[0], re.I)
            if not is_total or not re.match(r"^(?:all|total|sum|grand total)?\b", label, re.I):
                continue
            if last[0].strip() and not re.match(r"^(?:all|total|sum|grand total)\b", last[0], re.I):
                continue
            for ci in range(len(last)):
                tot = _g7_num(last[ci])
                if tot is None:
                    continue
                vals = [_g7_num(r[ci]) for r in rows[1:-1]]
                vals = [v for v in vals if v is not None]
                if len(vals) < 2:
                    continue
                if sum(vals) != tot:
                    emit("ERROR", f"[G7] {d.name} table {ti + 1} column {ci + 1}: the total row reads "
                                  f"{last[ci].strip()} but its {len(vals)} rows sum to {sum(vals):,.2f} - "
                                  "a golden table that does not tie to its own total is a grader's "
                                  "one-read hard fail (2026-09-02: an index-addressed "
                                  "cell edit landed on the last data row instead of the total row)")


# G21 (2026-09-10, Golden Quality): a table's printed figures
# must reproduce the table's own arithmetic AS PRINTED. This desk accepted a refrigeration
# quote whose per-unit table showed 766 kWh/year and 5,366 kWh over seven years; 766 x 7 is
# 5,362, and the same row pair was out by 3 on the second unit. Both printed figures were the
# correct rounding of the true values (766.50 and 5,365.50), so a re-derivation at full
# precision agreed with the golden and hid the defect completely - the re-derivation is what
# this desk ran, and it passed. A grader read the printed numbers the way the customer
# would and sent the task back. So: where a column is a constant multiple of another across
# every row, check the DISPLAYED values against that constant at the displayed precision.
#
# This fires on figures that are individually correct. The defect is presentation, and the fix
# is consistent rounding (carry the decimals, as that EC then did), never a recalculation.
# Only a multiplier a table would actually state: a small count, or a calendar constant. This
# is what keeps the check off columns whose ratio is merely near an integer by construction -
# the same golden's cost column is daily use times 459.9 (365 days x $0.18 x 7 years), which
# snapped to 460 and read as a broken multiple of 7 until this list narrowed it.
_G21_CONSTANTS = [Decimal(n) for n in (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 24, 52, 365, 2555)]
_G21_CLEAN_MAX_DRIFT = Decimal("0.01")   # ratios must agree within 1% to count as one constant


def _g21_display_tol(txt):
    """Half a unit at the precision the cell is printed to: 5,366 -> 0.5, 5,365.50 -> 0.005."""
    t = txt.strip().replace("$", "").replace(",", "").strip("()")
    dp = len(t.split(".")[1]) if "." in t else 0
    return Decimal(5) * (Decimal(10) ** -(dp + 1))


@check(codes=['G21'], rules=['GOLD-FID'], needs=['solution'], params=['folder'])
def check_docx_displayed_ratios(folder):
    """Where one docx table column is a constant multiple of another, the printed figures multiply out at the displayed precision.

    Since: 2026-09-10.
    Source: a grader.
    Drift-notes: the defect is rounding, never the values; only multipliers a table would state are tried.
    """
    for d in solution_files(folder, {".docx"}):
        doc = document(d)
        for ti, t in enumerate(doc.tables):
            rows = [[c.text for c in r.cells] for r in t.rows]
            if len(rows) < 3:
                continue
            data = rows[1:]
            ncol = min(len(r) for r in rows)
            for ci in range(ncol):
                for cj in range(ci + 1, ncol):
                    pairs = []
                    for r in data:
                        a, b = _g7_num(r[ci]), _g7_num(r[cj])
                        if a is None or b is None or a == 0:
                            continue
                        pairs.append((r[ci], r[cj], a, b))
                    if len(pairs) < 2:
                        continue
                    ratios = [b / a for _, _, a, b in pairs]
                    kr = next((k for k in _G21_CONSTANTS
                               if all(abs(r - k) / k <= _G21_CLEAN_MAX_DRIFT for r in ratios)), None)
                    if kr is None:                  # not one constant the table would state
                        continue
                    bad = [(ta, tb, a, b) for ta, tb, a, b in pairs
                           if abs(b - a * kr) > _g21_display_tol(tb)]
                    if not bad or len(bad) < len(pairs):
                        continue                    # one odd row is a different finding, not this
                    ta, tb, a, b = bad[0]
                    emit("ERROR", f"[G21] {d.name} table {ti + 1}: column {cj + 1} is column {ci + 1} "
                                  f"times {kr}, but the printed figures do not multiply out - "
                                  f"{ta.strip()} x {kr} is {a * kr:,.2f}, not {tb.strip()} "
                                  f"({len(bad)} of {len(pairs)} rows). The values are individually "
                                  "right and it is the ROUNDING that is inconsistent, so carry the "
                                  "decimals rather than recalculating (2026-09-10: "
                                  "a grader sent this back after a full-precision re-derivation "
                                  "matched the golden and missed it)")


_G6_SECTION_RE = re.compile(r"\bsection\s+(\d{1,2})\b", re.I)


_G6_HEADING_RE = re.compile(r"^\s*(\d{1,2})\.\s+\S", re.M)


_G6_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
             "eight": 8, "nine": 9, "ten": 10, "twelve": 12, "fifteen": 15, "twenty": 20,
             "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "ninety": 90, "hundred": 100}


def _g6_sections(text):
    """Split a numbered procedure into {section number: text}."""
    heads = list(_G6_HEADING_RE.finditer(text))
    out = {}
    for i, h in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        out.setdefault(int(h.group(1)), "")
        out[int(h.group(1))] += text[h.end():end]
    return out


def _g6_value_forms(v):
    """Every way a parameter literal can be written in prose."""
    forms = set()
    if isinstance(v, float) and 0 < v < 1:
        pct = v * 100
        p = f"{pct:g}"
        forms |= {f"{p} percent", f"{p}%", f"{p} per cent"}
        return forms, None
    n = int(v) if float(v).is_integer() else v
    forms.add(f"{n:,}" if isinstance(n, int) else f"{n:g}")
    forms.add(str(n))
    word = None
    if isinstance(n, int):
        word = next((w for w, k in _G6_WORDS.items() if k == n), None)
    return forms, word


@check(codes=['G6'], rules=['GOLD-FID'], needs=['inputs', 'solution'], params=['folder'])
def check_parameter_provenance(folder):
    """A literal parameter whose source cell names a section of an input document appears in that section.

    G6 (2026-09-03, AutoEval golden_source_fidelity 2/5): the
    golden's Params tab cited 'WH-4 section 7' as the source of three bin cubes it had
    in fact read off the location master, and section 7 stated three different figures
    (1,344 / 6,048 / 1,600 against 2,880 / 10,368 / 5,400). Every other fidelity check
    tests the rubric against the golden; a parameter row that names the right clause and
    the wrong basis is invisible to them, and the platform reads it as the golden
    contradicting its own source. For every literal parameter whose source cell names a
    section of an input .docx, the value has to appear in that section as digits, a
    number word or a percent. A figure of 100 or more that is absent while the section
    states some other figure of that size is the proven shape and errors; anything else
    absent is listed for hand confirmation (a derived constant such as 60 business days
    from 'twelve weeks at five days' is legitimate but must be worded as a derivation)."""
    inp = folder / "inputs"
    if not inp.is_dir():
        return
    docs = {d: _g6_sections(_docx_text(d)) for d in sorted(inp.glob("*.docx"))}
    docs = {d: sec for d, sec in docs.items() if sec}
    if not docs:
        return
    for x in solution_files(folder, {".xlsx"}):
        try:
            wb = workbook(x)
        except Exception:
            continue
        for ws in wb.worksheets:
            if not re.search(r"param|assumption|input", ws.title, re.I):
                continue
            for row in ws.iter_rows(values_only=True):
                cells = [c for c in row if c is not None]
                nums = [c for c in cells if isinstance(c, (int, float)) and not isinstance(c, bool)]
                srcs = [c for c in cells if isinstance(c, str) and _G6_SECTION_RE.search(c)]
                if len(nums) != 1 or not srcs:
                    continue
                value, src = nums[0], srcs[0]
                if re.search(r"\bderived\b|\bcomputed\b|\btimes\b", src, re.I):
                    continue   # the source is worded as a derivation, not a quotation
                label = next((c for c in cells if isinstance(c, str) and c is not src), "")
                for sec_no in {int(m.group(1)) for m in _G6_SECTION_RE.finditer(src)}:
                    hits = [(d, sec[sec_no]) for d, sec in docs.items() if sec_no in sec]
                    if not hits:
                        continue
                    forms, word = _g6_value_forms(value)
                    found = False
                    for _, text in hits:
                        low = text.lower()
                        if any(f.lower() in low for f in forms) or (word and re.search(rf"\b{word}\b", low)):
                            found = True
                            break
                    if found:
                        continue
                    at = f"{x.name} {ws.title} \"{label}\" = {value!r} cited to section {sec_no}"
                    big = isinstance(value, (int, float)) and value >= 100
                    other = [n for _, text in hits
                             for n in re.findall(r"\b\d{1,3}(?:,\d{3})+\b|\b\d{3,}\b", text)]
                    if big and other:
                        emit("ERROR", f"[G6] {at}, but that section states {', '.join(sorted(set(other)))} "
                                      "and not this figure - the golden cites a clause for a value it "
                                      "took from somewhere else, which the platform's golden_source_fidelity "
                                      "axis reads as the golden contradicting its own source "
                                      "(2026-09-03: bin cubes cited to WH-4 section 7 came off the "
                                      "location master). Name the actual source, and make the documents agree")
                    else:
                        print(f"        info: [G6] {at}, and the section does not state it - confirm "
                              "the value is derived from that section and word the source as the "
                              "derivation")


@check(codes=['G4'], rules=['GOLD-FID'], needs=['inputs', 'solution'], params=['folder'])
def check_register_shortbill(folder):
    """Every input register line billed under the golden's own agreement price appears on a golden row pairing the order and item with the correction.

    Since: 2026-09-01.
    Source: AutoEval golden_source_fidelity 2/5.
    """
    import csv as _csv
    agree = _g4_agreement_map(folder)
    inp = folder / "inputs"
    if not agree or not inp.is_dir():
        return
    short = []  # (order, item, qty, billed, agreement)
    for path in sorted(inp.glob("*.csv")):
        try:
            with open(path, newline="", encoding="utf-8-sig") as f:
                rows = list(_csv.reader(f))
        except Exception:
            continue
        if not rows or len(rows) < 2:
            continue
        heads = [h.strip() for h in rows[0]]
        def col(rx):
            return next((i for i, h in enumerate(heads) if rx.match(h)), None)
        ci, cq, cp = col(_G4_ITEM_H_RE), col(_G4_QTY_H_RE), col(_G4_PRICE_H_RE)
        co, cu = col(_G4_ORDER_H_RE), col(_G4_UOM_H_RE)
        if None in (ci, cq, cp, co):
            continue
        for row in rows[1:]:
            if len(row) <= max(ci, cq, cp, co):
                continue
            item = row[ci].strip().upper()
            uom = row[cu].strip().upper() if cu is not None and row[cu].strip() else None
            key = (item, uom) if (item, uom) in agree else (item, None)
            if key not in agree:
                continue
            try:
                billed, qty = float(row[cp]), float(row[cq])
            except ValueError:
                continue
            gap = agree[key] - billed
            if gap >= 0.005:
                short.append((row[co].strip(), item, qty, billed, agree[key]))
    if not short:
        return
    # each shortbilled line must sit on a golden row pairing order + item + context
    sol = folder / "solution"
    for path in sorted(sol.glob("*.xlsx")):
        try:
            vwb = workbook(path, data_only=True)
        except Exception:
            continue
        for order, item, qty, billed, agreement in list(short):
            gap = round(agreement - billed, 2)
            ext = round(gap * qty, 2)
            found = False
            for ws in vwb.worksheets:
                for wsrow in ws.iter_rows():
                    toks, nums = set(), []
                    for c in wsrow:
                        v = c.value
                        if v is None:
                            continue
                        if isinstance(v, (int, float)) and not isinstance(v, bool):
                            nums.append(float(v))
                            toks.add(f"{v:g}")
                        else:
                            toks.add(str(v).strip().upper())
                    if (order in toks or f"{float(order):g}" in toks) and item in toks:
                        if any(abs(n - t) < 0.005 for n in nums
                               for t in (agreement, gap, ext)):
                            found = True
                            break
                if found:
                    break
            if found:
                short.remove((order, item, qty, billed, agreement))
    for order, item, qty, billed, agreement in short:
        emit("ERROR", f"[G4] the input register bills order {order} line {item} at "
                      f"{billed:g} against the golden's own agreement price {agreement:g} "
                      f"({round(agreement - billed, 2):g}/unit short), and no golden row "
                      "pairs that order and item with the agreement price or the gap - "
                      "the correcting-invoice sweep missed it, which is a "
                      "hard fail (2026-09-01, AutoEval "
                      "golden_source_fidelity 2/5: a P10453 line mis-keyed at the load "
                      "was flagged on the Items and File Fixes tabs yet absent from the "
                      "Summary's correcting table, understating the stated total by 44%). "
                      "Surface every below-agreement register line where the correction "
                      "lives, or say why it stays")


@check(codes=['G1'], rules=['GOLD-FID'], needs=['solution'], params=['folder'])
def check_action_contradiction(folder):
    """No solution row carries a stays-as-placed status in one cell and a change instruction in another.

    G1: a solution row that carries a stays-as-placed status in one cell and an
    imperative change instruction in another.

    An AutoEval hard fail (2026-08-24, golden_source_fidelity 2/5): the
    Purchase Orders tab read line 26's status from the schedule as DE MINIMIS (rides
    the five percent allowance, delivered as placed) while the typed action cell two
    columns over said CHANGE TO RW-D — mutually exclusive outcomes on one row, and
    the Briefing repeated the wrong one. The judge recomputes both paths and scores
    the contradiction against fidelity, not against either figure.

    Tokens are matched uppercase-only so status labels and action verbs fire and
    narrative prose ("Change the 8IN and 6IN RW valve lines...") does not.
    """
    d = folder / "solution"
    if not d.is_dir():
        return
    for path in sorted(d.glob("*.xlsx")):
        try:
            wb = workbook(path, data_only=True)
        except Exception:
            continue
        for ws in wb.worksheets:
            for r, row in enumerate(ws.iter_rows(values_only=True), 1):
                cells = [(i + 1, v.strip()) for i, v in enumerate(row)
                         if isinstance(v, str) and v.strip()]
                statuses = [v for _, v in cells if v in STAY_STATUSES]
                keeps = [v for _, v in cells if v == "KEEP"]
                subs = [v for _, v in cells if v == "SUBSTITUTE"]
                actions = [v for _, v in cells if ACTION_TOKEN_RE.match(v)]
                if statuses and actions:
                    emit("ERROR", f"[G1] {path.name} '{ws.title}' row {r}: status "
                                  f"{statuses[0]!r} beside action {actions[0]!r} — the two "
                                  "outcomes are mutually exclusive and the judge scores the "
                                  "contradiction against golden source fidelity (a "
                                  "hard fail, 2026-08-24). Make one of them the canonical "
                                  "resolution everywhere")
                if subs and keeps:
                    emit("ERROR", f"[G1] {path.name} '{ws.title}' row {r}: status 'SUBSTITUTE' "
                                  "beside action 'KEEP' — a replaced line cannot stay as "
                                  "placed; align the action tabs with the schedule "
                                  "(same class, 2026-08-24)")
        wb.close()


# ---- G8 / G9 / G10: a grader's literal read of the golden ---------------------------
# A task REJECTED 2026-09-05 with seven golden findings
# the gate never saw, because every fidelity check then read the rubric against the golden or
# the golden against itself. Three of the seven are mechanical:
#   G8   the prompt says the deliverable is to be SIGNED and the golden carries no signature
#        line ("Missing ... purchase order, signature block for Darrell to sign")
#   G9   the deliverable is dated later than an action it schedules as done ("Dated 9/22 but
#        schedules work for 9/16-17")
#   G10  an identifier the golden cites (invoice, PO, work order) does not exist in the inputs
#        ("Wrong repair invoice numbers in inspection tab for U-05, 01, 04, and 02")
# The other four are a read (docs/submission/workflows/04-golden-solution.md, "The reviewer's
# read"): a fact date inferred from adjacent records, a same-day-fix rule not applied to its
# class, a "cost since <date>" that skips the partial period, and an asset carrying duties
# after the day it leaves.


def _solution_text_in_order(folder):
    """(where, text) for every string cell / paragraph of the solution files, document order."""
    from ..common import _docx_text, solution_files
    out = []
    for x in solution_files(folder, {".xlsx"}):
        out.extend((f"{x.name} {w}", t) for w, t in _all_text_cells(x))
    for d in solution_files(folder, {".docx"}):
        for i, para in enumerate(_docx_text(d).split("\n")):
            if para.strip():
                out.append((f"{d.name} para {i + 1}", para))
    return out


_inputs_text = input_texts      # the shared extractor (common.input_texts), kept under its old name here


# the DELIVERABLE is what gets signed: "ready for him to sign", "signs from it", "Wade signs the
# scrap", "goes out over my signature" - never an input that "was signed" or "to be signed by
# September 4", and never a "sign-out sheet"
_G8_SIGN_RE = re.compile(r"(?<![\w-])(?:to sign\b|signs? (?:it|from it|off|the \w+)\b|for (?:\w+ )?(?:to )?sign(?:ature)?\b"
                         r"|over (?:my|his|her|their) signature\b|ready (?:for|to) sign\b|signature (?:block|line|page)\b)", re.I)
# a signature LINE, not a mention of one: one golden said "ready for Darrell's signature on
# September 25" and carried nothing to sign
_G8_BLOCK_RE = re.compile(r"_{5,}|\bsignature\s*:|\bsigned\s*:|\bsign here\b|\b(?:approved|authori[sz]ed|accepted) by\s*:"
                          r"|\bsignature (?:line|block)\b|/s/", re.I)


@check(codes=['G8'], rules=['GOLD-FID'], needs=['prompt', 'solution'], params=['folder'])
def check_signature_block(folder):
    """When the prompt says who signs the deliverable, the golden carries a signature line."""
    p = folder / "prompt.md"
    if not p.is_file():
        return
    prompt = p.read_text(encoding="utf-8", errors="ignore")
    m = _G8_SIGN_RE.search(prompt)
    if not m:
        return
    texts = _solution_text_in_order(folder)
    if not texts:
        return
    if any(_G8_BLOCK_RE.search(t) for _, t in texts):
        return
    emit("ERROR", f'[G8] the prompt says the deliverable is to be signed ("...{prompt[max(0, m.start() - 40):m.end() + 40].strip()}...") '
                  "and no solution file carries a signature line (a Signature / ____ / approved-by block). "
                  "a task was rejected for \"Missing tables summarizing order and elections notice, "
                  "purchase order, signature block for Darrell to sign\" (2026-09-05): when the prompt says a "
                  "document is signed, the golden carries THAT document with addressee, reference, lines and a "
                  "signature-and-date line, not a table about it")


_G9_MONTHS = "|".join(MONTH_NAMES)      # capitalised, matched case-sensitively
_G9_LONG_RE = re.compile(rf"\b({_G9_MONTHS}) (\d{{1,2}}), (20\d\d)\b")
_G9_SHORT_RE = re.compile(r"(?<![\d/])(\d{1,2})/(\d{1,2})/(\d{2}|20\d\d)(?![\d/])")


def _g9_date(m, long):
    import datetime
    try:
        if long:
            mon = MONTH_NAMES.index(m.group(1)) + 1
            return datetime.date(int(m.group(3)), mon, int(m.group(2)))
        y = int(m.group(3))
        y = y + 2000 if y < 100 else y
        return datetime.date(y, int(m.group(1)), int(m.group(2)))
    except ValueError:
        return None


def _g9_input_clock(folder):
    """The latest dcterms:modified over the input Office files, as a date."""
    import datetime
    latest = None
    ind = folder / "inputs"
    for f in sorted(ind.glob("*")) if ind.is_dir() else []:
        if f.suffix not in {".docx", ".xlsx", ".pptx"}:
            continue
        try:
            with zipfile.ZipFile(f) as z:
                core = z.read("docProps/core.xml").decode("utf-8", "ignore")
        except Exception:
            continue
        m = re.search(r"<dcterms:modified[^>]*>(\d{4})-(\d{2})-(\d{2})", core)
        if m:
            d = datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
            latest = d if latest is None or d > latest else latest
    return latest


@check(codes=['G9'], rules=['GOLD-FID'], needs=['inputs', 'solution'], params=['folder'])
def check_actions_before_document_date(folder):
    """The deliverable is dated no later than the actions it schedules after the inputs' clock."""
    texts = _solution_text_in_order(folder)
    doc_date = None
    doc_where = None
    for where, t in texts[:40]:
        m = _G9_LONG_RE.search(t)
        if m:
            doc_date, doc_where = _g9_date(m, True), where
            break
    if not doc_date:
        return
    floor = _g9_input_clock(folder)
    p = folder / "prompt.md"
    if p.is_file():
        for m in _G9_LONG_RE.finditer(p.read_text(encoding="utf-8", errors="ignore")):
            d = _g9_date(m, True)
            if d and d < doc_date and (floor is None or d > floor):
                floor = d
    if floor is None or floor >= doc_date:
        return
    hits = {}
    for where, t in texts:
        for m in _G9_SHORT_RE.finditer(t):
            d = _g9_date(m, False)
            if d and floor < d < doc_date:
                hits.setdefault(d, where)
        for m in _G9_LONG_RE.finditer(t):
            d = _g9_date(m, True)
            if d and floor < d < doc_date:
                hits.setdefault(d, where)
    if hits:
        listed = "; ".join(f"{d.strftime('%m/%d/%y')} at {w}" for d, w in sorted(hits.items())[:6])
        emit("ERROR", f"[G9] the deliverable is dated {doc_date.strftime('%m/%d/%y')} ({doc_where}) but "
                      f"schedules or records {len(hits)} date(s) after the inputs' clock "
                      f"({floor.strftime('%m/%d/%y')}) and before its own date: {listed}. "
                      "a task was rejected for \"Dated 9/22 but schedules work for 9/16-17\" "
                      "(2026-09-05): date the deliverable the day the work is done, and every \"today\" "
                      "action on or after that date")


_G10_ID_RE = re.compile(r"\b([A-Z]{1,4})-?(\d{4,7})\b")

# G10 year-sequence arm (2026-09-15): a grader called the
# golden's "Our reference WD-2026-0114" a value that "appears in no input file". The family test
# above never saw it, because no input carries a WD- identifier at all. A PREFIX-YEAR-SEQUENCE
# reference is the shape of a document number an author mints; typed in a golden, it must be
# carried by an input or by the prompt. Probed over 51 goldens: two hits, this one and
# another golden's BID-2026-0447.
_G10_YEAR_SEQ_RE = re.compile(r"\b([A-Z]{2,5})-(20\d\d)-(\d{3,5})\b")


def _g10_year_sequence_refs(folder):
    """G10 year-sequence arm: a typed PREFIX-YEAR-SEQUENCE reference neither an input nor the prompt carries."""
    from pathlib import Path as _P
    folder = _P(folder)
    src = "\n".join(t for _, t in _inputs_text(folder))
    pr = folder / "prompt.md"
    if pr.exists():
        src += "\n" + pr.read_text(encoding="utf-8", errors="ignore")
    from ..common import solution_files
    formula_cells = set()
    for x in solution_files(folder, {".xlsx"}):
        try:
            fwb = workbook(x)
        except Exception:
            continue
        for ws in fwb.worksheets:
            for row in ws.iter_rows():
                for c in row:
                    if isinstance(c.value, str) and c.value.startswith("="):
                        formula_cells.add(f"{x.name} {ws.title}!{c.coordinate}")
        fwb.close()
    missing = {}
    for where, t in _solution_text_in_order(folder):
        if where in formula_cells:
            continue
        for m in _G10_YEAR_SEQ_RE.finditer(t):
            if m.group(0) not in src:
                missing.setdefault(m.group(0), where)
    if missing:
        listed = "; ".join(f"{k} ({w})" for k, w in list(missing.items())[:8])
        emit("ERROR", f"[G10] {len(missing)} year-sequence reference(s) the golden types carry no source in any "
                      f"input or the prompt: {listed}. A grader returned \"Our reference WD-2026-0114\" as a value "
                      "that appears in no input file (2026-09-15). Give the reference "
                      "its source, in the prompt where the requester would know it or in the input that issues it, "
                      "or leave the number out")



@check(codes=['G10'], rules=['GOLD-FID'], needs=['inputs', 'solution', 'prompt'], params=['folder'])
def check_cited_identifiers(folder):
    """Every invoice, PO or work-order style identifier the golden cites appears in an input.

    Drift-notes: tightened 2026-09-15: a typed
    year-sequence reference (WD-2026-0114, BID-2026-0447) in a family no input carries was never
    caught, because the family test needs the prefix in an input. Such a reference is flagged when
    neither an input nor the prompt carries the full string.
    """
    _g10_year_sequence_refs(folder)
    known = {}
    for _, text in _inputs_text(folder):
        for m in _G10_ID_RE.finditer(text):
            known.setdefault(m.group(1), set()).add(m.group(1) + m.group(2))
    if not known:
        return
    # an id the golden BUILDS by formula from input data (="VRM-"&RIGHT(F99,4) on a part key
    # the cross-reference does not carry) is derived and reproducible, never remembered - the
    # renumbering defect this check exists for lives only in TYPED ids (2026-09-07: eight
    # normalized part keys of the task's RET-PART device)
    from ..common import solution_files
    formula_cells = set()
    for x in solution_files(folder, {".xlsx"}):
        try:
            fwb = workbook(x)
        except Exception:
            continue
        for ws in fwb.worksheets:
            for row in ws.iter_rows():
                for c in row:
                    if isinstance(c.value, str) and c.value.startswith("="):
                        formula_cells.add(f"{x.name} {ws.title}!{c.coordinate}")
        fwb.close()
    missing = {}
    for where, t in _solution_text_in_order(folder):
        if where in formula_cells:
            continue
        for m in _G10_ID_RE.finditer(t):
            fam = m.group(1)
            if fam in known and (fam + m.group(2)) not in known[fam]:
                missing.setdefault(m.group(0), where)
    if missing:
        listed = "; ".join(f"{k} ({w})" for k, w in list(missing.items())[:8])
        emit("ERROR", f"[G10] {len(missing)} identifier(s) the golden cites exist in no input, although the "
                      f"inputs carry the same family: {listed}. A task was rejected for \"Wrong "
                      "repair invoice numbers in inspection tab for U-05, 01, 04, and 02\" (2026-09-05): the "
                      "generator renumbered the invoices after the golden text was written. Every cited "
                      "identifier is looked up in the shipped input, never remembered; a deliberately new "
                      "number (a PO the golden issues) goes in .gate-debt with the sequence it continues")


# "claim" is deliberately absent: a Claim Recap / Warranty Claims tab is a register the golden
# FILES with a vendor or carrier, not an answer to correspondence
_G14_SHEET_RE = re.compile(r"dispute|complaint|question|inquir", re.I)
_G14_NAME_COLS = {"ACCOUNT", "NAME", "ACCOUNT_NAME", "CUSTOMER", "CUSTOMER_NAME", "VENDOR", "VENDOR_NAME",
                  "SUPPLIER", "SUPPLIER_NAME", "CARRIER", "CARRIER_NAME", "CLAIMANT"}


def _g14_entity_names(folder):
    """Multi-word proper names from the inputs' name-like columns (csv and xlsx headers)."""
    import csv as _csv
    names = set()
    ind = folder / "inputs"
    if not ind.is_dir():
        return names

    def take(header, rows):
        idx = [i for i, h in enumerate(header) if re.sub(r"_\d+$", "", str(h or "").strip().upper()) in _G14_NAME_COLS]
        for r in rows:
            for i in idx:
                if i < len(r):
                    v = str(r[i] or "").strip()
                    if " " in v and re.fullmatch(r"[A-Za-z][A-Za-z0-9'&.\- ]{3,60}", v):
                        names.add(v)

    for f in sorted(ind.iterdir()):
        if f.suffix == ".csv":
            with open(f, newline="", encoding="utf-8", errors="ignore") as fh:
                rows = list(_csv.reader(fh))
            if rows:
                take(rows[0], rows[1:])
        elif f.suffix == ".xlsx":
            try:
                wb = workbook(f, data_only=True)
            except Exception:
                continue
            for ws in wb.worksheets:
                rows = [[c for c in r] for r in ws.iter_rows(values_only=True)]
                for k, r in enumerate(rows[:5]):
                    if any(str(h or "").strip().upper() in _G14_NAME_COLS for h in r):
                        take(r, rows[k + 1:])
                        break
            wb.close()
    return names


@check(codes=['G14'], rules=['GOLD-FID'], needs=['inputs', 'solution'], params=['folder'])
def check_dispute_entities(folder):
    """Every account a golden dispute or claim tab adjudicates is one the correspondence names.

    G14 (2026-09-05, AutoEval golden_source_fidelity 2/5): the golden's
    Disputes tab answered Boyd's bonus claim on Horse Cave Cafe, the account his statement had
    paid the bonus on, while his email in commission_disputes.docx named Cave City Diner, another
    representative's account that cleared the test. The answer was right on the figures and
    wrong on the name the claimant used, and the judge read the stated basis as fabricated. A
    dispute / claim / complaint tab in the golden answers what the correspondence says, so every
    account-style entity it names must appear in a correspondence input (a docx carrying From:
    and Subject: or Sent: lines). One direction only: an email may name accounts the golden
    does not adjudicate (a question that is not a dispute), but the golden cannot adjudicate an
    account no email named. The tab must be anchored to the correspondence (at least one account
    it names is one an email named), so a claims register with no email behind it is skipped."""
    from ..common import _docx_text, solution_files
    corr = []
    ind = folder / "inputs"
    for f in sorted(ind.glob("*.docx")) if ind.is_dir() else []:
        t = _docx_text(f)
        if "From:" in t and ("Subject:" in t or "Sent:" in t):
            corr.append(t.lower())
    if not corr:
        return
    names = _g14_entity_names(folder)
    if not names:
        return
    missing, anchored = {}, False
    for x in solution_files(folder, {".xlsx"}):
        try:
            wb = workbook(x, data_only=True)
        except Exception:
            continue
        for ws in wb.worksheets:
            if not _G14_SHEET_RE.search(ws.title):
                continue
            for row in ws.iter_rows():
                for c in row:
                    v = c.value
                    if not isinstance(v, str):
                        continue
                    low = v.lower()
                    for n in names:
                        nl = n.lower()
                        if not re.search(r"(?<![\w])" + re.escape(nl) + r"(?![\w])", low):
                            continue
                        if any(nl in t for t in corr):
                            anchored = True
                        else:
                            missing.setdefault(n, f"{x.name} {ws.title}!{c.coordinate}")
        wb.close()
    # the tab has to be answering the correspondence at all: at least one account it names is one
    # an email named, otherwise it is a register that happens to carry a dispute-like title
    if missing and anchored:
        listed = "; ".join(f"{k} ({w})" for k, w in list(missing.items())[:6])
        emit("ERROR", f"[G14] {len(missing)} account(s) the golden's dispute tab names appear in no "
                      f"correspondence input: {listed}. A task failed golden_source_fidelity "
                      "(2026-09-05) answering Boyd's bonus claim on Horse Cave Cafe when his email named "
                      "Cave City Diner: a dispute answer is read against the claimant's own words, so either "
                      "the email names the account the answer adjudicates, or the answer says which account "
                      "the claimant named and why the ruling lands elsewhere")


# G15 (2026-09-09, a grader's note): the golden's action table assigned the
# dock actions to "Hector Ybarra", a dock lead no input and not the prompt ever named. The
# grader: "this name appears in no input file. Remove it or replace it with a role
# description." A person a golden hands an action to is a fact the judge reads against the
# inputs, like G10's identifiers and G14's accounts: every Firstname Lastname in an owner-style
# column of a solution table (WHO / OWNER / RESPONSIBLE / ASSIGNED TO / LEAD) must appear in the
# prompt or in an input. Title-case roles ("Purchasing Manager") are not names and are the
# sanctioned replacement, so a pair ending in a role or business word is skipped.
_G15_HDR_RE = re.compile(r"^\s*(?:who|owners?|owned by|responsible|responsibility|assigned(?: to)?|assignee"
                         r"|lead|by whom|person|action owner|who does it)\s*$", re.I)
# a greedy title-case span: "Middle Georgia Truck Refrigeration" is one organisation, not two
# people, so a span of three or more words is skipped as a business name
_G15_NAME_RE = re.compile(r"\b([A-Z][a-z]+(?:\s+(?:[A-Z]\.|[A-Z][a-z]+(?:-[A-Z][a-z]+)?)){1,4})\b")
_G15_ROLE_RE = re.compile(
    r"\b(?:Manager|Managers|Lead|Leads|Supervisor|Desk|Team|Department|Dept|Clerk|Buyer|Controller|Dock|Office"
    r"|Group|Accounting|Purchasing|Warehouse|Sales|Operations|Receiving|Shipping|Driver|Drivers|Rep|Representative"
    r"|Coordinator|Director|President|Owner|Staff|Crew|Foreman|Analyst|Specialist|Assistant|Planner|Agent"
    r"|Creamery|Supply|Supplies|Inc|LLC|Co|Company|Corp|Freight|Lines|Foods|Distributors?|Wholesale|Brothers"
    r"|Bank|Mutual|Sanitary|District|Plumbing|Electric|Industries|Manufacturing|Hardware|Logistics|Trucking"
    r"|Transport|Express|Partners|Associates|Services|Systems|Solutions)\b$")
_G15_LEAD_RE = re.compile(r"^(?:The|Our|Each|Every|Any|Both|All|New|Same|Next|First|Second|Third|Not|No)\b")


def _g15_owner_cells(folder):
    """(where, text) for every data cell under an owner-style header in the solution's docx tables
    and xlsx sheets."""
    from ..common import _docx_tables, solution_files
    out = []
    for name, ti, rows in _docx_tables(folder):
        if not rows:
            continue
        cols = [i for i, h in enumerate(rows[0]) if _G15_HDR_RE.match(h or "")]
        for r in rows[1:]:
            for ci in cols:
                if ci < len(r) and r[ci]:
                    out.append((f"{name} table {ti + 1}", r[ci]))
    for x in solution_files(folder, {".xlsx"}):
        try:
            wb = workbook(x, data_only=True)
        except Exception:
            continue
        for ws in wb.worksheets:
            cols = []
            for row in ws.iter_rows(min_row=1, max_row=1):
                cols = [c.column for c in row if isinstance(c.value, str) and _G15_HDR_RE.match(c.value)]
            if not cols:
                continue
            for row in ws.iter_rows(min_row=2):
                for c in row:
                    if c.column in cols and isinstance(c.value, str):
                        out.append((f"{x.name} {ws.title}!{c.coordinate}", c.value))
        wb.close()
    return out


@check(codes=['G15'], rules=['GOLD-FID'], needs=['prompt', 'inputs', 'solution'], params=['folder'])
def check_owner_names_in_inputs(folder):
    """Every person the golden assigns an action to is named in the prompt or an input.

    Since: 2026-09-09.
    Source: a grader.
    """
    cells = _g15_owner_cells(folder)
    if not cells:
        return
    prompt_text = (folder / "prompt.md").read_text(encoding="utf-8") if (folder / "prompt.md").exists() else ""
    corpus = prompt_text + "\n" + "\n".join(t for _, t in _inputs_text(folder))
    missing = {}
    for where, text in cells:
        for m in _G15_NAME_RE.finditer(text):
            nm = re.sub(r"\s+", " ", m.group(1))
            if _G15_ROLE_RE.search(nm) or _G15_LEAD_RE.match(nm):
                continue
            if len([w for w in nm.split() if not w.endswith(".")]) >= 3:
                continue
            if nm in corpus:
                continue
            missing.setdefault(nm, where)
    if missing:
        listed = "; ".join(f"{k} ({w})" for k, w in list(missing.items())[:6])
        emit("ERROR", f"[G15] {len(missing)} person(s) the golden assigns an action to appear in no input "
                      f"and not in the prompt: {listed}. A grader sent the task "
                      "back on an invented dock lead (2026-09-09): a name the inputs never carry reads as "
                      "fabrication. Use a person the inputs name, or a role description in the owner cell")


# G16 (2026-09-10, a grader's note): the golden memo's From line and
# its docProps creator / lastModifiedBy carried "Carla Hershberger", an analyst the prompt
# (first person, unnamed) and the inputs never mention; the grader listed the name as
# fabricated even though it sat in no graded position. G15 reads owner columns; the same rule
# holds for the author fields of a memo (From / Prepared by / Signed / Reviewed by) and for
# the creator stamps of every shipped solution file: each Firstname Lastname must be in the
# prompt or an input, or be a role ("Purchasing and Inventory Analyst" is the sanctioned form
# when the prompt never names the requester).
_G16_LINE_RE = re.compile(r"^\s*(?:From|Prepared by|Author|Signed|Reviewed by|Approved by|Submitted by)"
                          r"\s*:\s*(.+)$", re.I | re.M)
_G16_PROP_RE = re.compile(r"<(?:dc:creator|cp:lastModifiedBy)>([^<]*)<")


def _g16_author_fields(path):
    """(where, text) for the author-style fields of one solution file: memo header lines in a
    docx and the creator / lastModifiedBy stamps of any Office package."""
    import zipfile
    out = []
    if path.suffix.lower() == ".docx":
        try:
            text = "\n".join(p.text for p in document(path).paragraphs)
        except Exception:
            text = ""
        for m in _G16_LINE_RE.finditer(text):
            out.append((f"{path.name} line '{m.group(0).strip()[:40]}'", m.group(1)))
    try:
        with zipfile.ZipFile(path) as z:
            core = z.read("docProps/core.xml").decode("utf-8", "ignore")
    except (KeyError, zipfile.BadZipFile, OSError):
        return out
    for m in _G16_PROP_RE.finditer(core):
        out.append((f"{path.name} docProps", m.group(1)))
    return out


# G16 second surface (2026-09-10, a grader's note): the fabricated
# name sat in a Briefing CELL, "Prepared by Verla Stroman for Stan Hemmen, 08/26/2026", which
# is neither a docx header line nor a colon-led field, so the line regex above never saw it
# (only the docProps stamp fired). The grader called it the one major issue. An
# attribution cue anywhere in the golden's text - a docx paragraph or an xlsx string cell -
# is read the same way as a From line: prepared / signed / reviewed ... by|for <Name>.
# The cue words are case-insensitive, the name is not: under a global re.I the name group
# ran on through "for Stan" and reported "Verla Stroman for Stan".
_G16_CUE_RE = re.compile(r"\b(?i:prepared|written|compiled|built|drafted|signed|approved|reviewed|"
                         r"submitted|authored|issued|assembled|worked up|put together)\s+(?i:by|for)\s+"
                         r"([A-Z][a-z]+(?:\s+(?:[A-Z]\.|[A-Z][a-z]+(?:-[A-Z][a-z]+)?)){1,2})\b")


def _g16_attribution_cells(folder):
    """(where, name) for every attribution cue in the golden's prose, docx paragraphs and xlsx
    string cells alike."""
    from ..common import solution_files, _docx_text
    out = []
    for path in solution_files(folder, {".docx", ".xlsx"}):
        if path.suffix.lower() == ".docx":
            texts = [(path.name, _docx_text(path))]
        else:
            try:
                texts = [(f"{path.name} {w}", t) for w, t in _all_text_cells(path)]
            except Exception:
                texts = []
        for where, text in texts:
            for m in _G16_CUE_RE.finditer(text):
                out.append((f"{where} '{m.group(0)[:50]}'", m.group(1)))
    return out


@check(codes=['G16'], rules=['GOLD-FID'], needs=['prompt', 'inputs', 'solution'], params=['folder'])
def check_author_names_in_inputs(folder):
    """Every person a memo author line, an attribution cue or a docProps creator names appears in an input or the prompt.

    G16 - a memo author line, an attribution cue in the golden's prose, or a docProps creator
    names a person no input and not the prompt names."""
    from ..common import solution_files
    fields = []
    for path in solution_files(folder, {".docx", ".xlsx"}):
        fields.extend(_g16_author_fields(path))
    fields.extend(_g16_attribution_cells(folder))
    if not fields:
        return
    prompt_text = (folder / "prompt.md").read_text(encoding="utf-8") if (folder / "prompt.md").exists() else ""
    corpus = prompt_text + "\n" + "\n".join(t for _, t in _inputs_text(folder))
    missing = {}
    for where, text in fields:
        for m in _G15_NAME_RE.finditer(text):
            nm = re.sub(r"\s+", " ", m.group(1))
            if _G15_ROLE_RE.search(nm) or _G15_LEAD_RE.match(nm):
                continue
            if len([w for w in nm.split() if not w.endswith(".")]) >= 3:
                continue
            if nm in corpus:
                continue
            missing.setdefault(nm, where)
    if missing:
        listed = "; ".join(f"{k} ({w})" for k, w in list(missing.items())[:6])
        emit("ERROR", f"[G16] {len(missing)} author name(s) on the golden appear in no input and not in the "
                      f"prompt: {listed}. A grader listed such a From-line name "
                      "as fabricated (2026-09-10) although nothing graded it: write the author field as the "
                      "requester's role when the prompt never names them, and set the file's creator and "
                      "lastModifiedBy stamps to the same")


# G17 (2026-09-10, a grader's note): the golden memo's header gave
# Randy Tackett as "General Manager", Sherry Adkins as "Counter Manager" and Jenna Caudill as
# "Purchasing and Inventory Analyst". No input carried any of the three (the procedure names
# Dwayne Sizemore as warehouse manager and nothing else), and the grader listed them as
# the memo's only unsupported claims after tracing every other name, date and figure. G16
# anchors the person on a header line; this anchors the TITLE bound to a person there
# ("Name, Title" on a To / Cc / From / Prepared-for line) to the prompt or an input, read
# case-insensitively as a phrase. A title standing alone (G16's role form for an unnamed
# requester) carries no name and is not read; a trailing company name passes when the
# inputs name the company.
_G17_LINE_RE = re.compile(r"^\s*(?:To|Cc|From|Prepared (?:by|for)|Author|Signed|Reviewed by|Approved by"
                          r"|Submitted by|Attention|Attn)\s*:\s*(.+)$", re.I | re.M)
# A one-cell header on an xlsx briefing runs several labels together ("To: Gail (Purchasing
# Manager) · ROA / LYN / DAN branch GMs      From: Tom Marsh, Purchasing & Inventory Analysis
# August 17, 2026"), so a cell is cut at every label and each labelled chunk is then split on
# the separators such a line uses (a middle dot, a pipe, a semicolon, a run of spaces).
_G17_LABEL_RE = re.compile(r"(?:^|(?<=\s))(To|Cc|From|Prepared (?:by|for)|Author|Signed|Reviewed by|Approved by"
                           r"|Submitted by|Attention|Attn)\s*:\s*", re.I)
_G17_SPLIT_RE = re.compile(r"\s{3,}|\s[·|]\s|;|\t")
_G17_NAME = r"([A-Z][a-z]+(?:\s+(?:[A-Z]\.|[A-Z][a-z]+(?:-[A-Z][a-z]+)?)){0,3})"
_G17_PAIR_RE = re.compile(r"^\s*" + _G17_NAME + r"\s*,\s*(.+?)\s*$")
_G17_PAREN_RE = re.compile(r"^\s*" + _G17_NAME + r"\s*\(\s*([^()]+?)\s*\)\s*$")


def _g17_pairs_from_text(where, text):
    """(where, name, title) for every 'Name, Title' or 'Name (Title)' segment of the labelled chunks of text."""
    out = []
    labels = list(_G17_LABEL_RE.finditer(text))
    for i, m in enumerate(labels):
        chunk = text[m.end():labels[i + 1].start() if i + 1 < len(labels) else len(text)]
        for seg in _G17_SPLIT_RE.split(chunk):
            pm = _G17_PAREN_RE.match(seg) or _G17_PAIR_RE.match(seg)
            if not pm:
                continue
            title = re.sub(r"\s+", " ", pm.group(2)).strip(" .")
            if not title or re.search(r"\d", title) or len(title.split()) > 6:
                continue
            out.append((where, pm.group(1), title))
    return out


def _g17_title_pairs(path):
    """(where, name, title) for every titled person on a memo header line (docx) or a header cell (xlsx)."""
    out = []
    if path.suffix.lower() == ".docx":
        try:
            paras = [p.text for p in document(path).paragraphs]
        except Exception:
            return out
        for t in paras:
            if _G17_LINE_RE.match(t):
                out.extend(_g17_pairs_from_text(f"{path.name} line '{t.strip()[:40]}'", t))
        return out
    if path.suffix.lower() == ".xlsx":
        try:
            import openpyxl
            wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        except Exception:
            return out
        for ws in wb.worksheets:
            for row in ws.iter_rows(max_row=12):
                for c in row:
                    v = c.value
                    if isinstance(v, str) and _G17_LABEL_RE.search(v):
                        out.extend(_g17_pairs_from_text(f"{path.name} {ws.title}!{c.coordinate}", v))
        wb.close()
    return out


def _g17_norm(text):
    import html
    # _inputs_text hands back raw XML entities (&amp;, &lt;), so unescape before the ampersand is spelled out
    return re.sub(r"\s+", " ", html.unescape(text).replace("&", "and")).lower()


def _g17_bound(corpus, name, title):
    """True when the title phrase sits within 160 characters of the person's name somewhere in the corpus."""
    t = _g17_norm(title)
    toks = [w for w in _g17_norm(name).split() if len(w) > 1 and not w.endswith(".")]
    for m in re.finditer(re.escape(t), corpus):
        window = corpus[max(0, m.start() - 160): m.end() + 160]
        if any(re.search(r"\b" + re.escape(w) + r"\b", window) for w in toks):
            return True
    return False


@check(codes=['G17'], rules=['GOLD-FID'], needs=['prompt', 'inputs', 'solution'], params=['folder'])
def check_header_titles_in_inputs(folder):
    """A header line on the golden gives a named person only a title an input or the prompt states beside that name.

    Since: 2026-09-10 (docx memo headers, the title phrase anywhere in the corpus).
    Tightened: 2026-09-14: xlsx header cells are read,
    'Name (Title)' is a pair, and the title must sit within 160 characters of the name in the
    prompt or an input. The original briefing carried 'To: Gail (Purchasing Manager)' on an
    xlsx cell while the email said only 'my purchasing manager' and the policy 'the purchasing
    manager'; the phrase existed, the binding did not, and a grader traced it three times
    running as inferred rather than sourced.
    """
    from ..common import solution_files
    pairs = []
    for path in solution_files(folder, {".docx", ".xlsx"}):
        pairs.extend(_g17_title_pairs(path))
    if not pairs:
        return
    prompt_text = (folder / "prompt.md").read_text(encoding="utf-8") if (folder / "prompt.md").exists() else ""
    corpus = _g17_norm(prompt_text + "\n" + "\n".join(t for _, t in _inputs_text(folder)))
    missing = {}
    for where, name, title in pairs:
        if _g17_norm(title) not in corpus:
            missing.setdefault(f"{name}, {title} (title nowhere)", where)
        elif not _g17_bound(corpus, name, title):
            missing.setdefault(f"{name}, {title} (title never beside the name)", where)
    if missing:
        listed = "; ".join(f"{k} ({w})" for k, w in list(missing.items())[:6])
        emit("ERROR", f"[G17] {len(missing)} header title(s) on the golden are not stated beside that person's "
                      f"name in any input or the prompt: {listed}. A grader "
                      "(2026-09-10) listed three unsupported memo titles as fabrications, and a grader "
                      "(2026-09-12 to 09-14) traced a briefing's 'Gail (Purchasing Manager)' to an email "
                      "saying only 'my purchasing manager' and called it inferred, not sourced: give a named person "
                      "only a title an input or the prompt states beside their name, or none")


# G18 (2026-09-10, a grader's note): "four action-item dates are
# planning dates with no input anchor". The golden's action list gave the agreement signing
# 08/28, the portal test 09/04, the first statement audit 10/09 and the spring return list
# 01/15/2027; none of the four stands in any input or in the prompt, while the load date
# (Tammy's "Tuesday, September 8") and the memo's "Wednesday the 26th" do. The grader's
# stated method is that every claim traces to the exact input source, and a date on a row that
# also carries an owner is a claim. Anchors are read generously: a full date in any common
# form, a month-day without a year ("September 8"), a bare day ("the 26th"), an ordinal
# weekday ("the first Tuesday of the month") resolved in every month of the corpus year, and
# "the end of <month>". Rows with no owner cell are not read (a schedule table is data, not a
# commitment), which keeps the check silent on one task's remittance dates.
# Probed portfolio-wide on 2026-09-10 before coding: exactly the four flagged rows on this
# task, and owner-dated rows on two earlier tasks (3 and 6 of them) that predate
# the check, left as their own debt.
_G18_MONTHS = list(MONTHS_LOWER)
_G18_MON = "|".join(_G18_MONTHS + [m[:3] for m in _G18_MONTHS])
_G18_WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


def _g18_mon(tok):
    return month_number(tok[:3])


_G18_FULL = [
    (re.compile(r"\b(\d{1,2})/(\d{1,2})/(\d{4})\b"), lambda m: (int(m[3]), int(m[1]), int(m[2]))),
    # mm/dd/yy, the form a CSV export carries (a task's invoice dates read 04/07/26 and
    # G20 called the memo's "April 7, 2026" unsupported, 2026-09-10)
    (re.compile(r"\b(\d{1,2})/(\d{1,2})/(\d{2})\b(?!\d)"), lambda m: (2000 + int(m[3]), int(m[1]), int(m[2]))),
    (re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b"), lambda m: (int(m[1]), int(m[2]), int(m[3]))),
    (re.compile(r"\b(" + _G18_MON + r")\.? (\d{1,2})(?:st|nd|rd|th)?,? (\d{4})\b", re.I),
     lambda m: (int(m[3]), _g18_mon(m[1]), int(m[2]))),
    (re.compile(r"\b(\d{1,2})(?:st|nd|rd|th)? (" + _G18_MON + r")\.?,? (\d{4})\b", re.I),
     lambda m: (int(m[3]), _g18_mon(m[2]), int(m[1]))),
]
_G18_PART = [
    (re.compile(r"\b(" + _G18_MON + r")\.? (\d{1,2})(?:st|nd|rd|th)?\b(?!,? \d{4})", re.I),
     lambda m: (_g18_mon(m[1]), int(m[2]))),
    (re.compile(r"\b(\d{1,2})(?:st|nd|rd|th)? (" + _G18_MON + r")\b(?!,? \d{4})", re.I),
     lambda m: (_g18_mon(m[2]), int(m[1]))),
    (re.compile(r"\b(\d{1,2})/(\d{1,2})\b(?!/)"), lambda m: (int(m[1]), int(m[2]))),
]
_G18_DAYONLY_RE = re.compile(r"\bthe (\d{1,2})(?:st|nd|rd|th)\b")
_G18_ORD_RE = re.compile(r"\b(first|second|third|fourth|last) (" + "|".join(_G18_WEEKDAYS) + r")\b", re.I)
_G18_ENDOF_RE = re.compile(r"\b(?:end|last day) of ("
                           + "|".join(_G18_MONTHS) + r")\b", re.I)
_G18_NAME_CELL_RE = re.compile(r"^[A-Z][a-z]+(?: [A-Z]\.)? [A-Z][a-z]+(?:-[A-Z][a-z]+)?$")


def _g18_full_dates(text):
    import datetime
    out = set()
    for rx, f in _G18_FULL:
        for m in rx.finditer(text):
            try:
                y, mo, d = f(m)
                datetime.date(y, mo, d)
                out.add((y, mo, d))
            except (ValueError, IndexError):
                pass
    return out


def _g18_anchors(corpus):
    """(full dates, month-day pairs, bare days) the prompt and inputs carry, ordinal weekdays
    and month ends resolved into full dates."""
    import calendar
    import datetime
    fd = _g18_full_dates(corpus)
    years = {y for y, _, _ in fd} or {datetime.date.today().year}
    md, days = set(), set()
    for rx, f in _G18_PART:
        for m in rx.finditer(corpus):
            try:
                md.add(f(m))
            except (ValueError, IndexError):
                pass
    for m in _G18_DAYONLY_RE.finditer(corpus):
        days.add(int(m[1]))
    for m in _G18_ORD_RE.finditer(corpus):
        o = {"first": 0, "second": 1, "third": 2, "fourth": 3, "last": -1}[m[1].lower()]
        wd = _G18_WEEKDAYS.index(m[2].lower())
        for y in years:
            for mo in range(1, 13):
                ds = [d for d in range(1, calendar.monthrange(y, mo)[1] + 1)
                      if datetime.date(y, mo, d).weekday() == wd]
                fd.add((y, mo, ds[o]))
    for m in _G18_ENDOF_RE.finditer(corpus):
        mo = _g18_mon(m[1])
        for y in years:
            fd.add((y, mo, calendar.monthrange(y, mo)[1]))
    return fd, md, days


def _g18_owner_dated_rows(folder):
    """(where, dates) for every golden row that carries both an owner-style cell (a bare
    Firstname Lastname, or a short role) and a bare date cell."""
    import datetime
    from ..common import solution_files, _docx_tables
    rows = []
    for p in solution_files(folder, {".xlsx"}):
        try:
            wb = workbook(p, data_only=True)
        except Exception:
            continue
        for ws in wb.worksheets:
            for row in ws.iter_rows():
                live = [c for c in row if c.value is not None]
                if live:
                    # read-only sheets hand back EmptyCell for leading blanks, which has no .row
                    rows.append((f"{p.name} {ws.title}!{live[0].row}", [c.value for c in live]))
        wb.close()
    for name, ti, table in _docx_tables(folder):
        for r in table:
            rows.append((f"{name} table {ti + 1}", [c for c in r if c]))
    out = []
    for where, vals in rows:
        owner = any(isinstance(v, str) and len(v.split()) <= 4
                    and (_G18_NAME_CELL_RE.match(v.strip()) or _G15_ROLE_RE.search(v.strip()))
                    for v in vals)
        if not owner:
            continue
        ds = set()
        for v in vals:
            if isinstance(v, datetime.datetime):
                ds.add((v.year, v.month, v.day))
            elif isinstance(v, str) and len(v.strip()) <= 14:
                ds |= _g18_full_dates(v)
        if ds:
            out.append((where, ds))
    return out


@check(codes=['G18'], rules=['GOLD-FID'], needs=['prompt', 'inputs', 'solution'], params=['folder'])
def check_action_dates_anchored(folder):
    """A date on a golden row that names an owner stands in an input or the prompt."""
    rows = _g18_owner_dated_rows(folder)
    if not rows:
        return
    prompt_text = (folder / "prompt.md").read_text(encoding="utf-8") if (folder / "prompt.md").exists() else ""
    corpus = prompt_text + "\n" + "\n".join(t for _, t in _inputs_text(folder))
    fd, md, days = _g18_anchors(corpus)
    bad = []
    for where, ds in rows:
        for y, mo, d in sorted(ds):
            if (y, mo, d) in fd or (mo, d) in md or d in days:
                continue
            bad.append(f"{where} {mo:02d}/{d:02d}/{y}")
    if bad:
        emit("ERROR", f"[G18] {len(bad)} owner-dated row(s) on the golden carry a date no input and not the "
                      f"prompt states: {'; '.join(bad[:6])}. A grader listed "
                      "four such action dates as planning dates with no input anchor (2026-09-10): date each "
                      "action off something the inputs say (a stated load day, a visit, a window end, a "
                      "deadline the memo names) and say the anchor in the action's own text, or leave the "
                      "date off the row")


# G19 (2026-09-10): the golden's Representative Notes said
# "Dwight's quarter moves up" and "Frank's quarter moves down" while the Review tab's CORRECTION
# column carried -190.54 and +407.25, and a grader sent the task back for material
# contradictions in representative-facing text that "could misinform employees", asking for a
# consistency criterion as well. The prose had been written against an earlier generation of the
# data and never re-read against the final tab. The mechanical half: a sentence of the form
# "<First name>'s quarter moves up/down" is a signed claim about one row of a table that carries a
# name column and a correction-style column, and the sign of that row's figure decides it. Only
# the up/down form is read; "overpaid"/"underpaid" depends on a sign convention the header does
# not state. First names shared by two rows are skipped.
_G19_DIR_RE = re.compile(r"\b([A-Z][a-z]+)(?:'s)?\s+(?:quarter|statement|commission|pay|total|correction|"
                         r"number|figure|net|share|balance)\s+(?:moves|goes|comes|went|is|was|ends up|lands)"
                         r"\s+(up|down)\b")
_G19_VAL_HDR_RE = re.compile(r"^\s*(?:corrections?|adjustments?|variance|difference|net change|change|movement)\s*$", re.I)
_G19_NAME_HDR_RE = re.compile(r"^\s*(?:name|rep|representative|employee|person|buyer|driver|customer|vendor|supplier)\s*$", re.I)


def _g19_signed_rows(path):
    """first name -> (where, full name, signed value) from every sheet carrying a name column and a
    correction-style column in its first six rows; a first name two rows share is dropped."""
    out, names = {}, {}
    try:
        wb = workbook(path, data_only=True)
    except Exception:
        return out
    for ws in wb.worksheets:
        # read-only rows are tuples padded with EmptyCell, which carries no column or row, so
        # columns are the tuple index and the row number is counted
        rows = list(ws.iter_rows(values_only=True))
        for ri, row in enumerate(rows[:6]):
            hdr = {ci: v for ci, v in enumerate(row) if isinstance(v, str)}
            name_cols = [k for k, v in hdr.items() if _G19_NAME_HDR_RE.match(v)]
            val_cols = [k for k, v in hdr.items() if _G19_VAL_HDR_RE.match(v)]
            if not name_cols or not val_cols:
                continue
            for di, drow in enumerate(rows[ri + 1:], start=ri + 2):
                cells = dict(enumerate(drow))
                name = next((cells[k] for k in name_cols if isinstance(cells.get(k), str) and " " in cells[k]), None)
                val = next((cells[k] for k in val_cols
                            if isinstance(cells.get(k), (int, float)) and not isinstance(cells.get(k), bool)), None)
                if name is None or val is None:
                    continue
                first = name.split()[0]
                names.setdefault(first, set()).add(name)
                out.setdefault(first, (f"{ws.title} row {di}", name, val))
            break
    wb.close()
    return {k: v for k, v in out.items() if len(names[k]) == 1}


@check(codes=['G19'], rules=['GOLD-FID'], needs=['solution'], params=['folder'])
def check_direction_claims(folder):
    """A prose claim that an item's quarter moves up or down agrees in sign with its correction column."""
    for x in solution_files(folder, {".xlsx"}):
        rows = _g19_signed_rows(x)
        if not rows:
            continue
        for where, text in _xlsx_prose(x):
            for m in _G19_DIR_RE.finditer(text):
                first, direction = m.group(1), m.group(2)
                if first not in rows:
                    continue
                src, name, val = rows[first]
                if val == 0:
                    continue
                if (val > 0) != (direction == "up"):
                    emit("ERROR", f"[G19] {x.name} {where} says \"{m.group(0)}\" while {src} carries {val:g} for "
                                  f"{name} - representative-facing prose contradicting the deliverable's own signed "
                                  "figure. A task went back (2026-09-10) on "
                                  "two such sentences, with the grader noting the text could misinform employees. "
                                  "Re-read every note against the final tab and state the direction the figure carries")


# G20 (2026-09-10): the golden's first page was dated
# "Tuesday, September 1, 2026", a day no input and not the prompt states (the requesting note is
# dated August 28), and a grader asked to "remove or correct the unsupported dates". Rule 2 of
# docs/submission/workflows/04-golden-solution.md already says a date the golden states as fact is
# written in an input or derived by a stated rule; G18 coded it for owner-dated action rows only.
# This is the general form: every full date (month, day and year) a solution prose cell or
# paragraph states must be a full date the prompt or an input carries. Month-day pairs and bare
# months are left to the hand read, and the docProps stamps are not text the grader sees.
_G20_COMMIT_HDR_RE = re.compile(r"^(?:by when|due|due date|target|target date|deadline|complete by|completion date|when)$", re.I)


def _g20_commitment_dates(folder):
    """Full dates sitting in a solution docx table column whose header names a commitment."""
    from ..common import solution_files
    out = set()
    for path in solution_files(folder, {".docx"}):
        for t in document(path).tables:
            if not t.rows:
                continue
            hdr = [c.text.strip() for c in t.rows[0].cells]
            cols = [i for i, h in enumerate(hdr) if _G20_COMMIT_HDR_RE.match(h)]
            for r in t.rows[1:]:
                for i in cols:
                    if i < len(r.cells):
                        out |= _g18_full_dates(r.cells[i].text)
    return out


_G40_REF_RE = re.compile(r"^='?([^'!]+)'?!\$?([A-Z]{1,3})\$?(\d+)$")
_G40_TOWARD_RE = re.compile(r"\b(?:to|into|onto)\b", re.I)
_G40_AWAY_RE = re.compile(r"\b(?:off|out of|away from)\b", re.I)
_G40_STOP = {"the", "a", "an", "and", "of", "on", "at", "per", "for", "year", "to", "into", "onto", "off",
             "out", "from", "away", "with", "their", "our", "its"}


def _g40_lemmas(text):
    return {w.rstrip("s") for w in re.findall(r"[a-z']+", text.lower()) if len(w) > 2 and w not in _G40_STOP}


def _g40_row_label(ws, r):
    for c in ws[r]:
        if isinstance(c.value, str) and not c.value.startswith("="):
            return c.value
    return None


@check(codes=['G40'], rules=['GOLD-FID'], needs=['solution'], params=['folder'])
def check_readthrough_label_direction(folder):
    """A read-through cell's row label never points the opposite way from the label on the row it references.

    Since: 2026-09-15.
    Source: a grader set Items!A36 "Web orders a year moving to their bench" beside
    Briefing!A9 "Web orders a year moving off Dean's bench", the front page reading =Items!C36,
    and noted the inconsistency; one figure labelled as moving to a bench and off a bench is two
    readings of one number.
    Drift-notes: fires only when the two labels differ, share two content lemmas (the same figure)
    and carry opposing direction particles (to/into/onto against off/out of/away from); ordinary
    front-page paraphrase ("Drop-ship shelf stock running off" of "Shelf stock running off") stays
    silent. Probed 2026-09-15 over 15 goldens: fires on this task alone.
    """
    try:
        import openpyxl
    except ImportError:
        return
    from ..common import solution_files
    for path in solution_files(folder, {".xlsx"}):
        try:
            wb = openpyxl.load_workbook(path)
        except Exception:
            continue
        for ws in wb.worksheets:
            for row in ws.iter_rows():
                for c in row:
                    m = _G40_REF_RE.match(c.value) if isinstance(c.value, str) else None
                    if not m or m.group(1) not in wb.sheetnames:
                        continue
                    here = _g40_row_label(ws, c.row)
                    there = _g40_row_label(wb[m.group(1)], int(m.group(3)))
                    if not here or not there or here == there:
                        continue
                    opposed = ((_G40_TOWARD_RE.search(here) and _G40_AWAY_RE.search(there))
                               or (_G40_AWAY_RE.search(here) and _G40_TOWARD_RE.search(there)))
                    if len(_g40_lemmas(here) & _g40_lemmas(there)) >= 2 and opposed:
                        emit("ERROR", f"[G40] {path.name} {ws.title}!{c.coordinate} labels the figure \"{here}\" "
                                      f"while the row it reads, {m.group(1)}!{m.group(2)}{m.group(3)}, labels it "
                                      f"\"{there}\" - opposite directions on one number "
                                      "(2026-09-15). Word both labels the same way, the front page's wording "
                                      "being the one the reader sees first")


@check(codes=['G20'], rules=['GOLD-FID'], needs=['prompt', 'inputs', 'solution'], params=['folder'])
def check_stated_dates_anchored(folder):
    """Every full date the golden states is carried by the prompt or an input, derived from one by a day count the record names, or set in a plan table's own date column."""
    corpus = "\n".join(t for _, t in _inputs_text(folder))
    pf = folder / "prompt.md"
    if pf.exists():
        corpus += "\n" + pf.read_text(encoding="utf-8", errors="ignore")
    # Widened 2026-09-10, the day it was coded: the first cut anchored on FULL dates only
    # and fired on a golden's Briefing dateline (08/26/2026, the memo's "Wednesday the
    # 26th") and title (09/08/2026, Tammy's "Tuesday, September 8") - dates the inputs DO
    # carry, in the partial forms G18 already reads generously. One anchor reader for both
    # checks: a golden full date is anchored by a corpus full date, a month-day pair or a
    # bare ordinal day (each taken in a corpus year), with ordinal weekdays and month ends
    # resolved by _g18_anchors. The true positive (09/01/2026 against a
    # corpus carrying only August 28) still fires: no partial form names September 1.
    fd, md, days = _g18_anchors(corpus)
    if not (fd or md or days):
        return
    years = {y for y, _, _ in fd}
    # A deadline the record DERIVES is anchored too: an input date plus a day count the prompt
    # or an input names ("within 180 days of the invoice date" puts April 7 + 180 = October 4 on
    # the schedule). And a plan table's own target column (BY WHEN / DUE / TARGET / DEADLINE) is
    # the deliverable's commitment, not an assertion about the record, so its dates are not
    # fabrications (2026-09-10).
    import datetime
    spans = {int(m) for m in re.findall(r"\b(\d{1,3}) days\b", corpus)}
    # 2026-09-14: a warranty or plan TERM the inputs
    # state in months ("twenty four months from the date of commissioning", "eighteen months")
    # derives an end date the same way a day count does, and the register's own date cells
    # (commissioning, cover-to) are dates the inputs carry even though they are not strings.
    # Both feed the anchor set: each input date plus each stated month term, and the day
    # before it (Article 6.2: "ends on the day immediately before the corresponding date").
    _MW = {"twelve": 12, "eighteen": 18, "twenty four": 24, "twenty-four": 24, "thirty six": 36,
           "thirty-six": 36, "six": 6, "three": 3, "nine": 9}
    months = {int(m) for m in re.findall(r"\b(\d{1,2}) months?\b", corpus)}
    for w, n in _MW.items():
        if re.search(r"\b" + w + r" months?\b", corpus, re.I):
            months.add(n)
    xd = set()
    try:
        from ..common import workbook
        ind = folder / "inputs"
        for xp in sorted(ind.glob("*.xlsx")) if ind.is_dir() else []:
            wb = workbook(xp, data_only=True)
            for ws in wb.worksheets:
                for row in ws.iter_rows():
                    for c in row:
                        v = c.value
                        if isinstance(v, (datetime.datetime, datetime.date)):
                            xd.add((v.year, v.month, v.day))
    except Exception:
        pass
    fd = set(fd) | xd
    derived = set()
    def _add_months(base, n):
        y2, m2 = base.year + (base.month - 1 + n) // 12, (base.month - 1 + n) % 12 + 1
        import calendar
        return base.replace(year=y2, month=m2, day=min(base.day, calendar.monthrange(y2, m2)[1]))
    for (y, mo, d) in fd:
        try:
            base = datetime.date(y, mo, d)
        except ValueError:
            continue
        for k in spans:
            t = base + datetime.timedelta(days=k)
            derived.add((t.year, t.month, t.day))
        for n in months:
            t = _add_months(base, n)
            derived.add((t.year, t.month, t.day))
            u = t - datetime.timedelta(days=1)
            derived.add((u.year, u.month, u.day))
    committed = _g20_commitment_dates(folder)
    seen = {}
    for where, text in _solution_text_in_order(folder):
        if not isinstance(text, str) or len(text) < 25:
            continue
        for (y, mo, d) in _g18_full_dates(text):
            year_ok = not years or y in years
            if (y, mo, d) in fd or (y, mo, d) in derived or (y, mo, d) in committed \
                    or (year_ok and ((mo, d) in md or d in days)):
                continue
            seen.setdefault((y, mo, d), where)
    for (y, mo, d), where in sorted(seen.items()):
        emit("ERROR", f"[G20] {where} states {mo}/{d}/{y}, a full date neither the prompt nor any input "
                      "carries - a golden's first page was dated September 1, 2026 with the "
                      "requesting note dated August 28, and a grader sent it back to \"remove or correct "
                      "the unsupported dates\" (2026-09-10). Anchor the date to an input (the note it "
                      "answers, the statement it corrects) or leave it off")


# G23 (2026-09-11, entity grounding check):
# the memo wrote "TXN-644093 on June 18 and TXN-644328 on June 19" and "completed on June 17".
# Every one of those dates is the transaction's own date cell in warehouse_inventory_transactions
# .xlsx, stored as a datetime and displayed mm-dd-yy; the platform read the inputs as text, found
# no "June 18" anywhere, and listed the three as fabricated ("confirmed absent from the input
# files"). G20 anchors a golden date against the corpus generously, partial forms included, so
# it read the datetime cells as anchors and said nothing. The platform does not: a date the
# golden spells out is grounded only by text a reader can find verbatim, and a date that exists
# only as a workbook date value is written in that cell's display form or left out.
_G23_MONTHS = ("january", "february", "march", "april", "may", "june", "july", "august",
               "september", "october", "november", "december")
_G23_SPELLED_RE = re.compile(r"\b(" + "|".join(m.capitalize() for m in _G23_MONTHS) + r")\s+(\d{1,2})\b(?!,?\s*20\d\d)")


def _g23_text_inputs(folder):
    """Text a reader can grep verbatim: docx, csv, txt, md inputs, xlsx STRING cells, the prompt."""
    from ..common import _docx_text, workbook
    out = []
    d = folder / "inputs"
    for p in sorted(d.glob("*")) if d.is_dir() else []:
        try:
            if p.suffix == ".docx":
                out.append(_docx_text(p))
            elif p.suffix in (".csv", ".txt", ".md", ".json"):
                out.append(p.read_text(encoding="utf-8", errors="ignore"))
            elif p.suffix == ".xlsx":
                wb = workbook(p, data_only=True)
                out.append("\n".join(str(c.value) for ws in wb.worksheets for row in ws.iter_rows()
                                     for c in row if isinstance(c.value, str)))
        except Exception:
            continue
    pf = folder / "prompt.md"
    if pf.exists():
        out.append(pf.read_text(encoding="utf-8", errors="ignore"))
    return "\n".join(out)


def _g23_date_cells(folder):
    """(month, day) pairs held as date values in the input workbooks."""
    import datetime
    from ..common import workbook
    pairs = set()
    d = folder / "inputs"
    for p in sorted(d.glob("*.xlsx")) if d.is_dir() else []:
        try:
            wb = workbook(p, data_only=True)
        except Exception:
            continue
        for ws in wb.worksheets:
            for row in ws.iter_rows():
                for c in row:
                    if isinstance(c.value, (datetime.datetime, datetime.date)):
                        pairs.add((c.value.month, c.value.day))
    return pairs


@check(codes=['G23'], rules=['GOLD-FID'], needs=['prompt', 'inputs', 'solution'], params=['folder'])
def check_spelled_date_only_a_cell(folder):
    """A month-day date the golden spells out is carried verbatim by some input text or the prompt, never only by a workbook date cell.

    Since: 2026-09-11.
    Source: the platform's golden solution entity grounding check (three dates listed as fabricated).
    Drift-notes: a spelled date absent from the cells too is G20's business; this fires only when a
    date value in an input workbook is the sole support, the case the platform reads as absent.
    """
    from ..common import _docx_text, workbook
    sol = folder / "solution"
    golden = ""
    for p in sorted(sol.glob("*")) if sol.is_dir() else []:
        try:
            if p.suffix == ".docx":
                golden += "\n" + _docx_text(p)
            elif p.suffix == ".xlsx":
                wb = workbook(p, data_only=True)
                golden += "\n" + "\n".join(str(c.value) for ws in wb.worksheets for row in ws.iter_rows()
                                           for c in row if isinstance(c.value, str))
        except Exception:
            continue
    spelled = {}
    for m in _G23_SPELLED_RE.finditer(golden):
        spelled.setdefault((_G23_MONTHS.index(m.group(1).lower()) + 1, int(m.group(2))), m.group(0))
    if not spelled:
        return
    corpus = _g23_text_inputs(folder)
    cells = None
    missing = []
    for (mo, day), label in sorted(spelled.items()):
        forms = [label, f"{mo}/{day}", f"{mo:02d}/{day:02d}", f"{mo:02d}-{day:02d}", f"{mo}/{day:02d}",
                 f"{_G23_MONTHS[mo - 1].capitalize()} {day:02d}"]
        if any(f in corpus for f in forms):
            continue
        if cells is None:
            cells = _g23_date_cells(folder)
        if (mo, day) in cells:
            missing.append(label)
    if missing:
        emit("ERROR", f"[G23] the golden spells out {', '.join(missing)}, and no input text or the prompt carries "
                     "the date; its only support is a date value in an input workbook, which the platform's entity "
                     "grounding check reads as absent and lists as fabricated "
                     "(2026-09-11, three dates). Write the date as the cell displays it, or leave it out")


_G24_KEY_RE = re.compile(r"^[A-Z]{2,4}-?\d{3,6}$")


def _g24_csv_aggregates(folder):
    """{csv name: (key column, {numeric column: {key: sum}})} for every input CSV keyed by an id."""
    import csv as _csv
    out = {}
    inp = folder / "inputs"
    for path in sorted(inp.glob("*.csv")) if inp.is_dir() else []:
        try:
            with open(path, newline="", encoding="utf-8-sig", errors="ignore") as fh:
                rows = list(_csv.DictReader(fh))
        except Exception:
            continue
        if len(rows) < 50:
            continue
        cols = [c for c in rows[0].keys() if c is not None]  # None holds a banner-headed CSV's overflow fields as a list
        key = next((c for c in cols if sum(1 for r in rows if _G24_KEY_RE.match(str(r.get(c) or "").strip())) > 0.9 * len(rows)), None)
        if not key:
            continue
        sums = {}
        for c in cols:
            if c == key:
                continue
            acc = {}
            ok = 0
            for r in rows:
                raw = str(r.get(c) or "").strip().replace(",", "")
                try:
                    val = float(raw)
                except ValueError:
                    continue
                ok += 1
                acc[r[key].strip()] = acc.get(r[key].strip(), 0.0) + val
            if ok > 0.9 * len(rows):
                sums[c] = acc
        if sums:
            out[path.name] = (key, sums)
    return out


@check(codes=['G24'], rules=['GOLD-FID'], needs=['inputs', 'solution'], params=['folder'])
def check_typed_aggregate_drift(folder):
    """A typed numeric column in the golden that mirrors a per-key aggregate of an input CSV equals that aggregate on every key.

    Since: 2026-09-11.
    Source: a grader re-summed pick_lines_jun12_aug28.csv and found Items!M (twelve-week
    units) off on 223 of 320 SKUs (HG1041 227 against 232), which moved a required cube across
    the shelf-bin line and invalidated the move list; the lines column beside it matched exactly.
    Drift-notes: a column is read as that aggregate when 80 percent of its keys sit within five
    units or ten percent of a CSV column's per-key sum; every key must then match exactly. Formula cells are skipped (their caches
    are the workbook's own arithmetic), and so are columns under 50 numeric values.
    """
    import openpyxl
    aggs = _g24_csv_aggregates(folder)
    if not aggs:
        return
    for x in solution_files(folder, {".xlsx"}):
        try:
            wb = openpyxl.load_workbook(x)
        except Exception:
            continue
        for ws in wb.worksheets:
            cols = {}
            for row in ws.iter_rows():
                for c in row:
                    cols.setdefault(c.column, []).append(c)
            keycol = next((ci for ci, cells in cols.items()
                           if sum(1 for c in cells if isinstance(c.value, str) and _G24_KEY_RE.match(c.value.strip())) >= 50), None)
            if keycol is None:
                continue
            keys = {c.row: c.value.strip() for c in cols[keycol] if isinstance(c.value, str) and _G24_KEY_RE.match(c.value.strip())}
            for ci, cells in cols.items():
                if ci == keycol:
                    continue
                typed = {c.row: float(c.value) for c in cells
                         if c.row in keys and isinstance(c.value, (int, float)) and not isinstance(c.value, bool)}
                if len(typed) < 50:
                    continue
                header = next((c.value for c in cells if isinstance(c.value, str) and c.row < min(typed)), f"column {ci}")
                for name, (key, sums) in aggs.items():
                    for col, acc in sums.items():
                        shared = [r for r in typed if keys[r] in acc]
                        if len(shared) < 0.6 * len(typed):
                            continue
                        match = [r for r in shared if abs(typed[r] - acc[keys[r]]) < 1e-6]
                        near = [r for r in shared if abs(typed[r] - acc[keys[r]]) <= max(5.0, 0.10 * abs(acc[keys[r]]))]
                        # the column IS this aggregate when nearly every key sits within a few units
                        # of it (the drifted units were off by -3 to +59 on 223 keys, 30% exact)
                        if len(near) < 0.8 * len(shared) or len(match) == len(shared):
                            continue
                        bad = [r for r in shared if r not in set(match)]
                        # reconciled drift is a DEVICE, not an error (2026-09-14):
                        # credited quantities short in the cage differed from the log sums on
                        # exactly the keys its Chargebacks schedule reconciles. When one column
                        # anywhere in the workbook carries, per bad key, exactly the difference,
                        # the mismatch is the task's shortage/variance mechanism - skip. The
                        # known-bad case (223 assorted drifts, no reconciling column)
                        # still fires; proven both ways on 2026-09-14.
                        diffs = {keys[r]: acc[keys[r]] - typed[r] for r in bad}
                        try:
                            wbv = openpyxl.load_workbook(x, data_only=True)
                            reconciled = False
                            for wsv in wbv.worksheets:
                                vcols = {}
                                for vrow in wsv.iter_rows():
                                    rk = next((str(c.value).strip() for c in vrow
                                               if isinstance(c.value, str) and c.value.strip() in diffs), None)
                                    if rk is None:
                                        continue
                                    for c in vrow:
                                        if isinstance(c.value, (int, float)) and not isinstance(c.value, bool):
                                            vcols.setdefault(c.column, {})[rk] = float(c.value)
                                if any(all(abs(col.get(k, 1e9) - abs(dv)) < 1e-6 for k, dv in diffs.items())
                                       for col in vcols.values()):
                                    reconciled = True
                                    break
                            if reconciled:
                                continue
                        except Exception:
                            pass
                        r0 = bad[0]
                        emit("ERROR", f"[G24] {x.name} {ws.title} \"{header}\" reads as the per-{key} sum of "
                                      f"{name} {col} ({len(match)} of {len(shared)} keys match) but {len(bad)} keys "
                                      f"differ, e.g. {keys[r0]} row {r0}: {typed[r0]:g} against {acc[keys[r0]]:g} - the "
                                      "grader re-sums the input and calls the golden's source data incorrect "
                                      "(2026-09-11: 223 of 320 units off, one item's required "
                                      "cube crossed the shelf-bin line and the move list followed). Retype the column "
                                      "from the input and recalculate everything downstream")


# G25 (2026-09-12, a grader's note): an early
# draft put "Phoenix Distribution Center" in the body subtitle and left "Marwood Fragrances Distribution
# Center" in word/footer1.xml, and four gates passed the memo, because every docx reader in this
# package opens word/document.xml only (python-docx's .paragraphs never lists a header or footer
# part). The grader reads the rendered page and quoted the footer back, four times. Names of
# organisations and facilities are the entity class the platform's grounding check and the
# grader both trace, so every part of a golden docx is read for them and each one is looked up
# in the inputs and the prompt.
_G25_SUFFIX = (r"(?:Center|Centre|Warehouse|DC|Inc\.?|LLC|Corp\.?|Corporation|Company|Co\.|Ltd\.?|Limited|Supply|"
               r"Lines|Group|Holdings|Brothers|Logistics|Freight|Industries|Enterprises|Partners|Wholesale|"
               r"Distributors|Distribution|Foods|Services|Depot|Terminal|Plant|Facility|Hub)")
_G25_NAME_RE = re.compile(r"\b((?:[A-Z][A-Za-z&'.-]+ )+" + _G25_SUFFIX + r")(?![A-Za-z])")
_G25_GENERIC = {w.lower().rstrip(".") for w in
                ("Center Centre Warehouse DC Inc LLC Corp Corporation Company Co Ltd Limited Supply Lines Group "
                 "Holdings Brothers Logistics Freight Industries Enterprises Partners Wholesale Distributors "
                 "Distribution Foods Services Depot Terminal Plant Facility Hub The A An").split()}
_G25_PART_RE = re.compile(r"^word/(header|footer)\d*\.xml$")


def _g25_docx_parts(path):
    """(part, text) for a docx's body and every header and footer part that carries text."""
    out = [("body", _docx_text(path))]
    with zipfile.ZipFile(path) as z:
        for name in sorted(z.namelist()):
            if _G25_PART_RE.match(name):
                xml = z.read(name).decode("utf-8", "ignore")
                txt = " ".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", xml)).strip()
                if txt:
                    out.append((name.split("/", 1)[1], txt))
    return out


@check(codes=['G25'], rules=['GOLD-FID'], needs=['prompt', 'inputs', 'solution'], params=['folder'])
def check_named_organisation_grounded(folder):
    """An organisation or facility name a solution docx carries, in its body or in a header or footer part, is carried by some input text or the prompt.

    Since: 2026-09-12.
    Source: a grader listed the footer's "Marwood Fragrances Distribution Center" as a fabricated
    entity after the body subtitle had been fixed earlier; the gate's docx readers open
    word/document.xml only, so four gates passed the memo with the footer untouched.
    Drift-notes: a name is a capitalised run ending in an organisation or facility word. A
    sentence-initial word is trimmed once before the lookup ("Move Castor Valley Supply"), and a run
    of generic words alone ("Distribution Center") is not a name. People (G16, G17) and cited
    identifiers (G10) have their own checks; solution workbooks are not read here.
    """
    src = " ".join(t for _, t in input_texts(folder)).lower()
    pf = folder / "prompt.md"
    if pf.exists():
        src += " " + pf.read_text(encoding="utf-8", errors="ignore").lower()
    if not src.strip():
        return

    def grounded(name):
        words = name.split()
        cands = [words] + ([words[1:]] if len(words) > 2 else [])
        seen_name = False
        for ws in cands:
            if all(w.lower().rstrip(".") in _G25_GENERIC for w in ws):
                continue
            seen_name = True
            if " ".join(ws).lower() in src:
                return True
        return not seen_name

    for path in solution_files(folder, {".docx"}):
        try:
            parts = _g25_docx_parts(path)
        except Exception:
            continue
        for part, text in parts:
            missing = []
            for m in _G25_NAME_RE.finditer(text):
                name = m.group(1).strip()
                if name not in missing and not grounded(name):
                    missing.append(name)
            if missing:
                where = "body" if part == "body" else f"{part}, a part the body readers never open"
                emit("ERROR", f"[G25] {path.name} {where}: \"{'\", \"'.join(missing[:4])}\" names an organisation or "
                              "facility that no input text and not the prompt carries. A grader reads the "
                              "rendered page, headers and footers included, and lists such a name as a fabricated "
                              "entity (2026-09-12: the footer kept the name an "
                              "earlier subtitle fix removed, and four gates passed it). Use the name the inputs use, "
                              "in every part of the document")


# G26 (2026-09-12, a grader's note): the fuel
# paragraph opened "NFPA 110 Class 72 wants 72 hours of fuel on site" where the prompt says only "The
# set has to hold 72 hours of fuel on site at full load" and no input mentions a Class 72. The same
# note traced "voltage dip inside the NFPA 110 allowance" (no input cites one) and "at full voltage
# with no soft starter" (the prompt says "starts across the line"), and an earlier pass had already
# removed an NFPA 25 mention and a 10-second start. A standard's number, and a class, type, level or
# tier stated in the same sentence as a standard, is a citation a grader traces to the prompt
# or an input; each one is looked up in the prompt and in every input, PDF data sheets included.
_G26_BODIES = ("NFPA|NEC|IEEE|ISO|IEC|ANSI|ASTM|ASME|UL|ASHRAE|NEMA|OSHA|EPA|CFR|IBC|NSF|SAE|DIN|CSA|FMCSA|DOT"
               "|GAAP|ASC|IFRS|HACCP|USDA|FDA")
_G26_NUMBERED_RE = re.compile(r"\b(" + _G26_BODIES + r")[  \-]?(\d+[A-Za-z]?(?:[.\-]\d+)*)\b")
_G26_BODY_RE = re.compile(r"\b(?:" + _G26_BODIES + r")\b")
_G26_QUAL_RE = re.compile(r"\b(Class|Type|Level|Tier|Category)[  ]+(\d+[A-Za-z]?)\b")


def _g26_tokens(text):
    """(numbered standards, qualifiers) as normalised keys: 'NFPA 110', 'CLASS 72'."""
    num = {f"{b.upper()} {n.upper()}" for b, n in _G26_NUMBERED_RE.findall(text)}
    qual = {f"{q.upper()} {n.upper()}" for q, n in _G26_QUAL_RE.findall(text)}
    return num, qual


def _g26_pdf_text(path):
    try:
        import pypdf
    except ImportError:
        return None
    try:
        return "\n".join((pg.extract_text() or "") for pg in pypdf.PdfReader(str(path)).pages)
    except Exception:
        return ""


def _g26_golden_parts(folder):
    """(file, text) for every solution part a reader sees: docx body, headers and footers, workbook
    string cells, plain text files."""
    out = []
    for path in solution_files(folder, {".docx", ".xlsx", ".md", ".txt", ".csv"}):
        try:
            if path.suffix == ".docx":
                out.extend((path.name, t) for _, t in _g25_docx_parts(path))
            elif path.suffix == ".xlsx":
                out.append((path.name, "\n".join(t for _, t in _all_text_cells(path))))
            else:
                out.append((path.name, path.read_text(encoding="utf-8", errors="ignore")))
        except Exception:
            continue
    return out


@check(codes=['G26'], rules=['GOLD-FID'], needs=['prompt', 'inputs', 'solution'], params=['folder'])
def check_standard_references_grounded(folder):
    """A standard cited by number in the golden (NFPA 110, ISO 8528, UL 2200), and a class, type, level or tier stated in the same sentence as a standard (Class 72), is carried by the prompt or by some input, PDF inputs included.

    Since: 2026-09-12.
    Source: a grader traced "NFPA 110 Class 72", "the NFPA 110 allowance" and "no soft starter"
    to the prompt's plain owner rule and found no input carrying them; an earlier pass had already
    struck an NFPA 25 mention and a 10-second start the same way.
    Drift-notes: a body token without a number (bare "EPA", "NFPA") is not checked, only the number
    beside it and a class-type-level-tier qualifier in its sentence; "Tier 2" beside "EPA" passes when
    the prompt says "EPA stationary emergency Tier 2". PDF inputs are read with pypdf; when a PDF
    input exists and pypdf is missing the check stays silent rather than fire on an unread source.
    """
    src = ""
    pf = folder / "prompt.md"
    if pf.exists():
        src += pf.read_text(encoding="utf-8", errors="ignore") + "\n"
    src += "\n".join(t for _, t in input_texts(folder))
    ind = folder / "inputs"
    for pdf in sorted(ind.glob("*.pdf")) if ind.is_dir() else []:
        t = _g26_pdf_text(pdf)
        if t is None:
            return
        src += "\n" + t
    if not src.strip():
        return
    src_num, src_qual = _g26_tokens(src)
    for fname, text in _g26_golden_parts(folder):
        missing = []
        for sent in re.split(r"(?<=[.!?])\s+|\n", text):
            num, qual = _g26_tokens(sent)
            for k in sorted(num - src_num):
                if k not in missing:
                    missing.append(k)
            if num or _G26_BODY_RE.search(sent):
                for k in sorted(qual - src_qual):
                    if k not in missing:
                        missing.append(k)
        if missing:
            emit("ERROR", f"[G26] {fname} cites {', '.join(missing[:5])}, a standard number or a class stated beside a "
                          "standard that no input text and not the prompt carries. A grader traces every code "
                          "reference to a source (2026-09-12: \"NFPA 110 Class 72\" "
                          "against a prompt that says only 72 hours of fuel on site). State the owner's rule in the "
                          "prompt's words, or cite the standard the way an input does")


# G27 (2026-09-13): the dataset quality
# check hard-failed cross-document consistency at 2 of 5 because every adjustment the memo
# cited carried a Related Transaction ID absent from the 514-row transaction log (TXN-840104
# against a log that ends at TXN-645279), and the reference documents on the two sides of one
# event differed (PCK-5011 / PCK-4937 on the adjustment, PCK-2847 / PCK-6077 on the picks it
# reconciled). The quantities tied and the checker said so, and still called the join broken:
# a record the golden cites has to join on the key it carries, not on an inference.
_G27_ID_RE = re.compile(r"\b([A-Z]{2,6})-(\d{4,8})\b")


_G27_PANEL_RE = re.compile(r"_\d+$")


def _g27_unpanel(header, rows):
    """A CSV laid out in side-by-side panels (H7: headers repeated with _2, _3 suffixes) is read
    as the flat table it stands for, block after block, empty panel cells dropped. Added
    2026-09-14: the join check read po_ref_2 as a
    column of its own and called every second-panel reference dangling."""
    suffixed = [j for j, h in enumerate(header) if _G27_PANEL_RE.search(h or "")]
    if not suffixed:
        return header, rows
    w = suffixed[0]
    if w == 0 or len(header) % w:
        return header, rows
    base = [_G27_PANEL_RE.sub("", h or "") for h in header]
    if any(base[b * w:(b + 1) * w] != header[:w] for b in range(1, len(header) // w)):
        return header, rows
    flat = []
    for b in range(len(header) // w):
        for r in rows:
            seg = list(r[b * w:(b + 1) * w])
            if any(c.strip() for c in seg if c):
                flat.append(seg)
    return header[:w], flat


def _g27_tables(folder):
    """(file name, header, rows of str-or-None) for every tabular input."""
    import csv
    d = folder / "inputs"
    for path in sorted(d.glob("*")) if d.is_dir() else []:
        if path.suffix.lower() == ".csv":
            try:
                rows = list(csv.reader(path.open(encoding="utf-8-sig", errors="ignore")))
            except Exception:
                continue
            if len(rows) > 1:
                header, body = _g27_unpanel(rows[0], rows[1:])
                yield path.name, header, [[(c.strip() or None) for c in r] for r in body]
        elif path.suffix.lower() == ".xlsx":
            try:
                wb = workbook(path, data_only=True)
            except Exception:
                continue
            for ws in wb.worksheets:
                data = list(ws.iter_rows(values_only=True))
                if len(data) > 1:
                    yield path.name, [str(h or "") for h in data[0]], \
                        [[(str(v).strip() or None) if v is not None else None for v in r] for r in data[1:]]


def _g27_keys(tables):
    """({file: (key column, family)}, {family: (file, ids)}): a file's key column is the first whose
    values are nine in ten one id shape, the shape being prefix and digit count."""
    keycol, ids = {}, {}
    for name, header, rows in tables:
        for j in range(len(header)):
            vals = [r[j] for r in rows if j < len(r) and r[j]]
            if len(vals) < 20:
                continue
            shapes = {}
            for v in vals:
                m = _G27_ID_RE.fullmatch(v)
                if m:
                    fam = (m.group(1), len(m.group(2)))
                    shapes[fam] = shapes.get(fam, 0) + 1
            if shapes:
                fam, n = max(shapes.items(), key=lambda kv: kv[1])
                if n >= 0.9 * len(vals):
                    keycol[name] = (j, fam)
                    ids.setdefault(fam, (name, set()))[1].update(vals)
                    break
    return keycol, ids


def _g27_golden_text(folder):
    sol = folder / "solution"
    out = []
    for p in sorted(sol.glob("*")) if sol.is_dir() else []:
        try:
            if p.suffix == ".docx":
                out.append(_docx_text(p))
            elif p.suffix == ".xlsx":
                wb = workbook(p, data_only=True)
                out.append("\n".join(str(c.value) for ws in wb.worksheets for row in ws.iter_rows()
                                     for c in row if isinstance(c.value, str)))
        except Exception:
            continue
    return "\n".join(out)


_G27_MISSING_RE = re.compile(r"not on the|does not carry|not established|will not settle|no instrument of|"
                             r"no such|cannot be matched|is not listed|not carried on|unsettled|no item file row", re.I)


def _g27_reported_missing(golden_text, ident):
    """True when the golden names `ident` inside a sentence that says the record is missing."""
    for m in re.finditer(re.escape(ident), golden_text):
        lo = max(0, golden_text.rfind(".", 0, m.start()) + 1)
        hi = golden_text.find(".", m.end())
        sent = golden_text[lo:(hi if hi != -1 else len(golden_text))]
        if _G27_MISSING_RE.search(sent):
            return True
    return False


@check(codes=['G27'], rules=['DATA-JOIN'], needs=['inputs', 'solution'], params=['folder'])
def check_cited_record_joins(folder):
    """A record the golden cites carries no related-record id of another input's key family that the input set does not hold.

    Since: 2026-09-13.
    Source: the dataset quality check's cross-document consistency axis, hard fail at 2 of 5 ("the
    formal ID keys linking adjustments to transactions are broken for every critical record in
    the task scope").
    Drift-notes: a key family is a prefix and a digit count, so a four-digit ADJ document number is
    not the six-digit adjustment key. Only rows the golden cites are read: an extract may reference
    prior-period records on rows the task never touches. An id the golden itself cites that no
    input carries is G10's business.
    """
    golden_text = _g27_golden_text(folder)
    cited = {m.group(0) for m in _G27_ID_RE.finditer(golden_text)}
    if not cited:
        return
    tables = list(_g27_tables(folder))
    keycol, ids = _g27_keys(tables)
    if len(ids) < 2:
        return
    dangling = []
    for name, header, rows in tables:
        if name not in keycol:
            continue
        kj, own = keycol[name]
        for r in rows:
            key = r[kj] if kj < len(r) else None
            if key not in cited:
                continue
            for j, v in enumerate(r):
                if j == kj or not v:
                    continue
                for m in _G27_ID_RE.finditer(v):
                    fam = (m.group(1), len(m.group(2)))
                    if fam != own and fam in ids and m.group(0) not in ids[fam][1]:
                        # 2026-09-14: a gap the golden
                        # itself reports as unsettled (an item number the item file does not
                        # carry, a plan against a serial number not on the register) is the
                        # task's designed question, not a broken key; the dataset check reads
                        # the golden's own statement of it. Exempt an id the golden names
                        # within a sentence saying the record is missing.
                        if _g27_reported_missing(golden_text, m.group(0)):
                            continue
                        dangling.append(f"{name} {key} \"{header[j]}\" {m.group(0)} (no such record in {ids[fam][0]})")
    if dangling:
        emit("ERROR", f"[G27] {len(dangling)} related-record id(s) on records the golden cites join to nothing: "
                      f"{'; '.join(dangling[:8])}. The dataset quality check's cross-document consistency axis "
                      "hard-fails at 2 on this (2026-09-13: every cited "
                      "adjustment's Related Transaction ID absent from the 514-row log, and quantities that tied "
                      "by inference did not save it). Point the field at the record the golden pairs it with, and "
                      "match the reference documents on both sides of the event")


# G28 (2026-09-14, platform entity grounding check):
# the prompt describes the owner as "a regional medical center in northern New Mexico" and the
# memo's subtitle title-cased it into "Regional Medical Center, Northern New Mexico". The
# grounding check read the capitalised run as an organisation name, found no such name in any
# input, and listed it as fabricated. G25 was quiet because its lookup lowercases both sides; a
# description the prompt gives in lowercase is grounded only as a description, not as a name.
@check(codes=['G28'], rules=['GOLD-FID'], needs=['prompt', 'inputs', 'solution'], params=['folder'])
def check_description_not_title_cased_into_name(folder):
    """An organisation-style capitalised run in a solution docx that the prompt or an input carries only in lowercase, as a description, is written in that lowercase form; title-casing a description makes a name the grounding check cannot find.

    Since: 2026-09-14 (entity grounding check).
    Source: the platform's entity grounding check listed "Regional Medical Center" as fabricated
    against a prompt that says "a regional medical center in northern New Mexico".
    Drift-notes: reads the same capitalised runs as G25 and fires only on the ones G25 grounds,
    when no source carries the run with its capitals; a generic run alone ("Distribution Center")
    is skipped as in G25.
    """
    src_raw = " ".join(t for _, t in input_texts(folder))
    pf = folder / "prompt.md"
    if pf.exists():
        src_raw += " " + pf.read_text(encoding="utf-8", errors="ignore")
    src_raw = re.sub(r"\s+", " ", src_raw)
    if not src_raw.strip():
        return
    src_low = src_raw.lower()
    for path in solution_files(folder, {".docx"}):
        try:
            parts = _g25_docx_parts(path)
        except Exception:
            continue
        flagged = []
        for part, text in parts:
            for m in _G25_NAME_RE.finditer(text):
                name = m.group(1).strip()
                words = name.split()
                if all(w.lower().rstrip(".") in _G25_GENERIC for w in words):
                    continue
                cands = [" ".join(words)] + ([" ".join(words[1:])] if len(words) > 2 else [])
                for c in cands:
                    if c.lower() in src_low and c not in src_raw and c not in flagged:
                        flagged.append(c)
                        break
        if flagged:
            emit("ERROR", f"[G28] {path.name} writes \"{'\", \"'.join(flagged[:4])}\" with capitals where the prompt or an "
                          "input carries it only in lowercase, as a description; the platform's entity grounding "
                          "check reads the capitalised run as an organisation name and lists it as fabricated "
                          "(2026-09-14, \"Regional Medical Center\" against \"a "
                          "regional medical center\"). Write it the way the source does")

_G29_RANGE_RE = re.compile(r"^\s*(\d+(?:\.\d+)?)\s+(?:to|-|\u2013)\s+(\d+(?:\.\d+)?)\s*$")
_G29_CONVENTION_RE = re.compile(
    r"\binclusive\b|\bexclusive\b|but not including|up to and including|takes the row|begins at that|"
    r"falls on the line|on the line between|\bboundary\b", re.I)


def _g29_docx_bands(path):
    """(table index, [(lo, hi, row text)]) for every docx table whose rows are numeric ranges."""
    import docx
    from decimal import Decimal, InvalidOperation
    out = []
    doc = docx.Document(str(path))
    prose = " ".join(p.text for p in doc.paragraphs)
    for ti, t in enumerate(doc.tables):
        rows = []
        for r in t.rows:
            cells = [c.text for c in r.cells]
            m = _G29_RANGE_RE.match(cells[0]) if cells else None
            if m:
                try:
                    rows.append((Decimal(m.group(1)), Decimal(m.group(2)), " | ".join(c.strip() for c in cells)))
                except InvalidOperation:
                    pass
        if len(rows) >= 3:
            out.append((ti, rows))
    return prose, out


@check(codes=['G29'], rules=['GOLD-FID'], needs=['inputs'], params=['folder'])
def check_band_boundary_convention(folder):
    """A banded lookup table in an input (rate, surcharge or tier rows written "a to b") whose adjacent rows share an endpoint states which row a value on the line takes, when a lookup value in the data lands exactly on a shared endpoint, because the golden's figure is otherwise not uniquely determined.

    Since: 2026-09-14 (items 2 and 4).
    Source: a grader read Appendix B's "3.65 to 3.70" at 24.0 and "3.70 to 3.75" at 25.0 with no
    inclusion rule against a diesel index of exactly 3.70 for the week one shipment moved, and called
    the exactly-graded rated and claim totals underdetermined.
    Drift-notes: reads docx tables whose first column is "a to b"; a convention sentence anywhere in the
    document's prose (inclusive, but not including, takes the row, on the line between) clears the table;
    the data scan takes every CSV and workbook cell in inputs/ that equals a shared endpoint, in a column
    whose numeric values mostly sit inside the table's span, so a weight of 3.70 in a column of tonnages
    does not fire.
    """
    import csv
    from decimal import Decimal, InvalidOperation
    inputs = folder / "inputs"
    if not inputs.is_dir():
        return
    tables = []
    for path in sorted(inputs.glob("*.docx")):
        try:
            prose, bands = _g29_docx_bands(path)
        except Exception:
            continue
        if _G29_CONVENTION_RE.search(prose):
            continue
        for ti, rows in bands:
            shared = set()
            for (lo1, hi1, _), (lo2, hi2, _) in zip(rows, rows[1:]):
                if hi1 == lo2:
                    shared.add(hi1)
            if shared:
                lo_all = min(lo for lo, _, _ in rows); hi_all = max(hi for _, hi, _ in rows)
                tables.append((path.name, ti + 1, rows, shared, lo_all, hi_all))
    if not tables:
        return
    columns = []  # (file, header, [Decimal values])
    for path in sorted(inputs.glob("*.csv")):
        try:
            with open(path, encoding="utf-8", errors="ignore", newline="") as fh:
                data = list(csv.reader(fh))
        except Exception:
            continue
        if len(data) < 2:
            continue
        for ci, hdr in enumerate(data[0]):
            vals = []
            for row in data[1:]:
                if ci < len(row):
                    try:
                        vals.append(Decimal(row[ci].strip()))
                    except (InvalidOperation, ValueError):
                        pass
            if vals:
                columns.append((path.name, hdr, vals))
    for path in sorted(inputs.glob("*.xlsx")):
        try:
            import openpyxl
            wb = openpyxl.load_workbook(str(path), data_only=True, read_only=True)
        except Exception:
            continue
        for ws in wb.worksheets:
            cols = {}
            for row in ws.iter_rows(values_only=True):
                for ci, v in enumerate(row):
                    if isinstance(v, (int, float)) and not isinstance(v, bool):
                        cols.setdefault(ci, []).append(Decimal(str(v)))
            for ci, vals in cols.items():
                columns.append((f"{path.name} '{ws.title}'", f"column {ci + 1}", vals))
    for fname, ti, rows, shared, lo_all, hi_all in tables:
        for ep in sorted(shared):
            above = next((r for r in rows if r[0] == ep), None)
            below = next((r for r in rows if r[1] == ep), None)
            if not above or not below or above[2].split("|")[-1].strip() == below[2].split("|")[-1].strip():
                continue  # both rows give the same result, nothing to decide
            hits = []
            for cf, hdr, vals in columns:
                inside = sum(1 for v in vals if lo_all <= v <= hi_all)
                if inside < max(3, int(0.8 * len(vals))):
                    continue
                n = sum(1 for v in vals if v == ep)
                if n:
                    hits.append(f"{cf} {hdr} ({n} value{'s' if n > 1 else ''} at {ep})")
            if hits:
                emit("ERROR", f"[G29] {fname} table {ti}: rows \"{below[2]}\" and \"{above[2]}\" share the "
                              f"endpoint {ep} and the document states no inclusion rule, while {'; '.join(hits)} "
                              "land exactly on it, so the golden's figure for those rows is not uniquely "
                              "determined (2026-09-14: the week of June 29 at 3.70 "
                              "left the rated and claim totals underdetermined). Add the convention to the "
                              "document ('a price on the line between two rows takes the row that begins at "
                              "that price') or move the data off the line")


# G30 (2026-09-14, golden
# solution role check): Table 2 of the golden read "... | Re-entry inspection required | Amount
# payable" and the SN-209410 row "... | Yes | 537.45". The judge read 537.45 as the inspection
# charge and failed the golden against Exhibit A's 285.00, because the money cell that follows
# a Yes/No cell headed with a charge's name is the charge's own value on a plain read. The fix
# is the charge's own column between the two ("Plan charge | Re-entry inspection charge | Amount
# payable"), never a footnote. The check keys on the header words a charge is called by and on
# a body that is Yes/No throughout, so a Yes/No column headed "Approved" beside a money column
# stays silent, and so does a charge column whose neighbour is headed with the same word.
_G30_CHARGE_RE = re.compile(r"\b(inspection|fee|charge|surcharge|penalty|deposit|levy|premium|retest)\b", re.I)
_G30_YESNO = {"yes", "no", "y", "n", "required", "not required"}
_G30_MONEY_RE = re.compile(r"^\(?\$?\s*\d{1,3}(?:,\d{3})*(?:\.\d{2})\)?$|^\(?\$?\s*\d+\.\d{2}\)?$")


@check(codes=['G30'], rules=['GOLD-FID'], needs=['solution'], params=['folder'])
def check_yesno_charge_column_beside_money(folder):
    """A golden docx table never sets a money column directly after a Yes/No column headed with a charge's name unless that money column is headed with the same name.

    Since: 2026-09-14.
    Source: the golden solution role check read Table 2's "Re-entry inspection required | Amount
    payable" row "Yes | 537.45" as the inspection charge and failed it against Exhibit A's 285.00.
    """
    for name, ti, rows in _docx_tables(folder):
        if len(rows) < 2:
            continue
        hdr = rows[0]
        body = rows[1:]
        for j in range(len(hdr) - 1):
            m = _G30_CHARGE_RE.search(hdr[j])
            if not m:
                continue
            vals = [r[j].strip().lower() for r in body if j < len(r) and r[j].strip()]
            if not vals or any(v not in _G30_YESNO for v in vals):
                continue
            nxt = hdr[j + 1]
            if re.search(r"\b" + re.escape(m.group(1)) + r"\b", nxt, re.I):
                continue
            money = [r[j + 1].strip() for r in body if j + 1 < len(r) and _G30_MONEY_RE.match(r[j + 1].strip())]
            if len(money) < 2:
                continue
            yes_rows = [r for r in body if j < len(r) and r[j].strip().lower() in ("yes", "y", "required")]
            sample = next((f"{r[0].strip()}: {r[j].strip()} | {r[j + 1].strip()}" for r in yes_rows if j + 1 < len(r)), "")
            emit("ERROR", f"[G30] {name} table {ti + 1}: the {hdr[j + 1].strip()!r} money column sits directly "
                          f"after the Yes/No column {hdr[j].strip()!r}, so a judge reads the money as the "
                          f"{m.group(1).lower()} itself ({sample}); put the {m.group(1).lower()}'s own column "
                          f"between them or head the money column with its name "
                          f"(2026-09-14: 'Yes | 537.45' was failed against Exhibit A's 285.00)")


# G31 (2026-09-14): the contradiction
# checker lifted "every SKU carried Under Review with an Inventory Control case open" out of a
# sentence that opened "Cycle count records establish ..." and read it against the 1005
# paragraph, where the adjustment is completed and its queue closed. The claim was true of the
# count sheet and false of the adjustment file, and the checker reads the claim, not the sentence
# it sits in, so the status has to carry its own source in the next few words.
_G31_STATUS_HDR_RE = re.compile(r"status|state|queue", re.I)
_G31_OPEN_RE = re.compile(r"review|pending|open|await|hold", re.I)
_G31_CLOSED_RE = re.compile(r"complet|closed|approved|resolved|posted|done|verified", re.I)
_G31_QUANT_RE = re.compile(r"\b(?:every|all|each)\s+(?:of\s+the\s+|of\s+)?[A-Za-z]", re.I)  # "each SKU", not "110 units each,"
_G31_ID_RE = re.compile(r"\b[A-Z]{2,6}(?:-[A-Z]{2,6})?-\d{3,8}\b")


def _g31_shape(v):
    return re.sub(r"\d", "9", re.sub(r"[A-Z]", "A", v))


_G31_SOURCE_WORDS = {"sheet", "file", "record", "records", "log", "report", "register", "table", "workbook", "column"}


def _g31_status_vocab(tables):
    """{status value: True if open, False if closed} from the inputs' status-like columns."""
    vocab = {}
    for name, header, rows in tables:
        for j, h in enumerate(header):
            if not _G31_STATUS_HDR_RE.search(h):
                continue
            for r in rows:
                v = r[j] if j < len(r) else None
                if v and 1 <= len(v.split()) <= 3 and v not in vocab:
                    if _G31_OPEN_RE.search(v) and not _G31_CLOSED_RE.search(v):
                        vocab[v] = True
                    elif _G31_CLOSED_RE.search(v):
                        vocab[v] = False
    return vocab


@check(codes=['G31'], rules=['GOLD-FID'], needs=['inputs', 'solution'], params=['folder'])
def check_universal_status_claim(folder):
    """A golden sentence asserting an open status for every, all or each of the cited keys names the record it reads within six words of the status, whenever another input carries a closed status for one of those keys; the contradiction checker reads the claim without its sentence.

    Since: 2026-09-14.
    Source: the platform's internal-contradiction check ("every SKU carried Under Review" against a
    completed adjustment with its review queue closed).
    Drift-notes: status values come from the inputs' own status-like columns; open is review, pending,
    open, awaiting or hold, closed is completed, closed, approved, resolved or posted. The source is
    a phrase right after the status ("on the count sheet", "in the adjustment file") whose noun is a
    token of an input file's name or sheet, file, record, log or report; a source named at the
    start of the sentence does not count, because the checker lifts the claim out of it. The keys a
    sentence covers are the ones it names, or every cited key when it names none; a sentence whose
    keys carry no closed status anywhere has nothing to contradict and is not read.
    """
    from ..common import split_sentences
    tables = list(_g27_tables(folder))
    if not tables:
        return
    vocab = _g31_status_vocab(tables)
    open_tokens = [v for v, is_open in vocab.items() if is_open]
    if not open_tokens:
        return
    golden = _g27_golden_text(folder)
    # key-like columns by SHAPE (AAA-AAA-9999), so a SKU column shared by four files counts
    # whatever its per-row prefix; a shape carried as a column in two or more files is shared
    keycols = {}
    for name, header, rows in tables:
        for j in range(len(header)):
            vals = [r[j] for r in rows if j < len(r) and r[j]]
            if len(vals) < 20:
                continue
            shapes = {}
            for v in vals:
                if _G31_ID_RE.fullmatch(v):
                    sh = _g31_shape(v)
                    shapes[sh] = shapes.get(sh, 0) + 1
            if shapes:
                sh, n = max(shapes.items(), key=lambda kv: kv[1])
                if n >= 0.9 * len(vals):
                    keycols.setdefault(sh, []).append((name, j))
    shared = {sh for sh, cols in keycols.items() if len({c[0] for c in cols}) >= 2}
    keys = {m.group(0) for m in _G31_ID_RE.finditer(golden) if _g31_shape(m.group(0)) in shared}
    if not keys:
        return
    closed_for = {}
    for name, header, rows in tables:
        kcols = [j for sh in shared for (n, j) in keycols[sh] if n == name]
        scols = [j for j, h in enumerate(header) if _G31_STATUS_HDR_RE.search(h)]
        if not kcols or not scols:
            continue
        for r in rows:
            ks = [r[j] for j in kcols if j < len(r) and r[j] in keys]
            if not ks:
                continue
            for j in scols:
                v = r[j] if j < len(r) else None
                if v in vocab and vocab[v] is False:
                    closed_for.setdefault(ks[0], set()).add(f"{name} {header[j]} {v}")
    if not closed_for:
        return
    source_words = set(_G31_SOURCE_WORDS)
    for name, _, _ in tables:
        source_words.update(w for w in re.split(r"[_\W]+", name.rsplit(".", 1)[0].lower()) if len(w) > 2)
    for line in golden.splitlines():
      for sent in split_sentences(line):
        q = _G31_QUANT_RE.search(sent)
        if not q:
            continue
        named = [m.group(0) for m in _G31_ID_RE.finditer(sent)]
        subjects = [t for t in named if t in keys] or (sorted(keys) if not named else [])
        if not any(t in closed_for for t in subjects):
            continue  # the keys this sentence covers carry no closed status anywhere: nothing to contradict
        for tok in open_tokens:
            m = re.search(r"\b" + re.escape(tok) + r"\b", sent, re.I)
            if not m or m.start() < q.start():
                continue
            tail = sent[m.end():].strip()
            sm = re.match(r"^[,]?\s*(?:on|in|per|from|by|across|under)\s+(?:the\s+|its\s+|each\s+)?((?:\w+\s+){0,2}\w+)", tail, re.I)
            if sm and any(w.lower() in source_words for w in sm.group(1).split()):
                continue
            k0 = next(t for t in subjects if t in closed_for)
            emit("ERROR", f"[G31] the golden says \"{sent.strip()[:140]}\" - an open status claimed for every key with "
                          f"no source named beside it, while {k0} carries {sorted(closed_for[k0])[0]}. The "
                          "contradiction checker lifts the claim out of its sentence and reads it against the "
                          "per-item detail (2026-09-14). Qualify the status "
                          "where it stands: \"Under Review on the count sheet\"")
            return


# G33 (2026-09-14, attribution / role check
# 1 of 32): "West also has the fewest visits logged in the quarter at just 19" was the one failed
# claim. The judge reads a 117-row log in slices, listed 18 West ids from its last slice, added
# "prior slices" from memory (the true remainder was one row, V-6199 on the line before the slice)
# and called the 19 inconsistent. A per-group record count stated in prose as a superlative sends
# the judge to re-count the whole file; the same count in Table 1 beside a per-account ledger
# drew nothing. The portfolio probe found the shape in no other golden's prose.
_G33_SUPERLATIVE_RE = re.compile(r"\b(?:fewest|most|highest|lowest|largest|smallest)\b([^.]{0,90})", re.I)
_G33_NOUN_RE = re.compile(r"\b(visits?|rows?|lines?|orders?|entries|records|invoices|tickets|shipments|receipts|calls)\b", re.I)
_G33_COUNT_RE = re.compile(r"(?<![\d.,])\d{1,3}(?![\d.,%])")
_G33_MONTH_RE = re.compile(r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s*$", re.I)
_G33_LONG_CSV = 40


def _g33_hit(text):
    """the span after a superlative that carries both a record noun and a bare count, in either order"""
    for m in _G33_SUPERLATIVE_RE.finditer(text):
        span = m.group(1)
        counts = [c for c in _G33_COUNT_RE.finditer(span) if not _G33_MONTH_RE.search(span[:c.start()])]
        if _G33_NOUN_RE.search(span) and counts:
            return text[m.start():m.end()]
    return None


@check(codes=['G33'], rules=['GOLD-FID'], needs=['inputs', 'solution'], params=['folder'])
def check_prose_superlative_count(folder):
    """A golden's prose never states a per-group record count over a long CSV as a superlative claim ("the fewest visits at just 19"); the count lives in a ledgered table and the prose keeps the comparison.

    Since: 2026-09-14.
    Source: the platform's attribution / role check (the judge re-counts the file in slices and miscounts).
    Drift-notes: docx prose only, and only when some input CSV runs past 40 lines; the portfolio probe found
    the shape nowhere else.
    """
    inputs = folder / "inputs"
    long_csv = [p.name for p in (sorted(inputs.glob("*.csv")) if inputs.is_dir() else [])
                if sum(1 for _ in p.open(encoding="utf-8-sig", errors="ignore")) > _G33_LONG_CSV]
    if not long_csv:
        return
    for d in solution_files(folder, {".docx"}):
        doc = document(d)
        for p in doc.paragraphs:
            hit = _g33_hit(p.text)
            if hit:
                emit("ERROR", f"{d.name}: prose states a per-group record count as a superlative "
                             f"(\"{hit}\") over {long_csv[0]}, which runs past "
                             f"{_G33_LONG_CSV} lines: the attribution judge re-counts the file in slices and failed "
                             "the true count of 19 (2026-09-14). Keep the count in "
                             "a ledgered table and the comparison in the prose without the figure")


_G34_TAB_RE = re.compile(r"\b[Tt]he ([A-Z][A-Za-z0-9 ]{1,40}?) tab\b")
_G34_HDR_RE = re.compile(r"\b([A-Z][A-Z0-9]{1,}(?: [A-Z][A-Z0-9]{1,}){0,3})\b")
_G34_STOP = {"UPHELD", "NOT UPHELD", "YES", "NO", "TOTAL", "Q1", "Q2", "Q3", "Q4", "GP", "PCT", "USD", "PO", "SKU", "ID", "CSV", "PDF", "XLSX", "DOCX", "A", "I"}


@check(codes=['G34'], rules=['GOLD-FID'], needs=['solution'], params=['folder'])
def check_tab_header_citations(folder):
    """A prose cell that sends the reader to a named tab for an upper-case column label names a label that tab's header rows carry; a label that lives on another tab is a wrong direction a grader follows and reports.

    Since: 2026-09-14.
    Source: Disputes!D6 read "The Invoices tab carries both figures, STMT GP against GROSS PROFIT"; STMT GP is a Statement Lines header and a grader sent the task back on it with three other prose slips.
    Drift-notes: a tab is named by "the <Title> tab"; a label is two or more upper-case tokens of two or more characters, checked case-insensitively against the string cells of the named tab's first eight rows; an unknown tab name is ignored (R112 owns that).
    """
    import openpyxl
    from ..common import solution_files
    for x in solution_files(folder, {".xlsx"}):
        try:
            wb = openpyxl.load_workbook(x, data_only=True, read_only=True)
        except Exception:
            continue
        heads = {}
        for ws in wb.worksheets:
            labels = set()
            for row in ws.iter_rows(min_row=1, max_row=8, values_only=True):
                for v in row:
                    if isinstance(v, str) and v.strip():
                        labels.add(v.strip().upper())
            heads[ws.title.strip().lower()] = labels
        bad = []
        for ws in wb.worksheets:
            for row in ws.iter_rows():
                for c in row:
                    v = c.value
                    if not isinstance(v, str) or len(v) < 40:
                        continue
                    for sent in re.split(r"(?<=[.;])\s+", v):
                        tabs = [t.strip().lower() for t in _G34_TAB_RE.findall(sent)]
                        tabs = [t for t in tabs if t in heads]
                        if len(tabs) != 1:
                            continue
                        for lab in _G34_HDR_RE.findall(sent):
                            if lab in _G34_STOP or " " not in lab or lab.upper() in heads[tabs[0]]:
                                continue
                            elsewhere = [t for t, labs in heads.items() if lab.upper() in labs]
                            if elsewhere:
                                bad.append(f"{ws.title}!{c.coordinate} names {lab} on the {tabs[0]} tab, a header of {', '.join(elsewhere)}")
        wb.close()
        if bad:
            emit("ERROR", f"[G34] {x.name}: {len(bad)} prose direction(s) to a tab for a label that tab does not carry: "
                          f"{'; '.join(bad[:4])}. A task was sent back (2026-09-14) on 'The Invoices tab "
                          "carries ... STMT GP', a Statement Lines header; name the tab that carries the label")



_R130_CITE_RE = re.compile(r"\bSection\s+(\d+\.\d+[a-z]?)\b")
_R130_GOLDEN_RE = re.compile(r"\bSections?\s+((?:\d+\.\d+[a-z]?)(?:\s*(?:,|and|to|through|or)\s*(?:\d+\.\d+[a-z]?))*)", re.I)
_R130_NUM_RE = re.compile(r"\d+\.\d+[a-z]?")


def _r129_golden_sections(folder):
    """Every numbered section the golden names, ranges 'Sections 5.1 to 5.4' expanded on the minor number."""
    import openpyxl
    texts = []
    for p in solution_files(folder, {".docx"}):
        texts.append(_docx_text(p))
    for p in solution_files(folder, {".xlsx"}):
        try:
            wb = openpyxl.load_workbook(p, data_only=True, read_only=True)
        except Exception:
            continue
        for ws in wb.worksheets:
            for row in ws.iter_rows(values_only=True):
                texts.extend(v for v in row if isinstance(v, str))
        wb.close()
    named = set()
    for m in _R130_GOLDEN_RE.finditer("\n".join(texts)):
        nums = _R130_NUM_RE.findall(m.group(1))
        named.update(nums)
        if re.search(r"\b(?:to|through)\b", m.group(1)) and len(nums) >= 2:
            lo, hi = nums[-2], nums[-1]
            lo_major, lo_minor = lo.split(".")[0], re.sub(r"[a-z]$", "", lo.split(".")[1])
            hi_major, hi_minor = hi.split(".")[0], re.sub(r"[a-z]$", "", hi.split(".")[1])
            if lo_major == hi_major and lo_minor.isdigit() and hi_minor.isdigit():
                named.update(f"{lo_major}.{n}" for n in range(int(lo_minor), int(hi_minor) + 1))
    return named


@check(codes=['R130'], rules=['GOLD-FID'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_cited_section_in_golden(rows, folder):
    """A positive criterion that cites a numbered section ("Section 3.2") names a section the golden's own text cites somewhere; a section the golden never names fails the criterion on every oracle run, whatever the golden says in substance.

    Since: 2026-09-14.
    Source: C14 read "left out of the demand to which Section 5.4 applies, under Section 3.2 of the program customer terms"; the golden cited Section 3.1 only and the oracle failed C14 on all three runs at 0.98, while an earlier golden-versus-rubric table had recorded the row as landing.
    Drift-notes: a cite is "Section N.N" in a positive-weight row; the golden's cites are read from every solution docx paragraph and xlsx string cell, and "Sections A to B" on one major number expands to every minor between; the document a section belongs to is not checked, and a range or bare "N.N" in a criterion is not a cite.
    """
    named = None
    for num, text, weight in rows:
        if weight <= 0:
            continue
        cites = sorted(set(_R130_CITE_RE.findall(text)))
        if not cites:
            continue
        if named is None:
            named = _r129_golden_sections(folder)
            if not named and not solution_files(folder, {".docx", ".xlsx"}):
                return
        missing = [s for s in cites if s not in named]
        if missing:
            emit("ERROR", f"C{num} [R130] cites Section {', '.join(missing)}, which no solution file names: "
                          f"the judge looks for the section by number and fails the row on every run. "
                          "a task lost C14 3 of 3 oracle runs (2026-09-14) on a "
                          "Section 3.2 cite the golden never made; name the section in the golden where "
                          "the criterion's point is stated, or drop the cite from the criterion")


# G37 (2026-09-14, attribution / role check
# 1 of 51 points): feature code B600-2 sits on two input data sheets with different figures, the
# DQCB table at 3,313 kVA and the DQGAB table at 5,743 kVA (Cummins reuses alternator codes across
# models). The memo's compliance table cell read "3,313 kVA starting capacity on winding B600-2
# against 1,200 kVA inrush", naming no model; the attribution check matched the code to the DQGAB
# sheet and called the figure a contradiction. The two prose mentions named the DQCB and passed.
# The first probe keyed on any identifier two inputs share and lit up 20 lines in four other
# goldens whose record ids (TXN-, HLD-, NB-, SN-, PCN-) join the same record across a workbook
# and a memo; the defect is a code whose figures DIFFER by input, so the check keys on a figure the
# golden paragraph carries that sits beside the code in one owning input and not in another.
_G37_ID_RES = (re.compile(r"\b[A-Z]{1,5}\d{2,5}-\d{1,4}\b"), re.compile(r"\b[A-Z]{2,5}-\d{2,6}\b"))
_G37_NUM_RE = re.compile(r"(?<![\w.])\d[\d,]*(?:\.\d+)?(?![\w])")


def _g37_input_texts(folder):
    """(file name, text) per input, PDFs read through pypdf; None when a PDF cannot be read."""
    out = list(input_texts(folder))
    ind = folder / "inputs"
    for pdf in sorted(ind.glob("*.pdf")) if ind.is_dir() else []:
        t = _g26_pdf_text(pdf)
        if t is None:
            return None
        out.append((pdf.name, t))
    return out


def _g37_figures(text):
    """Figures of three or more digits in a line, commas stripped, identifiers and plain years removed."""
    for rx in _G37_ID_RES:
        text = rx.sub(" ", text)
    out = set()
    for m in _G37_NUM_RE.findall(text):
        v = m.replace(",", "").rstrip(".")
        digits = v.split(".")[0]
        if len(digits) < 3:
            continue
        if "," not in m and "." not in v and len(digits) == 4 and 1900 <= int(digits) <= 2100:
            continue
        out.add(v)
    return out


@check(codes=['G37'], rules=['GOLD-FID'], needs=['prompt', 'inputs', 'solution'], params=['folder'])
def check_shared_identifier_scoped(folder):
    """An identifier two inputs carry with different figures beside it (an alternator feature code reused across data sheets) is scoped, in every golden paragraph or table cell that cites it with one input's figure, by that input's file name or a token only that file's name carries.

    Since: 2026-09-14 (attribution check).
    Source: the platform's attribution / role check matched an unscoped "winding B600-2" in a
    compliance cell to the DQGAB sheet (5,743 kVA) instead of the DQCB sheet (3,313 kVA).
    Drift-notes: fires only when the paragraph carries a figure (three or more digits, not a plain
    year) that sits on the identifier's line in one owning input and on no line carrying it in
    another, so record ids joined across a register and a memo stay quiet. The scope unit is the
    docx paragraph or table cell. A scope token is a stem part of the owning file's name (split on
    _ and -) of three or more characters, with a letter, carried by no other input's name.
    """
    texts = _g37_input_texts(folder)
    if not texts:
        return
    lines_by_tok = {}
    for name, text in texts:
        for line in text.splitlines():
            for rx in _G37_ID_RES:
                for tok in set(rx.findall(line)):
                    lines_by_tok.setdefault(tok, {}).setdefault(name, set()).update(_g37_figures(line))
    shared = {tok: per for tok, per in lines_by_tok.items() if len(per) >= 2}
    if not shared:
        return
    parts_by_file = {}
    for name, _ in texts:
        stem = name.rsplit(".", 1)[0]
        parts_by_file[name] = {p for p in re.split(r"[_\-\s]+", stem) if len(p) >= 3 and re.search(r"[A-Za-z]", p)}

    def scope_tokens(name):
        others = set().union(*(v for k, v in parts_by_file.items() if k != name))
        return {name} | (parts_by_file[name] - others)

    for path in solution_files(folder, {".docx"}):
        try:
            parts = _g25_docx_parts(path)
        except Exception:
            continue
        hits = []
        for _, text in parts:
            for para in text.split("\n"):
                para_figs = _g37_figures(para)
                if not para_figs:
                    continue
                for tok, per in shared.items():
                    if not re.search(r"(?<![\w-])" + re.escape(tok) + r"(?![\w-])", para):
                        continue
                    owners = [n for n, figs in per.items()
                              if (para_figs & figs) - set().union(*(f for k, f in per.items() if k != n))]
                    if not owners:
                        continue
                    scopes = set().union(*(scope_tokens(n) for n in owners))
                    if any(re.search(r"(?<![\w])" + re.escape(sc) + r"(?![\w])", para) for sc in scopes):
                        continue
                    snippet = para.strip()[:90]
                    if (tok, snippet) not in [(t, sn) for t, sn, _ in hits]:
                        hits.append((tok, snippet, sorted(per)))
        for tok, snippet, names in hits[:5]:
            emit("ERROR", f"[G37] {path.name}: \"{snippet}\" cites {tok}, which {', '.join(names)} each carry with "
                          "different figures beside it, and names none of them in that paragraph or cell. The "
                          "attribution check matches the identifier to whichever input it finds first and calls the "
                          "figure a contradiction (2026-09-14: \"winding B600-2\" at "
                          "3,313 kVA read against the DQGAB sheet's 5,743). Name the model or the file beside the identifier")


# G36 (2026-09-14, attribution / role check 1/64): the
# golden labelled its parameters "Class margins for bid work (policy 4.1)" and the judge failed the
# term: "terminology 'policy 4.1' does not appear in any input". The policy numbers its own clauses
# bare ("4.1  Class margins ...") and cross-refers to them bare ("under 4.2"); the addendum cites the
# ITB as "ITB Section 5" and the ITB's own number as "ITB No. 27-04". The golden had coined
# "policy 3.2", "ITB 5" and "ITB 27-04" in eighteen cells. A document noun joined to a number is a
# citation term, and the judge reads it as a term the inputs must carry verbatim.
_G36_CITE_RE = re.compile(
    r"\b(policy|section|itb|rfp|rfq|addendum|article|clause|paragraph|exhibit)\s+((?:no\.\s*)?\d+(?:[.-]\d+)*)\b",
    re.I)


_G36_HOUSE_STYLE_NOUNS = {"section", "article", "clause", "paragraph"}


@check(codes=['G36'], rules=['GOLD-FID'], needs=['inputs', 'solution'], params=['folder'])
def check_coined_citation_terms(folder):
    """A citation the golden writes as a document noun and a number ("policy 4.1", "ITB 5") appears in that exact form in some input; a citation form the inputs never use is coined terminology the attribution check fails.

    Since: 2026-09-14.
    Source: the platform's attribution / role check ("terminology 'policy 4.1' does not appear in any input").
    Tightened: 2026-09-15: formula cells are read by their cached text, since the judge reads values.
    Drift-notes: nouns policy, section, ITB, RFP, RFQ, addendum, article, clause, paragraph, exhibit; fires only when the noun itself occurs in some input, so a golden citing a document the inputs never name is left to the sourcing checks. Matching is case-insensitive with whitespace collapsed, and "No." is part of the form ("ITB 27-04" fails where the inputs write "ITB No. 27-04"). Narrowed 2026-09-15: "Section 6.4" passes when some input cross-refers with the same noun and a dotted number ("subject to Section 2.3") and 6.4 is a numbered clause heading in some input, because that is the inputs' own citation style applied to a clause they carry; the golden had scored 1.0 on two oracle runs with twenty such cites. Only section, article, clause and paragraph are narrowed; "policy 4.1" and "ITB 5" still fail. Narrowed again 2026-09-15: the same pass for a bare integer, "section 4" passes when some input cross-refers with the same noun and an integer ("a certificate under section 8") and 4 is an integer clause heading ("4. Discount and minimum charge") in some input; a grader wrote "Agreement section 4 states 68 percent discount" against that agreement.
    """
    import openpyxl
    from ..common import input_texts, solution_files
    texts = input_texts(folder)
    items = list(texts.items()) if isinstance(texts, dict) else list(texts or [])
    blob = re.sub(r"\s+", " ", "\n".join(t for _, t in items)).lower()
    if not blob:
        return
    def norm(noun, num):
        return re.sub(r"\s+", " ", f"{noun} {num}").lower()
    def present(phrase):
        return re.search(r"(?<![a-z0-9])" + re.escape(phrase) + r"(?![0-9]|\.\d)", blob) is not None
    clause_heads = {m.group(1) for _, t in items for m in re.finditer(r"(?m)^\s*(\d+\.\d+)\s+[A-Z]", t)}
    def noun_dotted(noun):
        return re.search(r"\b" + re.escape(noun.lower()) + r"s? \d+\.\d+\b", blob) is not None
    int_heads = {m.group(1) for _, t in items for m in re.finditer(r"(?m)^\s*(\d{1,2})\.\s+[A-Z]", t)}
    def noun_integer(noun):
        # a sentence-ending period after the number is still an integer cross-reference ("under section 8.")
        return re.search(r"\b" + re.escape(noun.lower()) + r"s? \d{1,2}(?![0-9]|\.\d)", blob) is not None
    for path in solution_files(folder, {".xlsx", ".docx"}):
        strings = []
        if path.suffix == ".xlsx":
            try:
                wb = openpyxl.load_workbook(path, read_only=True)
                wbv = openpyxl.load_workbook(path, read_only=True, data_only=True)
            except Exception:
                continue
            # typed strings, and the cached text of formula cells: a citation inside a formula's string
            # literal reaches the attribution judge as the cell's value (2026-09-15,
            # Bridge_Buy!C33 "Director of Operations, policy 2.4" and its briefing read-through)
            for ws, wsv in zip(wb.worksheets, wbv.worksheets):
                for row, rowv in zip(ws.iter_rows(), wsv.iter_rows()):
                    for c, cv in zip(row, rowv):
                        if isinstance(c.value, str) and not c.value.startswith("="):
                            strings.append((f"{ws.title}!{c.coordinate}", c.value))
                        elif isinstance(cv.value, str):
                            strings.append((f"{ws.title}!{c.coordinate} (formula)", cv.value))
            wb.close()
            wbv.close()
        else:
            try:
                doc = document(path)
            except Exception:
                continue
            strings = [(f"paragraph {i + 1}", p.text) for i, p in enumerate(doc.paragraphs) if p.text.strip()]
        bad = []
        for where, text in strings:
            for m in _G36_CITE_RE.finditer(text):
                noun, num = m.group(1), m.group(2)
                if not re.search(r"\b" + re.escape(noun.lower()) + r"\b", blob):
                    continue
                if present(norm(noun, num)):
                    continue
                if (noun.lower() in _G36_HOUSE_STYLE_NOUNS and re.fullmatch(r"\d+\.\d+", num)
                        and num in clause_heads and noun_dotted(noun)):
                    continue
                if (noun.lower() in _G36_HOUSE_STYLE_NOUNS and re.fullmatch(r"\d{1,2}", num)
                        and num in int_heads and noun_integer(noun)):
                    continue
                bad.append(f"{where} \"{m.group(0)}\"")
        if bad:
            emit("ERROR", f"[G36] {path.name}: {len(bad)} citation(s) in a form no input uses: {'; '.join(bad[:6])}"
                          f"{' ...' if len(bad) > 6 else ''}. The attribution check reads a document noun "
                          "plus a number as a term and fails it when no input carries that exact form "
                          "(2026-09-14, 'policy 4.1' where the policy cites its "
                          "clauses bare). Cite in the input's own form: the bare clause number, "
                          "'ITB Section 5', 'ITB No. 27-04'")


_SECOND_LOC_HDR_RE = re.compile(r"^\s*(?:SECOND|DUPLICATE|OTHER|ADDITIONAL)\s+(?:BIN|LOCATION|SLOT)S?\s*$|^\s*ALSO\s+IN\s*$", re.I)
_FROM_LOC_HDR_RE = re.compile(r"^\s*FROM(?:\s+(?:BIN|LOCATION|SLOT))?\s*$", re.I)


@check(codes=['G38'], rules=['GOLD-FID'], needs=['solution'], params=['folder'])
def check_second_locations_on_move_list(folder):
    """Every second location the golden records for an item appears as a from-location on the golden's move list.

    Since: 2026-09-14 (Golden deliverable, Major).
    Source: a grader found four items the location master shows in two bins counted as
    "second bins cleared" on the Items tab while the crew move list, one row per moving item read
    by INDEX/MATCH on a single order column, could carry only each item's primary bin as its from
    bin; WH-4 section 10 and the requester's email require a from and a to bin on every line.
    Drift-notes: reads cached values; a second-location column is a header SECOND/DUPLICATE/OTHER
    BIN (or LOCATION, SLOT) or ALSO IN, a move list is any column headed FROM, FROM BIN or FROM
    LOCATION; silent when the golden has no FROM column.
    """
    import openpyxl
    for x in solution_files(folder, {".xlsx"}):
        try:
            wb = openpyxl.load_workbook(x, data_only=True, read_only=True)
        except Exception:
            continue
        seconds, froms = {}, set()
        for ws in wb.worksheets:
            rows = list(ws.iter_rows(values_only=True))
            for hi, row in enumerate(rows[:8]):
                for ci, h in enumerate(row):
                    if not isinstance(h, str):
                        continue
                    target = seconds if _SECOND_LOC_HDR_RE.match(h) else froms if _FROM_LOC_HDR_RE.match(h) else None
                    if target is None:
                        continue
                    for r in rows[hi + 1:]:
                        v = r[ci] if ci < len(r) else None
                        if isinstance(v, str) and v.strip() and " " not in v.strip():
                            if target is froms:
                                froms.add(v.strip())
                            else:
                                seconds.setdefault(v.strip(), f"{ws.title} {h.strip()}")
        if not froms or not seconds:
            continue
        missing = sorted(k for k in seconds if k not in froms)
        if missing:
            emit("ERROR", f"[G38] {x.name}: {len(missing)} of {len(seconds)} second locations recorded under "
                          f"{seconds[missing[0]]} never appear as a from-location on the move list "
                          f"({', '.join(missing[:4])}) - a grader failed a task on exactly this "
                          "(2026-09-14, Major): a second bin counted as cleared is a modeled end state, not a "
                          "crew line. Give each second location its own ordered line with a from and a to "
                          "location, counted against the crew budget")


_G39_NUM_RE = re.compile(r"^-?[\d,]+(?:\.\d+)?$")


@check(codes=['G39'], rules=['GOLD-FID'], needs=['solution'], params=['folder'])
def check_shared_value_header_across_tables(folder):
    """Two tables in a solution document that key their rows on the same first-column label never carry an identically named value column with different figures for the same row key; the numeric grounding audit reads the pair as one figure stated twice and reports an internal contradiction.

    Since: 2026-09-15.
    Source: the numeric grounding (method audit) failed in both evaluations with four D3_disagreement items, "NB-6010 / Program value — 160266.6 ... 182868.3", because the withheld schedule and the unfilled schedule both headed their money column "Program value" over the same five items.
    Drift-notes: docx tables only; tables are grouped by their first header cell, a row key is the first cell and a key repeated inside one table is skipped; both cells must read as numbers (commas allowed) and differ; renaming the header after what it values ("Program value withheld") clears it.
    """
    by_doc = {}
    for name, ti, body in _docx_tables(folder):
        if len(body) < 2 or not body[0]:
            continue
        keys = [r[0] for r in body[1:] if r]
        dup = {k for k in keys if keys.count(k) > 1}
        cols = {}
        for ci, h in enumerate(body[0][1:], start=1):
            h = h.strip()
            if not h:
                continue
            vals = {}
            for r in body[1:]:
                if len(r) > ci and r[0] not in dup and _G39_NUM_RE.match(r[ci].strip() or "x"):
                    vals[r[0]] = r[ci].strip()
            if vals:
                cols[h.lower()] = (h, vals)
        by_doc.setdefault(name, {}).setdefault(body[0][0].strip().lower(), []).append((ti, cols))
    for name, groups in by_doc.items():
        bad = []
        for first, tables in groups.items():
            for a in range(len(tables)):
                for b in range(a + 1, len(tables)):
                    ta, ca = tables[a]
                    tb, cb = tables[b]
                    for h in set(ca) & set(cb):
                        for k in set(ca[h][1]) & set(cb[h][1]):
                            va, vb = ca[h][1][k], cb[h][1][k]
                            if va.replace(",", "") != vb.replace(",", ""):
                                bad.append(f"tables {ta + 1} and {tb + 1} \"{ca[h][0]}\" for {k}: {va} and {vb}")
                                break
        if bad:
            emit("ERROR", f"[G39] {name}: {len(bad)} value column(s) named alike in two tables keyed on the same rows carry different "
                          f"figures: {'; '.join(bad[:4])}. The numeric grounding audit reads them as one figure stated twice and "
                          "fails the golden on an internal contradiction (2026-09-15, "
                          "'Program value' on the withheld and the unfilled schedules). Name each column after what it values")
