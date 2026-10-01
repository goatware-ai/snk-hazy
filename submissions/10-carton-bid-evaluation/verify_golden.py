"""verify_golden.py for carton-bid-evaluation: re-derive every figure the evaluation states from inputs/ alone
under ITB 2026-17 as amended and policy PP-3 as the golden applies them (eleven bids read from the signed forms,
the bidders' letters, the later writings and the telephone message timed from the receipt log, the bid security,
the quality hold register with the clearance notice, the current drawing revisions and the plant that ships each
item), and list the
alternate readings a reviewer could take with the phrase the golden uses to settle each one.

    .venv/bin/python submissions/10-carton-bid-evaluation/verify_golden.py
"""
import os
import re
import sys
from decimal import Decimal as D, ROUND_HALF_UP
from pathlib import Path

import openpyxl
from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph

HERE = Path(__file__).resolve().parent
ROOT = os.environ.get("HAZY_ROOT") or next(str(p) for p in HERE.parents if (p / "tools" / "golden_verify.py").is_file())
sys.path.insert(0, os.path.join(ROOT, "tools"))
from golden_verify import Report  # noqa: E402

INPUTS = HERE / "inputs"
GOLDEN = HERE / "solution" / "bid_evaluation_itb_2026_17.xlsx"
STATE = {"Iowa": "IA", "Nebraska": "NE", "Minnesota": "MN", "Wisconsin": "WI", "Illinois": "IL", "North Dakota": "ND", "South Dakota": "SD"}


def r2(x):
    return D(x).quantize(D("0.01"), rounding=ROUND_HALF_UP)


def money(x):
    return f"{D(x):,.2f}"


def num(text):
    return D(text.replace(",", "").replace("$", "").strip())


def blocks(path):
    doc = Document(path)
    for ch in doc.element.body.iterchildren():
        if ch.tag.endswith("}p"):
            yield "p", Paragraph(ch, doc).text.strip()
        elif ch.tag.endswith("}tbl"):
            yield "t", [[c.text.strip() for c in r.cells] for r in Table(ch, doc).rows]


def key(date, time):
    mm, dd, yy = date.split("/")
    return int(yy + mm + dd + time.replace(":", ""))


# ---------------------------------------------------------------- the rules, read from the documents
itb = "\n".join(t for k, t in blocks(INPUTS / "itb_2026_17_cartons.docx") if k == "p")
add = "\n".join(t for k, t in blocks(INPUTS / "itb_2026_17_addendum_2.docx") if k == "p")
pol = "\n".join(t for k, t in blocks(INPUTS / "purchasing_policy_pp3_excerpt.docx") if k == "p")
QTY = [int(r[2].replace(",", "")) for k, t in blocks(INPUTS / "itb_2026_17_cartons.docx") if k == "t" for r in t[1:]]
QTY_SUPERSEDED_3 = QTY[2]
m = re.search(r"reduced from ([\d,]+) to ([\d,]+)", add)
assert int(m.group(1).replace(",", "")) == QTY_SUPERSEDED_3
QTY[2] = int(m.group(2).replace(",", ""))
SPEC = {2: "18x12x10", 5: "44ect"}          # item 2 as corrected by addendum 1, item 5 as changed by addendum 2
assert "to 18 x 12 x 10" in add and "to 44 ECT C flute" in add
AWARD_NOT_BEFORE = (2026, 10, 6)             # no award precedes the opening, so twelve months from award runs past 10/06/2027
DUE = key("10/06/2026", "10:00")
assert "10:00 on October 6, 2026" in itb
DISC_MIN_DAYS, APPROVAL, BAND, SECURITY = 20, 100000, D(100), D("0.05")
assert "twenty days" in itb and "one hundred thousand" in pol and "within one hundred dollars" in itb
assert "A modification that reaches the purchasing office after the due time is not considered" in itb
assert "A bid that is withdrawn and resubmitted is received when the resubmitted bid reaches" in itb
assert "each item's shipping weight is rated at the rate for the state of the plant that ships it" in itb
assert "a bid with less is treated as a bid without it" in add and "tooling included" in add
assert "conditions its prices on a shorter period or on an index" in itb and "signed by an officer of the bidder" in itb
assert "made to the specification in the drawing set as amended" in add and "releases are placed monthly in pallet multiples" in itb
assert "until quality engineering has cleared the hold" in pol and "passed over" in pol
assert "read from the signed bid form" in pol

