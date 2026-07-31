import subprocess, sys
from pathlib import Path
R = Path(r"C:\Projects\ChoongYin_OS"); EC = R/"workstreams/master-plan/ec-automation"
out = EC/"screens/Configuration/Messaging/Message_Group/VERIFY-REPORT.md"
cmd = [sys.executable, "-X", "utf8", str(R/"scripts/verify_screen.py"), "--name", "Message Group",
       "--t3", str(EC/"pageobjects/Configuration/Messaging/message_group_page.resource"),
       "--suite", str(EC/"tests/Configuration/Messaging/message_group_iud.robot"),
       "--driver", str(EC/"py/message_group_iud.py"), "--out", str(out)]
r = subprocess.run(cmd, cwd=str(R), capture_output=True, text=True, encoding="utf-8", errors="replace")
print((r.stdout or "").strip()[-5000:])
if r.stderr.strip(): print("STDERR:", r.stderr.strip()[-1500:])
print("EXIT:", r.returncode)
