"""Group 1: prompt frame rules (P0-P7).

P0-P3 were tools/prompt_check.py until 2026-09-04; its notes follow.
Prompt-quality checks, in one place.

    .venv/bin/python tools/prompt_check.py submissions/NN-task-name

Prompt rules had been scattered: P1 sat inline in the middle of `check_rubric()` in
autoeval_check.py, the missing-file sweep in audit_task.py, prompt recycling in
originality_check.py (which the gate never calls), and nothing at all covered the two
platform checks that failed a task on 2026-08-31. This module is the
one home for the rules that read instruction.md, so a prompt finding lands beside its siblings
instead of in whichever file grew last.

WHAT THE PLATFORM ACTUALLY CHECKS (docs/submission/platform/task-lifecycle.md, captured 2026-08-26)

  Stage 1 iv, "Prompt Quality Check": own voice; specific expert context; complex enough
  for multiple reasoning steps and 5 hours; no spelling or grammar errors; a single
  concrete output deliverable AND a file name; the input files referenced explicitly, so
  the task cannot be answered from the instructions alone; and uniqueness against the
  contributor's own prior prompts.

  Stage 4 iv, "Prompt verbosity": LLM-style tells, naming "excessive scene-setting,
  INPUT CATALOGUING, and scaffolding phrases".

Only the mechanical ones live here. Voice, expert context, complexity and grammar are
judgement and stay with the human checks in gate_families.py; uniqueness is U1/U2 in
originality_check.py.

  P1  the prompt names its deliverable, with an explicit naming cue
  P2  the prompt names at least one input source
  P3  the prompt does not catalogue its inputs

P1 and P2 are a BAND on the same dial and that is why they sit together. Naming no input
fails the platform's "Prompt input files reference check"; glossing nearly every input
fails its "Prompt human voice check". One task failed BOTH in one
afternoon, in that order, because the fix for the second overshot into the first.

Generated 2026-09-04 from autoeval_check.py; every check body is verbatim.
"""
import re
import sys
from pathlib import Path
from ..common import split_sentences
from ..core import check, emit, recommend, REPORT, OPTIONS


FILE_RE = r"[\w-]+\.(?:xlsx|csv|docx|pdf|pptx|json|xml|md)"

# P1: the naming cues that make a filename read as THE OUTPUT rather than a prior file.
# "One workbook back: X.xlsx" FAILed the platform's own output-filename check
# (2026-08-19) because the elliptical colon parsed as a reference to an existing
# workbook, so a bare mention never counts.
NAME_CUE_RE = re.compile(
    r"sav\w{0,4}\s+(it\s+|the\s+\w+\s+)?as\b|nam\w+\b|call\w*\s+(it|the\s+file)"
    r"|file\s*name|under\s+the\s+name|titled", re.I)
CREATION_CUE_RE = re.compile(
    r"\b(build|creat\w+|make|put\s+together|send(\s+me)?(\s+back)?|need|deliver\w*"
    r"|return\w*|want)\b[^.\n]{0,40}\b(workbook|file|spreadsheet)\b[,:]?\s*$", re.I)

# P3: a filename standing as the COMPLEMENT OF A COPULA is a definition of that file,
# which is what "input cataloguing" means: "their manifest is ratcliff_disposal_manifest.xlsx",
# "his bid is kunkel_salvage_bid.docx", "twelve months of movement is units_by_month.csv".
# A filename reached through a PREPOSITION ("off the pages in vendor_price_pages.xlsx") is
# an ordinary reference and is deliberately not matched.
CATALOGUE_RE = re.compile(rf"\b(?:is|are|being)\s+(?:in\s+)?({FILE_RE})\b", re.I)

# Calibrated on the one labelled platform FAIL and the 13 prompts that have not failed
# this check. The failing prompt as submitted: 12 definitions over 15 inputs = 0.80.
# The rest of the catalogue: 0 to 6 definitions, ratio 0.60 and below, every one of them
# naming 100% of its inputs. So the SHARE OF INPUTS NAMED is NOT the signal and a rule
# built on it would fire on all thirteen - the signal is the definition construction.
# Both gates must trip, so a small packet is not condemned by ratio alone.
CATALOGUE_MIN = 5
CATALOGUE_RATIO = 0.70


