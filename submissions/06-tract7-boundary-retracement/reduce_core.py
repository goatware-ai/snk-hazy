"""The office reduction under the firm standards as the rebuilt golden applies them. Shared by the design
model (to check outcomes) and by verify_golden.py (which parses the inputs and calls derive)."""
import math
from decimal import Decimal, ROUND_HALF_UP


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
