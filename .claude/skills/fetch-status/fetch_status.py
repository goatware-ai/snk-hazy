#!/usr/bin/env python3
"""Fetch Hazy submission counts and diff them against the previous check.

Runs `stb submissions list` for the Hazy-Production project, tallies the
Assignment State column, and compares the tally to the last snapshot stored in
history.jsonl. Submission IDs are resolved to task names through the repo's
submission-list.md index (one table per status), and the local rows there are
reconciled against what the platform actually reports:

- A row whose status disagrees with the platform is moved into the right
  status's table (the platform is the source of truth for state).
- A submission-list.md UID the platform no longer lists is either rejected and
  archived: the row moves to REJECTED and its folder is reduced to
  archived/{seq}-{name}/prompt.md. A row that had reached ACCEPTED before it
  vanished went to the refinement pipeline rather than being failed, so its
  Note records that and its last known payment status, recovered from the
  previous snapshot (the vanished UID can no longer be queried). A row
  that never reached ACCEPTED is a genuine rejection: moved to REJECTED, its
  submissions/ folder reduced to just prompt.md under archived/.
- A platform submission with no submission-list.md row, reporting OFFERED or
  EVALUATION_PENDING, is matched against drafts/*/metadata.json by Taskboard
  UID and promoted: the draft folder moves to submissions/ and a new row is added.
- An ACCEPTED row whose submissions/ folder still exists is archived: the whole
  folder is zipped into accepted/{seq}-{name}.zip and removed from submissions/.

Every write stamps the row's Updated cell with the current US Eastern time.
Prints a plain-text report on stdout.

Exits non-zero without recording a snapshot if the CLI call fails, so a failed
auth or network call never becomes a bogus "everything dropped to zero" diff.
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

# Hazy project nodes. PROJECT_ID is the production node this desk submits to.
# REFINE_PROJECT_ID is the Refinery node; Hazy may not have one, and while it holds the
# port placeholder the refinement block is simply skipped (see run_refinements_cli).
PROJECT_ID = "cda2e943-8524-45f0-a966-469903337102"
# Refinements are submissions on their own project node, with their own list file.
REFINE_PROJECT_ID = "TODO-HAZY-REFINEMENT-PROJECT-ID"


def refinements_configured():
    """False while REFINE_PROJECT_ID is still the port placeholder."""
    return not REFINE_PROJECT_ID.startswith("TODO-HAZY-")


def require_project_ids():
    """Exit rather than call stb while the production project id is a placeholder.

    Only PROJECT_ID blocks: it drives the submissions and reviews calls and the
    submission-list.md reconciliation, so a placeholder there would either fail or, worse,
    sync this desk against another project's board. A missing REFINE_PROJECT_ID only means
    no Refinery node is configured, which is a normal state for a new desk.
    """
    if PROJECT_ID.startswith("TODO-HAZY-"):
        sys.exit(
            "fetch_status.py is not configured for Hazy yet: PROJECT_ID still holds the "
            "port placeholder. Set it to Hazy's production project node id at the top of "
            "this file (see PORTING.md), then re-run."
        )
HISTORY = Path(__file__).resolve().parent / "history.jsonl"
# .claude/skills/fetch-status/ -> repo root
REPO = Path(__file__).resolve().parents[3]
SUBMISSION_LIST = REPO / "submission-list.md"
REFINEMENT_LIST = REPO / "refinement-list.md"
SUBMISSIONS_DIR = REPO / "submissions"
DRAFTS_DIR = REPO / "drafts"
ARCHIVED = REPO / "archived"
ACCEPTED_DIR = REPO / "accepted"
REFINEMENTS_DIR = REPO / "refinements"
EASTERN = ZoneInfo("America/New_York")

# The order sections appear in submission-list.md (user instruction 2026-08-26):
# finished work first, then what is still moving, then what is parked.
STATUSES = [
    "ACCEPTED",
    "REVIEW_PENDING",
    "EVALUATION_PENDING",
    "NEEDS_REVISION",
    "OFFERED",
    "REJECTED",
]

# NEEDS_REVISION and REJECTED are the two states that carry a Note column:
# NEEDS_REVISION because the next action has to be written down, and REJECTED
# because a row that vanished after reaching ACCEPTED went to the refinement
# pipeline rather than being failed, and its last known payment status (there
# is still a payout) is worth keeping visible. Every table carries Model, the
# model that built the task. A row leaving NEEDS_REVISION drops its note, which
# is intended - the durable record lives in that task's feedback-log.md.
NOTE_STATUSES = {"NEEDS_REVISION", "REJECTED"}
COLUMNS = ["Seq", "Task name", "Taskboard UID", "Updated", "Model"]
CELL_KEYS = {
    "Seq": "seq", "Task name": "name",
    "Taskboard UID": "uid", "Updated": "updated", "Model": "model", "Note": "note",
}

UPGRADE_CMD = (
    "  uv tool upgrade snorkelai-stb \\\n"
    "    --find-links https://snorkel-python-wheels.s3.us-west-2.amazonaws.com/stb/index.html \\\n"
    '    --python ">=3.12"'
)

# The four the report leads with, in the order they are displayed.
PRIMARY = [
    ("ACCEPTED", "Accepted"),
    ("REVIEW_PENDING", "Review pending"),
    ("EVALUATION_PENDING", "Evaluation pending"),
    ("NEEDS_REVISION", "Needs revision"),
]
SECONDARY = [
    ("OFFERED", "Offered"),
    ("REJECTED", "Rejected"),
    ("SKIPPED", "Skipped"),
]
KNOWN = [s for s, _ in PRIMARY] + [s for s, _ in SECONDARY]

# Review assignment states. Only two have been observed live so far (OFFERED, then
# REVIEW_PENDING once an assignment is taken), so this list orders what is known and
# anything else the platform returns is charted under the name it gives.
REVIEW_PRIMARY = [
    ("OFFERED", "Offered"),
    ("REVIEW_PENDING", "To review"),
]

# refinement-list.md is ONE table, not one per status (operator, 2026-09-11): a refinement
# is addressed by its UID everywhere, so the UID leads and the status is a cell again.
# Note carries the task name from submission-list.md when the refinement's
# origin_submission_id is one of OUR submissions - which is exactly the "is this my own
# task" question, since most refinements handed out are other contributors' work.
REFINE_COLUMNS = ["Task UID", "Task name", "Status", "Updated", "Note"]
REFINE_CELL_KEYS = {
    "Task UID": "uid", "Task name": "name", "Status": "status",
    "Updated": "updated", "Note": "note",
}
REFINE_PREAMBLE = """# Refinement List

Refinement tasks on the Hazy-Refinement project node, newest first. `/fetch-status` owns this file and syncs it
to the platform on every run.

Each row's work lives in `refinements/<Task UID>/`. `/refine-task <uid>` does
round 1; `/revise-refinement <uid>` does every round after.

**Note** names the original task when it is one of ours, resolved from the refinement's
`origin_submission_id` against `submission-list.md`. A blank Note means the refinement is
of another contributor's submission."""