def _findings(folder):
    folder = Path(folder)
    prompt, ind, sol = folder / "instruction.md", folder / "inputs", folder / "solution"
    out = []
    if not prompt.exists():
        return [("ERROR", "P0", "no instruction.md in the task folder")]
    text = prompt.read_text(encoding="utf-8", errors="ignore")

    # ---- P1: the deliverable is named, and named as the deliverable -------------------
    if sol.is_dir():
        for p in sorted(sol.iterdir()):
            if p.suffix not in (".xlsx", ".docx", ".csv", ".pdf", ".pptx"):
                continue
            spots = [m.start() for m in re.finditer(re.escape(p.name), text)]
            if not spots:
                out.append(("ERROR", "P1",
                            f"prompt never names the deliverable file {p.name} - the platform's "
                            "'Prompt Quality Check' requires a single concrete deliverable and a "
                            "file name"))
            elif not any(NAME_CUE_RE.search(text[max(0, i - 80):i])
                         or CREATION_CUE_RE.search(text[max(0, i - 80):i]) for i in spots):
                out.append(("ERROR", "P1",
                            f"prompt mentions {p.name} but with no output-naming cue (saved as / "
                            "named / call it / file name) in the 80 chars before it - an elliptical "
                            "construction reads as a PRIOR file, not the deliverable "
                            "(2026-08-19: 'One workbook back: X.xlsx' FAILed)"))

    # ---- P2 and P3: the band ----------------------------------------------------------
    if ind.is_dir():
        inputs = {q.name for q in ind.iterdir() if q.is_file()}
        named = sorted(n for n in inputs if n in text)
        if inputs and not named:
            out.append(("ERROR", "P2",
                        f"prompt names none of the {len(inputs)} input files - the platform's "
                        "'Prompt input files reference check' FAILs a prompt that points only at "
                        "'the folder', since the uploaded archive's own filename does not count "
                        "and the deliverable is an output, not a source "
                        "(2026-08-31). Name the source whose precedence "
                        "or governance changes the answer"))
        defined = sorted({m.group(1) for m in CATALOGUE_RE.finditer(text)} & inputs)
        ratio = len(defined) / len(inputs) if inputs else 0
        if len(defined) >= CATALOGUE_MIN and ratio >= CATALOGUE_RATIO:
            out.append(("ERROR", "P3",
                        f"prompt catalogues its inputs: {len(defined)} of {len(inputs)} input files "
                        f"({ratio:.0%}) are introduced as '... is <filename>', a definition of what "
                        "the file holds. The platform's 'Prompt human voice check' FAILs this as a "
                        "STRONG structural tell, 'nearly every referenced file is paired with an "
                        "explanation of what it contains', and stage 4 names input cataloguing a "
                        "prompt-verbosity tell (2026-08-31, 12 of 15). "
                        f"Definitions: {', '.join(defined[:4])}"
                        f"{'...' if len(defined) > 4 else ''}. Keep the ones whose precedence or "
                        "governance changes the answer and let the rest of the folder speak for "
                        "itself - but keep at least one, or P2 fails at the other end of the band"))
    return out


def check_folder(folder):
    """[(level, code, message)] for one task folder. Used by autoeval_check.py."""
    return _findings(folder)


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    rc = 0
    for target in argv[1:]:
        found = _findings(target.rstrip("/"))
        print(f"== {target} ==")
        for level, code, msg in found:
            print(f"  {level:5s} [{code}] {msg}")
            rc = 1
        if not found:
            print("  clean")
    return rc


# P2 (2026-08-31, pre-submission): the platform's Prompt human voice
# check FAILed a prompt it called "notably natural" on one structural rule - "nearly every
# named file receives an individual content or purpose gloss", which it scores as a STRONG
# tell whatever the surrounding voice. The glossed forms are mechanical: "<what it is> is
# <file>", "<file> is/holds/carries <what it is>", and "<what it is> (<file>)". The
# desk rule already in memory (2026-08-17) says name every input file, woven
# into the narrative, with no purpose clause; the platform check adds the threshold:
# gloss only the few distinctions that are genuinely unclear and let the names speak.
_P2_FILE_RE = re.compile(r"[\w-]+\.(?:xlsx|docx|csv|pdf|pptx)\b")


