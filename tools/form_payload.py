#!/usr/bin/env python3
"""Build the Hazy Helper payload from a task folder.

    .venv/bin/python tools/form_payload.py drafts/01-my-task
    .venv/bin/python tools/form_payload.py drafts/01-my-task -o form-payload.json

Reads the folder's own artifacts and writes the JSON the extension fills the form from:

    metadata.json   domain, occupation, the five time values, the tools list
    instruction.md       the task instruction, verbatim
    rubric-*.csv    one criterion per rubric row, with its weight
    inputs/         the Input File List, one entry per file
    solution/       the Output File List, one entry per deliverable

The form wants each input listed as "name - what it contains", so for every input file this
looks through instruction.md for the sentence that names it and offers that as the gloss. The
prompt is written to name every input and say what it holds, so the sentence is usually
there; where it is not, the entry is left as the bare filename and called out in the report.
Nothing is invented.

File uploads are not part of the payload. A page cannot set a file input from a path, so
both zips are attached by hand.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

TIME_KEYS = [
    ("read", "time_read_minutes"),
    ("files", "time_files_minutes"),
    ("work", "time_work_minutes"),
    ("qa", "time_qa_minutes"),
]

SKIP = {".DS_Store"}


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as exc:
        sys.exit(f"{path}: not valid JSON ({exc})")


def sentences(text: str) -> list[str]:
    """Split on sentence ends, keeping bullet and line breaks as boundaries too."""
    parts = re.split(r"(?<=[.!?])\s+|\n+", text)
    return [re.sub(r"\s+", " ", p).strip(" -*\t") for p in parts if p.strip()]


def gloss_for(name: str, sents: list[str], all_names: list[str]) -> str | None:
    """The shortest sentence that describes THIS file, or None.

    A prompt usually carries one sentence that simply lists every attached file. That
    sentence names this file, but says nothing about it, and using it would give every
    input the same meaningless description. So any candidate naming more than one input is
    rejected, and a file with no sentence of its own gets no gloss rather than a borrowed
    one. An operator can always write a better line than a wrong line.
    """
    others = [n for n in all_names if n != name]
    stems = {n: Path(n).stem for n in others}

    hits = [s for s in sents if name in s and not any(o in s for o in others)]
    if not hits:
        stem = Path(name).stem
        hits = [
            s for s in sents
            if stem and stem in s and not any(v and v in s for v in stems.values())
        ]
    if not hits:
        return None
    best = min(hits, key=len)
    best = re.sub(r"^[^A-Za-z0-9]*" + re.escape(name) + r"\s*[-,:\u2014]?\s*", "", best)
    best = best.strip(" .")
    # A leftover list fragment ("and", "in the folder") is not a description.
    return best if len(best.split()) >= 3 else None


def listing(folder: Path) -> list[str]:
    if not folder.is_dir():
        return []
    return sorted(
        p.name
        for p in folder.iterdir()
        if p.is_file() and p.name not in SKIP and not p.name.startswith("~$")
    )


def rubric_from(folder: Path, report: list[str]) -> list[dict]:
    csvs = sorted(folder.glob("rubric-*.csv")) or sorted(folder.glob("*.csv"))
    csvs = [c for c in csvs if c.parent == folder]
    if not csvs:
        report.append("no rubric CSV in the task folder; rubric left empty")
        return []
    if len(csvs) > 1:
        report.append(f"{len(csvs)} rubric CSVs; used {csvs[0].name}")
    rows: list[dict] = []
    bad = 0
    with open(csvs[0], newline="", encoding="utf-8-sig") as fh:
        for row in csv.DictReader(fh):
            text = (row.get("CRITERION") or "").strip()
            if not text:
                continue
            raw = (row.get("WEIGHT") or "").strip()
            try:
                w = float(raw)
            except ValueError:
                bad += 1
                rows.append({"description": text, "weight": ""})
                continue
            rows.append({"description": text, "weight": int(w) if w == int(w) else w})
    if bad:
        report.append(f"{bad} criterion row(s) have no numeric weight; left blank on the form")
    return rows


def build(folder: Path) -> tuple[dict, list[str]]:
    report: list[str] = []
    meta = load_json(folder / "metadata.json")
    if not meta:
        report.append("no metadata.json; domain, occupation, times and tools are empty")

    prompt_path = folder / "instruction.md"
    prompt = prompt_path.read_text(encoding="utf-8").strip() if prompt_path.exists() else ""
    if not prompt:
        report.append("no instruction.md; task instruction is empty")
    sents = sentences(prompt)

    inputs = []
    names = listing(folder / "inputs")
    for name in names:
        g = gloss_for(name, sents, names)
        if g:
            inputs.append(f"{name} - {g}")
        else:
            inputs.append(name)
            report.append(
                f"inputs/{name}: the prompt lists it but never describes it on its own; "
                "entry is the bare filename, add the description by hand"
            )
    if not inputs:
        report.append("inputs/ is empty or missing")

    outputs = listing(folder / "solution")
    if not outputs:
        report.append("solution/ is empty or missing; output file list is empty")

    times = {}
    for key, mkey in TIME_KEYS:
        if meta.get(mkey) is not None:
            times[key] = meta[mkey]
        else:
            report.append(f"metadata has no {mkey}")
    if meta.get("total_time_hours") is not None:
        times["total_hours"] = meta["total_time_hours"]
    else:
        report.append("metadata has no total_time_hours")

    occ = meta.get("onet_occupation") or {}
    payload = {
        "domain": meta.get("domain", ""),
        "occupation": occ.get("title", ""),
        "occupation_code": occ.get("code", ""),
        "task_instruction": prompt,
        "input_files": inputs,
        "output_files": outputs,
        "times": times,
        "tools": list(meta.get("tools") or []),
        "rubric": rubric_from(folder, report),
    }
    if not payload["tools"]:
        report.append("metadata has no tools; the form requires at least one non-AI tool")
    if not payload["domain"] or not payload["occupation"]:
        report.append("domain or occupation missing; section 1 cannot be filled")
    return payload, report


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("folder", help="the task folder, e.g. drafts/01-my-task")
    ap.add_argument("-o", "--out", help="where to write (default: <folder>/form-payload.json)")
    ap.add_argument("--stdout", action="store_true",
                    help="print the JSON alone on stdout, report on stderr, so it can be piped")
    args = ap.parse_args()

    folder = Path(args.folder)
    if not folder.is_dir():
        sys.exit(f"{folder} is not a directory")

    payload, report = build(folder)
    text = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"

    # With --stdout the JSON has to be the ONLY thing on stdout, or piping it into anything
    # that parses JSON fails on the trailing report. The report still gets printed, just on
    # stderr where a pipe will not swallow it.
    if args.stdout:
        print(text, end="")
        log = sys.stderr
    else:
        dest = Path(args.out) if args.out else folder / "form-payload.json"
        dest.write_text(text, encoding="utf-8")
        log = sys.stdout
        print(f"wrote {dest}", file=log)

    r = payload["rubric"]
    print(
        f"  instruction {len(payload['task_instruction'])} chars | "
        f"{len(payload['input_files'])} input(s) | {len(payload['output_files'])} output(s) | "
        f"{len(r)} criteria | {len(payload['tools'])} tool(s)",
        file=log,
    )
    if r:
        nums = [c["weight"] for c in r if isinstance(c["weight"], (int, float))]
        pos = sum(w for w in nums if w > 0)
        neg = sum(w for w in nums if w < 0)
        print(f"  rubric weights: +{pos:g} / {neg:g}", file=log)
    for line in report:
        print(f"  note: {line}", file=log)
    print("  uploads are not in the payload; attach both zips by hand", file=log)
    return 0


if __name__ == "__main__":
    sys.exit(main())
