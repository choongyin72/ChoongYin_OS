#!/usr/bin/env python3
"""ITEM 9 resolved. EC_KNOWN_ISSUES.md said the blocking child is removable "via the Chemical Usage Report
config screen". Checked against DefaultScreenTreeview: 1385 entries parsed, NO label contains
'chemical report' or 'chem usage'; the 6 'usage' screens are unrelated (Tank Usage CO.0038, Country /
Product / Node / Field Usage, Port Resource Usage Template). CHEM_USAGE_REPORT_CONF is CLASS_TYPE=TABLE
with no treeview screen. The remedy sentence pointed at a screen that does not exist."""
from pathlib import Path
p = Path(r"C:\Projects\ChoongYin_OS\ec-ui-knowledge\EC_KNOWN_ISSUES.md")
s = p.read_text(encoding="utf-8")
old = "via the Chemical Usage Report config screen"
assert s.count(old) == 1, "remedy phrase not found once (found %d)" % s.count(old)
new = ("**there is NO UI screen for it** - verified 2026-07-31 against `DefaultScreenTreeview` (1385 entries; "
       "no label matches 'chemical report'/'chem usage'; `CHEM_USAGE_REPORT_CONF` is CLASS_TYPE=TABLE with no "
       "treeview screen). An earlier version of this entry claimed a 'Chemical Usage Report config screen' - "
       "that screen does not exist. So the child can only be removed at DB level, which makes the UI delete "
       "path a genuine EC PRODUCT DEFECT (the UI also swallows the resulting ORA-02292/ORA-20102 - see above)")
s = s.replace(old, new)
p.write_text(s, encoding="utf-8")
print("EC_KNOWN_ISSUES.md remedy line corrected")

# and drop the now-settled UNCONFIRMED flag from the park doc
q = Path(r"C:\Projects\ChoongYin_OS\tmp\OV_SWEEP_PARKED.md")
t = q.read_text(encoding="utf-8")
old2 = "**One open discrepancy to resolve before anyone acts on the remedy**"
if old2 in t:
    i = t.index(old2)
    j = t.index("**Status: stays PARKED", i)
    t = t[:i] + ("**Discrepancy RESOLVED 2026-07-31:** KNOWN_ISSUES claimed a 'Chemical Usage Report config\n"
                 "screen'; there is none. Verified against DefaultScreenTreeview (1385 entries parsed, no\n"
                 "matching label) and class_cnfg (`CHEM_USAGE_REPORT_CONF` = TABLE, no screen). KNOWN_ISSUES\n"
                 "corrected. Consequence: the child is removable only at DB level, so the UI has NO delete path\n"
                 "at all - this strengthens the product-defect classification.\n\n") + t[j:]
    q.write_text(t, encoding="utf-8")
    print("park doc: UNCONFIRMED flag replaced with the resolved finding")
