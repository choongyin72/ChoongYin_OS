"""CANARY PACK - run before committing any shared keyword-file change.
One live RF suite per screen pattern (~15-20 min total), exercising every
shared keyword branch:
  Bank             (plain OV, manage_object generics, navigator GO)
  Area             (OV-GM: groupmodel navigator, value-dd, extra GO, date rule)
  MIME Type Mapping(TV: inline grid, physical delete)
  Object List Setup(PC: parent-child grid, dd-cells, count-delta oracle)
  Account Mapping  (combination screen, Select-by-value x9, waiting assert)
"""
import subprocess
import sys
import time

BASE = r"c:/Projects/ChoongYin_OS/workstreams/master-plan/ec-automation/tests"
SUITES = [
    ("Bank (OV)", f"{BASE}/Configuration/Assets/Financial_Objects/bank_iud.robot"),
    ("Area (OV-GM)", f"{BASE}/Configuration/Assets/Basic_Objects/area_iud.robot"),
    ("MIME (TV)", f"{BASE}/Configuration/System/mime_iud.robot"),
    ("Object List Setup (PC)", f"{BASE}/Configuration/Assets/Basic_Objects/object_list_setup_iud.robot"),
    ("Account Mapping (combo)", f"{BASE}/Configuration/Assets/Financial_Objects/account_mapping_iud.robot"),
]

out_root = rf"c:/tmp/rf_canary/{time.strftime('%Y%m%d_%H%M%S')}"
results = {}
for name, suite in SUITES:
    print(f"\n######## CANARY: {name} ########", flush=True)
    r = subprocess.run(["robot", "--outputdir", f"{out_root}/{name.split(' ')[0]}", suite],
                       capture_output=True, text=True, timeout=900, shell=True)
    tail = (r.stdout or "").splitlines()
    line = next((l for l in reversed(tail) if "tests," in l), "?")
    ok = r.returncode == 0
    results[name] = "PASS" if ok else f"FAIL ({line.strip()})"
    print(f"  {line.strip()}")

print("\n================ CANARY SUMMARY ================")
for k, v in results.items():
    print(f"  {k:28s} {v}")
fails = [k for k, v in results.items() if v != "PASS"]
print(f"\n{len(results) - len(fails)}/{len(results)} PASS" + (f"  FAILED: {fails}" if fails else "  - SAFE TO COMMIT"))
sys.exit(1 if fails else 0)
