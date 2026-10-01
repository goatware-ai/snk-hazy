"""verify_golden.py for title-exam-cedarbrook-lot12: re-derive every figure and every standing the
examination report states from inputs/ alone, under the conventions the report states, and list the
alternate readings a solver could take with the phrase the report uses to settle each one.

    .venv/bin/python submissions/02-title-exam-cedarbrook-lot12/verify_golden.py

The method reads the instruments as abstracted (guideline 1.3), measures the part of Lot 13 each deed
describes and walks record title to each piece of the land separately, identifies every person by
the full name the court records give, tests every mortgage release against the holder of record,
runs every certificate of judgment against the owner of each piece and the five-year life of the
lien, and works the taxes from the duplicate's dates. Each VARIANT is one missed read; every one of them moves
a graded standing or figure.
"""
import csv
import datetime as dt
import os
import re
import sys
import zipfile
from decimal import Decimal as D, ROUND_HALF_UP
from pathlib import Path

import openpyxl

HERE = Path(__file__).resolve().parent
ROOT = os.environ.get("HAZY_ROOT") or next(str(p) for p in HERE.parents if (p / "tools" / "golden_verify.py").is_file())
sys.path.insert(0, os.path.join(ROOT, "tools"))
from golden_verify import Report  # noqa: E402

INPUTS = HERE / "inputs"
MONTHS = {m: i for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July", "August",
                                      "September", "October", "November", "December"], 1)}


def c(x):
    return D(x).quantize(D("0.01"), rounding=ROUND_HALF_UP)


def money(x):
    return f"{D(x):,.2f}"


def pdate(s):
    return dt.datetime.strptime(s, "%m/%d/%Y").date()


def ldate(s):
    m = re.search(r"(January|February|March|April|May|June|July|August|September|October|November|December) (\d{1,2}), (\d{4})", s)
    return dt.date(int(m.group(3)), MONTHS[m.group(1)], int(m.group(2))) if m else None


def docx_paragraphs(path):
    xml = zipfile.ZipFile(path).read("word/document.xml").decode("utf-8")
    out = []
    for p in re.findall(r"<w:p[ >].*?</w:p>", xml, flags=re.S):
        t = "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", p))
        t = t.replace("&amp;", "&").replace("&apos;", "'").replace("&quot;", '"')
        if t.strip():
            out.append(t.strip())
    return out


# ---------------------------------------------------------------- read the inputs
INDEX = list(csv.DictReader(open(INPUTS / "recorder_index_cedarbrook_lot12.csv", newline="")))
BYNO = {r["INSTRUMENT_NO"]: r for r in INDEX}


def volpage_key(text):
    """'Official Record 1540, Page 291' or 'OR 1540/291' -> ('OR', '1540', '291')."""
    m = re.search(r"(Official Record|Mortgage Book|Deed Book) (\d+), Page (\d+)", text)
    if m:
        return ({"Official Record": "OR", "Mortgage Book": "MB", "Deed Book": "DB"}[m.group(1)], m.group(2), m.group(3))
    m = re.match(r"(OR|MB|DB) (\d+)/(\d+)", text)
    return (m.group(1), m.group(2), m.group(3)) if m else None


BYVP = {volpage_key(r["VOL_PAGE"]): r["INSTRUMENT_NO"] for r in INDEX}

ABS = {}
_paras = docx_paragraphs(INPUTS / "instrument_abstracts_hlt262214.docx")
for i, p in enumerate(_paras):
    m = re.search(r"instrument (\d{12}), recorded", p)
    if m and i + 1 < len(_paras):
        ABS[m.group(1)] = _paras[i + 1]

_order_xml = zipfile.ZipFile(INPUTS / "title_order_hlt262214.docx").read("word/document.xml").decode("utf-8")
ORDER = " ".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", _order_xml))
CLOSING = ldate(re.search(r"Closing date(.{0,40})", ORDER).group(1))
COMMIT = ldate(re.search(r"Commitment date(.{0,40})", ORDER).group(1))

