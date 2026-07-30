"""Resolve Disposition Type's real treeview path from the DB treeview JSON (authoritative).
TV_CTRL_CONFIGURATION_STORAGE.CONFIGURATION where NAME='DefaultScreenTreeview'. READ-ONLY."""
import os, json, oracledb
con = oracledb.connect(user=os.environ.get("EC_DB_USER","ECKERNEL_EC"),
                       password=os.environ.get("EC_DB_PASS","energy"),
                       dsn=os.environ.get("EC_DB_DSN","localhost:1521/ORCL"))
cur = con.cursor()
cur.execute("select CONFIGURATION from TV_CTRL_CONFIGURATION_STORAGE where NAME='DefaultScreenTreeview'")
row = cur.fetchone()
raw = row[0]
if hasattr(raw, "read"): raw = raw.read()
con.close()
data = json.loads(raw)
LABEL_KEYS = ("text","label","name","title","caption","screenName","displayName")
CHILD_KEYS = ("children","items","nodes","childNodes","sub","subNodes","child")

def label_of(n):
    for k in LABEL_KEYS:
        if isinstance(n, dict) and isinstance(n.get(k), str):
            return n[k]
    return None

def children_of(n):
    for k in CHILD_KEYS:
        if isinstance(n, dict) and isinstance(n.get(k), list):
            return n[k]
    # some trees nest lists directly
    return []

hits = []
def walk(node, path):
    lbl = node.get("label")
    newpath = path + ([lbl] if lbl else [])
    if node.get("screen") == "CO.0208" or (lbl and lbl.strip().lower() == "disposition type"):
        hits.append((newpath, node.get("screen")))
    for c in node.get("children", []) or []:
        if isinstance(c, dict): walk(c, newpath)

for r in data["configuration"]["items"]:
    walk(r, [])
for path, scr in hits:
    print(f"PATH ({scr}): " + " > ".join(path))
if not hits:
    print("CO.0208 not found in treeview JSON")