# ---------------------------------------------------------------- the bids, from the signed forms
FORMS = {}
cur, part = None, None
for kind, val in blocks(INPUTS / "bid_forms_itb_2026_17.docx"):
    if kind == "p":
        m = re.match(r"Bid form, (.+)", val)
        if m:
            cur = m.group(1)
            FORMS[cur] = dict(name=cur, letter="", tables=[])
            part = "form"
            continue
        if re.match(r"Letter enclosed with the bid, ", val):
            part = "letter"
            continue
        if cur and part == "letter":
            FORMS[cur]["letter"] += val + "\n"
        if cur and part == "form" and val.startswith("Plant of manufacture:"):
            FORMS[cur]["plant"] = val.split(":", 1)[1].strip()
        if cur and part == "form" and val.startswith("Bidder: "):
            FORMS[cur]["address"] = val.split(", ", 1)[1].strip()
            FORMS[cur]["hq_state"] = STATE[re.search(r", ([A-Za-z ]+) \d{5}$", val).group(1)]
    elif cur:
        FORMS[cur]["tables"].append(val)
NAMES = list(FORMS)
assert len(NAMES) == 11 and NAMES == sorted(NAMES)
for f in FORMS.values():
    price, entry = f["tables"]
    f["units"] = [D(price[1 + i][3]) for i in range(5)]
    f["written"] = [num(price[1 + i][4]) for i in range(5)]
    f["qty_bid"] = [int(price[1 + i][2].replace(",", "")) for i in range(5)]
    f["desc"] = [re.sub(r"\s+", "", price[1 + i][1].lower()) for i in range(5)]
    f["signer"] = None
    f["tooling"] = num(price[6][4])
    f["total_written"] = num(price[7][4])
    assert f["total_written"] == sum(f["written"]) + f["tooling"], f["name"]
    e = {r[0]: r[1] for r in entry[1:]}
    f["fob"], f["pay"], f["addenda"] = e["FOB terms"], e["Payment terms"], e["Addenda acknowledged by number"]
    f["security"] = e["Bid bond, five percent of the total bid"]
    f["samples"] = e["Samples, one of each item"]
    f["state"] = re.search(r", ([A-Z]{2})\b", f["plant"]).group(1)

# the tabulation: the office's working copy, the freight schedule and the item weights
tw = openpyxl.load_workbook(INPUTS / "bid_tabulation_itb_2026_17.xlsx", data_only=True)
ws = tw["Bids"]
TAB_UNITS = {}
for i, n in enumerate(NAMES):
    head = ws.cell(row=4, column=3 + 2 * i).value.replace("_UNIT", "")
    assert head.split("_")[0] == n.split()[0].upper(), (head, n)
    TAB_UNITS[n] = [D(str(ws.cell(row=5 + k, column=3 + 2 * i).value)) for k in range(5)]
    assert [D(str(ws.cell(row=5 + k, column=4 + 2 * i).value)) for k in range(5)] == FORMS[n]["written"], n
TAB_DIFF = [(n, k + 1) for n in NAMES for k in range(5) if TAB_UNITS[n][k] != FORMS[n]["units"][k]]
ws = tw["Freight Schedule"]
FREIGHT = {ws.cell(row=r, column=1).value: D(str(ws.cell(row=r, column=2).value)) for r in range(4, 11)}
ws = tw["Item Weights"]
REVS = {}
for r in range(4, 11):
    item, rev, date, lb = (ws.cell(row=r, column=c).value for c in (1, 3, 4, 6))
    REVS.setdefault(item, []).append((key(date, "00:00"), rev, D(str(lb))))
LB_CURRENT = {i: max(v)[2] for i, v in REVS.items()}
LB_FIRST = {i: min(v)[2] for i, v in REVS.items()}
assert max(REVS[5])[1] == "B" and max(REVS[2])[1] == "B" and "revision B replaces revision A" in add

# the receipt log
LOG = []
lw = openpyxl.load_workbook(INPUTS / "bid_receipt_log_itb_2026_17.xlsx", data_only=True)["Receipt Log"]
for r in range(4, lw.max_row + 1):
    v = [lw.cell(row=r, column=c).value for c in range(1, 8)]
    if v[0] and str(v[0]).startswith("R-"):
        LOG.append(dict(no=v[0], key=key(v[1], v[2]), date=v[1], time=v[2], who=v[3], how=v[4], item=v[5], sol=v[6]))


