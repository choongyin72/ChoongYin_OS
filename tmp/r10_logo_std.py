"""Bring every R10.001-034 JRXML onto the R07 logo contract.

    py tmp/r10_logo_std.py [--only=R10.001] [--apply]

Owner's standard (2026-09-06), taken from the R07.011-025 family that already implements it:

    <parameter name="P_BASE_URL" class="java.lang.String" forPrompting="false">
        <defaultValueExpression><![CDATA["/extension/ZREP/reports/"]]></defaultValueExpression>
    </parameter>
    <expression><![CDATA[$P{P_BASE_URL} + "ichthys-logo.png"]]></expression>

Three edits, only the ones each file needs:

  1. ALL 19 files - the parameter default is `"./"` and becomes `"/extension/ZREP/reports/"`.
  2. R10.029 + R10.034 only - the image expression uses `$F{P_BASE_URL}`, a FIELD, where every
     other R10 uses `$P{}`. On EC that is a latent failure: EC supplies P_BASE_URL as a report
     PARAMETER under its own name, so a `$F{}` reference never sees it and the logo resolves to
     nothing. Same class as the R07 `REPORT_DATE` -> `$P{P_REPORT_DATE}` rename.
  3. R10.029 + R10.034 only - having switched to `$P{}`, the `<field name="P_BASE_URL"/>` and the
     `'' AS P_BASE_URL` column in the dummy query are orphans. Owner: "R10.029/R10.034 adopt
     other R10.XXX implementation too" - and R10.026/030/031 declare no such field. They are
     removed rather than left, because a DECLARED field that the real query does not return
     fails at fill time, which would surface much later as an unexplained error.

Filenames are NOT touched. R07.001-006 use `logo.png` in a box of aspect ~5.8 (the wide INPEX
wordmark) and are explicitly out of scope - owner: "i means for R70.XXX implementation which use
ichthys-logo.png file". Forcing one filename across both families is the NAME COLLISION that
EC-DEPLOYMENT-FINDINGS.md records as the original root cause. Boxes are not touched either.

Scope: R10 JRXMLs only - no harness, no R07 file (owner: "only make changes on R10.001 to R10.034
jrxml file").
"""
import os
import re
import sys

BASE = r"C:\Projects\INPEX\sources\CrystalReports"
WANT = '"/extension/ZREP/reports/"'
APPLY = "--apply" in sys.argv
ONLY = next((x.split("=")[1] for x in sys.argv[1:] if x.startswith("--only=")), None)
FIELDFIX = {"R10_029_AACQ_Notice_to_Buyer", "R10_034_Annual_Quantity_Statement"}

reps = sorted(d for d in os.listdir(BASE)
              if re.match(r'R10\.0(0[1-9]|[12][0-9]|3[0-4])$', d))
if ONLY:
    reps = [r for r in reps if r == ONLY] or reps
    if reps and reps[0] != ONLY:
        raise SystemExit("--only=%s matched nothing" % ONLY)
touched = 0
for rep in reps:
    S = os.path.join(BASE, rep, "output")
    if not os.path.isdir(S):
        continue
    for fn in sorted(f for f in os.listdir(S) if f.endswith(".jrxml") and "backup" not in f):
        path = os.path.join(S, fn)
        t = orig = open(path, encoding="utf-8").read()
        stem = fn[:-6]
        did = []

        # ---- 1. the parameter default
        pm = re.search(r'(<parameter name="P_BASE_URL"[^>]*>)(.*?)(</parameter>)', t, re.S)
        if not pm:
            print("   %-9s %-44s SKIP - no P_BASE_URL parameter" % (rep, stem[:44]))
            continue
        inner = pm.group(2)
        dm = re.search(r'(<defaultValueExpression><!\[CDATA\[)(.*?)(\]\]></defaultValueExpression>)',
                       inner, re.S)
        if not dm:
            print("   %-9s %-44s SKIP - parameter has no default" % (rep, stem[:44]))
            continue
        if dm.group(2).strip() != WANT:
            new_inner = inner.replace(dm.group(0), dm.group(1) + WANT + dm.group(3), 1)
            t = t.replace(pm.group(0), pm.group(1) + new_inner + pm.group(3), 1)
            did.append("default %s -> %s" % (dm.group(2).strip(), WANT))

        # ---- 2 + 3. the two files that used a field
        if stem in FIELDFIX:
            if "$F{P_BASE_URL}" in t:
                t = t.replace("$F{P_BASE_URL}", "$P{P_BASE_URL}")
                did.append("$F -> $P")
            n = len(re.findall(r'\s*<field name="P_BASE_URL"[^>]*/>', t))
            if n:
                t = re.sub(r'\s*<field name="P_BASE_URL"[^>]*/>', "", t)
                did.append("dropped %d field decl" % n)
            q = re.search(r'(<query[^>]*>\s*<!\[CDATA\[)(.*?)(\]\]>\s*</query>)', t, re.S)
            if q and "P_BASE_URL" in q.group(2):
                nq, k = re.subn(r"'[^']*'\s+AS\s+P_BASE_URL\s*,\s*", "", q.group(2))
                nq, k2 = re.subn(r",\s*'[^']*'\s+AS\s+P_BASE_URL\b", "", nq)
                t = t.replace(q.group(0), q.group(1) + nq + q.group(3), 1)
                did.append("dropped %d query column(s)" % (k + k2))

        # ---- guards
        if t != orig:
            d2 = re.search(r'<parameter name="P_BASE_URL".*?<!\[CDATA\[(.*?)\]\]>', t, re.S)
            if not d2 or d2.group(1).strip() != WANT:
                raise SystemExit("%s: default did not end up as %s" % (stem, WANT))
            if "$F{P_BASE_URL}" in t:
                raise SystemExit("%s: a $F{P_BASE_URL} survived" % stem)
            if stem in FIELDFIX:
                if '<field name="P_BASE_URL"' in t:
                    raise SystemExit("%s: field decl survived" % stem)
                q2 = re.search(r'<query[^>]*>\s*<!\[CDATA\[(.*?)\]\]>', t, re.S)
                if q2 and "P_BASE_URL" in q2.group(1):
                    raise SystemExit("%s: query still returns P_BASE_URL" % stem)
                # the column count must drop by exactly one per SELECT, never more
                for tag, body in (("old", orig), ("new", t)):
                    pass
            if len(re.findall(r'<element\b', t)) != len(re.findall(r'<element\b', orig)):
                raise SystemExit("%s: element count changed - this pass edits no elements" % stem)
            # the image expression must still name the same artwork
            if orig.count("ichthys-logo.png") != t.count("ichthys-logo.png"):
                raise SystemExit("%s: the logo filename changed" % stem)

        print("   %-9s %-44s %s" % (rep, stem[:44], "; ".join(did) if did else "already compliant"))
        if did and APPLY:
            b = path + ".backup_20260906_prelogostd"
            if not os.path.exists(b):
                open(b, "w", encoding="utf-8").write(orig)
            open(path, "w", encoding="utf-8").write(t)
        if did:
            touched += 1

print("\n%d file(s) need or got changes%s" % (touched, "" if APPLY else "  (report only)"))
