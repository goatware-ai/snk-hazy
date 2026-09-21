"""Group 2: every figure a criterion asserts lands on one cell the judge can grep (GOLD-LAND).

Generated 2026-09-04 from autoeval_check.py; every check body is verbatim.
"""
import re
from decimal import Decimal, ROUND_HALF_UP
from ..common import (MONTHS_RE, _COUNT_RE, _FIGURE_RE, _MONEY_RE, _YEAR_RE, _docx_tables, _solution_cell_values,
                      _solution_raw_values, _without_cell_refs, workbook)
from ..core import check, emit, recommend, REPORT, OPTIONS


# R80 (2026-09-02, dfl-freight-audit AutoEval round 1, golden check 0.9792 / 1.0 / 1.0): an
# AGENTLESS COMPARATIVE in a positive criterion. "Invoice DFL7718186 has its fuel surcharge
# rated on the 573.72 net linehaul rather than the base charge, a claim of 292.60" failed 1/3
# on the golden, the judge reading the passive as the carrier's act ("the statement
# incorrectly claims DFL rated it on the net linehaul rather than the base charge") while the
# memo says the reverse: DFL rated on the base and the audit re-rates on the net. When the
# sentence's subject is the audited object (an invoice, a line, a pro, an item) and it carries
# "rather than" / "instead of", nothing in the grammar says WHO did the rating, so the judge
# hangs the comparison on whichever party it reads first, and one of them contradicts the
# golden. Put the agent in the sentence and make the deliverable the subject: "The memo claims
# 292.60 on invoice DFL7718186, where DFL applied the fuel surcharge to the base charge instead
# of the 573.72 net linehaul."
_R80_OBJECT_SUBJECT_RE = re.compile(
    r"^\s*(?:invoice|line|pro|item|row|cell|order|shipment|bill|claim|lot|sku|po|part|account"
    r"|vendor|supplier|customer)\s+\S+\s+(?:has|have|is|are|was|were|rates?|carries|carry|gets?"
    r"|shows?|comes?|takes?)\b", re.I)


_R80_COMPARATIVE_RE = re.compile(r"\brather than\b|\binstead of\b|\bnot (?:on|at|from|off) the\b", re.I)


@check(codes=['R80'], rules=['GOLD-LAND'], needs=['rubric'], params=['rows'])
def check_agentless_comparative(rows):
    """A positive comparative ('rather than', 'instead of') makes the deliverable its subject and names who did what, never the audited object alone.

    Since: 2026-09-02 (dfl-freight-audit C6, 1/3).
    Source: the oracle.
    """
    for num, text, weight in rows:
        if weight < 0:
            continue
        if not _R80_OBJECT_SUBJECT_RE.search(text):
            continue
        cmp = _R80_COMPARATIVE_RE.search(text)
        if not cmp:
            continue
        emit("ERROR", f"C{num} [R80] agentless comparative: the subject is the audited object and the "
                      f"sentence turns on \"{cmp.group(0)}\" with no agent, so the judge can read the "
                      "comparison as either party's act and one reading contradicts the golden "
                      "(dfl-freight-audit C6, 2026-09-02, 1/3: 'has its fuel surcharge rated on the net "
                      "linehaul rather than the base charge' was read as DFL's act). Make the deliverable "
                      "the subject and name who did what: 'The memo claims 292.60 on invoice X, where DFL "
                      "applied the surcharge to the base charge instead of the 573.72 net linehaul'")


_ATOMICITY_CODES = {"R27", "R49", "R54", "R55", "R85", "R105"}


def _atomicity_pending():
    """Criteria with an unresolved atomicity ERROR in this run: the figure-landing checks wait for them.

    A multi-figure row that atomicity already sends back re-reported as R20, R43 and R50 on the same
    figures (2026-09-15 catalog: R27 with R43 on 81 percent of R43's rows); once the row is split, the
    landing checks read the atomic rows. A finding carried as debt does not defer anything.
    """
    from ..core import FINDINGS
    return {str(n) for lvl, c, n, _ in FINDINGS if lvl == "ERROR" and c in _ATOMICITY_CODES and n}


