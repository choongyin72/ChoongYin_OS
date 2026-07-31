#!/usr/bin/env python3
"""VERIFY today's merged work against real facts. Read-only (git + file reads only).

Highest-risk item first: PR #287's reviewer RESTORED Truck / Contract Area Setup / Create Calculation but
KEPT my Driver / Trailer / Cargo Planning Forecast edits "as submitted", on the judgment that those had no
unique content to lose. That judgment is checkable - run the NO-LOSS DIFF I said would have caught #287:
for each file my sweep touched, list every line that EXISTED BEFORE and is GONE NOW, ignoring lines that
are merely reworded family vocabulary. Anything else that vanished is content I destroyed and nobody
restored.

Also verifies: Report Group's bundle is complete on master, its docs match the live facts I proved, and
no file still points at the pre-move tmp/check_known_issue.py path.
"""
import re
import subprocess
from pathlib import Path

R = Path(r"C:\Projects\ChoongYin_OS")
BASE = "d9b3f4871318bc4207c416689ff8188b81adad84"   # pre-#287 state
S = "workstreams/master-plan/ec-automation/screens"

# files the sweep touched for the three screens the reviewer did NOT restore
KEPT = {
    "Driver": ["ec-ui-knowledge/screens/driver.md",
               f"{S}/Configuration/Assets/Transport_Objects/Driver/CHECKLIST.md"],
    "Trailer": ["ec-ui-knowledge/screens/trailer.md",
                f"{S}/Configuration/Assets/Transport_Objects/Trailer/CHECKLIST.md"],
    "Cargo Planning Forecast": ["ec-ui-knowledge/screens/cargo_planning_forecast.md",
                                f"{S}/EC_Transport/Cargo_Planning/Forecast/Cargo_Planning_Forecast/CHECKLIST.md"],
}
# a deleted line is EXPECTED only if it is family vocabulary being corrected
FAMILY_WORDS = ["ov-gm", "manageobject:form:t_data", "op production unit", "cascade", "navigator-gated",
                "groupmodel", "gated-navigator", "pr #244", "apply_ovgm_navigator", "op pu"]


def a(s):
    return str(s).encode("ascii", "replace").decode("ascii")


def git(*args):
    return subprocess.run(("git",) + args, cwd=str(R), capture_output=True, text=True)


def before(path):
    r = git("show", "%s:%s" % (BASE, path))
    return r.stdout.splitlines() if r.returncode == 0 else None


print(a("=" * 78))
print(a("NO-LOSS DIFF - lines that existed pre-#287 and are GONE, excluding family-vocabulary rewrites"))
print(a("=" * 78))
total_unexplained = 0
for screen, paths in KEPT.items():
    print(a("\n### %s" % screen))
    for p in paths:
        old = before(p)
        if old is None:
            print(a("   %s : NOT IN BASE (new file)" % Path(p).name))
            continue
        cur = (R / p).read_text(encoding="utf-8", errors="replace").splitlines()
        cur_norm = {" ".join(l.split()) for l in cur}
        gone = [l for l in old if " ".join(l.split()) not in cur_norm and l.strip()]
        unexplained = [l for l in gone if not any(w in l.lower() for w in FAMILY_WORDS)]
        print(a("   %-34s gone=%-3d family-vocab=%-3d UNEXPLAINED=%d"
                % (Path(p).name, len(gone), len(gone) - len(unexplained), len(unexplained))))
        for l in unexplained:
            print(a("       LOST: %s" % l.strip()[:120]))
        total_unexplained += len(unexplained)
print(a("\nTOTAL unexplained deletions in the KEPT screens: %d" % total_unexplained))

print(a("\n" + "=" * 78))
print(a("REPORT GROUP - bundle completeness + docs vs the facts proved live"))
print(a("=" * 78))
b = R / S / "Configuration/Assets/Facility_Objects/Report_Group"
need = ["report_group_sow.md", "README.md", "JOURNAL.md", "CHECKLIST.md", "VERIFY-REPORT.md"]
for n in need:
    print(a("   %-24s %s" % (n, "present" if (b / n).is_file() else "MISSING")))
for d in ("investigation", "evidence"):
    files = list((b / d).glob("*")) if (b / d).is_dir() else []
    print(a("   %-24s %d file(s)" % (d + "/", len(files))))
vr = (b / "VERIFY-REPORT.md").read_text(encoding="utf-8", errors="replace")
print(a("   VERIFY-REPORT OVERALL PASS: %s" % ("OVERALL: PASS" in vr)))
cl = (b / "CHECKLIST.md").read_text(encoding="utf-8", errors="replace")
print(a("   CHECKLIST unticked items: %d (item 19 = PR, correctly unticked at package time)"
        % cl.count("- [ ]")))

kb = (R / "ec-ui-knowledge/screens/report_group.md").read_text(encoding="utf-8", errors="replace")
facts = {"grid report_group_table:form:T_data": "report_group_table:form:T_data" in kb,
         "date navigator nav:form:G:0:R:1:C:0:da_input": "nav:form:G:0:R:1:C:0:da_input" in kb,
         "NOT claiming manageObject grid": "manageObject:form:T_data" not in kb,
         "family = Plain OV": "Plain OV" in kb}
for k, v in facts.items():
    print(a("   KB fact %-46s %s" % (k, v)))

print(a("\n" + "=" * 78))
print(a("LEAK CHECK - stale references to the pre-move script path"))
print(a("=" * 78))
stale = []
for f in list(R.rglob("*.md")) + list(R.rglob("*.py")):
    if ".git" in f.parts or "node_modules" in f.parts:
        continue
    try:
        t = f.read_text(encoding="utf-8", errors="replace")
    except Exception:
        continue
    if "tmp/check_known_issue.py" in t:
        stale.append(f.relative_to(R).as_posix())
print(a("   files still pointing at tmp/check_known_issue.py: %d" % len(stale)))
for s in stale[:10]:
    print(a("      %s" % s))
print(a("   files referencing scripts/check_known_issue.py: %d"
        % sum(1 for f in list(R.rglob("*.md")) + list(R.rglob("*.py"))
              if ".git" not in f.parts and "scripts/check_known_issue.py"
              in f.read_text(encoding="utf-8", errors="replace"))))
