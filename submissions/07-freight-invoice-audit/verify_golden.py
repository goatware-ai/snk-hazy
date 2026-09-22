"""verify_golden.py for freight-invoice-audit: re-derive every figure the audit states from inputs/ alone
under the contract as the golden applies it, and list the alternate readings a reviewer could take with
the phrase the golden uses to settle each one.

    .venv/bin/python drafts/07-freight-invoice-audit/verify_golden.py
"""
import csv
import datetime as dt
import os
import sys
from decimal import Decimal as D, ROUND_HALF_UP
from pathlib import Path

import openpyxl

HERE = Path(__file__).resolve().parent
ROOT = os.environ.get("HAZY_ROOT") or next(str(p) for p in HERE.parents if (p / "tools" / "golden_verify.py").is_file())
sys.path.insert(0, os.path.join(ROOT, "tools"))
from golden_verify import Report  # noqa: E402

INPUTS = HERE / "inputs"
GOLDEN = HERE / "solution" / "northline_audit_sept2026.xlsx"


def r2(x):
    return D(str(x)).quantize(D("0.01"), rounding=ROUND_HALF_UP)


def money(x):
    return f"{D(x):,.2f}"


def pdate(s):
    return dt.datetime.strptime(s, "%m/%d/%Y").date()


# ---------------------------------------------------------------- inputs
tw = openpyxl.load_workbook(INPUTS / "northline_contract_rates_2026.xlsx", data_only=True)
ws = tw["Lane Rates"]
LANES = {ws.cell(row=r, column=1).value: [D(str(ws.cell(row=r, column=c).value)) for c in range(2, 7)] for r in range(5, 12)}
BREAK_MIN = [int(ws.cell(row=14, column=c).value) for c in range(2, 7)]
ws = tw["Class Factors"]
CLASS_FACTOR = {D(str(ws.cell(row=r, column=1).value)): D(str(ws.cell(row=r, column=2).value)) for r in range(4, 11)}
GROUP_CLASS = {ws.cell(row=r, column=1).value: D(str(ws.cell(row=r, column=2).value)) for r in range(15, 21)}
ws = tw["Accessorials"]
ACC = {ws.cell(row=r, column=2).value: D(str(ws.cell(row=r, column=3).value)) for r in range(4, 8)}
DISCOUNT = D(str(ws["C13"].value)); MIN_CHARGE = D(str(ws["C14"].value))
ws = tw["Fuel Surcharge"]
BANDS = [(D(str(ws.cell(row=r, column=1).value)), D(str(ws.cell(row=r, column=3).value))) for r in range(4, 22)]
from docx import Document  # noqa: E402
bul = Document(INPUTS / "northline_fuel_bulletin_sept_2026.docx")
DOE = {}
for t in bul.tables:
    for row in t.rows[1:]:
        DOE[dt.datetime.strptime(row.cells[0].text, "%B %d, %Y").date()] = D(row.cells[1].text)
BOLS = {b["PRO_NO"]: b for b in csv.DictReader(open(INPUTS / "bills_of_lading_sept_2026.csv", newline=""))}
INV = list(csv.DictReader(open(INPUTS / "northline_invoices_sept_2026.csv", newline="")))


def fsc_pct(price):
    pct = BANDS[0][1]
    for lo, p in BANDS:
        if price >= lo: pct = p
    return pct


def monday(d):
    return d - dt.timedelta(days=d.weekday())


def derive(deficit=True, fsc_on="pickup", reweigh_holds=False, net_undercharges=False):
    fig, standing = {}, {}
    seen = set(); rows = []
    for inv in INV:
        pro = inv["PRO_NO"]; b = BOLS[pro]; pickup = pdate(b["PICKUP_DATE"])
        dup = pro in seen; seen.add(pro)
        bol_w = int(b["WEIGHT_LB"]); billed_w = int(inv["BILLED_WEIGHT"])
        w = billed_w if (reweigh_holds and billed_w > bol_w) else bol_w
        cls = GROUP_CLASS[b["PRODUCT_GROUP"]]; f = CLASS_FACTOR[cls]
        i = max(k for k, m in enumerate(BREAK_MIN) if w >= m); rates = LANES[b["DEST_STATE"]]
        own = r2(D(w) / 100 * rates[i] * f)
        gross = own
        if deficit and i < 4:
            gross = min(own, r2(D(BREAK_MIN[i + 1]) / 100 * rates[i + 1] * f))
        net = max(r2(gross * (1 - DISCOUNT)), MIN_CHARGE)
        fdate = pickup if fsc_on == "pickup" else pdate(inv["INVOICE_DATE"])
        pct = fsc_pct(DOE.get(monday(fdate), DOE[max(DOE)])); fsc = r2(net * pct)
        acc = sum((ACC[k] for k in ACC if b[k] == "Y"), D(0))
        expected = D(0) if dup else net + fsc + acc
        billed = D(inv["INVOICE_TOTAL"]); var = billed - expected
        if dup: code = "7.1 duplicate bill"
        elif D(inv["BILLED_CLASS"]) != cls: code = "4.3 class"
        elif billed_w != bol_w: code = "4.5 reweigh"
        elif D(inv["BASE_CHARGE"]) != gross: code = "4.2 deficit weight"
        elif D(inv["FSC_PCT"]) / 100 != pct: code = "5.2 fuel week"
        elif D(inv["ACCESSORIAL_AMT"]) > acc: code = "6.1 accessorial not requested"
        elif D(inv["ACCESSORIAL_AMT"]) < acc: code = "6.1 accessorial omitted"
        else: code = ""
        rows.append(dict(inv=inv["INVOICE_NO"], pro=pro, expected=expected, billed=billed, var=var, code=code, net=net, fsc=fsc, acc=acc, pct=pct, gross=gross))
        standing[inv["INVOICE_NO"]] = "over" if var > 0 else "under" if var < 0 else "correct"
    over = [r for r in rows if r["var"] > 0]; under = [r for r in rows if r["var"] < 0]
    fig["invoices"] = len(rows); fig["billed total"] = money(sum(r["billed"] for r in rows)); fig["contract total"] = money(sum(r["expected"] for r in rows))
    fig["overbilled"] = money(sum(r["var"] for r in over)); fig["underbilled"] = money(-sum(r["var"] for r in under))
    fig["claim total"] = money(sum(r["var"] for r in over) - (sum(-r["var"] for r in under) if net_undercharges else 0))
    fig["claims"] = len(over); fig["undercharges"] = len(under); fig["exceptions"] = sum(1 for r in rows if r["code"]); fig["clean"] = sum(1 for r in rows if not r["code"])
    for c in ("7.1", "4.3", "4.5", "4.2", "5.2", "6.1"):
        fig[f"code {c}"] = sum(1 for r in rows if r["code"].startswith(c))
    fig["net difference"] = money(sum(r["var"] for r in rows))
    fig["rows"] = rows
    standing["claim total"] = fig["claim total"]
    return fig, standing


