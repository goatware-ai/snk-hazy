#!/usr/bin/env python3
"""Evidence harness for reviewing another contributor's Hazy task.

    .venv/bin/python tools/review_check.py reviews/<review-id>
    .venv/bin/python tools/review_check.py --lint-note reviews/<review-id>   # the worksheet's Note against the note standard

The harness lives in tools/gcheck/review.py; this file is the command. It reads the
fetch-task JSON and the two zips in the folder, stages them as a task-shaped folder, and
runs the same registered checks the submission gate runs, tiered against the reviewer bar.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gcheck.review import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main(sys.argv))
