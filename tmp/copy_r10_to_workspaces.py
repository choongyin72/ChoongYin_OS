"""Copy the R10 JRXMLs into BOTH Jaspersoft Studio workspaces' R10.XXX projects.

    py tmp/copy_r10_to_workspaces.py [--apply]

Owner, 2026-09-06:
  "...\\TIB_js-studiocomm_6.17.0_...\\INPEX_JasperReports\\R10.XXX for downgraded R10.XXX"
  "...\\js-studiocomm_7.0.3_...\\INPEX_JasperReports\\R10.XXX folder is for R10.XXX jrxml in
   ver 7.0.3"

So, exactly mirroring what tmp/copy_jr6_to_workspace.py and tmp/copy_jr7_to_workspace.py did for
R07 - same source-to-target rules, same naming, same backup-first behaviour:

  7.0.3 workspace   <report>/output/<stem>.jrxml          -> R10.XXX/<stem>.jrxml
  6.17.0 workspace  <report>/output/jr6/<stem>_jr6.jrxml  -> R10.XXX/<stem>_6_17.jrxml

The `_6_17` filename with a SINGLE underscore before it is the workspace's own existing
convention, taken from R07_012_FC_Lifting_Report_6_17.jrxml.

ONLY downgrades that the sweep verified are copied to 6.17 - `_jr6-downgrade/test_all.py`
reports IDENTICAL (exact span + rect + font equality against the 7.x render) and EC-LOAD-OK
(the 6.17 .jasper loads in EC's legacy 6.21.4 engine). That is the same rule the R07 copy
applied when it deliberately excluded R07.017-022. A downgrade that has not been verified does
not go into a workspace, because the workspace is where it gets picked up and deployed from.

Copies are byte-for-byte (shutil.copy2): these files are a mix of LF and CRLF, and rewriting
them in text mode would churn every line and make the next diff unreadable.
"""
import os
import shutil
import sys

S = r"C:\Projects\INPEX\sources\CrystalReports"
W7 = (r"C:\Tools\jasper\js-studiocomm_7.0.3_windows_x86_64\jaspersoftstudio"
      r"\JaspersoftWorkspace\INPEX_JasperReports\R10.XXX")
W6 = (r"C:\Tools\jasper\TIB_js-studiocomm_6.17.0_windows_x86_64\jaspersoftstudio"
      r"\JaspersoftWorkspace\INPEX_JasperReports\R10.XXX")
STAMP = ".backup_20260906_r10refresh"
APPLY = "--apply" in sys.argv

# All 19 R10 files verified IDENTICAL by _jr6-downgrade/test_all.py, 2026-09-06, against the
# final converter - and the same converter re-verified 21/21 IDENTICAL on R07, so the three
# extensions it needed for R10 (textAdjust, kind="break", band printWhenExpression) did not
# regress the already-deployed family.
JR6_OK = {"R10.001", "R10.002", "R10.003", "R10.006", "R10.007", "R10.008", "R10.009",
          "R10.010", "R10.011", "R10.012", "R10.026", "R10.029", "R10.030", "R10.031",
          "R10.034"}

reps = sorted(d for d in os.listdir(S) if d.startswith("R10.0"))
did7 = did6 = skip6 = 0
print("=== 7.0.3 workspace  ->  %s" % W7)
for rep in reps:
    out = os.path.join(S, rep, "output")
    if not os.path.isdir(out):
        continue
    for fn in sorted(f for f in os.listdir(out)
                     if f.endswith(".jrxml") and "backup" not in f):
        src, dst = os.path.join(out, fn), os.path.join(W7, fn)
        state = "new" if not os.path.exists(dst) else "overwrite (backed up)"
        print("   %-9s %-46s %s" % (rep, fn, state))
        if APPLY:
            os.makedirs(W7, exist_ok=True)
            if os.path.exists(dst) and not os.path.exists(dst + STAMP):
                shutil.copy2(dst, dst + STAMP)
            shutil.copy2(src, dst)
        did7 += 1

print("\n=== 6.17.0 workspace  ->  %s" % W6)
for rep in reps:
    jr6 = os.path.join(S, rep, "output", "jr6")
    if not os.path.isdir(jr6):
        print("   %-9s %-46s SKIP - no downgrade produced" % (rep, ""))
        skip6 += 1
        continue
    if rep not in JR6_OK:
        print("   %-9s %-46s SKIP - downgrade not verified IDENTICAL" % (rep, ""))
        skip6 += 1
        continue
    for fn in sorted(f for f in os.listdir(jr6)
                     if f.endswith("_jr6.jrxml") and "backup" not in f):
        tgt = fn[:-len("_jr6.jrxml")] + "_6_17.jrxml"
        src, dst = os.path.join(jr6, fn), os.path.join(W6, tgt)
        state = "new" if not os.path.exists(dst) else "overwrite (backed up)"
        print("   %-9s %-46s %s" % (rep, tgt, state))
        if APPLY:
            os.makedirs(W6, exist_ok=True)
            if os.path.exists(dst) and not os.path.exists(dst + STAMP):
                shutil.copy2(dst, dst + STAMP)
            shutil.copy2(src, dst)
        did6 += 1

print("\n%d file(s) -> 7.0.3 workspace, %d -> 6.17.0 workspace, %d report(s) skipped for 6.17%s"
      % (did7, did6, skip6, "" if APPLY else "   (report only - rerun with --apply)"))
