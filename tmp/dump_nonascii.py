from pathlib import Path
p = Path("workstreams/master-plan/ec-automation/py/orifice_plate_iud.py")
lines = p.read_text(encoding="utf-8").splitlines()
line = lines[42]  # line 43 (0-indexed 42)
print("line 43 repr:", repr(line))
for col, ch in enumerate(line, 1):
    if ord(ch) > 127:
        print(f"  col {col}: U+{ord(ch):04X} {ch!r}")
