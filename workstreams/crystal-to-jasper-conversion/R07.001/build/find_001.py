"""Print the absolute y of a text on a reference page, to aim zoom_001.py accurately."""
import sys

import fitz

B = r"C:\Projects\INPEX\sources\CrystalReports\R07.001"
ref = fitz.open(B + r"\crytsal report in pdf\R07.001 - Offshore Daily Operations Report.pdf")
needle = sys.argv[1]
for p in range(len(ref)):
    for r in ref[p].search_for(needle):
        print(f"page {p+1}: x {r.x0:7.2f}..{r.x1:7.2f}  y {r.y0:7.2f}..{r.y1:7.2f}")
