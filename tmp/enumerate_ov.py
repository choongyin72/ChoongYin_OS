"""Best-effort enumeration of OV (object) SCREENS in the treeview, split into: in-the-71 Bank-layout list
vs OTHER OV (beyond the 71). An OV screen = a treeview leaf whose label matches a CLASS_TYPE='OBJECT'
class label (class_property_cnfg LABEL -> class_cnfg). Read-only."""
import json, re
import oracledb
from pathlib import Path

c = oracledb.connect(user='ECKERNEL_EC', password='energy', dsn='localhost:1521/ORCL')
cur = c.cursor()

# 1) all OBJECT-class labels (the maintainable OV screens' names), + time scope for context
cur.execute("""select lower(p.property_value) lbl, c.time_scope_code
               from class_property_cnfg p join class_cnfg c on c.class_name=p.class_name
               where p.property_code='LABEL' and c.class_type='OBJECT'""")
ov_labels = {}
for lbl, ts in cur.fetchall():
    if lbl:
        ov_labels[lbl.strip()] = ts

# 2) treeview: every leaf screen (bf code + label + path)
cur.execute("select CONFIGURATION from TV_CTRL_CONFIGURATION_STORAGE where NAME='DefaultScreenTreeview'")
raw = cur.fetchone()[0]
if hasattr(raw, "read"):
    raw = raw.read()
c.close()
tv = json.loads(raw)
screens = []  # (bf, label, path)
def walk(n, path):
    lbl = n.get("label")
    np = path + ([lbl] if lbl else [])
    if n.get("screen"):
        screens.append((n.get("screen"), (lbl or "").strip(), " > ".join(path)))
    for ch in n.get("children", []) or []:
        if isinstance(ch, dict):
            walk(ch, np)
for r in tv["configuration"]["items"]:
    walk(r, [])

# 3) the 71 Bank-layout list = every BF code mentioned in the reuse-targets tracker
trk = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation\docs\ov-reuse-targets.md").read_text(encoding="utf-8")
the71 = set(re.findall(r"\b([A-Z]{2}\.\d{4})\b", trk))

# 4) classify treeview screens that are OV (label matches an OBJECT class)
ov_screens = []
seen = set()
for bf, lbl, path in screens:
    key = (bf, lbl.lower())
    if key in seen:
        continue
    seen.add(key)
    if lbl.lower() in ov_labels:
        ov_screens.append((bf, lbl, path, ov_labels[lbl.lower()]))

in71 = [s for s in ov_screens if s[0] in the71]
other = [s for s in ov_screens if s[0] not in the71]

print("=== OV screen enumeration (treeview leaves whose label = an OBJECT class) ===")
print("distinct treeview screens:", len({(b, l.lower()) for b, l, _ in screens}))
print("OV screens (label matches OBJECT class):", len(ov_screens))
print("  in the 71 Bank-layout tracker:", len(in71))
print("  OTHER OV (beyond the 71):", len(other))
print("\n=== OTHER OV screens (beyond the 71) - grouped by top-level path ===")
from collections import defaultdict
g = defaultdict(list)
for bf, lbl, path, ts in sorted(other, key=lambda x: (x[2], x[0])):
    top = " > ".join(path.split(" > ")[:3]) if path else "(root)"
    g[top].append("%s  %s [%s]" % (bf, lbl, ts))
for top in sorted(g):
    print("\n[%s]  (%d)" % (top, len(g[top])))
    for x in g[top]:
        print("   ", x)
Path(r"C:\Projects\ChoongYin_OS\tmp\ov_enum_result.json").write_text(
    json.dumps({"ov_total": len(ov_screens), "in71": len(in71), "other": len(other),
                "other_list": [{"bf": b, "label": l, "path": p, "time_scope": t} for b, l, p, t in other]}, indent=1),
    encoding="utf-8")
print("\nwrote tmp/ov_enum_result.json")
