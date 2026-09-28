"""verify_golden.py for lien-analysis-larkspur: re-derive every figure the analysis states from inputs/ alone
under Practice Note PN-14 as the golden applies it (the recorder's copies of the seven claims, the owner's notice
and waiver logs, the direct contractor's check ledger, and the close-out file), and list the alternate readings a
reviewer could take with the phrase the golden uses to settle each one.

    .venv/bin/python drafts/11-lien-analysis-larkspur/verify_golden.py
"""
import csv
import os
import re
import sys
import datetime as dt
from decimal import Decimal as D, ROUND_HALF_UP
from pathlib import Path

import openpyxl
from docx import Document

HERE = Path(__file__).resolve().parent
ROOT = os.environ.get("HAZY_ROOT") or next(str(p) for p in HERE.parents if (p / "tools" / "golden_verify.py").is_file())
sys.path.insert(0, os.path.join(ROOT, "tools"))
from golden_verify import Report  # noqa: E402

INPUTS = HERE / "inputs"
GOLDEN = HERE / "solution" / "lien_analysis_larkspur_crossing.xlsx"
MONTHS = {m: i for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July", "August",
                                       "September", "October", "November", "December"], start=1)}


def r2(x):
    return D(x).quantize(D("0.01"), rounding=ROUND_HALF_UP)


def money(x):
    return f"{D(x):,.2f}"


def longdate(s):
    m = re.search(r"([A-Z][a-z]+) (\d{1,2}), (\d{4})", s)
    return dt.date(int(m.group(3)), MONTHS[m.group(1)], int(m.group(2)))


def mdy(s):
    m, d, y = s.split("/")
    return dt.date(int(y), int(m), int(d))


def fmt(d):
    return d.strftime("%m/%d/%Y")


def dollars(s):
    return D(s.replace("$", "").replace(",", ""))


def doc_text(path):
    d = Document(path)
    return "\n".join(p.text for p in d.paragraphs), d


# ---------------------------------------------------------------- practice note: the constants
note, _ = doc_text(INPUTS / "practice_note_pn14_mechanics_liens.docx")
assert "within 15 days after completion" in note and "30 days after the owner records a notice of completion" in note
assert "60 days after the owner records a notice of completion" in note and "20 days after the claimant first furnishes" in note
assert "within 90 days after the claim is recorded" in note and "125 percent of the amount of the claim of lien as recorded" in note
assert "at least 10 days before the petition" in note and "Saturday, a Sunday, or a court holiday" in note
assert "the day the notice is given is excluded" in note and "effective when signed, whether or not the claimant has been paid" in note
assert "stopped or returned unpaid is not payment" in note and "does not follow the statutory form does not release the lien" in note
NOC_DAYS, SUB_DAYS, DC_DAYS, PRELIM_DAYS, ACTION_DAYS, BOND_PCT, DEMAND_DAYS = 15, 30, 60, 20, 90, D(125), 10

# ---------------------------------------------------------------- close-out file: completion, NOC, searches
corr, _ = doc_text(INPUTS / "completion_and_correspondence_larkspur.docx")
COMPLETION = longdate(re.search(r"was completed on ([A-Z][a-z]+ \d+, \d{4})", corr).group(0))
NOC_RECORDED = longdate(re.search(r"Recorded ([A-Z][a-z]+ \d+, \d{4}), Placer County Recorder, Document No\. 2026-0079143", corr).group(0))
INDEX_DATE = longdate(re.search(r"civil case index search, run ([A-Z][a-z]+ \d+, \d{4})", corr).group(0))
assert "no civil action found naming Piedmont Ridge Properties" in corr and "no notice of pendency of action" in corr
NO_ACTION = True
RETENTION = dollars(re.search(r"stands at (\$[\d,]+\.\d\d) against the contract sum", corr).group(1))
HVAC = dollars(re.search(r"estimated the correction at (\$[\d,]+\.\d\d)", corr).group(1))
DC_WINDOW_OPEN = "We will record our own claim if the retention is not released" in corr

# ---------------------------------------------------------------- the claims
ctext, cdoc = doc_text(INPUTS / "claims_of_lien_larkspur_crossing.docx")
CLAIMS = {}
for m in re.finditer(r"Claim (\d)\. (.+?), recorded ([A-Z][a-z]+ \d+, \d{4}), Document No\. (\S+)\n(.*?)(?=\nClaim \d\. |\Z)", ctext, re.S):
    n, name, rec, doc, body = m.groups()
    amount = dollars(re.search(r"after deducting all just credits and offsets, is (\$[\d,]+\.\d\d)", body).group(1))
    first = longdate(re.search(r"first furnished work on ([A-Z][a-z]+ \d+, \d{4})", body).group(0))
    last = longdate(re.search(r"last furnished work on ([A-Z][a-z]+ \d+, \d{4})", body).group(0))
    prelim = longdate(re.search(r"preliminary notice was given on ([A-Z][a-z]+ \d+, \d{4})", body).group(0))
    item6 = re.search(r"6\. General description of the work furnished: (.*?)\n7\.", body, re.S).group(1)
    CLAIMS[name] = dict(n=int(n), recorded=longdate(rec), doc=doc, amount=amount, first=first, last=last, prelim=prelim, item6=item6)
