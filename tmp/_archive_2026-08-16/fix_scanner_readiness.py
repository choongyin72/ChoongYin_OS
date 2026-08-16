#!/usr/bin/env python3
"""ITEM 3: scan_ec_screen.py reported `navigator: {'fields': [], 'go': []}` and `grid id: None` for Report
Group (CO.0158) - a screen that demonstrably HAS a visible date navigator
(nav:form:G:0:R:1:C:0:da_input), a visible+enabled GO (button:form:B) and grid
report_group_table:form:T_data with rows. It even missed the GO button, which cannot be a shape problem.

Root cause: after clicking the treeview link the script only calls ajax(page), then queries immediately.
On a slower screen those elements are not in the DOM yet, so every query returns empty. This is the FIRST
tool run per screen, so an empty reading is where mis-classification starts - it made me report 'plain OV
with no navigator' and nearly build on the wrong shape.

Fix: poll for readiness (any nav field / grid / objectForm / GO) before scanning, and if nothing ever
appears, FAIL LOUDLY with exit 2 rather than printing empty results that read like facts.
"""
from pathlib import Path

p = Path(r"C:\Projects\ChoongYin_OS\tmp\scripts\scan_ec_screen.py")
s = p.read_text(encoding="utf-8")

anchor = "    # 1) toolbar New/Delete enabled-state"
assert s.count(anchor) == 1, "toolbar section anchor not found"

READY = '''    # 0) SCREEN READINESS - added 2026-07-31. Without this the scan queried before the screen rendered
    #    and printed navigator={} / grid=None for Report Group, which HAS both. An empty scan result is
    #    indistinguishable from "this screen has no navigator", so it must never be reported as a fact.
    _ready = False
    for _ in range(30):                      # up to ~30s
        _state = page.evaluate("""() => ({
            nav: document.querySelectorAll("[id^='nav:form:G:']").length,
            grid: document.querySelectorAll("[id$=':T_data']").length,
            form: document.querySelectorAll("[id*='objectForm']").length,
            go: ['go_button:form:B','button:form:B','navButton:form:B']
                  .filter(i => document.getElementById(i)).length })""")
        if _state["nav"] or _state["grid"] or _state["form"] or _state["go"]:
            _ready = True
            print("screen ready:", _state)
            break
        page.wait_for_timeout(1000)
    if not _ready:
        print("=" * 78)
        print("SCAN ABORTED - the screen never rendered a navigator, grid, objectForm or GO button.")
        print("An EMPTY scan is NOT evidence that the screen lacks these - do NOT record it as a shape.")
        print("Re-run with EC_HEADED=1 and watch; the screen may need a different entry (custom URL).")
        print("=" * 78)
        b.close()
        sys.exit(2)
    page.wait_for_timeout(1200)              # let a late-rendering navigator settle

'''

s = s.replace(anchor, READY + anchor)

if "\nimport sys" not in s:                  # the abort path needs sys.exit
    s = s.replace("import os\n", "import os\nimport sys\n", 1)
    print("added missing 'import sys'")

p.write_text(s, encoding="utf-8")
print("scan_ec_screen.py: readiness poll + loud abort added")
