"""Build solution/tract7_boundary_analysis.xlsx for the 2026-09-30 rebuild: every figure a formula over the
notes file copied shot for shot and the deed calls typed on the Deed tab. Run from the hazy root."""
import csv
import re
import sys
import zipfile
import shutil
from pathlib import Path

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from docx import Document

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reduce_core import derive, rnd, bearing, azimuth

ROOT = Path("/Users/aladdin/projects/snk/hazy/submissions/06-tract7-boundary-retracement")
INPUTS = ROOT / "inputs"; OUT = ROOT / "solution" / "tract7_boundary_analysis.xlsx"
SHOTS = list(csv.DictReader(open(INPUTS / "field_notes_traverse_tract7.csv", newline="")))
LOOP = ["T1", "T7", "T2", "T3", "T4", "T5", "T6"]
LEGS = [f"{a}-{b}" for a, b in zip(LOOP, LOOP[1:] + LOOP[:1])]
DEED = [("N", 14, 44, "E", 640.4), ("S", 81, 6, "E", 588.8), ("S", 8, 46, "W", 597.2), ("S", 77, 59, "W", 510.1), ("N", 34, 31, "W", 225.5)]
SLIP = ("N", 43, 31, "W"); TRUST = 592.7
PK = float(re.search(r"PK nail.*?stands in the ground (\d\.\d+) foot from our hub", "\n".join(p.text for p in Document(INPUTS / "field_book_tract7.docx").paragraphs)).group(1))
STATION = {"101": "T1", "102": "T2", "201": "T2", "202": "T3", "103": "T4", "203": "T4", "107": "T4", "106": "T4", "204": "T4",
           "104": "T5", "205": "T5", "206": "T5", "207": "T5", "105": "T6", "208": "T6", "209": "T6"}
P = dict(prism=0.04, offset105=0.60, **{"class": "Rural"}, urban=15000, rural=10000, pair_ft=0.05, pair_sec=20, later_tol=0.5, enc_tol=0.25,
         n0=5000.0, e0=5000.0, deed_rate=1.0, dist_tol=1.0, bear_tol=10, sqft=43560, deed_acres=9.89, station=STATION,
         fences={"Hutchins": (1, ("201", "202", "203")), "Ballinger": (2, ("204", "205", "206")), "Farley": (3, ("207", "208", "209"))})
FIG, ST = derive(SHOTS, LOOP, DEED, SLIP, TRUST, P)
FIG_ROAD, _ = derive(SHOTS, LOOP, DEED, SLIP, TRUST, P, rotation="1-2")
import math as _m
def _road_rebar():
    pin2 = FIG["points"]["102"]; rebar = FIG["points"]["103"]
    az = (azimuth(*DEED[1][:3], 0, DEED[1][3]) + FIG["rotation road course minutes"] / 60)
    q = (pin2[0] + FIG["corner 3 along"] * _m.cos(_m.radians(az)), pin2[1] + FIG["corner 3 along"] * _m.sin(_m.radians(az)))
    return rnd(_m.hypot(rebar[0] - q[0], rebar[1] - q[1]), 2)
ROAD_REBAR = _road_rebar()

TITLE = Font(name="Calibri", size=13, bold=True); BOLD = Font(name="Calibri", size=11, bold=True); BODY = Font(name="Calibri", size=11)
HEAD = PatternFill("solid", fgColor="E3E8D9"); WRAP = Alignment(wrap_text=True, vertical="top"); LEFT = Alignment(horizontal="left")
N3, N2, N6, N1, N0, NC = "0.000", "0.00", "0.000000", "0.0", "0", "#,##0"

wb = openpyxl.Workbook(); wb.remove(wb.active)

def sheet(name, widths, title):
    ws = wb.create_sheet(name)
    for col, w in widths.items(): ws.column_dimensions[col].width = w
    ws["A1"] = title; ws["A1"].font = TITLE; ws.row_dimensions[1].height = 17
    return ws

def header(ws, row, labels, height=None):
    for i, t in enumerate(labels, 1):
        c = ws.cell(row=row, column=i, value=t); c.font = BOLD; c.fill = HEAD; c.alignment = WRAP
    if height: ws.row_dimensions[row].height = height

def put(ws, ref, value, fmt=None, bold=False, wrap=False, left=False):
    c = ws[ref]; c.value = value; c.font = BOLD if bold else BODY
    if fmt: c.number_format = fmt
    if wrap: c.alignment = WRAP
    if left: c.alignment = LEFT
    return c

def bearing_text(ref, seconds=True):
    """Excel text of a quadrant bearing from an azimuth cell; seconds via Parameters!$B$18, minutes via $B$17."""
    q = f"(IF({ref}<=90,{ref},IF({ref}<=180,180-{ref},IF({ref}<=270,{ref}-180,360-{ref}))))"
    if seconds:
        t = f"ROUND({q}*Parameters!$B$18,0)"
        return (f'=IF(OR({ref}<=90,{ref}>270),"N","S")&" "&TEXT(INT({t}/Parameters!$B$18),"0")&"° "&TEXT(INT(MOD({t},Parameters!$B$18)/Parameters!$B$17),"00")'
                f'&"\' "&TEXT(MOD({t},Parameters!$B$17),"00")&""""&" "&IF({ref}<=180,"E","W")')
    t = f"ROUND({q}*Parameters!$B$17,0)"
    return f'=IF(OR({ref}<=90,{ref}>270),"N","S")&" "&TEXT(INT({t}/Parameters!$B$17),"0")&"° "&TEXT(MOD({t},Parameters!$B$17),"00")&"\' "&IF({ref}<=180,"E","W")'

# ============================================================ Parameters
ps = sheet("Parameters", {"A": 54, "B": 14, "C": 100}, "Parameters and office readings for the tract 7 analysis")
header(ps, 3, ["Parameter", "Value", "Source"], 16)
PARAMS = [
    ("First station northing (ft)", 5000, "Firm standards 1.4"), ("First station easting (ft)", 5000, "Firm standards 1.4"),
    ("Closure standard, urban, one part in", 15000, "Firm standards 1.3"), ("Closure standard, rural, one part in", 10000, "Firm standards 1.3"),
    ("Tract classification on the field dates", "Rural", "Firm standards 1.3; record research: Parcel 041.00 comes inside the corporate limits under Ordinance O26-07, effective November 1, 2026, after the field work of September 29 and 30, 2026"),
    ("Square feet per acre", 43560, "Firm standards 2.1"), ("Deed acreage recited", 9.89, "Deed Book 412, Page 233"),
    ("Deed misclosure threshold (ft per 1,000 ft of perimeter)", 1, "Firm standards 3.1"), ("Perimeter unit for the deed misclosure rate (ft)", 1000, "Firm standards 3.1"),
    ("Tolerance of the original survey, distance (ft)", 1, "Firm standards 3.3"), ("Tolerance of the original survey, bearing (minutes)", 10, "Firm standards 3.3"),
    ("Later monument held within (ft)", 0.5, "Firm standards 3.6"), ("Occupation reported as encroachment beyond (ft)", 0.25, "Firm standards 3.8"),
    ("Minutes in a degree", 60, "Sexagesimal angle"), ("Seconds in a degree", 3600, "Sexagesimal angle"),
    ("Pairs on one course meaned together within (ft)", 0.05, "Firm standards 1.1; the same figures test a forward shot against its reverse"),
    ("Pairs on one course meaned together within (seconds)", 20, "Firm standards 1.1"),
    ("Prism constant set in the instrument (mm)", -30, "Field book, instrument"), ("Prism constant of the mini prism used on the ties (mm)", -17.5, "Field book, prisms"),
    ("Meters in a U.S. survey foot", 0.3048006, "Firm standards 1.5"),
    ("Prism correction on every tie (ft)", "=ROUND((B22-B21)/B29/B23,2)", "Firm standards 1.5: the constant of the prism used less the constant set"),
    ("Offset added to the tie on point 105 (ft)", 0.6, "Field book, point 105: the pole was held 0.60 foot short of the drill hole on the line of sight"),
    ("Distance of the 3-4 call in the 1978 deed of trust (ft)", 592.7, "Record research: Trust Book 88, Page 140"),
    ("Distance of the rebar from the Hutchins southwest corner on the 2008 plat (ft)", 588.8, "Record research: Plat Cabinet D, Slide 57"),
    ("Length of the Ballinger west line in the Ballinger deed (ft)", 806.9, "Record research: Deed Book 377, Page 102"),
    ("Millimeters in a meter", 1000, "Metric conversion, for the prism constants"),
    ("Turn applied to every leg azimuth before the direction mean (degrees)", 45, "Office convention. The mean bearing of a leg is taken from summed cosines and sines, and the turn keeps those of the T7-T2 leg away from zero where it straddles north. The turn is taken off again after the mean."),
]
for i, (a, b, c) in enumerate(PARAMS, 4):
    put(ps, f"A{i}", a); cb = put(ps, f"B{i}", b); put(ps, f"C{i}", c, wrap=True); ps.row_dimensions[i].height = 16 if len(c) < 95 else 32
    if i == 24: cb.number_format = N2
