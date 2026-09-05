"""Re-run the whole fix chain on every report/variant, then regenerate.

    py tmp/r10_chain.py [--apply]

TWICE NOW the owner has found a defect whose fix I already owned but had not re-run:

    R10.029  r10_dedupeborders.py was built while fixing R10.026 and only ever run on R10.026,
             so 216 text elements across the other seven still drew their own borders.
    R10.029  r10_textfill.py ran while the statement lived in `title`; after I moved it into a
             per-buyer `detail` band the MMBtu cell was again painting its own opaque fill,
             1pt wider and 2pt shorter than the rectangle under it - the notch the owner circled.

Both have the same shape: a fix is correct, is applied once, and then the report is restructured
or a sibling is never covered. The answer is not to remember - it is to have one command that
re-runs every fix over every file, so "did I re-run it?" is never a question I have to answer
from memory.

Order matters: sizes first (so gap-closing sees final geometry), then the layers that decide who
draws a border or a fill, then the pen.
"""
import os
import subprocess
import sys

BASE = r"C:\Projects\INPEX\sources\CrystalReports"
TMP = os.path.dirname(os.path.abspath(__file__))
APPLY = "--apply" in sys.argv

CHAIN = [
    # FIRST: a row's cell list must be right before anything reasons about that row
    ("r10_spuriouscells.py", "cells the original draws no counterpart for"),
    ("r10_fillmatch.py", "filled cell sizes taken from the original"),
    ("r10_textfill.py", "text that paints its own background over a rectangle"),
    ("r10_dedupeborders.py", "text that draws its own border over a rectangle"),
    ("r10_closegaps.py", "gaps between adjacent cells, both axes"),
    # after closegaps, which changes heights: two cells in a row with the same top and different
    # heights put a 1pt STEP in the rule under the row. Owner found four such rows on R10.029.
    # the mirror of closegaps: that pass only ever WIDENS a cell to meet its neighbour, so an
    # OVERLAP went unlooked-for. Owner found the label column crossing into the value column.
    ("r10_trimoverlap.py", "cells overlapping into their neighbour's column"),
    ("r10_rowbottom.py", "cells in a row whose bottom edges do not line up"),
    ("r10_rightedge.py", "rows falling short of the table's right edge"),
    # after rightedge: moving a row's outer edge by 1pt puts the header and the data grid back
    # out of agreement with EACH OTHER, which is the "left borderline is not aligned" class
    ("r10_aligncols.py", "header columns snapped onto the data grid"),
    ("r10_bordercolour.py", "pen colour and width from the original"),
    # LAST, and it has to be: bordercolour gives EVERY rectangle an explicit pen, which is what
    # makes both members of a co-located fill+border pair stroke the same boundary.
    ("r10_onestroke.py", "co-located rectangles stroking the same boundary twice"),
    # LAST: pure reordering, so it settles who wins the half-pen after every geometry pass has
    # finished moving things. A cell's fill drawn after its border eats half the outer edge.
    ("r10_strokelast.py", "a cell's border drawn before its fill instead of after"),
]

# ---------------------------------------------------------------------------------------------
# OWNER-VERIFIED - NOT TO BE TOUCHED.
#
# The chain exists to apply every fix to every file, and on 2026-09-05 it did exactly that to
# R10.026 - a report the owner had already verified OK. Three of the changes were real defects
# and one was self-inflicted (moving the outer edge put the header and data grid 1pt out of
# agreement, which I then had to repair). None of that is the point. Owner: *"R10.026 is
# completed verify.. u make changes on it?"* and *"U should ask premission or request from me
# first...."*
#
# A verified report is finished. If a later fix appears to apply to one, it is brought to the
# owner as a REQUEST with the measurement, and the owner decides - the chain does not decide.
# Adding a name here is not a note to myself; it is the chain refusing to open the file.
VERIFIED = {"R10_026_Average_ACQ_Balance",                   # verified 2026-09-05
            "R10_029_AACQ_Notice_to_Buyer",                  # verified 2026-09-05
            "R10_030_ADP_SDS_FOB_Buyers_ADP_per_buyer",      # verified 2026-09-05
            "R10_030_ADP_SDS_FOB_Buyers_ADP_per_contract",   # verified 2026-09-05
            "R10_030_ADP_SDS_FOB_Buyers_SDS_per_buyer",      # verified 2026-09-05
            "R10_031_ADP_SDS_DES_Buyers_SDS",                # verified 2026-09-05
            "R10_031_ADP_SDS_DES_Buyers_ADP",                # verified 2026-09-05
            "R10_034_Annual_Quantity_Statement"}             # verified 2026-09-05

targets = []
for rep in sorted(d for d in os.listdir(BASE) if d.startswith("R10.0")):
    if not ("026" <= rep[4:] <= "034"):
        continue
    S = os.path.join(BASE, rep, "output")
    if not os.path.isdir(S):
        continue
    jrs = [f for f in sorted(os.listdir(S)) if f.endswith(".jrxml") and "backup" not in f]
    for f in jrs:
        # --include=<stem> overrides the guard for ONE named report, and says so loudly. It
        # exists so that running against a verified file is a deliberate, visible act with the
        # owner's name on it, rather than a quiet edit to the VERIFIED set above.
        if f[:-6] in VERIFIED and ("--include=" + f[:-6]) in sys.argv:
            print("   OVERRIDE  %-9s %-40s owner-verified, included by explicit request"
                  % (rep, f[:-6]))
        elif f[:-6] in VERIFIED:
            print("   SKIP  %-9s %-46s owner-verified - ask before changing it" % (rep, f[:-6]))
            continue
        targets.append((rep, f[:-6], f[:-6] if len(jrs) > 1 else None))
print("%d report file(s)\n" % len(targets))

fail = []
for rep, stem, variant in targets:
    print("=" * 74)
    print("%s  %s" % (rep, stem))
    for tool, what in CHAIN:
        cmd = ["py", os.path.join(TMP, tool), rep] + \
              ([variant] if variant else []) + (["--apply"] if APPLY else [])
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=TMP)
        out = (r.stdout or "").strip().splitlines()
        body = [ln for ln in out[1:] if ln.strip() and not ln.strip().startswith("guard:")]
        head = body[0].strip() if body else "(no change)"
        flag = "  ** " if r.returncode else "     "
        print("%s%-24s %s" % (flag, tool[4:-3], head[:96]))
        if r.returncode:
            fail.append((rep, stem, tool, (r.stderr or r.stdout).strip().splitlines()[-1][:120]))

if fail:
    print("\n%d tool run(s) failed:" % len(fail))
    for rep, stem, tool, msg in fail:
        print("   %-9s %-46s %-22s %s" % (rep, stem[:46], tool[4:-3], msg))
    raise SystemExit(1)

if APPLY:
    print("\n" + "=" * 74)
    print("REGENERATE")
    print("=" * 74)
    r = subprocess.run(["py", os.path.join(TMP, "r10_regen_26_34.py")],
                       capture_output=True, text=True, cwd=TMP)
    print((r.stdout or r.stderr).strip())
else:
    print("\nreport only - rerun with --apply")
