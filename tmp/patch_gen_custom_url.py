"""Patch gen_ov_screen.py to support custom-URL OV screens: grid_id param (default manage-object),
Save And Refresh List reload (GO-or-Refresh), Refresh-on-open for custom-URL."""
p = r"C:\Projects\ChoongYin_OS\tmp\gen_ov_screen.py"
s = open(p, encoding="utf-8").read()
orig = s

# 1) compute grid_id / custom-url / open-reload just after slug is read
s = s.replace(
    'slug = c["slug"]',
    'slug = c["slug"]\n'
    'grid_id = c.get("grid_id", "manage_object_nav_nav:form:T_data")\n'
    '_custom_url = grid_id != "manage_object_nav_nav:form:T_data"\n'
    'open_reload = ("    Refresh Screen    # custom-URL OV: no GO; grid loads on open, toolbar Refresh after writes"\n'
    '               if _custom_url else "    Apply Navigator    # grid needs GO to populate (no default rows on open)")',
    1)

# 2) T3: declare a per-screen grid variable (default = the manage-object literal -> backward compatible)
s = s.replace('${{SCREEN_NAME}}          {screen}\n',
              '${{SCREEN_NAME}}          {screen}\n${{SCREEN_GRID}}          {grid_id}\n', 1)

# 3) T3 body: use ${SCREEN_GRID} instead of the hardcoded shared const
s = s.replace('${{OV_MANAGE_OBJECT_TABLE}}', '${{SCREEN_GRID}}')

# 4) Open keyword: GO for manage-object, Refresh for custom-URL
s = s.replace('    Apply Navigator    # grid needs GO to populate (no default rows on open)', '{open_reload}')

# 5) reload after writes: Save + (GO or Refresh) via the existing T2 keyword (3 occurrences: insert/update/delete)
s = s.replace('    Save\n    Apply Navigator', '    Save And Refresh List')

# 6) driver grid id from config
s = s.replace('GRID_DATA_ID  = "manage_object_nav_nav:form:T_data"', 'GRID_DATA_ID  = "{grid_id}"')

assert s != orig, "no changes applied - anchors not found"
open(p, "w", encoding="utf-8").write(s)
print("patched gen_ov_screen.py for custom-URL OV")
for probe in ('grid_id = c.get(', '${{SCREEN_GRID}}', '{open_reload}', 'Save And Refresh List', 'GRID_DATA_ID  = "{grid_id}"'):
    print("  present:", probe, "->", probe in s)
