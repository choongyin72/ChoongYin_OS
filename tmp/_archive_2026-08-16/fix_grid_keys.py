from pathlib import Path
import re
p = Path(r"C:\Projects\ChoongYin_OS\tmp\gen_ov.py")
s = p.read_text(encoding="utf-8")
# driver template exposes grid_id, not grid
old = "PLAIN OV (Bank family, grid %(grid)s): navigator is date-only - no mandatory"
assert s.count(old) == 1
s = s.replace(old, "PLAIN OV (Bank family, grid %(grid_id)s): navigator is date-only - no mandatory")
p.write_text(s, encoding="utf-8")
# what does the SOW template's dict expose?
m = re.search(r"sow = '''.*?''' % dict\((.*?)\)\n", s, re.S)
print("SOW dict args:", (m.group(1)[:300] if m else "NOT FOUND"))
print("grid in SOW dict:", bool(m and re.search(r"\bgrid\s*=", m.group(1))))
