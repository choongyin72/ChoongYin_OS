# R07.004 — Daily Onshore Report — Fact-Finding Summary (2026-09-01)

How the defects were traced and fixed in the owner-driven review round, what the root causes
actually were, and the mistakes I made along the way.

**Files:** `C:\Projects\INPEX\sources\CrystalReports\R07.004\output\R07_004_Daily_Onshore_Report.jrxml`
(+ its compiled PDF). Reference: `crytsal report in pdf\R07.004 - Daily Onshore Report.pdf`.
2 pages. Phase: LAYOUT ONLY — data binding still deferred.

---

## 1. Where the round started

The owner reported two defect classes by eye: *"borderline missing"* and *"border thickness"*.
Running the checks promoted from R07.003 (`compare_ink.py`, `diag_all_lines.py`, `crop_sheet.py`)
reproduced both within a minute, plus a much larger one nobody had reported.

| Check | At start | At end |
|---|---|---|
| Horizontal rule differences | 16 | 0 |
| Gridline ink mismatches | 29 | 11 (all ≤0.66pt) |
| Text differences | 58 missing | 2 (one span-split item) |
| Values in wrong column / alignment | 15 real | 0 |
| Font sizes | 278 spans at 6.5pt | matches Crystal (9.0 / 10.0 / 6.0) |
| Table column boundaries | 8 of 11 wrong | all 11 match |
| Border joints | broken in 8 tables | closed |

---

## 2. Root causes

### 2.1 Document-wide font size (found by me, not reported)
All body text rendered at **6.5pt where Crystal uses 9.0pt**; column headers 6.5pt where
Crystal uses 10.0pt bold-italic; footer 7.0pt where Crystal uses 6.0pt italic.

Confirmed by rendered width, not just the reported size: `"Injury events"` is 51.1pt wide in
the reference and 36.8pt in mine — a ratio of 1.39, exactly 9.0 ÷ 6.5.

**Fixed before any geometry work**, because row height follows font size. Crystal's HSE rows
are 17pt to hold 9pt text; mine were 12pt holding 6.5pt text. Measuring borders first would
have meant redoing every table.

### 2.2 Data cells built from their text width, not the table's columns
The single biggest cause, behind seven of the reported defects. Every table's header was
correct; its data rows were not. Examples:

| Table | Header columns | Data-row boundaries |
|---|---|---|
| HSE | `0 \| 134 \| 187 \| 795` | `4..134`, `140..180`, `190..230` — no Comments cell at all |
| Gas Export Pipeline | `25 \| 129 \| 236 \| 344 \| 451 \| 538 \| 624` | `37 \| 117 \| 222 \| 322 \| 422 \| 512 \| 617` |
| Offtakes | ends 813 | ends **822** (overshoots the table) |
| Environmental t2 | `25 \| 241 \| 347 \| 454 \| 560 \| 667` | `26 \| 276 \| 355 \| 460 \| 565 \| 673` |

Each value sat in a box sized around the number, floating inside its column — so rows read as
detached rectangles, didn't reach the table's edges, and in places ran past them.

Fixed by snapping every data cell onto its own table's header boundaries and adding an empty
bordered cell wherever a column had none (Crystal draws one). 44 cells snapped, 9 added.

### 2.3 Rows shorter than their pitch — the unjoined corners
The owner's *"not jointed / not connected"*. Data cells were 12pt tall on a 13–14pt row pitch,
so **every row boundary had a 1.4–1.6pt band with no vertical border drawn**: the horizontal
line was there, the vertical stopped short of it, and the corner stayed open.

Measured by walking down a column boundary at 600 dpi and reporting each break:

| Table | Crystal | Before | After |
|---|---|---|---|
| Production | `[11.3, 11.3, 11.3]` (sub-headings) | `[10.9, 0.5, 1.6, 1.4, 1.4, 1.6]` | `[12.0, 10.9, 10.9]` |
| CCPP | `[1.7, 1.1]` | `[0.5, 0.5, 1.4, 1.4, 1.6, 1.4]` | `[0.5, 0.6]` |
| GEP | `[1.0]` | `[2.4, 1.4]` | `[1.4]` |
| POB | `[]` | `[0.6, 0.5, 1.6]` | `[0.6, 0.6]` |

Fixed by setting each cell's height to the distance to the next row in its own table, and
growing each table's first row upward to meet its header.

### 2.4 Left edges derived globally instead of per table
Crystal uses exactly two left edges: 23.1 for most tables and **25.1 for Production and Gas
Export Pipeline**. Mine used five different values (local 0, 1, 2, 3, 4).

