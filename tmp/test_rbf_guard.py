import sys, importlib
from pathlib import Path
sys.path.insert(0, r"C:\Projects\ChoongYin_OS\scripts")
import check_bundle_hygiene as h; importlib.reload(h)
d = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation\screens\Configuration\Assets\Well_and_Reservoir_Objects\Reservoir_Block_Formation")
print("contradictions:", h.checklist_contradictions(d))
vr = (d/"VERIFY-REPORT.md").read_text(encoding="utf-8")
print("--- current report gates ---")
for ln in vr.splitlines():
    if ln.strip().startswith("- ["): print("   ", ln)
