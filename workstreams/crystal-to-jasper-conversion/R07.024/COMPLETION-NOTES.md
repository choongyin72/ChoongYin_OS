# R07.024 — LPG Consolidated Delivery Plan (CDP) — Completion Notes (2026-08-30)

**Phase:** LAYOUT ONLY (data queries deferred). Base copied from R07.023's JRXML/pom.xml/java
harness (per owner instruction), then rebuilt via direct measurement of THIS report's own
reference PDF — the main table is genuinely different from R07.023's shape.

**Build location:** `C:\Projects\INPEX\sources\CrystalReports\R07.024\output\`.

## What's different from R07.023 (measured, not assumed)
- **Main table columns**: R07.023 has 8 NAMED customer columns (INPEX/JERA/Kansai Electric/
  OPIC/Osaka Gas/Toho Gas/Tokyo Gas/TOTAL). R07.024 instead splits by **Propane/Butane
  product**, each with **Production/INPEX/TOTAL** leaves (6 data columns total, not 8).
- **Cargoes section has an extra split level**: R07.023's Cargoes has 2 leaf columns (INPEX
  count, TOTAL count). R07.024's Cargoes splits INPEX/TOTAL further into a **50/50 vs 75/25
  C3/C4 ratio** (4 leaf columns: INPEX-50/50, INPEX-75/25, TOTAL-50/50, TOTAL-75/25) — a real
  3-level header (Cargoes → INPEX/TOTAL → 50/50/75/25) vs R07.023's 2-level.
- **"Standard Cargo Size" is a real 2×4 mini-table** here (rows: Butane/Propane; columns:
  Sm3(50:50)/MT(50:50)/Sm3(75:25)/MT(75:25)) — R07.023's equivalent was a single value+unit.
- **Blank column after Cargoes confirmed present here too** — same convention, narrower gap
  (measured x=267–341 in local coordinates vs R07.023's x=175–272), confirmed via
  `get_drawings()` showing zero border lines in that range on both the header and every
  detail row.
- Header info block (Date of Issuance/Contract Year/Product/Version) is structurally identical
  to R07.023 — only the values differ (Product="LPG", Version="2025_CDP_LPG").

## Verification performed
- Font jar wired from the start (copied from R07.023's already-correct `pom.xml`); confirmed
  via `page.get_fonts()` — Arial variants embedded, no Helvetica fallback.
- Confirmed via `get_drawings()` that the blank column has zero vertical border lines across
  the header AND all 12 detail rows (checked both the left boundary at x=291 and right
  boundary at x=365, mapped/rotated coordinates — nothing in between).
- Confirmed all 12 months + Total row render with the correct 10 data columns each (4 Cargoes
  leaves + 6 Forecast Entitlement leaves).
- Confirmed the Standard Cargo Size mini-table renders the correct 8 values (2 rows × 4 cols)
  matching the reference's own measured figures (39,958 / 23,000 / 19,979 / 11,500 for Butane;
  45,338 / 23,000 / 68,007 / 34,500 for Propane).

## Not done this phase / known approximations (flagged for owner review)
- Header info-box exact pixel positions carried over from R07.023 without independent
  re-measurement (structurally identical section, reasonable to reuse, but not independently
  confirmed against R07.024's own reference).
- Live query/data verification — deferred, same as every other report this batch. Underlying
  table name/columns for this CDP data are entirely unknown.

## Follow-up check done same session
Went back and measured R07.024's OWN Remarks section (real content: 64.2pt tall, "31 cargoes
of LPG" vs R07.023's "28 cargoes of Field Condensate") rather than leaving R07.023's generic
placeholder text in place — confirmed the existing 85pt box comfortably fits it, and replaced
the placeholder with this report's own real remarks text.

**Status: report layout built and structurally verified (2026-08-30), unsupervised per owner
go-ahead while owner was offline. Data queries deferred to a later stage.**

## Owner review pass (2026-08-31) — first fix carried over from R07.023's own review
Owner asked to fix the background color for the info-block's 1st column (Date of Issuance/
Contract Year/Product/Version), same defect already found and fixed on R07.023 during its own
review pass. Re-measured THIS report's own reference PDF rather than assuming R07.023's value
carries over unchanged: `get_drawings()` confirmed the same fill `(0.0, 0.57, 0.71)` = `#0091B5`
at the label cell (`x=23.65-166.85, y=137.55-154.55`). Fixed:
- Backed up `R07_024_LPG_CDP.jrxml` to `.backup_20260831_before_review` BEFORE this edit (a
  gap the owner had to flag on R07.023 — corrected here from the start).
