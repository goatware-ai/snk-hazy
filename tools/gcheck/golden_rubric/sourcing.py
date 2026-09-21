"""Group 2b: the golden read against the SOURCES it cites (GOLD-FID).

Written 2026-09-05 from a task rejection. Every other check in
this package tests the rubric against the golden; the four defects that killed that task
were all the golden against its own inputs, which nothing could see:

  a deadline attributed to a named person that he never gave, the date lifted from an
  unrelated document in the same packet; a plan built on an entitlement the source says
  is only requested; a quantity column typed where the prompt demands live formulas; and
  a blended cost that priced three supply sources at one of their unit costs.

Two are errors with a mechanical signature. Two are review ledgers, because the judgement
is the builder's and a rule that guesses it would flag correct work.
"""
import re
import zipfile
from xml.etree import ElementTree as ET
from ..common import MONTH_NUM, MONTHS_RE, split_sentences, workbook
from ..core import check, emit

_W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
_MONTHS = MONTH_NUM
_DATE_SLASH = re.compile(r"\b(\d{1,2})/(\d{1,2})(?:/20\d\d)?\b")
_DATE_WORD = re.compile(r"\b(" + MONTHS_RE + r")\s+(\d{1,2})\b", re.I)
# a surname the packet actually uses, so "Monday" and "Friday" never read as people
_NAME = re.compile(r"\b(?:[A-Z]\.\s*)?([A-Z][a-z]{3,})\b")


def _daypairs(text):
    out = {(int(m), int(d)) for m, d in _DATE_SLASH.findall(text)}
    out |= {(_MONTHS[m.lower()], int(d)) for m, d in _DATE_WORD.findall(text)}
    return out


def _source_docs(folder):
    """Every document a claim could cite: the inputs and the prompt, kept separate."""
    docs = {}
    d = folder / "inputs"
    for p in sorted(d.glob("*")) if d.is_dir() else []:
        try:
            if p.suffix == ".docx":
                z = zipfile.ZipFile(p)
                docs[p.name] = " ".join(
                    "".join(n.text or "" for n in par.iter(_W + "t"))
                    for par in ET.fromstring(z.read("word/document.xml")).iter(_W + "p"))
            elif p.suffix == ".csv":
                docs[p.name] = p.read_text(errors="ignore")
            elif p.suffix == ".xlsx":
                wb = workbook(p, data_only=True)
                docs[p.name] = " ".join(str(c.value) for ws in wb for r in ws.iter_rows()
                                        for c in r if c.value is not None)
        except Exception:
            continue
    pr = folder / "prompt.md"
    if pr.exists():
        docs["prompt.md"] = pr.read_text(encoding="utf-8", errors="ignore")
    return docs


# G11: the defect that killed one task. Its action list carried "Base period recap ... to
# Balliet" against "Friday 08/28/2026", and the briefing said "Balliet has asked for it by
# Friday the 28th". Balliet's own message says only "Send me a recap by group and by month
# ... I will put it in front of Sandusky myself" - no date at all. The 28th was the SOWERS
# hold date, lifted out of a different document in the same packet. The source was checked
# and the task rejected on it.
#
# The test is source-scoped, which is what makes it quiet: a dated obligation put on a
# named person must carry a date that appears in a document mentioning that person. A
# deadline the buyer sets for himself is fine (the prompt names it, and the prompt is in
# the corpus); a deadline attributed to someone who never gave one is not.
# The signature is an ATTRIBUTION, not a co-occurrence: the golden must say the person
# ASKED FOR something BY a date. A memo header ("From: K. Delp, 08/19/2026") and an action
# list row (a deadline the buyer sets for himself, owner in one column and date in another)
# are neither, and a first cut that keyed on name-plus-date in a row flagged all of them.
_ATTRIB = re.compile(
    r"\b(?:[A-Z]\.\s*)?(?P<who>[A-Z][a-z]{3,})\b[^.]{0,90}?"
    r"\b(?:has asked|asked|is asking|requested|requests|wants|expects|is expecting|"
    r"requires|needs|set|gave|gives|insists)\b[^.]{0,90}?"
    r"\b(?:by|before|no later than|not later than)\b[^.]{0,40}?"
    r"(?P<date>\b\d{1,2}/\d{1,2}(?:/20\d\d)?\b|\b(?:%s)\s+\d{1,2}\b|\bthe\s+\d{1,2}(?:st|nd|rd|th)\b)"
    % MONTHS_RE, re.I)
_DAY_ONLY = re.compile(r"\bthe\s+(\d{1,2})(?:st|nd|rd|th)\b", re.I)


