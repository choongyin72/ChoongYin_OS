from pathlib import Path
RB = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
for pat in ["py/*.py","tests/**/*.robot","pageobjects/**/*.resource","resources/*.resource"]:
    for f in RB.glob(pat):
        b = f.read_bytes()
        if b"\x85" in b or any(x > 127 for x in b):
            bad = {x for x in b if x > 127}
            print(f.relative_to(RB), "->", sorted(hex(x) for x in bad))
