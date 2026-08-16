"""NEGATIVE TEST (correct this time): revert package_ovgm.py's recon.py-writing logic to the ORIGINAL
unconditional apply_ovgm_navigator call (simulating the pre-fix bug), confirm the sweep catches its own
output, then restore the real fix."""
import shutil, subprocess
from pathlib import Path
R = Path(__file__).resolve().parents[1]   # repo-relative, same fix as negtest_artifact_sweep.py
f = R / "tmp/package_ovgm.py"
fixed = f.read_text(encoding="utf-8")
# swap the templated call back to the unconditional original
bad = fixed.replace("%(recon_nav_block)s", "    pu = ec.apply_ovgm_navigator(pg)")
assert bad != fixed
f.write_text(bad, encoding="utf-8")
try:
    r = subprocess.run(["py", "tmp/run_pkg_service.py"], cwd=str(R), capture_output=True, text=True)
    out = (r.stdout or "") + (r.stderr or "")
    print([l for l in out.splitlines() if "recon.py" in l.lower() or "ABORT" in l][:6])
finally:
    f.write_text(fixed, encoding="utf-8")
    print("[template restored to the real fix]")
