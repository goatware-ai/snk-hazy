"""Group 1: input file sufficiency, parseability, budget and dates (A7 A11 A12 A16 A18 R23).

Generated 2026-09-04 from autoeval_check.py; every check body is verbatim.
"""
import csv
import re
import zipfile
from ..common import (MONTH_NUM, MONTHS_RE, _solution_cell_values, _solution_raw_values, docx_emdash_stats,
                      input_texts, solution_files, workbook)
from ..core import check, emit, recommend, REPORT, OPTIONS


# R23 (2026-08-20, rempel run 1): a quotation term date the golden never lands on.
_TERM_REL_RE = re.compile(
    r"(?:firm|good|valid|hold(?:s)?|guaranteed)[^.]{0,30}?for\s+"
    r"(sixty|thirty|ninety|forty five|\d{1,3})\s+days", re.I)


_TERM_RE = re.compile(
    r"(?:firm|good|valid|hold(?:s)?|guaranteed)[^.]{0,40}?"
    r"(?:through|until|thru|to)\s+(?:\w+day,\s*)?"
    r"(?:([A-Z][a-z]+)\s+(\d{1,2}),\s*(\d{4})|(\d{1,2})/(\d{1,2})/(\d{4}))", re.I)


def _a18_asof(folder):
    """No input records a completed event dated after the solution's own created stamp.

    Since: 2026-08-21 (oskaloosa reviewer send-back, as-of evidence failure).
    Source: reviewer.
    Drift-notes: scoped to columns whose header names a completed event; numbered A10 until 2026-09-04.
    """
    asof = _solution_asof(folder)
    if not asof: return
    hits = []
    for path in sorted((folder / "inputs").glob("*")):
        if path.suffix.lower() == ".csv":
            try:
                rows = list(csv.reader(path.open(encoding="utf-8-sig")))
            except Exception:
                continue
            if not rows: continue
            cols = [i for i, h in enumerate(rows[0]) if EVENT_COL_RE.search(h or "")]
            for row in rows[1:]:
                for i in cols:
                    if i < len(row) and DATE_CELL_RE.match((row[i] or "").strip()):
                        mm, dd, yy = row[i].split("/")
                        if f"{yy}-{mm}-{dd}" > asof:
                            hits.append(f"{path.name} {rows[0][i]}={row[i]}")
        elif path.suffix.lower() == ".xlsx":
            try:
                wb = workbook(path, data_only=True)
            except Exception:
                continue
            for ws in wb.worksheets:
                head, cols = None, []
                for row in ws.iter_rows(values_only=True):
                    if head is None:
                        if row and sum(1 for c in row if isinstance(c, str)) >= 3:
                            head = row
                            cols = [i for i, h in enumerate(row) if isinstance(h, str)
                                    and EVENT_COL_RE.search(h)]
                            if not cols: head = None
                        continue
                    for i in cols:
                        c = row[i] if i < len(row) else None
                        if isinstance(c, str) and DATE_CELL_RE.match(c.strip()):
                            mm, dd, yy = c.split("/")
                            if f"{yy}-{mm}-{dd}" > asof:
                                hits.append(f"{path.name} {head[i]}={c}")
            wb.close()
    for h in sorted(set(hits))[:6]:
        emit("ERROR", f"[A18] {h} records a completed event dated after the solution was prepared "
                      f"({asof}) — an input pulled for that deliverable cannot contain it "
                      "(oskaloosa reviewer send-back 2026-08-21, as-of evidence failure)")


