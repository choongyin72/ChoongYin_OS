# R07.012 — FC Lifting Report — Completion Notes (2026-08-29)

**Build location:** `C:\Projects\INPEX\sources\CrystalReports\R07.012\output\` (outside this
repo — a separate INPEX project directory, not tracked in ChoongYin_OS git).
**Output files:** `R07_012_FC_Lifting_Report.jrxml` (source), `R07_012_generated.pdf` (output),
verified via a standalone Maven/Java class (`R07012Verify.java`) calling
`JasperCompileManager.compileReport()` → `JasperFillManager.fillReport()` against the live local
Oracle sandbox → `JRPdfExporter`. No Jaspersoft Studio was used or available.

## What was built
- Full 14-column tabular report (Date/Production*/Inventory*/Lifted Qty/INPEX/TOTAL/OPIC/Osaka
  Gas/Kansai Electric/JERA/Toho Gas/Cargo ID/Vessel/Lifting Status), matching the reference
  Crystal Reports PDF's layout, fonts, colors, and grid structure.
- Opening Inventory row (label spans Date+Production*, value in Inventory* column, all other
  columns blank-but-bordered, matching the reference exactly).
- Total row (footer summary), including deliberately-borderless cells for Inventory*/Cargo
  ID/Vessel/Lifting Status — confirmed via direct measurement of the reference PDF that these are
  genuinely borderless by original design, not a rendering gap to "fix."
- Zero-value white-on-white suppression per numeric column (Lifted Qty/INPEX/TOTAL/OPIC/Osaka
  Gas/Kansai Electric/JERA/Toho Gas), matching the Crystal original's suppression trick.
- Live-DB-driven pivot query against `TV_FC_LIFTING_REPORT` (not the originally-supplied
  `queries.sql`, which didn't reproduce the report as-is — see the recon spec §6 above for the
  pivot logic).

## Defect-fix journey (why this took many rounds — read before the next conversion)
Nearly every round of back-and-forth in this build was a **border/layout** issue, not a data
issue. In order of discovery:
1. Header row column dividers invisible entirely → root cause: opaque header cells' own box
   border gets painted over by their own fill (see `JASPERREPORT-7-0-3.MD` Part D1).
2. First fix attempt (filled rectangles as separate divider shapes) worked technically but
   rendered visually bolder than the rest of the grid — traced to fill-shapes vs stroke-lines
   rendering with different visual weight.
3. Second attempt (freestanding `<line>` divider elements) fixed the boldness but introduced a
   0.5pt sub-pixel misalignment against real box-pen borders in adjacent rows/bands (Part D2) —
   looked like a "kink" or "doubled" line exactly where the header row met the row below it.
4. **Final, correct fix**: replaced every opaque header/label cell with the two-element
   rectangle+transparent-text-overlay pattern (Part D1) — the pattern was independently confirmed
   as the standard real-world convention from a different, already-working Ichthys JRXML the
   owner supplied mid-session. This eliminated the freestanding-line dependency entirely; every
   border is now a real box-pen edge, consistently aligned across every band with zero manual
   coordinate-matching between bands.
5. Adjacent-column 1pt x/width overlaps (inherited from the original recon's column-width
   values) were doubling every vertical grid line in the detail band — fixed by using
   `topPen`/`bottomPen`/`rightPen` only (no `leftPen`) on the shared cell styles (Part D3).
6. Total row's Inventory*/Cargo ID/Vessel/Lifting Status cells were initially given borders as a
   "completeness" assumption — turned out to deviate from the reference, which measurably leaves
   those cells borderless. Reverted once measured directly against the reference PDF rather than
   assumed.
7. Several verification methodology mistakes (documented in `JASPERREPORT-7-0-3.MD` Part D4)
   caused false "it's fixed" and false "it's broken" claims mid-session — resolved once raw
   content-stream byte inspection replaced pattern-guessing.

## Key takeaway for the next conversion
Read `JASPERREPORT-7-0-3.MD` Part D **before** building any header/label cell that needs both a
fill color and a border — go straight to the rectangle+overlay pattern (D1) rather than
discovering the opaque-fill-covers-border bug the hard way again. Apply the `topPen`/`bottomPen`/
`rightPen`-only convention (D3) to shared cell styles from the start, not after noticing doubled
lines.