SIGNER, OFFICER = {}, {}
for kind, val in blocks(INPUTS / "bid_forms_itb_2026_17.docx"):
    if kind == "p" and val.startswith("Signed: "):
        person, rest = val[8:].split(",", 1)
        firm = next(n for n in NAMES if n in rest)
        SIGNER[firm] = person.strip().split()[-1].lower()       # the log enters some items under the signer's name
        OFFICER[firm] = bool(re.search(r"president|owner|chief|treasurer|secretary", rest.split(firm)[0], re.I))


def log_rows(name, how=None, item=None):
    first = re.sub(r"[^a-z]", "", name.lower().split()[0])[:5]
    alt = "w&k" if name.startswith("Wenzel") else first
    out = []
    for g in LOG:
        who = g["who"].lower().replace(" ", "")
        if g["sol"] == "ITB 2026-17" and (first in re.sub(r"[^a-z]", "", who) or alt in who or who.endswith(SIGNER[name])):
            if (how is None or g["how"] == how) and (item is None or item in g["item"]):
                out.append(g)
    return out


HANDED_BACK = {m for g in LOG for m in re.findall(r"envelope (R-\d+) handed back", g["item"])}
RECEIPT, FIRST_LOGGED = {}, {}
for n in NAMES:
    env = [g for g in log_rows(n, item="Sealed bid envelope")]
    FIRST_LOGGED[n] = min(env, key=lambda g: g["key"])
    live = [g for g in env if g["no"] not in HANDED_BACK]
    assert len(live) == 1, (n, live)
    RECEIPT[n] = live[0]
    assert live[0]["key"] <= DUE                  # due BY 10:00, section 3.1; only a bid received after that time goes back

# the later writings
CHANGES = {}
cur = None
CLEARED_BY_NOTICE = {}
for kind, val in blocks(INPUTS / "bid_correspondence_itb_2026_17.docx"):
    if kind == "p":
        m = re.match(r"(.+?), (facsimile|letter)", val)
        if m and len(val) < 80:
            cur = next((n for n in NAMES if n == m.group(1)), None)
        m = re.search(r"unit price for item (\d).*from \$([\d.]+) to \$([\d.]+)", val)
        if m and cur:
            CHANGES.setdefault(cur, {})[int(m.group(1))] = (D(m.group(2)), D(m.group(3)))
    else:
        if val[0][0] == "Item" and cur:
            for row in val[1:]:
                CHANGES.setdefault(cur, {})[int(row[0])] = (D(row[1]), D(row[2]))
        if val[0][0] == "Entry":
            e = {r[0]: r[1] for r in val[1:]}
            CLEARED_BY_NOTICE[e["Hold number"]] = e["Cleared"]
LOT_PASSED_UNSIGNED = set()
_hold = None
for kind, val in blocks(INPUTS / "bid_correspondence_itb_2026_17.docx"):
    if kind == "p":
        m = re.match(r"Re: (QH-\d{2}-\d{3})", val)
        if m:
            _hold = m.group(1)
        if _hold and "verification lot" in val and "passed" in val and "has not yet signed" in val:
            LOT_PASSED_UNSIGNED.add(_hold)
assert LOT_PASSED_UNSIGNED == {"QH-26-031"}
CHANGE_RECEIVED = {n: log_rows(n, how="Fax")[0] for n in CHANGES}
# a telephone message is logged but is not a signed writing, section 3.4
TELEPHONE = {}
for n in NAMES:
    for g in log_rows(n, how="Telephone"):
        m = re.search(r"item (\d) to be read at ([\d.]+)", g["item"])
        TELEPHONE[n] = (int(m.group(1)), D(m.group(2)), g)
assert list(TELEPHONE) == ["Dahlgren Paper Box Co."] and TELEPHONE["Dahlgren Paper Box Co."][2]["key"] < DUE
for n, ch in CHANGES.items():
    for it, (old, new) in ch.items():
        assert FORMS[n]["units"][it - 1] == old, (n, it)

