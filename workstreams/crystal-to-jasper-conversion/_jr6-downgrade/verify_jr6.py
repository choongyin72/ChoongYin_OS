"""Verify a downgraded 6.x report renders identically to its 7.x original.

    py verify_jr6.py <report>            e.g. py verify_jr6.py R07.012
    py verify_jr6.py <report> --no-image  skip writing the comparison PNG

Compares, for the two PDFs:
  1. embedded FONT FAMILIES - catches the silent Arial->Helvetica fallback that makes 6.x drop
     isBold/isItalic without any error (README "two traps")
  2. every TEXT SPAN as an exact sorted tuple (page, x, y, size, font, text)
  3. every DRAWING RECT as an exact sorted tuple
  4. writes a stacked PNG so the result can be eyeballed, because a numeric pass has scored
     clean on a visibly wrong report before on this project

Exact whole-list equality is used deliberately instead of pairwise matching: matching spans by
(page, text, row) is ambiguous when a row holds repeated values like '0', and produced
fabricated 443pt offsets earlier.

Exit code 0 = identical, 1 = differences found.
"""
import collections
import os
import sys

import fitz

BASE = r"C:\Projects\INPEX\sources\CrystalReports"


def find_pdf(d, must_contain=None, exclude=None):
    best = None
    for f in os.listdir(d):
        if not f.lower().endswith(".pdf"):
            continue
        if must_contain and must_contain not in f:
            continue
        if exclude and exclude in f:
            continue
        p = os.path.join(d, f)
        if best is None or os.path.getmtime(p) > os.path.getmtime(best):
            best = p
    return best


def spans(d):
    return sorted((p, round(s["bbox"][0], 2), round(s["bbox"][1], 2),
                   round(s["size"], 2), s["font"], s["text"])
                  for p in range(len(d))
                  for bl in d[p].get_text("dict")["blocks"]
                  for l in bl.get("lines", []) for s in l["spans"] if s["text"].strip())


def rects(d):
    return sorted((p, round(g["rect"].x0, 2), round(g["rect"].y0, 2),
                   round(g["rect"].x1, 2), round(g["rect"].y1, 2))
                  for p in range(len(d)) for g in d[p].get_drawings())


def font_families(d):
    c = collections.Counter()
    for p in range(len(d)):
        for bl in d[p].get_text("dict")["blocks"]:
            for l in bl.get("lines", []):
                for s in l["spans"]:
                    if s["text"].strip():
                        c[s["font"]] += 1
    return c


def main():
    # --pdf mode: compare two explicit PDFs, e.g. two artifacts downloaded from EC. Same
    # comparison, no assumption about where they live.
    if sys.argv[1] == "--pdf":
        p6, p7 = sys.argv[2], sys.argv[3]
        jr6dir = os.path.dirname(os.path.abspath(p6))
        return run(p6, p7, jr6dir)

    report = sys.argv[1]
    out = os.path.join(BASE, report, "output")
    jr6dir = os.path.join(out, "jr6")

    p6 = find_pdf(jr6dir)
    p7 = find_pdf(out, exclude="reverify")
    if not p6 or not p7:
        raise SystemExit(f"need a PDF in {jr6dir} and in {out} (found {p6}, {p7})")
    return run(p6, p7, jr6dir)


def run(p6, p7, jr6dir):

    print(f"A (6.x) : {p6}")
    print(f"7.x : {p7}\n")
    a, b = fitz.open(p6), fitz.open(p7)

    ok = True

    f6, f7 = font_families(a), font_families(b)
    same_fonts = f6 == f7
    ok &= same_fonts
    print(f"font families  : {'IDENTICAL' if same_fonts else 'DIFFER'}")
    if not same_fonts:
        print(f"    6.x: {dict(f6)}")
        print(f"    7.x: {dict(f7)}")
        if len(f6) == 1 and "Helvetica" in next(iter(f6)):
            print("    -> only Helvetica: the font EXTENSION is missing from the 6.x")
            print("       classpath, so Arial fell back and isBold/isItalic were dropped.")

    print(f"pages          : 6.x={len(a)} 7.x={len(b)}")

    s6, s7 = spans(a), spans(b)
    same = s6 == s7
    ok &= same
    print(f"text spans     : 6.x={len(s6)} 7.x={len(s7)}  "
          f"{'IDENTICAL' if same else 'DIFFER'}")
    if not same:
        d = [(x, y) for x, y in zip(s6, s7) if x != y]
        print(f"    first differing of {len(d)}:")
        for x, y in d[:6]:
            print(f"      6.x={x}\n      7.x={y}")

    r6, r7 = rects(a), rects(b)
    same = r6 == r7
    ok &= same
    print(f"drawing rects  : 6.x={len(r6)} 7.x={len(r7)}  "
          f"{'IDENTICAL' if same else 'DIFFER'}")
    if not same:
        if len(r6) < len(r7) * 0.5:
            print("    -> 6.x has far fewer rects: likely a dropped <box>, which is where")
            print("       cell borders live. Check <box> children of <style>.")
        d = [(x, y) for x, y in zip(r6, r7) if x != y]
        for x, y in d[:6]:
            print(f"      6.x={x}\n      7.x={y}")

    if "--no-image" not in sys.argv:
        GAP = 12
        pa = a[0].get_pixmap(dpi=95)
        pb = b[0].get_pixmap(dpi=95)
        img = fitz.Pixmap(fitz.csRGB, fitz.IRect(
            0, 0, max(pa.width, pb.width), pa.height + GAP + pb.height))
        img.set_rect(img.irect, (200, 200, 200))
        pa.set_origin(0, 0)
        pb.set_origin(0, pa.height + GAP)
        img.copy(pa, pa.irect)
        img.copy(pb, pb.irect)
        path = os.path.join(jr6dir, "CMP_jr6_over_jr7.png")
        img.save(path)
        print(f"\nvisual (6.x on top): {path}")
        print("LOOK at it - a numeric pass has scored clean on a visibly wrong report before.")

    print(f"\nRESULT: {'IDENTICAL' if ok else 'DIFFERENCES FOUND'}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
