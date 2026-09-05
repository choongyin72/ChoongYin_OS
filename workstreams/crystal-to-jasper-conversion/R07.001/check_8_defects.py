"""Acceptance test for the 8 owner-reported defects on R07.001 (round 01, 2026-09-02).

Measures exactly what the owner reported, gen vs reference, so each fix can be attributed
rather than assumed. Written BEFORE the fixes so it can be shown to fail first.

Probe coordinates are the ones established during the GO verification pass and recorded in
DEFECT-ROUND-01.md - not re-derived here, so a change in the numbers means a change in the
report, not in the measurement.

    py check_8_defects.py            full report
    py check_8_defects.py --brief    one line per group
"""
import os
import sys

import fitz

B = r"C:\Projects\INPEX\sources\CrystalReports\R07.001"
REF = B + r"\crytsal report in pdf\R07.001 - Offshore Daily Operations Report.pdf"
# GENPDF override, same convention as the _checks suite: the real PDF is often open in a
# viewer and locked, and reading a stale file has produced wrong conclusions on this project
# more than once.
GEN = B + "\\output\\" + os.environ.get("GENPDF", "R07_001_Offshore_Daily_Ops_Report.pdf")

ref = fitz.open(REF)
gen = fitz.open(GEN)


def purple(d):
    f = d.get("fill")
    return bool(f) and f[2] > 0.4 and f[0] < 0.45 and f[1] < 0.45


def rects_in(doc, p, y_lo, y_hi, x_lo=0, x_hi=900, min_w=8, min_h=4, borders_only=False):
    """borders_only excludes purple FILLS.

    Group B must use it. Without it the test counted a band's fill as a border rect, and on
    pages 6-7 the fill's right edge coincidentally matched the data vertical - so a genuine
    1pt misalignment of the border scored 0.00 and item 8 looked fixed when it was not.
    """
    out = []
    for d in doc[p - 1].get_drawings():
        r = d["rect"]
        if borders_only and purple(d):
            continue
        if (r.x1 - r.x0) >= min_w and (r.y1 - r.y0) >= min_h \
                and y_lo <= r.y0 <= y_hi and r.x0 >= x_lo - 2 and r.x1 <= x_hi + 2:
            out.append((round(r.x0, 2), round(r.y0, 2), round(r.x1, 2), round(r.y1, 2),
                        purple(d)))
    return sorted(out, key=lambda t: (t[1], t[0]))


def vlines_in(doc, p, y_lo, y_hi, x_lo=0, x_hi=900):
    """Thin vertical marks - the data-row column lines."""
    out = []
    for d in doc[p - 1].get_drawings():
        r = d["rect"]
        if (r.x1 - r.x0) < 3 and (r.y1 - r.y0) >= 4 \
                and y_lo <= r.y0 <= y_hi and x_lo <= r.x0 <= x_hi:
            out.append((round(r.x0, 2), round(r.y0, 2), round(r.y1, 2)))
    return sorted(out)


def hlines_in(doc, p, y_lo, y_hi, min_w=200):
    out = []
    for d in doc[p - 1].get_drawings():
        r = d["rect"]
        if (r.y1 - r.y0) < 3 and (r.x1 - r.x0) >= min_w and y_lo <= r.y0 <= y_hi:
            out.append((round((r.y0 + r.y1) / 2, 2), round(r.x0, 2), round(r.x1, 2)))
    return sorted(out)


# ---- Group A: header row bottom -> data row vertical top -----------------------------
# (items 3,4,5,6) reference gap is 0.50-0.65pt; a larger or zero gap is the defect
# The two p1 "2nd CPF/FPSO" tables were removed from this group on 2026-09-02: Crystal gives
# their Total rows no verticals at all, so a header-bottom-to-vertical-top gap does not exist
# there and the measurement was meaningless. Item 3's real quantity is column-x alignment,
# measured in GROUP A2 below - per the owner's clarification, "head column row and data column
# row is no connected" means the vertical column separators do not line up, not a horizontal gap.
A_CASES = [
    ("item 4  p2 SupportVes", 2, 714, 732, 20, 330),
    ("item 5  p3 ProdRisk   ", 3, 156, 178, 20, 210),
    ("item 6  p5 ProdRisk   ", 5, 156, 178, 20, 210),
]

