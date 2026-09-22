"""verify_golden.py for carton-bid-evaluation: re-derive every figure the evaluation states from inputs/ alone
under ITB 2026-17 as amended and policy PP-3 as the golden applies them, and list the alternate readings a
reviewer could take with the phrase the golden uses to settle each one.

    .venv/bin/python drafts/10-carton-bid-evaluation/verify_golden.py
"""
import os
import re
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
GOLDEN = HERE / "solution" / "bid_evaluation_itb_2026_17.xlsx"


def r2(x):
    return D(x).quantize(D("0.01"), rounding=ROUND_HALF_UP)


def money(x):
    return f"{D(x):,.2f}"


# ---------------------------------------------------------------- inputs
tw = openpyxl.load_workbook(INPUTS / "bid_tabulation_itb_2026_17.xlsx", data_only=True)
ws = tw["Bids"]
BIDDERS = []
for c in range(3, 11, 2):
    BIDDERS.append(ws.cell(row=4, column=c).value.replace("_UNIT", ""))
PRICES = {b: [D(str(ws.cell(row=r, column=3 + 2 * i).value)) for r in range(5, 10)] for i, b in enumerate(BIDDERS)}
WRITTEN = {b: [D(str(ws.cell(row=r, column=4 + 2 * i).value)) for r in range(5, 10)] for i, b in enumerate(BIDDERS)}
TOOLING = {b: D(str(ws.cell(row=10, column=4 + 2 * i).value)) for i, b in enumerate(BIDDERS)}
ws = tw["Bidder Terms"]
TERMS = {}
for r in range(4, 8):
    name = ws.cell(row=r, column=1).value; key = name.split()[0].upper()
    TERMS[key] = dict(name=name, state=ws.cell(row=r, column=3).value, fob=ws.cell(row=r, column=4).value, pay=ws.cell(row=r, column=5).value, bond=ws.cell(row=r, column=6).value,
                      addenda=ws.cell(row=r, column=7).value, samples=ws.cell(row=r, column=8).value, hold=ws.cell(row=r, column=9).value, exc=ws.cell(row=r, column=10).value)
ws = tw["Freight Schedule"]
FREIGHT = {ws.cell(row=r, column=1).value: D(str(ws.cell(row=r, column=2).value)) for r in range(4, 11)}
ws = tw["Item Weights"]
LB = [D(str(ws.cell(row=r, column=2).value)) for r in range(4, 9)]
itb = "\n".join(p.text for p in Document(INPUTS / "itb_2026_17_cartons.docx").paragraphs)
add = "\n".join(p.text for p in Document(INPUTS / "itb_2026_17_addendum_2.docx").paragraphs)
pol = "\n".join(p.text for p in Document(INPUTS / "purchasing_policy_pp3_excerpt.docx").paragraphs)
QTY = [60000, 84000, 48000, 12000, 30000]
QTY[2] = int(re.search(r"reduced from 48,000 to ([\d,]+)", add).group(1).replace(",", ""))
DISC_MIN_DAYS = 20; APPROVAL = 100000
assert "twenty days" in itb and "one hundred thousand" in pol


def parse_terms(t):
    m = re.match(r"(\d+)% (\d+)", t)
    return (D(m.group(1)) / 100, int(m.group(2))) if m else (D(0), 0)


