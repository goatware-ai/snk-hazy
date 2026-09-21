"""Group 3: workbook shape tells the authorship detector reads (A1 A2 A5 A8 A9 A15 A17 F1).

Generated 2026-09-04 from autoeval_check.py; every check body is verbatim.
"""
import csv
import re
import zipfile
import fix_floats
from ..common import formula_cells, solution_files, workbook
from ..core import check, emit, recommend, REPORT, OPTIONS


BUILTIN_DATE_FMTS = set(range(14, 23)) | set(range(27, 37)) | set(range(45, 48)) | set(range(50, 59))


DATE_CODE_RE = re.compile(r"yy|dd|mmm|h:mm|mm/|/mm|\\-mm", re.I)


CELL_RE = re.compile(r'<c\b([^>]*)(?:/>|>(.*?)</c>)', re.S)


@check(codes=['F1'], rules=['LLM-NUM'], needs=['inputs', 'solution'], params=['folder'])
def check_floats(folder):
    """No cached value in any task workbook is a float-repr artifact.

    Source: tools/fix_floats.py scan; the LLM authorship number axis.
    """
    for p in sorted(folder.rglob("*.xlsx")):
        if ".tmp" in p.name:
            continue
        hits = fix_floats.scan(str(p))
        if hits:
            sample = ", ".join(lit for _, lit in hits[:3])
            emit("ERROR", f"[F1] {p.relative_to(folder)}: {len(hits)} float-repr cached values "
                         f"(e.g. {sample}) — run tools/fix_floats.py fix")


# The AI-blue family the Style Guide names as a trained, HIGH-severity rejection signal
# (docs/submission/platform/style-guide-llm-tells.md: "the hex range #1C3557 to #2E4A6B is a
# known, named rejection signal. Reviewers are trained to spot it."), merged with the
# variants docs/submission/platform/creating-input-files.md lists. The navy heuristic below
# (b > g >= r, gap >= 24) covers the whole range; the named set is kept for the message.
AI_BLUE_HEXES = {"1C3557", "1A3A5C", "1F3864", "2E4057", "1E2D56",
                 "1F4E79", "2E75B6", "2E4A6B"}


def _is_navy(rgb):
    r, g, b = (int(rgb[i:i + 2], 16) for i in (0, 2, 4))
    return b > g >= r and b - r >= 24


def blue_fills(path):
    with zipfile.ZipFile(path) as z:
        if "xl/styles.xml" not in z.namelist():
            return []
        styles = z.read("xl/styles.xml").decode("utf-8", "ignore")
    hits = []
    fills = re.search(r"<fills.*?</fills>", styles, re.S)
    for m in re.finditer(r'<(?:fg|bg)Color rgb="(?:FF)?([0-9A-Fa-f]{6})"', fills.group(0) if fills else ""):
        rgb = m.group(1).upper()
        if _is_navy(rgb):
            hits.append(rgb)
    return sorted(set(hits))


def docx_blue_shading(path):
    """Navy shading fills actually used in a docx body (word/document.xml only —
    styles.xml carries Word's latent default heading blues even in hand-made files,
    so scanning it would flag every ordinary document)."""
    with zipfile.ZipFile(path) as z:
        if "word/document.xml" not in z.namelist():
            return []
        xml = z.read("word/document.xml").decode("utf-8", "ignore")
    hits = set()
    for m in re.finditer(r'w:shd\b[^>]*w:fill="([0-9A-Fa-f]{6})"', xml):
        rgb = m.group(1).upper()
        if _is_navy(rgb):
            hits.add(rgb)
    return sorted(hits)


def pptx_blue_fills(path):
    """Named AI-blue solid fills in pptx slide/master content."""
    hits = set()
    with zipfile.ZipFile(path) as z:
        for n in z.namelist():
            if not (n.startswith(("ppt/slides/", "ppt/slideMasters/", "ppt/slideLayouts/"))
                    and n.endswith(".xml")):
                continue
            xml = z.read(n).decode("utf-8", "ignore")
            for m in re.finditer(r'srgbClr val="([0-9A-Fa-f]{6})"', xml):
                rgb = m.group(1).upper()
                if rgb in AI_BLUE_HEXES:
                    hits.add(rgb)
    return sorted(hits)


