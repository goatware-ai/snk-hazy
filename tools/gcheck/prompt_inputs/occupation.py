"""Group 1: the task's domain and O*NET occupation against the platform's closed list (M1-M3).

The form offers a CLOSED list of 14 domains and 64 occupations, which makes two things
mechanical and certain: an occupation off the list cannot be submitted at all, and a domain
that disagrees with the occupation's own O*NET job family is a form that gets bounced.

Sources: docs/submission/platform/domains-and-occupations.md (the two lists as the form
presents them) and docs/submission/platform/onet-codes.md (codes verified 2026-09-21
against onetonline.org).
"""
import re
from ..common import load_metadata
from ..core import check, emit, recommend, REPORT, OPTIONS


# The form's Domain radio. Fourteen entries: the thirteen O*NET job families the 64
# occupations actually span, plus "Healthcare Practitioners / Support", which is not an
# O*NET family and duplicates the two healthcare families either side of it.
DOMAINS = (
    "Architecture and Engineering",
    "Building and Grounds Cleaning and Maintenance",
    "Community and Social Service",
    "Educational Instruction and Library",
    "Food Preparation and Serving",
    "Healthcare Practitioners / Support",
    "Healthcare Practitioners and Technical",
    "Healthcare Support",
    "Installation, Maintenance, and Repair",
    "Legal",
    "Life, Physical, and Social Science",
    "Management",
    "Production",
    "Transportation and Material Moving",
)

# The domain the form offers that has no O*NET job family behind it. Allowed, but it tells
# a reviewer less than the specific family does, so M2 nudges rather than errors.
AMBIGUOUS_DOMAIN = "Healthcare Practitioners / Support"

# Job families as O*NET names them, mapped to the form's Domain wording where the two
# differ. The form drops "Related" from the food family.
FAMILY_TO_DOMAIN = {
    "Food Preparation and Serving Related": "Food Preparation and Serving",
}

