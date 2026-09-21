"""Group 4: the pre-zip hygiene sweeps (H1-H5), formerly tools/audit_task.py.

Every file in the folder is read (docx/xlsx member by member) for:

  H1  the programme codename anywhere, embedded metadata included
  H2  555-prefix phone numbers
  H3  weekday/date pairs that are calendar-false ("Friday, October 3, 2026")
  H4  packaging: a space in a name, a double extension, an empty file, and inside any zip
      a subfolder, a space or an empty member
  H5  a file the prompt names that does not exist in the folder
  H6  a placeholder or dummy phrase in an input file (sample data, dummy text, placeholder,
      lorem ipsum, TBD), PDFs included: the platform's Input Files Quality Check FAILs on the
      bare keyword even inside a published report (2026-09-12: EIA's "estimated
      from sample data reported on Form EIA-857")

Future dates (mm/dd/yyyy after today) are counted, not judged: genuinely prospective
deadlines are allowed, so the count prompts a date audit by hand. The per-date list was
dropped 2026-08-24 (255 advisory lines on one task, no platform failure ever traced to one).
"""
import csv
import datetime as dt
import os
import re
import zipfile

from ..common import MONTH_NUM, MONTHS_RE, package_texts, CODENAME_RE
from ..core import check, emit


def texts(path):
    """(member, text) over the file types the sweeps read; common.package_texts does the reading.

    PDFs are read page by page through pypdf (2026-09-12): the platform's Input Files Quality
    Check extracts their text and keyword-matches it like any other input."""
    if str(path).lower().endswith(".pdf"):
        try:
            import pypdf
            for i, pg in enumerate(pypdf.PdfReader(str(path)).pages, 1):
                yield f"page {i}", (pg.extract_text() or "")
        except Exception:
            return
        return
    yield from package_texts(path, suffixes=(".xlsx", ".docx", ".md", ".csv", ".txt"))


# H6 (2026-09-12, pre-submission): "Files contain placeholder
# or dummy text: sample data". The phrase sat in the EIA Natural Gas Monthly's own methodology
# notes; the check does not read context, so the phrase itself is the defect.
PLACEHOLDER_RE = re.compile(r"\b(?:sample data|dummy (?:text|data|values?|entr(?:y|ies))|placeholder(?: text)?"
                            r"|lorem ipsum|\bTBD\b|\bTBC\b|xxx+)\b", re.I)


WD = {w: i for i, w in enumerate(["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"])}
MN = MONTH_NUM
LONG = re.compile(r"(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),?\s+(" + MONTHS_RE + r")\s+(\d{1,2}),?\s+(\d{4})", re.I)
SHORT = re.compile(r"(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\s+(\d{2})/(\d{2})/(\d{4})", re.I)
MDY = re.compile(r"\b(\d{2}/\d{2}/\d{4})\b")


