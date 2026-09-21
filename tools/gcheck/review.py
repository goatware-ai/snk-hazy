"""Evidence harness for reviewing another contributor's Hazy task (tools/review_check.py).

    .venv/bin/python tools/review_check.py reviews/<review-id>

Since 2026-09-04 the mechanical checks come from the gcheck registry: the packet is staged
as a task-shaped folder (_task/) and every registered check whose needs it satisfies runs
there, tiered BAR/HOUSE by gate_families.REVIEW_TIER. What stays review-only is the
platform verdict reading, zip role matching, the fidelity ledgers, and the few reviewer-bar
rules the registry has no check for.

This does NOT decide the review and does NOT write the note. It prints ANCHORED FACTS -
file names, criterion numbers, cell references, recomputed arithmetic - for you to read,
judge, and write up in your own words.

Expected folder. The JSON is the one required file; everything else is optional:

    reviews/<review-id>/
        review_<short>.json        REQUIRED - `stb reviews fetch-task <id> -o <dir>`
        <anything>_input_files.zip      optional - downloaded by hand from the UI
        <anything>_golden_solution.zip  optional -   "

Zip names do not matter: they are matched to their role by the filenames the JSON records,
falling back to a name pattern. The prompt and the rubric come from the JSON, so there is
no need for a prompt.md or a rubric CSV.

JSON-ONLY MODE is the normal way to run this. The fetch-task payload carries the prompt,
the criteria, the platform's OWN eval verdicts (self-containment, answer leakage) and the
per-model difficulty runs, so the platform and rubric sections all run from it alone. The
key names in that payload are not a documented schema, so they are discovered by shape
rather than assumed; the [source] lines say what was actually found.

What JSON-only CANNOT check, because it needs the bytes: packaging and file naming,
generator strings in docProps, formula liveness, every figure a criterion asserts against
the solution's own cells, and input-file substance. Those are exactly the checks that
catch machine-made packets, so when you skip the zips you are taking that work on
manually - open the files in the platform UI and judge them there.

Read the platform's verdicts first either way: they tell you what the platform already
concluded before you spend any of your two hour window.

Findings are printed in two tiers, and the distinction matters:

  [BAR]   the reviewer bar in docs/reviewer/platform/reviewer-guidelines-v5.1.md. These can
          justify a Needs Revision.
  [HOUSE] this repo's own stricter authoring conventions. They are NOT the programme's
          review bar. Never send another contributor's task back for one of these.
"""
import collections
import contextlib
import csv
import io
import json
import os
import re
import shutil
import sys
import zipfile
from pathlib import Path

from . import core, checks  # noqa: F401
from .core import FINDINGS, RECOMMENDATIONS
from .common import MONTHS_RE, load_rows, split_clauses, split_sentences
from .state import workbook, document
import gate_families

BAR, HOUSE, INFO = "BAR", "HOUSE", "INFO"
OUT = []


def say(tier, section, msg):
    OUT.append((tier, section, msg))


# --- helpers ---------------------------------------------------------------------

def _formula_count(xlsx):
    """Formula cells. Counts namespaced <x:f> as well as bare <f> - a workbook written
    with an explicit namespace prefix otherwise reads as zero formulas (observed live on
    review 40a143f2, whose 770 formulas are all <x:f>)."""
    n = 0
    with zipfile.ZipFile(xlsx) as z:
        for part in z.namelist():
            if part.startswith("xl/worksheets/sheet") and part.endswith(".xml"):
                d = z.read(part)
                n += d.count(b"<f>") + d.count(b"<f ") + d.count(b"<x:f>") + d.count(b"<x:f ")
    return n


def _numbers(text):
    return {m.replace(",", "") for m in re.findall(r"(?<![\w.-])\d[\d,]*(?:\.\d+)?(?![\w-])", text)}


def _sd(folder):
    """The submission_document out of a `stb reviews fetch-task` JSON, or None."""
    js = sorted(folder.glob("review_*.json"))
    if not js:
        return None
    d = json.load(open(js[0], encoding="utf-8"))
    return (d.get("task_documents") or [{}])[0].get("submission_document", {}), d


def _json_prompt(sd):
    """The prompt text. `prompt` is the real key (confirmed against a live payload,
    2026-08-31); the shape-based fallback stays in case the form schema changes."""
    for k in ("prompt", "user_prompt", "task_prompt"):
        v = sd.get(k)
        if isinstance(v, str) and v.strip():
            return v
    best = ""
    for k, v in sd.items():
        if isinstance(v, str) and re.search(r"prompt", k, re.I) and len(v) > len(best):
            best = v
    return best


def _json_rows(sd):
    """(number, text, weight) per criterion.

    The real shape, confirmed live 2026-08-31: sd["criteria"] is a list of form rows keyed
    `textarea-criterion` and `numeric-weight`. Take that key by name - `criteria_breakdown`
    is the same length and would otherwise be a coin flip - and keep the shape-based
    fallback for a schema change."""
    if isinstance(sd.get("criteria"), list) and sd["criteria"]:
        rows = []
        for i, item in enumerate(sd["criteria"], 1):
            text = (item.get("textarea-criterion") or "").strip()
            w = item.get("numeric-weight")
            if text and isinstance(w, (int, float)) and not isinstance(w, bool):
                rows.append((str(i), text, float(w)))
        if rows:
            return rows
    cands = []
    for k, v in sd.items():
        if isinstance(v, list) and v and isinstance(v[0], dict) and \
                re.search(r"criteri|rubric", k, re.I):
            cands.append(v)
    if not cands:
        return []
    rows = []
    for i, item in enumerate(max(cands, key=len), 1):
        text = weight = num = None
        for k, v in item.items():
            if text is None and isinstance(v, str) and v.strip() and \
                    re.search(r"criterion|text|description|statement", k, re.I):
                text = v.strip()
            if weight is None and isinstance(v, (int, float)) and not isinstance(v, bool) and \
                    re.search(r"weight|points?|score", k, re.I):
                weight = float(v)
            if num is None and re.search(r"number|index|order", k, re.I) and \
                    isinstance(v, (int, float, str)):
                num = str(v)
        if text is None:  # fall back to the longest string on the item
            strs = [v for v in item.values() if isinstance(v, str) and len(v) > 20]
            text = max(strs, key=len).strip() if strs else None
        if text and weight is not None:
            rows.append((num or str(i), text, weight))
    return rows


def _deliverable_names(sd):
    """Filenames the golden is supposed to contain. `criteria_breakdown[].matched_file` is
    the oracle saying which file it actually verified against, so it is the best signal;
    fall back to file names appearing in the criteria text."""
    # Weighted by how many criteria named each file. A matched_file can name a file the
    # oracle READ rather than the deliverable it verified: on review 2c05f81d, 16 of 17
    # criteria recorded quote_audit.xlsx and one recorded "input/quotes_raised.csv", an
    # input. Weighting by criterion count keeps the real deliverable on top; treating
    # every distinct value as equal let an input path drive the role message, and could
    # have raised a false "the deliverable is in both zips, that is leakage" BAR finding.
    names = collections.Counter(
        c["matched_file"].rsplit("/", 1)[-1]
        for c in (sd.get("criteria_breakdown") or []) if c.get("matched_file"))
    if names:
        return names
    for item in (sd.get("criteria") or []):
        for m in re.findall(r"[\w][\w\-.]*\.(?:xlsx|docx|csv|pptx|pdf)",
                            item.get("textarea-criterion") or ""):
            names[m] += 1
    return names