assert ps["B24"].value.startswith("=ROUND((B22-B21)/B29") and ps["A29"].value == "Millimeters in a meter"

# ============================================================ Field Notes
fn = sheet("Field Notes", {"A": 6, "B": 12, "C": 7, "D": 6, "E": 6, "F": 4, "G": 5, "H": 5, "I": 5, "J": 4, "K": 14, "L": 7, "M": 9, "N": 8, "O": 12, "P": 9, "Q": 10, "R": 13, "S": 6, "T": 11, "U": 11, "V": 7, "W": 11, "X": 9, "Y": 12, "Z": 90},
           "Field notes, field_notes_traverse_tract7.csv, every shot as recorded, with the office columns beside them")
header(fn, 3, ["SHOT", "DATE", "TIME", "AT", "TO", "NS", "DEG", "MIN", "SEC", "EW", "HORIZ_DIST_FT", "CODE", "STATION USED", "POINT USED", "AZIMUTH", "LEG", "DIRECTION",
               "AZIMUTH ALONG THE LEG", "PAIR", "COSINE, LEG AZIMUTH LESS THE TURN", "SINE, LEG AZIMUTH LESS THE TURN", "USED", "PRISM CORRECTION (FT)", "OFFSET (FT)", "DISTANCE USED (FT)", "OFFICE NOTE"], 48)
NOTES = {
    "9": "Pair in error under firm standards 1.1: the reverse distance of this pair reads 1.20 feet longer than the forward. The pair is rejected, and the second pair carries the T3-T4 leg",
    "10": "Pair in error under firm standards 1.1, rejected with shot 9",
    "15": "Set aside: first pair on T5-T6, 0.28 foot short of the second pair, the distance of the county PK nail from the hub at T6",
    "16": "Set aside: first pair on T5-T6, taken to the PK nail and not to the hub",
    "24": "Station changed from T2 to T3: the field book ties point 202 from T3, the shot falls between the T2 and T4 set-ups, and from T3 the post stands on the fence line",
    "25": "Point changed from 103 to 203: the code is FNC, and this is the fence corner post",
    "26": "Point changed from 203 to 103: the code is IRF, and the mark stands 588.82 feet from the pin at corner 2, the distance on the 2008 plat",
    "34": "Pole held 0.60 foot short of the drill hole on the line of sight; the taped 0.60 foot is added",
}
PAIR = {}
seen = {}
for s in SHOTS:
    if s["CODE"] == "TRAV":
        key = tuple(sorted([s["AT"], s["TO"]])); seen.setdefault(key, []).append(s["SHOT"])
for key, ids in seen.items():
    for k, sid in enumerate(ids): PAIR[sid] = 1 if k < 2 else 2
USED_NO = {"9", "10", "15", "16"}
LAST = 3 + len(SHOTS)
for i, s in enumerate(SHOTS, 4):
    r = i
    put(fn, f"A{r}", int(s["SHOT"])); put(fn, f"B{r}", s["DATE"]); put(fn, f"C{r}", s["TIME"]); put(fn, f"D{r}", s["AT"]); put(fn, f"E{r}", s["TO"])
    put(fn, f"F{r}", s["NS"]); put(fn, f"G{r}", int(s["DEG"])); put(fn, f"H{r}", int(s["MIN"])); put(fn, f"I{r}", int(s["SEC"])); put(fn, f"J{r}", s["EW"])
    put(fn, f"K{r}", float(s["HORIZ_DIST_FT"]), N2); put(fn, f"L{r}", s["CODE"])
    at_used = "T3" if s["TO"] == "202" else s["AT"]; to_used = {"103": "203", "203": "103"}.get(s["TO"], s["TO"]) if s["CODE"] in ("IRF", "FNC") and s["TO"] in ("103", "203") else s["TO"]
    put(fn, f"M{r}", at_used); put(fn, f"N{r}", to_used)
    put(fn, f"O{r}", f'=ROUND(IF(AND(F{r}="N",J{r}="E"),(G{r}+H{r}/Parameters!$B$17+I{r}/Parameters!$B$18),IF(AND(F{r}="S",J{r}="E"),180-(G{r}+H{r}/Parameters!$B$17+I{r}/Parameters!$B$18),IF(AND(F{r}="S",J{r}="W"),180+(G{r}+H{r}/Parameters!$B$17+I{r}/Parameters!$B$18),360-(G{r}+H{r}/Parameters!$B$17+I{r}/Parameters!$B$18)))),6)', N6)
    if s["CODE"] == "TRAV":
        put(fn, f"P{r}", f'=IF(ISNUMBER(MATCH(M{r}&"-"&N{r},Traverse!$A$4:$A$10,0)),M{r}&"-"&N{r},N{r}&"-"&M{r})')
        put(fn, f"Q{r}", f'=IF(P{r}=M{r}&"-"&N{r},"Forward","Reverse")')
        put(fn, f"R{r}", f'=IF(Q{r}="Forward",O{r},ROUND(MOD(O{r}+180,360),6))', N6)
        put(fn, f"S{r}", PAIR[s["SHOT"]])
        put(fn, f"T{r}", f"=COS(RADIANS(R{r}-Parameters!$B$30))", "0.000000000"); put(fn, f"U{r}", f"=SIN(RADIANS(R{r}-Parameters!$B$30))", "0.000000000")
        put(fn, f"V{r}", "No" if s["SHOT"] in USED_NO else "Yes")
        put(fn, f"Y{r}", f"=K{r}", N2)
    else:
        put(fn, f"W{r}", "=Parameters!$B$24", N2); put(fn, f"X{r}", "=Parameters!$B$25" if s["TO"] == "105" else 0, N2)
        put(fn, f"Y{r}", f"=ROUND(K{r}+W{r}+X{r},2)", N2)
    if s["SHOT"] in NOTES: put(fn, f"Z{r}", NOTES[s["SHOT"]], wrap=True)
put(fn, f"A{LAST + 2}", "Columns A to L are the notes file as recorded. STATION USED and POINT USED carry the three changes the office made on reading the file against the field book, each with its reason in the note beside it. USED marks the traverse shots that enter the mean under firm standards 1.1: a pair in error is rejected, and the pair at fault on a doubled leg is set aside. The mean bearing of a leg is taken as a direction, from the summed cosines and sines of the azimuths turned by 45 degrees, because the T7-T2 leg straddles north.", wrap=True)
fn.row_dimensions[LAST + 2].height = 48
FN = f"'Field Notes'!"
def rng(col): return f"{FN}${col}$4:${col}${LAST}"

# ============================================================ Traverse
tr = sheet("Traverse", {"A": 46, "B": 14, "C": 14, "D": 13, "E": 13, "F": 14, "G": 18, "H": 14, "I": 13, "J": 13, "K": 11, "L": 11, "M": 12, "N": 12, "O": 13, "P": 13},
           "Traverse reduction: mean of the pairs that stand, latitudes and departures, closure, compass rule, station coordinates")
header(tr, 3, ["Leg", "From", "To", "Shots used", "Shots set aside", "Mean azimuth", "Mean bearing", "Mean distance (ft)", "Latitude (ft)", "Departure (ft)", "Latitude correction", "Departure correction", "Adjusted latitude", "Adjusted departure", "Northing of To (ft)", "Easting of To (ft)"], 32)
for k, leg in enumerate(LEGS):
    r = 4 + k; a, b = leg.split("-")
    put(tr, f"A{r}", leg); put(tr, f"B{r}", a); put(tr, f"C{r}", b)
    put(tr, f"D{r}", f'=COUNTIFS({rng("P")},A{r},{rng("V")},"Yes")'); put(tr, f"E{r}", f'=COUNTIFS({rng("P")},A{r},{rng("V")},"No")')
    put(tr, f"F{r}", f'=ROUND(MOD(DEGREES(ATAN2(SUMIFS({rng("T")},{rng("P")},A{r},{rng("V")},"Yes"),SUMIFS({rng("U")},{rng("P")},A{r},{rng("V")},"Yes")))+Parameters!$B$30,360),6)', N6)
    put(tr, f"G{r}", bearing_text(f"F{r}"))
    put(tr, f"H{r}", f'=ROUND(AVERAGEIFS({rng("K")},{rng("P")},A{r},{rng("V")},"Yes"),3)', N3)
    put(tr, f"I{r}", f"=ROUND(H{r}*COS(RADIANS(F{r})),3)", N3); put(tr, f"J{r}", f"=ROUND(H{r}*SIN(RADIANS(F{r})),3)", N3)
    put(tr, f"K{r}", f"=ROUND(-$I$11*H{r}/$H$11,3)", N3); put(tr, f"L{r}", f"=ROUND(-$J$11*H{r}/$H$11,3)", N3)
    put(tr, f"M{r}", f"=ROUND(I{r}+K{r},3)", N3); put(tr, f"N{r}", f"=ROUND(J{r}+L{r},3)", N3)
    put(tr, f"O{r}", "=ROUND(Parameters!$B$4+M4,3)" if k == 0 else f"=ROUND(O{r - 1}+M{r},3)", N3)
    put(tr, f"P{r}", "=ROUND(Parameters!$B$5+N4,3)" if k == 0 else f"=ROUND(P{r - 1}+N{r},3)", N3)
