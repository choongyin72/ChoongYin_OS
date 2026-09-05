"""Build LOAD_ALL_R10.sql, mirroring LOAD_ALL_R07.sql.

    py tmp/gen_load_all_r10.py [--apply]

The @@ list is read from the files actually present in sources/SQLs rather than typed out, and
every reference is checked to resolve before the file is written - a LOAD_ALL that names a
missing script fails halfway through with partial state, which the header itself warns about.

Differences from the R07 version, both factual rather than stylistic:
  * No exclusions. R07 skips R07.012/014 because those pairs are hand-maintained; every R10
    pair is generated, so all 19 are listed.
  * R07's 6.17 section carries a caveat that R07.017-022 point at a *_6_17.jasper that cannot
    be built, because the converter dropped their <group>. That no longer applies to R10: all
    19 downgrades verify IDENTICAL and all 38 artifacts are deployed and current.
"""
import os
import re
import sys

SQL = r"C:\Projects\INPEX\sources\SQLs"
OUT = os.path.join(SQL, "LOAD_ALL_R10.sql")
APPLY = "--apply" in sys.argv

six = sorted(f for f in os.listdir(SQL)
             if re.match(r'R10_.*\.sql$', f) and not f.endswith("_V7.sql")
             and "backup" not in f)
v7 = sorted(f for f in os.listdir(SQL)
            if re.match(r'R10_.*_V7\.sql$', f) and "backup" not in f)

if len(six) != len(v7):
    raise SystemExit("%d 6.17 script(s) but %d V7 - the pairs are incomplete" % (len(six), len(v7)))
for f in six:
    if f[:-4] + "_V7.sql" not in v7:
        raise SystemExit("%s has no _V7 partner" % f)

HDR = """-- =====================================================================
-- LOAD_ALL_R10.sql - load every generated EC report registration for R10
--
-- Run from THIS folder (@@ resolves relative to this script):
--     sqlplus ECKERNEL_EC/<pw>@<host>:1521/<svc> @LOAD_ALL_R10.sql
--
-- %d report files x 2 engines = %d registrations.
--
-- Each file carries its OWN TEMPLATE_CODE - <BASE>_6_17 for the JASPER (6.17)
-- registration, <BASE> for the JASPER_V7 (7.0.3) one - so both coexist and all %d
-- survive a full run. Order below is presentational only.
--
-- Every TEMPLATE_CODE is within the 32-character cap; the longest is
-- R10_030_FOB_ADP_CONTRACT_6_17 (29).
--
-- R10.012, R10.030 and R10.031 hold more than one report file, so they contribute
-- more than one pair each: 15 folders -> %d report files.
--
-- No COMMIT and no error handling, matching LOAD_ALL_R07.sql. Transaction control is
-- left to however this is invoked. Note the TV_ views auto-commit via their INSTEAD OF
-- triggers while the REPORT_ITEM / REPORT_ITEM_PARAM deletes do not, so a failure
-- partway through leaves partial state and will NOT stand out in the output.
-- =====================================================================

-- ---- 6.17 / JASPER  (%d scripts, code <BASE>_6_17, point at *_6_17.jasper) ----
--      All %d downgrades verify IDENTICAL against their 7.0.3 render and every
--      artifact is deployed and current, so nothing here is a placeholder.
""" % (len(six), len(six) * 2, len(six) * 2, len(six), len(six), len(six))

body = HDR + "".join("@@%s\n" % f for f in six)
body += ("\n-- ---- 7.0.3 / JASPER_V7  (%d scripts, code <BASE>, all artifacts verified) ----\n"
         % len(v7))
body += "".join("@@%s\n" % f for f in v7)

# ---- guard: every @@ reference must resolve
missing = [m for m in re.findall(r'^@@(\S+)', body, re.M)
           if not os.path.exists(os.path.join(SQL, m))]
if missing:
    raise SystemExit("these @@ references do not exist: %s" % missing)
print("%d @@ reference(s), all resolve" % len(re.findall(r'^@@', body, re.M)))
for f in six:
    print("   %-30s %s" % (f, f[:-4] + "_V7.sql"))

if APPLY:
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(body)
    print("\nwritten: %s (%d bytes)" % (OUT, len(body)))
else:
    print("\ndry run - rerun with --apply")
