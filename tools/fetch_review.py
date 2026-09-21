#!/usr/bin/env python3
"""Fetch a review assignment and stage reviews/<review-id>/ with both zips.

    python3 tools/fetch_review.py <review-id> [--force]

Writes three things into reviews/<review-id>/, creating the folder if it is not there:

    reviews/<review-id>/
    ├── review_<short>.json   raw `stb reviews fetch-task` output
    ├── <inputs zip>          the input_files widget, under the platform's own filename
    └── <golden zip>          the s3FileUploader widget, under the platform's own filename

Both zips keep the name the payload carries and are saved as zips, never extracted: the
review harness resolves which is which by content, reports them on its `[packaging]` lines,
and Gate 3 groups submissions on the prefix in the upload's s3Key. Extracting here would
lose all three.

Why not `stb reviews download`: the command exists but cannot serve a review packet. It
resolves the file through `get_submission_file_info`, which looks only at a widget named
`upload_a_zip_file` or one whose field starts with the lowercase literal `s3fileuploader-`.
A review submission document carries `input_files` and `s3FileUploader-4243d`; the first
matches neither test and the second differs in case, so the lookup falls through to
*"has no uploaded file to download"*. It also returns on the first widget it finds, so even
with the casing fixed it would hand back one zip and never both, and
`download_and_extract_zip` discards the archive once it has extracted it.

So this goes to the same presigned-get endpoint the CLI uses, one key at a time. That helper
lives in the stb tool's own virtualenv, so the download runs under the interpreter named in
the `stb` launcher's shebang, exactly as tools/fetch_refinement.py does it for refinements.

Re-running is safe. A folder that already holds any zip is left exactly as it is and the
JSON alone is refreshed, so a folder the operator filled by hand is never touched and never
gains a second copy under a different name: a browser download arrives as
`input_files (1).zip` where the platform calls it `input_files.zip`, and pulling on top of
that would leave the harness globbing two identical archives. --force re-pulls regardless.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ROOT = REPO / "reviews"

DOWNLOAD_SNIPPET = r"""
import sys
from pathlib import Path
from snorkelai_stb.utils import request_s3_presigned_get_url, download_from_s3
uri, dest = sys.argv[1], Path(sys.argv[2])
download_from_s3(request_s3_presigned_get_url(uri), dest)
print(dest.stat().st_size)
"""


def stb_python() -> str:
    """The interpreter the stb launcher runs under, which has snorkelai_stb importable."""
    launcher = shutil.which("stb")
    if not launcher:
        sys.exit("stb not on PATH; install snorkelai-stb first")
    first = Path(launcher).read_text(errors="replace").splitlines()[0]
    if not first.startswith("#!"):
        sys.exit(f"cannot read interpreter from {launcher}")
    return first[2:].strip()


def fetch_task_json(uid: str, folder: Path) -> Path:
    subprocess.run(["stb", "reviews", "fetch-task", uid, "-o", str(folder)],
                   check=True, stdout=subprocess.DEVNULL)
    files = sorted(folder.glob("review_*.json"))
    if not files:
        sys.exit(f"fetch-task wrote no review_*.json under {folder}")
    return files[0]


def safe_name(name: str, fallback: str) -> str:
    """Last path component only, no traversal, always ending .zip."""
    stem = Path(name.replace("\\", "/")).name.strip(". ")
    stem = re.sub(r"[^A-Za-z0-9._ ()-]", "_", stem)
    if not stem:
        stem = fallback
    return stem if stem.lower().endswith(".zip") else f"{stem}.zip"


def widgets(sd: dict) -> list[tuple[str, str, str]]:
    """(role, uri, filename) for every upload widget on the submission document.

    input_files is the inputs zip and the s3FileUploader-* fields are the golden. Both
    names are recorded for the report only; the harness decides the roles by content.
    """
    out = []
    for field, value in sd.items():
        if not isinstance(value, dict):
            continue
        uri = value.get("s3Uri") or value.get("s3Key")
        if not uri:
            continue
        role = "inputs" if field == "input_files" else (
            "golden" if field.lower().startswith("s3fileuploader-") else field)
        out.append((role, str(uri), str(value.get("filename") or "")))
    return out


def download_zip(py: str, uri: str, dest: Path) -> int:
    res = subprocess.run([py, "-c", DOWNLOAD_SNIPPET, uri, str(dest)],
                         capture_output=True, text=True)
    if res.returncode:
        dest.unlink(missing_ok=True)
        sys.exit(f"download failed for {uri}\n{res.stderr}")
    try:
        with zipfile.ZipFile(dest) as zf:
            members = len(zf.namelist())
    except zipfile.BadZipFile:
        dest.unlink(missing_ok=True)
        sys.exit(f"downloaded file is not a zip: {uri}")
    print(f"     {members} file(s) inside")
    return int(res.stdout.strip().splitlines()[-1])


def main() -> None:
    ap = argparse.ArgumentParser(description="Stage a review assignment with both zips.")
    ap.add_argument("uid", help="review id, the same one /review-task takes")
    ap.add_argument("--force", action="store_true",
                    help="re-pull both zips even where the folder already holds them")
    args = ap.parse_args()

    folder = ROOT / args.uid
    if not folder.exists():
        folder.mkdir(parents=True)
        print(f"created {folder.relative_to(REPO)}")
    else:
        print(f"using {folder.relative_to(REPO)}")

    jpath = fetch_task_json(args.uid, folder)
    print(f"  {jpath.name}")
    data = json.loads(jpath.read_text())
    sd = (data.get("task_documents") or [{}])[0].get("submission_document") or {}

    found = widgets(sd)
    if not found:
        sys.exit("no upload widget on the submission document carries an s3Uri or s3Key")

    present = sorted(p for p in folder.glob("*.zip"))
    if present and not args.force:
        for p in present:
            print(f"  {p.name}  held, {p.stat().st_size} B")
        print(f"\nthe folder already holds {len(present)} zip(s), so none were pulled; "
              f"--force replaces them")
        return

    py = stb_python()
    for role, uri, filename in found:
        dest = folder / safe_name(filename, f"{role}.zip")
        size = download_zip(py, uri, dest)
        print(f"  {dest.name}  {size} B  ({role})  <- {uri.rsplit('/', 1)[-1]}")

    print(f"\n{len(found)} zip(s) staged in {folder.relative_to(REPO)}")


if __name__ == "__main__":
    main()
