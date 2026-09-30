"""verify_golden.py for concrete-acceptance-review: re-derive every figure the summary states from inputs/ alone
under the specification and the laboratory procedure, and list the alternate readings a solver could take, each with
the phrase the golden uses to settle it. Every variant below is one missed read, and each moves a graded figure.

    .venv/bin/python submissions/09-concrete-acceptance-review/verify_golden.py
    .venv/bin/python submissions/09-concrete-acceptance-review/verify_golden.py --print
"""
import os
import sys

import csv
import math
import re
from datetime import datetime
from decimal import Decimal as D, ROUND_HALF_UP
from pathlib import Path

from docx import Document

FC = {"M-4000": 4000, "M-6000": 6000}
REQUIRED = {"6x12": 2, "4x8": 3}
RANGE_LIMIT = {"6x12": D("0.066"), "4x8": D("0.106")}
FRESH = {"M-4000": (D("3"), D("5"), D("4.5"), D("7.5"), 90), "M-6000": (D("5"), D("7"), D("2.0"), D("4.0"), 90)}
MONTHS = {"August": "08", "September": "09", "July": "07", "October": "10"}


def r10(x):
    return int((D(str(x)) / 10).quantize(D(1), rounding=ROUND_HALF_UP) * 10)


def stamp(date, time):
    return datetime.strptime(f"{date} {time}", "%m/%d/%Y %H:%M")


def load(inputs):
    inputs = Path(inputs)
    rd = lambda n: list(csv.DictReader(open(inputs / n, newline="", encoding="utf-8-sig")))
    field, breaks, places = rd("field_sampling_log_2417.csv"), rd("cylinder_breaks_2417.csv"), rd("placement_log_2417.csv")
    spec = Document(inputs / "spec_033000_excerpt.docx")
    mixmap = {}
    for row in spec.tables[0].rows[1:]:
        cells = [c.text.strip() for c in row.cells]
        mixmap[cells[-1]] = cells[0]
    corr = [p.text for p in Document(inputs / "project_correspondence_2417.docx").paragraphs]
    july = Document(inputs / "july_summary_transmittal_2417.docx")
    carry = {}
    for mix, tb in zip(("M-4000", "M-6000"), july.tables):
        rows = [[c.text.strip() for c in r.cells] for r in tb.rows[1:]]
        carry[mix] = dict(used=[int(r[3].replace(",", "")) for r in rows if r[5].startswith("Used")][-2:],
                          last_rows=[int(re.match(r"[\d,]+", r[3]).group(0).replace(",", "")) for r in rows][-2:])
    # a later correction to a July test governs the figure printed in the July tables
    july_sets = {mix: [r.cells[0].text.strip() for r in tb.rows[1:] if r.cells[5].text.strip().startswith("Used")][-2:]
                 for mix, tb in zip(("M-4000", "M-6000"), july.tables)}
    for mix in carry:
        carry[mix]["printed"] = list(carry[mix]["used"])
        carry[mix]["sets"] = july_sets[mix]
    for p in corr:
        m = re.search(r"corrected strength test for (S-\d+) is ([\d,]+) psi", p)
        if m:
            for mix in carry:
                if m.group(1) in july_sets[mix]:
                    carry[mix]["used"][july_sets[mix].index(m.group(1))] = int(m.group(2).replace(",", ""))
    # the engineer's written direction: a paragraph that directs a result be set aside
    directed = []
    for i, p in enumerate(corr):
        if re.search(r"\bI direct\b.*\bset aside\b", p):
            ctx = " ".join(corr[max(0, i - 3):i + 1])
            m = re.search(r"cast on (August|September) (\d+) from the (.+?) placement", ctx)
            directed.append((f"{MONTHS[m.group(1)]}/{int(m.group(2)):02d}/2026", m.group(3)))
    return dict(field=field, breaks=breaks, places=places, mixmap=mixmap, carry=carry, directed=directed)


ABBR = [(r"\bL(\d)\b", r"Level \1"), (r"\bCols\b", "Columns"), (r"C/D", "bays C and D"), (r"grid (\d+)-(\d+)", r"grid \1 to \2"),
        (r"South ramp", "Ramp slab south"), (r"North ramp", "Ramp slab north"), (r"Stair (\d) shear walls", r"Shear walls stair \1")]


