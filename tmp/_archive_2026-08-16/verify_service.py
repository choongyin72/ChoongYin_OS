import subprocess, sys
from pathlib import Path
R = Path(r"C:\Projects\ChoongYin_OS"); EC = R/"workstreams/master-plan/ec-automation"
out = EC/"screens/Configuration/Assets/Service_Objects/Service/VERIFY-REPORT.md"
cmd = [sys.executable, "-X", "utf8", str(R/"scripts/verify_screen.py"), "--name", "Service",
       "--t3", str(EC/"pageobjects/Configuration/Assets/Service_Objects/service_page.resource"),
       "--suite", str(EC/"tests/Configuration/Assets/Service_Objects/service_iud.robot"),
       "--driver", str(EC/"py/service_iud.py"), "--out", str(out)]
r = subprocess.run(cmd, cwd=str(R), capture_output=True, text=True, encoding="utf-8", errors="replace")
print((r.stdout or "").strip()[-4000:])
if r.stderr.strip(): print("STDERR:", r.stderr.strip()[-1200:])
print("EXIT:", r.returncode)