@check(codes=['R23', 'A18'], rules=['DATA-TIME'], needs=['inputs', 'solution'], params=['folder'])
def check_term_dates(folder):
    """Every term date or validity window an input states is visible on the golden, and no input records a completed event dated after the golden was prepared.

    Codes:
      R23  a firm-price or validity date (or relative window) stated in an input appears in a solution cell
      A18  no input records a completed event dated after the solution's own created stamp
    Since: R23 2026-08-20 (rempel run 1); A18 2026-08-21 (oskaloosa reviewer send-back).
    Source: AutoEval golden_source_fidelity (R23) and the reviewer's as-of evidence read (A18).
    Drift-notes: A18 was a carve-out twin (numbered A10 in the monolith), merged back 2026-09-11.
    """
    _a18_asof(folder)     # [A18] the carve-out twin, merged back 2026-09-11
    bags = _solution_cell_values(folder)
    if not bags:
        return
    joined = " | ".join(" | ".join(b) for b in bags.values())
    for name, text in input_texts(folder):
        if not name.endswith((".docx", ".xlsx")):
            continue
        for m in _TERM_RE.finditer(text):
            if m.group(1):
                mon = MONTH_NUM.get(m.group(1).lower())
                if not mon:
                    continue
                d, y = int(m.group(2)), int(m.group(3))
            else:
                mon, d, y = int(m.group(4)), int(m.group(5)), int(m.group(6))
            forms = {f"{mon:02d}/{d:02d}/{y}", f"{mon}/{d}/{y}"}
            if any(f in joined for f in forms):
                continue
            emit("ERROR", f"[R23] {name} states a term date of {mon:02d}/{d:02d}/{y} "
                          f'("{m.group(0)[:60]}") that no solution cell carries — rempel run 1 '
                          "hard-failed golden_source_fidelity for applying a firm-price rule to one "
                          "vendor and silently skipping another; put the date on the plan even when "
                          "the answer is that it does not bind")
        for m in _TERM_REL_RE.finditer(text):
            # Cleared when the solution's own text carries the same window: the check's
            # remedy is that the window be visible on the plan, and a plan that states
            # "hold ninety days" has done exactly that (returns-cage draft, 2026-08-24 —
            # the Briefing carried the Halbrook hold verbatim and the check fired anyway,
            # an unconditional error with no satisfiable clearing path). The rempel trap
            # stays caught: its window appeared in no solution cell.
            tok = m.group(1)
            variants = {f"{tok} days".lower()}
            words = {"30": "thirty", "45": "forty five", "60": "sixty", "90": "ninety"}
            nums = {v: k for k, v in words.items()}
            if tok in words:
                variants.add(f"{words[tok]} days")
            if tok.lower() in nums:
                variants.add(f"{nums[tok.lower()]} days")
            # the value bags drop prose over 40 chars, so scan the full cell text
            prose = " | ".join(_solution_raw_values(folder)).lower()
            if any(v in prose for v in variants):
                continue
            emit("ERROR", f"[R23] {name} states a relative term window "
                         f'("{m.group(0)[:50]}") that no solution cell mentions — work out the '
                         "date it lands on and put the window on the plan, the same trap rempel "
                         "run 1 failed on")


@check(codes=['A11'], rules=['DATA-SUFF'], needs=['inputs'], params=['folder'])
def check_prose_source_floor(folder):
    """Every prose input document carries at least the word floor the platform's thinness axis applies."""
    for p in (sorted((folder / "inputs").glob("*.docx")) if (folder / "inputs").is_dir() else []):
        stats = docx_emdash_stats(p)
        if not stats:
            continue
        words = stats[1]
        # 2026-08-24 vendor-terms-program dataset feedback: the content-thinness axis holds
        # technical documentation (policy/SOP/manual/procedure files) to a 600-word floor,
        # not the general 500 (inventory_policy.docx scored 196/600 and was a top issue).
        floor = 600 if re.search(r"policy|sop|manual|procedure|instructions", p.name, re.I) else 500
        if words < floor:
            emit("ERROR", f"[A11] inputs/{p.name}: {words} words — a prose source document sits under "
                          f"the {floor}-word floor the Input Files Quality Check applies (600 for "
                          "policy/SOP files per vendor-terms-program's 2026-08-24 dataset feedback; "
                          "a reviewer sent task 16 back at 441 and 411 words). Grow it with material "
                          "the author would really have put in, adding nothing the solver is meant "
                          "to deduce")


