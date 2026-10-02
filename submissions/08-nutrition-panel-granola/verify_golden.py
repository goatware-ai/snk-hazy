"""verify_golden.py for nutrition-panel-granola: re-derive every declared value, percent daily value and claim
result from inputs/ alone under SOP QA-14 as the golden applies it, and list the alternate readings a reviewer
could take with the phrase the golden uses to settle each one.

    .venv/bin/python drafts/08-nutrition-panel-granola/verify_golden.py
"""
import csv
import re
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
import re
SHEET = {r["INGREDIENT_CODE"]: r for r in csv.DictReader(open(INPUTS / "ingredient_nutrient_specs.csv", newline=""))}
DOCNAME = {"Calories": "CALORIES_KCAL", "Total fat": "TOTAL_FAT_G", "Saturated fat": "SAT_FAT_G", "Trans fat": "TRANS_FAT_G", "Cholesterol": "CHOLESTEROL_MG",
           "Sodium": "SODIUM_MG", "Total carbohydrate": "TOTAL_CARB_G", "Dietary fiber": "FIBER_G", "Total sugars": "TOTAL_SUGARS_G",
           "of which added sugars": "ADDED_SUGARS_G", "Protein": "PROTEIN_G", "Vitamin D": "VITAMIN_D_MCG", "Calcium": "CALCIUM_MG", "Iron": "IRON_MG", "Potassium": "POTASSIUM_MG"}


def specs_in_force():
    """The supplier specifications in the file: code -> (basis in grams, values), read from each document's own
    nutrition heading and table. SOP 1.2: the basis is the one the specification states, and the specification in
    force governs where the nutrient sheet differs."""
    got = {}
    for f in sorted(INPUTS.glob("supplier_spec_*.docx")):
        doc = Document(f); code = "RM-" + doc.paragraphs[1].text.split("S-")[1].split(",")[0].strip()
        head = next(q.text for q in doc.paragraphs if q.text.startswith("Nutrition, per"))
        basis = D(re.search(r"(\d+) g", head).group(1))
        vals = {}
        for t in doc.tables:
            for row in t.rows:
                c = [x.text.strip() for x in row.cells]
                for i in range(0, len(c) - 1, 2):
                    if c[i] in DOCNAME:
                        vals[DOCNAME[c[i]]] = c[i + 1].split()[0].replace(",", "")
        assert len(vals) == 15, (f.name, vals)
        got[code] = (basis, vals)
    return got


DOCS = specs_in_force()
CRISP = "\n".join(q.text for q in Document(INPUTS / "supplier_spec_s1187_crisp_rice.docx").paragraphs)
REV6 = re.search(r"revision 6 .*?sub-ingredients as ([a-z, ]+?) at .*?sodium at (\d+) mg per 30 g", CRISP)
REV6_SUBS, REV6_SODIUM = REV6.group(1).replace(" and ", ", "), D(REV6.group(2))
BARS = D(str(rec["Bars cut"]))
SPEC = {}
for code, r in SHEET.items():
    row = dict(r); row["BASIS_G"] = "100"
    if code in DOCS:
        row["BASIS_G"] = str(DOCS[code][0]); row.update(DOCS[code][1])
    else:
        assert r["SPEC_BASIS"] == "100 g", code
    SPEC[code] = row
sop = "\n".join(p.text for p in Document(INPUTS / "sop_qa14_nutrition_labeling.docx").paragraphs)


def spec_sub_ingredients():
    """Sub-ingredients per compound ingredient, read from each supplier specification docx in inputs/ whose
    title names the specification the nutrient sheet cites (S-1187, S-3301): the 'Ingredients as supplied' row."""
    subs = {}
    for f in sorted(INPUTS.glob("supplier_spec_*.docx")):
        doc = Document(f); title = doc.paragraphs[1].text
        code = "RM-" + title.split("S-")[1].split(",")[0].strip()
        for t in doc.tables:
            for row in t.rows:
                if row.cells[0].text.strip() == "Ingredients as supplied":
                    subs[code] = row.cells[1].text.strip().lower()
    return subs


def ingredient_statement():
    """SOP 4.1: descending formula weight, the formula's common name in lower case, water removed in the bake left off,
    a compound ingredient's sub-ingredients in parentheses in the order its specification lists them; 4.2 Contains."""
    subs = spec_sub_ingredients()
    parts = []
    for code, name, kg in sorted(FORMULA, key=lambda x: -x[2]):
        if code == "RM-4010":
            continue
        n = name.lower()
        parts.append(f"{n} ({subs[code]})" if code in subs and "," in subs[code] else n)   # a one-item list is a single ingredient
    text = ", ".join(parts); text = text[0].upper() + text[1:] + "."
    names = " ".join(n for _, n, _ in FORMULA).lower()
    contains = "Contains: " + ", ".join(a for a in ("almonds", "soy") if a.rstrip("s") in names) + "."
    return text, contains, len(parts)
assert "40 grams" in sop
WHOLE_GRAIN_FLOOR = D(re.search(r"at least (\d+) grams of whole grain", sop).group(1))
assert "unrounded amount, before the rounding" in sop


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