# 2026-09-10: the platform FAILed
# "visit_log.csv. It contains a row for every visit..." / "account_roster.csv
# and includes the route assignment..." / "route_standards.docx. It defines..." as
# formulaic per-file glosses, and this check stayed silent: the before-window of 12 chars
# ended in "the file " and the after-window never looked past the sentence break. Both
# windows now reach the next sentence's opener.
_P2_BEFORE_RE = re.compile(r"(?:\bis|\bare|\bwas|\bwere|\bcalled|\bnamed|\bfile|\()\s*$")


_P2_GLOSS_VERBS = r"is|are|holds|carries|has|covers|lists|shows|contains|includes|defines|records|gives|sets|details"
_P2_AFTER_RE = re.compile(
    r"^\s*(?:\)|,\s+(?:the|which|where|with|and)\b|(?:,?\s+and)?\s+(?:" + _P2_GLOSS_VERBS + r")\b"
    r"|[.;:]\s+(?:It|This|That|Which)\s+(?:" + _P2_GLOSS_VERBS + r")\b)")


# P4 - PROMPT FRAME (2026-09-02, a REJECTION). The task was rejected on
# prompt quality alone: "the task itself, input files, golden solution, and rubric are
# otherwise strong, but the prompt does not explicitly establish that the work is U.S.-based
# and does not clearly frame the analyst's professional role or assumed purchasing expertise
# level. Add a brief opening that identifies the requester/analyst as U.S.-based and states
# the expected procurement or purchasing experience." Both halves sit in the project
# house rules (a workflow "in the United States"; no job outside the US), and a sweep
# found no prompt in this catalogue establishing either, so this is a
# portfolio-wide exposure rather than one task's slip.
#
# Three parts, all read out of the prompt's OPENING (the rejection asked for "a brief
# opening", and a state named four paragraphs down does not frame anything):
#   P4a  the work is placed in the US - the state named, or the country said plainly. A town
#        name alone does not carry it; a reader is not required to know where Kewanee is.
#   P4b  the requester says what they do. "my desk" does NOT count: the rejected prompt
#        carried it and the finding still named no role framed.
#   P4c  the prompt says what the reader is expected to already know (the purchasing or
#        procurement experience assumed).
# And the repair must not swing into the banned persona shape, "You are a financial
# analyst. Utilizing your expertise ..." - P4d fires on that persona shape. All three halves
# are written in the requester's own voice, a plain sentence or two, e.g. "I buy the
# mechanical line for a wholesaler in north central Illinois ... whoever picks this up should
# have a few years of purchasing behind them."
_P4_OPENING_MIN = 900


_P4_STATE_NAMES = (
    "Alabama|Alaska|Arizona|Arkansas|California|Colorado|Connecticut|Delaware|Florida"
    "|Georgia|Hawaii|Idaho|Illinois|Indiana|Iowa|Kansas|Kentucky|Louisiana|Maine|Maryland"
    "|Massachusetts|Michigan|Minnesota|Mississippi|Missouri|Montana|Nebraska|Nevada"
    "|New Hampshire|New Jersey|New Mexico|New York|North Carolina|North Dakota|Ohio"
    "|Oklahoma|Oregon|Pennsylvania|Rhode Island|South Carolina|South Dakota|Tennessee"
    "|Texas|Utah|Vermont|Virginia|Washington|West Virginia|Wisconsin|Wyoming"
    "|District of Columbia")


_P4_STATE_ABBR = (
    "AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV"
    "|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY|DC")


# Case-SENSITIVE on purpose: a case-insensitive \bUS\b matches the pronoun "us", which is how
# an earlier cut of this check passed prompts that said nothing about the country at all
# ("the April bills start running out on us").
_P4_US_RE = re.compile(r"\bU\.S\.A?\.?|\bUSA?\b|\bUnited States\b")