put(tr, "A11", "Totals", bold=True); put(tr, "D11", "=SUM(D4:D10)"); put(tr, "E11", "=SUM(E4:E10)")
for col in "HIJKLMN": put(tr, f"{col}11", f"=ROUND(SUM({col}4:{col}10),3)", N3)
put(tr, "A13", "Closure, unadjusted", bold=True)
put(tr, "A14", "Perimeter (ft)"); put(tr, "B14", "=H11", N3)
put(tr, "A15", "Latitude misclosure (ft)"); put(tr, "B15", "=I11", N3)
put(tr, "A16", "Departure misclosure (ft)"); put(tr, "B16", "=J11", N3)
put(tr, "A17", "Linear error of closure (ft)"); put(tr, "B17", "=ROUND(SQRT(B15^2+B16^2),2)", N2)
put(tr, "A18", "Precision of closure, one part in"); put(tr, "B18", "=ROUNDDOWN(B14/B17,-2)", NC)
put(tr, "A19", "Tract classification on the field dates"); put(tr, "B19", "=Parameters!B8")
put(tr, "A20", "Firm standard for that class, one part in"); put(tr, "B20", '=IF(B19="Urban",Parameters!B6,Parameters!B7)', NC)
put(tr, "A21", "Closure test"); put(tr, "B21", '=IF(B18>=B20,"Meets the standard","Does not meet the standard")')
put(tr, "A23", "Station coordinates, adjusted", bold=True)
header(tr, 24, ["Station", "Northing (ft)", "Easting (ft)"], 16)
put(tr, "A25", "T1"); put(tr, "B25", "=Parameters!B4", N3); put(tr, "C25", "=Parameters!B5", N3)
for k, leg in enumerate(LEGS):
    r = 26 + k; put(tr, f"A{r}", leg.split("-")[1] if k < 6 else "T1 on return"); put(tr, f"B{r}", f"=O{4 + k}", N3); put(tr, f"C{r}", f"=P{4 + k}", N3)
put(tr, "A34", "Every pair, the forward shot against its reverse under firm standards 1.1", bold=True)
header(tr, 35, ["Leg", "Pair", "Forward distance (ft)", "Reverse distance (ft)", "Difference in distance (ft)", "Forward azimuth", "Reverse azimuth, turned", "Difference in bearing (seconds)", "Test"], 48)
PAIRS = [("T1-T7", 1), ("T7-T2", 1), ("T2-T3", 1), ("T2-T3", 2), ("T3-T4", 1), ("T3-T4", 2), ("T4-T5", 1), ("T5-T6", 1), ("T5-T6", 2), ("T6-T1", 1)]
for k, (leg, pr) in enumerate(PAIRS):
    r = 36 + k
    put(tr, f"A{r}", leg); put(tr, f"B{r}", pr)
    put(tr, f"C{r}", f'=AVERAGEIFS({rng("K")},{rng("P")},A{r},{rng("S")},B{r},{rng("Q")},"Forward")', N2)
    put(tr, f"D{r}", f'=AVERAGEIFS({rng("K")},{rng("P")},A{r},{rng("S")},B{r},{rng("Q")},"Reverse")', N2)
    put(tr, f"E{r}", f"=ROUND(ABS(C{r}-D{r}),3)", N3)
    put(tr, f"F{r}", f'=AVERAGEIFS({rng("R")},{rng("P")},A{r},{rng("S")},B{r},{rng("Q")},"Forward")', N6)
    put(tr, f"G{r}", f'=AVERAGEIFS({rng("R")},{rng("P")},A{r},{rng("S")},B{r},{rng("Q")},"Reverse")', N6)
    put(tr, f"H{r}", f"=ROUND(MIN(ABS(F{r}-G{r}),360-ABS(F{r}-G{r}))*Parameters!$B$18,0)", N0)
    put(tr, f"I{r}", f'=IF(OR(E{r}>Parameters!$B$19,H{r}>Parameters!$B$20),"Pair in error","Pair stands")')
put(tr, "A47", "Legs shot twice, the pairs compared under firm standards 1.1", bold=True)
header(tr, 48, ["Leg", "First pair, mean distance (ft)", "Second pair, mean distance (ft)", "Difference in distance (ft)", "First pair, mean azimuth", "Second pair, mean azimuth", "Difference in bearing (seconds)", "Pairs in error on the leg", "Test"], 48)
for k, leg in enumerate(["T2-T3", "T3-T4", "T5-T6"]):
    r = 49 + k
    put(tr, f"A{r}", leg)
    put(tr, f"B{r}", f'=ROUND(AVERAGEIFS({rng("K")},{rng("P")},A{r},{rng("S")},1),3)', N3); put(tr, f"C{r}", f'=ROUND(AVERAGEIFS({rng("K")},{rng("P")},A{r},{rng("S")},2),3)', N3)
    put(tr, f"D{r}", f"=ROUND(ABS(B{r}-C{r}),3)", N3)
    put(tr, f"E{r}", f'=ROUND(MOD(DEGREES(ATAN2(SUMIFS({rng("T")},{rng("P")},A{r},{rng("S")},1),SUMIFS({rng("U")},{rng("P")},A{r},{rng("S")},1)))+Parameters!$B$30,360),6)', N6)
    put(tr, f"F{r}", f'=ROUND(MOD(DEGREES(ATAN2(SUMIFS({rng("T")},{rng("P")},A{r},{rng("S")},2),SUMIFS({rng("U")},{rng("P")},A{r},{rng("S")},2)))+Parameters!$B$30,360),6)', N6)
    put(tr, f"G{r}", f"=ROUND(MIN(ABS(E{r}-F{r}),360-ABS(E{r}-F{r}))*Parameters!$B$18,0)", N0)
    put(tr, f"H{r}", f'=COUNTIFS($A$36:$A$45,A{r},$I$36:$I$45,"Pair in error")', N0)
    put(tr, f"I{r}", f'=IF(H{r}>0,"A pair in error is rejected, the other pair carries the leg",IF(AND(D{r}<=Parameters!$B$19,G{r}<=Parameters!$B$20),"Agree, meaned together","Do not agree, the pair at fault set aside"))')
put(tr, "A53", "Closure with other readings of the doubled legs, the other legs as above", bold=True)
header(tr, 54, ["Reading", "Mean azimuth", "Mean distance (ft)", "Latitude (ft)", "Departure (ft)", "Latitude misclosure (ft)", "Departure misclosure (ft)", "Linear error (ft)", "Precision, one part in"], 32)
ALT = [("T5-T6, the first pair alone", "T5-T6", 1, 9), ("T5-T6, both pairs meaned together", "T5-T6", None, 9), ("T3-T4, the pair in error alone", "T3-T4", 1, 7), ("T3-T4, both pairs meaned together", "T3-T4", None, 7)]
for k, (label, leg, pr, legrow) in enumerate(ALT):
    r = 55 + k; crit = f',{rng("S")},{pr}' if pr else ""
    put(tr, f"A{r}", label)
    put(tr, f"B{r}", f'=ROUND(MOD(DEGREES(ATAN2(SUMIFS({rng("T")},{rng("P")},"{leg}"{crit}),SUMIFS({rng("U")},{rng("P")},"{leg}"{crit})))+Parameters!$B$30,360),6)', N6)
    put(tr, f"C{r}", f'=ROUND(AVERAGEIFS({rng("K")},{rng("P")},"{leg}"{crit}),3)', N3)
    put(tr, f"D{r}", f"=ROUND(C{r}*COS(RADIANS(B{r})),3)", N3); put(tr, f"E{r}", f"=ROUND(C{r}*SIN(RADIANS(B{r})),3)", N3)
    put(tr, f"F{r}", f"=ROUND($I$11-$I${legrow}+D{r},3)", N3); put(tr, f"G{r}", f"=ROUND($J$11-$J${legrow}+E{r},3)", N3)
    put(tr, f"H{r}", f"=ROUND(SQRT(F{r}^2+G{r}^2),2)", N2); put(tr, f"I{r}", f"=ROUNDDOWN(($H$11-$H${legrow}+C{r})/H{r},-2)", NC)
put(tr, "A60", "Each leg is the mean of every shot marked used on the Field Notes tab, the reverse shots turned through 180 degrees and the bearings meaned as directions, under firm standards 1.1. The precision divides the perimeter by the linear error as reported to the hundredth, rounded down to the hundred, under firm standards 1.2. The closure is unadjusted, and the compass rule is applied afterwards for the station coordinates, under firm standards 1.4.", wrap=True)
tr.row_dimensions[60].height = 48

# ============================================================ Ties
ti = sheet("Ties", {"A": 8, "B": 60, "C": 9, "D": 7, "E": 13, "F": 12, "G": 14, "H": 14, "I": 11, "J": 11, "K": 13, "L": 13},
           "Monument and fence ties, reduced from the adjusted station coordinates")