@check(codes=['A16'], rules=['DATA-OPEN'], needs=['inputs', 'solution'], params=['folder'])
def check_package_parses(folder):
    # A16 (2026-08-26, pavelka reviewer revision): every packaged office file must PARSE.
    # Both pavelka xlsx inputs shipped a docProps/core.xml using dc:/dcterms:/xsi:
    # prefixes with no namespace declarations - lxml refuses the part, so openpyxl
    # (and pandas, which a solver's tooling rides on) cannot open the file at all.
    # Worse, every load_workbook site in THIS gate swallows the exception and skips
    # the file, so the unreadable input also passed the A12 thinness sweep it should
    # have failed (87 cells surfaced only after the namespace fix). Parse every XML
    # part of every .xlsx/.docx in inputs/ and solution/, and load each xlsx with
    # openpyxl, erroring instead of skipping: an unreadable file is a defect in
    # itself, and it blinds every downstream check that silently continues past it.
    """Every packaged Office file parses: each XML part is well-formed and openpyxl opens each workbook.

    Since: 2026-08-26 (pavelka reviewer revision).
    Source: reviewer; an unreadable part also blinded the A12 thinness sweep, so this errors rather than skips.
    """
    from lxml import etree as _etree
    for p_ in sorted(list((folder / "inputs").glob("*.[xd][lo]*")) +
                     (sorted((folder / "solution").glob("*.xlsx"))
                      if (folder / "solution").is_dir() else [])):
        if p_.suffix.lower() not in (".xlsx", ".docx"):
            continue
        try:
            with zipfile.ZipFile(p_) as z_:
                for n_ in z_.namelist():
                    if n_.endswith((".xml", ".rels")):
                        try:
                            _etree.fromstring(z_.read(n_))
                        except Exception as e_:
                            emit("ERROR", f"[A16] {p_.relative_to(folder)}: {n_} is not "
                                          f"well-formed XML ({e_}) — openpyxl/pandas refuse the "
                                          "whole file, a solver's tooling crashes on it, and this "
                                          "gate's own loaders silently skip it, blinding every "
                                          "downstream check (pavelka 2026-08-26: the broken part "
                                          "hid an A12 thinness failure)")
        except Exception as e_:
            emit("ERROR", f"[A16] {p_.relative_to(folder)}: unreadable as a zip package ({e_})")
        if p_.suffix.lower() == ".xlsx":
            try:
                workbook(p_).close()
            except Exception as e_:
                emit("ERROR", f"[A16] {p_.relative_to(folder)}: openpyxl cannot open it "
                              f"({type(e_).__name__}: {e_}) — fix the package rather than "
                              "trusting checks that skip what they cannot read")


@check(codes=['A12'], rules=['DATA-SUFF'], needs=['inputs', 'solution'], params=['folder'])
def check_input_thinness(folder):
    # A12 (2026-08-23, vondrak run 2): the platform's content-thinness axis applies a
    # 100-populated-cell floor to each input spreadsheet, with a 25-cell hard minimum and
    # an aggregate-bundle carveout it grants grudgingly (vondrak's 45-cell purchase record
    # passed "only under the aggregate-content carveout" and was named a top issue).
    # Clear the floor per file rather than leaning on the carveout.
    # Extended to CSVs 2026-08-24: rossville's open_po_lines_0821.csv sat at ~72 cells,
    # invisible to the xlsx-only sweep, and the dataset feedback named it a top issue.
    """Each input spreadsheet or CSV holds at least 100 populated cells, and never fewer than 25.

    Since: 2026-08-23 (vondrak run 2); CSVs added 2026-08-24 (rossville).
    Source: the Input Files Quality Check's content-thinness axis (100-cell floor, 25-cell hard minimum).
    """
    inp = folder / "inputs"
    for p_ in (sorted(q for q in inp.iterdir()
                      if q.suffix.lower() in (".xlsx", ".csv")) if inp.is_dir() else []):
        if p_.suffix.lower() == ".csv":
            try:
                rows_ = list(csv.reader(p_.open(encoding="utf-8-sig")))
            except Exception:
                continue
            cells = sum(1 for row_ in rows_ for v_ in row_ if v_.strip())
        else:
            try:
                wb_ = workbook(p_)
            except Exception:
                continue
            cells = sum(1 for ws_ in wb_.worksheets for row_ in ws_.iter_rows()
                        for c_ in row_ if c_.value is not None)
            wb_.close()
        if cells < 25:
            emit("ERROR", f"[A12] inputs/{p_.name}: {cells} populated cells — under the platform's "
                          "25-cell hard minimum for an input spreadsheet (thinness axis)")
        elif cells < 100:
            emit("ERROR", f"[A12] inputs/{p_.name}: {cells} populated cells — under the 100-cell "
                         "floor the content-thinness axis applies per spreadsheet; the aggregate "
                         "carveout can save it but gets named a top issue (vondrak run 2, "
                         "2026-08-23). Add the columns the record would really carry")


