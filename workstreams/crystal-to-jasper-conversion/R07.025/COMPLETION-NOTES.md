# R07.025 — PC Consolidated Delivery Plan (CDP) — Completion Notes (2026-08-30)

**Phase:** LAYOUT ONLY (data queries deferred). Base copied from R07.024's JRXML/pom.xml/java
harness (per owner instruction), then substantially rebuilt via direct measurement of THIS
report's own reference PDF — both the table shape AND the page orientation are genuinely
different from R07.024.

**Build location:** `C:\Projects\INPEX\sources\CrystalReports\R07.025\output\`.

## What's different from R07.024 (measured, not assumed)
- **Genuinely PORTRAIT**, confirmed via the reference PDF's own `page.rect` (595.25 × 841.85,
  `rotation=0`) — not just an `orientation="Portrait"` flag on an unchanged page size. Built
  with `pageWidth="595" pageHeight="842" columnWidth="550" leftMargin="23" rightMargin="22"`,
  confirmed against the reference's own logo bbox (x=22.65–167) and divider-line width
  (22.6–572.6 = exactly 550pt) landing on the same margin values.
- **Single-product (Plant Condensate) table — no Propane/Butane split**: Cargoes has just 2
  leaf columns (INPEX, TOTAL counts — matching R07.023's simplicity, NOT R07.024's 4-leaf
  50/50-75/25 split). Forecast Entitlement has just 3 leaf columns (Production, INPEX, TOTAL —
  no Propane/Butane group split at all).
- **"Standard Cargo Size" is a simple single value+unit** (320,000 bbl) — matches R07.023's
  pattern, NOT R07.024's 2-row × 4-column mini-table.
- **Blank column after Cargoes confirmed present here too**, proportionally narrower (~12pt
  gap, vs R07.023/024's ~74-98pt) — consistent with this report's much narrower portrait page.
  Confirmed via `get_drawings()`: boundaries only at the two outer edges (x=260, x=272 in
  generated-PDF coordinates), nothing in between.
- **A real, verified data point in the reference itself**: the "Version" field literally reads
  `2025_CDP_LPG` in this PC (Plant Condensate) report's own reference PDF — preserved exactly
  as measured rather than "corrected" to `2025_CDP_PC`, since replicating the reference
  precisely (including its own apparent inconsistencies) is the job here, not fixing it.

## Verification performed
- Font jar wired from the start; confirmed via `page.get_fonts()` — Arial variants embedded.
- Confirmed page dimensions (595×842) and rotation (0) match the reference exactly — this is
  the first report in the batch with genuine portrait geometry, not a landscape page examined
  through a `/Rotate 90` flag.
- Confirmed via `get_drawings()` that the blank column has zero border lines in the gap,
  bounded correctly on both sides.
- Confirmed all 12 months + Total row render with the correct 5 data columns each (2 Cargoes
  + 3 Forecast Entitlement leaves).
- **Remarks text measured directly from THIS report's own reference** (not carried over from
  R07.023/024) — "Total 21 cargoes of Plant Condensate are scheduled in 2025," confirmed to
  match the same paragraph structure/length as the other CDP reports, so the same generous
  box sizing (100pt) applies without needing separate re-measurement.

## Not done this phase (by design)
- Live query/data verification — deferred, same as every other report this batch. Underlying
  table name/columns for this CDP data are entirely unknown.
- Header info-box exact pixel positions are reasonable approximations (same standard applied
  to R07.023/024) rather than pixel-perfect — the core table's column boundaries (which matter
  for the blank-column requirement) were prioritized for precision.

**Status: report layout built and structurally verified (2026-08-30), unsupervised per owner
go-ahead while owner was offline. Data queries deferred to a later stage.** First-render
compile succeeded with zero validation warnings, unlike R07.023/024 which each needed one
band-height correction — the lessons from those two builds (checking element-bottom vs
band-height before first compile) were applied proactively here.

## Owner review pass (2026-08-31) — full 9-category sweep applied proactively
Owner: "R07.025 its same as R07.024... u can apply what u been fix in R07.023 or R07.024 into
R07.025... before I verify the pdf." Rebuilt the checklist from R07.023's AND R07.024's actual
COMPLETION-NOTES.md (not from memory — the exact lesson learned on R07.024, applied here) and
re-measured each item against THIS report's own reference PDF rather than copy-pasting
R07.024's coordinates. Backed up the JRXML before any edit.

1. **Info-block teal labels** — measured this report's own reference: same `#0091B5` fill.
   Added `InfoLabelHeaderStyle`, applied to the 4 label cells only (not "Standard Cargo Size").
