"""verify_golden.py for tract7-boundary-retracement (2026-09-30 rebuild): re-derive every figure the analysis
states from inputs/ alone under the firm's standards as the golden applies them, and list the readings a solver
could take instead, each with the phrase the golden uses to settle it.

    .venv/bin/python submissions/06-tract7-boundary-retracement/verify_golden.py

The facts the reduction turns on are read out of the input documents, never typed here: the pair on T3-T4 whose
forward and reverse disagree, the pair on T5-T6 that does not fit, the leg that straddles north, the prism
constants and the taped offset in the field book, the station the field book gives for each tie, the codes in the
notes file, the date the annexation takes effect, how each mark was set according to the recorded plats, the
distance the 1978 deed of trust carries, and the two deed calls that the held corners show to be in error.
"""
import csv
import math
import os
import re
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

import openpyxl
from docx import Document

HERE = Path(__file__).resolve().parent
ROOT = os.environ.get("HAZY_ROOT") or next(str(p) for p in HERE.parents if (p / "tools" / "golden_verify.py").is_file())
sys.path.insert(0, os.path.join(ROOT, "tools"))
from golden_verify import Report  # noqa: E402

INPUTS = HERE / "inputs"
GOLDEN = HERE / "solution" / "tract7_boundary_analysis.xlsx"



def rnd(x, n):
    return float(Decimal(format(x, ".15g")).quantize(Decimal(1).scaleb(-n), rounding=ROUND_HALF_UP))


def azimuth(ns, d, m, s, ew):
    a = d + m / 60 + s / 3600
    return {("N", "E"): a, ("S", "E"): 180 - a, ("S", "W"): 180 + a, ("N", "W"): 360 - a}[(ns, ew)]


def bearing(az, seconds=True):
    az %= 360
    ns, a, ew = ("N", az, "E") if az <= 90 else ("S", 180 - az, "E") if az <= 180 else ("S", az - 180, "W") if az <= 270 else ("N", 360 - az, "W")
    if seconds:
        t = int(rnd(a * 3600, 0))
        return f"{ns} {t // 3600}° {t % 3600 // 60:02d}' {t % 60:02d}\" {ew}"
    t = int(rnd(a * 60, 0))
    return f"{ns} {t // 60}° {t % 60:02d}' {ew}"


def az_of(dn, de):
    return rnd(math.degrees(math.atan2(de, dn)) % 360, 6)


def polar(p, az, d):
    return p[0] + d * math.cos(math.radians(az)), p[1] + d * math.sin(math.radians(az))


def dist(a, b):
    return math.hypot(b[0] - a[0], b[1] - a[1])


def vmean(azs):
    """mean direction of azimuths, as the golden takes it: ATAN2 of the summed cosines and sines."""
    c = sum(math.cos(math.radians(a - 45)) for a in azs); s = sum(math.sin(math.radians(a - 45)) for a in azs)
    return rnd((math.degrees(math.atan2(s, c)) + 45) % 360, 6)