# A state name only counts as a location, not as somebody's surname: require a locational cue
# ("in north central Illinois", "Kewanee, Illinois", "our Illinois branches") in front of it.
_P4_STATE_RE = re.compile(
    r"(?:\b(?:in|near|around|across|throughout|outside|from|of|to|into|our|the)\b[^.\n]{0,40}?|,\s*)"
    r"\b(?:" + _P4_STATE_NAMES + r")\b")


_P4_STATE_ABBR_RE = re.compile(r",\s(?:" + _P4_STATE_ABBR + r")\b")


# The requester's own role. "my desk", "my folder", "my inbox" are deliberately absent: they
# name a place work lands, not a job, and the rejected prompt proved a reader reads them
# that way too.
# Hazy port, 2026-09-21. P4 and P6 used to read expert context
# through a narrow trade lexicon - purchasing, buying, procurement, distribution,
# wholesale, inventory, freight. Hazy spans 13 O*NET job families and 64 occupations, so
# that lexicon misses almost every prompt this desk will now write: a phlebotomist's years
# on the bench, a paralegal's docket, a surveyor's fieldwork. One shared vocabulary covers
# all of them, ordered by family. It stays a list of DOMAIN nouns, never generic words like
# "work" or "experience", because P4 fires on the pairing of a duration with a domain.
_DOMAIN_WORDS = (
    # management, purchasing, compliance, HR, finance, quality
    r"purchasing|buying|procurement|supply|sourcing|vendor|contract|compliance|regulatory|"
    r"human resources|personnel|hiring|marketing|treasury|controller|budget|audit|"
    r"quality (?:control|assurance)|operations|"
    # healthcare practitioner and support
    r"clinical|clinic|patient care|patient|bedside|nursing|ward|floor|triage|"
    r"phlebotomy|venipuncture|draw|specimen|respiratory|dental|hygien\w*|pharmacy|"
    r"dispensing|prehospital|ambulance|EMS|paramedic|transcription|"
    r"(?:occupational|physical) therapy|home care|long[- ]term care|"
    # life, physical and social science
    r"laborator\w+|\blab\b|bench|assay|sampling|field ?work|survey work|specimens?|"
    r"research|analytic\w*|geolog\w*|atmospheric|environmental|soil|agronom\w*|"
    r"microbiolog\w*|biochem\w*|toxicolog\w*|econometric\w*|"
    # legal
    r"legal|litigation|docket|casework|caseload|title|conveyanc\w*|abstract\w*|"
    r"paralegal|chambers|mediation|arbitration|deposition|discovery|"
    # architecture and engineering
    r"engineering|design|drafting|CAD|survey(?:ing)?|geodetic|structural|electrical|"
    r"civil|manufacturing|fabrication|tolerance|"
    # production, installation, transport, grounds, food
    r"machining|machine shop|shop floor|inspection|metrolog\w*|packaging|production|"
    r"maintenance|repair|fleet|dispatch|warehouse|distribution|inventory|freight|"
    r"wholesale|logistics|materials handling|housekeeping|janitorial|custodial|"
    r"food service|kitchen|front of house|back of house|line cook|"
    # community, social service, education, library
    r"counsel(?:l)?ing|behavioral health|substance (?:abuse|use)|social work|case management|"
    r"curriculum|instructional|classroom|cataloguing|cataloging|collections|circulation"
)


_P4_ROLE_RE = re.compile(
    r"\bI(?:'m| am) (?:the|a|an|one of the)\s+[a-z]"
    r"|\bI (?:buy|do the buying|run|manage|handle|head|oversee|supervise|purchase|source"
    r"|look after|cover|carry|write|place) (?:the|our|a|my|all|every|for|here|at)\b"
    r"|\bmy (?:job|role|title|line|book|desk job|patch|territory|accounts|vendors|suppliers)\b"
    r"|\bas (?:the|our) [a-z]+(?: [a-z]+)? (?:buyer|manager|analyst|planner|agent|lead|clerk|supervisor)\b"
    r"|\bI(?:'ve| have) (?:bought|run|managed|handled|covered) (?:this|the|our)\b", re.I)


