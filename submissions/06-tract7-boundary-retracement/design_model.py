"""Design model for the tract 7 rebuild: true coordinates, generated shots, and the reduction that
mirrors the golden's rules, so every intended outcome is checked before any file is written."""
import csv
import math
import random
import sys
from reduce_core import rnd, polar, dist, derive, azimuth

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))

def az_of(a, b):
    return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])) % 360

def dms(az):
    az %= 360
    if az <= 90: ns, a, ew = "N", az, "E"
    elif az <= 180: ns, a, ew = "S", 180 - az, "E"
    elif az <= 270: ns, a, ew = "S", az - 180, "W"
    else: ns, a, ew = "N", 360 - az, "W"
    t = int(round(a * 3600))
    return ns, t // 3600, (t % 3600) // 60, t % 60, ew

DEED = [("N", 14, 44, "E", 640.4), ("S", 81, 6, "E", 588.8), ("S", 8, 46, "W", 597.2), ("S", 77, 59, "W", 510.1), ("N", 34, 31, "W", 225.5)]
SLIP = ("N", 43, 31, "W")      # the 5-1 call as written in 1962 (the transcription reads 34)
TRUST_34 = 592.7
DEED_AZ = [azimuth(ns, d, m, 0, ew) for ns, d, m, ew, _ in DEED]
AZ51_TRUE = azimuth(*SLIP[:3], 0, SLIP[3])
ROT = 132.3 / 60; ROT_DECOY = 134.65 / 60   # defaults, overridden by build()

def meet(p, az_p, q, az_q):
    b = math.radians(az_q); a = math.radians(az_p)
    t = ((q[1] - p[1]) * math.cos(b) - (q[0] - p[0]) * math.sin(b)) / math.sin(a - b)
    return polar(p, az_p, t), t

