"""Group 2: answer leakage and project vocabulary in shipped files (DATA-LEAK, PRE-NAME).

Generated 2026-09-04 from autoeval_check.py; every check body is verbatim.
"""
import os
import re
import zipfile
from pathlib import Path
from ..common import load_rows, package_texts, rubric_path, workbook, CODENAME_RE
from ..core import check, emit, recommend, REPORT, OPTIONS


@check(codes=['L1'], rules=['DATA-LEAK'], needs=['inputs', 'solution'], params=['folder'])
def check_leaked_enumeration(folder):
    """No input paragraph enumerates manufacturers across the golden's answer set.

    A leakage verdict (2026-08-24, ANSWER_LEAKED): RFI Question 8 named every
    approved substitute across six manufacturers in one parenthetical, handing the
    solver the complete non-compliant-to-replacement map the task exists to derive.
    Every other input carried one vendor's own facts and passed as raw data. The
    mechanical signature is cross-vendor concentration: a single input-docx paragraph
    naming four or more of the manufacturers the solution tracks. An approval or
    ruling document may rule on categories and procedure; the moment it enumerates
    the chosen products, it is the answer key. Note that a legitimate roll-up
    paragraph can exist; read every hit.
    """
    d = folder / "solution"
    inp = folder / "inputs"
    if not (d.is_dir() and inp.is_dir()):
        return
    names = set()
    for path in sorted(d.glob("*.xlsx")):
        try:
            wb = workbook(path, data_only=True)
        except Exception:
            continue
        for ws in wb.worksheets:
            header_cols = {}
            for row in ws.iter_rows(values_only=True):
                if not header_cols:
                    header_cols = {i for i, h in enumerate(row) if isinstance(h, str)
                                   and re.search(r"manufacturer|vendor|supplier", h, re.I)}
                    continue
                for i in header_cols:
                    v = row[i] if i < len(row) else None
                    if isinstance(v, str):
                        w = v.split()[0] if v.split() else ""
                        if len(w) > 3 and w[0].isupper() and w.isalpha():
                            names.add(w)
        wb.close()
    if len(names) < 4:
        return
    for path in sorted(inp.glob("*.docx")):
        try:
            with zipfile.ZipFile(path) as z:
                xml = z.read("word/document.xml").decode("utf-8", "replace")
        except Exception:
            continue
        for para in xml.split("</w:p>"):
            text = re.sub(r"<[^>]+>", " ", para)
            hits = {n for n in names if re.search(rf"\b{n}\b", text)}
            if len(hits) >= 4:
                emit("ERROR", f"[L1] inputs/{path.name}: one paragraph names {len(hits)} of the "
                             f"manufacturers the solution tracks ({', '.join(sorted(hits)[:6])}) — "
                             "a leakage verdict (ANSWER_LEAKED, 2026-08-24) came from "
                             "exactly this shape, an RFI answer enumerating every approved "
                             "substitute. Read the paragraph: rulings on categories and procedure "
                             "are fine, an enumeration of the chosen products is the answer key")


# L3 (2026-08-31, an AutoEval run, ANSWER_LEAKED): a memo
# rule that names the entity AND its verdict. Wessel memo rule 3 read "Vollintine already
# orders above its floor every time and stays exactly as it is", and the prompt's own ask
# ("any vendor that should stay as it is, said plainly with the why") was thereby answered
# verbatim, vendor and reason both, with no look at the history. Rules may set the test
# (weekly floor, biweekly ceiling); the moment an input applies the test to a named entity
# whose stay/no-change verdict a criterion scores, it is the answer key. Signature: a
# positive criterion carrying a stay verdict on a capitalised entity, and one input-docx
# paragraph carrying that entity name beside a stay verdict.
_L3_STAY_RE = re.compile(
    r"\bstays?\s+(?:exactly\s+)?(?:as\s+(?:it|they)\s+(?:is|are)|unchanged|the\s+same|put|untouched)"
    r"|\bno\s+change\b|\bunchanged\b|\buntouched\b|\bleft\s+(?:exactly\s+)?as\s+(?:it|they)\s+(?:is|are)",
    re.I)


