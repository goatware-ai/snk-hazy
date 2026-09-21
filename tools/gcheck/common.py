"""Shared helpers and regexes used by more than one check module.

One home each for the things the checks used to carry in copies (2026-09-11): the rubric
CSV loader, the input-text extractor, the package-member reader, the generator-string
reader, the sentence and clause splitters and the month table. File parses go through
gcheck/state.py so a run opens each workbook and document once.
"""
import csv
import json
import re
import sys
import zipfile
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from .state import workbook, document  # noqa: E402  (the run's parse-once loaders)


# H1: the programme codename, which the platform's Name Check forbids anywhere in a
# shipped package - content, file names, Office metadata. This desk is Hazy, but it was
# ported from the Geranium desk and still carries Geranium vocabulary through every doc,
# prompt and worked example, so BOTH names are screened: an author echoing a ported
# example leaks the old codename just as fatally as the new one. Defined once here and
# consumed by packaging/hygiene.py, golden_rubric/leakage.py and authorship/package.py,
# which each used to carry their own copy. A false positive costs a pre-submission
# reword; a false negative costs a platform cycle, so the screen stays wide.
# If "Hazy" is not in fact the platform-side codename, drop that alternative here and
# nowhere else. \b would miss HAZY_TASK_CREATION, because "_" is a word character, so
# the lookarounds key on letters: hazy-task, HAZY_TASK and "Hazy" trip, "hazier" does not.
CODENAME_PATTERN = r"geranium|(?<![a-z])hazy(?![a-z])"
CODENAME_RE = re.compile(CODENAME_PATTERN, re.I)
CODENAME_BYTES_RE = re.compile(CODENAME_PATTERN.encode(), re.I)








# R24: the STRICT set - criteria a hard-coded workbook fails outright, because the
# derivation is the thing asserted rather than a clause hanging off a value. A loose
# any-liveness-wording count over-credits: the platform's full-credit completeness
# check reasons that "a solver who hard-codes those exact correct values as typed
# constants still collects the full 5+5", so only criteria such a workbook FAILS
# count. Two tiers are counted separately here.
LIVENESS_STRICT_RE = re.compile(
    r"stored (?:cell )?formulas?|live formulas?|formula derived"
    r"|reach(?:es)? (?:its|their) values?\s+(?:from|through)"
    r"|rather than (?:being )?typed|typed constants?", re.I)






RANGE_KEY_RE = re.compile(
    r"(?:'([^']{1,40})'|\b([A-Za-z_][A-Za-z0-9_]{1,40}))!\$?([A-Z]{1,3})\$?(\d{1,5})(?::\$?([A-Z]{1,3})\$?(\d{1,5}))?")


def _col_num(letters):
    n = 0
    for ch in letters:
        n = n * 26 + ord(ch) - 64
    return n


# R20/R21 (2026-08-20, wamhoff run 1): the oracle judge verifies a criterion by
# grepping CELL VALUES in the deliverable. A figure that lives only in prose, or a
# chain whose figures are scattered over several sheets, flakes.
_YEAR_RE = re.compile(r"^(19|20)\d\d$")


_FIGURE_RE = re.compile(r"\d[\d,]*\.\d+|\d[\d,]{3,}")


# a criterion that names a landing cell (Recovery!H170, 'File Corrections'!A100) is not
# stating 170 or 100 as a figure; the address comes out before the figure/count scans
# (june-price-review run 1, 2026-08-23, where R20/R26 read H170 as a count of 170)
_CELL_REF_RE = re.compile(r"(?:'[^']+'|[A-Za-z_][\w ]*)!\$?[A-Z]{1,3}\$?\d+(?::\$?[A-Z]{1,3}\$?\d+)?")


def _without_cell_refs(text):
    return _CELL_REF_RE.sub(" ", text)


def _solution_cell_values(folder):
    """sheet title -> the set of cell values as a judge would grep them."""
    out = {}
    d = folder / "solution"
    for path in sorted(d.glob("*.xlsx")) if d.is_dir() else []:
        try:
            wb = workbook(path, data_only=True)
        except Exception:
            continue
        for ws in wb.worksheets:
            bag = out.setdefault(f"{path.name}:{ws.title}", set())
            for row in ws.iter_rows():
                for c in row:
                    v = c.value
                    if v is None:
                        continue
                    if isinstance(v, str):
                        # short strings are codes and labels the judge reads whole
                        # (HTS numbers, part numbers); long ones are prose and do not
                        # count as a value the judge can grep
                        if len(v) <= 40:
                            bag.add(v)
                        continue
                    nf = c.number_format or ""
                    dec = nf.count("0") - nf.split(".")[0].count("0") if "." in nf else 0
                    txt = (f"{v * 100:.{max(dec, 0)}f}" if "%" in nf
                           else f"{v:,.{max(dec, 0)}f}")
                    bag.add(txt)
                    bag.add(txt.replace(",", ""))
                    bag.add(repr(v))
    return out


