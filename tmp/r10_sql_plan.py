"""Work out what R10 registration SQL would need, BEFORE generating any.

    py tmp/r10_sql_plan.py

Two things gen_report_sql.py had settled for R07 that are open for R10:

  1. THE 32-CHAR TEMPLATE_CODE CAP. R07's codes came from the jrxml stem uppercased, with
     seven hand-abbreviated because <NAME>_6_17 overflowed. R10's stems are much longer
     (R10_030_ADP_SDS_FOB_Buyers_ADP_per_buyer -> 40 chars before the suffix), so most will
     need abbreviating. Those abbreviations were owner-approved for R07, so they are proposed
     here rather than chosen silently.

  2. THE PARAMETER SET. R07's template registers three parameters - JRXML, REPORT_DATE, FORMAT.
     R10 reports declare many more (P_BASE_URL, P_CONTRACT_YEAR, P_DATE_OF_ISSUANCE...), all
     with defaults in the JRXML. Whether EC needs them registered is a real decision, not a
     detail: EC passes a registered parameter under its own name, and an unregistered one
     simply never arrives, leaving the JRXML default in place.

Read-only.
"""
import os
import re

SRC = r"C:\Projects\INPEX\sources\CrystalReports"
MAX_CODE = 32
SUFFIX = "_6_17"

# proposed short codes - only where the automatic one overflows. Kept readable and unique.
PROPOSED = {
    "R10_001_JCC_Price_Calculation": "R10_001_JCC_PRICE",
    "R10_002_Monthly_LNG_Contract_Price": "R10_002_MTH_LNG_PRICE",
    "R10_003_Monthly_LPG_Contract_Price": "R10_003_MTH_LPG_PRICE",
    "R10_006_LPG_Freight_Rate_Calculation": "R10_006_LPG_FREIGHT",
    "R10_007_Monthly_Plant_Condensate_Contract_Price": "R10_007_MTH_PC_PRICE",
    "R10_008_Plant_Condensate_MOPJ_PremDisc_Average": "R10_008_PC_MOPJ_AVG",
    "R10_009_Plant_Condensate_Freight_Rate_Calculation": "R10_009_PC_FREIGHT",
    "R10_010_LNG_Demurrage_EBC_Calculation": "R10_010_LNG_DEMURRAGE",
    "R10_011_LPG_Demurrage_Calculation": "R10_011_LPG_DEMURRAGE",
    "R10_012_Condensate_Demurrage_Calculation_FC": "R10_012_FC_DEMURRAGE",
    "R10_012_Condensate_Demurrage_Calculation_PC": "R10_012_PC_DEMURRAGE",
    "R10_026_Average_ACQ_Balance": "R10_026_AVG_ACQ_BAL",
    "R10_029_AACQ_Notice_to_Buyer": "R10_029_AACQ_NOTICE",
    "R10_030_ADP_SDS_FOB_Buyers_ADP_per_buyer": "R10_030_FOB_ADP_BUYER",
    "R10_030_ADP_SDS_FOB_Buyers_ADP_per_contract": "R10_030_FOB_ADP_CONTRACT",
    "R10_030_ADP_SDS_FOB_Buyers_SDS_per_buyer": "R10_030_FOB_SDS_BUYER",
    "R10_031_ADP_SDS_DES_Buyers_ADP": "R10_031_DES_ADP",
    "R10_031_ADP_SDS_DES_Buyers_SDS": "R10_031_DES_SDS",
    "R10_034_Annual_Quantity_Statement": "R10_034_ANNUAL_QTY_STMT",
}

rows = []
for rep in sorted(d for d in os.listdir(SRC) if re.match(r'R10\.0', d)):
    out = os.path.join(SRC, rep, "output")
    if not os.path.isdir(out):
        continue
    for fn in sorted(f for f in os.listdir(out)
                     if f.endswith(".jrxml") and "backup" not in f
                     and "variant" not in f.lower()):
        stem = fn[:-6]
        auto = (stem[:-7] if stem.endswith("_Report") else stem).upper()
        code = PROPOSED.get(stem, auto)
        rows.append((rep, stem, auto, code))

print("%-9s %-48s %-5s %-26s %s" % ("report", "jrxml stem", "auto", "proposed code", "len+_6_17"))
print("-" * 108)
over = []
for rep, stem, auto, code in rows:
    n = len(code) + len(SUFFIX)
    flag = "  OVER" if n > MAX_CODE else ""
    if n > MAX_CODE:
        over.append((stem, code, n))
    print("%-9s %-48s %-5d %-26s %2d%s"
          % (rep, stem[:48], len(auto) + len(SUFFIX), code, n, flag))

dups = {c for _r, _s, _a, c in rows if [x[3] for x in rows].count(c) > 1}
print("\n%d report file(s); %d proposed code(s) over the %d cap; %d duplicate code(s)"
      % (len(rows), len(over), MAX_CODE, len(dups)))
for s, c, n in over:
    print("   OVER  %-46s %s (%d)" % (s, c, n))
for d in sorted(dups):
    print("   DUP   %s" % d)

# ---- 2. what parameters do the R10 jrxmls actually declare?
print("\n=== parameters declared per report (forPrompting shown separately) ===")
allp = {}
for rep, stem, _a, _c in rows:
    p = os.path.join(SRC, rep, "output", stem + ".jrxml")
    t = open(p, encoding="utf-8", errors="replace").read()
    params = re.findall(r'<parameter name="(\w+)"([^>]*)>', t)
    prompt = [n for n, a in params if 'forPrompting="false"' not in a]
    print("   %-9s %-46s %2d param(s), %d forPrompting" % (rep, stem[:46], len(params), len(prompt)))
    for n, _a in params:
        allp[n] = allp.get(n, 0) + 1

print("\nparameters common to ALL %d report file(s):" % len(rows))
for n, c in sorted(allp.items()):
    if c == len(rows):
        print("   %s" % n)
print("\nR07's template registers exactly: JRXML, P_REPORT_DATE, FORMAT")
