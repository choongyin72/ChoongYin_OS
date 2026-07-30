"""Split the 81 'other OV' (beyond the 71) into ALREADY-COVERED vs REMAINING, by checking whether each
screen's OV_ view (or slug) is referenced in pageobjects/ + tests/. Uses DB CLASS_TYPE=OBJECT (the same
Object/Data/Table classification the EC help text shows). Read-only."""
import json, re
from pathlib import Path
import oracledb

EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
other = json.load(open(r"C:\Projects\ChoongYin_OS\tmp\ov_enum_result.json", encoding="utf-8"))["other_list"]

# gather all RF/py automation text once
auto = ""
for sub in ("pageobjects", "tests", "py"):
    for f in (EC / sub).rglob("*"):
        if f.suffix in (".resource", ".robot", ".py"):
            try:
                auto += f.read_text(encoding="utf-8", errors="replace").upper()
            except Exception:
                pass

c = oracledb.connect(user='ECKERNEL_EC', password='energy', dsn='localhost:1521/ORCL')
cur = c.cursor()

def view_for(label):
    cur.execute("""select c.class_name from class_property_cnfg p join class_cnfg c on c.class_name=p.class_name
                   where p.property_code='LABEL' and lower(p.property_value)=:s and c.class_type='OBJECT'""", [label.lower()])
    for (cn,) in cur.fetchall():
        v = "OV_" + cn
        cur.execute("select 1 from all_views where view_name=:v", [v])
        if cur.fetchone():
            return v
    return None

covered, remaining = [], []
for o in other:
    v = view_for(o["label"])
    slug = re.sub(r"[^A-Z0-9]+", "_", o["label"].upper()).strip("_")
    is_cov = (v and re.search(r"\b" + re.escape(v) + r"\b", auto)) or (("%s_PAGE" % slug) in auto) or (("%s_IUD" % slug) in auto)
    rec = {"bf": o["bf"], "label": o["label"], "view": v, "path": o["path"]}
    (covered if is_cov else remaining).append(rec)
c.close()

print("OTHER OV beyond the 71 = %d  ->  already-covered %d | REMAINING %d" % (len(other), len(covered), len(remaining)))
print("\n=== ALREADY COVERED (not in the 71 tracker but automated historically) ===")
for r in sorted(covered, key=lambda x: x["bf"]):
    print("  %-9s %-28s %s" % (r["bf"], r["label"], r["view"]))
print("\n=== REMAINING OTHER OV (beyond 71, NOT yet automated) - by folder ===")
from collections import defaultdict
g = defaultdict(list)
for r in sorted(remaining, key=lambda x: (x["path"], x["bf"])):
    top = " > ".join(r["path"].split(" > ")[:4]) if r["path"] else "(root)"
    g[top].append("%-10s %-30s %s" % (r["bf"], r["label"], r["view"] or "(no OV_ view)"))
for top in sorted(g):
    print("\n[%s]  (%d)" % (top, len(g[top])))
    for x in g[top]:
        print("   ", x)
Path(r"C:\Projects\ChoongYin_OS\tmp\other_ov_remaining.json").write_text(
    json.dumps({"remaining": remaining, "covered": covered}, indent=1), encoding="utf-8")
print("\nwrote tmp/other_ov_remaining.json")