assert len(CLAIMS) == 7
# exhibits: Norcal's proof of service parties, Hedrick's statement of account
tables = cdoc.tables
norcal_parties = [r.cells[0].text for r in tables[0].rows[1:]]
assert all("direct contractor" in p for p in norcal_parties) and not any("Piedmont" in p or "owner" in p.lower() for p in norcal_parties)
hedrick = []
for r in tables[1].rows[1:-1]:
    inv, delivered, mat, amt, paid, bal = [c.text for c in r.cells]
    hedrick.append(dict(inv=inv, date=mdy(delivered), amount=dollars(amt), balance=dollars(bal)))
assert sum(h["balance"] for h in hedrick) == CLAIMS["Hedrick & Sons Building Supply"]["amount"]

# ---------------------------------------------------------------- owner's project file
wb = openpyxl.load_workbook(INPUTS / "owner_project_file_larkspur.xlsx", data_only=True)
ws = wb["Prelim Log"]
PRELIM = {}
for r in ws.iter_rows(min_row=5, values_only=True):
    if r[0]:
        PRELIM[r[0]] = dict(mailed=mdy(r[4]), first=mdy(r[6]), served=r[8])
ws = wb["Subcontractors"]
SUBVAL = {r[0]: D(str(r[3])) for r in ws.iter_rows(min_row=4, values_only=True) if r[0]}
ws = wb["Waiver Log"]
WAIVERS = []
for r in ws.iter_rows(min_row=5, values_only=True):
    for block in (r[0:9], r[9:18]):
        if block[0]:
            WAIVERS.append(dict(claimant=block[0], form=block[2], through=mdy(block[3]), amount=D(str(block[4])), exceptions=block[5], check=block[6]))
assert len(WAIVERS) == 40

# ---------------------------------------------------------------- the direct contractor's ledger
LEDGER = {}
with open(INPUTS / "dk_subcontractor_payments.csv", encoding="utf-8-sig") as fh:
    for row in csv.DictReader(fh):
        LEDGER[int(row["CHECK_NO"])] = row
assert LEDGER[4460]["STATUS"] == "Stopped" and LEDGER[4461]["STATUS"] == "Cleared"


# ---------------------------------------------------------------- the method
def extend(d):
    """Code of Civil Procedure section 12a: a last day on a weekend runs to the Monday."""
    if d.weekday() == 5:
        return d + dt.timedelta(days=2)
    if d.weekday() == 6:
        return d + dt.timedelta(days=1)
    return d


def components(name):
    """Each claim built up from its own statement: (label, date furnished through, amount, kind)."""
    c = CLAIMS[name]
    out = []
    if name == "Hedrick & Sons Building Supply":
        for h in hedrick:
            if h["balance"] > 0:
                out.append((h["inv"], h["date"], h["balance"], "materials"))
        return out
    if name == "Norcal Rebar & Mesh, LLC":
        return [("materials", c["last"], c["amount"], "materials")]
    if name == "Tallac Concrete, Inc.":
        ret = r2(SUBVAL[name] * D("0.05"))
        return [("retention", c["last"], ret, "retention"), ("May billing balance", c["last"], c["amount"] - ret, "progress")]
    t = c["item6"]
    for m in re.finditer(r"(?:progress payment|final billing|final progress payment) for the period ending ([A-Z][a-z]+ \d+, \d{4}) in the sum of (\$[\d,]+\.\d\d)", t):
        out.append((m.group(0)[:40], longdate(m.group(1)), dollars(m.group(2)), "progress"))
    m = re.search(r"retention withheld in the sum of (\$[\d,]+\.\d\d)", t)
    out.append(("retention", c["last"], dollars(m.group(1)), "retention"))
    m = re.search(r"invoice (\S+) dated .*? through ([A-Z][a-z]+ \d+, \d{4}) in the sum of (\$[\d,]+\.\d\d)", t)
    if m:
        out.append((m.group(1), longdate(m.group(2)), dollars(m.group(3)), "progress"))
    assert sum(x[2] for x in out) == c["amount"], (name, out, c["amount"])
    return out


