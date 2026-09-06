"""Every generated R10 script must be its template with only the code and stem swapped.

    py tmp/verify_r10_sql.py

This is the check that would have caught the dropped P_REPORT_DATE block immediately. Comparing
"does it contain JRXML/FORMAT" only proves what you thought to look for; normalising the code and
stem away and diffing the WHOLE file against the template proves nothing else moved at all.

Read-only.
"""
import os
import re

SQL = r"C:\Projects\INPEX\sources\SQLs"
T617 = os.path.join(SQL, "R07_016_PC_LIFTING.sql")
TV7 = os.path.join(SQL, "R07_016_PC_LIFTING_V7.sql")
DEPLOY = (r"C:\Projects\INPEX\DEV\ecaas_inpex_ichthys\extensions\zrep\zrep"
          r"\src\main\webapp\reports")
SRC = r"C:\Projects\INPEX\sources\CrystalReports"
MAX_CODE = 32


def norm(path, code, stem):
    t = open(path, encoding="utf-8", errors="replace").read().replace("\r\n", "\n")
    return t.replace(code, "<CODE>").replace(stem, "<STEM>")


# stem for each generated code, read back out of the file itself
pairs = []
for f in sorted(os.listdir(SQL)):
    if not re.match(r'R10_.*\.sql$', f) or f.endswith("_V7.sql") or "backup" in f:
        continue
    base = f[:-4]
    t = open(os.path.join(SQL, f), encoding="utf-8", errors="replace").read()
    m = re.search(r'reports/([A-Za-z0-9_]+)_6_17\.jrxml', t)
    if not m:
        print("  %-28s NO _6_17 jrxml path" % base)
        continue
    pairs.append((base, m.group(1)))

ref617 = norm(T617, "R07_016_PC_LIFTING_6_17", "R07_016_PC_Lifting_Report")
refv7 = norm(TV7, "R07_016_PC_LIFTING", "R07_016_PC_Lifting_Report")

print("%-28s %-8s %-8s %-6s %-7s %s" % ("code", "6.17", "V7", "code<=32", "params", "artifacts"))
print("-" * 88)
bad = 0
for base, stem in pairs:
    f6 = os.path.join(SQL, base + ".sql")
    f7 = os.path.join(SQL, base + "_V7.sql")
    s6 = "same" if norm(f6, base + "_6_17", stem) == ref617 else "DIFFERS"
    s7 = "same" if os.path.exists(f7) and norm(f7, base, stem) == refv7 else "DIFFERS"
    cap = "ok" if len(base + "_6_17") <= MAX_CODE else "OVER"
    t6 = open(f6, encoding="utf-8", errors="replace").read()
    prm = [p for p in ("'JRXML'", "'P_REPORT_DATE'", "'FORMAT'") if p in t6]
    ps = "3/3" if len(prm) == 3 else "%d/3" % len(prm)
    arts = [stem + "_6_17.jasper", stem + "_6_17.jrxml", stem + ".jasper", stem + ".jrxml"]
    got = sum(1 for a in arts if os.path.exists(os.path.join(DEPLOY, a)))
    ar = "%d/4" % got
    ok = (s6 == "same" and s7 == "same" and cap == "ok" and ps == "3/3" and ar == "4/4")
    if not ok:
        bad += 1
    print("%-28s %-8s %-8s %-6s %-7s %s%s"
          % (base, s6, s7, cap, ps, ar, "" if ok else "   <-- CHECK"))

print("\n%d pair(s) checked, %d with a problem" % (len(pairs), bad))
print("6.17/V7  = whole file identical to its template once <CODE>/<STEM> are normalised")
print("params   = JRXML + P_REPORT_DATE + FORMAT all registered")
print("artifacts= the 4 files the pair references exist in the extension folder")