# code -> (title as the form lists it, official O*NET title or None if identical, job family)
OCCUPATIONS = {
    "23-1022.00": ("Arbitrators, Mediators, and Conciliators", None, "Legal"),
    "11-9041.00": ("Architectural and Engineering Managers", None, "Management"),
    "19-2021.00": ("Atmospheric and Space Scientists", None, "Life, Physical, and Social Science"),
    "19-1021.00": ("Biochemists and Biophysicists", None, "Life, Physical, and Social Science"),
    "11-9041.01": ("Biofuels/Biodiesel Technology and Product Development Managers", None, "Management"),
    "19-1029.01": ("Bioinformatics Scientists", None, "Life, Physical, and Social Science"),
    "19-4021.00": ("Biological Technicians", None, "Life, Physical, and Social Science"),
    "19-1029.04": ("Biologists", None, "Life, Physical, and Social Science"),
    "19-2031.00": ("Chemists", None, "Life, Physical, and Social Science"),
    "17-3022.00": ("Civil Engineering Technologists and Technicians", None, "Architecture and Engineering"),
    "11-9199.02": ("Compliance Managers", None, "Management"),
    "17-2061.00": ("Computer Hardware Engineers", None, "Architecture and Engineering"),
    "29-1292.00": ("Dental Hygienists", None, "Healthcare Practitioners and Technical"),
    "19-3011.00": ("Economists", None, "Life, Physical, and Social Science"),
    "17-2071.00": ("Electrical Engineers", None, "Architecture and Engineering"),
    "29-2042.00": ("Emergency Medical Technicians", None, "Healthcare Practitioners and Technical"),
    "17-2081.00": ("Environmental Engineers", None, "Architecture and Engineering"),
    "19-2041.00": ("Environmental Scientists and Specialists",
                   "Environmental Scientists and Specialists, Including Health",
                   "Life, Physical, and Social Science"),
    "35-1012.00": ("First Line Supervisors of Food Prep and Serving Workers",
                   "First-Line Supervisors of Food Preparation and Serving Workers",
                   "Food Preparation and Serving Related"),
    "37-1011.00": ("First Line Supervisors of Housekeeping and Janitorial Workers",
                   "First-Line Supervisors of Housekeeping and Janitorial Workers",
                   "Building and Grounds Cleaning and Maintenance"),
    "53-1043.00": ("First Line Supervisors of Material Moving Operators",
                   "First-Line Supervisors of Material-Moving Machine and Vehicle Operators",
                   "Transportation and Material Moving"),
    "49-1011.00": ("First Line Supervisors of Mechanics, Installers, and Repairers",
                   "First-Line Supervisors of Mechanics, Installers, and Repairers",
                   "Installation, Maintenance, and Repair"),
    "19-1012.00": ("Food Scientists and Technologists", None, "Life, Physical, and Social Science"),
    "29-1216.00": ("General Internal Medicine Physicians", None, "Healthcare Practitioners and Technical"),
    "19-2042.00": ("Geoscientists", "Geoscientists, Except Hydrologists and Geographers",
                   "Life, Physical, and Social Science"),
    "31-1121.00": ("Home Health Aides", None, "Healthcare Support"),
    "11-3121.00": ("Human Resources Managers", None, "Management"),
    "51-9061.00": ("Inspectors, Testers, Sorters, Samplers, and Weighers", None, "Production"),
    "25-9031.00": ("Instructional Coordinators", None, "Educational Instruction and Library"),
    "23-1023.00": ("Judges, Magistrate Judges, and Magistrates", None, "Legal"),
    "23-1012.00": ("Judicial Law Clerks", None, "Legal"),
    "25-4022.00": ("Librarians and Media Collections Specialists", None, "Educational Instruction and Library"),
    "51-4041.00": ("Machinists", None, "Production"),
    "17-2112.03": ("Manufacturing Engineers", None, "Architecture and Engineering"),
    "11-2021.00": ("Marketing Managers", None, "Management"),
    "31-9092.00": ("Medical Assistants", None, "Healthcare Support"),
    "31-9094.00": ("Medical Transcriptionists", None, "Healthcare Support"),
    "21-1014.00": ("Mental Health Counselors", None, "Community and Social Service"),
    "21-1023.00": ("Mental Health and Substance Abuse Social Workers", None, "Community and Social Service"),
    "19-1029.02": ("Molecular and Cellular Biologists", None, "Life, Physical, and Social Science"),
    "11-9121.00": ("Natural Sciences Managers", None, "Management"),
    "31-1131.00": ("Nursing Assistants", None, "Healthcare Support"),
    "29-1218.00": ("Obstetricians and Gynecologists", None, "Healthcare Practitioners and Technical"),
    "31-2011.00": ("Occupational Therapy Assistants", None, "Healthcare Support"),
    "51-9111.00": ("Packaging and Filling Machine Operators and Tenders", None, "Production"),
    "23-2011.00": ("Paralegals and Legal Assistants", None, "Legal"),
    "29-2043.00": ("Paramedics", None, "Healthcare Practitioners and Technical"),
    "29-1221.00": ("Pediatricians, General", None, "Healthcare Practitioners and Technical"),
    "31-1122.00": ("Personal Care Aides", None, "Healthcare Support"),
    "31-9095.00": ("Pharmacy Aides", None, "Healthcare Support"),
    "31-9097.00": ("Phlebotomists", None, "Healthcare Support"),
    "31-1133.00": ("Psychiatric Aides", None, "Healthcare Support"),
    "11-3061.00": ("Purchasing Managers", None, "Management"),
    "11-3051.01": ("Quality Control Systems Managers", None, "Management"),
    "29-1126.00": ("Respiratory Therapists", None, "Healthcare Practitioners and Technical"),
    "21-1093.00": ("Social and Human Service Assistants", None, "Community and Social Service"),
    "19-1013.00": ("Soil and Plant Scientists", None, "Life, Physical, and Social Science"),
    "21-1011.00": ("Substance Abuse and Behavioral Disorder Counselors", None, "Community and Social Service"),
    "17-1022.00": ("Surveyors", None, "Architecture and Engineering"),
    "23-2093.00": ("Title Examiners, Abstractors, and Searchers", None, "Legal"),
    "11-3071.00": ("Transportation, Storage, and Distribution Managers", None, "Management"),
    "11-3031.01": ("Treasurers and Controllers", None, "Management"),
    "31-9096.00": ("Veterinary Assistants and Laboratory Animal Caretakers", None, "Healthcare Support"),
    "19-1023.00": ("Zoologists and Wildlife Biologists", None, "Life, Physical, and Social Science"),
}

CODE_RE = re.compile(r"^\d{2}-\d{4}\.\d{2}$")


def _norm(s):
    """Casefold and squash punctuation so a title compares on its words alone."""
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


