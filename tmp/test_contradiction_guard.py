import sys, tempfile
from pathlib import Path
sys.path.insert(0, r"C:\Projects\ChoongYin_OS\scripts")
import check_bundle_hygiene as h
d = Path(tempfile.mkdtemp())
(d / "VERIFY-REPORT.md").write_text("# VERIFY-REPORT - Test\n\n**OVERALL: FAIL**\n\n- [ ] **10** robocop clean - exit=1, ~4 issues\n- [x] **11** dryrun - 4/4\n", encoding="utf-8")
(d / "CHECKLIST.md").write_text("## C. Verification gates (OVERALL PASS)\n- [x] 10 robocop exit 0 - [x] 11 dryrun 4/4\n", encoding="utf-8")
res = h.checklist_contradictions(d)
print("contradictions found:", len(res))
for m in res: print("  -", m)
assert any("gate 10" in m for m in res), "FAIL: did not catch the robocop contradiction"
assert any("OVERALL" in m for m in res), "FAIL: did not catch the OVERALL contradiction"
print("GUARD SELF-TEST: PASS (catches both per-gate + OVERALL contradictions)")