def words(t):
    for a, b in ABBR:
        t = re.sub(a, b, t)
    return set(re.findall(r"[a-z0-9]+", t.lower())) - {"at", "pump", "bucket", "chute", "and", "to", "north", "south"} | (
        {"north"} if "Ramp slab north" in t else set()) | ({"south"} if "Ramp slab south" in t else set())


def match_placement(row, places, reconcile=True):
    """the placement a set was molded from: same mixture, the element its location names; the date on the field
    log is checked against the placement log, which the memo's list of Saturday placements bears out"""
    w = words(row["LOCATION"])
    same_day = [p for p in places if p["DATE"] == row["DATE_CAST"] and p["MIX_DESIGN"] == row["MIX_DESIGN"]]
    if same_day:
        return max(same_day, key=lambda p: len(w & words(p["ELEMENT"])))
    near = [p for p in places if p["MIX_DESIGN"] == row["MIX_DESIGN"]
            and abs((datetime.strptime(p["DATE"], "%m/%d/%Y") - datetime.strptime(row["DATE_CAST"], "%m/%d/%Y")).days) <= 3]
    return max(near, key=lambda p: len(w & words(p["ELEMENT"])))


def clock(t, lo=None, hi=None, as_typed=False):
    """a time as the technician wrote it; an entry on the 12 hour clock is read into the window it must fall in"""
    h, m = [int(x) for x in t.split(":")]
    if as_typed or (len(t.split(":")[0]) == 2 and t[0] == "0") or h >= 13:
        return h, m
    cands = [(h, m), ((h + 12) % 24, m)] if h != 12 else [(12, m), (0, m)]
    if lo is not None:
        inside = [c for c in cands if lo <= c <= hi]
        if inside:
            return inside[0]
    return cands[0]