def date_xf_indexes(styles):
    custom = {}
    for m in re.finditer(r'<numFmt numFmtId="(\d+)" formatCode="([^"]*)"', styles):
        code = re.sub(r'"[^"]*"|\[[^\]]*\]', "", m.group(2))
        custom[int(m.group(1))] = bool(DATE_CODE_RE.search(code))
    xfs = re.search(r"<cellXfs.*?</cellXfs>", styles, re.S)
    out = set()
    for i, m in enumerate(re.finditer(r"<xf\b[^>]*>", xfs.group(0) if xfs else "")):
        fid = re.search(r'numFmtId="(\d+)"', m.group(0))
        fid = int(fid.group(1)) if fid else 0
        if fid in BUILTIN_DATE_FMTS or custom.get(fid):
            out.add(i)
    return out


def datetime_cells(path):
    with zipfile.ZipFile(path) as z:
        if "xl/styles.xml" not in z.namelist():
            return []
        idx = date_xf_indexes(z.read("xl/styles.xml").decode("utf-8", "ignore"))
        hits = []
        for n in z.namelist():
            if not (n.startswith("xl/worksheets/") and n.endswith(".xml")):
                continue
            for m in CELL_RE.finditer(z.read(n).decode("utf-8", "ignore")):
                attrs, inner = m.group(1), m.group(2) or ""
                t = re.search(r' t="([^"]+)"', attrs)
                ref = re.search(r' r="([A-Z]+\d+)"', attrs)
                if t and t.group(1) == "d":
                    hits.append((n, ref.group(1) if ref else "?"))
                    continue
                if t and t.group(1) not in ("n",):
                    continue
                s = re.search(r' s="(\d+)"', attrs)
                if s and int(s.group(1)) in idx and "<v>" in inner:
                    hits.append((n, ref.group(1) if ref else "?"))
        return hits


def paste_walls(path):
    """A5 — statistical-detector driver isolated on one task (runs 1-4): a
    raw-paste sheet dominating the workbook's extracted text fails the chunked
    human-likeness detector. Calibrated on every big solution tab with a known
    detector outcome (Aug 2026): a 1011-row tab at 43% letters and a 429-row tab
    at 27% passed; that task's 884r wall failed at 5% letters (numeric form, run 4)
    and with a ~35-char desc column (runs 1-3); another task's 141-row Settings wall
    failed at 59 chars/row (run 1, detect 0.20). Detector scans solution files only.

    Row gate is 100, not 250: that task's two walls were 141 and 138 rows and slipped
    the old gate entirely. Mean-longest across every big tab with a known PASSING
    outcome: 1011r/8.2, 1028r/16.8, 429r/18.2 and 689r/22.3. Small tabs stay exempt
    by the row gate (a 58-row Repricing tab sits at 37.4 and scored detect 1.00), so
    string length only bites at scale.
    """
    findings = []
    try:
        wb = workbook(path, data_only=True)
    except Exception:
        return findings
    stats = []
    for ws in wb.worksheets:
        chars = letters = nrows = longest_sum = 0
        for row in ws.iter_rows(values_only=True):
            vals = [v for v in row if v is not None and str(v) != ""]
            if not vals:
                continue
            nrows += 1
            row_longest = 0
            for v in vals:
                s = str(v)
                chars += len(s) + 1
                letters += sum(ch.isalpha() for ch in s)
                if isinstance(v, str):
                    row_longest = max(row_longest, len(s))
            longest_sum += row_longest
        stats.append((ws.title, chars, letters, nrows, longest_sum / nrows if nrows else 0))
    wb.close()
    total = sum(s[1] for s in stats) or 1
    for title, chars, letters, nrows, mean_longest in stats:
        share = chars / total
        if nrows < 100 or share <= 0.35:
            continue
        ratio = letters / chars if chars else 0
        where = f'sheet "{title}" ({nrows} rows, {share:.0%} of extracted text)'
        if nrows >= 250 and ratio < 0.15:
            findings.append(("ERROR", f"{where} is a near-letterless data wall ({ratio:.0%} letters) — "
                             "the authorship detector reads these chunks as AI (an earlier task, run 4, detect 0.06); "
                             "move the raw paste to inputs and keep a rollup, or anchor rows with real-word columns"))
        elif mean_longest > 45:
            findings.append(("ERROR", f"{where} repeats a sentence-length text column (mean longest string "
                             f"{mean_longest:.0f} chars/row, pass band 8-23) — a task failed run 1 at 59 "
                             "chars/row over 141 rows (detect 0.20); replace templated reason sentences with "
                             "trade shorthand plus a legend on a params tab, and drop columns the workbook "
                             "duplicates from another tab"))
        elif mean_longest > 25:
            findings.append(("ERROR", f"{where} carries a long text column (mean longest string "
                             f"{mean_longest:.0f} chars/row, pass band 8-23) — desc-style walls failed "
                             "runs 1-3 on one task (detect 0.04-0.08) and run 1 on another (detect 0.20); "
                             "prefer short vendor/branch-style word anchors or a rollup"))
        # A5 dominant-tab signal (2026-08-26, rounds 1 and 3, detect 0.13 twice): a
        # word-ANCHORED register can still sink the detector when one tab
        # carries too much of the extracted fabric. The 792-row stop register sat at
        # 42% letters and mean-longest 17 — inside every per-row band above — yet 39/45
        # chunks read AI, because the tab held 80% of the workbook's text and prose was
        # 5%. No accepted workbook has a tab above 67%. The repair that moved the
        # composition into passing territory (sim 0.04 -> 0.22): drop columns the
        # tab duplicates from another tab via a key (the register's
        # DATE rode on RUN), and add a Working Notes tab of first-person desk prose
        # (an accepted task's device) plus prose note lines on the small tabs.
        elif share > 0.72:
            findings.append(("ERROR", f"{where} dominates the workbook's extracted text — even a "
                             "word-anchored register fails the chunked detector at this share "
                             "(2026-08-26: 80% share scored detect 0.13 twice; the "
                             "accepted maximum is 67%). Drop columns the tab duplicates "
                             "from another tab via a key, and grow prose mass: a Working Notes tab "
                             "in first-person desk register (an accepted task's shape) plus note "
                             "lines on the small tabs"))
    return findings