SECTION_RE = re.compile(r"^## (\w+)(?:\s*\([^)]*\))?\s*$", re.MULTILINE)
DRAFT_FOLDER_RE = re.compile(r"^(\d+)-(.+)$")


def now_stamp(now=None):
    """The US Eastern timestamp written into a row's Updated cell on every write."""
    return (now or datetime.now(EASTERN)).strftime("%Y-%m-%d %H:%M %Z")


def split_row(line):
    """The cells of a submission-list.md table row, or None if the line is not one."""
    if not line.strip().startswith("|"):
        return None
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) < 5 or not cells[0].isdigit():  # header, separator, prose
        return None
    return cells


def header_columns(line):
    """The column names of a table header row, or None if the line is not one."""
    if not line.strip().startswith("|"):
        return None
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return cells if cells and cells[0] == "Seq" else None


def parse_submission_list(text):
    """Split submission-list.md into (preamble, rows). Each row carries its status,

    read from the "## STATUS" heading of the section its table row was found
    under, since the status is no longer a cell of its own.
    """
    matches = list(SECTION_RE.finditer(text))
    preamble = text[: matches[0].start()].rstrip("\n") if matches else text.rstrip("\n")
    rows = []
    for i, m in enumerate(matches):
        status = m.group(1)
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        # Read each row against its own section's header rather than by fixed
        # position, so a table that carries Note and one that does not both parse,
        # and a hand-added column cannot silently shift a value into Model.
        columns = list(COLUMNS)
        for line in text[m.end():end].splitlines():
            head = header_columns(line)
            if head:
                columns = head
                continue
            cells = split_row(line)
            if not cells:
                continue
            row = {"status": status, "note": "", "model": ""}
            for name, cell in zip(columns, cells):
                key = CELL_KEYS.get(name)
                if key:
                    row[key] = cell
            row.setdefault("updated", "-")
            rows.append(row)
    return preamble, rows


BAR_WIDTH = 24
EIGHTHS = " \u258f\u258e\u258d\u258c\u258b\u258a\u2589"


def bar(n, peak, width=BAR_WIDTH):
    """A horizontal bar for n against the largest count in the same chart.

    Partial eighth-blocks keep small counts visible: at 18 accepted against 5 in
    evaluation, a whole-block-only bar rounds several states to nothing and the chart
    stops saying anything the numbers did not already say.
    """
    if peak <= 0 or n <= 0:
        return ""
    units = n / peak * width
    full = int(units)
    tail_idx = int(round((units - full) * 8))
    if tail_idx >= 8:
        full, tail_idx = full + 1, 0
    return "\u2588" * full + (EIGHTHS[tail_idx] if tail_idx else "")


def render_table(status, rows_for_status):
    if not rows_for_status:
        return "_None._"
    columns = COLUMNS + (["Note"] if status in NOTE_STATUSES else [])
    lines = [
        "| " + " | ".join(columns) + " |",
        "|" + "|".join("-" * (len(c) + 2) for c in columns) + "|",
    ]
    for r in sorted(rows_for_status, key=lambda r: int(r["seq"])):
        lines.append("| " + " | ".join(r.get(CELL_KEYS[c], "") for c in columns) + " |")
    return "\n".join(lines)


def render_submission_list(preamble, rows):
    by_status = {s: [] for s in STATUSES}
    for r in rows:
        by_status.setdefault(r["status"], []).append(r)
    parts = [preamble.rstrip("\n")] if preamble.strip() else []
    for status in STATUSES:
        rows_here = by_status[status]
        parts.append("## %s (%d)\n\n%s" % (status, len(rows_here), render_table(status, rows_here)))
    return "\n\n".join(parts).rstrip("\n") + "\n"


def load_tasks_md():
    """Return (preamble, rows, {uid: row}) from submission-list.md, or empty if absent."""
    if not SUBMISSION_LIST.exists():
        return "", [], {}
    preamble, rows = parse_submission_list(SUBMISSION_LIST.read_text(encoding="utf-8"))
    index = {
        r["uid"]: r for r in rows if re.fullmatch(r"[0-9a-f-]{36}", r["uid"])
    }
    return preamble, rows, index


def run_cli():
    """Return raw stdout from `stb submissions list`, or exit with its error."""
    cmd = ["stb", "submissions", "list", "-p", PROJECT_ID]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    except FileNotFoundError:
        sys.exit("stb not found on PATH. Install it per the Snorkel CLI user guide.")
    except subprocess.TimeoutExpired:
        sys.exit("stb submissions list timed out after 180s.")
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout).strip()
        msg = "stb submissions list failed (exit %d). No snapshot recorded.\n%s" % (
            proc.returncode,
            err,
        )
        # stb version-gates itself: once a newer release ships, every command
        # refuses to run until the CLI is upgraded.
        if "outdated" in err.lower() or "upgrade before continuing" in err.lower():
            msg += "\n\nUpgrade the CLI, then re-run:\n" + UPGRADE_CMD
        sys.exit(msg)
    return proc.stdout


def parse(output):
    """Extract [{id, state}] from the box-drawing table stb prints."""
    rows = [ln.strip() for ln in output.splitlines() if ln.strip().startswith("│")]
    if not rows:
        return []

    def cells(line):
        return [c.strip() for c in line.strip().strip("│").split("│")]

    # Locate columns from the header rather than assuming fixed positions.
    idx_id = idx_state = idx_pay = None
    for row in rows:
        c = cells(row)
        if "Assignment State" in c:
            idx_state = c.index("Assignment State")
            idx_id = c.index("Submission ID") if "Submission ID" in c else None
            idx_pay = c.index("Payment Status") if "Payment Status" in c else None
            break

    subs = []
    for row in rows:
        c = cells(row)
        if not c or not c[0].isdigit():  # header and separator rows
            continue
        state = ""
        if idx_state is not None and idx_state < len(c):
            state = c[idx_state]
        if state not in KNOWN:
            # Fall back to scanning the row for a known token.
            found = [s for s in KNOWN if re.search(r"\b%s\b" % s, row)]
            state = found[0] if found else (state or "UNKNOWN")
        subs.append(
            {
                "id": c[idx_id] if idx_id is not None and idx_id < len(c) else "",
                "state": state,
                "payment": c[idx_pay] if idx_pay is not None and idx_pay < len(c) else "",
            }
        )
    return subs


PAY_ORDER = ["PAYOUT_SUBMITTED", "PENDING"]


