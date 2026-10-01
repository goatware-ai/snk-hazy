"""verify_golden.py for pretreatment-smr-q3-2026: re-derive every figure and standing the report states
from inputs/ alone under the permit's rules as the golden states them, and list the alternate readings
a reviewer could take with the phrase the golden uses to settle each one.

Nothing in the laboratory's table says which results count. A result is a valid sample result when the
sample was taken at Outfall 001 (chain of custody log), the composite held at least twelve aliquots
across the 24 hours (operator logs), the analysis fell inside the holding time (Methods tab against the
analysis dates), and the laboratory did not reject it (case narratives). A revised report replaces the
figure first printed (case narratives). The monitoring frequency is met where valid results come from
two days of the month at least ten days apart (Section 2.1). The six-month measurements add the City's
two composites (the Coordinator's note, dated by the morning each was pulled), leave out the sample
collected before April 1, and average the valid results of one calendar day into one measurement
(Section 3.4). Daily flow is the difference between consecutive totalizer register readings, with the
volume that went around the meter on September 9 added to that day's discharge. Notices are timed
against the City's telephone log and the operator's own log, duties that began before July 1 and fell due
in the quarter are carried, and the report arm of Section 3.4 is tested on both reports due in the period.

    .venv/bin/python submissions/03-pretreatment-smr-q3-2026/verify_golden.py
"""
import datetime as dt
import os
import re
import sys
from decimal import Decimal as D, ROUND_HALF_UP
from pathlib import Path

import openpyxl
from docx import Document

HERE = Path(__file__).resolve().parent
ROOT = os.environ.get("HAZY_ROOT") or next(str(p) for p in HERE.parents if (p / "tools" / "golden_verify.py").is_file())
sys.path.insert(0, os.path.join(ROOT, "tools"))
from golden_verify import Report  # noqa: E402

INPUTS = HERE / "inputs"
PARAMS = ["Cd", "Cr", "Cu", "Ni", "Zn", "CN"]
METALS = ["Cd", "Cr", "Cu", "Ni", "Zn"]
NAMES = {"cadmium": "Cd", "chromium": "Cr", "copper": "Cu", "nickel": "Ni", "zinc": "Zn", "cyanide": "CN"}
MONTHS = {7: "Jul", 8: "Aug", 9: "Sep"}
MONTHNUM = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8,
            "September": 9, "October": 10, "November": 11, "December": 12}
PERIOD = (dt.date(2026, 4, 1), dt.date(2026, 9, 30))
MIN_ALIQUOTS = 12


def xround(x, places):
    return D(format(D(x), ".15g")).quantize(D(1).scaleb(-places), rounding=ROUND_HALF_UP)


def mdy(s):
    return dt.datetime.strptime(s.strip()[:10], "%m/%d/%Y").date()


def mdyhm(s):
    return dt.datetime.strptime(s.strip(), "%m/%d/%Y %H:%M")


def add_months(d, n):
    y, m = divmod(d.month - 1 + n, 12)
    last = (dt.date(d.year + y + (m == 11), (m + 1) % 12 + 1, 1) - dt.timedelta(days=1)).day
    return dt.date(d.year + y, m + 1, min(d.day, last))


def doc_text(doc):
    out = [p.text for p in doc.paragraphs]
    for t in doc.tables:
        for row in t.rows:
            out.append(" | ".join(c.text for c in row.cells))
    return out


# ------------------------------------------------------------------ the permit
permit = Document(INPUTS / "pretreatment_permit_ip0421.docx")
DAILY, MONTHLY = {}, {}
for row in permit.tables[0].rows[1:]:
    c = [x.text for x in row.cells]
    key = NAMES.get(c[0].split(",")[0].lower())
    if key:
        DAILY[key], MONTHLY[key] = D(c[1]), D(c[2])
    if c[0].startswith("Flow"):
        FLOW_LIMIT = int(c[1].replace(",", ""))
PH_LO, PH_HI = D("6.0"), D("9.0")

# ------------------------------------------------------------------ the laboratory's file
wb = openpyxl.load_workbook(INPUTS / "lab_results_apr_sep2026.xlsx", data_only=True)
rows = list(wb["Results"].iter_rows(values_only=True))
hdr = [str(h) for h in rows[3]]
EVENTS = {}
for r in rows[4:]:
    if not (isinstance(r[0], str) and r[0].startswith("VP-")):
        continue
    rec = dict(id=r[0], date=mdy(r[1]), kind=r[3], source="permittee", field_ph=D(str(r[hdr.index("FIELD PH")])))
    for p in PARAMS:
        rec[p] = (r[hdr.index(f"{p} MG/L")], (r[hdr.index(f"{p} QUAL")] or "").strip())
    EVENTS[r[0]] = rec
log = list(wb["Sample Log"].iter_rows(values_only=True))
lh = [str(h) for h in log[3]]
for r in log[4:]:
    if not (isinstance(r[0], str) and r[0].startswith("VP-")):
        continue
    e = EVENTS[r[0]]
    e["point"] = r[lh.index("SAMPLED AT")]
    e["collected dt"] = mdyhm(r[lh.index("COLLECTED")])            # the end of the composite period, or the grab
    e["metals analyzed"] = mdy(r[lh.index("METALS ANALYZED")])
    e["metals analyzed dt"] = mdyhm(r[lh.index("METALS ANALYZED")])
    cn = str(r[lh.index("CYANIDE ANALYZED")])
    e["CN analyzed"] = mdy(cn) if re.match(r"\d\d/\d\d/\d{4}", cn) else None
    e["CN analyzed dt"] = mdyhm(cn) if re.match(r"\d\d/\d\d/\d{4} \d\d:\d\d", cn) else None
    e["issued"] = mdyhm(r[lh.index("REPORT ISSUED")])
    e["aware"] = {p: e["issued"] for p in PARAMS}