def derive(shots, loop, deed, slip_call, trust_34, P, *, t5t6="fit", bust="reject", wrap="vector", prism=None, offset=None,
           klass=None, station="book", swap=True, rotation="4-5", corner3="line", adjust=True, precision_from="reported",
           hold_rebar=False, call51="slip"):
    """shots: list of dicts with AT, TO, NS, DEG, MIN, SEC, EW, HORIZ_DIST_FT, CODE, TIME.
    loop: station order. deed: five (ns, d, m, ew, dist) as transcribed. slip_call: (ns,d,m,ew) the 5-1 call as the
    analysis reads it after the slip is found. P: dict of parameters read from the inputs."""
    fig, st = {}, {}
    prism = P["prism"] if prism is None else prism; offset = P["offset105"] if offset is None else offset
    klass = P["class"] if klass is None else klass
    sh = [dict(s) for s in shots]
    changes = 0
    for s in sh:
        s["az"] = rnd(azimuth(s["NS"], int(s["DEG"]), int(s["MIN"]), int(s["SEC"]), s["EW"]), 6); s["d"] = float(s["HORIZ_DIST_FT"])
    if swap:   # the shot coded IRF is the rebar; the field book numbers the rebar 103 and the corner post 203
        irf = [s for s in sh if s["CODE"] == "IRF"]; assert len(irf) == 1
        if irf[0]["TO"] != "103":
            other = next(s for s in sh if s["TO"] == "103"); assert other["CODE"] == "FNC"
            other["TO"], irf[0]["TO"] = irf[0]["TO"], "103"; changes += 2
    if station == "book":
        for s in sh:
            if s["CODE"] != "TRAV" and P["station"][s["TO"]] != s["AT"]:
                s["AT"] = P["station"][s["TO"]]; changes += 1
    fig["changes"] = changes
    obs = {}
    for s in sh:
        if s["CODE"] == "TRAV": obs.setdefault((s["AT"], s["TO"]), []).append(s)
    legs_def = list(zip(loop, loop[1:] + loop[:1]))

    def leg_az(s, a):
        return s["az"] if s["AT"] == a else rnd((s["az"] + 180) % 360, 6)

    def mean_of(use, a):
        azs = [leg_az(s, a) for s in use]
        maz = vmean(azs) if wrap == "vector" else rnd(sum(azs) / len(azs), 6)
        return maz, rnd(sum(s["d"] for s in use) / len(use), 3)

    def closure(choice):
        legs = []; pairs_out = {}
        for a, b in legs_def:
            fw = sorted(obs[(a, b)], key=lambda r: r["TIME"]); rv = sorted(obs[(b, a)], key=lambda r: r["TIME"])
            pairs = list(zip(fw, rv))
            good = []
            for k, (f, r) in enumerate(pairs):
                dd = rnd(abs(f["d"] - r["d"]), 3); x = abs(leg_az(f, a) - leg_az(r, a)); da = rnd(min(x, 360 - x) * 3600, 0)
                ok = dd <= P["pair_ft"] and da <= P["pair_sec"]
                pairs_out[(a, b, k)] = (dd, da, ok)
                if ok or bust == "keep": good.append((f, r))
            if len(good) == 2:
                (a1, d1), (a2, d2) = mean_of(good[0], a), mean_of(good[1], a)
                x2 = abs(a1 - a2); agree = rnd(abs(d1 - d2), 3) <= P["pair_ft"] and rnd(min(x2, 360 - x2) * 3600, 0) <= P["pair_sec"]
                fig[f"pairs {a}-{b}"] = (d1, d2, rnd(abs(d1 - d2), 3), agree)
                use = list(good[0] + good[1]) if agree or choice == "all" else list(good[0]) if choice == "first" else list(good[1])
            else:
                use = list(good[0])
            maz, md = mean_of(use, a)
            legs.append([a, b, maz, md, rnd(md * math.cos(math.radians(maz)), 3), rnd(md * math.sin(math.radians(maz)), 3), len(use)])
        per = rnd(sum(l[3] for l in legs), 3); sl = rnd(sum(l[4] for l in legs), 3); sd = rnd(sum(l[5] for l in legs), 3)
        err = rnd(math.hypot(sl, sd), 2)
        prec = int(math.floor(per / (err if precision_from == "reported" else math.hypot(sl, sd)) / 100) * 100)
        return legs, per, sl, sd, err, prec, pairs_out

    first, second, both = closure("first"), closure("second"), closure("all")
    fit = second if second[5] > first[5] else first
    legs, per, sl, sd, err, prec, pairs_out = fit if t5t6 == "fit" else both if t5t6 == "all" else first
    fig["pair tests"] = pairs_out
    fig.update({"precision first pair": first[5], "precision second pair": second[5], "precision both pairs": both[5]})
    standard = P["urban"] if klass == "Urban" else P["rural"]
    nshots = sum(1 for s in sh if s["CODE"] == "TRAV")
    fig.update({"perimeter": per, "lat misclosure": sl, "dep misclosure": sd, "linear error": err, "precision": prec,
                "shots set aside": nshots - sum(l[6] for l in legs), "class": klass, "standard": standard, "legs": legs})
    st["closure test"] = "Meets the standard" if prec >= standard else "Does not meet the standard"
    st["standard applied"] = standard; st["precision"] = prec
    S = {loop[0]: (P["n0"], P["e0"])}; cur = S[loop[0]]
    for l in legs:
        cl = rnd(-sl * l[3] / per, 3) if adjust else 0.0; cd = rnd(-sd * l[3] / per, 3) if adjust else 0.0
        cur = (rnd(cur[0] + rnd(l[4] + cl, 3), 3), rnd(cur[1] + rnd(l[5] + cd, 3), 3))
        if l[1] != loop[0]: S[l[1]] = cur
    fig["stations"] = S
    pts = {}
    for s in sh:
        if s["CODE"] == "TRAV": continue
        d = rnd(s["d"] + prism + (offset if s["TO"] == "105" else 0.0), 2)
        q = S[s["AT"]]
        pts[s["TO"]] = (rnd(q[0] + rnd(d * math.cos(math.radians(s["az"])), 3), 3), rnd(q[1] + rnd(d * math.sin(math.radians(s["az"])), 3), 3))
    fig["points"] = pts
    pin1, pin2, rebar, s4, s5, pipe, set3 = (pts[k] for k in ("101", "102", "103", "104", "105", "106", "107"))
    fig["pin 2 to rebar"] = rnd(dist(pin2, rebar), 2); fig["pin 2 to corner post"] = rnd(dist(pin2, pts["203"]), 2); fig["stone to pipe"] = rnd(dist(s4, pipe), 2)
    fig["pin 2 to set pin"] = rnd(dist(pin2, set3), 2)
    # the deed on its own calls, as transcribed
    dz = [rnd(azimuth(ns, d, mi, 0, ew), 6) for ns, d, mi, ew, _ in deed]; dd = [c[4] for c in deed]
    lat = [rnd(dd[i] * math.cos(math.radians(dz[i])), 3) for i in range(5)]; dep = [rnd(dd[i] * math.sin(math.radians(dz[i])), 3) for i in range(5)]
    dl = rnd(sum(lat), 3); dp = rnd(sum(dep), 3); dper = rnd(sum(dd), 1); derr = rnd(math.hypot(dl, dp), 2)
    fig.update({"deed perimeter": dper, "deed misclosure": derr, "deed per 1000": rnd(derr / dper * 1000, 2), "deed misclosure bearing": bearing(az_of(dl, dp), False)})
    st["deed test"] = "Defect in the description" if fig["deed per 1000"] > P["deed_rate"] else "Within the tolerance of the original survey"
    # the deed with the record's figures: 592.7 in the 3-4 call, and the 5-1 bearing with its digits restored
    sz = rnd(azimuth(slip_call[0], slip_call[1], slip_call[2], 0, slip_call[3]), 6)
    def mis(d34, az51):
        L = list(lat); D = list(dep)
        L[2] = rnd(d34 * math.cos(math.radians(dz[2])), 3); D[2] = rnd(d34 * math.sin(math.radians(dz[2])), 3)
        L[4] = rnd(dd[4] * math.cos(math.radians(az51)), 3); D[4] = rnd(dd[4] * math.sin(math.radians(az51)), 3)
        return rnd(math.hypot(rnd(sum(L), 3), rnd(sum(D), 3)), 2)
    fig["deed misclosure, 592.7 only"] = mis(trust_34, dz[4]); fig["deed misclosure, 43 31 only"] = mis(dd[2], sz); fig["deed misclosure, both"] = mis(trust_34, sz)
    # rotation: the 4-5 course, stone to stone, both found original monuments of the tract (3.2 first arm)
    if rotation == "4-5":
        daz = dz[3]; maz = az_of(s5[0] - s4[0], s5[1] - s4[1])
    else:   # the road course, pin to pin, which the field book treats as the deed line
        daz = dz[0]; maz = az_of(pin2[0] - pin1[0], pin2[1] - pin1[1])
    fig["rotation deed azimuth"] = daz; fig["rotation measured azimuth"] = maz
    rot_min = int(rnd((maz - daz) * 60, 0))
    fig["rotation"] = f"{rot_min // 60}° {rot_min % 60:02d}' east of the deed bearings"; st["rotation"] = fig["rotation"]
    fig["rotation minutes"] = rot_min
    fig["rotation road course minutes"] = int(rnd((az_of(pin2[0] - pin1[0], pin2[1] - pin1[1]) - dz[0]) * 60, 0))
    rot = rnd(rot_min / 60, 6); raz = [rnd((a + rot) % 360, 6) for a in dz]
    raz51 = rnd((sz + rot) % 360, 6) if call51 == "restored" else raz[4]
    # corner 1: the later pin tested from the pin at corner 2 by the 1-2 call (the 5-1 call being in error)
    q1 = polar(pin2, (raz[0] + 180) % 360, dd[0]); q1 = (rnd(q1[0], 3), rnd(q1[1], 3))
    fig["pin 1 offset"] = rnd(dist(q1, pin1), 2)
    hold1 = fig["pin 1 offset"] <= P["later_tol"]
    st["corner 1 pin"] = "Held as the corner" if hold1 else "Found, not held"
    c1 = pin1 if hold1 else q1
    # corner 3: the rotated 2-3 course from corner 2 meeting the Ballinger west line, stone to pipe (3.7 first arm)
    b = az_of(pipe[0] - s4[0], pipe[1] - s4[1]); fig["ballinger az"] = b
    t = rnd(((s4[1] - pin2[1]) * math.cos(math.radians(b)) - (s4[0] - pin2[0]) * math.sin(math.radians(b))) / math.sin(math.radians(raz[1] - b)), 3) if corner3 == "line" else dd[1]
    x3 = polar(pin2, raz[1], t); x3 = (rnd(x3[0], 3), rnd(x3[1], 3))
    fig["corner 3 along"] = t
    fig["rebar offset"] = rnd(dist(x3, rebar), 2); fig["set pin offset"] = rnd(dist(x3, set3), 2)
    held3 = hold_rebar or fig["rebar offset"] <= P["later_tol"]
    st["corner 3 rebar"] = "Held as the corner" if held3 else "Found, not held"
    c3 = rebar if held3 else x3
    fig["corner 3"] = c3
    C = [c1, pin2, c3, s4, s5]; fig["corners"] = C
    out = []
    names = ["1-2", "2-3", "3-4", "4-5", "5-1"]
    for i, n in enumerate(names):
        a = az_of(C[(i + 1) % 5][0] - C[i][0], C[(i + 1) % 5][1] - C[i][1]); d = rnd(dist(C[i], C[(i + 1) % 5]), 2)
        ra = raz[i]
        bd = rnd((a - ra) * 60, 0); ddiff = rnd(d - dd[i], 2)
        fig[f"bearing {n}"] = bearing(a); fig[f"distance {n}"] = d; fig[f"bearing diff {n}"] = bd; fig[f"distance diff {n}"] = ddiff
        fig[f"rotated {n}"] = bearing(ra, seconds=False); fig[f"az {n}"] = a
        if abs(ddiff) > P["dist_tol"] or abs(bd) > P["bear_tol"]: out.append(n)
    fig["bearing diff 5-1 restored"] = rnd((fig["az 5-1"] - rnd((sz + rot) % 360, 6)) * 60, 0)
    fig["calls out"] = len(out); st["calls out of tolerance"] = ",".join(out)
    st["distance 2-3"] = fig["distance 2-3"]; st["distance 3-4"] = fig["distance 3-4"]
    st["corners to set"] = ",".join(str(i + 1) for i, h in ((0, hold1), (2, held3)) if not h) or "none"
    st["corner 3 rebar"] = st["corner 3 rebar"]
    area = int(rnd(abs(sum(C[i][0] * C[(i + 1) % 5][1] - C[(i + 1) % 5][0] * C[i][1] for i in range(5))) / 2, 0))
    fig["area"] = area; fig["acres"] = rnd(area / P["sqft"], 3); fig["acre difference"] = rnd(fig["acres"] - P["deed_acres"], 3); fig["area difference"] = rnd(area - P["deed_acres"] * P["sqft"], 0)
    st["acres"] = fig["acres"]
    for name, (i, ids) in P["fences"].items():
        a = az_of(C[i + 1][0] - C[i][0], C[i + 1][1] - C[i][1]); ar = math.radians(a)
        offs = [rnd((pts[p][1] - C[i][1]) * math.cos(ar) - (pts[p][0] - C[i][0]) * math.sin(ar), 2) for p in ids]
        for p, o in zip(ids, offs): fig[f"offset {p}"] = o
        fig[f"{name} inside"] = max(0, max(offs)); fig[f"{name} outside"] = max(0, -min(offs))
        st[f"{name} fence"] = "Encroachment" if max(offs) > P["enc_tol"] else "Occupation note only"
        fig[f"{name} fence"] = st[f"{name} fence"]
    return fig, st


