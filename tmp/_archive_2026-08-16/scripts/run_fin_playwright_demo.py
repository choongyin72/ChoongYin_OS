"""HEADED Playwright demo - all 15 Financial Objects screens, sequential.
Each bundle runs its full IUD cycle (insert/update/delete + DB verify) in a
visible browser with slow-mo; evidence screenshots refresh in each bundle's
evidence/ folder. AUTOTEST_* data only.
"""
import os
import subprocess
import sys
from pathlib import Path

FIN = Path(r"c:/Projects/ChoongYin_OS/workstreams/master-plan/ec-automation"
           r"/screens/Configuration/Assets/Financial_Objects")
ORDER = [
    "Bank", "Account", "Account_Mapping", "Bank_Account", "Cost_Centre",
    "Cost_Object_Mapping", "Currency", "DOA_Credit_Limit",
    "Exchange_Rate_Source", "Payment_Scheme", "Product_Description",
    "Revenue_Order", "Sales_Order", "VAT_Code", "WBS",
]

env = dict(os.environ, EC_HEADED="1", PYTHONUTF8="1")
results = {}
for i, screen in enumerate(ORDER, 1):
    script = next((FIN / screen / "playwright").glob("ec_iud_*.py"))
    print(f"\n{'='*60}\n[{i}/{len(ORDER)}] DEMO: {screen}\n{'='*60}", flush=True)
    r = subprocess.run(["py", "-u", str(script)], env=env, cwd=str(script.parent),
                       capture_output=True, text=True, timeout=900)
    out = (r.stdout or "") + (r.stderr or "")
    print(out[-2500:], flush=True)
    results[screen] = "PASS" if r.returncode == 0 else "FAIL"

print(f"\n{'='*60}\nDEMO SUMMARY\n{'='*60}")
for k, v in results.items():
    print(f"  {k:24s} {v}")
fails = [k for k, v in results.items() if v != "PASS"]
print(f"\n{len(results)-len(fails)}/{len(results)} PASS" + (f"  FAILED: {fails}" if fails else ""))
sys.exit(1 if fails else 0)