MDL, HOLD = {}, {}
for r in wb["Methods"].iter_rows(min_row=5, values_only=True):
    key = NAMES.get(str(r[0]).split(",")[0].lower())
    if key:
        MDL[key] = D(str(r[2]))
        HOLD[key] = str(r[6])

# ------------------------------------------------------------------ the case narratives
REJECTED, REVISED, KNOWN_REJECTED = set(), {}, {}
narr = Document(INPUTS / "lab_case_narratives_2026.docx")
current, rev_time = None, None
for p in narr.paragraphs:
    m = re.match(r"GLA-26-\d+, sample (VP-\w+),", p.text)
    if m:
        current = m.group(1)
        t = re.search(r"Revision 1 issued (\d\d/\d\d/\d{4}) at (\d\d:\d\d)", p.text)
        rev_time = mdyhm(f"{t.group(1)} {t.group(2)}") if t else None
        continue
    if current:
        for m in re.finditer(r"laboratory has rejected the (\w+) result", p.text):
            REJECTED.add((current, NAMES[m.group(1)]))
            if rev_time:
                KNOWN_REJECTED[(current, NAMES[m.group(1)])] = rev_time   # a rejection in a revision is known from the revision
        m = re.search(r"Revision 1 corrects (\w+) to ([\d.]+) mg/L", p.text)
        if m:
            when = re.search(r"on (\d\d/\d\d/\d{4}) at (\d\d:\d\d)", p.text)
            REVISED[(current, NAMES[m.group(1)])] = (D(m.group(2)), mdyhm(f"{when.group(1)} {when.group(2)}"))

# ------------------------------------------------------------------ the operator logs
START, REGISTER, BANDS, ALIQUOTS, VOICEMAIL, PULLED, AROUND, RESET, MONTH_END = {}, {}, {}, {}, [], {}, {}, {}, {}
for month, name in ((7, "jul"), (8, "aug"), (9, "sep")):
    doc = Document(INPUTS / f"operator_log_{name}2026.docx")
    intro = doc.paragraphs[1].text
    START[month] = int(re.search(r"Register at 07:00 on \d\d/01/2026: ([\d,]+) gallons", intro).group(1).replace(",", ""))
    e = re.search(r"Register read ([\d,]+) at 07:00 on \d\d/01 for the month total", doc.paragraphs[3].text)
    if e:
        MONTH_END[month] = int(e.group(1).replace(",", ""))     # the operator's own month-end reading
    for row in doc.tables[0].rows[1:]:
        cells = [c.text for c in row.cells]
        if not re.match(r"\d\d/\d\d/2026", cells[0]):
            continue
        day = int(cells[0][3:5])
        REGISTER[(month, day)] = int(cells[1].replace(",", ""))
        n = re.search(r"new register installed reading ([\d,]+)", cells[3])
        if n:
            RESET[(month, day)] = int(n.group(1).replace(",", ""))   # the reading the day's flow is read against
        m = re.match(r"(\d\.\d) to (\d\.\d)", cells[2])
        BANDS[(month, day)] = (D(m.group(1)), D(m.group(2))) if m else None
        # aliquot counts, sentence by sentence, against the sample the sentence or the row names
        ids = re.findall(r"VP-\d{6}", cells[3])
        for sentence in re.split(r"(?<=[.])\s+", cells[3]):
            named = re.findall(r"VP-\d{6}", sentence)
            if named and re.search(r"pulled|sampling event|collected at|taken at", sentence):
                PULLED[named[0]] = dt.date(2026, month, day)      # the day the log shows the sample pulled
            n = re.search(r"(\d+) aliquots", sentence)
            if n:
                ALIQUOTS[(named or ids[:1])[0]] = int(n.group(1))
        b = re.search(r"of the totalizer.*Estimated ([\d,]+) gallons bypassed", cells[3])
        if b:
            AROUND[(month, day)] = int(b.group(1).replace(",", ""))   # went to the sewer around the meter
        v = re.search(r"[Ll]eft a voicemail for Renee Castellanos at (\d\d:\d\d) on the ([\d.]+) copper", cells[3])
        if v:
            VOICEMAIL.append((dt.datetime(2026, month, day, int(v.group(1)[:2]), int(v.group(1)[3:])), v.group(2)))
def build_flows(as_written=False):
    """Daily flows from the register chain; a month's last line that disagrees with the next log's opening and the
    operator's month-end reading is read as transposed unless as_written."""
    flows, total, seg_start, prev, as_logged = {}, 0, START[7], START[7], {}
    for month in (7, 8, 9):
        assert prev == START[month] or as_written, (month, prev, START[month])
        prev = START[month]
        last = max(d for (m, d) in REGISTER if m == month)
        for day in range(1, 32):
            if (month, day) in REGISTER:
                reg = REGISTER[(month, day)]
                if day == last and month + 1 in START and reg != START[month + 1] and MONTH_END.get(month) == START[month + 1]:
                    as_logged[(month, day)] = reg
                    if not as_written:
                        reg = START[month + 1]
                if (month, day) in RESET:                            # a replaced register: close the old segment, restart
                    total += prev - seg_start
                    seg_start = prev = RESET[(month, day)]
                flows[(month, day)] = reg - prev
                prev = reg
    total += prev - seg_start
    return flows, total, as_logged


