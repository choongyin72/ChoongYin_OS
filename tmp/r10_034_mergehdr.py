"""Merge the AACQ table's label-column header across both header rows.

    py tmp/r10_034_mergehdr.py [--apply]

Owner: "the first column do a row merge". Our build gives that column TWO stacked navy cells,
one per header row, so a divider is drawn across it:

    x=2 y=319 w=263 h=27   Band454087      <- header row 1 (AACQ | Qty Actually Delivered | ...)
    x=2 y=346 w=263 h=15   Band454087      <- header row 2 (MMBtu | MMBtu | MMBtu)

The original merges them - its label-column header cell spans y 346.4..386.2 (39.8pt) while the
three value columns split into 27.6pt + 14.2pt - so this is the original's own shape rather than
a cosmetic preference. 319 + 27 = 346 and 346 + 15 = 361, so the merged cell is y=319 h=42.

Same defect class as R10.030's "set row merge for Unloading Port and Scheduled Unloading Date
columns", which is why it is worth a named pass rather than a hand edit.
"""
import os
import re
import sys

BASE = r"C:\Projects\INPEX\sources\CrystalReports"
S = os.path.join(BASE, "R10.034", "output")
FN = [f for f in sorted(os.listdir(S)) if f.endswith(".jrxml") and "backup" not in f][0]
path = os.path.join(S, FN)
t = orig = open(path, encoding="utf-8").read()
APPLY = "--apply" in sys.argv
X, W, TOP, MID = 2, 263, 319, 346
print("%s   merging the label-column header at x=%d w=%d" % (FN, X, W))

ELEM = re.compile(r'<element\b[^>]*?/>|<element\b[^>]*?>.*?</element>', re.S)


def one(y):
    hits = [s for s in ELEM.findall(t)
            if re.search(r'kind="rectangle" x="%d" y="%d" width="%d"' % (X, y, W), s)]
    if len(hits) != 1:
        raise SystemExit("expected 1 cell at x=%d y=%d w=%d, found %d" % (X, y, W, len(hits)))
    return hits[0]


top, mid = one(TOP), one(MID)
h_top = int(re.search(r'height="(\d+)"', top).group(1))
h_mid = int(re.search(r'height="(\d+)"', mid).group(1))
if TOP + h_top != MID:
    raise SystemExit("the two cells do not meet: %d+%d != %d" % (TOP, h_top, MID))
merged = re.sub(r'height="%d"' % h_top, 'height="%d"' % (h_top + h_mid), top, count=1)
t = t.replace(mid, "", 1).replace(top, merged, 1)
print("   h=%d + h=%d -> one cell y=%d h=%d, the divider removed"
      % (h_top, h_mid, TOP, h_top + h_mid))

# ---- guards
if len(re.findall(r'<element\b', t)) != len(re.findall(r'<element\b', orig)) - 1:
    raise SystemExit("element count moved by more than the one cell removed")
T0 = sorted(x for x in re.findall(r'<!\[CDATA\[(.*?)\]\]>', orig, re.S) if x.strip())
if T0 != sorted(x for x in re.findall(r'<!\[CDATA\[(.*?)\]\]>', t, re.S) if x.strip()):
    raise SystemExit("text changed - this pass only merges two rectangles")
if re.search(r'kind="rectangle" x="%d" y="%d" width="%d"' % (X, MID, W), t):
    raise SystemExit("the sub-row cell is still there")
bh = int(re.search(r'<detail>\s*<band height="(\d+)"', t, re.S).group(1))
if TOP + h_top + h_mid > bh:
    raise SystemExit("the merged cell overflows the %dpt band" % bh)
print("   guard: one element removed, text unchanged, nothing overflows")

if not APPLY:
    print("   report only - rerun with --apply")
else:
    b = path + ".backup_20260905_premergehdr"
    if not os.path.exists(b):
        open(b, "w", encoding="utf-8").write(orig)
        print("   backup: %s" % os.path.basename(b))
    open(path, "w", encoding="utf-8").write(t)
    print("   %d -> %d bytes, applied" % (len(orig), len(t)))