@check(codes=['A7'], rules=['DATA-BUDGET'], needs=['solution'], params=['folder'])
def check_reviewer_budget(folder):
    """The deliverable's extracted text stays within what an agentic reviewer can hold in one read.

    The Agentic Rubric Quality Review reads every input file AND the golden workbook
    through its own tools, then reads rubrics.txt and instruction.md. Kolterman's review
    (2026-08-21) came back needs_improvement with a [critical] completeness finding and no
    rubric analysis at all: both of those files returned "[Prior result omitted from
    context to avoid token overflow]". They are the two SMALLEST files in the submission
    (about 14k and 2k chars) and they were evicted because they were read first, behind
    260k chars of inputs and deliverable. The deliverable was 154k of that, 3.3x the next
    largest golden in the catalog (23k to 46k) because it carries a 907-row line-level
    ledger. Nothing in the rubric was wrong; the reviewer simply never saw it.

    Design lever, not a submission gate: keep the golden's own text inside the band the
    rest of the catalog sits in, and push row-level detail the answer does not need into
    the inputs.
    """
    d = folder / "solution"
    if not d.is_dir():
        return
    for path in sorted(d.glob("*.xlsx")):
        try:
            wb = workbook(path, data_only=True)
        except Exception:
            continue
        chars = sum(len(",".join("" if v is None else str(v) for v in row)) + 1
                    for ws in wb.worksheets for row in ws.iter_rows(values_only=True))
        wb.close()
        if chars > 100_000:
            emit("ERROR", f"[A7] {path.name} carries {chars:,} chars of text, against a 23k to 46k "
                         "band across the rest of the catalog. The Agentic Rubric Quality Review "
                         "reads the whole deliverable plus every input before it reads the rubric, "
                         "and kolterman's review evicted rubrics.txt and instruction.md from its own "
                         "context at 260k chars total (2026-08-21). Carry row-level ledgers only "
                         "where an answer needs them")


EVENT_COL_RE = re.compile(r"\b(received|posted|shipped|invoiced|picked|counted|delivered|"
                          r"paid|entered|keyed)\b", re.I)


DATE_CELL_RE = re.compile(r"^(0[1-9]|1[0-2])/([0-2]\d|3[01])/(20\d\d)$")


def _solution_asof(folder):
    """The analyst's working date: the earliest docProps created stamp on a solution file."""
    stamps = []
    for path in solution_files(folder, (".xlsx", ".docx", ".pptx")):
        try:
            with zipfile.ZipFile(path) as z:
                xml = z.read("docProps/core.xml").decode("utf-8", "replace")
        except Exception:
            continue
        m = re.search(r"<dcterms:created[^>]*>(\d{4}-\d{2}-\d{2})", xml)
        if m: stamps.append(m.group(1))
    return min(stamps) if stamps else None