# What the reader is expected to bring. Kept tight: a bare "should have" matches "the claim
# should have been filed", which is not an expertise statement.
_P4_EXPERIENCE_RE = re.compile(
    r"\b(?:few|several|couple of|\d+|ten|five|three|two)\s*(?:\+|plus)?\s*years?\b[^.\n]{0,60}"
    r"\b(?:" + _DOMAIN_WORDS + r"|behind (?:them|you|it))\b"
    r"|\byears? (?:of|in|on) (?:the )?(?:" + _DOMAIN_WORDS + r")\b"
    r"|\bshould (?:already )?(?:know|be comfortable|be familiar|understand|be able to read)\b"
    r"|\bshould have\b[^.\n]{0,40}\b(?:experience|years|background|behind)\b"
    r"|\bneeds? to (?:know|be comfortable|be familiar)\b"
    r"|\b(?:" + _DOMAIN_WORDS + r") (?:experience|background)\b"
    r"|\bexperience (?:in|with|as|around) (?:" + _DOMAIN_WORDS + r")\b"
    r"|\bsomeone who(?:'s| has| is)\b[^.\n]{0,60}\b(?:" + _DOMAIN_WORDS + r")\b"
    # credential forms, which carry the expert frame in most of Hazy's licensed
    # occupations the way "years of purchasing" carries it for a buying role
    r"|\b(?:board[- ]certified|licensed|registered|credentialed|chartered|"
    r"certified|accredited)\b[^.\n]{0,40}"
    r"|\b(?:RN|LPN|CNA|EMT|NP|PA|MD|DO|PhD|PE|RPh|CPA|JD)\b"
    # woven forms (a rejection, 2026-09-05): the experience stated as the
    # reason for the handoff, addressed to the reader, rather than as a gate on "whoever picks
    # this up" - "you have a few years of distribution operations behind you"
    r"|\byou (?:have|know|can read)\b[^.\n]{0,60}\b(?:years|" + _DOMAIN_WORDS + r")\b",
    re.I)


# P6 - the P4 frame delivered as a SELF-INTRODUCTION TO A COWORKER (REJECTED, 2026-09-05).
# The prompt opened by introducing the company, its trade and its town: "I run the warehouse
# and the pipe yard for <Company>, a pipe, valve and fitting wholesaler in <Town>,
# <State> ... Whoever picks this up should have a few years of distribution operations
# behind them." The finding: "Why would you say this to someone who works with you at the
# same company? They are your coworker. They know what the company is and what you do...
# Remove the entire first paragraph which contains no useful info and sounds LLM generated.
# If that info is needed for the LLM then include it, naturally, in the 'conversation'
# prompt." P4 stays (that rejection is real too); the frame has to be carried inside the ask,
# never as a paragraph describing the company and the reader to a colleague. Two shapes:
#   P6a  "I <run/am/...> <thing> for/at <Company>, a <trade> wholesaler in <Town>, <State>"
#   P6b  "whoever picks this up should ..." - gating the reader instead of addressing them
_P6_SELF_INTRO_RE = re.compile(
    r"\bI (?:run|am|manage|handle|head|oversee|buy|work|cover)\b[^.\n]{0,90}?\b(?:for|at|with) [A-Z][^.\n]{0,60}?,\s*an? "
    r"[^.\n]{0,70}?\b(?:wholesaler|distributor|supply house|supplier|dealer|company|manufacturer|jobber"
    r"|practice|clinic|hospital|health system|laborator\w+|firm|partnership|agency|"
    r"district|authority|department|institute|university|college|library|nonprofit)\b"
    r"[^.\n]{0,60}?\bin [A-Z][a-z]+(?: [A-Z][a-z]+)?,\s*[A-Z]")
_P6_GATEKEEP_RE = re.compile(
    r"\b(?:whoever|whomever|anyone who|anybody who) (?:picks|takes|gets|has|ends up with|inherits) (?:this|it)\b"
    r"[^.\n]{0,60}?\bshould\b", re.I)


_P4_PERSONA_RE = re.compile(
    r"\bYou are (?:a|an|the)\b|\bAs (?:a|an|the) [a-z ]{0,30}(?:analyst|buyer|manager|agent|"
    r"engineer|scientist|technician|nurse|aide|therapist|counsel(?:l)?or|paralegal|"
    r"supervisor|coordinator|specialist|inspector|machinist|surveyor|librarian)\s*,\s*you\b"
    r"|\b(?:utilizing|leveraging) your (?:expertise|experience|knowledge)\b", re.I)


