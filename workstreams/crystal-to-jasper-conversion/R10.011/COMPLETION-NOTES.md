# R10.011 — LPG Demurrage Calculation — Completion Notes (2026-08-30)

**Phase:** LAYOUT ONLY. Ninth R10 report. 2 STATIC pages (title=page1, summary=page2, natural
band-overflow break, same mechanism as R10.006/R10.010).

**Build location:** `C:\Projects\INPEX\sources\CrystalReports\R10.011\output\`.

## Report shape (measured directly)
- Info fields: Date Of Issue / Loading Port / Product / Vessel Name / Cargo Name / Loaded
  Quantity (MT), a 3-row 2-column grid with NO blank cell (6 fields fit exactly) — genuinely
  different from R10.010's 4-row/7-field grid with one blank cell, despite the very similar
  report name/purpose.
- Confirmed via direct word-position recon (not assumed) that the real visual section order is
  **Laytime → Allowed Laytime → Reimbursable Laytime** — the get_text('text') linear/content-
  stream extraction reads a different order (Laytime → Reimbursable Laytime → a set of
  "Adjustment"/"Laytime after Adjustment" rows that actually belong to the FIRST Laytime table →
  Allowed Laytime), the same underlying content-stream-vs-visual-order mismatch already
  documented for R10.008/009's Comments/section placement.
- All three Laytime/Allowed Laytime/Reimbursable Laytime tables share the SAME 4-column
  purple-header grid, confirmed via `get_drawings()` fill-color recon: label[0,227) /
  colA[227,312) / colB(Time)[312,397) / colC(hrs unit)[397,482) — the first "Laytime" table uses
  colA=Date/colB=Time with colC unused; the Allowed/Reimbursable Laytime tables use colB=value/
  colC="hrs" unit with colA unused (a blank purple header cell still present for visual
  consistency).
- Page 2: "Demurrage Rate" section (a/b/c equivalent cost breakdown → Calculated/Full/Adverse
  Weather rate) and "Demurrage Amount" section (Full/Adverse Weather/Total/Claim amount), plain
  label/value lines (no bordered cells this time, confirmed via `get_drawings()` — page 2 has no
  purple fills at all, unlike page 1's fully bordered tables).

## Build approach (applying the R10.010 Part J3 lesson directly)
Every row's local y-coordinate was taken DIRECTLY from the reference PDF's own measured
`abs_y - topMargin(28)` value (captured during recon), rather than computed from a uniform
row-height formula — this is the fix identified after R10.010's growing-offset defect. The
approach worked immediately for the title band (page 1): a coordinate spot-check on 4 widely
separated labels (Laytime, Allowed, Reimbursable, Darwin) landed within ~1-2pt of the reference
on the FIRST build attempt, with none of R10.010's growing drift.

## Defect found and fixed
The summary band (page 2) was NOT built the same exact-position way — its row y-values were
estimated from proportional spacing relative to the section headers, not read directly from
recon, and this reintroduced exactly the same class of growing offset just fixed for page 1
(spot-check showed "Calculated Demurrage Rate" landing ~43pt too high). Fixed by replacing every
summary-band element's y-value with its exact recon-measured target (`abs_y - 28`) via a direct
mapping table, the same method already proven for page 1 — post-fix spot-check on 3 labels
(Calculated, Total, Claim) landed within ~0.7-1.2pt of the reference.

## Verification performed
- Whole-page text extraction (`page.get_text('text')`) on both pages confirmed all reference
  text lines are represented; the only remaining diffs are the footer's "Last refresh date:" +
  timestamp being one joined element in the build vs two separate lines in the reference (a
  known PyMuPDF line-join artifact, not a real gap).
- Coordinate spot-check on 7 labels across both pages, before and after the summary-band fix,
  confirmed alignment within ~0.7-2pt everywhere on the final build.

## Not done this phase (by design)
- Live query/data verification — deferred, same as all prior R10 reports.

## Key takeaway
Applying R10.010's "use exact recon-measured y, not a formula" lesson to ONE band (title/page1)
but not the other (summary/page2) reproduced the exact same defect class in the unfixed band —
a lesson learned from a prior report's mistake must be applied consistently across every
comparable band/section within the SAME report, not just the first one built. Once applied
uniformly, this method produced the tightest alignment (sub-2pt) of any R10 report built so far
in this batch, on the first or second attempt, confirming it as the preferred approach for any
report with more than a handful of rows going forward — prefer measuring each row's real position
directly over computing it from an assumed uniform row height.
