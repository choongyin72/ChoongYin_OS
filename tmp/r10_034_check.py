"""Check the five R10.034 fixes in the RENDERED build against the original's own ink.

    py tmp/r10_034_check.py

Each check is pass/fail, not a number, because a number lets me argue "close enough" against
the owner's >98% standard. Every target is the original's measured geometry.
"""
import os
import sys

import pymupdf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r10_ref

BASE = r"C:\Projects\INPEX\sources\CrystalReports"
S = os.path.join(BASE, "R10.034", "output")
FN = [f for f in sorted(os.listdir(S)) if f.endswith(".jrxml") and "backup" not in f][0]
bld = pymupdf.open(os.path.join(S, FN[:-6] + ".pdf"))[0]
ref = pymupdf.open(r10_ref.pick_ref("R10.034", FN))[0]
LM = 22.0
fails = []


def cells(pg, y0, y1, lm):
    out = set()
    for g in pg.get_drawings():
        r = g["rect"]
        if r.y1 < y0 or r.y0 > y1:
            continue
        if r.x1 - r.x0 < 6 or not 3 < r.y1 - r.y0 < 40:
            continue
        out.add((round(r.y0), round(r.x0 - lm), round(r.x1 - lm)))
    return out


def says(ok, label, detail=""):
    print("   %-4s %-52s %s" % ("PASS" if ok else "FAIL", label, detail))
    if not ok:
        fails.append(label)


def find(pg, sub, lm, ymin=0):
    """First span containing sub, at or below ymin.

    ymin matters: "ACQ after adjustment" appears in BOTH tables - centred in the first and
    left-aligned as row 1 of the AACQ table - and taking the first match sent every AACQ row
    check to the wrong table, where it correctly reported no cell at x 265..342.
    """
    best = None
    for b in pg.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                if sub.lower() in s["text"].lower() and s["bbox"][1] >= ymin:
                    if best is None or s["bbox"][1] < best[0]:
                        best = (s["bbox"][1], s["bbox"][0] - lm, s["text"].strip())
    return best if best else (None, None, None)


print("R10.034  build vs original")

# ---- 1. no cell reaching past the info block's value column on its first row
y, _x, _s = find(bld, "Date of Issuance", LM)
wide = [c for c in cells(bld, y - 4, y + 10, LM) if c[1] < 200 and c[2] > 520]
says(not wide, "1 no extra cell right of Date of Issuance", "%d found" % len(wide))

# ---- 2. a gap above "ACQ after adjustment (Base ACQ)" in the first table
def gap_above(pg):
    """White between the first table's last two rows, taken from the label column's own cells.

    The earlier version of this went looking for "band edges wider than 100pt below the label"
    and returned None for the build - a fault in the helper, not evidence about the build, which
    measured 4.0pt against the original's 4.3pt. A check that fails for its own reasons is worse
    than no check, because it invites exactly the "close enough" argument it exists to prevent.
    """
    rows, prev = sorted({(round(g["rect"].y0, 1), round(g["rect"].y1, 1))
                         for g in pg.get_drawings()
                         if 300 < g["rect"].x1 - g["rect"].x0 < 360
                         and 3 < g["rect"].y1 - g["rect"].y0 < 30
                         and 200 < g["rect"].y0 < 340}), None
    gaps = []
    for y0, y1 in rows:
        if prev is not None and y0 - prev > 0.2:
            gaps.append(y0 - prev)
        prev = y1
    return max(gaps) if gaps else None


gr, gb = gap_above(ref), gap_above(bld)
says(gb is not None and gr is not None and abs(gb - gr) <= 1.5,
     "2 gap above ACQ after adjustment",
     "original %.1fpt, build %.1fpt" % (gr or -1, gb or -1))

# ---- 3 + 4. every data row of the AACQ table has all five cells, on the grid
y3 = find(bld, "Make-Good LNG", LM)[0]
TOP = y3 - 40                                  # above the AACQ table's own first data row
XS = [(1, 17), (13, 265), (265, 342), (343, 419), (420, 496)]
bad = []
for i, lbl in enumerate(("ACQ after adjustment (Base ACQ)", "Make-Up LNG", "Make-Good LNG",
                         "Force Majeure Restoration", "UQT scheduled", "Surplus")):
    yy = find(bld, lbl, LM, ymin=TOP)[0]
    if yy is None:
        bad.append("%s: label not on page 1" % lbl)
        continue
    row = cells(bld, yy - 2, yy + 6, LM)
    for x0, x1 in XS[2:]:                      # the three value columns
        if not any(abs(c[1] - x0) <= 3 and abs(c[2] - x1) <= 3 for c in row):
            bad.append("%s: no cell at x %d..%d" % (lbl[:22], x0, x1))
says(not bad, "3+4 all three value columns bordered on all 6 rows",
     bad[0] if bad else "18/18 cells present")

# rows 2, 4, 5 no longer carry a full-width cell, and their labels are on the grid
full = [c for c in cells(bld, y3 - 40, y3 + 60, LM) if c[1] < 4 and c[2] > 500]
says(not full, "3 no full-width white cell on rows 2/4/5", "%d found" % len(full))
off = [l for l in ("Make-Up LNG", "Force Majeure Restoration", "UQT scheduled")
       if (find(bld, l, LM, ymin=TOP)[1] or 0) > 24]
says(not off, "3 rows 2/4/5 labels indented like their siblings",
     ", ".join(off) if off else "all at x<=24")

# and their labels are no longer cut short
for l, want in (("Make-Up LNG", "Contract Year"), ("Force Majeure", "Contract Year"),
                ("UQT scheduled", "Contract Year")):
    txt = find(bld, l, LM, ymin=TOP)[2] or ""
    says(txt.endswith(want), "3 label complete: %s" % l, repr(txt[-28:]))

# ---- 5. Remarks: plain label, empty box below, no fill behind the label
yl = find(bld, "Remarks", LM)[0]
behind = [g for g in bld.get_drawings()
          if g["rect"].y0 <= yl + 2 and g["rect"].y1 >= yl + 6
          and g["rect"].x0 - LM < 6 and g.get("fill")]
says(not behind, "5 no fill behind the Remarks: label", "%d found" % len(behind))
box = [c for c in cells(bld, yl + 8, yl + 45, LM) if c[1] <= 3 and c[2] >= 490]
says(bool(box), "5 empty box below Remarks:", str(sorted(box)[:1]))

print("\n%s  (%d check(s) failed)" % ("OVERALL: PASS" if not fails else "OVERALL: FAIL",
                                      len(fails)))