# ---------------------------------------------------------------- the inputs, read
def text_of(name):
    d = Document(INPUTS / name)
    return "\n".join([p.text for p in d.paragraphs] + [c.text for t in d.tables for r in t.rows for c in r.cells])

SHOTS = list(csv.DictReader(open(INPUTS / "field_notes_traverse_tract7.csv", newline="")))
BOOK = text_of("field_book_tract7.docx"); DEEDTXT = text_of("deed_book_412_page_233.docx")
REC = text_of("record_research_tract7.docx").replace("“", '"').replace("”", '"'); STD = text_of("firm_survey_standards.docx")
MONTHS = {m: i for i, m in enumerate("January February March April May June July August September October November December".split(), 1)}
LOOP = re.search(r"The loop was run ((?:T\d, )+T\d), and back to T1", BOOK).group(1).split(", ")
assert LOOP[0] == "T1" and len(LOOP) == 7, LOOP
CALL = re.compile(r"([NS]) (\d+)° (\d+)' ([EW]) (\d+\.\d) feet")
DEED = [(ns, int(d), int(m), ew, float(x)) for ns, d, m, ew, x in CALL.findall(DEEDTXT)]
assert len(DEED) == 5, DEED
DEED_ACRES = float(re.search(r"containing (\d+\.\d+) acres", DEEDTXT).group(1))
# the 5-1 call with its two degree digits exchanged, the reading the held corners at both ends bear out
SLIP = (DEED[4][0], int(str(DEED[4][1])[::-1]), DEED[4][2], DEED[4][3])
URBAN = int(re.search(r"urban traverse must close to a precision of not worse than one part in ([\d,]+)", STD).group(1).replace(",", ""))
RURAL = int(re.search(r"rural traverse to one part in ([\d,]+)", STD).group(1).replace(",", ""))
PAIR_FT, PAIR_SEC = (float(x) for x in re.search(r"differ by more than (\d\.\d+) foot in distance or (\d+) seconds in bearing", STD).groups())
assert (PAIR_FT, PAIR_SEC) == tuple(float(x) for x in re.search(r"agree within (\d\.\d+) foot and (\d+) seconds", STD).groups())
LATER_TOL = float(re.search(r"within (\d\.\d+) foot of the position the corner would take", STD).group(1))
ENC_TOL = float(re.search(r"inside the tract by more than (\d\.\d+) foot", STD).group(1))
M_PER_FT = float(re.search(r"at (0\.\d+) meter to the U\.S\. survey foot", STD).group(1))
assert "ten minutes of bearing and one foot of distance" in STD and "43,560" in STD and "compass rule" in STD
assert "provisional" in STD and "a call that is within the tolerance of 3.3" in STD
SET_MM = float(re.search(r"prism constant set at (-?\d+(?:\.\d+)?) mm", BOOK).group(1))
MINI_MM = float(re.search(r"mini prism on the pole for the ties, constant (-?\d+(?:\.\d+)?) mm", BOOK).group(1))
PRISM = rnd((MINI_MM - SET_MM) / 1000 / M_PER_FT, 2)
OFFSET = float(re.search(r"Point 105.*?held (\d\.\d+) foot short of the hole", BOOK, re.S).group(1))
STATION = {}
for pts, st in re.findall(r"[Pp]oints? ([\d, and]+?) (?:was|were)? ?(?:tied )?from (T\d)", re.search(r"Each monument, the pin we set, and each fence post.*", BOOK).group(0)):
    for p in re.findall(r"\d{3}", pts):
        STATION[p] = st
