"""Measure the gap above "ACQ after adjustment (Base ACQ)" in both documents, by ink.

    py tmp/r10_034_gap.py

The check in r10_034_check.py returned None for the build, which is a fault in the helper and
not evidence about the build - so this measures the same thing the simplest possible way: list
every wide horizontal band edge in the region and print the run of white between the last two.
"""
import os
import sys

import pymupdf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r10_ref

BASE = r"C:\Projects\INPEX\sources\CrystalReports"
S = os.path.join(BASE, "R10.034", "output")
FN = [f for f in sorted(os.listdir(S)) if f.endswith(".jrxml") and "backup" not in f][0]

for tag, pth in (("original", r10_ref.pick_ref("R10.034", FN)),
                 ("build", os.path.join(S, FN[:-6] + ".pdf"))):
    pg = pymupdf.open(pth)[0]
    # the first table's own rows: wide cells in the label column
    rows = sorted({(round(g["rect"].y0, 1), round(g["rect"].y1, 1))
                   for g in pg.get_drawings()
                   if 300 < g["rect"].x1 - g["rect"].x0 < 360 and 3 < g["rect"].y1 - g["rect"].y0 < 30
                   and 200 < g["rect"].y0 < 340})
    print("\n%s - first table rows (label column):" % tag)
    prev = None
    for y0, y1 in rows:
        g = ("gap %+.1f" % (y0 - prev)) if prev is not None else ""
        print("   y %6.1f ..%6.1f    %s" % (y0, y1, g))
        prev = y1
