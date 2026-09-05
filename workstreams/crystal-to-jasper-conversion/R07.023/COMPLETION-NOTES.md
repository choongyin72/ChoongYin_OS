# R07.023 — FC Consolidated Delivery Plan (CDP) — Completion Notes (2026-08-30)

**Phase:** LAYOUT ONLY (data queries deferred). **Built entirely from scratch** — no prior
scaffolding existed (no `pom.xml`, no JRXML, no java harness); only the reference PDF was
present. This is a genuinely NEW report type for this batch: a single-page ANNUAL matrix
(Product × Month), not a daily lifting/production grid like every other R07 report so far.

**Build location:** `C:\Projects\INPEX\sources\CrystalReports\R07.023\output\`. `pom.xml`,
`java/src/.../R07023Verify.java`, and the JRXML were all authored fresh this session, following
the established conventions from the rest of the batch (font-jar wired in from the start,
`#D6D6D6` border color, `DetailTextStyle`/`TotalRowStyle` box pattern).

## Report shape (measured directly via `get_drawings()` + word-level text extraction)
- **Header info block** (4 label+value rows): Date of Issuance / Contract Year / Product /
  Version, plus a separate "Standard Cargo Size" callout box (label above, bordered value+unit
  box below).
- **Main table**: 1 row per month (Jan–Dec) + 1 Total summary row. Columns left to right:
  Month | "Lifting Plan" (Cargoes) INPEX count | Cargoes TOTAL count | **BLANK COLUMN**
  (confirmed via `get_drawings()` — the reference draws literally no cell/border in this
  x-range, matching the owner's own tip: "have a blank column after Cargoes column") |
  Production | Forecast Entitlement (bbl) × 8 sub-columns (INPEX/JERA/Kansai Electric/OPIC/
  Osaka Gas/Toho Gas/Tokyo Gas/TOTAL).
- **Remarks section**: a genuine multi-line paragraph block (measured ~76pt tall in the
  reference), sitting well below the Total row and well above the small bottom footer strip —
  NOT part of the single-line disclaimer pattern used by every other report in this batch.
  Modeled with generous height (85pt) since real remarks length will vary by issuance.

## Structural decisions (documented per the "novel pattern — use best judgment" authorization)
1. **Single `<title>` band for the whole header + table headers** (fires once), since this is
   a genuinely static, non-repeating single-page report — same pattern as the R10 batch's
   Part G precedent (`<title>`+`<summary>` for static reports), not the page-per-month
   `<pageHeader>`/`<group>` mechanism used by every other R07 report.
2. **12-row repeating `<detail>` band for the months**, with `MONTH_NAME` computed from
   `$V{REPORT_COUNT}` (1–12) rather than a real DAYTIME field, since no query exists yet
   (layout-only phase) — verified via `JREmptyDataSource(12)` in the harness.
3. **`<summary>` band for the Total row + Remarks**, summing the 12 detail rows via `Sum`
   variables (all currently `new BigDecimal("0")` placeholders, matching the "layout-only,
   deferred to data stage" convention already used for every other report's placeholder
   values) — avoided a 100+ parameter explosion that a per-cell-parameter approach (like the
   smaller 4-row recap blocks elsewhere) would have required.
4. **Two real JRXML syntax discoveries** (both caught immediately by the compiler, not
   guessed): `<summary>` in this compact format does NOT wrap a nested `<band>` element —
   height/splitType go directly on the `<summary>` tag, same as `<title>`/`<pageHeader>`/
   `<pageFooter>` (only `<detail>`/`<groupHeader>`/`<groupFooter>` wrap in `<band>`). Also hit
   a real "element reaches outside band area" validation error when the title band's declared
   height (260) was shorter than its own tallest element's bottom edge (293) — fixed by
   growing the band to 300.

## Verification performed
- Font jar wired from the start; confirmed via `page.get_fonts()` showing embedded Arial
  TrueType subsets (no Helvetica fallback risk this time, unlike every prior report in this
  batch which needed this added retroactively).
- Confirmed via `get_drawings()` that the blank column (x=199–296 in generated-PDF coordinates)
  has zero vertical border lines, matching the reference's own confirmed gap.
- Confirmed all 12 months (Jan–Dec) + Total row render with the correct 11 data columns each
  (2 Cargoes counts + Production + 8 products).
- Confirmed the full Remarks paragraph (all 6 bullet lines) renders without truncation.

## Not done this phase / known approximations (flagged for owner review, not guessed silently)
- **Header info-box area (title font size, exact info-row heights, Standard Cargo Size box
  position) is reasonably but not pixel-precisely measured** — this section is decorative/
  metadata, not the report's core data table, so effort was concentrated on the table's exact
  column boundaries (which matter for the blank-column requirement) rather than chasing every
  header pixel. Worth a visual pass once the owner is back online.
- Live query/data verification — deferred, same as every other report this batch. The
  underlying table name/columns for this CDP data are entirely unknown (no query existed to
  reverse-engineer from) — will need real DB investigation at the data-query stage.
- Standard checklist items (font jar, `leftPen`, double-border check, bare-pen audit) don't
  apply retroactively here since the report was built clean from scratch with these already
  in place — worth a final measurement pass to confirm no NEW instances crept in during the
  build (not done yet, given the scale of this report's from-scratch construction).

**Status: report layout built and structurally verified (2026-08-30), unsupervised per owner
go-ahead while owner was offline. Data queries deferred to a later stage.** Flagging for the
owner's own visual review given this is the first CDP-type report and the header area's
measurement was necessarily less precise than the main table.

## Owner visual review pass (2026-08-30, later same day)
Owner screenshot-flagged the info-block's label column (Date of Issuance/Contract Year/Product/
Version) rendering with a plain white background + black text, vs. the reference's teal-filled
+ white bold-italic label cells — exactly the kind of header-area imprecision already flagged
above as "worth a visual pass." Fixed:
- Measured the reference's REAL fill color via `get_drawings()` on the reference PDF (not
  guessed/eyeballed): `fill=(0.0, 0.5699999928474426, 0.7099999785423279)` → `#0091B5`.
