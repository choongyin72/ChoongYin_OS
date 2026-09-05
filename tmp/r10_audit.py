"""Run EVERY known defect check against one report, and list everything found.

    py tmp/r10_audit.py R10.034 [variant]

Owner, 2026-09-05: "u can't find a way to handle defects as most defects are repeated.. just that
its occurred in difference report layout".

That is exactly right, and it is a process failure rather than a knowledge one. By the time
R10.031 was verified there were fifteen passes in tmp/, each detecting a defect class that had
already cost a review round on an earlier report - and I was still finding them one at a time,
per report, when the owner pointed at them. The classes were known. They were simply never all
run at once.

So this runs all of them in REPORT mode - nothing is applied - plus the 14-check gate, and prints
one consolidated inventory. The point is to know the whole list BEFORE fixing anything, so a
report goes to the owner once rather than eight times.

    py tmp/r10_audit.py R10.034            # the inventory
    ...fix...
    py tmp/r10_audit.py R10.034            # confirm it is empty

Each entry names the pass that fixes it, so the inventory doubles as the work list.
"""
import os
import re
import subprocess
import sys

TMP = os.path.dirname(os.path.abspath(__file__))
BASE = r"C:\Projects\INPEX\sources\CrystalReports"
rep = sys.argv[1]
variant = next((x for x in sys.argv[2:] if not x.startswith("--")), None)

# every pass that DETECTS a class, with the line its report mode prints when it finds something
CHECKS = [
    ("r10_missingcells.py", "columns with text but no cell", ["--band=detail", "--force"]),
    ("r10_headergaps.py", "gaps in a header row", []),
    ("r10_headermerge.py", "sub-row cell inside a merged column", []),
    ("r10_headeralign.py", "sub-row not aligned to the merged row", []),
    ("r10_fillunder.py", "a fill painted over what it should sit under", []),
    ("r10_borderontop.py", "a border painted over by an opaque fill", []),
    ("r10_closegaps.py", "cells not meeting their neighbour", []),
    ("r10_trimoverlap.py", "cells overlapping their neighbour", ["--push", "--maxov=6"]),
    ("r10_rowbottom.py", "row cells with different bottom edges", []),
    ("r10_rowstyle.py", "a header cell the wrong colour for its row", []),
    ("r10_flatcells.py", "cells collapsed to a line", []),
    ("r10_spuriouscells.py", "cells the original has no counterpart for", []),
    ("r10_infocells.py", "info-block rows disagreeing on their shape", []),
    ("r10_inforow.py", "info rows or value cells missing", []),
    ("r10_infoconsistent.py", "info rows disagreeing with their siblings", []),
    ("r10_restorefill.py", "captions with no background left", []),
    ("r10_textfill.py", "text painting its own background over a cell", []),
    ("r10_strokelast.py", "a cell's border drawn before its fill", []),
    ("r10_onestroke.py", "a boundary stroked twice", []),
    ("r10_rulefix.py", "a rule missing or the wrong weight", []),
    ("r10_remarks.py", "the Remarks section", []),
    ("r10_subtitle.py", "the subtitle line under the title", []),
    ("r10_capalign.py", "captions aligned differently from the original", []),
    ("r10_dataalign.py", "data columns not on the header's grid", []),
]
NUM = re.compile(r'^\s{2,}(\d+) ')

print("=" * 78)
print("AUDIT  %s%s" % (rep, (" " + variant) if variant else ""))
print("=" * 78)
findings, clean, failed = [], [], []
for name, what, extra in CHECKS:
    p = os.path.join(TMP, name)
    if not os.path.exists(p):
        continue
    cmd = ["py", p, rep] + ([variant] if variant else []) + extra
    env = dict(os.environ)
    env["R10REP"] = rep                       # r10_subtitle.py takes its report this way
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=TMP, env=env)
    out = (r.stdout or "")
    if r.returncode:
        failed.append((name, (r.stderr or out).strip().splitlines()[-1][:80] if
                       (r.stderr or out).strip() else "no output"))
        continue
    # Count only lines that report FINDINGS. The passes also print diagnostics that begin with
    # a number - "30 cell span(s) measured in the original", "17 data column(s) paired..." - and
    # counting those made the audit report 30 findings for a pass that had found none. An audit
    # that miscounts is worse than no audit: it sends you looking for defects that are not there.
    NOISE = ("measured", "span(s)", "borderless", "paired", "grid:", "following the row",
             "page(s)", "header grid", "left alone", "outside", "skipped")
    n = 0
    for ln in out.splitlines():
        if any(w in ln for w in NOISE):
            continue
        m = NUM.match(ln)
        if m and "0" != m.group(1):
            n = max(n, int(m.group(1)))
    if n:
        findings.append((name, what, n))
    else:
        clean.append(name)

print("\nFINDINGS  (%d class(es) with something to fix)" % len(findings))
for name, what, n in findings:
    print("   %-24s %-46s %d" % (name[4:-3], what, n))
if failed:
    print("\nCOULD NOT RUN  (%d)" % len(failed))
    for name, why in failed:
        print("   %-24s %s" % (name[4:-3], why))
print("\nCLEAN  (%d): %s" % (len(clean), ", ".join(c[4:-3] for c in clean)))

print("\n" + "=" * 78)
print("GATE")
print("=" * 78)
g = subprocess.run(["py", os.path.join(TMP, "r10_verify_layout.py"), rep],
                   capture_output=True, text=True, cwd=TMP)
print((g.stdout or g.stderr).strip())
