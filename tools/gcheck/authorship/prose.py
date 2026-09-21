"""Group 3: LLM prose tells and em dashes (A6 A10).

Generated 2026-09-04 from autoeval_check.py; every check body is verbatim.
"""
import re
from ..common import _docx_text, _xlsx_all_text, _xlsx_prose, docx_emdash_stats, rubric_path, solution_files, split_sentences
from ..core import check, emit, recommend, REPORT, OPTIONS


# "X is X" / "X is still X" / "X is the whole story". The backreference is what
# keeps it tight: it fires on restatement, not on ordinary predication.
_TAUTOLOGY_RES = [
    re.compile(r"\b(\w+(?:\s+\w+){0,2})\s+(?:is|are)\s+(?:still\s+|just\s+)?\1\b", re.I),
    re.compile(r"\b(?:is|are)\s+the\s+whole\s+story\b", re.I),
    re.compile(r"\b(\w+)\s+is\s+\1[.,]", re.I),
    # head noun restated as the predicate: "Committed work is committed",
    # "policy 6.3 is still policy" — the two the adjacent-repeat form misses.
    # gap stays on ONE line: crossing a paragraph break matches unrelated list
    # items ("...attached\\nCertificates are attached") rather than a restatement.
    re.compile(r"\b(\w{5,})\b(?:[\w.\-]|[^\S\n]){0,20}?[^\S\n]+(?:is|are)\s+"
               r"(?:still\s+|just\s+|always\s+)?\1\b", re.I),
]


# Ordinary English that the restatement patterns catch by accident.
_TAUTOLOGY_OK_RE = re.compile(r"\bwhich is which\b|\bwhat is what\b|\bwho is who\b", re.I)


_SLOGAN_RES = [
    (re.compile(r"\buse it or lose it\b", re.I), "slogan"),
    (re.compile(r"\bis where the (?:money|pain|trouble|problem)\s+(?:hurts?|is|lands?)\b", re.I), "slogan"),
    (re.compile(r"\bnobody (?:promises|tells|asks|wants)\b[^.]{0,40}\bnot (?:coming|there|going)\b", re.I), "slogan"),
    (re.compile(r"\bwhere we are naked\b|\bknowing where we (?:stand|are) naked\b", re.I), "idiom for a quantity"),
    (re.compile(r"\bnot quietly (?:dropped|buried|lost)\b", re.I), "idiom for a quantity"),
    (re.compile(r"\bleave (?:them|it) and (?:they|it) (?:are|is) gone\b", re.I), "slogan"),
    (re.compile(r"\bI pulled the rest\b|\bI went and pulled\b", re.I), "first-person filler"),
    (re.compile(r"\bthe rest of it has to follow\b", re.I), "first-person filler"),
    (re.compile(r"\bhas to show as short\b|\bgoes short has to show\b", re.I), "slogan"),
    (re.compile(r"\btrying too hard\b", re.I), "slogan"),
    (re.compile(r"\bthat is close enough for (?:this|now|me)\b", re.I), "slogan"),
    (re.compile(r"\bis not (?:supply|going to happen|coming back)\.", re.I), "slogan"),
    (re.compile(r"\bwhat (?:we|they) leave on the counter\b", re.I), "idiom for a quantity"),
    (re.compile(r"\bthe one people forget\b|\bthe one thing everybody forgets\b", re.I), "slogan"),
    (re.compile(r"\bI am not spending my (?:fall|spring|summer|winter|year)\b", re.I), "slogan"),
    (re.compile(r"\bwould be buying it twice\b|\bpaying for it twice\b", re.I), "slogan"),
    # 2026-08-31, delivery-zone-reset reviewer (gate 2 round 2): six passages quoted as
    # "AI slop/slang" across two input memos; the reviewer's standard was "nobody with a
    # truly urgent issue speaks in less-than-clear language". Three new classes, probed
    # portfolio-wide before coding (one true hit, task 33's memo carrying the same
    # semicolon-balanced maxim; silent everywhere else). Catalog:
    # docs/reference/llm-prose-tells.md, classes 8-10.
    (re.compile(r"\bis (?:a|an) \w+;[^.;\n]{0,80}\bis (?:a|an) \w+\b", re.I),
     "aphoristic parallelism (semicolon-balanced maxim)"),
    (re.compile(r"\b(?:was|were) (?:old|new) when \w+ (?:was|were) (?:cheap|young|new|easy)\b", re.I),
     "idiom for a quantity"),
    (re.compile(r"\bbefore the pencil comes out\b|\bWord travels\.", re.I), "scene-setting fragment"),
    (re.compile(r"\bgoing to stay \w+ until\b", re.I), "idiom for a quantity"),
    (re.compile(r"\bstand at (?:a|the) counter and defend\b", re.I), "idiom for a quantity"),
    (re.compile(r"\bhonestly,? that is fine with me\b", re.I), "first-person filler"),
    (re.compile(r"\bmeets? (?:it |them )?cold on a\b|\bmeet cold on\b", re.I), "idiom for a quantity"),
    # 2026-09-10, review 30ce3cda (magnet-room line review, reviewer round 3): the
    # reviewer's heading was "Remove unclear LLM slang" and the standard was "State it
    # clearly". Two classes, both surviving into rev4 after the prompt was cleaned:
    # a physical surface standing in for the deliverable ("that is what goes on the
    # door", meaning the posted screening list), and an adverb-led opener whose clause
    # break is unpunctuated so the sentence reads as a fragment ("Read quickly that is
    # the clean end of the account"). Probed portfolio-wide before coding: silent on
    # every submissions/ and drafts/ file. Catalog: docs/reference/llm-prose-tells.md,
    # class 11.
    (re.compile(r"\b(?:read|taken|seen|viewed|looked at|put) "
                r"(?:quickly|fast|alone|together|straight|in isolation|side by side) "
                r"that (?:is|was)\b", re.I),
     "unpunctuated clause break reading as a fragment"),
]


