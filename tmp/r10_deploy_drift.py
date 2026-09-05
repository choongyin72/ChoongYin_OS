"""Do the DEPLOYED R10 artifacts match what we now produce?

    py tmp/r10_deploy_drift.py

The registration scripts just generated point at files in the EC extension folder. Those files
already existed - 19 _6_17.jrxml and 19 _6_17.jasper - even though sources/CrystalReports held
NO R10 downgrade at all until tonight. So they came from somewhere else, and whether they are
current is a question, not an assumption. A registration pointing at a stale artifact is worse
than one pointing at a missing file: the missing file fails loudly.

Compares, per R10 report file:
    deployed <stem>.jrxml        vs  sources/CrystalReports/<rep>/output/<stem>.jrxml
    deployed <stem>_6_17.jrxml   vs  sources/.../output/jr6/<stem>_jr6.jrxml

Read-only.
"""
import os
import re

SRC = r"C:\Projects\INPEX\sources\CrystalReports"
DEPLOY = (r"C:\Projects\INPEX\DEV\ecaas_inpex_ichthys\extensions\zrep\zrep"
          r"\src\main\webapp\reports")


def body(p):
    """Content minus the converter's generated header comment, which carries a timestamp."""
    t = open(p, encoding="utf-8", errors="replace").read().replace("\r\n", "\n")
    if t.startswith("<?xml") and "-->" in t[:2000]:
        t = t[t.index("-->") + 3:]
    return t.strip()


rows = []
for rep in sorted(d for d in os.listdir(SRC) if re.match(r'R10\.0', d)):
    o = os.path.join(SRC, rep, "output")
    if not os.path.isdir(o):
        continue
    for fn in sorted(f for f in os.listdir(o) if f.endswith(".jrxml")
                     and "backup" not in f and "variant" not in f.lower()):
        rows.append((rep, fn[:-6], o))

print("%-9s %-46s %-14s %s" % ("report", "stem", "v7 deployed", "6.17 deployed"))
print("-" * 92)
stale = []
for rep, stem, o in rows:
    d7 = os.path.join(DEPLOY, stem + ".jrxml")
    d6 = os.path.join(DEPLOY, stem + "_6_17.jrxml")
    s7 = os.path.join(o, stem + ".jrxml")
    s6 = os.path.join(o, "jr6", stem + "_jr6.jrxml")

    def cmp(dep, src):
        if not os.path.exists(dep):
            return "MISSING"
        if not os.path.exists(src):
            return "no source"
        return "same" if body(dep) == body(src) else "*** STALE"

    a, b = cmp(d7, s7), cmp(d6, s6)
    if "STALE" in a or "MISSING" in a:
        stale.append((stem, "v7", a))
    if "STALE" in b or "MISSING" in b:
        stale.append((stem, "6.17", b))
    print("%-9s %-46s %-14s %s" % (rep, stem[:46], a, b))

print("\n%d of %d artifact(s) need redeploying" % (len(stale), len(rows) * 2))
for stem, which, why in stale:
    print("   %-46s %-5s %s" % (stem[:46], which, why))
