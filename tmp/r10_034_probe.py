"""Read the ORIGINAL R10.034's own cells in the two regions the owner has flagged.

    py tmp/r10_034_probe.py

Three questions, all of which must be answered from the original rather than guessed:

  1. The AACQ table's data rows - does the original draw cells under the [Quantity Actually
     Delivered] and [Balance] columns? Owner: "the data columns for [Quantity Actually
     Delivered] and [Balance] columns dont have completed borderlines". Our build has a cell
     only under AACQ (x=265 w=78), so the other two columns render open. Before adding them I
     need the original's own x-spans, because r10_missingcells.py and r10_spuriouscells.py
     already fought each other to a standstill on this report when a heuristic was allowed to
     add cells the original has no counterpart for.

  2. Rows 5 and 6 of the FIRST table - the owner wants "a small narrow space gap" between
     "+/- Round-Up/Down Quantity scheduled" and "ACQ after adjustment (Base ACQ)". Our two rows
     are at y=360 h=16 and y=374 h=14, so they OVERLAP by 2pt. What is the original's gap?

  3. The Remarks section - our build paints "Remarks:" on a navy Band454087 rectangle. What
     does the original draw there: a plain label, or a label plus an empty box?
"""
import os
import sys

import pymupdf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r10_ref

BASE = r"C:\Projects\INPEX\sources\CrystalReports"
S = os.path.join(BASE, "R10.034", "output")
FN = [f for f in sorted(os.listdir(S)) if f.endswith(".jrxml") and "backup" not in f][0]
ref = r10_ref.pick_ref("R10.034", FN)
print("original: %s" % os.path.basename(ref))
d = pymupdf.open(ref)
p = d[0]

# the page's own left margin, so original x can be compared with jrxml x directly
LM = 22.0
print("\n(x values below are ORIGINAL page x minus %.0fpt, to match jrxml x)" % LM)


def cells(y0, y1):
    out = []
    for g in p.get_drawings():
        r = g["rect"]
        if r.y1 < y0 or r.y0 > y1:
            continue
        w, h = r.x1 - r.x0, r.y1 - r.y0
        if w < 6 or h < 3 or h > 40:
            continue
        out.append((round(r.y0, 1), round(r.y1, 1), round(r.x0 - LM, 1), round(r.x1 - LM, 1)))
    return sorted(set(out))


def text_at(sub):
    for b in p.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                if sub.lower() in s["text"].lower():
                    return s["text"].strip(), s["bbox"]
    return None, None


# ---- 1 + 2: locate the two tables by their own labels
for label in ("ACQ for the Contract Year", "ACQ after adjustment", "Make-Up LNG",
              "Make-Good LNG", "UQT scheduled", "Surplus", "Total", "Remarks"):
    t, bb = text_at(label)
    print("   %-28s %s" % (label, ("y %.1f..%.1f  x %.1f" % (bb[1], bb[3], bb[0] - LM))
                           if bb else "NOT FOUND on page 1"))

t, bb = text_at("Make-Good LNG")
if bb:
    y0, y1 = bb[1] - 60, bb[3] + 60
    print("\nAACQ TABLE - original cells around the data rows (y %.0f..%.0f):" % (y0, y1))
    last = None
    for cy0, cy1, cx0, cx1 in cells(y0, y1):
        if last is not None and cy0 != last:
            print()
        print("   y %6.1f ..%6.1f   x %6.1f ..%6.1f   (w %.1f)" % (cy0, cy1, cx0, cx1, cx1 - cx0))
        last = cy0

# the FIRST table - the owner wants a gap between its last two rows
print("\nFIRST TABLE - original cells (y 230..335):")
last = None
for cy0, cy1, cx0, cx1 in cells(230, 335):
    if last is not None and cy0 != last:
        print()
    print("   y %6.1f ..%6.1f   x %6.1f ..%6.1f   (w %.1f h %.1f)"
          % (cy0, cy1, cx0, cx1, cx1 - cx0, cy1 - cy0))
    last = cy0

t, bb = text_at("Remarks")
if bb:
    print("\nREMARKS - original cells within 60pt below the label:")
    got = cells(bb[1] - 4, bb[3] + 60)
    if not got:
        print("   none - the original draws NO rectangle there (plain label, no box, no fill)")
    for cy0, cy1, cx0, cx1 in got:
        print("   y %6.1f ..%6.1f   x %6.1f ..%6.1f   (w %.1f h %.1f)"
              % (cy0, cy1, cx0, cx1, cx1 - cx0, cy1 - cy0))
    # and its own colour, which is what decides whether the navy fill belongs
    for g in p.get_drawings():
        r = g["rect"]
        if r.y0 <= bb[1] + 2 and r.y1 >= bb[3] - 2 and r.x0 - LM < 10:
            print("   fill=%s stroke=%s at x %.1f..%.1f"
                  % (g.get("fill"), g.get("color"), r.x0 - LM, r.x1 - LM))