def payment_lines(records, prev_records, paid_when):
    """Rows for a payment chart, plus the one line that actually needs acting on.

    Payment lags status, so the count that matters is not "how many are pending" but
    "how many have finished the work and are still unpaid" - paid_when names the states
    where payment is owed.
    """
    counts = {}
    for r in records:
        counts[(r.get("payment") or "UNKNOWN").upper()] = counts.get(
            (r.get("payment") or "UNKNOWN").upper(), 0) + 1
    if not counts or set(counts) == {"UNKNOWN"}:
        return []
    order = [k for k in PAY_ORDER if k in counts] + sorted(k for k in counts if k not in PAY_ORDER)
    peak = max(counts.values())
    # A snapshot written before payment was tracked has no "payment" key at all, and
    # reading that as zero would print a full-count delta on the first run after the
    # upgrade. Treat "the field was never recorded" as no baseline rather than as none.
    has_baseline = any("payment" in r for r in (prev_records or []))
    prev_counts = {}
    if has_baseline:
        for r in prev_records:
            key = (r.get("payment") or "UNKNOWN").upper()
            prev_counts[key] = prev_counts.get(key, 0) + 1

    out = []
    for key in order:
        n = counts[key]
        before = prev_counts.get(key, 0) if has_baseline else None
        out.append("  %-20s %-*s %3d   %s"
                   % (key.replace("_", " ").capitalize(), BAR_WIDTH, bar(n, peak), n,
                      fmt_delta(n, before)))
    owed = [r for r in records
            if r.get("state") in paid_when
            and (r.get("payment") or "").upper() != "PAYOUT_SUBMITTED"]
    if owed:
        out.append("    %d of these are %s with no payout submitted"
                   % (len(owed), " or ".join(sorted(paid_when)).lower()))
    return out


def run_refinements_cli():
    """Raw stdout from `stb submissions list` on the refinement project, or None.

    Non-fatal like the reviews call: a refinement failure must not take the submissions
    report down, and not every session has refinement work.
    """
    if not refinements_configured():
        return None
    cmd = ["stb", "submissions", "list", "-p", REFINE_PROJECT_ID]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    return proc.stdout if proc.returncode == 0 else None


def parse_refinements(output, now=None):
    """[{id, state, payment, created_date}] from the refinement project's table.

    `Created At` comes back as "09/11 11:42" with no year, so the year is inferred:
    this year, unless that would put the row in the future, in which case it is last
    year's. Refinements are days old in practice, so this only matters across a New Year.
    """
    if not output:
        return []
    now = now or datetime.now(EASTERN)
    rows = [ln.strip() for ln in output.splitlines() if ln.strip().startswith("\u2502")]

    def cells(line):
        return [c.strip() for c in line.strip().strip("\u2502").split("\u2502")]

    idx = {}
    for row in rows:
        c = cells(row)
        if "Assignment State" in c:
            for name, key in (("Submission ID", "id"), ("Assignment State", "state"),
                              ("Payment Status", "payment"), ("Created At", "created")):
                if name in c:
                    idx[key] = c.index(name)
            break
    if "state" not in idx or "id" not in idx:
        return []

    out = []
    for row in rows:
        c = cells(row)
        if not c or not c[0].isdigit():  # header and separator rows
            continue
        rec = {k: (c[i] if i < len(c) else "") for k, i in idx.items()}
        raw = rec.pop("created", "")
        rec["created_date"] = ""
        m = re.match(r"(\d{2})/(\d{2})", raw)
        if m:
            mo, day = int(m.group(1)), int(m.group(2))
            year = now.year
            try:
                if datetime(year, mo, day, tzinfo=EASTERN).date() > now.date():
                    year -= 1
                rec["created_date"] = "%04d-%02d-%02d" % (year, mo, day)
            except ValueError:
                pass
        if rec["state"] not in KNOWN:
            found = [s for s in KNOWN if re.search(r"\b%s\b" % s, row)]
            rec["state"] = found[0] if found else (rec["state"] or "UNKNOWN")
        out.append(rec)
    return out


def refinement_meta(uid):
    """(task_name, origin_submission_id) from refinements/<uid>/metadata.json."""
    meta = REFINEMENTS_DIR / uid / "metadata.json"
    if not meta.exists():
        return "", ""
    try:
        d = json.loads(meta.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return "", ""
    r = d.get("refinement") or {}
    return d.get("task_name") or "", r.get("origin_submission_id") or ""


UID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")


def refine_header_columns(line):
    """Column names of the refinement table header, or None.

    split_row/header_columns above are submission-specific: they identify a data row by a
    numeric Seq in the first cell and a header by the literal "Seq". A refinement row
    leads with its UID and has no Seq at all, so it needs its own pair - without these the
    file re-reads as empty and every row is re-added on every run.
    """
    if not line.strip().startswith("|"):
        return None
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return cells if cells and cells[0] == "Task UID" else None


def refine_split_row(line):
    """Cells of a refinement data row, identified by carrying a UID cell."""
    if not line.strip().startswith("|"):
        return None
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) < 4 or not any(UID_RE.match(c) for c in cells):
        return None
    return cells


def parse_refinement_list(text):
    """(preamble, rows) from refinement-list.md - one table, status in its own cell."""
    lines = text.splitlines()
    preamble, rows, columns = [], [], list(REFINE_COLUMNS)
    for line in lines:
        head = refine_header_columns(line)
        if head:
            columns = head
            continue
        cells = refine_split_row(line)
        if not cells:
            # The "## All refinements (n)" heading is re-emitted by the renderer, so it
            # must not also be captured as preamble or it doubles on every write.
            if not rows and not line.strip().startswith(("|", "## ")):
                preamble.append(line)
            continue
        row = {"note": "", "status": "", "name": "", "updated": "-"}
        for name, cell in zip(columns, cells):
            key = REFINE_CELL_KEYS.get(name)
            if key:
                row[key] = "" if cell == "-" else cell
        if row.get("uid"):
            rows.append(row)
    return "\n".join(preamble).rstrip("\n"), rows


def load_refinement_list():
    """(preamble, rows, {uid: row}) from refinement-list.md, or the skeleton if absent."""
    if not REFINEMENT_LIST.exists():
        return REFINE_PREAMBLE, [], {}
    preamble, rows = parse_refinement_list(REFINEMENT_LIST.read_text(encoding="utf-8"))
    return (preamble or REFINE_PREAMBLE), rows, {r["uid"]: r for r in rows}


def render_refinement_list(preamble, rows):
    """One table, grouped by the STATUSES order then newest first inside each status."""
    order = {s: i for i, s in enumerate(STATUSES)}
    rows = sorted(rows, key=lambda r: (order.get(r.get("status"), len(STATUSES)),
                                       r.get("uid", "")))
    parts = [preamble.rstrip("\n")] if preamble.strip() else []
    body = ["| " + " | ".join(REFINE_COLUMNS) + " |",
            "|" + "|".join("-" * (len(c) + 2) for c in REFINE_COLUMNS) + "|"]
    for r in rows:
        body.append("| " + " | ".join(r.get(REFINE_CELL_KEYS[c]) or "-"
                                      for c in REFINE_COLUMNS) + " |")
    parts.append("## All refinements (%d)\n\n%s" % (len(rows), "\n".join(body)))
    return "\n\n".join(parts).rstrip("\n") + "\n"


def refinement_zip(row):
    """accepted/ file name for a refinement: r-{task-name}-{uid8}.zip.

    Not {task-name}.zip: a task can be refined more than once, so the name alone
    collides across rounds, and it can also collide with the submission of the same
    name already in accepted/. The r- prefix and the uid stem keep all three apart.
    """
    return "r-%s-%s" % (row.get("name") or "unnamed", row["uid"][:8])


