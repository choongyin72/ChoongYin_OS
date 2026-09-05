# R07.019 — LPG PLP Production Forecast Report — Completion Notes (2026-08-30)

**Phase:** LAYOUT ONLY (data queries deferred). Fifth multi-page report — reuses R07.018's
page-per-month mechanism verbatim; main-grid shape combines R07.013's 3-row nested Propane/
Butane header (3 group blocks: Liftings/Daily Entitlements/Lifting Position) with the
multi-page pattern.

**Build location:** `C:\Projects\INPEX\sources\CrystalReports\R07.019\output\`. **Base:**
copied R07.013's JRXML, extended with the page-per-month mechanism.

## Report shape (measured directly)
- Date/Production*/Inventory* are 3 SEPARATE Row-A cells with visible labels — genuinely
  different from R07.013 (whose Row A had these as distinct cells too, confirming this
  convention) but critically different from R07.018/020/022 (whose Row A merges Date+Prod+Inv
  under one "Publish Date" banner). Each report in this family needs its own Row-A structure
  check.
- **Date column has a real 3-row internal structure**: Row A = "Publish Date" (label), Row B =
  "05 Aug 2025" (value), Row C = "Date" (the actual column header) — not a simple row-merge
  like Cargo ID/Vessel in other reports.
- No per-month Opening Inventory row (same as R07.017).
- Bottom recap block: 4 rows (Opening Position, Monthly Production, Monthly Liftings, Closing
  Position) × 3 mini-groups (Overall/INPEX/TOTAL) × Propane/Butane, using its own independent,
  narrower grid — confirmed NOT to reuse either the main grid's or R07.013's Overall-block
  column positions (each report's Overall block genuinely needs its own measurement, per the
  R07.013 lesson, now confirmed a second time).

## Defect found and fixed: repeated the R07.020 mistake
First render, copying R07.013's Row-A convention too literally, left Production*/Inventory* as
blank continuation cells with no visible label — this is the EXACT same mistake already made
and fixed on R07.020, not caught proactively here despite being documented. Also left the Date
column as one merged "Date"-only cell (copying a different sibling's row-merge pattern),
missing that this report's Date column genuinely has 3 distinct pieces of text across the 3
rows. Fixed by: adding "Publish Date" (Row A)/" 05 Aug 2025" (Row B)/"Date" (Row C) as 3
separate elements, and adding the missing "Production*"/"Inventory*" labels to their Row-A
cells.

## Verification performed
- All header columns and the recap block's independent grid measured directly from the
  reference PDF's own grid-line/fill-rect drawings before building.
- Post-fix comparison confirmed all group labels, INPEX/TOTAL sub-labels, and Propane/Butane
  leaf columns land within ~5-10pt of the reference — the tightest match yet in this
  multi-page sub-family.
- Confirmed via the same 2-month synthetic data source technique as prior multi-page reports
  that the title block correctly repeats on page 2.

## Not done this phase (by design)
- Live query/data verification — deferred, same as prior R07 batch reports.
- 24 placeholder parameters (`P_OA_*`, 4 rows × 6 columns) need real values/derivation logic.

## Key takeaway (repeated from R07.020, now doubly reinforced)
A documented lesson from an earlier report ("check for missing group labels before assuming a
blank continuation cell") was not applied proactively here even though it was fresh from the
immediately-preceding sibling report — it had to be rediscovered from the render diff. Written
lessons need to be actively re-checked against the CURRENT report's own first-render diff, not
just trusted to "already be learned" from having applied them once before.

## Owner border/layout review pass (2026-08-30, same day, after initial build marked done)
Same checklist defects as the rest of the batch, plus several genuine structural fixes unique
to this report's shape:

1. **Font jar / `leftPen` / double-border (`topPen`+`bottomPen`) / bare pens** — same 4 fixes as
   every prior report this session.
2. **Production*/Inventory* row-merge**: these 2 columns had their label in Row A only, with a
   separate BLANK Row B cell directly below (no text) before the Propane/Butane leaf row — an
   awkward "extra empty row" look. Merged into one 34pt-tall cell each (removing the blank Row B
   cells), confirmed via measurement: no internal divider line, single continuous cell.
3. **Overall/INPEX/TOTAL groups floating disconnected**: these 3 recap-block group headers had
   real gaps (42pt/55pt) between them despite their own Propane/Butane sub-columns already
   being flush — connected them edge-to-edge (owner-confirmed via screenshot of the defect).
4. **Missing left border + missing corner-cell fill on the recap block's row-label column** —
   same class of defect as R07.011/013/015/017 (leftPen leak / corner cell left blank instead of
   purple-filled to match "Overall"). Fixed identically: corner cell split into 2 sub-rows
   matching this report's own 2-row header shape.
5. **Publish Date row-merge**: "Publish Date"/"05 Aug 2025" were 2 separate bordered cells (not
   merged) — same treatment as item 2, into one 34pt cell with both lines, `vTextAlign="Top"`
   and `topPadding="3"` (matching the R07.018 header-alignment fix pattern).
6. **Top alignment applied to the entire first header row** (Publish Date/Production*/
   Inventory*/Liftings/Daily Entitlements/Lifting Position), not just Publish Date — all 6 cells
   now consistently top-aligned with the same 3pt padding, verified all landing at the same y=142.1.
7. **Recap block's end position widened to align under the main grid** — the owner specifically
   wanted the recap block's right edge to land exactly at the main grid's **Liftings-TOTAL-
   Propane** column's right border (corrected mid-task from an initial wrong target of
   Liftings-INPEX-Propane). Distributed the extra width evenly across Overall/INPEX/TOTAL
   (Overall 71→124, INPEX 70→123, TOTAL 70→122); confirmed via `get_drawings()` that both
   boundaries land at the identical x-coordinate (599, rotation-corrected).

**Process note:** item 4 from the owner's message (widening the recap block's row-label column
itself, on the START side) was explicitly put ON HOLD per owner instruction ("if u unsure item
4, put it aside first... settle 1-3 items first") and never applied — remains open for a future
session if revisited.

**Status: report layout verified (2026-08-30). Data queries deferred to a later stage**, same
convention as the rest of the R07.011-022 batch.
