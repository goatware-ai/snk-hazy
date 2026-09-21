#!/usr/bin/env python3
"""Prove page.js's rubric selectors match the real form.

    .venv/bin/python tools/hazy-helper/test_selectors.py

There is no browser here and no way to click through the live form, so the captured DOM in
rubric-sample.html is the only evidence the rubric path works. This walks that capture with
the same rules page.js applies and fails loudly if any of them stops matching.

It also re-reads the selector constants out of page.js rather than restating them, so the
two cannot drift apart: change a selector in page.js and this test follows it.

What it does NOT cover: sections 1, 2, 3 and 5. No DOM for those was available, so page.js
matches them on label text and the popup's Scan button is how you check them against the
live page. Capture one of those views into this folder and extend this file when you can.
"""
from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
SAMPLE = HERE / "rubric-sample.html"
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

    print()
    if failures:
        print(f"{len(failures)} check(s) failed. The form's DOM has moved; re-capture it into")
        print(f"{SAMPLE.name} and update the selectors in page.js.")
        return 1
    print("all selector checks pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
