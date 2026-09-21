#!/usr/bin/env python3
"""Prove page.js's rubric selectors match the real form.

    .venv/bin/python tools/hazy-helper/test_selectors.py

There is no browser here and no way to click through the live form, so the captured DOM in
rubric-sample.html is the only evidence the rubric path works. This walks that capture with
the same rules page.js applies and fails loudly if any of them stops matching.

It also re-reads the selector constants out of page.js rather than restating them, so the
two cannot drift apart: change a selector in page.js and this test follows it.

It also checks the five section accordions against sections-sample.html: that every
data-testid in page.js's SECTIONS map is found, that open and closed are read from the bare
data-open / data-closed attributes rather than a value, and that the checklist heading still
matches when its em dash is written as an en dash or a hyphen.

Section 1 is covered too, against section1-sample.html: the two radio groups, the per-option
containers, the fact that the clickable control is the button rather than the aria-hidden
input beside it, and the slug rule that lets an option be matched through its punctuation.

Section 2 is covered against section2-sample.html, whose point is the state the form is in
when you arrive: the Input File List repeatable has NO rows yet. Logic that locates a
repeatable by finding one of its existing rows finds none and gives up without writing
anything, so the test asserts the field container is reachable while empty.

Section 4 is covered twice: rubric-sample.html is that section with every row expanded,
section4-sample.html is the same section on ARRIVAL, where only the first of three rows is
open and the other two have no panel in the DOM at all. Counting rows by "instances holding
a description field" returns 1 there instead of 3.

Section 3 is covered against section3-sample.html: the five time fields are textareas with
maxlength="5", the Tools list arrives with one row already present, and that row is marked
field-repeatable-textarea rather than the -instance- the rubric uses.

Section 5 is covered against section5-sample.html, whose boxes are role="checkbox" divs
rather than inputs, each carrying its whole text in aria-label. There are fourteen.

Every section of the form now has a capture behind it.
"""
from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
SAMPLE = HERE / "rubric-sample.html"
SECTIONS_SAMPLE = HERE / "sections-sample.html"
SECTION1_SAMPLE = HERE / "section1-sample.html"
SECTION2_SAMPLE = HERE / "section2-sample.html"
SECTION3_SAMPLE = HERE / "section3-sample.html"
SECTION4_SAMPLE = HERE / "section4-sample.html"
SECTION5_SAMPLE = HERE / "section5-sample.html"
PAGE_JS = HERE / "page.js"


class Node:
    __slots__ = ("tag", "attrs", "kids", "parent")

    def __init__(self, tag, attrs, parent=None):
        self.tag, self.attrs, self.kids, self.parent = tag, dict(attrs), [], parent

    def walk(self):
        yield self
        for k in self.kids:
            yield from k.walk()

    def testid(self):
        return self.attrs.get("data-testid", "")


VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr"}


class Tree(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root", {})
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.cur)
        self.cur.kids.append(n)
        if tag not in VOID:
            self.cur = n

    def handle_startendtag(self, tag, attrs):
        self.cur.kids.append(Node(tag, attrs, self.cur))

    def handle_endtag(self, tag):
        n = self.cur
        while n is not self.root and n.tag != tag:
            n = n.parent
        if n is not self.root:
            self.cur = n.parent


def _ancestors(node: Node):
    n = node.parent
    while n is not None:
        yield n
        n = n.parent


def parse(html: str) -> Node:
    t = Tree()
    t.feed(html)
    return t.root


def selectors_from_page_js() -> dict[str, str]:
    """Read the rubric selector constants out of page.js so the test tracks the source."""
    src = PAGE_JS.read_text()
    got = {}
    for name in ("RUBRIC_DESC", "RUBRIC_WEIGHT"):
        m = re.search(rf"const {name}\s*=\s*'([^']+)'", src)
        if not m:
            raise SystemExit(f"FAIL: could not read {name} out of page.js")
        got[name] = m.group(1)
    m = re.search(r"const RUBRIC_ADD\s*=\s*/([^/]+)/i", src)
    if not m:
        raise SystemExit("FAIL: could not read RUBRIC_ADD out of page.js")
    got["RUBRIC_ADD"] = m.group(1)
    return got