# The platform's LLM-authorship phrasing judge names three more classes in every FAIL
# report ("no pre-counted lists, no 'the sections that follow…' roadmaps, no
# self-describing titles like 'Golden Solution: …'"); pbw-rebate-reconciliation drew
# llm-only 3/5 on 2026-08-31 with the reviewer-salvaged golden. These are scanned over
# EVERY string cell and sheet title of the solution workbooks, not only prose-length
# cells, because a self-describing title is short.
_SELF_DESCRIBING_RES = [
    (re.compile(r"\bgolden[\s_-]*solution\b", re.I), "self-describing title"),
    (re.compile(r"\b(?:ai|llm|model)[\s-]*(?:generated|output|response|answer)\b", re.I), "self-describing title"),
    (re.compile(r"\bas requested,? (?:this|the) (?:workbook|document|memo|report|file|deliverable)\b", re.I),
     "self-describing sentence"),
    (re.compile(r"\bthis (?:workbook|document|memo|report|deliverable|analysis) (?:provides|presents|"
                r"summari[sz]es|outlines|contains|is organi[sz]ed|walks through)\b", re.I),
     "self-describing sentence"),
    (re.compile(r"\bthe (?:sections?|pages?|paragraphs?) (?:that follow|below)\b|\bthe following (?:sections?|pages?)\b"
                r"|\bthe remainder of this (?:document|memo|report|workbook)\b", re.I), "roadmap sentence"),
    (re.compile(r"\bthere are (?:two|three|four|five|six|seven|eight|nine|ten|\d+) (?:key |main |primary |major )?"
                r"(?:considerations|factors|drivers|reasons|issues|points|takeaways|findings|steps)\b", re.I),
     "pre-counted list"),
    (re.compile(r"\b(?:two|three|four|five|six|seven|eight|nine|ten|\d+) key (?:considerations|factors|drivers|"
                r"reasons|issues|points|takeaways|findings)\b", re.I), "pre-counted list"),
]


