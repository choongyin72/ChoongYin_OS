"""HEADED RF demo - 11 Commercial Objects suites, sequential.
Sub_Field is SKIPPED (parked: groupmodel not enabled on sandbox).
EC_HEADLESS=false (visible browser) + new maximize/full-page-expand keywords.
Results under c:/tmp/rf_com_demo/<timestamp>/<suite>/.
"""
import os
import subprocess
import sys
import time
from pathlib import Path

TESTS = Path(r"c:/Projects/ChoongYin_OS/workstreams/master-plan/ec-automation"
             r"/tests/Configuration/Assets/Commercial_Objects")
ORDER = [
    "commercial_entity_iud", "company_iud", "company_contact_iud",
    "customer_iud", "field_iud", "field_group_iud", "licence_iud",
    "mms_lease_iud", "operator_lease_iud", "state_lease_iud", "vendor_iud",
]  # sub_field parked - groupmodel off

env = dict(os.environ, EC_HEADLESS="false", PYTHONUTF8="1")
out_root = rf"c:/tmp/rf_com_demo/{time.strftime('%Y%m%d_%H%M%S')}"
results = {}
for i, suite in enumerate(ORDER, 1):
    print(f"\n{'='*60}\n[{i}/{len(ORDER)}] RF DEMO: {suite}\n{'='*60}", flush=True)
    r = subprocess.run(["robot", "--outputdir", f"{out_root}/{suite}", str(TESTS / f"{suite}.robot")],
                       env=env, capture_output=True, text=True, timeout=900, shell=True)
    lines = (r.stdout or "").splitlines()
    stat = next((l.strip() for l in reversed(lines) if "tests," in l), "?")
    results[suite] = ("PASS" if r.returncode == 0 else "FAIL") + f"  ({stat})"
    print(f"  {stat}", flush=True)

print(f"\n{'='*60}\nRF DEMO SUMMARY (sub_field skipped - parked)\n{'='*60}")
for k, v in results.items():
    print(f"  {k:28s} {v}")
fails = [k for k, v in results.items() if v.startswith("FAIL")]
print(f"\n{len(results)-len(fails)}/{len(results)} PASS" + (f"  FAILED: {fails}" if fails else ""))
sys.exit(1 if fails else 0)