def _p4_opening(text):
    """The prompt's opening: whole paragraphs, at least _P4_OPENING_MIN characters of them."""
    window = ""
    for para in text.split("\n\n"):
        window = f"{window}\n\n{para}" if window else para
        if len(window) >= _P4_OPENING_MIN:
            break
    return window


@check(codes=['P4'], rules=['PRE-FRAME'], needs=['prompt'], params=['folder'])
def check_prompt_role_and_locale(folder):
    """The prompt's opening frames the US setting, the requester's role and the expertise the reader brings."""
    prompt = folder / "instruction.md"
    if not prompt.exists():
        return
    text = prompt.read_text(encoding="utf-8")
    opening = _p4_opening(text)

    missing = []
    if not (_P4_US_RE.search(opening) or _P4_STATE_RE.search(opening)
            or _P4_STATE_ABBR_RE.search(opening)):
        missing.append("P4a the work is US-based (name the state, or say the country plainly "
                       "- a town name does not carry it)")
    if not _P4_ROLE_RE.search(opening):
        missing.append("P4b what the requester does (\"my desk\" does not count - the rejected "
                       "prompt had it)")
    if not _P4_EXPERIENCE_RE.search(opening):
        missing.append("P4c the purchasing or procurement experience the reader is expected "
                       "to bring")
    if missing:
        emit("ERROR", "[P4] instruction.md's opening does not establish " + "; ".join(missing) +
                      " - a task was REJECTED on this alone (2026-09-02) with its "
                      "inputs, golden and rubric all called strong. Add a brief opening in the "
                      "requester's own voice, inside the first ~900 characters")
    if _P4_PERSONA_RE.search(text):
        emit("ERROR", "[P4] instruction.md uses the persona shape the house rules ban "
                      "bad example (\"You are a financial analyst. Utilizing your expertise "
                      "...\"). Frame the role as the requester talking about themselves, never "
                      "as an instruction addressed to the solver")


@check(codes=['P6'], rules=['PRE-FRAME'], needs=['prompt'], params=['folder'])
def check_prompt_self_introduction(folder):
    """The prompt's frame is woven into the requester's own voice, never written as a self-introduction to a coworker."""
    prompt = folder / "instruction.md"
    if not prompt.exists():
        return
    text = prompt.read_text(encoding="utf-8")
    m = _P6_SELF_INTRO_RE.search(text)
    if m:
        emit("ERROR", f'[P6] instruction.md introduces the company to a coworker: "{m.group(0)[:90]}..." - '
                      "a task was REJECTED (2026-09-05) on this "
                      "paragraph (\"They are your coworker. They know what the company is and what you "
                      "do ... sounds LLM generated\"). Keep P4a-c but carry them inside the ask: the "
                      "state on a place the work touches, the role as ownership of the problem, the "
                      "experience as the reason for the handoff (docs/submission/workflows/02-prompt-writing.md, P6)")
    m = _P6_GATEKEEP_RE.search(text)
    if m:
        emit("ERROR", f'[P6] instruction.md gates the reader instead of addressing them: "{m.group(0)[:80]}" - '
                      "the same rejected paragraph; state the experience as why the work is being handed "
                      "over (\"you have a few years of distribution operations behind you\"), never as a "
                      "test for whoever picks it up")


# P7 - REPETITIVE SENTENCE OPENERS (2026-09-10).
# The platform's Prompt human voice check FAILed the deliverable paragraph as "a repetitive,
# templated pattern ('It should show...', 'It should list...', 'It should recommend...',
# 'Finally, it should be explicit...')" beside the per-file glosses P5 covers. Three or more
# sentences in one paragraph opening on the same two-word stem is that shape, after a leading
# connective (Finally, Then, Also, Next, Lastly, And, But) is dropped.
_P7_CONNECTIVE_RE = re.compile(r"^(?:finally|then|also|next|lastly|and|but|first|second|third),?\s+", re.I)