header(ti, 3, ["Point", "What was tied", "Station", "Shot", "Azimuth", "Distance used (ft)", "Station northing", "Station easting", "Latitude (ft)", "Departure (ft)", "Northing (ft)", "Easting (ft)"], 32)
WHAT = {"101": "Iron pin, cap PLS 1188, southwest corner at Stanhope Road", "102": "Iron pin, cap PLS 2207, northwest corner at the Hutchins line",
        "103": "Rebar, cap PLS 2207, at the northeast corner", "104": "Stone with chiseled cross, southeast corner", "105": "Stone with drill hole, angle point in the Farley line",
        "106": "Iron pipe, northwest corner of the Ballinger tract", "107": "Iron pin, cap PLS 2641, set by the crew at the northeast corner on September 30",
        "201": "Hutchins fence post", "202": "Hutchins fence post", "203": "Hutchins fence corner post, meeting the Ballinger fence",
        "204": "Ballinger fence post", "205": "Ballinger fence post", "206": "Ballinger fence post", "207": "Farley fence post", "208": "Farley fence post", "209": "Farley fence post"}
TIE_ORDER = ["101", "102", "103", "104", "105", "106", "107", "201", "202", "203", "204", "205", "206", "207", "208", "209"]
TROW = {p: 4 + k for k, p in enumerate(TIE_ORDER)}
for p, r in TROW.items():
    put(ti, f"A{r}", p); put(ti, f"B{r}", WHAT[p])
    put(ti, f"C{r}", f"=INDEX({rng('M')},MATCH(A{r},{rng('N')},0))"); put(ti, f"D{r}", f"=INDEX({rng('A')},MATCH(A{r},{rng('N')},0))")
    put(ti, f"E{r}", f"=INDEX({rng('O')},MATCH(A{r},{rng('N')},0))", N6); put(ti, f"F{r}", f"=INDEX({rng('Y')},MATCH(A{r},{rng('N')},0))", N2)
    put(ti, f"G{r}", f"=INDEX(Traverse!$B$25:$B$31,MATCH(C{r},Traverse!$A$25:$A$31,0))", N3); put(ti, f"H{r}", f"=INDEX(Traverse!$C$25:$C$31,MATCH(C{r},Traverse!$A$25:$A$31,0))", N3)
    put(ti, f"I{r}", f"=ROUND(F{r}*COS(RADIANS(E{r})),3)", N3); put(ti, f"J{r}", f"=ROUND(F{r}*SIN(RADIANS(E{r})),3)", N3)
    put(ti, f"K{r}", f"=ROUND(G{r}+I{r},3)", N3); put(ti, f"L{r}", f"=ROUND(H{r}+J{r},3)", N3)
put(ti, "A21", "Checks against the record", bold=True)
header(ti, 22, ["Check", "", "Measured (ft)", "Record (ft)", "Difference (ft)"], 32)
def tdist(p, q): return f"=ROUND(SQRT((K{TROW[p]}-K{TROW[q]})^2+(L{TROW[p]}-L{TROW[q]})^2),2)"
CHECKS = [("Pin at corner 2 to the mark coded IRF, the rebar", "102", "103", "=Parameters!B27"), ("Pin at corner 2 to the fence corner post, point 203", "102", "203", None),
          ("Pin at corner 2 to the pin the crew set, point 107", "102", "107", None), ("Stone at corner 4 to the iron pipe, the Ballinger west line", "104", "106", "=Parameters!B28")]
for k, (label, p, q, rec) in enumerate(CHECKS):
    r = 23 + k; put(ti, f"A{r}", label); put(ti, f"C{r}", tdist(p, q), N2)
    if rec: put(ti, f"D{r}", rec, N1); put(ti, f"E{r}", f"=ROUND(C{r}-D{r},2)", N2)
put(ti, "A28", "Every tie is reduced from the adjusted coordinates of the station the field book names, on the azimuth observed and the distance as corrected under firm standards 1.5: the prism correction on every tie, and the taped offset on point 105.", wrap=True)
ti.row_dimensions[28].height = 32

# ============================================================ Deed
de = sheet("Deed", {"A": 66, "B": 14, "C": 9, "D": 9, "E": 5, "F": 12, "G": 13, "H": 12, "I": 12, "J": 13, "K": 16, "L": 13, "M": 20, "N": 13, "O": 12, "P": 12, "Q": 18, "R": 20},
           "Deed Book 412, Page 233, reduced on its own calls as transcribed, and compared with the field")
header(de, 3, ["Call", "NS", "Degrees", "Minutes", "EW", "Deed distance (ft)", "Deed azimuth, magnetic 1962", "Latitude (ft)", "Departure (ft)", "Rotated azimuth, grid", "Rotated bearing", "Measured azimuth", "Measured bearing", "Measured distance (ft)", "Bearing difference (minutes)", "Distance difference (ft)", "Test against the tolerance", "Finding under 3.3"], 48)
NAMES = ["1-2", "2-3", "3-4", "4-5", "5-1"]
for k, (ns, d, m, ew, dd) in enumerate(DEED):
    r = 4 + k
    put(de, f"A{r}", NAMES[k]); put(de, f"B{r}", ns); put(de, f"C{r}", d); put(de, f"D{r}", m); put(de, f"E{r}", ew); put(de, f"F{r}", dd, N1)
    put(de, f"G{r}", f'=ROUND(IF(AND(B{r}="N",E{r}="E"),(C{r}+D{r}/Parameters!$B$17),IF(AND(B{r}="S",E{r}="E"),180-(C{r}+D{r}/Parameters!$B$17),IF(AND(B{r}="S",E{r}="W"),180+(C{r}+D{r}/Parameters!$B$17),360-(C{r}+D{r}/Parameters!$B$17)))),6)', N6)
    put(de, f"H{r}", f"=ROUND(F{r}*COS(RADIANS(G{r})),3)", N3); put(de, f"I{r}", f"=ROUND(F{r}*SIN(RADIANS(G{r})),3)", N3)
    put(de, f"J{r}", f"=ROUND(MOD(G{r}+$B$37,360),6)", N6); put(de, f"K{r}", bearing_text(f"J{r}", seconds=False))
    put(de, f"L{r}", f"=Corners!F{28 + k}", N6); put(de, f"M{r}", bearing_text(f"L{r}")); put(de, f"N{r}", f"=Corners!G{28 + k}", N2)
    put(de, f"O{r}", f"=ROUND((L{r}-J{r})*Parameters!$B$17,0)", N0); put(de, f"P{r}", f"=ROUND(N{r}-F{r},2)", N2)
    put(de, f"Q{r}", f'=IF(OR(ABS(P{r})>Parameters!$B$13,ABS(O{r})>Parameters!$B$14),"Out of tolerance","Within tolerance")')
    put(de, f"R{r}", f'=IF(Q{r}="Out of tolerance","Error in the deed","Call holds")')
