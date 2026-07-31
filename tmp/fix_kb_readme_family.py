#!/usr/bin/env python3
"""Remaining wrong-family sites, found by grepping the REGENERATED bundle rather than trusting my first
patch (the 'enumerate ALL variants' lesson: I fixed 4 sites and there were 7).

 - packager KB template: the Selectors table hardcodes an OV-GM cascade row and grid
   `manageObject:form:T_data` (factually wrong on any non-OV-GM screen), the fields line always appends
   "Op Production Unit (first-available, grid visibility)", the Automation line always cites
   `apply_ovgm_navigator`, and the Quirks section is an OV-GM essay.
 - gen_ov.py README template: claims every screen is "Built on the item-1 gated-navigator capability
   (PR #244)" - untrue for plain-OV builds, which come from tmp/gen_ov.py.
"""
from pathlib import Path

# ---------------------------------------------------------------- packager KB template
p = Path(r"C:\Projects\ChoongYin_OS\tmp\package_ovgm.py")
s = p.read_text(encoding="utf-8")

old = "| Navigator (gated) | cascade `nav:form:G:0:R:1:C:1..N:dd` = %(nav)s (first-available) -> GO `#button:form:B` |\n| Grid | `manageObject:form:T_data` (empty until cascade + GO) |"
assert s.count(old) == 1, "KB selectors block not found"
s = s.replace(old, "| Navigator | %(kb_nav)s |\n| Grid | `%(kb_grid)s`%(kb_grid_note)s |")

old = "**%(code_l)s*** - **%(name_l)s*** - **Start Date*** (date)%(dd_note)s%(pp_note)s - Op Production Unit (first-available, grid visibility). (`*` mandatory)"
assert s.count(old) == 1, "KB fields line not found"
s = s.replace(old, "**%(code_l)s*** - **%(name_l)s*** - **Start Date*** (date)%(dd_note)s%(pp_note)s%(kb_oppu)s. (`*` mandatory)")

old = "- **Playwright:** `py/%(slug)s_iud.py` (shared engine `ec_object_iud.py` + `apply_ovgm_navigator`)."
assert s.count(old) == 1
s = s.replace(old, "- **Playwright:** `py/%(slug)s_iud.py` (shared engine `ec_object_iud.py`%(kb_engine)s).")

old = """## Quirks
- OV-GM navigator-gated: grid empty until cascade + GO. First-available nav PU is a sparse test scope - it is
  NOT necessarily a valid Op Production Unit option, and it empties nav-scoped popups (see issue OV_SWEEP_PARKED);
  parent-dd + Op PU use first-available, probe per screen.
'''"""
assert s.count(old) == 1, "KB quirks block not found"
s = s.replace(old, """## Quirks
%(kb_quirks)s
'''""")

old = """           code_l=code_l, name_l=name_l, dd_note=dd_note, pp_note=pp_note, slug=slug, folder=folder,
           rf_txt=rf_txt, pw_txt=pw_txt, fam_type=FAM_KB_TYPE[family])"""
assert s.count(old) == 1
s = s.replace(old, """           code_l=code_l, name_l=name_l, dd_note=dd_note, pp_note=pp_note, slug=slug, folder=folder,
           rf_txt=rf_txt, pw_txt=pw_txt, fam_type=FAM_KB_TYPE[family], kb_nav=KB_NAV[family],
           kb_grid=_grid, kb_grid_note=KB_GRID_NOTE[family], kb_oppu=KB_OPPU[family],
           kb_engine=KB_ENGINE[family], kb_quirks=KB_QUIRKS[family])""")

# family tables for the KB (placed next to the others in the prelude)
anchor = 'FAM_KB_TYPE = {'
assert s.count(anchor) == 1
tables = '''KB_NAV = {
    "ovgm": "cascade `nav:form:G:0:R:1:C:1..N:dd` (first-available) -> GO `#button:form:B`",
    "plain": "date field `nav:form:G:0:R:1:C:0:da_input` -> GO `#button:form:B` (no cascade)",
    "custom": "none - grid loads from the screen URL; re-query via toolbar Refresh `[Ctrl+r]`",
    "tv": "per-screen context/date navigator (see SOW)",
    "gatedpf": "PER-FIELD nav groups `nav:form:G:<n>:R:1:C:0` -> GO `#button:form:B`",
}
KB_GRID_NOTE = {"ovgm": " (empty until cascade + GO)", "plain": " (lists after GO)",
                "custom": " (lists on open)", "tv": "", "gatedpf": " (empty until all nav fields + GO)"}
KB_OPPU = {"ovgm": " - Op Production Unit (first-available, grid visibility)", "plain": "",
           "custom": "", "tv": "", "gatedpf": ""}
KB_ENGINE = {"ovgm": " + `apply_ovgm_navigator`", "plain": " + `click_go`", "custom": " + toolbar Refresh",
             "tv": "", "gatedpf": " + per-field nav helpers"}
KB_QUIRKS = {
    "ovgm": "- OV-GM navigator-gated: grid empty until cascade + GO. First-available nav PU is a sparse test\\n"
            "  scope - NOT necessarily a valid Op Production Unit option, and it empties nav-scoped popups\\n"
            "  (see tmp/OV_SWEEP_PARKED.md); parent-dd + Op PU use first-available, probe per screen.",
    "plain": "- Plain OV (Bank family): the navigator is a single DATE field + GO, no cascade and no Op PU.\\n"
             "- An UNSAVED CHANGES dialog (YES/NO) can block GO right after the End=Start close - answer YES\\n"
             "  (that commits the intended delete).",
    "custom": "- Custom-URL OV: no navigator GO; the toolbar Refresh `[Ctrl+r]` is the re-query gesture.",
    "tv": "- TV-style: rows are edited in place; confirm the delete gesture per screen.",
    "gatedpf": "- Every nav group is a separate mandatory field; fill them all before GO or the grid stays empty.",
}
''' + anchor
s = s.replace(anchor, tables)
p.write_text(s, encoding="utf-8")
print("packager KB template: family-aware nav/grid/fields/engine/quirks")

# ---------------------------------------------------------------- gen_ov.py README
g = Path(r"C:\Projects\ChoongYin_OS\tmp\gen_ov.py")
gs = g.read_text(encoding="utf-8")
old = "date-effective. Built on the item-1 gated-navigator capability (PR #244). See `%(slug)s_sow.md` +"
assert gs.count(old) == 1, "gen_ov README line not found"
gs = gs.replace(old, "date-effective. Plain-OV (Bank family) build: date-only navigator + GO, no cascade.\nSee `%(slug)s_sow.md` +")
g.write_text(gs, encoding="utf-8")
print("gen_ov.py README: dropped the false gated-navigator/PR #244 claim")