VARIANTS = {
    "deficit weight rule not applied": ({"deficit": False}, "lesser of"),
    "fuel surcharge on the invoice-date week": ({"fsc_on": "invoice"}, "pickup date"),
    "carrier reweigh held without a scale ticket": ({"reweigh_holds": True}, "bill of lading weight"),
    "undercharges netted against the claim": ({"net_undercharges": True}, "not netted"),
}

if __name__ == "__main__":
    fig, standing = derive()
    if "--print" in sys.argv:
        for k, v in fig.items():
            if k != "rows": print(k, v)
        for r in fig["rows"]:
            if r["code"] or r["var"]: print(r["inv"], r["pro"], r["code"], money(r["billed"]), money(r["expected"]), money(r["var"]))
        sys.exit(0)
    wb = openpyxl.load_workbook(GOLDEN, data_only=True)
    s = wb["Summary"]
    rep = Report()
    summary = {s.cell(row=r, column=1).value: s.cell(row=r, column=2).value for r in range(1, 40) if s.cell(row=r, column=1).value}
    rep.expect("invoices", fig["invoices"], summary["Freight bills in the file"])
    rep.expect("billed total", fig["billed total"], money(summary["Total billed by Northline"]))
    rep.expect("contract total", fig["contract total"], money(summary["Total due under the contract"]))
    rep.expect("overbilled", fig["overbilled"], money(summary["Overcharges claimed"]))
    rep.expect("underbilled", fig["underbilled"], money(summary["Undercharges reported, not netted"]))
    rep.expect("claims", fig["claims"], summary["Freight bills claimed"])
    rep.expect("undercharges", fig["undercharges"], summary["Freight bills underbilled"])
    rep.expect("exceptions", fig["exceptions"], summary["Freight bills with an exception"])
    rep.expect("clean", fig["clean"], summary["Freight bills billed as the contract provides"])
    for c, label in (("7.1", "Duplicate freight bills (7.1)"), ("4.3", "Class not the product group class (4.3)"), ("4.5", "Reweigh with no scale ticket (4.5)"),
                     ("4.2", "Deficit weight rule not applied (4.2)"), ("5.2", "Fuel surcharge on the wrong week (5.2)"), ("6.1", "Accessorial not on the bill of lading or omitted (6.1)")):
        rep.expect(f"code {c}", fig[f"code {c}"], summary[label])
    # audit rows: every expected total and code across both panels
    a = wb["Audit"]
    hdr = {a.cell(row=3, column=c).value: c for c in range(1, a.max_column + 1) if a.cell(row=3, column=c).value}
    for k, r in enumerate(fig["rows"]):
        panel = "" if k < 19 else "_2"; row = 4 + (k if k < 19 else k - 19)
        rep.expect(f"{r['inv']} expected", money(r["expected"]), money(a.cell(row=row, column=hdr["CONTRACT_TOTAL" + panel]).value))
        rep.expect(f"{r['inv']} variance", money(r["var"]), money(a.cell(row=row, column=hdr["VARIANCE" + panel]).value))
        rep.expect(f"{r['inv']} code", r["code"], a.cell(row=row, column=hdr["EXCEPTION" + panel]).value or "")
    cl = wb["Claim Schedule"]
    rep.expect("claim schedule total", fig["claim total"], money(cl.cell(row=4 + fig["claims"], column=5).value))
    note = "\n".join(str(c.value) for row in wb["Note to Ingrid"].iter_rows() for c in row if c.value)
    for phrase in (f"${fig['overbilled']}", f"${fig['underbilled']}", f"${fig['billed total']}", f"{fig['claims']} freight bills"):
        rep.expect(f"note states {phrase}", phrase in note, True)
    rep.sensitivity(lambda **kw: derive(**kw)[1], VARIANTS)
    rep.finish()