def archive_accepted_refinement(row):
    """Zip refinements/<uid>/ into accepted/r-{name}-{uid8}.zip and remove the folder.

    The zip holds the folder under a <uid>/ top-level directory, so restoring it puts
    it back exactly where /revise-refinement expects. Idempotent: a refinement already
    zipped with no folder left is a no-op. Returns (ok, message).
    """
    uid = row["uid"]
    src = REFINEMENTS_DIR / uid
    stem = refinement_zip(row)
    dst = ACCEPTED_DIR / ("%s.zip" % stem)
    if not src.is_dir():
        if dst.exists():
            return True, "already archived"
        return False, "no refinements/%s folder and no accepted/%s.zip" % (uid[:8], stem)
    ACCEPTED_DIR.mkdir(parents=True, exist_ok=True)
    shutil.make_archive(str(ACCEPTED_DIR / stem), "zip", root_dir=REFINEMENTS_DIR, base_dir=uid)
    shutil.rmtree(src)
    return True, "zipped into accepted/%s.zip, refinements/%s removed" % (stem, uid[:8])


def restore_accepted_refinement(row):
    """Unzip accepted/r-{name}-{uid8}.zip back into refinements/ and drop the zip.

    The inverse, for a refinement that LEAVES ACCEPTED and has to be worked on again.
    Without it the zip would sit in accepted/ while the row said NEEDS_REVISION and
    /revise-refinement would find no folder - the drift that hit tasks 04, 10 and 22 on
    the submissions side (2026-08-27).
    """
    uid = row["uid"]
    stem = refinement_zip(row)
    src = ACCEPTED_DIR / ("%s.zip" % stem)
    dst = REFINEMENTS_DIR / uid
    if dst.is_dir():
        return (True, "already restored") if not src.exists() else (
            False, "both refinements/%s and accepted/%s.zip exist" % (uid[:8], stem))
    if not src.exists():
        return False, "no accepted/%s.zip to restore" % stem
    REFINEMENTS_DIR.mkdir(parents=True, exist_ok=True)
    shutil.unpack_archive(str(src), str(REFINEMENTS_DIR), "zip")
    if not dst.is_dir():
        return False, "accepted/%s.zip did not contain a %s/ directory" % (stem, uid)
    src.unlink()
    return True, "restored to refinements/%s, accepted/%s.zip removed" % (uid[:8], stem)


def sweep_accepted_refinements(rows, apply_changes):
    """Zip every ACCEPTED refinement away, and restore any that left ACCEPTED."""
    archived, restored = [], []
    for r in rows:
        uid = r.get("uid")
        if not uid:
            continue
        if r["status"] == "ACCEPTED":
            if not (REFINEMENTS_DIR / uid).is_dir():
                continue
            if not apply_changes:
                archived.append((r, True, "would zip into accepted/%s.zip" % refinement_zip(r)))
                continue
            archived.append((r,) + archive_accepted_refinement(r))
        elif (ACCEPTED_DIR / ("%s.zip" % refinement_zip(r))).exists():
            if not apply_changes:
                restored.append((r, True, "would restore from accepted/%s.zip" % refinement_zip(r)))
                continue
            restored.append((r,) + restore_accepted_refinement(r))
    return archived, restored


def sync_refinement_list(refs, now, apply_changes, tasks=None):
    """Reconcile refinement-list.md against the platform. Returns report lines.

    `tasks` is submission-list.md's {uid: row}, used to fill Note: a refinement whose
    origin_submission_id is one of ours gets that task's name, and a blank Note means it
    refines another contributor's submission.
    """
    preamble, rows, index = load_refinement_list()
    tasks = tasks or {}
    added, moved, unfetched, orphans = [], [], [], []
    stamp = now_stamp(now)

    for s in refs:
        uid = s["id"]
        name, origin = refinement_meta(uid)
        own = (tasks.get(origin) or {}).get("name", "") if origin else ""
        row = index.get(uid)
        if row is None:
            row = {"uid": uid, "name": name or "?", "status": s["state"],
                   "updated": stamp, "note": own}
            rows.append(row)
            index[uid] = row
            added.append("%s %s - %s" % (uid[:8], row["name"], s["state"]))
        elif row["status"] != s["state"]:
            moved.append("%s %s: %s -> %s" % (uid[:8], row.get("name") or "?",
                                              row["status"], s["state"]))
            row["status"] = s["state"]
            row["updated"] = stamp
        for key, val in (("name", name), ("note", own)):
            if val and (not row.get(key) or row.get(key) == "?"):
                row[key] = val
        if not (REFINEMENTS_DIR / uid / "metadata.json").exists():
            unfetched.append("%s %s (%s)" % (uid[:8], row.get("name") or "?", s["state"]))

    on_platform = {s["id"] for s in refs}
    for uid in sorted(set(index) - on_platform):
        orphans.append("%s %s (row says %s)" % (uid[:8], index[uid].get("name") or "?",
                                                index[uid]["status"]))

    if apply_changes and (added or moved or not REFINEMENT_LIST.exists()):
        REFINEMENT_LIST.write_text(render_refinement_list(preamble, rows), encoding="utf-8")

    # An accepted refinement is finished work: zip it into accepted/ and drop the folder,
    # the same steady state an accepted submission reaches.
    archived, restored = sweep_accepted_refinements(rows, apply_changes)

    out = []
    verb = "Updated" if apply_changes else "Would update"
    if added:
        out.append("  %s refinement-list.md, added:" % verb)
        out += ["    + %s" % a for a in added]
    if moved:
        out.append("  %s refinement-list.md, moved:" % verb)
        out += ["    > %s" % m for m in moved]
    if unfetched:
        out.append("  Not fetched yet (no refinements/<uid>/):")
        out += ["    ? %s - run /refine-task <uid>" % u for u in unfetched]
    if orphans:
        out.append("  Rows the platform no longer lists (left alone, check by hand):")
        out += ["    - %s" % o for o in orphans]
    if not out:
        out.append("  refinement-list.md matches the platform exactly (%d)." % len(refs))
    if archived:
        out.append("  %s accepted refinements into accepted/:" % ("Archived" if apply_changes else "Would archive"))
        out += ["    %s %s %s: %s" % ("+" if ok else "!", r["uid"][:8], r.get("name") or "?", msg)
                for r, ok, msg in archived]
    if restored:
        out.append("  %s from accepted/ (no longer ACCEPTED):" % ("Restored" if apply_changes else "Would restore"))
        out += ["    %s %s %s: %s" % ("+" if ok else "!", r["uid"][:8], r.get("name") or "?", msg)
                for r, ok, msg in restored]
    own_n = sum(1 for r in rows if r.get("note"))
    out.append("  %d of %d refine one of our own submissions." % (own_n, len(rows)))
    return out