_L3_STOP = {"The", "Any", "Every", "Each", "That", "This", "Those", "These", "Its", "Their"}


@check(codes=['L3'], rules=['DATA-LEAK'], needs=['inputs', 'rubric'], params=['folder'])
def check_leaked_stay_verdict(folder):
    """No input paragraph hands over an entity's stay or no-change verdict that a criterion scores."""
    inp = folder / "inputs"
    path = rubric_path(folder)
    if not (inp.is_dir() and path.exists()):
        return
    rows = load_rows(path)
    targets = {}
    for num, text, weight in rows:
        if weight <= 0 or not _L3_STAY_RE.search(text):
            continue
        for w in re.findall(r"\b([A-Z][a-z]{3,})(?:'s)?\b", text):
            if w not in _L3_STOP:
                targets.setdefault(w, num)
    if not targets:
        return
    for path in sorted(inp.glob("*.docx")):
        try:
            with zipfile.ZipFile(path) as z:
                xml = z.read("word/document.xml").decode("utf-8", "replace")
        except Exception:
            continue
        for para in xml.split("</w:p>"):
            text = re.sub(r"<[^>]+>", " ", para)
            if not _L3_STAY_RE.search(text):
                continue
            for name, num in targets.items():
                if re.search(rf"\b{name}\b", text):
                    snippet = re.sub(r"\s+", " ", text).strip()[:140]
                    emit("ERROR", f"C{num} [L3] inputs/{path.name} hands over the stay verdict this "
                                  f"criterion scores: a paragraph names {name} beside a stay/no-change "
                                  f"verdict ({snippet!r}) - the answer-leakage check returned "
                                  "ANSWER_LEAKED on exactly this "
                                  "(2026-08-31: 'Vollintine already orders above its floor every time "
                                  "and stays exactly as it is'). Let the input state the rule and "
                                  "leave the named application of it to the solver")
                    break


# N1 (2026-08-26, docs/submission/platform/creating-input-files.md section 4 + the in-app Name
# Check in docs/submission/platform/task-lifecycle.md): input and solution files are ordinary
# workplace documents and must not reference the project or the evaluation anywhere —
# content, file names, or document metadata. audit_task's canary already sweeps
# the programme codename; this covers the wider vocabulary the doc names, plus the file-naming
# tells from docs/submission/platform/style-guide-llm-tells.md (a file named for its category
# or AI status — golden_solution.xlsx, ai_output.pptx — is a HIGH tell checked before
# the file is even opened). Content tokens are chosen for near-zero false-positive
# risk in trade documents: "task", "eval" and "benchmark" are legitimate business
# words and are deliberately left out of the content scan.
_N1_CONTENT_RE = re.compile(
    r"golden[ _-]solution|\brubric\b|auto[- ]?eval\b|\bgdpval\b|\bas an ai\b|"
    r"ai[- ]generated|large language model|\bgrading criteri", re.I)


_N1_NAME_RE = re.compile(
    r"golden|ai[_-]output|model[_-]response|ai[_-]generated|deliverable|"
    r"_final_v\d+_final|_final_final|^prompt\b", re.I)


_H1_SUFFIXES = (".xlsx", ".docx", ".md", ".csv", ".txt")     # what the audit_task sweep reads
_H1_CODENAME_RE = CODENAME_RE    # common.py owns the pattern (Hazy)