def _solution_raw_values(folder):
    """every cell value as the judge's raw-value tools render it (no number formats)."""
    raw = set()
    d = folder / "solution"
    for path in sorted(d.glob("*.xlsx")) if d.is_dir() else []:
        try:
            wb = workbook(path, data_only=True)
        except Exception:
            continue
        for ws in wb.worksheets:
            for row in ws.iter_rows():
                for c in row:
                    if c.value is not None:
                        v = c.value
                        raw.add(repr(v) if isinstance(v, float) else str(v))
    return raw


# R26 (2026-08-21, task 20 oracle run 1): the oracle judge failed C10 in ALL THREE
# runs and quoted the golden's own footer back at us - the criterion said "18 of them
# short and 31 late" and the workbook counted 28. R20 never saw it because its figure
# regex wants a decimal or four digits, so every COUNT a criterion states (small bare
# integers: how many lines, rows, items, quarters) went unchecked. A count is the
# cheapest thing for the judge to verify and the easiest for a rebuild to leave stale,
# which is exactly the combination that fails 3/3. The same sweep caught C5 (stated 4
# never-acknowledged lines against 3 in the data), C6 (6 against 5) and C26 (12 against
# 11) on the same task.
# letters glued to the digits are an item code (DC300, BU075, Q-26071), not a count
_COUNT_RE = re.compile(r"(?<![A-Za-z\d.,/$-])(\d{1,3})(?![\d.,/%A-Za-z-])")


_MONEY_RE = re.compile(r"\b\d[\d,]*\.\d{2}\b")


def _docx_tables(folder):
    """(path.name, table index, [[cell text, ...], ...]) for every table in solution docx."""
    out = []
    for path in solution_files(folder, {".docx"}):
        try:
            doc = document(path)
        except Exception:
            continue
        for i, t in enumerate(doc.tables):
            out.append((path.name, i, [[c.text.strip() for c in r.cells] for r in t.rows]))
    return out


def rubric_path(folder):
    """The task's rubric CSV: rubric-{task-name}-{uid8}.csv under submissions/,
    rubric-{task-name}.csv anywhere else (2026-08-26). Glob rather than derive
    the name from folder.name, so a folder that does not follow the
    {seq}-{task-name} form still resolves. When none exists yet, guess the
    expected name — UID read from metadata.json — so the "missing" error is
    actionable rather than pointing at a retired form.
    """
    matches = sorted(folder.glob("rubric-*.csv"))
    if matches:
        return matches[0]
    m = re.match(r"^\d+-(.+)$", folder.name)
    task_name = m.group(1) if m else folder.name
    return folder / f"rubric-{task_name}{_rubric_uid_suffix(folder)}.csv"


def _rubric_uid_suffix(folder):
    """"-{first 8 of the Taskboard UID}" for a submissions/ folder, else "".

    The UID lives in metadata.json; a draft carries it null and so falls through
    to "", gaining the suffix only once it is promoted.
    """
    if folder.resolve().parent.name != "submissions":
        return ""
    uid = load_metadata(folder).get("taskboard_uid") or ""
    return f"-{uid[:8]}" if len(uid) >= 8 else ""


