#!/usr/bin/env python3
"""Record and recover which model built a task.

Claude Code writes one JSONL transcript per session under
~/.claude/projects/<slugified-cwd>/, and every assistant message in it carries the
model id it was produced by. That file is the ground truth for "which model did this",
and it is available two ways:

  current      the model driving THIS session, resolved through $CLAUDE_CODE_SESSION_ID
  attribute    the model that FIRST wrote a task folder, recovered by scanning every
               transcript for tool calls naming that folder (works retroactively)
  stamp        record the model in <folder>/metadata.json's built_with
  read         print the model recorded for a task folder
  check        compare the recorded model against this session's, exit 1 on a mismatch
  require      assert this session is running a named model, exit 1 if it is not
  resolve      map a model flag (0 = fable, 1 = opus) to its full id
  uid          map a Taskboard UID to its task folder via submission-list.md

Usage:
    tools/build_model.py current
    tools/build_model.py attribute [submissions/20-foo ...]      # no args = every known task
    tools/build_model.py stamp submissions/20-foo [--model ID]   # default: current session
    tools/build_model.py stamp --all --infer               # backfill from transcripts
    tools/build_model.py read submissions/20-foo
    tools/build_model.py check submissions/20-foo
    tools/build_model.py require sonnet
    tools/build_model.py resolve 0
    tools/build_model.py uid 865d895b-3cf9-4ab8-a7fb-d341b7998f03
"""

import collections
import glob
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRANSCRIPTS = os.path.join(
    os.path.expanduser("~/.claude/projects"), REPO.replace("/", "-")
)
# Only two models author tasks here, and the command files select between them by flag.
MODELS = {"0": "claude-fable-5", "1": "claude-opus-5"}
ALIASES = {"fable": "claude-fable-5", "opus": "claude-opus-5",
           "sonnet": "claude-sonnet-5"}


def resolve(flag):
    """Model id for a create-task flag: 0 = fable, 1 = opus. Also accepts a name."""
    if flag is None:
        return None
    key = str(flag).strip().lower()
    return MODELS.get(key) or ALIASES.get(key) or (key if key.startswith("claude-") else None)


def _norm(model):
    """Drop context-window and date suffixes so claude-opus-5[1m] == claude-opus-5, and
    fold a point release into its family so claude-fable-5-1 == claude-fable-5 for the
    gate (2026-09-10: the session moved to Fable 5.1 while every stamp says
    claude-fable-5). Stamps keep the exact id; only the comparison is family-wide."""
    if not model:
        return ""
    m = re.sub(r"\[[^\]]*\]$", "", model.strip()).lower()
    return re.sub(r"^(claude-[a-z]+-\d+)-\d+$", r"\1", m)


def _assistant_models(path):
    """Yield (timestamp, model, tool_input_blob) for each assistant turn in a transcript."""
    cur = None
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            try:
                d = json.loads(line)
            except Exception:
                continue
            msg = d.get("message") or {}
            model = msg.get("model")
            if model and model != "<synthetic>":
                cur = model
            if d.get("type") != "assistant" or not cur:
                continue
            content = msg.get("content")
            if not isinstance(content, list):
                continue
            blob = "".join(
                json.dumps({"name": c.get("name"), "input": c.get("input", {})})
                for c in content
                if isinstance(c, dict) and c.get("type") == "tool_use"
            )
            yield d.get("timestamp", ""), cur, blob


def current():
    """The model driving this session, or None outside a Claude Code session."""
    sid = os.environ.get("CLAUDE_CODE_SESSION_ID")
    if not sid:
        return None
    path = os.path.join(TRANSCRIPTS, f"{sid}.jsonl")
    if not os.path.exists(path):
        return None
    last = None
    for _, model, _ in _assistant_models(path):
        last = model
    return last


def read(folder):
    """The model recorded for a task folder: metadata.json's built_with.

    An archived folder is reduced to prompt.md and has no metadata.json, so it reads as
    None; recover those with `attribute`, which reads the transcripts."""
    return _load_meta(folder)[0].get("built_with") or None