2. **Standard Cargo Size box** — reference showed this as a full-width filled PURPLE (`#454087`,
   matching the main table's own header color — same as R07.023's fix, not R07.024's teal
   info-block treatment) header cell (`x=23-142` abs / local `x=0 width=119`, matching the
   combined value+unit width `66+53=119`), connected with zero gap to the value row below.
   Rebuilt from a plain unfilled/misaligned `staticText` (was `x=41`, not matching the main
   table's `x=0`) into a `HeaderCellBoxStyle` rectangle + `HeaderTextOverlayStyle` overlay, and
   re-centered the value/unit cells (was Right/Left-aligned, now Center per item 7 below).
3. **Main table header spacing** — checked for the R07.024-style overlap/gap defect; NONE
   found here (measured `bbl` value-row text at `y=237`, `Lifting` header text at `y=269.6` —
   a clean ~32pt gap, no title-band regrow needed).
4. **Main table month-column teal fill** — same `#0091B5`, applied to the `<detail>` band's
   Month cell and the `<summary>` band's "Total" label (`MonthLabelStyle`/
   `MonthTotalLabelStyle`, mirroring R07.023/024).
5. **Total-row top border** — `TotalRowStyle`/`MonthTotalLabelStyle` `topPen` set to `#454087`
   (purple), including the teal Month/Total cell (matching R07.023's owner-confirmed
   deliberate-deviation pattern). **Caveat, flagged honestly:** this report's own reference PDF
   drew the Total-row border area as one merged vector path (`get_drawings()` returned a single
   large rect rather than per-cell segments), so the exact per-cell color couldn't be
   independently re-confirmed here the way it was on R07.023/024 — applied per the established
   batch pattern, not silently claimed as freshly measured.
6. **Footer divider line** — measured this report's own reference: `y=790`, `x=22.65-572.6`
   (full column width `550`, narrower than R07.023/024's `1140` since this is portrait),
   `#454087`, width `1.5`. Added the line + moved the 3 footer text elements `y="0"→y="12"` in
   the same edit — correct order on the first render.
7. **Data-column alignment** — center-aligned the Standard Cargo Size value/unit cells (grid 2)
   and the main table's Cargoes INPEX/TOTAL columns in both `<detail>` and `<summary>` (grid 3,
   4 elements) — all were `hTextAlign="Right"`/`"Left"`. Grid 4 (Forecast Entitlement) left
   right-aligned, matching R07.023/024's scope.
8. **Dec/Total gap** — `<summary>` band's 6 Total-row elements were at `y="4"`, confirmed via
   `grep` as the only matches, shifted to `y="0"`. Verified Dec→Total spacing (16pt) now
   matches Nov→Dec spacing (16pt) exactly.
9. **Remarks bordered box** — added a `rectangle` (`#D6D6D6` border, width `550` matching the
   main table) under "Remarks:", moved the `textField` inside it (4pt padding). Verified via
   `get_drawings()` the border spans `x=23-573, y=539-639`.

**New finding, NOT fixed this pass (flagged for owner's call, not silently applied):** the
reference's info-block/Standard-Cargo-Size/main-table content all start at abs `x=34.6`
(local `x≈12`, not `x=0`) while the page's logo/title/divider genuinely start at `x=0`
(abs `≈22.65` = `leftMargin`) — i.e. the reference indents these 3 blocks ~12pt from the page
margin, consistently. The current build (and R07.023/024, unchecked) has them all at local
`x=0`. This is a NEW discovery, not one of the 9 known-repeatable categories from R07.023/024,
so it was NOT applied here without asking first — flagging it for the owner's decision rather
than unilaterally re-positioning every element in the report.

**Verification:** recompiled cleanly; regenerated PDF confirms all 9 fixes render correctly
(teal fills, purple label, purple Total-row border incl. teal cell, footer divider + correct
text order, closed Dec/Total gap, bordered Remarks box, center alignment). Swap into `output/`
pending — the PDF was locked (owner reviewing) at the time of this edit.

## Owner screenshot follow-up (2026-08-31, same session) — title-band overshoot gap, same class as R07.024
Owner screenshot showed a visible gap between the main table's header row and the first data
row ("Jan") — same defect class as R07.024's earlier title-band overshoot (Part O2 in
`JASPERREPORT-7-0-3.MD`). Fixed:
- Measured: header Row 2's lowest element ends at `y=244+17=261`; `<title height="270">` was
  9pt taller than that, showing as a blank gap. Shrunk to `<title height="261">` (the exact
  edge, not a rounded-up guess).
