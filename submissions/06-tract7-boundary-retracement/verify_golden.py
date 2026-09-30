"""verify_golden.py for tract7-boundary-retracement: re-derive every figure the analysis states from
inputs/ alone under the firm's standards as the golden applies them, and list the readings a solver
could take instead, each with the phrase the golden uses to settle it.

    .venv/bin/python submissions/06-tract7-boundary-retracement/verify_golden.py

The facts the reduction turns on are read out of the input documents, never typed here: the pair on
the T5-T6 leg that does not fit, the prism constants in the field book, the taped offset on the stone
at corner 5, the station the field book gives for each tie, the codes in the notes file, the date the
annexation takes effect, and how each mark was set according to the recorded plats. Each trap variant
below is one of those reads missed, and the sensitivity pass shows what it moves.
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
LEGS = [("T1", "T2"), ("T2", "T3"), ("T3", "T4"), ("T4", "T5"), ("T5", "T6"), ("T6", "T1")]
NAMES = ["1-2", "2-3", "3-4", "4-5", "5-1"]
FENCES = {"Hutchins": (1, ("201", "202", "203")), "Ballinger": (2, ("204", "205", "206")), "Farley": (3, ("207", "208", "209"))}
MONTHS = {m: i for i, m in enumerate("January February March April May June July August September October November December".split(), 1)}


def rnd(x, n):
    """Excel's ROUND: half up on the 15-digit value."""
    return float(Decimal(format(x, ".15g")).quantize(Decimal(1).scaleb(-n), rounding=ROUND_HALF_UP))


def azimuth(ns, d, m, s, ew):
    a = d + m / 60 + s / 3600
    k = (ns, ew)
    return a if k == ("N", "E") else 180 - a if k == ("S", "E") else 180 + a if k == ("S", "W") else 360 - a


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


def text_of(name):
    d = Document(INPUTS / name)
    return "\n".join([p.text for p in d.paragraphs] + [c.text for t in d.tables for r in t.rows for c in r.cells])


# ---------------------------------------------------------------- the inputs, read
SHOTS = list(csv.DictReader(open(INPUTS / "field_notes_traverse_tract7.csv", newline="")))
BOOK = text_of("field_book_tract7.docx"); DEEDTXT = text_of("deed_book_412_page_233.docx")
REC = text_of("record_research_tract7.docx"); STD = text_of("firm_survey_standards.docx")

CALL = re.compile(r"([NS]) (\d+)° (\d+)' ([EW]) (\d+\.\d) feet")
DEED = [(ns, int(d), int(m), ew, float(x)) for ns, d, m, ew, x in CALL.findall(DEEDTXT)]
assert len(DEED) == 5, DEED
DEED_ACRES = float(re.search(r"containing (\d+\.\d+) acres", DEEDTXT).group(1))

# the firm standards' own figures
URBAN = int(re.search(r"urban traverse must close to a precision of not worse than one part in ([\d,]+)", STD).group(1).replace(",", ""))
RURAL = int(re.search(r"rural traverse to one part in ([\d,]+)", STD).group(1).replace(",", ""))
PAIR_FT, PAIR_SEC = (float(x) for x in re.search(r"agree within (\d\.\d+) foot and (\d+) seconds", STD).groups())
LATER_TOL = float(re.search(r"within (\d\.\d+) foot of the position the corner would take", STD).group(1))
ENC_TOL = float(re.search(r"inside the tract by more than (\d\.\d+) foot", STD).group(1))
M_PER_FT = float(re.search(r"at (0\.\d+) meter to the U\.S\. survey foot", STD).group(1))
assert "ten minutes of bearing and one foot of distance" in STD and "43,560" in STD and "compass rule" in STD
BEAR_TOL, DIST_TOL, SQFT = 10, 1.0, 43560

