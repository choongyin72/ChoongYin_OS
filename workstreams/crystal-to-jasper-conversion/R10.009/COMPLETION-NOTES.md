# R10.009 — Plant Condensate Freight Rate Calculation — Completion Notes (2026-08-30)

**Phase:** LAYOUT ONLY. Seventh R10 report — portrait, single page, 2-line title + standard info
table (base: R10.007/R10.008), combining a boxed single-line formula (R10.007's pattern), a
First-Half/Second-Half formula-components table (R10.007's pattern), AND two side-by-side
15-day half-month calendar tables (R10.008's pattern) in one report.

**Build location:** `C:\Projects\INPEX\sources\CrystalReports\R10.009\output\`.

## Report shape (measured directly)
- 2-line title ("Plant Condensate Freight" / "Rate Calculation"), standard 4-row info table
  (row 4 col2 = "1" revision, same as R10.008/R10.003).
- Confirmed via direct word-position recon that the VISUAL top-to-bottom order differs from
  `get_text('text')`'s linear reading order — same underlying-content-stream-order phenomenon
  already documented for R10.008's Comments label. The real visual order is: Title → Info table →
  "Freight Rate Formula" (boxed single-line text) → "Freight Rate Calculation" (First/Second-Half
  table, 3 rows, 2 of them with 2-line labels) → "Half Month Average of Platts Spot Rate (30kt
  SIN-JPN)" (two side-by-side 15-day calendar tables) → Comments → footer.
- The two half-month calendar tables are, confirmed via direct x-position recon: "Second Half of
  April-2025" on the LEFT, "First Half of May-2025" on the RIGHT — an order that isn't
  chronological left-to-right and must not be assumed.
- Freight Rate values (20.988 / 21.437) match R10.007's own Freight Rate line-item parameters
  exactly — confirms R10.009 is the upstream source calculation feeding R10.007's downstream
  Contract Price formula (a useful cross-reference for later live-query wiring, though out of
  scope for this layout-only phase).

## Defects found and fixed
1. **"Freight Rate Calculation" table column headers wrongly duplicated both header lines into
   both sub-columns** (each of the 2 value columns showed BOTH the period label AND "% of
   Worldscale", instead of splitting them — the period label belongs over the date column, "% of
   Worldscale" over the value column). This is a different defect from the calendar-table header
   in R10.008 (which correctly used two distinct texts per column) — here the copy/paste
   introduced the same text twice. Fixed by removing the duplicate lines and keeping exactly one
   caption per header cell.
2. **The whole "Freight Rate Calculation" table was built far too wide**, spanning the full
   539pt column width (label 269pt + two 135pt value columns) copied from R10.007's
   formula-components table convention, without checking this report's OWN column positions.
   Direct recon showed the real table is much narrower (label ~140pt, each value column ~110-
   120pt, total ~380pt, not 539pt) — confirmed via the actual reference value positions (e.g.
   "20.988" at abs x=251, "21.437" at abs x=378.5, nowhere near the 539pt-wide layout's expected
   positions). Fixed by rebuilding all three data rows plus the header row with label width=140,
   H1 column x=140 width=120, H2 column x=260 width=120 — post-fix values landed within ~5-12pt
   of the reference, consistent with tolerances already accepted elsewhere in this family.

## Verification performed
- Whole-page text extraction (`page.get_text('text')`) confirmed all reference text content is
  represented (82 reference lines vs 76 generated, with every apparent gap traced to a PyMuPDF
  line-wrap/line-join difference, not a missing value) — this initially masked the duplicated-
  header defect (both wrong copies were still "present" as text), which was only caught by
  reading the raw diff output carefully enough to notice the duplication pattern, not just
  counting lines.
- Coordinate spot-check using exact-string word matching (to avoid the substring-ambiguity
  problem of repeated tokens like "148.556" appearing in two different sections) confirmed the
  Freight Rate Calculation table's values land within ~5-12pt of the reference after the
  column-width fix.

## Not done this phase (by design)
- Live query/data verification — deferred, same as all prior R10 reports.

## Key takeaway
Two lessons converge here: first, a whole-page text diff can look "clean" (no missing/extra
lines) even when content is structurally WRONG (duplicated into the wrong cells) — text-presence
verification catches missing/extra content but not misplaced-but-present content; a coordinate
check is still required even when the text diff passes. Second, and repeating a lesson from
R10.007 in a new form: copying a sibling report's table STRUCTURE (row layout, style names) is
fine, but copying its exact COLUMN WIDTHS without re-measuring is not — R10.007's
formula-components table genuinely spans the full page width, but R10.009's superficially similar
table is much narrower, and only direct recon of this report's own reference values would have
caught that before building.
