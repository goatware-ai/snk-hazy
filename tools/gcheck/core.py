"""Run state, finding emission and the check registry shared by every gcheck module.

Findings are binary: a check either proves a defect (ERROR) or does not exist. The one
side channel is `recommend`, reserved for findings the programme has ruled non-blocking
in terms (today only R61). Debt (`.gate-debt`) records findings that predate the check
that reports them; they print as DEBT and are not counted.

The registry is what lets the same checks serve both entry points. Each check declares:

  codes   the check ids it can emit (`[R24]` tokens in its messages)
  rules   the generalized rules those codes map to in gate_families.PRIMARY
  needs   what it reads: prompt, rubric, inputs, solution, metadata, folder,
          and 'originality' for the build-time recycling and packet forensics (U1 U2, G2b),
          which the gate supplies only with --originality, review always, the CLI directly
  params  its positional signature, drawn from ("rows", "folder"); `folder` arrives as the
          run's TaskState (gcheck/state.py), a Path carrying every parse already made

autoeval_check runs every check whose needs the task folder satisfies; review_check builds
a task-shaped folder from the review packet and runs every check whose needs THAT folder
satisfies, so a check that reads metadata.json skips itself in review
rather than erroring on a file that never existed there.
"""
import re
import sys
from pathlib import Path

# tools/ on the path, so the sibling single-purpose tools import by bare name from any
# module of the package, however the package itself was imported.
_TOOLS = str(Path(__file__).resolve().parent.parent)
if _TOOLS not in sys.path:
    sys.path.insert(0, _TOOLS)

import gate_families  # noqa: E402

REPORT = {"errors": 0}
FINDINGS = []        # (level, code, criterion number or None, message)
DEBT_HIT = []        # (code, criterion) pairs found in .gate-debt
ROLLUP = []          # (folder, per-family verdicts, criterion count, flake-prone count)
DEBT = {}            # (criterion or "", code) -> why this finding predates the check
RECOMMENDATIONS = []
OPTIONS = {"skip_caches": False, "originality": False}

NEEDS = ("prompt", "rubric", "inputs", "solution", "metadata", "folder", "originality")


def reset():
    """Clear the per-folder state. ROLLUP accumulates across folders and is left alone."""
    FINDINGS.clear()
    DEBT_HIT.clear()
    RECOMMENDATIONS.clear()
    DEBT.clear()


def load_debt(folder):
    """Findings that predate the check that reports them, in submissions/NN-x/.gate-debt.

    Replaces .gate-accepted (2026-08-24). That file could only silence the advisory
    tier, which no longer exists: every surviving check proves a defect. But a check added
    after a task was submitted still fires on it, and that is check debt, not a fault in
    the work — blocking a task on it would stop every in-flight submission at once.

    So debt is recorded per task, per finding, and never per rule: one line
    `C17 R43 = why`, or `R32 = why` for a file-level finding. A new finding of the same
    rule on a different criterion is NOT covered and errors normally, which is the whole
    point — the file records what is already known, and cannot hide what is not.

    Write one with `autoeval_check.py --record-debt <task-folder>`.
    """
    DEBT.clear()
    path = Path(folder) / ".gate-debt"
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, _, why = line.partition("=")
        parts = key.split()
        if not parts:
            continue
        if len(parts) == 1:
            DEBT[("", parts[0].upper())] = why.strip()
        else:
            DEBT[(parts[0].lstrip("Cc"), parts[1].upper())] = why.strip()


def emit(level, msg):
    """Findings are binary: a check either proves a defect (ERROR) or does not exist.

    The advisory tier was removed 2026-08-24 (user). An advisory nobody must act on is
    noise, and worse, it gets triaged away: rossville accepted five flake-class advisories
    as risk and then flaked the oracle on one of the criteria they named. Every check
    that survives here traces to a platform failure the feedback logs record; a check
    that cannot is deleted rather than demoted.
    """
    if level != "ERROR":
        raise ValueError(f"only ERROR findings exist; got {level!r} for: {msg}")
    m = re.search(r"\[([A-Z]\d+[a-z]?)\]", msg)
    code = m.group(1) if m else None
    cm = re.match(r"C(\d+)\b", msg)
    num = cm.group(1) if cm else None
    debtable = gate_families.PRIMARY.get(code) not in gate_families.NON_DEBTABLE
    if code and debtable and (num or "", code) in DEBT:
        # Recorded, not counted. Debt does not change the artifact, so a flake-class
        # criterion carried as debt still carries its risk into the oracle: the exposure
        # estimate counts it even though the gate does not.
        DEBT_HIT.append((code, num))
        FINDINGS.append(("DEBT", code, num, msg))
        print(f"  DEBT  {msg}")
        return
    FINDINGS.append((level, code, num, msg))
    REPORT["errors"] += 1
    print(f"  {level:5s} {msg}")