def _find_zips(folder):
    """Match each zip in the folder to its role: inputs or solution.

    Filenames cannot be trusted. Downloading from the platform UI names both files after
    the same submission UID, differing only by an embedded upload timestamp
    (`45d4116c-..._submission_2026-08-29T03:22:37.322Z.zip`), so the reviewer has to rename
    them and a rename in the wrong direction would silently swap two sets of findings.

    So decide by CONTENT first, and only fall back to names:

      1. the zip containing the deliverable the oracle verified against (`matched_file`)
         is the solution; the other zip is the inputs. `matched_file` is weighted by how
         many criteria carry it, because a stray value can name a file the oracle READ
         rather than the deliverable (review 2c05f81d: 16 of 17 said quote_audit.xlsx,
         one said "input/quotes_raised.csv"). Where the top-weighted name sits in BOTH
         zips the packet is broken: that is reported and the roles fall to rule 2, never
         guessed from a lower-weighted name
      2. the zip whose file count matches the declared reference-file count is the inputs
      3. the filenames the JSON records, if the UI names survived
      4. a role word in the name

    Deliberately NOT used: the upload timestamp embedded in the UID filename. The JSON puts
    03:22:37.322Z on `input_files` and 03:22:55.099Z on the golden solution, but the file
    the UI served as the INPUT zip came down named ...03_22_55.099Z (user, 2026-08-31). So
    the timestamp does not identify the role, and neither does anything else in the name.

    Ambiguity is reported, never guessed. Returns {"in": Path|None, "sol": Path|None}.
    """
    zips = sorted(folder.glob("*.zip"))
    found = {"in": None, "sol": None}
    if not zips:
        return found

    contents = {}
    for z in zips:
        try:
            with zipfile.ZipFile(z) as zf:
                contents[z] = [n for n in zf.namelist() if not n.endswith("/")]
        except zipfile.BadZipFile:
            say(BAR, "packaging", f"{z.name} is not a readable zip")

    got = _sd(folder)
    sd = got[0] if got else {}
    basis = None

    # 1. content: who holds the deliverable
    delivs = _deliverable_names(sd)
    if delivs:
        # per NAME, so a name in two zips is real duplication and a name that only
        # matches one zip cannot be dragged into a leakage claim by an unrelated one
        holders = {d: [z for z, ns in contents.items()
                       if any(d == n.rsplit("/", 1)[-1] for n in ns)] for d in delivs}
        # the deliverable is the name the most criteria were verified against. Resolve on
        # THAT name alone: if it sits in one zip the roles are settled, and if it sits in
        # two the packet is broken, so report it and let the count fallback decide rather
        # than dropping to a lower-weighted name, which on a duplicated deliverable would
        # pick an input filename and assign the roles backwards.
        top_name = max(delivs, key=lambda d: (delivs[d], d))
        if len(holders[top_name]) == 1:
            found["sol"] = holders[top_name][0]
            rest = [z for z in contents if z is not found["sol"]]
            if len(rest) == 1:
                found["in"] = rest[0]
            basis = f"content - {top_name} is in {found['sol'].name}"
        for d, zs in sorted(holders.items()):
            if len(zs) > 1:
                say(BAR, "packaging", f"{d} appears in more than one zip "
                                      f"({', '.join(z.name for z in zs)}) - if the inputs "
                                      "carry the answer file, that is leakage")

    # 2. content: declared reference-file count
    if not found["in"]:
        want = sd.get("numeric-how_many_reference_files_are_tied_to_your_prompt")
        if isinstance(want, int):
            hits = [z for z, ns in contents.items() if len(ns) == want and z is not found["sol"]]
            if len(hits) == 1:
                found["in"] = hits[0]
                basis = basis or f"content - {hits[0].name} holds the declared {want} reference files"

    # 3. the names the JSON recorded, if the UI kept them
    if not all(found.values()):
        want = {}
        f = sd.get("input_files")
        if isinstance(f, dict) and f.get("filename"):
            want["in"] = f["filename"]
        for k, v in sd.items():
            if k.startswith("s3FileUploader") and isinstance(v, dict) and v.get("filename"):
                want["sol"] = v["filename"]
                break
        for slot, name in want.items():
            if not found[slot]:
                for z in zips:
                    if z.name == name and z not in found.values():
                        found[slot] = z
                        basis = basis or "the filenames recorded in the JSON"
                        say(INFO, "packaging", "roles taken from the JSON's recorded "
                                               "filenames - confirm by opening the zips")

    # 4. last resort: a role word in the name (UID names have none, so this
    #    only fires when the submitter's own filenames survived the download)
    for slot, pat in (("in", r"input|reference"), ("sol", r"golden|solution|deliverable")):
        if not found[slot]:
            hits = [z for z in zips if re.search(pat, z.name, re.I) and z not in found.values()]
            if len(hits) == 1:
                found[slot] = hits[0]
                basis = basis or "a name pattern"

    for slot, label in (("in", "inputs"), ("sol", "solution")):
        if found[slot]:
            say(INFO, "packaging", f"{label} zip: {found[slot].name} "
                                   f"({len(contents.get(found[slot], []))} files)")
    if basis:
        say(INFO, "packaging", f"roles resolved by {basis} - names were not trusted")
    unmatched = [z.name for z in zips if z not in found.values()]
    if unmatched:
        say(BAR, "packaging", "zip(s) could not be matched to a role, so nothing was checked "
                              "against them: " + ", ".join(unmatched) + ". Open them and say "
                              "which is which - do NOT infer it from the filename")
    return found


# --- sections --------------------------------------------------------------------

