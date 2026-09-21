#!/usr/bin/env python3
"""Prompt-quality checks P0-P3, in one place.

    .venv/bin/python tools/prompt_check.py submissions/NN-task-name

The rules live in tools/gcheck/prompt_inputs/prompt_frame.py beside P4 and P5; this file
is the command. The gate runs them through check_prompt_rules.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gcheck.prompt_inputs.prompt_frame import check_folder, main  # noqa: E402,F401

if __name__ == "__main__":
    sys.exit(main(sys.argv))
