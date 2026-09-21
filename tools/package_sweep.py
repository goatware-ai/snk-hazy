#!/usr/bin/env python3
"""Mechanical packaging sweep across every task folder. Reports, never edits.

    .venv/bin/python tools/package_sweep.py [root...]      # default: submissions drafts

Run at the start of a revision: fix only the task named in the revision, report the rest.
The per-file inspection lives in tools/gcheck/authorship/package.py (inspect); this file
is the command. The repair is tools/office_resave.py.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gcheck.authorship.package import inspect, office_files, sweep_main  # noqa: E402,F401

if __name__ == "__main__":
    sys.exit(sweep_main(sys.argv[1:]))