# the hold register
hw = openpyxl.load_workbook(INPUTS / "supplier_quality_holds_2026.xlsx", data_only=True)["Holds"]
HOLDS = []
for r in range(4, hw.max_row + 1):
    if hw.cell(row=r, column=1).value and str(hw.cell(row=r, column=1).value).startswith("QH-"):
        HOLDS.append(dict(no=hw.cell(row=r, column=1).value, supplier=hw.cell(row=r, column=2).value, status=hw.cell(row=r, column=6).value, address=hw.cell(row=r, column=10).value or ""))


def open_holds(name, notice=True, lot_pass=False):
    street = FORMS[name]["address"].split(",")[0].strip().lower()
    return [h["no"] for h in HOLDS if h["address"].lower().startswith(street) and h["status"] == "Open"
            and not (notice and h["no"] in CLEARED_BY_NOTICE) and not (lot_pass and h["no"] in LOT_PASSED_UNSIGNED)]


MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]


def conditions(name):
    t = FORMS[name]["letter"].lower()
    short_date = False
    m = re.search(r"(?:firm|hold) through ([a-z]+) (\d+), (\d{4})", t)
    if m:
        through = (int(m.group(3)), MONTHS.index(m.group(1)) + 1, int(m.group(2)))
        short_date = through < (AWARD_NOT_BEFORE[0] + 1, AWARD_NOT_BEFORE[1], AWARD_NOT_BEFORE[2])
    return dict(price_hold=("surcharge" in t and "index" in t), short_date=short_date,
                sample_off=("sample" in t and "32 ect" in t),
                alt_only=any("alternate" in d for d in FORMS[name]["desc"]),
                truckload=("fee" in t and "release" in t and "pallets" in t),
                tooling_credit=num(re.search(r"credit the \$([\d,.]+\d) tooling", t).group(1)) if "tooling charge back" in t else D(0))


def item_state(name, item):
    letter = FORMS[name]["letter"]
    m = re.search(r"item (\d), would be made at our plant in ([A-Za-z ]+?), ([A-Za-z ]+?),", letter)
    if m and int(m.group(1)) == item:
        return STATE[m.group(3)]
    return FORMS[name]["state"]


def parse_terms(t):
    m = re.match(r"(\d+)% (\d+)", t)
    return (D(m.group(1)) / 100, int(m.group(2))) if m else (D(0), 0)


def security_ok(f, waive=False):
    m = re.search(r"\$([\d,]+\.\d\d)", f["security"])
    if not m or waive:
        return True, D(0)
    need = r2(f["total_written"] * SECURITY)
    short = need - num(m.group(1))
    return short <= 0, max(short, D(0))


