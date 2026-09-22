"""verify_golden.py for nutrition-panel-granola: re-derive every declared value, percent daily value and claim
result from inputs/ alone under SOP QA-14 as the golden applies it, and list the alternate readings a reviewer
could take with the phrase the golden uses to settle each one.

    .venv/bin/python drafts/08-nutrition-panel-granola/verify_golden.py
"""
import csv
import os
import sys
from decimal import Decimal as D, ROUND_HALF_UP
from pathlib import Path

import openpyxl
from docx import Document

HERE = Path(__file__).resolve().parent
ROOT = os.environ.get("HAZY_ROOT") or next(str(p) for p in HERE.parents if (p / "tools" / "golden_verify.py").is_file())
sys.path.insert(0, os.path.join(ROOT, "tools"))
from golden_verify import Report  # noqa: E402

INPUTS = HERE / "inputs"
GOLDEN = HERE / "solution" / "oat_cherry_bar_label_review.xlsx"
RACC = D(40)
DV = {"TOTAL_FAT_G": D(78), "SAT_FAT_G": D(20), "CHOLESTEROL_MG": D(300), "SODIUM_MG": D(2300), "TOTAL_CARB_G": D(275), "FIBER_G": D(28), "ADDED_SUGARS_G": D(50),
      "PROTEIN_G": D(50), "VITAMIN_D_MCG": D(20), "CALCIUM_MG": D(1300), "IRON_MG": D(18), "POTASSIUM_MG": D(4700)}
NUTS = ["CALORIES_KCAL", "TOTAL_FAT_G", "SAT_FAT_G", "TRANS_FAT_G", "CHOLESTEROL_MG", "SODIUM_MG", "TOTAL_CARB_G", "FIBER_G", "TOTAL_SUGARS_G", "ADDED_SUGARS_G",
        "PROTEIN_G", "VITAMIN_D_MCG", "CALCIUM_MG", "IRON_MG", "POTASSIUM_MG"]

# ---------------------------------------------------------------- inputs
fw = openpyxl.load_workbook(INPUTS / "formula_ocb_26_03.xlsx", data_only=True)
ws = fw["Formula"]
FORMULA = [(ws.cell(row=r, column=1).value, ws.cell(row=r, column=2).value, D(str(ws.cell(row=r, column=3).value))) for r in range(5, 18)]
BATCH = sum(kg for _, _, kg in FORMULA)
pb = fw["Pilot Batch Record"]
rec = {pb.cell(row=r, column=1).value: pb.cell(row=r, column=2).value for r in range(4, 14)}
FINISHED = D(str(rec["Finished batch weight, net of trim (kg)"])); BAR_G = D(str(rec["Target bar net weight (g)"])); BAR_SAMPLE = D(str(rec["Average bar weight, 30-bar sample (g)"]))
SPEC = {r["INGREDIENT_CODE"]: r for r in csv.DictReader(open(INPUTS / "ingredient_nutrient_specs.csv", newline=""))}
sop = "\n".join(p.text for p in Document(INPUTS / "sop_qa14_nutrition_labeling.docx").paragraphs)
assert "40 grams" in sop and "8 grams of whole grain" in sop


def rnd(x, q):
    return D(x).quantize(D(q), rounding=ROUND_HALF_UP)


def nearest(x, step):
    return (D(x) / D(step)).quantize(D(1), rounding=ROUND_HALF_UP) * D(step)


def declare(key, x):
    """SOP QA-14 section 2 rounding; returns the declared string."""
    x = D(x)
    if key == "CALORIES_KCAL":
        return "0" if x < 5 else str(nearest(x, 5)) if x <= 50 else str(nearest(x, 10))
    if key in ("TOTAL_FAT_G", "SAT_FAT_G", "TRANS_FAT_G"):
        return "0" if x < D("0.5") else (str(nearest(x, D("0.5")).normalize()) if x < 5 else str(nearest(x, 1)))
    if key == "CHOLESTEROL_MG":
        return "0" if x < 2 else "less than 5" if x <= 5 else str(nearest(x, 5))
    if key == "SODIUM_MG":
        return "0" if x < 5 else str(nearest(x, 5)) if x <= 140 else str(nearest(x, 10))
    if key in ("TOTAL_CARB_G", "FIBER_G", "TOTAL_SUGARS_G", "ADDED_SUGARS_G", "PROTEIN_G"):
        return "0" if x < D("0.5") else "less than 1" if x < 1 else str(nearest(x, 1))
    if key == "VITAMIN_D_MCG":
        return str(rnd(x, "0.1")) if x / DV[key] >= D("0.02") else "0"
    if key in ("CALCIUM_MG", "POTASSIUM_MG"):
        return str(nearest(x, 10)) if x / DV[key] >= D("0.02") else "0"
    if key == "IRON_MG":
        return str(rnd(x, "0.1")) if x / DV[key] >= D("0.02") else "0"
    raise KeyError(key)


