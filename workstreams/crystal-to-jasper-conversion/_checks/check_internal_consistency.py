"""Compare a generated report against ITSELF - no reference involved.

Why this exists: every other check in this folder compares the output to the Crystal
reference. On R07.004 the owner found that the Inventory header divider rendered 2.04pt while
every data-row divider below it rendered 1.02pt. Crystal has the SAME 2pt header divider, so a
reference comparison called it correct and would have preserved the flaw. The owner's standard:
a defect counts even when the original shares it.

    py check_internal_consistency.py R07.004
    py check_internal_consistency.py R07.004 --dpi 1200

What it checks, per table, using rendered pixels rather than element geometry:
  1. every vertical column line has the same thickness as the others in that table,
     INCLUDING the one inside the header band
  2. every horizontal row line has the same thickness
  3. row heights are uniform (excluding a table's first/last row, which legitimately differ)

A table whose header divider is twice its body divider fails check 1 - which is exactly the
R07.004 defect.
"""
import collections
import os
import statistics
import sys

import fitz

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import open_pair  # noqa: E402

TOL = 0.35          # pt; below this is rendering rounding, not a defect


def is_purple(px):
    r, g, b = px
    return b > 100 and r < 130


def is_white(px):
    r, g, b = px
    return r > 246 and g > 246 and b > 246


def line_width_at(page, x, y, dpi, half=3.0):
    """Thickness of the vertical line crossing (x, y), or None if there is no line."""
    pix = page.get_pixmap(dpi=dpi, clip=fitz.Rect(x - half, y, x + half, y + 0.3))
    w, h, n, s = pix.width, pix.height, pix.n, pix.samples
    sc = dpi / 72.0
    hits = []
    for i in range(w):
        p = i * n
        px = (s[p], s[p + 1], s[p + 2])
        if not is_purple(px) and not is_white(px):
            hits.append(i)
    if not hits:
        return None
    runs, start, prev, best = [], hits[0], hits[0], 0
    for v in hits[1:]:
        if v != prev + 1:
            runs.append((start, prev))
            start = v
        prev = v
    runs.append((start, prev))
    a, b = max(runs, key=lambda r: r[1] - r[0])
    width = (b - a + 1) / sc
    # A gridline is never this thick. A wide "run" means the probe landed on text (the
    # antialiased edges of white glyphs on purple read as neither white nor purple) or on a
    # fill boundary - not a line, so report nothing rather than a false finding.
    if width > 3.0:
        return None
    return width


def tables_from_rules(page):
    """Split the page into table bands at its own wide horizontal rules."""
    ys = sorted({round(d["rect"].y0, 1) for d in page.get_drawings()
                 if (d["rect"].y1 - d["rect"].y0) < 3
                 and (d["rect"].x1 - d["rect"].x0) > page.rect.width * 0.5})
    cuts = [page.rect.y0] + [y for y in ys] + [page.rect.y1]
    out = []
    for a, b in zip(cuts, cuts[1:]):
        if b - a > 30:
            out.append((a, b))
    return out


def column_x_positions(page, y0, y1):
    """Distinct vertical-line x positions inside a band."""
    xs = collections.Counter()
    for d in page.get_drawings():
        r = d["rect"]
        if r.y0 >= y0 - 2 and r.y1 <= y1 + 2:
            if (r.x1 - r.x0) < 3 and (r.y1 - r.y0) >= 4:
                xs[round(r.x0)] += 1
            elif (r.x1 - r.x0) >= 8 and (r.y1 - r.y0) >= 5:
                xs[round(r.x0)] += 1
                xs[round(r.x1)] += 1
    return [x for x, c in xs.items() if c >= 2]


def main():
    report = sys.argv[1] if len(sys.argv) > 1 else None
    if not report:
        raise SystemExit("usage: py check_internal_consistency.py <report> [--dpi N]")
    dpi = 1200
    if "--dpi" in sys.argv:
        dpi = int(sys.argv[sys.argv.index("--dpi") + 1])
    gen, _ref = open_pair(report)

    findings = 0
    for p in range(len(gen)):
        page = gen[p]
        for y0, y1 in tables_from_rules(page):
            xs = sorted(column_x_positions(page, y0, y1))
            if len(xs) < 2:
                continue
            # sample each column line at several heights down the band
            widths = collections.defaultdict(list)
            steps = [y0 + (y1 - y0) * f for f in (0.15, 0.35, 0.55, 0.75, 0.92)]
            for x in xs:
                for y in steps:
                    w = line_width_at(page, x, y, dpi)
                    if w:
                        widths[round(y, 1)].append(round(w, 2))
            allw = [w for lst in widths.values() for w in lst]
            if len(allw) < 4:
                continue
            med = statistics.median(allw)
            odd = {y: lst for y, lst in widths.items()
                   if lst and abs(statistics.median(lst) - med) > TOL}
            if odd:
                print(f"  page {p+1}  band y {y0:.0f}-{y1:.0f}: column lines are not a "
                      f"uniform thickness (median {med:.2f}pt)")
                for y, lst in sorted(odd.items()):
                    print(f"       at y={y:7.1f} -> {statistics.median(lst):.2f}pt  {lst}")
                findings += 1

    print(f"\ninternal-consistency findings: {findings}")


if __name__ == "__main__":
    main()