# the prism constants, and the correction the standards define from them
SET_MM = float(re.search(r"prism constant set at (-?\d+(?:\.\d+)?) mm", BOOK).group(1))
MINI_MM = float(re.search(r"mini prism on the pole for the ties, constant (-?\d+(?:\.\d+)?) mm", BOOK).group(1))
PRISM = rnd((MINI_MM - SET_MM) / 1000 / M_PER_FT, 2)
# the taped offset on the stone at corner 5
OFFSET = float(re.search(r"Point 105.*?held (\d\.\d+) foot short of the hole", BOOK, re.S).group(1))
# the station the field book gives for every tie
STATION = {}
for pts, st in re.findall(r"[Pp]oints? ([\d, and]+?) (?:was|were)? ?(?:tied )?from (T\d)", re.search(r"Each monument and each fence post.*", BOOK).group(0)):
    for p in re.findall(r"\d{3}", pts):
        STATION[p] = st
assert len(STATION) == 15, STATION
# the class of the traverse: the ordinance that takes in the parcel, and the day it takes effect
PARCEL = float(re.search(r"Tax Map 053, Parcel (\d+\.\d+), in the name of Wendell R\. Cope", REC).group(1))
FIELD = re.search(r"(\w+) (\d+), (\d{4}) \(traverse\) and (\w+) (\d+), (\d{4})", BOOK).groups()
FIELD_LAST = (int(FIELD[5]), MONTHS[FIELD[3]], int(FIELD[4]))
CLASS = "Rural"
for lo, hi, mon, day, yr in re.findall(r"Parcels (\d+\.\d+) through (\d+\.\d+),[^.]*?effective (\w+) (\d+), (\d{4})", REC):
    if float(lo) <= PARCEL <= float(hi) and (int(yr), MONTHS[mon], int(day)) <= FIELD_LAST:
        CLASS = "Urban"
# the pedigree of each mark, from the recorded plats
PLAT1994 = re.search(r"RLS 1188\. The plat notes read: (.*)", REC).group(1); PLAT2008 = re.search(r"RLS 2207\. The plat notes read: (.*)", REC).group(1)
CAP = {p: re.search(rf"Point {p}.*?stamped PLS (\d+)", BOOK, re.S).group(1) for p in ("101", "102", "103")}
assert CAP == {"101": "1188", "102": "2207", "103": "2207"}
PEDIGREE = {
    "101": "later" if re.search(r"northwest corner of the remaining lands.*?no monument was found", PLAT1994) else "original",
    "102": "original" if re.search(r"southwest corner.*?pin of the Tolliver survey was found in place.*?capped where it stood", PLAT2008) else "later",
    "103": "later" if re.search(r"southeast corner.*?no monument was found.*?rebar with cap was set (\d+\.\d) feet", PLAT2008) else "original",
    "104": "original" if re.search(r"stone at the Ballinger corner was found upright", PLAT1994) else "later",
    "105": "later" if re.search(r"stone at the angle point was found out of the ground.*?reset in concrete at the deed bearing and distance", PLAT1994) else "original",
}
assert PEDIGREE == {"101": "later", "102": "original", "103": "later", "104": "original", "105": "later"}, PEDIGREE
REBAR_REC = float(re.search(r"rebar with cap was set (\d+\.\d) feet", PLAT2008).group(1))
BALL_REC = float(re.search(r"thence with Farley N 8° 40' E (\d+\.\d) feet to an iron pipe", REC).group(1))
TRUST = float(re.search(r"third call reads \"S 8° 46' W (\d+\.\d) feet", REC.replace("“", '"').replace("”", '"')).group(1))
PK = float(re.search(r"PK nail.*?stands in the ground (\d\.\d+) foot from our hub", BOOK).group(1))