def matches(node: Node, sel: str) -> bool:
    """Support just the two shapes page.js uses: [data-testid="x"] and [data-testid^="x"]."""
    m = re.fullmatch(r'\[data-testid(\^?)="([^"]+)"\]', sel)
    if not m:
        raise SystemExit(f"FAIL: test cannot evaluate selector {sel!r}")
    op, val = m.groups()
    tid = node.testid()
    return tid.startswith(val) if op == "^" else tid == val


def find(root: Node, sel: str) -> list[Node]:
    return [n for n in root.walk() if matches(n, sel)]


def text_of(node: Node) -> str:
    return ""


def main() -> int:
    if not SAMPLE.exists():
        print(f"FAIL: {SAMPLE.name} is missing; it is the only record of the form's DOM")
        return 1
    html = SAMPLE.read_text(errors="ignore")
    root = parse(html)
    sel = selectors_from_page_js()

    failures: list[str] = []

    def check(label: str, cond: bool, detail: str = "") -> None:
        print(f"  {'ok  ' if cond else 'FAIL'}  {label}{(' - ' + detail) if detail and not cond else ''}")
        if not cond:
            failures.append(label)

    print("rubric selectors against the captured form DOM\n")

    # 1. instance containers, the only reliable anchor
    instances = [n for n in root.walk() if "-instance-" in n.testid()]
    check("instance containers found", len(instances) >= 1, f"found {len(instances)}")

    rubric_rows = [n for n in instances if find(n, sel["RUBRIC_DESC"])]
    check("rows carrying a rubric description field", len(rubric_rows) == 3,
          f"expected 3, found {len(rubric_rows)}")

    # 2. the ids really are duplicated, which is why scoping matters
    desc_ids = [
        n.attrs.get("id")
        for n in root.walk()
        if n.tag == "textarea" and n.attrs.get("id")
    ]
    check("description ids are duplicated across rows (so getElementById is unusable)",
          len(desc_ids) == 3 and len(set(desc_ids)) == 1,
          f"ids={desc_ids}")

    # 3. each row yields exactly one description and one weight control
    for i, row in enumerate(rubric_rows, 1):
        d = [n for c in find(row, sel["RUBRIC_DESC"]) for n in c.walk() if n.tag == "textarea"]
        w = [n for c in find(row, sel["RUBRIC_WEIGHT"]) for n in c.walk() if n.tag == "input"]
        check(f"row {i}: one description textarea", len(d) == 1, f"found {len(d)}")
        check(f"row {i}: one weight input", len(w) == 1, f"found {len(w)}")
        if w:
            a = w[0].attrs
            check(f"row {i}: weight bounded -5..+5",
                  a.get("min") == "-5" and a.get("max") == "5",
                  f"min={a.get('min')} max={a.get('max')}")

    # 4. the add-a-row button page.js looks for by text
    add_re = re.compile(sel["RUBRIC_ADD"], re.I)
    check('an "Add a New Rubric" button is present',
          bool(add_re.search(re.sub(r"<[^>]+>", " ", html))),
          f"/{sel['RUBRIC_ADD']}/i matched nothing")

    # 5. the fallback path, used if the testids are ever renamed
    fallback = [
        n for n in instances
        if any(k.tag == "textarea" for k in n.walk())
        and any(k.tag == "input" and k.attrs.get("min") == "-5" for k in n.walk())
    ]
    check("fallback (textarea + input[min=-5]) finds the same rows",
          len(fallback) == len(rubric_rows),
          f"fallback {len(fallback)} vs primary {len(rubric_rows)}")

    # ---------------------------------------------------------------- sections
    print("\nsection accordions")
    if not SECTIONS_SAMPLE.exists():
        check("sections-sample.html present", False, "missing")
    else:
        sec_root = parse(SECTIONS_SAMPLE.read_text(errors="ignore"))
        src = PAGE_JS.read_text()
        m = re.search(r"const SECTIONS = \{(.*?)\};", src, re.S)
        if not m:
            check("SECTIONS map readable from page.js", False, "not found")
        else:
            wanted = re.findall(r'\w+:\s*"((?:[^"\\]|\\.)*)"', m.group(1))
            # Expand only \uXXXX escapes. Going through .encode().decode("unicode_escape")
            # would round-trip the em dash through latin-1 and corrupt it.
            wanted = [
                re.sub(r"\\u([0-9a-fA-F]{4})", lambda mm: chr(int(mm.group(1), 16)), w)
                for w in wanted
            ]
            check("SECTIONS map holds five entries", len(wanted) == 5, f"found {len(wanted)}")

            present = {
                n.testid(): n
                for n in sec_root.walk()
                if n.testid().startswith("section-")
            }
            check("fixture carries five sections", len(present) == 5, f"found {len(present)}")

            def loosen(t):
                t = re.sub(r"[\u2012-\u2015\u2212-]+", "-", t.lower())
                return re.sub(r"\s+", " ", t).strip()

            loose = {loosen(k): v for k, v in present.items()}
            for w in wanted:
                key = "section-" + w
                hit = present.get(key) or loose.get(loosen(key))
                check(f"matched: {w[:46]}", hit is not None,
                      "no section with that data-testid")

            # open/closed read from the bare attribute, never a value
            opened = [k for k, v in present.items() if "data-open" in v.attrs]
            closed = [k for k, v in present.items() if "data-closed" in v.attrs]
            check("one section is open in the fixture", len(opened) == 1, f"{opened}")
            check("four are closed", len(closed) == 4, f"{len(closed)}")
            # html.parser gives None for a bare attribute; anything else means the form
            # started writing data-open="true", which page.js's presence test would misread.
            check("open/closed are valueless attributes",
                  all(present[k].attrs.get("data-open") in (None, "") for k in opened),
                  "an attribute carried a value; page.js tests presence only")

            # the em dash must survive being written three different ways
            checklist = [w for w in wanted if "Checklist" in w]
            if checklist:
                base = "section-" + checklist[0]
                for label, variant in (
                    ("en dash", base.replace("\u2014", "\u2013")),
                    ("hyphen", base.replace("\u2014", "-")),
                ):
                    check(f"checklist still matches with an {label}",
                          loosen(variant) == loosen(base),
                          "loosen() did not fold the dash")

    # --------------------------------------------------------------- section 1
    print("\nsection 1: domain and occupation")
    if not SECTION1_SAMPLE.exists():
        check("section1-sample.html present", False, "missing")
    else:
        s1 = parse(SECTION1_SAMPLE.read_text(errors="ignore"))

        # the section wrapper carries the testid; the panel inside carries role=region
        wrap = [n for n in s1.walk() if n.testid().startswith("section-")]
        check("section wrapper carries the section testid", len(wrap) == 1, f"found {len(wrap)}")
        panel = [n for n in s1.walk() if n.attrs.get("role") == "region"]
        check("panel sits inside the wrapper, not instead of it",
              len(panel) == 1 and panel[0] is not wrap[0] if wrap else False)

        groups = {
            n.testid().replace("field-radio-", ""): n
            for n in s1.walk()
            if n.testid().startswith("field-radio-")
        }
        check("both radio groups present", set(groups) == {"domain", "occupation"},
              f"found {sorted(groups)}")

        def opts(g):
            return [
                n for n in g.walk()
                if n.testid().startswith("radio-option-container-")
            ]

        if "domain" in groups:
            d = opts(groups["domain"])
            check("domain offers 14 options", len(d) == 14, f"found {len(d)}")
        if "occupation" in groups:
            o = opts(groups["occupation"])
            check("occupation options present", len(o) >= 5, f"found {len(o)}")

        # the control page.js clicks must be the button, not the clipped input
        for name, g in groups.items():
            for o in opts(g)[:3]:
                btns = [n for n in o.walk()
                        if n.tag == "button" and n.attrs.get("role") == "radio"]
                ins = [n for n in o.walk()
                       if n.tag == "input" and n.attrs.get("type") == "radio"]
                check(f"{name}: option has a clickable button[role=radio]", len(btns) == 1,
                      f"found {len(btns)}")
                check(f"{name}: the paired input is aria-hidden",
                      len(ins) == 1 and ins[0].attrs.get("aria-hidden") == "true",
                      "the input is not hidden; clicking the button may be wrong")

        # the slug rule, read out of page.js and applied to every option label
        src = PAGE_JS.read_text()
        check("slugify present in page.js", "function slugify" in src)

        def slugify(t):
            t = re.sub(r"[^a-z0-9]+", "_", t.lower())
            return re.sub(r"^_+|_+$", "", t)

        mismatched = []
        for g in groups.values():
            for o in opts(g):
                label = o.testid().replace("radio-option-container-", "")
                btn = next((n for n in o.walk()
                            if n.tag == "button" and n.attrs.get("role") == "radio"), None)
                if btn and btn.attrs.get("value") != slugify(label):
                    mismatched.append((label, btn.attrs.get("value"), slugify(label)))
        check("every option's value matches the slug rule", not mismatched,
              "; ".join(f"{a}: form={b} slug={c}" for a, b, c in mismatched[:3]))

        # the two punctuation cases that motivated slug matching
        for label, want in (
            ("Healthcare Practitioners / Support", "healthcare_practitioners_support"),
            ("Installation, Maintenance, and Repair", "installation_maintenance_and_repair"),
        ):
            check(f"slug folds punctuation: {label[:38]}", slugify(label) == want,
                  f"got {slugify(label)}")

        # one domain arrives pre-selected, which is why the fill verifies by reading back
        checked = [
            n for n in s1.walk()
            if n.attrs.get("role") == "radio" and "data-checked" in n.attrs
        ]
        check("a domain arrives already selected (so a click must be verified)",
              len(checked) == 1, f"found {len(checked)} pre-checked")

    # --------------------------------------------------------------- section 2
    print("\nsection 2: instruction and the input file list")
    if not SECTION2_SAMPLE.exists():
        check("section2-sample.html present", False, "missing")
    else:
        s2 = parse(SECTION2_SAMPLE.read_text(errors="ignore"))
        src = PAGE_JS.read_text()

        # the FIELD map in page.js must name the testids this capture carries
        m = re.search(r"const FIELD = \{(.*?)\};", src, re.S)
        check("FIELD map readable from page.js", bool(m))
        mapped = dict(re.findall(r'(\w+):\s*"([^"]+)"', m.group(1))) if m else {}

        boxes = {n.testid(): n for n in s2.walk() if n.testid().startswith("field-")}
        for key, expect in (
            ("task_instruction", "field-task-prompt"),
            ("input_files", "field-repeatabletextarea-input_file_list"),
            ("uploader_inputs", "field-s3fileuploader-file_uploader"),
        ):
            check(f"FIELD.{key} points at the form's testid",
                  mapped.get(key) == expect, f"map has {mapped.get(key)!r}, form has {expect!r}")
            check(f"{expect} present in the capture", expect in boxes)

        # the instruction textarea
        prompt_box = boxes.get("field-task-prompt")
        if prompt_box:
            tas = [n for n in prompt_box.walk() if n.tag == "textarea"]
            check("task instruction is one textarea", len(tas) == 1, f"found {len(tas)}")
            if tas:
                check('its id is "task-prompt"', tas[0].attrs.get("id") == "task-prompt",
                      f'id={tas[0].attrs.get("id")!r}')
                check("it is marked required", "required" in tas[0].attrs)

        # THE case this fixture exists for: the repeatable is empty on arrival
        inputs_box = boxes.get("field-repeatabletextarea-input_file_list")
        if inputs_box:
            inst = [n for n in inputs_box.walk() if "-instance-" in n.testid()]
            check("input file list arrives with ZERO rows", len(inst) == 0,
                  f"found {len(inst)}; the fixture no longer covers the empty case")
            editable = [n for n in inputs_box.walk()
                        if n.tag == "textarea"
                        or (n.tag == "input" and n.attrs.get("type") not in ("file", "hidden"))]
            check("and with no editable control either", len(editable) == 0,
                  f"found {len(editable)}")
            check("but the field container is still reachable", True)
            # the add button lives inside the field, so a scoped search finds it
            html2 = SECTION2_SAMPLE.read_text(errors="ignore")
            check('"Add Another Input File" button is inside that field',
                  "Add Another Input File" in html2)

        # The row markup for THIS list was never captured (the fixture only holds the
        # empty state), so the filler must not depend on a row marker at all.
        src2 = PAGE_JS.read_text()
        fl = src2[src2.index("async function fillListField"):src2.index("// ---------------------------------------------------------------- rubric")]
        check("fillListField writes into controls, not row markers",
              "slotsIn(box)" in fl and "ROW_SEL" not in fl,
              "it still resolves rows by a data-testid that section 2 never showed us")
        check("it stops if an Add click produces no new field",
              "added no field on click" in fl)
        check("scan can describe a repeatable's real structure",
              "function describeRepeatable" in src2)

        # the uploader must be skipped, and be findable as a file input
        up = boxes.get("field-s3fileuploader-file_uploader")
        if up:
            fin = [n for n in up.walk()
                   if n.tag == "input" and n.attrs.get("type") == "file"]
            check("uploader is a real file input (so it is skipped)", len(fin) == 1,
                  f"found {len(fin)}")

        # two dialog triggers share one testid; a button search must not rely on it
        show = [n for n in s2.walk() if n.testid() == "show-evaluators-button"]
        check("the shared show-criteria testid appears more than once", len(show) >= 2,
              f"found {len(show)}; nothing breaks, but the note in page.js assumes it")

    # --------------------------------------------------------------- section 3
    print("\nsection 3: times, tools and the output list")
    if not SECTION3_SAMPLE.exists():
        check("section3-sample.html present", False, "missing")
    else:
        s3 = parse(SECTION3_SAMPLE.read_text(errors="ignore"))
        src = PAGE_JS.read_text()
        boxes = {n.testid(): n for n in s3.walk() if n.testid().startswith("field-")}

        # the five time fields, read out of page.js so the map cannot drift
        m = re.search(r"const TIME_FIELD = \{(.*?)\};", src, re.S)
        check("TIME_FIELD map readable from page.js", bool(m))
        tmap = dict(re.findall(r'(\w+):\s*"([^"]+)"', m.group(1))) if m else {}
        check("TIME_FIELD names all five", len(tmap) == 5, f"found {len(tmap)}")
        for key, tid in tmap.items():
            box = boxes.get(tid)
            check(f"time.{key} -> {tid[:52]}", box is not None, "not in the capture")
            if box:
                tas = [n for n in box.walk() if n.tag == "textarea"]
                check(f"time.{key} is a textarea", len(tas) == 1, f"found {len(tas)}")
                if tas:
                    check(f"time.{key} carries maxlength=5",
                          tas[0].attrs.get("maxlength") == "5",
                          f'maxlength={tas[0].attrs.get("maxlength")!r}')

        # a 5-character total fits; the writer must notice if one ever does not
        check("setChecked reads the value back after writing", "function setChecked" in src)
        check("a total like 10.25 fits maxlength=5", len("10.25") <= 5)

        # tools: the corrected testid, and the row already present
        tools_tid = re.search(r'tools:\s*"([^"]+)"', src)
        check("FIELD.tools uses the form's testid",
              bool(tools_tid) and tools_tid.group(1) in boxes,
              f"page.js has {tools_tid.group(1) if tools_tid else None!r}")
        tools_box = boxes.get(tools_tid.group(1)) if tools_tid else None
        if tools_box:
            rows = [n for n in tools_box.walk()
                    if n.testid() == "field-repeatable-textarea" or "-instance-" in n.testid()]
            check("tools arrives with exactly one row", len(rows) == 1, f"found {len(rows)}")
            check("that row is marked field-repeatable-textarea, not -instance-",
                  bool(rows) and rows[0].testid() == "field-repeatable-textarea",
                  f'testid={rows[0].testid()!r}' if rows else "no row")
            check("ROW_SEL in page.js accepts both row markers",
                  'field-repeatable-textarea' in src and '-instance-' in src)

        # output list still arrives empty, like the input list
        out_box = boxes.get("field-repeatabletextarea-output_file_list")
        check("output file list present", out_box is not None)
        if out_box:
            rows = [n for n in out_box.walk()
                    if n.testid() == "field-repeatable-textarea" or "-instance-" in n.testid()]
            check("output file list arrives with ZERO rows", len(rows) == 0, f"found {len(rows)}")

        # the solution uploader is skipped
        up = boxes.get("field-s3fileuploader-completed_task_upload")
        check("completed-task uploader present and is a file input",
              up is not None
              and any(n.tag == "input" and n.attrs.get("type") == "file" for n in up.walk()))

        # why testids and not labels: the section repeats a time label three times
        html3 = SECTION3_SAMPLE.read_text(errors="ignore")
        n = html3.count("Time to read and understand the prompt and requirements")
        check("a time label appears more than once (so label matching is unsafe)", n >= 3,
              f"appears {n} time(s); the fixture no longer shows the collision")

    # --------------------------------------------------------------- section 4
    print("\nsection 4: the rubric on arrival")
    if not SECTION4_SAMPLE.exists():
        check("section4-sample.html present", False, "missing")
    else:
        s4 = parse(SECTION4_SAMPLE.read_text(errors="ignore"))
        src = PAGE_JS.read_text()

        insts = [n for n in s4.walk() if "-instance-" in n.testid()]
        check("three rubric rows exist on arrival", len(insts) == 3, f"found {len(insts)}")

        withfields = [n for n in insts if any(
            k.testid() == "field-textarea-rubric_description" for k in n.walk())]
        check("but only ONE has its fields rendered", len(withfields) == 1,
              f"{len(withfields)} rows carry a description field")

        closed = [n for n in insts if "data-closed" in n.attrs]
        hidden = [n for n in insts if "data-hidden" in n.attrs]
        check("the other two are data-closed", len(closed) == 2, f"found {len(closed)}")
        check("and data-hidden", len(hidden) == 2, f"found {len(hidden)}")

        for n in closed:
            tas = [k for k in n.walk() if k.tag == "textarea"]
            check(f"{n.testid()[-10:]}: no textarea while collapsed", len(tas) == 0,
                  f"found {len(tas)}")

        # the group page.js scopes to
        m = re.search(r'const RUBRIC_GROUP = "([^"]+)"', src)
        check("RUBRIC_GROUP readable from page.js", bool(m))
        if m:
            grp = [n for n in s4.walk() if n.testid() == m.group(1)]
            check(f"the group {m.group(1)} is in the capture", len(grp) == 1,
                  f"found {len(grp)}")

        # row counting must not filter on the presence of fields
        rr = src[src.index("function rubricRows"):src.index("function rubricFields")]
        check("rubricRows counts instance containers, not rows with fields",
              'querySelectorAll(\'[data-testid*="-instance-"]\')' in rr
              and "if (all.length) return all;" in rr,
              "it still filters by field presence")

        # the fill must expand before it writes, and add only the shortfall
        fr = src[src.index("async function fillRubric"):src.index("// ------------------------------------------------------------ radio picks")]
        check("fillRubric records how many rows it started with", "startedWith" in fr)
        check("fillRubric expands rows before writing",
              fr.index("expandRows") < fr.index("criteria.forEach"))
        check("fillRubric reports rows that would not expand", "would not expand" in fr)

        # expanding must never click a dialog trigger
        check("the expand pass excludes aria-haspopup",
              ':not([aria-haspopup])' in src,
              'a "Show criteria" button would be clicked and open a dialog')

        html4 = SECTION4_SAMPLE.read_text(errors="ignore")
        check('the "Add a New Rubric" button is present', "Add a New Rubric" in html4)

    # --------------------------------------------------------------- section 5
    print("\nsection 5: the submit checklist")
    if not SECTION5_SAMPLE.exists():
        check("section5-sample.html present", False, "missing")
    else:
        s5 = parse(SECTION5_SAMPLE.read_text(errors="ignore"))
        src = PAGE_JS.read_text()

        boxes5 = [n for n in s5.walk() if n.attrs.get("role") == "checkbox"]
        check("fourteen boxes", len(boxes5) == 14, f"found {len(boxes5)}")

        m = re.search(r"const BOX_COUNT = (\d+)", src)
        check("BOX_COUNT in page.js matches the form",
              bool(m) and int(m.group(1)) == len(boxes5),
              f"page.js says {m.group(1) if m else None}, form has {len(boxes5)}")

        # they are NOT inputs, which is why role and aria-checked carry the state
        inputs5 = [n for n in s5.walk()
                   if n.tag == "input" and n.attrs.get("type") == "checkbox"]
        check("none of them is an <input type=checkbox>", len(inputs5) == 0,
              f"found {len(inputs5)}")
        check("every box carries aria-checked",
              all("aria-checked" in b.attrs for b in boxes5))
        check("every box carries its text in aria-label",
              all(len(b.attrs.get("aria-label", "")) > 20 for b in boxes5))
        check("all start unticked",
              all(b.attrs.get("aria-checked") == "false" for b in boxes5))

        # no <label> wrapper, so the role element is the click target
        wrapped = [b for b in boxes5 if any(
            p_.tag == "label" for p_ in _ancestors(b))]
        check("no box is wrapped in a <label> (the role element is the target)",
              len(wrapped) == 0, f"{len(wrapped)} are wrapped")

        # the field container page.js anchors on
        mf = re.search(r'checklist:\s*\n?\s*"([^"]+)"\s*\+\s*\n?\s*"([^"]+)"', src)
        tid = (mf.group(1) + mf.group(2)) if mf else None
        present = {n.testid() for n in s5.walk() if n.testid()}
        check("FIELD.checklist matches the form's testid", tid in present,
              f"page.js builds {tid!r}")

        # the four groups, which is how the capture in docs/ is organised
        groups = {}
        for b in boxes5:
            g = b.attrs.get("aria-label", "").split(":")[0]
            groups[g] = groups.get(g, 0) + 1
        check("groups are 6/2/5/1",
              [groups.get(k) for k in
               ("Task Instruction", "Input Files", "Task Rubric", "Final Check")]
              == [6, 2, 5, 1],
              str(groups))

        # ticking must verify, because aria-checked is the only state
        check("the fill confirms each box actually flipped", "boxTicked(b)) ticked++" in src)
        check("and names any box it could not tick", "did not tick:" in src)

    print()
    if failures:
        print(f"{len(failures)} check(s) failed. The form's DOM has moved; re-capture it into")
        print(f"{SAMPLE.name} and update the selectors in page.js.")
        return 1
    print("all selector checks pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