put(de, "A9", "Totals", bold=True); put(de, "F9", "=ROUND(SUM(F4:F8),1)", N1); put(de, "H9", "=ROUND(SUM(H4:H8),3)", N3); put(de, "I9", "=ROUND(SUM(I4:I8),3)", N3)
put(de, "A11", "Deed closure on its own calls, as transcribed", bold=True)
put(de, "A12", "Deed perimeter (ft)"); put(de, "B12", "=F9", N1)
put(de, "A13", "Deed latitude misclosure (ft)"); put(de, "B13", "=H9", N3)
put(de, "A14", "Deed departure misclosure (ft)"); put(de, "B14", "=I9", N3)
put(de, "A15", "Deed linear misclosure (ft)"); put(de, "B15", "=ROUND(SQRT(B13^2+B14^2),2)", N2)
put(de, "A16", "Deed misclosure per 1,000 ft of perimeter"); put(de, "B16", "=ROUND(B15/B12*Parameters!$B$12,2)", N2)
put(de, "A17", "Deed precision, one part in"); put(de, "B17", "=ROUND(B12/B15,0)", NC)
put(de, "A18", "Deed description test"); put(de, "B18", '=IF(B16>Parameters!$B$11,"Defect in the description","Within the tolerance of the original survey")')
put(de, "A19", "Azimuth of the deed misclosure"); put(de, "B19", "=ROUND(MOD(DEGREES(ATAN2(B13,B14)),360),6)", N6)
put(de, "A20", "Bearing of the deed misclosure"); put(de, "B20", bearing_text("B19", seconds=False))
put(de, "A22", "The deed with the record's figures in place of the transcription's", bold=True)
put(de, "A23", "Distance of the 3-4 call in the 1978 deed of trust (ft)"); put(de, "B23", "=Parameters!B26", N1)
put(de, "A24", "Degrees of the 5-1 bearing with its two digits exchanged"); put(de, "B24", SLIP[1])
put(de, "A25", "Minutes of the 5-1 bearing, as transcribed"); put(de, "B25", "=D8")
put(de, "A26", "Azimuth of the 5-1 call so read, magnetic 1962"); put(de, "B26", "=ROUND(360-(B24+B25/Parameters!$B$17),6)", N6)
put(de, "A27", "Deed misclosure with 592.7 feet in the 3-4 call (ft)"); put(de, "B27", "=ROUND(SQRT((H9-H6+ROUND(B23*COS(RADIANS(G6)),3))^2+(I9-I6+ROUND(B23*SIN(RADIANS(G6)),3))^2),2)", N2)
put(de, "A28", "Deed misclosure with N 43° 31' W in the 5-1 call (ft)"); put(de, "B28", "=ROUND(SQRT((H9-H8+ROUND(F8*COS(RADIANS(B26)),3))^2+(I9-I8+ROUND(F8*SIN(RADIANS(B26)),3))^2),2)", N2)
put(de, "A29", "Deed misclosure with both figures (ft)"); put(de, "B29", "=ROUND(SQRT((H9-H6-H8+ROUND(B23*COS(RADIANS(G6)),3)+ROUND(F8*COS(RADIANS(B26)),3))^2+(I9-I6-I8+ROUND(B23*SIN(RADIANS(G6)),3)+ROUND(F8*SIN(RADIANS(B26)),3))^2),2)", N2)
put(de, "A31", "Rotation, deed magnetic bearings to the grid, under firm standards 3.2", bold=True)
put(de, "A32", "Rotation line, the one deed course with a found original monument at each end"); put(de, "B32", "Stone at corner 4 to stone at corner 5, the 4-5 call")
put(de, "A33", "Deed azimuth of the 4-5 call"); put(de, "B33", "=G7", N6)
put(de, "A34", "Measured azimuth, stone to stone"); put(de, "B34", "=ROUND(MOD(DEGREES(ATAN2(Corners!G8-Corners!G7,Corners!H8-Corners!H7)),360),6)", N6)
put(de, "A35", "Rotation (minutes of arc, to the nearest minute)"); put(de, "B35", "=ROUND((B34-B33)*Parameters!$B$17,0)", N0)
put(de, "A36", "Rotation, degrees and minutes"); put(de, "B36", '=TEXT(INT(B35/Parameters!$B$17),"0")&"° "&TEXT(MOD(B35,Parameters!$B$17),"00")&"\' east of the deed bearings"')
put(de, "A37", "Rotation applied (decimal degrees)"); put(de, "B37", "=ROUND(B35/Parameters!$B$17,6)", N6)
put(de, "A38", "Rotation the road course would give, pin to pin, the 1-2 call (minutes of arc)"); put(de, "B38", "=ROUND((ROUND(MOD(DEGREES(ATAN2(Corners!G5-Corners!G4,Corners!H5-Corners!H4)),360),6)-G4)*Parameters!$B$17,0)", N0)
put(de, "A39", "Road course less the 4-5 course (minutes)"); put(de, "B39", "=B38-B35", N0)
put(de, "A41", "Comparison", bold=True)
put(de, "A42", "Calls out of tolerance"); put(de, "B42", '=COUNTIF(Q4:Q8,"Out of tolerance")', N0)
put(de, "A43", "Calls in error in the deed, both ends held or set"); put(de, "B43", '=COUNTIF(R4:R8,"Error in the deed")', N0)
put(de, "A44", "3-4 call, deed distance as transcribed (ft)"); put(de, "B44", "=F6", N1)
put(de, "A45", "3-4 call, measured distance the plat carries (ft)"); put(de, "B45", "=N6", N2)
put(de, "A46", "3-4 call, measured less the 1978 figure (ft)"); put(de, "B46", "=ROUND(B45-B23,2)", N2)
put(de, "A47", "5-1 call, rotated bearing as transcribed"); put(de, "B47", "=K8")
put(de, "A48", "5-1 call, rotated bearing with the digits restored"); put(de, "B48", "=ROUND(MOD(B26+B37,360),6)", N6)
put(de, "A49", "5-1 call, that bearing in degrees and minutes"); put(de, "B49", bearing_text("B48", seconds=False))
put(de, "A50", "5-1 call, measured bearing"); put(de, "B50", "=M8")
put(de, "A51", "5-1 call, measured less restored (minutes)"); put(de, "B51", "=ROUND((L8-B48)*Parameters!$B$17,0)", N0)
put(de, "A52", "Finding on the calls in error"); put(de, "B52", '=IF(AND(B42=2,B43=2),"Two errors in the deed, the 3-4 distance and the 5-1 bearing; the measured courses stand","Review")')
put(de, "A54", "The deed is reduced on its magnetic bearings unrotated, as transcribed, under firm standards 3.1. The rotation comes from the 4-5 call, the one course with a found original monument at each end, under firm standards 3.2, and it is applied to every call before the comparison in columns J to R, under firm standards 3.3. The 2-3 course ends at the corner to be set, which lies on the rotated deed bearing by construction.", wrap=True)
de.row_dimensions[54].height = 48

# ============================================================ Corners
co = sheet("Corners", {"A": 10, "B": 16, "C": 34, "D": 44, "E": 64, "F": 30, "G": 13, "H": 13, "I": 13, "J": 13, "K": 12, "L": 26},
           "Monuments found, the test of each later mark, the crew's pin, and the corners as held or set")
header(co, 3, ["Point", "Corner", "Deed call for the monument", "Found in the field", "Record of the mark", "Class under firm standards 3.5 to 3.7", "Northing (ft)", "Easting (ft)", "Test position northing", "Test position easting", "Offset from the test position (ft)", "Disposition"], 48)
CROWS = [
    ("101", "1", "Iron pin on the east margin of Stanhope Road", "5/8-inch iron pin, plastic cap PLS 1188", "Plat Cabinet B, Slide 212 (1994): no monument found, pin set at the deed distance from the stone at the angle point", "Later monument", "B15", "B16"),
    ("102", "2", "Iron pin, southwest corner of Hutchins", "1/2-inch iron pin, aluminum cap PLS 2207, old bend", "Plat Cabinet D, Slide 57 (2008): pin of the Tolliver survey found in place, straightened and capped where it stood", "Original, capped in place", None, None),
    ("103", "3", "Iron pin in the west line of Ballinger", "1/2-inch rebar, aluminum cap PLS 2207", "Plat Cabinet D, Slide 57 (2008): no monument found, rebar set 588.8 feet from the southwest corner of Hutchins", "Later monument", "B25", "B26"),
    ("104", "4", "Stone, southeast corner", "Stone, 8 by 10 inches, chiseled cross", "Plat Cabinet B, Slide 212 (1994): found upright; called for in the Cope and the Ballinger deeds", "Original", None, None),
    ("105", "5", "Stone in the Farley line", "Stone, 6 by 8 inches, drill hole, leaning in the fence row", "Plat Cabinet B, Slide 212 (1994): found in the fence row, leaning, and left as found", "Original", None, None),
    ("106", "Ballinger NW", "Iron pipe, Deed Book 377, Page 102", "1-inch iron pipe, open top", "Called for in the Ballinger deed; no survey of the Ballinger tract is of record", "Original of the adjoiner's deed", None, None),
    ("107", "3, crew's pin", "None; set September 30, 2026", "5/8-inch iron pin, cap PLS 2641, set by the crew", "Field book: set where the 2-3 and 3-4 calls meet when the deed is turned on the road course, before the loop was closed", "Provisional mark under 3.7", "B25", "B26"),
]
for k, (p, c, call, found, rec, cls, tn, te) in enumerate(CROWS):
    r = 4 + k
    put(co, f"A{r}", p); put(co, f"B{r}", c); put(co, f"C{r}", call, wrap=True); put(co, f"D{r}", found, wrap=True); put(co, f"E{r}", rec, wrap=True); put(co, f"F{r}", cls, wrap=True)
    put(co, f"G{r}", f"=Ties!$K${TROW[p]}", N3); put(co, f"H{r}", f"=Ties!$L${TROW[p]}", N3)
    co.row_dimensions[r].height = 48
    if tn:
        put(co, f"I{r}", f"={tn}", N3); put(co, f"J{r}", f"={te}", N3); put(co, f"K{r}", f"=ROUND(SQRT((G{r}-I{r})^2+(H{r}-J{r})^2),2)", N2)
        if p == "107": put(co, f"L{r}", f'=IF(K{r}<=0.005,"Stands at the corner","To be reset at the corner")')
        else: put(co, f"L{r}", f'=IF(K{r}<=Parameters!$B$15,"Held as the corner","Found, not held")')
    else:
        put(co, f"L{r}", "Held")
