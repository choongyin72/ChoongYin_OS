"""Audit the EC report-registration scripts in sources/SQLs - 6.17 vs V7 pairs.

    py tmp/sql_reg_audit.py

READ-ONLY. The owner has said not to modify sources/SQLs or its DDLs subfolder; this only opens
and reports.

Each report has two registration scripts:
    <CODE>.sql       REPORT_SYSTEM_CODE = 'JASPER'      -> the 6.17.0-compiled artifact
    <CODE>_V7.sql    REPORT_SYSTEM_CODE = 'JASPER_V7'   -> the 7.0.3 artifact

They register the SAME TEMPLATE_CODE / REP_GROUP_CODE, and each begins with a DELETE block keyed
on that code - so they are mutually exclusive by construction: running one removes the other.
What distinguishes them is the ENGINE and the ARTIFACT PATH.

Checked per pair:
  1. does the 6.17 script point at a _6_17 artifact, or at the V7 one?
  2. do the two scripts point at the SAME file (which would make the pair pointless)?
  3. Jasper Definition Url - .jasper or .jrxml? R07.001 had to be switched to .jrxml because
     jdk.serialFilter rejects its 995KB .jasper, and its 6.17 .jasper is larger still.
  4. do the referenced artifacts actually exist in the deployment folder?
"""
import os
import re

S = r"C:\Projects\INPEX\sources\SQLs"
DEPLOY = (r"C:\Projects\INPEX\DEV\ecaas_inpex_ichthys\extensions\zrep\zrep"
          r"\src\main\webapp\reports")


def facts(p):
    t = open(p, encoding="utf-8", errors="replace").read()
    sysc = re.search(r"'(JASPER(?:_V7)?)'", t)
    url = re.search(r"PARAMETER_STATIC_VALUE = '([^']+)'", t)
    jrxml = re.search(r"PARAMETER_VALUE\s*=\s*'([^']*\.jrxml)'", t)
    grp = re.search(r"REP_GROUP_CODE = '([A-Z0-9_]+)'", t)
    return (sysc.group(1) if sysc else "?",
            url.group(1) if url else "-",
            jrxml.group(1) if jrxml else "-",
            grp.group(1) if grp else "?")


deployed = set(os.listdir(DEPLOY)) if os.path.isdir(DEPLOY) else set()
print("deployment folder: %s (%d file(s))"
      % (DEPLOY if deployed else "NOT FOUND", len(deployed)))

pairs = sorted({f[:-4].replace("_V7", "") for f in os.listdir(S)
                if f.endswith(".sql") and "backup" not in f and f[0] == "R"})
bad = []
print("\n%-22s %-11s %-52s %s" % ("code", "system", "Jasper Definition Url", "exists"))
print("-" * 104)
for code in pairs:
    for suffix, label in (("", "6.17"), ("_V7", "V7")):
        p = os.path.join(S, code + suffix + ".sql")
        if not os.path.exists(p):
            continue
        sysc, url, jrxml, grp = facts(p)
        base = os.path.basename(url)
        ex = "yes" if base in deployed else ("NOT DEPLOYED" if deployed else "?")
        print("%-22s %-11s %-52s %s" % (code + suffix, sysc, url[-52:], ex))
        # the 6.17 registration must not point at the V7 artifact
        if suffix == "" and url != "-" and "_6_17" not in base:
            bad.append((code, "6.17 script points at a NON-_6_17 artifact: %s" % base))
        if suffix == "_V7" and "_6_17" in base:
            bad.append((code, "V7 script points at the _6_17 artifact: %s" % base))
    # do the two point at the same file?
    a = os.path.join(S, code + ".sql")
    b = os.path.join(S, code + "_V7.sql")
    if os.path.exists(a) and os.path.exists(b):
        ua, ub = facts(a)[1], facts(b)[1]
        if ua == ub and ua != "-":
            bad.append((code, "BOTH scripts point at the SAME artifact: %s"
                        % os.path.basename(ua)))

print("\n=== findings: %d" % len(bad))
seen = set()
for code, why in bad:
    if (code, why) in seen:
        continue
    seen.add((code, why))
    print("   %-22s %s" % (code, why))