- Added `InfoLabelHeaderStyle` (`mode="Opaque"`, `backcolor="#0091B5"`, `forecolor="#FFFFFF"`,
  bold+italic), applied ONLY to the 4 info-block label cells — confirmed via `grep` that
  `InfoLabelStyle` had a 5th usage ("Standard Cargo Size" label) which was deliberately left
  untouched, same rule as R07.023.
- Recompiled + regenerated; confirmed via `get_drawings()` all 4 label cells now render with
  fill `(0, 145, 181)`, matching the reference. Swapped into `output/`.
- Note: R07.024 was NOT otherwise checked for the other R07.023 review-pass defects (Standard
  Cargo Size box alignment/fill, table-header spacing, month-column fill, Total-row border
  colors, footer divider line, alignment) — owner explicitly said not to proactively check
  R07.024/025 beyond what's directly asked; this fix was a specific owner request, not a
  self-initiated sweep.

Owner then asked for the same teal fill on the main table's 1st column (row C: Jan/Feb/.../
Dec/Total, under "Lifting Plan"), same as R07.023's month-column fix. Fixed:
- Backed up already covers this edit (same backup file as the previous fix, made before any
  edits this session).
- Added `MonthLabelStyle`/`MonthTotalLabelStyle` (same `#0091B5` fill, mirroring R07.023's
  styles) and applied them to the `<detail>` band's Month `textField` (`x=0 y=0 width=67`) and
  the `<summary>` band's "Total" `staticText` (`x=0 y=4 width=67`) — R07.024's Month column is
  67pt wide (vs R07.023's 54pt, consistent with this report's genuinely different column
  layout), confirmed via `grep` these were the only 2 matching elements before editing.
- Recompiled + regenerated; confirmed via `get_drawings()` 13 filled cells (12 months + Total)
  now render with the teal fill. Swapped into `output/`.

## Full remaining-defect sweep (2026-08-31) — owner directed applying all R07.023-class fixes
Owner correctly pointed out that since R07.024 was copied from R07.023's PRE-review-pass
base, the rest of R07.023's owner-found defects were almost certainly present here too, and
asked me to proactively find+fix them (each independently re-measured from R07.024's own
reference, not copy-pasted) rather than waiting to be shown each one again. Findings and
fixes, all measured via `get_drawings()`/word-position extraction on THIS report's own
reference PDF:

