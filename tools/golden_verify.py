"""Report builder for a task's verify_golden.py (gate check G43).

A task folder's verify_golden.py re-derives the golden's figures from the inputs alone, then
calls into this module so the gate can read the result:

    import os, sys
    from pathlib import Path
    root = os.environ.get("HAZY_ROOT") or next(str(p) for p in Path(__file__).resolve().parents
                                                   if (p / "tools" / "golden_verify.py").is_file())
    sys.path.insert(0, os.path.join(root, "tools"))
    from golden_verify import Report, golden_text

    rep = Report()
    rep.expect("rated total", derived_total, "43,027.40")          # every figure the golden states
    rep.sensitivity(rate_all, {                                     # every reading a reviewer might take
        "banker's rounding": ({"mode": "half_even"}, "rounded half up to the cent"),
        "boundary takes the lower row": ({"boundary": "ends"}, "takes the row that begins at that price"),
    })
    rep.finish()

`rate_all(**variant)` returns {key: standing}; every key whose standing differs from the
baseline run becomes a near flip carrying the convention phrase, and G43 fails any near flip
whose phrase the golden does not state. The last stdout line is the JSON report, and the exit
code is 1 when a figure is not reproduced or nothing was checked.
"""
import json
import re
import sys
import zipfile
from pathlib import Path


def _fmt(value):
    return str(value).replace(",", "").strip()


class Report:
    def __init__(self):
        self.checked = 0
        self.mismatches = []
        self.near_flips = []

    def expect(self, key, derived, golden):
        """Compare one derived figure with the figure the golden states (commas ignored)."""
        self.checked += 1
        if _fmt(derived) != _fmt(golden):
            self.mismatches.append({"key": str(key), "got": str(derived), "want": str(golden)})

    def sensitivity(self, run, variants):
        """run(**kwargs) -> {key: standing}; variants maps a name to (kwargs, convention phrase)."""
        base = run()
        for name, (kwargs, convention) in variants.items():
            alt = run(**kwargs)
            for key, standing in base.items():
                if alt.get(key) != standing:
                    self.near_flips.append({"key": str(key), "variant": name, "baseline": str(standing),
                                            "alternate": str(alt.get(key)), "convention": convention})
        return base

    def finish(self):
        print(json.dumps({"checked": self.checked, "mismatches": self.mismatches, "near_flips": self.near_flips}))
        sys.exit(1 if self.mismatches or not self.checked else 0)


def golden_text(folder="."):
    """Paragraph, table and header/footer text of every solution docx, plus xlsx shared strings."""
    out = []
    for path in sorted((Path(folder) / "solution").glob("*")):
        if path.suffix.lower() not in (".docx", ".xlsx"):
            continue
        with zipfile.ZipFile(path) as z:
            for name in z.namelist():
                if re.match(r"(word/(document|header\d*|footer\d*)\.xml|xl/sharedStrings\.xml)$", name):
                    xml = z.read(name).decode("utf-8", "ignore")
                    out.append(re.sub(r"<[^>]+>", "", re.sub(r"</w:p>|</si>", "\n", xml)))
    return "\n".join(out)
