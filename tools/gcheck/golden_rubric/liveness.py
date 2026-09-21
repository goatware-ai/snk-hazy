"""Group 2: formula-liveness criteria and answer keys (GOLD-LIVE, GOLD-KEY).

Generated 2026-09-04 from autoeval_check.py; every check body is verbatim.
"""
import re
from pathlib import Path
from ..common import LIVENESS_STRICT_RE, RANGE_KEY_RE, _COUNT_RE, _FIGURE_RE, _MONEY_RE, _YEAR_RE, _col_num, _without_cell_refs, workbook
from ..core import check, emit, recommend, REPORT, OPTIONS, FINDINGS


# Anchored to the key: the verb must directly follow the range ("!C3:C30 store
# SUMIFS"), else a later bare-range assertion gets misattributed to the previous
# quoted key (marathon C29 chain wording, run-5 rework).
FUNC_ASSERT_RE = re.compile(r"\A[\s,]{0,2}(?:all\s+|each\s+)?(?:stores?|contains?|holds?|carr(?:y|ies))\b[^.;)]{0,30}?\b(SUMIFS?|SUMPRODUCT|X?LOOKUP|VLOOKUP|INDEX|COUNTIFS?|IF)\b")


FUNC_BEFORE_RE = re.compile(r"\b(SUMIFS?|SUMPRODUCT|X?LOOKUP|VLOOKUP|COUNTIFS?)\b[^.;]{0,20}\($")


# Function names worth cross-checking when a criterion cites them. Deliberately
# excludes short/English-ambiguous tokens (IF, SUM, MIN, MAX, AND, OR, NOT).
FUNC_TOKENS_RE = re.compile(
    r"\b(LARGE|SMALL|INDEX|MATCH|VLOOKUP|HLOOKUP|XLOOKUP|LOOKUP|SUMIFS?|SUMPRODUCT|COUNTIFS?"
    r"|AVERAGEIFS?|FLOOR|CEILING|OFFSET|INDIRECT|RANK|AGGREGATE|ROUND(?:UP|DOWN)?|SUBTOTAL"
    r"|CHOOSE|TEXTJOIN|FILTER|SORT|UNIQUE)\b")


def _quoted_formula_after(text, start):
    """Extract a ' =FORMULA' snippet following a cell key, paren-balanced.

    Accepts paren-less reference/arithmetic hops too (=C3*D3, ='Usage Rollup'!E3
    — the chain keys marathon run 5 showed judges trace hop by hop), ending them
    at the first bare whitespace outside quotes/parens.
    """
    m = re.match(r"\s*(=['A-Z@_].*)", text[start:], re.S)
    if not m:
        return None
    body, depth, in_quote, out = m.group(1), 0, False, []
    for ch in body:
        if ch == "'":
            in_quote = not in_quote
        elif not in_quote:
            if ch == "(":
                depth += 1
            elif ch == ")":
                if depth == 0:
                    break
                depth -= 1
            elif ch in ";\n" or (ch in ", " and depth == 0):
                break
        out.append(ch)
    snippet = "".join(out).strip()
    return snippet if "(" in snippet or re.search(r"\b[A-Z]{1,3}\d+\b", snippet) else None


def _load_task_sheets(folder):
    """sheet name -> list of openpyxl worksheets across all task xlsx (formulas kept)."""
    sheets = {}
    for sub in ("solution", "inputs"):
        d = folder / sub
        for path in sorted(d.glob("*.xlsx")) if d.is_dir() else []:
            try:
                wb = workbook(path)
            except Exception:
                continue
            for ws in wb.worksheets:
                sheets.setdefault(ws.title, []).append(ws)
    return sheets


def _load_task_sheets_cached(folder):
    """sheet name -> worksheets across all task xlsx, cached VALUES (data_only)."""
    sheets = {}
    for sub in ("solution", "inputs"):
        d = folder / sub
        for path in sorted(d.glob("*.xlsx")) if d.is_dir() else []:
            try:
                wb = workbook(path, data_only=True)
            except Exception:
                continue
            for ws in wb.worksheets:
                sheets.setdefault(ws.title, []).append(ws)
    return sheets


STATED_NUM_RE = re.compile(r"-?\$?\d[\d,]*(?:\.\d+)?")


LIVENESS_CRIT_RE = re.compile(r"formula|live\b|=[A-Z]{2,}\(", re.I)