def recommend(msg):
    """A finding the PROGRAM has ruled non-blocking. Not a revival of the advisory tier.

    The advisory tier died (2026-08-24) because it held checks that might or might not prove
    a defect, and nobody had to act on them. This tier holds the opposite thing: a check whose
    arithmetic is certain and whose finding the program has said in terms must never send a
    task back. Team manager, 2026-09-02, on the 20 percent penalty-weight floor: "this is a
    nice to have and not a blocking requirement to submit or get an accepted task ... it
    should never be the main reason to send a task back."

    So it prints, it never counts toward errors, and it stays out of FINDINGS so no rollup,
    debt file or stage estimate can turn it back into a gate. Nothing enters this tier on our
    own judgment that a rule feels soft: only a finding the program has explicitly downgraded,
    with the ruling quoted at the call site. Everything else is still ERROR or deleted.
    """
    RECOMMENDATIONS.append(msg)
    print(f"  REC   {msg}")


# ---- registry ---------------------------------------------------------------------------

class Check:
    __slots__ = ("name", "fn", "codes", "rules", "needs", "params", "module", "group")

    def __init__(self, fn, codes, rules, needs, params):
        self.name = fn.__name__
        self.fn = fn
        self.codes = tuple(codes)
        self.rules = tuple(rules)
        self.needs = frozenset(needs)
        self.params = tuple(params)
        mod = fn.__module__.split(".")
        self.module = ".".join(mod[1:]) if mod[0] == "gcheck" else fn.__module__
        self.group = self.module.split(".")[0]

    def __repr__(self):
        return f"Check({self.name}, codes={list(self.codes)}, needs={sorted(self.needs)})"


CHECKS = []
BY_NAME = {}
BY_CODE = {}
# Codes that legitimately belong to more than one check: one rule read on two surfaces.
SHARED_CODES = {"A6"}


def check(codes=(), rules=(), needs=(), params=("folder",)):
    """Register a check function. Refuses a duplicate name, an unknown need, and a code
    already owned by another check (the collision class the 2026-09-04 refactor removed)."""
    def deco(fn):
        c = Check(fn, codes, rules, needs, params)
        if c.name in BY_NAME:
            raise ValueError(f"duplicate check name {c.name}")
        bad = c.needs - set(NEEDS)
        if bad:
            raise ValueError(f"{c.name}: unknown needs {sorted(bad)}")
        for code in c.codes:
            owner = BY_CODE.get(code)
            if owner and owner is not c and code not in SHARED_CODES:
                raise ValueError(f"check id {code} is emitted by both {owner.name} and {c.name}")
            BY_CODE.setdefault(code, c)
        CHECKS.append(c)
        BY_NAME[c.name] = c
        return fn
    return deco


GROUP_ORDER = ("prompt_inputs", "golden_rubric", "authorship", "packaging")


def ordered_checks():
    """Registered checks grouped in GROUP_ORDER, registration order inside each group.

    Registration order is import order in checks.py; grouping keeps a module that imports a
    helper from another group (fidelity from authorship.prose) from splitting a group's
    printed section in two.
    """
    rank = {g: i for i, g in enumerate(GROUP_ORDER)}
    return sorted(CHECKS, key=lambda c: rank.get(c.group, len(rank)))