@check(codes=['M1', 'M2', 'M3'], rules=['PRE-OCC'], needs=['metadata'], params=['folder'])
def check_metadata(folder):
    """The domain and O*NET occupation are both on the platform's closed list and agree with each other.

    Codes:
      M1  the occupation code is one of the platform's 64
      M2  the domain is one of the platform's 14 and matches the occupation's O*NET job family
      M3  the recorded occupation title matches the code, and the metadata carries no legacy "sector" key
    Since: 2026-09-21.
    Source: docs/submission/platform/domains-and-occupations.md, onet-codes.md.
    """
    meta = load_metadata(folder)
    if not meta:
        return

    occ = meta.get("onet_occupation") or {}
    code = (occ.get("code") or "").strip()
    title = (occ.get("title") or "").strip()
    domain = (meta.get("domain") or "").strip()

    # --- M3a: the legacy key --------------------------------------------------
    if "sector" in meta:
        emit("ERROR", "[M3] metadata carries a legacy \"sector\" key - Hazy has no fixed "
                      "sector. Replace it with \"domain\", one of the platform's 14 "
                      "(docs/submission/platform/domains-and-occupations.md)")

    # --- M1: the occupation ---------------------------------------------------
    if not code:
        emit("ERROR", "[M1] metadata records no O*NET occupation code. The form's first "
                      "section requires one of 64 (docs/submission/platform/onet-codes.md)")
    elif not CODE_RE.match(code):
        emit("ERROR", f"[M1] \"{code}\" is not an O*NET-SOC code (expected nn-nnnn.nn). Eight "
                      "of the platform's 64 are detail codes ending .01 to .04, so the "
                      "suffix is never optional")
    elif code not in OCCUPATIONS:
        emit("ERROR", f"[M1] {code} is not one of the platform's 64 occupations. The list is "
                      "closed: the guidelines say a domain or sector not visible in the form "
                      "is not available, so a task idea built on an off-list occupation "
                      "cannot be submitted as written "
                      "(docs/submission/platform/onet-codes.md)")

    # Every branch above is terminal: without a known code there is nothing for M2 and M3
    # to compare against. A missing return here walked a malformed code into the table
    # lookup and raised KeyError, taking the whole gate down.
    if code not in OCCUPATIONS:
        return

    form_title, official, family = OCCUPATIONS[code]

    # --- M3b: the title -------------------------------------------------------
    if title and _norm(title) not in (_norm(form_title), _norm(official or form_title)):
        want = f"\"{form_title}\"" + (f" (officially \"{official}\")" if official else "")
        emit("ERROR", f"[M3] occupation title \"{title}\" does not match {code}, which is "
                      f"{want}")

    # --- M2: the domain -------------------------------------------------------
    expected = FAMILY_TO_DOMAIN.get(family, family)
    if not domain:
        emit("ERROR", f"[M2] metadata records no domain. {code} sits in the {expected} "
                      "family, which is the domain to pick")
    elif domain not in DOMAINS:
        emit("ERROR", f"[M2] \"{domain}\" is not one of the platform's 14 domains "
                      "(docs/submission/platform/domains-and-occupations.md)")
    elif domain == AMBIGUOUS_DOMAIN and expected != AMBIGUOUS_DOMAIN:
        recommend(f"[M2] domain \"{AMBIGUOUS_DOMAIN}\" duplicates the two healthcare "
                  f"families either side of it and is not an O*NET family at all. {code} "
                  f"sits in {expected}, which tells a reviewer more")
    elif domain != expected:
        emit("ERROR", f"[M2] domain \"{domain}\" disagrees with the occupation: {code} "
                      f"({form_title}) is in the {expected} family. The four First-Line "
                      "Supervisor rows are the usual trap - they are NOT Management")


# ---------------------------------------------------------------------------
# The form's own required fields, added 2026-09-21. The form asks for four minute
# fields, a total in hours that must cover them, and at least one non-AI tool. None
# of it was checked anywhere, and all of it blocks submission.
# ---------------------------------------------------------------------------

TIME_KEYS = (
    ("time_read_minutes",    "read and understand the prompt and requirements"),
    ("time_files_minutes",   "open, skim/search, and use the reference files"),
    ("time_work_minutes",    "perform the required work"),
    ("time_qa_minutes",      "verification/QA and final review"),
)

# The form's advisory Difficulty check wants manual effort over 3 hours; the guidelines
# target 5-10. Below 3 the task is rejected as too easy, between 3 and 5 it is thin.
TOTAL_HOURS_FLOOR = 3
TOTAL_HOURS_TARGET = 5

INPUT_MIN = 2          # form section 3: "Minimum 2 files"
INPUT_PREFERRED = 3    # "3+ strongly preferred"