# G22 (2026-09-11, returns-cage-disposition FINAL REJECTION): the 08/14 cage count
# tagged goods under authorizations the RGA log issues on 08/15 and 08/16, and the
# controller memo's suspense balance "at the close of business Friday, August 14"
# equalled the credit register summed WITHOUT a date filter - three credit memos dated
# 08/15-08/16 (736.76 at item cost) sat inside a stated 08/14 balance. The golden
# inherited both, the rubric pinned the balance, and every fidelity re-derivation
# "matched" because it summed the same undated register (a matching recomputation
# proves consistency, not correctness). Adjudication rejected the task on this alone
# after the revision limit. Two mechanical faces:
#   (a) referential chronology: a snapshot input stamped _MMDD in its filename must not
#       reference record ids another input dates AFTER the snapshot date;
#   (b) as-of balance: a docx figure anchored "at/as of <date>" that equals a register's
#       UNFILTERED cost sum while the date-filtered sum differs is a cutoff violation.
_G22_ID_RE = re.compile(r"^[A-Z]{1,2}\d{3,7}$")
_G22_DATE_RE = re.compile(r"^(\d{1,2})/(\d{1,2})/(\d{4})$")
_G22_STAMP_RE = re.compile(r"_(0[1-9]|1[0-2])([0-2]\d|3[01])(?:\D|$)")
_G22_ASOF_RE = re.compile(
    r"(?:stood at|balance (?:of|was)|balance stood at)\s*\$?([\d,]+\.\d{2})\b"
    r"[^.]{0,120}?(?:as of|at the close of business|on|at)\s+(?:\w+day,?\s*)?"
    r"(?:(" + MONTHS_RE + r")\s+(\d{1,2})|(\d{1,2})/(\d{1,2}))", re.I)


def _g22_parse(s):
    m = _G22_DATE_RE.match(str(s).strip())
    return (int(m.group(3)), int(m.group(1)), int(m.group(2))) if m else None


def _g22_tables(folder):
    """Every csv and first-sheet xlsx input as a list of string rows."""
    out = {}
    d = folder / "inputs"
    for path in sorted(d.iterdir()) if d.is_dir() else []:
        try:
            if path.suffix == ".csv":
                out[path.name] = [[(c or "").strip() for c in row]
                                  for row in csv.reader(path.open(encoding="utf-8-sig"))]
            elif path.suffix == ".xlsx":
                ws = workbook(path, data_only=True).worksheets[0]
                out[path.name] = [["" if c is None else str(c).strip() for c in row]
                                  for row in ws.iter_rows(values_only=True)]
        except Exception:
            continue
    return out


# G22 (c), 2026-09-14 (recall-response refinement round 3): a workbook input's PAST-EVENT date
# column (returned_date, received_date, Transaction Date ...) never runs later than the file's
# own dcterms:modified stamp. A Returns sheet dated 2026-08-24 sat inside a snapshot stamped
# 2026-08-18, the notice's own day; adjudication read the return as includable or excludable
# and the pinned unaccounted figure as moving by one either way. Headers that name a future
# event (due, expiry, deadline, planned, scheduled ...) are left alone.
_G22_PAST_HDR_RE = re.compile(
    r'''(?:returned|received|receipt|posted|issued|invoice|adjust\w*|transaction|shipped|ship|delivered|paid|logged|recorded|entered|count|transfer|pick|packed|sold|order)[ _]?date'''
    r'''|date[ _]?(?:received|returned|shipped|posted|issued|paid|delivered|adjusted|counted|of[ _]receipt|of[ _]return)''', re.I)
_G22_FUTURE_HDR_RE = re.compile(r'''due|expir|deadline|planned|scheduled|promised|target|forecast|eta|arrival|renew|valid|next''', re.I)


