#!/usr/bin/env python3
"""Pre-zip audit sweeps for a task folder (generic, any task).

  .venv/bin/python tools/audit_task.py submissions/NN-task-name

The sweeps live in tools/gcheck/packaging/hygiene.py as H1-H5; this file is the command.
Exit code 1 on any failure; future dates are counted for a manual date audit, not judged.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gcheck.packaging.hygiene import main, sweep, texts  # noqa: E402,F401

if __name__ == '__main__':
    sys.exit(main(sys.argv[1].rstrip('/')))