# Scanned over EVERY string cell and sheet title, like _SELF_DESCRIBING_RES and for the
# same reason: on review 30ce3cda the metonymy was the sheet HEADING ("What goes on the
# door" at Keep out!A1), far below the prose-length threshold the slogan list works over.
# The "what goes on the X" framing is required — it is the subjectless relative that makes
# the surface stand in for the document. A declarative with a real subject ("the notice
# goes on the noticeboard") is literal and stays silent.
_SHORT_IDIOM_RES = [
    (re.compile(r"\b(?:what|that is what|which is what|this is what) goes (?:up )?on the "
                r"(?:door|wall|board|fridge)\b", re.I),
     "place metonymy for the deliverable"),
]


@check(codes=['A10'], rules=['REV-PROSE'], needs=['inputs', 'prompt', 'solution'], params=['folder'])
def check_llm_prose(folder):
    """The prompt, inputs and golden carry none of the reviewer-flagged LLM prose shapes."""
    sources = []
    p = folder / "prompt.md"
    if p.is_file():
        sources.append(("prompt.md", "", p.read_text(encoding="utf-8", errors="ignore")))
    ind = folder / "inputs"
    for d in sorted(ind.glob("*.docx")) if ind.is_dir() else []:
        sources.append((d.name, "", _docx_text(d)))
    for x in solution_files(folder, {".xlsx"}):
        for where, text in _xlsx_prose(x):
            sources.append((x.name, where, text))
    for name, where, text in sources:
        at = f"{name} {where}".strip()
        for rx in _TAUTOLOGY_RES:
            m = next((m for m in rx.finditer(text)
                      if not _TAUTOLOGY_OK_RE.search(m.group(0))), None)
            if m:
                emit("ERROR", f'[A10] {at}: tautology "{m.group(0).strip()[:60]}" — the highest-confidence '
                              "LLM prose tell (three flagged in task 12, 2026-08-22: \"committed work is "
                              "committed\", \"policy 6.3 is still policy\", \"paragraph 8 is the whole "
                              "story\"); state the rule and its consequence instead (docs/reference/llm-prose-tells.md)")
                break
        for rx, kind in _SLOGAN_RES:
            m = rx.search(text)
            if m:
                emit("ERROR", f'[A10] {at}: {kind} "{m.group(0).strip()[:60]}" — reviewers read these as '
                             "\"punchy phrases ... stylistic of an LLM trying too hard to sound real and "
                             "busy\" (task 12, 2026-08-22); state the mechanism or the quantity instead "
                             "(docs/reference/llm-prose-tells.md)")
    short = list(sources)
    for x in solution_files(folder, {".xlsx"}):
        for where, text in _xlsx_all_text(x):
            short.append((x.name, where, text))
    seen = set()
    for name, where, text in short:
        at = f"{name} {where}".strip()
        for rx, kind in _SHORT_IDIOM_RES:
            m = rx.search(text)
            if m and (at, kind) not in seen:
                seen.add((at, kind))
                emit("ERROR", f'[A10] {at}: {kind} "{m.group(0).strip()[:60]}" — the reviewer on '
                             "30ce3cda headed this \"Remove unclear LLM slang\" and asked which artifact "
                             "the phrase means (\"a posted warning, an exclusion list, a brand level "
                             "restriction?\"); name the artifact instead "
                             "(docs/reference/llm-prose-tells.md, class 11)")
        for rx, kind in _SELF_DESCRIBING_RES:
            m = rx.search(text)
            if m and (at, kind) not in seen:
                seen.add((at, kind))
                emit("ERROR", f'[A10] {at}: {kind} "{m.group(0).strip()[:60]}" — the platform\'s '
                             "LLM-authorship phrasing judge names pre-counted lists, \"the sections that "
                             "follow\" roadmaps and self-describing titles (\"Golden Solution: ...\") in "
                             "every FAIL report (pbw-rebate-reconciliation, 2026-08-31, llm-only 3/5); "
                             "delete the sentence or give the thing its real title "
                             "(docs/submission/platform/style-guide-llm-tells.md)")