@check(codes=['G11'], rules=['GOLD-FID'], needs=['inputs', 'solution'],
       params=['folder'])
def check_attributed_dates(folder):
    """A deadline the golden attributes to a named person carries a date that appears in a document mentioning that person.

    Since: 2026-09-05 (a task rejected 2026-09-04).
    Source: task feedback.
    """
    docs = _source_docs(folder)
    if not docs:
        return
    names = {}
    for text in docs.values():
        for who in set(_NAME.findall(text)):
            names.setdefault(who, set()).update(_daypairs(text))
    d = folder / "solution"
    seen = set()
    for path in sorted(d.glob("*.xlsx")) if d.is_dir() else []:
        try:
            wb = workbook(path, data_only=True)
        except Exception:
            continue
        for ws in wb.worksheets:
            for row in ws.iter_rows():
                for c in row:
                    if not isinstance(c.value, str) or len(c.value) < 25:
                        continue
                    for sent in split_sentences(c.value):
                        m = _ATTRIB.search(sent)
                        if not m:
                            continue
                        who, tok = m.group("who"), m.group("date")
                        if who not in names or not names[who]:
                            continue
                        dayonly = _DAY_ONLY.match(tok)
                        if dayonly:
                            ok = int(dayonly.group(1)) in {dd for _, dd in names[who]}
                            shown = tok.strip()
                        else:
                            pairs = _daypairs(tok)
                            ok = bool(pairs & names[who])
                            shown = "/".join(f"{a:02d}" for a in sorted(pairs)[0]) if pairs else tok
                        if ok:
                            continue
                        key = (path.name, who, shown)
                        if key in seen:
                            continue
                        seen.add(key)
                        emit("ERROR", f"[G11] {path.name} '{ws.title}'!{c.coordinate} has {who} "
                                      f"asking for something by {shown}, but no document that "
                                      f"mentions {who} carries that date - the golden is putting a "
                                      "deadline on a source that never gave one (a task "
                                      "rejected 2026-09-04: \"Balliet has asked "
                                      "for it by Friday the 28th\" against a message that asks for "
                                      "a recap with no date at all, the 28th lifted from the Sowers "
                                      "hold in another input). Cite the date the source gave, or "
                                      "drop the attribution and own the deadline")


# G12 (review ledger): the inputs' own conditions and prohibitions. That task was rejected
# partly for planning October through December at the corrected 589 ceiling when Balliet's
# message says only "I will put it in front of Sandusky myself ... Realistically a
# correction lands with the October ceilings ... do not build September around a bigger
# number" - a correction REQUESTED, not granted. The same task had already been sent back
# once for the same shape, planning on a Sowers lot whose quotation says "subject to prior
# sale" and "I can hold this list for you until Friday August 28".
#
# Whether the golden may lean on a conditioned figure is a judgement, and a rule that
# guessed it would flag correct work, so this prints the clauses and the builder ticks them
# off - the same contract as the future-dates sweep.
_CONDITION_RE = re.compile(
    r"\b(?:do not|don't|must not|may not|will not|cannot|can't|subject to|only with|only if|"
    r"provided that|realistically|no (?:earlier|later) than|not until|until further|"
    r"hold[^.]{0,30}\buntil\b|before[^.]{0,40}\b(?:may|can|is placed|goes)\b)\b", re.I)


@check(codes=['G12'], rules=['GOLD-FID'], needs=['inputs'], params=['folder'])
def check_input_conditions(folder):
    """List every condition or prohibition the inputs state, for the builder to tick off against the golden (information only).

    Since: 2026-09-05.
    Source: task feedback; a rule that guessed which conditions bind would flag correct work.
    """
    hits = []
    for name, text in _source_docs(folder).items():
        if name == "prompt.md":
            continue
        for sent in split_sentences(re.sub(r"\s+", " ", text)):
            if re.search(r"\bI (?:do not|don't) want\b", sent, re.I):
                continue                      # a preference, not a condition on a figure
            if 20 < len(sent) < 300 and _CONDITION_RE.search(sent):
                hits.append((name, sent.strip()))
    if hits:
        print(f"        info: {len(hits)} input conditions to tick off against the golden "
              f"(G12 - a figure the source only CONDITIONS may not be planned on as granted)")
        for name, sent in hits[:14]:
            print(f"          {name}: {sent[:132]}")


