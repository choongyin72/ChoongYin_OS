"""Render generated-vs-reference section crops so they can actually be LOOKED at.

This is the step that must run BEFORE any numeric diff (lessons file Part Y8): a per-attribute
diff can score zero on a section that is visibly wrong, because it is blind wherever its
attribute is absent.

    py crop_sheet.py R07.004                 # auto-slice every page into bands
    py crop_sheet.py R07.004 --page 1        # one page only
    py crop_sheet.py R07.004 --dpi 200

Sections are cut at the report's own full-width horizontal rules, so each crop is a real
section rather than an arbitrary slice. Output goes to <report>/_crops/ as pairs named
pNN_sMM_ref.png / pNN_sMM_gen.png - open them side by side, or read them one pair at a time.
"""
import os
import sys

import fitz

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import BASE, open_pair, resolve   # noqa: E402


def section_bounds(page, top_pad=6, bottom_pad=6):
    """Cut points = the page's own full-width horizontal rules."""
    ys = sorted({round(d["rect"].y0, 1) for d in page.get_drawings()
                 if (d["rect"].y1 - d["rect"].y0) < 3
                 and (d["rect"].x1 - d["rect"].x0) > page.rect.width * 0.5})
    cuts = [page.rect.y0]
    for y in ys:
        if y - cuts[-1] > 40:            # ignore rules that are only pixels apart
            cuts.append(y)
    cuts.append(page.rect.y1)
    out = []
    for a, b in zip(cuts, cuts[1:]):
        if b - a > 25:
            out.append((max(page.rect.y0, a - top_pad), min(page.rect.y1, b + bottom_pad)))
    return out


def main():
    report = sys.argv[1] if len(sys.argv) > 1 else None
    if report is None:
        raise SystemExit("usage: py crop_sheet.py <report> [--page N] [--dpi N]")
    only = None
    dpi = 150
    if "--page" in sys.argv:
        only = int(sys.argv[sys.argv.index("--page") + 1])
    if "--dpi" in sys.argv:
        dpi = int(sys.argv[sys.argv.index("--dpi") + 1])

    gen, ref = open_pair(report)
    outdir = os.path.join(BASE, report, "_crops")
    os.makedirs(outdir, exist_ok=True)
    for f in os.listdir(outdir):
        if f.endswith(".png"):
            os.remove(os.path.join(outdir, f))

    if len(gen) != len(ref):
        print(f"!! PAGE COUNT DIFFERS: generated={len(gen)} reference={len(ref)}")

    total = 0
    for p in range(min(len(gen), len(ref))):
        if only and p + 1 != only:
            continue
        # slice on the REFERENCE, so sections are defined by the thing being matched
        for s, (y0, y1) in enumerate(section_bounds(ref[p]), start=1):
            clip = fitz.Rect(ref[p].rect.x0, y0, ref[p].rect.x1, y1)
            for tag, doc in (("ref", ref), ("gen", gen)):
                doc[p].get_pixmap(dpi=dpi, clip=clip).save(
                    os.path.join(outdir, f"p{p+1:02d}_s{s:02d}_{tag}.png"))
            print(f"  page {p+1} section {s:2}  y {y0:7.1f} - {y1:7.1f}")
            total += 1
    print(f"\n{total} crop pairs written to {outdir}")
    print("LOOK at these before running any numeric diff.")


if __name__ == "__main__":
    main()