def run_checks(folder, available, rows=None, on_error=None, on_check=None):
    """Run every registered check whose needs `available` covers, over one shared TaskState.

    `folder` is the task folder (a Path) or an existing TaskState; `rows` is the parsed
    rubric (NUMBER, CRITERION, WEIGHT) when the caller already has it, else the state's own
    read. `on_error`, when given, receives (check, exception) instead of the exception
    propagating; review mode uses it so one check that trips on an unusual packet does not
    hide the rest. `on_check(check)` is called before each check that runs (the driver
    prints group headings from it). Returns the list of checks skipped for unmet needs.
    """
    from . import state as _state
    st = folder if isinstance(folder, _state.TaskState) else _state.TaskState(folder, rows)
    if rows is not None:
        st._rows = rows
    skipped = []
    previous = _state.CURRENT
    _state.CURRENT = st
    try:
        for c in ordered_checks():
            if not c.needs <= available:
                skipped.append(c)
                continue
            if on_check:
                on_check(c)
            args = [st.rows if p == "rows" else st for p in c.params]
            if on_error is None:
                c.fn(*args)
            else:
                try:
                    c.fn(*args)
                except Exception as exc:  # noqa: BLE001 - reported, not swallowed
                    on_error(c, exc)
    finally:
        _state.CURRENT = previous
    return skipped


_CODES_LINE_RE = re.compile(r"^\s*([A-Z]+\d+[a-z]?)\s{2,}(\S.*)$")


def statement(c, code=None):
    """The canonical one-sentence rule: the first line of the check's docstring.

    A check emitting several ids may carry a `Codes:` block, one line per id (`R20  ...`);
    with `code` given, that id's own line is returned when the block carries it.
    """
    doc = (c.fn.__doc__ or "").strip()
    if not doc:
        return ""
    if code:
        in_block = False
        for line in doc.splitlines():
            if line.strip().lower() == "codes:":
                in_block = True
                continue
            if in_block:
                m = _CODES_LINE_RE.match(line)
                if m and m.group(1) == code:
                    return m.group(2).strip()
                if not m:
                    in_block = False
    return doc.splitlines()[0].strip()


def catalog(out=print):
    """One line per registered check: group, name, codes, rules, needs, then its rule."""
    for c in CHECKS:
        out(f"{c.group:14s} {c.name:34s} {' '.join(c.codes) or '-':22s} "
            f"{'/'.join(c.rules) or '-':22s} needs {','.join(sorted(c.needs))}")
        out(f"{'':14s} {statement(c)}")
    out(f"{len(CHECKS)} checks, {len(BY_CODE)} check ids")


# ---- self-test ----------------------------------------------------------------------------

_CODE_LIT_RE = re.compile(r"\[([A-Z]+\d+[a-z]?)\]")


def _string_literals(module):
    """Every non-docstring string literal in a module's source, for the code-literal scan."""
    import ast
    import inspect
    src = inspect.getsource(module)
    tree = ast.parse(src)
    docs = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)):
            d = ast.get_docstring(node, clean=False)
            if d:
                docs.add(d)
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and node.value not in docs:
            yield node.value


def selfcheck(out=print):
    """Registry hygiene, run at every driver start and by `autoeval_check.py --selfcheck`.

    Fails when a registered check has no first-line docstring, when a check's own source
    emits a `[CODE]` it does not declare, when any check module carries a `[CODE]` literal
    no check in that module declares (a helper emitting for its caller), when a check's
    `rules` disagree with gate_families.PRIMARY for its codes, or when a declared code has
    no PRIMARY family. Returns the list of failures; empty means clean.
    """
    import inspect
    import sys as _sys
    failures = []
    by_module = {}
    for c in CHECKS:
        by_module.setdefault(c.fn.__module__, set()).update(c.codes)
        st = statement(c)
        if not st:
            failures.append(f"{c.name}: no first-line docstring (the canonical rule)")
        elif (re.match(r"^[A-Z]{1,2}\d+[a-z]?\b", st) or not re.search(r"[.?!)\"']$", st) or len(st) < 30):
            # 60 checks carried an id stub or a dated story cut mid-sentence here, which docs/rules.md
            # printed as the rule (2026-09-15)
            failures.append(f"{c.name}: first docstring line is not a rule sentence (opens with an id, "
                            f"stops mid-sentence or runs under 30 characters): {st[:70]}")
        try:
            src = inspect.getsource(c.fn)
        except (OSError, TypeError):
            src = ""
        for code in sorted(set(_CODE_LIT_RE.findall(src))):
            if code not in c.codes:
                failures.append(f"{c.name}: emits [{code}] but declares {list(c.codes) or 'nothing'}")
        want = {gate_families.PRIMARY.get(code) for code in c.codes}
        if None in want:
            missing = [code for code in c.codes if code not in gate_families.PRIMARY]
            failures.append(f"{c.name}: code(s) {missing} have no family in gate_families.PRIMARY")
            want.discard(None)
        if c.codes and set(c.rules) != want:
            failures.append(f"{c.name}: rules={list(c.rules)} but PRIMARY maps its codes to {sorted(want)}")
    for code, rule in gate_families.PRIMARY.items():
        if rule not in gate_families.RULES:
            failures.append(f"PRIMARY maps {code} to {rule}, which is not a RULES family, so docs/rules.md "
                            "never lists it")
    from pathlib import Path as _Path
    from .procedural import PROCEDURAL
    known = {p["id"] for p in PROCEDURAL}
    root = _Path(__file__).resolve().parents[2]
    for pattern in ("memory/*.md", "prompts/*.md", "docs/**/*.md", ".claude/**/*.md"):
        for doc in root.glob(pattern):
            try:
                cited = set(re.findall(r"(?<![\w-])PR\d{1,3}(?![\w-])", doc.read_text(encoding="utf-8", errors="ignore")))
            except OSError:
                continue
            for pr in sorted(cited - known):
                # PR18 was cited in memory and never registered, so no rules doc carried it (2026-09-15)
                failures.append(f"{doc.relative_to(root)} cites {pr}, which no procedural rule registers")
    for modname, declared in by_module.items():
        module = _sys.modules[modname]
        lits = set()
        for text in _string_literals(module):
            lits.update(_CODE_LIT_RE.findall(text))
        for code in sorted(lits - declared):
            failures.append(f"{modname}: string literal [{code}] is declared by no check in the module")
    for f in failures:
        out(f"  SELFCHECK {f}")
    return failures