put(co, "A12", "Test position of corner 1, firm standards 3.7: the 1-2 call reversed and rotated, at the deed distance, from the pin at corner 2, the nearest held original monument reached by a call within tolerance (the 5-1 call being in error)", bold=True)
put(co, "A13", "Rotated azimuth of the 1-2 call, reversed"); put(co, "B13", "=ROUND(MOD(Deed!J4+180,360),6)", N6)
put(co, "A14", "Deed distance of the 1-2 call (ft)"); put(co, "B14", "=Deed!F4", N1)
put(co, "A15", "Northing (ft)"); put(co, "B15", "=ROUND(G5+B14*COS(RADIANS(B13)),3)", N3)
put(co, "A16", "Easting (ft)"); put(co, "B16", "=ROUND(H5+B14*SIN(RADIANS(B13)),3)", N3)
put(co, "A18", "Position of corner 3, firm standards 3.7: the rotated 2-3 course from corner 2, met with the Ballinger west line run from the stone at corner 4 to the iron pipe", bold=True)
put(co, "A19", "Rotated azimuth of the 2-3 call"); put(co, "B19", "=Deed!J5", N6)
put(co, "A20", "Azimuth of the Ballinger west line, stone to pipe"); put(co, "B20", "=ROUND(MOD(DEGREES(ATAN2(G9-G7,H9-H7)),360),6)", N6)
put(co, "A21", "Distance from corner 2 to the meeting point (ft)"); put(co, "B21", "=ROUND(((H7-H5)*COS(RADIANS(B20))-(G7-G5)*SIN(RADIANS(B20)))/SIN(RADIANS(B19-B20)),3)", N3)
put(co, "A22", "Deed distance of the 2-3 call, which gives way (ft)"); put(co, "B22", "=Deed!F5", N1)
put(co, "A23", "Meeting point less the deed distance (ft)"); put(co, "B23", "=ROUND(B21-B22,2)", N2)
put(co, "A24", "Where the rotated 2-3 course alone would put the corner, at the deed distance: northing"); put(co, "B24", "=ROUND(G5+B22*COS(RADIANS(B19)),3)", N3)
put(co, "A25", "Northing (ft)"); put(co, "B25", "=ROUND(G5+B21*COS(RADIANS(B19)),3)", N3)
put(co, "A26", "Easting (ft)"); put(co, "B26", "=ROUND(H5+B21*SIN(RADIANS(B19)),3)", N3)
header(co, 27, ["Corner", "Status", "Northing (ft)", "Easting (ft)", "Course from this corner", "Measured azimuth", "Measured distance (ft)", "Measured bearing"], 32)
STAT = {1: ('=IF(L4="Held as the corner","Found, later monument, held","To be set")', '=IF(L4="Held as the corner",G4,I4)', '=IF(L4="Held as the corner",H4,J4)'),
        2: ('="Found, original monument, held"', "=G5", "=H5"),
        3: ('=IF(L6="Held as the corner","Found, later monument, held","To be set")', '=IF(L6="Held as the corner",G6,I6)', '=IF(L6="Held as the corner",H6,J6)'),
        4: ('="Found, original monument, held"', "=G7", "=H7"), 5: ('="Found, original monument, held"', "=G8", "=H8")}
for n in range(1, 6):
    r = 27 + n; nxt = 27 + (n % 5) + 1
    put(co, f"A{r}", n); put(co, f"B{r}", STAT[n][0]); put(co, f"C{r}", STAT[n][1], N3); put(co, f"D{r}", STAT[n][2], N3); put(co, f"E{r}", NAMES[n - 1])
    put(co, f"F{r}", f"=ROUND(MOD(DEGREES(ATAN2(C{nxt}-C{r},D{nxt}-D{r})),360),6)", N6); put(co, f"G{r}", f"=ROUND(SQRT((C{nxt}-C{r})^2+(D{nxt}-D{r})^2),2)", N2); put(co, f"H{r}", bearing_text(f"F{r}"))
put(co, "A34", "Counts", bold=True)
put(co, "A35", "Original monuments of the tract found and held"); put(co, "B35", '=COUNTIF(F4:F8,"Original*")', N0)
put(co, "A36", "Later monuments held as the corner"); put(co, "B36", '=COUNTIFS(F4:F8,"Later monument",L4:L8,"Held as the corner")', N0)
put(co, "A37", "Later monuments found and not held"); put(co, "B37", '=COUNTIFS(F4:F8,"Later monument",L4:L8,"Found, not held")', N0)
put(co, "A38", "Corners to be set"); put(co, "B38", '=COUNTIF(B28:B32,"To be set")', N0)
put(co, "A39", "Corner to be set"); put(co, "B39", '=INDEX(A28:A32,MATCH("To be set",B28:B32,0))', N0)
put(co, "A40", "Distance the crew's pin is to be moved to the corner (ft)"); put(co, "B40", "=K10", N2)
put(co, "A41", "Rebar at corner 3, offset from the corner under the road-course rotation (ft)"); put(co, "B41", "=ROUND(SQRT((G6-(G5+B21*COS(RADIANS(Deed!G5+Deed!B38/Parameters!$B$17))))^2+(H6-(H5+B21*SIN(RADIANS(Deed!G5+Deed!B38/Parameters!$B$17))))^2),2)", N2)
put(co, "A43", "The pin at corner 2 and the stones at corners 4 and 5 are original monuments under firm standards 3.5 and are held. The pin at corner 1 and the rebar at corner 3 are later monuments under 3.6, each tested against the position the corner takes under 3.7. The crew's pin at corner 3 is a provisional mark under 3.7 and is moved to the position the analysis gives.", wrap=True)
co.row_dimensions[43].height = 48

# ============================================================ Area
ar = sheet("Area", {"A": 40, "B": 16, "C": 16, "D": 26, "E": 26, "F": 34}, "Area by the coordinate method on the corners as held or set")
header(ar, 3, ["Corner", "Northing (ft)", "Easting (ft)", "Cross product N(i) x E(i+1)", "Cross product N(i+1) x E(i)", "Status"], 16)
for n in range(1, 6):
    r = 3 + n; nxt = 3 + (n % 5) + 1
    put(ar, f"A{r}", n); put(ar, f"B{r}", f"=Corners!C{27 + n}", N3); put(ar, f"C{r}", f"=Corners!D{27 + n}", N3)
    put(ar, f"D{r}", f"=ROUND(B{r}*C{nxt},3)", "#,##0.000"); put(ar, f"E{r}", f"=ROUND(B{nxt}*C{r},3)", "#,##0.000"); put(ar, f"F{r}", f"=Corners!B{27 + n}")
put(ar, "A9", "Totals", bold=True); put(ar, "D9", "=ROUND(SUM(D4:D8),3)", "#,##0.000"); put(ar, "E9", "=ROUND(SUM(E4:E8),3)", "#,##0.000")
put(ar, "A11", "Area (sq ft)"); put(ar, "B11", "=ROUND(ABS(D9-E9)/2,0)", NC)
put(ar, "A12", "Area (acres)"); put(ar, "B12", "=ROUND(B11/Parameters!$B$9,3)", N3)
put(ar, "A13", "Deed acreage recited"); put(ar, "B13", "=Parameters!B10", N2)
put(ar, "A14", "Difference, computed less deed (acres)"); put(ar, "B14", "=ROUND(B12-B13,3)", N3)
put(ar, "A15", "Difference (sq ft)"); put(ar, "B15", "=ROUND(B11-B13*Parameters!$B$9,0)", N0)
put(ar, "A17", "The corners are the five corners as held or set on the Corners tab, under firm standards 2.1. The deed recites its acreage more or less, and area is the last of the calls under firm standards 3.4.", wrap=True)
ar.row_dimensions[17].height = 32

# ============================================================ Fences
fe = sheet("Fences", {"A": 10, "B": 16, "C": 10, "D": 13, "E": 13, "F": 14, "G": 13, "H": 13, "I": 13, "J": 13, "K": 13, "L": 22}, "Fence ties against the boundary as computed")
header(fe, 3, ["Point", "Fence", "Boundary course", "From corner northing", "From corner easting", "Course azimuth", "Course length (ft)", "Post northing", "Post easting", "Distance along the course (ft)", "Offset, inside the tract positive (ft)", "Side"], 48)
FPOSTS = [("201", "Hutchins", 2), ("202", "Hutchins", 2), ("203", "Hutchins", 2), ("204", "Ballinger", 3), ("205", "Ballinger", 3), ("206", "Ballinger", 3), ("207", "Farley", 4), ("208", "Farley", 4), ("209", "Farley", 4)]
for k, (p, fence, cn) in enumerate(FPOSTS):
    r = 4 + k; cr = 27 + cn
    put(fe, f"A{r}", p); put(fe, f"B{r}", fence); put(fe, f"C{r}", NAMES[cn - 1])
    put(fe, f"D{r}", f"=Corners!$C${cr}", N3); put(fe, f"E{r}", f"=Corners!$D${cr}", N3); put(fe, f"F{r}", f"=Corners!$F${cr}", N6); put(fe, f"G{r}", f"=Corners!$G${cr}", N2)
    put(fe, f"H{r}", f"=Ties!$K${TROW[p]}", N3); put(fe, f"I{r}", f"=Ties!$L${TROW[p]}", N3)
    put(fe, f"J{r}", f"=ROUND((H{r}-D{r})*COS(RADIANS(F{r}))+(I{r}-E{r})*SIN(RADIANS(F{r})),2)", N2)
    put(fe, f"K{r}", f"=ROUND((I{r}-E{r})*COS(RADIANS(F{r}))-(H{r}-D{r})*SIN(RADIANS(F{r})),2)", N2)
    put(fe, f"L{r}", f'=IF(K{r}>0,"Inside the tract",IF(K{r}<0,"Outside the tract","On the line"))')
