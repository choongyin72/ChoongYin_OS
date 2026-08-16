"""Parse tmp/ov_gm_55_nav_recipe.xlsx -> per-screen navigator config. Cols A-F = #/BF/Screen/OV_view/Folder,
G.. = navigator fields (header row 1). Emits tmp/ov_gm_55_nav_config.json + a readable summary grouped by
navigator pattern (which nav fields each screen needs)."""
import json
from pathlib import Path
import openpyxl

wb = openpyxl.load_workbook(r"C:\Projects\ChoongYin_OS\tmp\ov_gm_55_nav_recipe.xlsx", data_only=True)
ws = wb.active
rows = list(ws.iter_rows(values_only=True))
hdr = [(str(c).strip() if c is not None else "") for c in rows[0]]
print("HEADERS:", [h for h in hdr if h])

# columns: find BF/Screen/OV_view/Folder by header; nav = everything after Folder
def col(name):
    for i, h in enumerate(hdr):
        if h.lower().startswith(name.lower()):
            return i
    return None
i_bf = col("BF"); i_scr = col("Screen"); i_view = col("OV"); i_fold = col("Folder")
nav_start = (i_fold + 1) if i_fold is not None else 6
nav_cols = [(i, hdr[i]) for i in range(nav_start, len(hdr)) if hdr[i]]

out = []
for r in rows[1:]:
    if not r or not r[i_bf]:
        continue
    bf = str(r[i_bf]).strip()
    scr = str(r[i_scr]).strip()
    nav = {}
    for i, h in nav_cols:
        v = r[i] if i < len(r) else None
        if v is not None and str(v).strip():
            nav[h] = str(v).strip()
    out.append({"bf": bf, "screen": scr,
                "view": (str(r[i_view]).strip() if r[i_view] else ""),
                "folder": (str(r[i_fold]).strip() if r[i_fold] else ""),
                "nav": nav})

Path(r"C:\Projects\ChoongYin_OS\tmp\ov_gm_55_nav_config.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
print("parsed screens:", len(out))
# group by nav-field signature
from collections import defaultdict
g = defaultdict(list)
for o in out:
    sig = " + ".join(o["nav"].keys()) if o["nav"] else "(no navigator)"
    g[sig].append("%s %s" % (o["bf"], o["screen"]))
print("\n=== navigator-pattern groups ===")
for sig in sorted(g, key=lambda k: -len(g[k])):
    print("\n[%s]  (%d)" % (sig, len(g[sig])))
    for x in g[sig]:
        print("   ", x)
print("\nwrote tmp/ov_gm_55_nav_config.json")
