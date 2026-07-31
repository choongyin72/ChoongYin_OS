import json, subprocess, sys
from pathlib import Path
R = Path(r"C:\Projects\ChoongYin_OS")
cfg = (R / "tmp" / "cfg_report_group.json").read_text(encoding="utf-8")
json.loads(cfg)   # fail fast on bad JSON before spawning
r = subprocess.run([sys.executable, "-X", "utf8", str(R / "tmp" / "gen_ov.py"), cfg],
                   cwd=R, capture_output=True, text=True, encoding="utf-8", errors="replace")
print((r.stdout or "").strip()[-3000:])
if r.returncode:
    print("STDERR:", (r.stderr or "").strip()[-2000:])
sys.exit(r.returncode)