def run_reviews_cli():
    """Raw stdout from `stb reviews list`, or None.

    A reviews failure must never take the submissions report down with it: not every
    contributor has reviewer access, and the section is additive.
    """
    cmd = ["stb", "reviews", "list", "-p", PROJECT_ID]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    return proc.stdout if proc.returncode == 0 else None


def parse_reviews(output):
    """[{id, state, payment, created}] from `stb reviews list`'s box-drawing table."""
    if not output:
        return []
    rows = [ln.strip() for ln in output.splitlines() if ln.strip().startswith("\u2502")]

    def cells(line):
        return [c.strip() for c in line.strip().strip("\u2502").split("\u2502")]

    idx = {}
    for row in rows:
        c = cells(row)
        if "Assignment State" in c:
            for name, key in (("Review ID", "id"), ("Assignment State", "state"),
                              ("Payment Status", "payment"), ("Created At", "created")):
                if name in c:
                    idx[key] = c.index(name)
            break
    if "state" not in idx:
        return []

    out = []
    for row in rows:
        c = cells(row)
        if not c or not c[0].isdigit():  # header and separator rows
            continue
        rec = {}
        for key, i in idx.items():
            rec[key] = c[i] if i < len(c) else ""
        rec.setdefault("state", "UNKNOWN")
        out.append(rec)
    return out


def label_for(sub, tasks):
    """The submission-list.md task name, falling back to a short UID."""
    row = tasks.get(sub["id"])
    if row:
        return "%s %s" % (row["seq"], row["name"])
    return sub["id"][:8]


def tally(subs):
    counts = {}
    for s in subs:
        counts[s["state"]] = counts.get(s["state"], 0) + 1
    return counts


def load_previous():
    if not HISTORY.exists():
        return None
    prev = None
    for line in HISTORY.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            prev = json.loads(line)
        except json.JSONDecodeError:
            continue  # skip a corrupt line rather than losing the whole history
    return prev


def save(snapshot):
    HISTORY.parent.mkdir(parents=True, exist_ok=True)
    with HISTORY.open("a") as fh:
        fh.write(json.dumps(snapshot) + "\n")


def fmt_delta(now, before):
    if before is None:
        return ""
    d = now - before
    if d > 0:
        return "+%d" % d
    if d < 0:
        return "-%d" % abs(d)
    return "."


def ago(then, now):
    secs = (now - then).total_seconds()
    if secs < 90:
        return "just now"
    mins = secs / 60
    if mins < 90:
        return "%d minutes ago" % round(mins)
    hours = mins / 60
    if hours < 36:
        return "%d hours ago" % round(hours)
    return "%d days ago" % round(hours / 24)


# The platform runs three gates in order: AutoEval, then a human reviewer, then
# adjudication. Only the first two have an Assignment State of their own, so
# REVIEW_PENDING covers both "sitting with the reviewer" (gate 2) and "reviewer
# cleared it, sitting with adjudication" (gate 3).
#
# Every unequal row means the platform has moved past it and submission-list.md is
# stale. The platform is the source of truth for state, so unequal rows are
# caught up to whatever it reports on every run rather than reported as
# standing discrepancies. REMARKS annotates the ones worth a word of
# explanation; an unlisted pair is ordinary forward progress along the pipeline.
REMARKS = {
    ("NEEDS_REVISION", "EVALUATION_PENDING"): "resubmitted, AutoEval running",
    ("NEEDS_REVISION", "REVIEW_PENDING"): "resubmitted and cleared AutoEval, now with the reviewer",
    ("OFFERED", "EVALUATION_PENDING"): "submitted, AutoEval running",
    ("OFFERED", "REVIEW_PENDING"): "submitted and cleared AutoEval",
    ("EVALUATION_PENDING", "REVIEW_PENDING"): "cleared AutoEval, now with the reviewer",
    ("REVIEW_PENDING", "ACCEPTED"): "accepted",
    ("NEEDS_REVISION", "ACCEPTED"): "accepted outright",
    ("ACCEPTED", "NEEDS_REVISION"): "it came back after acceptance",
    ("ACCEPTED", "REVIEW_PENDING"): "not accepted yet; back with the reviewer or adjudication",
    ("ACCEPTED", "REJECTED"): "rejected after acceptance",
}

# Landing on one of these is more than a status change: the findings and the
# pending platform actions belong in that task's feedback-log.md.
NEEDS_FOLLOW_UP = ("NEEDS_REVISION", "REJECTED")


def classify(subs, tasks):
    """Place each submission on the pipeline using submission-list.md.

    Returns aligned count, catch-up entries (each carrying a reference to the
    row dict itself, so applying one is a plain mutation), submissions with no
    submission-list.md row at all, submissions reporting a state this script does not
    know, and rows whose local status token isn't one of the six.
    """
    aligned, catch_up, no_row, unrecognised, unreadable = 0, [], [], [], []
    for s in subs:
        row = tasks.get(s["id"])
        if row is None:
            no_row.append(s)
            continue
        if row["status"] == s["state"]:
            aligned += 1
        elif s["state"] not in KNOWN:
            unrecognised.append((row, s))
        elif row["status"] not in STATUSES:
            # Never catch such a row up: an unreadable token is not evidence
            # that submission-list.md is behind, and overwriting it discards whatever
            # the row was actually recording.
            unreadable.append(row)
        else:
            catch_up.append(
                {
                    "row": row,
                    "seq": row["seq"],
                    "name": row["name"],
                    "old": row["status"],
                    "new": s["state"],
                    "remark": REMARKS.get((row["status"], s["state"]), ""),
                    "follow_up": s["state"] in NEEDS_FOLLOW_UP,
                }
            )
    return aligned, catch_up, no_row, unrecognised, unreadable


def vanished(tasks, subs):
    """submission-list.md rows whose UID the platform no longer lists at all."""
    live = {s["id"] for s in subs}
    return [
        r for uid, r in sorted(tasks.items(), key=lambda kv: int(kv[1]["seq"]))
        if uid not in live
    ]


def apply_catch_ups(catch_up, now):
    for c in catch_up:
        c["row"]["status"] = c["new"]
        c["row"]["updated"] = now_stamp(now)
    return catch_up


def archive_task(seq, name):
    """Reduce submissions/{seq}-{name}/ to archived/{seq}-{name}/prompt.md.

    Returns (ok, message). Idempotent: a task already archived is a no-op.
    """
    folder = "%s-%s" % (seq, name)
    src = SUBMISSIONS_DIR / folder
    dst = ARCHIVED / folder
    if (dst / "prompt.md").exists():
        return True, "already archived"
    if not src.exists():
        return False, "no submissions/%s folder found to archive" % folder
    prompt_src = src / "prompt.md"
    if not prompt_src.exists():
        return False, "submissions/%s has no prompt.md to archive" % folder
    dst.mkdir(parents=True, exist_ok=True)
    shutil.copy2(prompt_src, dst / "prompt.md")
    shutil.rmtree(src)
    return True, "archived, submissions/%s removed" % folder