def derive(unit_governs=True, discount_min_days=DISC_MIN_DAYS, freight_on="origin", price_hold_material=True,
           truckload_material=True, addendum_material=True, hold_bars=True, notice_counts=True, weights="current",
           plants="by item", unit_source="form", late_change=False, timely_change=True, band=BAND,
           receipt="bid opened", security_waived=False, description_read=True, firm_date_read=True, tooling="in full",
           telephone_change=False, alternate_only_read=True, sample_read=True, lot_pass_as_clearance=False):
    fig, standing, ev = {}, {}, {}
    lb = LB_CURRENT if weights == "current" else LB_FIRST
    for n in NAMES:
        f = FORMS[n]
        units = list(f["units"] if unit_source == "form" else TAB_UNITS[n])
        for it, (old, new) in CHANGES.get(n, {}).items():
            timely = CHANGE_RECEIVED[n]["key"] < DUE
            if (timely and timely_change) or (not timely and late_change):
                units[it - 1] = new
        if telephone_change and n in TELEPHONE:
            units[TELEPHONE[n][0] - 1] = TELEPHONE[n][1]
        ext = [r2(units[i] * QTY[i]) if unit_governs else f["written"][i] for i in range(5)]
        sub = sum(ext)
        freight = D(0)
        cwt_by_state = {}
        if f["fob"].startswith("Origin") and freight_on == "origin":
            for i in range(5):
                st = item_state(n, i + 1) if plants == "by item" else (f["hq_state"] if plants == "office" else f["state"])
                cwt = lb[i + 1] * QTY[i] / 100
                cwt_by_state[st] = cwt_by_state.get(st, D(0)) + cwt
                freight += r2(cwt * FREIGHT[st])
        rate, days = parse_terms(f["pay"])
        credit = r2(sub * rate) if days >= discount_min_days else D(0)
        c = conditions(n)
        tool = f["tooling"] - (c["tooling_credit"] if tooling == "net of the credit offered" else D(0))
        total = sub + tool + freight - credit
        ok, short = security_ok(f, security_waived)
        reasons = []
        if not ok:
            reasons.append("bid security short")
        if "2" not in f["addenda"] and addendum_material:
            reasons.append("addendum 2 not acknowledged")
        if f["written"][2] == r2(f["units"][2] * QTY_SUPERSEDED_3) and "2" in f["addenda"] and addendum_material:
            reasons.append("item 3 at the superseded quantity")
        if c["price_hold"] and price_hold_material:
            reasons.append("price hold exception")
        if c["short_date"] and firm_date_read:
            reasons.append("prices firm to a date short of twelve months from award")
        if description_read and "2" in f["addenda"] and any(v not in f["desc"][i - 1] for i, v in SPEC.items()):
            reasons.append("item described on a superseded specification")
        if c["truckload"] and truckload_material:
            reasons.append("truckload condition")
        if c["alt_only"] and alternate_only_read:
            reasons.append("an item offered only as an alternate, no bid on the item as specified")
        if c["sample_off"] and sample_read:
            reasons.append("a sample not made to the specification as amended")
        rc = RECEIPT[n] if receipt == "bid opened" else FIRST_LOGGED[n]
        ev[n] = dict(ext=ext, sub=sub, freight=freight, credit=credit, total=total, responsive=not reasons, short=short,
                     written=f["total_written"], holds=open_holds(n, notice_counts, lot_pass_as_clearance), key=rc["key"], rcv=rc["date"] + " " + rc["time"],
                     cwt=cwt_by_state, units=units)
        fig[f"{n} subtotal"] = money(sub)
        fig[f"{n} freight"] = money(freight)
        fig[f"{n} credit"] = money(credit)
        fig[f"{n} total"] = money(total)
        fig[f"{n} responsive"] = "Responsive" if not reasons else "Non-responsive"
        fig[f"{n} written total"] = money(f["total_written"])
        fig[f"{n} received"] = ev[n]["rcv"]
        fig[f"{n} security short"] = money(short)
        standing[f"{n} responsive"] = fig[f"{n} responsive"]
    resp = [n for n in NAMES if ev[n]["responsive"]]

    def place(n):
        t, k = ev[n]["total"], ev[n]["key"]
        ahead = sum(1 for m in resp if ev[m]["total"] < t - band)
        ahead += sum(1 for m in resp if m != n and t - band <= ev[m]["total"] <= t + band and ev[m]["key"] < k)
        return ahead + 1
    order = sorted(resp, key=place)
    assert sorted(place(n) for n in resp) == list(range(1, len(resp) + 1))
    award, passed, nxt = None, [], None
    for i, n in enumerate(order):
        if hold_bars and ev[n]["holds"]:
            passed.append(n)
            continue
        award = n
        nxt = order[i + 1] if i + 1 < len(order) else None
        break
    fig["order"] = ", ".join(order)
    fig["award"] = award
    fig["award total"] = money(ev[award]["total"])
    fig["next"] = nxt or "None"
    fig["next total"] = money(ev[nxt]["total"]) if nxt else "None"
    fig["award above next"] = money(ev[award]["total"] - ev[nxt]["total"]) if nxt else "None"
    fig["passed over"] = ", ".join(passed) or "None"
    fig["passed total"] = money(ev[passed[0]]["total"]) if passed else "None"
    fig["passed below award"] = money(ev[award]["total"] - ev[passed[0]]["total"]) if passed else "None"
    fig["passed hold"] = ", ".join(ev[passed[0]]["holds"]) if passed else "None"
    fig["approver"] = "Vice president of operations" if ev[award]["total"] > APPROVAL else "Director of supply chain"
    fig["lowest as written"] = min(NAMES, key=lambda n: ev[n]["written"])
    fig["responsive count"] = len(resp)
    fig["informality"] = ", ".join(n for n in NAMES if not OFFICER[n])
    fig["bids received"] = len(NAMES)
    for n in NAMES:
        for st, cwt in ev[n]["cwt"].items():
            fig[f"{n} hundredweight {st}"] = money(cwt)
    for n in NAMES:
        for i in range(5):
            if ev[n]["ext"][i] != FORMS[n]["written"][i]:
                fig[f"moved {n} item {i + 1}"] = f"{money(FORMS[n]['written'][i])} to {money(ev[n]['ext'][i])}"
    standing["award"] = award
    standing["award total"] = fig["award total"]
    standing["passed over"] = fig["passed over"]
    return fig, standing, ev