# G13 (review ledger): one item carrying more than one unit cost across the inputs.
# That task's blended job cost priced stock, the PO 78214 backlog and the new buy at the
# item file's 8.95, when the open order report carries those 23 backlog units at 9.33. Which
# cost applies to which source is the builder's call; that two exist is mechanical.
@check(codes=['G13'], rules=['GOLD-FID'], needs=['inputs'], params=['folder'])
def check_multiple_unit_costs(folder):
    """List every item carrying more than one unit cost across the inputs, so a blended cost prices each source at its own (information only).

    Since: 2026-09-05.
    Source: task feedback.
    """
    key_re = re.compile(r"^(item|catalog|sku|part|code|cat ?no|catalog ?no)\b", re.I)
    cost_re = re.compile(r"\b(cost|price)\b", re.I)
    per_item = {}
    d = folder / "inputs"
    for p in sorted(d.glob("*.xlsx")) if d.is_dir() else []:
        try:
            wb = workbook(p, data_only=True)
        except Exception:
            continue
        for ws in wb.worksheets:
            for row in ws.iter_rows(max_row=min(ws.max_row, 12)):
                heads = {c.column: str(c.value) for c in row if isinstance(c.value, str)}
                kcol = next((c for c, v in heads.items() if key_re.match(v.strip())), None)
                ccols = [c for c, v in heads.items() if cost_re.search(v)]
                if kcol is None or not ccols:
                    continue
                for r in ws.iter_rows(min_row=row[0].row + 1):
                    k = ws.cell(r[0].row, kcol).value
                    if not isinstance(k, str) or not k.strip():
                        continue
                    for cc in ccols:
                        v = ws.cell(r[0].row, cc).value
                        if isinstance(v, (int, float)) and not isinstance(v, bool) and v:
                            per_item.setdefault(k.strip(), {}).setdefault(
                                round(float(v), 4), set()).add(f"{p.name}:{heads[cc]}")
                break
    multi = {k: v for k, v in per_item.items() if len(v) > 1}
    if multi:
        print(f"        info: {len(multi)} item(s) carry more than one unit cost in the inputs "
              f"(G13 - a blended cost must price each source at its own)")
        for k, v in sorted(multi.items())[:10]:
            shown = ", ".join(f"{c:g} ({'/'.join(sorted(s))[:44]})" for c, s in sorted(v.items()))
            print(f"          {k}: {shown[:150]}")



# R97: the prompt asks for a per-month view, the golden builds one, and no criterion states
# a single figure out of it. The rejected task's demand tab carries SEP/OCT/NOV/DEC columns and the
# rubric scored only the basis and the totals, so a deliverable reporting one lump figure
# for the period would have kept full marks - the finding on the rejection
# ("no criterion requires that demand be reported separately for Sept., Oct., Nov. and
# Dec. as the prompt requires"). Fires per sheet, so a month-split table that IS pinned
# elsewhere on the same sheet passes.
_MONTH_HEAD = re.compile(r"^(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)"
                         r"(?:t?[a-z]*)?\.?$", re.I)
_PER_MONTH_PROMPT = re.compile(r"\beach of the \w+ months\b|\bby month\b|\bmonth by month\b"
                               r"|\beach month\b|\bin each of the\b[^.]{0,20}\bmonths\b", re.I)


@check(codes=['R97'], rules=['GOLD-LIVE'], needs=['prompt', 'rubric', 'solution'],
       params=['rows', 'folder'])
