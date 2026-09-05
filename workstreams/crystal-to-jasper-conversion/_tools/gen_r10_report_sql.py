"""Generate EC report-registration SQL for the R10 reports, cloned from the R07.016 pair.

    py tmp/gen_r10_report_sql.py            # dry run -> tmp/_r10sql_preview/
    py tmp/gen_r10_report_sql.py --apply    # write into sources/SQLs

Two files per report file, exactly as gen_report_sql.py does for R07:

    <CODE>.sql      from R07_016_PC_LIFTING.sql     REPORT_SYSTEM_CODE=JASPER     code=<BASE>_6_17
    <CODE>_V7.sql   from R07_016_PC_LIFTING_V7.sql  REPORT_SYSTEM_CODE=JASPER_V7  code=<BASE>

R07.016 is the reference the owner named, and it is the right one: it is a GENERATED pair, so it
already carries the three things the hand-written R07.012 original lacks - distinct TEMPLATE_CODEs
per engine (so both registrations coexist instead of deleting each other), _6_17 on the 6.17
artifact paths, and P_REPORT_DATE rather than the unprefixed REPORT_DATE.

THE _6_17 SUFFIX IS ON THE TEMPLATE_CODE, not only on the filename or the artifact path. Every one
of the 24 code literals in the 6.17 script carries it. Owner: "for downgraded jrxml, its
template_code need to include _6_17".

TEMPLATE_CODE is capped at 32 characters. Sizing is done against <BASE>_6_17, the longer of the
pair, so if that fits both do. Every R10 stem uppercased overflows on its own (32-54 chars), so
all 19 use an explicit short code - the R07 abbreviations were owner-approved and these are too.

PARAMETERS. All three of R07.016's template parameters are kept: JRXML, P_REPORT_DATE and
FORMAT. An earlier version of this script DROPPED the P_REPORT_DATE block, reasoning that no R10
report declares that parameter (true - checked all 19) and that registering it would put an
unread parameter in EC's run dialog. Owner: "its missing the P_REPORT_DATE scripts where
R07_016_PC_LIFTING.sql did contains it". The template is the specification here; the registration
is not required to mirror only what today's layout-only JRXML happens to consume, and the real
queries are still to come. Match the template, do not optimise it.

Sources are never modified. Output is fully reproducible by re-running.
"""
import os
import re
import sys

SRC = r"C:\Projects\INPEX\sources\CrystalReports"
SQL = r"C:\Projects\INPEX\sources\SQLs"
PREVIEW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_r10sql_preview")
BASE_617 = os.path.join(SQL, "R07_016_PC_LIFTING.sql")
BASE_V7 = os.path.join(SQL, "R07_016_PC_LIFTING_V7.sql")
APPLY = "--apply" in sys.argv
DEST = SQL if APPLY else PREVIEW
MAX_CODE = 32

OLD_CODE_617 = "R07_016_PC_LIFTING_6_17"
OLD_CODE_V7 = "R07_016_PC_LIFTING"
OLD_STEM = "R07_016_PC_Lifting_Report"

# One short code per report FILE. Sized so <CODE>_6_17 fits the 32-char cap, and unique.
CODE = {
    "R10_001_JCC_Price_Calculation":                     "R10_001_JCC_PRICE",
    "R10_002_Monthly_LNG_Contract_Price":                "R10_002_MTH_LNG_PRICE",
    "R10_003_Monthly_LPG_Contract_Price":                "R10_003_MTH_LPG_PRICE",
    "R10_006_LPG_Freight_Rate_Calculation":              "R10_006_LPG_FREIGHT",
    "R10_007_Monthly_Plant_Condensate_Contract_Price":   "R10_007_MTH_PC_PRICE",
    "R10_008_Plant_Condensate_MOPJ_PremDisc_Average":    "R10_008_PC_MOPJ_AVG",
    "R10_009_Plant_Condensate_Freight_Rate_Calculation": "R10_009_PC_FREIGHT",
    "R10_010_LNG_Demurrage_EBC_Calculation":             "R10_010_LNG_DEMURRAGE",
    "R10_011_LPG_Demurrage_Calculation":                 "R10_011_LPG_DEMURRAGE",
    "R10_012_Condensate_Demurrage_Calculation_FC":       "R10_012_FC_DEMURRAGE",
    "R10_012_Condensate_Demurrage_Calculation_PC":       "R10_012_PC_DEMURRAGE",
    "R10_026_Average_ACQ_Balance":                       "R10_026_AVG_ACQ_BAL",
    "R10_029_AACQ_Notice_to_Buyer":                      "R10_029_AACQ_NOTICE",
    "R10_030_ADP_SDS_FOB_Buyers_ADP_per_buyer":          "R10_030_FOB_ADP_BUYER",
    "R10_030_ADP_SDS_FOB_Buyers_ADP_per_contract":       "R10_030_FOB_ADP_CONTRACT",
    "R10_030_ADP_SDS_FOB_Buyers_SDS_per_buyer":          "R10_030_FOB_SDS_BUYER",
    "R10_031_ADP_SDS_DES_Buyers_ADP":                    "R10_031_DES_ADP",
    "R10_031_ADP_SDS_DES_Buyers_SDS":                    "R10_031_DES_SDS",
    "R10_034_Annual_Quantity_Statement":                 "R10_034_ANNUAL_QTY_STMT",
}