def sweep(folder, codename=True):
    """([(code, message)], {future date: {files}}) for one task folder.

    `codename=False` leaves H1 out: the gate emits it from check_meta_references' single pass
    over the same files (2026-09-11); the standalone audit_task command still reports it."""
    folder = str(folder)
    fails = []
    # feedback-log.md quotes historical defects verbatim (bad weekdays, flagged values) - not a deliverable
    allfiles = [os.path.join(r, f) for r, _, fs in os.walk(folder) for f in fs
                if f != 'feedback-log.md']
    today = dt.date.today()
    future = {}
    for p in allfiles:
        base = os.path.basename(p)
        if ' ' in base: fails.append(("H4", f"SPACE IN NAME {p}"))
        if re.search(r'\.(docx|xlsx|csv|zip|md|pdf|pptx)\.(docx|xlsx|csv|zip|md|pdf|pptx)$', base):
            fails.append(("H4", f"DOUBLE EXTENSION {p}"))
        try:
            size = os.path.getsize(p)
            with open(p, "rb"):
                pass
        except OSError as exc:
            # an unreadable file is a finding, not a crash: a PermissionError here aborted a
            # 22-task catalog run on 2026-09-15
            fails.append(("H4", f"UNREADABLE FILE {p} ({exc.strerror or exc})"))
            continue
        if size == 0: fails.append(("H4", f"EMPTY FILE {p}"))
        for n, t in texts(p):
            if codename and CODENAME_RE.search(t): fails.append(("H1", f"CANARY {p} ({n})"))
            if re.search(r'\b555-\d{4}|\(555\)', t): fails.append(("H2", f"555 PHONE {p} ({n})"))
            if os.sep + 'inputs' + os.sep in p and not re.search(
                    r'(?:styles\w*|numbering|settings|webSettings|fontTable|theme\d*)\.xml$|customXml/', n):
                # Word's own style catalogue names a "Placeholder Text" style in every docx;
                # only body, header, footer, sheet and string parts carry what a reader sees
                m6 = PLACEHOLDER_RE.search(t)
                if m6: fails.append(("H6", f"PLACEHOLDER PHRASE \"{m6.group(0)}\" {p} ({n}) - the platform's Input "
                                           "Files Quality Check FAILs on the keyword whatever the context; drop the "
                                           "page or reword the passage"))
            for m in LONG.finditer(t):
                d = dt.date(int(m.group(4)), MN[m.group(2).lower()], int(m.group(3)))
                if d.weekday() != WD[m.group(1).lower()]:
                    fails.append(("H3", f"WEEKDAY {p}: '{m.group(0)}' is a {d.strftime('%A')}"))
            for m in SHORT.finditer(t):
                d = dt.date(int(m.group(4)), int(m.group(2)), int(m.group(3)))
                if d.weekday() != WD[m.group(1).lower()]:
                    fails.append(("H3", f"WEEKDAY {p}: '{m.group(0)}' is a {d.strftime('%A')}"))
            for m in MDY.finditer(t):
                try: d = dt.datetime.strptime(m.group(1), '%m/%d/%Y').date()
                except ValueError: continue
                if d > today: future.setdefault(m.group(1), set()).add(os.path.basename(p))
    for z in [p for p in allfiles if p.endswith('.zip')]:
        try:
            zf = zipfile.ZipFile(z)
        except (OSError, zipfile.BadZipFile) as exc:
            if not any(msg.startswith(f"UNREADABLE FILE {z} ") for _, msg in fails):
                fails.append(("H4", f"UNREADABLE ZIP {z} ({exc})"))
            continue
        with zf:
            for n in zf.namelist():
                if '/' in n: fails.append(("H4", f"SUBFOLDER IN ZIP {z}: {n}"))
                if ' ' in n: fails.append(("H4", f"SPACE IN ZIP MEMBER {z}: {n}"))
                if zf.getinfo(n).file_size == 0: fails.append(("H4", f"EMPTY ZIP MEMBER {z}: {n}"))
    prompt = os.path.join(folder, 'prompt.md')
    if os.path.exists(prompt):
        try:
            ptext = open(prompt, encoding='utf-8').read()
        except OSError:
            # already reported as UNREADABLE FILE above; H5 cannot be judged without the prompt
            return fails, future
        named = set(re.findall(r'[\w-]+\.(?:docx|xlsx|csv|pdf|pptx|json|xml|md)', ptext))
        have = {os.path.basename(p) for p in allfiles}
        for f in sorted(named - have):
            fails.append(("H5", f"PROMPT NAMES MISSING FILE: {f}"))
    return fails, future


@check(codes=['H2', 'H3', 'H4', 'H5', 'H6'], rules=['REV-CREDIBLE', 'PRE-PACK'],
       needs=['inputs', 'solution'], params=['folder'])
def check_hygiene(folder):
    """Every shipped file is free of 555 phone numbers and calendar-false weekdays, packaging is flat with clean non-empty names, and every file the prompt names exists.

    Codes:
      H2  no 555-prefix phone number
      H3  no weekday/date pair that is calendar-false
      H4  no space or double extension in a name, no empty file, no subfolder, space or empty member in a zip
      H5  every file the prompt names exists in the folder
      H6  no placeholder or dummy phrase (sample data, dummy text, placeholder, lorem ipsum, TBD) in an input file, PDFs read too
    Source: tools/audit_task.py sweeps (the in-app Name Check and packaging checks).
    Drift-notes: H1 is emitted from check_meta_references' single pass since 2026-09-11; the standalone
    audit_task command still reports it.
    """
    fails, future = sweep(folder, codename=False)     # H1 comes from check_meta_references' pass
    for code, msg in fails:
        emit("ERROR", f"[{code}] {msg}")
    print(f"        info: {len(fails)} hygiene failures, {len(future)} future dates to review")