def build(ball_rot=0.17, d12=640.32, d45=510.25, d51=225.3, az51_off=0.05, seed=26, leg_err=0.19, rot=131.8, rot_decoy=134.6, rebar_back=0.45):
    global ROT, ROT_DECOY
    ROT = rot / 60; ROT_DECOY = rot_decoy / 60
    G = {}
    T1 = (5000.0, 5000.0)
    PIN1 = polar(T1, azimuth("S", 67, 54, 47, "W"), 13.83)
    C1 = PIN1
    C2 = polar(C1, DEED_AZ[0] + ROT_DECOY, d12)
    C5 = polar(C1, (AZ51_TRUE + ROT + az51_off + 180) % 360, d51)
    C4 = polar(C5, (DEED_AZ[3] + ROT + 180) % 360, d45)
    ball_az = azimuth("N", 8, 40, 0, "E") + ROT + ball_rot
    PIPE = polar(C4, ball_az, 806.7)
    C3, L = meet(C2, DEED_AZ[1] + ROT, C4, ball_az)
    C3D, LD = meet(C2, DEED_AZ[1] + ROT_DECOY, C4, ball_az)
    REBAR = polar(C3D, ball_az + 180, rebar_back)                                       # 0.45 past the decoy point along the Ballinger line
    PIN107, L107 = meet(C2, DEED_AZ[1] + ROT_DECOY, C4, (DEED_AZ[2] + ROT_DECOY + 180) % 360)   # the crew's computed corner
    T2 = polar(C2, 151.0, 11.2); T7 = (T2[0] - 300.0, T2[1] + 0.0022)
    T3 = polar(polar(C2, DEED_AZ[1] + ROT, 292.0), DEED_AZ[1] + ROT + 90, 20.0)
    T4 = polar(C3, 236.5, 13.5); T5 = polar(C4, 320.5, 12.3); T6 = polar(C5, 5.3, 8.83)
    ST = {"T1": T1, "T2": T2, "T3": T3, "T4": T4, "T5": T5, "T6": T6, "T7": T7}
    C = [C1, C2, C3, C4, C5]
    def on_line(a, b, along, inside):
        az = az_of(a, b); return polar(polar(a, az, along), az + 90, inside)
    POSTS = {"201": on_line(C2, C3, 32.0, -0.15), "202": on_line(C2, C3, 296.0, 0.70), "203": on_line(C2, C3, 588.9, -0.35),
             "204": on_line(C3, C4, 52.0, -0.12), "205": on_line(C3, C4, 380.0, -0.35), "206": on_line(C3, C4, 560.0, -0.20),
             "207": on_line(C4, C5, 55.0, 0.17), "208": on_line(C4, C5, 262.0, 0.22), "209": on_line(C4, C5, 480.0, 0.09)}
    MON = {"101": PIN1, "102": C2, "103": REBAR, "104": C4, "105": C5, "106": PIPE, "107": PIN107}
    G.update(C=C, ST=ST, POSTS=POSTS, MON=MON, L=L, LD=LD, L107=L107, C3D=C3D, ball_az=ball_az, PIPE=PIPE)
    # shots
    random.seed(seed)
    LOOP = ["T1", "T7", "T2", "T3", "T4", "T5", "T6"]
    rows = []
    legs = list(zip(LOOP, LOOP[1:] + LOOP[:1]))
    for a, b in legs:
        az = az_of(ST[a], ST[b]); d = dist(ST[a], ST[b])
        if (a, b) == ("T4", "T5"): d += leg_err
        sets = 2 if (a, b) in (("T2", "T3"), ("T3", "T4"), ("T5", "T6")) else 1
        noise = [(random.uniform(-3, 3) / 3600, random.uniform(-3, 3) / 3600, random.uniform(-0.02, 0.02), random.uniform(-0.02, 0.02)) for _ in range(sets)]
        for k in range(sets):
            n1, n2, e1, e2 = noise[1] if (a, b) == ("T5", "T6") else noise[k]   # the PK-nail pair shares the second pair's noise, so the pairs differ by the nail's 0.28 exactly
            fa, ra, fd, rd = az + n1, (az + 180) % 360 + n2, d + e1, d + e2
            if (a, b) == ("T7", "T2"): fa, ra = 359 + 59 / 60 + 57 / 3600, 180 + 1 / 3600
            if (a, b) == ("T5", "T6") and k == 0: fd, rd = d - 0.28 + e1, d - 0.28 + e2
            if (a, b) == ("T3", "T4") and k == 0: rd = d + 1.22
            rows.append([a, b, fa, fd, "TRAV"]); rows.append([b, a, ra, rd, "TRAV"])
    TIE_FROM = {"101": "T1", "102": "T2", "201": "T2", "202": "T3", "103": "T4", "203": "T4", "107": "T4", "106": "T4", "204": "T4",
                "104": "T5", "205": "T5", "206": "T5", "207": "T5", "105": "T6", "208": "T6", "209": "T6"}
    CODE = {"101": "IPF", "102": "IPF", "103": "IRF", "104": "STN", "105": "STN", "106": "IP", "107": "IPS"}
    for p in ["101", "102", "201", "202", "203", "103", "107", "106", "204", "104", "206", "205", "207", "105", "209", "208"]:
        frm = TIE_FROM[p]; tgt = MON.get(p) or POSTS[p]
        az = az_of(ST[frm], tgt) + random.uniform(-2, 2) / 3600
        d = dist(ST[frm], tgt) - 0.04 - (0.60 if p == "105" else 0.0)
        rows.append([frm, p, az, d, CODE.get(p, "FNC")])
    # the notes file as the crew's collector stored it: 202 recorded from T2, points 103 and 203 exchanged
    shots = []
    times = iter(["08:42", "09:26", "09:38", "10:04", "10:31", "10:36", "11:09", "11:14", "11:22", "13:05", "13:11", "13:17", "13:26", "14:40", "14:49", "15:33", "15:40", "16:27", "16:48", "17:21"] +
                 ["08:10", "08:49", "08:53", "09:31", "10:12", "10:15", "10:19", "10:24", "10:31", "11:17", "11:20", "11:26", "11:33", "13:22", "13:27", "13:35"])
    for i, (frm, to, az, d, code) in enumerate(rows, 1):
        ns, dd, mm, ss, ew = dms(az)
        rec_to = {"103": "203", "203": "103"}.get(to, to)
        rec_from = "T2" if to == "202" else frm
        shots.append({"SHOT": i, "DATE": "09/29/2026" if code == "TRAV" else "09/30/2026", "TIME": next(times), "AT": rec_from, "TO": rec_to,
                      "NS": ns, "DEG": dd, "MIN": mm, "SEC": ss, "EW": ew, "HORIZ_DIST_FT": f"{rnd(d, 2):.2f}", "CODE": code})
    G["shots"] = shots; G["TIE_FROM"] = TIE_FROM; G["LOOP"] = LOOP
    return G

