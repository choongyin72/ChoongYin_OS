from pathlib import Path
for f in ["workstreams/master-plan/ec-automation/py/meter_run_iud.py",
          "workstreams/master-plan/ec-automation/py/orifice_plate_iud.py"]:
    p = Path(f); t = p.read_text(encoding="utf-8")
    raw = t.count("°")            # actual degree char still present?
    esc = t.count("\u00b0")           # escaped form present?
    print(f"{f}: raw_degree={raw} escaped={esc}")
    for i, line in enumerate(t.splitlines(), 1):
        if "°" in line:
            print(f"   still-raw line {i}: {line.strip()[:70]}")