def platform_verdicts(folder):
    got = _sd(folder)
    if not got:
        say(BAR, "platform", "no review_*.json in this folder - run "
                             "`stb reviews fetch-task <id> -o <folder>` (the -o matters). "
                             "Without it there are no platform verdicts and, if the zips were "
                             "not downloaded, nothing else to check either")
        return
    sd, d = got
    for key, label in (("self_containment_text_summary", "self-containment"),
                       ("golden_solution_leakage_summary", "answer leakage")):
        v = sd.get(key)
        if v:
            say(INFO, "platform", f"{label}: {v.splitlines()[0][:110]}")
    if sd.get("difficulty"):
        say(INFO, "platform", f"platform difficulty rating: {sd['difficulty']}")
    for key, label in (("dataset_quality_text_summary", "dataset quality"),
                       ("llm_authorship_text_summary", "llm authorship")):
        v = sd.get(key)
        if v:
            say(INFO, "platform", f"{label}: {v.splitlines()[0][:120]}")
    if sd.get("oracle_reward") is not None:
        say(INFO, "platform", f"oracle: reward {sd['oracle_reward']}, "
                              f"passed={sd.get('oracle_passed')}")

    stats = sd.get("all_agent_stats") or {}
    for _, s in stats.items():
        acc = s.get("accuracy")
        if acc is not None:
            say(INFO, "platform", f"difficulty: {s.get('label','model')} accuracy {float(acc):.0%} "
                                  f"over {s.get('n_runs','?')} runs, "
                                  f"rewards {s.get('run_rewards')}")
    if stats:
        # "Both models exceed 80%" binds on the LOWEST accuracy, so the worst agent is the
        # min. This read max until 2026-09-04, which printed 100% for a pair of 100%/0% and
        # read as Easy when only one model had solved it (review be517911).
        worst = min(float(s.get("accuracy", 0)) for s in stats.values())
        say(INFO, "platform",
            f"worst-agent accuracy {worst:.0%} - the check FAILs as Easy only when BOTH "
            f"models exceed 80%")

    # Per-criterion oracle results. This is the strongest rubric evidence in the payload:
    # it says, criterion by criterion, whether the judges could verify it in the golden and
    # how stable that was across runs. A criterion that passes on some runs and not others
    # is not a solid criterion, whatever the aggregate says.
    cb = sd.get("criteria_breakdown") or []
    if cb:
        stab = {}
        for c in cb:
            stab[c.get("oracle_stability", "?")] = stab.get(c.get("oracle_stability", "?"), 0) + 1
        say(INFO, "rubric", f"oracle per-criterion: {len(cb)} criteria, "
                            + ", ".join(f"{v} {k}" for k, v in sorted(stab.items())))
        for i, c in enumerate(cb, 1):
            rate = c.get("oracle_fail_rate") or 0
            if 0 < rate < 1:
                say(BAR, "rubric", f"C{i} is FLAKY for the oracle - passed "
                                   f"{c.get('oracle_pass_count')}/{c.get('oracle_run_count')} runs "
                                   f"({c.get('oracle_stability')}): \"{c.get('criterion','')[:70]}\"")
            elif rate == 1:
                say(BAR, "rubric", f"C{i} FAILED the oracle on every run: "
                                   f"\"{c.get('criterion','')[:70]}\"")

    for key, label in (("input_files", "inputs zip"), ("s3FileUploader-4243d", "solution zip")):
        f = sd.get(key)
        if isinstance(f, dict) and f.get("filename"):
            say(INFO, "packaging", f"{label} uploaded as {f['filename']}")

    if d.get("eval_revision_notes"):
        say(INFO, "platform", "this submission has prior eval revision notes: "
                              + d["eval_revision_notes"].splitlines()[0][:120])
    if d.get("revision_notes"):
        say(INFO, "platform", "prior REVIEWER revision notes exist - it has been sent back before")

    seen = set()
    for e in d.get("evaluation_display_results", []) or []:
        name = e.get("name")
        if not e.get("passed") and name not in seen:
            seen.add(name)
            say(BAR, "platform", f"platform eval FAILED: {name}: {str(e.get('details'))[:90]}")


def packaging(folder, prompt, zips):
    for slot, label in (("in", "inputs"), ("sol", "solution")):
        p = zips.get(slot)
        if not p:
            say(INFO, "packaging", f"no {label} zip in the folder - download it from the "
                                   "platform UI and drop it in; nothing that needs the file "
                                   "bytes can run without it")
            continue
        with zipfile.ZipFile(p) as z:
            names = [n for n in z.namelist() if not n.endswith("/")]
        say(INFO, "packaging", f"{label}: {len(names)} file(s) - {', '.join(names[:6])}")
        for n in names:
            if "/" in n:
                say(BAR, "packaging", f"{label}: '{n}' sits in a subfolder; the zip must be flat")
            if re.search(r"\.(xlsx|docx|csv|pdf|pptx)\.", n, re.I):
                say(BAR, "packaging", f"{label}: '{n}' has a double extension")
            if " " in n:
                say(BAR, "packaging", f"{label}: '{n}' contains a space")
        if label == "inputs":
            for n in names:
                if n not in prompt:
                    say(BAR, "packaging", f"input '{n}' is never named in the prompt")
        else:
            for n in names:
                if n not in prompt:
                    say(BAR, "packaging", f"deliverable '{n}' does not match the name the prompt asks for")


def rubric_structure(rows, prompt):
    n = len(rows)
    say(INFO, "rubric", f"{n} criteria")
    negs = [r for r in rows if r[2] < 0]
    if len(negs) < 2:
        say(BAR, "rubric", f"{len(negs)} negatively weighted criteria; the bar requires at least two")
    pos = sum(w for _, _, w in rows if w > 0)
    style_re = re.compile(r"format|font|colou?r|shading|header row|bold|layout|tab (?:is |named)|"
                          r"presentation|styled|conditional formatting", re.I)
    style = [r for r in rows if r[2] > 0 and style_re.search(r[1])]
    sw = sum(r[2] for r in style)
    if style:
        say(INFO, "rubric", f"style/formatting-looking criteria: {len(style)} of {n}, "
                            f"{sw} of {pos} positive weight")
    if len(style) * 2 >= n:
        say(BAR, "rubric", f"style/formatting criteria are {len(style)} of {n}; the bar is fewer than half")
    if pos and sw > 0.25 * pos:
        say(BAR, "rubric", f"style/formatting weight {sw} is over a quarter of positive weight {pos}")
    for num, text, w in rows:
        if re.search(r"^\s*[\[(]?[-+]?\d+\s*(?:points?|pts?|marks?)?[\])]", text) or \
           re.search(r"\[[-+]\d\]", text):
            say(BAR, "rubric", f"C{num}: a weight appears inside the criterion text; it belongs "
                               "only in the numeric weight field")
        if w > 0 and re.search(r"\b(accurate|thorough|well[- ]reasoned|appropriate|comprehensive|"
                               r"clear|robust|as needed|where appropriate)\b", text, re.I) \
                and not _numbers(text):
            say(BAR, "rubric", f"C{num}: evaluative wording with no stated value or condition - "
                               "check whether a grader could tell whether a response passes")


def golden_vs_rubric(rows, folder):
    sol = folder / "_x" / "sol"
    books = sorted(sol.glob("*.xlsx")) if sol.is_dir() else []
    if not books:
        say(INFO, "golden", "no extracted solution workbook; skipping figure verification")
        return
    values, prose = set(), []
    for b in books:
        wb = workbook(b, data_only=True)
        for ws in wb.worksheets:
            for row in ws.iter_rows():
                for c in row:
                    v = c.value
                    if isinstance(v, bool):
                        continue
                    if isinstance(v, (int, float)):
                        values.add(f"{float(v):g}")
                    elif isinstance(v, str):
                        prose.append(v)
        say(INFO, "golden", f"{b.name}: {len(wb.worksheets)} sheets, "
                            f"{_formula_count(b)} formula cells")
        if _formula_count(b) == 0:
            say(BAR, "golden", f"{b.name}: no stored formulas - the bar asks that spreadsheets "
                               "use formulas rather than hard-coded values")
    blob = " | ".join(prose)
    missing = []
    for num, text, w in rows:
        if w <= 0:
            continue
        for lit in sorted(_numbers(text)):
            if len(lit) < 3 or re.fullmatch(r"(19|20)\d\d", lit):
                continue
            try:
                norm = f"{float(lit):g}"
            except ValueError:
                continue
            if norm not in values and lit not in blob:
                missing.append((num, lit))
    if missing:
        for num, lit in missing[:20]:
            say(BAR, "golden", f"C{num}: states {lit}, which no solution cell or text carries - "
                               "verify by hand before calling it a mismatch")
    else:
        say(INFO, "golden", "every figure asserted by a positive criterion is present in the "
                            "solution's cells or prose")


