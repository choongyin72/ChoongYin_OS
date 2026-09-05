# R07.022 — PC Provisional Lifting Program — Completion Notes (2026-08-30)

**Phase:** LAYOUT ONLY (data queries deferred). Third multi-page report — reuses R07.018's
page-per-month mechanism and title-merge fix verbatim, and applies the R07.020 lesson (Top
vertical alignment for row-merged header text) proactively from the first draft.

**Build location:** `C:\Projects\INPEX\sources\CrystalReports\R07.022\output\`. **Base:**
copied R07.018's JRXML, header/columns adapted to R07.016's flat (no Propane/Butane split)
2-group INPEX/TOTAL pattern.

## Report shape (measured directly)
- Flat 2-row header (no Row C, unlike R07.020's LPG version): Row A groups (Publish Date
  banner spanning Date+Production*+Inventory*, "Liftings (BBL)", "Liftings (MT)", blank
  cargo-detail cell), Row B (Date/Production*/Inventory*/INPEX/TOTAL ×2 groups/6 cargo-detail
  columns, all single-level — no Propane/Butane split at all).
- Same 6 cargo-detail columns as R07.020 (Cargo ID, Vessel, Arrival Date Range, ADR Status,
  Loading Date Range, LDR Status — no Representative column).
- Total row: Production* and both Liftings(BBL) columns (INPEX/TOTAL) summed; Inventory*,
  Liftings(MT) columns, and cargo-detail columns genuinely blank.

## First clean build this batch — no defects found
Unlike R07.020 (which needed a post-render fix for row-merged text alignment and missing
Production*/Inventory* labels), this report's first render matched the reference within the
same ~5-15pt caption-text tolerance on every column, with Opening Inventory's value (224,231)
matching exactly. Applying the R07.020 lesson proactively (Top alignment for all row-merged
header text, explicit Production*/Inventory* labels rather than assuming a blank continuation
cell) avoided repeating that report's mistakes here.

## Verification performed
- All header columns measured directly from the reference PDF's own grid-line/fill-rect
  drawings before building.
- Confirmed via the same 2-month synthetic data source technique as R07.018/020 that the title
  block and Opening Inventory group header both correctly repeat on page 2.

## Not done this phase (by design)
- Live query/data verification — deferred, same as prior R07 batch reports.
- Real Opening-Inventory carry-forward logic — placeholder field only.

## Key takeaway
The multi-page "Provisional Lifting Program" sub-family's mechanics (page-per-month, title
merge, Top-aligned row-merged captions) are now stable and proven across 3 reports (FC/LPG/PC
variants) — the remaining reports in this sub-family (R07.017/019/021, forecast-style variants)
should be buildable with the same recipe, still measuring each one's own column widths/labels
directly rather than assuming they match.

## Owner border/layout review pass (2026-08-30, later same day, unsupervised — owner offline)
Same checklist defects as the rest of the batch, plus a genuine correction to this report's own
"first clean build" claim above — proving that even a report that looked correct on caption-text
tolerance can still have a real data-binding defect that only word-level extraction catches:

1. **Font jar / `leftPen` / double-border (`topPen`+`bottomPen`) / bare pens (18)** — same 4
   fixes as every prior report this session.
2. **Total row's summed-vs-blank pattern was WRONG** (correcting item 21 above/the original
   header comment's own claim of "both Liftings(BBL) columns summed; Liftings(MT)...genuinely
   blank"). Word-level text extraction, cross-checked against the header's own INPEX/TOTAL
   column x-positions, found the reference's real Total row is: Production*=summed,
   Liftings(BBL)-INPEX=summed, **Liftings(BBL)-TOTAL=blank**, **Liftings(MT)-INPEX=summed**,
   Liftings(MT)-TOTAL=blank — the opposite of what the original build assumed for the BBL-TOTAL/
   MT-INPEX pair. Removed the wrong `V_LIFTBBL_TOTAL_TOTAL` sum, added a new
   `V_LIFTMT_INPEX_TOTAL` variable, and rebuilt the Total row's 6 data cells to match. **Lesson:
   a report "matching the reference within caption-text tolerance" says nothing about whether
   its DATA-BINDING pattern (which cells sum vs. stay blank) is correct — that needs its own
   explicit word-level verification, not just column-position matching.**
3. **Remarks box resized + repositioned + bordered**: measured all 4 months (8.9pt Aug/Sep/Nov,
   27.3pt Oct) — resized from height=24 to 35, label gap increased from 2pt to 10pt (matching
   the reference's own measured gap), text placed in a bordered cell spanning the full 1140pt
   grid width (same R07.018/020 pattern).
4. **Row B top-alignment padding**: all 13 Top-aligned Row B header cells (Date/Production*/
   Inventory*/INPEX×2/TOTAL×2/6 cargo columns) were flush against the top border — added
   `topPadding="3"` to all of them, matching the established convention from R07.019/020.

**Status: report layout verified (2026-08-30). Data queries deferred to a later stage**, same
convention as the rest of the R07.011-022 batch.
