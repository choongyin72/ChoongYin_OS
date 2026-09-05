# R07.021 — PC PLP Production Forecast Report — Completion Notes (2026-08-30)

**Phase:** LAYOUT ONLY (data queries deferred). Sixth and final multi-page report in the R07
batch — reuses R07.018's page-per-month mechanism verbatim; main-grid shape combines R07.015's
flat (no Propane/Butane split) 3-group structure with the multi-page pattern.

**Build location:** `C:\Projects\INPEX\sources\CrystalReports\R07.021\output\`. **Base:**
copied R07.015's JRXML, extended with the page-per-month mechanism.

## Report shape (measured directly)
- Flat 9-column header (Date+Production*+Inventory* combined under one "Publish Date" banner,
  matching R07.018/020/022's convention — NOT R07.019's 3-separate-cell convention; each
  report's Row-A structure genuinely needs checking, confirmed here rather than assumed).
- 3 group blocks (Liftings, Daily Entitlements, Lifting Position), each INPEX/TOTAL only (no
  Propane/Butane split, matching R07.015).
- No per-month Opening Inventory row (same as R07.017/019).
- Total row: Production*, Liftings-INPEX/TOTAL, Daily Entitlements-INPEX/TOTAL summed (5
  populated values); Inventory* and Lifting Position (INPEX/TOTAL) genuinely blank.
- Bottom recap block: 4 rows (Opening Inventory, Monthly Production, Monthly Liftings, Closing
  Inventory) × 3 columns (Overall/INPEX/TOTAL) — confirmed via direct grid-line measurement
  that this report's Overall block DOES reuse the main grid's own Production*/Inventory*/
  Liftings-INPEX/Liftings-TOTAL column x-positions directly (unlike R07.013/019, whose Overall
  blocks used independent narrower grids). Applied the standing lesson (never assume reuse-vs-
  independent from a sibling report) and measured this report's own Overall block before
  building — confirmed reuse, first attempt landed within tolerance with no rework needed.

## No iteration needed this time
Unlike R07.019 (which repeated the R07.020 missing-label mistake) and R07.017 (systematic
column offset), this report's first render matched the reference closely on every measured
column (~5-8pt, well within the established tolerance) with no post-render fixes required —
attributed to explicitly re-verifying, before writing any JRXML, both (a) whether Production*/
Inventory* have visible labels here (yes — added them from the start) and (b) whether the
Overall block reuses the main grid or uses its own grid (measured directly — confirmed reuse).

## Verification performed
- All header columns and the Overall block's column reuse measured directly from the reference
  PDF's own grid-line/fill-rect drawings before building.
- Confirmed via the same 2-month synthetic data source technique as prior multi-page reports
  that the title block correctly repeats on page 2.

## Not done this phase (by design)
- Live query/data verification — deferred, same as prior R07 batch reports.
- 12 placeholder parameters (`P_OA_*`, 4 rows × 3 columns) need real values/derivation logic.

## R07 batch complete
This is the 10th and final report in the confirmed R07 batch order (R07.016 → 015 → 013 → 011
→ 018 → 020 → 022 → 017 → 019 → 021). All 10 reports built, layout-verified against their own
reference PDFs, and backed up. Per the owner's sequencing instruction, the R10 batch (15
reports) begins next.

## Owner border/layout review pass (2026-08-30, later same day, unsupervised — owner offline)
Same 4 checklist defects as the rest of the batch, plus the corner-cell purple-fill convention
(owner authorized applying this proactively per established pattern before going offline):

1. **Font jar / `leftPen` / double-border (`topPen`+`bottomPen`) / bare pens (16)** — same 4
   fixes as every prior report this session.
2. **Corner cell above the row-label column filled purple** to match "Overall"'s color — single
   cell (this report's recap header is 1 row, no Propane/Butane sub-row), same deliberate
   deviation from the reference already applied on R07.011/013/015/017/019. Confirmed via
   `get_drawings()` that the reference genuinely leaves this blank (no border extends up from
   the row-label column into the header row) before applying the fill.

Verified via direct measurement: fonts embedded, zero bare pens remaining, no doubled border
lines, corner-cell fill color matches "Overall"'s own purple exactly.

**Status: report layout verified (2026-08-30). Data queries deferred to a later stage**, same
convention as the rest of the R07.011-022 batch.
