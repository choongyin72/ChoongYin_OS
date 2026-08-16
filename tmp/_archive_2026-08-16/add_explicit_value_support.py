#!/usr/bin/env python3
"""ITEM 2 prerequisite: gen_ovgm.py can only ever pick __FIRST__ and always runs the navigator cascade with
levels=4. Service (CO.2103) cannot be built that way, for reasons established by read-only recon:

 - its navigator C:3 exists with ZERO options for the first-available BU, so levels=4 raises
   RuntimeError("dropdown has no options");
 - OV_SERVICE has no business-unit column - a row's scope comes from CONTRACT_ID - and the alphabetically
   first BU ('EC LNG Norway') owns no contracts at all, while all 43 existing rows sit under BU TS3_BU1.
   First-available everywhere therefore saves a row that NEVER lists in the grid (how Message Group failed);
 - reference dropdowns only offer objects effective at the form's START DATE, so 2000-01-01 must be
   overridable (this cost me a false 'engine defect' on Area earlier today).

Three opt-in, backwards-compatible config keys, wired in BOTH layers (Playwright driver + RF T3/suite):
   nav_value   - select this exact value in navigator C:1 instead of first-available (+ Apply Navigator)
   nav_levels  - cap the cascade (default 4, unchanged)
   start_date  - override the form start date (default 2000-01-01, unchanged)
plus extra_dropdowns entries may now be ["Label", "Value"] pairs as well as plain "Label" (= __FIRST__).

Existing configs pass none of these, so their output must be byte-identical - asserted by regenerating a
shipped screen after the patch.
"""
from pathlib import Path

p = Path(r"C:\Projects\ChoongYin_OS\tmp\gen_ovgm.py")
s = p.read_text(encoding="utf-8")

# ---------------------------------------------------------------- 1. parse the new keys + normalise pairs
anchor = 'popups = a.get("popups", [])'
assert s.count(anchor) == 1, "popups parse line not found"
s = s.replace(anchor, '''nav_value = a.get("nav_value", "")      # explicit navigator C:1 value (else first-available)
nav_levels = int(a.get("nav_levels", 4))  # cap the cascade; Service's C:3 is present but empty
start_date = a.get("start_date", "2000-01-01")   # ref dropdowns only offer objects effective at this date
NAV_DD = "nav:form:G:0:R:1:C:1:dd"      # C:1 = the first cascade level (C:0 is the Date field)
# extra_dropdowns: "Label" (=> __FIRST__) or ["Label", "Value"] for a value that MUST be exact
extra_dd_pairs = [(d, "__FIRST__") if isinstance(d, str) else (d[0], d[1]) for d in extra_dd]
extra_dd_labels = [lbl for lbl, _ in extra_dd_pairs]
''' + anchor)

# parent_dd's assert must compare against the LABELS now, not raw entries
old = 'assert parent_dd not in extra_dd, ('
assert s.count(old) == 1
s = s.replace(old, 'assert parent_dd not in [d if isinstance(d, str) else d[0] for d in extra_dd], (')

# ---------------------------------------------------------------- 2. driver: insert fields use pair values
old = """for d in extra_dd:
    ins.append('                {"label": %r, "value": "__FIRST__", "kind": "dropdown"},' % d)"""
assert s.count(old) == 1, "driver extra_dd loop not found"
s = s.replace(old, """for _lbl, _val in extra_dd_pairs:
    ins.append('                {"label": %r, "value": %r, "kind": "dropdown"},' % (_lbl, _val))""")

# ---------------------------------------------------------------- 3. driver: navigator + start date
old = "START_DATE    = \"2000-01-01\""
assert s.count(old) == 1, "driver START_DATE not found"
s = s.replace(old, "START_DATE    = \"%(start_date)s\"")

old = """            pu = ec.apply_ovgm_navigator(page)
            results["nav_pu"] = "PASS: PU=%%r" %% pu"""
assert s.count(old) == 1, "driver navigator call not found"
s = s.replace(old, """%(nav_block)s
            results["nav_pu"] = "PASS: PU=%%r" %% pu""")

# ---------------------------------------------------------------- 4. T3: extra_dd + explicit nav
old = """for d in extra_dd:
    t3_ins.append("    Fill OV Dropdown By Label    objectForm    %s    __FIRST__" % d)"""
assert s.count(old) == 1, "t3 extra_dd loop not found"
s = s.replace(old, """for _lbl, _val in extra_dd_pairs:
    t3_ins.append("    Fill OV Dropdown By Label    objectForm    %s    %s" % (_lbl, _val))""")

old = """    Launch EC And Open Screen    ${SCR}    ${user}    ${pass}
    ${pu}=    Apply OV-GM Navigator First Available
    RETURN    ${pu}"""
assert s.count(old) == 1, "t3 open-screen body not found"
s = s.replace(old, """    Launch EC And Open Screen    ${SCR}    ${user}    ${pass}
%(t3_nav_block)s
    RETURN    ${pu}""")

old = "${GM_PU}            ${EMPTY}"
assert s.count(old) == 1
s = s.replace(old, "${GM_PU}            ${EMPTY}\n${NAV_DD}            " + "%(nav_dd)s")

# ---------------------------------------------------------------- 5. suite start date
old = "${START_DATE}       2000-01-01"
assert s.count(old) == 1, "suite START_DATE not found"
s = s.replace(old, "${START_DATE}       %(start_date)s")

# ---------------------------------------------------------------- 6. build the two nav blocks + feed dicts
anchor = "driver = '''"
assert s.count(anchor) == 1
blocks = '''# navigator blocks - explicit value (Area's proven pattern: Select option -> Apply Navigator) or the
# existing first-available cascade. `pu` must end up holding the top-parent either way, because parent_dd
# and the grid-visibility checks depend on it.
if nav_value:
    nav_block = ('            ec.select_dropdown(page, "%s_input", %r)\\n'
                 '            ec.click_go(page)\\n'
                 '            pu = %r' % (NAV_DD, nav_value, nav_value))
    t3_nav_block = ('    Select EC Dropdown Option    ${NAV_DD}    %s\\n'
                    '    Apply Navigator\\n'
                    '    ${pu}=    Set Variable    %s' % (nav_value, nav_value))
else:
    nav_block = "            pu = ec.apply_ovgm_navigator(page%s)" % (
        "" if nav_levels == 4 else ", levels=%d" % nav_levels)
    t3_nav_block = "    ${pu}=    Apply OV-GM Navigator First Available"

''' + anchor
s = s.replace(anchor, blocks)

# add the new keys to every template dict that now references them
for key, val in (("nav_block", "nav_block"), ("start_date", "start_date"),
                 ("t3_nav_block", "t3_nav_block"), ("nav_dd", "NAV_DD")):
    pass   # handled below in one pass per template

import re as _re


def add_keys(match):
    body = match.group(1)
    for k, v in (("nav_block", "nav_block"), ("start_date", "start_date"),
                 ("t3_nav_block", "t3_nav_block"), ("nav_dd", "NAV_DD")):
        if "%s=" % k not in body:
            body += ", %s=%s" % (k, v)
    return "''' %% dict(%s)\n" % body


s = _re.sub(r"''' % dict\((.*?)\)\n", add_keys, s, flags=_re.S)

p.write_text(s, encoding="utf-8")
print("gen_ovgm.py: nav_value / nav_levels / start_date + explicit extra_dropdown values wired in")