- Added a new style `InfoLabelHeaderStyle` (`mode="Opaque"`, `backcolor="#0091B5"`,
  `forecolor="#FFFFFF"`, bold+italic) applied ONLY to the 4 info-block label cells — the
  "Standard Cargo Size" label (which shares `InfoLabelStyle` but is NOT teal-filled in the
  reference) was deliberately left untouched.
- Recompiled + regenerated the PDF; sampled the rendered pixel color at the label cells
  (`(0, 145, 180)`) — matches the reference's measured fill (`(0, 145, 181)`) within rounding.
- Exactly one PDF remains in `output/` (regenerated in place, old one overwritten).

Owner then screenshot-flagged a second header-area defect: the "Standard Cargo Size" box was
offset (x=31, not aligned with the info-block/main-table's shared x=0 left edge) and had a
plain unfilled header label instead of a filled purple header cell, with a visible gap between
its header row and value row instead of the two rows reading as one connected 2-row table.
Fixed:
- Re-measured the REAL header-cell and value-row coordinates from the reference via
  `get_drawings()`: header rect `x=23.65-173.6, y=248.55-268.55` (fill `(0.27,0.25,0.53)` =
  `#454087`, same purple as the main table's `HeaderCellBoxStyle`); value row rect
  `x=23.15-174.1, y=269.6-287.05` (2 cells split at x≈121). Converted to local (title-band)
  coords by subtracting the page's own `leftMargin`/`topMargin` (24/28): header `x=0 y=221
  width=150 height=20`; value row `x=0/98 y=241 width=98/52 height=17` — header bottom
  (y=241) exactly meets value-row top (y=241), zero gap.
- Rebuilt the box as: 1 filled purple rectangle + white bold-italic overlay text for the
  header (reusing the existing `HeaderCellBoxStyle`/`HeaderTextOverlayStyle` pair the main
  table already uses, for visual consistency), + the existing bordered `InfoValueStyle` value
  cells repositioned to `x=0`/`x=98`, `y=241`.
- Recompiled + regenerated; re-measured the GENERATED PDF's own `get_drawings()` (applying
  `page.rotation_matrix` since this landscape report exports with `rotation=90`) — confirmed
  header at `x=24-174, y=249-269` (matches reference almost exactly) and value row starting
  at `y=269`, i.e. touching the header's bottom edge with no gap.
- Confirmed via style definition (not re-guessed) that the info-block's own label column
  (`InfoLabelHeaderStyle`, added in the first fix above) is already `bold="true"
  italic="true"` — owner asked to confirm this separately, no change needed.
- Exactly one PDF remains in `output/` (regenerated in place).

Owner then screenshot-flagged that the newly-repositioned "Standard Cargo Size" box (row A+B)
sat too close to the main table's "Lifting Plan" header directly below it, in fact overlapping
by ~6pt (value row bottom y=258 vs. table header row1 top y=252). Fixed:
- Shifted the entire main-table header (both Row 1 `y=252→272` and Row 2 `y=277→297`, all 28
  rectangle+overlay-text elements) down by 20pt — confirmed via `grep` that `y="252"`/`y="277"`
  appeared ONLY within this header block before applying the shift, so no unrelated element was
  touched.
- Grew the `<title>` band height `300→330` to fit the new lowest element's bottom edge
  (297+16=313).
- Recompiled + regenerated; re-measured the GENERATED PDF (`rotation_matrix`-corrected) —
  value row now ends at `y=286`, table header now starts at `y=300`, a clean 14pt gap (was a
  6pt overlap before the fix). This also pushes the `<detail>` (12 month rows) and `<summary>`
  (Total row + Remarks) sections further down automatically, since JasperReports stacks bands
  sequentially — exactly the "push 3rd/4th grid + Remarks further down" the owner asked for,
  achieved by fixing the actual overlap rather than inserting arbitrary extra spacing.
- Exactly one PDF remains in `output/` (regenerated in place).

That 330-height title band overshot its own content's real bottom edge (313) by 17pt, which
then showed as a visible blank gap between the table header and the first data row (`Jan`) —
owner flagged this too ("data rows are not connected to its column header row"). Fixed:
- Shrank `<title height="330">` back down to `<title height="313">` — exactly the lowest
  element's bottom edge (header Row 2: `y=297+16=313`), so the `<detail>` band (month rows)
  starts immediately where the header ends, with zero extra band-level gap.
- Recompiled + regenerated; confirmed via rotation-corrected word extraction that `Jan`'s text
  now starts at `y=346`, right after the header rectangle's own bottom edge (`y=341`) — the
  ~5pt difference is normal cell padding/vertical centering within the 16pt detail row, not a
  stray gap.
- Note: the original `output/R07_023_FC_CDP.pdf` was locked (owner had it open for screenshot
  review) when this fix was verified — exported to a temp file first, verified, then swapped
  in to replace the locked original once released. Exactly one PDF remains in `output/`.

Owner then asked for the main table's first column (row C: Jan/Feb/.../Dec/Total, under the
"Lifting Plan" header) to get the same teal fill as the info-block's first column
(`InfoLabelHeaderStyle`, `#0091B5`). Fixed:
- Added two new styles reusing the same measured `#0091B5` fill: `MonthLabelStyle` (for the
  12 month detail rows — white bold-italic text, `DetailTextStyle`'s border pattern minus
  `topPen` since adjoining rows already supply it) and `MonthTotalLabelStyle` (for the Total
  row's label cell — same fill, keeps `TotalRowStyle`'s `topPen` since the Total row sits in
  a genuinely gapped `<summary>` band, per the project's established topPen convention).
- Applied `MonthLabelStyle` to the `<detail>` band's Month `textField` and
  `MonthTotalLabelStyle` to the `<summary>` band's "Total" `staticText` — both were previously
  plain `DetailTextStyle`/`TotalRowStyle` (white background, black text).
- Recompiled + regenerated; confirmed via `get_drawings()` (rotation-corrected) that all 12
  month-row cells + the Total row cell now render with fill `(0, 145, 181)`, matching the
  info-block column's measured fill exactly.
- Original PDF was locked again (owner reviewing) — exported to a temp file, verified, then
  swapped in. Exactly one PDF remains in `output/`.

Owner then flagged a visible white gap between the "Dec" row and the "Total" row (screenshot),
caused by the `<summary>` band's Total-row elements all sitting at `y="4"` instead of `y="0"`
(the `<detail>` band's rows are `y="0"`, height 16, stacked with zero gap between each other —
the Total row's own `y="4"` broke that pattern). Fixed:
- Confirmed via `grep` that `y="4"` appeared ONLY on the 11 Total-row elements (lines 207-218),
  then shifted all of them to `y="0"`.
- Recompiled + regenerated; confirmed via word-position extraction that Nov→Dec spacing
  (16pt) now exactly matches Dec→Total spacing (16pt) — previously Dec→Total had an extra 4pt
  gap. Swapped into `output/` once the owner's PDF viewer released its lock on the original.

Owner then asked for the Remarks section to follow the same "Remarks:" label + single
bordered full-width cell pattern already established on R07.018/020/022, rather than a plain
borderless textField. Fixed:
- Added a `rectangle` (`mode="Transparent"`, `#D6D6D6` border, same `1140` width as the main
  table) directly under the "Remarks:" label, and moved the remarks `textField` inside it
  (4pt padding, its own box pens zeroed out since the rectangle now supplies the border) —
  same structure as R07.018's own Remarks box, just re-measured for this report's own
  y-position (`y=49`, `height=85`, matching the existing generous sizing already in place).
- Recompiled + regenerated; confirmed via `get_drawings()` the border rectangle spans
  `x=24-1164` (matching the main table's own left/right edges) with the correct `#D6D6D6`
  color. Swapped into `output/`.

Owner asked (from a screenshot) to set the Total row's top border to solid black. Measured
the reference's real top-border color first rather than applying black on the screenshot's
visual impression — `get_drawings()` on the reference showed the top border above the Total
row's NUMERIC cells is actually `#454087` (the same purple used for the header row, width
1.0), not black; the Month/Total teal label cell's own top border is the grid's normal gray
`#D6D6D6`. Applied the REAL measured color:
- `TotalRowStyle`'s `topPen` changed from `#D6D6D6` to `#454087`. `MonthTotalLabelStyle`'s
  `topPen` left as `#D6D6D6` (already correct per the same measurement — the Month/Total
  teal cell does NOT get the purple top border in the reference).
- Recompiled + regenerated; confirmed via `get_drawings()` the Total row's numeric cells now
  render with top-border color `(0.27, 0.25, 0.53)` = `#454087`, matching the reference
  exactly, while the teal cell keeps its gray border. Swapped into `output/`.

Owner then screenshot-flagged that the teal cell's gray top border (correct per the raw
reference measurement) was visually INVISIBLE against the `#0091B5` teal fill — no visible
Dec/Total separation on that side, unlike the clearly-visible purple line on the numeric side.
Re-verified the reference measurement twice more (broad column scan + precise Dec/Total
word-position bracketing) before changing anything — both confirmed the reference's raw color
really is gray there, so this was a genuine visual-intent vs. raw-value conflict, not a
measurement error. Owner chose to deliberately deviate from the raw reference value for
visual clarity:
- `MonthTotalLabelStyle`'s `topPen` changed from `#D6D6D6` to `#454087`, explicitly documented
  in the JRXML as a deliberate deviation (not a fresh "fix the measurement" edit), so a future
  reviewer doesn't mistake it for an unverified guess.
- Recompiled + regenerated; confirmed via `get_drawings()` the teal cell's top border now
  overlaps the same `#454087` purple as the adjacent numeric cell, giving a continuous visible
  line across the whole Total row. Swapped into `output/`.

Owner flagged a missing divider line in the `pageFooter`, above the "Last refresh date: ..."
text. Measured the reference directly: a line at `y=790` (abs), `x=22.65-1165.9` (full column
width), color `#454087`, width `1.5` — same purple/width as the title-banner's own divider
line, just previously never carried over into the footer. Fixed:
- Added the line (`x=0 y=10 width=1140 height=1`, `pen lineWidth="1.5" lineColor="#454087"`)
  to the `pageFooter` band.
- First pass put the line ABOVE the footer text but left the text at its old `y=0` — this
  inverted the reference's real order (reference: line at `y=790`, text starting at `y=792`,
  i.e. text BELOW the line). Caught via re-measurement of the regenerated PDF's own word
  positions (`Last` at `y=780`, above the line at `y=790` — wrong), not assumed correct on
  first render.
- Fixed by moving all 3 footer elements (`Last refresh date`/`Security Classification`/`Page
  X of Y`) from `y="0"` to `y="12"`, confined-scope-checked via `grep` (`FooterStripStyle`
  appears only on these 3 lines) before the shift.
- Recompiled + regenerated; confirmed via `get_drawings()`/word extraction that the line
  now renders at `y=790.5` and the footer text starts at `y=792.97`, right below it — matching
  the reference's real line-then-text order. Also confirmed `P_LAST_REFRESH`'s existing default
  (`2025-09-08 13:00:14`) already matches the reference's own footer text exactly, so no
  parameter change was needed there. Swapped into `output/`.

Owner asked for the data columns in grid 2 (Standard Cargo Size box) and grid 3 (main table's
"Lifting Plan"/Cargoes block) to be center-aligned instead of the previous right/left
alignment. Scope: this request named only grids 2 and 3, NOT grid 4 (the Forecast
Entitlement table), so its numeric columns were deliberately left right-aligned. Fixed:
- Grid 2: `P_STD_CARGO_SIZE` value cell (`hTextAlign="Right"→"Center"`) and the "bbl" unit
  cell (`hTextAlign="Left"→"Center"`).
- Grid 3: the Cargoes INPEX/TOTAL count columns (`x=54`/`x=115`) in both the `<detail>` band
  (12 month rows) and the `<summary>` band's Total row — 4 elements total, all
  `hTextAlign="Right"→"Center"`. Confirmed via `grep` these 4 lines were the only matches for
  that x-position pattern before editing, so the FE table's own numeric cells (different
  x-positions) were untouched.
- Recompiled — compiled cleanly, swapped into `output/`.

## FINAL STATUS: Owner-verified OK (2026-08-31)
Owner confirmed the report layout is now OK after the full review pass above (teal info-block
labels, Standard Cargo Size box alignment/fill/connection, table-header spacing, month-column
teal fill, Total-row top border colors — including one deliberate raw-value-vs-visual-intent
deviation — footer divider line, and grid 2/3 center alignment). `output/R07_023_FC_CDP.jrxml`
+ one `output/R07_023_FC_CDP.pdf` are the authoritative build artifacts. Moving on to R07.024
next; since R07.024/025 were copied from an EARLIER (pre-review-pass) version of this JRXML,
they need to be checked for the same defects rather than assumed clean — see each report's own
COMPLETION-NOTES.md for the outcome of that check.