@check(codes=['A6'], rules=['REV-PROSE'], needs=['inputs', 'solution'], params=['folder'])
def check_emdash_docx(folder):
    """No input or solution .docx carries em dashes."""
    docx = solution_files(folder, {".docx"}) + \
        (sorted((folder / "inputs").glob("*.docx")) if (folder / "inputs").is_dir() else [])
    for p in docx:
        stats = docx_emdash_stats(p)
        if not stats:
            continue
        em, words = stats
        per_k = 1000 * em / max(words, 1)
        if em >= 4 and per_k >= 12:
            sev = "ERROR"
        elif em >= 3 and per_k >= 8:
            sev = "ERROR"
        else:
            continue
        emit(sev, f"[A6] {p.relative_to(folder)}: {em} em dashes in {words} words "
                  f"({per_k:.0f}/1000) — repeated 'clause — clause' punctuation reads as "
                  "LLM-styled (reviewer fail, deadstock inputs 2026-08-19); rewrite with "
                  "conventional punctuation, keep facts unchanged")


@check(codes=['A6'], rules=['REV-PROSE'], needs=['prompt', 'rubric'], params=['folder'])
def check_emdash_text(folder):
    """The prompt and the rubric CSV carry no em dashes."""
    for p in (folder / "prompt.md", rubric_path(folder)):
        if p.is_file():
            em = p.read_text(encoding="utf-8", errors="ignore").count("—")
            if em:
                emit("ERROR", f"[A6] {p.name}: {em} em dash(es) — house rule since the 2026-08-19 "
                             "reviewer fail is zero em dashes in platform-entered text; swap for "
                             "conventional punctuation (portfolio scrubbed to zero that day)")


# ---- A20: sentence mechanics the reviewer corrects by hand ------------------------------
# lift-truck-fleet-plan, REJECTED at first human review 2026-09-05. The reviewer rewrote the
# prompt's opening sentence into three ("Sentence 1 ... Sentence 2 ... Sentence 3") and a
# golden paragraph into four, then stated the rule: "When two sentences are joined with 'and'
# or 'so' or 'but' or 'or' or another coordinating conjunction, they need a comma ... No more
# than 2 sentences can be joined with a comma and coordinating conjunction. Basic comma rules
# should be used throughout. Nobody is looking for perfection, but commas in lists and commas
# in compound sentences are basics." Applied to the prompt, the input documents AND the golden
# ("Fix the extensive run-on sentences throughout"). Two shapes are mechanical:
#   A20a  a bare coordinating conjunction followed by a new subject and its verb - the comma
#         before the conjunction is missing ("... past ten thousand hours and U-03 crosses it")
#   A20b  two or more independent-clause joins in one sentence - three or more clauses
#         ("..., so neither can be bought out under the rules, and U-02 fails the ...")
# The serial comma in lists is the third rule the reviewer named and is a read, not a check.
_A20_PRON = r"(?:I|we|they|he|she|it|you|there|nobody|neither|none|everyone|everybody|nothing)"
_A20_DET = r"(?:the|our|my|a|an|this|that|these|those|his|her|their|its|each|every|no|both|all|one)"
# auxiliaries, modals and verbs that are rarely nouns; noun-ambiguous forms (charge, order,
# record, list, plan, cost, run, sign, ...) are left out on purpose - precision over recall
_A20_VERB = (
    r"(?:is|are|was|were|has|have|had|will|can|cannot|could|would|should|may|might|must|does|do|did|"
    r"goes|comes|came|went|needs|gets|got|takes|took|becomes|became|stays|remains|seems|means|says|said|"
    r"tells|told|knows|knew|wants|expects|thinks|thought|agrees|agreed|belongs|owes|arrives|expires|lapses|"
    r"starts|begins|began|fell|rises|rose|crosses|passes|reaches|reached|fails|puts|ran|keeps|kept|makes|made|"
    r"wrote|bought|sold|owns|wore|broke|carries|pays|paid|sends|sent|sees|saw|left|"
    r"stood|asked|includes|excludes|allows|requires|applies|renews|"
    r"picked|crossed|failed|tripped|landed|moved|stayed|covered|"
    r"needed|wanted|asked|caught|lost|found|sat|held|ended|started|closed|opened)")
