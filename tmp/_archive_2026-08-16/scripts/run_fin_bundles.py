"""Run the Playwright bundle scripts for the 11 PASSING Financial Objects
screens (3 parked screens skipped), collecting pass/fail."""
import subprocess
import sys
from pathlib import Path

FIN = Path(r"c:/Projects/ChoongYin_OS/workstreams/master-plan/ec-automation/screens/Configuration/Assets/Financial_Objects")
SKIP = {"Account_Mapping", "Bank_Account", "Cost_Object_Mapping"}
summary = {}
for d in sorted(FIN.iterdir()):
    if not d.is_dir() or d.name in SKIP:
        continue
    script = next((d / "playwright").glob("ec_iud_*.py"), None)
    if not script:
        continue
    print(f"\n######## {d.name} ########", flush=True)
    r = subprocess.run([sys.executable, "-X", "utf8", str(script)],
                       capture_output=True, text=True, timeout=600)
    print((r.stdout or "")[-300:])
    ok = "ALL PASS" in (r.stdout or "")
    summary[d.name] = "ALL PASS" if ok else f"FAIL rc={r.returncode}"
    if not ok:
        print((r.stderr or "")[-300:])

print("\n================ SUMMARY ================")
for k, v in summary.items():
    print(f"  {k:<24} {v}")
fails = [k for k, v in summary.items() if v != "ALL PASS"]
print(f"\n{len(summary) - len(fails)}/{len(summary)} ALL PASS" + (f"  (failed: {fails})" if fails else ""))