# H7 (2026-09-14): a finding returned "the
# fuel index table jumps from 2026-07-27 straight to 2026-11-30, omitting every Monday from
# 2026-08-03 through 2026-11-23" twice against a 57-line CSV that was complete, and the six
# invoice lines it cited as examples were exactly the FUEL lines inside the first 25 and last
# 15 lines of carrier_invoices.csv. The platform previews that window of every CSV and
# reads it as the whole file; answering that the file is complete does not land, the note
# comes back verbatim. A chronological reference table (a weekly index, a monthly series) is
# the shape it expects to see whole and reads as gapped; a long transaction log is sampled and
# nobody expects the middle. Probed 2026-09-14 over 62 portfolio CSVs: fires on the pre-fix
# fuel_index.csv and on one other chronological series; quiet on logs and lookups whose first
# column is an id. Widened 2026-09-14: the same window hid
# lines 26 to 146 of a 161-line parts master keyed by a sorted, unique part number, and the note
# called PN-30744 and PN-30702 absent while quoting the file's last line as its end. A sorted
# unique-id lookup is a reference table too, read whole and read as ending where the preview
# ends, so that shape fires at any length over 40 lines; a log repeats its keys and stays out.
_H7_DATE_RE = re.compile(r"^\d{4}-\d{2}(?:-\d{2})?$|^\d{1,2}-[A-Za-z]{3}-\d{4}$|^\d{1,2}/\d{1,2}/\d{4}$")
_H7_ID_RE = re.compile(r"^[A-Za-z]{1,6}[-_]?\d{2,}[A-Za-z0-9-]*$")


@check(codes=['H7'], rules=['PRE-PACK'], needs=['inputs'], params=['folder'])
def check_previewable_series(folder):
    """A reference CSV input, a dated series or a sorted unique-id lookup, is 40 lines or fewer, laid out in side-by-side panels if it is longer, because the platform previews the first 25 and last 15 lines of a CSV and reads the hidden middle as missing rows.

    Since: 2026-09-14 (the same note twice on one task; the id arm from a second task the same day; the date arm widened to any length the same day on a third).
    Source: a platform finding (input omissions), proven by the note's own example lines.
    Drift-notes: the date arm fires on any file over 40 lines whose first column is a date on 90 percent of rows and
    sorted ascending, repeated keys allowed; the id arm fires on any file over 40 lines whose first column is an id on
    90 percent of rows, unique and sorted ascending. The 120-line cap and the "logs are sampled" assumption were
    dropped 2026-09-14: an 1,800-line reefer logger, an 1,128-line invoice file
    and a 160-line manifest were each read as the first 25 and last 15 lines and the golden's rows called absent.
    """
    inputs = folder / "inputs"
    if not inputs.is_dir():
        return
    for path in sorted(inputs.glob("*.csv")):
        try:
            with open(path, encoding="utf-8-sig", newline="") as fh:
                rows = list(csv.reader(fh))
        except (OSError, UnicodeDecodeError):
            continue
        n = len(rows)
        if n < 41:
            continue
        col = [r[0].strip() for r in rows[1:] if r]
        if not col:
            continue
        datelike = sum(1 for c in col if _H7_DATE_RE.match(c))
        idlike = sum(1 for c in col if _H7_ID_RE.match(c))
        if datelike / len(col) >= 0.9 and col == sorted(col):
            emit("ERROR", f"[H7] {path.name}: {n} lines of a chronological series ({col[0]} to {col[-1]}); "
                          "the platform previews the first 25 and last 15 lines of a CSV and returned "
                          "fuel_index.csv's rows 25 to 41 as 'every Monday from 2026-08-03 through 2026-11-23 "
                          "omitted' twice (2026-09-12 and 09-14) and called every excursion "
                          "reading of an 1,800-line reefer logger missing (2026-09-14). Lay the "
                          "series out in side-by-side panels, or one row per key with the series across columns, "
                          "so the file is 40 lines or fewer")
        elif idlike / len(col) >= 0.9 and len(set(col)) == len(col) and col == sorted(col):
            emit("ERROR", f"[H7] {path.name}: {n} lines of a lookup keyed by a sorted unique id ({col[0]} to "
                          f"{col[-1]}); the platform previews the first 25 and last 15 lines of a CSV and called "
                          "PN-30744 and PN-30702 absent from a 161-line parts master whose last line it quoted as "
                          "the file's end (2026-09-14). Lay the table out in side-by-side "
                          "panels so the file is 40 lines or fewer")