_A20_SUBJECT = (rf"(?:{_A20_PRON}|{_A20_DET} \w+(?:'s)?(?: \w+){{0,2}}|[A-Z][\w-]+(?: [A-Z][\w-]+)?)")
# a bare conjunction (no comma in front) that opens a new clause; "or" is left out because it
# joins alternatives far more often than clauses
_A20_BARE_RE = re.compile(rf"(?<![,;:])\s(and|but|so|yet)\s+(?!that\b|then\b|long as\b|far as\b|much as\b|on\b)"
                          rf"({_A20_SUBJECT})\s+(?:\w+\s+)?(?:{_A20_VERB})\b")
# a comma-and-conjunction join that opens a new clause (an Oxford-comma list item has no verb)
_A20_COMMA_RE = re.compile(rf",\s+(and|but|so|or|yet)\s+(?!that\b)({_A20_SUBJECT})\s+(?:\w+\s+)?(?:{_A20_VERB})\b")
# a semicolon that opens a new clause (a semicolon list item has no subject and verb)
_A20_SEMI_RE = re.compile(rf";\s+({_A20_SUBJECT})\s+(?:\w+\s+)?(?:{_A20_VERB})\b")
_A20_CAP = 6
# a compound subject ("Reggie and Curtis run", "you and Darrell can") or an all-caps list
# item ("FORKS or MAST_CHAINS takes") is not a clause join
_A20_COMPOUND_RE = re.compile(r"(?:^|\s)(?:[A-Z][\w-]*|you|I|we|me|us|him|her|them)$")


_A20_ANYVERB_RE = re.compile(rf"\b{_A20_VERB}\b")
_A20_SUBORD_RE = re.compile(r"\b(?:when|whenever|if|because|where|while|unless|until|after|before|although|though|since|"
                            r"whether|once|provided|which|who|whose|as long as|so that)\b", re.I)


def _a20_bare_hits(s):
    """Bare-conjunction clause joins, minus compound subjects: if the stretch back to the
    previous comma holds no verb yet ("Nine roof panels and a section of coping came off",
    "the covers and the tape are"), the conjunction is joining subjects, not clauses."""
    out = []
    for m in _A20_BARE_RE.finditer(s):
        before = s[:m.start()].rstrip()
        subj = m.group(2)
        if _A20_COMPOUND_RE.search(before) or subj.isupper():
            continue
        segment = re.split(r"[,;:]", before)[-1]
        if not _A20_ANYVERB_RE.search(segment):
            continue
        # "between the last passing test and this adjustment were" pairs objects, not clauses
        if re.search(r"\b(?:between|both|either|neither)\b", segment, re.I):
            continue
        # inside a subordinate clause ("when the vendors answer and the reconciliation has to
        # hold", "if the driver is willing to wait and a receiver is free") no comma is due
        if _A20_SUBORD_RE.search(segment):
            continue
        out.append(m)
    return out


def _a20_sentences(text):
    for line in text.split("\n"):
        line = line.strip()
        if not line or "|" in line or line.upper() == line:
            continue
        for s in split_sentences(line, capital=True):
            s = s.strip()
            if len(s.split()) >= 8:
                yield s