@check(codes=['R8'], rules=['GOLD-KEY'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_key_values(rows, folder):
    """A criterion that states a numeric answer and keys a single golden cell states that cell's cached value.

    R8: a criterion states a numeric answer AND keys a single golden cell, but
    that cell's cached value is not among the numbers the criterion states.

    Answer-keyed criteria are what stabilised the oracle (task 06 C29/C32), and the
    judge takes a stated key at face value, so a key that has drifted away from the
    number beside it fails the run deterministically. R5 only proves the key
    RESOLVES; this proves it still says what the criterion claims. Cheap insurance
    whenever the golden workbook is edited after the rubric was written (dillman
    2026-08-19 rebuilt its settings and usage tabs under a finished rubric).

    Liveness criteria are exempt: they point at a cell to show WHERE a formula lives
    and legitimately state no value (marathon C31, boettcher C29 both fire without
    the carve-out).
    """
    sheets = _load_task_sheets_cached(folder)
    if not sheets:
        return
    for num, text, _ in rows:
        if LIVENESS_CRIT_RE.search(text):
            continue
        stated = set()
        for m in STATED_NUM_RE.finditer(text):
            try:
                stated.add(float(m.group(0).replace("$", "").replace(",", "")))
            except ValueError:
                pass
        if not stated:
            continue
        for m in RANGE_KEY_RE.finditer(text):
            name = m.group(1) or m.group(2)
            c1, r1, c2 = m.group(3), int(m.group(4)), m.group(5)
            if c2:
                continue
            targets = sheets.get(name)
            if not targets:
                continue
            vals = [ws.cell(row=r1, column=_col_num(c1)).value for ws in targets]
            vals = [v for v in vals
                    if isinstance(v, (int, float)) and not isinstance(v, bool)]
            if not vals:
                continue
            v = vals[0]
            if any(abs(v - n) <= max(0.005 * abs(v), 0.01) for n in stated):
                continue
            emit("ERROR", f"C{num} [R8] key '{name}'!{c1}{r1} caches {v!r}, which is none of the "
                          f"numbers the criterion states ({', '.join(str(n) for n in sorted(stated))}) "
                          "- the judge reads a stated key at face value, so a drifted key fails every "
                          "oracle run; re-derive the criterion against the current golden")


@check(codes=['R5', 'R7'], rules=['GOLD-KEY', 'GOLD-LIVE'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_rubric_keys(rows, folder):
    """Every answer key resolves to an existing sheet and cell, its asserted function is what the cells store, and a keyed range stores pure single-call formulas.

    Codes:
      R5  a key names a sheet the task workbooks carry, inside its used area, and its asserted or quoted formula is what the cell stores
      R7  a keyed range asserting a function stores pure single-call formulas, never compound ones
    Since: 2026-08-19 (marathon C29 runs 4/6/7, R7).
    Source: the oracle, which misreads compound cells as typed values.
    """
    sheets = _load_task_sheets(folder)
    if not sheets:
        return
    for num, text, _ in rows:
        for m in RANGE_KEY_RE.finditer(text):
            name = m.group(1) or m.group(2)
            c1, r1, c2, r2 = m.group(3), int(m.group(4)), m.group(5), m.group(6)
            targets = sheets.get(name)
            if not targets:
                emit("ERROR", f"C{num} [R5] key cites sheet '{name}' — no such sheet in any task workbook")
                continue
            lo_c, hi_c = _col_num(c1), _col_num(c2 or c1)
            lo_r, hi_r = r1, int(r2 or r1)
            if not any(hi_r <= ws.max_row and hi_c <= ws.max_column for ws in targets):
                emit("ERROR", f"C{num} [R5] key '{name}'!{c1}{r1}:{c2 or c1}{r2 or r1} lies outside "
                              f"the sheet's used area ({max(ws.max_row for ws in targets)} rows, "
                              f"{max(ws.max_column for ws in targets)} cols)")
                continue
            func = None
            after = FUNC_ASSERT_RE.search(text[m.end():m.end() + 60])
            before = FUNC_BEFORE_RE.search(text[:m.start()][-40:])
            if after:
                func = after.group(1)
            elif before:
                func = before.group(1)
            if func:
                ok = any(all(isinstance((ws.cell(row=r, column=c).value), str)
                             and ws.cell(row=r, column=c).value.startswith("=")
                             and func in ws.cell(row=r, column=c).value.upper()
                             for r in range(lo_r, hi_r + 1) for c in range(lo_c, hi_c + 1))
                         for ws in targets)
                if not ok:
                    emit("ERROR", f"C{num} [R5] key asserts every cell of '{name}'!{c1}{r1}:"
                                  f"{c2 or c1}{r2 or r1} stores a {func} formula, but the workbook disagrees")
                    continue
                # R7: a key over cells whose stored formula is COMPOUND (the named
                # function plus further terms, e.g. =SUMIFS(...)+IF(...,SUMIFS(...)))
                # is judge-illegible: oracle judges verified pure single-call ranges
                # ('Program Scenarios'!B3:C7 =SUMIFS(...)) on every marathon run but
                # misread the compound Usage Rollup C column as typed values in runs
                # 4, 6, and 7 (run 7: "C3 contains typed 180", 3/3, wording-proof).
                def _pure(v):
                    if not re.match(rf"=\s*{func}\(", v, re.I):
                        return False
                    depth, in_q = 0, False
                    for i, ch in enumerate(v):
                        if ch == '"':
                            in_q = not in_q
                        elif not in_q:
                            if ch == "(":
                                depth += 1
                            elif ch == ")":
                                depth -= 1
                                if depth == 0:
                                    return i == len(v) - 1
                    return False
                for ws in targets:
                    cells = [ws.cell(row=r, column=c).value
                             for r in range(lo_r, hi_r + 1) for c in range(lo_c, hi_c + 1)]
                    if not all(isinstance(v, str) and v.startswith("=") and func in v.upper()
                               for v in cells):
                        continue
                    impure = [v for v in cells if not _pure(v)]
                    if impure:
                        emit("ERROR", f"C{num} [R7] key asserts '{name}'!{c1}{r1}:{c2 or c1}{r2 or r1} "
                                     f"store {func}, but {len(impure)} cell(s) store COMPOUND formulas "
                                     f"(e.g. {impure[0][:60]!r}) — judges misread compound cells as "
                                     "typed values (marathon C29 runs 4/6/7); anchor the criterion on "
                                     "a pure single-call range, simplify the golden formula, or drop it")
                    break
                continue
            quoted = _quoted_formula_after(text, m.end()) if not c2 else None
            if quoted:
                want = quoted.lstrip("=").replace(" ", "")
                got = [str(ws.cell(row=lo_r, column=lo_c).value or "").lstrip("=").replace(" ", "")
                       for ws in targets]
                if not any(g == want for g in got):
                    emit("ERROR", f"C{num} [R5] key quotes '{name}'!{c1}{r1} as ={want} but the stored "
                                  f"formula is {got[0][:80]!r}")


def _r90_function_tokens(rows):
    """A liveness criterion names no spreadsheet function token.

    Since: 2026-08-24 (branch-stocking-reset run 5).
    Source: the oracle (search_xlsx greps cached values and can never find the token).
    Drift-notes: numbered R39 in the monolith until 2026-09-04.
    """
    for num, text, weight in rows:
        if weight <= 0 or not LIVENESS_STRICT_RE.search(text):
            continue
        named = sorted({f for f in _R39_FUNCS if re.search(rf"\b{f}\b", text)})
        if not named:
            continue
        emit("ERROR", f"C{num} [R90] names the function token(s) {', '.join(named)} in a liveness "
                     "criterion, but the judge's search tool greps cached VALUES, not formulas, "
                     "so that token is unfindable and the criterion passes only when the run "
                     "happens to reach for the formula summary (branch-stocking-reset run 5: "
                     "\"no matches for pattern 'COUNTIF' across 8 sheet(s)\" against a golden "
                     "that really does use COUNTIFS). Claim a read-through instead, plain cell "
                     "references into the named tab plus a cached value anchor, with no "
                     "function name in the criterion")


def _r44_function_range_liveness(rows):
    """Liveness is graded on plain read-through cells, never on a range storing a named function.

    Since: june-price-review run 3 (2/3 despite W4/W10 anchoring).
    Source: the oracle.
    Drift-notes: numbered R40 in the monolith until 2026-09-04.
    """
    for num, text, weight in rows:
        if weight > 0 and _FN_RANGE_LIVENESS_RE.search(text) \
                and re.search(r"rather than typed|not (?:as )?a typed|typed (?:amounts|constants)", text, re.I):
            emit("ERROR", f"C{num} [R44] grades liveness on a range storing a named function — "
                          "this flaked 2/3 on june-price-review run 3 despite full W4/W10 "
                          "anchoring (value-mode read, the marathon run-6 stall). Grade cells "
                          "holding a plain =Tab!Cell reference instead, split into disjoint "
                          "cell sets if the weight needs two criteria")


@check(codes=['R6', 'R90', 'R44'], rules=['GOLD-LIVE'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_named_functions(rows, folder):
    """A criterion names no spreadsheet function token, and grades liveness on plain read-through cells rather than on a range storing a function.

    Codes:
      R6   a criterion cites no function name: the judge greps cached values, never formula text, and fails on a token it cannot find
      R90  a liveness criterion names no spreadsheet function token
      R44  liveness is graded on plain read-through cells, never on a range storing a named function
    Since: R6 deadstock run 4 and rademacher C44 (2026-08-24); R90 2026-08-24 (branch-stocking-reset run 5); R44 june-price-review run 3.
    Source: the oracle (search_xlsx greps cached values; the formula summary surfaces head functions only).
    Drift-notes: R90 and R44 were carve-out twins (numbered R39 and R40 in the monolith), merged back 2026-09-11.
    """
    _r44_function_range_liveness(rows)     # [R44] the carve-out twin, merged back 2026-09-11
    _r90_function_tokens(rows)     # [R90] the carve-out twin, merged back 2026-09-11
    heads, anywhere = set(), set()
    sol = folder / "solution"
    for path in sorted(sol.glob("*.xlsx")) if sol.is_dir() else []:
        try:
            wb = workbook(path)
        except Exception:
            continue
        for ws in wb.worksheets:
            for row in ws.iter_rows():
                for c in row:
                    v = c.value
                    if isinstance(v, str) and v.startswith("="):
                        m = re.match(r"=\s*([A-Z][A-Z0-9.]*)\(", v)
                        if m:
                            heads.add(m.group(1))
                        anywhere.update(re.findall(r"\b([A-Z][A-Z0-9.]*)\(", v))
    if not anywhere:
        return
    for num, text, _ in rows:
        for tok in sorted(set(FUNC_TOKENS_RE.findall(text))):
            if tok not in anywhere:
                emit("ERROR", f"C{num} [R6] cites function {tok}, which no stored solution formula "
                              "uses — answer-key drift; the judge will search for it and fail")
            elif tok not in heads:
                emit("ERROR", f"C{num} [R6] cites function {tok}, which appears only NESTED inside "
                              "other functions — judge tooling surfaces head functions and greps "
                              "values, so the token is invisible (deadstock C18 run 4, 3/3 fail); "
                              "cite the outermost function or key on displayed values instead")
            else:
                # Being a HEAD function is not enough. rademacher C44 named COUNTIF,
                # the golden stores eight head-function COUNTIFs, and the judge still
                # failed it 3/3 reporting "No matches for pattern 'COUNTIF' across 9
                # sheet(s)": search_xlsx greps cached VALUES, so it searched for the
                # literal string and found none. Any function token in a criterion is
                # a search the judge can lose.
                emit("ERROR", f"C{num} [R6] cites function {tok}. It IS a head function here, but the "
                             "judge greps cached values, not formula text, and fails the criterion when "
                             "the literal token returns nothing (rademacher C44 named COUNTIF over eight "
                             "stored head-function COUNTIFs and failed 3/3, 2026-08-24). State the "
                             "liveness demand without the token and give the judge a value and a label "
                             "to land on instead")


# R30 (2026-08-23, vondrak run 1): a strict liveness criterion that names neither a head
# function nor "cell reference" gives the judge nothing to land on. C23 asked for "stored
# formulas over the impact, move and rebate cells" and every one of those cells was a
# compound =ROUND(...) expression, the shape R7 already reports reads as typed (marathon C29),
# but R7 only fires on a keyed range and C23 keyed none. The judge failed it 1/3 with the
# cached values quoted back as evidence. Key strict liveness on a named pure single-call
# head (COUNTIF over the verdict column, SUM over the savings column) or on plain cell
# references (the reference-chain page); an unanchored "stored formulas" criterion flakes.
# SUPERSEDED IN PART, 2026-08-24: naming the head function turned out to be the worse of the
# two repairs, because search_xlsx greps cached values and never sees the token. See R39. The
# surviving advice is the other half, plain cell references into a named tab.
LIVENESS_LAND_RE = re.compile(
    r"\b(?:cell references?|SUM|SUMIFS?|COUNTIFS?|COUNTA?|AVERAGEIFS?|SUMPRODUCT|MAX|MIN|INDEX|MATCH"
    r"|VLOOKUP|XLOOKUP|IF|ROUND|ABS)\b")


@check(codes=['R30'], rules=['GOLD-LIVE'], needs=['rubric'], params=['rows'])
def check_liveness_landing(rows):
    """A strict liveness criterion names a plain cell reference or a head function for the judge to land on.

    Since: 2026-08-23 (vondrak run 1, C23).
    Source: the oracle.
    Drift-notes: superseded in part 2026-08-24 (R90): plain cell references are the surviving repair, never a function token.
    """
    for num, text, weight in rows:
        if weight <= 0 or not LIVENESS_STRICT_RE.search(text):
            continue
        body = re.sub(r"a plain cell reference to such a formula[^,.;]*", "", text, flags=re.I)
        if not LIVENESS_LAND_RE.search(body):
            emit("ERROR", f"C{num} [R30] strict liveness criterion names no head function and no "
                         "plain cell reference for the judge to land on (vondrak run 1: 'stored "
                         "formulas over the impact, move and rebate cells' sat over compound "
                         "ROUND formulas and flaked 1/3). Key it on plain cell references into "
                         "a named tab plus a cached value anchor; do NOT reach for a head "
                         "function name to fix this, see R39 (branch-stocking-reset run 5), "
                         "because the judge greps cached values and can never find the token")


# R72 (2026-08-31, inbound-consolidation-plan AutoEval round 1): a strict liveness
# criterion that claims reference-chain form ("cell references") and pins a decimal
# anchor whose golden cell stores an ARITHMETIC formula flakes with nothing else wrong.
# C11 pinned 4,545.38 as "reached through stored formulas whose operands are cell
# references"; the judge landed on 'Vendors'!K6 (match: exact) every run, but K6 stores
# =ROUND(E6-I6+J6,2), the compound shape R7 documents as judge-illegible (marathon runs
# 4/6/7), and the criterion failed 1 of 3 oracle runs at 0.8958 with the platform
# marking it flaky. R30 was satisfied by the words "cell references", so no check ever
# compared the claim against the stored formula of the cell the value actually lives in.
# A cell is judge-legible when it stores a plain reference (=K6, ='Vendors'!K6) or a
# single pure function call whose arguments carry no arithmetic (=SUM(K5:K10),
# =SUMIF(...)); +-*/ between terms, inside or outside a wrapping call, reads as typed
# to some judges. Fires only when NO cell carrying the pinned value is legible.
_R72_DECIMAL_RE = re.compile(r"\d[\d,]*\.\d{1,4}")


_R72_PLAIN_REF_RE = re.compile(
    r"=\s*(?:'[^']{1,40}'!|[A-Za-z_][A-Za-z0-9_.]{0,40}!)?\$?[A-Z]{1,3}\$?\d{1,5}\s*$")


def _r72_legible(v):
    if _R72_PLAIN_REF_RE.match(v):
        return True
    if not re.match(r"=\s*[A-Z][A-Z0-9.]*\(", v, re.I):
        return False
    v = v.rstrip()
    depth, in_q = 0, False
    for i, ch in enumerate(v):
        if ch == '"':
            in_q = not in_q
        elif not in_q:
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0 and i != len(v) - 1:
                    return False
            elif depth >= 1 and ch in "+-*/^&":
                return False
    return depth == 0


@check(codes=['R72'], rules=['GOLD-LIVE'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_liveness_anchor_cells(rows, folder):
    """Strict reference-chain liveness is pinned on a value whose cell is a reference or one aggregation, never arithmetic."""
    crits = [(num, text) for num, text, weight in rows
             if weight > 0 and LIVENESS_STRICT_RE.search(text)
             and re.search(r"cell references?", text, re.I)
             and _R72_DECIMAL_RE.search(text)]
    d = Path(folder) / "solution"
    paths = sorted(d.glob("*.xlsx")) if d.is_dir() else []
    if not (paths and crits):
        return
    carriers = {}  # cached decimal value -> [(cell ref, stored formula or None)]
    for path in paths:
        try:
            wbf = workbook(path)
            wbv = workbook(path, data_only=True)
        except Exception:
            continue
        for ws in wbf.worksheets:
            wsv = wbv[ws.title]
            for row in ws.iter_rows():
                for c in row:
                    v = wsv.cell(row=c.row, column=c.column).value
                    if isinstance(v, (int, float)) and not isinstance(v, bool):
                        f = c.value if isinstance(c.value, str) and c.value.startswith("=") else None
                        carriers.setdefault(round(float(v), 4), []).append(
                            (f"'{ws.title}'!{c.coordinate}", f))
    for num, text in crits:
        for lit in _R72_DECIMAL_RE.findall(text):
            cells = carriers.get(round(float(lit.replace(",", "")), 4))
            if not cells or any(f and _r72_legible(f) for _ref, f in cells):
                continue
            ref, f = cells[0]
            emit("ERROR", f"C{num} [R72] pins {lit} as reached through cell references, but every "
                          f"golden cell carrying it stores an arithmetic or compound formula "
                          f"({ref} = {(f or 'typed constant')[:60]!r}), the shape judges misread as "
                          "typed (marathon C29 runs 4/6/7; inbound-consolidation-plan C11 flaked "
                          "1/3 on 'Vendors'!K6 =ROUND(E6-I6+J6,2), 2026-08-31). Re-key the "
                          "criterion on the value and its arithmetic chain in the workbook's own "
                          "nouns, or point the liveness demand at a plain reference-chain cell")
            break


# R36 (2026-08-20, luebbert run 2): see the module docstring. A liveness criterion that
# names how wide the summed range is must match the stored formula of the cell that
# actually carries the value it states, because that is the cell the judge opens.
_SPAN_WORDS = {"two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
               "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12}


_SPAN_RE = re.compile(
    r"\bacross\s+(?:the\s+)?(\d{1,2}|" + "|".join(_SPAN_WORDS) + r")\s+"
    r"(?:\w+\s+){0,2}?(column|row)s\b", re.I)


_SUM_RANGE_RE = re.compile(
    r"\A=\s*SUM\(\s*\$?([A-Z]{1,3})\$?(\d{1,5})\s*:\s*\$?([A-Z]{1,3})\$?(\d{1,5})\s*\)\Z",
    re.I)


# The proven shape only: a SUMPRODUCT whose argument multiplies a comparison, ((range="X")*1),
# ((range<>"")*range). Plain arithmetic (=C10-C11, =ROUND(D16-D17,2)) is left to R72, which has
# oracle evidence on pinned decimals; eleven accepted or in-flight goldens carry it on their
# front-page read-throughs and have passed 3/3, so it is not a flake shape on its own.
_R96_BOOL_PRODUCT_RE = re.compile(r"SUMPRODUCT\s*\(.*\([^()]*(?:<>|>=|<=|=|<|>)[^()]*\)\s*\*", re.I | re.S)
_R96_DEMAND_RE = re.compile(r"\bformulas?\b|rather than (?:a )?(?:keyed|typed)|typed constants?|cell references?", re.I)


@check(codes=['R96'], rules=['GOLD-LIVE'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_readthrough_targets(rows, folder):
    """A cell a plain reference points at never stores a SUMPRODUCT multiplying a comparison when the rubric demands live computation.

    R96 (2026-09-04, pick-module-reslot golden_solution_check 2/3): a front-page cell was a
    plain reference (=Items!$D$345) into a summary cell storing
    =SUMPRODUCT((range="SEP 12-13")*range), and one judge followed the reference, read the
    boolean-product SUMPRODUCT as 'a hardcoded typed numeric value', and failed a +1
    'computed in a cell rather than keyed' criterion (0.9792). R72 tests only the cells that
    carry a pinned decimal; a rule-only rubric pins nothing, so nothing tested the cell the
    read-through lands on. A cell that a plain reference points at must not store the proven
    shape, a SUMPRODUCT multiplying a comparison, whenever the rubric demands live computation
    anywhere; re-key it as COUNTIF / COUNTIFS / SUMIFS / SUMPRODUCT(range,range). Plain
    arithmetic is left to R72. Re-key the target, never the reference."""
    if not any(w > 0 and _R96_DEMAND_RE.search(t) for _, t, w in rows):
        return
    d = Path(folder) / "solution"
    for path in sorted(d.glob("*.xlsx")) if d.is_dir() else []:
        try:
            wb = workbook(path)
        except Exception:
            continue
        seen = set()
        for ws in wb.worksheets:
            for row in ws.iter_rows():
                for c in row:
                    v = c.value
                    if not (isinstance(v, str) and _R72_PLAIN_REF_RE.match(v)):
                        continue
                    m = re.match(r"=\s*(?:'([^']+)'!|([A-Za-z_][A-Za-z0-9_.]*)!)?\$?([A-Z]{1,3})\$?(\d+)\s*$", v)
                    if not m:
                        continue
                    sheet = m.group(1) or m.group(2) or ws.title
                    if sheet not in wb.sheetnames:
                        continue
                    tgt = wb[sheet][f"{m.group(3)}{m.group(4)}"]
                    f = tgt.value
                    if not (isinstance(f, str) and f.startswith("=")) or not _R96_BOOL_PRODUCT_RE.search(f):
                        continue
                    key = (sheet, tgt.coordinate)
                    if key in seen:
                        continue
                    seen.add(key)
                    emit("ERROR", f"[R96] {path.name}: {ws.title}!{c.coordinate} reads through to "
                                  f"{sheet}!{tgt.coordinate}, which stores {f[:70]!r} - a boolean-product "
                                  "or arithmetic formula one oracle judge read as 'a hardcoded typed numeric "
                                  "value' after following the reference (pick-module-reslot, 2026-09-04, "
                                  "0.9792 on a +1 'computed in a cell' row). Re-key the target as one pure "
                                  "call with no arithmetic in its arguments (COUNTIF / COUNTIFS / SUMIFS / "
                                  "SUMPRODUCT(range,range)) and leave the reference as it is")


def _col_index(letters):
    n = 0
    for ch in letters.upper():
        n = n * 26 + ord(ch) - 64
    return n


@check(codes=['R36'], rules=['GOLD-LIVE'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_sum_span(rows, folder):
    """A criterion stating how many columns or rows a total sums matches the stored SUM range of the cell carrying that total.

    Since: 2026-08-20 (luebbert run 2, C28).
    Source: the oracle.
    """
    d = folder / "solution"
    paths = sorted(d.glob("*.xlsx")) if d.is_dir() else []
    if not paths:
        return
    # value -> list of (sheet, ref, span) for cells storing a single SUM(range)
    by_value = {}
    for path in paths:
        try:
            wbf = workbook(path)
            wbv = workbook(path, data_only=True)
        except Exception:
            continue
        for ws in wbf.worksheets:
            wsv = wbv[ws.title]
            for row in ws.iter_rows():
                for c in row:
                    if not (isinstance(c.value, str) and c.value.startswith("=")):
                        continue
                    m = _SUM_RANGE_RE.match(c.value.strip())
                    if not m:
                        continue
                    c1, r1, c2, r2 = _col_index(m.group(1)), int(m.group(2)), \
                        _col_index(m.group(3)), int(m.group(4))
                    span = (abs(c2 - c1) + 1) if r1 == r2 else (abs(r2 - r1) + 1)
                    axis = "column" if r1 == r2 else "row"
                    val = wsv[c.coordinate].value
                    if isinstance(val, (int, float)):
                        key = f"{val:,.0f}" if float(val).is_integer() else f"{val:,}"
                        by_value.setdefault(key, []).append((ws.title, c.coordinate, span, axis))
    if not by_value:
        return
    for num, text, weight in rows:
        if weight <= 0:
            continue
        m = _SPAN_RE.search(text)
        if not m:
            continue
        want = int(m.group(1)) if m.group(1).isdigit() else _SPAN_WORDS[m.group(1).lower()]
        figs = [f for f in _FIGURE_RE.findall(_without_cell_refs(text))
                if not _YEAR_RE.match(f.replace(",", ""))]
        figs += [f for f in _COUNT_RE.findall(_without_cell_refs(text))]
        seen = [(f, by_value[f]) for f in dict.fromkeys(figs) if f in by_value]
        if not seen:
            continue
        bad = [(f, cells) for f, cells in seen
               if not any(sp == want for _, _, sp, _ in cells)]
        if bad and len(bad) == len(seen):
            f, cells = bad[0]
            where = ", ".join(f"{sh}!{ref} sums {sp}" for sh, ref, sp, _ in cells[:3])
            emit("ERROR", f"C{num} [R36] says the total is summed across {want} {m.group(2)}s, but "
                         f"the cell carrying the stated {f} sums a different width ({where}). The "
                         "judge opens the cell holding the number, not the cell you had in mind, "
                         "and reads the mismatch as a typed value (luebbert C28 run 2, 1/3, the "
                         "only thing between 0.9868 and a pass). Match the stored formula to the "
                         "described span, or restate the span")


COMPOUND_AGG_RE = re.compile(r"^(SUM|SUMIFS|SUMPRODUCT|COUNTIFS?|AVERAGEIFS?)\(")


@check(codes=['R16'], rules=['GOLD-LIVE'], needs=['solution'], params=['folder'])
def check_compound_totals(folder):
    """A golden total cell stores one pure aggregation, never an aggregation plus further terms.

    R16: a golden total cell stores an aggregation plus further terms
    (=SUM(L5:O5)+P5). The oracle judge's xlsx_formula_summary renders it normalised
    (task 12 run 2, 2026-08-19: the judge quoted "Plan!Q5: =SUM(L5:P5)" for a stored
    =SUM(L5:O5)+P5) and the liveness criterion covering that column failed 1 of 3
    runs at weight 5, sinking the run to 0.9537. Widen the range so the total is one
    pure call, or keep the extra term in its own cell.
    """
    sol = folder / "solution"
    for path in sorted(sol.glob("*.xlsx")) if sol.is_dir() else []:
        try:
            wb = workbook(path)
        except Exception:
            continue
        hits = []
        for ws in wb.worksheets:
            for row in ws.iter_rows():
                for c in row:
                    v = c.value
                    if not isinstance(v, str) or not v.startswith("="):
                        continue
                    body = v[1:]
                    if not COMPOUND_AGG_RE.match(body):
                        continue
                    depth = 0
                    for i, ch in enumerate(body):
                        if ch == "(":
                            depth += 1
                        elif ch == ")":
                            depth -= 1
                            if depth == 0:
                                if body[i + 1:].strip():
                                    hits.append(f"{ws.title}!{c.coordinate} {v}")
                                break
        if hits:
            emit("ERROR", f"[R16] {path.name}: {len(hits)} aggregation cells store a compound total "
                         f"(e.g. {hits[0]}) — the judge's formula summary normalises these and a liveness "
                         "criterion over that column flaked 1/3 on task 12 run 2 (0.9537); make the total a "
                         "single pure call over a widened range")


LIVENESS_CRIT_POS_RE = re.compile(r"stored (?:cell )?formulas?|live formulas?|rather than (?:being )?typed|typed constants?", re.I)


@check(codes=['R17'], rules=['GOLD-LIVE'], needs=['rubric'], params=['rows'])
def check_liveness_count(rows):
    """A rubric carries fewer than three formula-only liveness positives, since each one multiplies the flake exposure.

    R17: a rubric carrying three or more formula-only liveness positives multiplies
    its own flake exposure.

    Kolterman run 1 (2026-08-20): C25, C26 and C27 were near-identical liveness
    criteria over three different tabs. C26 and C27 passed 3/3; C25 failed 2/3 with the
    judge quoting the exact SUMIFS it could not "observe", which alone sank two runs
    (0.9643 and 0.9306) and the submission. Shape does not predict which one flakes, so
    the only lever is how many of them are on the board: keep at most two, and drop any
    that has flaked twice (the house 2-flaky-runs rule, deadstock C8 precedent).
    """
    live = [n for n, t, w in rows if w > 0 and LIVENESS_CRIT_POS_RE.search(t)]
    if len(live) >= 3:
        emit("ERROR", f"[R17] {len(live)} formula-only liveness positives (C{', C'.join(live)}) — each carries an "
                     "independent judge-variance risk and one flake fails the 3/3 rule (kolterman C25 failed 2/3 "
                     "while its two twins passed 3/3, 2026-08-20); consolidate to at most two")


# R114 (2026-09-11, weldon-bridge-plan refinement round 2, Rubric Quality Review [minor]
# redundant_or_double_counted_criteria): "Criteria 24 and 25 both score the transition order
# total: criterion 24 awards +5 for the unit count and criterion 25 awards +5 for the dollar
# total. These are the same underlying requirement (correct transition order sizing)". The two
# +5 strict rows sat on Bridge_Buy!M26 and N26, one TOTAL row of one table, because 469 was
# the only other unique read-through value; the review reads siblings of one total line as one
# requirement scored twice. The strict pair has to sit on two different deliverables' outputs
# (rubric-coverage-and-completeness: "pick the two strict anchors from two different
# requirements' outputs on working sheets"). Landing-based: the figure each strict row pins is
# located in the golden; two strict rows whose figures share a sheet and a row are siblings of
# one total line (adjacent rows were tried and matched a stray small integer).
_R114_FIG_RE = re.compile(r"(?:exactly|at)\s+\$?(\d[\d,]*(?:\.\d+)?)", re.I)


def _r114_figure(text):
    m = _R114_FIG_RE.search(text)
    if not m:
        nums = re.findall(r"\$?(\d[\d,]*\.\d+|\d[\d,]{3,})", text)
        if not nums:
            return None
        m = nums[-1]
        return float(m.replace(",", ""))
    return float(m.group(1).replace(",", ""))


@check(codes=['R114'], rules=['RUBQ-WEIGHT'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_strict_pair_one_total_row(rows, folder):
    """The strict liveness rows pin figures from different deliverables' outputs; two strict rows whose figures sit on one total row of one sheet score one requirement twice (redundant_or_double_counted to the Rubric Quality Review).

    Since: 2026-09-11
    Source: weldon-bridge-plan refinement round 2 (C24 469 units and C25 $31,918.95, Bridge_Buy
    M26 and N26, [minor] redundant_or_double_counted_criteria).
    Drift-notes: landing-based, same sheet and the SAME row only (an adjacent-row form matched a
    reset count of 61 sitting one row above the order total, weldon fixed rubric); a figure found
    nowhere is R26/R60's business, not this check's."""
    strict = [(n, t, _r114_figure(t)) for n, t, w in rows if w >= 4 and LIVENESS_STRICT_RE.search(t)]
    strict = [(n, t, f) for n, t, f in strict if f is not None]
    if len(strict) < 2:
        return
    d = folder / "solution"
    paths = sorted(d.glob("*.xlsx")) if d.is_dir() else []
    if not paths:
        return
    where = {}
    for path in paths:
        try:
            wb = workbook(path, data_only=True)
        except Exception:
            return
        for ws in wb.worksheets:
            for row in ws.iter_rows():
                for c in row:
                    v = c.value
                    if isinstance(v, bool) or not isinstance(v, (int, float)):
                        continue
                    for n, t, f in strict:
                        if abs(float(v) - f) < 0.005:
                            where.setdefault(n, set()).add((ws.title, c.row, c.column))
    for i in range(len(strict)):
        for j in range(i + 1, len(strict)):
            a, b = strict[i][0], strict[j][0]
            hits = [(sa, ra, ca, rb, cb) for (sa, ra, ca) in where.get(a, ()) for (sb, rb, cb) in where.get(b, ())
                    if sa == sb and ra == rb and ca != cb]
            if hits:
                sa, ra, ca, rb, cb = sorted(hits)[0]
                emit("ERROR", f"C{a} [R114] and C{b} are both strict liveness rows anchored on one total line "
                              f"('{sa}' row {ra} col {ca} and row {rb} col {cb}) - the Rubric Quality Review read "
                              "weldon-bridge-plan's 469 units and $31,918.95 (Bridge_Buy M26/N26) as one "
                              "requirement scored twice (redundant_or_double_counted, 2026-09-11). Move one "
                              "strict row onto another deliverable's own output (a reset count cell, a "
                              "transfer value), never a sibling of the same total")


_FN_RANGE_LIVENESS_RE = re.compile(
    r"\b(?:store|stores|storing|computes?[^.]{0,40}with)\b[^.]{0,60}\b"
    r"(?:SUMIFS?|COUNTIFS?|SUMPRODUCT|[VX]LOOKUP|INDEX|MATCH)\b", re.I)


_R39_SWEEP_RE = re.compile(r"\bthe\s+([a-z][a-z ]{0,30}?)\s+(?:tab|sheet)'s\s+"
                           r"(?:figures|cells|rows|numbers)\b", re.I)


def _r38_liveness_backing(rows, folder):
    """A strict liveness criterion naming a sheet lands on a shape the sheet holds: a sole-call head function it names, or a reference-chain cell.

    Since: 2026-08-24 (branch-stocking-reset run 2, C5).
    Source: the oracle.
    Drift-notes: numbered R37 in the monolith until 2026-09-04.
    """
    sol = folder / "solution"
    if not sol.is_dir():
        return
    sole, chain = {}, {}
    for path in sorted(sol.glob("*.xlsx")):
        try:
            wb = workbook(path)
        except Exception:
            continue
        for ws in wb.worksheets:
            heads, has_chain = set(), False
            for row in ws.iter_rows():
                for c in row:
                    f = c.value
                    if not isinstance(f, str) or not f.startswith("="):
                        continue
                    calls = _R38_CALL_RE.findall(f)
                    if len(calls) == 1:
                        heads.add(calls[0].upper())
                    if not calls and _R38_CHAIN_RE.match(f):
                        has_chain = True
            sole[ws.title.lower()] = heads
            chain[ws.title.lower()] = has_chain
        wb.close()
    if not sole:
        return
    for num, text, weight in rows:
        if weight <= 0 or not LIVENESS_STRICT_RE.search(text):
            continue
        named = [t for t in sole if t and t in text.lower()]
        if not named:
            continue
        named_heads = {h for h in _R38_HEADS if re.search(rf"\b{h}\b", text)}
        # A head function the criterion names must really be a sole call on that sheet;
        # a stray reference-chain cell elsewhere on the sheet must not rescue it.
        if named_heads:
            if any(named_heads & sole[t] for t in named):
                continue
        elif re.search(r"cell references?|reference chain", text, re.I):
            if any(chain[t] for t in named):
                continue
        opts = sorted({h for t in named for h in sole[t]}) or ["none"]
        emit("ERROR", f"C{num} [R38] keys liveness on {', '.join(named)}, but nothing it names "
                     "lands on that sheet: no head function it cites is the sole call in any of "
                     "the sheet's formulas, and no reference-chain cell backs a bare \"cell "
                     "references\" claim, so the judge opens compound wrappers and "
                     "reads them as typed (branch-stocking-reset run 2: C5 flaked 1/3 over "
                     "=IF(K5=\"N\",\"-\",ROUNDUP(Q5+R5,0))). Sole calls available there: "
                     f"{', '.join(opts)}")


@check(codes=['R39', 'R38'], rules=['GOLD-LIVE'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_tab_sweep_liveness(rows, folder):
    """A strict liveness criterion naming a sheet lands on a shape the sheet holds, and never sweeps a whole tab that carries typed constants.

    Codes:
      R39  a whole-tab liveness sweep never names a tab holding typed numeric constants
      R38  a liveness criterion naming a sheet lands on a sole-call head function it names, or a reference-chain cell, that the sheet holds
    Since: R39 2026-08-24 (vendor-terms-program); R38 2026-08-24 (branch-stocking-reset run 2).
    Source: the oracle.
    Drift-notes: R38 was a carve-out twin (numbered R37 in the monolith), merged back 2026-09-11.
    """
    _r38_liveness_backing(rows, folder)     # [R38] the carve-out twin, merged back 2026-09-11
    sol = folder / "solution"
    if not sol.is_dir():
        return
    consts = {}
    for path in sorted(sol.glob("*.xlsx")):
        try:
            wb = workbook(path)
        except Exception:
            continue
        for ws in wb.worksheets:
            cells = [f"{c.coordinate} {c.value!r}" for row in ws.iter_rows() for c in row
                     if isinstance(c.value, (int, float)) and not isinstance(c.value, bool)]
            consts[ws.title.lower()] = cells
        wb.close()
    if not consts:
        return
    for num, text, weight in rows:
        if weight <= 0 or not LIVENESS_STRICT_RE.search(text):
            continue
        for m in _R39_SWEEP_RE.finditer(text):
            named = m.group(1).strip().lower()
            hit = next((t for t in consts if t == named or t.endswith(" " + named) or named in t), None)
            if hit and consts[hit]:
                emit("ERROR", f"C{num} [R39] sweeps the whole {hit} tab for liveness, but that tab "
                              f"holds {len(consts[hit])} typed numeric constants the judge quotes "
                              f"back as the violation (e.g. {'; '.join(consts[hit][:3])}) — "
                              "vendor-terms-program run 1 failed its program-tab sweep 1/3 on the "
                              "keyed 60,000 line, 1,456.30 repayment and 16,115 unclaimed figures. "
                              "Name the read-through cells with their cached values instead of "
                              "sweeping the tab")


# R38 (2026-08-24, branch-stocking-reset run 2): R30 lets the bare phrase "cell references"
# stand as a landing, and that is not enough on its own. C3 ("plain cell references into the
# tabs that compute them") has passed every oracle run because the Briefing cells really are
# reference chains, ='Inventory Effect'!F9. C5 used almost the same words over the Settings
# tab, where every decision cell is a compound wrapper such as
# =IF(K5="N","-",ROUNDUP(Q5+R5,0)), and it flaked 1 of 3 with the cached values quoted back
# as evidence. The wording cannot tell those two apart; only the golden can. So a positive
# strict-liveness criterion naming a sheet has to land on something that sheet actually
# holds: a head function that appears as the SOLE call in one of its formulas, or a pure
# reference-chain cell. C5 was rescued by naming ROUND, which is the sole call in
# =ROUND(P5*O5,2) on that sheet.
_R38_HEADS = ("SUM","SUMIFS","SUMIF","COUNTIFS","COUNTIF","COUNTA","COUNT","AVERAGEIFS",
              "AVERAGEIF","AVERAGE","SUMPRODUCT","MAX","MIN","INDEX","MATCH","VLOOKUP",
              "XLOOKUP","ROUND","ROUNDUP","ROUNDDOWN","ABS","IF")


_R38_CALL_RE = re.compile(r"\b([A-Z][A-Z0-9.]*)\s*\(")


_R38_CHAIN_RE = re.compile(r"\A=\s*'?[^!()=]*'?!?\$?[A-Z]{1,3}\$?\d{1,5}\s*\Z")


# R42 (2026-08-24, task 20 oracle run 6): a strict liveness criterion anchored on a value
# whose cell is a COMPOUND formula. The 11 sat in `=A53+A54`, two pure COUNTIFs added
# together, and the judge read the sum as typed and failed a weight 5 criterion 1/3. R7
# knows compound cells read as typed but only fires on a keyed range, and this criterion
# keyed none. Both clause texts carried "the requested date stands", so one COUNTIF over
# the column reaches 11 in a single call and the flake goes away.
_PURE_CALL_RE = re.compile(r"^=\s*[A-Z][A-Z0-9.]*\((?:[^()]|\([^()]*\))*\)\s*$", re.I)


# A read-through is a cell that only forwards another cell. R42 carved out the
# sheet-qualified form ='Commitment'!C5 but not the bare same-sheet form =C5, and a bare
# reference is strictly simpler than the one already allowed - there is no operator for the
# judge to open. open-order-cleanup, 2026-08-24: C4 anchored on 84866.21, which Briefing!B14
# reaches as ='Commitment'!C5 (allowed) and Commitment!E5 reaches as =C5 (flagged compound),
# so the only clean anchors in the workbook were unreachable. Accept both forms.
_READ_THROUGH_RE = re.compile(r"^='?[A-Za-z0-9 _]+'?![$A-Z0-9]+$|^=\$?[A-Z]{1,3}\$?[0-9]{1,5}$")


def _cells_holding(fwb, vwb, value, tol=0.005):
    out = []
    for ws in vwb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                v = c.value
                if isinstance(v, (int, float)) and not isinstance(v, bool) and abs(v - value) <= tol:
                    out.append((ws.title, c.coordinate, fwb[ws.title][c.coordinate].value))
    return out


@check(codes=['R42'], rules=['GOLD-LIVE'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_liveness_anchor_cell(rows, folder):
    """A strict liveness anchor value sits in a cell that is one pure function call or a plain read-through, never a compound formula.

    Since: 2026-08-24 (task 20 run 6, =A53+A54).
    Source: the oracle.
    Drift-notes: bare same-sheet read-throughs accepted 2026-08-24 (open-order-cleanup).
    """
    d = folder / "solution"
    paths = sorted(d.glob("*.xlsx")) if d.is_dir() else []
    if not paths:
        return
    for num, text, weight in rows:
        if weight <= 0 or not LIVENESS_STRICT_RE.search(text):
            continue
        anchors = [float(m) for m in re.findall(r"\bexactly (\d[\d,]*(?:\.\d+)?)\b", text.replace(",", ""))]
        # a shortage is quoted unsigned ("exactly 8,940.5 short") while the cell stores it
        # negative, so scan both signs or the anchor is never checked at all (oskaloosa
        # C33, 2026-08-24: two of three candidate anchors were negative-only).
        anchors = [s * a for a in anchors for s in (1, -1)]
        if not anchors:
            continue
        for path in paths:
            try:
                fwb = workbook(path)
                vwb = workbook(path, data_only=True)
            except Exception:
                continue
            for a in anchors:
                for title, ref, formula in _cells_holding(fwb, vwb, a):
                    if not isinstance(formula, str) or not formula.startswith("="):
                        continue
                    if _PURE_CALL_RE.match(formula):
                        continue
                    if _READ_THROUGH_RE.match(formula):
                        continue                       # a plain read-through is fine
                    emit("ERROR", f"C{num} [R42] anchors liveness on {a:g}, which {title}!{ref} "
                                 f"reaches with the compound formula {formula} — the judge reads a "
                                 "compound cell as typed and fails the criterion (task 20 run 6: "
                                 "`=A53+A54` cost a weight 5 criterion 1/3). Anchor on a cell that "
                                 "is one function call, or rebuild the cell so it is")
                    break


@check(codes=['R45'], rules=['GOLD-LIVE'], needs=['rubric'], params=['rows'])
def check_liveness_anchor_overlap(rows):
    """A liveness criterion never anchors on a money figure another criterion already scores.

    Since: 2026-08-24 (task 20).
    Source: the platform's near identical criteria check.
    """
    owner = {}
    for num, text, weight in rows:
        if weight <= 0:
            continue
        for tok in _MONEY_RE.findall(text):
            if not LIVENESS_STRICT_RE.search(text):
                owner.setdefault(tok, num)
    for num, text, weight in rows:
        if weight <= 0 or not LIVENESS_STRICT_RE.search(text):
            continue
        for tok in _MONEY_RE.findall(text):
            if tok in owner:
                emit("ERROR", f"C{num} [R45] anchors liveness on {tok}, which C{owner[tok]} already "
                             "scores — the platform's near-identical check reads the liveness "
                             "criterion as subsuming the other one and FAILs the rubric (task 20, "
                             "2026-08-24, and the same shape in round 1). R9 wants a displayed value "
                             "beside the liveness clause; pick one no other criterion states")
                break


# R46 (2026-08-24, task 20 oracle run 7): a strict liveness criterion whose anchor cell is a
# COUNTIF over a TEXT pattern that many cells match. The count of lines measured against the
# requested date sat in =COUNTIF(P5:P50,"*the requested date stands*") and eleven rows of that
# column carry the phrase, so a judge sent to "the clause column" reads the rows and quotes
# them back (run 7 quoted two of them and failed a weight 5 criterion), never reaching the one
# cell the criterion is about. Two consecutive rounds died on that column under two wordings.
# Anchor liveness where the value has no textual twins: a plain read-through of a figure that
# appears twice, once at its source and once where it is used.
@check(codes=['R46'], rules=['GOLD-LIVE'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_anchor_twins(rows, folder):
    """A liveness anchor is never a COUNTIF over a text pattern that many cells on the sheet match.

    Since: 2026-08-24 (task 20 run 7).
    Source: the oracle.
    """
    d = folder / "solution"
    paths = sorted(d.glob("*.xlsx")) if d.is_dir() else []
    if not paths:
        return
    for num, text, weight in rows:
        if weight <= 0 or not LIVENESS_STRICT_RE.search(text):
            continue
        anchors = [float(m.replace(",", ""))
                   for m in re.findall(r"\b(?:exactly|equals) (\d[\d,]*(?:\.\d+)?)\b", text)]
        anchors = [s * a for a in anchors for s in (1, -1)]   # shortages store negative
        if not anchors:
            continue
        for path in paths:
            try:
                fwb = workbook(path)
                vwb = workbook(path, data_only=True)
            except Exception:
                continue
            for a in anchors:
                for title, ref, formula in _cells_holding(fwb, vwb, a):
                    if not isinstance(formula, str):
                        continue
                    cm = re.match(r'^=COUNTIFS?\((\$?[A-Z]{1,3}\$?\d+):(\$?[A-Z]{1,3}\$?\d+),\s*"([^"]*)"\)$',
                                  formula, re.I)
                    if not cm:
                        continue
                    pat = cm.group(3).strip("*").lower()
                    if not pat or len(pat) < 8:
                        continue
                    hits = sum(1 for row in vwb[title].iter_rows() for c in row
                               if isinstance(c.value, str) and pat in c.value.lower())
                    if hits > 3:
                        emit("ERROR", f"C{num} [R46] anchors liveness on {a:g}, which {title}!{ref} "
                                     f"counts with {formula}; {hits} cells on that sheet carry the "
                                     "phrase it matches, so the judge reads those rows and quotes "
                                     "them back instead of reaching the count (task 20 run 7 lost a "
                                     "weight 5 criterion that way, the second round running on the "
                                     "same column). Anchor on a figure with no textual twins")
                        return


# R39 (2026-08-24, branch-stocking-reset run 5): a positive liveness criterion must not name
# a spreadsheet FUNCTION TOKEN. The judge's evidence for the failing run was literally
# "[no matches for pattern 'COUNTIF' across 8 sheet(s) in branch_stocking_reset.xlsx]" for a
# criterion keyed on =COUNTIFS(Settings!$B$5:$B$58,...). The token is really there, in the
# formula; search_xlsx greps CACHED VALUES, so a function name can never be found that way,
# and whether the criterion passes comes down to whether that run happened to reach for
# xlsx_formula_summary instead. Naming the function is therefore a liability, not the anchor
# R30 takes it for. The shapes that have never flaked on this portfolio name no function at
# all and claim a read-through instead: C3 over the briefing, and C5 once it was rekeyed onto
# the Settings tab's 282 bare ='Demand Basis'!I5 style cells. Key liveness on "plain cell
# references into <tab>" plus a cached value anchor, and leave the function names out.
_R39_FUNCS = ("SUM","SUMIF","SUMIFS","COUNT","COUNTA","COUNTIF","COUNTIFS","AVERAGE",
              "AVERAGEIF","AVERAGEIFS","SUMPRODUCT","ROUND","ROUNDUP","ROUNDDOWN","MAX",
              "MIN","INDEX","MATCH","VLOOKUP","XLOOKUP","IFERROR","ABS")


_NESTED_LIT_RE = re.compile(r"(?<![A-Za-z0-9_.$])(\d{4,}(?:\.\d+)?)(?![0-9])")


@check(codes=['R89'], rules=['GOLD-LIVE'], needs=['solution'], params=['folder'])
def check_nested_literals(folder):
    """No money-sized literal is nested inside a stored golden formula.

    The oracle judge's search_xlsx greps cached values and its formula summary
    surfaces head functions only; a constant buried in ROUND(D5*393900.0,2) is not
    a thing it can land on. Task 26 (vendor-terms-program, 2026-08-23) flaked 1/3
    on its Selzer merchandise-only negative because the Terms Economics row showed
    456,300 of purchases and the 393,900 base lived only inside the formula. Put
    the figure in a cell and reference the cell.
    """
    d = folder / "solution"
    if not d.is_dir():
        return
    for path in sorted(d.glob("*.xlsx")):
        try:
            wb = workbook(path)
        except Exception:
            continue
        hits = []
        for ws in wb.worksheets:
            for row in ws.iter_rows():
                for c in row:
                    v = c.value
                    if not (isinstance(v, str) and v.startswith("=")):
                        continue
                    body = re.sub(r'"[^"]*"', '""', v)                      # criteria strings
                    body = re.sub(r"'[^']*'!|\$?[A-Z]{1,3}\$?\d+", " ", body)  # refs
                    for m in _NESTED_LIT_RE.finditer(body):
                        x = float(m.group(1))
                        if x < 1000 or (1900 <= x <= 2100 and x.is_integer()):
                            continue            # small, or a year
                        before = body[:m.start()].rstrip()[-1:]
                        after = body[m.end():].lstrip()[:1]
                        if before in "*/+-" or after in "*/+-":   # an arithmetic operand, not a threshold
                            hits.append(f"{ws.title}!{c.coordinate} {v[:50]}")
        if hits:
            emit("ERROR", f"[R89] {path.name}: {len(hits)} formulas carry a nested money literal "
                         f"(e.g. {'; '.join(hits[:3])}) — the judge greps cached values and head "
                         "functions only and cannot land on a constant inside a formula "
                         "(vendor-terms-program run 1, Selzer 393,900 base, 1/3). Give the figure "
                         "a cell and reference it")


# R98 (2026-09-05, packaging-consolidation golden_solution_check 2/3, rewards 1.0 / 0.7917 /
# 1.0): two +5 strict liveness rows promised that the first page's landed cost and annual
# saving "reach their value through a cell reference into the branches tab or a sum over the
# spend rows", and the golden reached both through same-sheet arithmetic, =MIN(B9,B13) and
# =B5-B15, over cells that DO read the branches tab. Two judges accepted the chain; the third
# stopped at the arithmetic hop and quoted it back, "calculated within the sheet ... rather
# than through a cell reference into the branches tab", failing both rows in one run. R38
# could not see it: it asks whether SOME sheet the row names holds a reference-chain cell,
# never whether the row's own SUBJECT cell is what the row says it is. The rule: locate the
# cell the row is about by its row label, follow bare same-sheet read-throughs only, and the
# cell reached has to be a pure reference into the named tab or one aggregation call over
# another sheet. Anything else, an arithmetic hop, a MIN/IF wrapper, a typed number, is a
# criterion that is false of the golden on a literal read, and one judge in three reads it
# literally.
_R98_ROW_RE = re.compile(
    r"^The (?P<page>[a-z][a-z ]*?)(?:'s| page's| tab's| sheet's) (?P<subject>.+?) reach(?:es)? "
    r"(?:its|their) values? through (?:a )?(?:plain )?cell references? into the "
    r"(?P<tab>[a-z][a-z' ]*?) (?:tab|sheet|page)\b", re.I)


_R98_XREF_RE = re.compile(r"^=\s*(?:'(?P<q>[^']+)'|(?P<b>[A-Za-z][A-Za-z0-9_ ]*))!\$?[A-Z]{1,3}\$?\d{1,5}\s*$")


_R98_SAME_SHEET_RE = re.compile(r"^=\s*\$?([A-Z]{1,3})\$?(\d{1,5})\s*$")


_R98_AGG_RE = re.compile(
    r"^=\s*(?:ROUND\s*\(\s*)?(?:SUM|SUMIF|SUMIFS|COUNT|COUNTA|COUNTIF|COUNTIFS|SUMPRODUCT"
    r"|AVERAGE|AVERAGEIF|AVERAGEIFS)\s*\((?:[^()]|\([^()]*\))*\)(?:\s*,\s*\d+\s*\))?\s*$", re.I)


_R98_STOP = {"the", "a", "an", "of", "on", "in", "at", "to", "and", "for", "with", "by",
             "as", "its", "their", "all", "every", "against", "after", "before", "under",
             "over", "from", "that", "which"}


def _r98_words(text):
    text = re.sub(r",\s*(?:standing at |showing )?(?:exactly )?\$?\d[\d,]*(?:\.\d+)?,?", " ", text)
    text = re.sub(r"\b(?:standing at|showing) exactly \$?\d[\d,]*(?:\.\d+)?", " ", text)
    return [w for w in re.findall(r"[a-z]+", text.lower()) if w not in _R98_STOP]


_R98_TRACE = []          # (criterion, file, sheet, cell, formula) each row resolved to; for reports


def _r98_sheet_is(name, tab):
    n, t = name.lower().strip(), tab.lower().strip()
    return n == t or n.startswith(t) or t.startswith(n) or n.rstrip("s") == t.rstrip("s")


@check(codes=['R98'], rules=['GOLD-LIVE'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_liveness_subject_cell(rows, folder):
    """The cell a strict liveness row is about has the shape the row claims."""
    sol = folder / "solution"
    paths = sorted(sol.glob("*.xlsx")) if sol.is_dir() else []
    if not paths:
        return
    claims = []
    for num, text, weight in rows:
        if weight <= 0 or not LIVENESS_STRICT_RE.search(text):
            continue
        m = _R98_ROW_RE.match(text.strip())
        if not m:
            continue
        words = _r98_words(m.group("subject"))
        if len(words) < 2:
            continue
        claims.append((num, words, m.group("tab")))
    if not claims:
        return
    for path in paths:
        try:
            fwb = workbook(path)
        except Exception:
            continue
        for num, words, tab in claims:
            if not any(_r98_sheet_is(ws.title, tab) for ws in fwb.worksheets):
                continue
            best = None                       # (coverage, -label length, sheet, row, col, label)
            for ws in fwb.worksheets:
                if _r98_sheet_is(ws.title, tab):
                    continue
                for row in ws.iter_rows(max_row=min(ws.max_row, 300), max_col=min(ws.max_column, 12)):
                    for c in row:
                        if not isinstance(c.value, str) or c.value.startswith("="):
                            continue
                        label = set(re.findall(r"[a-z]+", c.value.lower()))
                        cov = sum(1 for w in words if w in label) / len(words)
                        if cov < 0.99:
                            continue
                        # the figure sits to the right of its label, as a number or a formula;
                        # a text neighbour means the match was a column header, not a label
                        target = next((n for n in ws[c.row][c.column:min(c.column + 4, ws.max_column)]
                                       if n.value not in (None, "")), None)
                        if target is None or not (isinstance(target.value, (int, float))
                                                  or (isinstance(target.value, str)
                                                      and target.value.startswith("="))):
                            continue
                        cand = (cov, -len(c.value), ws.title, target.coordinate, target.value, c.value)
                        if best is None or cand[:2] > best[:2]:
                            best = cand
            if best is None:
                continue
            _, _, title, ref, formula, label = best
            _R98_TRACE.append((num, path.name, title, ref, formula))
            ws = fwb[title]
            hops = 0
            while isinstance(formula, str) and _R98_SAME_SHEET_RE.match(formula) and hops < 8:
                mm = _R98_SAME_SHEET_RE.match(formula)
                ref = f"{mm.group(1)}{mm.group(2)}"
                formula = ws[ref].value
                hops += 1
            ok = False
            if isinstance(formula, str):
                xm = _R98_XREF_RE.match(formula)
                if xm and _r98_sheet_is(xm.group("q") or xm.group("b"), tab):
                    ok = True
                elif _R98_AGG_RE.match(formula) and re.search(r"(?:'[^']+'|[A-Za-z][A-Za-z0-9_ ]*)!", formula) \
                        and not re.search(rf"(?:'{re.escape(title)}'|\b{re.escape(title)})!", formula, re.I):
                    ok = True
            if ok:
                continue
            emit("ERROR", f"C{num} [R98] promises a cell reference into the {tab} tab or an aggregation "
                         f"over another sheet's rows for \"{label[:50]}\", but {path.name} {title}!{ref} "
                         f"holds {formula!r}: a same-sheet hop the judge stops at and quotes back as "
                         "'calculated within the sheet rather than through a cell reference' "
                         "(packaging-consolidation 2026-09-05, both +5 rows failed 1/3 over =MIN(B9,B13) "
                         "and =B5-B15). Anchor the row on a first-page cell that reads =Tab!Cell or one "
                         "aggregation call, or rebuild the cell so it does")


# R106 (2026-09-11, rossville-material-compliance refinement, golden check 1.0 / 1.0 / 0.8913):
# the +5 allowance row anchored on "the allowance standing at exactly $16,189.44" after
# naming "the allowance's running total" and "the allowance used" in the same sentence. Two
# judges read the bare noun as the cap (Allowance!E5, 16,189.44, labelled "Allowance at five
# percent"); the third read it as the allowance used (16,155.4) and failed the row: "the
# allowance used stands at $16,155.40, whereas $16,189.44 represents the maximum 5% allowance
# capacity limit". A bare head noun that the sentence has already qualified twice is the
# judge's choice of referent. The anchor label has to be the cell's own words, which no other
# figure in the sentence shares.
_R106_ANCHOR_RE = re.compile(
    r",\s*(?:the|its|their)\s+(?P<label>[a-z][a-z' -]*?)\s+"
    r"(?:standing|stands|sitting|sits|reading|reads|showing|shows)\s+at\s+exactly\s+", re.I)


@check(codes=['R106'], rules=['GOLD-LIVE'], needs=['rubric'], params=['rows'])
def check_liveness_anchor_label(rows):
    """A strict liveness row's value anchor is labelled in the cell's own words, never a bare noun the same sentence uses for another quantity.

    Since: 2026-09-11 (rossville-material-compliance refinement, oracle run 3 of 3).
    Source: the oracle (golden solution check, 0.8913 on a +5 row two other runs passed).
    Drift-notes: fires only on a one- or two-word anchor label that recurs in its own criterion; a
    label of three words or more is read as the cell's label and left alone.
    """
    for num, text, weight in rows:
        if weight <= 0 or not LIVENESS_STRICT_RE.search(text):
            continue
        for m in _R106_ANCHOR_RE.finditer(text):
            label = m.group("label").strip()
            if len(label.split()) > 2:
                continue
            uses = re.findall(r"\b" + re.escape(label) + r"(?:'s)?\b", text, re.I)
            if len(uses) < 2:
                continue
            emit("ERROR", f"C{num} [R106] anchors liveness on \"the {label} standing at exactly\", and the "
                         f"same sentence uses \"{label}\" {len(uses)} times for different quantities; one "
                         "oracle run in three picks the other referent and fails the row on its value "
                         "(rossville-material-compliance 2026-09-11, 0.8913 on a +5 that two runs passed). "
                         "Label the anchor in the words of the cell that holds it")
            break


# R109 (2026-09-11, rossville-material-compliance refinement round 4, golden check 1.0 / 0.9783 /
# 0.9783): a +1 row closed with "the arrival date cell a formula rather than a keyed date". The
# cell, Schedule!V37, holds =IF(AD37="","",TEXT(AD37,"mm/dd/yyyy")); the judge QUOTED that
# formula in its evidence and still wrote "keyed text dates ('10/07/2026') rather than formulas",
# because the value it reads is a text date and a text date is what a keyed date looks like. The
# same run failed the sibling clause "the line's action cell a formula rather than a keyed word"
# on a nested-IF verdict cell it read by value alone. A gated clause survives only on a cell
# whose cached value is a number the judge cannot mistake for typing; the date arm is mechanical
# (the golden renders dates through TEXT()), the word arm is logged, not coded.
_R109_DATE_CLAUSE_RE = re.compile(r"\bformulas?\s+rather\s+than\s+(?:a\s+)?keyed\s+(?:text\s+)?dates?\b", re.I)


@check(codes=['R109'], rules=['GOLD-LIVE'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_gated_clause_on_text_date(rows, folder):
    """A gated liveness clause never claims a date cell is a formula when the golden renders dates as text through TEXT().

    Since: 2026-09-11 (rossville-material-compliance refinement round 4).
    Source: the oracle (golden solution check; the judge quoted the TEXT() formula and called the date keyed).
    Drift-notes: keyed on the clause wording plus any TEXT( formula in a solution workbook; the
    sibling "keyed word" flake on a nested-IF verdict cell is a one-off in the change log.
    """
    claims = [num for num, text, weight in rows if weight > 0 and _R109_DATE_CLAUSE_RE.search(text)]
    if not claims:
        return
    d = folder / "solution"
    text_dates = 0
    for path in sorted(d.glob("*.xlsx")) if d.is_dir() else []:
        try:
            wb = workbook(path)
        except Exception:
            continue
        for ws in wb.worksheets:
            for row in ws.iter_rows():
                for c in row:
                    if isinstance(c.value, str) and c.value.startswith("=") and "TEXT(" in c.value.upper():
                        text_dates += 1
    if not text_dates:
        return
    for num in claims:
        emit("ERROR", f"C{num} [R109] claims a date cell is a formula rather than a keyed date, and the golden "
                     f"renders its dates through TEXT() in {text_dates} cells: the judge reads the text date "
                     "as keyed even while quoting the formula (rossville-material-compliance 2026-09-11, "
                     "0.9783 in two runs of three). Drop the clause and let the date stand as a value, or "
                     "gate a numeric cell instead")


# R117 (2026-09-11, packaging-consolidation Rubric Quality Review [major] redundant_or_double_counted):
# the two +5 strict rows both read first-page figures (Summary!B5 and Summary!B23) and the review
# scored them as one traceability requirement graded twice. weldon-bridge-plan drew the same
# finding on two strict rows over one order's count and total, and R114 codes only that landing
# (one total row of one sheet). The pair has to sit on two different deliverables' outputs, and
# the sheet a subject cell resolves to is the mechanical proxy for the deliverable.
@check(codes=['R117'], rules=['GOLD-LIVE'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_strict_pair_sheets(rows, folder):
    """Two strict liveness rows resolve to cells on two different sheets, one deliverable's output each.

    Since: 2026-09-11 (packaging-consolidation Rubric Quality Review, redundant_or_double_counted [major]).
    Source: the review reads two first-page read-through rows as one traceability requirement scored twice; R114 covers only the one-total-row landing.
    """
    _R98_TRACE.clear()
    saved = list(FINDINGS)
    check_liveness_subject_cell(rows, folder)
    del FINDINGS[len(saved):]                     # R98 reports its own findings in its own run
    by_sheet = {}
    for num, fname, title, ref, _ in _R98_TRACE:
        by_sheet.setdefault((fname, title), []).append(f"C{num} ({ref})")
    for (fname, title), cells in by_sheet.items():
        if len(cells) >= 2:
            emit("ERROR", f"[R117] {', '.join(cells)} are strict liveness rows whose subject cells all sit "
                          f"on {fname} '{title}': the Rubric Quality Review scores two read-through rows "
                          "on one page as the same traceability requirement graded twice "
                          "(packaging-consolidation 2026-09-11, [major]). Anchor the second row on "
                          "another deliverable's own output, a by-vendor table cell or a register "
                          "total on its own tab")


# R118 (2026-09-11, same review, [major] redundant_or_double_counted): C5 "the standard quantity ...
# is a formula multiplying ..." and C8 "the tier price ... is a formula over ..." carried no value
# claim, only a mechanism, and the review read them as one property (live formulas) scored twice.
# The gated tier is meant to ride on VALUE rows ("... is $X, the cell a formula rather than a keyed
# figure"); a formula-only gated row is the mechanism description the judge cannot verify by value
# anyway, so a rubric gets one at most.
_R118_FIGURE_RE = re.compile(r"\d")


@check(codes=['R118'], rules=['GOLD-LIVE'], needs=['rubric'], params=['rows'])
def check_formula_only_gated_rows(rows):
    """At most one positive row is a formula-only gated clause with no figure; further gated clauses ride on value rows.

    Since: 2026-09-11 (packaging-consolidation Rubric Quality Review, redundant_or_double_counted [major]).
    Source: two mechanism-only formula rows read as one live-formula property scored twice.
    """
    from .rubric_form import LIVENESS_GATED_RE
    bare = [n for n, t, w in rows if w > 0 and LIVENESS_GATED_RE.search(t)
            and not LIVENESS_STRICT_RE.search(t) and not _R118_FIGURE_RE.search(t)]
    if len(bare) >= 2:
        emit("ERROR", f"C{', C'.join(bare)} [R118] are formula-only gated rows with no figure: the Rubric "
                      "Quality Review reads a second one as the same live-formula property scored twice "
                      "(packaging-consolidation C5/C8, 2026-09-11, [major]). Keep one, and turn the others "
                      "into value rows (the figure first, the formula clause as its condition) or plain "
                      "rule rows")


# R125 (2026-09-14, twincreek-bid-worksheet refinement round 2, golden check 1.0 / 1.0 / 0.98): a
# +1 row read "The 47 count on the pricing tab's total row is a formula counting the priced lines
# rather than a keyed figure". The cell, 'Bid Pricing'!H60, holds =COUNT(H6:H59) at the foot of a
# column whose 47 other formulas are VLOOKUPs, and the label beside it types "(47 lines priced)".
# One judge in three wrote "contains a hardcoded typed numeric value of 47": xlsx_formula_summary
# reports a column by its dominant head, a lone COUNT under a lookup column is not in that
# picture, and the value search_xlsx greps is the same 47 the label types. vondrak C24 (2026-08,
# a sole =COUNTIF footer) failed 3/3 the same way. A count cell is gradeable when it sits in a
# column of its own kind (a counter column, a labelled summary block); under a data column of
# another head it is the shape to avoid, and the row is re-keyed onto the column the count
# summarises (a column claim naming the count mid-sentence, W16-safe with no leading Each).
_R125_COUNT_WORD_RE = re.compile(r"\bcount(?:s|ed|ing)?\b|\btally\b|\bnumber of\b", re.I)
_R125_INT_RE = re.compile(r"(?<![\d.,$])(\d{1,3}(?:,\d{3})+|\d{2,6})(?![\d.,%])")
_R125_COUNT_HEAD_RE = re.compile(r"\A=\s*(COUNTA?|COUNTIFS?|COUNTBLANK)\s*\(", re.I)
_R125_HEAD_RE = re.compile(r"\A=\s*([A-Z][A-Z0-9.]*)\s*\(", re.I)


@check(codes=['R125'], rules=['GOLD-LIVE'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_lone_count_footer(rows, folder):
    """A gated liveness clause on a count never lands on a lone COUNT cell at the foot of a column whose other formulas share a different head.

    Since: 2026-09-14 (twincreek-bid-worksheet refinement round 2, golden check 1.0 / 1.0 / 0.98 on a +1 row).
    Source: the oracle (xlsx_formula_summary lists a column by its dominant head; a lone COUNT under a lookup column reads as the typed 47 the label beside it carries).
    Drift-notes: fires only when EVERY formula cell carrying the row's integer is such a footer; a count cell in a column of its own kind (its head shared by other formulas there, or no other formulas at all) is left alone, and four-digit years are skipped. vondrak C24 (a sole =COUNTIF footer, 3/3) is the wider shape, logged not coded.
    """
    from .rubric_form import LIVENESS_GATED_RE
    d = folder / "solution"
    paths = sorted(d.glob("*.xlsx")) if d.is_dir() else []
    crits = [(num, text) for num, text, weight in rows
             if weight > 0 and LIVENESS_GATED_RE.search(text)
             and not LIVENESS_STRICT_RE.search(text) and _R125_COUNT_WORD_RE.search(text)]
    if not (paths and crits):
        return
    books = []
    for path in paths:
        try:
            books.append((path.name, workbook(path), workbook(path, data_only=True)))
        except Exception:
            continue
    heads = {}   # (file, sheet, column index) -> {formula head: count}
    for name, fwb, _ in books:
        for ws in fwb.worksheets:
            for row in ws.iter_rows():
                for c in row:
                    if isinstance(c.value, str) and c.value.startswith("="):
                        hm = _R125_HEAD_RE.match(c.value)
                        key = (name, ws.title, c.column)
                        head = hm.group(1).upper() if hm else "="
                        heads.setdefault(key, {})[head] = heads.get(key, {}).get(head, 0) + 1
    for num, text in crits:
        for tok in _R125_INT_RE.findall(text):
            val = float(tok.replace(",", ""))
            if "," not in tok and 1900 <= val <= 2100:
                continue
            carriers = []
            for name, fwb, vwb in books:
                for title, ref, formula in _cells_holding(fwb, vwb, val, tol=0.0):
                    if isinstance(formula, str) and formula.startswith("="):
                        carriers.append((name, fwb, title, ref, formula))
            if not carriers:
                continue
            lone = None
            for name, fwb, title, ref, formula in carriers:
                cm = _R125_COUNT_HEAD_RE.match(formula)
                if not cm:
                    lone = None
                    break
                own = cm.group(1).upper()
                cnt = heads.get((name, title, fwb[title][ref].column), {})
                others = [(h, n) for h, n in cnt.items() if h != own]
                other, other_n = max(others, key=lambda x: x[1]) if others else (None, 0)
                if cnt.get(own, 0) <= 1 and other_n >= 3:
                    lone = (name, title, ref, formula, own, other, other_n)
                else:
                    lone = None
                    break
            if lone is None:
                continue
            name, title, ref, formula, own, other, other_n = lone
            emit("ERROR", f"C{num} [R125] pins the count {tok} on a formula, but every cell carrying it "
                          f"is a lone {own} at the foot of a column of {other_n} {other} formulas "
                          f"({name} {title}!{ref} = {formula}): xlsx_formula_summary lists that column "
                          f"by its dominant head, so one judge in three greps the cached {tok} and calls "
                          "it typed (twincreek-bid-worksheet refinement 2026-09-14, 0.98 on a +1 two runs "
                          "passed; vondrak C24 3/3). Re-key the row on the column the count summarises, "
                          "as a column claim naming the count mid-sentence, or move the counter into a "
                          "column of its own kind")
            break