@check(codes=['N1', 'H1'], rules=['PRE-NAME'], needs=['inputs', 'prompt', 'rubric', 'solution'], params=['folder'])
def check_meta_references(folder):
    """No shipped file references the project, the evaluation or AI generation anywhere, and the programme codename appears in no file of the task folder, metadata included.

    Codes:
      N1  no input or solution file carries project/eval vocabulary in its content, XML parts or name, and no file name reads as a category or AI-output label
      H1  the programme codename appears in no file of the folder (every member of every Office package, every text file)
    Since: N1 2026-08-26 (creating-input-files.md section 4 and the in-app Name Check); H1 the audit_task canary.
    Source: the platform's Name Check; docs/submission/platform/creating-input-files.md; style-guide-llm-tells.md.
    Drift-notes: H1 is computed from this check's single pass over the folder since 2026-09-11; check_hygiene
    emits H2-H5 and tools/audit_task.py standalone still prints the canary itself.
    """
    root = str(folder)
    # one walk over the folder: every file is read once, its members feeding both codes
    for r, _dirs, fs in os.walk(root):
        for f in sorted(fs):
            if f == "feedback-log.md":
                continue      # quotes historical defects verbatim; not a deliverable
            p = os.path.join(r, f)
            path = Path(p)
            office = path.suffix.lower() in (".xlsx", ".docx", ".pptx")
            members = list(package_texts(path)) if path.suffix.lower() in _H1_SUFFIXES + (".pptx", ".json") else []
            if path.suffix.lower() in _H1_SUFFIXES:
                for n, t in members:
                    if _H1_CODENAME_RE.search(t):
                        emit("ERROR", f"[H1] CANARY {p} ({n})")
            try:
                sub = path.relative_to(folder).parts[0]
            except ValueError:
                sub = None
            if sub not in ("inputs", "solution") or path.parent != folder / sub:
                continue
            if _N1_NAME_RE.search(path.stem):
                emit("ERROR", f"[N1] {sub}/{path.name}: file name reads as a category or AI-output "
                             "label — file names are checked before the file is opened, and a "
                             "'golden solution'-class name is a HIGH tell "
                             "(docs/submission/platform/style-guide-llm-tells.md). Name it the way a "
                             "practitioner names a real deliverable")
            for member, text in members:
                if office and not member.endswith((".xml", ".rels")):
                    continue
                if not office:
                    member = path.name
                m = _N1_CONTENT_RE.search(text)
                if m:
                    emit("ERROR", f"[N1] {sub}/{path.name} ({member}): contains "
                                 f"{m.group(0)!r} — shipped files must not reference the "
                                 "project, the rubric, or AI generation anywhere, including "
                                 "document metadata (docs/submission/platform/creating-input-files.md "
                                 "section 4: an eval reference is both an authenticity tell "
                                 "and a form of leakage)")
                    break