def main(folder):
    """The old audit_task.py command: FAIL lines and a summary, exit 1 on any failure."""
    fails, future = sweep(folder)
    for _, f in fails: print("FAIL", f)
    print(f"{folder}: {len(fails)} failures, {len(future)} future dates to review")
    return 1 if fails else 0


# H8 (2026-09-14): the finding
# reported the five receipts, the two 1004 requests with their log entries, and the
# 1005 damage pair as "no occurrence in the provided input previews or query-matched rows",
# while quoting adjustments row 249 and transactions rows 338 and 407 back verbatim. The rows
# sat at 122 to 180 of 300, 296 to 407 of 514 and 184 to 255 of 257: the hidden middle of the
# 25+15 window H7 describes for a CSV, here on xlsx logs, with the query matching finding some
# rows and not others. PR12 once said to order the log so the cited key's rows sit near the top (superseded 2026-09-15 by the panel relay);
# this is that rule as a detector, for every id the golden cites.
_H8_ID_RE = re.compile(r"\b[A-Z]{2,6}(?:-[A-Z]{2,6})?-\d{3,8}\b")
_H8_HEAD, _H8_TAIL, _H8_MIN_ROWS = 25, 15, 40
# two side-by-side panels of 23 data rows fit the head window (2026-09-14:
# a 31-serial account block on a 239-row register was called absent at rows 40 and 60 with the cap at 25)
_H8_PANEL_CAP = 2 * (_H8_HEAD - 2)


def _h8_shape(v):
    return re.sub(r"\d", "9", re.sub(r"[A-Z]", "A", v))


def _h8_tables(folder):
    import csv
    from ..common import workbook
    d = folder / "inputs"
    for path in sorted(d.glob("*")) if d.is_dir() else []:
        if path.suffix.lower() == ".csv":
            try:
                rows = list(csv.reader(path.open(encoding="utf-8-sig", errors="ignore")))
            except Exception:
                continue
            if len(rows) > 1:
                yield path.name, [[(c.strip() or None) for c in r] for r in rows[1:]], _H8_TAIL
        elif path.suffix.lower() == ".xlsx":
            try:
                wb = workbook(path, data_only=True)
            except Exception:
                continue
            for ws in wb.worksheets:
                data = list(ws.iter_rows(values_only=True))
                if len(data) > 1:
                    yield f"{path.name} {ws.title}", [[(str(v).strip() or None) if v is not None else None for v in r] for r in data[1:]], 0


_H8_FIG_RE = re.compile(r"-?\d*\.\d+")
_H8_FIG_MIN_ROWS = 5


def _h8_fig(v):
    return round(float(v), 6)


def _h8_golden_typed_figures(folder):
    """Decimal figures of three or more digits typed (not computed) into the golden's cells."""
    from ..common import workbook
    sol = folder / "solution"
    out = set()
    for p in sorted(sol.glob("*.xlsx")) if sol.is_dir() else []:
        try:
            wb = workbook(p, data_only=False)
        except Exception:
            continue
        for ws in wb.worksheets:
            for row in ws.iter_rows():
                for c in row:
                    v = c.value
                    if isinstance(v, float) and not isinstance(v, bool) and v != int(v):
                        if len(re.sub(r"[^0-9]", "", repr(v))) >= 3:
                            out.add(round(v, 6))
    return out


def _h8_golden_text(folder):
    from ..common import _docx_text, workbook
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


_H8_EXEMPT_VISIBLE = True


def _h8_visible_figures(folder):
    """Decimal figures some input shows inside the platform's preview: every row of a table of 40 rows or
    fewer, the head window (and a CSV's tail) of a longer one, and the whole text of a docx input."""
    from ..common import _docx_text
    out = set()
    for _name, rows, tail in _h8_tables(folder):
        n = len(rows)
        for i, r in enumerate(rows, start=1):
            if n <= _H8_MIN_ROWS or i <= _H8_HEAD or i > n - tail:
                out.update(_h8_fig(v) for v in r if v and _H8_FIG_RE.fullmatch(v))
    d = folder / "inputs"
    for path in sorted(d.glob("*.docx")) if d.is_dir() else []:
        try:
            out.update(_h8_fig(m.group(0)) for m in re.finditer(r"-?\d*\.\d+", _docx_text(path)))
        except Exception:
            continue
    return out