PAYMENT_NOTE = {"PAYOUT_SUBMITTED": "Payout submitted", "PENDING": "Payment pending"}


def reject_and_archive(gone, now, prev_states=None):
    """Move each vanished-UID row to REJECTED and archive its task folder.

    A row already REJECTED is left alone but still gets an archive attempt,
    covering a prior run whose archive step didn't complete.

    The Note records what the row's own history says about why it vanished.
    A row that had reached ACCEPTED did not fail: the platform took it into
    the refinement pipeline, and it still pays out. That, plus its last known
    payment status - read from the previous snapshot, since a vanished UID
    can no longer be queried - is what the Note carries.
    """
    prev_states = prev_states or {}
    newly_rejected, archive_results = [], []
    for r in gone:
        if r["status"] != "REJECTED":
            went_to_refinement = r["status"] == "ACCEPTED"
            prev = prev_states.get(r["uid"]) or {}
            pay = PAYMENT_NOTE.get((prev.get("payment") or "").upper(), "")
            bits = [b for b in (pay, "refinement pipeline" if went_to_refinement else "") if b]
            r["status"] = "REJECTED"
            r["updated"] = now_stamp(now)
            r["note"] = "; ".join(bits)
            newly_rejected.append(r)
        ok, msg = archive_task(r["seq"], r["name"])
        archive_results.append((r, ok, msg))
    return newly_rejected, archive_results


def archive_accepted_task(seq, name):
    """Zip submissions/{seq}-{name}/ into accepted/{seq}-{name}.zip and remove the folder.

    The zip holds the whole folder under a {seq}-{name}/ top-level directory,
    matching the hand-built zips already in accepted/. Returns (ok, message).
    Idempotent: a task already zipped with no submissions/ folder left is a no-op.
    """
    folder = "%s-%s" % (seq, name)
    src = SUBMISSIONS_DIR / folder
    dst = ACCEPTED_DIR / ("%s.zip" % folder)
    if not src.exists():
        if dst.exists():
            return True, "already archived"
        return False, "no submissions/%s folder and no accepted/%s.zip" % (folder, folder)
    ACCEPTED_DIR.mkdir(parents=True, exist_ok=True)
    shutil.make_archive(str(ACCEPTED_DIR / folder), "zip", root_dir=SUBMISSIONS_DIR, base_dir=folder)
    shutil.rmtree(src)
    return True, "zipped into accepted/%s.zip, submissions/%s removed" % (folder, folder)


def accepted_needing_archive(rows):
    """ACCEPTED rows not yet in their steady state (zip present, submissions/ folder gone)."""
    return [
        r
        for r in sorted((r for r in rows if r["status"] == "ACCEPTED"), key=lambda r: int(r["seq"]))
        if (SUBMISSIONS_DIR / ("%s-%s" % (r["seq"], r["name"]))).exists()
        or not (ACCEPTED_DIR / ("%s-%s.zip" % (r["seq"], r["name"]))).exists()
    ]


def restore_from_accepted(seq, name):
    """Unzip accepted/{seq}-{name}.zip back into submissions/ and drop the zip.

    The inverse of archive_accepted_task, for a task that LEAVES ACCEPTED — it
    comes back as NEEDS_REVISION and its folder has to exist again to be revised.
    Without this the zip sat in accepted/ while the row said otherwise, which is
    how 04, 10 and 22 drifted (2026-08-27). Returns (ok, message).
    """
    folder = "%s-%s" % (seq, name)
    src = ACCEPTED_DIR / ("%s.zip" % folder)
    dst = SUBMISSIONS_DIR / folder
    if dst.exists():
        return (True, "already restored") if not src.exists() else (
            False, "both submissions/%s and accepted/%s.zip exist" % (folder, folder))
    if not src.exists():
        return False, "no accepted/%s.zip to restore" % folder
    SUBMISSIONS_DIR.mkdir(parents=True, exist_ok=True)
    shutil.unpack_archive(str(src), str(SUBMISSIONS_DIR), "zip")
    if not dst.is_dir():
        return False, "accepted/%s.zip did not contain a %s/ directory" % (folder, folder)
    src.unlink()
    return True, "restored to submissions/%s, accepted/%s.zip removed" % (folder, folder)


def accepted_needing_restore(rows):
    """Rows that left ACCEPTED for rework whose accepted/ zip is still sitting there.

    Excludes REJECTED: a row that vanished after reaching ACCEPTED goes through
    reject_and_archive instead, which reduces it to archived/{name}/prompt.md -
    the zip is not meant to come back as a working folder for that path.
    """
    return [
        r
        for r in sorted(
            (r for r in rows if r["status"] not in ("ACCEPTED", "REJECTED")),
            key=lambda r: int(r["seq"]),
        )
        if (ACCEPTED_DIR / ("%s-%s.zip" % (r["seq"], r["name"]))).exists()
        and not (SUBMISSIONS_DIR / ("%s-%s" % (r["seq"], r["name"]))).exists()
    ]


def restore_accepted(rows):
    """Restore every row that left ACCEPTED but whose folder is still a zip."""
    return [
        (r,) + restore_from_accepted(r["seq"], r["name"])
        for r in accepted_needing_restore(rows)
    ]


def archive_accepted(rows):
    """Archive every ACCEPTED row whose submissions/ folder still exists.

    Covers both a row that just landed on ACCEPTED this run and one accepted on
    an earlier run whose archive step never happened. Rows already in their
    steady state are skipped silently rather than reported every run.
    """
    return [
        (r,) + archive_accepted_task(r["seq"], r["name"])
        for r in accepted_needing_archive(rows)
    ]


def find_draft_by_uid(uid):
    """The drafts/{seq}-{name}/ folder whose metadata.json carries this UID, if any."""
    if not DRAFTS_DIR.exists():
        return None
    uid_l = uid.lower()
    for meta in sorted(DRAFTS_DIR.glob("*/metadata.json")):
        try:
            got = json.loads(meta.read_text(encoding="utf-8")).get("taskboard_uid")
        except (ValueError, OSError):
            continue
        if got and got.lower() == uid_l:
            return meta.parent
    return None


def promote_draft(draft_folder, sub, now):
    """Move a matched draft into submissions/ and return its new submission-list.md row, or

    (None, reason) if the folder name or destination is unusable.
    """
    m = DRAFT_FOLDER_RE.match(draft_folder.name)
    if not m:
        return None, "draft folder %r doesn't match {seq}-{name}" % draft_folder.name
    seq, name = m.group(1), m.group(2)
    dest = SUBMISSIONS_DIR / draft_folder.name
    if dest.exists():
        return None, "submissions/%s already exists" % draft_folder.name
    shutil.move(str(draft_folder), str(dest))
    rename_rubric_for_uid(dest, sub["id"])
    row = {
        "seq": seq,
        "name": name,
        "uid": sub["id"],
        "updated": now_stamp(now),
        "model": model_for(dest),
        "note": "",
        "status": sub["state"],
    }
    return row, None


