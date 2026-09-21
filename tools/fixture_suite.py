#!/usr/bin/env python3
"""Planted-defect fixtures for the gate: prove each check still fires on the artifact that motivated it
and stays silent on the corrected one, and report how much of the catalog has a fixture.

    .venv/bin/python tools/fixture_suite.py            # every fixture, then coverage
    .venv/bin/python tools/fixture_suite.py package-corrected  # named fixtures only

A fixture is a folder under tools/check_fixtures/ with a fixture.json:

    {"about": "...",
     "base": "other-fixture",                 # optional: copy that fixture first, then this folder over it
     "chmod": {"instruction.md": 0},               # optional: file modes applied in the temporary copy
     "fires":  [{"code": "G41", "criterion": "3", "contains": "text"}],   # ERROR lines that must appear
     "silent": [{"code": "R55", "criterion": "2"}],                       # ERROR lines that must not
     "stdout_contains": ["..."], "silent_contains": ["..."]}              # raw gate output either way

Each fixture runs in a temporary copy outside the repository, so git history never moves a date
check's build date. Since 2026-09-15 (rule-catalog cleanup): 162 of 260 codes fired on none of 68
task folders, which cannot tell a working check from a dead one; a fixture can.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "tools" / "check_fixtures"
LINE_RE = re.compile(r"^\s*ERROR\s+(?:C(\d+)(?:\s+and\s+C\d+)?\s+)?\[([A-Z]+\d+[a-z]?)\]\s*(.*)$")


def _materialise(name, dest):
    spec = json.loads((FIXTURES / name / "fixture.json").read_text())
    if spec.get("base"):
        _materialise(spec["base"], dest)
    for src in (FIXTURES / name).rglob("*"):
        if src.is_file() and src.name != "fixture.json":
            target = dest / src.relative_to(FIXTURES / name)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, target)
    return spec


def run_fixture(name):
    tmp = Path(tempfile.mkdtemp(prefix="fixture-"))
    folder = tmp / name
    folder.mkdir()
    spec = _materialise(name, folder)
    for rel, mode in spec.get("chmod", {}).items():
        os.chmod(folder / rel, mode)
    try:
        out = subprocess.run([sys.executable, str(ROOT / "tools" / "autoeval_check.py"), str(folder)],
                             capture_output=True, text=True, timeout=900).stdout
    finally:
        for rel in spec.get("chmod", {}):
            os.chmod(folder / rel, 0o644)
        shutil.rmtree(tmp, ignore_errors=True)
    errors = [(m.group(1), m.group(2), m.group(3)) for m in map(LINE_RE.match, out.splitlines()) if m]
    def hit(want):
        return any(code == want["code"] and (not want.get("criterion") or crit == want["criterion"])
                   and want.get("contains", "") in msg for crit, code, msg in errors)
    problems = [f"expected {w} to fire" for w in spec.get("fires", []) if not hit(w)]
    problems += [f"expected {w} to stay silent" for w in spec.get("silent", []) if hit(w)]
    problems += [f"expected output to contain {t!r}" for t in spec.get("stdout_contains", []) if t not in out]
    problems += [f"expected output not to contain {t!r}" for t in spec.get("silent_contains", []) if t in out]
    asserted = {w["code"] for w in spec.get("fires", []) + spec.get("silent", [])}
    return problems, asserted


def main(argv):
    names = argv[1:] or sorted(p.name for p in FIXTURES.iterdir() if (p / "fixture.json").is_file())
    covered, failed = set(), 0
    for name in names:
        problems, asserted = run_fixture(name)
        covered |= asserted
        print(f"{'FAIL' if problems else 'ok  '}  {name}")
        for p in problems:
            print(f"        {p}")
        failed += bool(problems)
    sys.path.insert(0, str(ROOT / "tools"))
    from gcheck import checks, core  # noqa: F401
    registered = set(core.BY_CODE)
    print(f"\n{len(names) - failed} of {len(names)} fixtures pass; {len(covered & registered)} of "
          f"{len(registered)} check codes carry a fixture assertion")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