@check(codes=['L2'], rules=['DATA-LEAK'], needs=['inputs', 'solution'], params=['folder'])
def check_hidden_content(folder):
    """No answer content hides where a visible-page read never shows it.

    docs/submission/platform/creating-input-files.md section 4: check hidden worksheet tabs,
    hidden/filtered rows and columns, cell comments and tracked changes, document
    properties, and slide speaker notes — LLM assistance makes stray content in these
    places more likely, and none of it is visible on the page the builder proofread.
    Solution files are held to the same bar for comments/tracked changes/hidden sheets
    (a deliverable carrying revision residue is not client-ready and the oracle's
    judges read every tab they can see, hidden or not).
    """
    for sub in ("inputs", "solution"):
        d = folder / sub
        for p in (sorted(d.glob("*.xlsx")) if d.is_dir() else []):
            try:
                with zipfile.ZipFile(p) as z:
                    names = set(z.namelist())
                    wb_xml = z.read("xl/workbook.xml").decode("utf-8", "ignore") \
                        if "xl/workbook.xml" in names else ""
                    hidden_sheets = re.findall(
                        r'<sheet [^>]*name="([^"]+)"[^>]*state="(?:hidden|veryHidden)"', wb_xml) + \
                        re.findall(
                        r'<sheet [^>]*state="(?:hidden|veryHidden)"[^>]*name="([^"]+)"', wb_xml)
                    comment_parts = [n for n in names
                                     if re.search(r"xl/(?:comments|threadedComments/)", n)]
                    hidden_rows = 0
                    for n in names:
                        if n.startswith("xl/worksheets/") and n.endswith(".xml"):
                            sheet = z.read(n).decode("utf-8", "ignore")
                            hidden_rows += len(re.findall(r'<(?:row|col) [^>]*hidden="(?:1|true)"', sheet))
            except Exception:
                continue
            if hidden_sheets:
                emit("ERROR", f"[L2] {sub}/{p.name}: hidden sheet(s) {', '.join(hidden_sheets[:4])} — "
                             "hidden tabs are the first place the leakage audit looks "
                             "(docs/submission/platform/creating-input-files.md section 4); unhide and "
                             "review, then delete or surface the content")
            if hidden_rows:
                emit("ERROR", f"[L2] {sub}/{p.name}: {hidden_rows} hidden row(s)/column(s) — "
                             "hidden or filtered rows carry content the visible page never "
                             "shows; review every one for leaked answers, then unhide or delete")
            if comment_parts:
                emit("ERROR", f"[L2] {sub}/{p.name}: cell comments part present "
                             f"({comment_parts[0]}) — comments and notes are a leakage hiding "
                             "place and revision residue; strip them before zipping")
        for p in (sorted(d.glob("*.docx")) if d.is_dir() else []):
            try:
                with zipfile.ZipFile(p) as z:
                    names = set(z.namelist())
                    doc = z.read("word/document.xml").decode("utf-8", "ignore") \
                        if "word/document.xml" in names else ""
                    tracked = len(re.findall(r"<w:(?:ins|del)\b", doc))
                    has_comments = "word/comments.xml" in names and \
                        "<w:comment " in z.read("word/comments.xml").decode("utf-8", "ignore")
            except Exception:
                continue
            if tracked:
                emit("ERROR", f"[L2] {sub}/{p.name}: {tracked} tracked change(s) in the body — "
                             "tracked changes and revision history are a leakage hiding place; "
                             "accept/reject all and strip before zipping")
            if has_comments:
                emit("ERROR", f"[L2] {sub}/{p.name}: Word comments present — strip them before "
                             "zipping (docs/submission/platform/creating-input-files.md section 4)")
    # Speaker notes: an INPUT deck's notes are a leakage hiding place; a solution
    # deck's notes are legitimate talking points (style guide) and are not flagged.
    inp = folder / "inputs"
    for p in (sorted(inp.glob("*.pptx")) if inp.is_dir() else []):
        try:
            with zipfile.ZipFile(p) as z:
                noted = []
                for n in z.namelist():
                    if n.startswith("ppt/notesSlides/") and n.endswith(".xml"):
                        text = re.sub(r"<[^>]+>", "", z.read(n).decode("utf-8", "ignore")).strip()
                        if len(text) > 40:
                            noted.append(n)
        except Exception:
            continue
        if noted:
            emit("ERROR", f"[L2] inputs/{p.name}: {len(noted)} notes slide(s) carry text — "
                         "speaker notes in an input deck are a leakage hiding place; review "
                         "and strip (docs/submission/platform/creating-input-files.md section 4)")


@check(codes=['T1'], rules=['DATA-LEAK'], needs=['folder', 'inputs', 'solution'], params=['folder'])
def check_tell_log(folder):
    """A tell log is a standalone file, never inside the shipped packages.

    docs/submission/platform/creating-input-files.md section 6: create a tell log only when
    tells were found and fixed, keep it as its own file, and never place it inside an
    input file or embed it as a tab, comment, or note within any deliverable — no meta
    content may cross-contaminate the task.
    """
    tell_re = re.compile(r"tell[-_ ]?log", re.I)
    for sub in ("inputs", "solution"):
        d = folder / sub
        for p in (sorted(d.iterdir()) if d.is_dir() else []):
            if tell_re.search(p.name):
                emit("ERROR", f"[T1] {sub}/{p.name}: a tell log must never ship inside the "
                             "input or solution package — keep it as a standalone file "
                             "outside both zips (docs/submission/platform/creating-input-files.md "
                             "section 6)")
    for z_path in sorted(folder.glob("*.zip")):
        try:
            with zipfile.ZipFile(z_path) as z:
                for n in z.namelist():
                    if tell_re.search(n):
                        emit("ERROR", f"[T1] {z_path.name}: contains {n} — a tell log must "
                                     "never ship inside a submitted zip")
        except Exception:
            continue


# L4 (2026-09-11, a ruling note): C24 scored "Kraft paper and packing
# peanuts are listed as items a branch buys today for less than the recommended supplier's
# price", and the Bay City manager's email said "The kraft paper and the peanuts are not"
# (cheaper at the bidder). The ruling: the email "hands the solver the exact answer graded
# by rubric line 24 instead of requiring the comparison to be computed from the invoice and bid
# data". L3 catches a stay verdict on a named entity; this is the enumeration form, the items a
# criterion scores as the found set named together in one input paragraph. An input may raise
# the concern ("some of the items we buy most of may be higher, check them item by item"); the
# moment it names the members, it is the answer key.
_L4_LISTED_RE = re.compile(
    r"^(?:The\s+)?(.+?)\s+(?:are|is)\s+(?:listed|flagged|named|identified|shown|reported)\s+as\b", re.I)


