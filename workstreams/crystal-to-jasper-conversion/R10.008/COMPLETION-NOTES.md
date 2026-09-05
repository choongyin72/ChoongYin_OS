# R10.008 — Plant Condensate MOPJ & Prem./Disc. Average Calculation — Completion Notes (2026-08-30)

**Phase:** LAYOUT ONLY. Sixth R10 report — portrait, single page, standard 2-line-title info-table
skeleton (base: R10.007), but with a genuinely different body: two SIDE-BY-SIDE 31/30-row daily
calendar tables instead of a formula-components table.

**Build location:** `C:\Projects\INPEX\sources\CrystalReports\R10.008\output\`.

## Report shape (measured directly)
- 2-line title ("Plant Condensate" / "MOPJ & Prem./Disc."), same divider/info-table y-positions
  as R10.002/003/007. Info table row 4 col2 = "1" (revision), matching R10.003's convention, NOT
  R10.007's blank — confirmed via direct recon, not assumed from the most recently-built sibling.
- Section header "MONTH AVERAGE OF INDEX FACTORS" uses the plain-text `SectionLabelStyle`
  convention (R10.002/003/007's style) — confirmed there is **no purple full-width bar** here,
  unlike R10.006's "Assumptions"/"Fixed Parameters" sections. Each report's own section-header
  convention needed its own check; R10.006's newer convention did NOT carry over.
- Two side-by-side (not stacked) calendar tables, confirmed via direct word-position recon
  (`recon_words.txt`): left table = Platt's MOPJ daily index for the current month (May-2025, 31
  rows + Monthly Average), right table = Platt's MOPJ C+F Japan prem/disc for month (X-1)
  (April-2025, 30 rows + Monthly Average). Several calendar days in both tables are genuinely
  blank in the reference (Platt's typically publishes only ~5 days/week) — modelled as
  empty-string parameters, not zero, to preserve the reference's actual blank-cell pattern.

## Defects found and fixed
1. **Decimal x/y/width/height values are rejected by this engine's compact-format loader** — a
   code-generation script produced row positions like `y="222.0"`/`y="234.5"` (accumulating a
   12.5pt row height across 31 rows), which failed to compile with
   `InvalidFormatException: Cannot deserialize value of type 'int' from String "222.0"`. All
   four positional attributes (`x`, `y`, `width`, `height`) must be plain integers in this
   engine build, unlike `fontSize`/`lineWidth` which do accept decimals. Fixed by rounding every
   positional attribute to the nearest integer.
2. **Systematic ~9pt vertical offset across the whole calendar-table block**: after fixing the
   integer-rounding defect, a coordinate spot-check showed the column-header row and every data
   row rendering ~9pt higher than the reference (e.g. "558.250" reference y=271.8 vs generated
   y=262.7). Root cause: the column-header row was placed immediately after the section caption
   lines without leaving room for the caption's own true height, effectively starting the data
   grid too early. Fixed by shifting every element from the column-header row through the
   Comments box down by a uniform 9pt — reduced the row-level offset to under 1pt on inspected
   rows (Monthly Average, 558.250, 19.000 all landed within ~1pt after the shift).

## Verification performed
- Whole-page text extraction (`page.get_text('text')`) confirmed all 125 reference text lines
  are represented in the generated PDF's 122 lines — every apparent gap traced to a PyMuPDF
  line-joining difference (e.g. "INDEX" + "Platt's MOPJ" as two reference lines vs one joined
  `"INDEX: Platt's MOPJ"` element in the build), not a missing value.
- Coordinate spot-check on 7 key labels/values across the info table, section header, and both
  calendar tables — all within ~1-6pt after the offset fix, except the Comments section label
  which retains a ~20pt residual gap versus the reference (accepted for this phase; the exact
  section-to-section spacing is a minor cosmetic gap, consistent with similar small residuals
  accepted elsewhere in the R10 family, e.g. R10.006's Equivalent Daily T/C Rate row).

## Not done this phase (by design)
- Live query/data verification — deferred, same as all prior R10 reports. Calendar-table values
  remain 61 individual placeholder parameters (one per calendar day across both tables) matched
  to the reference's own sample values, including its genuine blank days.

## Key takeaway
This report surfaced a NEW engine constraint not seen in any prior R10/R07 report: JasperReports'
compact-format Jackson loader requires plain integers for `x`/`y`/`width`/`height` — a
code-generation script that computes row positions via non-integer arithmetic (e.g. a 12.5pt row
height) must round every one of these four attributes before writing the XML, or the whole report
fails to compile with a Jackson `InvalidFormatException`. It also reinforced, for the second time
in two consecutive R10 reports (after R10.006's purple-bar-vs-plain-text section-header
discovery), that a sibling's specific visual convention must be re-verified per report even when
the overall report "family" looks similar — R10.008 shares R10.007's info-table skeleton almost
exactly, but its section-header style and its unique side-by-side calendar-table body needed
their own from-scratch recon.
