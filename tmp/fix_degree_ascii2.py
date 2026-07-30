from pathlib import Path
deg = chr(0x00B0)
for f in ["workstreams/master-plan/ec-automation/py/meter_run_iud.py",
          "workstreams/master-plan/ec-automation/py/orifice_plate_iud.py"]:
    p = Path(f); t = p.read_text(encoding="utf-8")
    n = t.count(deg)
    t = t.replace(deg, "\u00b0")
    p.write_text(t, encoding="utf-8", newline="\n")
    # verify no non-ASCII byte remains
    bad = [c for c in t if ord(c) > 127]
    print(f"{f}: replaced {n} remaining; non-ascii left={len(bad)}")