def _header_tokens(cells):
    return {str(c).strip().upper() for c in cells if c is not None and str(c).strip()}


def _input_extract_headers(folder):
    """(input name, header token set, data row count) for every tabular input."""
    import csv as _csv
    out = []
    d = folder / "inputs"
    for p in sorted(d.iterdir()) if d.is_dir() else []:
        if p.suffix.lower() == ".csv":
            try:
                rows = list(_csv.reader(open(p, newline="", encoding="utf-8", errors="ignore")))
            except Exception:
                continue
            for i, r in enumerate(rows[:10]):
                if len([x for x in r if x.strip()]) >= 4:
                    out.append((p.name, _header_tokens(r), max(0, len(rows) - i - 1)))
                    break
        elif p.suffix.lower() == ".xlsx":
            try:
                wb = workbook(p, data_only=True)
            except Exception:
                continue
            for ws in wb.worksheets:
                n, first = 0, None
                for i, r in enumerate(ws.iter_rows(values_only=True)):
                    vals = [v for v in r if v is not None and str(v).strip()]
                    if first is None and len(vals) >= 4 and sum(isinstance(v, str) for v in vals) >= 4:
                        first = (i, _header_tokens(r))
                    if vals:
                        n += 1
                if first:
                    out.append((f"{p.name}:{ws.title}", first[1], n - first[0] - 1))
            wb.close()
    return out