def _g22_workbook_stamps(folder):
    """G22 (c): each inputs/*.xlsx past-event date column against the file's own modified stamp."""
    import openpyxl, zipfile, datetime, glob, os
    for path in sorted(glob.glob(os.path.join(str(folder), "inputs", "*.xlsx"))):
        try:
            with zipfile.ZipFile(path) as z:
                core = z.read("docProps/core.xml").decode("utf-8", "replace")
            m = re.search(r"<dcterms:modified[^>]*>(\d{4})-(\d\d)-(\d\d)", core)
            if not m:
                continue
            stamp = datetime.date(*map(int, m.groups()))
            wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
        except Exception:
            continue
        for ws in wb.worksheets:
            rows = ws.iter_rows(values_only=True)
            hdr = next(rows, None)
            if not hdr:
                continue
            cols = [j for j, h in enumerate(hdr)
                    if h and _G22_PAST_HDR_RE.search(str(h)) and not _G22_FUTURE_HDR_RE.search(str(h))]
            if not cols:
                continue
            latest = {}
            for r in rows:
                for j in cols:
                    v = r[j] if j < len(r) else None
                    d = None
                    if isinstance(v, datetime.datetime):
                        d = v.date()
                    elif isinstance(v, datetime.date):
                        d = v
                    elif isinstance(v, str) and re.fullmatch(r"\d{4}-\d\d-\d\d", v.strip()):
                        try:
                            d = datetime.date.fromisoformat(v.strip())
                        except ValueError:
                            d = None
                    if d and (j not in latest or d > latest[j]):
                        latest[j] = d
            for j, d in latest.items():
                if d > stamp:
                    emit("ERROR", f"[G22] inputs/{os.path.basename(path)} sheet {ws.title!r} column {hdr[j]!r} "
                                  f"runs to {d.isoformat()} but the workbook's own modified stamp is {stamp.isoformat()} - "
                                  "a record dated after the file was written. Adjudication read a return dated six days "
                                  "after the notice as includable or excludable and the pinned unaccounted figure as "
                                  "moving by one (recall-response refinement round 3, 2026-09-14). Date every record on "
                                  "or before the stamp, or move the stamp")
        wb.close()


