"""Health pass step 2: robot --dryrun over EVERY suite in ec-automation/tests.
Proves keyword resolution / imports / syntax after the refactor. No browser, no DB writes.
"""
import subprocess
import sys
from pathlib import Path

TESTS = Path(r"c:/Projects/ChoongYin_OS/workstreams/master-plan/ec-automation/tests")
OUT = r"c:/tmp/health_dryrun"

suites = sorted(TESTS.rglob("*.robot"))
print(f"{len(suites)} suites found")
fails = []
for i, s in enumerate(suites, 1):
    rel = s.relative_to(TESTS)
    r = subprocess.run(
        ["robot", "--dryrun", "--outputdir", f"{OUT}/{rel.stem}", str(s)],
        capture_output=True, text=True, timeout=300, shell=True)
    ok = r.returncode == 0
    if not ok:
        fails.append(str(rel))
    print(f"[{i:2d}/{len(suites)}] {'PASS' if ok else 'FAIL'}  {rel}")
    if not ok:
        tail = (r.stdout or "").splitlines()[-25:]
        print("        " + "\n        ".join(tail))

print(f"\n{len(suites)-len(fails)}/{len(suites)} dryrun PASS")
if fails:
    print("FAILED: " + ", ".join(fails))
sys.exit(1 if fails else 0)
