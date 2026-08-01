"""NEGATIVE TEST: inject a genuine stale claim into a generated driver file (Contract Capacity, which
uses nav_value/nav_is_explicit=True) and confirm the sweep catches it. File restored afterwards."""
import subprocess
from pathlib import Path
# repo-relative, not hardcoded (reviewer NICE-TO-HAVE on #300: this script is only useful if it works on
# any checkout location, not just this machine's path).
R = Path(__file__).resolve().parents[1]
f = R / "workstreams/master-plan/ec-automation/py/contract_capacity_iud.py"
orig = f.read_text(encoding="utf-8")
bad = orig.replace(
    "Fields by label.",
    "Fields by label. Built on the gated-navigator capability (apply_ovgm_navigator), first-available.",
    1
)
assert bad != orig, "injection point not found"
f.write_text(bad, encoding="utf-8")
try:
    r = subprocess.run(["py", "tmp/run_pkg_cc.py"], cwd=str(R), capture_output=True, text=True)
    out = (r.stdout or "") + (r.stderr or "")
    print("exit:", r.returncode)
    print([l for l in out.splitlines() if "sweep" in l.lower() or "ABORT" in l or "contract_capacity_iud.py" in l][:6])
finally:
    f.write_text(orig, encoding="utf-8")
    print("\n[restored original file]")