def derive(t5t6="fit", prism=PRISM, offset=OFFSET, klass=CLASS, station="book", swap=True, rotation="pathB", stone5="later",
           hold_rebar=False, corner3="line", adjust=True, precision_from="reported"):
    fig, st = {}, {}
    shots = [dict(s) for s in SHOTS]
    changes = 0
    for s in shots:
        s["az"] = rnd(azimuth(s["NS"], int(s["DEG"]), int(s["MIN"]), int(s["SEC"]), s["EW"]), 6); s["d"] = float(s["HORIZ_DIST_FT"])
    # a point whose code is a monument's while the field book calls its number a fence post, and the reverse
    if swap:
        irf = [s for s in shots if s["CODE"] == "IRF"]; assert len(irf) == 1
        if irf[0]["TO"] != "103":
            other = next(s for s in shots if s["TO"] == "103"); assert other["CODE"] == "FNC"
            other["TO"], irf[0]["TO"] = irf[0]["TO"], "103"; changes += 2
    # the station the field book gives for the tie
    if station == "book":
        for s in shots:
            if s["CODE"] != "TRAV" and STATION[s["TO"]] != s["AT"]:
                s["AT"] = STATION[s["TO"]]; changes += 1
    fig["changes"] = changes
    obs = {}
    for s in shots:
        if s["CODE"] == "TRAV": obs.setdefault((s["AT"], s["TO"]), []).append(s)

    def leg_mean(use, a):
        azs = [s["az"] if s["AT"] == a else rnd((s["az"] + 180) % 360, 6) for s in use]
        return rnd(sum(azs) / len(azs), 6), rnd(sum(s["d"] for s in use) / len(use), 3)

    def closure(choice):
        legs = []
        for a, b in LEGS:
            fw = sorted(obs[(a, b)], key=lambda r: r["TIME"]); rv = sorted(obs[(b, a)], key=lambda r: r["TIME"])
            pairs = list(zip(fw, rv))
            if len(pairs) == 2:
                (a1, d1), (a2, d2) = leg_mean(pairs[0], a), leg_mean(pairs[1], a)
                agree = rnd(abs(d1 - d2), 3) <= PAIR_FT and rnd(abs(a1 - a2) * 3600, 0) <= PAIR_SEC
                fig[f"pairs {a}-{b}"] = (d1, d2, rnd(abs(d1 - d2), 3), agree)
                use = list(pairs[0] + pairs[1]) if agree or choice == "all" else list(pairs[0]) if choice == "first" else list(pairs[1])
            else:
                use = list(pairs[0])
            maz, md = leg_mean(use, a)
            legs.append([a, b, maz, md, rnd(md * math.cos(math.radians(maz)), 3), rnd(md * math.sin(math.radians(maz)), 3), len(use)])
        per = rnd(sum(l[3] for l in legs), 3); sl = rnd(sum(l[4] for l in legs), 3); sd = rnd(sum(l[5] for l in legs), 3)
        err = rnd(math.hypot(sl, sd), 2)
        return legs, per, sl, sd, err, int(math.floor(per / (err if precision_from == "reported" else math.hypot(sl, sd)) / 100) * 100)

    first, second, both = closure("first"), closure("second"), closure("all")
    # the pair at fault is the one the closure and the PK nail both point to
    fit = second if second[5] > first[5] else first
    assert fit is second and abs(fig["pairs T5-T6"][2] - PK) < 0.005
    legs, per, sl, sd, err, prec = fit if t5t6 == "fit" else both if t5t6 == "all" else first
    fig.update({"precision first pair": first[5], "precision both pairs": both[5]})
    standard = URBAN if klass == "Urban" else RURAL
    fig.update({"perimeter": per, "lat misclosure": sl, "dep misclosure": sd, "linear error": err, "precision": prec,
                "shots set aside": 16 - sum(l[6] for l in legs), "class": klass, "standard": standard, "legs": legs})
    st["closure test"] = "Meets the standard" if prec >= standard else "Does not meet the standard"
    st["standard applied"] = standard; st["precision"] = prec
    P = {"T1": (5000.0, 5000.0)}; cur = (5000.0, 5000.0)
    for l in legs:
        cl = rnd(-sl * l[3] / per, 3) if adjust else 0.0; cd = rnd(-sd * l[3] / per, 3) if adjust else 0.0
        cur = (rnd(cur[0] + rnd(l[4] + cl, 3), 3), rnd(cur[1] + rnd(l[5] + cd, 3), 3))
        if l[1] != "T1": P[l[1]] = cur
    fig["stations"] = P
    pts = {}
    for s in shots:
        if s["CODE"] == "TRAV": continue
        d = rnd(s["d"] + prism + (offset if s["TO"] == "105" else 0.0), 2)
        q = P[s["AT"]]
        pts[s["TO"]] = (rnd(q[0] + rnd(d * math.cos(math.radians(s["az"])), 3), 3), rnd(q[1] + rnd(d * math.sin(math.radians(s["az"])), 3), 3))
    fig["points"] = pts
    pin1, pin2, rebar, s4, s5, pipe = (pts[k] for k in ("101", "102", "103", "104", "105", "106"))
    fig["pin 2 to rebar"] = rnd(dist(pin2, rebar), 2); fig["pin 2 to corner post"] = rnd(dist(pin2, pts["203"]), 2); fig["stone to pipe"] = rnd(dist(s4, pipe), 2)
    dz = [rnd(azimuth(ns, d, mi, 0, ew), 6) for ns, d, mi, ew, _ in DEED]; dd = [c[4] for c in DEED]
    lat = [rnd(dd[i] * math.cos(math.radians(dz[i])), 3) for i in range(5)]; dep = [rnd(dd[i] * math.sin(math.radians(dz[i])), 3) for i in range(5)]
    dl = rnd(sum(lat), 3); dp = rnd(sum(dep), 3); dper = rnd(sum(dd), 1); derr = rnd(math.hypot(dl, dp), 2)
    fig.update({"deed perimeter": dper, "deed misclosure": derr, "deed per 1000": rnd(derr / dper * 1000, 2), "deed misclosure bearing": bearing(az_of(dl, dp), False)})
    st["deed test"] = "Defect in the description" if fig["deed per 1000"] > 1 else "Within the tolerance of the original survey"
    fig["deed misclosure with trust figure"] = rnd(math.hypot(dl - lat[2] + rnd(TRUST * math.cos(math.radians(dz[2])), 3), dp - dep[2] + rnd(TRUST * math.sin(math.radians(dz[2])), 3)), 2)
    # rotation: the line between the two found original monuments of the tract, the call in error left out
    if rotation == "pathB":
        daz = az_of(rnd(lat[3] + lat[4] + lat[0], 3), rnd(dep[3] + dep[4] + dep[0], 3)); maz = az_of(pin2[0] - s4[0], pin2[1] - s4[1])
    elif rotation == "pathA":
        daz = az_of(lat[1] + lat[2], dep[1] + dep[2]); maz = az_of(s4[0] - pin2[0], s4[1] - pin2[1])
    elif rotation == "4-5":
        daz = dz[3]; maz = az_of(s5[0] - s4[0], s5[1] - s4[1])
    else:
        daz = dz[0]; maz = az_of(pin2[0] - pin1[0], pin2[1] - pin1[1])
    fig["rotation deed azimuth"] = daz; fig["rotation measured azimuth"] = maz
    rot_min = int(rnd((maz - daz) * 60, 0))
    fig["rotation"] = f"{rot_min // 60}° {rot_min % 60:02d}' east of the deed bearings"; st["rotation"] = fig["rotation"]
    fig["rotation path A"] = int(rnd(((az_of(s4[0] - pin2[0], s4[1] - pin2[1])) - az_of(lat[1] + lat[2], dep[1] + dep[2])) * 60, 0))
    rot = rnd(rot_min / 60, 6); raz = [rnd((a + rot) % 360, 6) for a in dz]
    # later monuments against the 3.7 position
    q5 = polar(s4, raz[3], dd[3]); q5 = (rnd(q5[0], 3), rnd(q5[1], 3))
    fig["stone 5 offset"] = rnd(dist(q5, s5), 2)
    hold5 = stone5 == "original" or fig["stone 5 offset"] <= LATER_TOL
    st["corner 5 stone"] = "Held as the corner" if hold5 else "Found, not held"
    c5 = s5 if hold5 else q5
    q1 = polar(pin2, (raz[0] + 180) % 360, dd[0]) if stone5 == "later" else polar(c5, raz[4], dd[4])
    q1 = (rnd(q1[0], 3), rnd(q1[1], 3))
    fig["pin 1 offset"] = rnd(dist(q1, pin1), 2)
    hold1 = fig["pin 1 offset"] <= LATER_TOL
    st["corner 1 pin"] = "Held as the corner" if hold1 else "Found, not held"
    c1 = pin1 if hold1 else q1
    b = az_of(pipe[0] - s4[0], pipe[1] - s4[1])
    t = rnd(((s4[1] - pin2[1]) * math.cos(math.radians(b)) - (s4[0] - pin2[0]) * math.sin(math.radians(b))) / math.sin(math.radians(raz[1] - b)), 3) if corner3 == "line" else dd[1]
    x3 = polar(pin2, raz[1], t); x3 = (rnd(x3[0], 3), rnd(x3[1], 3))
    fig["rebar offset"] = rnd(dist(x3, rebar), 2)
    held3 = hold_rebar or fig["rebar offset"] <= LATER_TOL
    st["corner 3 rebar"] = "Held as the corner" if held3 else "Found, not held"
    c3 = rebar if held3 else x3
    fig["corner 3"] = c3
    C = [c1, pin2, c3, s4, c5]; fig["corners"] = C
    out = []
    for i, n in enumerate(NAMES):
        a = az_of(C[(i + 1) % 5][0] - C[i][0], C[(i + 1) % 5][1] - C[i][1]); d = rnd(dist(C[i], C[(i + 1) % 5]), 2)
        bd = rnd((a - raz[i]) * 60, 0); ddiff = rnd(d - dd[i], 2)
        fig[f"bearing {n}"] = bearing(a); fig[f"distance {n}"] = d; fig[f"bearing diff {n}"] = bd; fig[f"distance diff {n}"] = ddiff
        fig[f"rotated {n}"] = bearing(raz[i], seconds=False)
        if abs(ddiff) > DIST_TOL or abs(bd) > BEAR_TOL: out.append(n)
    fig["calls out"] = len(out); st["calls out of tolerance"] = ",".join(out); fig["call in error"] = st["calls out of tolerance"]
    st["distance 2-3"] = fig["distance 2-3"]; st["distance 3-4"] = fig["distance 3-4"]
    st["corners to set"] = ",".join(str(i + 1) for i, h in ((0, hold1), (2, held3), (4, hold5)) if not h) or "none"
    area = int(rnd(abs(sum(C[i][0] * C[(i + 1) % 5][1] - C[(i + 1) % 5][0] * C[i][1] for i in range(5))) / 2, 0))
    fig["area"] = area; fig["acres"] = rnd(area / SQFT, 3); fig["acre difference"] = rnd(fig["acres"] - DEED_ACRES, 3); fig["area difference"] = rnd(area - DEED_ACRES * SQFT, 0)
    st["acres"] = fig["acres"]
    for name, (i, ids) in FENCES.items():
        a = az_of(C[i + 1][0] - C[i][0], C[i + 1][1] - C[i][1]); ar = math.radians(a)
        offs = [rnd((pts[p][1] - C[i][1]) * math.cos(ar) - (pts[p][0] - C[i][0]) * math.sin(ar), 2) for p in ids]
        for p, o in zip(ids, offs): fig[f"offset {p}"] = o
        fig[f"{name} inside"] = max(0, max(offs)); fig[f"{name} outside"] = max(0, -min(offs))
        st[f"{name} fence"] = "Encroachment" if max(offs) > ENC_TOL else "Occupation note only"
        fig[f"{name} fence"] = st[f"{name} fence"]
    return fig, st


