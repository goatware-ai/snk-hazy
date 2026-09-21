#!/usr/bin/env python3
"""Rebuild a submissions/{seq}-{name}/ folder from the platform.

    python3 tools/restore_submission.py <uid> [<uid> ...] [--all-needs-revision] [--dry-run]

Why this exists: a submission whose UID drops off `stb submissions list` is treated as
gone and archived, which reduces its folder to archived/{seq}-{name}/prompt.md. When the
platform later re-lists that UID as NEEDS_REVISION the row moves back, but the package
does not: /revise-task then has a row and no folder to revise. This restores the folder
from the platform, which still holds every part.

`stb submissions download` does NOT work for these (it serves only a file you uploaded to
that assignment and reports "has no uploaded file to download"). Everything is taken from
`stb submissions fetch-task` instead: the prompt and criteria come back as text, and the
input and golden zips as S3 URIs fetched through stb's presigned-get helper, which lives
in stb's own virtualenv and so runs under the interpreter in the `stb` launcher's shebang.

Rebuilt, in the exact shape a built task has:

    submissions/{seq}-{name}/
    ├── prompt.md                        the live prompt
    ├── inputs/                          extracted from the input zip
    ├── solution/                        extracted from the golden zip
    ├── i-{name}.zip / s-{name}.zip      the zips as the platform holds them
    ├── rubric-{name}-{uid8}.csv         NUMBER,CRITERION,WEIGHT
    ├── metadata.json                    rebuilt from the form's own values
    └── feedback-log.md                  carried over, or opened with the restore entry

What cannot come back: build_session, and any feedback-log history the archive step
discarded. The archived/{seq}-{name}/ folder is removed once the rebuild succeeds, and
Model in submission-list.md is the source for built_with.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SUBMISSIONS = REPO / "submissions"
ARCHIVED = REPO / "archived"
LIST_MD = REPO / "submission-list.md"

DOWNLOAD_SNIPPET = r"""
import sys
from pathlib import Path
from snorkelai_stb.utils import request_s3_presigned_get_url, download_from_s3
uri, dest = sys.argv[1], Path(sys.argv[2])
download_from_s3(request_s3_presigned_get_url(uri), dest)
print(dest.stat().st_size)
"""


def stb_python() -> str:
    launcher = shutil.which("stb")
    if not launcher:
        sys.exit("stb not on PATH; install snorkelai-stb first")
    first = Path(launcher).read_text(errors="replace").splitlines()[0]
    if not first.startswith("#!"):
        sys.exit(f"cannot read interpreter from {launcher}")
    return first[2:].strip()


def rows_from_list() -> list[dict]:
    """Every submission-list.md row as {status, seq, name, uid, model}."""
    text = LIST_MD.read_text(encoding="utf-8")
    out, status = [], ""
    for line in text.splitlines():
        head = re.match(r"^## (\w+)", line)
        if head:
            status = head.group(1)
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 5 or not cells[0].isdigit():
            continue
        out.append({"status": status, "seq": cells[0], "name": cells[1],
                    "uid": cells[2], "updated": cells[3], "model": cells[4]})
    return out


def fetch_json(uid: str, scratch: Path) -> dict:
    out = scratch / "ft"
    subprocess.run(["stb", "submissions", "fetch-task", uid, "-o", str(out)],
                   check=True, stdout=subprocess.DEVNULL)
    files = sorted(out.glob("*.json"))
    if not files:
        sys.exit(f"fetch-task wrote nothing for {uid}")
    return json.loads(files[0].read_text())


class Failed(Exception):
    """One task could not be restored. Never aborts the batch."""


def download(py: str, uri: str, dest: Path, tries: int = 3) -> int:
    """Fetch one zip, retrying transient S3 resets.

    A dropped connection killed a 17-task batch mid-run (2026-09-14), so a failure here
    raises Failed for this one task rather than exiting: the rest of the batch still runs
    and the summary names what to re-run.
    """
    last = ""
    for attempt in range(1, tries + 1):
        res = subprocess.run([py, "-c", DOWNLOAD_SNIPPET, uri, str(dest)],
                             capture_output=True, text=True)
        if not res.returncode:
            return int(res.stdout.strip().splitlines()[-1])
        last = (res.stderr or "").strip().splitlines()[-1] if res.stderr else "unknown error"
        if attempt < tries:
            time.sleep(2 * attempt)
    raise Failed(f"download failed after {tries} tries: {last}")


def extract_flat(zpath: Path, target: Path) -> list[str]:
    """Extract to a flat folder, refusing any member that escapes it."""
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    root = target.resolve()
    with zipfile.ZipFile(zpath) as zf:
        names = [n for n in zf.namelist() if not n.endswith("/") and "__MACOSX" not in n]
        for n in names:
            if not (root / Path(n).name).resolve().is_relative_to(root):
                sys.exit(f"zip member escapes target: {n}")
        for n in names:
            (target / Path(n).name).write_bytes(zf.read(n))
    return sorted(Path(n).name for n in names)


def golden_key(sd: dict) -> str | None:
    for k, v in sd.items():
        if k.startswith("s3FileUploader") and isinstance(v, dict) and v.get("s3Uri"):
            return k
    return None


def restore(row: dict, py: str, dry_run: bool) -> str:
    uid, seq, name = row["uid"], row["seq"], row["name"]
    folder = SUBMISSIONS / f"{seq}-{name}"
    if folder.is_dir():
        return f"{seq}-{name}: already in submissions/, skipped"
    if dry_run:
        return f"{seq}-{name}: would restore from {uid[:8]}"

    scratch = Path(tempfile.mkdtemp(prefix=f"restore-{uid[:8]}-"))
    try:
      try:
          data = fetch_json(uid, scratch)
          sd = (data.get("task_documents") or [{}])[0].get("submission_document") or {}
          if not sd.get("prompt"):
              raise Failed("fetch-task returned no prompt")
          gkey = golden_key(sd)
          if not gkey or not (sd.get("input_files") or {}).get("s3Uri"):
              raise Failed("no input/golden S3 refs in the payload")

          izip, szip = scratch / "inputs.zip", scratch / "solution.zip"
          download(py, sd["input_files"]["s3Uri"], izip)
          download(py, sd[gkey]["s3Uri"], szip)

          folder.mkdir(parents=True)
          inputs = extract_flat(izip, folder / "inputs")
          extract_flat(szip, folder / "solution")
          shutil.copy2(izip, folder / f"i-{name}.zip")
          shutil.copy2(szip, folder / f"s-{name}.zip")
          (folder / "prompt.md").write_text(sd["prompt"].rstrip() + "\n", encoding="utf-8")

          with open(folder / f"rubric-{name}-{uid[:8]}.csv", "w",
                    encoding="utf-8-sig", newline="") as fh:
              w = csv.writer(fh)
              w.writerow(["NUMBER", "CRITERION", "WEIGHT"])
              for i, c in enumerate(sd.get("criteria") or [], 1):
                  w.writerow([i, c.get("textarea-criterion", ""), c.get("numeric-weight", "")])

          occ = (sd.get("multiselect-onet_occupation") or [""])[0]
          code, _, title = occ.partition("|")
          static = (data.get("static_document") or {}).get("static_document") or {}
          (folder / "metadata.json").write_text(json.dumps({
              "task_name": name,
              "taskboard_uid": uid,
              "sector": static.get("Sector"),
              "onet_occupation": {"code": code or None, "title": title or None},
              "onet_tasks": sd.get("multiselect-onet_tasks") or [],
              "onet_skills": sd.get("multiselect-onet_skills") or [],
              "input_file_count": sd.get("numeric-how_many_reference_files_are_tied_to_your_prompt")
                                  or len(inputs),
              "multimodal": bool(sd.get("boolean-are_the_input_files_multi-modal")),
              "web_search_allowed": bool(sd.get("boolean-3f359")),
              "manual_time_hours": sd.get(
                  "numeric-if_you_were_to_do_this_prompt_manually_without_the_help_of_any_llms_"
                  "how_long_would_this_task_take"),
              "llm_starting_point": (sd.get("radio-2ed38") or "").title() or None,
              "built_with": row.get("model") or None,
          }, indent=2) + "\n", encoding="utf-8")

          archived = ARCHIVED / f"{seq}-{name}"
          log = folder / "feedback-log.md"
          carried = archived / "feedback-log.md"
          if carried.exists():
              shutil.copy2(carried, log)
          elif not log.exists():
              log.write_text(
                  f"# Feedback log — {name}\n\n"
                  f"## {dt.date.today().isoformat()} · source: restore · verdict: NEEDS_REVISION\n\n"
                  f"Folder rebuilt from the platform with tools/restore_submission.py after the "
                  f"archive step had reduced it to prompt.md. Prompt, criteria, inputs and golden "
                  f"are the platform's current copies. Earlier feedback history was lost with "
                  f"the archive.\n", encoding="utf-8")
          if archived.is_dir():
              shutil.rmtree(archived)
          return (f"{seq}-{name}: restored, {len(inputs)} input(s), "
                  f"{len(sd.get('criteria') or [])} criteria, archived/ removed")
      except Failed as e:
        # Downloads run before the folder is created, so a failure leaves nothing behind.
        if folder.is_dir() and not (folder / "metadata.json").exists():
            shutil.rmtree(folder)
        return f"{seq}-{name}: FAILED, {e} - re-run: tools/restore_submission.py {uid[:8]}"
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("uids", nargs="*", help="taskboard UIDs to restore")
    ap.add_argument("--all-needs-revision", action="store_true",
                    help="restore every NEEDS_REVISION row that has no submissions/ folder")
    ap.add_argument("--dry-run", action="store_true", help="list what would be restored")
    args = ap.parse_args()

    rows = rows_from_list()
    if args.all_needs_revision:
        todo = [r for r in rows
                if r["status"] == "NEEDS_REVISION"
                and not (SUBMISSIONS / f"{r['seq']}-{r['name']}").is_dir()]
    else:
        by_uid = {r["uid"]: r for r in rows}
        todo = []
        for u in args.uids:
            hit = by_uid.get(u) or next((r for r in rows if r["uid"].startswith(u)), None)
            if not hit:
                sys.exit(f"{u} is not a UID in submission-list.md")
            todo.append(hit)
    if not todo:
        print("nothing to restore")
        return

    py = stb_python()
    print(f"restoring {len(todo)} submission(s)\n")
    results = [restore(r, py, args.dry_run) for r in todo]
    for line in results:
        print("  " + line)
    failed = [ln for ln in results if "FAILED" in ln]
    if failed:
        print(f"\n{len(failed)} of {len(results)} failed; the rest are restored. "
              f"Re-run the tool to retry just those.")


if __name__ == "__main__":
    main()