# GROUP A2 (item 3): header-band column boundary x vs data-row column-line x.
# (label, page, header-band y window, data-row y window)
A2_CASES = [
    ("item 3  p1 1st CPF   ", 1, 168, 186, 187, 238),
    ("item 3  p1 1st FPSO  ", 1, 241, 255, 256, 310),
]

# ---- Group B: header right edge vs data-row right vertical --------------------------
B_CASES = [
    ("item 2  p1 1st FPSO  ", 1, 238, 300, 770, 830),
    ("item 8  p6 Comments  ", 6, 155, 200, 780, 830),
    ("item 8  p7 Comments  ", 7, 125, 200, 780, 830),
]

# ---- Group C: first-column text inset from the table's left border -------------------
C_CASES = [
    ("p2 MajEquip CPF ", 2, "Major Equipment Status for CPF", "Utilities"),
    ("p3 ProdRisk CPF ", 3, "Production Risks for CPF", "Utilities"),
    ("p4 MajEquip FPSO", 4, "Major Equipment Status for FPSO", "Flash gas"),
    ("p5 ProdRisk FPSO", 5, "Production Risks for FPSO", "MEG system"),
    ("p5 Consum CPF   ", 5, "Consumables for CPF", "Diesel"),
    ("p5 Consum FPSO  ", 5, "Consumables for FPSO", "Diesel"),
]

fails = 0
brief = "--brief" in sys.argv


def report(label, r_val, g_val, tol, unit="pt", target=None):
    global fails
    t = r_val if target is None else target
    ok = abs(g_val - t) <= tol
    if not ok:
        fails += 1
    print(f"  {label}  ref={r_val:7.2f}  gen={g_val:7.2f}  "
          f"delta={g_val - t:+6.2f}{unit}  {'OK' if ok else 'FAIL'}")


print("=" * 78)
print("GROUP A - header row joined to its data row (items 3,4,5,6)")
print("=" * 78)
for label, p, ylo, yhi, xlo, xhi in A_CASES:
    vals = {}
    for tag, doc in (("ref", ref), ("gen", gen)):
        rs = rects_in(doc, p, ylo, yhi, xlo, xhi)
        vs = vlines_in(doc, p, ylo, yhi + 6, xlo, xhi)
        if not rs or not vs:
            vals[tag] = None
            continue
        header_bottom = max(r[3] for r in rs)
        data_top = min(v[1] for v in vs if v[1] >= header_bottom - 1.5) \
            if any(v[1] >= header_bottom - 1.5 for v in vs) else None
        vals[tag] = None if data_top is None else round(data_top - header_bottom, 2)
    if vals["ref"] is None or vals["gen"] is None:
        print(f"  {label}  MEASUREMENT FAILED ref={vals['ref']} gen={vals['gen']}")
        continue
    # TARGET IS 0.00, NOT CRYSTAL'S VALUE. Crystal leaves a 0.50-0.65pt hairline here, but the
    # owner's requirement was explicit on R07.005: "all data column row should be connected...
    # no short horizontal line between those data column row". JasperReports 7.0.3 rejects
    # decimal coordinates (Part Z9), so 0.50 is not reachable on an integer grid anyway - the
    # options are 0.00 (joined) or 1.00 (a visible break). Crystal's value is printed for
    # comparison; the pass criterion is "joined".
    report(label, vals["ref"], vals["gen"], 0.35, target=0.0)

print()
print("=" * 78)
print("GROUP A2 - column verticals line up header-to-data (item 3, owner-clarified)")
print("=" * 78)
for label, p, hy0, hy1, dy0, dy1 in A2_CASES:
    vals = {}
    for tag, doc in (("ref", ref), ("gen", gen)):
        pg = doc[p - 1]
        hx = sorted({round(d["rect"].x0, 2) for d in pg.get_drawings()
                     if hy0 <= d["rect"].y0 <= hy1 and (d["rect"].x1 - d["rect"].x0) >= 8}
                    | {round(d["rect"].x1, 2) for d in pg.get_drawings()
                       if hy0 <= d["rect"].y0 <= hy1 and (d["rect"].x1 - d["rect"].x0) >= 8})
        dx = sorted({round(d["rect"].x0, 2) for d in pg.get_drawings()
                     if dy0 <= d["rect"].y0 <= dy1 and (d["rect"].x1 - d["rect"].x0) < 3
                     and (d["rect"].y1 - d["rect"].y0) >= 4})
        # only columns that HAVE a header boundary within 2pt - otherwise the nearest-match
        # is a different column entirely and the number is nonsense (it read +230pt once)
        offs = [abs(x - min(hx, key=lambda h: abs(h - x))) for x in dx
                if hx and abs(x - min(hx, key=lambda h: abs(h - x))) <= 2.0]
        vals[tag] = round(max(offs), 2) if offs else None
    if vals["ref"] is None or vals["gen"] is None:
        print(f"  {label}  no comparable columns (ref={vals['ref']} gen={vals['gen']})")
        continue
    report(label, vals["ref"], vals["gen"], 0.3, target=0.0)

