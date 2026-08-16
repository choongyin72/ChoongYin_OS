#!/usr/bin/env python3
"""gen_ov.py hardcodes the DEFAULT grid id in its prose (SOW line 379, README line 389, driver docstring
line 47) while the actual grid comes from the config (`grid` key). Report Group's real grid is
`report_group_table:form:T_data`, so all three shipped a factually wrong id. Line 24 is the legitimate
default and stays. Found by READING THE GENERATED README back, not by reviewing the patch."""
from pathlib import Path
p = Path(r"C:\Projects\ChoongYin_OS\tmp\gen_ov.py")
s = p.read_text(encoding="utf-8")

# driver docstring
old = "PLAIN OV (Bank family, grid manage_object_nav_nav:form:T_data): navigator is date-only - no mandatory"
assert s.count(old) == 1
s = s.replace(old, "PLAIN OV (Bank family, grid %(grid)s): navigator is date-only - no mandatory")

# SOW
old = "- **Type:** PLAIN OV (Bank family; grid `manage_object_nav_nav:form:T_data`), date-only navigator + GO, date-effective."
assert s.count(old) == 1
s = s.replace(old, "- **Type:** PLAIN OV (Bank family; grid `%(grid)s`), date-only navigator + GO, date-effective.")

# README - also de-duplicate the two family sentences my earlier patch left side by side
old = """**Screen:** %(folder_h)s > %(screen)s (BF %(bf)s). PLAIN OV (grid `manage_object_nav_nav:form:T_data`), date-only navigator + GO,
date-effective. Plain-OV (Bank family) build: date-only navigator + GO, no cascade.
See `%(slug)s_sow.md` +"""
assert s.count(old) == 1
s = s.replace(old, """**Screen:** %(folder_h)s > %(screen)s (BF %(bf)s). PLAIN OV (Bank family, grid `%(grid)s`),
date-only navigator + GO (no cascade), date-effective. See `%(slug)s_sow.md` +""")
old = "''' % dict(screen=screen, folder_h=folder.replace(\"/\", \" > \"), bf=bf, slug=slug, folder=folder)"
assert s.count(old) == 1
s = s.replace(old, "''' % dict(screen=screen, folder_h=folder.replace(\"/\", \" > \"), bf=bf, slug=slug, folder=folder, grid=grid_id)")
p.write_text(s, encoding="utf-8")
print("gen_ov.py: 3 hardcoded grid ids -> config value")
