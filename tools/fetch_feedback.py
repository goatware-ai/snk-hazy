#!/usr/bin/env python3
"""Fetch a submitted task's feedback from the platform and write it up.

    .venv/bin/python tools/fetch_feedback.py <uid>
    .venv/bin/python tools/fetch_feedback.py <uid> --folder submissions/NN-task-name
    .venv/bin/python tools/fetch_feedback.py <uid> --json-only

Runs `stb submissions fetch-task` (and `stb submissions feedback`) read-only, then writes
`feedback-<uid8>.md` into the task folder and prints the same report.

Why not just read the notes file: `stb submissions feedback` writes a notes.txt that is
often only a header with no text in it at all. The real signal is in the fetch-task JSON,
under `eval_revision_notes` and the per-check notes inside
`evaluations[].overall_evaluation_result`. A return whose visible note says nothing is the
normal case, not an error, so this reads the JSON first and treats notes.txt as an extra.

It also diffs what the PLATFORM holds against what the repo holds, because the two can
disagree: an edit made on the platform after submission does not come back to the folder,
and a criterion changed there is invisible locally until something compares them.

Read-only. It never creates, updates or syncs anything on the platform.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

RUBRIC_DESC = "textarea-rubric_description"
RUBRIC_WEIGHT_PREFIX = "numeric-add_a_criteria_weight"
PROMPT_KEY = "task-prompt"
RUBRIC_KEY = "repeatable-bfbf1"


def run(cmd: list[str], timeout: int = 300) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except FileNotFoundError:
        sys.exit("stb not found on PATH. Install it per the Snorkel CLI user guide.")
    except subprocess.TimeoutExpired:
        sys.exit(f"{' '.join(cmd[:3])} timed out after {timeout}s")


def fetch_json(uid: str, out_dir: Path) -> dict:
    proc = run(["stb", "submissions", "fetch-task", uid, "-o", str(out_dir)])
    if proc.returncode != 0:
        sys.exit(
            f"stb submissions fetch-task {uid} failed:\n"
            + (proc.stderr or proc.stdout or "").strip()
        )
    files = sorted(out_dir.glob("*.json"))
    if not files:
        sys.exit(f"fetch-task wrote no JSON into {out_dir}")
    return json.loads(files[0].read_text(encoding="utf-8"))


def fetch_notes(uid: str) -> str:
    """The notes.txt body, minus its header. Empty is normal and not an error."""
    proc = run(["stb", "submissions", "feedback", uid])
    m = re.search(r"written to (\S+)", proc.stdout or "")
    if not m:
        return ""
    path = Path(m.group(1))
    candidates = [path] if path.is_file() else sorted(path.glob("*.txt")) if path.is_dir() else []
    for c in candidates:
        text = c.read_text(encoding="utf-8", errors="ignore")
        body = text.split("=" * 20, 1)[-1].strip() if "=" * 20 in text else text.strip()
        # Drop the identifier header; what is left is the human note, if any.
        body = re.sub(r"^(Feedback for Submission|Assignment ID|Project ID|Project):.*$", "",
                      body, flags=re.M)
        body = re.sub(r"^[=\-_]{10,}$", "", body, flags=re.M).strip()
        if body:
            return body
    return ""


def checks_from(data: dict) -> list[dict]:
    """One row per evaluation check: its name, whether it passed, and its full text."""
    rows = []
    for ev in data.get("evaluations") or []:
        overall = ev.get("overall_evaluation_result") or {}
        for note in overall.get("notes") or []:
            if not isinstance(note, dict):
                rows.append({"name": "note", "passed": None, "details": str(note)})
                continue
            rows.append({
                "name": note.get("name") or "check",
                "passed": note.get("passed"),
                "details": (note.get("details") or "").strip(),
                "suggestions": note.get("suggestions"),
                "fields": note.get("associated_fields"),
            })
    return rows


def local_rubric(folder: Path) -> list[tuple[str, str]]:
    for path in sorted(folder.glob("rubric-*.csv")):
        rows = []
        with open(path, newline="", encoding="utf-8-sig") as fh:
            for row in csv.DictReader(fh):
                text = (row.get("CRITERION") or "").strip()
                if text:
                    rows.append((text, (row.get("WEIGHT") or "").strip()))
        return rows
    return []


def platform_rubric(sd: dict) -> list[tuple[str, str]]:
    rows = []
    for item in sd.get(RUBRIC_KEY) or []:
        if not isinstance(item, dict):
            continue
        desc = (item.get(RUBRIC_DESC) or "").strip()
        weight = ""
        for k, v in item.items():
            if k.startswith(RUBRIC_WEIGHT_PREFIX):
                weight = str(v).strip()
        if desc:
            rows.append((desc, weight))
    return rows


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()


def drift(folder: Path, sd: dict) -> list[str]:
    """Where the platform's copy and the repo's copy disagree.

    An edit made on the platform after submission never reaches the folder, so a revision
    that trusts the folder alone can rewrite a criterion the platform no longer has.
    """
    out = []
    if not folder:
        return out

    inst = folder / "instruction.md"
    if inst.exists():
        if norm(inst.read_text(encoding="utf-8")) != norm(sd.get(PROMPT_KEY) or ""):
            out.append(
                "instruction.md differs from the prompt the platform holds; the platform's "
                "copy is what was graded"
            )

    mine, theirs = local_rubric(folder), platform_rubric(sd)
    if mine and theirs:
        if len(mine) != len(theirs):
            out.append(
                f"rubric row count differs: **{len(mine)}** in the CSV, "
                f"**{len(theirs)}** on the platform"
            )
        # Listing every differing row is a wall on a long rubric and says nothing about
        # WHY. Count them, name the first, and check whether the platform's rows are simply
        # a prefix of the CSV's - which is what a fill that stopped early leaves behind.
        text_diff = [
            i for i, (a, b) in enumerate(zip(mine, theirs), 1) if norm(a[0]) != norm(b[0])
        ]
        weight_diff = [
            (i, a[1], b[1])
            for i, (a, b) in enumerate(zip(mine, theirs), 1)
            if norm(a[0]) == norm(b[0]) and a[1] and b[1]
            and a[1].rstrip("0").rstrip(".") != b[1].rstrip("0").rstrip(".")
        ]
        if text_diff:
            out.append(
                f"{len(text_diff)} of {min(len(mine), len(theirs))} compared criteria differ "
                f"in text, first at row {text_diff[0]}"
            )
            a, b = mine[text_diff[0] - 1][0], theirs[text_diff[0] - 1][0]
            out.append(f"  row {text_diff[0]} CSV:      {a[:110]}")
            out.append(f"  row {text_diff[0]} platform: {b[:110]}")
        for i, a, b in weight_diff[:5]:
            out.append(f"criterion {i} weight differs: CSV {a}, platform {b}")

        # Is the platform holding a shifted or truncated copy rather than a different one?
        mset = [norm(t) for t, _ in mine]
        tset = [norm(t) for t, _ in theirs]
        missing = [t for t in mset if t not in tset]
        extra = [t for t in tset if t not in mset]
        if missing:
            out.append(
                f"{len(missing)} CSV criteria are absent from the platform entirely "
                "(a fill that stopped early leaves exactly this)"
            )
        if extra:
            out.append(f"{len(extra)} platform criteria are not in the CSV")
    return out


def resolve_folder(uid: str, given: str | None) -> Path | None:
    if given:
        p = Path(given)
        return p if p.is_dir() else None
    for base in ("submissions", "drafts", "accepted", "archived"):
        for d in sorted((REPO / base).glob("*")):
            meta = d / "metadata.json"
            if not meta.is_file():
                continue
            try:
                if (json.loads(meta.read_text()).get("taskboard_uid") or "") == uid:
                    return d
            except json.JSONDecodeError:
                continue
    return None


def report(uid: str, data: dict, notes: str, folder: Path | None) -> str:
    sd = ((data.get("task_documents") or [{}])[0].get("submission_document")) or {}
    checks = checks_from(data)
    failed = [c for c in checks if c.get("passed") is False]
    ev = (data.get("evaluations") or [{}])[0]

    L = [f"# Feedback — {uid[:8]}", ""]
    L.append(f"- **UID:** `{uid}`")
    if folder:
        L.append(f"- **Folder:** `{folder.relative_to(REPO)}`")
    L.append(f"- **Outcome:** {ev.get('outcome') or data.get('assignment_state') or 'unknown'}")
    for key, label in (
        ("eval_revision_requested_at", "Eval revision requested"),
        ("reviewer_revision_requested_at", "Reviewer revision requested"),
        ("expiry_time", "Expires"),
    ):
        if data.get(key):
            L.append(f"- **{label}:** {data[key]}")
    L.append(f"- **Further revisions allowed:** {data.get('further_revision_requests_allowed')}")
    L.append("")

    for key, label in (
        ("eval_revision_notes", "Eval revision notes"),
        ("revision_notes", "Reviewer revision notes"),
        ("rebuttal_notes", "Rebuttal notes"),
        ("accept_notes", "Accept notes"),
        ("ec_override_feedback", "Override feedback"),
    ):
        if data.get(key):
            L += [f"## {label}", "", str(data[key]).strip(), ""]

    if notes:
        L += ["## notes.txt", "", notes, ""]

    L += [f"## Checks ({len(failed)} failed of {len(checks)})", ""]
    if not checks:
        L.append("The evaluation carries no per-check notes.")
    for c in checks:
        mark = {True: "PASS", False: "FAIL", None: "----"}[c.get("passed")]
        L.append(f"### {mark} — {c['name']}")
        L.append("")
        L.append(c.get("details") or "_no detail_")
        if c.get("suggestions"):
            L += ["", f"**Suggestions:** {c['suggestions']}"]
        if c.get("fields"):
            L += ["", f"**Fields:** {c['fields']}"]
        L.append("")

    d = drift(folder, sd) if folder else []
    L += ["## Platform vs repo", ""]
    if not folder:
        L.append("No task folder resolved, so nothing was compared.")
    elif d:
        L.append("The platform's copy and this folder disagree. The platform's is what was graded.")
        L.append("")
        for line in d:
            L.append(f"- {line}")
    else:
        L.append("The prompt and every rubric row match the folder.")
    L.append("")

    L += ["## What the platform holds", ""]
    L.append(f"- domain / occupation: {sd.get('radio-domain')} / {sd.get('radio-occupation')}")
    L.append(f"- input files: {len(sd.get('repeatabletextarea-input_file_list') or [])}")
    L.append(f"- output files: {len(sd.get('repeatabletextarea-output_file_list') or [])}")
    L.append(f"- rubric rows: {len(platform_rubric(sd))}")
    tools = sd.get("repeatabletextarea-please_insert_any_tool_used_for_this_task_human") or []
    L.append(f"- tools: {', '.join(str(t) for t in tools) or 'none'}")
    times = [
        sd.get("textarea-time_to_read_prompt"),
        sd.get("textarea-time_to_open_skimsearch_and_use_the_reference_files_human"),
        sd.get("textarea-time_to_perform_the_required_work_analysis_writing_calculations_"
               "coding_spreadsheet_edits_formatting_human"),
        sd.get("textarea-time_for_verificationqa_and_final_review_human"),
    ]
    L.append(f"- times: {' / '.join(str(t) for t in times)} min, total {sd.get('textarea-total_time_in_hours')} h")
    L.append("")
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("uid", help="the submission id, as /revise-task takes it")
    ap.add_argument("--folder", help="task folder, when metadata.json does not carry the UID")
    ap.add_argument("--json-only", action="store_true",
                    help="keep the raw fetch-task JSON and print its path, write no report")
    ap.add_argument("--keep-json", metavar="PATH", help="also copy the raw JSON here")
    args = ap.parse_args()

    tmp = Path(tempfile.mkdtemp(prefix=f"fb-{args.uid[:8]}-"))
    data = fetch_json(args.uid, tmp)
    raw = sorted(tmp.glob("*.json"))[0]

    if args.keep_json:
        Path(args.keep_json).write_bytes(raw.read_bytes())
    if args.json_only:
        print(raw)
        return 0

    folder = resolve_folder(args.uid, args.folder)
    text = report(args.uid, data, fetch_notes(args.uid), folder)

    if folder:
        dest = folder / f"feedback-{args.uid[:8]}.md"
        dest.write_text(text, encoding="utf-8")
        print(f"wrote {dest.relative_to(REPO)}\n")
    else:
        print(f"no task folder carries taskboard_uid {args.uid}; report not written\n")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
