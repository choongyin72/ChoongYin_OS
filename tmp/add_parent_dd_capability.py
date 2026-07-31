#!/usr/bin/env python3
"""Message Group (CO.0236) exposed a MISSING generator capability, not a groupmodel-off screen.

Evidence: the insert PERSISTED (OV_MESSAGE_GROUP.code_present = True) but the grid never listed it, and
the persisted row's FUNCTIONAL_AREA_CODE was **ALLOCATION** while the navigator's first-available scope
was **Administration**. The form dropdown and the navigator offer DIFFERENT first options, so the row was
written into a scope the grid was not showing. `docs/ov-gm-navigator-capability.md` step 3 warns about
exactly this ("never assume the nav value is a valid parent-dd option"), and the generator already
CAPTURES the navigator's top-parent - as `pu` in the driver and `${GM_PU}` in the T3 - but never USES it.
Half-built machinery.

This adds the missing half: config key `parent_dd` = the form dropdown label that must be set to the
CAPTURED navigator value rather than to __FIRST__.
"""
from pathlib import Path

p = Path(r"C:\Projects\ChoongYin_OS\tmp\gen_ovgm.py")
s = p.read_text(encoding="utf-8")

# ---- parse the new key --------------------------------------------------------------------------
anchor = 'extra_dd = a.get("extra_dropdowns", []); has_op_pu = a.get("has_op_pu", True)'
assert s.count(anchor) == 1, "extra_dd parse line not found"
s = s.replace(anchor, anchor + '''
# parent_dd: the objectForm dropdown that MUST equal the navigator's captured top-parent, or the new row
# lands outside the scope the grid is showing (Message Group: nav first = 'Administration' but the form's
# first = 'ALLOCATION' -> insert persisted, grid never listed it). Do NOT also list it in
# extra_dropdowns, or it gets set twice (second write wins, __FIRST__ would clobber the scope).
parent_dd = a.get("parent_dd", "")
assert parent_dd not in extra_dd, ("parent_dd %r must not also appear in extra_dropdowns - it would be "
                                   "overwritten with __FIRST__" % parent_dd)''')

# ---- driver: bind to the captured `pu` variable (NOT a literal) ---------------------------------
anchor = '''if has_op_pu:
    ins.append('                {"label": "Op Production Unit", "value": "__FIRST__", "kind": "dropdown"},')'''
assert s.count(anchor) == 1, "driver op-pu block not found"
s = s.replace(anchor, anchor + '''
if parent_dd:
    # value is the runtime variable `pu`, deliberately unquoted - insert_fields is built AFTER
    # apply_ovgm_navigator() returns, so the captured top-parent is in scope here.
    ins.append('                {"label": %r, "value": pu, "kind": "dropdown"},' % parent_dd)''')

# ---- T3: use ${GM_PU} ---------------------------------------------------------------------------
anchor = '''if has_op_pu:
    t3_ins.append("    Fill OV Dropdown By Label    objectForm    Op Production Unit    __FIRST__")'''
assert s.count(anchor) == 1, "t3 op-pu block not found"
s = s.replace(anchor, anchor + '''
if parent_dd:
    t3_ins.append("    Fill OV Dropdown By Label    objectForm    %s    ${GM_PU}" % parent_dd)''')

# ---- document the key in the usage docstring ----------------------------------------------------
anchor = "             has_op_pu (bool: set Op Production Unit first-available for grid visibility)"
assert s.count(anchor) == 1
s = s.replace(anchor, anchor + "\n             parent_dd (label of the form dd that must EQUAL the "
                               "navigator's captured top-parent)")

p.write_text(s, encoding="utf-8")
print("gen_ovgm.py: parent_dd capability added (driver binds `pu`, T3 binds ${GM_PU})")
