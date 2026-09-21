"""verify_golden.py for <task-name>: re-derive every figure the golden states from inputs/ alone.

Copy into the task folder root (never into inputs/ or solution/, so it stays out of both zips),
replace derive() and the expectations with this task's method, and run it:

    .venv/bin/python <task-folder>/verify_golden.py      # the gate (G43) runs it the same way

Rules for the method: read only inputs/, never the golden; apply every convention exactly as
the golden's method text states it (rounding at each step, band boundaries, tolerances); and
list in VARIANTS every other reading a reviewer could reasonably take, with the phrase the
golden uses to settle it, so G43 can check that the golden says so.
"""
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = os.environ.get("HAZY_ROOT") or next(str(p) for p in HERE.parents if (p / "tools" / "golden_verify.py").is_file())
sys.path.insert(0, os.path.join(ROOT, "tools"))
from golden_verify import Report  # noqa: E402

INPUTS = HERE / "inputs"


def derive(**variant):
    """Rate every record from INPUTS under the stated conventions, overridden by `variant`.
    Return (figures, standings): figures maps a golden label to its derived value, standings
    maps each record key to its outcome (for example over / under / correct)."""
    raise NotImplementedError("replace with this task's method")


# Each variant: name -> (keyword overrides for derive, the phrase the golden states to settle it)
VARIANTS = {
    # "banker's rounding": ({"rounding": "half_even"}, "rounded half up to the cent at each step"),
}

# Each figure the golden states: label -> the text the golden prints
EXPECTED = {
    # "rated total": "43,027.40",
}

if __name__ == "__main__":
    rep = Report()
    figures, _ = derive()
    for label, golden in EXPECTED.items():
        rep.expect(label, figures.get(label), golden)
    rep.sensitivity(lambda **kw: derive(**kw)[1], VARIANTS)
    rep.finish()
