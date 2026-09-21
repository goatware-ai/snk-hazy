#!/usr/bin/env python3
"""Lint rubric CSV files for wording patterns that fail the AutoEval oracle judge.

    .venv/bin/python tools/rubric_lint.py                          # every rubric under submissions/
    .venv/bin/python tools/rubric_lint.py path/to/rubric-{task-name}-{uid8}.csv

The rules live in tools/gcheck/golden_rubric/lint.py (their catalog is its docstring);
this file is the command. The gate runs the same rules through check_rubric_lint.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gcheck.golden_rubric.lint import lint_file, main  # noqa: E402,F401

if __name__ == "__main__":
    sys.exit(main(sys.argv))