def inputs_substance(folder):
    inp = folder / "_x" / "in"
    if not inp.is_dir():
        return
    for p in sorted(inp.iterdir()):
        if p.suffix.lower() == ".csv":
            rows = list(csv.reader(p.open(encoding="utf-8-sig")))
            cells = sum(1 for r in rows for v in r if v.strip())
            say(INFO, "inputs", f"{p.name}: {len(rows)-1} rows, {cells} populated cells")
        elif p.suffix.lower() == ".xlsx":
            try:
                wb = workbook(p, data_only=True)
            except Exception:
                continue   # A16 in the registry reports an unreadable workbook
            cells = sum(1 for ws in wb.worksheets for row in ws.iter_rows()
                        for c in row if c.value is not None)
            say(INFO, "inputs", f"{p.name}: {cells} populated cells across {len(wb.worksheets)} sheet(s)")
        elif p.suffix.lower() == ".docx":
            try:
                with zipfile.ZipFile(p) as z:
                    xml = z.read("word/document.xml").decode("utf-8", "ignore")
            except (KeyError, zipfile.BadZipFile):
                continue   # A16 in the registry reports an unreadable package
            words = len(re.sub(r"<[^>]+>", " ", xml).split())
            say(INFO, "inputs", f"{p.name}: ~{words} words")


# --- fidelity: the golden against the inputs and against itself ------------------------
# Added 2026-09-02 after po-conformance-review's second reviewer round. Every section above
# tests the rubric against the golden, or the golden's own package. The reviewer found four
# defects none of them can see: a convention stated in one section and broken in another
# ("an order is reported under every attribute it fails", while two over-limit orders sat
# under one attribute only); a prose count the golden's own schedule contradicts ("two
# approvals after a delegation ended", the schedule listing three); a state claim the input
# refutes ("the three open orders", two of them CLOSED in the register); and a corrective
# action the inputs do not support. This section prints the ledgers a reviewer needs to
# catch those by hand, and flags the one class it can prove: a state word in the golden
# beside a record whose status column says otherwise.

# state words on three axes; a word contradicts a record only when the record's categorical
# value sits on the SAME axis and is not the word's own value ("open" against CLOSED, never
# "open" against ACTIVE). Verbs such as approved / received are not states and are not listed.
_STATE_AXES = [
    {"open": {"OPEN"}, "closed": {"CLOSED"}, "cancelled": {"CANCELLED", "CANCELED"},
     "canceled": {"CANCELLED", "CANCELED"}},
    {"active": {"ACTIVE"}, "inactive": {"INACTIVE"}, "pending": {"PENDING"}},
    {"paid": {"PAID"}, "unpaid": {"UNPAID"}},
]
_STATE_WORDS = {w: v for axis in _STATE_AXES for w, v in axis.items()}
_AXIS_OF = {w: set().union(*axis.values()) for axis in _STATE_AXES for w in axis}
_DATEVAL_RE = re.compile(r"^\d{1,2}/\d{1,2}/\d{2,4}")
_STATE_RE = re.compile(r"\b(" + "|".join(_STATE_WORDS) + r")\b", re.I)
_STATUS_COL_RE = re.compile(r"STATUS|STATE|PAID|EMERG|FLAG|ACTIVE|OPEN|APPROV|CANCEL|PENDING|INACTIVE",
                            re.I)
_MONTH_BEFORE_RE = re.compile(r"(" + MONTHS_RE + r")\s+$", re.I)
_COUNT_RE = re.compile(
    r"\b((?:\d{1,3}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|"
    r"fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty)(?:[- ]"
    r"(?:one|two|three|four|five|six|seven|eight|nine))?)\s+(?:[a-z-]+\s+)?([a-z]{4,}s)\b", re.I)
_COUNT_NOT_NOUN = {"lists", "carries", "shows", "reads", "forms", "orders"}   # verbs after a date/number
# a sentence that states a RULE is not a claim about a record's state
_RULE_RE = re.compile(r"\b(?:required|requirement|must|should|may not|policy|section \d)\b", re.I)
_CONVENTION_RE = re.compile(
    r"\b(?:every (?:attribute|category|section|schedule|test|line)|reported under|counted "
    r"(?:once|twice|a second time)|not counted|only once|no (?:order|line|item|row|invoice|receipt) "
    r"(?:in|fails|is|was)|none of the|in every case|throughout)\b", re.I)
_ALSO_RE = re.compile(r"\b(?:also|as well|too|both|a second time|would have needed|in any case|"
                      r"whatever the)\b", re.I)
_ID_RE = re.compile(r"\b[A-Z]{0,4}-?\d{2,}-\d{2,}\b|\b\d{4,}\b")


def _docx_blocks(path):
    """[(kind, heading, text)] in document order: kind is 'p' or 'cell'; heading is the
    last short, period-free paragraph seen (the section the text sits under)."""
    try:
        from docx.table import Table
        from docx.text.paragraph import Paragraph
    except ImportError:
        return [], []
    doc = document(path)
    blocks, tables, heading = [], [], ""
    for child in doc.element.body.iterchildren():
        tag = child.tag.rsplit("}", 1)[-1]
        if tag == "p":
            t = Paragraph(child, doc).text.strip()
            if not t:
                continue
            if len(t) < 80 and not t.endswith("."):
                heading = t
            blocks.append(("p", heading, t))
        elif tag == "tbl":
            rows = [[c.text.strip() for c in r.cells] for r in Table(child, doc).rows]
            tables.append((heading, rows))
            # a column that states the RULE ("What the policy required") is not a claim
            # about the record; keep it out of the state scan
            keep = [i for i, h in enumerate(rows[0])
                    if not re.search(r"required|requirement|policy|rule", h or "", re.I)] if rows else []
            for r in rows[1:]:
                blocks.append(("cell", heading, " | ".join(r[i] for i in keep if i < len(r))))
    return blocks, tables


def _input_index(inp):
    """distinct CSV cell value -> [(file, header, row)], for values a golden sentence could
    name: identifiers (digits with a dash) or text of six characters or more. Amounts,
    dates and bare numbers are skipped, since they are ambiguous across rows."""
    idx = collections.defaultdict(list)
    for p in sorted(inp.glob("*.csv")):
        try:
            rows = list(csv.DictReader(p.open(encoding="utf-8-sig")))
        except Exception:
            continue
        if not rows:
            continue
        hdr = list(rows[0].keys())
        for r in rows:
            for k, v in r.items():
                v = (v or "").strip()
                if not v:
                    continue
                idlike = bool(re.fullmatch(r"[A-Z]{0,4}-?\d{2,}-\d{2,}", v))
                if not idlike and (len(v) < 6 or re.fullmatch(r"[\d.,/$ -]+", v)):
                    continue
                if not idlike and (k or "").upper() in ("DESCRIPTION", "NOTES", "NOTE", "COMMENT"):
                    continue
                idx[v].append((p.name, hdr, r))
    return idx