FLOWS, REGISTER_TOTAL, AS_LOGGED = build_flows()
FLOWS_AS_WRITTEN = build_flows(as_written=True)[0]

# ------------------------------------------------------------------ the Coordinator's note
corr = Document(INPUTS / "city_correspondence_oct2026.docx")
CITY, CALLS = [], []
for p in corr.paragraphs:
    m = re.search(r"set the sampler at manhole 44-118 on (\w+) (\d+) and again on (\w+) (\d+), and they pulled a 24-hour composite the next morning", p.text)
    if not m:
        continue
    pulled = [dt.date(2026, MONTHNUM[m.group(1)], int(m.group(2))) + dt.timedelta(days=1),
              dt.date(2026, MONTHNUM[m.group(3)], int(m.group(4))) + dt.timedelta(days=1)]
    r = re.search(r"first composite came back at ([\d.]+) mg/L copper and ([\d.]+) mg/L zinc, and the second came back at ([\d.]+) mg/L copper and ([\d.]+) mg/L zinc", p.text)
    for day, cu, zn in ((pulled[0], r.group(1), r.group(2)), (pulled[1], r.group(3), r.group(4))):
        CITY.append(dict(id=f"City {day:%m/%d}", date=day, kind="City", source="City", point="manhole 44-118",
                         Cu=(float(cu), ""), Zn=(float(zn), ""),
                         Cd=("under the limit", ""), Cr=("under the limit", ""), Ni=("under the limit", ""), CN=(None, "NS")))
assert len(CITY) == 2
for p in corr.paragraphs:
    g = re.search(r"On (\w+) (\d+) the crew .*? dipped a grab at (\d\d:\d\d), which the laboratory ran by the same method; "
                  r"it came back at ([\d.]+) mg/L copper and ([\d.]+) mg/L zinc", p.text)
    if g:
        day = dt.date(2026, MONTHNUM[g.group(1)], int(g.group(2)))
        CITY.append(dict(id=f"City grab {day:%m/%d}", date=day, kind="City grab", source="City", point="manhole 44-118",
                         grab=True, Cu=(float(g.group(4)), ""), Zn=(float(g.group(5)), ""),
                         Cd=("under the limit", ""), Cr=("under the limit", ""), Ni=("under the limit", ""), CN=(None, "NS")))
assert len(CITY) == 3
for t in corr.tables:
    if t.cell(0, 0).text == "Date":
        for row in t.rows[1:]:
            c = [x.text for x in row.cells]
            CALLS.append((mdyhm(f"{c[0]} {c[1]}"), c[3]))
SIGNATORY = re.search(r"Authorized representative: ([^.]+)\.", permit.paragraphs[3].text).group(1)
q2 = [re.search(r"second-quarter report on file, received (\w+) (\d+) over Mr\. Vandeveer's signature", p.text) for p in corr.paragraphs]
q2 = [m for m in q2 if m][0]
Q2_RECEIVED = dt.date(2026, MONTHNUM[q2.group(1)], int(q2.group(2)))     # the Coordinator's date
Q2_DUE = dt.date(2026, 7, 15)
q1 = [re.search(r"first quarter report was the one Renee wrote us up for.*did not get to her until (\w+) (\d+)", p.text) for p in corr.paragraphs]
q1 = [m for m in q1 if m][0]
Q1_RECEIVED = dt.date(2026, MONTHNUM[q1.group(1)], int(q1.group(2)))     # the plant manager's date
Q1_DUE = dt.date(2026, 4, 15)                                   # Section 3.1, the fifteenth of the month after the quarter
assert any("a little late but fine" in p.text for p in corr.paragraphs)
assert "manhole 44-118" in permit.paragraphs[3].text          # the City's sampling point is Outfall 001's manhole

OVERFLOW = dt.datetime(2026, 9, 9, 7, 50)
PH_EVENT = dt.datetime(2026, 9, 17, 14, 10)


def call_about(*words):
    hits = [when for when, subject in CALLS if all(w in subject for w in words)]
    return hits[0] if hits else None


