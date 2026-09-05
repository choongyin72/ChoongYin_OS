"""The four defects the owner raised on R10.034, each measured against the original first.

    py tmp/r10_034_fix.py [--apply]

Every target below is the ORIGINAL's own geometry, read by tmp/r10_034_probe.py, not a
heuristic. The original's page y maps to jrxml y as (page - 25): the detail band starts 25pt
down, which is why the info block's jrxml y=111 renders at page 136.

1. EXTRA BORDERLINE beside "Date of Issuance"
   The info block's first row carries TWO value cells - x 194..497 and x 194..551 - while rows
   2..5 carry only x 194..497. The wide one draws the box to the right of the value that the
   owner circled. Remove it.

2. NO GAP before "ACQ after adjustment (Base ACQ)"
   In the original the first table's rows sit 0.5pt apart, EXCEPT before the last row, where it
   leaves 3.8pt:
        297.1 .. 312.8   +/- Round-Up/Down Quantity scheduled
        316.6 .. 334.0   ACQ after adjustment (Base ACQ)      <- 3.8pt of white above it
   Our build has that row at y=271 h=19, so 271+19 = 290 = the next row's y: dead flush, no gap
   at all. Reducing it to h=15 leaves 4pt, across BOTH columns - owner: "across the whole table".

3. ROWS 2, 4 and 5 of the AACQ table are built differently from 1, 3 and 6
        row 1 (y=360)   x=2 w=15 teal   x=17 w=248 teal   x=265 w=78 white   <- renders
        row 2 (y=374)   x=0 w=551 ValueCellStyle           x=4 w=10 navy     <- wrong
   The labels are white text on a transparent style, which is correct on a teal cell and
   invisible on a white one. That is also why their numbers show as navy chips, their labels are
   cut short ("Make-Up LNG Quantity scheduled in the Contract Year" in a 193pt box against the
   245pt its siblings get) and their values sit 22pt right of the column.

   The owner confirmed the three labels, which match what is already in the file:
        2  Make-Up LNG Quantity scheduled in the Contract Year
        4  Force Majeure Restoration Quantity scheduled in Contract Year
        5  UQT scheduled in the Contract Year
   so nothing needs retyping - only the cells behind them and the x they sit at.

4. MISSING CELLS under [Quantity Actually Delivered] and [Balance]
   The original draws FIVE cells on every data row of that table:
        x 1.6..16.7   13.2..264.5   265.6..342.0   342.9..419.2   420.0..496.3
   Our build draws the first three at most, so those two columns render as open gaps on all
   seven rows. Owner: "the data columns for [Quantity Actually Delivered] and [Balance] columns
   dont have completed borderlines". The widths come from the build's OWN header cells
   (265 w78, 343 w77, 420 w76) so the data lands on the header's grid.

5. "Remarks:" painted on a navy bar
   Our build gives the label a Band454087 rectangle - a navy fill - so it reads as a dark chip.
   The original has a plain label and then an empty box below it:
        label   page y 707.8 .. 717.9   (no rectangle at all)
        box     page y 718.7 .. 740.9   x 1.1 .. 497.2   (w 496, h 22)
   So the navy rectangle goes, and the box is added under the label.
"""
import os
import re
import sys

BASE = r"C:\Projects\INPEX\sources\CrystalReports"
S = os.path.join(BASE, "R10.034", "output")
FN = [f for f in sorted(os.listdir(S)) if f.endswith(".jrxml") and "backup" not in f][0]
path = os.path.join(S, FN)
t = orig = open(path, encoding="utf-8").read()
APPLY = "--apply" in sys.argv
ELEM = re.compile(r'<element\b[^>]*?/>|<element\b[^>]*?>.*?</element>', re.S)
CW = int(re.search(r'columnWidth="(\d+)"', t).group(1))
print("%s   columnWidth=%d" % (FN, CW))
done = []


def drop(pat, why):
    """Remove the single element matching pat."""
    global t
    hits = [s for s in ELEM.findall(t) if re.search(pat, s)]
    if len(hits) != 1:
        raise SystemExit("%s: expected 1 element for %s, found %d" % (why, pat, len(hits)))
    t = t.replace(hits[0], "", 1)
    done.append((why, "-1 element"))


def swap(old, new, why, n=1):
    global t
    if t.count(old) != n:
        raise SystemExit("%s: %r appears %d time(s), expected %d" % (why, old, t.count(old), n))
    t = t.replace(old, new, n)
    done.append((why, "%d edit(s)" % n))


# ---- 1. the extra value cell on the info block's first row
drop(r'kind="rectangle" x="194" y="111" width="357"', "1 extra borderline by Date of Issuance")

# ---- 2. a 4pt gap above "ACQ after adjustment (Base ACQ)", both columns
for x, w in ((2, 340), (342, 155)):
    swap('x="%d" y="271" width="%d" height="19"' % (x, w),
         'x="%d" y="271" width="%d" height="15"' % (x, w),
         "2 gap above ACQ after adjustment (x=%d)" % x)

# ---- 3 + 4. the AACQ table's data rows
# the three columns, taken from the build's own header row so data sits on the header grid
COLS = ((265, 78), (343, 77), (420, 76))
BROKEN = (374, 402, 416)                       # rows 2, 4, 5
GOOD = (360, 388, 430)                         # rows 1, 3, 6
TOTAL = 449
TEAL = ('<element kind="rectangle" x="%d" y="%d" width="%d" height="%d" style="Band0091B5">'
        '<pen lineWidth="1.0" lineColor="#D6D6D6"/></element>')
WHITE = ('<element kind="rectangle" x="%d" y="%d" width="%d" height="%d" style="CellFFFFFFB">'
         '<pen lineWidth="1.0" lineColor="#D6D6D6"/></element>')
