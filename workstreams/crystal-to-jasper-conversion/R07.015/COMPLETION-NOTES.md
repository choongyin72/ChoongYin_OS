# R07.015 — PC Production Report — Completion Notes (2026-08-30)

**Phase:** LAYOUT ONLY (data queries deferred, same as R07.016 — see that report's notes for
the standing convention: placeholder query never executed, `JREmptyDataSource` fill).

**Build location:** `C:\Projects\INPEX\sources\CrystalReports\R07.015\output\`. **Base:**
copied R07.016's JRXML (closest existing single-page flat-grid structure), then substantially
rebuilt for this report's different shape.

## Why this report is structurally different (found via direct recon, not assumed)
- **9 flat columns**, not R07.016's 10: Date, Production*, Inventory*, then 3 group-pairs
  (Liftings INPEX/TOTAL, Daily Entitlements INPEX/TOTAL, Lifting Position INPEX/TOTAL) — no
  Cargo ID/Vessel/Lifting Status columns at all (this report has no per-cargo detail).
- **No separate "Opening Inventory" columnHeader row** — confirmed via grid-line extraction
  that the reference's first row after column headers is the first real detail row (01-07-2025)
  directly, with zero fill/pen rects in that y-band. This concept instead appears as one row
  inside a different, unique block described below. Verifying this via `get_drawings()` before
  building — rather than assuming R07.016's columnHeader pattern carried over — avoided
  building a phantom row that doesn't exist in this report.
- **A static 6-row "Overall" recap block** below the Total row, reusing the Production*/
  Inventory*/Liftings-INPEX/Liftings-TOTAL column x-positions with its own mini header
  ("Overall"/"INPEX"/"TOTAL") and 6 labeled rows: Opening Inventory, Monthly Production, Monthly
  Liftings, Cumulative Production, Cumulative Liftings, Closing Inventory. Not present in any
  report built so far this batch. Modeled as parameters (placeholder values) since Cumulative
  figures span prior months and aren't derivable from this report's own daily query.

## Verification performed
- All 9 column-header x-positions measured directly from the reference PDF's own vertical
  grid-line/fill-rect drawings (ground truth) before building — applying the R07.016 lesson
  (never split a combined-width span by estimation) up front instead of discovering a mis-split
  after the first render.
- Post-build comparison (rotation-corrected, per `JASPERREPORT-7-0-3.MD` Part D4) confirmed all
  9 column-header positions, the Total row, and the "Overall" block's label/column positions
  match the reference within ~1.5pt — no iteration needed this time.
- Total row: matches reference's own 5 populated sums (Production*, Liftings INPEX/TOTAL, Daily
  Entitlements INPEX/TOTAL); Inventory* and both Lifting Position columns confirmed genuinely
  blank (running-balance figures, not summable) — cross-checked against the reference's actual
  Total-row text spans, not assumed from convention.

## Not done this phase (by design)
- Live query/data verification — deferred, same as R07.016.
- The "Overall" block's 18 placeholder parameters (`P_OA_*`) need real values/derivation logic
  once the data-query stage begins — likely a separate cumulative-tracking query or a
  different table entirely, since cumulative figures aren't within a single month's data.

## Key takeaway
Measuring the reference PDF's real grid lines BEFORE writing any column x/width (not after a
failed render) avoided repeating R07.016's Date/Production* mis-split mistake — this report's
9-column grid matched the reference within ~1.5pt on the first build attempt.
