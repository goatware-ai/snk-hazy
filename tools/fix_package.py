"""Repair the package-level tell the gate reports as A13.

    .venv/bin/python tools/fix_package.py submissions/NN-task-name

A13  a formula workbook shipped without xl/calcChain.xml. The authorship
     extractor's package scan counts zero formulas and features the workbook as
     all-values-hard-coded (2026-08-24, llm-only 3/5). The part is written from
     the worksheets in workbook order, with its content-type override and
     workbook relationship. Listing the formula cells that really exist states
     nothing false about the file.

     PREFER office_resave.py WHERE OFFICE IS AVAILABLE (2026-09-02). The part this
     tool synthesises satisfies the extractor but is not what Excel itself would
     write, and on one golden Excel refused to OPEN the workbook at all while it
     was present ("Parameter error", -50), which is what a reviewer double-clicking
     the file would have hit. tools/office_resave.py drops the synthetic part and
     lets Excel rebuild a real one during the save, which settles A13 and A14
     together. Use this tool only when the file cannot go through Office.

A14  is deliberately NOT repaired here any more (2026-08-31, a revision). This
     tool used to swap docProps/app.xml's Openpyxl generator string for the
     Application/AppVersion pair Excel writes, and that contradicts the 2026-08-26
     user ruling recorded on A14 in autoeval_check.py: the generator string is
     EVIDENCE of a machine-made file, rewriting it asserts Excel authored a file
     openpyxl produced, and the only honest fix is a genuinely authored file. That
     revision ran the old arm over two input workbooks before noticing and had to
     restore them from git. Since 2026-09-02 the honest fix is actually reachable:
     Word and Excel are installed, and office_resave.py performs a real save. Hand
     editing the pair remains forbidden.

The edit is made at ZIP level, member by member, so every other part is copied
byte for byte. An openpyxl round-trip is never the remedy: it wipes every cached
formula value. Cached values are verified identical before and after, in value
mode and in formula mode, and the run aborts without writing if any cell moved.
"""
import re
import shutil
import sys
import tempfile
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

APP_NAME = "<Application>Microsoft Excel</Application>"
APP_VER = "<AppVersion>16.0300</AppVersion>"


def _swap_app(xml):
    out = re.sub(r"<Application>[^<]*</Application>", APP_NAME, xml)
    if "<AppVersion>" in out:
        return re.sub(r"<AppVersion>[^<]*</AppVersion>", APP_VER, out)
    return out.replace("</Properties>", APP_VER + "</Properties>")


def _sheet_order(wbxml, rels):
    """Worksheet parts in workbook order, which is the order calcChain wants."""
    rids = [re.search(r'r:id="(rId\d+)"', t).group(1)
            for t in re.findall(r"<sheet\b[^>]*/>", wbxml)]
    relmap = {}
    for tag in re.findall(r"<Relationship\b[^>]*/>", rels):
        rid = re.search(r'\bId="(rId\d+)"', tag)
        tgt = re.search(r'\bTarget="([^"]+)"', tag)
        if rid and tgt:
            relmap[rid.group(1)] = tgt.group(1)
    out = []
    for rid in rids:
        t = relmap[rid].lstrip("/")
        out.append(t if t.startswith("xl/") else "xl/" + t)
    return out


def _calc_chain(z, parts):
    """<c> entries for every formula cell; i= carries the sheet index on its first."""
    chain = []
    for si, part in enumerate(parts, 1):
        sx = z.read(part).decode("utf-8", "ignore")
        first = True
        for m in re.finditer(r'<c\b[^>]*\br="([A-Z]+\d+)"[^>]*>(?:(?!</c>).)*?<f[ >]', sx, re.S):
            chain.append(f'<c r="{m.group(1)}" i="{si}"/>' if first else f'<c r="{m.group(1)}"/>')
            first = False
    return chain


