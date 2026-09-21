"""The submission-side driver: what `tools/autoeval_check.py` runs.

    autoeval_check.py [--no-caches] [--brief] [--record-debt] [--originality] [--catalog] [--selfcheck] [--rules] [task-folder ...]

Runs every registered check over a task folder (grouped by the artifact under test, in
registration order inside each group) over one shared TaskState, then prints the
consolidated gate view from gate_families. No args = every folder under submissions/.
"""
import contextlib
import datetime
import io
from pathlib import Path

from . import core, checks  # noqa: F401  (importing `checks` populates the registry)
from .common import load_rows, rubric_path
from .state import TaskState
from .core import emit, FINDINGS, DEBT_HIT, RECOMMENDATIONS, REPORT, ROLLUP
import gate_families

GROUP_TITLES = {
    "prompt_inputs": "[1] Prompt and input files",
    "golden_rubric": "[2] Golden solution and rubric",
    "authorship": "[3] LLM authorship of shipped files",
    "packaging": "[4] Packaging and hygiene",
}


def task_available(folder):
    """The needs a task folder can satisfy, plus its parsed rubric rows (None when the CSV is missing).

    Every need is offered except the rubric ones when the CSV is missing, which reproduces
    the old gate's early return: one 'rubric CSV missing' error and no rubric checks. A
    check that handles an absent prompt.md or inputs/ itself (P0, for instance) still runs,
    because that absence is a finding, not a reason to skip.
    """
    available = set(core.NEEDS)
    if not core.OPTIONS["originality"]:
        # U1/U2 and G2b are build-time gates for the task being built (user, 2026-08-22);
        # G2c and G2d, retired 2026-09-15, held portfolio-wide on the python-docx template
        # (2026-09-02), so they stay opt-in here and always-on in review.
        available.discard("originality")
    rows = None
    path = rubric_path(folder)
    if path.exists():
        rows = load_rows(path)
    else:
        emit("ERROR", f"rubric CSV missing (expected {path.name})")
        available.discard("rubric")
    return available, rows


def _criterion_count(folder):
    """Rows with a CRITERION, numeric weight or not (the rollup's denominator)."""
    path = rubric_path(folder)
    if not path.exists():
        return 0
    bad = []
    rows = load_rows(path, bad=bad)
    return len(rows) + sum(1 for _, text, _ in bad if text)


def run(folder, skip_caches=False, brief=False):
    folder = Path(folder)
    print(f"== {folder} ==")
    core.reset()
    core.OPTIONS["skip_caches"] = skip_caches
    core.load_debt(folder)
    # --brief keeps the per-check detail out of the way: the consolidated gate view is
    # what a submission decision is actually made on, and 80 future-date lines bury it.
    sink = io.StringIO() if brief else None
    with (contextlib.redirect_stdout(sink) if brief else contextlib.nullcontext()):
        _run_checks(folder)
    _finish(folder, brief)


def _run_checks(folder):
    available, rows = task_available(folder)
    state = TaskState(folder, rows)
    seen = []

    def heading(c):
        if not seen or seen[-1] != c.group:
            seen.append(c.group)
            print(GROUP_TITLES.get(c.group, c.group))
    def crashed(c, exc):
        # one check that trips must not hide every check after it (2026-09-15: a PermissionError
        # in the packaging sweep stopped a 22-task run after two folders)
        emit("ERROR", f"check {c.name} crashed with {type(exc).__name__}: {exc}; the remaining "
                      "checks still ran, fix the check")
    core.run_checks(state, available, rows, on_check=heading, on_error=crashed)


def _finish(folder, brief):
    if brief and RECOMMENDATIONS:
        # --brief swallows per-check output; a non-blocking finding still has to be seen
        # or the tier is just a delete with extra steps.
        for msg in RECOMMENDATIONS:
            print(f"  REC   {msg}")
    hit = {(n or "", c) for c, n in DEBT_HIT}
    stale = [f"{'C' + n + ' ' if n else ''}{c}" for (n, c) in core.DEBT if (n, c) not in hit]
    if stale:
        # debt keyed to a renamed id or a finding since fixed shelters nothing and misleads the reader
        # (one task carried R39 lines after R39 became R90/R91; another two R9 lines no longer firing)
        print(f"  NOTE  .gate-debt line(s) matched no finding this run: {', '.join(stale)}; clear them at "
              "the task's next revision")
    holes = gate_families.unmapped({c for _, c, _, _ in FINDINGS if c})
    if holes:
        print(f"  NOTE  coded checks with no generalized rule: {', '.join(holes)} — "
              "add them to tools/gate_families.py PRIMARY")
    v = gate_families.report(list(FINDINGS), _criterion_count(folder), DEBT_HIT)
    ROLLUP.append((folder, v, _criterion_count(folder),
                   len({n for _, c, n, _ in FINDINGS if c in gate_families.FLAKE_CLASS and n})))
    print()