def model_for(folder):
    """The model that built a task folder, from metadata.json's built_with, or "".

    An accepted task's folder is gone (zipped) and a rejected one is reduced to
    prompt.md, so those rows keep whatever the table already holds — the value is
    recovered once, by tools/build_model.py attribute, and then persists in the file.
    """
    meta = folder / "metadata.json"
    if meta.exists():
        try:
            return json.loads(meta.read_text(encoding="utf-8")).get("built_with") or ""
        except (ValueError, OSError):
            return ""
    return ""


def rename_rubric_for_uid(folder, uid):
    """Give a just-promoted folder's rubric its UID suffix.

    A draft carries rubric-{name}.csv because it has no UID yet; under
    submissions/ the convention is rubric-{name}-{uid8}.csv. Silent when the
    rubric is missing or already suffixed — promotion must not fail over it.
    """
    for csv in sorted(folder.glob("rubric-*.csv")):
        stem = csv.stem
        if re.fullmatch(r"rubric-.+-[0-9a-f]{8}", stem):
            continue
        csv.rename(folder / ("%s-%s.csv" % (stem, uid[:8])))
        return


def promote_drafts(no_row, now):
    """Match OFFERED/EVALUATION_PENDING submissions with no row to a draft.

    Returns (promoted rows, still-unmatched submissions).
    """
    promoted, still = [], []
    for s in no_row:
        if s["state"] not in ("OFFERED", "EVALUATION_PENDING"):
            still.append(s)
            continue
        draft = find_draft_by_uid(s["id"])
        if not draft:
            still.append(s)
            continue
        row, reason = promote_draft(draft, s, now)
        if row is None:
            still.append(s)  # reason surfaces via unmapped reporting below
        else:
            promoted.append(row)
    return promoted, still