@check(codes=['P7'], rules=['PRE-VERBOSE'], needs=['prompt'], params=['folder'])
def check_repetitive_openers(folder):
    """No paragraph of the prompt opens three or more sentences on the same two-word stem."""
    prompt = folder / "instruction.md"
    if not prompt.exists():
        return
    text = prompt.read_text(encoding="utf-8")
    for para in re.split(r"\n\s*\n", text):
        sents = [x.strip() for x in split_sentences(para) if x.strip()]
        if len(sents) < 3:
            continue
        stems = {}
        for sent in sents:
            words = re.findall(r"[A-Za-z']+", _P7_CONNECTIVE_RE.sub("", sent))[:2]
            if len(words) == 2:
                stem = " ".join(w.lower() for w in words)
                stems[stem] = stems.get(stem, 0) + 1
        for stem, n in stems.items():
            if n >= 3:
                emit("ERROR", f"[P7] {n} sentences in one paragraph of instruction.md open on '{stem} ...' - "
                              "the platform's Prompt human voice check FAILs this as a repetitive, "
                              "templated pattern ('It should show... It should list... It should "
                              "recommend... Finally, it should be explicit', 2026-09-10); vary the "
                              "sentences so each ask carries its own shape")


def _p5_prompt_glosses(folder):
    """At most half of the input files the prompt names carry an individual content or purpose gloss.

    Since: 2026-08-31; both gloss windows widened 2026-09-10.
    Source: the platform's Prompt human voice check ('nearly every named file receives an individual gloss').
    Drift-notes: emitted as P2 until 2026-09-04; P2 now means the prompt names no input source at all.
    """
    prompt = folder / "instruction.md"
    if not prompt.exists():
        return
    text = prompt.read_text(encoding="utf-8")
    sol = folder / "solution"
    outputs = {p.name for p in (sol.iterdir() if sol.is_dir() else [])}
    files = [m for m in _P2_FILE_RE.finditer(text) if m.group(0) not in outputs]
    if len(files) < 3:
        return
    glossed = []
    for m in files:
        before = text[max(0, m.start() - 24):m.start()]
        after = text[m.end():m.end() + 24]
        if _P2_BEFORE_RE.search(before) or _P2_AFTER_RE.match(after):
            glossed.append(m.group(0))
    if len(glossed) >= 0.5 * len(files):
        emit("ERROR", f"[P5] {len(glossed)} of {len(files)} input files named in instruction.md carry an "
                      f"individual gloss ({', '.join(glossed[:3])}...) - the platform's Prompt human "
                      "voice check FAILs on 'nearly every named file receives an individual content "
                      "or purpose gloss' as a STRONG structural tell even when the voice reads human "
                      "(2026-08-31). Name the files in one natural run, gloss only "
                      "the one or two distinctions that are genuinely unclear, and let the filenames "
                      "speak for the rest")


@check(codes=['P0', 'P1', 'P2', 'P3', 'P5'], rules=['PRE-FILES', 'PRE-SOURCES', 'PRE-VERBOSE'], needs=['inputs', 'prompt', 'solution'], params=['folder'])
def check_prompt_rules(folder):
    """The prompt names its deliverable with a naming cue, names at least one input source, never catalogues its inputs, and glosses at most half of the files it names.

    Codes:
      P0  the task folder carries a instruction.md
      P1  the prompt names the deliverable file, with an output-naming cue (saved as / named / call it) in the 80 chars before it
      P2  the prompt names at least one input file
      P3  the prompt does not introduce five or more inputs, 70% or more of them, as '... is <filename>'
      P5  at most half of the input files the prompt names carry an individual content or purpose gloss
    Since: P1 2026-08-19; P2 and P3 2026-08-31; P5 2026-08-31.
    Source: the platform's Prompt Quality Check, Prompt input files reference check and Prompt human voice check.
    Drift-notes: P5 was a carve-out twin (emitted as P2 until 2026-09-04), merged back 2026-09-11.
    """
    _p5_prompt_glosses(folder)     # [P5] the carve-out twin, merged back 2026-09-11
    for level, code, msg in check_folder(folder):
        emit(level, f"[{code}] {msg}")