@check(codes=['L4'], rules=['DATA-LEAK'], needs=['inputs', 'rubric'], params=['folder'])
def check_leaked_listed_items(folder):
    """No input paragraph names together every item a positive criterion scores as the listed or flagged set.

    Since: 2026-09-11 (a ruling note).
    Source: the ruling found the Bay City email naming kraft paper and packing peanuts hands the solver the answer graded by the exceptions row.
    """
    inp = folder / "inputs"
    path = rubric_path(folder)
    if not (inp.is_dir() and path.exists()):
        return
    rows = load_rows(path)
    targets = []
    for num, text, weight in rows:
        if weight <= 0:
            continue
        m = _L4_LISTED_RE.match(text.strip())
        if not m:
            continue
        items = [x.strip() for x in re.split(r",\s*|\s+and\s+", m.group(1)) if x.strip()]
        keys = [it.split()[-1].lower() for it in items if len(it.split()[-1]) >= 5]
        if len(items) >= 2 and len(keys) >= 2:
            targets.append((num, items, keys))
    if not targets:
        return
    for path in sorted(inp.glob("*.docx")):
        try:
            with zipfile.ZipFile(path) as z:
                xml = z.read("word/document.xml").decode("utf-8", "replace")
        except Exception:
            continue
        for para in xml.split("</w:p>"):
            text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", para)).strip()
            low = text.lower()
            for num, items, keys in targets:
                if all(re.search(rf"\b{re.escape(k)}\b", low) for k in keys):
                    emit("ERROR", f"C{num} [L4] inputs/{path.name} names together the items this "
                                  f"criterion scores as the listed set ({', '.join(items)}): "
                                  f"{text[:140]!r}. A task was sent back on exactly this "
                                  "(2026-09-11, the Bay City email naming kraft "
                                  "paper and peanuts). Let the input raise the concern and leave the "
                                  "members to be computed from the data")
                    break


@check(codes=['L5'], rules=['DATA-LEAK'], needs=['inputs', 'solution'], params=['folder'])
def check_golden_among_inputs(folder):
    """No input file is the deliverable or a copy of it: no input shares a golden file's basename, and no input workbook carries three or more of a golden workbook's sheet titles.

    Since: 2026-09-14 (a ruling note).
    Source: the ruling found the finished workbook among the platform's input files, every scored tab populated, and held that it gives away every conclusion; the repo's i- zip never held it, so the upload put the deliverable in the input widget. The check reads whatever inputs are staged.
    """
    import openpyxl
    inp, sol = folder / "inputs", folder / "solution"
    if not (inp.is_dir() and sol.is_dir()):
        return
    golden = sorted(f for f in sol.iterdir() if f.is_file() and not f.name.startswith("."))
    if not golden:
        return
    names = {g.name.lower(): g.name for g in golden}
    sheets = {}
    for g in golden:
        if g.suffix.lower() == ".xlsx":
            try:
                wb = openpyxl.load_workbook(g, read_only=True)
                sheets[g.name] = {t.strip().lower() for t in wb.sheetnames}
                wb.close()
            except Exception:
                pass
    for f in sorted(inp.iterdir()):
        if not f.is_file() or f.name.startswith("."):
            continue
        if f.name.lower() in names:
            emit("ERROR", f"[L5] inputs/{f.name} carries the deliverable's own name ({names[f.name.lower()]} in "
                          "solution/): the finished workbook is shipped as an input and hands over every "
                          "conclusion (2026-09-14)")
            continue
        if f.suffix.lower() == ".xlsx" and sheets:
            try:
                wb = openpyxl.load_workbook(f, read_only=True)
                titles = {t.strip().lower() for t in wb.sheetnames}
                wb.close()
            except Exception:
                continue
            for gname, gset in sheets.items():
                shared = titles & gset
                if len(shared) >= 3:
                    emit("ERROR", f"[L5] inputs/{f.name} carries {len(shared)} of {gname}'s sheet titles "
                                  f"({', '.join(sorted(shared)[:5])}): an input that is the deliverable under "
                                  "another name (2026-09-14)")
                    break