@check(codes=['A20'], rules=['REV-REGISTER'], needs=['prompt'], params=['folder'])
def check_run_on_sentences(folder):
    """A sentence puts a comma before a clause-joining conjunction and joins no more than two clauses."""
    sources = []
    p = folder / "prompt.md"
    if p.is_file():
        sources.append(("prompt.md", "", p.read_text(encoding="utf-8", errors="ignore")))
    rp = rubric_path(folder)
    if rp and rp.is_file():
        sources.append((rp.name, "", rp.read_text(encoding="utf-8-sig", errors="ignore")))
    ind = folder / "inputs"
    for d in sorted(ind.glob("*.docx")) if ind.is_dir() else []:
        sources.append((d.name, "", _docx_text(d)))
    for x in sorted(ind.glob("*.xlsx")) if ind.is_dir() else []:
        for where, text in _xlsx_prose(x):
            sources.append((x.name, where, text))
    for d in solution_files(folder, {".docx"}):
        sources.append((d.name, "", _docx_text(d)))
    for x in solution_files(folder, {".xlsx"}):
        for where, text in _xlsx_prose(x):
            sources.append((x.name, where, text))
    per_file = {}
    for name, where, text in sources:
        at = f"{name} {where}".strip()
        for s in _a20_sentences(text):
            bares = _a20_bare_hits(s)
            bare = bares[0] if bares else None
            joins = len(_A20_COMMA_RE.findall(s)) + len(_A20_SEMI_RE.findall(s)) + len(bares)
            if bare:
                per_file.setdefault(name, []).append(
                    f'[A20] {at}: no comma before "{bare.group(1)}" where a new clause starts '
                    f'("...{s[max(0, bare.start() - 30):bare.end() + 20].strip()}...")')
            elif joins >= 2:
                per_file.setdefault(name, []).append(
                    f'[A20] {at}: {joins + 1} independent clauses in one sentence ("{s[:100]}...")')
    for name, msgs in per_file.items():
        for msg in msgs[:_A20_CAP]:
            emit("ERROR", msg + " - the lift-truck-fleet-plan reviewer rewrote these by hand and rejected "
                          "the task (2026-09-05): comma before and/but/so/or between clauses, never more "
                          "than two clauses in a sentence, serial comma in lists; prompt, inputs, golden "
                          "and rubric alike (docs/submission/workflows/02-prompt-writing.md)")
        if len(msgs) > _A20_CAP:
            emit("ERROR", f"[A20] {name}: {len(msgs) - _A20_CAP} more sentences of the same shapes")


# A21 (2026-09-11, hathi-replenishment-order-decision refinement round 4, LLM-authorship check
# FAILED, llm-only 0.50 against 0.55): the platform's reader flagged an input memo, MEDIUM, for
# "every section follows an identical formal-operational sentence pattern ('[Activity]
# continued/remained/completed according to [established/standard] procedures; No [negative
# event] was reported') with no variation across 13 distinct topic sections, consistent with
# template-generated content". Thirty of its forty sentences matched that skeleton; the next
# highest input document in the portfolio matched fourteen percent. A10 reads rhythm and
# vocabulary tells sentence by sentence and never saw a document whose every sentence is the
# same status-report sentence.
_A21_TEMPLATE_RE = re.compile(
    r"\b(?:remain(?:s|ed)?|continues?|continued|(?:was|were|has been|have been) completed"
    r"|according to (?:established|standard|existing|approved)"
    r"|no [a-z -]+ (?:was|were|have been|has been|occurred|reported))\b", re.I)
_A21_MIN_SENTENCES = 20
_A21_SHARE = 0.5