def derive(nondetect="zero", include_march=False, ignore_composite=False, ignore_city=False, ignore_revision=False,
           include_process=False, exclude_additional=False, ignore_rejection=False, ignore_hold=False,
           metals_hold_days=None, hold_exclusive=False, city_in_average=False, repeat_before_aware=False,
           repeat_by_collection=False, trc="1.2", manager_attestation=False, range_exclusive=False,
           notice_from_manager=False, resample_in_month=True, ignore_same_day=False, frequency_by_count=False,
           ignore_voicemail=False, city_by_set_date=False, lab_dates_govern=False,
           bypass_metered=False, first_quarter_report_outside=False, quarter_events_only=False,
           count_city_grab=False, test_kit_sample=False, register_line_as_written=False, log_note_governs=False,
           hold_in_whole_days=False):
    events = [dict(e) for e in EVENTS.values()] + ([] if ignore_city else [dict(c) for c in CITY])
    if test_kit_sample:                                   # the 09/24 test kit reading taken as an Outfall 001 sample
        kit = dict(id="kit 09/24", date=dt.date(2026, 9, 24), kind="Additional", source="permittee", point="OF-001",
                   field_ph=D("7.2"), **{p: (None, "NS") for p in PARAMS})
        kit["Cu"] = (3.9, "")
        kit["metals analyzed"], kit["CN analyzed"] = dt.date(2026, 9, 24), None
        kit["issued"] = dt.datetime(2026, 9, 24, 10, 15)
        kit["aware"] = {p: kit["issued"] for p in PARAMS}
        events.append(kit)
    if not lab_dates_govern:
        for e in events:
            if e["id"] in PULLED:
                e["date"] = PULLED[e["id"]]
    if city_by_set_date:
        for e in events:
            if e["source"] == "City":
                e["date"] = e["date"] - dt.timedelta(days=1)
    for e in events:
        if e["source"] == "permittee":
            e["aware"] = dict(e["aware"])
    if not ignore_revision:
        for (sid, p), (value, when) in REVISED.items():
            for e in events:
                if e["id"] == sid:
                    e[p] = (float(value), e[p][1])
                    e["aware"][p] = when

    def at_outfall(e):
        return e["source"] == "City" or e["point"] == "OF-001" or include_process

    def valid(p, e):
        val, q = e[p]
        if q == "NS" or val is None:
            return False
        if not at_outfall(e):
            return False
        if p in METALS and e.get("grab") and not count_city_grab:
            return False                              # a metals grab is not a sample collected as Section 2.1 requires
        if e["source"] == "City":
            return True
        if exclude_additional and e["kind"] == "Additional":
            return False
        if p in METALS and not ignore_composite and e["id"] in ALIQUOTS and ALIQUOTS[e["id"]] < MIN_ALIQUOTS:
            return False
        if not ignore_rejection and (e["id"], p) in REJECTED:
            return False
        if not ignore_hold:
            analyzed = e["CN analyzed"] if p == "CN" else e["metals analyzed"]
            if p == "CN" and not hold_in_whole_days and e.get("CN analyzed dt"):
                hours = (e["CN analyzed dt"] - e["collected dt"]).total_seconds() / 3600   # elapsed hours, Section 2.3
                if hours > int(HOLD["CN"].split()[0]) * 24:
                    return False
                return True
            if p == "CN":
                limit = e["date"] + dt.timedelta(days=int(HOLD["CN"].split()[0]))
            elif metals_hold_days:
                limit = e["date"] + dt.timedelta(days=metals_hold_days)
            else:
                limit = add_months(e["date"], int(HOLD[p].split()[0]))
            if analyzed > limit or (hold_exclusive and analyzed == limit):
                return False
        return True

    def treated(p, e):
        val, q = e[p]
        if not valid(p, e):
            return None
        if isinstance(val, str):
            return D(0)                       # a City result stated only as under the limit
        if q == "U":
            return {"zero": D(0), "mdl": MDL[p], "half": MDL[p] / 2}[nondetect]
        return D(str(val))

    figures, standings = {}, {}
    # ---- monthly figures, the permittee's valid samples
    for m, label in MONTHS.items():
        for p in PARAMS:
            pool = [e for e in events if e["date"].month == m and (e["source"] == "permittee" or city_in_average)
                    and (resample_in_month or e["kind"] != "Resample")]
            good = [(e["date"], treated(p, e)) for e in pool if not isinstance(e[p][0], str) and treated(p, e) is not None]
            vals = [v for _, v in good]
            days = sorted({d for d, _ in good})
            n = len(vals)
            avg = xround(sum(vals) / n, 3) if n else None
            mx = max(vals) if n else None
            figures[f"{label} {p} valid samples"] = str(n)
            figures[f"{label} {p} monthly average"] = f"{avg:.3f}" if avg is not None else "none"
            figures[f"{label} {p} daily maximum"] = f"{mx:.3f}" if mx is not None else "none"
            standings[f"{label} {p} monthly average status"] = ("No valid sample" if avg is None else
                                                               "Met" if avg <= MONTHLY[p] else "Exceeded")
            standings[f"{label} {p} daily maximum status"] = ("No valid sample" if mx is None else
                                                              "Met" if mx <= DAILY[p] else "Exceeded")
            spaced = len(days) >= 2 and (days[-1] - days[0]).days >= 10
            standings[f"{label} {p} frequency status"] = "Met" if (n >= 2 if frequency_by_count else spaced) else "Below frequency"
            figures[f"{label} {p} days between the valid samples"] = str((days[-1] - days[0]).days) if len(days) >= 2 else "none"
    # ---- the six-month measurements
    for p in PARAMS:
        pool = [e for e in events if (PERIOD[0] <= e["date"] <= PERIOD[1] or (include_march and e["date"] < PERIOD[0]))]
        byday = {}
        for e in pool:
            v = treated(p, e)
            if v is None:
                continue
            key = e["date"] if not ignore_same_day else (e["date"], e["id"])
            byday.setdefault(key, []).append((v, isinstance(e[p][0], str)))
        vals = []
        for key, group in byday.items():
            stated = [v for v, text in group if not text] or [D(0)]
            vals.append(sum(stated) / len(stated))
        n = len(vals)
        if p == "Cu" and not ignore_same_day:
            figures["copper measurement of 08/19/2026"] = f"{xround(byday[dt.date(2026, 8, 19)][0][0] / 2 + byday[dt.date(2026, 8, 19)][1][0] / 2, 3):.2f}" if len(byday.get(dt.date(2026, 8, 19), [])) == 2 else "not averaged"
        if p == "Zn" and not ignore_same_day:
            figures["zinc measurement of 08/19/2026"] = f"{xround(sum(v for v, _ in byday[dt.date(2026, 8, 19)]) / 2, 3):.3f}" if len(byday.get(dt.date(2026, 8, 19), [])) == 2 else "not averaged"
        thr = xround(DAILY[p] * D(trc), 3)
        above = sum(1 for v in vals if v > DAILY[p])
        above_trc = sum(1 for v in vals if v > thr)
        share = xround(D(above) / n * 100, 1)
        share_trc = xround(D(above_trc) / n * 100, 1)
        figures[f"SNC {p} measurements"] = str(n)
        figures[f"SNC {p} above limit"] = str(above)
        figures[f"SNC {p} above TRC"] = str(above_trc)
        figures[f"SNC {p} share above limit pct"] = f"{share}"
        figures[f"SNC {p} share above TRC pct"] = f"{share_trc}"
        figures[f"SNC {p} TRC threshold"] = f"{thr:.3f}"
        standings[f"SNC {p}"] = "Significant noncompliance" if share >= 66 or share_trc >= 33 else "Not in significant noncompliance"
    # ---- holding days and hours the golden prints
    for e in events:
        if e["source"] == "permittee" and "metals analyzed" in e:
            figures[f"metals hold days {e['id']}"] = str((e["metals analyzed"] - e["date"]).days)
            if e["CN analyzed"]:
                figures[f"cyanide hold days {e['id']}"] = str((e["CN analyzed"] - e["date"]).days)
                figures[f"cyanide hold hours {e['id']}"] = f"{(e['CN analyzed dt'] - e['collected dt']).total_seconds() / 3600:.1f}"
    # ---- replacement samples under Section 2.3: a result not valid, known while the month was open, needs a later valid
    #      sample of the parameter in the month
    for e in events:
        if e["source"] != "permittee" or not (dt.date(2026, 7, 1) <= e["date"] <= dt.date(2026, 9, 30)):
            continue
        if not at_outfall(e):
            continue                                   # process control information is not a sample
        for p in PARAMS:
            val, q = e[p]
            if q == "NS" or val is None or valid(p, e):
                continue
            if e["id"] in ALIQUOTS and ALIQUOTS[e["id"]] < MIN_ALIQUOTS and p in METALS:
                known = dt.datetime.combine(e["date"], dt.time(5, 30))            # the operator's round
            else:
                known = KNOWN_REJECTED.get((e["id"], p), e["issued"])
            month_end = (dt.date(e["date"].year, e["date"].month + 1, 1) - dt.timedelta(days=1))
            if known.date() > month_end:
                continue
            later = [x for x in events if x["source"] == "permittee" and x["date"].month == e["date"].month
                     and x["date"] > known.date() and valid(p, x) and x[p][1] != "NS" and x[p][0] is not None]
            standings[f"replacement after {e['id']} {p}"] = "Collected" if later else "Not collected"
            figures[f"replacement known {e['id']} {p}"] = f"{known:%m/%d/%Y %H:%M}"
    # ---- flow and in-line pH
    flows_all = FLOWS_AS_WRITTEN if register_line_as_written else FLOWS
    for m, label in MONTHS.items():
        flows = {d: f for (mm, d), f in flows_all.items() if mm == m}
        highs = [b[1] for (mm, d), b in BANDS.items() if mm == m and b]
        lows = [b[0] for (mm, d), b in BANDS.items() if mm == m and b]
        if manager_attestation and m in (7, 8):
            standings[f"{label} flow"] = "Met"
            standings[f"{label} in-line pH"] = "Met"
            continue
        figures[f"{label} highest metered day"] = str(max(flows.values()))
        if not bypass_metered:
            flows = {d: f + AROUND.get((m, d), 0) for d, f in flows.items()}
        figures[f"{label} highest daily flow"] = str(max(flows.values()))
        figures[f"{label} days above the flow limit"] = str(sum(1 for v in flows.values() if v > FLOW_LIMIT))
        figures[f"{label} flow total"] = str(sum(flows.values()))
        figures[f"{label} in-line pH high"] = f"{max(highs)}"
        figures[f"{label} in-line pH low"] = f"{min(lows)}"
        standings[f"{label} flow"] = "Exceeded" if max(flows.values()) > FLOW_LIMIT else "Met"
        inside = (lambda lo, hi: lo > PH_LO and hi < PH_HI) if range_exclusive else (lambda lo, hi: lo >= PH_LO and hi <= PH_HI)
        standings[f"{label} in-line pH"] = "Met" if inside(min(lows), max(highs)) else "Exceeded"
    figures["quarter flow total from the registers"] = str(REGISTER_TOTAL)
    figures["quarter flow total"] = str(sum(FLOWS.values()))
    figures["July 17 daily flow"] = str(FLOWS[(7, 17)])
    figures["August 31 daily flow"] = str(flows_all[(8, 31)])
    figures["August 31 register as logged"] = str(AS_LOGGED.get((8, 31), "as the next log opens"))
    standings["August 31 flow"] = "Positive" if flows_all[(8, 31)] > 0 else "Negative"
    sep9 = next(e for e in events if e["id"] == "VP-260909")
    figures["September 9 composite period end"] = f"{sep9['collected dt']:%H:%M}"
    standings["September 9 zinc cause"] = "Overflow" if (log_note_governs or sep9["collected dt"] > OVERFLOW) else "Not established"
    figures["September 9 metered flow"] = str(FLOWS[(9, 9)])
    figures["September 9 discharge"] = str(FLOWS[(9, 9)] + AROUND[(9, 9)])
    figures["August 13 daily flow"] = str(FLOWS[(8, 13)])
    figures["July 28 daily flow"] = str(FLOWS[(7, 28)])
    # ---- grab pH at the outfall by month (the clarifier grab is not an outfall reading)
    for m, label in MONTHS.items():
        grabs = [e["field_ph"] for e in events if e["source"] == "permittee" and e["date"].month == m and at_outfall(e)]
        figures[f"{label} grab pH high"] = f"{max(grabs)}"
        standings[f"{label} grab pH"] = "Met" if all(PH_LO <= g <= PH_HI for g in grabs) else "Exceeded"
    # ---- telephone notices and repeat sampling on each daily maximum exceedance
    quarter = (dt.date(2026, 7, 1), dt.date(2026, 9, 30))
    for e in events:
        if e["source"] != "permittee":
            continue
        for p in PARAMS:
            v = treated(p, e)
            if v is None or v <= DAILY[p]:
                continue
            aware = e["aware"][p]
            tag = f"{e['id']} {p}"
            due = aware.date() + dt.timedelta(days=30)
            later = [x for x in events if x["source"] == "permittee" and treated(p, x) is not None
                     and (x["date"] > aware.date() or (repeat_before_aware and x["date"] > e["date"]))]
            if repeat_by_collection:
                ok = [x for x in later if x["date"] <= due]
            else:
                ok = [x for x in later if x["aware"][p].date() <= due and x["issued"].date() <= due]
            if quarter_events_only and e["date"] < quarter[0]:
                continue
            if quarter[0] <= due or quarter[0] <= aware.date():
                figures[f"repeat due {tag}"] = f"{due:%m/%d/%Y}"
                standings[f"repeat sampling {tag}"] = "Met" if ok else "Late" if later else "Open"
                if later:
                    first = min(later, key=lambda x: x["date"])
                    figures[f"first valid repeat {tag}"] = f"{first['id']} issued {first['issued']:%m/%d/%Y}"
            if quarter[0] <= aware.date() <= quarter[1]:
                name = {v: k for k, v in NAMES.items()}[p].capitalize()
                call = call_about(name, str(e[p][0]))
                figures[f"notice due {tag}"] = f"{aware + dt.timedelta(hours=24):%m/%d/%Y %H:%M}"
                left = [w for w, what in VOICEMAIL if what == str(e[p][0]) and p == "Cu"]
                if call is None and left and not ignore_voicemail:
                    hours = (left[0] - aware).total_seconds() / 3600
                    figures[f"voicemail hours {tag}"] = f"{hours:.2f}"
                    standings[f"telephone notice {tag}"] = "Met" if hours <= 24 else "Late"
                elif call is None:
                    standings[f"telephone notice {tag}"] = "Not made"
                else:
                    hours = (call - aware).total_seconds() / 3600
                    figures[f"notice hours {tag}"] = f"{hours:.2f}"
                    standings[f"telephone notice {tag}"] = "Met" if hours <= 24 else "Late"
    overflow_call = call_about("overflow")
    start = dt.datetime(2026, 9, 9, 8, 30) if notice_from_manager else OVERFLOW
    standings["overflow telephone notice"] = "Late" if overflow_call > start + dt.timedelta(hours=24) else "Met"
    figures["hours from the overflow to the telephone notice"] = f"{(overflow_call - OVERFLOW).total_seconds() / 3600:.2f}"
    ph_call = call_about("pH")
    standings["pH excursion telephone notice"] = "Met" if ph_call <= PH_EVENT + dt.timedelta(hours=24) else "Late"
    figures["minutes from the pH excursion to the telephone notice"] = str(int((ph_call - PH_EVENT).total_seconds() // 60))
    read_0814 = dt.datetime(2026, 8, 14, 7, 0)
    standings["August 13 flow telephone notice"] = "Not made" if not [w for w, s in CALLS if read_0814 <= w <= read_0814 + dt.timedelta(days=7) and "flow" in s] else "Made"
    standings["August 20 pH telephone notice"] = "Not made" if not [w for w, s in CALLS if w.date() in (dt.date(2026, 8, 20), dt.date(2026, 8, 21)) and "pH" in s] else "Made"
    figures["authorized representative on the permit"] = SIGNATORY
    late = {}
    for name, received, due in (("first", Q1_RECEIVED, Q1_DUE), ("second", Q2_RECEIVED, Q2_DUE)):
        figures[f"{name} quarter report, days after its due date"] = str((received - due).days)
        day45 = due + dt.timedelta(days=45)
        figures[f"{name} quarter report, forty-fifth day"] = f"{day45:%m/%d/%Y}"
        late[name] = received > day45 and PERIOD[0] <= day45 <= PERIOD[1] and not (first_quarter_report_outside and name == "first")
        standings[f"{name} quarter report under the 45-day arm"] = "Significant noncompliance" if late[name] else "Not counted"
    late = any(late.values())
    standings["plant, six-month review"] = ("Significant noncompliance" if late or any(
        standings[f"SNC {p}"] == "Significant noncompliance" for p in PARAMS) else "Not in significant noncompliance")
    return figures, standings


VARIANTS = {
    "the March 31 sample counted in the six months": ({"include_march": True}, "collected before April 1"),
    "the City's grab of June 23 counted as a measurement": ({"count_city_grab": True}, "not collected as Section 2.1 requires"),
    "the test kit reading of September 24 counted as a sample": ({"test_kit_sample": True}, "not a method approved under 40 CFR Part 136"),
    "the August 31 register line taken as written": ({"register_line_as_written": True}, "two digits transposed"),
    "the log's note that the composite ran through the overflow taken as true": ({"log_note_governs": True}, "before the 07:50 overflow"),
    "the cyanide holding time counted in whole days": ({"hold_in_whole_days": True}, "elapsed hours"),
    "the July 7 composite counted as collected": ({"ignore_composite": True}, "9 aliquots"),
    "the City's two composites left out of the measurements": ({"ignore_city": True}, "whether the sample was collected by the permittee or by the City"),
    "the copper figure first printed for August 25 used": ({"ignore_revision": True}, "the revised result replaces the result first reported"),
    "the clarifier weir grab counted as a sample": ({"include_process": True}, "process control information"),
    "the additional Outfall 001 composite left out": ({"exclude_additional": True}, "additional samples included"),
    "the two results of August 19 counted as two measurements": ({"ignore_same_day": True}, "of the same calendar day"),
    "the additional composite dated as the laboratory's file prints it": ({"lab_dates_govern": True}, "the day on which the composite is pulled"),
    "the City's composites dated by the day the sampler was set": ({"city_by_set_date": True}, "pulled the next morning"),
    "the 2,900 gallons taken as inside the metered flow": ({"bypass_metered": True}, "around the meter"),
    "the first quarter report left to the period before April": ({"first_quarter_report_outside": True}, "the forty-fifth day"),
    "duties read only on the samples collected in the quarter": ({"quarter_events_only": True}, "fell due in the quarter"),
    "frequency read as a count of two valid samples": ({"frequency_by_count": True}, "at least ten days apart"),
    "the voicemail of August 27 left out of the record": ({"ignore_voicemail": True}, "voicemail"),
    "the rejected zinc figure of July 21 counted": ({"ignore_rejection": True}, "the laboratory has rejected"),
    "the August 11 cyanide counted at 15 days": ({"ignore_hold": True}, "outside the 14-day holding time"),
    "metals held to 28 days": ({"metals_hold_days": 28}, "6 months for total metals"),
    "an analysis on the fourteenth day read as outside the holding time": ({"hold_exclusive": True}, "on the fourteenth day"),
    "the City's results averaged into the monthly figures": ({"city_in_average": True}, "collected by the permittee"),
    "a sample collected before the report counted as the repeat": ({"repeat_before_aware": True}, "collected after the permittee became aware"),
    "the repeat sample tested on its collection date alone": ({"repeat_by_collection": True}, "reaches the Coordinator within the 30 days"),
    "non-detects carried at the detection limit": ({"nondetect": "mdl"}, "carried at zero"),
    "non-detects carried at half the detection limit": ({"nondetect": "half"}, "carried at zero"),
    "resample left out of the September averages": ({"resample_in_month": False}, "counts in the month's average"),
    "technical review criterion of 1.4 applied to metals": ({"trc": "1.4"}, "technical review criterion of 1.2"),
    "24 hours counted from the plant manager being told": ({"notice_from_manager": True}, "from the 07:50 event"),
    "July and August flow and pH taken from the plant manager's note": ({"manager_attestation": True}, "logs say otherwise"),
    "pH range read as excluding 6.0 and 9.0": ({"range_exclusive": True}, "inside the range"),
}

EXPECTED = {
    "Jul Cu monthly average": "4.090", "Jul Cu valid samples": "1", "Jul Cd valid samples": "1", "Jul Cr valid samples": "1",
    "Jul Ni valid samples": "1", "Jul Zn valid samples": "0", "Jul Zn monthly average": "none",
    "Jul CN valid samples": "1", "Jul CN monthly average": "0.270", "Jul CN days between the valid samples": "none",
    "Aug Cu valid samples": "3", "Aug Cu monthly average": "3.977", "Aug Cu daily maximum": "4.330",
    "Aug Ni valid samples": "3", "Aug Ni monthly average": "2.083", "Aug Zn monthly average": "1.093",
    "Aug Cd monthly average": "0.005", "Aug Cr monthly average": "0.697",
    "Aug CN valid samples": "2", "Aug CN monthly average": "0.255", "Aug CN days between the valid samples": "6",
    "Aug Cu days between the valid samples": "14",
    "Sep Cu monthly average": "2.053", "Sep Cu daily maximum": "2.960", "Sep Cu valid samples": "3",
    "Sep Zn monthly average": "1.653", "Sep Zn daily maximum": "3.140",
    "Sep Cd monthly average": "0.004", "Sep CN monthly average": "0.240", "Sep CN valid samples": "1",
    "Sep CN days between the valid samples": "none",
    "cyanide hold hours VP-260721": "339.8", "cyanide hold hours VP-260505": "335.7", "cyanide hold hours VP-260811": "367.1",
    "replacement known VP-260909 CN": "09/25/2026 09:40", "replacement known VP-260721 CN": "07/30/2026 14:05",
    "August 31 daily flow": "34598", "August 31 register as logged": "1137773",
    "September 9 composite period end": "06:40",
    "second quarter report, days after its due date": "47", "second quarter report, forty-fifth day": "08/29/2026",
    "SNC Cu measurements": "14", "SNC Cu above limit": "7", "SNC Cu above TRC": "4",
    "SNC Cu share above TRC pct": "28.6", "SNC Cu share above limit pct": "50.0", "SNC Cu TRC threshold": "4.056",
    "SNC Zn measurements": "13", "SNC Zn above limit": "4", "SNC Zn above TRC": "4",
    "SNC Zn share above TRC pct": "30.8", "SNC Zn TRC threshold": "3.132",
    "SNC Cd measurements": "14", "SNC Cr measurements": "14", "SNC Ni measurements": "14", "SNC CN measurements": "10",
    "copper measurement of 08/19/2026": "3.86", "zinc measurement of 08/19/2026": "1.145",
    "metals hold days VP-260407": "37", "cyanide hold days VP-260811": "15", "cyanide hold days VP-260505": "14",
    "Jul highest daily flow": "44880", "Jul days above the flow limit": "0", "July 28 daily flow": "44880",
    "July 17 daily flow": "30947",
    "Aug highest daily flow": "46150", "Aug days above the flow limit": "1", "August 13 daily flow": "46150",
    "Sep highest metered day": "43650", "September 9 metered flow": "43650", "September 9 discharge": "46550",
    "Sep highest daily flow": "46550", "Sep days above the flow limit": "1",
    "Jul in-line pH high": "9.0", "Aug in-line pH high": "9.2", "Sep in-line pH low": "5.8",
    "Aug grab pH high": "7.5", "Sep grab pH high": "7.9", "Jul grab pH high": "8.4",
    "hours from the overflow to the telephone notice": "32.67",
    "minutes from the pH excursion to the telephone notice": "70",
    "repeat due VP-260616 Cu": "07/26/2026", "first valid repeat VP-260616 Cu": "VP-260721 issued 07/30/2026",
    "repeat due VP-260616 Zn": "07/26/2026", "first valid repeat VP-260616 Zn": "VP-260811 issued 08/27/2026",
    "repeat due VP-260721 Cu": "08/29/2026", "repeat due VP-260811 Cu": "09/26/2026",
    "repeat due VP-260818 Cu": "09/25/2026", "repeat due VP-260825 Cu": "10/14/2026",
    "repeat due VP-260909 Zn": "10/15/2026",
    "notice due VP-260721 Cu": "07/31/2026 14:05", "notice hours VP-260721 Cu": "19.58",
    "notice due VP-260811 Cu": "08/28/2026 09:30", "notice hours VP-260811 Cu": "30.67",
    "notice due VP-260818 Cu": "08/27/2026 15:40", "voicemail hours VP-260818 Cu": "25.42",
    "notice due VP-260825 Cu": "09/15/2026 10:15",
    "notice due VP-260909 Zn": "09/16/2026 11:20", "notice hours VP-260909 Zn": "22.75",
    "first quarter report, days after its due date": "43", "first quarter report, forty-fifth day": "05/30/2026",
    "authorized representative on the permit": "Harlan Vandeveer, President",
}

EXPECTED_STANDINGS = {
    "plant, six-month review": "Significant noncompliance",
    "first quarter report under the 45-day arm": "Not counted",
    "second quarter report under the 45-day arm": "Significant noncompliance",
    "September 9 zinc cause": "Not established", "August 31 flow": "Positive",
    "replacement after VP-260707 Cd": "Collected", "replacement after VP-260707 Cr": "Collected",
    "replacement after VP-260707 Cu": "Collected", "replacement after VP-260707 Ni": "Collected",
    "replacement after VP-260707 Zn": "Not collected",
    "replacement after VP-260721 Zn": "Not collected", "replacement after VP-260721 CN": "Not collected",
    "replacement after VP-260811 CN": "Not collected", "replacement after VP-260909 CN": "Not collected",
    "SNC Cu": "Not in significant noncompliance", "SNC Zn": "Not in significant noncompliance",
    "SNC Cd": "Not in significant noncompliance", "SNC Cr": "Not in significant noncompliance",
    "SNC Ni": "Not in significant noncompliance", "SNC CN": "Not in significant noncompliance",
    "Jul Cu frequency status": "Below frequency", "Jul Zn frequency status": "Below frequency",
    "Jul Zn monthly average status": "No valid sample", "Jul CN frequency status": "Below frequency",
    "Jul Cu monthly average status": "Exceeded",
    "Aug Cu monthly average status": "Exceeded", "Aug Ni monthly average status": "Met", "Aug Ni frequency status": "Met",
    "Aug CN frequency status": "Below frequency", "Sep Zn monthly average status": "Exceeded",
    "Sep Cu monthly average status": "Met", "Sep CN frequency status": "Below frequency",
    "Jul flow": "Met", "Aug flow": "Exceeded", "Sep flow": "Exceeded",
    "Jul in-line pH": "Met", "Aug in-line pH": "Exceeded", "Sep in-line pH": "Exceeded",
    "Jul grab pH": "Met", "Aug grab pH": "Met", "Sep grab pH": "Met",
    "repeat sampling VP-260616 Cu": "Late", "repeat sampling VP-260616 Zn": "Late",
    "repeat sampling VP-260721 Cu": "Met",
    "repeat sampling VP-260811 Cu": "Met", "repeat sampling VP-260818 Cu": "Met",
    "repeat sampling VP-260825 Cu": "Met", "repeat sampling VP-260909 Zn": "Met",
    "telephone notice VP-260721 Cu": "Met", "telephone notice VP-260811 Cu": "Late",
    "telephone notice VP-260818 Cu": "Late", "telephone notice VP-260825 Cu": "Not made",
    "telephone notice VP-260909 Zn": "Met",
    "overflow telephone notice": "Late", "pH excursion telephone notice": "Met",
    "August 13 flow telephone notice": "Not made", "August 20 pH telephone notice": "Not made",
}

if __name__ == "__main__":
    rep = Report()
    figures, standings = derive()
    if "--dump" in sys.argv:
        for k in sorted(figures):
            print("F", k, "=", figures[k])
        for k in sorted(standings):
            print("S", k, "=", standings[k])
    for label, golden in EXPECTED.items():
        rep.expect(label, figures.get(label), golden)
    rep.expect("quarter total ties to the registers", figures["quarter flow total"], figures["quarter flow total from the registers"])
    for label, golden in EXPECTED_STANDINGS.items():
        rep.expect(label, standings.get(label), golden)
    unexpected = sorted(k for k in standings if k.startswith(("repeat sampling", "telephone notice", "replacement after")) and k not in EXPECTED_STANDINGS)
    rep.expect("no notice or repeat line beyond the golden's", ", ".join(unexpected) or "none", "none")
    rep.sensitivity(lambda **kw: derive(**kw)[1], VARIANTS)
    rep.finish()