def fidelity(folder):
    sol = folder / "_x" / "sol"
    inp = folder / "_x" / "in"
    docs = sorted(sol.glob("*.docx")) if sol.is_dir() else []
    if not docs:
        say(INFO, "fidelity", "no solution .docx - the prose ledgers below need a memo golden; "
                              "for a workbook golden read the front page's prose cells the same way")
        return
    idx = _input_index(inp) if inp.is_dir() else {}
    # 0. date columns per input: a date-gated test (a cutoff, a delegation window, a limit
    # change) can be keyed on the order date or on the approval timestamp, and a golden
    # keyed on the wrong one reproduces exactly when the reviewer's recomputation makes the
    # same choice (po-conformance-review round 3, 2026-09-02: 26-0346 dated April 16,
    # approved under a departed manager's ID on April 20, missing from the schedule).
    if inp.is_dir():
        for c in sorted(inp.glob("*.csv")):
            try:
                rows = list(csv.DictReader(c.open(encoding="utf-8-sig")))
            except Exception:
                continue
            if not rows:
                continue
            datecols = [h for h in rows[0] if h and sum(
                1 for r in rows[:50] if re.match(r"\d{1,2}/\d{1,2}/\d{4}", (r.get(h) or "").strip())) >= 5]
            if len(datecols) > 1:
                say(INFO, "fidelity", f"{c.name} carries {len(datecols)} date columns ({', '.join(datecols)}): "
                                      "re-key every date-gated test in the golden on each of them and diff, "
                                      "since the policy usually names one (an approval recorded after a "
                                      "separation is the approval timestamp, not the order date)")
    # values sorted longest first so a vendor's full name wins over a prefix of it
    vals = sorted(idx, key=len, reverse=True)
    for d in docs:
        blocks, tables = _docx_blocks(d)
        sentences = []
        for kind, heading, text in blocks:
            for s in split_clauses(text):
                if s.strip():
                    sentences.append((kind, heading, s.strip()))
        # 1. table ledger: what each schedule actually carries
        for heading, rows in tables:
            if len(rows) < 2:
                continue
            ids = [r[0] for r in rows[1:] if r and _ID_RE.fullmatch(r[0] or "")]
            say(INFO, "fidelity", f"{d.name} table under \"{heading[:50]}\": {len(rows) - 1} data rows"
                                  + (f", first-column ids {ids[0]} .. {ids[-1]}" if ids else ""))
        # 2. count claims in prose, with the section they sit under
        seen = set()
        for kind, heading, s in sentences:
            if kind != "p":
                continue
            for m in _COUNT_RE.finditer(s):
                if m.group(2).lower() in _COUNT_NOT_NOUN and m.group(1).isdigit():
                    continue
                if m.group(2).lower().endswith(("ss", "us", "is")):     # business, status
                    continue
                if _MONTH_BEFORE_RE.search(s[:m.start()]):
                    continue
                key = (heading, m.group(0).lower())
                if key in seen:
                    continue
                seen.add(key)
                say(INFO, "fidelity", f"count \"{m.group(0)}\" under \"{heading[:40]}\": "
                                      f"\"{s[:110]}\" - confirm against the schedule that carries it")
        # 3. convention sentences: rules the golden sets for itself
        for kind, heading, s in sentences:
            if _CONVENTION_RE.search(s):
                say(INFO, "fidelity", f"convention under \"{heading[:40]}\": \"{s[:140]}\" - test it "
                                      "against every section it governs")
        # 4. ids named with also / as well / would have needed: which tables carry them
        table_ids = {}
        for heading, rows in tables:
            for r in rows[1:]:
                for cell in r[:2]:
                    for tok in _ID_RE.findall(cell or ""):
                        table_ids.setdefault(tok, set()).add(heading[:30] or "(untitled)")
        for kind, heading, s in sentences:
            if kind != "p" or not _ALSO_RE.search(s):
                continue
            for tok in dict.fromkeys(_ID_RE.findall(s)):
                where = table_ids.get(tok)
                if where is not None:
                    say(INFO, "fidelity", f"{tok} in \"{s[:90]}\" sits in table(s) {sorted(where)} - "
                                          "if the sentence says it fails another test too, that "
                                          "schedule must list it")
        # 5. state claims against the input record
        if not vals:
            continue
        reported = set()
        for kind, heading, s in sentences:
            sw = [w.lower() for w in _STATE_RE.findall(s)]
            if not sw or _RULE_RE.search(s):
                continue
            hits = []
            low = s
            for v in vals:
                if v in low:
                    hits.append((v, low.index(v)))
                    low = low.replace(v, " " * len(v))
                    if len(hits) >= 6:
                        break
            if not hits:
                continue
            words = [(m.group(1).lower(), m.start()) for m in _STATE_RE.finditer(s)]
            for v, at in hits:
                # the state word that governs this record is the nearest one, and only
                # within 120 characters: "the two Keuka orders are closed, and the open
                # Juniata order 26-0663" pairs 26-0663 with open, not closed
                if len({w for w, _ in words}) == 1:
                    sw = [words[0][0]]          # one state word governs every record named
                else:
                    near = sorted(words, key=lambda wp: abs(wp[1] - at))
                    sw = [near[0][0]] if near and abs(near[0][1] - at) <= 120 else []
                if not sw:
                    continue
                for fname, hdr, r in idx[v][:6]:
                    cols = [h for h in hdr if h and _STATUS_COL_RE.search(h)]
                    if not cols:
                        continue
                    state = {h: (r.get(h) or "").strip() for h in cols
                             if (r.get(h) or "").strip() and not _DATEVAL_RE.match((r.get(h) or "").strip())}
                    actual = {x.upper() for x in state.values()}
                    if not actual:
                        continue
                    contradicted = [w for w in sw
                                    if (actual & _AXIS_OF[w]) and not (actual & _STATE_WORDS[w])]
                    key = (s[:80], v, fname)
                    if key in reported:
                        continue
                    reported.add(key)
                    line = (f"\"{s[:100]}\" names {v}; {fname} row: " +
                            ", ".join(f"{h}={x}" for h, x in state.items() if x))
                    if contradicted:
                        say(BAR, "fidelity", line + f" - the sentence says '{contradicted[0]}' "
                                                    "and the record does not")
                    else:
                        say(INFO, "fidelity", line)


CATEGORIES = """
Form categories, and what the evidence above does or does not support. You decide;
these are only the places to look.

  Prompt Quality ............. voice, expert context, named files, difficulty, not answerable
                               without the inputs. MOSTLY YOUR JUDGEMENT - read the prompt aloud.
  Input File Quality ......... substance, relevance, formatting, hard-coded values. See [inputs].
  LLM-Generated: Input Files . fabricated feel, generic names, round numbers, generator strings.
  LLM-Generated: Golden Sol .. unedited model output, generic headers, hedged prose.
  Golden Solution Quality .... fails a criterion, data mismatch, not presentation ready. See [golden].
  Rubric Quality ............. atomicity, specificity, caps, negatives, file-name criterion. See [rubric].
  Suspected duplicate/template scenario or structure reused from another task. YOUR JUDGEMENT.
  No Issues - Recommend EC ... exceptional across all four components. Accept only.
  Adjudication Ready ......... no errors, but not exceptional. Accept only.
"""