_P8_MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"
_P8_WEEKDAY = r"(?:(?:Mon|Tues|Wednes|Thurs|Fri|Satur|Sun)day,?\s+)?"
_P8_DUE_RES = (
    re.compile(r"\b(?:need|want|have|get|see)\s+(?:it|this|that|them|these|the\s+\w+(?:\s+\w+)?)\s+(?:back\s+)?"
               r"(?:by\s+|on\s+|before\s+)?" + _P8_WEEKDAY + r"(" + _P8_MONTHS + r")\s+(\d{1,2})(?:,?\s+(\d{4}))?\b"),
    re.compile(r"\bdue\s+(?:back\s+)?(?:by\s+|on\s+)?" + _P8_WEEKDAY + r"(" + _P8_MONTHS + r")\s+(\d{1,2})(?:,?\s+(\d{4}))?\b"),
)
_P8_DATE_LINE_RE = re.compile(r"(?mi)^\s*Date:\s*" + _P8_WEEKDAY + r"(" + _P8_MONTHS + r")\s+(\d{1,2}),?\s+(\d{4})\b")


def _p8_build_date(folder):
    """The date instruction.md was first committed, following renames; today for an untracked folder."""
    import datetime as _dt
    import subprocess as _sp
    try:
        out = _sp.run(["git", "-C", str(folder), "log", "--follow", "--diff-filter=A", "--format=%ad",
                       "--date=short", "--", "instruction.md"], capture_output=True, text=True, timeout=30).stdout.split()
        if out:
            return _dt.date.fromisoformat(out[-1])
    except Exception:
        pass
    return _dt.date.today()


@check(codes=['P8'], rules=['REV-CREDIBLE'], needs=['prompt', 'folder'], params=['folder'])
def check_due_date_ahead_of_review(folder):
    """A due date the prompt gives for the deliverable, and a Date line on the golden document, fall at least 21 days after the task was built, so the in-world deadline has not already passed when the task is read.

    Since: 2026-09-15 (a rejection).
    Source: the task was built on September 1 with "I need it Tuesday, September 8" and a memo dated
    September 8; eleven rounds later the rejection called the prompt's timeline impossible, the work
    "being prepared on September 17 but due September 8".
    Drift-notes: the build date is the first commit of instruction.md (git, following renames), or today for
    a folder git does not track, such as a draft. Due dates are read only from explicit asks ("I need it
    Tuesday, September 8", "want it by ...", "due on ..."), never from scenario dates such as a meeting,
    an invoice or a notice, and a date with no year takes the build year. Leaving an absolute due date
    out of the prompt passes.
    """
    import datetime as _dt
    folder = Path(folder)
    p = folder / "instruction.md"
    if not p.is_file():
        return
    built = _p8_build_date(folder)
    floor = built + _dt.timedelta(days=21)
    months = _P8_MONTHS.split("|")
    found = []
    for rx in _P8_DUE_RES:
        for m in rx.finditer(p.read_text(encoding="utf-8", errors="ignore")):
            found.append(("instruction.md", m.group(0), m.group(1), m.group(2), m.group(3)))
    for d in sorted((folder / "solution").glob("*.docx")) if (folder / "solution").is_dir() else []:
        try:
            from ..state import document as _document
            text = "\n".join(par.text for par in _document(d).paragraphs)
        except Exception:
            continue
        for m in _P8_DATE_LINE_RE.finditer(text):
            found.append((d.name, m.group(0).strip(), m.group(1), m.group(2), m.group(3)))
    for where, phrase, month, day, year in found:
        try:
            when = _dt.date(int(year) if year else built.year, months.index(month) + 1, int(day))
        except ValueError:
            continue
        if when < floor:
            emit("ERROR", f"[P8] {where}: \"{phrase}\" is {(when - built).days} day(s) after the build on {built}; a "
                          f"deliverable date must be on or after {floor}, or the prompt gives none, because a task is "
                          "read weeks after the build and a deadline already past reads as an impossible timeline "
                          "(a rejection, 2026-09-15). Move the prompt's due date and the golden's "
                          "Date line together")