def input_extract_walls(path, folder):
    """A5, third signal - a VERBATIM input extract carrying too much of the solution's text.

    One task (2026-08-31, detect 0.15, 23 of 27 chunks AI): the solution pasted the
    81-row, 36-month usage CSV whole as a Usage tab. At 81 rows it slipped the
    100-row gate of the two signals above, yet it held 36.5% of the workbook's extracted
    text at 26% letters, and two of the three passages the detector quoted came off it.
    The CSV already ships in the inputs, so the paste adds nothing a reader needs and a
    third of the fabric the detector reads as machine-made. The fix that lifted the chunk
    simulator from 0.29 to 0.64 was an accepted task's device: drop the paste, carry a
    27-row season rollup of typed pivot values, keep every decision formula live on top
    of it.

    Detection is structural, not textural: a solution sheet whose header row matches an
    input file's header (Jaccard >= 0.8) with at least 80% of that input's rows is a
    verbatim extract, and it errors when it holds more than 30% of the extracted text.
    Calibration (2026-08-31 probe, every accepted workbook and every submission): no
    accepted workbook carries a verbatim extract at all (one accepted task deleted its
    Item Data extract on the way to its pass); the failing paste sat at 36.5%; extracts
    that pass the gate today sit at 27.4% (a Receipts tab), 13.4% (a Price Page), 9.6%
    (a Runs tab) and 8% (the same package's Stock and Price Pages). One untested point
    above the bar: a History tab at 66.2%, no platform authorship verdict yet - if it
    passes, raise the bar.
    """
    findings = []
    inputs = [x for x in _input_extract_headers(folder) if x[1]]
    if not inputs:
        return findings
    try:
        wb = workbook(path, data_only=True)
    except Exception:
        return findings
    stats = []
    for ws in wb.worksheets:
        chars = nrows = 0
        first = None
        for i, r in enumerate(ws.iter_rows(values_only=True)):
            vals = [v for v in r if v is not None and str(v) != ""]
            if not vals:
                continue
            nrows += 1
            if first is None and len(vals) >= 4 and sum(isinstance(v, str) for v in vals) >= 4:
                first = _header_tokens(r)
            chars += sum(len(str(v)) + 1 for v in vals)
        stats.append((ws.title, chars, nrows, first))
    wb.close()
    total = sum(s[1] for s in stats) or 1
    for title, chars, nrows, hdr in stats:
        if not hdr or chars / total <= 0.30:
            continue
        for name, toks, n in inputs:
            jacc = len(hdr & toks) / len(hdr | toks)
            if jacc >= 0.8 and nrows >= 0.8 * n:
                findings.append(("ERROR", f'sheet "{title}" ({nrows} rows, {chars / total:.0%} of extracted '
                                 f"text) is a verbatim extract of {name} (header match {jacc:.0%}) - the "
                                 "input already ships the data, and a paste holding over 30% of the "
                                 "solution's text reads as machine-made whatever its row count "
                                 "(2026-08-31, 81 rows at 36.5% scored detect "
                                 "0.15; no accepted workbook carries one). Drop the paste and carry a "
                                 "rollup of the season or period figures the decisions actually use, "
                                 "with the decision formulas live on top of it"))
                break
    return findings


