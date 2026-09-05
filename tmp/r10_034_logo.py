"""What is in the top 130pt of R10.034 - original vs build - so the "logo rule" claim is checked
rather than repeated.

    py tmp/r10_034_logo.py
"""
import os
import sys

import pymupdf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r10_ref

BASE = r"C:\Projects\INPEX\sources\CrystalReports"
S = os.path.join(BASE, "R10.034", "output")
FN = [f for f in sorted(os.listdir(S)) if f.endswith(".jrxml") and "backup" not in f][0]

for tag, pth in (("ORIGINAL", r10_ref.pick_ref("R10.034", FN)),
                 ("BUILD", os.path.join(S, FN[:-6] + ".pdf"))):
    pg = pymupdf.open(pth)[0]
    print("\n%s - horizontal rules in the top 140pt (wide and thin):" % tag)
    found = False
    for g in sorted(pg.get_drawings(), key=lambda z: z["rect"].y0):
        r = g["rect"]
        if r.y0 > 140 or r.x1 - r.x0 < 120 or r.y1 - r.y0 > 6:
            continue
        print("   y %6.2f ..%6.2f   x %6.2f ..%6.2f   h %.2f  fill=%s stroke=%s"
              % (r.y0, r.y1, r.x0, r.x1, r.y1 - r.y0, g.get("fill"), g.get("color")))
        found = True
    if not found:
        print("   none")
    print("   images:", [(round(b[1], 1), round(b[3], 1), round(b[0], 1), round(b[2], 1))
                         for b in (pg.get_image_bbox(i) for i in pg.get_images(full=True))]
          if pg.get_images(full=True) else "none")
    print("   text in the top 140pt:")
    for b in pg.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                if s["bbox"][1] < 140:
                    print("      y %6.2f  x %6.2f   %r" % (s["bbox"][1], s["bbox"][0],
                                                           s["text"][:52]))
