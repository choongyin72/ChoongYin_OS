"""Which logo file does each R10.0xx JRXML reference?

    py tmp/r10_logo_audit.py

Read-only. Reports the image expression, the box it is drawn in, and the scale mode, for every
non-backup JRXML in R10.001 .. R10.034.

Context for why the box matters: on R07 the root cause of the logo failures was a NAME COLLISION
- R07.001-006 and R07.011-025 both asked for `logo.png` but need different artwork (a wide INPEX
wordmark, aspect ~5.78, versus an "INPEX | Ichthys Project" tile, aspect 1.903), and one flat
extension folder cannot serve that. So a mismatch between the file asked for and the box's aspect
is the signal worth surfacing, not just the filename.
"""
import os
import re

BASE = r"C:\Projects\INPEX\sources\CrystalReports"
ELEM = re.compile(r'<element\b[^>]*?/>|<element\b[^>]*?>.*?</element>', re.S)

rows, missing = [], []
for rep in sorted(d for d in os.listdir(BASE) if re.match(r'R10\.0(0[1-9]|[12][0-9]|3[0-4])$', d)):
    S = os.path.join(BASE, rep, "output")
    if not os.path.isdir(S):
        missing.append((rep, "no output/ folder"))
        continue
    jrs = [f for f in sorted(os.listdir(S)) if f.endswith(".jrxml") and "backup" not in f]
    if not jrs:
        missing.append((rep, "no jrxml"))
        continue
    for fn in jrs:
        t = open(os.path.join(S, fn), encoding="utf-8", errors="replace").read()
        hit = None
        for s in ELEM.findall(t):
            if 'kind="image"' not in s:
                continue
            e = re.search(r'<expression><!\[CDATA\[(.*?)\]\]></expression>', s, re.S)
            g = dict(re.findall(r'\b(x|y|width|height)="(-?\d+)"', s))
            sc = re.search(r'scaleImage="(\w+)"', s)
            hit = (re.sub(r'\s+', ' ', e.group(1)).strip() if e else "(no expression)",
                   int(g.get("width", 0)), int(g.get("height", 0)),
                   sc.group(1) if sc else "-")
            break
        if hit:
            rows.append((rep, fn[:-6], hit))
        else:
            rows.append((rep, fn[:-6], None))

print("%-9s %-44s %-9s %-7s %-12s %s"
      % ("report", "jrxml", "box", "aspect", "scale", "image expression"))
print("-" * 124)
names = {}
for rep, stem, hit in rows:
    if hit is None:
        print("%-9s %-46s %s" % (rep, stem[:46], "NO IMAGE ELEMENT"))
        names.setdefault("(none)", []).append(rep)
        continue
    expr, w, h, sc = hit
    f = re.search(r'"([^"]*\.(?:png|jpg|jpeg|gif))"', expr)
    fname = f.group(1) if f else "(dynamic)"
    names.setdefault(fname, []).append(rep)
    print("%-9s %-44s %-9s %-7s %-12s %s"
          % (rep, stem[:44], "%dx%d" % (w, h), ("%.2f" % (w / h)) if h else "-", sc, expr))

print("\nlogo file usage:")
for k, v in sorted(names.items()):
    print("   %-24s %2d report file(s): %s" % (k, len(v), ", ".join(sorted(set(v)))))
if missing:
    print("\nno jrxml found:")
    for rep, why in missing:
        print("   %-9s %s" % (rep, why))

# does the referenced file actually exist anywhere under the project?
print("\nfiles present on disk (searched under C:\\Projects\\INPEX):")
want = {k for k in names if k not in ("(none)", "(dynamic)")}
seen = {}
for root, _d, fs in os.walk(r"C:\Projects\INPEX"):
    for f in fs:
        if f in want:
            seen.setdefault(f, []).append(os.path.join(root, f))
for k in sorted(want):
    got = seen.get(k, [])
    print("   %-24s %d copy(ies)%s" % (k, len(got), "" if got else "   <-- NOT FOUND"))
