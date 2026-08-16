"""NEGATIVE TEST: inject a stale claim into Service's generated recon.py and confirm the sweep catches it.
File restored afterwards."""
import subprocess
from pathlib import Path
R = Path(__file__).resolve().parents[1]   # repo-relative, same fix as negtest_artifact_sweep.py
f = R / "workstreams/master-plan/ec-automation/screens/Configuration/Assets/Service_Objects/Service/investigation/recon.py"
orig = f.read_text(encoding="utf-8")
bad = orig.replace(
    "ec.click_go(pg)",
    "ec.click_go(pg)  # apply_ovgm_navigator first-available",
    1
)
assert bad != orig, "injection point not found"
f.write_text(bad, encoding="utf-8")
try:
    r = subprocess.run(["py", "tmp/run_pkg_service.py"], cwd=str(R), capture_output=True, text=True)
    out = (r.stdout or "") + (r.stderr or "")
    print([l for l in out.splitlines() if "recon.py" in l or "ABORT" in l][:5])
finally:
    f.write_text(orig, encoding="utf-8")
    print("[restored]")
