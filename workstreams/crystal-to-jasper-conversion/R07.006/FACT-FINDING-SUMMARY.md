# R07.006 — Onshore Production Report — Fact-Finding Summary (2026-09-01)

**Owner-verified OK, 2026-09-01** ("look OK and fine for R07.006 report layout").

**Files:** `C:\Projects\INPEX\sources\CrystalReports\R07.006\output\R07_006_Onshore_Production_Report.jrxml`
Reference: `crytsal report in pdf\R07.006 - Onshore Production Report.pdf`. 1 page,
`<title>` lines 53-571. Phase: LAYOUT ONLY.

---

## 1. Result

| Check | Start | End |
|---|---|---|
| Gridline ink mismatches | 31 | 7 (sub-point) |
| Internal consistency | 2 | **0** |
| Values in wrong column / alignment | 47 | **0** |
| Rule differences | 0 | **0** |
| Text differences | 0 | **0** |
| Font sizes | already exact | exact |

Fastest of the four reports, because the playbook from R07.003-005 applied almost unchanged.

---

## 2. What was structurally different about this report

**It defines NO styles.** Every element carries inline attributes (`fontName`, `bold`,
`fontSize`, `hTextAlign`...), and borders are separate `rectangle` elements with text in
separate `staticText` elements.

Two consequences:
- **Every style-based selector found nothing.** All the passes from earlier reports had to be
  re-keyed on `kind` + coordinates.
- **Tiling the borders was risk-free.** The rectangles hold no text, so shrinking them cannot
  trigger the Part F1 text drop — which meant a single pass could tile all 149 of them.

---

## 3. Root causes

### 3.1 Almost every row was 1pt off its pitch
`GAP 1` or `OVERLAP 1` on nearly every row, so every horizontal boundary carried two strokes
and rendered 1.92-2.04pt against the reference's 0.96pt. That was the owner's "borderline
thickness" and "not jointed properly". 149 rectangles tiled to their row pitch.

### 3.2 Border rectangles OVERLAPPED, putting a neighbour's border inside a column
The most interesting one. On a main-table data row:
```
4..187 | 185..273 | 268..359 | 355..446 | 446..532 | 530..618 | 616..704 | 699..784
        ^overlap 2  ^overlap 5  ^overlap 4  ^0        ^2        ^2        ^5
```
Column 2 is drawn 185..273 while column 3 starts at 268 — so **column 3's left border renders
five points inside column 2**. The owner reported this as "extra borderline shown in Monthly
Quantity - Volume, Mass, YTD Volume, YTD Mass, Annual Budget Forecast", and the varying overlap
(2/5/4/0/2/2/5) is why the thickness looked uneven across the table.

180 rectangles re-laid to tile on one boundary each. The table went from **15 rendered column
lines to 9** — one per column.

### 3.3 20 column boundaries with 1pt gaps
Inventory's and Liftings' header rects sat 1pt off their own data rows (header col2 at 299 where
the data rows use 298), so those verticals rendered ~2pt.

### 3.4 Inventory and Liftings values right-aligned where the reference centres them
22 values, up to 110pt out of position. Confirmed against the column centres:
Inventory col2 = 298..534, centre 416, reference value centre local 415.

### 3.5 Main-table labels not indented under their sub-headings
Reference: sub-headings x=27.3, data labels x=41.2. Mine: 27.0 and **29.0** — a 12.2pt shortfall
on 22 labels. Same class as R07.005 §2.10.

### 3.6 A duplicated value element
Row 'Liquid flare (m3)' had **two** value elements at the same x=268 with the same text '0';
one belonged in the Monthly Volume column at x=185. Only the tightened 4.0pt value-position
tolerance caught this.

### 3.7 Liftings section rule too close to its table
Two 1pt offsets compounding: my rule 0.85pt low and my header 1pt high, giving a 2.50pt gap
against the reference's 4.35pt. Rule up 1pt, header down 1pt with its height reduced by 1 so its
bottom still met the first data row and nothing below moved. Result 4.50pt.

### 3.8 Footer classification text centred 31pt off
Same defect as R07.004 and R07.005.

---

## 4. A deliberate deviation, owner-approved

The reference draws **two** lines at each main-table column boundary, 0.6-4.6pt apart, because
Crystal leaves a gap between adjacent cells rather than tiling them:
```
207.3/208.8   290.5/294.9   377.5/381.4   467.6/468.2   552.2/553.7   637.8/639.7   721.2/725.8
```
I tile to **one** line per boundary, positioned inside the reference's pair on every one. That
is the internally-consistent choice and is what the owner accepted on the three previous
reports. Offered to reproduce the doubled lines exactly; owner accepted the single line.

---

## 5. Remaining known items

7 sub-point ink mismatches: six purple-band edges at 0.48-0.6pt, and two verticals where the
reference is thinner than mine (abs 290: 0.12 vs 0.96) or thicker (abs 23: 3.48 vs 4.44).
