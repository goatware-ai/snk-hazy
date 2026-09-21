#!/usr/bin/env python3
"""Build the Hazy Helper payload from a task folder.

    .venv/bin/python tools/form_payload.py drafts/01-my-task
    .venv/bin/python tools/form_payload.py drafts/01-my-task -o form-payload.json

Reads the folder's own artifacts and writes the JSON the extension fills the form from:

    form-lists.md   the two file lists, the five times, the tools, domain and occupation
    instruction.md  the task instruction, verbatim
    rubric-*.csv    one criterion per rubric row, with its weight
    metadata.json   a fallback for anything form-lists.md does not carry
    inputs/         checked against the Input File List, both directions
    solution/       checked against the Output File List, both directions

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


def read_form_lists(folder: Path, report: list[str]) -> dict:
    """Parse form-lists.md, the hand-written entries for the form.

    This is the authoritative source and the reason the generator does not have to infer
    anything. Someone wrote each Input File List entry as the form wants it - the exact
    file name, a hyphen, then what the file contains - and recorded the times, tools,
    domain and occupation in two small tables. Deriving those from the instruction and the
    metadata is a fallback for a folder that has no form-lists.md, not the main path.

    Returns only what it finds; every key is optional.
    """
    path = folder / "form-lists.md"
    if not path.exists():
        report.append("no form-lists.md; falling back to metadata.json and instruction.md")
        return {}

    text = path.read_text(encoding="utf-8")
    out: dict = {}

    # Sections are "## <name>" and run to the next "## ".
    sections: dict[str, str] = {}
    for m in re.finditer(r"^##\s+(.+?)\s*$(.*?)(?=^##\s|\Z)", text, re.M | re.S):
        sections[m.group(1).strip().lower()] = m.group(2)

    def bullets(name: str) -> list[str]:
        body = sections.get(name, "")
        return [
            re.sub(r"\s+", " ", b.group(1)).strip()
            for b in re.finditer(r"^\s*[-*]\s+(.+?)\s*$", body, re.M)
        ]

    def table(name: str) -> dict[str, str]:
        body = sections.get(name, "")
        rows = {}
        for r in re.finditer(r"^\|([^|\n]+)\|([^|\n]+)\|\s*$", body, re.M):
            k, v = r.group(1).strip(), r.group(2).strip()
            if not k or set(k) <= set("-: ") or k.lower() == "form field":
                continue
            rows[k.lower()] = v
        return rows

    ins = bullets("input file list")
    outs = bullets("output file list")
    if ins:
        out["input_files"] = ins
    if outs:
        out["output_files"] = outs

    tt = table("times and tools")
    times = {}
    for key, pat in (
        ("read", r"read and understand"),
        ("files", r"open, ?skim"),
        ("work", r"perform the required work"),
        ("qa", r"verification"),
        ("total_hours", r"total time"),
    ):
        for k, v in tt.items():
            if re.search(pat, k, re.I):
                num = re.search(r"-?\d+(?:\.\d+)?", v)
                if num:
                    f = float(num.group(0))
                    times[key] = int(f) if f == int(f) and key != "total_hours" else f
                break
    if times:
        out["times"] = times

    for k, v in tt.items():
        if k.startswith("tool"):
            # "Microsoft Excel; Microsoft Word" -> one entry per tool
            out["tools"] = [t.strip() for t in re.split(r"[;,]", v) if t.strip()]
            break

    dom = table("domain and occupation")
    for k, v in dom.items():
        if k.startswith("domain"):
            out["domain"] = v
        elif k.startswith("occupation"):
            out["occupation"] = v
        elif "code" in k:
            out["occupation_code"] = v
    return out


def cross_check(listed: list[str], folder: Path, label: str, report: list[str]) -> None:
    """Compare the names in a form list against the files actually on disk.

    The form calls a mismatch here one of the most common reasons a submission is sent
    back, and it is invisible until the platform rejects it, so it is worth its own check.
    """
    if not folder.is_dir():
        return
    on_disk = set(listing(folder))
    named = set()
    for entry in listed:
        m = re.match(r"\s*([^\s\-]+(?:\.[A-Za-z0-9]+))", entry)
        if m:
            named.add(m.group(1))
    for missing in sorted(on_disk - named):
        report.append(f"{label}: {missing} is in {folder.name}/ but not in form-lists.md")
    for extra in sorted(named - on_disk):
        report.append(f"{label}: form-lists.md names {extra}, which is not in {folder.name}/")



def build(folder: Path) -> tuple[dict, list[str]]:
    report: list[str] = []
    meta = load_json(folder / "metadata.json")
    fl = read_form_lists(folder, report)

    prompt_path = folder / "instruction.md"
    prompt = prompt_path.read_text(encoding="utf-8").strip() if prompt_path.exists() else ""
    if not prompt:
        report.append("no instruction.md; task instruction is empty")

    # --- the two file lists ------------------------------------------------
    # form-lists.md is hand-written for the form and wins. Only when it has no list does
    # the generator fall back to naming the files and hunting the instruction for a
    # sentence that describes each one.
    if fl.get("input_files"):
        inputs = fl["input_files"]
        cross_check(inputs, folder / "inputs", "input", report)
    else:
        sents = sentences(prompt)
        names = listing(folder / "inputs")
        inputs = []
        for name in names:
            g = gloss_for(name, sents, names)
            if g:
                inputs.append(f"{name} - {g}")
            else:
                inputs.append(name)
                report.append(
                    f"inputs/{name}: no description; form-lists.md has no Input File List "
                    "and the instruction never describes this file on its own"
                )
    if not inputs:
        report.append("no input files")

    if fl.get("output_files"):
        outputs = fl["output_files"]
        cross_check(outputs, folder / "solution", "output", report)
    else:
        outputs = listing(folder / "solution")
        if not outputs:
            report.append("solution/ is empty or missing; output file list is empty")

    # --- times -------------------------------------------------------------
    times = dict(fl.get("times") or {})
    for key, mkey in TIME_KEYS:
        if key not in times:
            if meta.get(mkey) is not None:
                times[key] = meta[mkey]
            else:
                report.append(f"no {key} time (form-lists.md or metadata {mkey})")
    if "total_hours" not in times:
        if meta.get("total_time_hours") is not None:
            times["total_hours"] = meta["total_time_hours"]
        else:
            report.append("no total time (form-lists.md or metadata total_time_hours)")

    # The form's five time fields carry maxlength="5". A browser truncates a longer value
    # silently, so a total like 10.255 becomes 10.25 with no warning and the arithmetic the
    # form checks no longer holds. The gate does not know about this cap because it is a
    # property of the form, not of the task, so it is caught here.
    for key, v in list(times.items()):
        if len(str(v)) > 5:
            report.append(
                f"times.{key} is {v!r}, {len(str(v))} characters; the form's field caps at 5 "
                "and truncates the rest without saying so. Round it"
            )

    mins = [times.get(k) for k, _ in TIME_KEYS]
    if all(isinstance(m, (int, float)) for m in mins) and isinstance(
        times.get("total_hours"), (int, float)
    ):
        floor = sum(mins) / 60
        if times["total_hours"] + 1e-9 < floor:
            report.append(
                f"total {times['total_hours']}h is below the four parts "
                f"({sum(mins)} min = {floor:.2f}h); the form requires at least their sum"
            )

    # --- identity and tools ------------------------------------------------
    occ = meta.get("onet_occupation") or {}
    payload = {
        "domain": fl.get("domain") or meta.get("domain", ""),
        "occupation": fl.get("occupation") or occ.get("title", ""),
        "occupation_code": fl.get("occupation_code") or occ.get("code", ""),
        "task_instruction": prompt,
        "input_files": inputs,
        "output_files": outputs,
        "times": times,
        "tools": fl.get("tools") or list(meta.get("tools") or []),
        "rubric": rubric_from(folder, report),
    }

    # form-lists.md and metadata.json are written separately, so they can disagree.
    for key, mine in (("domain", meta.get("domain")),
                      ("occupation", occ.get("title")),
                      ("occupation_code", occ.get("code"))):
        if fl.get(key) and mine and fl[key] != mine:
            report.append(
                f"{key}: form-lists.md says {fl[key]!r}, metadata.json says {mine!r}; "
                "the form gets form-lists.md"
            )

    if not payload["tools"]:
        report.append("no tools; the form requires at least one non-AI tool")
    if not payload["domain"] or not payload["occupation"]:
        report.append("domain or occupation missing; section 1 cannot be filled")

    # Rows are typed onto the form in array order, and the form requires the general
    # formatting-and-style criterion to be the last one. R135 gates this too; it is
    # repeated here because this file is what actually gets typed.
    r = payload["rubric"]
    if r and not re.search(r"overall\b[^.]{0,40}\b(formatting|style)", r[-1]["description"], re.I):
        report.append(
            "the last criterion is not the general formatting-and-style line; rows are "
            "written in this order, so reorder the CSV before filling"
        )
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
