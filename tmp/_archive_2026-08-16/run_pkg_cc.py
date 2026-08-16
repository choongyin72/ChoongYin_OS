import json, subprocess, sys
from pathlib import Path
R = Path(r"C:\Projects\ChoongYin_OS")
cfg = json.loads((R/"tmp/cfg_contract_capacity.json").read_text(encoding="utf-8"))
cfg["date"] = "2026-08-01"
r = subprocess.run([sys.executable, "-X", "utf8", str(R/"tmp/package_ovgm.py"), json.dumps(cfg)],
                   cwd=str(R), capture_output=True, text=True, encoding="utf-8", errors="replace")
print((r.stdout or "").strip()[-1800:])
if r.returncode: print("STDERR:", (r.stderr or "").strip()[-1200:])
print("EXIT:", r.returncode)