def _record_debt(folder):
    """Write every finding currently open on a task into its .gate-debt file.

    The migration path off the advisory tier: a task submitted before a check existed carries
    that check's findings as debt, not as a fault. Run once per in-flight task, then
    every NEW finding errors normally.
    """
    rows = [(n or "", c, m) for lvl, c, n, m in FINDINGS if c and lvl == "ERROR"]
    path = Path(folder) / ".gate-debt"
    lines = ["# Findings open when this file was written: checks added after the task was",
             "# submitted. Each line is one finding, not one rule — the same rule firing on",
             "# another criterion still errors. Clear a line when you fix it.",
             f"# recorded {datetime.date.today().isoformat()} by autoeval_check.py --record-debt", ""]
    for num, code, msg in sorted(rows, key=lambda r: (r[1], int(r[0]) if r[0] else 0)):
        key = f"C{num} {code}" if num else code
        lines.append(f"{key:12s} = predates the check; {msg.split(' — ')[0][:70]}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote {path} with {len(rows)} findings")


def _rollup():
    """One line per task: which lifecycle stage it would trip, and its oracle odds."""
    print("== gate rollup ==")
    stages = ["PRE", "AUTO", "HUMAN"]
    print(f"  {'task':34s} {'crit':>4} {'flaky':>5} {'P(3/3)':>7}  " +
          "  ".join(f"{s:6s}" for s in stages))
    worst = []
    for folder, v, ncrit, nflaky in ROLLUP:
        cells = []
        for st in stages:
            e = sum(x[3] for x in v.values() if x[0] == st)
            d = sum(x[4] for x in v.values() if x[0] == st)
            cells.append("FAIL" if e else ("debt" if d else "ok"))
        p = gate_families.exposure(ncrit, nflaky)
        # exposure() has no estimate for some folders (see its docstring); print n/a rather than
        # crash the rollup before the TOTAL line (2026-09-15)
        shown = f"{p:6.0%}" if p is not None else "   n/a"
        print(f"  {folder.name:34s} {ncrit:4d} {nflaky:5d} {shown}   " +
              "  ".join(f"{c:6s}" for c in cells))
        if p is not None:
            worst.append((p, folder.name, ncrit, nflaky))
    worst.sort()
    print("\n  Lowest odds of clearing the golden solution check on one submission:")
    for p, name, ncrit, nflaky in worst[:5]:
        print(f"    {p:5.0%}  {name} ({ncrit} criteria, {nflaky} flake-prone)")
    print()


def main(argv):
    flags = {"--no-caches", "--brief", "--record-debt", "--catalog", "--originality",
             "--selfcheck", "--rules"}
    skip_caches = "--no-caches" in argv
    core.OPTIONS["originality"] = "--originality" in argv
    brief = "--brief" in argv
    record = "--record-debt" in argv
    if "--catalog" in argv:
        core.catalog()
        return 0
    # Registry hygiene runs before every gate so a regression is loud: an undeclared code,
    # a missing rule statement or a check whose family disagrees with gate_families.
    failures = core.selfcheck()
    if "--selfcheck" in argv:
        print("selfcheck: " + ("clean" if not failures else f"{len(failures)} failure(s)"))
        return 1 if failures else 0
    if failures:
        print(f"SELFCHECK FAILED: {len(failures)} registry problem(s), see above")
        return 1
    if "--rules" in argv:
        root = Path(__file__).resolve().parent.parent.parent
        out = root / "docs" / "rules.md"
        out.write_text(core.rules_markdown(), encoding="utf-8")
        print(f"wrote {out}")
        return 0
    args = [a for a in argv[1:] if a not in flags]
    root = Path(__file__).resolve().parent.parent.parent
    if args:
        folders = [Path(a.rstrip("/")) for a in args]
    else:
        folders = sorted(p for p in root.glob("submissions/*") if p.is_dir())
    for f in folders:
        run(f, skip_caches, brief)
        if record:
            _record_debt(f)
    if len(ROLLUP) > 1:
        _rollup()
    print(f"TOTAL: {REPORT['errors']} errors")
    return 1 if REPORT["errors"] else 0
