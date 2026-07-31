#!/usr/bin/env python3
"""ov-non-bank-targets.md's 'Flavour' column is STALE and nearly mis-built Report Group.

It labels Report Group, Truck, Trailer and Driver as **OV-GM / manageObject:form:T_data** from the
2026-07-27 batch investigation. Truck/Trailer/Driver were subsequently SHIPPED as plain OV, proven live
(that mislabel is what issue #278 was about), and Report Group was proven plain OV today:
  - navigator = ONE visible date field `nav:form:G:0:R:1:C:0:da_input` + GO `button:form:B`
  - grid `report_group_table:form:T_data` (NOT manageObject:form:T_data)
  - verify_screen OVERALL PASS, LIVE RF 4/4 + Playwright 8/8
Left alone: Production Sub Unit, Facility Class 2, External Location - still unproven, so their rows now
carry an explicit warning instead of a silent claim.
"""
from pathlib import Path

p = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation\docs\ov-non-bank-targets.md")
s = p.read_text(encoding="utf-8")

PROVEN = {
    "CO.0158": ("Report Group", "**plain OV** (PROVEN live 2026-07-31)", "report_group_table:form:T_data",
                "**DONE** - verify_screen PASS (RF 4/4 + PW 8/8)"),
    "CO.0264": ("Truck", "**plain OV** (PROVEN live, shipped)", "manage_object_nav_nav:form:T_data",
                "**DONE #277**"),
    "CO.0265": ("Trailer", "**plain OV** (PROVEN live, shipped)", "manage_object_nav_nav:form:T_data",
                "**DONE #279**"),
    "CO.0266": ("Driver", "**plain OV** (PROVEN live, shipped)", "manage_object_nav_nav:form:T_data",
                "**DONE #281**"),
}
UNPROVEN = ("CO.0100", "CO.0021", "CO.0227")

changed = 0
out = []
for line in s.splitlines(keepends=True):
    bf = line.split("|")[1].strip() if line.startswith("|") and line.count("|") >= 5 else ""
    if bf in PROVEN and "**OV-GM**" in line:
        scr, flav, grid, phase = PROVEN[bf]
        out.append("| %s | %s | %s | %s | %s |\n" % (bf, scr, flav, grid, phase))
        changed += 1
        continue
    if bf in UNPROVEN and "**OV-GM**" in line and "UNVERIFIED" not in line:
        out.append(line.rstrip("\n").rstrip("|").rstrip() +
                   " -- **UNVERIFIED 2026-07-27 batch guess**; siblings in this block (Truck/Trailer/"
                   "Driver/Report Group) all turned out plain OV, so SCAN before building. |\n")
        changed += 1
        continue
    out.append(line)
s = "".join(out)

# the targets checklist row for Report Group
old = "| CO.0158 | Report Group | OV_REPORT_GROUP | Assets > Facility Objects | [ ] |"
assert s.count(old) == 1, "Report Group target row not found"
s = s.replace(old, "| CO.0158 | Report Group | OV_REPORT_GROUP | Assets > Facility Objects | [x] plain OV, live 4/4 |")
changed += 1

# a standing warning at the top of the flavour table so the column is never trusted blind again
anchor = "| BF | Screen | Flavour | grid_id | Phase |"
assert s.count(anchor) == 1
s = s.replace(anchor, "> WARNING: the 'Flavour' column below started as a 2026-07-27 BATCH GUESS. Four rows\n"
                      "> (Truck/Trailer/Driver/Report Group) were labelled OV-GM and proved to be plain OV on\n"
                      "> contact - issue #278 came from trusting it. Treat any row without 'PROVEN' as a\n"
                      "> hypothesis and SCAN the screen first.\n\n" + anchor)
changed += 1

p.write_text(s, encoding="utf-8")
print("ov-non-bank-targets.md: %d line(s) corrected" % changed)
assert changed == 9, "expected 9 edits (4 proven + 3 unproven-warned + 1 checkbox + 1 header), got %d" % changed
