import subprocess, sys
from pathlib import Path
R = Path(r"C:\Projects\ChoongYin_OS"); EC = R/"workstreams/master-plan/ec-automation"
b = EC/"screens/Configuration/Assets/Basic_Objects/Area"
b.mkdir(parents=True, exist_ok=True)
cmd = [sys.executable, "-X", "utf8", str(R/"scripts/verify_screen.py"), "--name", "Area",
       "--t3", str(EC/"pageobjects/Configuration/Assets/Basic_Objects/area_page.resource"),
       "--suite", str(EC/"tests/Configuration/Assets/Basic_Objects/area_iud.robot"),
       "--driver", str(EC/"screens/Configuration/Assets/Basic_Objects/Area/playwright/ec_iud_area.py"),
       "--out", str(b/"VERIFY-REPORT.md")]
r = subprocess.run(cmd, cwd=str(R), capture_output=True, text=True, encoding="utf-8", errors="replace")
print((r.stdout or "").strip()[-2500:]); print("EXIT:", r.returncode)
