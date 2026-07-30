from pathlib import Path
BS = chr(92)  # backslash, without writing it as a literal escape
for f in ["workstreams/master-plan/ec-automation/py/meter_run_iud.py",
          "workstreams/master-plan/ec-automation/py/orifice_plate_iud.py"]:
    p = Path(f)
    src = p.read_text(encoding="utf-8")
    out = []
    repl = 0
    for ch in src:
        if ord(ch) > 127:
            out.append(BS + "u%04x" % ord(ch)); repl += 1
        else:
            out.append(ch)
    p.write_text("".join(out), encoding="ascii", newline="\n")
    disk = Path(f).read_text(encoding="utf-8")
    left = sum(1 for c in disk if ord(c) > 127)
    print(f"{f}: escaped {repl}; non-ascii on disk now = {left}")
