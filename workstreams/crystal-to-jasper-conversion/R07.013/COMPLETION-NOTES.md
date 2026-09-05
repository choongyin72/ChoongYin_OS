# R07.013 — LPG Production Report — Completion Notes (2026-08-30)

**Phase:** LAYOUT ONLY (data queries deferred, same convention as R07.015/016).

**Build location:** `C:\Projects\INPEX\sources\CrystalReports\R07.013\output\`. **Base:**
copied R07.014's JRXML (3-row nested Propane/Butane header pattern), extended to 3 group
blocks (Liftings / Daily Entitlements / Lifting Position) per R07.015's shape, plus this
report's own "Overall" recap block.

## Why this is the most complex report in the R07 batch so far
- **17-column, 3-row nested header**: Row A = 6 group cells (Publish Date, Production,
  Inventory, Liftings, Daily Entitlements, Lifting Position — each its OWN cell, unlike
  R07.015/016 where Date+Production+Inventory were merged under one banner). Row B = INPEX/
  TOTAL sub-labels under the 3 group blocks only (Date/Production/Inventory have a blank
  continuation cell in Row B). Row C = 16 Propane/Butane leaf cells; Date itself is a single
  cell spanning the full 3-row header height (`vTextAlign="Bottom"`), same row-merge pattern
  used for Date/Cargo ID/Vessel/Lifting Status in R07.012.
- **A distinctly-labeled 6-row "Overall" recap block** below the Total row — confirmed via
  direct text extraction that this report uses different row labels than R07.015's block
  ("Opening Position"/"Cumulative Entitlement"/"Closing Position" here vs "Opening Inventory"/
  "Cumulative Production"/"Closing Inventory" there), split Propane/Butane (6 data columns:
  Overall/INPEX/TOTAL × Propane/Butane).

## Defect found and fixed during this build
Initially reused the main daily-grid's Liftings-INPEX/TOTAL column x-positions (width 142/138)
for the Overall block's INPEX/TOTAL sub-columns, copying R07.015's "reuse the main grid
columns" convention without re-measuring. First render showed the Overall block's INPEX/TOTAL
mini-headers and Propane/Butane leaf cells drifting up to ~44pt right of the reference.

Root-caused by extracting the Overall block's own grid-line/fill-rect boundaries directly:
the block actually uses 3 independent, evenly-sized ~113pt-wide groups (not the wider Liftings
column widths), each split Propane(57)/Butane(56). Fixed by repositioning the INPEX/TOTAL
Propane/Butane sub-columns (x=311→311 unchanged, 384→368, 453→424, 522→481) and the mini-group
header spans (198-311/311-424/424-537 instead of 198-311/311-453/453-591). Recompiled,
re-rendered, re-verified — all Overall-block positions now within ~3-5pt of the reference.

## Verification performed
- All 17 header columns (Row A groups, Row B INPEX/TOTAL, Row C Propane/Butane leaves) measured
  directly from the reference PDF's own grid-line/fill-rect drawings before building.
- Post-build comparison (rotation-corrected) confirmed all header-row text positions match the
  reference within ~2-6pt on the main grid.
- Total row: matches reference's own 10 populated sums (Production P/B, Liftings INPEX/TOTAL
  P/B, Daily Entitlements INPEX/TOTAL P/B); Inventory* and Lifting Position (all 4: INPEX/TOTAL
  × P/B) confirmed genuinely blank — cross-checked against the reference's actual Total-row
  text spans.
- Overall block: label positions and all 6 rows' text confirmed against the reference's own
  labels (not assumed from R07.015) — this report's labels are genuinely different wording.

## Not done this phase (by design)
- Live query/data verification — deferred, same as R07.015/016.
- 36 placeholder parameters (`P_OA_*`, 6 rows × 6 columns) need real values/derivation logic
  once the data-query stage begins.

## Key takeaway
Even when reusing a proven pattern (R07.015's "Overall block reuses main-grid columns"), each
report's OWN grid must still be measured directly — this report's Overall block turned out to
use its own independent, narrower column layout, not the main daily-grid's. The fix followed
the same recon-first discipline established on R07.015/016: extract real grid-line boundaries
before trusting an assumption carried over from a sibling report.

## Owner border/layout review pass (2026-08-30, same day, after initial build marked done)
A detailed owner review of the rendered PDF found 7 additional real defects the initial build's
verification had missed — all confirmed by direct measurement against the reference PDF's own
`get_drawings()` output, not visual inspection:

1. **Font extension jar not wired into `pom.xml`** — same root cause as R07.011: without
   `inpex-arial-fonts.jar` on the classpath, `fontName="Arial"` silently falls back to plain
   Helvetica, so every `bold="true"`/`italic="true"` in the JRXML rendered as plain text. Fixed
   by adding the same system-scope dependency used for R07.011.
2. **`DetailTextStyle`/`TotalRowStyle` missing `leftPen`** — same omission class as R07.011,
   invisible in most of the grid (masked by the neighboring cell's rightPen) but exposed at any
   column-group boundary with a gap.
3. **`DetailTextStyle`/`TotalRowStyle` defining both `topPen` AND `bottomPen`** — causes most
   interior row boundaries to be drawn twice (once by each neighboring row), reading as
   inconsistent line thickness across the grid. Fixed by removing `topPen` from both — but this
   is where a real regression was caught: `TotalRowStyle` needed its `topPen` restored, because
   (unlike ordinary adjacent detail rows) the Total row sits ~6.5pt below the last detail row
   with nothing else providing that boundary. **Lesson: a shared-style fix proven correct in one
   context does not always transfer as-is to every band using that style — check whether the
   row above is genuinely adjacent before assuming its bottomPen covers the gap.**
4. **INPEX-Propane column width typo (73 instead of ~57)** in all 6 "Overall" recap-block rows —
   caused a ~16pt overlap between INPEX-Propane and INPEX-Butane. A genuine copy-paste artifact
   (the same 73pt value also legitimately appears elsewhere in the file, for the main grid's
   unrelated Liftings-Propane column in a different band — same number, different meaning,
   easy to conflate when grepping blindly).
5. **Recap-block row-label cells (Opening Position, etc.) wrongly stripped of their border** —
   an earlier mis-check only looked at the HEADER rows for a box left of the label column (found
   none, correctly) and wrongly generalized that to "labels have no border anywhere," missing
   that the DATA rows have their own bordered white-fill cell there. Reverted to bordered
   `DetailTextStyle`, with x/width tightened from 92/104 to 92/105→106 (iterated to the exact
   value with zero gap/overlap against the "Overall" column, confirmed via `get_drawings()`).
6. **Corner cell above the row-label column** — reference genuinely leaves this blank (confirmed
   via three independent checks: `get_drawings()` fill/color search, a fresh visual render, and
   a pixel-level scan of the saved image). Owner requested it be filled purple anyway, matching
   "Overall"'s own color, as a deliberate deviation from the reference — implemented as **two
   separate row cells** (not one merged block), matching how Overall/INPEX/TOTAL are themselves
   stacked as 2 cells, not merged into 1.
7. Multiple small (1-3pt) inter-column gaps/overlaps closed by computing the exact target x/width
   from both neighbors' true boundaries, not by iteratively nudging a value and re-rendering.

**Process lesson (the actual point of this pass, logged in full in the self-eval journal and in
`DeepDiveLearnings/JASPERREPORT-7-0-3.MD` Part M):** several of the above were things an earlier
"comprehensive" check had already measured and dismissed as "within tolerance" — a border either
touches or it doesn't; there is no acceptable non-zero gap. Measure the actual PDF files
directly (exact point coordinates, `get_drawings()`, pixel scans) before concluding anything,
and re-verify a fix's own side-effects on its immediate neighbors in the same pass, not the next
round.
