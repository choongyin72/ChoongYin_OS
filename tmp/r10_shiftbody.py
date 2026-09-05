"""Shift a band's body up or down so its rows land where the original's do.

    py tmp/r10_shiftbody.py R10.034 [variant] --dy=-41 --from=152 [--apply]

R10.034's whole body sits 41pt below the original's, measured block by block:

    Date of Issuance            138 -> 178    +40
    ACQ for the Contract Year   238 -> 278    +40
    ACQ after adjustment        318 -> 358    +40
    Total Delivered Quantity    622 -> 658    +36
    Last refresh (footer)       792 -> 794     +2      <- its own band, unaffected

One constant offset, not many defects - which is why every close-up crop looked correct while the
page read as wrong. It stayed invisible to me for a whole session because I cropped both
documents at the SAME coordinates: a uniform shift moves both windows together and cannot show up
that way. Only a whole-page comparison reveals it.

The logo and title are already right (54 against 58), so the shift starts below them: --from is
the lowest y that moves. Nothing is allowed to go negative or past the band's height.
"""
import os
import re
import sys

BASE = r"C:\Projects\INPEX\sources\CrystalReports"
rep = sys.argv[1]
APPLY = "--apply" in sys.argv
DY = next((int(x.split("=")[1]) for x in sys.argv[1:] if x.startswith("--dy=")), 0)
FROM = next((int(x.split("=")[1]) for x in sys.argv[1:] if x.startswith("--from=")), 0)
if DY == 0:
    raise SystemExit("--dy is required, e.g. --dy=-41")
S = os.path.join(BASE, rep, "output")
_pick = [x for x in sys.argv[2:] if not x.startswith("--")]
_jrs = [f for f in sorted(os.listdir(S)) if f.endswith(".jrxml") and "backup" not in f]
if _pick:
    _c = [f for f in _jrs if f[:-6].endswith(_pick[0])] or \
         [f for f in _jrs if _pick[0] in f[:-6]]
    FN = _c[0]
elif len(_jrs) > 1:
    raise SystemExit("%s holds %d jrxml - name the variant" % (rep, len(_jrs)))
else:
    FN = _jrs[0]
path = os.path.join(S, FN)
t = orig = open(path, encoding="utf-8").read()
ELEM = re.compile(r'<element\b[^>]*?/>|<element\b[^>]*?>.*?</element>', re.S)
print("%s  %s   dy=%+d from y>=%d" % (rep, FN, DY, FROM))

BANDS = [("detail", r'(<detail>\s*<band height="(\d+)"[^>]*>)(.*?)(</band>\s*</detail>)'),
         ("groupHeader",
          r'(<groupHeader>\s*<band height="(\d+)"[^>]*>)(.*?)(</band>\s*</groupHeader>)'),
         ("pageHeader", r'(<pageHeader height="(\d+)"[^>]*>)(.*?)(</pageHeader>)'),
         ("title", r'(<title height="(\d+)"[^>]*>)(.*?)(</title>)')]
moved = 0
for bn, pat in BANDS:
    m = re.search(pat, t, re.S)
    if not m or not m.group(3).strip():
        continue
    head, bh, body, tail = m.group(1), int(m.group(2)), m.group(3), m.group(4)
    newbody = body
    for s in ELEM.findall(body):
        ym = re.search(r'\by="(\d+)"', s)
        hm = re.search(r'\bheight="(\d+)"', s)
        if not ym:
            continue
        y = int(ym.group(1))
        if y < FROM:
            continue
        ny = y + DY
        h = int(hm.group(1)) if hm else 0
        if ny < 0:
            raise SystemExit("y=%d would become %d - negative" % (y, ny))
        if ny + h > bh:
            raise SystemExit("y=%d h=%d would overflow the %dpt band" % (ny, h, bh))
        ns = re.sub(r'\by="%d"' % y, 'y="%d"' % ny, s, count=1)
        if ns != s:
            newbody = newbody.replace(s, ns, 1)
            moved += 1
    t = t.replace(head + body + tail, head + newbody + tail, 1)
    print("   %s: %d element(s) at or below y=%d moved by %+d" % (bn, moved, FROM, DY))
    break

# ---- guards
if re.search(r'\b(x|y|width|height)="\d+\.\d+"', t):
    raise SystemExit("decimal coordinate introduced (Part Z9)")
if len(re.findall(r'<element\b', t)) != len(re.findall(r'<element\b', orig)):
    raise SystemExit("element count changed")
T0 = sorted(x for x in re.findall(r'<!\[CDATA\[(.*?)\]\]>', orig, re.S) if x.strip())
T1 = sorted(x for x in re.findall(r'<!\[CDATA\[(.*?)\]\]>', t, re.S) if x.strip())
if T0 != T1:
    raise SystemExit("text changed - this pass only moves elements vertically")
gx = re.findall(r'<element\b[^>]*?\bx="(\d+)"', orig)
if gx != re.findall(r'<element\b[^>]*?\bx="(\d+)"', t):
    raise SystemExit("an x changed - this pass moves vertically only")
print("   guard: element count, text and every x unchanged")

if not APPLY:
    print("   report only - rerun with --apply")
elif t != orig:
    b = path + ".backup_20260905_preshiftbody"
    if not os.path.exists(b):
        open(b, "w", encoding="utf-8").write(orig)
    open(path, "w", encoding="utf-8").write(t)
    print("   %d -> %d bytes" % (len(orig), len(t)))