def derive(data, age="hours", defects=True, combine=True, field_cured_out=True, engineer=True, contractor_void=False,
           order="time", carry="used", clock_as_typed=False, group="batch", cast_date="reconciled", box="either", area="measured", sampling="day", sampling_counts="tests", b_rule="spec",
           a_equal_meets=True, pi=math.pi, avg_dia_places=None):
    field = {r["SET_NO"]: r for r in data["field"]}
    places = data["places"]
    mix_of = data["mixmap"]
    sets = {}
    for b in data["breaks"]:
        sid = b["SET_NO"]
        f = dict(field[sid])
        pl = match_placement(f, places)
        if cast_date == "reconciled":
            f["DATE_CAST"] = pl["DATE"]
        hm = lambda t: tuple(int(x) for x in t.split(":"))
        mh, mm = clock(f["TIME_MOLDED"], hm(pl["START"]), hm(pl["FINISH"]), clock_as_typed)
        f["TIME_MOLDED"] = "%02d:%02d" % (mh, mm)
        bh, bm = clock(f["BATCH_TIME"], (max(mh - 3, 0), 0), (mh, mm), clock_as_typed)
        f["BATCH_TIME"] = "%02d:%02d" % (bh, bm)
        pd_, pt_ = f["PICKED_UP"].split(" ")
        ph, pm_ = clock(pt_, (5, 30), (19, 0), clock_as_typed)
        f["PICKED_UP"] = "%s %02d:%02d" % (pd_, ph, pm_)
        if f["BOX_TEMPS_F"]:
            t1, t2 = [int(x) for x in f["BOX_TEMPS_F"].split("/")]
            f["BOX_MIN_F"], f["BOX_MAX_F"] = (min(t1, t2), max(t1, t2)) if box == "either" else (t1, t2)
        else:
            f["BOX_MIN_F"] = f["BOX_MAX_F"] = ""
        molded = stamp(f["DATE_CAST"], f["TIME_MOLDED"])
        remark = b["REMARKS"]
        cyls = []
        for m in "ABCDE":
            if not b[f"{m}_TEST_DATE"]:
                continue
            d1, d2 = D(b[f"{m}_DIA1_IN"]), D(b[f"{m}_DIA2_IN"])
            avg = (d1 + d2) / 2
            if avg_dia_places is not None:
                avg = avg.quantize(D(1).scaleb(-avg_dia_places), rounding=ROUND_HALF_UP)
            if area == "measured":
                a = pi * float(avg) ** 2 / 4
            else:
                a = 28.27 if b["CYL_SIZE"] == "6x12" else 12.57
            strength = r10(int(b[f"{m}_MAX_LOAD_LBF"]) / a)
            broke = stamp(b[f"{m}_TEST_DATE"], b[f"{m}_TEST_TIME"])
            hours = (broke - molded).total_seconds() / 3600
            datediff = (broke.date() - molded.date()).days
            if age == "hours":
                at28 = abs(hours - 672) <= 20
            elif age == "dates":
                at28 = datediff == 28
            else:  # "within a day of its date"
                at28 = abs(datediff - 28) <= 1
            # a defect recorded on the break record at the time of the test, named by cylinder letter
            defect = bool(re.search(rf"Cyl {m}: ", remark)) and "No defect" not in remark
            hours2 = D(str(round(hours * 100))) / 100
            days2 = (hours2 / 24).quantize(D("0.01"), rounding=ROUND_HALF_UP)
            cyls.append(dict(mark=m, strength=strength, hours=hours, days=hours / 24, days2=days2, at28=at28, defect=defect,
                             fract=b[f"{m}_FRACTURE"], datediff=datediff))
        standard = f["INITIAL_CURING"].startswith("Box")
        mix = mix_of[f["MIX_DESIGN"]]
        hrs_box = None
        if standard:
            hrs_box = (datetime.strptime(f["PICKED_UP"], "%m/%d/%Y %H:%M") - molded).total_seconds() / 3600
        temp_exc = bool(standard and (int(f["BOX_MIN_F"]) < 60 or int(f["BOX_MAX_F"]) > 80))
        long_box = standard and hrs_box > 48
        fr = FRESH[mix]
        fresh_out = not (fr[0] <= D(f["SLUMP_IN"]) <= fr[1] and fr[2] <= D(f["AIR_PCT"]) <= fr[3] and int(f["CONC_TEMP_F"]) <= fr[4])
        sets[sid] = dict(set=sid, mix=mix, size=b["CYL_SIZE"], ticket=f["TICKET_NO"], molded=molded, cyls=cyls, standard=standard,
                         placement=pl["PLACEMENT_ID"], truck=f["TRUCK"], batch=f["BATCH_TIME"], box_min=f["BOX_MIN_F"], box_max=f["BOX_MAX_F"],
                         pickup=f["PICKED_UP"], temp_exc=temp_exc, long_box=long_box, hrs_box=hrs_box,
                         fresh_out=fresh_out, date=f["DATE_CAST"], loc=f["LOCATION"])
    # the engineer's direction lands on the deck sample cast that day from the named placement
    for date, element in data["directed"]:
        for s in sets.values():
            if s["date"] == date and s["mix"] == "M-4000" and words(element) <= words(s["loc"]) | {"deck"}:
                s["directed"] = True
    # samples: one per delivery ticket
    groups = {}
    for sid in sorted(sets):
        s = sets[sid]
        # one batch is one truck loaded at one time on one day, whatever ticket number was written down
        key = (s["date"], s["truck"], s["batch"]) if group == "batch" else s["ticket"]
        key = key if combine else sid
        groups.setdefault(key, []).append(s)
    tests = []
    for key, members in groups.items():
        members.sort(key=lambda s: s["molded"])
        first = members[0]
        for s_ in members:
            s_["batch_ticket"] = first["ticket"]
        std = [s for s in members if s["standard"] or not field_cured_out]
        entering = [c["strength"] for s in std for c in s["cyls"] if c["at28"] and not (defects and c["defect"])]
        near28 = [c for s in members for c in s["cyls"] if 25 <= c["days"] <= 31]
        info = [c["strength"] for c in near28 if not (defects and c["defect"])]
        required = REQUIRED[first["size"]]
        t = dict(key=first["ticket"], sets=[s["set"] for s in members], mix=first["mix"], placement=first["placement"], molded=first["molded"],
                 size=first["size"], n=len(entering), required=required, date=first["date"],
                 temp_exc=any(s["temp_exc"] for s in members), long_box=any(s["long_box"] for s in members),
                 fresh_out=first["fresh_out"], directed=any(s.get("directed") for s in members))
        t["field_cured"] = not any(s["standard"] for s in members)
        if t["field_cured"] and field_cured_out:
            t["used"], t["reason"] = False, "Field cured"
        elif not any(c["at28"] for s in std for c in s["cyls"]):
            t["used"], t["reason"] = False, "Outside the age tolerance"
        elif len(entering) < required:
            t["used"], t["reason"] = False, "Incomplete test"
        elif engineer and t["directed"]:
            t["used"], t["reason"] = False, "Set aside by the engineer"
        elif contractor_void and first["set"] == "S-105":
            t["used"], t["reason"] = False, "Voided at the contractor's request"
        else:
            t["used"], t["reason"] = True, ""
        vals = entering if len(entering) >= 1 and (t["used"] or t["reason"] in ("Set aside by the engineer", "Incomplete test", "Voided at the contractor's request")) else info
        t["value"] = r10(D(sum(vals)) / len(vals)) if vals else None
        if vals:
            t["low"], t["high"] = min(vals), max(vals)
            t["range"] = (D(max(vals) - min(vals)) / D(t["value"])).quantize(D("0.0001"), rounding=ROUND_HALF_UP)
            t["range_note"] = t["used"] and t["range"] > RANGE_LIMIT[t["size"]]
        t["age_days"] = [round(c["days"], 2) for c in near28]
        tests.append(t)
    keyf = (lambda t: (t["molded"],)) if order == "time" else (lambda t: (t["molded"].date(), t["sets"][0]))
    tests.sort(key=keyf)
    out = dict(tests=tests, sets=sets, mix={})
    for mix, fc in FC.items():
        seq = [("carry", v) for v in (data["carry"][mix][carry] if carry in ("used", "last_rows", "printed") else [])]
        used = [t for t in tests if t["mix"] == mix and t["used"]]
        allow = (500 if fc <= 5000 else fc // 10) if b_rule == "spec" else 500
        vals = [v for _, v in seq]
        a_fail, b_fail, movs = [], [], {}
        for t in used:
            vals.append(t["value"])
            if t["value"] < fc - allow:
                b_fail.append(t)
            if len(vals) >= 3:
                m = (D(sum(vals[-3:])) / 3).quantize(D("0.1"), rounding=ROUND_HALF_UP)
                movs[t["key"]] = m
                if m < fc or (not a_equal_meets and m == fc):
                    a_fail.append(t)
        not_used = [t for t in tests if t["mix"] == mix and not t["used"]]
        out["mix"][mix] = dict(used=used, a_fail=a_fail, b_fail=b_fail, movs=movs, not_used=not_used, allow=allow,
                               lowest=min(t["value"] for t in used),
                               status="Meets 3.11.1" if not a_fail and not b_fail else "Does not meet 3.11.1")
    # sampling by mixture and day
    days = {}
    for p in places:
        k = (p["DATE"], mix_of[p["MIX_DESIGN"]]) if sampling == "day" else (p["DATE"], mix_of[p["MIX_DESIGN"]], p["PLACEMENT_ID"])
        dd = days.setdefault(k, dict(cy=0, area=0, placements=[]))
        dd["cy"] += int(p["CUBIC_YARDS"])
        dd["area"] += int(p["SURFACE_AREA_SF"] or 0)
        dd["placements"].append(p["PLACEMENT_ID"])
    for k, dd in days.items():
        dd["required"] = max(1, math.ceil(dd["cy"] / 150), math.ceil(dd["area"] / 5000))
        mine = [t for t in tests if t["date"] == k[0] and t["mix"] == k[1] and (len(k) == 2 or t["placement"] == k[2])]
        if sampling_counts == "tests":
            dd["have"] = sum(1 for t in mine if t["used"])
        else:
            dd["have"] = sum(len(t["sets"]) for t in mine)
        dd["taken"] = len(mine)
        dd["short"] = dd["have"] < dd["required"]
    out["days"] = days
    return out


def standing(o):
    s = {}
    for mix, m in o["mix"].items():
        s[f"{mix} tests used"] = len(m["used"])
        s[f"{mix} sets not used"] = sum(len(t["sets"]) for t in m["not_used"])
        s[f"{mix} lowest test"] = m["lowest"]
        s[f"{mix} criterion (a) failures"] = len(m["a_fail"])
        s[f"{mix} criterion (b) failures"] = len(m["b_fail"])
        s[f"{mix} criterion (b) placements"] = " ".join(t["placement"] for t in m["b_fail"])
        s[f"{mix} lowest moving average"] = str(min(m["movs"].values()))
        s[f"{mix} status"] = m["status"]
    short = sorted(k for k, d in o["days"].items() if d["short"])
    s["sampling short count"] = len(short)
    s["sampling short list"] = " ".join("/".join(k) for k in short)
    used = [t for t in o["tests"] if t["used"]]
    s["range notes"] = sum(1 for t in used if t.get("range_note"))
    s["curing notes on tests used"] = sum(1 for t in used if t["temp_exc"] or t["long_box"])
    s["fresh outside"] = sum(1 for t in o["tests"] if t["fresh_out"])
    return s


VARIANT_KW = {
    "every time on the field log read on the 24 hour clock as typed": dict(clock_as_typed=True),
    "sets grouped by the ticket number as typed": dict(group="ticket"),
    "cast date taken as typed against the placement log": dict(cast_date="typed"),
    "box thermometer read low first on every line": dict(box="low_first"),
    "July tests carried as printed, without the correction": dict(carry="printed"),
    "age judged on calendar dates, 28 days to the day": dict(age="dates"),
    "age accepted within a day of the date": dict(age="day"),
    "a cylinder with a recorded defect kept in the test": dict(defects=False),
    "sets from one delivery ticket counted as separate tests": dict(combine=False),
    "field cured cylinders counted as a strength test": dict(field_cured_out=False),
    "the engineer's written direction not applied": dict(engineer=False),
    "the contractor's request to void a set honoured": dict(contractor_void=True),
    "tests ordered by set number within a day": dict(order="setno"),
    "moving averages started fresh in August": dict(carry="none"),
    "last two rows of the July tables carried": dict(carry="last_rows"),
    "nominal areas of 28.27 and 12.57 square inches": dict(area="nominal"),
    "sampling judged placement by placement": dict(sampling="placement"),
    "sampling judged on sets cast": dict(sampling_counts="sets"),
    "500 psi allowance applied to both mixtures": dict(b_rule="500"),
    "an average equal to f'c counted as failing": dict(a_equal_meets=False),
    "pi taken as 3.14": dict(pi=3.14),
    "average diameter rounded to 0.01 inch": dict(avg_dia_places=2),
}


CONVENTION = {
    "every time on the field log read on the 24 hour clock as typed": "each time is read into the hours the placement log gives for the placement",
    "sets grouped by the ticket number as typed": "one truck batched at one time is one delivery ticket whatever number was written on the line",
    "cast date taken as typed against the placement log": "The cast date of a set is the date the placement log gives for the placement it was molded from",
    "box thermometer read low first on every line": "The box thermometer is read as a low and a high, whichever was written first",
    "July tests carried as printed, without the correction": "as corrected by the laboratory's letter of September 15",
    "age judged on calendar dates, 28 days to the day": "within 20 hours of 672 hours",
    "age accepted within a day of the date": "within 20 hours of 672 hours",
    "a cylinder with a recorded defect kept in the test": "A cylinder with a defect written on the break record is discarded",
    "sets from one delivery ticket counted as separate tests": "Sets molded from one delivery ticket are one sample",
    "field cured cylinders counted as a strength test": "Field cured cylinders are reported apart",
    "the engineer's written direction not applied": "only on the written direction of the engineer of record",
    "the contractor's request to void a set honoured": "only on the written direction of the engineer of record",
    "tests ordered by set number within a day": "in the order their samples were molded, by date and time",
    "moving averages started fresh in August": "take in the last two July tests used for acceptance",
    "last two rows of the July tables carried": "take in the last two July tests used for acceptance",
    "nominal areas of 28.27 and 12.57 square inches": "the average of the two measured diameters",
    "sampling judged placement by placement": "the day's total of each mixture across every placement of the day",
    "sampling judged on sets cast": "met only by strength tests used for acceptance",
    "500 psi allowance applied to both mixtures": "The 10 percent allowance of criterion (b) applies to M-6000",
    "an average equal to f'c counted as failing": "A moving average equal to f'c meets criterion (a)",
    "pi taken as 3.14": "with pi carried in full",
    "average diameter rounded to 0.01 inch": "the average diameter carried without rounding",
}

HERE = Path(__file__).resolve().parent
ROOT = os.environ.get("HAZY_ROOT") or next(str(p) for p in HERE.parents if (p / "tools" / "golden_verify.py").is_file())
sys.path.insert(0, os.path.join(ROOT, "tools"))
from golden_verify import Report  # noqa: E402

INPUTS = HERE / "inputs"
GOLDEN = HERE / "solution" / "acceptance_summary_2417_aug_sep.xlsx"

if __name__ == "__main__":
    import openpyxl
    data = load(INPUTS)
    o = derive(data)
    base = standing(o)
    if "--print" in sys.argv:
        for k, v in base.items():
            print(k, "=", v)
        for name, kw in VARIANT_KW.items():
            alt = standing(derive(data, **kw))
            print("VARIANT", name, "->", {k: (base[k], alt[k]) for k in base if base[k] != alt[k]} or "no graded figure moves")
        sys.exit(0)
    wb = openpyxl.load_workbook(GOLDEN, data_only=True)
    rep = Report()
    s = wb["Summary"]
    summ = {s.cell(row=r, column=1).value: (s.cell(row=r, column=2).value, s.cell(row=r, column=3).value)
            for r in range(1, 40) if s.cell(row=r, column=1).value}
    one = lambda v: str(D(str(v)).quantize(D("0.1")))
    for j, mix in enumerate(("M-4000", "M-6000")):
        m = o["mix"][mix]
        rep.expect(f"{mix} tests used", base[f"{mix} tests used"], summ["Strength tests used for acceptance"][j])
        rep.expect(f"{mix} sets not used", base[f"{mix} sets not used"], summ["Sets cast and not used for acceptance"][j])
        rep.expect(f"{mix} lowest test", base[f"{mix} lowest test"], summ["Lowest strength test (psi)"][j])
        rep.expect(f"{mix} a failures", base[f"{mix} criterion (a) failures"], summ["Moving averages of three below f'c, criterion (a)"][j])
        rep.expect(f"{mix} lowest moving average", base[f"{mix} lowest moving average"], one(summ["Lowest moving average of three (psi)"][j]))
        rep.expect(f"{mix} b failures", base[f"{mix} criterion (b) failures"], summ["Tests below f'c by more than the allowance, criterion (b)"][j])
        rep.expect(f"{mix} b placements", base[f"{mix} criterion (b) placements"] or "None", summ["Placements with a test failing criterion (b)"][j])
        rep.expect(f"{mix} status", base[f"{mix} status"], summ["Acceptance under 3.11.1"][j])
        rep.expect(f"{mix} core average floor", int(FC[mix] * 0.85), summ["Core average floor, 85 percent of f'c (psi)"][j])
        rep.expect(f"{mix} core single floor", int(FC[mix] * 0.75), summ["Core single floor, 75 percent of f'c (psi)"][j])
        nxt = summ["What 3.11.2 calls for next"][j]
        rep.expect(f"{mix} next step names investigation", bool(m["b_fail"]), "investigates under ACI 318-19 section 26.12.6" in nxt)
        rep.expect(f"{mix} next step names the average", bool(m["a_fail"]), "increase the average" in nxt)
    short = sorted((k for k, d in o["days"].items() if d["short"]), key=lambda k: (k[0][6:] + k[0][:5], k[1]))
    rep.expect("sampling short count", len(short), summ["Days on which a mixture was sampled short of 3.10.1"][0])
    rep.expect("sampling short list", "; ".join(f"{d[:5]} {mix}" for d, mix in short), summ["Days short, listed"][0])
    rep.expect("sets not used, both", sum(len(t["sets"]) for t in o["tests"] if not t["used"]), summ["Sets cast and not used, both mixtures"][0])
    rep.expect("range notes", base["range notes"], summ["Tests with a within-test range note"][0])
    rep.expect("curing notes on tests used", base["curing notes on tests used"], summ["Tests used that carry a curing note"][0])
    rep.expect("fresh outside", base["fresh outside"], summ["Samples outside a fresh concrete limit"][0])
    rep.expect("cylinders on the record", sum(len(x["cyls"]) for x in o["sets"].values()), summ["Cylinders on the break record"][0])

    def table(ws, hdr_row=3):
        hdr = {ws.cell(row=hdr_row, column=c).value: c for c in range(1, ws.max_column + 1) if ws.cell(row=hdr_row, column=c).value}
        rows = []
        for r in range(hdr_row + 1, ws.max_row + 1):
            if ws.cell(row=r, column=1).value is None:
                break
            rows.append({h: ws.cell(row=r, column=c).value for h, c in hdr.items()})
        return rows

    cyl = {r["CYLINDER"]: r for r in table(wb["Cylinders"])}
    for sid, x in o["sets"].items():
        for c in x["cyls"]:
            g = cyl[f"{sid}-{c['mark']}"]
            rep.expect(f"{sid}-{c['mark']} strength", c["strength"], g["STRENGTH_PSI"])
            rep.expect(f"{sid}-{c['mark']} age days", str(c["days2"]), "%.2f" % g["AGE_DAYS"])
            rep.expect(f"{sid}-{c['mark']} within tolerance", "Yes" if c["at28"] else "No", g["WITHIN_20_HOURS_OF_28_DAYS"])
            rep.expect(f"{sid}-{c['mark']} defect", "Yes" if c["defect"] else "No", g["DEFECT_ON_RECORD"])
    smp = {r["SET_NO"]: r for r in table(wb["Samples"])}
    for sid, x in o["sets"].items():
        rep.expect(f"{sid} placement", x["placement"], smp[sid]["PLACEMENT_ID"])
        rep.expect(f"{sid} mixture", x["mix"], smp[sid]["MIXTURE"])
        rep.expect(f"{sid} curing class", "Standard" if x["standard"] else "Field", smp[sid]["CURING_CLASS"])
        rep.expect(f"{sid} curing note", bool(x["temp_exc"] or x["long_box"]), bool(smp[sid]["CURING_NOTE"]))
        rep.expect(f"{sid} fresh", "Outside 2.4" if x["fresh_out"] else "Within 2.4", smp[sid]["FRESH_CONCRETE"])
        rep.expect(f"{sid} engineer direction", bool(x.get("directed")), bool(smp[sid]["ENGINEER_DIRECTION"]))
        rep.expect(f"{sid} cast date", x["date"], smp[sid]["DATE_CAST"])
        rep.expect(f"{sid} time molded", x["molded"].strftime("%H:%M"), smp[sid]["TIME_MOLDED"])
        rep.expect(f"{sid} batch ticket", x["batch_ticket"], smp[sid]["TICKET_NO"])
        rep.expect(f"{sid} box low", x["box_min"], smp[sid]["BOX_LOW_F"] if smp[sid]["BOX_LOW_F"] is not None else "")
        rep.expect(f"{sid} box high", x["box_max"], smp[sid]["BOX_HIGH_F"] if smp[sid]["BOX_HIGH_F"] is not None else "")
        rep.expect(f"{sid} picked up", x["pickup"], f"{smp[sid]['PICKED_UP_DATE']} {smp[sid]['PICKED_UP_TIME']}")
    tst = {str(r["TICKET_NO"]): r for r in table(wb["Tests"])}
    REASON = {"Field cured": "Field cured", "Outside the age tolerance": "Tested outside the 20 hour tolerance", "Incomplete test": "Incomplete test",
              "Set aside by the engineer": "Set aside by the engineer of record"}
    for t in o["tests"]:
        g = tst[t["key"]]
        rep.expect(f"{t['key']} sets", " ".join(t["sets"]), g["SETS"])
        rep.expect(f"{t['key']} used", "Yes" if t["used"] else "No", g["USED_FOR_ACCEPTANCE"])
        rep.expect(f"{t['key']} cylinders entering", t["n"], g["CYLINDERS_ENTERING"])
        if t["used"]:
            rep.expect(f"{t['key']} test", t["value"], g["STRENGTH_TEST_PSI"])
            rep.expect(f"{t['key']} range", "%.2f" % (t["range"] * 100), "%.2f" % g["RANGE_PCT"])
            rep.expect(f"{t['key']} range note", bool(t["range_note"]), bool(g["RANGE_NOTE"]))
        else:
            rep.expect(f"{t['key']} reason", True, str(g["REASON_NOT_USED"]).startswith(REASON[t["reason"]]))
            rep.expect(f"{t['key']} result for information", t["value"], g["RESULT_FOR_INFORMATION_PSI"])
    for mix, tab in (("M-4000", "Acceptance decks"), ("M-6000", "Acceptance columns")):
        rows = table(wb[tab])
        per = [r for r in rows if r["TICKET_NO"] != "July"]
        rep.expect(f"{mix} carried tests", data["carry"][mix]["used"], [r["STRENGTH_TEST_PSI"] for r in rows if r["TICKET_NO"] == "July"])
        rep.expect(f"{mix} molding order", [t["key"] for t in o["tests"] if t["mix"] == mix], [str(r["TICKET_NO"]) for r in per])
        m = o["mix"][mix]
        for r in per:
            k = str(r["TICKET_NO"])
            if k in m["movs"]:
                rep.expect(f"{k} moving average", str(m["movs"][k]), one(r["MOVING_AVERAGE_3"]))
                rep.expect(f"{k} criterion a", "Below f'c" if any(t["key"] == k for t in m["a_fail"]) else "Meets", r["CRITERION_A"])
                rep.expect(f"{k} criterion b", "Fails" if any(t["key"] == k for t in m["b_fail"]) else "Meets", r["CRITERION_B"])
    for r in table(wb["Sampling"]):
        dd = o["days"][(r["DATE"], r["MIXTURE"])]
        rep.expect(f"{r['DATE']} {r['MIXTURE']} required", dd["required"], r["TESTS_REQUIRED"])
        rep.expect(f"{r['DATE']} {r['MIXTURE']} samples", dd["taken"], r["SAMPLES_TAKEN"])
        rep.expect(f"{r['DATE']} {r['MIXTURE']} tests used", dd["have"], r["TESTS_USED"])
        rep.expect(f"{r['DATE']} {r['MIXTURE']} status", "Short" if dd["short"] else "Met", r["STATUS"])
    rep.expect("sampling rows", len(o["days"]), len(table(wb["Sampling"])))
    note = "\n".join(str(c.value) for row in wb["Note to Gunnar"].iter_rows() for c in row if c.value)
    T = {t["sets"][0]: t for t in o["tests"]}
    for phrase in (f"{T['S-202']['value']:,} psi", f"{T['S-105']['value']:,} psi", f"{T['S-206']['value']:,} psi", f"{T['S-110']['value']:,} psi",
                   "P-05", "P-06", "P-13", "P-25", "3,996.7", "5,993.3", "5,940.0", "S-103 and S-104", "S-207", "S-114", "S-208", "S-116", "S-106",
                   "letter of October 2", "letter of September 15", "772071", "772017", "14:37", "13:52", "%.2f percent" % (T["S-105"]["range"] * 100)):
        rep.expect(f"note states {phrase}", phrase in note, True)
    rep.sensitivity(lambda **kw: standing(derive(data, **VARIANT_KW[kw["variant"]])) if kw else standing(derive(data)),
                    {name: ({"variant": name}, CONVENTION[name]) for name in VARIANT_KW})
    rep.finish()
