# R07.016 — PC Lifting Report — Completion Notes (2026-08-30)

**Phase:** LAYOUT ONLY. Data queries for this report are explicitly deferred to a later
stage (owner instruction, 2026-08-29 batch GO) — the report's query is a placeholder against
an unverified table name (`TV_PC_LIFTING_REPORT`) and is never executed this phase; the
harness fills via `JREmptyDataSource` purely to check the visual layout.

**Build location:** `C:\Projects\INPEX\sources\CrystalReports\R07.016\output\` (outside this
repo). **Base:** copied `R07_014_LPG_Lifting_Report.jrxml` (flat single-product structure is
closer to R07.016 than R07.012's, since both are single-product "Lifting Report" titles with
an INPEX/TOTAL split, just without the Propane/Butane sub-split).

## What was built
- Title band: reused R07.014's y-positions/height=110/divider-at-y=92 as-is (measured to match
  R07.016's reference almost exactly) — only text content changed ("Plant Condensate" / "(in US
  BBL at 60F)").
- Page header collapsed from R07.014's 3-row nested (group→INPEX/TOTAL→Propane/Butane) structure
  to R07.016's real flat 2-row structure (Row A height=19: Publish Date banner + Liftings(BBL)/
  Liftings(MT) group labels; Row B height=13: 10 flat column headers). Total pageHeader
  height=32 (vs R07.014's 40) — measured directly, not copied.
- Column layout: 10 flat columns (Date, Production*, Inventory*, Liftings(BBL)-INPEX/TOTAL,
  Liftings(MT)-INPEX/TOTAL, Cargo ID, Vessel, Lifting Status) replacing R07.014's 16
  Propane/Butane-split leaf columns. Fields/variables/zero-suppression styles collapsed
  correspondingly (e.g. `LiftInpexPropaneZeroStyle`+`LiftInpexButaneZeroStyle` → one
  `LiftInpexZeroStyle`).
- Total row: measured directly from the reference PDF's own Total-row text spans — confirmed 5
  populated sums (Production*, Lift-INPEX/TOTAL ×2 units) with Inventory* genuinely blank,
  matching the same convention already established on R07.012/014 (not assumed — independently
  re-verified for this report specifically).

## Defect found and fixed during this build
Initial column split for the combined "Date+Production*" 209pt-wide span used 49/160 (copied
mentally from a rough visual estimate), which happened to sum to the right total width but
placed the internal Date/Production* boundary in the wrong place. First render showed both
column header text elements landing ~24pt to the left of the reference's real position — every
other column (Inventory* onward) matched the reference almost exactly, isolating the defect to
just those two.

Root-caused by extracting the reference PDF's actual vertical grid-line/fill-rect boundaries
(not text-center back-solving, which is unreliable) for the column-header row: real widths are
Date=97, Production*=112 (not 49/160). Fixed, recompiled, re-rendered, re-verified against the
same grid extraction — all 10 columns now match the reference to within ~1pt.

## Verification performed
- Page rotation: generated PDF reports `rotation=90` with a portrait mediabox (842×1191) — this
  is the same known, expected PDF landscape-encoding pattern documented in
  `JASPERREPORT-7-0-3.MD` Part D4, not a defect. All comparisons applied `page.rotation_matrix`
  before comparing coordinates.
- Column x-positions: cross-checked against the reference PDF's own vertical grid-line/fill-rect
  drawings (ground truth), not text-center estimation — all 10 columns match within ~1pt after
  the Date/Production* fix.
- Total row: cross-checked against the reference's own Total-row text spans directly (5 values,
  Inventory* blank) — matches what was built.
- Remaining ~2-5pt vertical (y-axis) offsets in header/title text are the same font-metric
  rendering variance already accepted as normal on R07.012/R07.014 (Crystal's PDF export vs
  JasperReports' PDF export use different font ascent/descent metrics for the same nominal
  font/size) — not a real layout defect.

## Not done this phase (by design)
- Live query/data verification — deferred to the later "queries" stage per owner instruction.
- `<field>` declarations are placeholders (`TV_PC_LIFTING_REPORT`, `COMPANY_CODE` values assumed
  from the R07.014 pattern) — must be re-verified against the real table/columns when queries
  are tackled.

## Key takeaway
The Date/Production* mis-split reinforces the standing rule: measure the reference PDF's own
grid lines directly for column boundaries, even when a combined span's total width happens to
match — an internal boundary can still be wrong while the total is right, and only real
grid-line extraction (not text-center estimation) catches that class of error.

## Owner border/layout review pass (2026-08-30, same day, after initial build marked done)
A round-trip happened on this report: fixes were first made without asking, then fully reverted
at the owner's request, then re-applied one item at a time only after explicit go-ahead — see
[[feedback_confirm_before_proceed]]. Once approved, the following real defects were fixed and
verified by direct measurement (not visual inspection):

1. **Font extension jar not wired into `pom.xml`** — same root cause as every other report in
   this batch. Fixed via the same system-scope dependency; verified via `page.get_fonts()`
   showing embedded Arial TrueType subsets instead of a Helvetica fallback.
2. **`DetailTextStyle`/`TotalRowStyle` + 4 zero-suppression styles missing `leftPen`** — fixed.
3. **`DetailTextStyle` and the 4 zero-suppression styles defined both `topPen` and `bottomPen`**,
   causing doubled interior row borders — removed `topPen` from all 5, kept it on
   `TotalRowStyle` (Total row sits in a genuinely gapped `<summary>` band).
4. **15 bare `<pen lineWidth="1.0"/>`** (defaulting to black) — fixed to `#D6D6D6`.
5. **"Opening Inventory" row column merge** — owner requested the 7 separate blank cells
   (INPEX through Lifting Status columns) be merged into a single blank cell, matching how the
   reference doesn't subdivide that trailing region on this row. Verified via `get_drawings()`
   that no internal vertical dividers remain between x=320 and the page's right margin.

**Status: report layout verified (2026-08-30). Data queries deferred to a later stage**, same
convention as the rest of the R07.011-022 batch.
