#!/usr/bin/env python3
"""One-command pre-flight for a task folder, against the platform's documented pipeline.

    .venv/bin/python tools/autoeval_check.py [--no-caches] [--brief] [--record-debt] submissions/NN-task-name
    .venv/bin/python tools/autoeval_check.py               # every folder in submissions/
    .venv/bin/python tools/autoeval_check.py --catalog     # every registered check, its ids, needs and rule
    .venv/bin/python tools/autoeval_check.py --selfcheck   # registry hygiene only (also runs before every gate)
    .venv/bin/python tools/autoeval_check.py --rules       # regenerate docs/rules.md from the registry
    .venv/bin/python tools/autoeval_check.py --originality submissions/NN-task-name   # + U1/U2 and G2b, for a task being built

The checks live in tools/gcheck/ (see its __init__ and tools/README.md for the layout);
this file is the command. Every check id's canonical rule is in docs/rules.md, generated
from the registry by `--rules`.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gcheck.driver import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main(sys.argv))