assert len(STATION) == 16, STATION
PARCEL = float(re.search(r"Tax Map 053, Parcel (\d+\.\d+), in the name of Wendell R\. Cope", REC).group(1))
FIELD = re.search(r"(\w+) (\d+), (\d{4}) \(traverse\) and (\w+) (\d+), (\d{4})", BOOK).groups()
FIELD_LAST = (int(FIELD[5]), MONTHS[FIELD[3]], int(FIELD[4]))
CLASS = "Rural"
for lo, hi, mon, day, yr in re.findall(r"Parcels (\d+\.\d+) through (\d+\.\d+),[^.]*?effective (\w+) (\d+), (\d{4})", REC):
    if float(lo) <= PARCEL <= float(hi) and (int(yr), MONTHS[mon], int(day)) <= FIELD_LAST:
        CLASS = "Urban"
PLAT1994 = re.search(r"RLS 1188\. The plat notes read: (.*)", REC).group(1); PLAT2008 = re.search(r"RLS 2207\. The plat notes read: (.*)", REC).group(1)
CAP = {p: re.search(rf"Point {p}.*?stamped PLS (\d+)", BOOK, re.S).group(1) for p in ("101", "102", "103", "107")}
assert CAP == {"101": "1188", "102": "2207", "103": "2207", "107": "2641"}, CAP
PEDIGREE = {
    "101": "later" if re.search(r"northwest corner of the remaining lands.*?no monument was found", PLAT1994) else "original",
    "102": "original" if re.search(r"southwest corner.*?pin of the Tolliver survey was found in place.*?capped where it stood", PLAT2008) else "later",
    "103": "later" if re.search(r"southeast corner.*?no monument was found.*?rebar with cap was set (\d+\.\d) feet", PLAT2008) else "original",
    "104": "original" if re.search(r"stone at the Ballinger corner was found upright", PLAT1994) else "later",
    "105": "original" if re.search(r"stone at the angle point was found in the fence row.*?left as found", PLAT1994) else "later",
}
assert PEDIGREE == {"101": "later", "102": "original", "103": "later", "104": "original", "105": "original"}, PEDIGREE
assert "Point 107" in BOOK and "before the loop was closed" in BOOK
REBAR_REC = float(re.search(r"rebar with cap was set (\d+\.\d) feet", PLAT2008).group(1))
BALL_REC = float(re.search(r"thence with Farley N 8° 40' E (\d+\.\d) feet to an iron pipe", REC).group(1))
TRUST = float(re.search(r"third call reads \"S 8° 46' W (\d+\.\d) feet", REC).group(1))
PK = float(re.search(r"PK nail.*?stands in the ground (\d\.\d+) foot from our hub", BOOK).group(1))
P = dict(prism=PRISM, offset105=OFFSET, urban=URBAN, rural=RURAL, pair_ft=PAIR_FT, pair_sec=PAIR_SEC, later_tol=LATER_TOL, enc_tol=ENC_TOL,
         n0=5000.0, e0=5000.0, deed_rate=1.0, dist_tol=1.0, bear_tol=10, sqft=43560, deed_acres=DEED_ACRES, station=STATION,
         fences={"Hutchins": (1, ("201", "202", "203")), "Ballinger": (2, ("204", "205", "206")), "Farley": (3, ("207", "208", "209"))})