@check(codes=['G22'], rules=['DATA-TIME'], needs=['inputs'], params=['folder'])
def check_cutoff_chronology(folder):
    """A snapshot input stamped with a date never references records another input dates after it, and a stated as-of balance equals the date-filtered register sum.

    Since: 2026-09-11 (returns-cage-disposition, rejected at adjudication after the revision limit).
    Source: adjudication; a matching re-derivation over an undated register proves consistency, not correctness.
    Drift-notes: tightened 2026-09-14 (a workbook's past-event date column against its own modified stamp).
    """
    _g22_workbook_stamps(folder)
    tables = _g22_tables(folder)
    if not tables:
        return
    # id -> (record date, source file): first id-like column against first date column
    dated, years = {}, {}
    for name, rows in tables.items():
        body = [r for r in rows if any(r)][1:]
        if len(body) < 3:
            continue
        ncol = max(len(r) for r in body)
        # a register dates its OWN records, whose id leads the row: only column 0 may
        # feed the id map (narrowed 2026-09-11 after the first cut mapped frankfort's
        # STOCK NO item codes, column 3 of an order backlog, to order dates)
        idc = datec = None
        col0 = [r[0] for r in body if r and r[0]]
        if len(col0) >= 3 and sum(bool(_G22_ID_RE.match(v)) for v in col0) >= 0.8 * len(col0):
            idc = 0
        for j in range(1, ncol):
            col = [r[j] for r in body if j < len(r) and r[j]]
            if len(col) < 3:
                continue
            if datec is None and sum(bool(_g22_parse(v)) for v in col) >= 0.8 * len(col):
                datec = j
        if idc is None or datec is None:
            continue
        for r in body:
            if idc < len(r) and datec < len(r):
                d_ = _g22_parse(r[datec])
                if d_ and _G22_ID_RE.match(r[idc]):
                    dated.setdefault(r[idc], (d_, name))
                    years[d_[0]] = years.get(d_[0], 0) + 1
    if not dated:
        return
    year = max(years, key=years.get)

    # (a) snapshot files referencing later-dated records
    for name, rows in tables.items():
        m = _G22_STAMP_RE.search(name)
        if not m:
            continue
        cut = (year, int(m.group(1)), int(m.group(2)))
        late = []
        for r in rows:
            for v in r:
                hit = dated.get(v)
                if hit and hit[0] > cut and v not in [x[0] for x in late]:
                    late.append((v, hit))
        if late:
            listed = "; ".join(f"{v} dated {d_[1]:02d}/{d_[2]:02d}/{d_[0]} in {src}"
                               for v, (d_, src) in late[:6])
            emit("ERROR", f"[G22] inputs/{name} is a snapshot stamped "
                          f"{cut[1]:02d}/{cut[2]:02d} but references records dated after it "
                          f"({listed}) - the returns-cage 08/14 cage count carried "
                          "authorizations issued 08/15-08/16 and the task was REJECTED at "
                          "adjudication on the chronology (2026-09-11). Date every referenced "
                          "record on or before the snapshot, or move the snapshot date")

    # (b) an as-of balance equal to an unfiltered register sum
    docx_texts = {n: t for n, t in input_texts(folder) if n.endswith(".docx")}
    # item -> candidate cost columns from any table whose first column looks like item codes
    item_cost = {}
    for name, rows in tables.items():
        body = [r for r in rows if any(r)][1:]
        col0 = [r[0] for r in body if r and r[0]]
        if len(col0) >= 3 and sum(bool(re.match(r"^[A-Z]{2,3}-\w+", v)) for v in col0) >= 0.8 * len(col0):
            for r in body:
                if r and r[0]:
                    nums = []
                    for v in r[1:]:
                        try:
                            nums.append(float(str(v).replace(",", "")))
                        except ValueError:
                            nums.append(None)
                    item_cost.setdefault(r[0], nums)
    for docname, text in docx_texts.items():
        for m in _G22_ASOF_RE.finditer(text):
            stated = float(m.group(1).replace(",", ""))
            if stated < 100:
                continue
            if m.group(2):
                cut = (year, MONTH_NUM[m.group(2).lower()], int(m.group(3)))
            else:
                cut = (year, int(m.group(4)), int(m.group(5)))
            for name, rows in tables.items():
                body = [r for r in rows if any(r)][1:]
                if len(body) < 3:
                    continue
                hdr = next((r for r in rows if any(r)), [])
                cols = {h.strip().upper(): j for j, h in enumerate(hdr) if h}
                itemc = next((j for h, j in cols.items() if "ITEM" in h), None)
                qtyc = next((j for h, j in cols.items() if h in ("QTY", "QUANTITY", "UNITS")), None)
                datec = next((j for j in range(len(hdr))
                              if sum(bool(_g22_parse(r[j])) for r in body if j < len(r))
                              >= 0.8 * len(body)), None)
                if itemc is None or qtyc is None or datec is None:
                    continue
                ncost = max((len(v) for v in item_cost.values()), default=0)
                for k in range(ncost):
                    full = filt = 0.0
                    ok = True
                    for r in body:
                        try:
                            unit = item_cost.get(r[itemc], [])[k]
                            q = float(r[qtyc])
                            d_ = _g22_parse(r[datec])
                        except (IndexError, ValueError, TypeError):
                            ok = False
                            break
                        if unit is None or d_ is None:
                            ok = False
                            break
                        full += unit * q
                        if d_ <= cut:
                            filt += unit * q
                    if ok and abs(full - stated) <= 0.02 and abs(filt - stated) > 0.02:
                        emit("ERROR", f"[G22] inputs/{docname} states a balance of {m.group(1)} as of "
                                      f"{cut[1]:02d}/{cut[2]:02d}/{cut[0]}, and inputs/{name} reproduces "
                                      f"it only when summed WITHOUT the date cutoff (filtered sum "
                                      f"{filt:,.2f}) - the returns-cage memo's 15,127.75 'at the close "
                                      "of business Friday, August 14' included credit memos dated "
                                      "08/15-08/16 and the task was REJECTED at adjudication "
                                      "(2026-09-11). Set the stated balance to the date-filtered sum "
                                      "or redate the late records")
                        break