@check(codes=['R20', 'R21'], rules=['GOLD-LAND'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_stated_figures(rows, folder):
    """Every figure a positive criterion states is a cached cell value in the golden, and all of one criterion's figures sit on one sheet.

    Codes:
      R20  every stated figure is a cached cell value somewhere in the golden
      R21  one sheet carries all of a criterion's figures
    Since: 2026-08-20 (wamhoff run 1: C11 for R20, C4 for R21).
    Source: the oracle, which greps cached cell values.
    """
    bags = _solution_cell_values(folder)
    if not bags:
        return
    joined = {t: " | ".join(b) for t, b in bags.items()}
    everything = " | ".join(joined.values())
    pending = _atomicity_pending()
    deferred = sorted((str(n) for n, _, w in rows if w > 0 and str(n) in pending), key=int)
    if deferred:
        print(f"        info: R20, R43 and R50 wait on C{', C'.join(deferred)} until the atomicity finding is fixed")
    for num, text, weight in rows:
        if weight > 0 and str(num) in pending:
            continue
        figs = [f for f in _FIGURE_RE.findall(_without_cell_refs(text))
                if not _YEAR_RE.match(f.replace(",", ""))]
        if not figs:
            continue
        absent = [f for f in figs
                  if f not in everything and f.replace(",", "") not in everything]
        if absent and weight > 0:
            emit("ERROR", f"C{num} [R20] states {', '.join(absent)}, which no solution cell "
                          "carries as a value — the judge greps cached cell values and "
                          "reports the figure as absent even when the prose mentions it "
                          "(wamhoff C11 failed 1/3 on an 8,000 that was only a briefing "
                          "sentence). Put the figure in a cell or restate the criterion on "
                          "figures that are already cells")
            continue
        if absent:
            continue
        if weight > 0 and len(figs) > 1:
            whole = [t for t, b in joined.items()
                     if all(f in b or f.replace(",", "") in b for f in figs)]
            if not whole:
                emit("ERROR", f"C{num} [R21] no single sheet carries all of {', '.join(figs)}, "
                             "so the judge has to assemble the chain across tabs — that is "
                             "the wamhoff C4 flake (failed 1/3 with the judge quoting the "
                             "one tab it landed on). Co-locate the figures on one row or "
                             "restate the criterion on the figures that already share a sheet")


# R50 (2026-08-24, june-price-review oracle run 7): C32 said "a 10.80 credit" while the
# credit cell stores 10.8 - the judge's read_xlsx tools render RAW stored values, never
# the number-format rendering, so it quoted the very row it was grading and still
# verdicted the 10.80 not observed (failed 2/3). R20 never fired because
# _solution_cell_values bags the FORMATTED value ("10.80") beside the raw repr, assuming
# the judge sees display formatting; it does not. A positive-criterion figure whose
# trailing zero exists only in the format is a deterministic grep miss: quote the figure
# as stored (10.8, 67.3). The same sweep caught C20's 67.30 (stored 67.3) on the task.
_PADDED_FIG_RE = re.compile(r"(?<![\d.,])(\d[\d,]*\.\d*0)(?![\d%])")


_R50_KEY_RE = re.compile(r"\b\d{4,}\b|\b[A-Z]{2,}[0-9][\w-]*\b")


_R50_SHEETS = {}


def _other_anchor(body, plain, folder):
    """True if a criterion offers the judge more than the money figure itself.

    A sheet title it can open, or a row key (an order number, an item code) it can grep,
    is what carries the judge to the row whose PROSE spells the padded figure. Without one
    the only route in is the figure, and the judge lands on the bare stored cell instead.
    """
    key = str(folder)
    if key not in _R50_SHEETS:
        titles = set()
        d = folder / "solution"
        for path in sorted(d.glob("*.xlsx")) if d.is_dir() else []:
            try:
                titles |= {w.title.lower() for w in workbook(path).worksheets}
            except Exception:
                pass
        _R50_SHEETS[key] = {t for t in titles if t}
    if any(t in body.lower() for t in _R50_SHEETS[key]):
        return True
    return any(k.replace(",", "") not in plain for k in _R50_KEY_RE.findall(body))


def _r94_stored_form_anchor(rows, folder):
    """A criterion quoting a figure in raw stored form names the sheet or row label holding it when the golden's prose spells the figure padded.

    Since: 2026-08-25 (open-order-cleanup run 8, C14).
    Source: the oracle.
    Drift-notes: R50's mirror; numbered R58 in the monolith until 2026-09-04.
    """
    sheets = _sheets_carrying(folder)
    if not sheets:
        return
    bag = " | ".join(sheets.values())
    for num, text, weight in rows:
        if weight <= 0:
            continue
        body = _without_cell_refs(text)
        for raw in _R58_RAW_RE.findall(body):
            whole, _, cents = raw.partition(".")
            padded = f"{int(whole):,}." + (cents + "0" if len(cents) == 1 else cents)
            if padded == raw or padded not in bag:
                continue
            if _other_anchor(body, raw, folder):
                continue
            emit("ERROR", f"C{num} [R94] quotes {raw} as the cell stores it, but the golden's "
                         f"prose spells it {padded} and this criterion names no sheet and no row "
                         "label - the judge lands on the sentence and cannot match the raw form "
                         "against it (open-order-cleanup run 8: C14 quoted 6407.6 and the judge "
                         "returned the briefing's \"taking $6,407.60 off the book\" as "
                         "unverifiable). Keep the stored form and name the row that holds it, "
                         "which is the anchor R50 asks for in the other direction")


@check(codes=['R50', 'R94'], rules=['GOLD-LAND'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_padded_figures(rows, folder):
    """A criterion quotes a figure as the cell stores it, and names the sheet or row label holding it when the golden's prose spells the figure padded.

    Codes:
      R50  a figure whose trailing zero lives only in the number format is quoted as stored (10.8, not 10.80)
      R94  a raw-form figure the prose spells padded is anchored on the sheet or row label holding the cell
    Since: R50 2026-08-24 (june-price-review run 7); R94 2026-08-25 (open-order-cleanup run 8).
    Source: the oracle, whose tools render raw stored values.
    Drift-notes: R94 was a carve-out twin (numbered R58 in the monolith), merged back 2026-09-11.
    """
    _r94_stored_form_anchor(rows, folder)     # [R94] the carve-out twin, merged back 2026-09-11
    raw = _solution_raw_values(folder)
    if not raw:
        return
    # search_xlsx greps SUBSTRINGS of the raw values, and a golden's own prose routinely
    # spells a figure out comma-formatted ("7,950.00 of margin the branches lost"), which
    # is a hit the exact-cell test misses. Task 20 run 9: eleven of R50's twelve findings
    # on that rubric were echoed in the briefing prose in the padded form and had passed
    # 3/3 for rounds, while the twelfth, C44's 495,000.00, appeared nowhere in any comma
    # form and was the one the judge failed, quoting 'Position'!E23 = '495000' back. Test
    # the whole readable surface, so the rule fires only on a real grep miss.
    blob = "\n".join(raw)
    pending = _atomicity_pending()
    for num, text, weight in rows:
        if weight <= 0 or str(num) in pending:
            continue
        for fig in _PADDED_FIG_RE.findall(_without_cell_refs(text)):
            plain = fig.replace(",", "")
            # The prose carve-out holds only while the criterion hands the judge a SECOND
            # anchor. open-order-cleanup C18 (2026-08-24, oracle run 6) said "The cancelled
            # lines total $18,508.10 at the cost carried on the order", named no sheet and
            # no row key, and the briefing's own "$18,508.10" did not save it: the judge
            # landed on Commitment!C55 = '18508.1' and verdicted unverifiable_from_
            # deliverable, costing the run. Task 20's eleven survivors all carry a row key
            # or a sheet, which is what walks the judge to the prose in the first place.
            if (fig in blob or plain in blob) and _other_anchor(
                    _without_cell_refs(text), plain, folder):
                continue
            stripped = plain.rstrip("0").rstrip(".")
            # a shortage or a credit is quoted unsigned but stored negative, so the
            # padded figure has to be matched against both signs (oskaloosa C21 stated
            # 8,940.50 against a cell storing -8940.5 and R50 walked past it, 2026-08-24)
            if any(s in raw for s in (stripped, stripped + ".0",
                                      "-" + stripped, "-" + stripped + ".0")):
                emit("ERROR", f"C{num} [R50] states {fig}, but the cell stores {stripped} - the "
                              "judge's tools render raw stored values, not number formats, so it "
                              "greps the padded figure, misses, and verdicts not-observed while "
                              "quoting the very row (june-price-review C32 failed 2/3 on a 10.80 "
                              "the cell stores as 10.8). Quote the figure as stored")


# R51 (2026-08-24, june-price-review oracle run 8): C32 bound "a 10.8 credit" to the
# H96284 row, and that row carries 10.8 TWICE (an overbilled column and a credit column,
# =F34 mirroring the other) - the judge quoted the whole row in its evidence on three
# submissions running and still stalled 1/3-2/3, because confirming WHICH 10.8 is the
# credit needs a header-to-column binding it cannot make reliably. A same-row name+figure
# claim is the proven R37 shape only while the figure is unique on its row (KUCERA 647.26
# passed 3/3 three times). When the row twins the figure, no rewording saves it: drop the
# criterion or re-key it on a cell whose value is unique on that row.
_ROW_KEY_RE = re.compile(r"\b[A-Z]{1,3}-?\d{3,6}\b")


@check(codes=['R51'], rules=['GOLD-LAND'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_row_figure_twins(rows, folder):
    """A criterion's figure appears only once on the named row it is bound to."""
    d = folder / "solution"
    books = []
    for path in sorted(d.glob("*.xlsx")) if d.is_dir() else []:
        try:
            books.append((path.name, workbook(path, data_only=True)))
        except Exception:
            continue
    if not books:
        return
    for num, text, weight in rows:
        if weight <= 0:
            continue
        clean = _without_cell_refs(text)
        keys = set(_ROW_KEY_RE.findall(clean))
        figs = {f for f in _FIGURE_RE.findall(clean)
                if not _YEAR_RE.match(f.replace(",", ""))}
        # _FIGURE_RE keeps only decimals and thousands-separated money, so a bare unit
        # quantity was invisible here: oskaloosa C26 bound 550 to PI-125 while the Cover
        # order row carried 550 in THREE columns (POSITION, NEED and QTY), and the judge
        # failed it 1/3 (2026-08-24). Twinning is about the row, not about whether the
        # figure is money. The lookbehind keeps the digits of an item code (PI-125) out.
        # a slash on either side means the digits are part of a date literal (07/28/2027),
        # not a bare quantity: R51 bound 28 out of a criterion's sell-by date to an
        # unrelated row pair and errored twice (chemical-lot-review, 2026-08-24)
        figs |= {m for m in re.findall(r"(?<![\d.,\-A-Za-z/])\d{2,6}(?!/|[\d,]|\.\d)", clean)
                 if not _YEAR_RE.match(m)}
        if not keys or not figs:
            continue
        # rstrip("0") is for a decimal's formatting zero (10.80 -> 10.8). On an INTEGER it
        # eats a significant digit, so 250 also matched every cell holding 25 - harmless
        # while figs were decimals only, a false-positive engine once bare quantities count.
        def _forms(f):
            plain = f.replace(",", "")
            return {plain, plain.rstrip("0").rstrip(".")} if "." in plain else {plain}
        fig_raw = {f: _forms(f) for f in figs}
        for name, wb in books:
            for ws in wb.worksheets:
                for row in ws.iter_rows():
                    vals = [repr(c.value) if isinstance(c.value, float) else str(c.value)
                            for c in row if c.value is not None]
                    if not any(v in keys for v in vals):
                        continue
                    for f, forms in fig_raw.items():
                        hits = sum(1 for v in vals if v in forms)
                        if hits >= 2:
                            emit("ERROR", f"C{num} [R51] binds {f} to the row keyed "
                                 f"{sorted(set(vals) & keys)[0]} ({name}:{ws.title} row "
                                 f"{row[0].row}), and that row carries {f} in {hits} cells - "
                                 "the judge cannot bind the figure to the named column and "
                                 "stalls even while quoting the row (june-price-review C32, "
                                 "three flaky submissions on 10.8 twinned across OVERBILLED "
                                 "and CREDIT). Key the claim on a value unique on its row, "
                                 "or drop it")
                            break
                    else:
                        continue
                    break


# R58 (2026-08-25, june-price-review oracle run 10): C24 tied the K118343 DC300 line to
# "the DWV never keyed cause" while the row's cause cell reads the opaque code pg2 -
# zero shared tokens, so confirming the attribution means mapping the code through the
# Summary cause table, and the judge quoted the row verbatim and still stalled 1/3 (the
# R21 cross-tab hop). The proven sibling C22 never flaked because its phrase "copper L2
# January" finds L2 in the row's own level cell. A cause attribution on a NAMED line is
# in-row verifiable only if some word of the cause phrase appears among that row's own
# cells; otherwise anchor the criterion on figures the row carries and leave the class
# attribution to the cause-table criteria.
_CAUSE_PHRASE_RE = re.compile(r"\b(?:under|to)\s+the\s+((?:\w+[ -]){0,5}?\w+)\s+cause\b", re.I)


@check(codes=['R58'], rules=['GOLD-LAND'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_cause_attribution(rows, folder):
    """A cause a criterion attributes to a named line is confirmable from that line's own row."""
    d = folder / "solution"
    books = []
    for path in sorted(d.glob("*.xlsx")) if d.is_dir() else []:
        try:
            books.append((path.name, workbook(path, data_only=True)))
        except Exception:
            continue
    if not books:
        return
    for num, text, weight in rows:
        if weight <= 0:
            continue
        m = _CAUSE_PHRASE_RE.search(text)
        keys = set(_ROW_KEY_RE.findall(_without_cell_refs(text)))
        if not m or not keys:
            continue
        ptoks = {w.lower() for w in re.findall(r"[A-Za-z]\w+", m.group(1))}
        confirmed = False
        seen_key = False
        for name, wb in books:
            for ws in wb.worksheets:
                for row in ws.iter_rows():
                    vals = [str(c.value) for c in row if c.value is not None]
                    # the judge lands on the row carrying EVERY key the criterion names;
                    # a partial-key row (the item on another list) is not where it grades
                    if not all(any(k == v for v in vals) for k in keys):
                        continue
                    seen_key = True
                    rowtoks = {w.lower() for v in vals for w in re.findall(r"[A-Za-z]\w+", v)}
                    if ptoks & rowtoks:
                        confirmed = True
        if seen_key and not confirmed:
            emit("ERROR", f"C{num} [R58] attributes the {'/'.join(sorted(keys))} line to "
                 f"\"the {m.group(1)} cause\" and no word of that phrase appears on any row "
                 "carrying the key - the row holds only an opaque code, so the judge must "
                 "map it through another sheet and stalls while quoting the very row "
                 "(june-price-review C24, pg2 vs 'DWV never keyed', 1/3). Anchor on figures "
                 "the row carries and leave the class to the cause-table criteria")


# the trailing-hyphen exclusion keeps a document id PREFIX (the 26 of 26-4523) from
# reading as a count, the mirror of the R27 tag-SUFFIX lesson (the 1 of HB-1);
# semrad revision 2026-08-26, R31 false-positive on "the schedule's 26-4523 line"
_CELL_CLAIM_RE = re.compile(
    r"(?:standing|stands|stand|sits|sitting)\s+in\s+a\s+cell|in\s+the\s+cell\s+(?:beside|below|above|next to)|"
    r"\bbeside\b|in\s+a\s+cell\s+(?:beside|below|above|next to)", re.I)


_COUNT_SKIP_BEFORE_RE = re.compile(
    r"(?:article|clause|section|procedure|pu-|po|purchase order|line|no\.?|number|"
    r"quotation|revision|rev)\s*$", re.I)


def _solution_numbers(folder):
    """every number the judge can read off a cell, as floats it can compare."""
    nums, texts = set(), []
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
                    if isinstance(v, bool) or v is None:
                        continue
                    if isinstance(v, (int, float)):
                        nums.add(round(float(v), 6))
                        if 0 < v < 1:                       # a rate stored as a fraction
                            nums.add(round(float(v) * 100, 6))
                    elif isinstance(v, str):
                        texts.append(v)
    # dates and decimals inside prose would answer to almost any two-digit count
    # ("31" matches 01/31/2026), so they come out before the words are searched
    prose = " | ".join(texts)
    prose = re.sub(r"\d+/\d+/\d+", " ", prose)
    prose = re.sub(r"\d[\d,]*\.\d+", " ", prose)
    return nums, prose


_CARRIES_COUNT_RE = re.compile(r"\b(?:carries|runs|lists)\s+\d{2,}\b", re.I)


# R58 (2026-08-25, open-order-cleanup oracle run 8): R50's mirror, and a regression R50
# itself caused. R50 makes a criterion quote money as the cell STORES it, because the judge's
# tools render raw values; C14 and C18 were duly converted from $6,407.60 and $18,508.10 to
# 6407.6 and 18508.1. C14 then came back unverifiable_from_deliverable with the judge quoting
# the briefing's prose, "Six lines are trimmed to the thirteen week ceiling in policy 3.3,
# taking $6,407.60 off the book" - it had landed on the sentence that spells the figure and
# could not match the raw form against it. So the stored form is right and it is not enough
# on its own: where the golden's readable text carries BOTH forms, the criterion has to name
# the sheet or the label of the row holding the raw cell, or the judge is free to land on the
# prose. Same anchor requirement R50 already applies in the other direction, which is why
# _other_anchor is reused rather than re-implemented.
_R58_RAW_RE = re.compile(r"(?<![\d.,$])(\d{3,}\.\d{1,2})(?![\d%])")


@check(codes=['R26', 'R31'], rules=['GOLD-LAND'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_stated_counts(rows, folder):
    """Every count a positive criterion states is held by a golden cell, and a count the criterion promises in a cell is not carried only in prose.

    Codes:
      R26  every stated count is held by a golden cell (or carried in a cell's words)
      R31  a count the criterion says stands in a cell is a numeric cell, not prose
    Since: 2026-08-21 (task 20 run 1, C10 0/3) for R26; june-price-review C2 for R31.
    Source: the oracle.
    """
    nums, prose = _solution_numbers(folder)
    if not nums:
        return
    for num, text, weight in rows:
        if weight <= 0:
            continue
        bad, incell = [], []
        text = _without_cell_refs(text)
        for m in _COUNT_RE.finditer(text):
            n = int(m.group(1))
            if n < 2:                                        # "1 to a row" is a shape
                continue
            if _COUNT_SKIP_BEFORE_RE.search(text[:m.start()]):
                continue                                     # a citation, not a count
            if float(n) in nums:
                continue
            if re.search(r"\b%d\b" % n, prose):
                if _CELL_CLAIM_RE.search(text):
                    incell.append(str(n))                    # promised a cell, got prose
                continue                                     # carried in a cell's words
            bad.append(str(n))
        if bad:
            emit("ERROR", f"C{num} [R26] states the count(s) {', '.join(bad)}, which no "
                          "solution cell holds — a count is the first thing the judge "
                          "recomputes off the deliverable, and a stale one fails every "
                          "oracle run (task 20 C10 said 31 late against the workbook's "
                          "own 28 and went 0/3). Recount it against the data, then put "
                          "the count in a cell so the judge reads it instead of tallying")
        if incell:
            emit("ERROR", f"C{num} [R31] promises a cell for the count(s) {', '.join(incell)} "
                          "(\"standing in a cell\" / \"beside\" / \"below\"), but the workbook "
                          "carries that number only inside a sentence — the judge reads the "
                          "cell the criterion points at, finds the other figure missing and "
                          "fails it (june-price-review C2, 1/3, 987 only in briefing prose). "
                          "Put the count in a numeric cell next to the one the criterion names")


# R78 (2026-08-31, radke-price-protection Rubric Quality Review, [major]
# ungrounded_verification): "Criterion 5 requires exactly 8 action items, but task sources
# do not enumerate 8 specific pre-filing actions or provide a bounded list to verify
# against." R26 was satisfied because the golden held the 8 in a cell, but a count of PLAN
# items (actions, steps, asks, recommendations, things to be done) is the solver's own
# authoring choice, not a fact the inputs bound, so no cell can ground it. Portfolio measure
# before coding: one other hit, frankfort C28 "the 8 things to be decided or signed", the
# same class. Score the milestones the sources name instead ("carries all four of the
# recount, the verification, the signature and the filing").
_R78_PLAN_COUNT_RE = re.compile(
    r"\b(?:\d+|all \w+ of the|exactly \w+)\s+(?:things|actions?|action items|steps|asks|"
    r"recommendations|items? (?:to be done|on the list)|open items|to-?dos?)\b", re.I)


# R79 (2026-08-31, radke-price-protection golden solution check, 1/3 on a weight-2 row):
# "The front page carries the 09/08/2026 filing deadline BESIDE the figure to file" - the
# date sits on Briefing row 14, the figure to file (3,415.09) on row 6. The judge that read
# the layout literally failed it and was right to. A golden-adjacency detector was tried
# first and was born dead: the neighbour phrase shares the word "file" with the label that
# really is beside the date ("File form WP-11 by"), so word overlap can never see it. The
# signal that CAN be seen is the shape of the neighbour: an ABSTRACT referent (the figure /
# total / value / amount to ...) that the judge has to resolve to a cell before it can
# check adjacency. A placement claim is safe only when it names the literal label beside
# the pinned value, so the check fires on abstract neighbours and stays silent on labels.
_R79_PLACE_RE = re.compile(
    r"\b(beside|next to|alongside|under|below|above)\s+(?:the\s+|a\s+|its\s+)?"
    r"([a-z][a-z ,'-]{3,40}?)(?=[,.;]|\s+(?:on|in|at|so|and|which)\b|$)", re.I)


_R79_ABSTRACT_RE = re.compile(
    r"\b(?:figure|figures|total|totals|value|amount|number|sum|result|answer)\b", re.I)


_R79_LIT_RE = re.compile(r"\d{2}/\d{2}/\d{4}|\d[\d,]*\.\d{2}\b|\b\d{1,3}(?:,\d{3})+\b")


@check(codes=['R79'], rules=['GOLD-LAND'], needs=['rubric'], params=['rows', 'folder'])
def check_placement_claims(rows, folder=None):
    """A placement claim ('beside', 'below') names the literal label next to the pinned value, never an abstract referent.

    Since: 2026-08-31 (radke-price-protection C24, 1/3).
    Source: the oracle.
    """
    for num, text, weight in rows:
        if weight <= 0:
            continue
        pm = _R79_PLACE_RE.search(text)
        if not (pm and _R79_LIT_RE.search(text)):
            continue
        if _R79_ABSTRACT_RE.search(pm.group(2)) and not re.search(r"\bcell\b", pm.group(2), re.I):
            emit("ERROR", f"C{num} [R79] places a pinned literal \"{pm.group(0)}\" - the neighbour is "
                          "an abstract referent the judge must resolve to a cell before it can "
                          "check adjacency, and in the golden it need not be adjacent at all "
                          "(radke C24: the 09/08/2026 deadline sat eight rows from 'the figure "
                          "to file', 1/3, 2026-08-31). Name the label literally beside the value, "
                          "or drop the placement clause")


@check(codes=['R78'], rules=['GOLD-LAND'], needs=['rubric'], params=['rows'])
def check_plan_counts(rows):
    """A criterion never pins a count of solver-authored plan items (actions, steps, recommendations).

    Since: 2026-08-31 (radke-price-protection).
    Source: the Rubric Quality Review, ungrounded_verification [major].
    """
    for num, text, weight in rows:
        if weight <= 0:
            continue
        m = _R78_PLAN_COUNT_RE.search(text)
        if m:
            emit("ERROR", f"C{num} [R78] pins a count of solver-authored plan items (\"{m.group(0)}\") "
                          "- the Rubric Quality Review calls that ungrounded_verification [major] "
                          "because no input bounds how many actions a plan lists (radke "
                          "2026-08-31: 'sources do not enumerate 8 specific pre-filing actions'). "
                          "Name the milestones the sources require and score their presence")


# R35 (2026-08-23, branch-stocking-reset run 1): a positive criterion that asserts an
# attribute of ONE row, names that row by a key the golden repeats on several sheets, and
# names neither the sheet nor a figure, lets the judge land on the wrong tab. C11 "The
# CPVC ball valve on the Wausau base is held back from the class its dollars give it, its
# demand having fallen in five of the twelve months" failed 1 of 3 oracle runs with the
# judge quoting Demand Basis, a tab that carries no class column at all; the holdback it
# had to see (CLASS $ = B against CLASS = C) sits on Settings, and CPV-1150 WAUSAU appears
# on both. The two passing runs found Settings unaided. Spelled-out quantities ("five",
# "twelve") are not greppable in a workbook and do not rescue the criterion. The fix is to
# pin a figure in digits and name the sheet, which is why the check clears as soon as
# either is present. Deliberately narrow: a criterion stating a METHOD or a RULE asserts
# no single-row attribute and must not fire, so an ambiguous key is required.
_R35_KEY_RE = re.compile(r"\b[A-Z][a-z]{3,}\b")


_R35_SKIP = {"January","February","March","April","June","July","August","September",
             "October","November","December","Monday","Tuesday","Wednesday","Thursday",
             "Friday","Saturday","Sunday","The","This","That","Every","Where","Each"}


def _sheet_index(folder):
    """token -> set of sheet names carrying it as a cell value, over the golden workbooks."""
    idx = {}
    sol = folder / "solution"
    if not sol.is_dir():
        return idx, set()
    for path in sorted(sol.glob("*.xlsx")):
        try:
            wb = workbook(path, data_only=True)
        except Exception:
            continue
        for ws in wb.worksheets:
            for row in ws.iter_rows(values_only=True):
                for v in row:
                    # Only ALL-CAPS cell values are row keys in these workbooks
                    # (branch, supplier, item labels). Prose cells are not keys.
                    if not isinstance(v, str) or not v.isupper():
                        continue
                    for tok in _R35_KEY_RE.findall(v.title()):
                        idx.setdefault(tok.upper(), set()).add(ws.title)
        wb.close()
    names = set()
    for path in sorted(sol.glob("*.xlsx")):
        try:
            wb = workbook(path)
            names |= set(wb.sheetnames)
            wb.close()
        except Exception:
            pass
    return idx, names


@check(codes=['R35'], rules=['GOLD-LAND'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_landable_literals(rows, folder):
    """A one-row attribute claim is keyed on a token that only one sheet carries."""
    idx, sheets = _sheet_index(folder)
    if not idx:
        return
    for num, text, weight in rows:
        if weight <= 0:
            continue
        if re.search(r"\d", _without_cell_refs(text)):
            continue
        if any(sh.lower() in text.lower() for sh in sheets):
            continue
        # A sentence-initial capital is ordinary prose, not a row key.
        amb = sorted({m.group(0) for m in _R35_KEY_RE.finditer(text)
                      if m.start() > 0 and not text[:m.start()].rstrip().endswith(".")
                      and m.group(0) not in _R35_SKIP
                      and len(idx.get(m.group(0).upper(), ())) > 1})
        if not amb:
            continue
        emit("ERROR", f"C{num} [R35] keys a one-row claim on {', '.join(amb)}, which the golden "
                     "carries on more than one sheet, and names no sheet and no figure in "
                     "digits, so the judge lands on whichever tab it reaches first "
                     "(branch-stocking-reset run 1: the class-holdback claim failed 1/3 with "
                     "the judge quoting a tab that has no class column). Pin a figure in "
                     "digits or name the sheet")


# R31 (2026-08-23, task 20 adjudication): a criterion that states the BASIS of a pinned
# figure has to reproduce it by that basis. C38 pinned 1,097.90 as "two percent of the
# purchases that leave Rademacher"; two percent of 54,894.70 is 1,097.894, so a solver
# computing it directly lands on 1,097.89 and is marked wrong. The golden reaches 1,097.90
# by subtracting two separately rounded rebate amounts, which is the right business answer
# and a different arithmetic path. State the path the deliverable actually takes.
_RATE_WORDS = {
    "one": 1.0, "two": 2.0, "three": 3.0, "four": 4.0, "five": 5.0, "ten": 10.0,
    "fifteen": 15.0, "twenty": 20.0, "twenty five": 25.0, "fifty": 50.0,
    "one half": 0.5, "one and one half": 1.5, "one and a half": 1.5,
    "two and one half": 2.5, "two and a half": 2.5, "three and one half": 3.5,
}


_RATE_RE = re.compile(
    r"(\d+(?:\.\d+)?|one and one half|one and a half|two and one half|two and a half|"
    r"three and one half|twenty five|one half|one|two|three|four|five|ten|fifteen|twenty|fifty)"
    r"\s+percent\b", re.I)


@check(codes=['R64', 'R87'], rules=['GOLD-LAND'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_stated_basis(rows, folder):
    # R64 (2026-08-26, pavelka AutoEval): the Agentic Rubric Quality Review RE-DERIVES a
    # "percent of <base>" total from the raw inputs, and when the base's components span
    # two input files it can assemble the wrong subset - it netted one of the three Q2
    # credit memos (the one whose RGA row was authorized in the quarter; the second was
    # authorized a quarter earlier and the third lives on the AP register, not the RGA
    # log) and reported the CORRECT 812.96 as a [major] arithmetic error demanding
    # 828.30. A rate criterion that carries no inline base figure leaves the checker
    # free to re-derive; stating the base pins its path (and R43 then forces the pair
    # onto the sheet the judge lands on). Probed 2026-08-26: fires on pre-fix C13/C14,
    # zero hits on every criterion in the catalog that has passed the review.
    """A percent-of-base criterion states its base inline, and the pinned figure reproduces from that base at the stated rate.

    Codes:
      R64  a total pinned as a percent of a base states the base figure inline
      R87  a figure pinned as N percent of something reproduces from a golden value at that rate to the cent
    Since: 2026-08-23 (task 20 adjudication) for R87; 2026-08-26 (pavelka) for R64.
    Source: adjudication and the Agentic Rubric Quality Review.
    Drift-notes: R87 was emitted as R31 by this check until 2026-09-04.
    """
    for num, text, weight in rows:
        if weight <= 0:
            continue
        if not re.search(r"percent\s+of\s+(?:the\s+)?[a-z]", text, re.I):
            continue
        if re.search(r"percent\s+of\s+(?:the\s+)?\d", text, re.I):
            continue
        figs = re.findall(r"(?<![\w-])\d[\d,]*\.?\d*", text)
        if len(figs) < 2:
            emit("ERROR", f"C{num} [R64] pins a total as a percent of an UNSTATED base - the "
                          "Agentic Rubric Quality Review re-derives the base from the raw "
                          "inputs and can assemble the wrong component subset (pavelka "
                          "2026-08-26: netted one of three Q2 credit memos and called the "
                          "correct 812.96 a [major] arithmetic error). State the base figure "
                          "inline, co-located with the pinned total per R43")

    nums, _ = _solution_numbers(folder)
    if not nums:
        return
    bases = sorted(nums)
    for num, text, weight in rows:
        if weight <= 0:
            continue
        rm = _RATE_RE.search(text)
        if not rm:
            continue
        token = rm.group(1).lower()
        rate = _RATE_WORDS.get(token)
        if rate is None:
            try:
                rate = float(token)
            except ValueError:
                continue
        for tok in _MONEY_RE.findall(text):
            pinned = float(tok.replace(",", ""))
            exact = any(abs(b * rate / 100.0 - pinned) <= 0.005 for b in bases)
            if exact:
                continue
            near = [b for b in bases if 0.005 < abs(b * rate / 100.0 - pinned) <= 0.05]
            if near:
                emit("ERROR", f"C{num} [R87] pins {tok} as {token} percent of something, but that rate "
                             f"over {near[0]:,.2f} gives {near[0] * rate / 100.0:,.4f} — the stated "
                             "basis and the deliverable's own rounding path differ by a cent, and a "
                             "solver computing the basis directly is marked wrong (task 20 "
                             "adjudication, 2026-08-23: 1,097.90 against a direct 1,097.89). State "
                             "the path the workbook takes, or accept both cents")
                break


# R32 (2026-08-23, task 20 adjudication): an exact count of the FIGURES on a summary page is
# a presentation choice the prompt never fixes, so pinning it fails a solver who puts eleven
# or thirteen useful figures up front. A count of data ROWS meeting a condition is different:
# that one falls out of the inputs and is fair to pin.
_SUMMARY_COUNT_RE = re.compile(
    r"\bexactly (\d+) (?:of them|figures?|cells?|references?|numbers?)\b"
    # R32 widened 2026-08-26 (delivery-zone-reset gate-2 reviewer): "8 actions in all
    # beside a cell counting them" was called overfitting the golden - the prompt asked
    # for a name and a date on everything that has to happen, never for eight things.
    # The count of an author-composed LIST (actions, steps, recommendations, notes) is
    # a presentation count wherever it sits; data-row counts (792 tickets, 128 runs)
    # stay fair because the inputs fix them.
    r"|\b(\d+) (?:actions?|steps?|recommendations?|notes?|bullets?|items?) in all\b"
    r"|\bexactly (\d+) (?:actions?|steps?|recommendations?|notes?|bullets?)\b", re.I)


_SUMMARY_CTX_RE = re.compile(r"\bsummary\b|\bfront (?:page|tab)\b|\bopening\b|\bfirst tab\b"
                             r"|\baction list\b|\bto be done\b|\bnext steps\b", re.I)


def _r91_carried_counts(rows):
    """A criterion points at the count cell rather than saying the deliverable 'carries N items' with the count standing in a cell.

    Since: june-price-review run 2 (C24, 1/3).
    Source: the oracle.
    Drift-notes: numbered R32 in the monolith until 2026-09-04.
    """
    for num, text, weight in rows:
        if weight > 0 and _CARRIES_COUNT_RE.search(text) and re.search(r"count\s+stand|that count", text, re.I):
            emit("ERROR", f'C{num} [R91] says the deliverable "carries N items" and that the count '
                          "stands in a cell — the judge sometimes recounts the list rather than "
                          "reading the cell and flakes on headers and note rows (june-price-review "
                          "run 2, C24, 1/3 with the count cell quoted as not_observed). Point the "
                          "claim at the count cell: \"closes with its count, N, computed in a cell\"")


@check(codes=['R32', 'R91'], rules=['GOLD-LAND'], needs=['rubric'], params=['rows'])
def check_presentation_counts(rows):
    """A criterion never pins a count of figures or list items on a summary page, and points at a count cell rather than saying the deliverable 'carries N items'.

    Codes:
      R32  no exact count of figures or author-composed list items on a summary page
      R91  a criterion points at the count cell rather than saying 'carries N items' with the count standing in a cell
    Since: R32 2026-08-23 (task 20 adjudication), widened 2026-08-26 (delivery-zone-reset); R91 june-price-review run 2.
    Source: adjudication, the gate-2 reviewer and the oracle.
    Drift-notes: R91 was a carve-out twin (numbered R32 in the monolith), merged back 2026-09-11.
    """
    _r91_carried_counts(rows)     # [R91] the carve-out twin, merged back 2026-09-11
    for num, text, weight in rows:
        if weight <= 0:
            continue
        m = _SUMMARY_COUNT_RE.search(text)
        if m and _SUMMARY_CTX_RE.search(text):
            n_ = next(g for g in m.groups() if g)
            emit("ERROR", f"C{num} [R32] pins exactly {n_} figures on the summary, a "
                         "presentation count the prompt does not fix — a reviewer called this out "
                         "on task 20 (2026-08-23): grade that each NAMED summary figure is formula "
                         "derived and let a solver carry more. A count of data rows meeting a "
                         "condition is fair to pin; a count of cells on a front page is not")


# R65 (2026-08-26, tessendorf AutoEval oracle run): a positive stating a NEW value beside
# the OLD value it replaces ("moves to 17.95 from 12.95") flaked 1/3 - the judge searched
# the row key AS-260, landed on the Items row, which carries the sides and the decision but
# NEITHER price (both live only on the drop-ship pricing row), and verdicted the criterion
# failed at reward 0.9796. The sibling criterion in the identical one-figure template ("The
# hot side stem ST-7712 moves to 23.95 on the web under the floor") passed 3/3 in the same
# runs, so the repair is adopting that template: ONE figure beside the row key, the
# superseded price dropped. Probed 2026-08-26 against every rubric in submissions/: the
# two-price move shape appears nowhere else, so this fires on nothing watched passing.
_R65_TWO_PRICE_RE = re.compile(
    r"\bmoves? to \d[\d,]*\.?\d* from \d[\d,]*\.?\d*|\bfrom \d[\d,]*\.\d+ to \d[\d,]*\.\d+")


@check(codes=['R65'], rules=['GOLD-LAND'], needs=['rubric'], params=['rows'])
def check_two_price_moves(rows):
    """A positive states a price move as one figure, never as a new price beside the old one."""
    for num, text, weight in rows:
        if weight <= 0:
            continue
        m = _R65_TWO_PRICE_RE.search(text)
        if m:
            emit("ERROR", f"C{num} [R65] states the move \"{m.group(0)}\" with both the new and the "
                          "superseded value - the judge lands on whichever sheet holds the row key "
                          "and the old price may not be there (tessendorf AS-260 flaked 1/3 at "
                          "0.9796, 2026-08-26, while the one-figure template passed 3/3). State the "
                          "new value alone beside the row key")


# R57 (2026-08-24, chemical-lot-review oracle run 2): the negative on the pan tablet lot
# quoted its printed month "EXP 01/2027", and the judge's search for the fragment 01/2027
# landed on 'Lot Detail'!O23 = '04/01/2027' - a Brekke flux lot seven rows over whose
# full date EMBEDS the month token ("04/[01/2027]") - and fired the negative against the
# wrong row (1/3). A month-form MM/YYYY token is a substring of every stored MM/DD/YYYY
# date whose day-and-year tail spells it, so a negative quoting one leaves the judge to
# pick its landing row by grep order. The fix that passed: name an item or lot code that
# sits on the same row as the exact token (R34's name-the-member, applied to dates).
_MONTH_FRAG_RE = re.compile(r"(?<!\d)(?<!\d/)(?:0[1-9]|1[0-2])/20\d{2}\b")


_MONTH_ROW_ID_RE = re.compile(r"\b[A-Z]{1,3}-?\d{3,6}[A-Z]?\b")


# R43 (2026-08-24, task 20 oracle run 6): R21 asks whether SOME sheet carries all of a
# criterion's figures. The judge does not choose that sheet. C23 pinned 2,032.54 and
# 135,502.60; the scorecard carried both, the claim tab carried only the first, and the
# judge landed on the claim tab and failed it 1/3. Every sheet that carries the pinned
# figure has to carry the rest of them too.
def _sheets_carrying(folder):
    """sheet -> the text a judge reads off it, values and prose together."""
    out = {}
    d = folder / "solution"
    for path in sorted(d.glob("*.xlsx")) if d.is_dir() else []:
        try:
            wb = workbook(path, data_only=True)
        except Exception:
            continue
        for ws in wb.worksheets:
            bag = []
            for row in ws.iter_rows():
                for c in row:
                    v = c.value
                    if v is None:
                        continue
                    if isinstance(v, str):
                        bag.append(v)
                    elif not isinstance(v, bool):
                        bag.append(f"{v:,.2f}")
                        bag.append(f"{v:,.10g}")
                        # ALSO the raw stored forms, with no thousands separator. R50's
                        # whole premise is that the judge's tools render raw stored values,
                        # so a bag carrying only "12,019.23" hides the "12019.23" the judge
                        # actually greps, and R43/R56 then report a co-location failure
                        # against a sheet that really does carry the figure (open-order-
                        # cleanup C21, 2026-08-24: Supplier Calls holds 44016, 04/27/2026,
                        # 09/04 and 12019.23 on one row and R56 could not see the last one).
                        bag.append(f"{v:.10g}")
                        bag.append(str(v))
            out[f"{path.name}:{ws.title}"] = " | ".join(bag)
    return out


@check(codes=['R43'], rules=['GOLD-LAND'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_figure_colocation(rows, folder):
    """Every sheet that carries a criterion's pinned money figure carries the rest of that criterion's figures too.

    Since: 2026-08-24 (task 20 run 6, C23).
    Source: the oracle.
    """
    sheets = _sheets_carrying(folder)
    if not sheets:
        return
    pending = _atomicity_pending()
    for num, text, weight in rows:
        if weight <= 0 or str(num) in pending:
            continue
        figs = [f for f in _MONEY_RE.findall(text)]
        if len(figs) < 2:
            continue
        pinned = figs[0]
        for title, bag in sheets.items():
            has = [f for f in figs if f in bag or f.replace(",", "") in bag]
            if pinned in has and len(has) < len(figs):
                missing = [f for f in figs if f not in has]
                emit("ERROR", f"C{num} [R43] {title} carries {pinned} but not "
                             f"{', '.join(missing)} — the judge lands on the first sheet holding "
                             "the pinned figure and fails the criterion when the rest of the chain "
                             "is on another tab (task 20 run 6: the claim tab had 2,032.54 and the "
                             "scorecard had the 135,502.60 behind it). Put the supporting figure on "
                             "the same row, or state only the figures that sheet already carries")
                break


# R56 (2026-08-24, open-order-cleanup run 5): R43 makes every sheet that carries a pinned
# MONEY figure carry the rest of the chain too, and a criterion pinning a date to an order
# needs the same thing in tokens R43 cannot see. "September 4 is named as the date the answer
# on order 44243 is required" failed 2 of 3 runs. Both halves are in the golden and neither is
# on a sheet with the other: the briefing spells "an answer by September 4" without naming the
# order, the exceptions row carries "44243 line 1" against "answer needed by 09/04", and the
# supplier calls row the judge actually landed on carries 44243 and no date at all, saying only
# "See the exceptions sheet". A judge that greps one anchor and reads that sheet finds the
# other missing and scores the criterion unverified. Date FORM is half of it, so the tokens are
# compared as the criterion writes them: "September 4" and "09/04" are different anchors here
# even though they are the same day, which is R48 for percentages and R50 for money in a third
# unit. The fix is to write both anchors as one row of the golden carries them.
_R56_MONTHS = MONTHS_RE


_R56_DATE_RE = re.compile(
    r"\b(?:" + _R56_MONTHS + r")\s+\d{1,2}(?:st|nd|rd|th)?\b|\b\d{1,2}/\d{1,2}(?:/\d{2,4})?\b",
    re.I)


_R56_KEY_RE = re.compile(r"\b\d{4,}\b|\b[A-Z]{2,}[0-9][\w-]*\b")


def _r93_month_fragment_landing(rows, folder):
    """A negative quoting a month token (MM/YYYY) names an item or lot code on the row carrying the exact token.

    Since: 2026-08-24 (chemical-lot-review run 2).
    Source: the oracle, whose substring search lands on any date embedding the token.
    Drift-notes: numbered R57 in the monolith until 2026-09-04.
    """
    d = folder / "solution"
    sheet_rows = []
    for path in sorted(d.glob("*.xlsx")) if d.is_dir() else []:
        try:
            wb = workbook(path, data_only=True)
        except Exception:
            continue
        for ws in wb.worksheets:
            for row in ws.iter_rows():
                vals = [str(c.value) for c in row if c.value is not None]
                if vals:
                    sheet_rows.append(vals)
    if not sheet_rows:
        return
    for num, text, weight in rows:
        if weight >= 0:
            continue
        for frag in sorted(set(_MONTH_FRAG_RE.findall(text))):
            embed_re = re.compile(r"\d/" + re.escape(frag))
            exact_re = re.compile(r"(?<!\d)(?<!\d/)" + re.escape(frag))
            embedded = sorted({v for vals in sheet_rows for v in vals if embed_re.search(v)})
            if not embedded:
                continue
            ids = set(_MONTH_ROW_ID_RE.findall(text))
            anchored = any(
                any(exact_re.search(v) for v in vals)
                and any(i in v for i in ids for v in vals)
                for vals in sheet_rows)
            if not anchored:
                emit("ERROR", f"C{num} [R93] quotes the month token {frag}, and the golden stores "
                              f"{len(embedded)} full date(s) embedding it ({embedded[0]} ...) - the "
                              "judge's substring search lands on whichever row greps first and fires "
                              "the negative against it (chemical-lot-review run 2: EXP 01/2027 landed "
                              "on a flux lot's 04/01/2027, 1/3). Name an item or lot code sitting on "
                              "the row that carries the exact token")


@check(codes=['R56', 'R93'], rules=['GOLD-LAND'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_date_key_colocation(rows, folder):
    """A criterion pinning a date to a row key names them as one golden row carries them, and a negative quoting a month token names a code on the row carrying the exact token.

    Codes:
      R56  a date pinned to a row key sits beside that key on some golden sheet, in the form the criterion writes it
      R93  a negative quoting a month token (MM/YYYY) names an item or lot code on the row carrying the exact token
    Since: R56 2026-08-24 (open-order-cleanup run 5); R93 2026-08-24 (chemical-lot-review run 2).
    Source: the oracle.
    Drift-notes: R93 was a carve-out twin (numbered R57 in the monolith), merged back 2026-09-11.
    """
    _r93_month_fragment_landing(rows, folder)     # [R93] the carve-out twin, merged back 2026-09-11
    sheets = _sheets_carrying(folder)
    if not sheets:
        return
    for num, text, weight in rows:
        body = _without_cell_refs(text)
        dates = sorted({m.group(0) for m in _R56_DATE_RE.finditer(body)})
        if not dates:
            continue
        keys = sorted({m.group(0) for m in _R56_KEY_RE.finditer(body)
                       if not _R56_DATE_RE.fullmatch(m.group(0))})
        keys = [k for k in keys if not any(k in d for d in dates)]
        if not keys:
            continue
        for title, bag in sheets.items():
            low = bag.lower()
            if all(k.lower() in low for k in keys) and all(d.lower() in low for d in dates):
                break
        else:
            emit("ERROR", f"C{num} [R56] pins {', '.join(dates)} to {', '.join(keys)} and no "
                         "sheet in the golden carries them together — the judge greps one "
                         "anchor, reads that sheet and finds the other missing (open-order-"
                         "cleanup run 5: the 44243 branch answer failed 2/3, the briefing "
                         "spelling September 4 without the order and the supplier call row "
                         "carrying the order without a date). Write both anchors in the form "
                         "one row already carries, as R43 does for money")


# R66 (2026-08-26, kolterman-valve-advisory golden_solution_check): a criterion whose
# SECOND figure is a count, landing on a row of the golden that states that count
# differently. "2,318 affected units were invoiced to customers across 41 accounts" failed
# 2 of 3 runs, and both failing runs quoted the same row back: Briefing row 9 carries the
# 2318 the judge greps for and, beside it, the note "40 accounts and the counter". Both
# lines are right - 41 accounts on the list, 40 of them named and the counter cash account
# the forty-first - but a judge that lands on the pinned figure reads 40 against the
# criterion's 41 and scores it unverified. R43 checks that the sheet carrying the pinned
# figure carries the rest of the chain; it cannot see a sheet that carries a DIFFERENT
# value for it. The repair is on the deliverable, not the wording: make the landing row
# state the criterion's own count (here a live COUNTA on the roster, on the total row that
# holds the pinned figure) and align the prose note beside it.
_R66_COUNT_RE = re.compile(r"\b(\d[\d,]*)\s+(?:[a-z]+\s+){0,2}([a-z]{4,}s)\b")


_R66_NUM_RE = re.compile(r"\b\d[\d,]*(?:\.\d+)?\b")


_R66_YEAR_RE = re.compile(r"(?:19|20)\d{2}")


def _solution_rows(folder):
    """(sheet, row number) -> the text a judge reads off that one row."""
    out = {}
    d = folder / "solution"
    for path in sorted(d.glob("*.xlsx")) if d.is_dir() else []:
        try:
            wb = workbook(path, data_only=True)
        except Exception:
            continue
        for ws in wb.worksheets:
            for row in ws.iter_rows():
                bag = []
                for c in row:
                    v = c.value
                    if v is None:
                        continue
                    if isinstance(v, str):
                        bag.append(v)
                    elif not isinstance(v, bool):
                        bag.append(f"{v:,.10g}")
                        bag.append(f"{v:.10g}")
                if bag:
                    out[(f"{path.name}:{ws.title}", row[0].row)] = " | ".join(bag)
    return out


@check(codes=['R66'], rules=['GOLD-LAND'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_landing_row_counts(rows, folder):
    """The row carrying a criterion's pinned figure states the same count the criterion does."""
    sheets = _solution_rows(folder)
    if not sheets:
        return
    for num, text, weight in rows:
        if weight <= 0:
            continue
        figs = _R66_NUM_RE.findall(text)
        # the pinned figure is the one a judge greps: the first number big enough to
        # land on one row rather than on every row of a table, and never a year, which
        # lands on every dated row in the workbook
        figs = [f for f in figs if len(f.replace(",", "").split(".")[0]) >= 3
                and not _R66_YEAR_RE.fullmatch(f)]
        if not figs:
            continue
        pinned = figs[0]
        pairs = [(n, noun) for n, noun in _R66_COUNT_RE.findall(text)
                 if n.replace(",", "") != pinned.replace(",", "")]
        if not pairs:
            continue
        for (title, rnum), bag in sheets.items():
            if pinned not in bag and pinned.replace(",", "") not in bag:
                continue
            said = _R66_COUNT_RE.findall(bag)
            for want, noun in pairs:
                same = [n for n, nn in said if nn == noun]
                if not same:
                    continue
                if any(n.replace(",", "") == want.replace(",", "") for n in same):
                    continue
                # a row that puts the noun on the PINNED figure ("4,471 units" under a
                # criterion reading "369 of the 4,471 units") is the criterion's own
                # framing, not a contradiction of its count
                if any(n.replace(",", "") == pinned.replace(",", "") for n in same):
                    continue
                emit("ERROR", f"C{num} [R66] {title} row {rnum} carries the pinned {pinned} and "
                              f"states \"{same[0]} {noun}\" against the criterion's {want} - a "
                              "judge that greps the figure lands on this row and reads the count "
                              "back as a contradiction (kolterman C9 failed 2 of 3 oracle runs on "
                              "\"40 accounts and the counter\" beside 2318). Fix the DELIVERABLE: "
                              "put the criterion's own count on the landing row, live off the rows "
                              "it counts, and align any prose note beside it")
                return


# R70 (2026-08-31, po-conformance-review golden_solution_check): a completeness criterion
# that pins a COUNT of rows ("all 72 purchase orders ... one row each") flaked 2 of 3
# oracle runs when the 72 rows were spread over seven attribute schedules, one of which
# grouped its eleven orders into five rows. The judge reads tables one at a time and
# sums across them unreliably, and "one row each" was literally false on the grouped
# table. The lever is the deliverable: give the judge ONE table whose data-row count IS
# the pinned number (a consolidated schedule in an appendix, one row per order), and keep
# every per-attribute schedule one row per order too. This check reads the golden's docx
# tables and fails when no single table carries exactly the pinned count of data rows.
_R70_RE = re.compile(
    r"\ball (\d{1,4}) [^.]*?\b(?:one row (?:each|per|apiece)|its own row|a row each|one to a row"
    r"|one line (?:each|per)|separate rows?)\b", re.I)


@check(codes=['R70'], rules=['GOLD-LAND'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_docx_row_count_landing(rows, folder):
    """A pinned row count equals the data-row count of one golden table."""
    tables = None
    for num, text, weight in rows:
        if weight <= 0:
            continue
        m = _R70_RE.search(text)
        if not m:
            continue
        if tables is None:
            tables = _docx_tables(folder)
        if not tables:
            return
        want = int(m.group(1))
        counts = [len(body) - 1 for _, _, body in tables if len(body) > 1]
        if want in counts:
            continue
        emit("ERROR", f"C{num} [R70] pins all {want} rows, one per item, but no single table in the "
                      f"golden docx has {want} data rows (tables carry {sorted(set(counts))}). The "
                      "judge counts one table at a time and sums across tables unreliably, and a "
                      "grouped table makes 'one row each' literally false: po-conformance-review "
                      "C26 failed 2 of 3 oracle runs with 72 orders over seven schedules "
                      "(2026-08-31). Add one consolidated schedule with exactly that many rows and "
                      "keep every other schedule one row per item")


# R48 (2026-08-24, task 20 oracle run 8): a criterion ASSERTS a figure as a PERCENTAGE
# ("on time delivery ... is 97.1 percent") where the cell holds 0.971 under a percent
# format. search_xlsx greps cached VALUES, so "97.1" is nowhere in the workbook and the
# judge reports "[no matches for pattern '97.1' across 9 sheet(s)]" and fails the
# criterion. The percent format is what the human sees and the decimal is what the tool
# sees, and only the criterion can carry both. The one criterion of the eight that already
# named its stored decimal (C9, "shown as 0.853") has never flaked. Contextual mentions of
# a commitment ("at or above the 92 percent commitment") are left alone: the judge greps
# what the criterion asserts, not what it cites.
_R48_ASSERT_RE = re.compile(r"\b(?:is|are|comes? to|stands? at|reads?|equals?)\s+"
                            r"(\d{1,3}(?:\.\d+)?)\s+percent\b", re.I)


def _workbook_surface(folder):
    """(numeric cached values, text a judge can grep) across the golden workbooks."""
    nums, text = [], []
    d = folder / "solution"
    for path in sorted(d.glob("*.xlsx")) if d.is_dir() else []:
        try:
            vwb = workbook(path, data_only=True)
        except Exception:
            continue
        for ws in vwb.worksheets:
            for row in ws.iter_rows():
                for c in row:
                    v = c.value
                    if isinstance(v, bool):
                        continue
                    if isinstance(v, (int, float)):
                        nums.append(float(v))
                    elif isinstance(v, str):
                        text.append(v)
    return nums, "\n".join(text)


@check(codes=['R48'], rules=['GOLD-LAND'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_percent_anchors(rows, folder):
    """A criterion asserting N percent lands on a cell whose stored value reads N, not N/100."""
    surface = None
    for num, text, weight in rows:
        if weight <= 0:
            continue
        pcts = {float(m) for m in _R48_ASSERT_RE.findall(text)}
        if not pcts:
            continue
        if surface is None:
            surface = _workbook_surface(folder)
        nums, prose = surface
        if not nums:
            return
        for p in sorted(pcts):
            lit = f"{p:g}"
            if any(abs(v - p) <= 0.05 for v in nums) or lit in prose:
                continue                      # the judge can grep the percentage itself
            dec = p / 100.0
            if not any(abs(v - dec) <= 5e-5 for v in nums):
                continue                      # not the stored-decimal shape at all
            declit = f"{dec:g}"
            if declit in text:
                continue                      # the criterion already carries the anchor
            emit("ERROR", f"C{num} [R48] asserts {lit} percent, but no cell holds {lit} and none of "
                         f"the prose carries it - the workbook holds {declit} under a percent format "
                         "and search_xlsx greps cached VALUES, so the judge reports no matches and "
                         "fails the criterion (task 20 run 8: \"[no matches for pattern '97.1' "
                         "across 9 sheet(s)]\" against a scorecard that really does read 97.1%). "
                         f"Name the stored figure in the criterion too, as C9 does with 0.853")


# R63 (2026-08-26, task 20 oracle run 10): a criterion that quotes a FORMULA REFERENCE names
# a sheet the workbook does not have. The submitted C44 asked for "a direct reference like
# =Parameters!<cell>" while the golden's tab is Params and the cell really holds =Params!C15,
# and the judge came back "Position!E23 contains the hardcoded value 495000 instead of a
# formula direct reference like =Params!C15", failing a weight 5 criterion 1/3. Two faults
# compound: search_xlsx greps cached VALUES so the token is unfindable either way (R39), and
# the sheet name in the criterion does not exist, so nothing can satisfy it as written. Check
# the name against the workbook's real sheets; the tab a criterion sends a judge to has to be
# a tab that is there.
_R63_REF_RE = re.compile(r"=\s*'?([A-Za-z][A-Za-z0-9 _]{0,30}?)'?\s*!")


@check(codes=['R63'], rules=['GOLD-LAND'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_named_sheet_exists(rows, folder):
    """A criterion quoting =Sheet! names a sheet the workbook carries."""
    d = folder / "solution"
    paths = sorted(d.glob("*.xlsx")) if d.is_dir() else []
    if not paths:
        return
    sheets = set()
    for path in paths:
        try:
            sheets |= {t.strip().lower() for t in workbook(path).sheetnames}
        except Exception:
            return
    if not sheets:
        return
    for num, text, weight in rows:
        for name in _R63_REF_RE.findall(text):
            if name.strip().lower() in sheets:
                continue
            emit("ERROR", f"C{num} [R63] quotes the formula reference ={name}! but the golden carries "
                         f"no such sheet ({', '.join(sorted(sheets))}) - nothing in the workbook can "
                         "satisfy the criterion as written, and the judge reports the cell as hard "
                         "coded because its value-grep never reaches a formula anyway (task 20 run "
                         "10: \"Position!E23 contains the hardcoded value 495000 instead of a formula "
                         "direct reference like =Params!C15\", weight 5 lost 1/3). Name the tab as the "
                         "workbook spells it, or drop the formula token and anchor on the value")


# R112 (2026-09-11, weldon-bridge-plan refinement round 2, Rubric Quality Review [major]
# misaligned_or_unjustified_rigidity): "Criteria 2, 5, and 13 require specific tab names
# ('Briefing', 'Bridge_Buy', 'ROP_SS_Reset') that appear only in the golden workbook.
# instruction.md requires a front tab briefing and working content but does not specify tab
# names." W12 catches Sheet!A1 references, "the X column" and "under HEADER", but a bare tab
# name in prose ("The Bridge_Buy tab carries ...", "on the ROP_SS_Reset tab", "into the
# Bridge_Buy tab") walked through it. The review's rewrite is functional ("The workbook
# includes a transition order with buy quantities ..."). A name the prompt or an input itself
# mandates (a procedure listing the seven tabs, a standard's five tabs) is not golden-only and
# stays clear; so does a name shorter than four characters, which is too likely to be a word.
_R112_WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9_]{3,}")


@check(codes=['R112'], rules=['RUBQ-SCHEMA'], needs=['rubric', 'solution', 'prompt', 'inputs'],
       params=['rows', 'folder'])
def check_golden_only_tab_name(rows, folder):
    """A criterion names a golden worksheet only when the prompt or an input mandates that name; a bare golden-only tab name in prose is schema imposition the Rubric Quality Review fails as unjustified rigidity.

    Since: 2026-09-11
    Source: weldon-bridge-plan refinement round 2 (three [major] findings on 'Briefing',
    'Bridge_Buy' and 'ROP_SS_Reset' named in C2, C5 and C13; four more rows carried them).
    Drift-notes: sibling of W12 (Sheet!Cell, 'the X column', 'under HEADER'); exempts names
    present in the prompt or any input text, and names under four characters."""
    d = folder / "solution"
    paths = sorted(d.glob("*.xlsx")) if d.is_dir() else []
    if not paths:
        return
    names = set()
    for path in paths:
        try:
            names |= set(workbook(path).sheetnames)
        except Exception:
            return
    names = {n.strip() for n in names if _R112_WORD_RE.fullmatch(n.strip() or "")}
    if not names:
        return
    mandated = (folder.prompt_text or "").lower()
    for _name, text in (folder.input_texts or []):
        mandated += "\n" + (text or "").lower()
    golden_only = {n for n in names if n.lower() not in mandated}
    if not golden_only:
        return
    for num, text, weight in rows:
        for n in sorted(golden_only):
            if re.search(r"(?<![\w!'])" + re.escape(n) + r"(?![\w!])", text):
                emit("ERROR", f"C{num} [R112] names the golden-only tab '{n}' - the Rubric Quality Review "
                              "failed weldon-bridge-plan (2026-09-11) as misaligned_or_unjustified_rigidity "
                              "on exactly this: 'require specific tab names that appear only in the golden "
                              "workbook; the instruction does not specify tab names'. Name what the tab "
                              "IS (the transition order, the reset, the front tab, the open order row) and "
                              "keep the answer key; a tab name is legal only when the prompt or an input "
                              "mandates it")


# R59 (2026-08-25, hollenbach-allocation-plan AutoEval run 4): C30 stated "897 unit
# months" and the judge's own evidence quoted BOTH cells that hold it - 'Buying Ahead'!G32
# (=SUM(C32:F32), the month-end positions added across the four months, on a row labelled
# ALL) and 'Buying Ahead'!C40 (=SUM(C37:C39), the same quantity added across the three
# groups, on a row labelled TOTAL) - and then verdicted unverifiable_from_deliverable.
# Two TOTAL rows on one sheet reaching one number by different arithmetic leave the judge
# no way to decide which cell the criterion means, and naming the sheet cannot help because
# both are on it. R51 guards a row and R46 guards textual twins on a liveness anchor;
# neither sees a total twinned across two blocks of one tab.
#
# Deliberately narrow. A first cut fired on any figure a sheet happened to hold twice and
# lit up eleven of this rubric's own passing criteria - a counter quantity of 26 in a
# 75-row demand table is not something a judge mistakes for the answer. The defect needs
# BOTH holders to be range aggregations sitting on a total row, which is what makes each
# of them look like the figure a criterion is asking for. A cell that simply reads the
# other is the chain R46 endorses, not a twin.
_R59_TOTAL_ROW_RE = re.compile(r"^\s*(TOTAL|ALL|GRAND TOTAL|PERIOD TOTAL)\b", re.I)


_R59_AGG_RE = re.compile(r"^=\s*(SUM|SUMIFS|SUMPRODUCT|COUNTA?|COUNTIFS?)\s*\(", re.I)


@check(codes=['R59'], rules=['GOLD-LAND'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_figure_sheet_twins(rows, folder):
    """A figure a criterion states is totalled once per sheet, never twice by different aggregations on two total rows.

    Since: 2026-08-25 (hollenbach-allocation-plan run 4, C30).
    Source: the oracle, unverifiable_from_deliverable while quoting both cells.
    """
    d = folder / "solution"
    paths = sorted(d.glob("*.xlsx")) if d.is_dir() else []
    if not paths:
        return
    for path in paths:
        try:
            fwb = workbook(path)
            vwb = workbook(path, data_only=True)
        except Exception:
            continue
        index = {}
        for ws in fwb.worksheets:
            vs = vwb[ws.title]
            for row in ws.iter_rows():
                label = ws.cell(row[0].row, 1).value
                if not isinstance(label, str) or not _R59_TOTAL_ROW_RE.match(label):
                    continue
                for c in row:
                    f = c.value
                    if not isinstance(f, str) or not _R59_AGG_RE.match(f):
                        continue
                    v = vs[c.coordinate].value
                    if not isinstance(v, (int, float)) or isinstance(v, bool) or abs(v) < 10:
                        continue
                    index.setdefault(f"{round(float(v), 4):g}", {}).setdefault(
                        ws.title, []).append((c.coordinate, f))
        for num, text, weight in rows:
            if weight <= 0:
                continue
            for fig in sorted(set(re.findall(r"(?<![\w.-])(\d[\d,]*(?:\.\d+)?)(?![\w-])", text))):
                try:
                    key = f"{round(float(fig.replace(',', '')), 4):g}"
                except ValueError:
                    continue
                for sheet, cells in index.get(key, {}).items():
                    if len(cells) < 2:
                        continue
                    refs = {r for r, _ in cells}
                    indep = [(r, f) for r, f in cells
                             if not (refs - {r}) & set(re.findall(r"\$?([A-Z]{1,3}\$?\d{1,5})",
                                                                  f.replace("$", "")))]
                    if len(indep) < 2:
                        continue
                    where = " and ".join(f"{sheet}!{r} {f}" for r, f in indep[:2])
                    emit("ERROR", f"C{num} [R59] states {fig}, which '{sheet}' totals twice by "
                                  f"different arithmetic ({where}) - the judge quotes BOTH total "
                                  "rows and then verdicts unverifiable_from_deliverable, because "
                                  "nothing in the criterion picks one (hollenbach C30, 2026-08-25: "
                                  "897 unit months added once across the months and once across the "
                                  "groups). Naming the sheet cannot fix it when both twins are on "
                                  "that sheet - leave one of the two totals on the tab, or key the "
                                  "criterion on a figure the tab totals once")
                    break


# R62 (2026-08-26, oskaloosa-count-adjustment AutoEval run 6): C4 said the late receipts
# "are added to the book quantity, 3,490.02", and the judge quoted the very row it needed -
# Corrections row 39, TYPE late, EXTENDED 3490.02, with the reference numbers and the keying
# date beside it - and then FAILED the criterion rather than verdicting it unverifiable. It
# had settled the direction against the criterion, and the workbook gave it two ways to do
# that: the row it landed on named no side at all (the tab note even read "signed the way it
# enters the count"), and the only cell that did name a side, Adjustment C27, held the same
# magnitude NEGATIVE, on a row reading "put on book". A sign-flipped twin plus a row that
# does not say the direction in the criterion's own words is a decidable-the-wrong-way claim,
# which is worse than an unfindable one: an unverifiable verdict costs nothing, a failed one
# costs the criterion's weight.
#
# Narrow by construction, and probed before coding. It needs all three of: a direction phrase
# in the criterion, a magnitude the golden holds with BOTH signs, and NO row holding that
# magnitude carrying the direction verb in its own text. On the catalogue as it stands it
# fires zero times, and on the pre-fix oskaloosa workbook it fires once, on C4 alone - not on
# C5 or C6, whose sign twins sit on rows that did say "taken off". That separation is the
# point: the repair is the WORKBOOK saying the direction on the row that holds the figure,
# not a reworded criterion (the house rule that a criterion must use the cell's own words,
# made checkable for the one case where the cell contradicts it).
_R62_DIR_RE = re.compile(r"\b(added to|taken off|taken out of|left out of|put on|counted into|"
                         r"removed from|deducted from|brought into|credited to|charged to)\b", re.I)


_R62_FIG_RE = re.compile(r"(?<![\w.-])(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+\.\d+)(?![\w])")


@check(codes=['R62'], rules=['GOLD-LAND'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_direction_sign_twins(rows, folder):
    """A direction claim is made only on a figure the golden holds with one sign."""
    d = folder / "solution"
    paths = sorted(d.glob("*.xlsx")) if d.is_dir() else []
    if not paths:
        return
    cells, rowtext = [], {}
    for path in paths:
        try:
            wb = workbook(path, data_only=True)
        except Exception:
            continue
        for ws in wb.worksheets:
            for row in ws.iter_rows():
                for c in row:
                    v = c.value
                    if isinstance(v, (int, float)) and not isinstance(v, bool):
                        cells.append((ws.title, c.row, float(v)))
                    elif isinstance(v, str):
                        key = (ws.title, c.row)
                        rowtext[key] = rowtext.get(key, "") + " " + v
    if not cells:
        return
    for num, text, weight in rows:
        if weight <= 0:
            continue
        m = _R62_DIR_RE.search(text)
        if not m:
            continue
        verb = m.group(1).lower()
        head = verb.split()[0]
        for raw in sorted({mm.group(1) for mm in _R62_FIG_RE.finditer(text)}):
            try:
                val = abs(float(raw.replace(",", "")))
            except ValueError:
                continue
            hits = [c for c in cells if abs(abs(c[2]) - val) < 0.005]
            if not hits or len({c[2] > 0 for c in hits}) < 2:
                continue
            if any(head in rowtext.get((s, r), "").lower() for s, r, _ in hits):
                continue
            where = ", ".join(f"{s}!row {r} = {v:g}" for s, r, v in hits[:3])
            emit("ERROR", f"C{num} [R62] says {raw} is \"{verb}\" something, but the golden holds "
                          f"that figure with both signs ({where}) and no row holding it says "
                          f"\"{head}\" in its own words - the judge lands on one of them, settles "
                          "the direction against the criterion and FAILS it rather than calling it "
                          "unverifiable, which costs the weight (oskaloosa C4, 2026-08-26: 3,490.02 "
                          "positive on Corrections with no side named, negative on Adjustment under "
                          "\"put on book\"). Say the direction on the row that holds the figure")
            break


_R103_ENUM_RE = re.compile(r"\b(?:each|every|all)\s+(?:of\s+the\s+)?(\d{1,4}|[a-z]+)\b", re.I)


@check(codes=['R103'], rules=['GOLD-LAND'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_enumeration_on_prose_tab(rows, folder):
    """A positive enumerating five or more items on a prose tab has at least that many short cells there, one per item, for the judge to count.

    R103 (2026-09-10, commission-review-q2 golden check 0/3 at 0.9792): C7 scored the
    Representative Notes tab on naming "each of the 10 new account bonuses", and every one of
    the ten sat at the tail of a 900-character paragraph, one per representative. All three
    judges reported the tab "contains only general commentary" and failed the row: a
    per-item enumeration is never verified inside long prose cells, whether the tool
    truncates the cell or the judge stops reading. When a positive criterion enumerates N
    items (N >= 5) on a tab whose text is prose (three or more cells of 300+ characters), the
    tab has to carry at least N short cells, a row or a cell per item, or the judge has
    nothing to count."""
    from ..common import _G5_WORDS, solution_files
    sheets = {}
    for x in solution_files(folder, {".xlsx"}):
        try:
            wb = workbook(x, data_only=True)
        except Exception:
            continue
        for ws in wb.worksheets:
            long = short = 0
            for row in ws.iter_rows(values_only=True):
                for v in row:
                    if isinstance(v, str):
                        if len(v) >= 300:
                            long += 1
                        elif 0 < len(v.strip()) <= 60:
                            short += 1
            sheets[ws.title] = (long, short, x.name)
        wb.close()
    for num, text, weight in rows:
        if weight <= 0:
            continue
        low = text.lower()
        best = None
        for m in _R103_ENUM_RE.finditer(text):
            tok = m.group(1).lower()
            n = int(tok) if tok.isdigit() else _G5_WORDS.get(tok)
            if n and n >= 5:
                best = max(best or 0, n)
        if not best:
            continue
        for title, (long, short, fname) in sheets.items():
            t = title.lower()
            named = re.search(r"\b" + re.escape(t) + r"\s+tab\b", low) or (
                len(t.split()) >= 2 and re.search(r"\b" + re.escape(t) + r"\b", low))
            if named and long >= 3 and short < best:
                emit("ERROR", f"C{num} [R103] enumerates {best} items on the {title} tab of {fname}, whose text is "
                              f"{long} prose cell(s) of 300+ characters with only {short} short cell(s) to count: "
                              "commission-review-q2's C7 failed all three golden-check runs (2026-09-10) on ten "
                              "bonuses named at the tails of six paragraphs, the judges reading 'only general "
                              "commentary'. Give the items a row each on that tab (a small table under the prose, "
                              "verdicts as formulas off the tab that computes them) or score the enumeration on the "
                              "tab that already tabulates it")
                break


# R108 (2026-09-11, standby-generator-recommendation refinement, golden check 0.9825 x 3): a +1
# row said "Findings are tied to the four provided files, the three Cummins data sheets and
# Diesel_Retail_Price_History.xlsx, each cited where its figures are used", and the memo named
# no input file anywhere; it said "the three sheets" and "the price history". The judge grepped
# the file name at the price sentence, found nothing, and failed the row in every run. A
# criterion that promises a citation by file name is landed only by that file name in the
# deliverable's own text; a paraphrase of the file is a miss the judge cannot forgive.
_R108_FILE_RE = re.compile(r"\b[\w-]+\.(?:xlsx|docx|pdf|csv|pptx|txt|md|json)\b")
_R108_CITE_RE = re.compile(
    r"\b(?:cit(?:e|es|ed|ing|ation)|tied to|ties|attribut\w+|sourced to"
    r"|names? (?:the )?(?:file|source|workbook|sheet)|reference[sd]? (?:the )?file)\b", re.I)


def _r108_golden_text(folder):
    from ..common import _docx_text, _xlsx_all_text
    sol = folder / "solution"
    text = ""
    for p in sorted(sol.glob("*")) if sol.is_dir() else []:
        if p.suffix == ".docx":
            text += "\n" + _docx_text(p)
        elif p.suffix == ".xlsx":
            text += "\n" + "\n".join(t for _, t in _xlsx_all_text(p))
        elif p.suffix in (".md", ".txt", ".csv"):
            text += "\n" + p.read_text(encoding="utf-8", errors="ignore")
    return text


@check(codes=['R108'], rules=['GOLD-LAND'], needs=['rubric', 'inputs', 'solution'], params=['rows', 'folder'])
def check_cited_file_named_in_golden(rows, folder):
    """A positive that promises a citation of an input file by name lands only on that file name in the golden's own text.

    Since: 2026-09-11 (standby-generator-recommendation refinement, 0.9825 in all three runs).
    Source: the oracle (golden solution check).
    Drift-notes: keyed on a citation verb beside the file name; a row that merely names a file as
    the source of a figure (dfl-freight-audit, 16 rows) is not a citation claim and stays quiet.
    """
    d = folder / "inputs"
    inputs = {p.name for p in d.glob("*")} if d.is_dir() else set()
    if not inputs:
        return
    claims = []
    for num, text, weight in rows:
        if weight <= 0 or not _R108_CITE_RE.search(text):
            continue
        named = [n for n in _R108_FILE_RE.findall(text) if n in inputs]
        if named:
            claims.append((num, named))
    if not claims:
        return
    golden = _r108_golden_text(folder)
    for num, named in claims:
        missing = [n for n in named if n not in golden]
        if missing:
            emit("ERROR", f"C{num} [R108] promises the deliverable cites {', '.join(missing)} by name, and no "
                         "solution file carries that name in its text; the judge greps the file name where "
                         "the figure is used and fails the row in every run (standby-generator-recommendation "
                         "2026-09-11, 0.9825 x 3 on \"the three sheets\" and \"the price history\"). Name the "
                         "file in the sentence that uses its figure, or drop the citation claim")


# R120 (2026-09-11, packaging-consolidation golden_solution_check 1/3, rewards 1.0 / 0.9792 / 0.9792):
# "The agreement items' current cost of $21,536.05 is stated on the first page" failed 2 of 3 with
# the judge reporting the figure "on the 'Summary' tab (cell B19) ... but not on the first
# page/tab of the workbook, which is 'Crossref'". The house idiom "first page" means the summary,
# and the workbooks built before September kept it first (Summary, Briefing, Front Page, Q2
# Review); the September batch put the reference tabs first and the summary last. A judge reads
# "first page" as the first worksheet, so the sheet the first-page rows resolve to has to BE the
# first worksheet.
_R120_PAGE_RE = re.compile(r"\b(?:first|front) page\b", re.I)


_R120_SUMMARY_TITLE_RE = re.compile(
    r"summary|briefing|front|cover|overview|review|memo|recommendation|dashboard|page|award|plan\b", re.I)


@check(codes=['R120'], rules=['GOLD-LAND'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_first_page_is_first_sheet(rows, folder):
    """When a positive row says first page or front page, the workbook's first worksheet is that page.

    Since: 2026-09-11 (packaging-consolidation golden_solution_check, 2/3 runs).
    Source: the judge read 'first page' as the first worksheet and found the figure only on the sixth.
    """
    import openpyxl
    from .liveness import _R98_TRACE, check_liveness_subject_cell
    from ..core import FINDINGS
    if not any(w > 0 and _R120_PAGE_RE.search(t) for _, t, w in rows):
        return
    sol = folder / "solution"
    paths = sorted(sol.glob("*.xlsx")) if sol.is_dir() else []
    if not paths:
        return
    _R98_TRACE.clear()
    saved = len(FINDINGS)
    check_liveness_subject_cell(rows, folder)
    del FINDINGS[saved:]
    resolved = {(fname, title) for num, fname, title, _, _ in _R98_TRACE
                if any(str(num) == n and _R120_PAGE_RE.search(t) for n, t, _ in rows)}
    for path in paths:
        try:
            first = openpyxl.load_workbook(path, read_only=True).sheetnames[0]
        except Exception:
            continue
        pages = {title for fname, title in resolved if fname == path.name}
        if pages and first not in pages:
            emit("ERROR", f"[R120] {path.name}: the rubric's first-page rows read the '{', '.join(sorted(pages))}' "
                          f"sheet, but the first worksheet is '{first}'. The judge reads 'first page' as the "
                          "first worksheet and reported the figure absent from it (packaging-consolidation "
                          "2026-09-11, 2/3). Move the summary to the first tab")
        elif not pages and not _R120_SUMMARY_TITLE_RE.search(first):
            emit("ERROR", f"[R120] {path.name}: the rubric says 'first page' and the first worksheet is "
                          f"'{first}', a reference tab. The judge reads 'first page' as the first worksheet "
                          "(packaging-consolidation 2026-09-11, 2/3). Move the summary to the first tab")


# R123 (2026-09-12, standby-generator-recommendation refinement round 4, golden check 1.0 / 0.9825 /
# 1.0): the memo wrote the alternator feature code as "B601 2" where the Cummins sheet writes
# "B601-2". The judge searched the deliverable for the sheet's token, found nothing, fell back on
# a text read of the PDF's alternator table and concluded B601-2 was a 600 V winding. An
# identifier the golden borrows from an input is written in the input's exact form; a space or
# a dash variant in place of the hyphen is a token the judge's grep never lands on.
_R123_CODE_RES = (re.compile(r"\b([A-Z]{1,5}\d{2,5})-(\d{1,4})\b"),      # B601-2, ADS-311, EDS-1087
                  re.compile(r"\b([A-Z]{2,5})-(\d{2,6})\b"))             # CM-2515, PO-44817
_R123_SEP = r"[  ‐‑‒–—―−]"


def _r123_source_text(folder):
    from ..common import input_texts
    from .fidelity import _g26_pdf_text
    src = ""
    pf = folder / "prompt.md"
    if pf.exists():
        src += pf.read_text(encoding="utf-8", errors="ignore") + "\n"
    src += "\n".join(t for _, t in input_texts(folder))
    ind = folder / "inputs"
    for pdf in sorted(ind.glob("*.pdf")) if ind.is_dir() else []:
        src += "\n" + (_g26_pdf_text(pdf) or "")
    return src


@check(codes=['R123'], rules=['GOLD-LAND'], needs=['prompt', 'inputs', 'solution'], params=['folder'])
def check_borrowed_identifier_exact_form(folder):
    """An identifier the golden borrows from an input (a feature code, a document number, a credit memo id) is written in the input's exact hyphenated form, never with a space or a dash variant in place of the hyphen.

    Since: 2026-09-12 (standby-generator-recommendation refinement round 4, 0.9825 in one of three runs).
    Source: the oracle (golden solution check), which grepped the sheet's "B601-2" against the memo's "B601 2".
    Drift-notes: only identifiers some input or the prompt carries in the hyphenated form are checked, and an
    input that itself writes the loose form too is left alone. Shapes: letters+digits-digits and letters-digits.
    """
    src = _r123_source_text(folder)
    if not src.strip():
        return
    tokens = set()
    for rx in _R123_CODE_RES:
        tokens.update(rx.findall(src))
    if not tokens:
        return
    golden = _r108_golden_text(folder)
    hits = []
    for a, b in sorted(tokens):
        loose = re.compile(re.escape(a) + _R123_SEP + re.escape(b) + r"\b")
        m = loose.search(golden)
        if m and not loose.search(src):
            hits.append((m.group(0), f"{a}-{b}"))
    for got, want in hits[:6]:
        emit("ERROR", f"[R123] the golden writes \"{got}\" where an input writes \"{want}\"; the judge greps the "
                      "input's exact token, misses it, and reads the source table by hand instead "
                      "(standby-generator-recommendation 2026-09-12: \"B601 2\" cost a +1 row in one of three "
                      "runs). Write the identifier exactly as the input does")


# R131 (2026-09-14, rempel-buyout-plan refinement round 2, golden check 0.98 on 3 of 3): C25
# graded "the front page states that PM-4 3.3 buys a revise and resubmit line on the basis of
# design and names the two lines it applies to". The Briefing stated it twice, at character 250
# of a 900-character water closet paragraph and at character 420 of the mixing valve paragraph.
# Every judge grepped the cite, landed on the first long cell, read the sentence around the hit
# as the whole claim ("references PM-4 3.3 solely in connection with WC-1") and failed the row.
# A cite a criterion grades has to sit where the judge reads: at the head of a cell or inside a
# short one. R130 is the sibling for a cite the golden never makes at all.
_R131_CITE_RE = re.compile(r"\b(?:[Ss]ection\s+\d+\.\d+[a-z]?|[A-Z]{1,5}-\d{1,3}\s+\d+\.\d+[a-z]?)\b")
_R131_HEAD = 200   # characters from the start of a cell inside which the judge reads a hit as the claim
_R131_LONG = 500   # a cell shorter than this is read whole


_R131_FRONT_RE = re.compile(r"\b(?:front|first|cover|opening)\s+(?:page|tab|sheet|worksheet)\b", re.I)


def _r131_golden_units(folder, front_only=False):
    """Every text unit of the golden as (where, text, front): xlsx string cells and docx paragraphs; front marks the first worksheet of each workbook, the only place a "front page" or "first page" row is read (R120)."""
    import os
    from ..common import solution_files
    units = []
    for p in solution_files(folder, {".docx"}):
        try:
            from docx import Document
            paras = Document(str(p)).paragraphs
        except Exception:
            continue
        for i, para in enumerate(paras, 1):
            if para.text.strip():
                units.append((f"{os.path.basename(str(p))} paragraph {i}", para.text, i == 1))
    for p in solution_files(folder, {".xlsx"}):
        try:
            wb = workbook(p, data_only=True)
        except Exception:
            continue
        for k, ws in enumerate(wb.worksheets):
            for row in ws.iter_rows():
                for c in row:
                    if isinstance(c.value, str) and c.value.strip():
                        units.append((f"{os.path.basename(str(p))} {ws.title}!{c.coordinate}", c.value, k == 0))
    return units


@check(codes=['R131'], rules=['GOLD-LAND'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_section_cite_past_read_head(rows, folder):
    """A positive criterion citing a numbered section ("Section 3.2", "PM-4 3.3") finds that cite in the golden at the head of a cell or inside a short cell; a cite that occurs only past the first 200 characters of 500-character prose cells is read by the judge as the sentence around the hit and the row fails.

    Since: 2026-09-14 (rempel-buyout-plan refinement round 2, golden check 0.98 on 3 of 3 runs).
    Source: C25 graded the front page stating that PM-4 3.3 buys a revise and resubmit line on the basis of design and naming the two lines; the Briefing stated it at character 250 of a 900-character WC-1 paragraph and at character 420 of the MV-1 paragraph, and every judge quoted the WC-1 sentence and reported the rule unstated.
    Drift-notes: cites are "Section N.N" and "<CODE>-<n> N.N" in positive rows, read case-insensitively over every solution xlsx string cell and docx paragraph; a row naming the front, first, cover or opening page, tab or sheet is read on the first worksheet of each workbook only (R120: "first page" is the first worksheet to the judge); a cite the golden never carries is R130's ground and is skipped here; one hit inside the head window, or inside a cell shorter than the long floor, clears the cite.
    """
    units = None
    for num, text, weight in rows:
        if weight <= 0:
            continue
        cites = sorted(set(_R131_CITE_RE.findall(text)))
        if not cites:
            continue
        if units is None:
            units = _r131_golden_units(folder)
            if not units:
                return
        front = bool(_R131_FRONT_RE.search(text))
        for cite in cites:
            rx = re.compile(r"\s+".join(re.escape(w) for w in cite.split()), re.I)
            hits = []
            for where, unit, is_front in units:
                if front and not is_front:
                    continue
                for m in rx.finditer(unit):
                    hits.append((where, m.start(), len(unit)))
            if not hits:
                continue
            if any(off < _R131_HEAD or length < _R131_LONG for _, off, length in hits):
                continue
            shown = "; ".join(f"{w} at character {o} of {n}" for w, o, n in hits[:3])
            scope = "the front page" if front else "the golden"
            emit("ERROR", f"C{num} [R131] cites {cite}, which {scope} states only past the read head of long "
                          f"prose cells ({shown}): the judge reads the sentence around the first hit as the whole "
                          "claim and fails the row (rempel-buyout-plan lost C25 3 of 3 oracle runs, 2026-09-14). "
                          "State the cited rule in the opening sentence of that cell or in a short cell of its own")


# R133 (2026-09-15, hx4180-fa26-spec-rev3 refinement round 3, adjudication): a pinned figure
# that sits on a rounding tie. C11 pinned the size L body length shortfall at -0.725, which the
# golden reached as ROUND(projection - spec, 3) over a projection already ROUNDed to three
# places (28.0245 -> 28.025); the adjudicator recomputed 29.75 x 0.942 - 28.75 = -0.7255, which
# rounds to -0.726, and returned the row twice over: "a correct single-rounding solver is marked
# wrong" and "sits on a rounding boundary". Only formulas built from cell references, numbers,
# + - * / ^ and ROUND, ABS, MIN, MAX are evaluated; anything else is skipped rather than guessed.
_R133_FIG_RE = re.compile(r"(?<![\d.,])-?\d+\.\d{2,}\b")
_R133_TOK_RE = re.compile(
    r"\s*(?:(?:'(?P<qs>[^']+)'|(?P<bs>[A-Za-z_][A-Za-z0-9_.]*))!\$?(?P<c1>[A-Z]{1,3})\$?(?P<r1>\d+)(?![\w:(])"
    r"|\$?(?P<c2>[A-Z]{1,3})\$?(?P<r2>\d+)(?![\w:(])"
    r"|(?P<num>\d+(?:\.\d+)?)"
    r"|(?P<fn>[A-Z]+)\("
    r"|(?P<op>[-+*/^(),]))")


class _R133Unsupported(Exception):
    pass


def _r133_parse(formula, sheet):
    """AST of an arithmetic formula: ('n', D) ('r', sheet, coord) ('-', x) ('b', op, a, b) ('f', name, args)."""
    src, pos, toks = formula.lstrip("="), 0, []
    while pos < len(src):
        if src[pos:].strip() == "":
            break
        m = _R133_TOK_RE.match(src, pos)
        if not m or m.end() == pos:
            raise _R133Unsupported(src[pos:])
        pos = m.end()
        if m.group("c1"):
            toks.append(("r", m.group("qs") or m.group("bs"), m.group("c1") + m.group("r1")))
        elif m.group("c2"):
            toks.append(("r", sheet, m.group("c2") + m.group("r2")))
        elif m.group("num"):
            toks.append(("n", Decimal(m.group("num"))))
        elif m.group("fn"):
            toks.append(("fn", m.group("fn")))
        else:
            toks.append(("op", m.group("op")))
    i = 0

    def peek(*ops):
        return i < len(toks) and toks[i][0] == "op" and toks[i][1] in ops

    def expr():
        nonlocal i
        node = term()
        while peek("+", "-"):
            op = toks[i][1]; i += 1
            node = ("b", op, node, term())
        return node

    def term():
        nonlocal i
        node = power()
        while peek("*", "/"):
            op = toks[i][1]; i += 1
            node = ("b", op, node, power())
        return node

    def power():
        nonlocal i
        node = unary()
        while peek("^"):
            i += 1
            node = ("b", "^", node, unary())
        return node

    def unary():
        nonlocal i
        if peek("-", "+"):
            op = toks[i][1]; i += 1
            inner = unary()
            return ("-", inner) if op == "-" else inner
        return primary()

    def primary():
        nonlocal i
        if i >= len(toks):
            raise _R133Unsupported("end")
        t = toks[i]; i += 1
        if t[0] in ("n", "r"):
            return t
        if t[0] == "fn":
            if t[1] not in ("ROUND", "ABS", "MIN", "MAX"):
                raise _R133Unsupported(t[1])
            args = [expr()]
            while peek(","):
                i += 1
                args.append(expr())
            if not peek(")"):
                raise _R133Unsupported("args")
            i += 1
            return ("f", t[1], args)
        if t == ("op", "("):
            node = expr()
            if not peek(")"):
                raise _R133Unsupported("paren")
            i += 1
            return node
        raise _R133Unsupported(str(t))

    node = expr()
    if i != len(toks):
        raise _R133Unsupported("trailing")
    return node


def _r133_round(x, n):
    return x.quantize(Decimal(1).scaleb(-n), rounding=ROUND_HALF_UP)


class _R133Book:
    """Evaluates a workbook's arithmetic cells in exact decimals, as written (strip None) or with every ROUND to `strip` places or more left unrounded."""

    def __init__(self, fwb, vwb):
        self.fwb, self.vwb, self.memo = fwb, vwb, {}

    def cell(self, sheet, coord, strip, depth=0):
        key = (sheet, coord, strip)
        if key in self.memo:
            return self.memo[key]
        if sheet not in self.fwb.sheetnames or depth > 60:
            raise _R133Unsupported(sheet)
        raw = self.fwb[sheet][coord].value
        if isinstance(raw, str) and raw.startswith("="):
            val = self.eval(_r133_parse(raw, sheet), strip, depth + 1)
        elif isinstance(raw, bool) or not isinstance(raw, (int, float, type(None))):
            raise _R133Unsupported(coord)
        else:
            val = Decimal(str(raw or 0))
        self.memo[key] = val
        return val

    def eval(self, node, strip, depth=0):
        kind = node[0]
        if kind == "n":
            return node[1]
        if kind == "r":
            return self.cell(node[1], node[2], strip, depth)
        if kind == "-":
            return -self.eval(node[1], strip, depth)
        if kind == "b":
            a, b = self.eval(node[2], strip, depth), self.eval(node[3], strip, depth)
            if node[1] == "+":
                return a + b
            if node[1] == "-":
                return a - b
            if node[1] == "*":
                return a * b
            if node[1] == "/":
                if b == 0:
                    raise _R133Unsupported("div0")
                return a / b
            if b != b.to_integral_value():
                raise _R133Unsupported("power")
            return a ** int(b)
        args = [self.eval(a, strip, depth) for a in node[2]]
        if node[1] == "ABS":
            return abs(args[0])
        if node[1] == "MIN":
            return min(args)
        if node[1] == "MAX":
            return max(args)
        if len(args) != 2 or args[1] != args[1].to_integral_value():
            raise _R133Unsupported("ROUND")
        places = int(args[1])
        return args[0] if strip is not None and places >= strip else _r133_round(args[0], places)


@check(codes=['R133'], rules=['GOLD-LAND'], needs=['rubric', 'solution'], params=['rows', 'folder'])
def check_pinned_figure_rounding_tie(rows, folder):
    """A decimal figure a positive pins is the single rounding of its unrounded inputs, and that unrounded value does not sit on a tie at the places the figure is printed to.

    Since: 2026-09-15 (hx4180-fa26-spec-rev3 refinement round 3, adjudication, both items).
    Source: C11 pinned -0.725 on a cell that rounded a difference of cells already rounded to three places; the adjudicator recomputed 29.75 x (1 - 0.058) - 28.75 = -0.7255, rounded it once half away from zero to -0.726, and called the row a boundary a correct solver fails.
    Drift-notes: reads positive rows' decimals of two or more places, both signs, against every solution xlsx cell whose cached value equals one and whose formula's outermost call is ROUND; the cell is evaluated in exact decimals as written (skipped unless that reproduces the cache) and again with every ROUND beneath it to the outer places or more left unrounded (a ROUND to fewer places is a unit the chain means, cents or whole counts, and stays: without that floor the 2026-09-15 probe over 47 folders fired on ri-conversion-review C23, a ratio over a one-place applications count); fires when the stripped value is a tie at the outer places or rounds to another figure. Cross-workbook references, ranges and every other function are skipped, so a pin reached through SUM or a lookup is not read.
    """
    figs = {}
    for num, text, weight in rows:
        if weight <= 0:
            continue
        for m in _R133_FIG_RE.finditer(text):
            d = Decimal(m.group(0))
            for s in (d, -d):
                figs.setdefault(s, num)
    if not figs:
        return
    d = folder / "solution"
    fired = set()
    for path in sorted(d.glob("*.xlsx")) if d.is_dir() else []:
        try:
            fwb, vwb = workbook(path), workbook(path, data_only=True)
        except Exception:
            continue
        book = _R133Book(fwb, vwb)
        for ws in vwb.worksheets:
            for row in ws.iter_rows():
                for c in row:
                    v = c.value
                    if isinstance(v, bool) or not isinstance(v, (int, float)):
                        continue
                    hit = [(fig, n) for fig, n in figs.items() if abs(Decimal(str(v)) - fig) < Decimal("1e-9")]
                    formula = fwb[ws.title][c.coordinate].value
                    if not hit or not isinstance(formula, str) or not formula.upper().startswith("=ROUND("):
                        continue
                    try:
                        node = _r133_parse(formula, ws.title)
                        if node[0] != "f" or node[1] != "ROUND":
                            continue
                        places = book.eval(node[2][1], None)
                        if places != places.to_integral_value():
                            continue
                        places = int(places)
                        if _r133_round(book.eval(node[2][0], None), places) != Decimal(str(v)).quantize(Decimal(1).scaleb(-places)):
                            continue
                        exact = book.eval(node[2][0], places)
                    except (_R133Unsupported, ArithmeticError, KeyError, ValueError):
                        continue
                    single = _r133_round(exact, places)
                    tie = (abs(exact) * (Decimal(10) ** places)) % 1 == Decimal("0.5")
                    if not tie and single == Decimal(str(v)).quantize(Decimal(1).scaleb(-places)):
                        continue
                    for fig, num in hit:
                        if (num, ws.title, c.coordinate) in fired:
                            continue
                        fired.add((num, ws.title, c.coordinate))
                        why = (f"its unrounded value {exact.normalize()} is a tie at {places} places, where a "
                               "rounded-first chain, half-up and half-even solvers land on different figures"
                               if tie else
                               f"rounding once from the unrounded inputs gives {single}, because the formula "
                               "rounds cells that are already rounded")
                        emit("ERROR", f"C{num} [R133] pins {fig}, which {ws.title}!{c.coordinate} reaches as "
                                      f"{formula}: {why}. The adjudicator recomputes from the inputs and marks the "
                                      "row as failing a correct solver (hx4180-fa26-spec-rev3, 2026-09-15: -0.725 "
                                      "against 29.75 x 0.942 - 28.75 = -0.7255). Pin a figure the chain reaches "
                                      "exactly, or carry the chain unrounded so the golden shows the exact figure")