VARIANTS = {
    "bidder's written extensions carried": ({"unit_governs": False}, "unit price govern"),
    "discount credited at any period": ({"discount_min_days": 0}, "twenty day floor"),
    "freight not added for FOB origin": ({"freight_on": "none"}, "FOB origin"),
    "price hold condition waived": ({"price_hold_material": False}, "material term"),
    "truckload release condition waived or its later withdrawal accepted": ({"truckload_material": False}, "quantity term"),
    "unacknowledged addendum waived": ({"addendum_material": False}, "non-responsive"),
    "bid security shortfall waived": ({"security_waived": True}, "bid without security"),
    "open quality hold ignored": ({"hold_bars": False}, "not responsible"),
    "clearance notice of October 15 not read, register extract alone": ({"notice_counts": False}, "cleared it on October 15"),
    "items weighed at the first drawing revisions": ({"weights": "first"}, "current drawing revisions"),
    "all freight rated at the bid form's plant state": ({"plants": "form"}, "plant that ships it"),
    "unit prices taken from the tabulation": ({"unit_source": "tabulation"}, "signed form reads 1.575"),
    "modification received after the due time applied": ({"late_change": True}, "after the due time"),
    "modification received before the due time left out": ({"timely_change": False}, "before the due time"),
    "lower price taken inside the $100 band": ({"band": D(0)}, "bid received first"),
    "receipt timed from the first envelope logged": ({"receipt": "first logged"}, "times a resubmitted bid from the resubmission"),
    "item descriptions on the forms not read against the addenda": ({"description_read": False}, "bid on a superseded specification"),
    "a firm-through date taken as twelve months": ({"firm_date_read": False}, "short of twelve months from any award"),
    "tooling netted of the credit a letter offers": ({"tooling": "net of the credit offered"}, "added in full"),
    "telephone price change applied": ({"telephone_change": True}, "signed writing"),
    "an alternate-only item taken as a bid on the item": ({"alternate_only_read": False}, "item as specified"),
    "a sample on the superseded board not read": ({"sample_read": False}, "specification as amended"),
    "freight rated at the state of the bidder's office": ({"plants": "office"}, "plant that ships it"),
    "the verification lot's pass taken as clearance of the hold": ({"lot_pass_as_clearance": True}, "has not signed the clearance"),
}

