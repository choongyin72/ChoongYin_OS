"""Same missing/extra horizontal-rule check as page 2, run across all 5 pages."""
import fitz

from _common import open_pair

gen, ref = open_pair()


def rules(page):
    d = {}
    for dr in page.get_drawings():
        r = dr["rect"]
        if (r.x1 - r.x0) < 40:
            continue
        if (r.y1 - r.y0) < 2:
            d.setdefault(round((r.y0 + r.y1) / 2, 1), []).append((r.x0, r.x1))
        elif (r.y1 - r.y0) >= 5:
            d.setdefault(round(r.y0, 1), []).append((r.x0, r.x1))
            d.setdefault(round(r.y1, 1), []).append((r.x0, r.x1))
    out = {}
    for k in sorted(d):
        tgt = next((o for o in out if abs(o - k) <= 1.5), None)
        if tgt is None:
            out[k] = list(d[k])
        else:
            out[tgt].extend(d[k])
    return {k: (round(min(s[0] for s in v), 1), round(max(s[1] for s in v), 1))
            for k, v in out.items()}


def label(page, y):
    best, bd = "", 1e9
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                t = s["text"].strip()
                if not t:
                    continue
                dy = y - s["bbox"][3]
                if 0 <= dy < bd:
                    bd, best = dy, t
    return best[:34]


grand = 0
for pg in range(min(len(gen), len(ref))):
    gr, rr = rules(gen[pg]), rules(ref[pg])
    msgs, shown = [], set()
    for y in sorted(set(list(rr) + list(gr))):
        rm = next((k for k in rr if abs(k - y) <= 2.5), None)
        gm = next((k for k in gr if abs(k - y) <= 2.5), None)
        if (rm, gm) in shown:
            continue
        shown.add((rm, gm))
        if rm is not None and gm is None:
            msgs.append(f"   MISSING  ref y={rm:7.1f} span={rr[rm]}  "
                        f"after {label(ref[pg], rm)!r}")
        elif gm is not None and rm is None:
            msgs.append(f"   EXTRA    gen y={gm:7.1f} span={gr[gm]}  "
                        f"after {label(gen[pg], gm)!r}")
    print(f"===== page {pg+1}: {len(msgs)} rule differences =====")
    for m in msgs:
        print(m)
    grand += len(msgs)
print(f"\nTOTAL rule differences across all pages: {grand}")
