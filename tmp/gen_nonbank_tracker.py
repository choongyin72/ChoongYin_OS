"""Generate ov-non-bank-targets.md (the 55 OV-GM screens beyond the 71) from the parsed nav recipe,
grouped by navigator pattern, with a Status column. Marks screens already delivered as [x]."""
import json
from pathlib import Path
from collections import defaultdict

cfg = json.load(open(r"C:\Projects\ChoongYin_OS\tmp\ov_gm_55_nav_config.json", encoding="utf-8"))
DONE = {"CO.1049": "Conversion Group #TBD (custom-URL OV)"}   # updated as screens ship

def group(nav):
    keys = list(nav.keys())
    if not keys: return "A. No navigator (manage-object no-cascade OR custom-URL)"
    s = set(keys)
    if s == {"Business Unit"}: return "C1. Business Unit only"
    if "Contract Area" in s: return "C2. Business Unit + Contract Area"
    if "Functional Area" in s: return "F. Functional Area"
    if "Well Bore Interval" in s: return "E3. Well hierarchy (deepest)"
    if "Well Bore" in s or "Well" in s: return "E. Well hierarchy"
    if "Facility Class 1" in s: return "B. Production Unit + Area + Facility Class 1"
    if "Area" in s: return "D. Production Unit + Area"
    return "Z. other"

g = defaultdict(list)
for o in cfg:
    g[group(o["nav"])].append(o)

lines = ["# OV Non-Bank Targets - the 55 OV-GM object screens beyond the 71",
         "",
         "**Scope:** OV (`CLASS_TYPE=OBJECT`) screens NOT in the 71 Bank-layout list and not yet automated.",
         "Grouped by NAVIGATOR pattern (owner's recipe `tmp/ov_gm_55_nav_recipe.xlsx`). Build order = easiest first.",
         "Nav values resolved FIRST-AVAILABLE live (recipe gives the nav *shape*, not hardcoded P1/SS1).",
         "Two OV flavours: **manage-object** (grid `manage_object_nav_nav:form:T_data` + GO) vs **custom-URL**",
         "(grid `nav:form:T_data`, no GO, toolbar Refresh) - recon each; engine `click_go` now does GO-or-Refresh.",
         "", "**Legend:** [x] done+verified · [~] driver-proven/partial · [ ] pending · (P) parked (reason).", ""]
total = done = 0
for grp in sorted(g):
    lines.append("## %s  (%d)" % (grp, len(g[grp])))
    lines.append("| BF | Screen | OV_ view | Folder | Status |")
    lines.append("|---|---|---|---|---|")
    for o in sorted(g[grp], key=lambda x: x["bf"]):
        total += 1
        st = "[x] " + DONE[o["bf"]] if o["bf"] in DONE else "[ ]"
        if o["bf"] in DONE: done += 1
        lines.append("| %s | %s | %s | %s | %s |" % (o["bf"], o["screen"], o["view"], o["folder"], st))
    lines.append("")
lines.insert(11, "**Progress: %d/%d done.**\n" % (done, total))
Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation\docs\ov-non-bank-targets.md").write_text("\n".join(lines), encoding="utf-8")
print("wrote ov-non-bank-targets.md  (%d screens, %d done)" % (total, done))
