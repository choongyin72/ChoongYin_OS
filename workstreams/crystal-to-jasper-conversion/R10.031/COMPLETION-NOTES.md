# R10.031 — ADP & SDS DES Buyers — Completion Notes (2026-08-30)

**Phase:** LAYOUT ONLY. Two reference PDF variants (ADP, SDS) genuinely differ in layout, so
built as TWO SEPARATE JRXMLs per the standing multi-variant rule (unlike R10.012's FC/PC pair,
which shared one layout — compared both before deciding).

**Build location:** `C:\Projects\INPEX\sources\CrystalReports\R10.031\output\` —
`R10_031_ADP_SDS_DES_Buyers_ADP.jrxml` and `R10_031_ADP_SDS_DES_Buyers_SDS.jrxml`.

## Why two JRXMLs, not one
Direct comparison of both reference PDFs before building: ADP ("LNG Annual Delivery Program")
and SDS ("LNG Specific Delivery Schedule") have different titles, different info-field sets
(ADP: Contract Year/Contract/Buyer/Date Of Issue/Version; SDS: Contract/Buyer/Date Of
Issue/Version/Start Date/End Date — no Contract Year, but two extra date-range rows), and
different populated content in the "Unloading Port" column (blank throughout ADP's sample,
populated with "One Safe Port in Taiwan" in SDS's). This is a genuinely different layout, not
just different sample values — confirming the R10.030/R10.031 multi-variant rule applies here,
unlike R10.012's FC/PC pair.

## Report shape (measured directly, both variants)
- Extra-wide landscape page (1190.55x841.85), margins ~22pt (same convention discovered on
  R10.026 — confirmed via leftmost/rightmost text extremes, not assumed).
- A genuinely REPEATING cargo-delivery grid (one row per LNG cargo), modelled as a `<detail>`
  band bound to a `JRMapCollectionDataSource` — same approach as R10.026, not parameters.
- Grid columns (IDENTICAL x-positions confirmed via direct word-position recon on BOTH variants,
  so the column layout was built once and reused): No. | Delivery Term | Cargo No. | Parcel No.
  | Buyer (2-line wrap) | Vessel Name | Vessel Size (m3) | Estimated Loading Date | Estimated
  Loading Quantity (MMBtu/tonne/m3) | Unloading Port | Scheduled Unloading Date | Estimated
  Unloading Quantity (MMBtu/tonne/m3) | Note.
- SDS-specific: a cargo row can show `*** CANCELLED ***` (as 3 separate text runs) in place of
  the Vessel Name, and the Unloading Port column is populated with values like "One Safe Port in
  Taiwan" (2-line wrap) — both modelled in the sample dataset.

## Defects found and fixed
1. **(Both variants) Title/columnHeader bands built far too compressed** — an initial guess of
   title=200/columnHeader=40 (ADP) put the grid header and data rows ~68-84pt too high versus
   the reference. Fixed the same way as R10.026: measured the reference's actual info-field and
   grid-header y-positions directly and resized title=284/columnHeader=49, repositioning every
   internal element to its measured local y — reduced the gap to ~2-15pt.
2. **(SDS only) Two entire label/value pairs ("Start Date"/"End Date") were completely absent
   from the render, with zero compile warning** — same class of bug as the F1
   "height-too-small-silently-drops-text" lesson, but notably occurring at `height="9"` even
   though 4 structurally-identical sibling elements (Contract/Buyer/Date Of Issue/Version, same
   style, same height) rendered correctly. Root cause not fully isolated, but the fix (bumping
   just these two elements' height from 9 to 14) resolved it immediately — confirmed via
   whole-page `get_text('text')` showing the values present before vs. absent after. Flags that
   this class of bug can occur even among visually-identical sibling elements, not just "big
   height jump" cases — always verify each NEW element pair independently, don't assume a
   pattern that worked for siblings automatically holds for elements added afterward.
3. **(SDS only) A field bound to a genuinely `null` sample value (`VESSEL_SIZE_M3` for the
   cancelled cargo row) rendered the literal string "null"** instead of blank — missing
   `blankWhenNull="true"` on that one field (present on most other optional fields already).
   Fixed by adding it. Caught by whole-page text diff showing `null` in the EXTRA list.

## Verification performed
- Whole-page text extraction (`page.get_text('text')`) on both variants confirmed the
  "Start Date"/"End Date" and "null" defects, and confirmed their fixes.
- Coordinate spot-check on both variants (grid header, cargo data cells, cancelled-row marker,
  populated Unloading Port cell) confirmed alignment within a similar ~2-15pt band to R10.026
  after the band-height fix, with the same known column-width imprecision on the wide numeric
  columns (not re-derived via `get_drawings()` for this report either).

## Not done this phase (by design)
- Live query/data verification — deferred, same as all prior R10 reports.
- Full multi-row verification — both variants were verified with 2 representative sample rows
  each (not the reference's full ~15-22 row set), sufficient to confirm the column template and
  header structure are correct; the remaining rows are mechanically identical repetitions.

## Key takeaway
Reinforces R10.012's lesson on handling multiple reference-PDF variants: compare structurally
FIRST, then decide one-JRXML-vs-two based on whether the difference is a genuine layout change
(here: yes) or just sample-value/optional-row differences (R10.012's FC/PC: no). Also surfaced a
new instance of the "silently dropped text" bug class in a place least expected — among elements
built identically to already-working siblings — reinforcing that no element pair is exempt from
verification just because a structurally similar one nearby already works.