def load_metadata(folder):
    """The task's metadata.json as a dict, or {} when absent or unreadable."""
    meta = folder / "metadata.json"
    if not meta.exists():
        return {}
    try:
        return json.loads(meta.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return {}


def load_rows(path, bad=None):
    """(NUMBER, CRITERION, WEIGHT) per non-empty criterion: the one rubric loader.

    A row whose WEIGHT is not numeric is skipped, and appended to `bad` as
    (NUMBER, CRITERION, raw weight) when a list is given (lint reports it as E0).
    """
    rows = []
    with open(path, newline="", encoding="utf-8-sig") as fh:
        for row in csv.DictReader(fh):
            text = (row.get("CRITERION") or "").strip()
            num = (row.get("NUMBER") or "").strip()
            try:
                weight = float((row.get("WEIGHT") or "0").strip())
            except ValueError:
                if bad is not None:
                    bad.append((num, text, (row.get("WEIGHT") or "").strip()))
                continue
            if text:
                rows.append((num, text, weight))
    return rows


def _weights(rows):
    """(positive total, negative total) of a rubric's weights."""
    pos = sum(w for _, _, w in rows if w > 0)
    neg = sum(w for _, _, w in rows if w < 0)
    return pos, neg


def solution_files(folder, exts):
    sol = folder / "solution"
    return sorted(p for p in (sol.glob("*") if sol.is_dir() else []) if p.suffix in exts)


def docx_emdash_stats(path):
    """A6 — em-dash count and word count of a docx's paragraph text."""
    with zipfile.ZipFile(path) as z:
        if "word/document.xml" not in z.namelist():
            return None
        xml = z.read("word/document.xml").decode("utf-8", "ignore")
    text = " ".join(m.group(1) for m in re.finditer(r"<w:t[^>]*>([^<]*)</w:t>", xml))
    text = text.replace("&#8212;", "—").replace("&mdash;", "—")
    return text.count("—"), len(text.split())


def _docx_text(path):
    with zipfile.ZipFile(path) as z:
        if "word/document.xml" not in z.namelist():
            return ""
        xml = z.read("word/document.xml").decode("utf-8", "ignore")
    xml = re.sub(r"</w:p>", "\n", xml)
    return re.sub(r"<[^>]+>", "", xml)


def _xlsx_all_text(path):
    """Every string cell plus every sheet title, as (sheet!cell, text)."""
    out = []
    try:
        wb = workbook(path, data_only=True)
    except Exception:
        return out
    for ws in wb.worksheets:
        out.append((f"{ws.title} (sheet title)", ws.title))
        for row in ws.iter_rows():
            for c in row:
                if isinstance(c.value, str):
                    out.append((f"{ws.title}!{c.coordinate}", c.value))
    return out


def input_texts(folder):
    """(file name, readable text) for every input: csv/txt/md/json bodies, docx paragraph text,
    xlsx string cells one per line, pdf page text (2026-09-14). The one input-text extractor (2026-09-11), memoised on
    the running TaskState."""
    from . import state as _state
    st = _state.current()
    if st is not None and Path(folder) == Path(st):
        return st.input_texts
    return _read_input_texts(folder)


def formula_cells(folder):
    """[(file name, sheet, coordinate, formula, cached value)] over every solution workbook: the
    one cache-recompute pass G2 and A9 both read, memoised on the running TaskState."""
    from . import state as _state
    st = _state.current()
    if st is not None and Path(folder) == Path(st):
        return st.formula_cells
    return _state.TaskState(folder).formula_cells


def _read_input_texts(folder):
    out = []
    ind = folder / "inputs"
    if not ind.is_dir():
        return out
    for f in sorted(ind.iterdir()):
        if f.suffix in {".csv", ".txt", ".md", ".json"}:
            out.append((f.name, f.read_text(encoding="utf-8", errors="ignore")))
        elif f.suffix == ".docx":
            out.append((f.name, _docx_text(f)))
        elif f.suffix == ".xlsx":
            out.append((f.name, "\n".join(t for _, t in _xlsx_all_text(f))))
        elif f.suffix == ".pdf":
            # 2026-09-14 (caraway-credit-review refinement): a date, a name and the tab names the
            # policy and the thread mandate all sat in PDF inputs, and every grounding check read
            # past them (G20 flagged a Secretary of State status date the PDF carries). pypdf's
            # page text joins the corpus; a missing pypdf or an unreadable file adds nothing.
            try:
                import pypdf
                out.append((f.name, "\n".join((pg.extract_text() or "") for pg in pypdf.PdfReader(str(f)).pages)))
            except Exception:
                pass
    return out


def _xlsx_prose(path):
    """Text cells long enough to be prose (not labels), as (sheet!cell, text)."""
    out = []
    try:
        wb = workbook(path, data_only=True)
    except Exception:
        return out
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                v = c.value
                if isinstance(v, str) and len(v) >= 40 and " " in v:
                    out.append((f"{ws.title}!{c.coordinate}", v))
    wb.close()
    return out


_G5_WORDS = {w: i for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen "
    "fifteen sixteen seventeen eighteen nineteen".split())}