@check(codes=['M4', 'M5', 'M6'], rules=['PRE-OCC'], needs=['metadata'], params=['folder'])
def check_form_fields(folder):
    """The metadata carries the form's required time breakdown, tool list and input count.

    Codes:
      M4  four integer minute fields, and a total in hours at least their sum and over 3
      M5  at least one non-AI tool is logged
      M6  at least 2 input files are present, 3+ preferred
    Since: 2026-09-21.
    Source: docs/submission/platform/platform-submission-form.md section 3 (Times, Tools)
    and section 2 (File Uploader), with the Completed Task Checks panel's Difficulty note.
    """
    meta = load_metadata(folder)
    if not meta:
        return

    # --- M4: the five time values -----------------------------------------
    if "manual_time_hours" in meta:
        emit("ERROR", "[M4] metadata carries the legacy \"manual_time_hours\" key - the Hazy "
                      "form asks for four minute fields plus a total in hours. Replace it "
                      "with " + ", ".join(k for k, _ in TIME_KEYS) + " and total_time_hours")

    mins, missing = [], []
    for key, label in TIME_KEYS:
        v = meta.get(key)
        if v is None:
            missing.append(f"{key} ({label})")
        elif not isinstance(v, int) or isinstance(v, bool) or v <= 0:
            emit("ERROR", f"[M4] {key} is {v!r} - the form takes whole minutes, so it must be "
                          "a positive integer")
        else:
            mins.append(v)
    if missing:
        emit("ERROR", "[M4] metadata is missing " + "; ".join(missing) +
                      ". All five time fields are required on the form")

    total = meta.get("total_time_hours")
    if total is None:
        emit("ERROR", "[M4] metadata records no total_time_hours. The form requires a total "
                      "in hours, decimals allowed")
    elif not isinstance(total, (int, float)) or isinstance(total, bool) or total <= 0:
        emit("ERROR", f"[M4] total_time_hours is {total!r} - expected a positive number of "
                      "hours (90 minutes is 1.5)")
    else:
        if len(mins) == len(TIME_KEYS):
            floor = sum(mins) / 60
            if total + 1e-9 < floor:
                emit("ERROR", f"[M4] total_time_hours {total:g} is below the sum of the four "
                              f"parts ({sum(mins)} minutes = {floor:.2f}h). The form says the "
                              "total must be at least their sum, converted. It may be higher")
        if total < TOTAL_HOURS_FLOOR:
            emit("ERROR", f"[M4] total_time_hours {total:g} is under {TOTAL_HOURS_FLOOR} - the "
                          "form's Difficulty check wants estimated manual effort over 3 hours, "
                          "and a task under it reads as too easy for the benchmark")
        elif total < TOTAL_HOURS_TARGET:
            recommend(f"[M4] total_time_hours {total:g} clears the 3-hour floor but the "
                      "guidelines target 5-10 hours (create-the-task-guidelines.md, "
                      "\"The key rule\"). Check the task is really hard enough")

    # --- M5: tools ---------------------------------------------------------
    tools = meta.get("tools")
    if not tools or not isinstance(tools, list) or not any(str(t).strip() for t in tools):
        emit("ERROR", "[M5] metadata records no tools. The form requires at least one non-AI "
                      "tool a solver would reasonably use (Excel, SolidWorks, LabVIEW and so "
                      "on); its Completed Task Checks panel reports on it")
    else:
        ai = [t for t in tools if re.search(r"\b(?:chatgpt|gpt|claude|copilot|gemini|llm|"
                                            r"\bai\b)\b", str(t), re.I)]
        if ai:
            emit("ERROR", f"[M5] tools lists an AI assistant ({ai[0]!r}) - the field is for "
                          "NON-AI tools, and the time estimates are explicitly for completing "
                          "the task without one")

    # --- M6: input files ---------------------------------------------------
    inputs = folder / "inputs"
    if inputs.is_dir():
        n = len([f for f in inputs.iterdir()
                 if f.is_file() and not f.name.startswith((".", "~$"))])
        if n < INPUT_MIN:
            emit("ERROR", f"[M6] {n} input file(s) - the form requires a minimum of 2 "
                          "(platform-submission-form.md section 3)")
        elif n < INPUT_PREFERRED:
            recommend(f"[M6] {n} input files - 3 or more is strongly preferred, and difficulty "
                      "is supposed to come from information distributed across sources")
        declared = meta.get("input_file_count")
        if isinstance(declared, int) and declared != n:
            emit("ERROR", f"[M6] metadata says input_file_count {declared} but inputs/ holds "
                          f"{n}. A mismatch between the Input File List and the upload is "
                          "called out on the form as one of the most common reasons a "
                          "submission is sent back")