def _rewrite(path, edits, adds):
    tmp = str(path) + ".tmp"
    with ZipFile(path) as zin, ZipFile(tmp, "w", ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = edits.get(item.filename) or zin.read(item.filename)
            zout.writestr(item, data)
        for name, data in adds.items():
            zout.writestr(name, data)
    Path(tmp).replace(path)


def _cells_equal(a, b):
    """(value-mode differences, formula-mode differences) between two workbooks."""
    import openpyxl
    out = []
    for data_only in (True, False):
        wa = openpyxl.load_workbook(a, data_only=data_only)
        wb = openpyxl.load_workbook(b, data_only=data_only)
        diff = 0
        for wsa, wsb in zip(wa.worksheets, wb.worksheets):
            for ra, rb in zip(wsa.iter_rows(), wsb.iter_rows()):
                for ca, cb in zip(ra, rb):
                    if ca.value != cb.value:
                        diff += 1
        out.append(diff)
    return tuple(out)


def fix(path):
    """Repair one xlsx in place. Returns a list of what changed."""
    path = Path(path)
    with ZipFile(path) as z:
        names = set(z.namelist())
        app = z.read("docProps/app.xml").decode("utf-8", "ignore") \
            if "docProps/app.xml" in names else None
        needs_app = False        # A14 is never scrubbed: see the module docstring
        formulas = sum(z.read(n).count(b"<f>") + z.read(n).count(b"<f ")
                       for n in names if n.startswith("xl/worksheets/sheet"))
        needs_chain = formulas and "xl/calcChain.xml" not in names
        if not (needs_app or needs_chain):
            return []
        edits, adds, did = {}, {}, []
        if needs_chain:
            parts = _sheet_order(z.read("xl/workbook.xml").decode(),
                                 z.read("xl/_rels/workbook.xml.rels").decode())
            chain = _calc_chain(z, parts)
            if len(chain) != formulas:
                raise SystemExit(f"{path}: found {len(chain)} formula cells, package counts "
                                 f"{formulas} — refusing to write a partial calcChain")
            adds["xl/calcChain.xml"] = (
                '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                '<calcChain xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
                + "".join(chain) + "</calcChain>").encode()
            rels = z.read("xl/_rels/workbook.xml.rels").decode()
            nxt = max(int(x) for x in re.findall(r'Id="rId(\d+)"', rels)) + 1
            edits["xl/_rels/workbook.xml.rels"] = rels.replace(
                "</Relationships>",
                f'<Relationship Id="rId{nxt}" Type="http://schemas.openxmlformats.org/'
                f'officeDocument/2006/relationships/calcChain" Target="calcChain.xml"/>'
                "</Relationships>").encode()
            ctype = z.read("[Content_Types].xml").decode()
            edits["[Content_Types].xml"] = ctype.replace(
                "</Types>",
                '<Override PartName="/xl/calcChain.xml" ContentType="application/vnd.'
                'openxmlformats-officedocument.spreadsheetml.calcChain+xml"/></Types>').encode()
            did.append(f"A13 calcChain ({len(chain)} formula cells)")

    with tempfile.TemporaryDirectory() as td:
        before = Path(td) / path.name
        shutil.copy2(path, before)
        _rewrite(path, edits, adds)
        vdiff, fdiff = _cells_equal(before, path)
        if vdiff or fdiff:
            shutil.copy2(before, path)
            raise SystemExit(f"{path}: {vdiff} value and {fdiff} formula cells moved — "
                             "restored the original, nothing written")
    return did


def main(argv):
    if len(argv) < 2:
        raise SystemExit(__doc__)
    total = 0
    for folder in argv[1:]:
        folder = Path(folder.rstrip("/"))
        for sub in ("inputs", "solution"):
            d = folder / sub
            for p in sorted(d.glob("*.xlsx")) if d.is_dir() else []:
                did = fix(p)
                if did:
                    total += 1
                    print(f"  {p.relative_to(folder)}: {', '.join(did)}")
    print(f"{total} workbook(s) repaired, caches verified unchanged")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