1. **"Standard Cargo Size" label was unfilled/narrow/misaligned** — reference shows it as a
   FULL-WIDTH filled purple header cell (`x=23.65-307.75` abs = local `x=0 width=284`,
   matching the 4 sub-columns' combined width `47+61+59+59+58=284`), not the small unfilled
   `InfoLabelStyle` staticText the build had. Rebuilt as a `HeaderCellBoxStyle` rectangle +
   `HeaderTextOverlayStyle` overlay (same pattern the main table's own header already uses).
2. **Standard Cargo Size sub-rows (column-header/Butane/Propane) were at the wrong y-position
   and not tightly connected** — re-measured real abs positions (header row `y=258.5-277.45`,
   Butane `y=277.95-291.45`, Propane `y=291.95-305.45`) and converted to local coords
   (`topMargin=28`): header row `y=230 height=18`, Butane `y=248`, Propane `y=262` — all now
   sit back-to-back with the new full-width label (`y=213 height=17`, ending exactly at 230).
3. **Main table header (Row 1/2/3) was too close to the taller, now-repositioned Standard
   Cargo Size block** — same class of defect as R07.023's title-band spacing issue. Reference
   shows the header's top edge at abs `y=326` (local `≈298`); shifted all 3 header rows down
   14pt (`282→296`, `297→311`, `314→328`) and grew `<title height="335">` to `345` (the new
   lowest element's bottom edge, not a rounded-up guess — per Part O2's lesson from R07.023).
4. **Total row's top border was gray, invisible on the teal Month/Total cell** — same
   deliberate-deviation fix as R07.023: `TotalRowStyle` and `MonthTotalLabelStyle`'s `topPen`
   both changed `#D6D6D6→#454087` (purple), matching the main header's own color and giving a
   continuous visible line across the whole Total row, including the teal cell.
5. **Missing footer divider line** — measured this report's own reference: identical values to
   R07.023 (`y=790`, `x=22.65-1165.9`, `#454087`, width `1.5`). Added the line + moved the 3
   footer text elements `y="0"→y="12"` in the SAME edit (learned from R07.023's ordering slip —
   got the line-then-text order right on the first render this time).
6. **Data-column alignment** — center-aligned the Standard Cargo Size mini-table's 8 numeric
   value cells (grid 2) and the main table's 4 Cargoes 50/50-75/25 leaf columns in both the
   `<detail>` and `<summary>` bands (grid 3, 8 elements total) — all were `hTextAlign="Right"`.
   The FE table (grid 4) numeric columns were deliberately left right-aligned, matching
   R07.023's scope (owner named grids 2/3 only there too).

**Verification:** recompiled cleanly; regenerated PDF confirms — full-width purple label
(`x=24-308,y=241-258`), header rows stacking correctly with zero overlap and a clean gap
(`y=324-373`, connecting directly into the first detail row with NO gap at `y=373`), Total
row's top border purple across all 4 Month+Cargoes columns including the teal cell
(`y=569`), and the footer divider line + text in the correct order. Swapped into `output/`.

**Not re-checked this pass:** the Remarks section's exact real content length (R07.023's own
completion notes already flagged this as a "same generous placeholder, not yet confirmed
against this report's real remarks" item) — out of scope for this specific defect sweep,
which targeted the 6 categories explicitly known-repeatable from R07.023's review.

## Two categories MISSED in the sweep above, caught by the owner
The "6 categories" list above was drawn up from memory of what R07.023 needed and was
INCOMPLETE — it missed two real defects that R07.023's own review pass also fixed. Owner:
"still have 2 defects u not fixed... 1. the TOP borderline between data column Jan and Total
for 3rd and 4th grid table. 2. add a grid table with one column after Remarks:. These 2
defects u had fixed in R07.023." Fixed:
1. **Total row sat 4pt below the last detail row instead of flush against it** (same defect
   as R07.023: `<summary>` band elements were at `y="4"` while `<detail>` rows are `y="0"`,
   height 16, stacked with zero gap). Confirmed via `grep` that `y="4"` appeared only on the
   10 Total-row elements (both grid 3's Cargoes columns AND grid 4's FE columns share this
   `<summary>` band), then shifted all 10 to `y="0"`. Recompiled + regenerated; confirmed via
   word-position extraction that Dec→Total spacing (16pt) now matches Nov→Dec spacing (16pt)
   exactly (previously an extra 4pt gap).
2. **Remarks text was a plain borderless textField, not the single bordered full-width cell
   pattern** established on R07.018/020/022/023. Added a `rectangle` (`mode="Transparent"`,
   `#D6D6D6` border, width `1140` matching the main table) under the "Remarks:" label, moved
   the remarks `textField` inside it (4pt padding, own box pens zeroed). Recompiled +
   regenerated; confirmed via `get_drawings()` the border spans `x=24-1164, y=614-699`.
- Both fixes verified in the regenerated PDF; the original PDF was locked (owner reviewing)
  at swap time — will finalize the swap once released.
- **Lesson: when told to "apply all remaining fixes from a sibling report's review", rebuild
  the checklist from that report's actual COMPLETION-NOTES.md (grep/read it), not from memory
  of "what I recall fixing" — memory dropped 2 of 8 real items here.**
- Swap completed once the owner's PDF viewer released the lock; `output/R07_024_LPG_CDP.pdf`
  now reflects all 8 fixes (the 6 from the first sweep + these 2).

## FINAL STATUS: Owner-verified OK (2026-08-31)
Owner confirmed the report layout is OK. All 8 fixes carried over from R07.023's own review
pass (info-block teal labels, Standard Cargo Size box rebuild/repositioning/spacing, main
table header shift, Total-row top border purple including the teal cell, footer divider
line, grid 2/3 data-column center-alignment, Dec/Total gap closure, Remarks bordered box) are
in `output/R07_024_LPG_CDP.jrxml` + the single `output/R07_024_LPG_CDP.pdf`. Not otherwise
re-verified beyond what R07.023's review surfaced — if the owner finds anything further,
treat as a fresh finding, not a regression of something already fixed here.