# ---- rules document -----------------------------------------------------------------------

def rules_markdown():
    """docs/rules.md: every check id under its gate_families stage, family and rule, one line
    per code with the canonical statement, then the procedural rules that have no check."""
    import datetime
    from .procedural import PROCEDURAL
    gf = gate_families
    lines = [
        "# Rules",
        "",
        f"Generated by `autoeval_check.py --rules` on {datetime.date.today().isoformat()}. "
        "Do not edit by hand: the statement on each line is the first line of the check's "
        "docstring in tools/gcheck/, and the grouping is tools/gate_families.py. Regenerate "
        "after any check or family change.",
        "",
        f"{len(CHECKS)} checks, {len(BY_CODE)} check ids, {len(gf.RULES)} families, "
        f"{len(PROCEDURAL)} procedural rules.",
        "",
    ]
    by_rule = {}
    for code, rule in gf.PRIMARY.items():
        by_rule.setdefault(rule, []).append(code)

    def code_key(code):
        m = re.match(r"([A-Z]+)(\d+)([a-z]?)", code)
        return (m.group(1), int(m.group(2)), m.group(3)) if m else (code, 0, "")

    for stage, (sname, when, cost) in gf.STAGES.items():
        reports = [r for r, v in gf.REPORTS.items() if v[0] == stage]
        if not reports:
            continue
        lines += [f"## {sname}", "", f"*{when}; {cost}.*", ""]
        for rep in reports:
            _st, repname = gf.REPORTS[rep]
            lines += [f"### {repname}", ""]
            for rule, (r, oneline, _why) in gf.RULES.items():
                if r != rep:
                    continue
                codes = sorted(by_rule.get(rule, []), key=code_key)
                lines += [f"#### {rule}: {oneline}", ""]
                if not codes:
                    lines += ["- *no detector; a human check* (see gate_families.NO_DETECTOR)", ""]
                    continue
                for code in codes:
                    c = BY_CODE.get(code)
                    if c is None:
                        lines.append(f"- **{code}** — *(mapped in PRIMARY, no registered check)*")
                        continue
                    lines.append(f"- **{code}** — {statement(c, code)}")
                    lines.append(f"  <sub>{c.name} · needs {', '.join(sorted(c.needs)) or 'nothing'}</sub>")
                lines.append("")
    lines += ["## Procedural rules (not mechanically checked)", "",
              "House rules with no detector, registered in tools/gcheck/procedural.py so they carry an id.", ""]
    for r in PROCEDURAL:
        lines.append(f"- **{r['id']}** — {r['statement']}")
        lines.append(f"  <sub>{r['source']}</sub>")
    lines.append("")
    return "\n".join(lines)
