import json, subprocess, sys
from pathlib import Path
R = Path(r"C:\Projects\ChoongYin_OS")
cfg = json.loads((R / "tmp" / "cfg_report_group.json").read_text(encoding="utf-8"))
cfg["date"] = "2026-07-31"
r = subprocess.run([sys.executable, "-X", "utf8", str(R / "tmp" / "package_ovgm.py"), json.dumps(cfg)],
                   cwd=R, capture_output=True, text=True, encoding="utf-8", errors="replace")
print((r.stdout or "").strip()[-4000:])
if r.stderr.strip(): print("STDERR:", (r.stderr or "").strip()[-1500:])
print("EXIT:", r.returncode)
