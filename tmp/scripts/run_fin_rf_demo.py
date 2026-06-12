"""HEADED RF demo - all 15 Financial Objects suites, sequential.
EC_HEADLESS=false per the demo rule (visible browser). Results under
c:/tmp/rf_fin_demo/<timestamp>/<suite>/.
"""
import os
import subprocess
import sys
import time
from pathlib import Path

TESTS = Path(r"c:/Projects/ChoongYin_OS/workstreams/master-plan/ec-automation"
             r"/tests/Configuration/Assets/Financial_Objects")
ORDER = [
    "bank_iud", "account_iud", "account_mapping_iud", "bank_account_iud",
    "cost_centre_iud", "cost_object_mapping_iud", "currency_iud",
    "doa_credit_limit_iud", "exchange_rate_source_iud", "payment_scheme_iud",
    "product_description_iud", "revenue_order_iud", "sales_order_iud",
    "vat_code_iud", "wbs_iud",
]

env = dict(os.environ, EC_HEADLESS="false", PYTHONUTF8="1")
out_root = rf"c:/tmp/rf_fin_demo/{time.strftime('%Y%m%d_%H%M%S')}"
results = {}
for i, suite in enumerate(ORDER, 1):
    print(f"\n{'='*60}\n[{i}/{len(ORDER)}] RF DEMO: {suite}\n{'='*60}", flush=True)
    r = subprocess.run(["robot", "--outputdir", f"{out_root}/{suite}", str(TESTS / f"{suite}.robot")],
                       env=env, capture_output=True, text=True, timeout=900, shell=True)
    lines = (r.stdout or "").splitlines()
    stat = next((l.strip() for l in reversed(lines) if "tests," in l), "?")
    results[suite] = ("PASS" if r.returncode == 0 else "FAIL") + f"  ({stat})"
    print(f"  {stat}", flush=True)

print(f"\n{'='*60}\nRF DEMO SUMMARY\n{'='*60}")
for k, v in results.items():
    print(f"  {k:28s} {v}")
fails = [k for k, v in results.items() if v.startswith("FAIL")]
print(f"\n{len(results)-len(fails)}/{len(results)} PASS" + (f"  FAILED: {fails}" if fails else ""))
sys.exit(1 if fails else 0)
