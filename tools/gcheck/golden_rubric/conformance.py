"""Group 2: deliverable conformance (R134, G41, G42, G43).

These checks read the prompt's asks against what the package actually delivers, where every
other golden check reads the artifacts against each other. They come from dfl-freight-audit's
rejection (2026-09-15): eleven rounds of feedback and a clean gate on a golden that never
produced the claim forms the prompt asked for, a phrase struck from the prose that survived
in a table cell, and a rating engine that lived in a scratchpad and was never re-run.

Task-folder files they read (never zipped):
  clause-map.md      R134, the prompt clause -> golden anchor -> rubric row map, with a
                     "Rebuilt: YYYY-MM-DD" line after the third return (PR19)
  struck-phrases.md  G42, one bullet per struck phrase: - "literal" or - /regex/, then source
  verify_golden.py   G43, re-derives the golden from the inputs; see tools/golden_verify.py
"""
import html
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from ..common import _docx_tables, _xlsx_all_text, input_texts, package_texts, solution_files
from ..core import check, emit
from ..state import document, workbook
from .rubric_form import _R83_BASENAME_RE

_STOP = {"the", "a", "an", "and", "or", "of", "to", "in", "on", "for", "with", "by", "at", "from",
         "as", "is", "are", "was", "be", "it", "its", "that", "this", "what", "where", "who", "so",
         "we", "us", "our", "she", "he", "they", "them", "her", "his", "their", "wants", "want",
         "need", "needs", "has", "have", "will", "can", "every", "each", "all", "any", "set", "out"}
_MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"
_WEEKDAYS = "Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday"
_DATE_RE = re.compile(r"\b(?:" + _WEEKDAYS + r")\b|\b(?:" + _MONTHS + r")\s+\d{1,2}\b")


def _norm(text):
    return re.sub(r"\s+", " ", (text or "").replace("’", "'").replace("“", '"')
                  .replace("”", '"')).strip().lower()


def _words(text):
    return [w.lower() for w in re.findall(r"[A-Za-z0-9][A-Za-z0-9'\-]*", text or "")]


def _stem(word):
    w = word.lower().strip("'")
    if w.endswith("ies") and len(w) > 4:
        return w[:-3] + "y"
    if w.endswith("es") and len(w) > 4 and w[-3] in "sxz":
        return w[:-2]
    if w.endswith("s") and not w.endswith("ss") and len(w) > 3:
        return w[:-1]
    return w


def _content(text):
    return {_stem(w) for w in _words(text) if w not in _STOP and len(w) > 2}


def _quotes(cell):
    return [a or b for a, b in re.findall(r'"([^"]+)"|“([^”]+)”', cell or "")]


def ask_segments(folder):
    """The deliverable asks of prompt.md: the clauses, split at commas and semicolons, of every
    paragraph naming the deliverable file, leaving out date phrases and fragments under four words."""
    folder = Path(folder)
    p = folder / "prompt.md"
    if not p.is_file():
        return []
    prompt = p.read_text(encoding="utf-8", errors="ignore")
    inputs = {q.name.lower() for q in (folder / "inputs").glob("*")} if (folder / "inputs").is_dir() else set()
    names = [m.group(1) for m in _R83_BASENAME_RE.finditer(prompt) if m.group(1).lower() not in inputs]
    paras = [x for x in re.split(r"\n\s*\n", prompt) if x.strip()]
    ask = [x for x in paras if any(n in x for n in names)] or paras[-1:]
    segs = []
    for para in ask:
        for sent in re.split(r"(?<=[.!?])\s+(?=[A-Z])", para.strip()):
            for seg in re.split(r",\s+(?:and\s+|or\s+)?|;\s+", sent):
                seg = seg.strip().rstrip(".!?").strip()
                if len(_words(seg)) < 4 or _DATE_RE.search(seg):
                    continue
                segs.append(seg)
    return segs


def golden_text(folder):
    """Normalised text of every solution file: docx paragraphs and tables, xlsx strings and sheet titles."""
    parts = []
    for path in solution_files(Path(folder), {".docx"}):
        try:
            doc = document(path)
        except Exception:
            continue
        parts.extend(p.text for p in doc.paragraphs)
        parts.extend(c.text for t in doc.tables for r in t.rows for c in r.cells)
    for path in solution_files(Path(folder), {".xlsx"}):
        parts.extend(t for _, t in _xlsx_all_text(path))
    return _norm("\n".join(parts))


