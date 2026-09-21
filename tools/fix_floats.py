"""Rewrite float-repr artifacts in cached xlsx values to shortest clean decimals.

Edits xl/worksheets/*.xml inside the xlsx zip directly (regex on <v> payloads),
so formulas and everything else are byte-identical. A replacement is accepted
only if the new literal parses back within 1e-9 relative drift of the original.
"""
import re, sys, zipfile, shutil, os

V_RE = re.compile(r'(<v>)(-?\d+\.\d+(?:[eE]-?\d+)?)(</v>)')
# artifact tell: long mantissa with a 9999/0000 run, or scientific notation, or >10 sig decimals
def is_artifact(lit):
    if 'e' in lit or 'E' in lit:
        return True
    frac = lit.split('.', 1)[1]
    if len(frac) > 10:
        return True
    return bool(re.search(r'(9{5,}|0{5,})\d*$', frac))

def shortest(v):
    for k in range(0, 13):
        cand = round(v, k)
        if abs(cand - v) <= 1e-9 * max(1.0, abs(v)):
            s = f'{cand:.{k}f}'.rstrip('0').rstrip('.')
            return s if s not in ('', '-0') else '0'
    return repr(v)

def fix_xml(data, stats):
    def repl(m):
        lit = m.group(2)
        if not is_artifact(lit):
            return m.group(0)
        v = float(lit)
        new = shortest(v)
        if abs(float(new) - v) > 1e-9 * max(1.0, abs(v)):
            return m.group(0)
        stats.append((lit, new))
        return m.group(1) + new + m.group(3)
    return V_RE.sub(repl, data)

def fix_xlsx(path):
    tmp = path + '.tmp'
    stats = []
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename.startswith('xl/worksheets/') and item.filename.endswith('.xml'):
                data = fix_xml(data.decode('utf-8'), stats).encode('utf-8')
            zout.writestr(item, data)
    os.replace(tmp, path)
    print(f'{path}: {len(stats)} cached values rewritten')
    for old, new in stats[:12]:
        print(f'   {old} -> {new}')
    if len(stats) > 12:
        print(f'   ... and {len(stats)-12} more')
    return len(stats)

def scan(path):
    hits = []
    with zipfile.ZipFile(path) as z:
        for n in z.namelist():
            if n.startswith('xl/worksheets/') and n.endswith('.xml'):
                for m in V_RE.finditer(z.read(n).decode('utf-8')):
                    if is_artifact(m.group(2)):
                        hits.append((n, m.group(2)))
    return hits

if __name__ == '__main__':
    mode = sys.argv[1]
    for p in sys.argv[2:]:
        if mode == 'scan':
            hits = scan(p)
            print(f'{p}: {len(hits)} artifacts')
            for n, lit in hits[:8]:
                print(f'   {n}: {lit}')
        else:
            fix_xlsx(p)
