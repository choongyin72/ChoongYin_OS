"""Flakiness is the defect, so test for STABILITY: scan Service 3 times and require identical grid ids."""
import subprocess, sys, os, re
R = r"C:\Projects\ChoongYin_OS"
def a(s): return str(s).encode("ascii","replace").decode("ascii")
env = dict(os.environ, SCREEN="Service")
seen = []
for i in range(3):
    r = subprocess.run([sys.executable, "-X", "utf8", "tmp/scripts/scan_ec_screen.py"],
                       cwd=R, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    m = re.search(r"grid id: (\S+)", r.stdout or "")
    n = re.search(r"navigator: (\{.*?\})\n", r.stdout or "", re.S)
    seen.append(m.group(1) if m else "ERR")
    print(a("run %d -> grid=%s" % (i + 1, seen[-1])))
print(a("\nstable: %s (%s)" % (len(set(seen)) == 1, set(seen))))
raise SystemExit(0 if len(set(seen)) == 1 and "None" not in seen else 1)
