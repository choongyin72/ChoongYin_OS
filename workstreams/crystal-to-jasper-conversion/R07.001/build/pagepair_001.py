"""Side-by-side full-page renders, reference LEFT and generated RIGHT, one PNG per page.

The documented rule for this project is to LOOK first and measure second - a numeric diff
scored zero on a visibly-wrong section on R07.003. Whole-page pairs are the cheapest way to
catch anything gross before spending time in the 75 section crops.
"""
import fitz

B = r"C:\Projects\INPEX\sources\CrystalReports\R07.001"
gen = fitz.open(B + r"\output\R07_001_Offshore_Daily_Ops_Report.pdf")
ref = fitz.open(B + r"\crytsal report in pdf\R07.001 - Offshore Daily Operations Report.pdf")
DPI = 105
GAP = 14

for p in range(len(ref)):
    rp = ref[p].get_pixmap(dpi=DPI)
    gp = gen[p].get_pixmap(dpi=DPI)
    w, h = rp.width + GAP + gp.width, max(rp.height, gp.height)
    out = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, w, h))
    out.set_rect(out.irect, (255, 255, 255))
    rp.set_origin(0, 0)
    gp.set_origin(rp.width + GAP, 0)
    out.copy(rp, rp.irect)
    out.copy(gp, gp.irect)
    path = B + rf"\_crops\PAIR_page{p+1}.png"
    out.save(path)
    print(f"page {p+1}: {path}   ref {rp.width}x{rp.height}  gen {gp.width}x{gp.height}")