@check(codes=['A21'], rules=['REV-PROSE'], needs=['inputs', 'solution'], params=['folder'])
def check_status_template_register(folder):
    """A document never carries the status-report sentence skeleton (remained / continue / completed according to procedure / no X was reported) on half or more of its sentences.

    Since: 2026-09-11 (hathi-replenishment-order-decision refinement round 4).
    Source: the platform's LLM-authorship check (Claude reader, MEDIUM on an input, the check FAILED at 0.50).
    Drift-notes: measured on sentences of six words or more, twenty or more of them; the flagged
    file scored 0.75, its sibling audit report 0.32, every other input docx 0.14 or under.
    """
    from ..common import _docx_text
    for sub in ("inputs", "solution"):
        d = folder / sub
        for path in sorted(d.glob("*.docx")) if d.is_dir() else []:
            try:
                text = _docx_text(path)
            except Exception:
                continue
            sents = [s.strip() for para in text.split("\n") for s in re.split(r"(?<=[.!?])\s+", para)
                     if len(s.split()) >= 6]
            if len(sents) < _A21_MIN_SENTENCES:
                continue
            hits = [s for s in sents if _A21_TEMPLATE_RE.search(s)]
            share = len(hits) / len(sents)
            if share >= _A21_SHARE:
                sample = "; ".join(h[:70] for h in hits[:3])
                emit("ERROR", f"{path.name}: {len(hits)} of {len(sents)} sentences ({share:.0%}) are the status-report "
                             f"skeleton (remained / continue / completed according to procedure / no X was reported): "
                             f"\"{sample}\". The platform's authorship reader calls this template-generated content "
                             "and failed the check at 0.50 (hathi-replenishment-order-decision 2026-09-11). Rewrite "
                             "in plain professional voice, varying the sentence shape section by section")


# A32 (2026-09-14, hathi-replenishment-order-decision refinement round 9): the LLM-authorship
# check FAILED at llm-only 0.25 on the golden alone, "partial generic section header sequence
# ('Executive Summary', 'Recommendations'): MEDIUM". The reader keeps a list of the headings a
# model reaches for and reads two of them in one document as its outline. Across the portfolio
# only this memo carried two; two goldens carry "Recommendation" alone.
_A32_GENERIC = {"executive summary", "recommendations", "recommendation", "introduction", "overview", "background",
                "conclusion", "conclusions", "next steps", "key findings", "findings", "methodology", "summary",
                "analysis", "purpose", "objectives", "scope"}


def _a32_headings(path):
    """Heading-styled paragraphs and short all-bold lines of a docx, as text."""
    from docx import Document
    out = []
    for p in Document(str(path)).paragraphs:
        t = p.text.strip()
        if not t:
            continue
        runs = [r for r in p.runs if r.text.strip()]
        if p.style.name.lower().startswith("heading") or (runs and all(r.bold for r in runs) and len(t.split()) <= 6):
            out.append(t)
    return out


@check(codes=['A32'], rules=['REV-PROSE'], needs=['solution'], params=['folder'])
def check_generic_heading_pair(folder):
    """A solution docx never carries two or more headings from the generic report outline (Executive Summary, Recommendations, Introduction, Overview, Background, Conclusion, Next Steps, Key Findings, Methodology); the authorship reader reads the pair as a model's outline and fails the golden on it.

    Since: 2026-09-14 (hathi-replenishment-order-decision refinement round 9).
    Source: the platform's LLM-authorship check, MEDIUM on the output file for exactly two such headings.
    Drift-notes: one generic heading is tolerated (two accepted goldens carry "Recommendation"); the
    prompt's own words stay in the body, so a section can be titled for its content ("Summary for
    the July Purchasing Cycle", "Order Decisions by SKU") and still answer the ask.
    """
    for path in solution_files(folder, {".docx"}):
        try:
            heads = _a32_headings(path)
        except Exception:
            continue
        generic = [h for h in heads if h.lower().rstrip(":") in _A32_GENERIC]
        if len(generic) >= 2:
            emit("ERROR", f"[A32] {path.name}: {len(generic)} headings from the generic report outline ({', '.join(generic)}) - "
                          "the platform's LLM-authorship check reads the pair as a model's outline and failed the "
                          "golden at MEDIUM (hathi-replenishment-order-decision 2026-09-14). Title each section for "
                          "what it holds; the prompt's words stay in the body")
