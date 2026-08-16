"""Test the EXACT-comparison guard on real files: identical -> no-op; different -> preserve + .generated."""
from pathlib import Path
R = Path(r"C:\Projects\ChoongYin_OS")
S = R / "workstreams/master-plan/ec-automation/screens/Configuration/Assets"
for label, f in (("Pilot (hand-edited)", S/"Transport_Objects/Pilot/JOURNAL.md"),
                 ("Truck (hand-edited)", S/"Transport_Objects/Truck/JOURNAL.md"),
                 ("Report Group", S/"Facility_Objects/Report_Group/JOURNAL.md")):
    cur = f.read_text(encoding="utf-8", errors="replace")
    generated_stub = "# JOURNAL - X (Y) ovgm IUD\n\n## 2026-07-31\n\n## Lessons\n- z\n"
    same = cur.strip() == generated_stub.strip()
    print("  %-22s identical_to_generated=%-5s -> %s"
          % (label, same, "no-op" if same else "PRESERVE + JOURNAL.generated.md (correct)"))
