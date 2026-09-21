#!/usr/bin/env python3
"""Two gates the reviewer caught by hand on task 21 (2026-08-21).

    .venv/bin/python tools/originality_check.py submissions/NN-task-name

Runs on the ONE task folder named on the command line; there is deliberately no
sweep-everything mode (user, 2026-08-22). The checks live in gcheck: U1/U2 prompt
recycling in prompt_inputs/uniqueness.py, G2b input authorship forensics in
authorship/package.py. The gate runs both on every submission folder.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gcheck import core  # noqa: E402
from gcheck.prompt_inputs.uniqueness import check_recycling  # noqa: E402
from gcheck.authorship.package import check_input_authorship  # noqa: E402


def run(folder):
    print(f"== {folder} ==")
    print("[1] Prompt recycling")
    check_recycling(folder)
    print("[2] Input authorship forensics")
    check_input_authorship(folder)


def main(argv):
    if len(argv) < 2:
        print(__doc__.strip().splitlines()[0])
        print("\nusage: tools/originality_check.py submissions/NN-task-name")
        print("Name the one task folder to check. There is no catalogue-wide mode.")
        return 2
    for t in [Path(a) for a in argv[1:]]:
        run(t)
    print(f"\nTOTAL: {core.REPORT['errors']} errors")
    return 1 if core.REPORT["errors"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
