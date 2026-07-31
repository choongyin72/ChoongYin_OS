#!/usr/bin/env python3
"""My first JOURNAL guard used a shape/length heuristic - and the test proved it classifies HAND-EDITED
journals (Pilot, Truck) as generator-fresh, so it would have overwritten exactly what it was meant to
protect. Heuristic deleted.

Replacement needs no guessing: NEVER overwrite an existing JOURNAL.md.
  - identical to what the generator would write -> nothing to do (silent, no churn)
  - different in any way                        -> keep the file, write JOURNAL.generated.md, warn loudly
Divergence is precisely when a human must decide, so the tool stops rather than picks."""
from pathlib import Path

p = Path(r"C:\Projects\ChoongYin_OS\tmp\package_ovgm.py")
s = p.read_text(encoding="utf-8")
old_start = "# do NOT clobber a hand-edited JOURNAL"
i = s.index(old_start)
j = s.index('    _jr.write_text(journal, encoding="utf-8")', i)
j = s.index("\n", j) + 1
new = '''# NEVER overwrite an existing JOURNAL.md. A packager re-run silently replaced Pilot's real
# Pilot-vs-Pilot-Boat lesson with the template once already (found as a floating diff 2026-07-31).
# A shape/length heuristic was tried first and FAILED its own test (it classed hand-edited journals as
# generator-fresh), so this compares content exactly and defers to a human on any divergence.
_jr = bundle / "JOURNAL.md"
if not _jr.exists():
    _jr.write_text(journal, encoding="utf-8")
elif _jr.read_text(encoding="utf-8", errors="replace").strip() == journal.strip():
    pass                                    # identical - nothing to do
else:
    (bundle / "JOURNAL.generated.md").write_text(journal, encoding="utf-8")
    print("WARNING: existing JOURNAL.md differs from the generated one - KEPT yours, wrote "
          "JOURNAL.generated.md beside it. Merge by hand; do not delete history.")
'''
s = s[:i] + new + s[j:]
p.write_text(s, encoding="utf-8")
print("guard replaced with exact-content comparison")