header(fe, 15, ["Fence", "Adjoining owner", "Boundary course", "Posts tied", "Greatest offset inside the tract (ft)", "Greatest offset outside the tract (ft)", "Finding under firm standards 3.8"], 48)
for k, (fence, course, rows) in enumerate([("Hutchins", "2-3", "K4:K6"), ("Ballinger", "3-4", "K7:K9"), ("Farley", "4-5", "K10:K12")]):
    r = 16 + k
    put(fe, f"A{r}", f"{fence} fence"); put(fe, f"B{r}", fence); put(fe, f"C{r}", course); put(fe, f"D{r}", f"=COUNTIF($B$4:$B$12,B{r})", N0)
    put(fe, f"E{r}", f"=MAX(0,MAX({rows}))", N2); put(fe, f"F{r}", f"=MAX(0,-MIN({rows}))", N2)
    put(fe, f"G{r}", f'=IF(E{r}>Parameters!$B$16,"Encroachment","Occupation note only")')
put(fe, "A20", "Fences reported as encroachments"); put(fe, "B20", '=COUNTIF(G16:G18,"Encroachment")', N0)
put(fe, "A22", "The tract lies to the right of each course in the order 1, 2, 3, 4, 5, so a post to the right of its course stands inside the tract. Offsets are at right angles to the boundary as computed, under firm standards 3.8.", wrap=True)
fe.row_dimensions[22].height = 32

# ============================================================ Findings (first sheet)
fi = sheet("Findings", {"A": 62, "B": 36, "C": 16}, "Tract 7 boundary analysis, job 26-2214, Estate of Wendell R. Cope")
put(fi, "A2", "Prepared for Ellen Vance, who seals the plat, by the office; report prepared October 29, 2026")
put(fi, "A3", "Deed Book 412, Page 233, Putnam County, Tennessee; field work September 29 and 30, 2026")
header(fi, 5, ["Finding", "Value", "Read from"], 16)
ROWS = [
    ("Traverse closure", None, None, None),
    ("Perimeter of the traverse (ft)", "=Traverse!B14", "Traverse", N3), ("Latitude misclosure (ft)", "=Traverse!B15", "Traverse", N3), ("Departure misclosure (ft)", "=Traverse!B16", "Traverse", N3),
    ("Linear error of closure (ft)", "=Traverse!B17", "Traverse", N2), ("Precision of closure, one part in", "=Traverse!B18", "Traverse", NC),
    ("Traverse shots set aside or rejected", "=Traverse!E11", "Traverse", N0), ("Tract classification on the field dates", "=Traverse!B19", "Parameters", None),
    ("Firm standard for that class, one part in", "=Traverse!B20", "Parameters", NC), ("Closure test", "=Traverse!B21", "Traverse", None),
    ("Notes file and ties", None, None, None),
    ("Prism correction on every tie (ft)", "=Parameters!B24", "Parameters", N2), ("Offset added to the tie on point 105 (ft)", "=Parameters!B25", "Parameters", N2),
    ("Changes made to the notes file", "=COUNTA('Field Notes'!Z27:Z29)", "Field Notes", N0),
    ("Deed comparison", None, None, None),
    ("Deed linear misclosure on its own calls, as transcribed (ft)", "=Deed!B15", "Deed", N2), ("Deed misclosure per 1,000 ft of perimeter", "=Deed!B16", "Deed", N2),
    ("Deed description test", "=Deed!B18", "Deed", None), ("Deed misclosure with the 1978 distance and the 5-1 bearing restored (ft)", "=Deed!B29", "Deed", N2),
    ("Rotation line", "=Deed!B32", "Deed", None), ("Rotation, deed magnetic bearings to the grid", "=Deed!B36", "Deed", None),
    ("Rotation the road course would give (minutes of arc)", "=Deed!B38", "Deed", N0),
    ("Calls out of tolerance", "=Deed!B42", "Deed", N0), ("Calls in error in the deed", "=Deed!B43", "Deed", N0),
    ("3-4 call, deed distance as transcribed (ft)", "=Deed!B44", "Deed", N1), ("3-4 call, measured distance the plat carries (ft)", "=Deed!B45", "Deed", N2),
    ("3-4 call, distance in the 1978 deed of trust (ft)", "=Deed!B23", "Deed", N1),
    ("5-1 call, rotated bearing as transcribed", "=Deed!B47", "Deed", None), ("5-1 call, rotated bearing with the digits restored", "=Deed!B49", "Deed", None),
    ("5-1 call, measured bearing the plat carries", "=Deed!B50", "Deed", None), ("5-1 call, measured less restored (minutes)", "=Deed!B51", "Deed", N0),
    ("Finding on the calls in error", "=Deed!B52", "Deed", None),
    ("Monuments and corners", None, None, None),
    ("Original monuments of the tract found and held", "=Corners!B35", "Corners", N0), ("Later monuments held as the corner", "=Corners!B36", "Corners", N0),
    ("Offset of the corner 1 pin from its test position (ft)", "=Corners!K4", "Corners", N2), ("Later monuments found and not held", "=Corners!B37", "Corners", N0),
    ("Offset of the corner 3 rebar from the corner (ft)", "=Corners!K6", "Corners", N2), ("Corners to be set", "=Corners!B38", "Corners", N0), ("Corner to be set", "=Corners!B39", "Corners", N0),
    ("Distance from corner 2 to corner 3 (ft)", "=Corners!G29", "Corners", N2), ("Distance from corner 3 to the stone at corner 4 (ft)", "=Corners!G30", "Corners", N2),
    ("Distance the crew's pin at corner 3 is to be moved (ft)", "=Corners!B40", "Corners", N2),
    ("Plat coordinates of the corners, adjusted", None, None, None),
]
for n in range(1, 6):
    ROWS.append((f"Corner {n} northing (ft)", f"=Corners!C{27 + n}", "Corners", N3)); ROWS.append((f"Corner {n} easting (ft)", f"=Corners!D{27 + n}", "Corners", N3))
ROWS += [
    ("Area", None, None, None),
    ("Area by coordinates (sq ft)", "=Area!B11", "Area", NC), ("Area (acres)", "=Area!B12", "Area", N3), ("Deed acreage recited", "=Area!B13", "Area", N2), ("Difference, computed less deed (acres)", "=Area!B14", "Area", N3),
    ("Fences", None, None, None),
    ("Hutchins fence, greatest offset inside the tract (ft)", "=Fences!E16", "Fences", N2), ("Hutchins fence finding", "=Fences!G16", "Fences", None),
    ("Ballinger fence, greatest offset outside the tract (ft)", "=Fences!F17", "Fences", N2), ("Ballinger fence finding", "=Fences!G17", "Fences", None),
    ("Farley fence, greatest offset inside the tract (ft)", "=Fences!E18", "Fences", N2), ("Farley fence finding", "=Fences!G18", "Fences", None),
]
r = 6
for label, f, src, fmt in ROWS:
    if f is None: put(fi, f"A{r}", label, bold=True)
    else:
        put(fi, f"A{r}", label); c = put(fi, f"B{r}", f, fmt, left=True); put(fi, f"C{r}", src)
    r += 1
put(fi, f"A{r + 1}", "Every value on this page reads from the tab named beside it. The tabs behind read from the Field Notes tab, which copies the crew's file shot for shot, and from the deed calls typed on the Deed tab.", wrap=True)
fi.row_dimensions[r + 1].height = 32
wb.move_sheet("Findings", offset=-(len(wb.sheetnames) - 1))

