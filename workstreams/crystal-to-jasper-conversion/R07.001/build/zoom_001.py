"""Magnified reference-vs-generated crop of one region, stacked ref-above / gen-below.

    py zoom_001.py <page> <x0> <y0> <x1> <y1> [dpi]
"""
import sys

import fitz

B = r"C:\Projects\INPEX\sources\CrystalReports\R07.001"
gen = fitz.open(B + r"\output\R07_001_Offshore_Daily_Ops_Report.pdf")
ref = fitz.open(B + r"\crytsal report in pdf\R07.001 - Offshore Daily Operations Report.pdf")

p = int(sys.argv[1])
clip = fitz.Rect(*[float(v) for v in sys.argv[2:6]])
dpi = int(sys.argv[6]) if len(sys.argv) > 6 else 400

rp = ref[p - 1].get_pixmap(dpi=dpi, clip=clip)
gp = gen[p - 1].get_pixmap(dpi=dpi, clip=clip)
GAP = 10
w, h = max(rp.width, gp.width), rp.height + GAP + gp.height
out = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, w, h))
out.set_rect(out.irect, (210, 210, 210))
rp.set_origin(0, 0)
gp.set_origin(0, rp.height + GAP)
out.copy(rp, rp.irect)
out.copy(gp, gp.irect)
path = B + r"\_crops\ZOOM.png"
out.save(path)
print(f"{path}  (reference on top, generated below)  {w}x{h}")
