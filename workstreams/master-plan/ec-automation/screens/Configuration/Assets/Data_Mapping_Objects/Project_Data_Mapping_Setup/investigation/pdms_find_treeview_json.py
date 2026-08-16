import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[5] / "libraries"))
import DbVerify as db

conn = db._connect()
cur = conn.cursor()
cur.execute("SELECT CONFIGURATION FROM TV_CTRL_CONFIGURATION_STORAGE WHERE NAME = 'DefaultScreenTreeview'")
rows = cur.fetchall()
print("matching rows:", len(rows))
for r in rows:
    blob = r[0]
    text = blob.read() if hasattr(blob, "read") else blob
    if isinstance(text, bytes):
        text = text.decode("utf-8", errors="replace")
    for needle in ["manage_cost_mapping", "COST_MAPPING", "Project Data Mapping Setup"]:
        idx = text.find(needle)
        print(f"contains {needle!r} at index:", idx)
        if idx >= 0:
            print(text[max(0, idx-1000):idx+300])
            print("---")
cur.close()
conn.close()