- Recompiled + regenerated; confirmed via `get_drawings()` the header's merged "Lifting Plan"
  cell now ends at `y=289` and the first teal Month cell starts at `y=289` — zero gap.
- **Process note:** during the swap, `rm -f R07_025_PC_CDP.pdf R07_025_PC_CDP_new.pdf` removed
  BOTH files (the old locked one had just released, and the new one alongside it), losing the
  fixed file before it could be renamed into place. Recovered by re-running the verify harness
  straight to the final filename (`R07_025_PC_CDP.pdf`) and re-confirming the fix was intact —
  no data was lost since the JRXML source (the actual fix) was untouched, only a regenerated
  PDF output had to be rebuilt, which is a cheap, deterministic operation. Lesson: when
  swapping in a fix, `mv` the new file over the old one directly rather than `rm` both by name
  in one command — a single `mv` can't accidentally delete the source it's supposed to keep.
- Exactly one PDF remains in `output/` (`R07_025_PC_CDP.pdf`, regenerated 2026-08-31 02:22).

## Owner screenshot follow-up — FE table's TOTAL column stopped short of the info-block's right edge
Owner screenshot (red-boxed) showed the "Forecast Entitlement (bbl)" table's TOTAL column
ending well before the info-block's own right edge, leaving a visible unused strip on the
right side of the page — and asked for the 5 data columns (Cargoes INPEX/TOTAL + FE
Production/INPEX/TOTAL) to share a common width once the table was extended to fill it.
- Measured: FE table previously ended at `x=482` (`408+74`) vs. the info-block's own right
  edge at `x=550` (page's `columnWidth`) — a 68pt gap.
- Recomputed the 5 data columns to share equal width: `96(month) + 88 + 88 + 12(gap) +
  88 + 88 + 90 = 550` (last column 90pt to absorb the rounding remainder from `442/5=88.4`,
  keeping the right edge landing exactly on the column boundary rather than off by a
  fraction). Applied to all 3 layers that reference these columns: header Row 1 group cells
  (`Cargoes` width `141→176`, `Forecast Entitlement (bbl)` `x=249→284, width=233→266`),
  header Row 2 leaf cells (5 cells, all repositioned/rewidened), the `<detail>` band's 5
  data `textField`s, and the `<summary>` band's 5 Total-row `textField`s.
- Recompiled + regenerated; confirmed via `get_drawings()` the FE table's right border now
  lands at `x=573` (abs), exactly matching the info-block's own value-column right border
  (`x=573`) — same page-width alignment, confirmed by direct comparison of both borders'
  x-coordinates, not assumed from the arithmetic alone.
- **Process fix applied from the earlier lesson this same report:** swapped the file via a
  single `mv -f R07_025_PC_CDP_new.pdf R07_025_PC_CDP.pdf` (not `rm` both by name) — no
  repeat of the earlier accidental double-delete.
- Exactly one PDF remains in `output/`.

## FINAL STATUS: Owner-verified OK (2026-08-31)
Owner confirmed the report layout is OK. All fixes carried over from R07.023/024's review
passes (info-block teal labels, Standard Cargo Size box rebuild/alignment, month-column teal
fill, Total-row purple top border incl. teal cell, footer divider line, grid 2/3 center
alignment, Dec/Total gap closure, Remarks bordered box) plus two R07.025-specific fixes
(title-band overshoot gap, FE table width extension + 5-column redistribution to fill the
full page width) are in `output/R07_025_PC_CDP.jrxml` + the single `output/R07_025_PC_CDP.pdf`.
One flagged-but-not-applied finding remains open for the owner's own call: the reference's
info-block/Standard-Cargo-Size/main-table content appears to sit ~12pt indented from the
page's left margin in the ORIGINAL reference PDF (not replicated in this build, which keeps
everything at local x=0) — see the "New finding" note earlier in this file.
**R07.021-025 (all 5 CDP-adjacent + daily-grid reports touched this session) are now
owner-verified OK.** R07.001 remains SCOPED-NOT-BUILT (see its own SCOPING-NOTES.md).
