# R07.011 — FC Production Report — Completion Notes (2026-08-30)

**Phase:** LAYOUT ONLY (data queries deferred, same convention as R07.013/015/016). The
biggest report in the R07 batch: 19 columns in the main grid, plus a 9-row x 7-column bottom
recap block.

**Build location:** `C:\Projects\INPEX\sources\CrystalReports\R07.011\output\`. **Base:**
copied R07.015's JRXML (flat Production-Report shape, no Propane/Butane split), then expanded
from 2 columns/group (INPEX/TOTAL) to 7 columns/group (INPEX, TOTAL, OPIC, Osaka Gas, Kansai
Electric, JERA, Toho Gas) across 2 group blocks (Daily Entitlement, Lifting Position).

## Report shape (measured directly, not assumed from any sibling report)
- Main grid: Date, Production*, Inventory*, then a "Lifting Quantity" section with 2 leaf
  columns (`Quantity` numeric + `Lifter` text — a wide, mostly-blank text column showing the
  lifting vessel/company name), then 2 group blocks x 7 customer columns each (Daily
  Entitlement, Lifting Position) = 19 columns total.
- Total row: Production*, Quantity, and all 7 Daily-Entitlement columns summed; Inventory*,
  Lifter, and all 7 Lifting-Position columns genuinely blank (running-balance/text) — matches
  the reference PDF's own Total-row text positions exactly.
- A 9-row bottom recap block reusing the Daily-Entitlement group's 7 customer column
  x-positions directly (confirmed via the reference's own Total-row and recap-block text
  landing at those same x-ranges): Participant (mini-header), Entitlement %, Opening Lifting
  Position, Entitlement, Current Month Liftings, Entitlement (cumulative), Cumulative Liftings,
  Closing Lifting Position, Month-End Not-Lifted/Lifting in Progress, UJV Reportable Closing
  Lifting Position.

## Layout quirk found and handled: split row-label captions
Row labels in the recap block are NOT single wide left-aligned strings (unlike R07.013/015's
Overall-block labels) — the reference renders each multi-word label as TWO separate text
fragments at different x-positions: a "prefix" fragment around local x=90-210 (roughly under
Production*/Inventory*) and a "suffix" fragment around local x=270-370 (within the Lifter
column). Single-word labels (Participant, Entitlement, Entitlement %) sit only in the suffix
zone. Discovered by comparing the first render's label positions against the reference's
actual text spans — initial build used one wide centered/left label per row (copying the
R07.013/015 convention) and every multi-word label landed far from the reference. Fixed by
splitting each into prefix+suffix static-text elements at the measured zones; all label
fragments now land within ~5-25pt of the reference (labels are non-data captions, so this is
within the same tolerance already accepted for header/title text elsewhere this session).

## Verification performed
- All 14 main-header customer columns (7 x 2 groups) measured directly from the reference
  PDF's own grid-line/fill-rect drawings before building; post-build comparison confirmed all
  14 match within ~5-6pt.
- Total row's 9 populated sums (Production*, Quantity, 7x Daily Entitlement) cross-checked
  against the reference's own Total-row text positions and column mapping.
- Recap block: "Participant" mini-header and all 9 row labels' prefix/suffix fragments
  cross-checked against the reference's actual text spans after the split-label fix.

## Not done this phase (by design)
- Live query/data verification — deferred, same as prior R07 batch reports.
- 63 placeholder parameters (`P_OA_*`, 9 rows x 7 customers) need real values/derivation logic
  once the data-query stage begins (entitlement %, cumulative, and UJV-reportable figures all
  need dedicated business logic, not simple sums of the daily fields).

## Key takeaway
Even a report that looks like a straightforward "extend the customer-column count" job can
hide a genuinely different caption-layout convention (split prefix/suffix labels vs one wide
label) — worth comparing the FULL reference text-position list against the first render before
assuming a sibling report's label convention carries over unchanged.