def check_month_split_scored(rows, folder):
    """When the prompt asks for a per-month view and a golden sheet splits its figures by month, some criterion pins one month's figure from it.

    Since: 2026-09-05 (a task rejected 2026-09-04).
    Source: task feedback.
    """
    prompt = folder / "prompt.md"
    if not prompt.exists() or not _PER_MONTH_PROMPT.search(
            prompt.read_text(encoding="utf-8", errors="ignore")):
        return
    # only a criterion that NAMES a month and states a figure counts as scoring the split.
    # A bare figure match passes on coincidence: that task's "26 catalog numbers" collided
    # with a 26 sitting in a month column and let two unscored tables through.
    month_name = re.compile(r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\b", re.I)
    stated = set()
    for _, text, weight in rows:
        if weight <= 0 or not month_name.search(text):
            continue
        for tok in re.findall(r"(?<![\w.-])(\d[\d,]*(?:\.\d+)?)(?![\w-])", text):
            try:
                stated.add(round(float(tok.replace(",", "")), 2))
            except ValueError:
                pass
    d = folder / "solution"
    for path in sorted(d.glob("*.xlsx")) if d.is_dir() else []:
        try:
            wb = workbook(path, data_only=True)
        except Exception:
            continue
        for ws in wb.worksheets:
            for row in ws.iter_rows(max_row=min(ws.max_row, 30)):
                cols = [c.column for c in row
                        if isinstance(c.value, str) and _MONTH_HEAD.match(c.value.strip())]
                if len(cols) < 3:
                    continue
                vals = set()
                for r in ws.iter_rows(min_row=row[0].row + 1):
                    for cc in cols:
                        v = ws.cell(r[0].row, cc).value
                        if isinstance(v, (int, float)) and not isinstance(v, bool) and abs(v) >= 10:
                            vals.add(round(float(v), 2))
                if len(vals) >= 8 and not (vals & stated):
                    emit("ERROR", f"[R97] {path.name} '{ws.title}' splits its figures across "
                                  f"{len(cols)} month columns and the prompt asks for the period "
                                  "month by month, but no criterion states a single figure out of "
                                  "them - a deliverable reporting one lump total for the period "
                                  "keeps full marks (a task rejected "
                                  "2026-09-04: \"no criterion requires that demand be reported "
                                  "separately for Sept., Oct., Nov. and Dec.\"). Pin one month's "
                                  "figure from this sheet")
                break


# R107 (2026-09-11, Rubric Quality Review needs_improvement): eleven positives cited
# transaction, adjustment, hold and receipt ids
# (TXN-644093, ADJ-690649, HLD-4101, ...) that sit at rows 122 to 407 of the input logs. The
# review reads each sheet through a window of about 28 rows (TXN-641436 at row 30 was the last
# transaction it named) and rated every one of them [critical] ungrounded_verification: "could
# not be verified in the agent-visible source files". The ids were real; the window was the
# problem, and PR1 already said so for worked examples. This arm is mechanical: an id-shaped
# token a positive pins that the inputs carry only past the window, and no docx or the prompt
# carries at all, cannot be grounded by the review.
_R107_ID_RE = re.compile(r"\b[A-Z]{2,5}(?:-[A-Z]{2,5})?-\d{3,}\b")
_R110_CITE_RE = re.compile(r"\bcit(?:e|es|ed|ing)\b|\b(?:record|transaction|adjustment|receipt) ids?\b"
                           r"|\bon the (?:transaction|adjustment|receiving) log\b", re.I)
_R107_WINDOW = 28


def _r107_id_rows(folder):
    """id token -> {input file name: lowest sheet row (1-based, header counted)}."""
    import csv
    pos = {}
    d = folder / "inputs"
    for path in sorted(d.glob("*")) if d.is_dir() else []:
        rows = None
        if path.suffix.lower() == ".xlsx":
            try:
                wb = workbook(path, data_only=True)
            except Exception:
                continue
            rows = ((i, row) for ws in wb.worksheets
                    for i, row in enumerate(ws.iter_rows(values_only=True), 1))
        elif path.suffix.lower() == ".csv":
            try:
                rows = enumerate(csv.reader(path.open(encoding="utf-8", errors="ignore")), 1)
            except Exception:
                continue
        if rows is None:
            continue
        for i, row in rows:
            for v in row:
                if isinstance(v, str) and "-" in v:
                    for tok in _R107_ID_RE.findall(v):
                        per = pos.setdefault(tok, {})
                        if i < per.get(path.name, 10 ** 9):
                            per[path.name] = i
    return pos


_R132_ROUNDING_RE = re.compile(
    r"round(?:ed|ing|s)? up|next \.9\d|next (?:whole|full) (?:case|pack|unit)|rounded to the next", re.I)
_R132_CONDITION_RE = re.compile(
    r"at or above|clears?\b|clearing|not below|no lower than|end(?:s|ing)? in \.\d\d"
    r"|whole (?:cases|packs|units)|multiple of|rounded? (?:up|to)", re.I)
_R132_VALUE_RE = re.compile(
    r"\blowest\b|\bsmallest\b|\bnext\b|\bnearest\b|\bminimum\b|\bexactly\b|\bround(?:s|ed)? up to\b", re.I)


@check(codes=['R132'], rules=['PRE-COVER'], needs=['rubric', 'inputs'], params=['rows', 'folder'])
def check_rounding_rule_graded_on_value(rows, folder):
    """A rounding rule the prompt or an input states is graded on the value it produces, never only on conditions a higher value also meets.

    Since: 2026-09-15 (a rejection finding).
    Source: the rubric coverage axis - the memo's rule 6 says a floor-moved price
    "rounds up to the next figure ending in .95", while the rubric graded only that each repriced
    price sat at or above the floor and ended in .95, so "an inflated .95 price would still earn
    full credit"; the repair was one row in the rule's own words, "the next figure ending in .95
    at or above the margin floor".
    Drift-notes: fires when the prompt or an input carries round-up language, some positive grades
    a condition (at or above, clears, ends in .95, whole cases, multiple of) and no such condition
    row names the value (lowest, smallest, next, nearest, minimum, exactly, rounds up to). Probed
    2026-09-15 over every rubric in submissions/: fires on this task alone.
    """
    corpus = " ".join(_source_docs(folder).values())
    if not _R132_ROUNDING_RE.search(corpus):
        return
    cond = [(num, text) for num, text, weight in rows if weight > 0 and _R132_CONDITION_RE.search(text)]
    if not cond or any(_R132_VALUE_RE.search(text) for _, text in cond):
        return
    nums = " and C".join(str(n) for n, _ in cond)
    emit("ERROR", f"C{nums} [R132] grade the sources' rounding rule (\"{_R132_ROUNDING_RE.search(corpus).group(0)}\") "
                  "only by conditions any higher value also meets, so an inflated figure that clears them earns "
                  "full credit - the coverage axis failed a task on exactly this (2026-09-15: "
                  "floor clearance and a .95 ending, never the next .95). Grade the value the rule produces, in "
                  "the source's own words")


@check(codes=['R107', 'R110'], rules=['RUBQ-GROUND'], needs=['rubric', 'inputs'], params=['rows', 'folder'])
def check_ids_inside_review_window(rows, folder):
    """A positive never pins a record id, or claims a citation of a key's records, that the input sheets carry only past row 28.

    Codes:
      R107  a record id a positive pins sits only past row 28 of the input sheets and in no docx or the prompt
      R110  a positive claims the deliverable cites records for a key (a SKU, an account) whose rows in some input sheet all sit past row 28
    Since: R107 2026-09-11; R110 the same task, later,
    when the id-free rewrite ("cites by transaction id the outbound pick transactions" for HAT-FRG-1001) drew the
    same [critical] ungrounded_verification six times over: the review looks for the key's records, not the id.
    Source: the Agentic Rubric Quality Review (ungrounded_verification, critical and major).
    Drift-notes: the window is the 28 rows PR1 records; an id absent from every input is another
    check's business (R20/R21 read the golden), so only a present-but-deep id errors here. R110 needs
    a key token in the row; a citation claim over an unnamed set ("each of the five SKUs") is not
    caught and is answered by writing the row as the memo's reasoning, never as what a log shows.
    """
    toks = {}
    for num, text, weight in rows:
        if weight <= 0:
            continue
        for tok in _R107_ID_RE.findall(text):
            toks.setdefault(tok, num)
    if not toks:
        return
    prose = ""
    for name, text in _source_docs(folder).items():
        if name.lower().endswith(".docx") or name == "prompt.md":
            prose += " " + text
    pos = _r107_id_rows(folder)
    # R110: a citation claim about a key whose records some input sheet holds only past the window
    for num, text, weight in rows:
        if weight <= 0 or not _R110_CITE_RE.search(text):
            continue
        for tok in sorted(set(_R107_ID_RE.findall(text))):
            per = pos.get(tok)
            if not per:
                continue
            deep_files = sorted(f"{f} (row {r})" for f, r in per.items() if r > _R107_WINDOW)
            if deep_files:
                emit("ERROR", f"C{num} [R110] claims the deliverable cites records for {tok}, and the input sheets "
                             f"carry that key only past row {_R107_WINDOW} in {', '.join(deep_files)}; the Rubric "
                             "Quality Review looks for the key's records inside its window, id or no id, and "
                             "rated the id-free wording [critical] ungrounded_verification again "
                             "(2026-09-11). Write the row as what the "
                             "memo's explanation states, never as what a log shows or what it cites")
                break
    deep = sorted((min(pos[t].values()), t, n) for t, n in toks.items()
                  if t in pos and min(pos[t].values()) > _R107_WINDOW and t not in prose)
    if not deep:
        return
    by_row = ", ".join(f"{t} (C{n}, row {r})" for r, t, n in deep[:8])
    emit("ERROR", f"[R107] {len(deep)} record id(s) pinned by positives sit only past row {_R107_WINDOW} "
                 f"of the input sheets and in no docx or the prompt: {by_row}. The Rubric Quality Review "
                 "reads each sheet through a window of about 28 rows and rated every such id "
                 "[critical] ungrounded_verification (2026-09-11). "
                 "Score the deliverable's property instead (cites the records by id, states their "
                 "status) and keep the id out of the criterion")