P["class"] = CLASS
NAMES = ["1-2", "2-3", "3-4", "4-5", "5-1"]


def run(**kw):
    return derive(SHOTS, LOOP, DEED, SLIP, TRUST, P, **kw)


VARIANTS = {
    "rotation from the road course, the pin at corner 1 read as original": ({"rotation": "1-2"}, "the one deed course with a found original monument at each end"),
    "every doubled leg meaned over all its shots, the pair in error kept": ({"bust": "keep", "t5t6": "all"}, "is rejected"),
    "first pair on T5-T6 used": ({"t5t6": "first"}, "The first pair is set aside"),
    "both pairs on T5-T6 meaned together": ({"t5t6": "all"}, "are not meaned together"),
    "azimuths on T7-T2 averaged as numbers across north": ({"wrap": "arith"}, "meaned as directions"),
    "urban standard, the annexation read as in force": ({"klass": "Urban"}, "rural on the field dates"),
    "prism correction on the ties missed": ({"prism": 0.0}, "prism correction of 0.04 foot"),
    "taped offset on the stone at corner 5 missed": ({"offset": 0.0}, "carries the 0.60 foot"),
    "point 202 reduced from the station in the notes file": ({"station": "file"}, "reduced from T3 and not from T2"),
    "point numbers 103 and 203 taken as recorded": ({"swap": False}, "the numbers of points 103 and 203 are exchanged"),
    "rebar at corner 3 held as found": ({"hold_rebar": True}, "so it is not held"),
    "corner 3 set at the deed distance on the rotated course": ({"corner3": "distance"}, "meets that line"),
    "ties reduced from unadjusted station coordinates": ({"adjust": False}, "compass rule"),
    "precision from the unrounded linear error": ({"precision_from": "raw"}, "linear error as reported"),
}