def build(base, out, code, old_code, stem, jasper_stem, label):
    t = open(base, encoding="utf-8").read()
    # paths first: they spell the stem in mixed case, which the CODE literal does not match
    for ext in ("jasper", "jrxml"):
        t = t.replace(f"{OLD_STEM}_6_17.{ext}", f"{jasper_stem}.{ext}")
        t = t.replace(f"{OLD_STEM}.{ext}", f"{jasper_stem}.{ext}")
    t = t.replace(f"{OLD_STEM} (Template", f"{stem} (Template")
    t = t.replace(old_code, code)

    # P_REPORT_DATE is KEPT, exactly as the template has it - it must survive, so it is
    # asserted present rather than listed as a leftover to reject.
    if t.count("'P_REPORT_DATE'") != 1:
        raise SystemExit(f"{out}: expected 1 'P_REPORT_DATE', found {t.count(chr(39) + 'P_REPORT_DATE' + chr(39))}")
    for leftover in ("R07_016", "R07.016", "PC_LIFTING", "PC_Lifting"):
        if leftover in t:
            raise SystemExit(f"{out}: {leftover!r} survived substitution")
    if f"'{code}'" not in t:
        raise SystemExit(f"{out}: the new code never appears")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(t)
    return t.count(f"'{code}'")


rows = []
for rep in sorted(d for d in os.listdir(SRC) if re.match(r'R10\.0', d)):
    o = os.path.join(SRC, rep, "output")
    if not os.path.isdir(o):
        continue
    for fn in sorted(f for f in os.listdir(o) if f.endswith(".jrxml")
                     and "backup" not in f and "variant" not in f.lower()):
        rows.append((rep, fn[:-6]))

print("writing to %s%s\n" % (DEST, "" if APPLY else "   (DRY RUN)"))
print("%-9s %-30s %-6s %-30s %s" % ("report", "TEMPLATE_CODE (V7)", "len", "6.17 code", "len"))
print("-" * 92)
seen = {}
for rep, stem in rows:
    if stem not in CODE:
        raise SystemExit(f"{stem}: no short code defined")
    base = CODE[stem]
    c617, cv7 = base + "_6_17", base
    for c in (c617, cv7):
        if len(c) > MAX_CODE:
            raise SystemExit(f"{stem}: code {c} is {len(c)} chars, over {MAX_CODE}")
        if c in seen:
            raise SystemExit(f"{stem}: code {c} already used by {seen[c]}")
        seen[c] = stem
    n1 = build(BASE_617, os.path.join(DEST, base + ".sql"), c617, OLD_CODE_617,
               stem, stem + "_6_17", "6.17")
    n2 = build(BASE_V7, os.path.join(DEST, base + "_V7.sql"), cv7, OLD_CODE_V7,
               stem, stem, "V7")
    print("%-9s %-30s %-6d %-30s %d" % (rep, cv7, len(cv7), c617, len(c617)))

print("\n%d report file(s) -> %d sql file(s)%s"
      % (len(rows), len(rows) * 2, "" if APPLY else "   (dry run - rerun with --apply)"))
