"""Does the fix's formula - "../" * (segments + 1) - match what real files of EVERY shape use?"""
import re
from pathlib import Path
EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
def a(s): return str(s).encode("ascii","replace").decode("ascii")
seen, bad = {}, 0
for f in sorted(list(EC.glob("pageobjects/**/*_page.resource")) + list(EC.glob("tests/**/*_iud.robot"))):
    root = "pageobjects" if "pageobjects" in f.parts else "tests"
    segs = len(f.parts[f.parts.index(root) + 1:-1])
    for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
        m = re.match(r"^(Resource|Library)\s+((?:\.\./)+)", line.strip())
        if m:
            used = len(m.group(2)) // 3
            expected = segs + 1
            if used != expected:
                bad += 1
                print(a("MISMATCH %s segs=%d used=%d expected=%d" % (f.name, segs, used, expected)))
            seen.setdefault(segs, (f.relative_to(EC).as_posix(), used, expected))
            break
for segs in sorted(seen):
    n, used, exp = seen[segs]
    print(a("%d-segment  used=%d  formula=%d  %s  %s" % (segs, used, exp, "OK" if used == exp else "WRONG", n)))
print(a("\nmismatches: %d" % bad))
raise SystemExit(1 if bad else 0)
