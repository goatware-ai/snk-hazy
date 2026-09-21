"""Group 1: prompt recycling against the catalogue (U1 U2), formerly section 1 of
tools/originality_check.py.

Two gates caught by hand on an earlier task (2026-08-21).

    tools/originality_check.py submissions/NN-task-name

Runs on the ONE task folder named on the command line. There is deliberately no
sweep-everything mode: this is a build-time gate for the task being built, not an
audit of the catalogue (user, 2026-08-22). Prior prompts are still read, because
that is what the recycling check compares against, but no verdict is emitted for
any folder other than the one named.

Section 1, PROMPT RECYCLING. One prompt was read by hand as "the same unusual user
story, rewritten with names and nouns changed" as an earlier one, and flagged to the
team. Raw n-gram overlap alone does not catch it (the pair scores under 5%),
because the recycling lives in a handful of load-bearing narrative moves, not in
bulk wording. So this checks BOTH: the top n-gram overlap against every other
prompt in the catalogue, and the count of signature narrative moves reused. That
prompt hit 7 of 7 markers, the only one in the catalogue that did.

The markers are the moves that read as "not a generic professional
convention": the live-formulas user story ("the manager pulls a line in front of
people and the dollars have to follow"), the "up front, ahead of the detail"
presentation instruction, the "ground rules came Monday" memo introduction, the
"our own procedure is X, the N/26 revision" policy introduction, and the "the
rest I pulled <weekday> night" data-extract introduction.

Section 2, INPUT AUTHORSHIP FORENSICS. A hand read found "direct evidence of
batch programmatic construction" in the input packet, and every claim verified:
all five xlsx named Openpyxl in docProps/app.xml and carried one identical zip
timestamp; all four docx shared 15 of 17 byte-identical package components and a
single Word rsidRoot. Input files must be real, or indistinguishable from real
(docs/submission/platform/creating-input-files.md); batch-programmatic provenance is a
rejection without a revision cycle plus offboarding risk.

This gate exists to STOP a packet, not to launder one. If it fires, the files
have to be replaced with real ones. Editing app.xml, spreading the timestamps or
varying the rsids would remove the evidence while leaving the packet exactly as
machine-made as it was, which is misrepresenting authorship to the screen the
programme runs. Do not do it.

Exit code 1 if any ERROR is found.
"""
import glob
import re
from collections import defaultdict
from pathlib import Path

from ..core import check, emit

ROOT = Path(__file__).resolve().parents[3]

SIGNATURES = {
    "live-formulas user story":
        r"keep (?:the math live|it on live formulas|every calculation live)",
    "manager edits in front of people":
        r"in front of (?:people|her|him)\b|moves? numbers around in review"
        r"|changes? a number in front|pulls? a line out",
    "'up front, ahead of the detail'":
        r"up front,? ahead of the detail",
    "'ground rules came <day>'":
        r"ground rules came",
    "'our own procedure is X, the N/26 revision'":
        r"our own (?:rules|procedure)[^.]{0,60}revision",
    "'the rest I pulled <weekday> night'":
        r"the rest (?:of it )?i pulled",
    "'so <name> wants this <day>'":
        r"so \w+ wants (?:this|it|the whole)",
}


def norm(t):
    t = t.lower()
    t = re.sub(r"[a-z_0-9]+\.(?:docx|xlsx|csv|pdf|pptx)", " FILE ", t)
    t = re.sub(r"[^a-z ]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def ngrams(t, n=6):
    w = t.split()
    return {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}


@check(codes=['U1', 'U2'], rules=['PRE-UNIQ'], needs=['prompt', 'folder', 'originality'], params=['folder'])
def check_recycling(folder):
    """The prompt reuses neither the bulk wording nor the signature narrative moves of a prior prompt in the catalogue.

    Since: 2026-08-21 (one prompt read as an earlier one rewritten, flagged to the team).
    Source: task feedback.
    Drift-notes: U1 at 12% 6-gram overlap (6% is a check), U2 at three or more reused signature moves;
    build-time only in the gate (--originality).
    """
    p = folder / "instruction.md"
    if not p.exists():
        return
    mine = norm(p.read_text(encoding="utf-8"))
    g = ngrams(mine)

    others = {}
    for f in sorted(glob.glob(str(ROOT / "submissions/*/instruction.md"))) + \
             sorted(glob.glob(str(ROOT / "archived/*/instruction.md"))):
        name = Path(f).parent.name
        if name == folder.name:
            continue
        others[name] = norm(Path(f).read_text(encoding="utf-8"))

    scored = []
    for name, txt in others.items():
        o = ngrams(txt)
        if not o or not g:
            continue
        scored.append((len(g & o) / max(1, min(len(g), len(o))), len(g & o), name, g & o))
    scored.sort(reverse=True)
    if scored:
        r, n, name, shared = scored[0]
        print(f"        nearest prompt: {name} ({r:.1%}, {n} shared 6-grams)")
        if r >= 0.12:
            emit("ERROR", f"[U1] {r:.1%} 6-gram overlap with {name} — bulk wording reuse; "
                          "rewrite the prompt from the situation, not from a prior prompt")
        elif r >= 0.06:
            emit("ERROR", f"[U1] {r:.1%} 6-gram overlap with {name} — check the shared "
                         "phrases are ordinary trade language, not an authored user story")

    hits = [k for k, pat in SIGNATURES.items() if re.search(pat, mine)]
    reuse = defaultdict(list)
    for k in hits:
        for name, txt in others.items():
            if re.search(SIGNATURES[k], txt):
                reuse[k].append(name)
    recycled = [k for k in hits if reuse[k]]
    print(f"        signature narrative moves: {len(hits)} of {len(SIGNATURES)} present, "
          f"{len(recycled)} of those already used elsewhere")
    for k in recycled:
        print(f"          - {k}: also in {', '.join(sorted(reuse[k])[:6])}")
    if len(recycled) >= 4:
        emit("ERROR", f"[U2] {len(recycled)} signature narrative moves are reused from other "
                      "prompts in the catalogue — this is what a hand read called \"the same "
                      "unusual user story, rewritten with names and nouns changed\" "
                      "(2026-08-21, flagged to the team). These are authored moves, not trade "
                      "convention: say the deadline, the liveness requirement and the summary "
                      "placement in words this scenario would actually use, or leave them out")
    elif len(recycled) == 3:
        emit("ERROR", f"[U2] 3 signature narrative moves reused from other prompts — one more "
                     "and the prompt reads as a rewrite of a prior one")