# Each variant is one read missed or one convention taken another way; the phrase is the golden's own.
VARIANTS = {
    "both pairs on T5-T6 meaned together": ({"t5t6": "all"}, "are not meaned together"),
    "first pair on T5-T6 used": ({"t5t6": "first"}, "the first pair is set aside"),
    "urban standard, the annexation read as in force": ({"klass": "Urban"}, "the tract is rural on the field dates"),
    "prism correction on the ties missed": ({"prism": 0.0}, "prism correction of 0.04 foot"),
    "taped offset on the stone at corner 5 missed": ({"offset": 0.0}, "carries the 0.60 foot"),
    "point 202 reduced from the station in the notes file": ({"station": "file"}, "reduced from T3 and not from T2"),
    "point numbers 103 and 203 taken as recorded": ({"swap": False}, "the numbers of points 103 and 203 are exchanged"),
    "rotation through the 2-3 and 3-4 calls as written": ({"rotation": "pathA"}, "the 3-4 call being left out"),
    "rotation from the 4-5 course, the reset stone read as original": ({"rotation": "4-5", "stone5": "original"}, "no deed course has both"),
    "rotation from the 1-2 course": ({"rotation": "1-2"}, "no deed course has both"),
    "rebar at corner 3 held as found": ({"hold_rebar": True}, "the rebar at corner 3 is not held"),
    "corner 3 set at the deed distance on the rotated course": ({"corner3": "distance"}, "meets that line"),
    "ties reduced from unadjusted station coordinates": ({"adjust": False}, "compass rule"),
    "precision from the unrounded linear error": ({"precision_from": "raw"}, "linear error as reported"),
}

