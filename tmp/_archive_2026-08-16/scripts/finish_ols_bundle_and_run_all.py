"""Copy OLS investigation probes into its bundle, then run ALL 12 Playwright
bundle scripts sequentially (headless), collecting pass/fail per screen.
Evidence screenshots + results JSON land in each bundle's evidence/ folder."""
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"c:/Projects/ChoongYin_OS/workstreams/master-plan/ec-automation/screens/Configuration/Assets/Basic_Objects")
TMPS = Path(r"c:/Projects/ChoongYin_OS/tmp/scripts")

ols_inv = ROOT / "Object_List_Setup" / "investigation"
ols_inv.mkdir(parents=True, exist_ok=True)
(ROOT / "Object_List_Setup" / "evidence").mkdir(exist_ok=True)
for probe in ["basic_objects_recon2.py", "phase_b_deep_dive.py", "phase_b_confirm_probe.py",
              "probe_ols_item_row.py", "probe_ols_save_reject.py"]:
    src = TMPS / probe
    if src.exists():
        shutil.copy2(src, ols_inv / probe)
print("OLS investigation copied")

ORDER = ["Production_Unit", "Business_Unit", "Country", "State", "County", "Region",
         "Object_List", "Functional_Area", "Regulatory_Permits", "Area", "Sub_Area",
         "Object_List_Setup"]
summary = {}
for name in ORDER:
    script = next((ROOT / name / "playwright").glob("ec_iud_*.py"))
    print(f"\n######## {name} ########", flush=True)
    r = subprocess.run([sys.executable, "-X", "utf8", str(script)],
                       capture_output=True, text=True, timeout=600)
    tail = (r.stdout or "")[-400:]
    print(tail)
    ok = "ALL PASS" in (r.stdout or "")
    summary[name] = "ALL PASS" if ok else f"FAIL rc={r.returncode}"
    if not ok:
        print((r.stderr or "")[-400:])

print("\n================ SUMMARY ================")
for k, v in summary.items():
    print(f"  {k:<22} {v}")
fails = [k for k, v in summary.items() if v != "ALL PASS"]
print(f"\n{12 - len(fails)}/12 ALL PASS" + (f"  (failed: {fails})" if fails else ""))