wb = openpyxl.load_workbook(INPUTS / "tax_and_lien_search_hlt262214.xlsx", data_only=True)
TAX = [r for r in wb["Tax Duplicate"].iter_rows(values_only=True) if isinstance(r[0], int)]
JL = [r for r in wb["Judgment Liens"].iter_rows(values_only=True) if isinstance(r[0], str) and re.match(r"\d\dJL\d+", r[0])]
ENTRIES = [r for r in wb["Docket Entries"].iter_rows(values_only=True) if isinstance(r[0], str) and re.match(r"\d\dJL\d+", r[0])]
cw = openpyxl.load_workbook(INPUTS / "court_records_search_hlt262214.xlsx", data_only=True)
PROBATE = [r for r in cw["Probate"].iter_rows(values_only=True) if isinstance(r[0], str) and re.match(r"\d\d[A-Z]{2}\d+", r[0])]
DOMESTIC = [r for r in cw["Domestic Relations"].iter_rows(values_only=True) if isinstance(r[0], str) and re.match(r"\d\dDR\d+", r[0])]


def survey_rows():
    """Improvement -> (north-south size, east-west size, feet south of the north line, feet west of the front line)."""
    xml = zipfile.ZipFile(INPUTS / "location_survey_418_cedarbrook.docx").read("word/document.xml").decode("utf-8")
    out = {}
    for tr in re.findall(r"<w:tr[ >].*?</w:tr>", xml, flags=re.S):
        cells = ["".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", tc)) for tc in re.findall(r"<w:tc>.*?</w:tc>", tr, flags=re.S)]
        if len(cells) == 4 and re.match(r"\d", cells[2]):
            size = re.findall(r"\d+\.\d\d", cells[1])
            ns = D(size[0])
            ew = D(size[1]) if len(size) > 1 else None
            out[cells[0].split(",")[0].split(" on ")[0]] = (ns, ew, D(cells[2]), D(cells[3].split()[0]))
    return out


LOT_WIDTH = D("84.50")
LOT_DEPTH = D("150.00")

PIECES = ("L12", "N24", "STRIP")     # Lot 12; the north 24.25 feet of Lot 13; the next 18.00 feet of Lot 13


def describes(no):
    """The land an instrument describes, from the abstract of the instrument itself."""
    text = ABS.get(no, "")
    out = set()
    if re.search(r"Lot (Number Twelve \(12\)|12)", text):
        out.add("L12")
    m = re.search(r"[Nn]orth (?:[A-Z][a-z-]+ and 25/100 \()?(\d+\.\d\d)\)? feet\s+of Lot", text)
    if m:
        feet = D(m.group(1))
        out.add("N24")
        if feet >= D("42.25"):
            out.add("STRIP")
    return out


def strip_feet():
    full = D(re.search(r"\((\d+\.\d\d)\) feet", ABS["200303070115"]).group(1))
    part = D(re.search(r"\((\d+\.\d\d)\) feet", ABS["201409190112"]).group(1))
    return full - part


def full_names():
    """Index-form name of each owner -> the full name the court records give that person."""
    out = {}
    lic = [r for r in PROBATE if r[1] == "Marriage license"]
    est = [r for r in PROBATE if r[1] == "Estate"]
    # Pruitt: the owner is the man married to Lorraine K., who signed the mortgages with him
    for r in lic:
        if r[3].startswith("STROUD LORRAINE") or r[2].startswith("STROUD LORRAINE"):
            out["Pruitt Daniel R"] = r[2]
        if r[3].startswith("TOLLIVER MARGARET ANN"):
            out["Kessler Robert L"] = r[2]
        if r[3].startswith("BELLO TAMSIN"):
            out["Bello Tamsin N"] = r[3]
            out["Okafor Emeka C"] = r[2]
    for r in est:
        if r[2].startswith("VOSS HAROLD"):
            out["Voss Harold E"] = r[2]
    return out


def caption_name(case):
    who = case.split(" v. ")[-1].split()
    return " ".join([who[-1]] + who[:-1]).upper()


def derive(description_skimmed=False, reference_by_index=False, assignor_release_clears=False,
           insure_over_at_closing=False, late_refile_renews=False, lien_ends_at_conveyance=False,
           payment_ignored=False, interest_from_filing=False, late_payment_missed=False, penalty="0.10",
           proration_through_closing=True, prorate_assessment=False, year_days=365, pending_case_terminates=False,
           decree_ignored=False, dower_is_title=False, inclusive_days=False, same_initial_same_man=False,
           nickname_read=False, porch_ignored=False, all_survivorship=False, vacated_credit_applied=False,
           amendment_counted_loosely=False, maturity_ignored=False, lapsed_in_force=False, chain_from_filing=False,
           credits_to_principal=False, short_payment_missed=False, proration_on_gross=False):
    # ---------------------------------------------------------- chain of title, piece by piece
    deeds = [r for r in INDEX if r["DOC_TYPE"] == "WARRANTY DEED" and "L12" in describes(r["INSTRUMENT_NO"])]
    holder = {p: None for p in PIECES}
    held = {p: [] for p in PIECES}
    gap = None
    for r in deeds:
        no = r["INSTRUMENT_NO"]
        land = describes(no)
        if description_skimmed and "N24" in land:
            land = land | {"STRIP"}
        for piece in PIECES:
            if holder[piece] is None:
                if piece in land:
                    holder[piece] = r["GRANTEE"]
                    held[piece].append([r["GRANTEE"], pdate(r["RECORDED"]), None])
                continue
            surname = r["GRANTOR"].split()[0] == holder[piece].split()[0]
            if piece in land and surname:
                held[piece][-1][2] = pdate(r["RECORDED"])
                holder[piece] = r["GRANTEE"]
                held[piece].append([r["GRANTEE"], pdate(r["RECORDED"]), None])
            elif piece not in land and surname and gap is None:
                gap = no

    def owners(piece):
        out = []
        for names, d0, d1 in held[piece]:
            sur = names.split()[0]
            for given in names[len(sur):].split("&"):
                out.append((f"{sur} {given.strip()}", d0, d1))
        return out

    names = full_names()

    # ---------------------------------------------------------- survivorship (guideline 4.4)
    death = {r[2]: (r[0], pdate(r[6])) for r in PROBATE if r[1] == "Estate" and r[5] == "Date of death"}
    surv = []
    common = []
    for i, r in enumerate(deeds[:-1]):
        if "remainder to the survivor" not in ABS[r["INSTRUMENT_NO"]] and not all_survivorship:
            sur = r["GRANTEE"].split()[0]
            took = [g.strip() for g in r["GRANTEE"][len(sur):].split("&")]
            gave = [g.strip() for g in deeds[i + 1]["GRANTOR"][len(sur):].split("&")]
            for t in took:
                if len(took) > 1 and t not in gave:
                    dead = next((k for k in death if k.startswith(f"{sur} {t.split()[0]}".upper())), None)
                    transfer = [x for x in INDEX if x["DOC_TYPE"].startswith("CERTIFICATE OF TRANSFER")]
                    if not transfer:
                        common.append(f"{sur} {t}" + (f", estate {death[dead][0]}" if dead else ""))
            continue
        nxt = deeds[i + 1]
        sur = r["GRANTEE"].split()[0]
        took = [g.strip() for g in r["GRANTEE"][len(sur):].split("&")]
        gave = [g.strip() for g in nxt["GRANTOR"][len(sur):].split("&")]
        for t in took:
            if t in gave:
                continue
            dead = next((k for k in death if k.startswith(f"{sur} {t}".upper().rstrip(".")[:len(sur) + 1 + len(t.split()[0])])), None)
            if nickname_read and len(gave) == len(took):
                continue            # the odd grantor is read as the same woman under a nickname
            surv.append(f"{sur} {t}" + (f", died {death[dead][1]:%m/%d/%Y}, estate {death[dead][0]}" if dead else ""))
    variance = "none"
    if nickname_read:
        variance = "affidavit of identity, Peggy A. Kessler and Margaret Ann Kessler"

    # ---------------------------------------------------------- dower (guideline 4.2)
    def ended(a, b):
        for row in DOMESTIC:
            if {row[2], row[3]} == {a, b}:
                if row[5].startswith("Decree"):
                    return row[0]
                if pending_case_terminates and row[5].startswith("Final hearing"):
                    return row[0]
        return None

    lorraine = None if decree_ignored else ended("PRUITT DANIEL R", "PRUITT LORRAINE K")
    lorraine_dower = ("terminated by decree %s" % lorraine) if lorraine else "release required"
    owner_full = names["Pruitt Daniel R"]
    spouse = "none of record"
    for r in PROBATE:
        if r[1] != "Marriage license":
            continue
        same = r[2] == owner_full or (same_initial_same_man and r[2].split()[:2] == owner_full.split()[:2]
                                      and r[2].split()[2][0] == owner_full.split()[2][0])
        if same and pdate(r[6]) > dt.date(2016, 11, 22):
            spouse = r[3]
    seller_spouse = "joins the deed" if ended("OKAFOR TAMSIN N", "OKAFOR EMEKA C") is None else "not required"

    # ---------------------------------------------------------- mortgages (guidelines 6.3, 10.5, 1.3)
    mortgages = [r for r in INDEX if r["DOC_TYPE"] == "MORTGAGE" and "L12" in describes(r["INSTRUMENT_NO"])]
    standing = {}
    for mtg in mortgages:
        no = mtg["INSTRUMENT_NO"]
        holder_of_record = [(pdate(mtg["RECORDED"]), mtg["GRANTEE"])]
        for a in INDEX:
            if a["DOC_TYPE"] == "ASSIGNMENT OF MORTGAGE" and BYVP.get(volpage_key(ABS[a["INSTRUMENT_NO"]])) == no:
                holder_of_record.append((ldate(ABS[a["INSTRUMENT_NO"]].split("Dated")[-1]), a["GRANTEE"]))
        state = "open"
        for sat in INDEX:
            if not sat["DOC_TYPE"].startswith("SATISFACTION"):
                continue
            target = sat["REF_INSTRUMENT"] if reference_by_index else BYVP.get(volpage_key(ABS[sat["INSTRUMENT_NO"]]))
            if target != no:
                continue
            signed = ldate(ABS[sat["INSTRUMENT_NO"]].split("Dated")[-1])
            holder_then = [h for d, h in sorted(holder_of_record) if d <= signed][-1]
            if sat["GRANTOR"] == holder_then or assignor_release_clears:
                state = "released by " + sat["INSTRUMENT_NO"]
            else:
                state = "open, satisfaction %s signed by the assignor" % sat["INSTRUMENT_NO"]
        if state.startswith("open"):
            matured = ldate(re.search(r"(final installment due|matures) ([A-Z][a-z]+ \d{1,2}, \d{4})", ABS[no]).group(2))
            as_of = CLOSING if insure_over_at_closing else COMMIT
            rec = pdate(mtg["RECORDED"])
            if dt.date(rec.year + 20, rec.month, rec.day) < as_of and (matured < as_of or maturity_ignored):
                state = "insured over"
        standing[no] = state
    requirements_mtg = [no for no, st in standing.items() if st.startswith("open")]
    ml_open = []
    for l in [r for r in INDEX if r["DOC_TYPE"] == "MECHANICS LIEN"]:
        rel = [x for x in INDEX if x["DOC_TYPE"].startswith("RELEASE") and x["GRANTOR"] == l["GRANTOR"]
               and (x["REF_INSTRUMENT"] if reference_by_index else BYVP.get(volpage_key(ABS[x["INSTRUMENT_NO"]]))) == l["INSTRUMENT_NO"]]
        if not rel:
            ml_open.append(l["INSTRUMENT_NO"])

    # ---------------------------------------------------------- judgment liens (guideline 7.4)
    jl, payoff = {}, {}
    for row in JL:
        no, filed, rendered, debtor = row[0], pdate(row[1]), pdate(row[2]), row[4]
        ents = [e for e in ENTRIES if e[0] == no]
        if any(e[2].startswith("Satisfaction") for e in ents):
            jl[no] = "satisfied"
            continue
        start = filed
        life_end = dt.date(filed.year + 5, filed.month, filed.day)
        first_life = life_end
        for e in sorted(ents, key=lambda e: pdate(e[1])):
            if e[2] == "Certificate of judgment refiled":
                when = pdate(e[1])
                within = when <= (first_life if chain_from_filing else life_end)
                if not (within or late_refile_renews):
                    start = when
                life_end = dt.date(when.year + 5, when.month, when.day)
        person = caption_name(row[5])
        hit = []
        for piece in PIECES:
            for name, d0, d1 in owners(piece):
                if name != debtor:
                    continue
                if names.get(name) != person and not same_initial_same_man:
                    continue
                end = d1 or dt.date(9999, 1, 1)
                if end >= start and not (lien_ends_at_conveyance and d1 is not None):
                    hit.append(piece)
        if dower_is_title and debtor == "Okafor Emeka C":
            hit.append("L12")
        if not hit:
            jl[no] = "does not attach"
        elif life_end < CLOSING and not lapsed_in_force:
            jl[no] = "lapsed"
        else:
            jl[no] = "in force on " + "+".join(p for p in PIECES if p in hit)
            principal, costs = D(str(row[6])), D(str(row[7]))
            rate = D(row[8].split("%")[0]) / 100
            d0 = filed if interest_from_filing else rendered
            interest = D(0)          # interest paid or still due, in all
            unpaid_int = D(0)        # accrued and not covered by a credit
            for e in sorted(ents, key=lambda e: pdate(e[1])):
                vacated = any(x[2].startswith("Credit of " + e[1]) for x in ents)
                if e[2].endswith("credited") and not payment_ignored and (vacated_credit_applied or not vacated):
                    accrued = c(principal * rate * (pdate(e[1]) - d0).days / year_days)
                    interest += accrued
                    amt = D(str(e[3]))
                    if credits_to_principal:
                        principal -= amt
                    else:
                        to_int = min(amt, unpaid_int + accrued)
                        unpaid_int = unpaid_int + accrued - to_int
                        principal -= amt - to_int
                    d0 = pdate(e[1])
            n = (CLOSING - d0).days + (1 if inclusive_days else 0)
            interest += c(principal * rate * n / year_days)
            if credits_to_principal:
                payoff[no] = (principal, interest, costs, principal + interest + costs)
            else:
                paid_int = interest - unpaid_int - c(principal * rate * n / year_days)
                payoff[no] = (principal, interest, costs, principal + (interest - paid_int) + costs)

    # ---------------------------------------------------------- taxes (guideline 9.2)
    pen = D(penalty)
    due = D(0)
    late = D(0)
    short = D(0)
    for r in TAX:
        gross, net, assess, billed, paid, status = D(str(r[3])), D(str(r[5])), D(str(r[6])), D(str(r[7])), D(str(r[8])), r[10]
        if status == "Unpaid":
            due += net + c(net * pen) + assess + c(assess * pen)
        elif pdate(r[9]) > pdate(r[2]) and not late_payment_missed:
            days_late = (pdate(r[9]) - pdate(r[2])).days
            charge = c(billed * (D("0.05") if days_late <= 10 else D("0.10")))
            late += billed + charge - paid
        elif paid < billed and not short_payment_missed:
            short += (billed - paid) + c((billed - paid) * D("0.10"))
    last = max(r[0] for r in TAX)
    annual = sum((D(str(r[3] if proration_on_gross else r[5])) for r in TAX if r[0] == last), D(0))
    if prorate_assessment:
        annual += sum((D(str(r[6])) for r in TAX if r[0] == last), D(0))
    days = (CLOSING - dt.date(CLOSING.year, 1, 1)).days + (1 if proration_through_closing else 0)
    credit = c(annual * days / 365)

    # ---------------------------------------------------------- the survey against the restrictions
    sv = survey_rows()
    full = D(re.search(r"\((\d+\.\d\d)\) feet", ABS["200303070115"]).group(1))
    part = full if description_skimmed else D(re.search(r"\((\d+\.\d\d)\) feet", ABS["201409190112"]).group(1))
    tract_south = LOT_WIDTH + full
    title_south = LOT_WIDTH + part
    porch = sv["Roofed front porch"]
    garage = sv["Detached frame garage"]
    shed = sv["Frame storage shed"]
    house = sv["Dwelling"]
    wall = house if porch_ignored else porch
    over_line = max(D(0), D(30) - wall[3])
    lots = int(re.search(r"all (\d+) lots", ABS["198611030018"]).group(1))
    signed = int(re.search(r"owners of (\d+) lots", ABS["202506120087"]).group(1))
    need = -(-2 * lots // 3)
    amendment = "effective" if (signed >= need or amendment_counted_loosely) else "short of two-thirds, %d of %d lots" % (signed, lots)
    if amendment == "effective":
        over_line = D(0)

    garage_clear = tract_south - (garage[2] + garage[0])
    shed_rear = LOT_DEPTH - (shed[3] + shed[1])
    shed_in = max(D(0), D(10) - shed_rear)
    garage_on = "on the strip" if garage[2] >= title_south else "on the seller's land"

    figures = {
        "lots needed to amend": str(need),
        "seller's record line, feet south": str(title_south),
        "porch over the building line, feet": str(over_line),
        "garage to the south line, feet": str(garage_clear),
        "shed inside the rear easement, feet": str(shed_in),
        "omitted strip, feet": str(strip_feet()),
        "annual tax estimate": money(annual),
        "proration days": str(days),
        "seller tax credit": money(credit),
        "second-half 2025 with penalty": money(due),
        "penalty open on the first half": money(late),
        "unpaid on the installment paid short, with penalty": money(short),
        "delinquent taxes and penalty": money(due + late + short),
    }
    for no, (pr, i, co, tot) in payoff.items():
        figures[no + " principal"] = money(pr)
        figures[no + " interest"] = money(i)
        figures[no + " payoff"] = money(tot)
    figures["judgment payoffs, total"] = money(sum((v[3] for v in payoff.values()), D(0)))
    figures["of record to clear, total"] = money(sum((v[3] for v in payoff.values()), D(0)) + due + late + short)

    standings = {
        "garage and driveway": garage_on,
        "2025 amendment of the restrictions": amendment,
        "undivided share with no transfer of record": "; ".join(common) or "none",
        "front building line": ("porch %s feet over" % over_line) if over_line else "clear",
        "deed omitting part of Lot 13": gap or "none",
        "record owner of the omitted strip": holder["STRIP"],
        "survivorship tenants with no death of record": "; ".join(surv) or "none",
        "name variance": variance,
        "dower of Lorraine K. Pruitt": lorraine_dower,
        "spouse of the strip's owner": spouse,
        "seller's spouse": seller_spouse,
        "open mechanics liens": ",".join(ml_open) or "none",
        "mortgage requirements": ",".join(requirements_mtg),
        "delinquent taxes and penalty": figures["delinquent taxes and penalty"],
        "seller tax credit": figures["seller tax credit"],
        "of record to clear, total": figures["of record to clear, total"],
    }
    for no, st in standing.items():
        standings["mortgage " + no] = st
    for no, st in jl.items():
        standings[no] = st
    for no in ("10JL00227", "16JL00541", "17JL00288", "22JL00151", "23JL00644", "25JL01133"):
        standings[no + " payoff"] = figures.get(no + " payoff", "none")
    return figures, standings


# name -> (keyword overrides, the phrase the report states to settle it)
VARIANTS = {
    "every two-name deed read as a survivorship deed": ({"all_survivorship": True}, "no words of survivorship"),
    "the vacated August credit applied to the payoff": ({"vacated_credit_applied": True}, "vacated on August 31, 2026"),
    "25 of 38 lots read as two-thirds": ({"amendment_counted_loosely": True}, "fewer than the 26"),
    "the building line measured to the main wall only": ({"porch_ignored": True}, "Roofed front porch"),
    "the 2014 description read as the same as the others": ({"description_skimmed": True}, "24.25 feet"),
    "a same-initial namesake read as the owner": ({"same_initial_same_man": True}, "Daniel Robert Pruitt"),
    "Peggy read as a nickname for Margaret Ann": ({"nickname_read": True}, "two different women"),
    "the index reference column read in place of the satisfaction": ({"reference_by_index": True}, "by book and page"),
    "a satisfaction signed by the assignor taken as a release": ({"assignor_release_clears": True}, "no longer held the mortgage of record"),
    "the twenty years measured to the closing date": ({"insure_over_at_closing": True}, "fewer than twenty years before the commitment date"),
    "a certificate refiled late read as a renewal": ({"late_refile_renews": True}, "after the five years had run"),
    "a lien read as ending when the debtor conveyed": ({"lien_ends_at_conveyance": True}, "remains on the parcel after the debtor conveys"),
    "the docket payment left out of the payoff": ({"payment_ignored": True}, "A payment or garnishment the docket credits"),
    "interest run from the filing date": ({"interest_from_filing": True}, "from the date the judgment was rendered"),
    "interest days counted inclusively": ({"inclusive_days": True}, "counting the closing date and not the starting date"),
    "interest on a 360-day year": ({"year_days": 360}, "365-day year"),
    "the late first-half payment read as paid in full": ({"late_payment_missed": True}, "six days after its due date"),
    "penalty at 5% on the unpaid installment": ({"penalty": "0.05"}, "10% penalty"),
    "proration to the day before closing": ({"proration_through_closing": False}, "through the day of closing"),
    "special assessment prorated with the tax": ({"prorate_assessment": True}, "The special assessment is not prorated"),
    "a pending divorce read as ending dower": ({"pending_case_terminates": True}, "a pending case is not a decree"),
    "the dissolution decree overlooked": ({"decree_ignored": True}, "terminated by the decree of dissolution"),
    "a spouse's dower read as record title": ({"dower_is_title": True}, "inchoate dower is not record title"),
    "the maturity test skipped on a mortgage older than twenty years": ({"maturity_ignored": True}, "its stated maturity has not passed"),
    "a certificate never refiled read as still in force": ({"lapsed_in_force": True}, "with no refiling"),
    "every refiling measured from the first filing": ({"chain_from_filing": True}, "each refiling inside the five years from the one before it"),
    "a docket credit taken off principal with the interest untouched": ({"credits_to_principal": True}, "goes first to the interest accrued"),
    "the installment paid short read as paid": ({"short_payment_missed": True}, "has stood unpaid since its due date"),
    "the proration run on the gross tax": ({"proration_on_gross": True}, "after the rollback credits"),
}

EXPECTED = {
    "lots needed to amend": "26",
    "seller's record line, feet south": "108.75",
    "porch over the building line, feet": "3.30",
    "garage to the south line, feet": "1.55",
    "shed inside the rear easement, feet": "3.50",
    "omitted strip, feet": "18.00",
    "annual tax estimate": "3,143.28",
    "proration days": "310",
    "seller tax credit": "2,669.64",
    "second-half 2025 with penalty": "2,072.55",
    "penalty open on the first half": "94.21",
    "unpaid on the installment paid short, with penalty": "175.91",
    "delinquent taxes and penalty": "2,342.67",
    "10JL00227 principal": "4,318.55",
    "10JL00227 interest": "2,886.92",
    "10JL00227 payoff": "6,329.47",
    "17JL00288 interest": "2,276.38",
    "17JL00288 payoff": "8,543.78",
    "23JL00644 interest": "687.06",
    "23JL00644 payoff": "4,724.26",
    "25JL01133 principal": "5,752.23",
    "25JL01133 interest": "794.07",
    "25JL01133 payoff": "6,243.07",
    "judgment payoffs, total": "25,840.58",
    "of record to clear, total": "28,183.25",
}
EXPECTED_STANDINGS = {
    "garage and driveway": "on the strip",
    "front building line": "porch 3.30 feet over",
    "deed omitting part of Lot 13": "201409190112",
    "record owner of the omitted strip": "Pruitt Daniel R",
    "survivorship tenants with no death of record": "Kessler Margaret Ann, died 03/08/2015, estate 15ES0388",
    "undivided share with no transfer of record": "Voss Mildred J, estate 01ES0117",
    "2025 amendment of the restrictions": "short of two-thirds, 25 of 38 lots",
    "name variance": "none",
    "dower of Lorraine K. Pruitt": "terminated by decree 16DR0842",
    "spouse of the strip's owner": "none of record",
    "seller's spouse": "joins the deed",
    "open mechanics liens": "202307210033",
    "mortgage requirements": "199907160122,200610190027,201103140062,201805040072",
    "mortgage 198705120042": "released by 199808210077",
    "mortgage 199907160122": "open",
    "mortgage 199409220103": "insured over",
    "mortgage 200303070116": "released by 201106020188",
    "mortgage 200610190027": "open",
    "mortgage 201103140062": "open, satisfaction 201410060131 signed by the assignor",
    "mortgage 201409190113": "released by 201804270239",
    "mortgage 201805040072": "open",
    "10JL00227": "in force on L12+N24+STRIP",
    "11JL00318": "does not attach",
    "12JL00655": "satisfied",
    "15JL00932": "does not attach",
    "16JL00541": "lapsed",
    "17JL00288": "in force on L12+N24",
    "20JL00417": "does not attach",
    "22JL00151": "does not attach",
    "23JL00644": "in force on STRIP",
    "24JL00902": "does not attach",
    "25JL01133": "in force on L12+N24",
}

if __name__ == "__main__":
    rep = Report()
    figures, standings = derive()
    if "-v" in sys.argv:
        for k, v in {**figures, **standings}.items():
            print(f"{k}: {v}", file=sys.stderr)
    for label, golden in EXPECTED.items():
        rep.expect(label, figures.get(label), golden)
    for label, golden in EXPECTED_STANDINGS.items():
        rep.expect(label, standings.get(label), golden)
    rep.sensitivity(lambda **kw: derive(**kw)[1], VARIANTS)
    rep.finish()
