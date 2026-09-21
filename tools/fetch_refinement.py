#!/usr/bin/env python3
"""Fetch a Hazy-Refinement task and stage it as a task-shaped folder.

    python3 tools/fetch_refinement.py <uid> [--name task-name] [--force]

Stages refinements/<uid>/ as ONE flat folder in submission-folder shape, so every existing
gate (autoeval_check, office_resave, fix_floats, fix_metadata, package_sweep,
build_model check) runs on `refinements/<uid>` unchanged:

    refinements/<uid>/
    ├── prompt.md               the working prompt (starts as the platform's, then edited)
    ├── original-prompt.md      the platform's prompt, verbatim, never edited
    ├── feedback.md             the "Feedback to Improve Task" panel, verbatim
    ├── inputs/                 extracted from the hand-over's input zip
    ├── solution/               extracted from the hand-over's golden zip
    ├── rubric-<task-name>.csv  NUMBER,CRITERION,WEIGHT
    ├── metadata.json           task_name, taskboard_uid, sector, onet_occupation, ...
    ├── feedback-log.md         opened with the fetch entry
    ├── change.log              what was updated, and what was not and why
    ├── review-comment.md       the form's Section 3 paragraph, nothing else
    ├── i-<task-name>.zip       copy of the hand-over input zip until rebuilt
    └── s-<task-name>.zip       copy of the hand-over golden zip until rebuilt

There is no `original/` and no `refined/` (operator, 2026-09-11). The hand-over is
downloaded to a scratch directory, the two things worth keeping from it are written out as
`original-prompt.md` and `feedback.md`, and the scratch directory is removed. What the
platform sent that is not kept is recoverable by re-running this command: the zips survive
as `inputs/`, `solution/` and the `i-`/`s-` copies, and the criteria as the rubric CSV.

Why not `stb submissions download`: it serves only the zip *you* uploaded, and a fresh
refinement has none. The materials sit in the fetch-task JSON under
static_document.static_document (prompt, criteria_md/json, seed_file_1/2 S3 URIs,
combined_feedback). The seed zips are plain submission keys the platform's presigned-get
endpoint serves; that helper lives in the stb tool's own virtualenv, so the download runs
under the interpreter named in the `stb` launcher's shebang.

Re-running on an existing folder re-downloads the hand-over, says whether the feedback
changed, rewrites feedback.md and original-prompt.md, and leaves everything you edit alone.
--force restages the whole folder from a fresh hand-over (destroys local edits).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
import tempfile
import subprocess
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ROOT = REPO / "refinements"
DELIVERABLE_EXT = (".docx", ".xlsx", ".pptx", ".pdf", ".md", ".csv", ".txt")
MULTIMODAL_EXT = (".pdf", ".pptx", ".png", ".jpg", ".jpeg", ".gif", ".mp4", ".mp3", ".wav")

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


def fetch_task_json(uid: str, platform: Path) -> dict:
    tmp = platform / "_fetch"
    subprocess.run(["stb", "submissions", "fetch-task", uid, "-o", str(tmp)], check=True,
                   stdout=subprocess.DEVNULL)
    files = sorted(tmp.glob("*.json"))
    if not files:
        sys.exit(f"fetch-task wrote nothing under {tmp}")
    data = json.loads(files[0].read_text())
    shutil.move(str(files[0]), platform / "task.json")
    shutil.rmtree(tmp, ignore_errors=True)
    return data


def download_zip(py: str, uri: str, dest: Path) -> int:
    res = subprocess.run([py, "-c", DOWNLOAD_SNIPPET, uri, str(dest)],
                         capture_output=True, text=True)
    if res.returncode:
        sys.exit(f"download failed for {uri}\n{res.stderr}")
    return int(res.stdout.strip().splitlines()[-1])


def zip_names(zpath: Path) -> list[str]:
    with zipfile.ZipFile(zpath) as zf:
        return [n for n in zf.namelist() if not n.endswith("/") and "__MACOSX" not in n]


def extract(zpath: Path, target: Path) -> list[str]:
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    root = target.resolve()
    with zipfile.ZipFile(zpath) as zf:
        names = zip_names(zpath)
        for n in names:
            if not (root / n).resolve().is_relative_to(root):
                sys.exit(f"zip member escapes target: {n}")
        for n in names:
            # flatten: the working folders are flat, like inputs/ and solution/ of a build
            (target / Path(n).name).write_bytes(zf.read(n))
    return [Path(n).name for n in names]


def onet_code(data: dict, title: str) -> str | None:
    """Resolve the occupation title to its O*NET code from the form's own dropdown."""
    for sec in data.get("form_schema", {}).get("sections", []):
        for f in sec.get("fields", []):
            if f.get("field") == "multiselect-onet_occupation":
                for opt in f.get("options", []):
                    code, _, label = str(opt.get("value", "")).partition("|")
                    if label.strip().lower() == title.strip().lower():
                        return code
    return None


