#!/usr/bin/env python3
"""ITEM 8 resolved - and it was a DESTRUCTIVE change, not pending work.

The floating Pilot/JOURNAL.md would REPLACE hand-written history (its real Pilot-vs-Pilot-Boat exact-match
lesson, the registry-first finding) with the generic packager template. Contract_Area_Setup/evidence/
results.json only bumped "date" 2026-07-30 -> 2026-07-31 without a verify re-run, which would misdate the
evidence. Both reverted to the committed content.

ROOT CAUSE: package_ovgm.py writes JOURNAL.md UNCONDITIONALLY, so any re-run silently overwrites a
hand-edited journal. This is exactly the risk I avoided by hand-fixing (not regenerating) the 6 swept
bundles - here is the proof it is real. Guard added: if JOURNAL.md already exists and does NOT look
generator-fresh, keep it and write JOURNAL.generated.md beside it instead.
"""
import subprocess
from pathlib import Path

R = Path(r"C:\Projects\ChoongYin_OS")
S = "workstreams/master-plan/ec-automation/screens/Configuration/Assets"
PATHS = [f"{S}/Transport_Objects/Pilot/JOURNAL.md",
         f"{S}/Contract_Objects/Contract_Area_Setup/evidence/results.json"]

r = subprocess.run(["git", "restore", "--"] + PATHS, cwd=str(R), capture_output=True, text=True)
print("git restore ->", r.returncode, (r.stderr or "").strip()[:150])
left = subprocess.run(["git", "status", "--porcelain"] + PATHS, cwd=str(R),
                      capture_output=True, text=True).stdout.strip()
assert not left, "still dirty: %r" % left
print("both files back to committed content; Pilot's hand-written journal preserved")

p = R / "tmp" / "package_ovgm.py"
s = p.read_text(encoding="utf-8")
old = '(bundle / "JOURNAL.md").write_text(journal, encoding="utf-8")'
assert s.count(old) == 1, "JOURNAL write line not found"
new = '''# do NOT clobber a hand-edited JOURNAL: a re-run silently replaced Pilot's real
# Pilot-vs-Pilot-Boat lesson with this template once already (found 2026-07-31 as a floating diff).
_jr = bundle / "JOURNAL.md"
if _jr.exists():
    _cur = _jr.read_text(encoding="utf-8", errors="replace")
    _fresh = _cur.lstrip().startswith("# JOURNAL - ") and "## Lessons" in _cur and len(_cur) < 1800
    if not _fresh:
        (bundle / "JOURNAL.generated.md").write_text(journal, encoding="utf-8")
        print("KEPT existing hand-edited JOURNAL.md; wrote JOURNAL.generated.md beside it - merge by hand")
    else:
        _jr.write_text(journal, encoding="utf-8")
else:
    _jr.write_text(journal, encoding="utf-8")'''
s = s.replace(old, new)
p.write_text(s, encoding="utf-8")
print("package_ovgm.py: JOURNAL overwrite guard added")