def derive(weekend_ext=True, cond_on_signing=False, uncond_needs_payment=False, dc_notice_suffices=False,
           expiry_checked=True, late_notice_covers_all=False, bond_pct=BOND_PCT, deadline_from="noc"):
    fig, standing = {}, {}
    noc_ok = (NOC_RECORDED - COMPLETION).days <= NOC_DAYS
    fig["days completion to noc"] = (NOC_RECORDED - COMPLETION).days
    base = NOC_RECORDED if deadline_from == "noc" else COMPLETION
    last_sub = base + dt.timedelta(days=SUB_DAYS)
    last_dc = base + dt.timedelta(days=DC_DAYS)
    if weekend_ext:
        last_sub, last_dc = extend(last_sub), extend(last_dc)
    fig["last day others"] = fmt(last_sub)
    fig["last day direct contractor"] = fmt(last_dc)
    fig["retention due"] = fmt(extend(COMPLETION + dt.timedelta(days=45)))
    fig["withhold for hvac"] = money(r2(HVAC * D("1.5")))
    total_rec = total_enf = total_bond = release_amt = D(0)
    for name, c in CLAIMS.items():
        # lien rights: notice given to the owner
        if name == "Norcal Rebar & Mesh, LLC":
            given = c["prelim"]
            served_owner = dc_notice_suffices
        else:
            given = PRELIM[name]["mailed"]
            served_owner = PRELIM[name]["served"].startswith("Owner")
        first = c["first"]
        timely_notice = (given - first).days <= PRELIM_DAYS
        coverage = first if (timely_notice or late_notice_covers_all) else given - dt.timedelta(days=PRELIM_DAYS)
        rights = served_owner
        # recording deadline
        timely = c["recorded"] <= last_sub
        # expiry
        due = c["recorded"] + dt.timedelta(days=ACTION_DAYS)
        if weekend_ext:
            due = extend(due)
        expired = expiry_checked and NO_ACTION and INDEX_DATE > due
        # waivers
        def released(date, kind):
            if kind == "retention":
                return False
            for w in WAIVERS:
                if w["claimant"] != name or w["through"] < date:
                    continue
                statutory = w["form"].startswith("Unconditional") or w["form"].startswith("Conditional")
                if not statutory:
                    continue
                if w["form"].startswith("Unconditional"):
                    if uncond_needs_payment:
                        m = re.search(r"check (\d{4})", w["check"] or "")
                        paid = bool(m) and LEDGER[int(m.group(1))]["STATUS"] == "Cleared"
                        if not paid:
                            continue
                    return True
                m = re.search(r"check (\d{4})", w["check"] or "")
                paid = bool(m) and LEDGER[int(m.group(1))]["STATUS"] == "Cleared"
                if paid or cond_on_signing:
                    return True
            return False
        enf = D(0)
        for label, date, amt, kind in components(name):
            if date >= coverage and not released(date, kind):
                enf += amt
        if not rights:
            st = "No lien rights"
        elif not timely:
            st = "Untimely"
        elif expired:
            st = "Expired"
        else:
            st = "Enforceable"
        enforceable = enf if st == "Enforceable" else D(0)
        bond = r2(c["amount"] * bond_pct / 100) if st == "Enforceable" else D(0)
        total_rec += c["amount"]; total_enf += enforceable; total_bond += bond
        if st != "Enforceable":
            release_amt += c["amount"]
        fig[f"{name} standing"] = st
        fig[f"{name} enforceable"] = money(enforceable)
        fig[f"{name} bond"] = money(bond)
        fig[f"{name} timely"] = "Yes" if timely else "No"
        fig[f"{name} rights"] = "Yes" if rights else "No"
        fig[f"{name} expired"] = "Yes" if expired else "No"
        fig[f"{name} coverage from"] = fmt(coverage)
        standing[f"{name} standing"] = st
        standing[f"{name} enforceable"] = money(enforceable)
        standing[f"{name} bond"] = money(bond)
    fig["claims as recorded"] = money(total_rec)
    fig["enforceable total"] = money(total_enf)
    fig["bonds total"] = money(total_bond)
    fig["release demands amount"] = money(release_amt)
    fig["noc effective"] = "Yes" if noc_ok else "No"
    standing["last day others"] = fig["last day others"]
    standing["bonds total"] = fig["bonds total"]
    return fig, standing