def derive(unit_governs=True, discount_min_days=DISC_MIN_DAYS, freight_on="origin", exceptions_material=True, addendum_material=True):
    fig, standing = {}, {}
    ev = {}
    for b in BIDDERS:
        t = TERMS[b]
        ext = [r2(PRICES[b][i] * QTY[i]) if unit_governs else WRITTEN[b][i] for i in range(5)]
        sub = sum(ext)
        lb_total = sum(LB[i] * QTY[i] for i in range(5))
        freight = r2(lb_total / 100 * FREIGHT[t["state"]]) if (t["fob"].startswith("Origin") and freight_on == "origin") else D(0)
        rate, days = parse_terms(t["pay"])
        credit = r2(sub * rate) if days >= discount_min_days else D(0)
        total = sub + TOOLING[b] + freight - credit
        reasons = []
        if t["bond"] != "Yes": reasons.append("no bid bond")
        if "2" not in t["addenda"] and addendum_material: reasons.append("addendum 2 not acknowledged; bid on the superseded item 3 quantity and item 5 grade")
        if t["samples"] != "Yes": reasons.append("samples not received")
        if "Exception" in t["exc"] and exceptions_material: reasons.append("exception to the twelve month price hold, a material term")
        responsive = not reasons
        ev[b] = dict(ext=ext, sub=sub, freight=freight, credit=credit, total=total, responsive=responsive, reason="; ".join(reasons), written=sum(WRITTEN[b]) + TOOLING[b])
        fig[f"{b} subtotal"] = money(sub); fig[f"{b} freight"] = money(freight); fig[f"{b} credit"] = money(credit); fig[f"{b} total"] = money(total)
        fig[f"{b} responsive"] = "Responsive" if responsive else "Non-responsive"; fig[f"{b} written total"] = money(ev[b]["written"])
        standing[f"{b} responsive"] = fig[f"{b} responsive"]
    resp = sorted([b for b in BIDDERS if ev[b]["responsive"]], key=lambda b: ev[b]["total"])
    fig["award"] = TERMS[resp[0]]["name"]; fig["award total"] = money(ev[resp[0]]["total"]); fig["runner up"] = TERMS[resp[1]]["name"] if len(resp) > 1 else "None"
    fig["margin"] = money(ev[resp[1]]["total"] - ev[resp[0]]["total"]) if len(resp) > 1 else "None"
    fig["approver"] = "Vice president of operations" if ev[resp[0]]["total"] > APPROVAL else "Director of supply chain"
    low_written = min(BIDDERS, key=lambda b: ev[b]["written"]); fig["lowest as written"] = TERMS[low_written]["name"]
    fig["responsive count"] = len(resp); fig["freight lb"] = str(sum(LB[i] * QTY[i] for i in range(5)))
    # the corrected extension
    for b in BIDDERS:
        for i in range(5):
            if ev[b]["ext"][i] != WRITTEN[b][i]:
                fig[f"corrected {b} item {i + 1}"] = f"{money(WRITTEN[b][i])} to {money(ev[b]['ext'][i])}"
    standing["award"] = fig["award"]; standing["approver"] = fig["approver"]
    return fig, standing


VARIANTS = {
    "bidder's written extensions carried": ({"unit_governs": False}, "unit price governs"),
    "discount credited at any period": ({"discount_min_days": 0}, "twenty days or longer"),
    "freight not added for FOB origin": ({"freight_on": "none"}, "FOB origin"),
    "price hold exception waived": ({"exceptions_material": False}, "material term"),
    "unacknowledged addendum waived": ({"addendum_material": False}, "non-responsive"),
}

if __name__ == "__main__":
    fig, standing = derive()
    if "--print" in sys.argv:
        for k, v in fig.items(): print(k, v)
        sys.exit(0)
    wb = openpyxl.load_workbook(GOLDEN, data_only=True)
    rep = Report()
    s = wb["Recommendation"]
    rows = {s.cell(row=r, column=1).value: [s.cell(row=r, column=c).value for c in range(2, 6)] for r in range(1, 40) if s.cell(row=r, column=1).value}
    hdr = rows["Bidder"]
    for j, name in enumerate(hdr):
        key = name.split()[0].upper()
        rep.expect(f"{key} responsive", fig[f"{key} responsive"], rows["Responsiveness"][j])
        rep.expect(f"{key} written total", fig[f"{key} written total"], money(rows["Total bid as written"][j]))
        if fig[f"{key} responsive"] == "Responsive":
            rep.expect(f"{key} subtotal", fig[f"{key} subtotal"], money(rows["Corrected extensions"][j]))
            rep.expect(f"{key} freight", fig[f"{key} freight"], money(rows["Freight added, FOB origin"][j]))
            rep.expect(f"{key} credit", fig[f"{key} credit"], money(rows["Payment discount credit"][j]))
            rep.expect(f"{key} total", fig[f"{key} total"], money(rows["Total evaluated price"][j]))
    rep.expect("award", fig["award"], rows["Recommended award"][0])
    rep.expect("award total", fig["award total"], money(rows["Recommended award, total evaluated price"][0]))
    rep.expect("margin", fig["margin"], money(rows["Margin over the next responsive bid"][0]))
    rep.expect("approver", fig["approver"], rows["Approver required by PP-3.5.3"][0])
    rep.expect("lowest as written", fig["lowest as written"], rows["Lowest bid as written"][0])
    rep.expect("responsive count", fig["responsive count"], rows["Responsive bids"][0])
    note = "\n".join(str(c.value) for row in wb["Note to Torsten"].iter_rows() for c in row if c.value)
    for phrase in (f"${fig['award total']}", f"${fig['margin']}", "45,112.00", "35,112.00", "8,933.70", "1,292.46"):
        rep.expect(f"note states {phrase}", phrase in note, True)
    rep.sensitivity(lambda **kw: derive(**kw)[1], VARIANTS)
    rep.finish()