if __name__ == "__main__":
    fig, standing = derive()
    wb = openpyxl.load_workbook(GOLDEN, data_only=True)
    g, tr, ti, de, co, ar, fe = (wb[n] for n in ("Findings", "Traverse", "Ties", "Deed", "Corners", "Area", "Fences"))
    rep = Report()
    F = {str(g[f"A{r}"].value): g[f"B{r}"].value for r in range(6, 70) if g[f"B{r}"].value is not None}
    exp = [("Perimeter of the traverse (ft)", fig["perimeter"]), ("Latitude misclosure (ft)", fig["lat misclosure"]), ("Departure misclosure (ft)", fig["dep misclosure"]),
           ("Linear error of closure (ft)", fig["linear error"]), ("Precision of closure, one part in", fig["precision"]), ("Traverse shots set aside", fig["shots set aside"]),
           ("Tract classification on the field dates", fig["class"]), ("Firm standard for that class, one part in", fig["standard"]), ("Closure test", standing["closure test"]),
           ("Prism correction on every tie (ft)", PRISM), ("Offset added to the tie on point 105 (ft)", OFFSET), ("Changes made to the notes file", fig["changes"]),
           ("Deed linear misclosure on its own calls (ft)", fig["deed misclosure"]), ("Deed misclosure per 1,000 ft of perimeter", fig["deed per 1000"]), ("Deed description test", standing["deed test"]),
           ("Rotation, deed magnetic bearings to the grid", fig["rotation"]), ("Calls out of tolerance", fig["calls out"]), ("Call in error", fig["call in error"]),
           ("Deed distance of that call as transcribed (ft)", DEED[2][4]), ("Measured distance of that course (ft)", fig["distance 3-4"]), ("Distance of that call in the 1978 deed of trust (ft)", TRUST),
           ("Original monuments of the tract found and held", sum(1 for v in PEDIGREE.values() if v == "original")), ("Later monuments held as the corner", 2),
           ("Offset of the corner 1 pin from its test position (ft)", fig["pin 1 offset"]), ("Offset of the corner 5 stone from its test position (ft)", fig["stone 5 offset"]),
           ("Later monuments found and not held", 1), ("Offset of the corner 3 rebar from its test position (ft)", fig["rebar offset"]), ("Corners to be set", 1), ("Corner to be set", int(standing["corners to set"])),
           ("Corner 3 northing (ft)", fig["corner 3"][0]), ("Corner 3 easting (ft)", fig["corner 3"][1]),
           ("Distance from corner 2 to corner 3 (ft)", fig["distance 2-3"]), ("Distance from corner 3 to the stone at corner 4 (ft)", fig["distance 3-4"]),
           ("Area by coordinates (sq ft)", fig["area"]), ("Area (acres)", fig["acres"]), ("Deed acreage recited", DEED_ACRES), ("Difference, computed less deed (acres)", fig["acre difference"]),
           ("Hutchins fence, greatest offset outside the tract (ft)", fig["Hutchins outside"]), ("Hutchins fence finding", fig["Hutchins fence"]),
           ("Ballinger fence, greatest offset inside the tract (ft)", fig["Ballinger inside"]), ("Ballinger fence finding", fig["Ballinger fence"]),
           ("Farley fence, greatest offset inside the tract (ft)", fig["Farley inside"]), ("Farley fence finding", fig["Farley fence"])]
    num = lambda v: f"{float(v) + 0.0:.6f}" if isinstance(v, (int, float)) else str(v)
    for label, want in exp:
        rep.expect(label, num(want), num(F.get(label)))
    for k, l in enumerate(fig["legs"]):
        r = 4 + k
        rep.expect(f"leg {l[0]}-{l[1]} mean azimuth", num(l[2]), num(tr[f"F{r}"].value)); rep.expect(f"leg {l[0]}-{l[1]} mean distance", num(l[3]), num(tr[f"H{r}"].value))
        rep.expect(f"leg {l[0]}-{l[1]} shots used", l[6], tr[f"D{r}"].value)
    for k, s in enumerate(["T1", "T2", "T3", "T4", "T5", "T6"]):
        rep.expect(f"station {s} N", num(fig["stations"][s][0]), num(tr[f"B{24 + k}"].value)); rep.expect(f"station {s} E", num(fig["stations"][s][1]), num(tr[f"C{24 + k}"].value))
    rep.expect("pair difference T2-T3", num(fig["pairs T2-T3"][2]), num(tr["D34"].value)); rep.expect("pair difference T5-T6", num(fig["pairs T5-T6"][2]), num(tr["D35"].value))
    rep.expect("precision on the first pair", fig["precision first pair"], tr["I39"].value); rep.expect("precision on both pairs", fig["precision both pairs"], tr["I40"].value)
    for r in range(4, 19):
        p = str(ti[f"A{r}"].value)
        rep.expect(f"point {p} N", num(fig["points"][p][0]), num(ti[f"K{r}"].value)); rep.expect(f"point {p} E", num(fig["points"][p][1]), num(ti[f"L{r}"].value))
    rep.expect("pin 2 to rebar", num(fig["pin 2 to rebar"]), num(ti["C22"].value)); rep.expect("record of the rebar", num(REBAR_REC), num(ti["D22"].value))
    rep.expect("pin 2 to corner post", num(fig["pin 2 to corner post"]), num(ti["C23"].value))
    rep.expect("stone to pipe", num(fig["stone to pipe"]), num(ti["C24"].value)); rep.expect("record of the Ballinger line", num(BALL_REC), num(ti["D24"].value))
    for k, n in enumerate(NAMES):
        r = 4 + k
        rep.expect(f"rotated bearing {n}", fig[f"rotated {n}"], de[f"K{r}"].value); rep.expect(f"measured bearing {n}", fig[f"bearing {n}"], de[f"M{r}"].value)
        rep.expect(f"measured distance {n}", num(fig[f"distance {n}"]), num(de[f"N{r}"].value))
        rep.expect(f"bearing difference {n}", num(fig[f"bearing diff {n}"]), num(de[f"O{r}"].value)); rep.expect(f"distance difference {n}", num(fig[f"distance diff {n}"]), num(de[f"P{r}"].value))
        rep.expect(f"corner {k + 1} N", num(fig["corners"][k][0]), num(co[f"C{30 + k}"].value)); rep.expect(f"corner {k + 1} E", num(fig["corners"][k][1]), num(co[f"D{30 + k}"].value))
    rep.expect("deed perimeter", num(fig["deed perimeter"]), num(de["B12"].value)); rep.expect("deed misclosure bearing", fig["deed misclosure bearing"], de["B20"].value)
    rep.expect("deed azimuth of the rotation line", num(fig["rotation deed azimuth"]), num(de["B28"].value)); rep.expect("measured azimuth of the rotation line", num(fig["rotation measured azimuth"]), num(de["B29"].value))
    rep.expect("rotation through the calls as written", fig["rotation path A"], de["B33"].value)
    rep.expect("deed misclosure with the 1978 figure", num(fig["deed misclosure with trust figure"]), num(de["B43"].value))
    rep.expect("area difference sq ft", num(fig["area difference"]), num(ar["B15"].value))
    for r in range(4, 13):
        p = str(fe[f"A{r}"].value); rep.expect(f"fence post {p} offset", num(fig[f"offset {p}"]), num(fe[f"K{r}"].value))
    note = "\n".join(str(c.value) for row in wb["Note to Ellen"].iter_rows() for c in row if c.value)
    for phrase in (f"one part in {fig['precision']:,}", f"one part in {fig['precision first pair']:,}", f"{fig['linear error']:.2f} foot", f"{fig['perimeter']:,.2f} feet", f"{fig['lat misclosure']:.3f} foot", f"{fig['dep misclosure']:.3f} foot",
                   f"{fig['pairs T5-T6'][2]:.2f} foot", f"{fig['deed misclosure']:.2f} feet", f"{fig['deed per 1000']:.2f} feet per 1,000", fig["deed misclosure bearing"], f"{fig['area']:,} square feet", f"{fig['acres']:.3f} acres",
                   f"{abs(fig['acre difference']):.3f} acre", f"{abs(fig['area difference']):.0f} square feet", "2° 16' east of the deed bearings", f"would give {fig['rotation path A'] // 60}° {fig['rotation path A'] % 60:02d}'",
                   bearing(fig["rotation deed azimuth"], False), bearing(fig["rotation measured azimuth"], False),
                   f"{fig['distance 3-4']:.2f} feet", f"{fig['distance 2-3']:.2f} feet", f"{fig['pin 1 offset']:.2f} foot", f"{fig['stone 5 offset']:.2f} foot", f"{fig['rebar offset']:.2f} feet",
                   f"{fig['pin 2 to rebar']:.2f} feet", f"{fig['stone to pipe']:.2f} feet", f"{TRUST} feet", f"within {fig['deed misclosure with trust figure']:.2f} foot",
                   f"{fig['Ballinger inside']:.2f} foot", f"{fig['offset 205']:.2f} foot", f"{fig['offset 206']:.2f} foot", f"{fig['Farley inside']:.2f} foot", f"{-fig['offset 201']:.2f} to {fig['Hutchins outside']:.2f} foot",
                   f"{fig['corner 3'][0]:,.3f}", f"{fig['corner 3'][1]:,.3f}", f"prism correction of {PRISM:.2f} foot"):
        rep.expect(f"note states {phrase}", phrase in note, True)
    rep.sensitivity(lambda **kw: derive(**kw)[1], VARIANTS)
    rep.finish()
