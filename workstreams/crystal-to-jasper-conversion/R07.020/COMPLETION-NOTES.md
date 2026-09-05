# R07.020 — LPG Provisional Lifting Program — Completion Notes (2026-08-30)

**Phase:** LAYOUT ONLY (data queries deferred). Second multi-page report — reuses R07.018's
page-per-month group mechanism and title-merged-into-pageHeader fix verbatim (both already
proven working, no rediscovery needed this time).

**Build location:** `C:\Projects\INPEX\sources\CrystalReports\R07.020\output\`. **Base:**
copied R07.018's JRXML, header/columns adapted to R07.014's 3-row nested Propane/Butane
pattern extended to 2 group blocks (Liftings / Liftings (MT)).

## Report shape (measured directly)
- 3-row nested header: Row A groups (Publish Date banner spanning Date+Production*+Inventory*,
  "Liftings", "Liftings (MT)", blank cargo-detail cell), Row B (INPEX/TOTAL sub-labels under the
  2 group blocks; Date/Production*/Inventory*/6 cargo-detail columns row-merge across Row B+C),
  Row C (Propane/Butane leaf labels under Production*/Inventory*/both group blocks).
- 6 cargo-detail columns with no "Representative" column (confirmed via direct header text
  recon — differs from R07.018's FC version, which has 7 including Representative/Lifter).
- Total row: Production*(P/B) and both Liftings-group columns (INPEX/TOTAL × P/B) summed;
  Inventory*, Liftings(MT) columns, and cargo-detail columns genuinely blank.

## Defect found and fixed: row-merged text alignment + missing labels
First render, copying R07.018's convention, used `vTextAlign="Bottom"` for the row-merged
Date/cargo-detail columns and left Production*/Inventory* as blank continuation cells (matching
R07.014's pattern where these have no visible label). Comparing against the reference showed:
- Date/Cargo ID/Vessel/etc. text actually sits at the TOP of the merged Row B+C region (abs
  y≈156.6, matching Row B's own top edge) — not the bottom. Fixed by changing `vTextAlign` from
  `"Bottom"` to `"Top"` on all row-merged elements.
- **Production*/Inventory* DO have visible labels here** (unlike R07.014, where these columns
  sit under a Propane/Butane split with no separate group-level label) — this report shows
  "Production*"/"Inventory*" as their own row-merged labels (same Top-aligned convention as
  Date), missed on the first pass because R07.014's blank-continuation-cell convention was
  copied without re-measuring this report's own Row B text. Fixed by adding the two missing
  `staticText` labels spanning the full Row B+C height.

## Verification performed
- All header columns (Row A/B/C) measured directly from the reference PDF's own grid-line/
  fill-rect drawings before building.
- Post-fix comparison confirmed Date/Production*/Inventory*/Cargo ID/Vessel/etc. all land at
  the correct y-position (top of the merged region) and within ~3-15pt x-tolerance of the
  reference (same range already accepted for caption/label text this session).
- Confirmed via the same 2-month synthetic data source technique as R07.018 that the title
  block and Opening Inventory group header both correctly repeat on page 2.

## Not done this phase (by design)
- Live query/data verification — deferred, same as prior R07 batch reports.
- Real Opening-Inventory carry-forward logic — placeholder field only.

## Key takeaway
Reusing a sibling report's *mechanism* (page-per-group, title-merge) verbatim was correct and
saved real rework — but reusing its *specific layout conventions* (blank continuation cell,
bottom-aligned row-merge text) without re-measuring this report's own reference caused two
real, fixable defects. Mechanism reuse and layout-detail reuse are different things; only the
former is safe to carry over unchecked.

## Owner border/layout review pass (2026-08-30, same day, after initial build marked done)
Same 4 checklist defects as the rest of the batch, plus several report-specific structural
corrections — all confirmed by direct measurement:

1. **Font jar / `leftPen` / double-border (`topPen`+`bottomPen`) / bare pens (30)** — same 4
   fixes as every prior report this session.
2. **Remarks box resized + repositioned**: measured all 4 months' real content (8.9pt Aug/Sep/
   Nov single-line, 27.3pt Oct 2-line) — original `height="24"` would have clipped October.
   Resized to 35pt, label moved from a 2pt gap to a 10pt gap from the Total row (matching the
   reference's own measured 10.1pt gap), and — per owner request, same as R07.018 — the
   placeholder text now sits in a single bordered cell spanning the full 1140pt grid width.
3. **Cargo ID/Vessel/Arrival Date Range/ADR Status/Loading Date Range/LDR Status un-merged**:
   these 6 columns had been row-merged (height=44, spanning what should be Row B+C) in an
   earlier session; owner explicitly said NOT to merge these — reverted to Row B (26pt, label +
   topPadding) + a separate Row C (18pt). Confirmed via measurement: a real divider line now
   exists between the two, where none existed when merged.
4. **Row B top-alignment made fully consistent**: Date/Production*/Inventory*/the 6 cargo
   columns were already top-aligned but flush against the border (no padding) — added
   `topPadding="3"` to all of them. The INPEX/TOTAL sub-header cells (×4) were still
   `vTextAlign="Middle"` — owner asked for these to match too; changed to `Top` + `topPadding="3"`.
   All 11 Row B header cells now land at the identical y-position.
5. **Total row extended through Liftings(MT)-TOTAL-Butane**: the Total row previously had no
   cells at all for Inventory*(P/B) or the entire Liftings(MT) group (4 columns) — a visible
   gap in the row's border/styling. Added 6 blank `TotalRowStyle` cells (Inventory*-P/B,
   Liftings(MT)-INPEX/TOTAL×P/B) so the row's bordered region is now continuous from the Total
   label through Liftings(MT)-TOTAL-Butane's right edge, with genuinely blank values (matching
   the header comment's own "running-balance, genuinely blank" note) — confirmed via
   `get_drawings()` that the row-height band has zero gaps end-to-end.
6. **Row C simplified**: after un-merging item 3, the resulting 6 separate blank Row C cells
   (one per cargo column) were merged back into ONE cell spanning Cargo ID through LDR Status —
   owner explicitly said these don't need individual right borders. Confirmed via measurement:
   only the outer two boundaries remain, no internal dividers.

**Status: report layout verified (2026-08-30). Data queries deferred to a later stage**, same
convention as the rest of the R07.011-022 batch.
