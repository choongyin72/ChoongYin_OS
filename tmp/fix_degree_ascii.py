from pathlib import Path
files = [
    r"workstreams/master-plan/ec-automation/py/meter_run_iud.py",
    r"workstreams/master-plan/ec-automation/py/orifice_plate_iud.py",
]
for f in files:
    p = Path(f)
    t = p.read_text(encoding="utf-8")
    n = t.count("°")
    if n:
        t = t.replace("°", "\u00b0")   # raw degree byte -> ASCII escape (runtime string identical)
        p.write_text(t, encoding="utf-8", newline="\n")
    print(f"{f}: replaced {n} degree char(s)")