MANUAL = """
Nothing above can settle these. They are the review.

  1. Read the prompt aloud. Does it sound like a practitioner handing off work, or like a
     generated task? Stacked adjectives followed by a list of failures is a send-back.
  2. Open every input file. Are they real, substantial, and necessary?
  3. Is the work genuinely 5+ hours by hand, with 3 the floor?
  4. Pick 2 to 3 rubric criteria and verify the golden actually satisfies them.
  5. Pick 2 to 3 figures in the golden and trace them to the input files.
  6. Bounded subjective criteria are VALID. Only send back criteria that name no
     conditions at all.
  7. RE-DERIVE every schedule the golden reports from the inputs with a throwaway
     script (limits by date, delegations, business days, whatever the policy sets) and
     diff it against the golden's tables. Then walk the [fidelity] ledgers above: every
     count word against the table that carries it, every convention sentence against
     every section it governs, every state word (open, closed, paid, flagged) against
     the input column, and every corrective action against the record it relies on.
     A cross-section contradiction, a count the schedule refutes, a state the register
     refutes, or an action the inputs do not support is a Golden Solution Quality
     send-back (po-conformance-review reviewer round 2, 2026-09-02, four of them).
     A recomputation that MATCHES the golden exactly proves consistency, not
     correctness: key each test on the column the policy sentence names, and where an
     input carries more than one date column, re-key every date-gated test on each and
     diff (round 3: the golden and the first recomputation both keyed a separation
     cutoff on the order date; the approval timestamp put a twelfth order in).

Then: decide, fix what falls inside your editing authority (10 min per element, 30 total
if only one element; input files can NEVER be edited), and write the note yourself -
what is wrong, why it is wrong, what to do about it, two paragraphs at most.
"""


def package_sweep_section(folder):
    """package_sweep.py per file: generator string, absPath, synthetic calcChain, codename."""
    from .authorship import package as ps
    x = folder / "_x"
    files = [p for sub in ("in", "sol")
             for p in (sorted((x / sub).iterdir()) if (x / sub).is_dir() else [])]
    if not files:
        say(INFO, "authorship", "no extracted files - package sweep skipped")
        return
    hits = 0
    for f in files:
        if f.suffix.lower() not in (".xlsx", ".docx"):
            continue
        for code, detail in ps.inspect(f):
            hits += 1
            say(HOUSE, "authorship", f"[{code}] {f.name}: {detail}")
    if not hits:
        say(INFO, "authorship",
            f"package sweep clean over {len(files)} file(s) - no generator string, "
            "absPath, synthetic calcChain or codename")