PARAMS = dict(prism=0.04, offset105=0.60, class_="Rural", urban=15000, rural=10000, pair_ft=0.05, pair_sec=20, later_tol=0.5, enc_tol=0.25,
              n0=5000.0, e0=5000.0, deed_rate=1.0, dist_tol=1.0, bear_tol=10, sqft=43560, deed_acres=9.89,
              fences={"Hutchins": (1, ("201", "202", "203")), "Ballinger": (2, ("204", "205", "206")), "Farley": (3, ("207", "208", "209"))})

if __name__ == "__main__":
    for br in [0.15, 0.2, 0.22, 0.25]:
        G = build(ball_rot=br)
        print(f"ball_rot {br:+.2f}: L {G['L']:.2f} LD {G['LD']:.2f} L107 {G['L107']:.2f} | 3-4 {dist(G['C'][2], G['C'][3]):.2f} az diff {(az_of(G['C'][2], G['C'][3]) - (DEED_AZ[2] + ROT)) * 60:+.1f}' | rebar-C3 {dist(G['MON']['103'], G['C'][2]):.2f} rebar-C3D {dist(G['MON']['103'], G['C3D']):.2f} pin107-C3 {dist(G['MON']['107'], G['C'][2]):.2f} | pin2-rebar {dist(G['C'][1], G['MON']['103']):.2f}")
    br = float(sys.argv[1]) if len(sys.argv) > 1 else -0.1
    le = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
    G = build(ball_rot=br, leg_err=le)
    P = dict(PARAMS); P["class"] = P.pop("class_"); P["station"] = G["TIE_FROM"]
    fig, st = derive(G["shots"], G["LOOP"], DEED, SLIP, TRUST_34, P)
    keys = ["perimeter", "lat misclosure", "dep misclosure", "linear error", "precision", "precision first pair", "precision second pair", "precision both pairs", "shots set aside", "changes",
            "deed misclosure", "deed per 1000", "deed misclosure bearing", "deed misclosure, 592.7 only", "deed misclosure, 43 31 only", "deed misclosure, both",
            "rotation", "rotation minutes", "rotation road course minutes", "pin 1 offset", "rebar offset", "set pin offset", "corner 3 along", "pin 2 to rebar", "pin 2 to corner post", "pin 2 to set pin", "stone to pipe", "ballinger az",
            "distance 1-2", "bearing diff 1-2", "distance diff 1-2", "distance 2-3", "bearing diff 2-3", "distance diff 2-3", "distance 3-4", "bearing diff 3-4", "distance diff 3-4", "distance 4-5", "bearing diff 4-5", "distance diff 4-5",
            "distance 5-1", "bearing diff 5-1", "distance diff 5-1", "bearing diff 5-1 restored", "calls out", "area", "acres", "acre difference", "Hutchins inside", "Hutchins outside", "Ballinger inside", "Ballinger outside", "Farley inside", "Farley outside"]
    for k in keys: print(f"  {k}: {fig[k]}")
    for p in ("201", "202", "203", "204", "205", "206", "207", "208", "209"): print(f"  offset {p}: {fig['offset ' + p]}")
    print("  pair tests:", {k: v for k, v in fig["pair tests"].items()})
    print("  standing:", st)
    print("  corner 3:", fig["corner 3"], "stations", fig["stations"])
    for name, kw in {"road-course rotation": dict(rotation="1-2"), "bust kept": dict(bust="keep"), "arithmetic mean on T7-T2": dict(wrap="arith"), "first pair T5-T6": dict(t5t6="first"),
                     "both pairs T5-T6": dict(t5t6="all"), "urban": dict(klass="Urban"), "no prism": dict(prism=0.0), "no offset": dict(offset=0.0), "202 from file station": dict(station="file"),
                     "no swap": dict(swap=False), "rebar held": dict(hold_rebar=True), "corner 3 at deed distance": dict(corner3="distance"), "unadjusted": dict(adjust=False), "raw precision": dict(precision_from="raw")}.items():
        f2, s2 = derive(G["shots"], G["LOOP"], DEED, SLIP, TRUST_34, P, **kw)
        diff = {k: (st[k], s2[k]) for k in st if st[k] != s2[k]}
        print(f"  variant {name}: {diff}  rebar {f2['rebar offset']} pin1 {f2['pin 1 offset']} prec {f2['precision']} acres {f2['acres']}")
    with open("shots.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(G["shots"][0].keys())); w.writeheader(); w.writerows(G["shots"])