@check(codes=['H8'], rules=['PRE-PACK'], needs=['inputs', 'solution'], params=['folder'])
def check_cited_rows_in_window(folder):
    """Every input row keyed by an id the golden cites, or carrying a decimal figure the golden types into a cell that no input shows inside its own preview, sits inside the platform's preview window, the first 25 rows of a workbook sheet or the first 25 and last 15 lines of a CSV, when the file is longer than 40 rows; a cited row outside it is reported as absent whatever the golden says about it.

    Since: 2026-09-14.
    Source: a platform finding ("no occurrence of ADJ-546964, ADJ-700916, TXN-643651, TXN-643748, or
    HAT-FRG-1004 in the provided input previews or query-matched rows"), rows 296 to 407 of 514.
    Drift-notes: a key-like column is one whose values are nine in ten of one id shape (AAA-999999,
    AAA-AAA-9999); every such column is read, so a SKU column counts beside the record-id column.
    Only files whose cited rows total 46 or fewer are read, the rows two side-by-side panels put in a head window (2026-09-14: 31 cited serials on a 239-row register, two called absent); a golden
    citing hundreds of ids or keys with dozens of rows each is the ledger shape of PR6, not this one
    (the first portfolio pass hit 24 such files). A workbook sheet gets the head window only: the note called ADJ-546964 and ADJ-700916 absent at
    rows 254 and 255 of 258, inside a CSV's tail window. The fix is a relay, never a reorder: lay the
    file out in side-by-side panels, or one row per key, so every cited row sits inside the preview;
    a lead block of the rows under review hands the solver the scope decision by file order
    (2026-09-15; PR12).
    Figure arm (2026-09-14): a 57-line measurement report keyed by
    size and point carried no id the golden names, and the golden's sample-read tab typed the size L readings
    from lines 30 to 43; the finding reported "the only size L record is pocket opening 16.7 cm", the one
    line inside the tail. So a row in the hidden middle whose decimal figure of three or more digits the golden
    types into a cell counts as cited too, from five such rows up; a relaid file of 40 lines or fewer is exempt.
    Narrowed 2026-09-15: a typed figure some input already shows inside
    its preview is sourced there and is not counted; the golden's net costs 78.25, 84.5 and 11.85 come from rows
    13, 14 and 25 of a 27-row item status report and only repeat as UNIT_PRICE on transfer lines deep in a
    1,026-row ledger, which the golden never reads for cost.
    """
    cited = {m.group(0) for m in _H8_ID_RE.finditer(_h8_golden_text(folder))}
    typed = _h8_golden_typed_figures(folder)
    if typed and _H8_EXEMPT_VISIBLE:
        # a figure the golden types from a row the platform can see is sourced there, whatever deeper rows repeat it
        typed -= _h8_visible_figures(folder)
    if not cited and not typed:
        return
    for name, rows, tail in _h8_tables(folder):
        n = len(rows)
        if n <= _H8_MIN_ROWS:
            continue
        width = max(len(r) for r in rows)
        outside, cited_rows = [], set()
        for j in range(width):
            vals = [r[j] for r in rows if j < len(r) and r[j]]
            if len(vals) < 20:
                continue
            shapes = {}
            for v in vals:
                if _H8_ID_RE.fullmatch(v):
                    shapes[_h8_shape(v)] = shapes.get(_h8_shape(v), 0) + 1
            if not shapes or max(shapes.values()) < 0.9 * len(vals):
                continue
            col_cited, col_outside = set(), []
            for i, r in enumerate(rows, start=1):
                v = r[j] if j < len(r) else None
                if v in cited:
                    col_cited.add(i)
                    if _H8_HEAD < i <= n - tail:
                        col_outside.append((v, i + 1))
            # each key column is judged on its own: a serial column with 31 cited rows is the
            # account block, while the item-number column beside it is a foreign key that lands
            # on dozens of other accounts' rows (the block escaped the cap
            # only because both columns were pooled); a column where a cited id recurs is that
            # foreign key, and the golden cites it to the master file, not to these rows
            col_ids = {r[j] for i, r in enumerate(rows, start=1) if i in col_cited and j < len(r)}
            if col_outside and len(col_cited) <= _H8_PANEL_CAP and len(col_cited) == len(col_ids):
                cited_rows |= col_cited
                outside.extend(col_outside)
        # figure arm: rows in the hidden middle whose decimal figures the golden re-keys
        fig_rows = []
        if typed and not outside:
            for i, r in enumerate(rows, start=1):
                if not (_H8_HEAD < i <= n - tail):
                    continue
                hit = next((v for v in r if v and _H8_FIG_RE.fullmatch(v) and _h8_fig(v) in typed), None)
                if hit:
                    fig_rows.append((hit, i + 1))
            if len(fig_rows) >= _H8_FIG_MIN_ROWS:
                ex = "; ".join(f"{v} row {i}" for v, i in fig_rows[:6])
                emit("ERROR", f"[H8] {name}: {len(fig_rows)} row(s) in the hidden middle of a {n}-row file carry "
                              f"figures the golden types into its cells (rows 27 to {n - tail + 1} are outside the "
                              f"preview): {ex}. A 57-line measurement report was read as holding one size L "
                              "record and the golden's size L readings called unsourced "
                              "(2026-09-14). Lay the file out in side-by-side panels, or one row per key with the "
                              "readings across columns, so it is 40 lines or fewer (H7)")
        # a handful of cited records is relaid into panels so they sit in the preview; a golden that
        # reads most of a file, or keys with dozens of rows each, is PR6's ledger shape, not this one
        if outside:
            ids = sorted({v for v, _ in outside})
            ex = "; ".join(f"{v} row {i}" for v, i in outside[:6])
            emit("ERROR", f"[H8] {name}: {len(outside)} row(s) for {len(ids)} cited id(s) sit in the hidden middle of a "
                          f"{n}-row sheet (rows 27 to {n - tail + 1} are outside the preview): {ex}. Such rows were "
                          "reported as 'no occurrence in the provided input previews or query-matched rows' "
                          "(2026-09-14). Lay the file out in side-by-side panels, or one "
                          "row per key, so every cited row sits inside the preview; never move the rows under review "
                          "to the top, which hands the solver the scope decision by file order (PR12)")