if __name__ == "__main__":
    fig, standing, ev = derive()
    if "--print" in sys.argv:
        for k, v in fig.items():
            print(k, v)
        for name, (kw, _) in VARIANTS.items():
            f2, s2, _e = derive(**kw)
            print(f"{name:70s} -> {f2['award']} {f2['award total']} next {f2['next']} passed {f2['passed over']}")
        sys.exit(0)
    wb = openpyxl.load_workbook(GOLDEN, data_only=True)
    rep = Report()
    rep.expect("tabulation cells that differ from the forms", str(TAB_DIFF), str([("Ridgecrest Packaging", 4)]))
    s = wb["Recommendation"]
    rows = {s.cell(row=r, column=1).value: [s.cell(row=r, column=c).value for c in range(2, 2 + len(NAMES))] for r in range(1, 46) if s.cell(row=r, column=1).value}
    hdr = rows["Bidder"]
    rep.expect("bidders", str(hdr), str(NAMES))
    for j, n in enumerate(hdr):
        rep.expect(f"{n} responsive", fig[f"{n} responsive"], rows["Responsiveness"][j])
        rep.expect(f"{n} written total", fig[f"{n} written total"], money(rows["Total bid as written"][j]))
        rep.expect(f"{n} subtotal", fig[f"{n} subtotal"], money(rows["Corrected extensions"][j]))
        rep.expect(f"{n} tooling", money(FORMS[n]["tooling"]), money(rows["Tooling"][j]))
        rep.expect(f"{n} freight", fig[f"{n} freight"], money(rows["Freight added, FOB origin"][j]))
        rep.expect(f"{n} credit", fig[f"{n} credit"], money(rows["Payment discount credit"][j]))
        rep.expect(f"{n} total", fig[f"{n} total"], money(rows["Total evaluated price"][j]))
        rep.expect(f"{n} received", fig[f"{n} received"], rows["Bid received"][j])
    order = fig["order"].split(", ")
    for j, n in enumerate(hdr):
        want = order.index(n) + 1 if n in order else "Set aside"
        rep.expect(f"{n} order in line", want, rows["Order in line among responsive bids, 5.1 and 5.6"][j])
    rep.expect("award", fig["award"], rows["Recommended award"][0])
    rep.expect("award total", fig["award total"], money(rows["Recommended award, total evaluated price"][0]))
    rep.expect("next", fig["next"], rows["Next responsive bidder in line"][0])
    rep.expect("next total", fig["next total"], money(rows["Next bidder in line, total evaluated price"][0]))
    rep.expect("award above next", fig["award above next"], money(rows["Recommended award above the next bid in line by"][0]))
    rep.expect("order rests on 5.6", abs(D(fig["award above next"].replace(",", ""))) <= BAND, rows["Order between the two bids rests on"][0].startswith("5.6"))
    rep.expect("award received", fig[f"{fig['award']} received"], rows["Recommended bid received"][0])
    rep.expect("next received", fig[f"{fig['next']} received"], rows["Next bid in line received"][0])
    rep.expect("passed over", fig["passed over"], rows["Responsive bid passed over, open quality hold"][0])
    rep.expect("passed total", fig["passed total"], money(rows["Passed-over bid, total evaluated price"][0]))
    rep.expect("passed below award", fig["passed below award"], money(rows["Passed-over bid below the recommended award by"][0]))
    rep.expect("approver", fig["approver"], rows["Approver required by PP-3.5.3"][0])
    rep.expect("lowest as written", fig["lowest as written"], rows["Lowest bid as written"][0])
    rep.expect("responsive count", fig["responsive count"], rows["Responsive bids"][0])
    rep.expect("set aside count", len(NAMES) - fig["responsive count"], rows["Bids set aside as non-responsive"][0])
    moved = [k for k in fig if k.startswith("moved ")]
    timely = sum(len(ch) for n, ch in CHANGES.items() if CHANGE_RECEIVED[n]["key"] < DUE)
    late = sum(len(ch) for n, ch in CHANGES.items() if CHANGE_RECEIVED[n]["key"] >= DUE) + len(TELEPHONE)
    rep.expect("extensions corrected", len(moved) - timely, rows["Extensions corrected for arithmetic or quantity"][0])
    rep.expect("changes applied", timely, rows["Unit price changes applied from a timely signed modification"][0])
    rep.expect("changes not considered", late, rows["Unit price changes not considered under section 3.4"][0])
    rep.expect("corrected on the award, written", fig["moved Pemberton Container item 2"].split(" to ")[0], money(rows["Extension corrected on the recommended bid, as written"][0]))
    rep.expect("corrected on the award, corrected", fig["moved Pemberton Container item 2"].split(" to ")[1], money(rows["Extension corrected on the recommended bid, corrected"][0]))
    resp_col = {n: j for j, n in enumerate(hdr)}
    rep.expect("passed over responsibility", "Not responsible, open quality hold, PP-3.7.1", rows["Responsibility of the bidder in line, PP-3.7.1"][resp_col[fig["passed over"]]])
    rep.expect("award responsibility", "Responsible", rows["Responsibility of the bidder in line, PP-3.7.1"][resp_col[fig["award"]]])
    rep.expect("informality", fig["informality"], "Pemberton Container" if str(rows["Informality waived under 5.7"][0]).startswith("Form signed by a regional sales manager") else rows["Informality waived under 5.7"][0])
    # per-line columns behind the front page
    e = wb["Evaluation"]
    for j, n in enumerate(NAMES):
        for i in range(5):
            rep.expect(f"{n} item {i + 1} unit evaluated", f"{ev[n]['units'][i]:.3f}", f"{e.cell(row=4 + i, column=2 + j).value:.3f}")
            rep.expect(f"{n} item {i + 1} extension", money(ev[n]["ext"][i]), money(e.cell(row=9 + i, column=2 + j).value))
    x = wb["Extensions"]
    for j, n in enumerate(NAMES):
        for i in range(5):
            r = 4 + 5 * j + i
            rep.expect(f"{n} item {i + 1} unit on the form", f"{FORMS[n]['units'][i]:.3f}", f"{x.cell(row=r, column=3).value:.3f}")
            rep.expect(f"{n} item {i + 1} written", money(FORMS[n]["written"][i]), money(x.cell(row=r, column=6).value))
    b = wb["Bid Security"]
    for j, n in enumerate(NAMES):
        rep.expect(f"{n} security short", fig[f"{n} security short"], money(b.cell(row=4 + j, column=6).value))
        rep.expect(f"{n} five percent", money(r2(FORMS[n]["total_written"] * SECURITY)), money(b.cell(row=4 + j, column=5).value))
    fr = wb["Freight"]
    rep.expect("hundredweight IA", fig["Ridgecrest Packaging hundredweight IA"], money(fr["F16"].value))
    rep.expect("hundredweight NE", fig["Ridgecrest Packaging hundredweight NE"], money(fr["F17"].value))
    rep.expect("hundredweight MN", fig["Mesabi Container Co. hundredweight MN"], money(fr["F18"].value))
    rep.expect("Ridgecrest freight on the tab", fig["Ridgecrest Packaging freight"], money(fr["J14"].value))
    rep.expect("Mesabi freight on the tab", fig["Mesabi Container Co. freight"], money(fr["J15"].value))
    h = wb["Holds on Bidders"]
    for r in range(4, 8):
        no = h.cell(row=r, column=1).value
        reg = next(g for g in HOLDS if g["no"] == no)
        rep.expect(f"{no} registered name", reg["supplier"], h.cell(row=r, column=2).value)
        rep.expect(f"{no} status in the extract", reg["status"], h.cell(row=r, column=6).value)
        want = "Cleared" if reg["status"] == "Cleared" or no in CLEARED_BY_NOTICE else "Open"
        rep.expect(f"{no} status at recommendation", want, h.cell(row=r, column=9).value)
    lwr = wb["Later Writings"]
    for r in range(4, 10):
        no = lwr.cell(row=r, column=4).value
        g = next(g for g in LOG if g["no"] == no)
        rep.expect(f"{no} received", g["date"] + " " + g["time"], f"{lwr.cell(row=r, column=5).value} {lwr.cell(row=r, column=6).value}")
        rep.expect(f"{no} before the due time", "Yes" if g["key"] < DUE else "No", lwr.cell(row=r, column=8).value)
    note = "\n".join(str(c.value) for row in wb["Note to Torsten"].iter_rows() for c in row if c.value)
    late_fig, _s, _e = derive(late_change=True)
    for phrase in ("vice president", f"${fig['Kessel Container Corp. total']}", f"${fig['Thorsgard Box & Label total']}", f"${fig['Otter Tail Corrugated total']}", f"${fig['award total']}", f"${fig['next total']}", f"${fig['award above next']}", f"${fig['passed below award']}",
                   f"${fig['passed total']}", fig["passed hold"], "26,912.00", "26,112.00", "25,900.00", "25,600.00", f"${fig['Ridgecrest Packaging freight']}",
                   f"${fig['Ridgecrest Packaging credit']}", f"${fig['Ridgecrest Packaging total']}", "1,072 hundredweight", "396 hundredweight", f"${fig['Ridgecrest Packaging security short']}",
                   f"${fig['Dahlgren Paper Box Co. total']}", f"${fig['Halvard Corrugated total']}", f"${fig['Wenzel & Krause Corrugated total']}",
                   f"${fig['Pemberton Container subtotal']}", f"${fig['Ridgecrest Packaging written total']}", "4,554.95", "4,674.95",
                   "11:37 on October 5", "09:33 on October 6", "09:12 on October 6", "10:07 on October 6", "QH-26-034", "October 20", "October 16", "L&V Container Corp.", "regional sales manager",
                   f"${fig['Mesabi Container Co. total']}", f"${fig['Mesabi Container Co. freight']}", "1,468 hundredweight", "10:00 on October 6", "09:38 on October 6", "0.594"):
        rep.expect(f"note states {phrase}", phrase in note, True)
    rep.sensitivity(lambda **kw: derive(**kw)[1], VARIANTS)
    rep.finish()