def derive(basis_as_stated=True, yield_applied=True, serving=None, pct_from="declared", cherry_added="spec"):
    fig, standing = {}, {}
    serving = BAR_G if serving is None else D(serving)
    scale = serving / (FINISHED * 1000) if yield_applied else serving / (BATCH * 1000)   # grams of finished bar per gram of batch input
    per = {k: D(0) for k in NUTS}; contrib = {}
    for code, name, kg in FORMULA:
        sp = SPEC[code]; basis = D(sp["BASIS_G"]) if basis_as_stated else D(100)
        g_bar = rnd(kg * 1000 * scale, "0.0001")
        contrib[code] = {}
        for k in NUTS:
            v = D(sp[k])
            if k == "ADDED_SUGARS_G" and code == "RM-3301" and cherry_added == "none": v = D(0)
            if k == "ADDED_SUGARS_G" and code == "RM-3301" and cherry_added == "all": v = D(sp["TOTAL_SUGARS_G"])
            v100 = rnd(v / basis * 100, "0.0001"); c = rnd(g_bar / 100 * v100, "0.0001")
            per[k] += c; contrib[code][k] = c
        contrib[code]["g"] = g_bar
    per = {k: rnd(v, "0.0001") for k, v in per.items()}; per_racc = {k: rnd(v * RACC / serving, "0.0001") for k, v in per.items()}
    fig["yield"] = str(rnd(FINISHED / BATCH, "0.0001")); fig["serving g"] = str(serving); fig["bar count"] = rec["Bars cut"]
    for k in NUTS:
        fig[f"{k} unrounded"] = str(rnd(per[k], "0.001")); fig[f"{k} declared"] = declare(k, per[k])
        if k in DV:
            base = D(fig[f"{k} declared"]) if (pct_from == "declared" and not fig[f"{k} declared"].startswith("less")) else per[k]
            fig[f"{k} pct dv"] = str(rnd(base / DV[k] * 100, "1"))
    # whole grain per serving: rolled oats grams in the bar
    fig["whole grain g"] = str(rnd(contrib["RM-1042"]["g"], "0.01"))
    fig["cherries g"] = str(rnd(contrib["RM-3301"]["g"], "0.01"))
    # claims per SOP 5: unrounded, per RACC and per serving, both must pass
    fiber_ok = per_racc["FIBER_G"] / DV["FIBER_G"] >= D("0.10") and per["FIBER_G"] / DV["FIBER_G"] >= D("0.10")
    sodium_ok = per_racc["SODIUM_MG"] <= 140 and per["SODIUM_MG"] <= 140
    whole_ok = contrib["RM-1042"]["g"] >= 8
    fig["fiber pct dv racc"] = str(rnd(per_racc["FIBER_G"] / DV["FIBER_G"] * 100, "0.1")); fig["fiber pct dv serving"] = str(rnd(per["FIBER_G"] / DV["FIBER_G"] * 100, "0.1"))
    fig["sodium racc"] = str(rnd(per_racc["SODIUM_MG"], "0.1")); fig["sodium serving"] = str(rnd(per["SODIUM_MG"], "0.1"))
    claims = {"Good source of fiber": "Supported" if fiber_ok else "Not supported", "Low sodium": "Supported" if sodium_ok else "Not supported",
              "Made with whole grain oats": "Supported" if whole_ok else "Not supported", "No artificial flavors": "Supported",
              "No added sugar": "Not supported", "Real fruit": "Supported"}
    fig.update({f"claim {k}": v for k, v in claims.items()})
    standing.update({f"claim {k}": v for k, v in claims.items()})
    standing.update({f"{k} declared": fig[f"{k} declared"] for k in NUTS})
    standing.update({f"{k} pct dv": fig[f"{k} pct dv"] for k in NUTS if k in DV})
    return fig, standing