print()
print("=" * 78)
print("GROUP B - header right borderline aligned with data rows (items 2,8)")
print("=" * 78)
for label, p, ylo, yhi, xlo, xhi in B_CASES:
    vals = {}
    for tag, doc in (("ref", ref), ("gen", gen)):
        rs = rects_in(doc, p, ylo, yhi, 0, 900, borders_only=True)
        rs = [r for r in rs if xlo <= r[2] <= xhi]
        vs = vlines_in(doc, p, ylo, yhi + 40, xlo, xhi)
        if not rs or not vs:
            vals[tag] = None
            continue
        vals[tag] = round(abs(max(r[2] for r in rs) - vs[0][0]), 2)
    if vals["ref"] is None or vals["gen"] is None:
        print(f"  {label}  MEASUREMENT FAILED ref={vals['ref']} gen={vals['gen']}")
        continue
    # Same reasoning as Group A: the requirement is "aligned" (0.00 offset). Crystal's own
    # header/data right edges are 0.05-0.40pt apart - the owner reported that misalignment as
    # a defect even though Crystal shares it (the R07.004 rule: a defect counts even when the
    # original has it).
    report(label, vals["ref"], vals["gen"], 0.35, target=0.0)

print()
print("=" * 78)
print("GROUP C - first-column text inset from the left border (item 7)")
print("=" * 78)
for label, p, title, first in C_CASES:
    vals = {}
    for tag, doc in (("ref", ref), ("gen", gen)):
        page = doc[p - 1]
        t = page.search_for(title)
        if not t:
            vals[tag] = None
            continue
        cands = [r for r in page.search_for(first) if r.y0 > t[0].y1]
        if not cands:
            vals[tag] = None
            continue
        cell = min(cands, key=lambda r: r.y0)
        mid = (cell.y0 + cell.y1) / 2
        vs = vlines_in(doc, p, cell.y0 - 14, cell.y1 + 2, 10, cell.x0 + 2)
        vs += [(round(d["rect"].x0, 2), 0, 0) for d in page.get_drawings()
               if abs(d["rect"].y0 - cell.y0) < 14 and 10 < d["rect"].x0 < cell.x0 + 2
               and (d["rect"].x1 - d["rect"].x0) >= 8]
        if not vs:
            vals[tag] = None
            continue
        vals[tag] = round(cell.x0 - min(v[0] for v in vs), 2)
    if vals["ref"] is None or vals["gen"] is None:
        print(f"  {label}  MEASUREMENT FAILED ref={vals['ref']} gen={vals['gen']}")
        continue
    report(label, vals["ref"], vals["gen"], 0.6)

print()
print("=" * 78)
print("GROUP D - separator rule between page-1 CPF and FPSO tables (item 1)")
print("=" * 78)
for tag, doc in (("ref", ref), ("gen", gen)):
    vs = vlines_in(doc, 1, 215, 240, 20, 260)
    hs = hlines_in(doc, 1, 236, 242)
    rs = [r for r in rects_in(doc, 1, 239, 246, 20, 300) if r[4]]
    if not (vs and hs and rs):
        print(f"  {tag}: MEASUREMENT FAILED v={len(vs)} h={len(hs)} fill={len(rs)}")
        continue
    tbl_bottom = max(v[2] for v in vs)
    rule = hs[0][0]
    fpso_top = min(r[1] for r in rs)
    print(f"  {tag}: table_bottom={tbl_bottom:.2f}  rule={rule:.2f}  "
          f"fpso_header_top={fpso_top:.2f}   "
          f"rule-to-table={rule - tbl_bottom:+.2f}  rule-to-header={fpso_top - rule:+.2f}")

print()
print("=" * 78)
print(f"GROUPS A-C failing measurements: {fails}")
print("=" * 78)


