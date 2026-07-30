import sys, tempfile
from pathlib import Path
sys.path.insert(0, r"C:\Projects\ChoongYin_OS\scripts")
import importlib, check_bundle_hygiene as h
importlib.reload(h)

def mk(vr, chk):
    d = Path(tempfile.mkdtemp())
    (d / "VERIFY-REPORT.md").write_text(vr, encoding="utf-8")
    (d / "CHECKLIST.md").write_text(chk, encoding="utf-8")
    return h.checklist_contradictions(d)

VR_FAIL = "**OVERALL: FAIL**\n- [ ] **10** robocop clean - exit=1, ~4 issues\n- [ ] **12** LIVE RF suite - 1/5 pass, 4 fail\n- [x] **16** hygiene - exit=0\n"
VR_PASS = "**OVERALL: PASS**\n- [x] **10** robocop clean - exit=0\n- [x] **12** LIVE RF suite - 5/5 pass\n"

# 1) dishonest: ticks a PASS + robocop clean while failing -> must flag 2
r1 = mk(VR_FAIL, "## gates (OVERALL PASS)\n- [x] 10 robocop - [x] 12 LIVE RF 5/5\n")
print("1 dishonest ->", len(r1), r1)
assert any("OVERALL" in m for m in r1) and any("gate 10" in m for m in r1)

# 2) HONEST RBF-style: robocop NOT claimed, OVERALL PASS only in an unchecked pending line -> must be CLEAN
r2 = mk(VR_FAIL, "- [x] Playwright 15/15\n- [ ] LIVE RF suite - WIP (1/5)\n- [ ] Full verify_screen OVERALL PASS - pending the RF fixes\n")
print("2 honest-pending ->", len(r2), r2)
assert r2 == [], "FALSE POSITIVE on honest pending checklist"

# 3) real RBF line 5: '[x] robocop clean' while robocop failed -> must flag gate 10 by keyword
r3 = mk(VR_FAIL, "- [x] robocop clean - [x] hygiene clean - [x] robot --dryrun 5/5\n- [ ] Full verify_screen OVERALL PASS - pending\n")
print("3 robocop-keyword ->", len(r3), r3)
assert any("gate 10" in m for m in r3), "missed the [x] robocop clean contradiction"

# 4) fully honest PASS -> clean
r4 = mk(VR_PASS, "- [x] robocop clean - [x] LIVE RF 5/5\n- [x] Full verify_screen OVERALL PASS\n")
print("4 honest-pass ->", len(r4), r4)
assert r4 == []
print("\nALL GUARD TESTS PASS")