add = []
for ry in BROKEN:
    # the wrong cells go
    drop(r'kind="rectangle" x="0" y="%d" width="551"' % ry, "3 full-width white cell y=%d" % ry)
    drop(r'kind="rectangle" x="4" y="%d" width="10"' % ry, "3 navy number chip y=%d" % ry)
    # the sibling rows' cells arrive
    add.append(TEAL % (2, ry, 15, 14))
    add.append(TEAL % (17, ry, 248, 14))
    # The LABEL first, and identified by being the WIDE staticText on the row. Doing the number
    # first and then taking "the first staticText at this y" picked up the number AGAIN - it had
    # just become x="1" width="16" - so the number was moved into the label's slot and the label
    # was left at x=26 width=193, where "Year" fell off the end of "...the Contract Year".
    lm = re.search(r'kind="staticText" x="(\d+)" y="%d" width="(\d{3})"' % ry, t)
    if not lm:
        raise SystemExit("no wide staticText (the label) on row y=%d" % ry)
    swap('x="%s" y="%d" width="%s"' % (lm.group(1), ry, lm.group(2)),
         'x="20" y="%d" width="245"' % ry, "3 label text y=%d" % ry)
    swap('x="4" y="%d" width="10"' % ry, 'x="1" y="%d" width="16"' % ry,
         "3 number text y=%d" % ry)
    # and the two right-hand values come back onto the column grid
    for old_x, (nx, _nw) in zip((365, 442), COLS[1:]):
        fm = re.search(r'kind="textField" x="%d" y="%d" width="(\d+)"' % (old_x, ry), t)
        swap('x="%d" y="%d" width="%s"' % (old_x, ry, fm.group(1)),
             'x="%d" y="%d" width="74"' % (nx, ry), "3 value x=%d y=%d" % (old_x, ry))

# every data row gets the cells the original draws - the ones already present are left alone
for ry, rh in [(y, 16 if y == 360 else 14) for y in GOOD] + \
              [(y, 14) for y in BROKEN] + [(TOTAL, 14)]:
    for cx, cw in COLS:
        if re.search(r'kind="rectangle" x="%d" y="%d"' % (cx, ry), t):
            continue
        add.append(WHITE % (cx, ry, cw, rh))

# ---- 5. Remarks: plain label, empty box below
drop(r'kind="rectangle" x="1" y="679" width="149"', "5 navy bar behind Remarks:")
add.append('<element kind="rectangle" x="1" y="694" width="496" height="22" '
           'style="CellFFFFFFB"><pen lineWidth="1.0" lineColor="#D6D6D6"/></element>')

# everything added goes in FIRST, so a cell is painted UNDER the text it sits behind
anchor = re.search(r'(\n\s*)<element kind="rectangle" x="2" y="360"', t)
t = t[:anchor.start(1)] + "".join("\n            " + a for a in add) + t[anchor.start(1):]
done.append(("cells added", "%d element(s)" % len(add)))

# ---- guards
if re.search(r'\b(x|y|width|height)="\d+\.\d+"', t):
    raise SystemExit("decimal coordinate introduced (Part Z9)")
T0 = sorted(x for x in re.findall(r'<!\[CDATA\[(.*?)\]\]>', orig, re.S) if x.strip())
T1 = sorted(x for x in re.findall(r'<!\[CDATA\[(.*?)\]\]>', t, re.S) if x.strip())
if T0 != T1:
    raise SystemExit("text changed - this pass never edits text, only cells and positions")
bh = int(re.search(r'<detail>\s*<band height="(\d+)"', t, re.S).group(1))
body = re.search(r'<detail>\s*<band height="\d+"[^>]*>(.*?)</band>\s*</detail>', t, re.S).group(1)
for s in ELEM.findall(body):
    def a(k):
        m = re.search(r'\b%s="(-?\d+)"' % k, s)
        return int(m.group(1)) if m else None
    y, h, x, w = a("y"), a("height"), a("x"), a("width")
    if None not in (y, h) and y + h > bh:
        raise SystemExit("y=%d h=%d overflows the %dpt detail band" % (y, h, bh))
    if None not in (x, w) and x + w > CW:
        raise SystemExit("x=%d w=%d exceeds columnWidth %d" % (x, w, CW))
# each rebuilt row must end up with the number AND the label in their sibling slots - this is
# the guard that would have caught the number being moved into the label's place
for ry in BROKEN:
    for x, w, what in ((1, 16, "number"), (20, 245, "label")):
        n = len(re.findall(r'kind="staticText" x="%d" y="%d" width="%d"' % (x, ry, w), t))
        if n != 1:
            raise SystemExit("row y=%d has %d %s text at x=%d w=%d, expected 1"
                             % (ry, n, what, x, w))

# no data row may still be missing a column cell
for ry in GOOD + BROKEN + (TOTAL,):
    miss = [cx for cx, _ in COLS if not re.search(r'kind="rectangle" x="%d" y="%d"' % (cx, ry), t)]
    if miss:
        raise SystemExit("row y=%d still has no cell at x=%s" % (ry, miss))
print("   guard: no decimals, text unchanged, nothing overflows, every data row has 3 cells")

for why, what in done:
    print("   %-46s %s" % (why, what))
print("   %d -> %d bytes" % (len(orig), len(t)))

if not APPLY:
    print("   report only - rerun with --apply")
else:
    b = path + ".backup_20260905_pre034fix"
    if not os.path.exists(b):
        open(b, "w", encoding="utf-8").write(orig)
        print("   backup: %s" % os.path.basename(b))
    open(path, "w", encoding="utf-8").write(t)
    print("   applied")
