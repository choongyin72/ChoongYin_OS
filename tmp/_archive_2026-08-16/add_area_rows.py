#!/usr/bin/env python3
"""TASK: Area (CO.0003) is BUILT but UNRECORDED - it has a T3, a suite and a Playwright driver that all
pass, yet 0 registry rows and no entry in screen_families.json. Consequences: the Group A count treated it
as unbuilt, and because the manifest drives hygiene's doc-row family gate, Area's rows were never checked.

NARROWEST POSSIBLE EDIT (the #287 lesson): append the three missing rows only. Do NOT run the full packager
- Area already has its own README/SOW/investigation/evidence, and regenerating would risk overwriting
content I did not write. No CHECKLIST/JOURNAL/KB is created here; that stays a separate decision.

Row text is taken from the VERIFY-REPORT this task just produced (OVERALL PASS: robocop 0, hygiene 0,
dryrun 4/4, LIVE RF 4/4 pass, Playwright 6/6), not from memory.
"""
import json
from pathlib import Path

R = Path(r"C:\Projects\ChoongYin_OS")
EC = R / "workstreams" / "master-plan" / "ec-automation"
DATE = "2026-08-01"

rpt = (EC / "screens/Configuration/Assets/Basic_Objects/Area/VERIFY-REPORT.md").read_text(encoding="utf-8")
assert "OVERALL: PASS" in rpt, "refusing to record rows for a screen whose report is not PASS"
assert "4/4 pass" in rpt and "6/6" in rpt, "expected RF 4/4 and PW 6/6 in the report"

reg = EC / "docs" / "ec_screen_registry.md"
sc = R / "docs" / "automation-scorecard.md"
man = EC / "docs" / "screen_families.json"

reg_txt = reg.read_text(encoding="utf-8")
sc_txt = sc.read_text(encoding="utf-8")
fams = json.loads(man.read_text(encoding="utf-8"))

changed = []

# ---- registry row (family-correct wording: Area IS OV-GM and DOES have Op PU) --------------------
if "| Area |" not in reg_txt:
    row = ("| Area | Configuration > Assets > Basic Objects > Area (CO.0003) | OV-GM (manage-object, "
           "groupmodel) verify_screen PASS %s - RF 4/4 pass + Playwright 6/6, DB-verified, self-clean; "
           "label-driven | `OV_AREA` (versioned) | Production Unit + GO | End Date = Start Date | "
           "`manageObject:form:T_data` | `pageobjects/Configuration/Assets/Basic_Objects/area_page.resource`;"
           " driver `screens/Configuration/Assets/Basic_Objects/Area/playwright/ec_iud_area.py` (mandatory "
           "Area Code/Area Name/Start Date + Op Production Unit = the navigator PU, which is REQUIRED here "
           "for the row to appear in the filtered grid) |\n")
    reg.write_text(reg_txt.rstrip("\n") + "\n" + row, encoding="utf-8")
    changed.append("registry")

# ---- scorecard row ------------------------------------------------------------------------------
if "| Area (" not in sc_txt:
    row = ("| Area (OV-GM, CO.0003) | OK Done %s - RF 4/4 pass + Playwright 6/6 via verify_screen.py "
           "(OVERALL PASS), DB-verified vs OV_AREA (Name), self-clean; OV-GM gated-navigator; label-driven;"
           " Op PU must EQUAL the navigator PU | see docs/ov-non-bank-targets.md |\n" % DATE)
    sc.write_text(sc_txt.rstrip("\n") + "\n" + row, encoding="utf-8")
    changed.append("scorecard")

# ---- manifest ------------------------------------------------------------------------------------
if "Area" not in fams:
    fams["Area"] = "ovgm"
    man.write_text(json.dumps(fams, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    changed.append("screen_families")

print("rows added: %s" % (changed or "none - already recorded"))
print("manifest screens now: %d" % len(fams))