@check(codes=['H9'], rules=['PRE-PACK'], needs=['inputs'], params=['folder'])
def check_csv_fields_without_commas(folder):
    """No field in an input CSV contains a comma, because the platform splits CSV lines on commas without honouring quotes and reads every column after a quoted comma as shifted.

    Since: 2026-09-15 (a rejection finding, item 1).
    Source: the finding counted 18 fields against a 16-column header on the bill of lading register
    row carrying "Bittner residence, c/o Hilltop Plumbing" and "Water heaters, commercial", and 25
    against 24 on the freight bills row for "Ohlsen residence, c/o Kammerer Plumbing", and warned that
    weight, class, rate and accessorial columns come out shifted; both files were valid quoted CSV.
    Drift-notes: reads every CSV under inputs/ with the csv module and fires on any data field holding a
    comma, whatever the quoting. The remedy is rewording the value without a comma ("Commercial water
    heaters", "Bittner residence c/o Hilltop Plumbing"), never a different delimiter, since a solver's
    parser is not told one. A thousands separator inside a number is a comma too and is written without it.
    """
    import csv as _csv
    inputs = os.path.join(str(folder), "inputs")
    if not os.path.isdir(inputs):
        return
    for name in sorted(os.listdir(inputs)):
        if not name.lower().endswith(".csv"):
            continue
        try:
            with open(os.path.join(inputs, name), encoding="utf-8", errors="ignore", newline="") as fh:
                rows = list(_csv.reader(fh))
        except Exception:
            continue
        if len(rows) < 2:
            continue
        hdr = rows[0]
        hits = [(i + 2, hdr[j] if j < len(hdr) else f"column {j + 1}", v)
                for i, r in enumerate(rows[1:]) for j, v in enumerate(r) if "," in v]
        if not hits:
            continue
        cols = sorted({c for _, c, _ in hits})
        line, col, val = hits[0]
        emit("ERROR", f"[H9] inputs/{name}: {len(hits)} field(s) in {', '.join(cols)} contain a comma (first at line "
                      f"{line}, {col} \"{val}\"); the platform splits CSV lines on commas without honouring quotes and "
                      "reads every later column as shifted (2026-09-15: 18 fields against a 16-column "
                      "header). Reword each value without the comma")

