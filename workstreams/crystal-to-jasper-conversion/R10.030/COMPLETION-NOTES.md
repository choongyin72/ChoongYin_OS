# R10.030 — ADP & SDS FOB Buyers — Completion Notes (2026-08-30)

**Phase:** LAYOUT ONLY. Three reference PDF variants (ADP-per-buyer, ADP-per-contract,
SDS-per-buyer) built as THREE SEPARATE JRXMLs per the standing rule.

**Build location:** `C:\Projects\INPEX\sources\CrystalReports\R10.030\output\` —
`R10_030_ADP_SDS_FOB_Buyers_ADP_per_buyer.jrxml`,
`R10_030_ADP_SDS_FOB_Buyers_ADP_per_contract.jrxml`,
`R10_030_ADP_SDS_FOB_Buyers_SDS_per_buyer.jrxml`.

## Why three JRXMLs — verified genuinely different, not just following the rule blindly
- **ADP-per-buyer vs ADP-per-contract**: page-1 content looks nearly identical at first read,
  but direct word-position recon of BOTH found one real structural difference: the per-buyer
  variant's grid has a **"Contract"** column (useful when the report is paged/grouped BY buyer —
  each buyer's page needs to show which contract each cargo belongs to), while the per-contract
  variant's grid has a **"Buyer"** column instead (the inverse — useful when grouped BY contract).
  Confirmed via each variant's own header text, not assumed. Built the per-contract file from the
  per-buyer file with only that one header label (and its field's semantic meaning) changed —
  every other column, position, and info-field is identical between the two.
- **SDS-per-buyer**: confirmed genuinely different from both ADP variants (title "LNG Specific
  Delivery Schedule" vs "LNG Annual Delivery Program"; info fields include Start Date/End Date
  and no Contract Year, matching R10.031's SDS pattern; grid's "Buyer" column is POPULATED with
  real values here vs blank in ADP; "Destination Port" is populated with real port names here vs
  blank in ADP).

## Report shape (measured directly, all three variants)
- Same extra-wide landscape page/margins family as R10.031 (1190.55x841.85, ~22pt margins).
- A genuinely REPEATING cargo-delivery grid, modelled as a `<detail>` band bound to a
  `JRMapCollectionDataSource` — same approach as R10.026/R10.031.
- Grid columns differ from R10.031's DES-buyer family (confirmed via direct word-position
  recon, not assumed to match a sibling report): No. | Delivery Term | Cargo No. | Parcel No. |
  Contract-or-Buyer | Vessel Name | Vessel Size(m3) | Scheduled Loading Date | Estimated Loading
  Quantity (MMBtu/tonne/m3) | Gassing Up/Cooling Down | Destination Port | Note. **No
  unloading-side columns at all** — FOB buyers take delivery at the loading port, so there's
  nothing to report on the discharge end; this is a materially different column set from
  R10.031's DES-buyer family (which has Unloading Port/Scheduled Unloading Date/Estimated
  Unloading Quantity instead), confirmed by recon rather than assumed just because both reports
  are "cargo schedules."

## Defects found and fixed
1. **(SDS-per-buyer) Two fields (`LOAD_TONNE`, `LOAD_M3`) rendered the literal string "null"**
   for rows where the sample data had genuinely null values — missing `blankWhenNull="true"` on
   those two fields specifically, even though the pattern was already applied correctly to most
   other optional fields in the same detail band. Caught via whole-page `get_text('text')`
   showing `null` present, same class of bug as R10.031's SDS variant (a field missed the
   blankWhenNull convention that its siblings already had) — reinforces R10.031's lesson that no
   field is exempt from this check just because most of its siblings already have it right.
2. Applied R10.031's `Start Date`/`End Date` height-14 fix from the start on this report's SDS
   variant (rather than discovering the same silently-dropped-text defect again) — both labels
   rendered correctly on the first build attempt.

## Verification performed
- Whole-page text extraction (`page.get_text('text')`) confirmed the `null` defect and its fix on
  the SDS-per-buyer variant; confirmed clean compiles and correct page counts on all three files.
- Coordinate spot-check on all three variants (reusing the proven title=284/columnHeader=49 band
  heights established on R10.031's build, rather than re-deriving from scratch) landed within the
  same ~2-20pt tolerance band already accepted for this wide-grid report family, with the same
  known column-width imprecision on numeric columns as R10.026/R10.031 (not re-derived via
  `get_drawings()` for this report family).

## Not done this phase (by design)
- Live query/data verification — deferred, same as all prior R10 reports.
- Full multi-row verification — all three variants were verified with 2 representative sample
  rows each, sufficient to confirm the column template, header structure, and per-variant
  differences are correct; remaining rows are mechanically identical repetitions.
- The actual per-buyer/per-contract GROUPING/pagination logic (which buyer's or contract's cargo
  rows appear on which page) is a query/data-binding concern, explicitly out of scope for this
  layout-only phase — each JRXML currently renders one page's worth of sample rows via a static
  datasource, not a real multi-page grouped report.

## Key takeaway
Reinforced (a third time, after R10.012 and R10.031) that comparing multiple reference-PDF
variants structurally BEFORE deciding one-JRXML-vs-many pays off — the ADP-per-buyer/per-contract
pair looked nearly identical on first read but had one genuine, easy-to-miss column-header
difference that would have been silently wrong if copied without checking. Also reused two
established fixes (Start Date/End Date height, blankWhenNull convention) proactively from the
start on this report's SDS variant, though one field (LOAD_TONNE/LOAD_M3) still slipped through —
confirming that "applying a known fix" still requires checking EVERY field individually, not just
the ones most similar to where the bug was first found.