VARIANTS = {
    "crisp rice specification read as per 100 g": ({"basis_as_stated": False}, "per 30 g serving"),
    "no bake yield applied": ({"yield_applied": False}, "finished batch weight"),
    "serving computed on the pilot sample weight": ({"serving": "42.1"}, "target net weight"),
    "percent daily value from the unrounded amount": ({"pct_from": "unrounded"}, "declared, rounded amount"),
    "cherry sugars all counted as added": ({"cherry_added": "all"}, "sucrose taken up in the infusion"),
    "cherry sugars none counted as added": ({"cherry_added": "none"}, "sucrose taken up in the infusion"),
}

if __name__ == "__main__":
    fig, standing = derive()
    if "--print" in sys.argv:
        for k, v in fig.items(): print(k, v)
        sys.exit(0)
    wb = openpyxl.load_workbook(GOLDEN, data_only=True)
    rep = Report()
    panel = wb["Panel"]
    rows = {panel.cell(row=r, column=1).value: (panel.cell(row=r, column=2).value, panel.cell(row=r, column=4).value) for r in range(1, 40) if panel.cell(row=r, column=1).value}
    LABEL = {"CALORIES_KCAL": "Calories", "TOTAL_FAT_G": "Total Fat", "SAT_FAT_G": "Saturated Fat", "TRANS_FAT_G": "Trans Fat", "CHOLESTEROL_MG": "Cholesterol", "SODIUM_MG": "Sodium",
             "TOTAL_CARB_G": "Total Carbohydrate", "FIBER_G": "Dietary Fiber", "TOTAL_SUGARS_G": "Total Sugars", "ADDED_SUGARS_G": "Includes Added Sugars", "PROTEIN_G": "Protein",
             "VITAMIN_D_MCG": "Vitamin D", "CALCIUM_MG": "Calcium", "IRON_MG": "Iron", "POTASSIUM_MG": "Potassium"}
    for k, lab in LABEL.items():
        val, pct = rows[lab]
        rep.expect(f"{lab} declared", str(D(fig[f"{k} declared"]).normalize()) if not fig[f"{k} declared"].startswith("less") else fig[f"{k} declared"], str(D(str(val)).normalize()) if isinstance(val, (int, float)) else val)
        if k in DV:
            rep.expect(f"{lab} pct dv", fig[f"{k} pct dv"], str(rnd(D(str(pct)) * 100, "1")))
    rep.expect("serving", f"1 bar ({fig['serving g']}g)", rows["Serving size"][0])
    comp = wb["Nutrients"]
    hdr = {comp.cell(row=3, column=c).value: c for c in range(1, comp.max_column + 1) if comp.cell(row=3, column=c).value}
    tot = {comp.cell(row=r, column=1).value: r for r in range(4, 22) if comp.cell(row=r, column=1).value}
    for k in NUTS:
        rep.expect(f"{k} unrounded per serving", fig[f"{k} unrounded"], str(rnd(D(str(comp.cell(row=tot["Per serving, unrounded"], column=hdr[k]).value)), "0.001")))
    cl = wb["Claims"]
    claims = {cl.cell(row=r, column=1).value: cl.cell(row=r, column=6).value for r in range(4, 10)}
    for k in ("Good source of fiber", "Low sodium", "Made with whole grain oats", "No artificial flavors", "No added sugar", "Real fruit"):
        rep.expect(f"claim {k}", fig[f"claim {k}"], claims[k])
    note = "\n".join(str(c.value) for row in wb["Note to Priya"].iter_rows() for c in row if c.value)
    for phrase in (f"{fig['fiber pct dv racc']} percent", f"{D(fig['sodium racc']).normalize()} mg", "per 30 g serving", "revision 5"):
        rep.expect(f"note states {phrase}", phrase in note, True)
    rep.sensitivity(lambda **kw: derive(**kw)[1], VARIANTS)
    rep.finish()
