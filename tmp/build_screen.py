"""Orchestrate one plain OV screen end-to-end (no shell chaining):
  1) generate T3+suite+bundle+KB+driver via gen_ov_screen.py
  2) run the Playwright driver headless -> require 'Overall: ALL PASS'
  3) run scripts/verify_screen.py -> require OVERALL PASS
  4) copy evidence (png 01-05 + rf_report.html) into the bundle
Prints a final RESULT line. Does NOT touch git (caller does branch/commit/PR).

Usage: py tmp/build_screen.py '<json config>'
"""
import json, os, subprocess, sys, shutil
from pathlib import Path

ROOT = Path(r"C:\Projects\ChoongYin_OS")
EC = ROOT / "workstreams" / "master-plan" / "ec-automation"
c = json.loads(sys.argv[1])
slug = c["slug"]; folder = c["folder"].strip("/"); Screen_dir = c["screen"].replace(" ", "_")
env = dict(os.environ)


def run(cmd, **kw):
    print("  $ " + " ".join(str(x) for x in cmd), flush=True)
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


# 1) generate
r = run(["py", str(ROOT / "tmp" / "gen_ov_screen.py"), json.dumps(c)])
print(r.stdout[-500:]);
if r.returncode != 0:
    print(r.stderr[-800:]); print("RESULT %s: FAIL (generate)" % slug); sys.exit(1)

# 2) driver
driver_rel = "workstreams/master-plan/ec-automation/py/%s_iud.py" % slug
e = dict(env); e["EC_HEADED"] = "0"
r = run(["py", "-X", "utf8", str(ROOT / driver_rel)], cwd=str(ROOT), env=e)
tail = r.stdout[-700:]
print(tail)
if "Overall: ALL PASS" not in r.stdout:
    print(r.stderr[-800:]); print("RESULT %s: FAIL (driver)" % slug); sys.exit(1)

# 3) verify_screen
t3 = "workstreams/master-plan/ec-automation/pageobjects/%s/%s_page.resource" % (folder, slug)
suite = "workstreams/master-plan/ec-automation/tests/%s/%s_iud.robot" % (folder, slug)
out = "workstreams/master-plan/ec-automation/screens/%s/%s/VERIFY-REPORT.md" % (folder, Screen_dir)
r = run(["py", "-X", "utf8", str(ROOT / "scripts" / "verify_screen.py"),
         "--name", "%s (%s)" % (c["screen"], c["bfcode"]),
         "--t3", t3, "--suite", suite, "--driver", driver_rel, "--out", out], cwd=str(ROOT))
print(r.stdout[-900:])
if "OVERALL: PASS" not in r.stdout:
    print(r.stderr[-600:]); print("RESULT %s: FAIL (verify_screen)" % slug); sys.exit(1)

# 4) evidence
B = EC / "screens" / Path(folder) / Screen_dir
(B / "evidence").mkdir(parents=True, exist_ok=True)
(B / "investigation").mkdir(parents=True, exist_ok=True)
srcev = ROOT / "tmp" / slug / "evidence"
if srcev.exists():
    for png in sorted(srcev.glob("%s_0[1-5]_*.png" % slug)):
        shutil.copy(str(png), str(B / "evidence" / png.name))
rf = EC / "results" / "_verify_live" / "report.html"
if rf.exists():
    shutil.copy(str(rf), str(B / "evidence" / "rf_report.html"))
recon = ROOT / "tmp" / slug / "recon.py"
if recon.exists():
    shutil.copy(str(recon), str(B / "investigation" / "recon.py"))

print("RESULT %s: PASS  bundle=%s" % (slug, B))