# L6 (2026-09-14): ANSWER_LEAKED on three comments written into
# inventory_adjustments.xlsx earlier ("picks ... not posted,
# timing, hold until WMS posts"; "bin corrected to QC hold, no qty change"; "242 short, cannot tie
# to txns"). Each sat on a record the memo cites and stated the memo's diagnosis and action for
# that SKU in the memo's own words. A note on a cited row may name a document or a bin; it may
# not carry the conclusion.
_L6_ID_RE = re.compile(r"\b([A-Z]{2,6})-(\d{4,8})\b")
_L6_NOTE_HDR_RE = re.compile(r"\b(?:notes?|comments?|remarks?)\b", re.I)
_L6_CONCLUSION_RE = re.compile(
    r"\btiming\b|\bduplicate\b|\bunexplained\b|\bcannot (?:tie|account|reconcile|explain)\b|\bnot a loss\b"
    r"|\bno (?:qty|quantity) change\b|\bno adjustment\b|\bhold until\b|\bshould\b|\bexplained by\b"
    r"|\bnot posted\b|\bpost(?:ing)? (?:still )?pending\b|\bwrite[- ]?off approved\b|\baccept(?:ed)?\b|\bsuspend\b", re.I)


def _l6_tables(folder):
    import csv
    d = folder / "inputs"
    for path in sorted(d.glob("*")) if d.is_dir() else []:
        if path.suffix.lower() == ".csv":
            try:
                rows = list(csv.reader(path.open(encoding="utf-8-sig", errors="ignore")))
            except Exception:
                continue
            if len(rows) > 1:
                yield path.name, rows[0], [[(c.strip() or None) for c in r] for r in rows[1:]]
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


@check(codes=['L6'], rules=['DATA-LEAK'], needs=['inputs', 'solution'], params=['folder'])
def check_conclusion_in_cited_note(folder):
    """A note or comment cell on an input row the golden cites carries no conclusion word (timing, duplicate, unexplained, cannot tie, no quantity change, hold until, should); the leakage check reads such a note as the answer handed over.

    Since: 2026-09-14.
    Source: the platform's golden_solution_leakage_check, ANSWER_LEAKED on three adjustment comments
    written earlier into the same file.
    Drift-notes: the row must be one the golden cites by id and the column note-like; the word list is
    closed and the golden's own wording is not required (the leak "cannot tie to txns" stood against a
    golden that said "do not account for the shortage"). A note naming a document or a bin is not read.
    """
    from ..common import _docx_text
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
    cited = {m.group(0) for m in _L6_ID_RE.finditer(golden)}
    if not cited:
        return
    leaks = []
    for name, header, rows in _l6_tables(folder):
        keycols = [j for j, h in enumerate(header)
                   if sum(1 for r in rows if j < len(r) and r[j] and _L6_ID_RE.fullmatch(r[j])) >= 0.9 * max(1, len(rows))]
        notecols = [j for j, h in enumerate(header) if _L6_NOTE_HDR_RE.search(h)]
        if not keycols or not notecols:
            continue
        for r in rows:
            keys = [r[j] for j in keycols if j < len(r) and r[j] in cited]
            if not keys:
                continue
            for j in notecols:
                v = r[j] if j < len(r) else None
                if not v:
                    continue
                hits = [m.group(0) for m in _L6_CONCLUSION_RE.finditer(v)]
                if hits:
                    leaks.append(f"{name} {keys[0]} \"{header[j]}\": \"{v}\" ({', '.join(sorted(set(hits)))})")
    if leaks:
        emit("ERROR", f"[L6] {len(leaks)} note(s) on records the golden cites carry the golden's conclusion: "
                      f"{'; '.join(leaks[:5])}. The leakage check returned ANSWER_LEAKED on exactly this "
                      "(2026-09-14: three adjustment comments stating the "
                      "diagnosis and the action). A note on a cited row names a document or a bin, never the "
                      "finding")