def stage_task(folder, prompt, rows, zips):
    """Lay the packet out as a task folder under _task/ so the registry checks can read it
    the way they read submissions/NN-x: prompt.md, rubric-review.csv, inputs/, solution/.

    Rebuilt on every run from the JSON and the extracted zips. Returns the folder and the
    set of needs it satisfies; metadata and the build folder never exist
    here, so checks needing them skip themselves."""
    t = folder / "_task"
    if t.exists():
        shutil.rmtree(t)
    t.mkdir()
    available = set()
    if prompt:
        (t / "prompt.md").write_text(prompt, encoding="utf-8")
        available.add("prompt")
    if rows:
        with open(t / "rubric-review.csv", "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["NUMBER", "CRITERION", "WEIGHT"])
            for num, text, weight in rows:
                w.writerow([num, text, f"{weight:g}"])
        available.add("rubric")
    x = folder / "_x"
    for sub, dest in (("in", "inputs"), ("sol", "solution")):
        if zips.get(sub) and (x / sub).is_dir():
            shutil.copytree(x / sub, t / dest)
            available.add(dest)
    if available:
        available.add("originality")   # the reviewer's own packet forensics, always
    return t, available


def registry_section(folder, prompt, rows, zips):
    """Run every gcheck check the packet can satisfy and tier its findings.

    Tier comes from gate_families.REVIEW_TIER by the check's generalized rule: BAR for the
    rules the reviewer guidelines state, HOUSE for this repo's own authoring conventions.
    A recommendation (R61) is context. A check that trips on an unusual packet is reported
    as not run rather than hiding the rest."""
    t, available = stage_task(folder, prompt, rows, zips)
    if not available:
        say(INFO, "registry", "nothing to stage - no prompt, criteria or zips in the folder")
        return
    core.reset()
    say(INFO, "registry", f"staged {t.name}/ with {', '.join(sorted(available))}; running the "
                          "gcheck registry against it")
    rows_ = [(n, txt, w) for n, txt, w in rows] if rows else None
    failed = []
    with contextlib.redirect_stdout(io.StringIO()):
        skipped = core.run_checks(t, available, rows_,
                                  on_error=lambda c, e: failed.append((c, e)))
    for level, code, num, msg in FINDINGS:
        tier = BAR if gate_families.review_tier(code) == "BAR" else HOUSE
        section = core.BY_CODE[code].group if code in core.BY_CODE else "registry"
        say(tier, section, msg.split(" \u2014 ")[0].strip())
    for msg in RECOMMENDATIONS:
        say(INFO, "registry", msg.split(" \u2014 ")[0].strip())
    # The note's LLM-authorship sentence is written from these lines (memory:
    # review-worksheet-form-only), so the prose check reports even when clean.
    prose = core.BY_NAME.get("check_llm_prose")
    if prose and prose.needs <= available and not any(f[1] == "A10" for f in FINDINGS):
        say(INFO, "authorship", "A10 prose-tell check clean over the prompt, the input .docx "
                                "files and the solution's prose cells")
    ran = len(core.CHECKS) - len(skipped) - len(failed)
    say(INFO, "registry", f"{ran} registry checks ran, {len(FINDINGS)} findings; "
                          f"{len(skipped)} skipped for needs the packet cannot supply "
                          f"({', '.join(sorted({n for c in skipped for n in c.needs - available}))})")
    for c, e in failed:
        say(INFO, "registry", f"{c.name} did not run ({type(e).__name__}: {e})")


# --- note linter -----------------------------------------------------------------------
# The Note is pasted into the platform form, so it is held to the same prose bar the review
# enforces on the task (A10) plus the phrases the platform's feedback guide and the operator
# (2026-09-04) name as reading machine-written.

# A sentence ends at .!? followed by a capital, or at a line break, since each item is its own
# line. The uppercase lookahead is what keeps "2.10 and", "5,365.50 and" and "criterion 12,"
# from reading as sentence ends.

_NOTE_BANNED = [
    (re.compile(r"^\s*(?:hi|hello|thanks|thank you)\b", re.I | re.M), "greeting or thanks"),
    (re.compile(r"\boverall\b", re.I), "\"overall\" summary opener"),
    (re.compile(r"\bdemonstrates?\b|\bshowcases?\b|\bleverag(?:e|es|ing)\b|\butili[sz](?:e|es|ing)\b", re.I), "LLM verb"),
    (re.compile(r"\bwell[- ](?:structured|organi[sz]ed|reasoned|written)\b|\bcomprehensive\b|\brobust\b", re.I), "stacked-adjective vocabulary"),
    (re.compile(r"\b(?:you )?may want to consider\b|\bconsider (?:possibly )?(?:revising|adjusting)\b|\bit (?:might|may) be worth\b", re.I), "hedged instruction"),
    (re.compile(r"\bgreat job\b|\bexcellent work\b|\bnice work\b", re.I), "praise before substance"),
    (re.compile(r"\bpartly\b", re.I), "\"partly\" (house form is \"partially\")"),
    # Operator, 2026-09-10, on the req 33 note: "carry" reads as filler when its subject is a
    # criterion, which is a piece of text and does not carry anything. Scoped to that subject on
    # purpose. A file, a cell or a document carrying a value is the precise anchoring form this
    # desk's notes are built on ("promotion_review.xlsx carries dc:creator ...", "neither CSV
    # carries a publication schedule"), and a blanket ban flagged 19 of those across the
    # worksheets written to date. This narrow form flagged 1.
    (re.compile(r"\bcriteri(?:on|a)\b[^.]{0,40}?\bcarr(?:y|ies)\b", re.I),
     "\"carry\" with a criterion as its subject (state / include / cover)"),
    (re.compile("\u2014"), "em dash"),
    (re.compile(r"\b(?:I|we) (?:verified|checked|confirmed|rebuilt|re-derived|reconciled)\b|\bwas (?:verified|checked and found|reconciled)\b|\bno (?:prohibited )?llm[- ]authorship evidence\b", re.I), "verification sentence (belongs in the chat report)"),
    # A status line on previous feedback is REQUIRED since 2026-09-04, so the old blanket ban on
    # naming the last round is gone. What stays banned is a narrative recap: retelling what the
    # previous reviewer said at length rather than giving its verdict in one line.
    (re.compile(r"\b(?:as|like) (?:the )?(?:previous|last) (?:reviewer|round|review)\b"
                r"|\bthe (?:previous|last) (?:reviewer|round) (?:noted|said|wrote|observed|asked|flagged)\b"
                r"|\bin the (?:previous|last) round,? (?:I|you|we|the EC)\b", re.I),
     "narrative recap of a prior round (give its verdict in one line instead)"),
    (re.compile(r"^\s*[-*]\s", re.M), "bullet scaffolding (use numbered items)"),
    (re.compile(r"^\s*#{1,6}\s", re.M), "markdown heading inside the note"),
    # The EC must not learn what this desk works in (operator, 2026-09-04). A defect is stated
    # as a property of THEIR file, never as what our reader did with it. Naming a generator
    # string the EC's own docProps carry is different and is not matched here: these patterns
    # look for our toolchain, not for a quoted docProps value.
    # Quoting a tool name that the EC's OWN file properties carry is the point of the finding,
    # so a mention on a line that also names docProps / a property field is not our toolchain.
    (re.compile(r"^(?!.*(?:docProps|dc:creator|dc:description|cp:lastModifiedBy|document propert|file propert|generator))"
                r".*\b(?:python-docx|openpyxl|lxml|pandas|matplotlib|BeautifulSoup)\b", re.I | re.M),
     "names our own tooling (operator 2026-09-04: keep the note to what the EC can see in their file)"),
    (re.compile(r"\.venv|(?<![\w-])pip install|\bjupyter\b", re.I), "names our own tooling"),
    (re.compile(r"\bI (?:ran|wrote|scripted)\b[^.]{0,40}\b(?:script|parser|notebook)\b", re.I),
     "says a script was run; state the defect, not how it was found"),
    # Operator, 2026-09-11: the slot opens "Optional:" on both decisions. "Not blocking:" said
    # what the item is NOT, so it still read as a deficiency the EC was expected to act on, which
    # is the opposite of what the slot is for; the platform's own feedback-best-practices.md has
    # no such slot at all and allows only what the reviewer fixed and one pattern for next time.
    # Both retired openers are banned. Matched on the subordinate clause for the older one so the
    # looser variants a note might drift into are caught by the same rule.
    (re.compile(r"\bnot why (?:this|it) is going back\b", re.I),
     "retired optional-slot opener; the slot opens \"Optional:\" on both decisions"),
    (re.compile(r"^\s*(?:\d+[.)]\s*)?Not blocking:", re.I | re.M),
     "retired optional-slot opener (operator 2026-09-11); the slot opens \"Optional:\" instead, "
     "because \"Not blocking\" names what the item is not and still reads as a fault to fix"),
]

# The four form area names the note groups its items under, per prompts/review.md.
_FORM_AREA_HEADINGS = {"Prompt", "Input files", "Golden solution", "Rubric"}


def lint_note(folder):
    """Report every phrase in the worksheet's Note that reads as generated or as filler."""
    from .authorship.prose import _TAUTOLOGY_RES, _TAUTOLOGY_OK_RE, _SLOGAN_RES, _SELF_DESCRIBING_RES
    ws = folder / "worksheet.md"
    if not ws.exists():
        print(f"no worksheet.md in {folder}")
        return 1
    text = ws.read_text(encoding="utf-8")
    m = re.search(r"^## Note\s*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    if not m:
        print("worksheet.md has no '## Note' section")
        return 1
    note = m.group(1).strip("\n")
    dm = re.search(r"^## Decision\s*\n\s*(.+)$", text, re.M)
    decision = (dm.group(1).strip() if dm else "")
    # The note groups its items under the review form's own area names when more than one
    # area is touched (prompts/review.md, "Filling the form"). "Golden solution" as a bare
    # grouping line is that required heading, not the self-describing deliverable title the
    # A10 rule hunts, so blank those lines before the prose patterns run.
    prose = "\n".join(
        "" if l.strip() in _FORM_AREA_HEADINGS else l for l in note.splitlines()
    )
    hits = []
    for rx, label in _NOTE_BANNED:
        for mm in rx.finditer(note):
            hits.append((label, mm.group(0).strip()[:60]))
    for rx in _TAUTOLOGY_RES:
        for mm in rx.finditer(prose):
            if not _TAUTOLOGY_OK_RE.search(mm.group(0)):
                hits.append(("tautology (A10)", mm.group(0).strip()[:60]))
    for rx, label in _SLOGAN_RES:
        for mm in rx.finditer(prose):
            hits.append((f"{label} (A10)", mm.group(0).strip()[:60]))
    for rx, label in _SELF_DESCRIBING_RES:
        for mm in rx.finditer(prose):
            hits.append((f"{label} (A10)", mm.group(0).strip()[:60]))
    lines = [l for l in note.splitlines() if l.strip()]
    if decision.lower().startswith("needs") and not any(re.match(r"\s*\d+[.)]\s", l) for l in lines):
        hits.append(("form", "Needs Revision note carries no numbered items"))
    # Every item names the exact place. This was question 1 of the pre-submit walk; that walk
    # stopped being reported on 2026-09-04, so the one mechanical question in it moved here.
    # An anchor is a filename with an extension, "criterion N", a Sheet!CELL or bare cell ref,
    # an XML element, or a quoted heading the EC can search for.
    _ANCHOR = re.compile(
        r"[\w-]+\.(?:xlsx|docx|pptx|csv|pdf|md|txt|zip|xml)\b"  # a named file or package part
        r"|\bcriteri(?:on|a) \d+"                                 # criterion 12
        r"|\b[A-Za-z][\w ]*![$]?[A-Z]{1,3}[$]?\d+"                # Sheet!B14
        r"|\b[A-Z]{1,3}\d+\b"                                    # B14
        r"|\bw:[a-zA-Z]+\b"                                       # an OOXML element
        r"|\brow \d+|\bparagraph\b|\bfootnote\b"
        r"|\bslides? \d+|\bappendix [A-Z]\d*"                    # a deck address: slide 7, Appendix A2
        r"|\bsection \d+(?:\.\d+)*"                              # a document address: section 7.8
        r"|[“\"][^”\"]{4,}[”\"]",                          # a quoted string to search for
        re.I)
    for l in lines:
        if not re.match(r"\s*\d+[.)]\s", l):
            continue
        body = re.sub(r"^\s*\d+[.)]\s*", "", l)
        # The optional slot opens "Optional:" on both decisions (operator, 2026-09-11,
        # replacing "Not blocking:", which replaced "Optional, not why this is going back:").
        # Both retired forms are still stripped so worksheets already submitted with them do not
        # also report a missing anchor; _NOTE_BANNED above is what stops them being written again.
        body = re.sub(r"^(?:Optional:|Not blocking:|Optional, not why this is going back:)\s*",
                      "", body, flags=re.I)
        if not _ANCHOR.search(body):
            hits.append(("form", f"item carries no anchor (name the file, criterion, cell or row): {body[:60]}"))
    if decision.lower().startswith("accept"):
        if not note.lstrip().startswith("Accepted."):
            hits.append(("form", "Accept note does not open with \"Accepted.\""))
        if len(lines) > 3:
            hits.append(("form", f"Accept note has {len(lines)} lines; the ceiling is Accepted., one line of credit, one Optional: line"))
    # A generator string is reported, never instructed (operator, 2026-09-04): the remedy for a
    # machine-made packet is authoring it differently, and telling the EC to re-save through
    # Office reads as coaching them to scrub the trace.
    _GEN = re.compile(r"docProps|dc:creator|dc:description|cp:lastModifiedBy|document propert"
                      r"|\bgenerator\b|python-docx|python-pptx|openpyxl|reportlab", re.I)
    _REMEDY = re.compile(r"\bre-?save\b|\brebuild (?:it|them|the file)\b|\bset the (?:author|creator|title|dates?)\b"
                         r"|\bclear the (?:description|field|string)\b|\bthrough (?:Excel|Word|Office)\b"
                         r"|\bgive it a title\b|\bre-?upload\b", re.I)
    for l in lines:
        if _GEN.search(l) and _REMEDY.search(l):
            hits.append(("form", f"generator-string item carries a remedy; report the finding only: {_REMEDY.search(l).group(0)}"))
    for l in lines:
        if len(l) > 600:
            hits.append(("form", f"line of {len(l)} chars; one item per line, one fix per item"))
    # Length and density (core team, #ec-geranium-project, 2026-09-10, resharing Hollie's
    # standing preference). Two paragraphs of a few sentences each, 25 sentences the absolute
    # ceiling, and no sentence so long or so packed with figures that the EC cannot act on it.
    # The complaint the team named was feedback that "feels highly synthetic and difficult to
    # action", which is what a 50-word clause carrying nine numbers reads as.
    sentences = [s.strip() for line in note.split("\n") for s in split_sentences(line, capital=True) if s.strip()]
    if len(sentences) > 25:
        hits.append(("form", f"note runs {len(sentences)} sentences; 25 is the hard ceiling"))
    for s in sentences:
        n = len(s.split())
        if n > 40:
            hits.append(("form", f"sentence of {n} words; split it so each carries one job: {s[:60]}"))
        figures = re.findall(r"(?<![\w.])[$]?\d[\d,]*(?:\.\d+)?", s)
        if len(figures) > 4:
            hits.append(("form", f"sentence carries {len(figures)} figures; name the ones the EC "
                                 f"must act on: {s[:60]}"))
    words = len(note.split())
    print(f"== note lint: {folder} ({decision or 'no decision'}, {len(lines)} lines, "
          f"{len(sentences)} sentences, {words} words) ==")
    for label, frag in hits:
        print(f"  {label}: {frag}")
    if not hits:
        print("  clean")
    return 1 if hits else 0


def main(argv):
    if len(argv) < 2:
        raise SystemExit(__doc__)
    if "--lint-note" in argv:
        targets = [a for a in argv[1:] if a != "--lint-note"]
        return max(lint_note(Path(t.rstrip("/"))) for t in targets) if targets else 1
    folder = Path(argv[1].rstrip("/"))
    prompt = (folder / "prompt.md").read_text(encoding="utf-8") if (folder / "prompt.md").exists() else ""
    rows = []
    for c in sorted(folder.glob("rubric*.csv")):
        rows = load_rows(c)
        break

    # JSON-only mode: with no `stb reviews download`, the fetch-task payload is the whole
    # assignment. Take the prompt and the criteria from it so the rubric checks still run.
    got = _sd(folder)
    if got:
        sd, _ = got
        if not prompt:
            prompt = _json_prompt(sd)
            if prompt:
                say(INFO, "source", f"prompt read from the fetch-task JSON ({len(prompt)} chars)")
        if not rows:
            rows = _json_rows(sd)
            if rows:
                say(INFO, "source", f"{len(rows)} criteria read from the fetch-task JSON")
            else:
                say(INFO, "source", "no criteria found in the JSON - the rubric checks are skipped")
    # extract zips once
    zips = _find_zips(folder)
    x = folder / "_x"
    for sub in ("in", "sol"):
        src = zips.get(sub)
        if src and not (x / sub).exists():
            (x / sub).mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(src) as zf:
                zf.extractall(x / sub)

    platform_verdicts(folder)
    packaging(folder, prompt, zips)
    if rows:
        rubric_structure(rows, prompt)
        golden_vs_rubric(rows, folder)
    inputs_substance(folder)
    fidelity(folder)
    package_sweep_section(folder)
    registry_section(folder, prompt, rows, zips)

    print(f"\n== review evidence: {folder} ==\n")
    for tier in (BAR, HOUSE, INFO):
        items = [(s, m) for t, s, m in OUT if t == tier]
        if not items:
            continue
        head = {BAR: "AGAINST THE REVIEWER BAR (can justify Needs Revision)",
                HOUSE: "HOUSE CONVENTIONS ONLY (never send a task back for these)",
                INFO: "CONTEXT"}[tier]
        print(f"  {head}")
        for s, m in items:
            print(f"    [{s}] {m}")
        print()
    print(CATEGORIES)
    print(MANUAL)
    return 0