_G5_WORDS.update({"twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60,
                  "seventy": 70, "eighty": 80, "ninety": 90})



def package_texts(path, suffixes=(".xlsx", ".docx", ".pptx", ".csv", ".md", ".txt", ".json")):
    """(member, text) for every text-bearing part of a task file: each zip member of an Office
    package (decoded, errors ignored), or the file itself for a plain text file. The one
    package-member reader (H1, N1)."""
    path = Path(path)
    if path.suffix.lower() not in suffixes:
        return
    if path.suffix.lower() in (".xlsx", ".docx", ".pptx"):
        try:
            with zipfile.ZipFile(path) as z:
                for n in z.namelist():
                    yield n, z.read(n).decode("utf-8", "ignore")
        except Exception:
            return
    else:
        try:
            yield str(path), path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return


# The one generator-string needle table (A14, the package sweep). `kind` separates a
# python library, which a reviewer reads as batch construction, from an office suite: a
# LibreOffice re-save is the reviewer's own remedy, so A14 and the sweep never fire on it.
GENERATORS = (
    ("Openpyxl", rb"openpyxl", "library"),
    ("python-docx", rb"python-docx", "library"),
    ("XlsxWriter", rb"xlsxwriter", "library"),
    ("pandas", rb"pandas", "library"),
    ("python", rb"python", "library"),
    ("LibreOffice", rb"libreoffice", "office"),
)


def generator_in(text):
    """The label of the first generator needle found in `text` (str or bytes), or None."""
    if isinstance(text, str):
        text = text.encode("utf-8", "ignore")
    for label, needle, _kind in GENERATORS:
        if re.search(needle, text, re.I):
            return label
    return None


def generator_of(path):
    """(label, kind, application) read off docProps/app.xml and core.xml: the generator named
    there (None when clean), its kind ('library' or 'office'), and the raw <Application> text."""
    try:
        with zipfile.ZipFile(path) as z:
            names = set(z.namelist())
            props = b"".join(z.read(n) for n in ("docProps/app.xml", "docProps/core.xml") if n in names)
    except Exception:
        return None, None, ""
    m = re.search(rb"<Application>([^<]*)</Application>", props)
    application = m.group(1).decode("utf-8", "ignore") if m else ""
    for label, needle, kind in GENERATORS:
        if re.search(needle, props, re.I):
            return label, kind, application
    return None, None, application


# The one sentence splitter and the one clause splitter.
_SENTENCE_END_RE = re.compile(r"(?<=[.!?])\s+")
_SENTENCE_END_CAP_RE = re.compile(r"(?<=[.!?])\s+(?=[\"\u201c'(]?[A-Z])")
_CLAUSE_END_RE = re.compile(r"(?<=[.;])\s+")
_CLAUSE_END_CAP_RE = re.compile(r"(?<=[.;])\s+(?=[A-Z])")


def split_sentences(text, capital=False):
    """Sentences of `text`, split after . ! ? and whitespace; with `capital`, only where the
    next character (after an optional opening quote or paren) is a capital, which keeps
    '2.10 and' and '5,365.50 and' whole."""
    return (_SENTENCE_END_CAP_RE if capital else _SENTENCE_END_RE).split(text)


def split_clauses(text, capital=False):
    """Clauses of `text`, split after . or ; and whitespace (before a capital with `capital`)."""
    return (_CLAUSE_END_CAP_RE if capital else _CLAUSE_END_RE).split(text)


# The one month table.
MONTH_NAMES = ("January", "February", "March", "April", "May", "June", "July", "August",
               "September", "October", "November", "December")
MONTHS_LOWER = tuple(m.lower() for m in MONTH_NAMES)
MONTH_NUM = {m: i for i, m in enumerate(MONTHS_LOWER, 1)}
MONTHS_RE = "|".join(MONTHS_LOWER)          # use with re.I
MONTHS_ABBR_RE = "|".join(MONTHS_LOWER + tuple(m[:3] for m in MONTHS_LOWER))


def month_number(token):
    """1-12 for a month name or its three-letter prefix, any case; None otherwise."""
    t = (token or "").strip().lower().rstrip(".")
    for i, m in enumerate(MONTHS_LOWER, 1):
        if t == m or (len(t) >= 3 and m.startswith(t[:3]) and t == m[:len(t)]):
            return i
    return None