### 2.5 Header captions never centred on the reference
28 captions were off by up to 43.8pt (`"Comments"`), 33.4pt (`"Name"`), 43.1pt
(`"Description"`).

### 2.6 Whole-page furniture missing or misplaced
The first section rule on each page was 12.6pt too high; every section title sat at local 0
where Crystal has them at 5 or 7; the footer rule was drawn **inside the content bands** at two
different heights (1098.5 on page 1, 1074.5 on page 2) instead of in `pageFooter` at 1138.7.

### 2.7 Environmental's section rule is SHORT in Crystal
Crystal draws it `24.6 → 527.5`, stopping at the width of the narrow table beneath it. Mine ran
the full page width.

### 2.8 The disclaimer
Crystal: left-aligned at x=22.6, 9.0pt, `"Disclaimer: "` in ArialBoldItalic and the body in
ArialItalic. Mine: one centred element at 192.6, 6.5pt, plain. Split into two elements, since
a JasperReports `staticText` carries a single font.

### 2.9 Header divider twice the body divider — a defect Crystal ALSO has
The last one the owner found, and the most instructive. Inventory's header divider rendered
**2.04pt** while every data-row divider below rendered **1.02pt**:

```
header row : 282.48 .. 284.46  = 2.04pt  solid #D6D6D6
data row   : 282.48 .. 283.44  = 1.02pt  solid #D6D6D6
```

Cause: the header cells sat at local `1..261` and `262..522`, leaving a 1pt gap, so **two**
separate 1pt strokes landed side by side at abs 283 and 284. The body cells share their edge,
so one stroke. Fixed by making the header cells share their edges on the body's own boundaries
(261 and 522).

**Crystal has the same 2pt header divider.** A reference comparison called this correct. The
owner judged it against the data row directly below it inside my own table — see §4.

---

## 3. My own mistakes in this round

1. **Raising the font size silently dropped 58 captions.** 10pt text in 10pt-tall boxes; the
   Part F1 rule fires the moment font size changes. Caught by the text-presence check.
2. **Snapping cells by nearest left edge mis-assigned Environmental t2's values** — all four
   moved one column right and two stacked in the same cell. Borders were perfect; the data was
   wrong. Assignment must be by ORDER.
3. **Tiling grouped rows by BAND, not by table.** Page 1's title band holds seven tables, so a
   table's last row measured its step against a neighbouring table's row and never grew. Half
   the gaps survived the pass.
4. **A style-scoped regex missed Production's sub-heading rows** (`SubSectionTitleStyle`, not
   `Plain*Style`), so the three gaps the owner circled survived two more passes.
5. **Centring a left-aligned caption pushed x negative** — `"POB"` rendered as `"B"`,
   `"Description"` as `"cription"`. Their boxes are far wider than their text.
6. **One global left-edge pass moved 18 Production elements the wrong way** — that table belongs
   to Crystal's *other* left edge (25.1, not 23.1).
7. **I diagnosed the Inventory header from a magnified crop and acted on it.** I concluded "the
   grey outline is missing", rebuilt all three cells as border + inset fill, and **introduced
   1.98pt of white into dividers that were already correct at 2.04pt**. Only caught by measuring
   the pre-fix state. The outline was never missing; the band was 1pt short.
8. **The stale-PDF trap.** The output PDF was open in the owner's viewer for much of the round,
   so writes failed and the owner reviewed a file up to four builds behind — three of the
   defects raised were already fixed.

---

## 4. The standing rule this round produced

> **A defect counts even when the original has it.**

Two standards, not one: match Crystal, *and* be internally consistent. Where they conflict the
owner decides. On §2.9 a pure reference comparison would have preserved the flaw.

This exposed a structural gap: every check in `_checks/` compared the output to the reference,
so this class was invisible to all of them. `check_internal_consistency.py` now compares a
report against ITSELF — divider weights, row-line weights, uniformity within each table.

**Validated, not assumed:** run against the pre-fix build it reports the defect
(`2.04pt against a 1.02pt median` at the header row); against the current build it reports 0.

---

## 5. Order of work that actually worked

1. Fonts first — geometry depends on them
2. Snap data rows onto their own header's columns (per table, by order)
3. Tile rows to their pitch — per TABLE, grow only
4. Left edges per table, from the reference
5. Captions and alignment, measured individually
6. Page furniture — section rules, titles, footer
7. Then internal consistency, which no reference comparison can give you

At every step: re-measure before changing, and re-run the whole check set after — including a
text-presence check, because several geometry fixes silently drop text.
