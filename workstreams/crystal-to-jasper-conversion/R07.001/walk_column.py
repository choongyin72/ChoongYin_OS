"""Walk down a column boundary at 600 dpi and report every break - the R07.004 diagnostic.

This is the method that solved the identical "not jointed / not connected" defect on R07.004
(see that report's FACT-FINDING-SUMMARY.md 2.3): data cells shorter than their row pitch leave
a band at each row boundary with no vertical drawn, so the horizontal line is there, the
vertical stops short of it, and the corner stays open. Comparing the break LIST against
Crystal's shows immediately whether the verticals reach their horizontals.

    py walk_column.py <page> <x> <y0> <y1>
    e.g. py walk_column.py 1 196 168 310

Counts PURPLE as ink deliberately - a purple band is drawn, not a gap. An earlier attempt that
treated only grey as ink reported false breaks wherever a band crossed the column.
"""
import os
import sys

import fitz

B = r"C:\Projects\INPEX\sources\CrystalReports\R07.001"
REF = B + r"\crytsal report in pdf\R07.001 - Offshore Daily Operations Report.pdf"
GEN = B + "\\output\\" + os.environ.get("GENPDF", "R07_001_Offshore_Daily_Ops_Report.pdf")

P = int(sys.argv[1])
X = float(sys.argv[2])
Y0, Y1 = float(sys.argv[3]), float(sys.argv[4])
DPI = 600
MIN_BREAK = 0.25        # below this is antialiasing, not an open corner


def breaks(path, x):
    pg = fitz.open(path)[P - 1]
    pm = pg.get_pixmap(dpi=DPI, clip=fitz.Rect(x - 0.7, Y0, x + 0.7, Y1))
    w, h, n, s = pm.width, pm.height, pm.n, pm.samples
    out, run = [], 0
    for row in range(h):
        ink = False
        for col in range(w):
            q = (row * w + col) * n
            r, g, b = s[q], s[q + 1], s[q + 2]
            if not (r > 246 and g > 246 and b > 246):
                ink = True
                break
        if ink:
            if run:
                sz = run * (Y1 - Y0) / h
                if sz >= MIN_BREAK:
                    out.append((round(Y0 + (row - run) * (Y1 - Y0) / h, 2), round(sz, 2)))
            run = 0
        else:
            run += 1
    if run:
        sz = run * (Y1 - Y0) / h
        if sz >= MIN_BREAK:
            out.append((round(Y1 - sz, 2), round(sz, 2)))
    return out


rb = breaks(REF, X)
gb = breaks(GEN, X)
print(f"page {P}, column x={X}, y {Y0}..{Y1}\n")
print(f"Crystal  : {len(rb)} break(s)  {[b[1] for b in rb]}")
for y, sz in rb:
    print(f"             at y={y:7.2f}  {sz:.2f}pt")
print(f"\nGenerated: {len(gb)} break(s)  {[b[1] for b in gb]}")
for y, sz in gb:
    print(f"             at y={y:7.2f}  {sz:.2f}pt")

extra = [g for g in gb if not any(abs(g[0] - r[0]) < 2.0 for r in rb)]
print(f"\nBREAKS PRESENT IN MINE BUT NOT CRYSTAL'S: {len(extra)}")
for y, sz in extra:
    print(f"             at y={y:7.2f}  {sz:.2f}pt  <- open corner")
