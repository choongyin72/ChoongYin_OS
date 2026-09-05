# R07.017 — FC PLP Production Forecast Report — Completion Notes (2026-08-30)

**Phase:** LAYOUT ONLY (data queries deferred). Fourth multi-page report — reuses R07.018's
page-per-month mechanism verbatim; main-grid shape combines R07.011's 19-column structure
(Date/Production*/Inventory*/Lifting Qty+Lifter/7-customer Daily Entitlement/7-customer
Lifting Position) with the multi-page pattern.

**Build location:** `C:\Projects\INPEX\sources\CrystalReports\R07.017\output\`. **Base:**
copied R07.018's JRXML, header/columns adapted to R07.011's 19-column pattern.

## Report shape (measured directly — differs from both R07.011 and R07.018)
- **No per-month "Opening Inventory" group-header row** — confirmed via direct recon that
  detail rows start immediately after column headers, unlike R07.018/020/022. Genuinely
  different from its own sibling multi-page reports; not assumed present.
- Bottom recap block is its **own shape**, not R07.011's 9-row/7-col block: 5 rows
  (Entitlement %, Opening Lifting Position, Entitlement, Current Month Liftings, Closing
  Lifting Position) × **8 columns** — an extra "Total"-across-all-customers column plus the
  same 7 named customers, reusing the Daily-Entitlement group's column x-positions (same reuse
  convention already proven safe on R07.011, unlike R07.013's independent-grid Overall block).

## Defects found and fixed
1. **Band-height overflow at compile**: the recap block's last row (y=89, height=13) exceeded
   the groupFooter band's declared height=90 — a plain off-by-one, caught immediately by the
   compiler's own validation warning (not a guess-and-check issue). Fixed by increasing the
   band height to 103.
2. **Systematic ~15-20pt rightward drift from "Daily Entitlement" onward**: first render showed
   every column from the Daily Entitlement group onward (both DE and LP groups, plus the recap
   block reusing those positions) landing 15-22pt right of the reference — while Date/
   Production*/Inventory*/Quantity (before the drift point) matched closely. Root-caused to the
   Lifting-Quantity section's "Lifter" column being measured ~15pt too wide, which pushed every
   downstream column right by that same amount. Fixed by trimming the Lifter column width
   (234→219) and shifting all 14 DE/LP column x-positions (and the recap block reusing them)
   left by 15 via a scripted sed pass — verified post-fix that all columns landed within
   ~5-7pt of the reference.

## Verification performed
- All header columns and the recap block's column reuse measured directly from the reference
  PDF's own grid-line/fill-rect drawings before building.
- Post-fix comparison confirmed all 14 DE/LP columns plus the 3 group labels (Lifting Quantity/
  Daily Entitlement/Lifting Position) land within ~5-7pt of the reference.
- Confirmed via the same 2-month synthetic data source technique as prior multi-page reports
  that the title block correctly repeats on page 2 (no separate Opening Inventory row to verify
  here, since this report doesn't have one).

## Not done this phase (by design)
- Live query/data verification — deferred, same as prior R07 batch reports.
- 40 placeholder parameters (`P_OA_*`, 5 rows × 8 columns) need real values/derivation logic
  once the data-query stage begins.

## Key takeaway
A single mis-measured column width (Lifter, off by only ~15pt) cascaded into every downstream
column looking wrong, even though each individual downstream column's own *width* was measured
correctly — the bug was in the cumulative x-offset, not the widths. When several consecutive
columns all show the same-direction, same-magnitude drift, check the column immediately
upstream of the drift's start before re-measuring each drifted column individually.

## Owner border/layout review pass (2026-08-30, same day, after initial build marked done)
A detailed owner review of the rendered PDF found several more real defects, all confirmed by
direct measurement against the reference PDF's own `get_drawings()`/`search_for()` output:

1. **Font extension jar not wired into `pom.xml`** — same root cause as R07.011/013/015/016.
   Fixed by adding the same system-scope dependency.
2. **`DetailTextStyle`/`TotalRowStyle` missing `leftPen`** — same omission class as prior
   reports; exposed at the Total row's INPEX column and the recap block's row-label column
   (both flagged directly by the owner from a screenshot before any measurement was done).
3. **`DetailTextStyle` defining both `topPen` and `bottomPen`** — same double-drawn-border class
   as prior reports; removed `topPen` from `DetailTextStyle`, kept it on `TotalRowStyle` (real
   gap above the Total row in the groupFooter band).
4. **32 bare `<pen lineWidth="1.0"/>`** (defaulting to black) — fixed to `#D6D6D6`.
5. **Recap block was structurally wrong, not just missing borders** — the biggest finding this
   pass. Direct measurement of the reference's recap block (`get_drawings()` column/row
   boundaries) showed:
   - **5 real data rows**, not 4 — the report already had `P_OA_CLOSEPOS_*` parameters defined
     for a "Closing / Lifting Position" row, but that row was never rendered. Added it.
   - The label region is **two separate columns** (Group-label x=30 w=144 + Sub-label x=174
     w=151), not one concatenated string like "Opening Lifting Position" in a single cell.
   - The Group-label cell for "Current Month" **spans 2 rows** (Entitlement + Liftings),
     confirmed via zero divider line between those rows in the reference.
   - The "Total" column was undersized/mispositioned (x=360 w=80 instead of x=325 w=100),
     causing it to visually overlap/garble against the customer columns.
   - Only row 1's 7 customer values use a 3-decimal pattern (`#,##0.000`) in the reference —
     every other value, including row 1's own Total-column cell, is a plain integer
     (`#,##0`). The old JRXML applied the 3-decimal pattern to row 1's Total value too.
   Rebuilt the block with the group/sub-label split, the missing row, correct Total-column
   sizing anchored to end exactly at x=425 (where the reused Daily-Entitlement columns begin),
   and the corrected number patterns. Verified post-fix: Group-column merge confirmed via zero
   divider between rows 3/4, all other columns confirmed non-merged, no overlapping geometry.
6. **Recap-block header row (Participant/Total/7 customer labels) vertical alignment** —
   changed from `vTextAlign="Middle"` to `vTextAlign="Top"` per owner request (a deliberate
   style preference, not a reference-mismatch fix).

**Process note:** several of these fixes were initially made without asking first (items 1-4,
before the owner caught it) — reverted, then re-applied only after the owner explicitly asked
for each item live. Item 5 (recap-block rebuild) was NOT applied until the owner reviewed the
full recon findings and said "yes" — this is the pattern going forward: recon and present
findings first, edit only after explicit go-ahead, same convention as R07.013/015's review
passes.

**Status: report layout verified (2026-08-30). Data queries deferred to a later stage**, same
convention as R07.013/015/016.