def format_catch_up(c):
    line = "    %s %s: %s -> %s" % (c["seq"], c["name"], c["old"] or "(blank)", c["new"])
    if c["remark"]:
        line += "  (%s)" % c["remark"]
    return line


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument(
        "--no-apply",
        action="store_true",
        help="report the submission-list.md and refinement-list.md changes without writing them",
    )
    args = ap.parse_args()

    require_project_ids()

    subs = parse(run_cli())
    reviews = parse_reviews(run_reviews_cli())
    now_for_refs = datetime.now(EASTERN)
    refs = parse_refinements(run_refinements_cli(), now_for_refs)
    preamble, rows, tasks = load_tasks_md()
    counts = tally(subs)
    now = datetime.now(EASTERN)

    prev = load_previous()
    prev_counts = prev["counts"] if prev else None
    prev_states = {s["id"]: s for s in prev.get("submissions", [])} if prev else {}

    lines = []
    lines.append("Hazy submissions - %s" % now.strftime("%Y-%m-%d %H:%M %Z"))
    lines.append("")

    # Chart every state that has a task in it, not just the four the report leads
    # with - a REJECTED or OFFERED pile is part of "all tasks by status", and hiding
    # it makes the bars add up to less than the total.
    charted = [(k, lab) for k, lab in PRIMARY]
    charted += [(k, lab) for k, lab in SECONDARY if counts.get(k, 0)]
    peak = max([counts.get(k, 0) for k, _ in charted] or [0])

    for key, label in charted:
        n = counts.get(key, 0)
        before = prev_counts.get(key, 0) if prev_counts is not None else None
        delta = fmt_delta(n, before)
        lines.append("  %-20s %-*s %3d   %s" % (label, BAR_WIDTH, bar(n, peak), n, delta))

    lines.append("  %s" % ("-" * (22 + BAR_WIDTH + 10)))
    total = len(subs)
    total_before = sum(prev_counts.values()) if prev_counts is not None else None
    lines.append("  %-20s %-*s %3d   %s"
                 % ("Total", BAR_WIDTH, "", total, fmt_delta(total, total_before)))

    unknown = sorted(k for k in counts if k not in KNOWN)
    if unknown:
        lines.append("")
        lines.append("  Unrecognised states: "
                     + ", ".join("%s %d" % (k, counts[k]) for k in unknown))

    pay = payment_lines(subs, prev.get("submissions") if prev else None, {"ACCEPTED"})
    if pay:
        lines.append("")
        lines.append("  Payment")
        lines.extend(pay)

    if reviews:
        prev_reviews = prev.get("review_counts") if prev else None
        r_counts = {}
        for r in reviews:
            r_counts[r["state"]] = r_counts.get(r["state"], 0) + 1
        charted_r = [(k, lab) for k, lab in REVIEW_PRIMARY if r_counts.get(k, 0)]
        charted_r += [(k, k.replace("_", " ").capitalize())
                      for k in sorted(r_counts) if k not in dict(REVIEW_PRIMARY)]
        r_peak = max([r_counts[k] for k, _ in charted_r] or [0])

        lines.append("")
        lines.append("  Review assignments (other contributors' tasks, assigned to me)")
        for key, label in charted_r:
            n = r_counts[key]
            before = prev_reviews.get(key, 0) if prev_reviews is not None else None
            lines.append("  %-20s %-*s %3d   %s"
                         % (label, BAR_WIDTH, bar(n, r_peak), n, fmt_delta(n, before)))
        r_pay = payment_lines(reviews, prev.get("reviews") if prev else None, set())
        if r_pay:
            lines.append("  Payment")
            lines.extend(r_pay)

    if refs:
        prev_refs = prev.get("refinement_counts") if prev else None
        f_counts = {}
        for r in refs:
            f_counts[r["state"]] = f_counts.get(r["state"], 0) + 1
        charted_f = [(k, lab) for k, lab in PRIMARY if f_counts.get(k, 0)]
        charted_f += [(k, lab) for k, lab in SECONDARY if f_counts.get(k, 0)]
        charted_f += [(k, k.replace("_", " ").capitalize()) for k in sorted(f_counts)
                      if k not in KNOWN]
        f_peak = max([f_counts[k] for k, _ in charted_f] or [0])

        lines.append("")
        lines.append("  Refinements (Hazy-Refinement project)")
        for key, label in charted_f:
            n = f_counts[key]
            before = prev_refs.get(key, 0) if prev_refs is not None else None
            lines.append("  %-20s %-*s %3d   %s"
                         % (label, BAR_WIDTH, bar(n, f_peak), n, fmt_delta(n, before)))
        lines.append("  %s" % ("-" * (22 + BAR_WIDTH + 10)))
        lines.append("  %-20s %-*s %3d   %s"
                     % ("Total", BAR_WIDTH, "", len(refs),
                        fmt_delta(len(refs), sum(prev_refs.values()) if prev_refs else None)))
        f_pay = payment_lines(refs, prev.get("refinements") if prev else None, {"ACCEPTED"})
        if f_pay:
            lines.append("  Payment")
            lines.extend(f_pay)

    lines.append("")
    if prev is None:
        lines.append("  First check - no previous snapshot, so no deltas. Baseline saved.")
    else:
        then = datetime.fromisoformat(prev["timestamp"])
        lines.append(
            "  Compared against %s (%s)."
            % (then.astimezone(EASTERN).strftime("%Y-%m-%d %H:%M %Z"), ago(then, now))
        )
        moved = []
        for s in subs:
            was = prev_states.get(s["id"])
            name = label_for(s, tasks)
            if was is None:
                moved.append("    + new: %s - %s" % (name, s["state"]))
            elif was["state"] != s["state"]:
                moved.append("    > %s: %s to %s" % (name, was["state"], s["state"]))
            elif "payment" in was and (was["payment"] or "") != (s.get("payment") or ""):
                moved.append("    $ %s: payment %s to %s"
                             % (name, was["payment"] or "-", s.get("payment") or "-"))
        gone_since = [p for pid, p in prev_states.items() if pid not in {s["id"] for s in subs}]
        for p in gone_since:
            moved.append("    - gone: %s (was %s)" % (label_for(p, tasks), p["state"]))
        if moved:
            lines.append("")
            lines.append("  Movement since then:")
            lines.extend(moved)
        else:
            lines.append("  No submission changed state since then.")

    aligned, catch_up, no_row, unrecognised, unreadable = classify(subs, tasks)
    gone = vanished(tasks, subs)

    if args.no_apply:
        applied, newly_rejected, archive_results, promoted, still_no_row = [], [], [], [], no_row
        accepted_results = []
        # What the accepted sweep would touch, counting rows a catch-up would land
        # on ACCEPTED (their status isn't updated in --no-apply).
        would_accept = {id(c["row"]) for c in catch_up if c["new"] == "ACCEPTED"}
        pending_accept = accepted_needing_archive(
            [{**r, "status": "ACCEPTED"} if id(r) in would_accept else r for r in rows]
        )
        # Same projection as pending_accept, the other way round: a row the platform
        # has moved OFF ACCEPTED needs its folder back out of the zip.
        moves = {id(c["row"]): c["new"] for c in catch_up}
        projected = [{**r, "status": moves[id(r)]} if id(r) in moves else r for r in rows]
        pending_restore = accepted_needing_restore(projected)
        restore_results = []
    else:
        applied = apply_catch_ups(catch_up, now)
        newly_rejected, archive_results = reject_and_archive(gone, now, prev_states)
        promoted, still_no_row = promote_drafts(no_row, now)
        restore_results = restore_accepted(rows)
        accepted_results = archive_accepted(rows)
        pending_accept, pending_restore = [], []
        if applied or newly_rejected or archive_results or promoted or restore_results:
            rows.extend(promoted)
            SUBMISSION_LIST.write_text(render_submission_list(preamble, rows), encoding="utf-8")

    lines.append("")
    if applied:
        lines.append("  Updated submission-list.md (the platform is the source of truth):")
        lines.extend(format_catch_up(c) for c in applied)
        for c in applied:
            if c["follow_up"]:
                lines.append(
                    "      record the findings in submissions/%s-%s/feedback-log.md"
                    % (c["seq"], c["name"])
                )
        lines.append("")

    pending_catch_up = [] if not args.no_apply else catch_up
    if pending_catch_up:
        lines.append("  submission-list.md is behind the platform on:")
        lines.extend(format_catch_up(c) for c in pending_catch_up)
        lines.append("    Catch up by re-running without --no-apply.")
        lines.append("")

    if newly_rejected or (archive_results and not args.no_apply):
        lines.append("  Rejected and archived (UID dropped from the platform list):")
        for r, ok, msg in archive_results:
            why = (" - %s" % r["note"]) if r.get("note") else ""
            lines.append("    - %s %s: REJECTED%s (%s)"
                         % (r["seq"], r["name"], why, msg if ok else "ARCHIVE FAILED: " + msg))
        lines.append("")
    elif args.no_apply and any(r["status"] != "REJECTED" for r in gone):
        lines.append("  Would reject and archive (UID dropped from the platform list):")
        lines.extend("    - %s %s" % (r["seq"], r["name"]) for r in gone if r["status"] != "REJECTED")
        lines.append("")

    if any(ok for _, ok, _ in restore_results):
        lines.append("  Restored from accepted/ (left ACCEPTED, folder needed again):")
        for r, ok, msg in restore_results:
            if ok:
                lines.append("    - %s %s: %s" % (r["seq"], r["name"], msg))
        lines.append("")
    if pending_restore:
        lines.append("  Would restore from accepted/ (re-run without --no-apply):")
        lines.extend("    - %s %s" % (r["seq"], r["name"]) for r in pending_restore)
        lines.append("")

    if any(ok for _, ok, _ in accepted_results):
        lines.append("  Accepted and archived (submissions/ folder zipped into accepted/):")
        for r, ok, msg in accepted_results:
            if ok:
                lines.append("    - %s %s: %s" % (r["seq"], r["name"], msg))
        lines.append("")
    if pending_accept:
        lines.append("  Would archive into accepted/ (re-run without --no-apply):")
        lines.extend("    - %s %s" % (r["seq"], r["name"]) for r in pending_accept)
        lines.append("")

    if promoted:
        lines.append("  Promoted from drafts/ (new submission, no prior row):")
        lines.extend(
            "    + %s %s: %s" % (r["seq"], r["name"], r["status"]) for r in promoted
        )
        lines.append("")

    needs_attention = []
    for s in still_no_row:
        needs_attention.append(
            "    ? %s  %s  has no submission-list.md row and no matching draft" % (s["id"][:8], s["state"])
        )
    for row, s in unrecognised:
        needs_attention.append(
            "    ? %s %s: platform reports an unrecognised state %s"
            % (row["seq"], row["name"], s["state"])
        )
    for row in unreadable:
        needs_attention.append(
            "    ? %s %s: sits under a %r section, which is not a recognised status"
            % (row["seq"], row["name"], row["status"])
        )
    for r, ok, msg in archive_results:
        if not ok:
            needs_attention.append("    ! %s %s: %s" % (r["seq"], r["name"], msg))
    for r, ok, msg in accepted_results:
        if not ok:
            needs_attention.append("    ! %s %s: %s" % (r["seq"], r["name"], msg))

    if needs_attention:
        lines.append("  Needs attention:")
        lines.extend(needs_attention)
    elif (
        not applied
        and not pending_catch_up
        and not newly_rejected
        and not promoted
        and not accepted_results
        and not pending_accept
    ):
        lines.append(
            "  Nothing to reconcile: all %d submission(s) match submission-list.md exactly."
            % aligned
        )

    if refs:
        lines.append("")
        lines.extend(sync_refinement_list(refs, now, not args.no_apply, tasks))

    print("\n".join(lines))

    save(
        {
            "timestamp": now.isoformat(),
            "counts": counts,
            "total": total,
            "submissions": subs,
            "review_counts": {r["state"]: sum(1 for x in reviews if x["state"] == r["state"])
                              for r in reviews},
            "reviews": reviews,
            "refinement_counts": {r["state"]: sum(1 for x in refs if x["state"] == r["state"])
                                  for r in refs},
            "refinements": refs,
        }
    )


if __name__ == "__main__":
    main()
