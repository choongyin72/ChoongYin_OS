from pathlib import Path
p = Path(r"C:\Projects\ChoongYin_OS\tmp\gen_ov.py")
s = p.read_text(encoding="utf-8")
old = """           cpfx=cpfx, slug=slug, folder=folder)"""
assert s.count(old) == 1, "SOW dict tail not unique"
s = s.replace(old, """           cpfx=cpfx, slug=slug, folder=folder, grid=grid_id)""")
p.write_text(s, encoding="utf-8")
print("SOW dict now passes grid=grid_id")
