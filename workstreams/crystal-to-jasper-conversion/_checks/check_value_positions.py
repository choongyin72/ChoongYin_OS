"""Did any value land in the wrong column? Compare each text's rendered x-centre in gen
against the reference. A value in the wrong column shows up as a large centre shift, which
neither a text-presence diff nor a border-boundary check can see."""
import collections
import fitz

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import open_pair  # noqa: E402

gen, ref = open_pair()
# 12.0 was too loose: on R07.005 the data-row labels were 11.8pt out (they were not indented
# under their sub-headings at all) and this check passed them. The owner found it by eye.
# 4.0 still ignores rendering rounding and font-metric differences of ~1-2pt.
TOL = 4.0


def spans(page):
    out = collections.defaultdict(list)
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                t = s["text"].strip()
                if t:
                    out[t].append(((s["bbox"][0] + s["bbox"][2]) / 2, s["bbox"][1]))
    return out


bad = 0
for p in range(min(len(gen), len(ref))):
    G, R = spans(gen[p]), spans(ref[p])
    for t, rlist in R.items():
        glist = G.get(t)
        if not glist or len(glist) != len(rlist):
            continue
        # sort by (row, then x) - sorting by y alone cannot pair duplicates that share a
        # row, which produced false "shifts" of up to 264pt on rows of four zeros
        rlist = sorted(rlist, key=lambda z: (round(z[1] / 10), z[0]))
        glist = sorted(glist, key=lambda z: (round(z[1] / 10), z[0]))
        for (rc, ry), (gc, gy) in zip(rlist, glist):
            if abs(gc - rc) > TOL:
                print(f"  page {p+1}  y~{ry:7.1f}  {t[:34]!r:38} "
                      f"ref centre {rc:7.1f}  gen {gc:7.1f}  shift {gc-rc:+7.1f}")
                bad += 1
print(f"\nvalues off by more than {TOL}pt: {bad}")