def _load_meta(folder):
    """(metadata dict, path). An absent or unreadable file reads as {}."""
    meta = os.path.join(folder, "metadata.json")
    if not os.path.exists(meta):
        return {}, meta
    try:
        return json.load(open(meta, encoding="utf-8")), meta
    except (ValueError, OSError):
        return {}, meta


def uid_folder(uid):
    """Task folder for a Taskboard UID, resolved through the submission-list.md index."""
    tasks_md = os.path.join(REPO, "submission-list.md")
    if not os.path.exists(tasks_md):
        return None
    for line in open(tasks_md, encoding="utf-8"):
        if uid.lower() not in line.lower():
            continue
        for cell in (c.strip() for c in line.split("|")):
            cand = os.path.join(REPO, "submissions", cell)
            if cell and os.path.isdir(cand):
                return cand
        # The table may carry the bare name without its sequence prefix.
        for cell in (c.strip() for c in line.split("|")):
            for d in glob.glob(os.path.join(REPO, "submissions", f"*-{cell}")):
                if os.path.isdir(d):
                    return d
    return None


def _known_tasks():
    out = []
    for pat in ("submissions/*", "drafts/*", "archived/*"):
        out += [p for p in glob.glob(os.path.join(REPO, pat)) if os.path.isdir(p)]
    out += [p[:-4] for p in glob.glob(os.path.join(REPO, "accepted/*.zip"))]
    return sorted(out)


# Reading a folder is not authoring it: uniqueness diffing opens old prompts, and a
# plain mention would credit the reader. Only turns that could have WRITTEN the folder
# count -- the file-writing tools, or a shell command carrying a write-ish token.
WRITE_TOOLS = ("Write", "Edit", "MultiEdit", "NotebookEdit")
WRITE_SHELL = re.compile(r">>?\s|\bcp\b|\bmv\b|\bmkdir\b|\bzip\b|\btee\b|"
                         r"sed -i|python|\brm\b|\btouch\b|<<")


def _authored(blob):
    """True if this assistant turn wrote files rather than merely reading them."""
    if any(f'"name": "{t}"' in blob for t in WRITE_TOOLS):
        return True
    return '"name": "Bash"' in blob and bool(WRITE_SHELL.search(blob))


def attribute(folders):
    """folder -> [(model, first_day, write_count, session)] ordered earliest first.

    The earliest model to write a folder is the one that built it; later models are
    revisions. Accepted tasks live on as a bare zip, so their folder name is matched
    with and without the {NN}- sequence prefix."""
    names = {}
    for f in folders:
        n = os.path.basename(f.rstrip("/"))
        bare = n.split("-", 1)[1] if n[:2].isdigit() and "-" in n else n
        names[n] = (n, bare)
    hits = collections.defaultdict(lambda: collections.defaultdict(list))
    for path in sorted(glob.glob(os.path.join(TRANSCRIPTS, "*.jsonl"))):
        sess = os.path.basename(path)[:8]
        for ts, model, blob in _assistant_models(path):
            if not blob or not _authored(blob):
                continue
            for n, (full, bare) in names.items():
                if full in blob or bare in blob:
                    hits[n][model].append((ts, sess))
    out = {}
    for n in names:
        rows = []
        for model, lst in hits[n].items():
            lst.sort()
            rows.append((model, lst[0][0], len(lst), lst[0][1]))
        rows.sort(key=lambda r: r[1])
        rows = [(m, ts[:10], n_, s_) for m, ts, n_, s_ in rows]
        out[n] = rows
    return out


