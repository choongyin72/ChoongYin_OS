# R07.014 — LPG Lifting Report — Completion Notes (2026-08-30)

**Build location:** `C:\Projects\INPEX\sources\CrystalReports\R07.014\output\` (outside this
repo, same as R07.012). **Approach:** copied `R07_012_FC_Lifting_Report.jrxml` as a base (styles,
fonts, geometry, and — critically — the border-rendering fix patterns from R07.012's Part D
lessons), then substantially rebuilt the header/detail/summary bands and query for this report's
different structure. Verified via the same Maven/Java harness pattern (`R07014Verify.java`),
compile → fill (live DB) → export, no Jaspersoft Studio.

## What was built
- Same page geometry/font scheme as R07.012, plus an extra title-block line ("LPG" product name +
  units subtitle) — title band height reduced from 134→110 to match this report's tighter measured
  gap before the divider line.
- A genuine **3-level nested header** (group row → INPEX/TOTAL sub-row → Propane/Butane leaf row) —
  structurally more complex than R07.012's flat single-row header. Column x/width values for all 16
  leaf columns were measured directly from the reference PDF's own grid lines, not estimated.
- A **double-pivot query** (`STORAGE_CODE` × `COMPANY_CODE`, crossed with two separate lifted-qty
  units) against `TV_LPG_LIFTING_REPORT` — more involved than R07.012's single-dimension customer
  pivot. Verified live against 3 individual days AND an independent full-month SQL aggregate before
  and after wiring into the JRXML.
- Opening Inventory row, zero-value white-suppression styles (8 lifting columns, confirmed the
  same trick is used here), and a Total row with the correct genuinely-borderless Inventory* gap
  (matching R07.012's established convention, verified against the reference rather than assumed).

## Why this build went far more smoothly than R07.012
R07.012 took many rounds of back-and-forth specifically on border/layout bugs. For R07.014, every
lesson from that session (`JASPERREPORT-7-0-3.MD` Part D) was applied **from the first draft**,
not discovered mid-build:
- Every opaque header/label cell used the rectangle+transparent-text-overlay pattern (D1) from the
  start — never attempted a bordered opaque `staticText` directly.
- Every shared cell style used `topPen`/`bottomPen`/`rightPen` only (D3) from the start — no
  doubled-border cleanup needed.
- No freestanding `<line>` divider elements were used at all (D2) — every border is a real
  element's own box edge, so there was no cross-band coordinate-matching to get wrong.
- Result: the header/detail/summary bands compiled, filled, and rendered correctly on the **first
  real build attempt** — confirmed via close-zoom visual inspection with zero doubling, kinks, or
  misalignment found.

## Verification performed
- Field-level: Opening Inventory (83,743/56,182), a non-lifting day (01-07), and a lifting day
  (02-07, both units) — all matched the reference PDF exactly.
- Total row: all 10 summed values matched an **independent** full-month `SUM()` SQL query run
  directly against the live DB (not just the report's own aggregation) — genuine, non-circular
  verification.
- Footer: an apparent large positional discrepancy turned out to be a bug in the verification
  script itself (only transforming one bbox corner through the page's rotation matrix instead of
  all four) — corrected and documented as a refinement to `JASPERREPORT-7-0-3.MD` Part D4, since
  it produces symptoms that look exactly like a real misalignment bug.

## Key takeaway for the next conversion
Copying a working JRXML as a base and applying the previous report's lessons proactively (not
reactively) turned what was a multi-hour debugging cycle on R07.012 into a same-session, low-drama
build on R07.014. Keep doing this: read `JASPERREPORT-7-0-3.MD` Part D in full before starting the
next report, and copy the most structurally-similar already-completed JRXML as the starting point
rather than building from an empty file.
