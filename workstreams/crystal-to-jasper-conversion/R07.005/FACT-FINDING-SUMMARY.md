# R07.005 — Offshore Production Report — Fact-Finding Summary (2026-09-01)

**Owner-verified OK, 2026-09-01.** How the defects were traced and fixed, what the root causes
were, and the mistakes I made.

**Files:** `C:\Projects\INPEX\sources\CrystalReports\R07.005\output\R07_005_Offshore_Production_Report.jrxml`
Reference: `crytsal report in pdf\R07.005 - Offshore Production Report.pdf`. 2 pages,
`<title>` = page 1 (lines 78-804), `<summary>` = page 2 (806-853). Phase: LAYOUT ONLY.

---

## 1. Result

| Check | Start | End |
|---|---|---|
| Gridline ink mismatches | 36 | 7 (sub-point) |
| Horizontal rule differences | 1 | **0** |
| Internal consistency (output vs itself) | 3 | **0** |
| Values in wrong column / alignment | 42 | **0** |
| Text differences | 0 | **0** |
| Font sizes | 86 texts wrong | **exact match** |

Owner reported the classes up front — "missing borderline, borderline not connected/aligned,
column header row not connected to data row, borderline thickness" — and then found five
further rounds of specifics by eye that my checks had passed.

---

## 2. Root causes

### 2.1 The report uses TWO base font sizes
The reference renders 471 spans at 8.0pt (the 30-well grid) **and** 101 at 9.0pt (every other
table). Mine had everything at 8.0. A blanket style change would have wrongly enlarged the well
grid, so each element's size was derived from its own reference span **by position**.

Two-stage, because text matching cannot place repeated values (`'0'`, `'4'`, `'41,253'`):
first by text+position (47 elements), then the remaining 49 by pure position, which showed they
all sat on page 1 between abs y 752 and 1094 — the block below the well grid.

Result: `6.0×6, 8.0×471, 9.0×101, 10.0×55, 11.0×2, 21.0×2` — identical to the reference.

### 2.2 The 30-well grid was on entirely wrong columns
```
reference : 23, 78, 136.5, 203.5, 252, 304.5, 356.5, 410.5, 470.5, 530.5, 580.5, 624.5, 669.5, 727.5, 770.5, 813
mine      : -2, 57, 114,   183,   [16pt hole] 246, 295, 347, 408, 464, 518, 570, 611, 661, 708, 754, 788
```
A 16pt hole after column 4 and a progressive drift up to 15pt from column 6 on. Header and
data rows agreed with each other, just not with the reference — so no internal check could see
it. 471 cells re-laid by mapping each cell's position in MY boundary list to the same index in
the reference's, which handled the three 12-cell totals rows (they skip columns 2-4) without
special-casing.

### 2.3 285 doubled column lines
Neighbouring cells not sharing an edge, so two 1pt strokes render as ~2pt. Plus **11 header
boundaries** that the first pass missed because header cells are `rectangle`/`HeaderCellBoxStyle`
and the pattern only matched `staticText`/`textField`. (Same miss as R07.004 — see §3.3.)

### 2.4 Well-grid columns 1-3 centred where the reference left-aligns them
Measured per column from the reference's own text offsets: cols 0-2 have left offsets of
3.6/3.3/1.6 against right offsets of 19.8/14.3/32.9 — unambiguously Left. Mine centred them:
a 15.1pt error on 29 cells.

### 2.5 Data rows not inheriting their table's columns
The lower table was inset 12pt (started at local 13 rather than 1) with a 1pt cell overlap that
double-drew the row line; the page-2 table's values sat in text-sized boxes floating inside
their columns, producing extra verticals at abs 415/485/655/725 where the reference has none.

### 2.6 Rows missing their empty bordered cells — and why it breaks the LINE
The 'Delivered' rows and the 'CPF gas buyback' row carried 4 cells where the others carried 6:
Short Term Forecast (328) and Annual Budget (556) did not exist at all.

**Why that shows up as a broken horizontal line, not just a missing box:** the `Plain*` styles
use `topPen 0`, so a row's top line is drawn by the row ABOVE's bottom border. With the cell
absent there is no bottom border either — so the horizontal line breaks into stubs and the
column vanishes for that row. That is exactly what the owner described as "a short horizontal
line stub".

### 2.7 Sub-heading rows overlapping the row below
```
'Production'  local 717 + height 14 -> bottom 731     next row starts 729
'Losses'      local 854 + height 14 -> bottom 868     next row starts 866
'Delivered'   local 908 + height 14 -> bottom 922     next row starts 920
```
Two horizontal lines 2pt apart with white between — the "narrow space gap".
'Internal Consumption' was already 813+13=826, which is why it looked right and the other
three did not.

### 2.8 A tall header cell stops the inter-header line crossing it
The label column's header was one cell spanning both header rows (`y=679 height=38`), so no
horizontal line crossed it and the inter-header line appeared to start partway across. The
reference draws that line the full table width. Split at local 692.

### 2.9 Header not joined to its body
Inventory, Liftings and both page-2 tables had their header ending 1-2pt above the first data
row. **The reference has the same gap** — fixed anyway, per the owner's standing rule, at the
cost of the purple band being 0.9-1.8pt taller than the reference's. Owner approved the
trade-off explicitly.

### 2.10 Label indentation
The reference indents each data-row label under its sub-heading: sub-headings at x=24.6, data
labels at x=38.8. Mine had both at 27.0 — no indent at all. **Every border check passed this**,
because the defect is text position inside correct boxes, and my value-position check had a
12pt tolerance while the error was 11.8pt. Threshold now 4.0.

---

## 3. My mistakes

1. **Assumed a style's font size instead of reading it.** My first font dry-run had
   `HeaderTextOverlayStyle` at 8.0; it is 10.0. That proposed changing 37 captions which were
   already correct. Caught only because I inspected before applying.
2. **Raising two totals to 8.0pt clipped their last digit** (`1,360,617` -> `1,360,61`) — 39pt
   of width with 1pt padding for 37.8pt of text (Part F1).
3. **Header `rectangle` elements missed twice** — once in the well-grid re-lay, once in the
   de-double pass. The same omission had already cost a round on R07.004. A pattern matching
   only text elements will always miss the header.
4. **Over-applied the Left-alignment fix** to the well-grid totals rows, which the reference
   centres.
5. **Ran the de-double pass too early** — before the well-grid and page-2 snapping, so those
   passes introduced new 1pt gaps that needed a second run.
6. **`sed` with backslash Windows paths silently did nothing**, twice, and I read a stale PDF
   both times before noticing. Use the Edit tool or a `GENPDF` env var.
7. **`py -` waits on stdin and times out.** Did it twice. Write the script to a file.
8. **The stale-PDF trap, repeatedly.** The output was open in the owner's viewer for much of
   the session; writes failed and the owner reviewed builds up to four generations behind.

---

## 4. What the owner had to find by eye, and why

| Owner found | Why every check missed it |
|---|---|
| Well-grid header edges 1pt inside the data rows | header elements are `rectangle`; my checks compared outer extents that happened to agree |
| Gas totals touching the right border | padding, not geometry - no check measured text-to-border distance |
| Label indentation | text position inside correct boxes; value-position tolerance was 12pt, error 11.8pt |
| Header not joined to body | the reference has the same gap, so a reference comparison passed it |
| Stub horizontal lines | missing cells: the boundary set still looked complete because neighbouring cells' pens supplied the verticals |
| Narrow gap at sub-headings | a 2pt row OVERLAP; my tiling passes only closed GAPS |

Every one is a checkable property. They are now checks.