@check(codes=['A15'], rules=['LLM-SHAPE'], needs=['inputs'], params=['folder'])
def check_number_series(folder):
    # A15 (2026-08-26, an LLM-authorship FAIL, detect 0.13): the
    # statistical detector reads input CSVs too, and machine-generated NUMBER SERIES
    # sank the whole package: run-log city miles cycled a strict period-5 sequence
    # [14,16,18,20,22] and hours a period-4 sequence across all 64 city rows with zero
    # variation, and the ticket-amount column held 38 unique values across 792 stops,
    # each repeating ~20-28 times ("near-uniform programmatic distribution inconsistent
    # with real invoice data"). Two mechanical signals, probed portfolio-wide before
    # coding (2026-08-26: zero hits outside the failing originals): (a) a numeric
    # column that repeats a short pattern (period >= 3, >= 3 distinct values) exactly,
    # whole-column or within any low-cardinality grouping column - period-1/2 is
    # excluded because constant-within-group ID columns and zero columns are honest;
    # (b) an amount-like money column (header says amount/total/charge, not unit/rate,
    # which legitimately repeat per catalog item) of 300+ rows with 10% or fewer unique
    # values. Fix by regenerating the data with realistic variation, preserving every
    # planted count and band so the golden's story survives the retune (R26 checks the
    # counts).
    """No input CSV column repeats a strict short cycle or holds a near-uniform amount distribution.

    Since: 2026-08-26 (detect 0.13).
    Source: the LLM authorship statistical detector.
    """
    def _a15_cycles(vals, kmax=8):
        n = len(vals)
        for k in range(3, kmax + 1):
            if n >= 3 * k and len(set(vals[:k])) >= 3 \
                    and all(vals[i] == vals[i % k] for i in range(n)):
                return k
        return 0

    def _a15_isnum(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    _a15_amt = re.compile(r"amount|total|dollars|ext(?:ended)?\b|charge|invoice|ticket", re.I)
    _a15_unit = re.compile(r"unit|each|rate|per\b", re.I)
    for p_ in (sorted((folder / "inputs").glob("*.csv")) if (folder / "inputs").is_dir() else []):
        try:
            rows_ = list(csv.reader(p_.open(encoding="utf-8-sig")))
        except Exception:
            continue
        if len(rows_) < 20:
            continue
        hdr_, data_ = rows_[0], [r for r in rows_[1:] if any(c.strip() for c in r)]
        cols_ = {i: [r[i].strip() for r in data_ if i < len(r) and r[i].strip()]
                 for i in range(len(hdr_))}
        numcols_ = [i for i in cols_ if cols_[i] and len(set(cols_[i])) > 1
                    and sum(_a15_isnum(v) for v in cols_[i]) >= 0.8 * len(cols_[i])]
        groupcols_ = [i for i in cols_ if i not in numcols_ and 1 < len(set(cols_[i])) <= 12]
        for i in numcols_:
            vals_ = cols_[i]
            hits_ = []
            k_ = _a15_cycles(vals_)
            if k_:
                hits_.append(f"whole column repeats a period-{k_} sequence over {len(vals_)} rows")
            for g_ in groupcols_:
                seqs_ = {}
                for r in data_:
                    if len(r) > max(i, g_) and r[i].strip():
                        seqs_.setdefault(r[g_].strip(), []).append(r[i].strip())
                for gv_, seq_ in seqs_.items():
                    k_ = _a15_cycles(seq_) if len(seq_) >= 24 else 0
                    if k_:
                        hits_.append(f"rows where {hdr_[g_]}={gv_} repeat a period-{k_} "
                                     f"sequence over {len(seq_)} rows")
                        break
            if hits_:
                emit("ERROR", f"[A15] inputs/{p_.name}: column {hdr_[i]!r} {hits_[0]} with zero "
                              "variation - the authorship detector calls strict cycling "
                              "machine-generated, not a real log (2026-08-26, "
                              "detect 0.13). Regenerate with realistic jitter, "
                              "preserving the planted counts and bands")
                continue
            dec2_ = sum(1 for v in vals_ if "." in v and len(v.split(".")[-1]) == 2)
            if (len(vals_) >= 300 and dec2_ >= 0.5 * len(vals_) and _a15_amt.search(hdr_[i])
                    and not _a15_unit.search(hdr_[i])
                    and len(set(vals_)) / len(vals_) <= 0.10):
                emit("ERROR", f"[A15] inputs/{p_.name}: column {hdr_[i]!r} holds only "
                              f"{len(set(vals_))} unique values across {len(vals_)} rows - a "
                              "near-uniform repeating amount distribution reads as programmatic, "
                              "not real invoice data (2026-08-26). "
                              "Regenerate the amounts with a realistic spread, preserving each "
                              "row's price band")


@check(codes=['A1'], rules=['LLM-PKG'], needs=['inputs', 'solution'], params=['folder'])
def check_blue_fills(folder):
    # A1 applies to INPUT files as well as the solution (style guide: "Applies To:
    # Input files, Output files"), and to Word shading and pptx fills, not just xlsx.
    """No shipped file uses a fill, shading or slide colour in the AI-blue family.

    Source: docs/submission/platform/style-guide-llm-tells.md (#1C3557 to #2E4A6B, HIGH); inputs and outputs alike.
    """
    inp_dir = folder / "inputs"
    a1_xlsx = solution_files(folder, {".xlsx"}) + \
        (sorted(inp_dir.glob("*.xlsx")) if inp_dir.is_dir() else [])
    for p in a1_xlsx:
        blues = blue_fills(p)
        if blues:
            named = sorted(set(blues) & AI_BLUE_HEXES)
            tag = (f" (including named rejection hex {', '.join(named)})" if named else "")
            emit("ERROR", f"[A1] {p.relative_to(folder)}: blue-family fill(s) {', '.join(blues)}{tag} — "
                         "the AI-blue range #1C3557–#2E4A6B is a named, trained-for rejection "
                         "signal (docs/submission/platform/style-guide-llm-tells.md, HIGH); use gray "
                         "(D9D9D9/F2F2F2), industry-appropriate colors, or warm accents")
    a1_docx = solution_files(folder, {".docx"}) + \
        (sorted(inp_dir.glob("*.docx")) if inp_dir.is_dir() else [])
    for p in a1_docx:
        blues = docx_blue_shading(p)
        if blues:
            emit("ERROR", f"[A1] {p.relative_to(folder)}: navy table/paragraph shading "
                         f"{', '.join(blues)} in the document body — Word/PDF table fills in "
                         "the AI-blue family are the same HIGH-severity tell as Excel header "
                         "fills (docs/submission/platform/style-guide-llm-tells.md)")
    for p in solution_files(folder, {".pptx"}) + \
            (sorted(inp_dir.glob("*.pptx")) if inp_dir.is_dir() else []):
        blues = pptx_blue_fills(p)
        if blues:
            emit("ERROR", f"[A1] {p.relative_to(folder)}: AI-blue fill(s) {', '.join(blues)} in "
                         "slide content — blue-on-white slide masters with no other palette "
                         "variation are a HIGH-severity tell (docs/submission/platform/style-guide-llm-tells.md)")


@check(codes=['A2', 'A5'], rules=['LLM-PKG', 'LLM-SHAPE'], needs=['solution'], params=['folder'])
def check_datetime_and_walls(folder):
    """A solution workbook stores dates as plain text and carries no raw-paste data wall, long text column, dominant tab or verbatim input extract.

    Codes:
      A2  no datetime-formatted cells (a date is stored as plain text in the source format)
      A5  no paste wall: a big tab that is near-letterless, repeats a sentence-length column, holds over 72% of the extracted text, or is a verbatim input extract over 30% of it
    Since: runs 1-4 on one task and run 1 on another (Aug 2026); 2026-08-26; 2026-08-31.
    Source: the LLM authorship statistical detector.
    """
    for p in solution_files(folder, {".xlsx"}):
        rel = p.relative_to(folder)
        dcells = datetime_cells(p)
        if dcells:
            sample = ", ".join(str(c[1]) for c in dcells[:5])
            emit("ERROR", f"[A2] {rel}: {len(dcells)} datetime-formatted cell(s) (e.g. {sample}) — "
                         "extract as '2025-12-02 00:00:00'; store dates as plain text in the source format")
        for sev, msg in paste_walls(p):
            emit(sev, f"[A5] {rel}: {msg}")
        for sev, msg in input_extract_walls(p, folder):
            emit(sev, f"[A5] {rel}: {msg}")


@check(codes=['A8'], rules=['LLM-NUM'], needs=['solution'], params=['folder'])
def check_hidden_precision(folder):
    """No stored value carries more precision than its own number format shows.

    The LLM-authorship reviewer reads CACHED VALUES, not the formatted display, and reads
    a long tail of decimals as programmatic computation. It failed a task (2026-08-21,
    detect 1.00 / llm-only 0.50 / combined 0.85) on six cells: five MARGIN AT RISK values
    like 199.7626667 and 682.554687 behind a #,##0.00 format, and a briefing total of
    2121.543045 behind a currency format. fix_floats does not catch these: they are not
    float-repr tails, they are honest unrounded arithmetic that the format hides.

    Fix at the source, not with formatting: round the money the system would round (a
    unit margin is cents, a per-month usage figure is two places), so the stored value is
    the value a reader sees. That fix moved one pinned figure by ten cents and
    left every other answer untouched.
    """
    d = folder / "solution"
    if not d.is_dir():
        return
    for path in sorted(d.glob("*.xlsx")):
        try:
            wb = workbook(path, data_only=True)
        except Exception:
            continue
        hits = []
        for ws in wb.worksheets:
            for row in ws.iter_rows():
                for c in row:
                    v = c.value
                    if not isinstance(v, float) or isinstance(v, bool):
                        continue
                    nf = c.number_format or ""
                    if "." not in nf or "E" in nf.upper():
                        continue
                    shown = len(nf.split(".")[-1].split(";")[0].strip("%\"' "))
                    if "%" in nf:
                        shown += 2          # a percent format scales the stored value
                    if shown and abs(round(v, shown) - v) > 10 ** -(shown + 4):
                        hits.append(f"{ws.title}!{c.coordinate}={v!r} shown to {shown}dp")
        if hits:
            emit("ERROR", f"[A8] {path.name}: {len(hits)} cells store more precision than their "
                          f"format shows (e.g. {'; '.join(hits[:3])}) — the authorship reviewer "
                          "reads cached values, not the display, and reads the tail as "
                          "programmatic computation (a FAIL 2026-08-21, combined 0.85). "
                          "Round at the source with ROUND() so the stored figure is the figure a "
                          "reader sees; formatting alone does not fix it")


_REF_RE = re.compile(r"^'?([A-Za-z][A-Za-z0-9 _]*)'?!\$?([A-Z]{1,3})\$?(\d+)$"
                     r"|^\$?([A-Z]{1,3})\$?(\d+)$")


_RANGE_RE = re.compile(r"^=SUM\(\$?([A-Z]{1,3})\$?(\d+):\$?([A-Z]{1,3})\$?(\d+)\)$", re.I)


_ARITH_RE = re.compile(r"^=[A-Za-z0-9$!'._ ]+(?:[-+*/][A-Za-z0-9$!'._ ]+)+$")


_HAS_FN_RE = re.compile(r"\b(IF|SUM|COUNT|MIN|MAX|ROUND|AVERAGE|N|SUMIF|SUMIFS|VLOOKUP|"
                        r"INDEX|MATCH|SUMPRODUCT|TEXT|IFERROR)\s*\(", re.I)


@check(codes=['A9'], rules=['LLM-NUM'], needs=['solution'], params=['folder'])
def check_stored_arithmetic(folder):
    """Every cached value is what the cell's own formula computes.

    The build injects cached values into the sheet XML because openpyxl leaves them
    empty, and it injects the ROUNDED money figure while the formula itself is
    unrounded. The file therefore ships one number and computes another the moment
    anyone opens it with fullCalcOnLoad set. One task (2026-08-21) shipped
    `=E22*Params!C16` cached at 11,217.40 against a true 11,217.395, and a cell
    downstream subtracted two such cells and moved a rubric-pinned figure by a cent:
    1,097.90 in the rubric, in the prose and in the cache, 1,097.89 on recalculation.
    The oracle failed that criterion.

    Fix at the source with ROUND(...,2) in the formula, never by adjusting the cache,
    so the stored figure, the recalculated figure and the criterion agree. Only pure
    arithmetic, plain references and SUM over a column are evaluated here; anything
    with a conditional in it is left alone.
    """
    from itertools import groupby
    # one walk over the formula cells, shared with G2 (common.formula_cells)
    for fname, cells in groupby(formula_cells(folder), key=lambda t: t[0]):
        path = folder / "solution" / fname
        vwb = workbook(path, data_only=True)

        def cached(sheet, ref):
            m = _REF_RE.match(ref.strip())
            if not m:
                raise ValueError(ref)
            if m.group(1):
                if m.group(1) not in vwb.sheetnames:
                    raise ValueError(ref)
                return vwb[m.group(1)][m.group(2) + m.group(3)].value
            return vwb[sheet][m.group(4) + m.group(5)].value

        bad, soft = [], []
        for _fname, title, coord, f, here in cells:
            if not isinstance(here, (int, float)) or isinstance(here, bool):
                continue
            got = None
            rng = _RANGE_RE.match(f)
            try:
                if rng and rng.group(1) == rng.group(3):
                    col = rng.group(1)
                    got = sum(float(cached(title, f"{col}{r}") or 0)
                              for r in range(int(rng.group(2)), int(rng.group(4)) + 1))
                elif _HAS_FN_RE.search(f):
                    continue
                elif _ARITH_RE.match(f):
                    expr = ""
                    for tok in re.split(r"([-+*/])", f[1:]):
                        t = tok.strip()
                        if t in "+-*/":
                            expr += t
                        else:
                            expr += repr(float(cached(title, t)))
                    got = eval(expr)          # arithmetic over cached numbers only
                elif _REF_RE.match(f[1:].strip()):
                    got = float(cached(title, f[1:]))
            except Exception:
                continue
            if got is None:
                continue
            gap = abs(got - float(here))
            if gap <= 1e-9 * max(1.0, abs(got)):
                continue
            note = (f"{title}!{coord} {f} stores {here!r} "
                    f"but computes {round(got, 6)!r}")
            # a tenth of a cent is the line: below it the display cannot move,
            # at or above it a money figure can, and so can anything downstream
            (bad if gap >= 5e-4 else soft).append(note)
        if bad:
            emit("ERROR", f"[A9] {path.name}: {len(bad)} cells store a value their own formula "
                          f"does not reproduce ({'; '.join(bad[:3])}) — the workbook changes on "
                          "open, and a rubric figure pinned to the stored value moves with it "
                          "(a rebate-given-up figure went 1,097.90 to 1,097.89 and the oracle "
                          "failed the criterion). Round inside the formula, not in the cache")
        if soft:
            emit("ERROR", f"[A9] {path.name}: {len(soft)} cells recompute a hair off their stored "
                         f"value ({soft[0]}) — under a tenth of a cent, so no display moves, but "
                         "a cell that subtracts two of them can still land on the wrong cent")


@check(codes=['A17'], rules=['LLM-PKG'], needs=['solution'], params=['folder'])
def check_caches(folder):
    """Every formula cell carries exactly one cached <v>.

    Since: 2026-08-31 (a reviewer) for the multi-<v> case; empty caches since the first oracle misreads.
    Source: reviewer; judges misread empty caches as typed.
    Drift-notes: --no-caches skips it; shared formulas are legal OOXML (fenced 2026-09-02).
    """
    skip = OPTIONS["skip_caches"]
    if skip:
        print("        skipped (--no-caches)")
        return
    import re as _re
    import zipfile as _zf
    # a formula cell is cached if it carries a non-empty <v>, or an empty <v>
    # on a t="str" cell (a legitimate empty-string result)
    # Both halves are fenced with (?!</c>) so a cell can never swallow the cells after
    # it. Without the fence the <f ...>...</f> branch matched a SHARED formula's
    # self-closing <f t="shared" si="0"/> on its opening bracket and then ran forward to
    # the next real </f> several cells away, so every shared formula was reported as a
    # multi-<v> cell (A17). openpyxl writes each formula out in full and never emits a
    # shared one, so the bug only surfaced once workbooks started coming back from a
    # real Excel save (2026-09-02); shared formulas are correct OOXML, not a defect.
    cell_pat = _re.compile(
        rb'<c ([^>]*?)>((?:<f[ >](?:(?!</c>).)*?</f>|<f[^>]*/>)(?:(?!</c>).)*?)(?=</c>)',
        _re.S)
    for p in solution_files(folder, {".xlsx"}):
        try:
            with _zf.ZipFile(p) as z:
                nf = nv = nmulti = 0
                for name in z.namelist():
                    if name.startswith("xl/worksheets/") and name.endswith(".xml"):
                        for attrs, inner in cell_pat.findall(z.read(name)):
                            nf += 1
                            if len(_re.findall(rb"<v[ >]|<v/>", inner)) > 1:
                                nmulti += 1
                            if _re.search(rb"<v>[^<]", inner):
                                nv += 1
                            elif (b"<v>" in inner or _re.search(rb"<v\s*/>", inner)) and b't="str"' in attrs:
                                nv += 1
            if nf and nv < nf:
                emit("ERROR", f"{p.relative_to(folder)}: {nf - nv} of {nf} formula cells have no "
                             "cached <v> — judges misread empty caches; open the workbook in a "
                             "spreadsheet app and save to recalculate before zipping")
            if nmulti:
                # A17 (2026-08-31, a reviewer): a cell holding more than one <v> is
                # malformed OOXML (openpyxl reads the first and Excel repairs the file, so no
                # loader catches it). Cause: a cache injector appending a value without
                # stripping the empty <v></v> openpyxl writes after <f>. Exactly one <v> per
                # formula cell.
                emit("ERROR", f"[A17] {p.relative_to(folder)}: {nmulti} of {nf} formula cells "
                             "carry more than one cached-value <v> element — malformed OOXML; "
                             "rewrite each cell to exactly one <v> holding the computed value")
        except Exception as e:
            emit("ERROR", f"{p.relative_to(folder)}: cache scan failed ({e}); verify caches manually")
