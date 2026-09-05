# R10.003 — Monthly LPG Contract Price — rebuild notes (2026-09-04)

## ✅ OWNER-VERIFIED COMPLETE (2026-09-04)
*"Done for R10.003 report layout... its OK with Original Crystal Report Layout."*

## Type 2 applied (owner screenshot, 2026-09-04) — both DEVIATE FROM CRYSTAL
1. **The `1` removed from the info-block's third purple cell.** Owner: *"No wordings here."*
   That was `$P{P_REVISION}`, which the reference DOES render (abs x=284.8, white bold-italic
   on purple). The purple cell is retained; only the text was dropped.
2. **The 2.8pt purple sliver removed** before the `Contract Price*` row, leaving a clean
   full-width gap with a borderline either side. Crystal draws that sliver at abs y=373.1.

Owner has now requested the sliver removal on R10.001, R10.002 and R10.003, so it is treated
as STANDING for the remaining reports — still recorded per report as a deviation. Stray
report-specific content like the `1` is NOT generalised and stays flagged individually.

## Buyer-name item — superseded
The `Singapo` truncation difference was raised as an open item but the owner has since signed
the layout off, so ours (clean word break, text inside the cell) stands. Crystal cuts mid-word
and overflows into the neighbouring cell. Same situation exists on R10.007.

Rebuilt against `crytsal report in pdf/R10.003 - Monthly LPG Contract Price.pdf`.
Files: `output/R10_003_Monthly_LPG_Contract_Price.jrxml` + `.pdf`.
Backup: `*.backup_20260904_rebuild`.

## Verification
| Check | Result |
|---|---|
| pages / images | 1/1 · 1/1 |
| embedded fonts | 18 BoldItalic / 15 Plain / 6 Bold — **exact match** |
| span positions | **0 of 39** off at 1.5pt; dx=0 for 36, −1 for 2 |
| font/size mismatches | 0 |
| words | 1 difference — see the open item below |

## Type 1 — defects against the reference (all fixed)
Systemic set as R10.001/002: no font jar, zero italics, sizes 8.0/16/7.0 → 9.0/18/8.0, purple
`#444080` → `#444088`, no logo, no footer rule, footer missing its second line, white-pen bug
(33 pens), info-block values wrongly tinted `#F8FBFC` instead of unfilled white.

**Report-specific, and the largest defect of the three reports so far:**

1. **The formula text was 32pt out of place — rendered ABOVE its own label.**
   Built at `y=196`, while its `Price Formula` label sits at `y=214` and the bordered box at
   `y=228`. The reference puts the formula INSIDE the box: abs y=259.7 → local 231.7. It was
   also `PlainLabelStyle` at 8.0 where the reference is **`Arial-BoldMT` at 12.0**.
2. **`Price Formula` is `Arial-BoldMT`** — bold, NOT italic — while
   `Price Formula Components (per MT)` right below it IS BoldItalic. Two adjacent labels with
   different emphasis; a single shared style gets one of them wrong.
3. **`$P{P_REVISION}` was in the wrong column.** Built into the 4th column at x=383; the
   reference has it at abs x=284.8 = local 256.8, i.e. inside the **purple label cell** at
   x=255, white bold-italic, with the 4th column EMPTY. Odd content for a label cell, but
   that is what Crystal does.
4. **Comments box was 38pt too short** — built h=94 w=539; measured h=132.1 w=537.1. The title
   band had to grow 540 → 576 to hold it.
5. **The footnote had an inline `fontSize="6.5"`** where the reference is 9.0 BoldItalic.
6. Missing 2.8pt filler at local y=345 (abs 373.1) before the Contract Price row.

## 🔶 OPEN ITEM for the owner — buyer name truncation
The only word-level difference, and both versions are arguably wrong:

| | renders |
|---|---|
| reference (Crystal) | `INPEX Energy Trading Singapo` — clipped **mid-word**, and it visibly **overflows** past its cell into the neighbouring purple `Status` cell |
| ours | `INPEX Energy Trading` — JasperReports breaks at the last whole word and stays inside the cell |

`P_BUYER` is `"INPEX Energy Trading Singapore"`; the column is ~125pt, which cannot hold it at
9.0pt. So Crystal spills and cuts mid-word, JasperReports truncates cleanly.

Three options, owner's call — this is a type-2 judgement:
1. keep ours (cleaner, stays inside the cell) — **my recommendation**
2. match Crystal's mid-word cut and overflow
3. widen the Buyer value column, or shrink that field's font, so the full name fits

Not changed pending direction.

## Residual border-audit flags
Vertical flags cluster in x=36–155, which is the Buyer row where the reference's overflowing
text crosses a cell boundary and ours does not — a consequence of the item above, not a
separate defect. `EXTRA 74.64` is the logo raster's edge. `MISSING 798.24 / EXTRA 799.68` is
the footer TEXT row detected as a rule, 1.4pt apart and inside the span tolerance already
passed.

## Type 2 — none applied
R10.001's three presentation changes were NOT carried here (owner ruled type-2 is per report).
The 2.8pt filler is present because Crystal has it.