if __name__ == "__main__":
    fig, standing = run()
    wb = openpyxl.load_workbook(GOLDEN, data_only=True)
    g, tr, ti, de, co, ar, fe = (wb[n] for n in ("Findings", "Traverse", "Ties", "Deed", "Corners", "Area", "Fences"))
    rep = Report()
    F = {str(g[f"A{r}"].value): g[f"B{r}"].value for r in range(6, 90) if g[f"B{r}"].value is not None}
    num = lambda v: f"{float(v) + 0.0:.6f}" if isinstance(v, (int, float)) else str(v)
    sz = rnd(azimuth(SLIP[0], SLIP[1], SLIP[2], 0, SLIP[3]), 6)
    restored = bearing(rnd((sz + fig["rotation minutes"] / 60) % 360, 6), False)
    pin2 = fig["points"]["102"]; rebar = fig["points"]["103"]
    road_az = azimuth(DEED[1][0], DEED[1][1], DEED[1][2], 0, DEED[1][3]) + fig["rotation road course minutes"] / 60
    q = (pin2[0] + fig["corner 3 along"] * math.cos(math.radians(road_az)), pin2[1] + fig["corner 3 along"] * math.sin(math.radians(road_az)))
    road_rebar = rnd(math.hypot(rebar[0] - q[0], rebar[1] - q[1]), 2)
    exp = [("Perimeter of the traverse (ft)", fig["perimeter"]), ("Latitude misclosure (ft)", fig["lat misclosure"]), ("Departure misclosure (ft)", fig["dep misclosure"]),
           ("Linear error of closure (ft)", fig["linear error"]), ("Precision of closure, one part in", fig["precision"]), ("Traverse shots set aside or rejected", fig["shots set aside"]),
           ("Tract classification on the field dates", fig["class"]), ("Firm standard for that class, one part in", fig["standard"]), ("Closure test", standing["closure test"]),
           ("Prism correction on every tie (ft)", PRISM), ("Offset added to the tie on point 105 (ft)", OFFSET), ("Changes made to the notes file", fig["changes"]),
           ("Deed linear misclosure on its own calls, as transcribed (ft)", fig["deed misclosure"]), ("Deed misclosure per 1,000 ft of perimeter", fig["deed per 1000"]), ("Deed description test", standing["deed test"]),
           ("Deed misclosure with the 1978 distance and the 5-1 bearing restored (ft)", fig["deed misclosure, both"]),
           ("Rotation, deed magnetic bearings to the grid", fig["rotation"]), ("Rotation the road course would give (minutes of arc)", fig["rotation road course minutes"]),
           ("Calls out of tolerance", fig["calls out"]), ("Calls in error in the deed", fig["calls out"]),
           ("3-4 call, deed distance as transcribed (ft)", DEED[2][4]), ("3-4 call, measured distance the plat carries (ft)", fig["distance 3-4"]), ("3-4 call, distance in the 1978 deed of trust (ft)", TRUST),
           ("5-1 call, rotated bearing as transcribed", fig["rotated 5-1"]), ("5-1 call, rotated bearing with the digits restored", restored),
           ("5-1 call, measured bearing the plat carries", fig["bearing 5-1"]), ("5-1 call, measured less restored (minutes)", fig["bearing diff 5-1 restored"]),
           ("Original monuments of the tract found and held", sum(1 for v in PEDIGREE.values() if v == "original")), ("Later monuments held as the corner", 1 if standing["corner 1 pin"] == "Held as the corner" else 0),
           ("Offset of the corner 1 pin from its test position (ft)", fig["pin 1 offset"]), ("Later monuments found and not held", 1 if standing["corner 3 rebar"] == "Found, not held" else 0),
           ("Offset of the corner 3 rebar from the corner (ft)", fig["rebar offset"]), ("Corners to be set", 1), ("Corner to be set", int(standing["corners to set"])),
           ("Distance from corner 2 to corner 3 (ft)", fig["distance 2-3"]), ("Distance from corner 3 to the stone at corner 4 (ft)", fig["distance 3-4"]),
           ("Distance the crew's pin at corner 3 is to be moved (ft)", fig["set pin offset"]),
           ("Area by coordinates (sq ft)", fig["area"]), ("Area (acres)", fig["acres"]), ("Deed acreage recited", DEED_ACRES), ("Difference, computed less deed (acres)", fig["acre difference"]),
           ("Hutchins fence, greatest offset inside the tract (ft)", fig["Hutchins inside"]), ("Hutchins fence finding", fig["Hutchins fence"]),
           ("Ballinger fence, greatest offset outside the tract (ft)", fig["Ballinger outside"]), ("Ballinger fence finding", fig["Ballinger fence"]),
           ("Farley fence, greatest offset inside the tract (ft)", fig["Farley inside"]), ("Farley fence finding", fig["Farley fence"])]
    for n in range(1, 6):
        exp.append((f"Corner {n} northing (ft)", fig["corners"][n - 1][0])); exp.append((f"Corner {n} easting (ft)", fig["corners"][n - 1][1]))
    for label, want in exp:
        rep.expect(label, num(want), num(F.get(label)))
    for k, l in enumerate(fig["legs"]):
        r = 4 + k
        rep.expect(f"leg {l[0]}-{l[1]} mean azimuth", num(l[2]), num(tr[f"F{r}"].value)); rep.expect(f"leg {l[0]}-{l[1]} mean distance", num(l[3]), num(tr[f"H{r}"].value))
        rep.expect(f"leg {l[0]}-{l[1]} shots used", l[6], tr[f"D{r}"].value)
    for k, s in enumerate(LOOP):
        rep.expect(f"station {s} N", num(fig["stations"][s][0]), num(tr[f"B{25 + k}"].value)); rep.expect(f"station {s} E", num(fig["stations"][s][1]), num(tr[f"C{25 + k}"].value))
    PAIRS = [("T1", "T7", 0), ("T7", "T2", 0), ("T2", "T3", 0), ("T2", "T3", 1), ("T3", "T4", 0), ("T3", "T4", 1), ("T4", "T5", 0), ("T5", "T6", 0), ("T5", "T6", 1), ("T6", "T1", 0)]
    for k, key in enumerate(PAIRS):
        dd, da, ok = fig["pair tests"][key]; r = 36 + k
        rep.expect(f"pair {key[0]}-{key[1]} {key[2] + 1} distance difference", num(dd), num(tr[f"E{r}"].value)); rep.expect(f"pair {key[0]}-{key[1]} {key[2] + 1} bearing difference", num(da), num(tr[f"H{r}"].value))
        rep.expect(f"pair {key[0]}-{key[1]} {key[2] + 1} test", "Pair stands" if ok else "Pair in error", tr[f"I{r}"].value)
    rep.expect("pair difference T2-T3", num(fig["pairs T2-T3"][2]), num(tr["D49"].value)); rep.expect("pair difference T5-T6", num(fig["pairs T5-T6"][2]), num(tr["D51"].value))
    rep.expect("precision on the first pair T5-T6", fig["precision first pair"], tr["I55"].value); rep.expect("precision on both pairs T5-T6", fig["precision both pairs"], tr["I56"].value)
    for r in range(4, 20):
        p = str(ti[f"A{r}"].value)
        rep.expect(f"point {p} N", num(fig["points"][p][0]), num(ti[f"K{r}"].value)); rep.expect(f"point {p} E", num(fig["points"][p][1]), num(ti[f"L{r}"].value))
    rep.expect("pin 2 to rebar", num(fig["pin 2 to rebar"]), num(ti["C23"].value)); rep.expect("record of the rebar", num(REBAR_REC), num(ti["D23"].value))
    rep.expect("pin 2 to corner post", num(fig["pin 2 to corner post"]), num(ti["C24"].value)); rep.expect("pin 2 to the set pin", num(fig["pin 2 to set pin"]), num(ti["C25"].value))
    rep.expect("stone to pipe", num(fig["stone to pipe"]), num(ti["C26"].value)); rep.expect("record of the Ballinger line", num(BALL_REC), num(ti["D26"].value))
    for k, n in enumerate(NAMES):
        r = 4 + k
        rep.expect(f"rotated bearing {n}", fig[f"rotated {n}"], de[f"K{r}"].value); rep.expect(f"measured bearing {n}", fig[f"bearing {n}"], de[f"M{r}"].value)
        rep.expect(f"measured distance {n}", num(fig[f"distance {n}"]), num(de[f"N{r}"].value))
        rep.expect(f"bearing difference {n}", num(fig[f"bearing diff {n}"]), num(de[f"O{r}"].value)); rep.expect(f"distance difference {n}", num(fig[f"distance diff {n}"]), num(de[f"P{r}"].value))
        rep.expect(f"corner {k + 1} N", num(fig["corners"][k][0]), num(co[f"C{28 + k}"].value)); rep.expect(f"corner {k + 1} E", num(fig["corners"][k][1]), num(co[f"D{28 + k}"].value))
    rep.expect("deed perimeter", num(fig["deed perimeter"]), num(de["B12"].value)); rep.expect("deed misclosure bearing", fig["deed misclosure bearing"], de["B20"].value)
    rep.expect("deed misclosure, 592.7 only", num(fig["deed misclosure, 592.7 only"]), num(de["B27"].value)); rep.expect("deed misclosure, 43 31 only", num(fig["deed misclosure, 43 31 only"]), num(de["B28"].value))
    rep.expect("deed azimuth of the rotation line", num(fig["rotation deed azimuth"]), num(de["B33"].value)); rep.expect("measured azimuth of the rotation line", num(fig["rotation measured azimuth"]), num(de["B34"].value))
    rep.expect("rotation minutes", fig["rotation minutes"], de["B35"].value); rep.expect("road course less the 4-5 course", fig["rotation road course minutes"] - fig["rotation minutes"], de["B39"].value)
    rep.expect("rebar offset under the road-course rotation", num(road_rebar), num(co["B41"].value))
    rep.expect("corner 3 along the 2-3 course", num(fig["corner 3 along"]), num(co["B21"].value)); rep.expect("set pin disposition", "To be reset at the corner", co["L10"].value)
    rep.expect("area difference sq ft", num(fig["area difference"]), num(ar["B15"].value))
    for r in range(4, 13):
        p = str(fe[f"A{r}"].value); rep.expect(f"fence post {p} offset", num(fig[f"offset {p}"]), num(fe[f"K{r}"].value))
    note = "\n".join(str(c.value) for row in wb["Note to Ellen"].iter_rows() for c in row if c.value)
    for phrase in (f"one part in {fig['precision']:,}", f"one part in {fig['precision first pair']:,}", f"{fig['linear error']:.2f} foot", f"{fig['perimeter']:,.2f} feet", f"{fig['pairs T5-T6'][2]:.2f} foot",
                   f"{fig['pair tests'][('T3', 'T4', 0)][0]:.2f} feet apart", f"{fig['deed misclosure']:.2f} feet", f"{fig['deed per 1000']:.2f} feet per 1,000", f"{fig['deed misclosure, both']:.2f} foot",
                   f"{fig['area']:,} square feet", f"{fig['acres']:.3f} acres", f"{abs(fig['area difference']):.0f} square feet", fig["rotation"], f"{fig['rotation road course minutes'] // 60}° {fig['rotation road course minutes'] % 60:02d}'",
                   f"{fig['distance 3-4']:.2f} feet", f"{fig['distance 2-3']:.2f} feet", f"{fig['pin 1 offset']:.2f} foot", f"{fig['rebar offset']:.2f} foot", f"{road_rebar:.2f} foot", f"{fig['set pin offset']:.2f} foot",
                   f"{fig['pin 2 to rebar']:.2f} feet", f"{fig['stone to pipe']:.2f} feet", f"{TRUST} feet", restored, fig["bearing 5-1"], f"{fig['bearing diff 5-1 restored']:.0f} minutes",
                   f"{fig['offset 202']:.2f} foot", f"{fig['Ballinger outside']:.2f} foot", f"{fig['Farley inside']:.2f} foot", f"{fig['corner 3'][0]:,.3f}", f"{fig['corner 3'][1]:,.3f}", f"prism correction of {PRISM:.2f} foot", "meaned as directions"):
        rep.expect(f"note states {phrase}", phrase in note, True)
    rep.sensitivity(lambda **kw: run(**kw)[1], VARIANTS)
    rep.finish()