# =============================================================================
# PERMANENT GUARDRAILS (added 2026-09-02)
#
# Both of these defects were fixed, then silently re-introduced by later edits of mine and
# found by the owner rather than by a check. Nothing in the acceptance test stopped either.
#   1. DOUBLE GREY LINE at a band->row boundary - the header's closing line and the body's
#      opening line sitting ~1pt apart instead of being one shared line. Came back when I
#      disabled the second-line drop on a mistaken "missing line" diagnosis.
#   2. TEXT INK ON A LINE - a row label's first inked pixel less than 2.5pt below the line
#      above it. Was mis-measured for several rounds because the check used PyMuPDF's span
#      bbox (an ASCENDER box) instead of the visible ink.
# =============================================================================
print()
print("=" * 78)
print("GUARDRAIL 1 - exactly ONE grey line at each band->row boundary")
print("=" * 78)


def band_boundaries(doc, p):
    pg = doc[p - 1]
    return sorted(round(d["rect"].y1, 2) for d in pg.get_drawings()
                  if purple(d) and (d["rect"].x1 - d["rect"].x0) > 100)


g1 = 0
for p in range(1, len(gen) + 1):
    for b in band_boundaries(gen, p):
        pm = gen[p - 1].get_pixmap(dpi=600, clip=fitz.Rect(99.3, b, 100.7, b + 5.0))
        w, h, n, s = pm.width, pm.height, pm.n, pm.samples
        runs, prev = [], None
        for row in range(h):
            # PURPLE IS NOT A LINE. Counting any non-white pixel flagged pages 6 and 7, which
            # stack two purple bands (section band + column-header band) - the check was
            # reading the second band's fill as a second grey line. A grey line is grey.
            grey = False
            for c in range(w):
                q = (row * w + c) * n
                r, g, b = s[q], s[q + 1], s[q + 2]
                if b > 100 and r < 130:          # purple fill
                    continue
                if not (r > 246 and g > 246 and b > 246):
                    grey = True
                    break
            if grey != prev:
                runs.append([grey, 1])
                prev = grey
            else:
                runs[-1][1] += 1
        # count grey runs thicker than a hairline (antialiased fill edges are ~1 px)
        thick = [r for r in runs if r[0] and r[1] * 5.0 / h > 0.4]
        if len(thick) > 1:
            g1 += 1
            print(f"  page {p} band bottom y={b:.2f}: {len(thick)} grey lines  FAIL")
print(f"  band boundaries with a doubled line: {g1}  "
      f"{'OK' if g1 == 0 else 'FAIL'}")

print()
print("=" * 78)
print("GUARDRAIL 2 - every row label's INK at least 2.5pt below the line above")
print("=" * 78)
MIN_INK_CLEAR = 2.5
lines1 = sorted({round(d["rect"].y0, 2) for d in gen[0].get_drawings()
                 if (d["rect"].y1 - d["rect"].y0) < 3 and (d["rect"].x1 - d["rect"].x0) > 300}
                | {round(d["rect"].y1, 2) for d in gen[0].get_drawings()
                   if (d["rect"].x1 - d["rect"].x0) > 300 and (d["rect"].y1 - d["rect"].y0) >= 4})
LABELS = ("Injury events", "Environmental events", "Safety events", "Security events",
          "Main facility", "Total")
g2 = 0
for bl in gen[0].get_text("dict")["blocks"]:
    for l in bl.get("lines", []):
        for s in l["spans"]:
            if s["text"].strip() not in LABELS or s["bbox"][1] > 430:
                continue
            x0, y0, x1, y1 = s["bbox"]
            pm = gen[0].get_pixmap(dpi=600,
                                   clip=fitz.Rect(x0, y0 - 3, min(x1, x0 + 60), y1 + 1))
            w, h, n, sm = pm.width, pm.height, pm.n, pm.samples
            ink = None
            for row in range(h):
                if any(sm[(row * w + c) * n] < 128 and sm[(row * w + c) * n + 1] < 128
                       for c in range(w)):
                    ink = (y0 - 3) + row * ((y1 + 1) - (y0 - 3)) / h
                    break
            if ink is None:
                continue
            above = [ln for ln in lines1 if ln <= ink]
            if above and (ink - max(above)) < MIN_INK_CLEAR:
                g2 += 1
                print(f"  {s['text'].strip()[:24]:24} ink={ink:.2f} "
                      f"line={max(above):.2f} clr={ink - max(above):.2f}  FAIL")
print(f"  labels with ink under {MIN_INK_CLEAR}pt clearance: {g2}  "
      f"{'OK' if g2 == 0 else 'FAIL'}")
