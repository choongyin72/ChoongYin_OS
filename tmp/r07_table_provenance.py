"""Resolve the "unverified provenance" of the TV_* table names in R07.011-022.

    py tmp/r07_table_provenance.py

`EC-DEPLOYMENT-FINDINGS.md` records this as the blocker for SQL query binding:

    "Only 2 of those tables have DDLs (sources/SQLs/DDLs/) ... The other table names have
     UNVERIFIED provenance. They predate any of my edits ... but appear nowhere in
     sources/SQLs. The uniform naming is equally consistent with a real convention or a
     pattern extrapolated from the two that exist."

That note is dated 2026-09-03. `sources/SQLs/DDLs/` now holds TWELVE files, and R07.011-022 is
twelve reports - so this checks, name by name, whether every table a JRXML actually selects FROM
has a real DDL on disk. A name with a DDL is not extrapolated.

Read-only: it opens JRXMLs and .sql files and writes nothing.
"""
import os
import re

BASE = r"C:\Projects\INPEX\sources\CrystalReports"
DDLDIR = r"C:\Projects\INPEX\sources\SQLs\DDLs"
SQLDIR = r"C:\Projects\INPEX\sources\SQLs"

ddls = {}
for f in sorted(os.listdir(DDLDIR)):
    if not f.lower().endswith(".sql"):
        continue
    body = open(os.path.join(DDLDIR, f), encoding="utf-8", errors="replace").read()
    m = re.search(r'CREATE\s+(?:OR\s+REPLACE\s+)?(TABLE|VIEW)\s+"?(\w+)"?', body, re.I)
    ddls[f[:-4].upper()] = (m.group(1).upper() if m else "?",
                            m.group(2).upper() if m else "?",
                            len(re.findall(r'^\s*"?\w+"?\s+(?:VARCHAR2|NUMBER|DATE|CHAR|CLOB|'
                                           r'TIMESTAMP)', body, re.I | re.M)))
print("DDLs on disk: %d" % len(ddls))
for k, (kind, name, cols) in sorted(ddls.items()):
    flag = "" if k == name else "   <-- file name != object name (%s)" % name
    print("   %-42s %-5s %3d col(s)%s" % (k, kind, cols, flag))

# every table a JRXML actually selects FROM
print("\nreports and the table they query:")
used, unmatched = {}, []
for rep in sorted(d for d in os.listdir(BASE) if d.startswith("R07.0")):
    S = os.path.join(BASE, rep, "output")
    if not os.path.isdir(S):
        continue
    for fn in sorted(f for f in os.listdir(S) if f.endswith(".jrxml") and "backup" not in f):
        t = open(os.path.join(S, fn), encoding="utf-8", errors="replace").read()
        q = re.search(r'<query[^>]*>\s*<!\[CDATA\[(.*?)\]\]>', t, re.S)
        if not q:
            continue
        for tab in {x.upper() for x in re.findall(r'\bFROM\s+"?(\w+)"?', q.group(1), re.I)}:
            if tab == "DUAL":
                print("   %-9s %-46s %s" % (rep, fn[:-6][:46], "DUAL (record generator)"))
                continue
            used.setdefault(tab, []).append(rep)
            has = tab in ddls or any(v[1] == tab for v in ddls.values())
            print("   %-9s %-46s %-38s %s"
                  % (rep, fn[:-6][:46], tab, "DDL ok" if has else "NO DDL"))
            if not has:
                unmatched.append((rep, tab))

print("\n%d distinct table(s) queried, %d without a DDL" % (len(used), len(set(unmatched))))
for rep, tab in unmatched:
    print("   %-9s %s" % (rep, tab))

spare = sorted(set(ddls) - {t for t in used})
print("\nDDLs with no report querying them: %d" % len(spare))
for s in spare:
    print("   %s" % s)

# is there loader data for them?
print("\nrow-data loaders in sources/ (INSERT scripts):")
for f in sorted(os.listdir(os.path.dirname(SQLDIR))):
    if f.lower().endswith("_insert.sql"):
        print("   %s" % f)