# ============================================================ Note to Ellen
F = FIG
pct = lambda x: f"{x:,}"
note = sheet("Note to Ellen", {"A": 125}, "Note to Ellen Vance on the tract 7 analysis")
paras = [
    "Ellen, this is the office analysis on tract 7 for the Cope estate, job 26-2214, from Dwight's traverse of September 29, the ties of September 30, and Colleen's record research of October 1 and 2. The findings page carries every figure the plat will rest on, and each one reads from the tab named beside it.",
    f"The traverse closes inside the rural standard. Three legs were shot twice. On T3 to T4 the first pair reads {F['pair tests'][('T3','T4',0)][0]:.2f} feet apart between its forward and reverse, so it is a pair in error under firm standards 1.1. It is rejected, and the second pair carries the leg. On T5 to T6 both pairs stand on their own but differ by {F['pairs T5-T6'][2]:.2f} foot, so they are not meaned together. The first pair is set aside: the field book puts the county's PK nail {PK:.2f} foot from the hub at T6 on the side toward T5, the first pair is short by that distance, and the loop closes to one part in {pct(F['precision first pair'])} on the first pair against one part in {pct(F['precision'])} on the second. The two pairs on T2 to T3 agree within {F['pairs T2-T3'][2]:.2f} foot and are meaned together. On the shots used the seven legs run {F['perimeter']:,.2f} feet and miss T1 by {abs(F['lat misclosure']):.3f} foot in latitude and {abs(F['dep misclosure']):.3f} foot in departure, a linear error of {F['linear error']:.2f} foot and a precision of one part in {pct(F['precision'])}.",
    "The T7 to T2 leg runs within seconds of due north, and its forward shot falls on the west side of north while the reverse falls on the east. The bearings are meaned as directions on every leg, from the summed cosines and sines of the azimuths turned by 45 degrees, with the turn taken off again after the mean. A plain average of the two azimuths on that leg, 359.999 and 0.000, would point the leg south and throw the loop open by six hundred feet.",
    f"The tract is rural on the field dates under firm standards 1.3, as the crew ran it. Parcel 041.00 comes inside the corporate limits of Cookeville under Ordinance O26-07, which takes effect on November 1, 2026, after the field work. The standard is one part in 10,000, and the traverse meets it. The same closure would not meet the urban standard of one part in 15,000.",
    f"Three entries in the notes file are changed on the field book and the record. The shot to point 202 is reduced from T3 and not from T2, because the field book ties that post from T3 and the shot was taken between the T2 and T4 set-ups. The numbers of points 103 and 203 are exchanged, because the shot coded IRF is the rebar, and it stands {F['pin 2 to rebar']:.2f} feet from the pin at corner 2, the distance on the 2008 plat. Every tie distance carries a prism correction of {P['prism']:.2f} foot under firm standards 1.5, since the mini prism of -17.5 mm was shot with the instrument set at -30 mm, and the tie to the stone at corner 5 carries the 0.60 foot the crew taped as well.",
    f"The deed does not close on its own calls as transcribed. Reduced on its magnetic bearings, the description runs {F['deed perimeter']:,.1f} feet and misses the point of beginning by {F['deed misclosure']:.2f} feet, which is {F['deed per 1000']:.2f} feet per 1,000 feet of perimeter. That is a defect in the description under firm standards 3.1. Two calls are at fault. With the 1978 deed of trust's 592.7 feet in the 3-4 call alone the misclosure is {F['deed misclosure, 592.7 only']:.2f} feet; with the 5-1 bearing read N 43° 31' W alone it is {F['deed misclosure, 43 31 only']:.2f} feet; with both it is {F['deed misclosure, both']:.2f} foot.",
    f"Three original monuments of the tract are found and held: the pin at corner 2, which the 2008 Hutchins survey found in place as the Tolliver pin and capped where it stood, the stone at corner 4, found upright in 1994, and the stone at corner 5, which the 1994 survey found in the fence row and left as found. The 4-5 call is the one deed course with a found original monument at each end, so the rotation comes from it under firm standards 3.2. The deed bearing S 77° 59' W stands against the measured {bearing(F['rotation measured azimuth'])}, a rotation of {F['rotation']} taken to the nearest minute. Every call is rotated by that amount. The road course, pin to pin, would give {F['rotation road course minutes'] // 60}° {F['rotation road course minutes'] % 60:02d}', but the pin at corner 1 is not an original monument: its cap reads PLS 1188, and the 1994 plat records that no monument was found there, with a pin set at the deed distance from the stone.",
    f"The pin at corner 1 is a later monument under firm standards 3.6. The 5-1 call is in error, so its test position comes from the pin at corner 2 by the reversed 1-2 call. That position lies {F['pin 1 offset']:.2f} foot from the pin, inside the 0.50 foot, and the pin is held as the corner. The rebar at corner 3 is a later monument as well. The 2008 survey set it at the deed distance from corner 2 with no monument found, and it lies {F['rebar offset']:.2f} foot from the position the corner takes under firm standards 3.7, so it is not held. Under the road-course rotation the same rebar would sit {ROAD_REBAR:.2f} foot from the corner and would wrongly hold.",
    f"The deed places corner 3 in the west line of Ballinger, and that line runs between the stone at corner 4 and the iron pipe at the Ballinger northwest corner, both called for in Deed Book 377, Page 102. Corner 3 is set where the rotated 2-3 course from corner 2 meets that line, at northing {F['corner 3'][0]:,.3f} and easting {F['corner 3'][1]:,.3f}, which is {F['distance 2-3']:.2f} feet from corner 2 and {F['distance 3-4']:.2f} feet from the stone at corner 4. The stone and the pipe measure {F['stone to pipe']:.2f} feet apart against 806.9 feet in the Ballinger deed. Dwight's pin at corner 3 was set on the road-course rotation where the 2-3 and 3-4 calls meet, before the loop was closed; it stands {F['set pin offset']:.2f} foot from the corner and is to be reset there under 3.7.",
    f"The 3-4 and 5-1 calls are the two in error, and the field is right on both. Our transcription reads 597.2 feet for the 3-4 call, the measured course is {F['distance 3-4']:.2f} feet, and the 1978 deed of trust reads 592.7 feet, which is 597.2 with its last two digits exchanged; the plat carries the measured {F['distance 3-4']:.2f} feet. Our transcription reads N 34° 31' W for the 5-1 call, which is 9 degrees off the course between the stone at corner 5 and the pin at corner 1. With its first two digits exchanged the call reads N 43° 31' W, which rotated is {F['rotated 5-1'] if False else bearing(rnd((azimuth(*SLIP[:3], 0, SLIP[3]) + F['rotation minutes'] / 60) % 360, 6), False)} against the measured {F['bearing 5-1']}, a difference of {F['bearing diff 5-1 restored']:.0f} minutes; the plat carries the measured bearing. Every other call agrees with the field within ten minutes and one foot. Both are errors in the deed under firm standards 3.3, each resting on held or set corners at both ends.",
    f"The area by coordinates on the five corners as held or set is {F['area']:,} square feet, which is {F['acres']:.3f} acres. The deed recites 9.89 acres more or less, so the computed area is under the deed by {abs(F['acre difference']):.3f} acre, which is {abs(F['area difference']):.0f} square feet.",
    f"The Hutchins wire fence stands inside the tract along the 2-3 course at its middle post, by {F['offset 202']:.2f} foot, with the post by the road {abs(F['offset 201']):.2f} foot outside and the corner post {abs(F['offset 203']):.2f} foot outside. That is an encroachment by Hutchins under firm standards 3.8, because the greatest offset inside is over 0.25 foot. The Ballinger board fence stands outside the tract by {abs(F['offset 204']):.2f} to {F['Ballinger outside']:.2f} foot, and the Farley fence stands inside it by {F['Farley inside']:.2f} foot at most, so both are occupation notes only.",
    f"Five things the field evidence leaves open. First, Dwight's pin at corner 3 is to be reset {F['set pin offset']:.2f} foot away at the position above, so the crew goes back before the plat is final. Second, the corner 1 pin is held on the 1994 survey's measurements and not on an original mark, so an original pin recovered at that corner would control over it. Third, the register's image of Deed Book 412, Page 233, should be read again at the 3-4 and 5-1 calls, because the slips may be in our transcription and not in the deed. Fourth, the tract comes inside the city on November 1, 2026, before the closing, and this traverse would not meet the urban standard that applies to field work from that date. Fifth, the Hutchins fence encroachment at the middle post is for you to show on the plat and to raise with the buyer.",
]
for k, t in enumerate(paras):
    c = put(note, f"A{3 + k}", t, wrap=True); note.row_dimensions[3 + k].height = 30 + 15 * (len(t) // 120)

# ============================================================ properties and save
wb.properties.creator = "Hollins & Vance Surveying"; wb.properties.title = "Tract 7 boundary analysis, job 26-2214"; wb.properties.lastModifiedBy = "Hollins & Vance Surveying"
import datetime
wb.properties.created = datetime.datetime(2026, 10, 26, 8, 10, 24); wb.properties.modified = datetime.datetime(2026, 10, 29, 9, 52, 18)
wb.calculation.fullCalcOnLoad = True
wb.save(OUT)
# restore the in-world core.xml the workbook carried before
CORE = b'<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"><dc:creator xmlns:dc="http://purl.org/dc/elements/1.1/">Hollins &amp; Vance Surveying</dc:creator><dc:title xmlns:dc="http://purl.org/dc/elements/1.1/">Tract 7 boundary analysis, job 26-2214</dc:title><dcterms:created xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="dcterms:W3CDTF">2026-10-26T08:10:24Z</dcterms:created><dcterms:modified xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="dcterms:W3CDTF">2026-10-29T09:52:18Z</dcterms:modified><cp:lastModifiedBy>Hollins &amp; Vance Surveying</cp:lastModifiedBy></cp:coreProperties>'
tmp = str(OUT) + ".tmp"
with zipfile.ZipFile(OUT) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        zout.writestr(item, CORE if item.filename == "docProps/core.xml" else zin.read(item.filename))
shutil.move(tmp, OUT)
print("written", OUT, "sheets", wb.sheetnames)
print("key figures:", {k: FIG[k] for k in ("precision", "rotation", "pin 1 offset", "rebar offset", "set pin offset", "distance 2-3", "distance 3-4", "area", "acres", "Hutchins inside", "corner 3")})
