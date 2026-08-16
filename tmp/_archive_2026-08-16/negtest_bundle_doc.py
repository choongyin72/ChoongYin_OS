import subprocess, sys
from pathlib import Path
R = Path(r"C:\Projects\ChoongYin_OS")
f = R/"workstreams/master-plan/ec-automation/screens/Configuration/Assets/Transport_Objects/Truck/CHECKLIST.md"
orig = f.read_text(encoding="utf-8")
f.write_text(orig + "\nGrid is manageObject:form:T_data, populated by the navigator cascade + GO.\n", encoding="utf-8")
try:
    r = subprocess.run([sys.executable, "-X", "utf8", str(R/"tmp/check_row_vocab.py"), "Truck", "plain"],
                       cwd=str(R), capture_output=True, text=True, encoding="utf-8", errors="replace")
    print("validator exit:", r.returncode); print((r.stdout or "").strip()[:400])
    h = subprocess.run([sys.executable, "-X", "utf8", str(R/"scripts/check_bundle_hygiene.py")],
                       cwd=str(R), capture_output=True, text=True, encoding="utf-8", errors="replace")
    print("hygiene exit:", h.returncode)
    for line in (h.stdout or "").splitlines():
        if "Truck" in line or "RESULT" in line or "family" in line.lower(): print("  ", line.strip()[:170])
finally:
    f.write_text(orig, encoding="utf-8")
    print("\n[restored]")