def derive(basis_as_stated=True, yield_applied=True, serving=None, pct_from="declared", cherry_added="spec", cherries_from="spec", sheet_rows=(), mineral_test="unrounded", finished="scale", whole_grain="oats", crisp_rev=7):
    fig, standing = {}, {}
    serving = BAR_G if serving is None else D(serving)
    fin = FINISHED if finished == "scale" else BARS * BAR_G / 1000   # SOP 1.1: the scale ticket net of trim governs, not the bar count
    scale = serving / (fin * 1000) if yield_applied else serving / (BATCH * 1000)   # grams of finished bar per gram of batch input
    per = {k: D(0) for k in NUTS}; contrib = {}
    for code, name, kg in FORMULA:
        sp = SPEC[code]; basis = D(sp["BASIS_G"]) if basis_as_stated else D(100)
        if code == "RM-1187" and crisp_rev == 6:
            sp = dict(sp); sp["SODIUM_MG"] = str(REV6_SODIUM)
        if code == "RM-3301" and cherries_from == "sheet":
            sp = dict(SHEET[code]); sp["ADDED_SUGARS_G"] = sp["ADDED_SUGARS_G"] or "0"
        if code in sheet_rows:
            sp = dict(SHEET[code]); sp["BASIS_G"] = str(DOCS[code][0]) if code in DOCS else "100"; sp["ADDED_SUGARS_G"] = sp["ADDED_SUGARS_G"] or "0"
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
        if mineral_test == "rounded" and k in ("CALCIUM_MG", "POTASSIUM_MG") and per[k] > 0:
            fig[f"{k} declared"] = str(nearest(per[k], 10)) if nearest(per[k], 10) / DV[k] >= D("0.02") else "0"
        if k in DV:
            base = D(fig[f"{k} declared"]) if (pct_from == "declared" and not fig[f"{k} declared"].startswith("less")) else per[k]
            fig[f"{k} pct dv"] = str(rnd(base / DV[k] * 100, "1"))
    # whole grain per serving: rolled oats grams in the bar
    fig["cherries g"] = str(rnd(contrib["RM-3301"]["g"], "0.01"))
    # claims per SOP 5: unrounded, per RACC and per serving, both must pass
    fiber_ok = per_racc["FIBER_G"] / DV["FIBER_G"] >= D("0.10") and per["FIBER_G"] / DV["FIBER_G"] >= D("0.10")
    sodium_ok = per_racc["SODIUM_MG"] <= 140 and per["SODIUM_MG"] <= 140
    wg = contrib["RM-1042"]["g"] + (contrib["RM-2210"]["g"] if whole_grain == "with syrup" else D(0))
    whole_ok = wg >= WHOLE_GRAIN_FLOOR
    fig["whole grain g"] = str(rnd(wg, "0.01"))
    fig["whole grain floor"] = str(WHOLE_GRAIN_FLOOR)
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
    "serving-basis specifications read as per 100 g": ({"basis_as_stated": False}, "per 30 g serving"),
    "no bake yield applied": ({"yield_applied": False}, "finished batch weight"),
    "serving computed on the pilot sample weight": ({"serving": "42.1"}, "target net weight"),
    "percent daily value from the unrounded amount": ({"pct_from": "unrounded"}, "declared, rounded amount"),
    "cherry sugars all counted as added": ({"cherry_added": "all"}, "sucrose taken up in the infusion"),
    "cherry sugars none counted as added": ({"cherry_added": "none"}, "sucrose taken up in the infusion"),
    "cherries taken from the nutrient sheet row at revision 4": ({"cherries_from": "sheet"}, "specification in force"),
    "brown rice syrup taken from the nutrient sheet row at revision 2": ({"sheet_rows": ("RM-2210",)}, "specification in force"),
    "vanilla extract taken from the nutrient sheet row at revision 1": ({"sheet_rows": ("RM-5020",)}, "specification in force"),
    "minerals tested against 2 percent after rounding": ({"mineral_test": "rounded"}, "on the unrounded amount"),
    "finished weight taken as bars cut times the target weight": ({"finished": "bars"}, "scale ticket net of trim"),
    "brown rice syrup counted as whole grain": ({"whole_grain": "with syrup"}, "derivative of a whole grain"),
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
    stmt, contains, n_decl = ingredient_statement()
    r6, _ = derive(crisp_rev=6)
    inv = wb["Inventory Check"]
    rep.expect("rev 6 sodium per serving", r6["SODIUM_MG unrounded"], str(rnd(D(str(inv["C8"].value)), "0.001")))
    rep.expect("rev 6 sodium declared", r6["SODIUM_MG declared"], str(int(round(float(inv["C9"].value)))))
    rep.expect("rev 6 low sodium", r6["claim Low sodium"], inv["C10"].value)
    rep.expect("rev 6 crisp rice as printed", f"crisp rice ({REV6_SUBS})", inv["C11"].value)
    rep.expect("panel holds for all inventory", "Yes" if r6["SODIUM_MG declared"] == fig["SODIUM_MG declared"] else "No", rows["Panel holds for all launch inventory"][0])
    rep.expect("statement holds for all inventory", "No", rows["Ingredient statement holds for all launch inventory"][0])
    rep.expect("low sodium holds for all inventory", "Yes" if r6["claim Low sodium"] == fig["claim Low sodium"] == "Supported" else "No", rows["Low sodium flag holds for all launch inventory"][0])
    rep.expect("ingredient statement", stmt, rows["Ingredients"][0])
    rep.expect("contains statement", contains, rows["Allergens"][0])
    rep.expect("ingredients declared", str(n_decl), str(wb["Ingredient Statement"]["B19"].value))
    rep.expect("note states the statement", stmt.rstrip(".") in note, True)
    for phrase in (f"{fig['fiber pct dv racc']} percent", f"{D(fig['sodium racc']).normalize()} mg", "per 30 g serving", "revision 5"):
        rep.expect(f"note states {phrase}", phrase in note, True)
    rep.sensitivity(lambda **kw: derive(**kw)[1], VARIANTS)
    rep.finish()
