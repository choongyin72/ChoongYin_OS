"""Type-audit the OV reuse tracker vs DB ground truth (CLASS_TYPE): OBJECT=OV, TABLE=TV.
Reads each uncovered note's URL CLASS_NAME, queries class_cnfg. READ-ONLY. tmp scratch."""
import os, re, glob
import oracledb
from pathlib import Path

NOTES = Path(r"C:\Projects\ChoongYin_OS\DeepDiveLearnings\ec-screens\notes")
# uncovered BF_CODEs from ov-reuse-targets.md (excl. done Disposition Type CO.0208, Report Area RP.0017)
BFCODES = ["CD.0013","CD.0015","CD.0016","CD.0017","CD.0035","CD.0097","CD.0099","CD.0115","CD.0135",
           "CO.0072","CO.0089","CO.0091","CO.0120","CO.0133","CO.0135","CO.0137","CO.0149","CO.0185",
           "CO.0217","CO.0219","CO.0245","CO.0257","CO.1059","CO.1063","CO.2003","CO.2012","CO.2069",
           "CO.2091","IN.0023","IN.0031","IN.0033","SP.0043","SP.0049",
           "CO.0208","RP.0017"]  # last 2 = done, for confirmation

con = oracledb.connect(user=os.environ.get("EC_DB_USER","ECKERNEL_EC"),
                       password=os.environ.get("EC_DB_PASS","energy"),
                       dsn=os.environ.get("EC_DB_DSN","localhost:1521/ORCL"))
cur = con.cursor()

def class_type(cls):
    try:
        cur.execute("select class_type from class_cnfg where class_name=:c", c=cls)
        r = cur.fetchone()
        return r[0] if r else "(not in class_cnfg)"
    except Exception as e:
        return "ERR " + repr(e)[:40]

def view_exists(v):
    cur.execute("select count(*) from all_views where view_name=:v", v=v)
    return cur.fetchone()[0] > 0

print(f"{'BF_CODE':<9} {'CLASS':<26} {'CLASS_TYPE':<14} {'OV_view':<8} {'TV_view':<8} name")
ov, tv, other = [], [], []
for bf in BFCODES:
    note = NOTES / (bf + ".md")
    if not note.exists():
        print(f"{bf:<9} (no note)"); continue
    txt = note.read_text(encoding="utf-8", errors="ignore")
    title = txt.splitlines()[0].lstrip("# ").strip()
    m = re.search(r"/CLASS_NAME/([A-Z0-9_]+)", txt) or re.search(r"`([A-Z0-9_]+)`\s*\|\s*(OBJECT|TABLE)", txt)
    cls = m.group(1) if m else "?"
    ct = class_type(cls) if cls != "?" else "?"
    ovv = view_exists("OV_" + cls) if cls != "?" else False
    tvv = view_exists("TV_" + cls) if cls != "?" else False
    tag = "OV" if ct == "OBJECT" else "TV" if ct == "TABLE" else "?"
    (ov if tag=="OV" else tv if tag=="TV" else other).append(bf)
    print(f"{bf:<9} {cls:<26} {ct:<14} {str(ovv):<8} {str(tvv):<8} {title[:40]}")
con.close()
print(f"\nSUMMARY: OBJECT/OV={len(ov)}  TABLE/TV={len(tv)}  other/unknown={len(other)}")
print("TV (misclassified as OV -> move out):", tv)
print("unknown:", other)