_RETURN_RE = re.compile(r"NEEDS_REVISION|needs_improvement|REJECTED|reviewer|adjudicat|auto-?eval|"
                        r"golden solution check|rubric quality review|refinement panel", re.I)
_RETURN_SKIP_RE = re.compile(r"pre-submission|in-app|\bbuild\b|restore|re-save|hand-over|\bsubmitted\b", re.I)


def return_dates(folder):
    """Distinct dates of the platform returns recorded in feedback-log.md headings, oldest first."""
    log = Path(folder) / "feedback-log.md"
    if not log.is_file():
        return []
    dates = set()
    for m in re.finditer(r"(?m)^##\s+(\d{4}-\d{2}-\d{2})\b(.*)$", log.read_text(encoding="utf-8", errors="ignore")):
        if _RETURN_RE.search(m.group(2)) and not _RETURN_SKIP_RE.search(m.group(2)):
            dates.add(m.group(1))
    return sorted(dates)


def _clause_map(path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    rebuilt = re.search(r"(?mi)^\s*Rebuilt:\s*(\d{4}-\d{2}-\d{2})", text)
    header, rows = None, []
    for line in text.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", c) for c in cells if c):
            continue
        if header is None:
            header = [c.lower() for c in cells]
            continue
        rows.append(dict(zip(header, cells)))
    return header or [], rows, rebuilt.group(1) if rebuilt else None


@check(codes=['R134'], rules=['PRE-COVER'], needs=['prompt', 'rubric', 'solution', 'folder'], params=['rows', 'folder'])
def check_clause_map(rows, folder):
    """Every deliverable ask in the prompt is mapped in the task's clause-map.md to a clause quoted verbatim from the prompt, a quoted anchor the golden contains and at least one positive rubric row, and once three returns are logged the map carries a Rebuilt date on or after the latest one.

    Since: 2026-09-15 (dfl-freight-audit rejection).
    Source: the rejection's central finding, "it does not provide the 71 individual DFL claim forms
    required", held through eleven rounds and a clean gate, because no check and no rubric row read the
    prompt's asks against the deliverable; the eight reason-code groups went unscored the same way.
    Drift-notes: the asks are the comma and semicolon clauses of each prompt paragraph naming the
    deliverable file, fragments under four words and date phrases dropped; an ask is covered when 60
    percent of its content words sit in one mapped clause. The map is a markdown table with columns
    whose headers contain "prompt", "golden" and "rubric". Returns are feedback-log.md headings naming a
    reviewer, adjudication, AutoEval, a golden solution check, a Rubric Quality Review, a refinement
    panel, NEEDS_REVISION, needs_improvement or REJECTED, counted by distinct date (PR19).
    """
    folder = Path(folder)
    segs = ask_segments(folder)
    if not segs:
        return
    cm = folder / "clause-map.md"
    if not cm.is_file():
        emit("ERROR", f"[R134] no clause-map.md: the prompt makes {len(segs)} deliverable asks (first: \"{segs[0]}\") "
                      "and nothing maps each one to where the golden delivers it and the rubric row that fails "
                      "without it (dfl-freight-audit was rejected on an ask the golden never met, 2026-09-15). "
                      "Write the table: | # | Prompt clause | Golden location | Rubric rows |, clauses and golden "
                      "anchors in double quotes")
        return
    header, mrows, rebuilt = _clause_map(cm)
    pick = lambda key: next((h for h in header if key in h), None)
    pc, gc, rc = pick("prompt"), pick("golden"), pick("rubric")
    if not (pc and gc and rc and mrows):
        emit("ERROR", "[R134] clause-map.md has no table with Prompt clause, Golden location and Rubric rows columns")
        return
    prompt_norm = _norm((folder / "prompt.md").read_text(encoding="utf-8", errors="ignore"))
    gold = golden_text(folder)
    weights = {str(n).strip(): w for n, _, w in rows}
    mapped, problems = [], []
    for i, r in enumerate(mrows, 1):
        q = _quotes(r.get(pc, ""))
        if not q or not all(_norm(x) in prompt_norm for x in q):
            problems.append(f"row {i} quotes no prompt text verbatim")
        else:
            mapped.append(set().union(*(_content(x) for x in q)))
        g = _quotes(r.get(gc, ""))
        if not g or not any(_norm(x) in gold for x in g):
            problems.append(f"row {i} names no quoted text the golden contains")
        nums = re.findall(r"\d+", r.get(rc, ""))
        if not nums or any(n not in weights or weights[n] <= 0 for n in nums):
            problems.append(f"row {i} cites rubric rows {nums or 'none'} that are not positive rows")
    if problems:
        emit("ERROR", "[R134] clause-map.md rows do not anchor: " + "; ".join(problems[:6]) +
                      (" ..." if len(problems) > 6 else ""))
    uncovered = [s for s in segs if _content(s) and
                 not any(len(_content(s) & m) / len(_content(s)) >= 0.6 for m in mapped)]
    if uncovered:
        emit("ERROR", f"[R134] {len(uncovered)} prompt ask(s) have no row in clause-map.md: " +
                      "; ".join(f"\"{s}\"" for s in uncovered[:5]) + (" ..." if len(uncovered) > 5 else "") +
                      ". Map each to where the golden delivers it and a rubric row that fails without it")
    back = return_dates(folder)
    if len(back) >= 3 and (rebuilt is None or rebuilt < back[-1]):
        emit("ERROR", f"[R134] {len(back)} returns are logged (latest {back[-1]}) and clause-map.md carries "
                      f"{'no Rebuilt line' if rebuilt is None else 'Rebuilt: ' + rebuilt}: from the third return the "
                      "package is rebuilt from the clause map, every ask re-read against the golden and the rubric, "
                      "not patched item by item (PR19); date the map when that is done")


_CREATE_VERB = r"prepare|draft|write(?: up)?|build|produce|compile|complete|fill (?:out|in)|put together|assemble|create|issue"
_DISPATCH_VERB = r"file|send|submit|e-?mail|mail|post|lodge"
_NUMWORD = r"(?:\d[\d,]*|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred)(?:-(?:one|two|three|four|five|six|seven|eight|nine))?"
_LEAD_RE = re.compile(r"^\s*(?P<verb>" + _CREATE_VERB + "|" + _DISPATCH_VERB + r")\s+"
                      r"(?:the |all |every |each |a |an |our |their |its |any )?(?:" + _NUMWORD + r"\s+)?"
                      r"(?P<obj>(?:[A-Za-z][\w'\-]*\s+){0,3}?[A-Za-z][\w'\-]*?)"
                      r"(?=\s+(?:on|to|with|for|by|from|under|in|into|at|and|so|before|after|using|via)\b|[,.;:]|$)", re.I)
# a sending verb defers the making only when the thing is still to be put onto a form ("File the 71
# claims on DFL's form"); "email the 71 claim forms in this memo" sends what the deliverable holds
_FILL_ON_FORM_RE = re.compile(r"\b(?:on|onto|using|via|through)\s+(?:the\s+|a\s+|an\s+)?(?:[\w'\-]+\s+){0,3}?forms?\b", re.I)
_OWNER_HEAD_RE = re.compile(r"\b(?:WHO|OWNER|RESPONSIBLE|BY WHEN|DUE|DEADLINE|TARGET DATE)\b", re.I)
_ACTION_HEAD_RE = re.compile(r"^\s*(?:WHAT|ACTIONS?|STEPS?|TASKS?|NEXT STEPS?|CHANGES?)\s*$", re.I)


def _solution_tables(folder):
    out = [(f"{name} table {i + 1}", rows) for name, i, rows in _docx_tables(folder)]
    for path in solution_files(Path(folder), {".xlsx"}):
        try:
            wb = workbook(path, data_only=True)
        except Exception:
            continue
        for ws in wb.worksheets:
            rows = [["" if v is None else str(v).strip() for v in r] for r in ws.iter_rows(values_only=True)]
            for h in range(min(10, len(rows))):
                if any(_OWNER_HEAD_RE.search(c) for c in rows[h]):
                    out.append((f"{path.name} '{ws.title}'", rows[h:]))
                    break
            else:
                out.append((f"{path.name} '{ws.title}'", rows))
    return out


@check(codes=['G41'], rules=['GOLD-FID'], needs=['prompt', 'inputs', 'solution'], params=['folder'])
def check_deferred_deliverable(folder):
    """The golden delivers every artifact the prompt asks for inside the deliverable itself: no action row hands the making or form-filing of an asked-for artifact to later work, and where an input requires one form per record the golden carries one form block per record rather than a single schedule.

    Since: 2026-09-15 (dfl-freight-audit rejection).
    Source: the prompt asked for "the claims themselves in the form Dahlquist's claims desk will
    accept", the agreement and the claims desk required "DFL's claim form, one claim per invoice", and
    the golden gave a 71-row schedule plus the action "File the 71 claims on DFL's form"; the rejection
    called it a failed central requirement.
    Drift-notes: arm 1 reads action tables (a header naming WHO, OWNER, RESPONSIBLE, BY WHEN, DUE,
    DEADLINE or TARGET DATE) whose action text has four or more words and opens on a making verb
    (prepare, draft, write, build, produce, compile, complete, fill out, assemble, create, issue), or on
    a sending verb (file, send, submit, email) whose object is still to be put on, onto or through a
    form ("File the 71 claims on DFL's form"; "email the claim forms in this memo" passes); it fires when the
    object's head noun is in a prompt ask. Arm 2 fires only on an input sentence that names a form and
    says "one X per Y" (or for each / for every), with X in a prompt ask and a golden table whose header
    names both X and Y: the golden must carry at least as many X form blocks (a table of three columns
    or fewer headed by X, or a paragraph opening "X" with a number) as that table has rows. The
    portfolio probe of 2026-09-15 found no other task on either arm once two-word disposition values
    and form-free "one fee per order" sentences were set aside.
    """
    folder = Path(folder)
    segs = ask_segments(folder)
    if not segs:
        return
    asks = " ".join(segs)
    tables = _solution_tables(folder)
    for where, rows in tables:
        if not rows or not any(_OWNER_HEAD_RE.search(c) for c in rows[0]):
            continue
        col = next((i for i, c in enumerate(rows[0]) if _ACTION_HEAD_RE.match(c)), 0)
        for r in rows[1:]:
            text = r[col] if col < len(r) else ""
            if len(_words(text)) < 4:
                continue
            m = _LEAD_RE.match(text)
            if not m:
                continue
            if re.fullmatch(_DISPATCH_VERB, m.group("verb"), re.I) and not _FILL_ON_FORM_RE.search(text):
                continue
            head = _stem(m.group("obj").split()[-1])
            if len(head) < 4 or not re.search(r"\b" + re.escape(head), asks, re.I):
                continue
            emit("ERROR", f"[G41] {where}: the action \"{text[:110]}\" hands the {m.group('obj')} to later work, "
                          f"and the prompt asks for them in the deliverable (\"{next(s for s in segs if re.search(chr(92) + 'b' + re.escape(head), s, re.I))}\"). "
                          "Produce them in the golden; an action row may send what the deliverable already holds, "
                          "never make it (dfl-freight-audit rejection, 2026-09-15)")
    texts = input_texts(folder)
    items = list(texts.items()) if isinstance(texts, dict) else list(texts or [])
    seen = set()
    for name, text in items:
        for sent in re.split(r"(?<=[.!?])\s+", text or ""):
            if not re.search(r"\bforms?\b", sent, re.I):
                continue
            for m in re.finditer(r"\bone ([a-z]+) (?:per|for each|for every) ([a-z]+)\b", sent, re.I):
                x, y = _stem(m.group(1)), _stem(m.group(2))
                if (x, y) in seen or len(x) < 4 or not re.search(r"\b" + re.escape(x), asks, re.I):
                    continue
                seen.add((x, y))
                expected, schedule = 0, None
                for where, rows in tables:
                    if rows and any(re.search(r"\b" + re.escape(x), c, re.I) for c in rows[0]) \
                            and any(re.search(r"\b" + re.escape(y), c, re.I) for c in rows[0]):
                        n = sum(1 for r in rows[1:] if any(c.strip() for c in r))
                        if n > expected:
                            expected, schedule = n, where
                if expected < 2:
                    continue
                blocks = sum(1 for _, rows in tables
                             if rows and len(rows[0]) <= 3 and len(rows) >= 3
                             and re.search(r"\b" + re.escape(x), " ".join(rows[0]), re.I))
                for path in solution_files(folder, {".docx"}):
                    try:
                        blocks += sum(1 for p in document(path).paragraphs
                                      if re.match(r"^\s*" + re.escape(x) + r"\w*(?:\s+form)?\s*(?:no\.?|number|#)?\s*[:\-]?\s*\S*\d", p.text, re.I))
                    except Exception:
                        pass
                if blocks < expected:
                    emit("ERROR", f"[G41] {name} requires \"{m.group(0)}\" on a form and the prompt asks for the {m.group(1)}s, "
                                  f"but the golden carries {blocks} {m.group(1)} form block(s) against {expected} rows in "
                                  f"{schedule}. Give each {m.group(2)} its own {m.group(1)} form in the deliverable, the fields the "
                                  "form requires filled, rather than one schedule (dfl-freight-audit rejection, 2026-09-15)")


def _ledger(folder):
    path = Path(folder) / "struck-phrases.md"
    if not path.is_file():
        return []
    out = []
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        s = line.strip()
        if not s.startswith("- "):
            continue
        body = s[2:].strip()
        m = re.match(r'^"([^"]+)"', body) or re.match(r"^“([^”]+)”", body)
        if m:
            out.append((m.group(0), re.compile(re.escape(_norm(m.group(1))).replace(r"\ ", r"\s+"), re.I)))
            continue
        m = re.match(r"^/(.+)/(?=\s|$)", body)
        if m:
            try:
                out.append((m.group(0), re.compile(m.group(1), re.I)))
            except re.error:
                out.append((m.group(0), None))
    return out


def _searchable(folder):
    folder = Path(folder)
    files = [folder / "prompt.md", folder / "review-comment.md"] + sorted(folder.glob("rubric-*.csv"))
    for sub in ("inputs", "solution"):
        if (folder / sub).is_dir():
            files += sorted(p for p in (folder / sub).iterdir() if p.is_file())
    out = []
    for f in files:
        if not f.is_file():
            continue
        if f.suffix.lower() in (".docx", ".xlsx", ".pptx"):
            for member, text in package_texts(f):
                if not member.endswith(".xml") or not re.match(r"(word/|xl/sharedStrings|xl/worksheets/|ppt/slides/)", member):
                    continue
                text = re.sub(r"</w:p>|</a:p>|</si>|</c>|<w:br/>|<w:tab/>", "\n", text)
                out.append((f"{f.parent.name}/{f.name}", html.unescape(re.sub(r"<[^>]+>", "", text))))
        elif f.suffix.lower() == ".pdf":
            texts = input_texts(folder)
            items = list(texts.items()) if isinstance(texts, dict) else list(texts or [])
            out += [(f"inputs/{n}", t) for n, t in items if n == f.name]
        else:
            try:
                out.append((f.name if f.parent == folder else f"{f.parent.name}/{f.name}",
                            f.read_text(encoding="utf-8", errors="ignore")))
            except Exception:
                pass
    return out


@check(codes=['G42'], rules=['GOLD-FID'], needs=['folder'], params=['folder'])
def check_struck_phrases(folder):
    """No phrase recorded in the task's struck-phrases.md, as a literal or a pattern, appears anywhere in the prompt, the rubric, the Section 3 text, an input or a solution file, table cells and headers included.

    Since: 2026-09-15 (dfl-freight-audit rejection).
    Source: on 2026-09-10 a reviewer struck "figures that appear nowhere in Appendix B" and "carries no
    half point row at all"; the revision reworded both paragraphs and left the same claim in the
    reason-code table cell, "billed at a percentage Appendix B does not carry", which the rejection
    named as an internal inconsistency.
    Drift-notes: a bullet opening "literal" matches that text with any whitespace, case-insensitive; a
    bullet opening /regex/ matches the pattern, which is how a claim is caught under new wording
    (/Appendix B (does not|doesn't) carry|nowhere in Appendix B|no half point row/). Office files are read
    part by part (document, headers, footers, shared strings, sheets, slides); feedback-log.md,
    change.log, clause-map.md and the ledger itself are never searched, since they quote the phrases.
    Recording each struck phrase is PR20.
    """
    entries = _ledger(folder)
    if not entries:
        return
    texts = [(where, re.sub(r"\s+", " ", t)) for where, t in _searchable(folder)]
    for label, rx in entries:
        if rx is None:
            emit("ERROR", f"[G42] struck-phrases.md: {label} is not a valid pattern")
            continue
        hits = []
        for where, t in texts:
            for m in rx.finditer(t):
                hits.append(f"{where} \"...{t[max(0, m.start() - 40):m.end() + 40].strip()}...\"")
        if hits:
            emit("ERROR", f"[G42] struck phrase {label} is back in {len(hits)} place(s): " + "; ".join(hits[:4]) +
                          (" ..." if len(hits) > 4 else "") + ". A struck claim is removed from every copy, table "
                          "cells and rubric rows included (dfl-freight-audit rejection, 2026-09-15)")


@check(codes=['G43'], rules=['GOLD-FID'], needs=['solution', 'folder'], params=['folder'])
def check_golden_verification(folder):
    """The task folder carries verify_golden.py, which re-derives the golden's figures from the inputs alone and exits 0 with every figure reproduced, and every standing a reasonable alternate reading flips names a convention phrase the golden itself states.

    Since: 2026-09-15 (dfl-freight-audit rejection).
    Source: the rating engine behind the golden was rebuilt in a scratchpad three times and never kept,
    so no revision re-ran it, and the rejection found "at least one underbilled invoice" marked correct:
    leaving the base charge unrounded moves DFL7718237 to under-billed by one cent, and four more
    standings move on a one-cent rounding choice or the band-boundary rule the golden never stated.
    Drift-notes: the script runs from the task folder under the gate's interpreter with HAZY_ROOT set,
    ten minutes at most, and prints a JSON object on its last stdout line: {"checked": N, "mismatches":
    [...], "near_flips": [{"key", "variant", "convention"}]}. tools/golden_verify.py builds that report
    and runs the sensitivity pass; tools/templates/verify_golden.py is the starting point. A near flip
    passes when its convention phrase appears, case-insensitive, in the golden's text.
    """
    folder = Path(folder)
    if not solution_files(folder, {".docx", ".xlsx"}):
        return
    script = folder / "verify_golden.py"
    if not script.is_file():
        emit("ERROR", "[G43] no verify_golden.py: nothing re-derives the golden's figures from the inputs, so no "
                      "revision re-checks them (dfl-freight-audit's engine lived in a scratchpad and was lost three "
                      "times). Start from tools/templates/verify_golden.py")
        return
    env = dict(os.environ, HAZY_ROOT=str(Path(__file__).resolve().parents[3]))
    try:
        proc = subprocess.run([sys.executable, script.name], cwd=str(folder), env=env,
                              capture_output=True, text=True, timeout=600)
    except subprocess.TimeoutExpired:
        emit("ERROR", "[G43] verify_golden.py ran past ten minutes")
        return
    last = next((ln for ln in reversed(proc.stdout.splitlines()) if ln.strip().startswith("{")), None)
    try:
        rep = json.loads(last) if last else None
    except ValueError:
        rep = None
    if not isinstance(rep, dict):
        tail = (proc.stderr or proc.stdout or "").strip().splitlines()[-3:]
        emit("ERROR", f"[G43] verify_golden.py printed no JSON report (exit {proc.returncode}): " + " | ".join(tail))
        return
    mism = rep.get("mismatches") or []
    if proc.returncode != 0 or mism or not rep.get("checked"):
        shown = "; ".join(f"{m.get('key')}: golden {m.get('want')}, derived {m.get('got')}" for m in mism[:5])
        emit("ERROR", f"[G43] verify_golden.py: {rep.get('checked', 0)} figure(s) checked, {len(mism)} not reproduced"
                      + (f" ({shown})" if shown else "") + (" and it checked nothing" if not rep.get("checked") else ""))
    gold = golden_text(folder)
    flips = rep.get("near_flips") or []
    unstated = [f for f in flips if not f.get("convention") or _norm(f["convention"]) not in gold]
    if unstated:
        by = {}
        for f in unstated:
            by.setdefault((f.get("variant"), f.get("convention")), []).append(str(f.get("key")))
        listed = "; ".join(f"{v} flips {', '.join(ks[:4])}{' ...' if len(ks) > 4 else ''} "
                           f"(golden does not state \"{c}\")" for (v, c), ks in list(by.items())[:5])
        emit("ERROR", f"[G43] {len(unstated)} standing(s) move under an alternate reading the golden never settles: {listed}. "
                      "State the convention in the golden's method text, in the words the report names")
    elif rep.get("checked"):
        print(f"        info: [G43] verify_golden.py reproduced {rep['checked']} figure(s); "
              f"{len(flips)} near flip(s), each settled by a convention the golden states")
