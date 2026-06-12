"""HEADED Playwright demo - 11 Commercial Objects screens, sequential.
Sub_Field is SKIPPED (parked: groupmodel not enabled on sandbox).
Visible browser + slow-mo; evidence screenshots refresh per bundle.
AUTOTEST_* data only.
"""
import os
import subprocess
import sys
from pathlib import Path

COM = Path(r"c:/Projects/ChoongYin_OS/workstreams/master-plan/ec-automation"
           r"/screens/Configuration/Assets/Commercial_Objects")
ORDER = [
    "Commercial_Entity", "Company", "Company_Contact", "Customer", "Field",
    "Field_Group", "Licence", "MMS_Lease", "Operator_Lease", "State_Lease",
    "Vendor",
]  # Sub_Field parked - groupmodel off

env = dict(os.environ, EC_HEADED="1", PYTHONUTF8="1")
results = {}
for i, screen in enumerate(ORDER, 1):
    script = next((COM / screen / "playwright").glob("ec_iud_*.py"))
    print(f"\n{'='*60}\n[{i}/{len(ORDER)}] DEMO: {screen}\n{'='*60}", flush=True)
    r = subprocess.run(["py", "-u", str(script)], env=env, cwd=str(script.parent),
                       capture_output=True, text=True, timeout=900)
    out = (r.stdout or "") + (r.stderr or "")
    print(out[-2500:], flush=True)
    results[screen] = "PASS" if r.returncode == 0 else "FAIL"

print(f"\n{'='*60}\nDEMO SUMMARY (Sub_Field skipped - parked)\n{'='*60}")
for k, v in results.items():
    print(f"  {k:24s} {v}")
fails = [k for k, v in results.items() if v != "PASS"]
print(f"\n{len(results)-len(fails)}/{len(results)} PASS" + (f"  FAILED: {fails}" if fails else ""))
sys.exit(1 if fails else 0)
