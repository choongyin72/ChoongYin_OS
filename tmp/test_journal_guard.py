#!/usr/bin/env python3
"""Prove the JOURNAL overwrite guard classifies BOTH cases correctly, using the same test the packager
applies: a hand-edited journal must be PRESERVED, a generator-fresh one must still be regenerated
(otherwise the guard would block legitimate updates)."""
from pathlib import Path

R = Path(r"C:\Projects\ChoongYin_OS")
S = R / "workstreams/master-plan/ec-automation/screens/Configuration/Assets"
CASES = [
    ("Pilot (hand-edited history)", S / "Transport_Objects/Pilot/JOURNAL.md", False),
    ("Report Group (generator-fresh)", S / "Facility_Objects/Report_Group/JOURNAL.md", True),
    ("Truck (hand-edited #278 story)", S / "Transport_Objects/Truck/JOURNAL.md", False),
]
bad = 0
for label, f, expect_fresh in CASES:
    if not f.is_file():
        print("  MISSING %s" % f)
        bad += 1
        continue
    t = f.read_text(encoding="utf-8", errors="replace")
    fresh = t.lstrip().startswith("# JOURNAL - ") and "## Lessons" in t and len(t) < 1800
    action = "regenerate" if fresh else "PRESERVE + write JOURNAL.generated.md"
    ok = (fresh == expect_fresh)
    print("  %-34s len=%-5d fresh=%-5s -> %-38s %s"
          % (label, len(t), fresh, action, "OK" if ok else "WRONG"))
    if not ok:
        bad += 1
print("\nresult:", "all cases classified correctly" if not bad else "%d case(s) WRONG" % bad)
raise SystemExit(1 if bad else 0)