def kebab(stem: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", stem.lower()).strip("-")


def write_platform(uid: str, platform: Path, data: dict, py: str) -> tuple[dict, dict]:
    sd = data["static_document"]["static_document"]
    if "prompt" not in sd:
        # Not a Refinery hand-over: a REVIEW task (someone's submission to review) carries its
        # prompt under task_documents[0].submission_document instead, and is fetched by
        # tools/fetch_review.py via /review-task. Leave nothing behind but the raw JSON.
        cat = data.get("task_category") or "non-refinement"
        keep = (platform.parent / "refined" / "metadata.json").exists()
        if not keep:
            shutil.rmtree(platform.parent, ignore_errors=True)
        sys.exit(f"{uid} is not a Hazy-Refinement hand-over: the platform returned a {cat} "
                 f"task on {data.get('project')} with no prompt under static_document. "
                 "A REVIEW task is fetched with tools/fetch_review.py (/review-task <uid>); "
                 "check reviews-list.md, it may already be reviewed.")
    (platform / "prompt.md").write_text(sd["prompt"].rstrip() + "\n")
    (platform / "rubrics.md").write_text(sd["criteria_md"].rstrip() + "\n")
    criteria = [{"weight": c["numeric-weight"], "text": c["textarea-criterion"]}
                for c in sd["criteria_json"]]
    (platform / "rubrics.json").write_text(json.dumps(criteria, indent=2) + "\n")
    fb = (sd.get("combined_feedback") or "").rstrip()
    if not fb:
        # 2026-09-14 (ambrose-nardelli): a hand-over listing three feedback categories arrived
        # with combined_feedback empty. Fall back to every other feedback-bearing field the
        # static document carries, each under its own heading, and say which keys were read.
        parts = []
        for k, v in sd.items():
            kl = k.lower()
            if k == "combined_feedback" or not isinstance(v, str) or not v.strip():
                continue
            if any(w in kl for w in ("feedback", "revision", "reviewer", "note", "comment", "issue")):
                parts.append(f"## {k}\n\n{v.strip()}")
        fb = "\n\n".join(parts)
        print(f"  combined_feedback empty; feedback.md built from {len(parts)} other field(s): "
              f"{[k for k in sd if isinstance(sd[k], str) and any(w in k.lower() for w in ('feedback','revision','reviewer','note','comment','issue'))]}")
        print(f"  static_document keys: {sorted(k for k in sd if not k.startswith('seed_file'))}")
    (platform / "feedback.md").write_text(fb + "\n")
    meta = {
        "uid": uid,
        "project": data.get("project"),
        "project_id": (data.get("project_id") or {}).get("id"),
        "assignment_id": (data.get("assignment_id") or {}).get("id"),
        "origin_submission_id": sd.get("Submission ID (automated)"),
        "sector": sd.get("Sector"),
        "occupation": sd.get("Occupation"),
        "feedback_category": sd.get("feedback_category"),
        "revision_notes": data.get("revision_notes"),
        "eval_revision_notes": data.get("eval_revision_notes"),
        "criteria_count": len(criteria),
        "fetched_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
    }
    (platform / "meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    for key, role in (("seed_file_1", "inputs"), ("seed_file_2", "solution")):
        uri = (sd.get(key) or {}).get("s3_uri")
        if not uri:
            sys.exit(f"{key} ({role}) carries no s3_uri; the task is not fetchable this way")
        size = download_zip(py, uri, platform / f"{role}.zip")
        print(f"  {role}.zip  {size:>7} B  <- {uri.rsplit('/', 1)[-1]}")
    return sd, meta


def stage(uid: str, root: Path, name: str | None, platform: Path) -> str:
    """Build the flat refinement folder from the hand-over staged in `platform`."""
    folder = root
    folder.mkdir(parents=True, exist_ok=True)
    meta = json.loads((platform / "meta.json").read_text())
    criteria = json.loads((platform / "rubrics.json").read_text())
    data = json.loads((platform / "task.json").read_text())

    inputs = extract(platform / "inputs.zip", folder / "inputs")
    golden = extract(platform / "solution.zip", folder / "solution")
    deliverables = [n for n in golden if n.lower().endswith(DELIVERABLE_EXT)]
    if not name:
        stem = Path(deliverables[0] if deliverables else (golden[0] if golden else uid)).stem
        name = kebab(stem)
    if not deliverables:
        print("!! solution/ holds no deliverable-shaped file; check the seed roles by hand")

    shutil.copy2(platform / "prompt.md", folder / "prompt.md")
    # The platform's prompt is kept verbatim beside the working copy: with no original/ it
    # gone it is the only record of what the prompt looked like before this round.
    shutil.copy2(platform / "prompt.md", folder / "original-prompt.md")
    if (platform / "feedback.md").exists():
        shutil.copy2(platform / "feedback.md", folder / "feedback.md")
    shutil.copy2(platform / "inputs.zip", folder / f"i-{name}.zip")
    shutil.copy2(platform / "solution.zip", folder / f"s-{name}.zip")

    with open(folder / f"rubric-{name}.csv", "w", encoding="utf-8-sig", newline="") as fh:
        import csv
        w = csv.writer(fh)
        w.writerow(["NUMBER", "CRITERION", "WEIGHT"])
        for i, c in enumerate(criteria, 1):
            w.writerow([i, c["text"], c["weight"]])

    title = meta.get("occupation") or ""
    metadata = {
        "task_name": name,
        "taskboard_uid": uid,
        "sector": meta.get("sector"),
        "onet_occupation": {"code": onet_code(data, title), "title": title},
        "onet_tasks": [],
        "onet_skills": [],
        "input_file_count": len(inputs),
        "multimodal": any(n.lower().endswith(MULTIMODAL_EXT) for n in inputs),
        "web_search_allowed": False,
        "manual_time_hours": None,
        "llm_starting_point": None,
        "built_with": None,
        "refinement": {
            "project_id": meta.get("project_id"),
            "assignment_id": meta.get("assignment_id"),
            "origin_submission_id": meta.get("origin_submission_id"),
            "feedback_category": meta.get("feedback_category"),
        },
    }
    (folder / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")

    today = dt.date.today().isoformat()
    log = folder / "feedback-log.md"
    if not log.exists():
        log.write_text(
            f"# Feedback log — {name} (refinement {uid})\n\n"
            f"## {today} · source: platform (Hazy-Refinement fetch) · verdict: OFFERED\n\n"
            f"Feedback category: {meta.get('feedback_category')}. Origin submission "
            f"{meta.get('origin_submission_id')}. The panel text is in feedback.md and the "
            f"prompt as handed over is original-prompt.md; the untouched inputs and golden "
            f"are the i- and s- zips until they are rebuilt.\n"
        )
    log = folder / "change.log"
    if not log.exists():
        log.write_text(
            f"# Change log — {name}\n\n"
            f"Task UID {uid}. Feedback category: {meta.get('feedback_category')}.\n"
            f"`original-prompt.md` and `feedback.md` are the platform's hand-over; everything\n"
            f"else here is the revision. This log is the record of the difference. The paragraph\n"
            f"entered in the form's Section 3 lives in review-comment.md.\n\n"
            "## Feedback items and what was done\n\n"
            "_One entry per item in feedback.md and per in-app check that failed: what it pointed at, the root cause, the change._\n\n"
            "## Files changed\n\n"
            "_prompt.md / inputs/… / solution/… / rubric CSV — one line each, with what changed in it._\n\n"
            "## Not changed, and why\n\n"
            "_Anything the feedback raised that was left alone, with the reason._\n\n"
            "## Golden scored against the final rubric\n\n"
            "_One row per criterion: the golden sentence or cell that satisfies it, or why a negative does not fire._\n"
        )
    comment = folder / "review-comment.md"
    if not comment.exists():
        comment.write_text(
            "_Replace this line with the paragraph for the form's Section 3, \"Briefly summarize the "
            "changes made and note any changes not completed, including why you decided not to make "
            "them.\" 60 to 120 words, plain first person, the way you would type it into the form._\n"
        )
    return name


def tree(folder: Path) -> None:
    for p in sorted(folder.rglob("*")):
        if p.is_file():
            print(f"  {p.relative_to(folder)}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("uid", help="refinement task uid (the submission id on the Refinery node)")
    ap.add_argument("--name", help="task name (default: kebab of the golden deliverable's stem)")
    ap.add_argument("--force", action="store_true",
                    help="restage the whole folder from a fresh hand-over (discards local edits)")
    args = ap.parse_args()

    root = ROOT / args.uid
    folder = root
    existed = (folder / "metadata.json").exists()
    # The hand-over lands in a scratch directory and is deleted once the two things worth
    # keeping (the prompt as handed over, the feedback panel) have been written into the
    # folder. Nothing under refinements/<uid>/ is a platform mirror any more.
    old_feedback = (folder / "feedback.md").read_text() if (folder / "feedback.md").exists() else None
    platform = Path(tempfile.mkdtemp(prefix=f"refine-{args.uid[:8]}-"))
    try:
        py = stb_python()
        print(f"fetching {args.uid} -> {root.relative_to(REPO)}/")
        data = fetch_task_json(args.uid, platform)
        sd, meta = write_platform(args.uid, platform, data, py)

        if existed and not args.force:
            name = json.loads((folder / "metadata.json").read_text())["task_name"]
            new_feedback = (platform / "feedback.md").read_text() if (platform / "feedback.md").exists() else None
            changed = old_feedback is not None and new_feedback is not None and old_feedback != new_feedback
            if new_feedback is not None:
                (folder / "feedback.md").write_text(new_feedback)
            shutil.copy2(platform / "prompt.md", folder / "original-prompt.md")
            print("\nhand-over refreshed; your edits untouched (--force to restage)")
            print(f"feedback.md: {'CHANGED since last fetch' if changed else 'unchanged'}")
        else:
            name = stage(args.uid, root, args.name, platform)
    finally:
        shutil.rmtree(platform, ignore_errors=True)

    print(f"\n{root.relative_to(REPO)}/  task_name={name}")
    tree(root)
    print(f"\ncriteria: {meta['criteria_count']}  "
          f"weights: {[c['numeric-weight'] for c in sd['criteria_json']]}")
    print(f"feedback category: {meta['feedback_category']}   occupation: {meta['occupation']}")


if __name__ == "__main__":
    main()