VARIANTS = {
    "no weekend extension of the last day": ({"weekend_ext": False}, "fell on a Saturday"),
    "conditional waiver treated as effective when signed": ({"cond_on_signing": True}, "stopped"),
    "unconditional waiver treated as ineffective without payment": ({"uncond_needs_payment": True}, "effective when signed"),
    "notice to the direct contractor alone accepted": ({"dc_notice_suffices": True}, "never given to the owner"),
    "ninety day expiry not checked": ({"expiry_checked": False}, "has expired"),
    "late preliminary notice treated as covering all deliveries": ({"late_notice_covers_all": True}, "reaches back only to May 9"),
    "bond measured at 100 percent": ({"bond_pct": D(100)}, "125 percent of the recorded"),
    "thirty days counted from completion": ({"deadline_from": "completion"}, "thirtieth day after the notice of completion"),
}

if __name__ == "__main__":
    fig, standing = derive()
    if "--print" in sys.argv:
        for k, v in fig.items():
            print(k, v)
        sys.exit(0)
    gwb = openpyxl.load_workbook(GOLDEN, data_only=True)
    rep = Report()
    s = gwb["Summary"]
    kd = {s.cell(row=r, column=1).value: s.cell(row=r, column=2).value for r in range(6, 15)}
    rep.expect("days completion to noc", fig["days completion to noc"], kd["Days from completion to recording"])
    rep.expect("last day others", fig["last day others"], kd["Last day to record, claimants other than the direct contractor"])
    rep.expect("last day direct contractor", fig["last day direct contractor"], kd["Last day to record, direct contractor"])
    rep.expect("noc effective", fig["noc effective"], "Yes" if str(kd["Notice of completion effective"]).startswith("Yes") else "No")
    hdr_row = next(r for r in range(15, 20) if s.cell(row=r, column=1).value == "CLAIMANT")
    for r in range(hdr_row + 1, hdr_row + 8):
        name = s.cell(row=r, column=1).value
        rep.expect(f"{name} standing", fig[f"{name} standing"], s.cell(row=r, column=7).value)
        rep.expect(f"{name} rights", fig[f"{name} rights"], s.cell(row=r, column=4).value)
        rep.expect(f"{name} timely", fig[f"{name} timely"], s.cell(row=r, column=5).value)
        rep.expect(f"{name} expired", fig[f"{name} expired"], s.cell(row=r, column=6).value)
        rep.expect(f"{name} enforceable", fig[f"{name} enforceable"], money(s.cell(row=r, column=8).value))
        rep.expect(f"{name} bond", fig[f"{name} bond"], money(s.cell(row=r, column=10).value))
        rep.expect(f"{name} recorded amount", money(CLAIMS[name]["amount"]), money(s.cell(row=r, column=3).value))
    tot = {s.cell(row=r, column=1).value: s.cell(row=r, column=2).value for r in range(hdr_row + 8, hdr_row + 16) if s.cell(row=r, column=1).value}
    rep.expect("claims as recorded", fig["claims as recorded"], money(tot["Amount of the seven claims as recorded"]))
    rep.expect("enforceable total", fig["enforceable total"], money(tot["Amount the claimants could enforce against the property"]))
    rep.expect("bonds total", fig["bonds total"], money(tot["Release bonds required, total penal sum at 125 percent"]))
    rep.expect("release demands amount", fig["release demands amount"], money(tot["Recorded amount of the claims to demand released"]))
    p = gwb["Prelim Notices"]
    for r in range(4, 11):
        name = p.cell(row=r, column=1).value
        rep.expect(f"{name} coverage from", fig[f"{name} coverage from"], p.cell(row=r, column=8).value)
    pr = gwb["Parameters"]
    prm = {pr.cell(row=r, column=1).value: pr.cell(row=r, column=2).value for r in range(4, 40) if pr.cell(row=r, column=1).value}
    rep.expect("retention due", fig["retention due"], prm["Retention due to the direct contractor"])
    rep.expect("withhold for hvac", fig["withhold for hvac"], money(prm["Retention the owner may withhold for the rooftop unit correction"]))
    rep.expect("retention withheld", money(RETENTION), money(prm["Retention withheld from the direct contractor"]))
    note = "\n".join(str(c.value) for row in gwb["Note to Marguerite"].iter_rows() for c in row if c.value)
    for phrase in (f"${fig['bonds total']}", f"${fig['enforceable total']}" if False else "$33,982.19", "$8,125.00", "$159,145.00", "$61,477.00",
                   "$198,931.25", "$76,846.25", "$65,398.05", "$58,250.00", "$99,830.00", f"${fig['claims as recorded']}",
                   "September 21, 2026", "October 19, 2026", "$187,412.50", "$33,000.00", "check 4460", "check 4461", "May 9", "$18,336.25"):
        rep.expect(f"note states {phrase}", phrase in note, True)
    rep.expect("direct contractor window still open in the correspondence", DC_WINDOW_OPEN, True)
    rep.sensitivity(lambda **kw: derive(**kw)[1], VARIANTS)
    rep.finish()
