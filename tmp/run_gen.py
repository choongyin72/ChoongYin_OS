"""Generic runner: py tmp/run_gen.py <cfg.json> <generator.py>"""
import json, subprocess, sys
from pathlib import Path
R = Path(r"C:\Projects\ChoongYin_OS")
cfg = (R / sys.argv[1]).read_text(encoding="utf-8")
json.loads(cfg)
r = subprocess.run([sys.executable, "-X", "utf8", str(R / sys.argv[2]), cfg],
                   cwd=str(R), capture_output=True, text=True, encoding="utf-8", errors="replace")
print((r.stdout or "").strip()[-2500:])
if r.returncode: print("STDERR:", (r.stderr or "").strip()[-1500:])
sys.exit(r.returncode)
