"""Matched gridline ink comparison, gen vs ref, both axes, all pages.

For every horizontal and vertical rule, measure the RENDERED ink thickness at 600 dpi
(probing only clean-white positions so glyphs cannot inflate it), pair gen rules to ref
rules by nearest position, and report every pair differing by more than 0.4pt.

This is the check that should gate any "matches" claim - a per-attribute diff can pass
while the rendered line is twice as thick.
"""
import collections
import statistics
import fitz

from _common import open_pair

gen, ref = open_pair()
DPI, SC = 600, 600 / 72.0
TOL = 0.4


def rules(page):
    """Return (horizontals, verticals) as {pos: (span_lo, span_hi)} merged clusters."""
    h, v = collections.defaultdict(list), collections.defaultdict(list)
    for dr in page.get_drawings():
        r = dr["rect"]
        hh, ww = r.y1 - r.y0, r.x1 - r.x0
        if hh < 3 and ww >= 20:
            h[round((r.y0 + r.y1) / 2, 1)].append((r.x0, r.x1))
        elif ww < 3 and hh >= 5:
            v[round((r.x0 + r.x1) / 2, 1)].append((r.y0, r.y1))
        elif ww >= 20 and hh >= 5:
            h[round(r.y0, 1)].append((r.x0, r.x1))
            h[round(r.y1, 1)].append((r.x0, r.x1))
            v[round(r.x0, 1)].append((r.y0, r.y1))
            v[round(r.x1, 1)].append((r.y0, r.y1))

    def merge(d):
        out = {}
        for k in sorted(d):
            if out and k - max(out) <= 1.4:
                mk = max(out)
                out[mk] = out[mk] + d[k]
            else:
                out[k] = list(d[k])
        return {round(sum(v2 for v2 in [k]) , 1): sp for k, sp in out.items()}
    return merge(h), merge(v)


def ink(page, pos, lo, hi, horizontal):
    ws = []
    step = max(5, int((hi - lo) / 14))
    for t in range(int(lo) + 6, int(hi) - 5, step):
        clip = (fitz.Rect(t, pos - 4, t + 1.0, pos + 4) if horizontal
                else fitz.Rect(pos - 4, t, pos + 4, t + 1.0))
        pix = page.get_pixmap(dpi=DPI, clip=clip)
        w, hgt, n, s = pix.width, pix.height, pix.n, pix.samples
        if horizontal:
            c = w // 2
            lum = [(s[(r*w+c)*n]*30 + s[(r*w+c)*n+1]*59 + s[(r*w+c)*n+2]*11)//100
                   for r in range(hgt)]
        else:
            r0 = hgt // 2
            lum = [(s[(r0*w+x)*n]*30 + s[(r0*w+x)*n+1]*59 + s[(r0*w+x)*n+2]*11)//100
                   for x in range(w)]
        runs, i = [], 0
        while i < len(lum):
            if lum[i] < 225:
                j = i
                while j < len(lum) and lum[j] < 225:
                    j += 1
                runs.append(j - i); i = j
            else:
                i += 1
        if len(runs) == 1 and runs[0] / SC < 6:
            ws.append(runs[0] / SC)
    return round(statistics.median(ws), 2) if len(ws) >= 2 else None


total = 0
for p in range(min(len(gen), len(ref))):
    gh, gv = rules(gen[p])
    rh, rv = rules(ref[p])
    issues = []
    for axis, gd, rd, horiz in (("H", gh, rh, True), ("V", gv, rv, False)):
        for pos, spans in sorted(gd.items()):
            lo, hi = min(s[0] for s in spans), max(s[1] for s in spans)
            if hi - lo < 30:
                continue
            cand = [q for q in rd if abs(q - pos) <= 3.0]
            if not cand:
                issues.append(f"  {axis} {pos:7.1f}  no matching rule in ref")
                continue
            q = min(cand, key=lambda z: abs(z - pos))
            gi = ink(gen[p], pos, lo, hi, horiz)
            rspans = rd[q]
            rlo, rhi = min(s[0] for s in rspans), max(s[1] for s in rspans)
            ri = ink(ref[p], q, rlo, rhi, horiz)
            if gi is None or ri is None:
                continue
            if abs(gi - ri) > TOL:
                issues.append(f"  {axis} {pos:7.1f} (ref {q:7.1f})  gen={gi:4.2f}pt "
                              f"ref={ri:4.2f}pt  diff={gi-ri:+.2f}")
    if issues:
        print(f"===== page {p+1}: {len(issues)} gridline mismatches =====")
        for s in issues:
            print(s)
        print()
        total += len(issues)

print(f"TOTAL gridline ink mismatches: {total}")
