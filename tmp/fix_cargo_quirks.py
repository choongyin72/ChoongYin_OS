from pathlib import Path
p = Path(r"C:\Projects\ChoongYin_OS\ec-ui-knowledge\screens\cargo_planning_forecast.md")
s = p.read_text(encoding="utf-8")
old = """- OV-GM navigator-gated: grid empty until cascade + GO. First-available nav PU is a sparse test scope - it is
  NOT necessarily a valid Op Production Unit option, and it empties nav-scoped popups (see issue OV_SWEEP_PARKED);
  EC Transport layout:"""
assert s.count(old) == 1, "cargo quirks block not found (hand-edited shape)"
new = """- Gated OV with PER-FIELD navigator groups: every nav group is a SEPARATE mandatory field (not one
  cascade widget) - fill them all before GO or the grid stays empty.
- EC Transport layout:"""
s = s.replace(old, new)
p.write_text(s, encoding="utf-8")
print("cargo quirks corrected (hand-written EC Transport line preserved)")
