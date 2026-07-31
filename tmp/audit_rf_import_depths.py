#!/usr/bin/env python3
"""Verify the RF import-depth fix against EVERY shipped T3 + suite, not the 2 shapes I happened to test.

I claimed "no regression" on the strength of ONE file (Report Group, 3 segments) being byte-identical.
That is the same thin-evidence habit as everything else today: the fix is only as verified as the number
of variants checked. This resolves each `Resource`/`Library` relative path against the file's own location
and asserts the target EXISTS - which is the property that actually matters (a wrong depth silently fails
to resolve, and RF reports it as "no keyword with name ... found", pointing nowhere near the path).
"""
import re
from collections import Counter
from pathlib import Path

EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")


def a(s):
    return str(s).encode("ascii", "replace").decode("ascii")


files = sorted(list(EC.glob("pageobjects/**/*_page.resource")) + list(EC.glob("tests/**/*_iud.robot")))
print(a("checking %d RF files" % len(files)))

broken, shapes = [], Counter()
for f in files:
    # folder segments between pageobjects|tests and the file
    root = "pageobjects" if "pageobjects" in f.parts else "tests"
    idx = f.parts.index(root)
    segs = len(f.parts[idx + 1:-1])
    shapes[segs] += 1
    for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
        m = re.match(r"^(Resource|Library)\s+((?:\.\./)+[^\s]+)", line.strip())
        if not m:
            continue
        target = (f.parent / m.group(2)).resolve()
        if not target.exists():
            broken.append((f.relative_to(EC).as_posix(), segs, m.group(2), "MISSING"))

print(a("folder-depth shapes present: %s"
        % ", ".join("%d-segment: %d file(s)" % (k, v) for k, v in sorted(shapes.items()))))
if broken:
    print(a("\nUNRESOLVABLE imports: %d" % len(broken)))
    for f, segs, rel, why in broken[:20]:
        print(a("   %-58s segs=%d %s %s" % (f, segs, rel, why)))
else:
    print(a("\nALL relative imports resolve to files that exist - every shape, not just the 2 I tested."))
raise SystemExit(1 if broken else 0)