def stamp(folder, model, note):
    """Record the model in metadata.json's built_with."""
    if not os.path.isdir(folder):
        return f"SKIP {folder} (no such folder)"
    data, meta = _load_meta(folder)
    if not data:
        return (f"SKIP     {os.path.relpath(folder, REPO)} has no metadata.json, so there is "
                f"nowhere to record {model} - for an archived task the Model column in "
                f"submission-list.md holds it, and `attribute` recovers it from the transcripts")
    verb = "updated" if data.get("built_with") else "added"
    data["built_with"] = model
    session = re.search(r"session\s+([0-9a-f]+)", note or "")
    if session:
        data["build_session"] = session.group(1)
    with open(meta, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return f"{verb:8s} {os.path.relpath(folder, REPO)}/metadata.json: {model}"


def main(argv):
    cmd = argv[0] if argv else "current"
    rest = argv[1:]

    if cmd == "current":
        model = current()
        if not model:
            print("unknown (no CLAUDE_CODE_SESSION_ID transcript)", file=sys.stderr)
            return 1
        print(model)
        return 0

    if cmd == "require":
        want = resolve(rest[0]) if rest else None
        if not want:
            print("require: name the model this job must run under "
                  "(sonnet, fable, opus, or a model id)", file=sys.stderr)
            return 2
        have = current()
        if not have:
            print(f"UNKNOWN  this job must run under {want}, but this session's model "
                  f"could not be read - stop and ask before continuing")
            return 2
        if _norm(want) == _norm(have):
            print(f"OK       running {have}, which is the model this job requires")
            return 0
        print(f"MISMATCH this job must run under {want}, but this session is {have}. "
              f"Stop and ask to switch with /model {rest[0]}, then start again")
        return 1

    if cmd == "resolve":
        model = resolve(rest[0] if rest else None)
        if not model:
            print("resolve: pass 0 (fable), 1 (opus), or a model id", file=sys.stderr)
            return 2
        print(model)
        return 0

    if cmd == "uid":
        folder = uid_folder(rest[0]) if rest else None
        if not folder:
            print("uid: no task folder for that UID in submission-list.md", file=sys.stderr)
            return 1
        print(os.path.relpath(folder, REPO))
        return 0

    if cmd == "read":
        model = read(os.path.join(REPO, rest[0])) if rest else None
        if not model:
            print("read: no model recorded for that folder", file=sys.stderr)
            return 1
        print(model)
        return 0

    if cmd == "check":
        if not rest:
            print("check: name a task folder", file=sys.stderr)
            return 2
        folder = os.path.join(REPO, rest[0])
        want, have = read(folder), current()
        if not want:
            print(f"MISSING  {rest[0]} records no built_with - run: "
                  f"tools/build_model.py stamp {rest[0]} --infer")
            return 2
        if not have:
            print(f"UNKNOWN  recorded {want}, but this session's model could not be read")
            return 2
        if _norm(want) == _norm(have):
            print(f"OK       {rest[0]} was built with {want}, and that is the model running now")
            return 0
        print(f"MISMATCH {rest[0]} was built with {want}, but this session is {have} - "
              f"switch with /model {want} and re-run")
        return 1

    if cmd == "attribute":
        folders = [os.path.join(REPO, f) for f in rest] if rest else _known_tasks()
        for name, rows in sorted(attribute(folders).items()):
            if not rows:
                print(f"{name:38s} NO TRANSCRIPT HIT")
                continue
            built = rows[0]
            later = "  |  ".join(f"{m} from {d}" for m, d, _, _ in rows[1:])
            print(f"{name:38s} built {built[0]} {built[1]} "
                  f"({built[2]} calls, sess {built[3]})"
                  + (f"   later: {later}" if later else ""))
        return 0

    if cmd == "stamp":
        infer = "--infer" in rest
        rest = [a for a in rest if a != "--infer"]
        model = None
        if "--model" in rest:
            i = rest.index("--model")
            model = rest[i + 1]
            rest = rest[:i] + rest[i + 2:]
        folders = _known_tasks() if "--all" in rest else [
            os.path.join(REPO, f) for f in rest if not f.startswith("--")
        ]
        if not folders:
            print("stamp: name a task folder, or pass --all", file=sys.stderr)
            return 2
        table = attribute(folders) if infer else {}
        for folder in folders:
            name = os.path.basename(folder.rstrip("/"))
            if infer:
                rows = table.get(name) or []
                if not rows:
                    print(f"SKIP {name} (no transcript hit)")
                    continue
                m, day, _, sess = rows[0]
                print(stamp(folder, m, f" (session {sess}, {day}; recovered from the "
                                       f"session transcript, local bookkeeping only)"))
            else:
                m = model or current()
                if not m:
                    print("stamp: no --model and no session transcript", file=sys.stderr)
                    return 1
                sid = (os.environ.get("CLAUDE_CODE_SESSION_ID") or "")[:8]
                print(stamp(folder, m, f" (session {sid}; local bookkeeping only, "
                                       f"not part of the platform form)"))
        return 0

    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
