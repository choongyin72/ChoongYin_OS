from pathlib import Path
p = Path(r"C:\Projects\ChoongYin_OS\tmp\package_ovgm.py")
s = p.read_text(encoding="utf-8")
old = 'FAM_GRID_TXT = {"ovgm": "OV-GM (grid `manageObject:form:T_data`)",'
assert s.count(old) == 1
new = ('''# grid_txt/nav_txt are LOCAL to the registry-row function, so recompute them here from the same
# module-level family tables (single source of truth, no second guess at the values).
_grid = FAM_TEXT[family][1] or a.get("grid", "manage_object_nav_nav:form:T_data")
nav_txt = ((" -> ".join(nav) + " cascade + GO") if family in ("ovgm", "gatedpf")
           else FAM_NAV_TXT.get(family, "see SOW"))
''' + old)
s = s.replace(old, new)
s = s.replace('"plain": "plain OV (Bank family, grid `%s`)" % grid_txt,',
              '"plain": "plain OV (Bank family, grid `%s`)" % _grid,')
s = s.replace('"custom": "custom-URL OV (grid `%s`)" % grid_txt,',
              '"custom": "custom-URL OV (grid `%s`)" % _grid,')
s = s.replace('"tv": "TV-style inline grid (`%s`)" % grid_txt,',
              '"tv": "TV-style inline grid (`%s`)" % _grid,')
s = s.replace('"gatedpf": "gated OV, per-field nav groups (grid `%s`)" % grid_txt}',
              '"gatedpf": "gated OV, per-field nav groups (grid `%s`)" % _grid}')
assert "grid_txt`" not in s and "% grid_txt" not in s.split("def ")[0], "a grid_txt ref remains at module level"
p.write_text(s, encoding="utf-8")
print("prelude now uses module-level _grid / nav_txt")
