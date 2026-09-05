# R07.018 — FC Provisional Lifting Program — Completion Notes (2026-08-30)

**Phase:** LAYOUT ONLY (data queries deferred, same convention as prior R07 batch reports).
First of the multi-page "Forecast/Program" family — reference PDF confirmed 4 pages (one per
forecast month: Aug/Sep/Oct/Nov 2025).

**Build location:** `C:\Projects\INPEX\sources\CrystalReports\R07.018\output\`. **Base:**
copied R07.011's JRXML (7-customer-column pattern), adapted to this report's single customer
group + cargo-detail columns + page-per-month grouping.

## New mechanism introduced this report: page-per-group ("Pattern C")
This is the first report in the batch needing JasperReports' `<group>` with
`startNewPage="true"` — one page per calendar month, with a per-month "Opening Inventory" group
header row (carried-forward closing balance) and a per-month Total/Remarks group footer.

## Two real defects found and fixed via the Jackson-error-driven property-discovery technique
1. **Wrong group XML property names** — first attempt used `isStartNewPage` and
   `groupExpression` (guessed from general JasperReports XML docs), both rejected by the
   compact-format Jackson deserializer. The resulting `UnrecognizedPropertyException` messages
   listed the real accepted properties each time: `startNewPage` (not `isStartNewPage`) and
   `expression` (not `groupExpression`, since it's nested inside `<group>` here rather than a
   top-level element name prefix). Same technique already documented in
   `JASPERREPORT-7-0-3.MD` Part D for element `kind`s, now confirmed to work for `<group>`
   properties too.
2. **`<groupFooter name="...">` is not a valid top-level sibling** in this compact format —
   unlike `<detail>`, group header/footer bands must be nested INSIDE the `<group>` element
   itself (`<group>...<groupHeader>...</groupHeader><groupFooter>...</groupFooter></group>`).
   An initial draft had the Total-row/Remarks content in a top-level
   `<groupFooter name="G_MONTH">` sibling (copying `<detail>`'s top-level pattern) — this parsed
   without error but was structurally wrong; caught by re-reading the Jackson known-properties
   list, which showed `groupFooter` as a property of `JRDesignGroup`, not a report-level element.
3. **Title band only prints on page 1, by JasperReports design** — after fixing 1-2, the first
   successful 2-page render showed the full title/subtitle block on page 1 but NOTHING (title
   missing entirely) on page 2, with the pageHeader content shifted up to fill the gap. Root
   cause: `<title>` is a special band that ONLY renders once, at the very start of the report,
   regardless of grouping/page breaks — but this report's reference PDF shows the full title
   block (including the per-page-varying month name) on EVERY page. Fixed by removing the
   `<title>` band entirely and merging its content into the (page-repeating) `<pageHeader>`
   band, shifting the existing Row A/Row B header content down by the title's height (110pt).
   Verified via a 2-row/2-month synthetic in-memory data source (`JRMapCollectionDataSource`)
   since `JREmptyDataSource` can't exercise a month-based group expression (all fields null).

## Report shape (measured directly)
- 18 columns: Date, Production*, Inventory*, Lifting Qty, 7 customer columns (INPEX/TOTAL/OPIC/
  Osaka Gas/Kansai Electric/JERA/Toho Gas) under one "Lifters / Quantity" group, then 7
  cargo-detail columns with no group label (Cargo ID, Vessel, Representative/Lifter, Arrival
  Date/Range, ADR Status, Loading Date/Range, LDR Status).
- Per-month group header: "Opening Inventory" row (same convention as R07.012/014/016's
  per-report Opening Inventory row, but now per-month instead of per-report).
- Per-month group footer: Total row (Production*, Lifting Qty, 7 customer columns summed) +
  free-text "Remarks:" section (replaces the Overall-recap-block pattern from R07.011/013/015 —
  this report has no such block).

## Verification performed
- All 18 header columns measured directly from the reference PDF's own grid-line/fill-rect
  drawings before building.
- Confirmed via a 2-month synthetic data source that: (a) the group/page-break fires correctly
  (2 rows in 2 different months → 2 pages), (b) the title/subtitle block (with correct
  per-page month text) now repeats on every page, (c) the pageHeader column-header content
  correctly repeats on every page at the right y-position after the title-merge fix.

## Not done this phase (by design)
- Live query/data verification — deferred, same as prior R07 batch reports.
- Real Opening-Inventory carry-forward logic (previous month's closing balance) — the
  `OPENING_INVENTORY` field is a placeholder column expected from the future real query
  (likely a subquery/window function), not solved at the layout stage.
- Remarks free-text content/line-count logic — placeholder single-parameter text for now.

## Key takeaway for the remaining multi-page reports (R07.017/019/020/021/022)
The title-band-only-prints-once trap will hit every report in this sub-family identically since
they all share the page-per-month pattern with a repeating title block — apply the
title-merged-into-pageHeader fix proactively from the first draft on each remaining report,
rather than rediscovering it after a multi-page render. Documented in
`JASPERREPORT-7-0-3.MD` Part E for reuse.

## Owner border/layout review pass (2026-08-30, same day, after initial build marked done)
A detailed owner review found several real defects, all confirmed by direct measurement against
the reference PDF's own `get_drawings()`/`search_for()` output before fixing:

1. **Font extension jar not wired into `pom.xml`** — same root cause as every other report in
   this batch. Fixed via the same system-scope dependency.
2. **`DetailTextStyle`/`TotalRowStyle` missing `leftPen`** — fixed.
3. **`DetailTextStyle` defining both `topPen` and `bottomPen`** — same double-drawn-border class
   as prior reports; removed `topPen` from `DetailTextStyle`, kept it on `TotalRowStyle` (real
   gap above the Total row in the groupFooter band).
4. **22 bare `<pen lineWidth="1.0"/>`** (defaulting to black) — fixed to `#D6D6D6`.
5. **Remarks textField undersized for real content** — measured the Remarks section's actual
   text height across all 4 months in the reference PDF (41.1pt Aug, 41.1pt Sep, 51.5pt Oct,
   30.8pt Nov) rather than guessing; the original `height="24"` box would have clipped every
   month's real content. Resized to `height="60"` (band grown from 60 to 100), and put the
   text into a single bordered cell spanning the full 1140pt grid width (owner request), with
   the "Remarks:" label given a ~9pt gap from the Total row (matching the reference's own gap)
   instead of the original 2pt.
6. **Row B (Date row) was an effective 3-line-tall header** — reference's actual Row B height
   measured at ~20.4pt (2-line capacity); the JRXML used `height="28"` (~3-line capacity).
   Reduced to `height="20"` across all 18 leaf columns, `pageHeader` height adjusted from 157
   to 149 accordingly. Row B header text vAlign also changed from `Middle` to `Top` per owner
   request, then given `topPadding="3"` after the owner flagged the text sitting flush against
   the top border with no `Middle` centering to cushion it.
7. **"Field Condensate" subtitle** — made bold and resized to match the title's 18pt font per
   owner request. Caught a real rendering bug in the process: the original box (`height="16"`)
   was too short for 18pt bold text and the text disappeared entirely (JasperReports silently
   drops text that can't fit rather than erroring) — fixed by growing the box to `height="24"`,
   matching the exact height the reference itself uses for this line (confirmed via
   `search_for()`, both title and "Field Condensate" occupy the same ~23.5pt height there).
8. **Opening-Inventory-row style "Remarks:" label leftPen leak** — after item 2 added `leftPen`
   to `DetailTextStyle`, the Remarks label (which reuses that style but only explicitly zeroed
   `topPen`/`bottomPen`/`rightPen`) picked up an unwanted left border. Fixed by explicitly
   zeroing `leftPen` too. **Lesson: any style-level fix must be re-checked against every
   element reusing that style with a box override, not just the elements it was fixed for.**

**Status: report layout verified (2026-08-30). Data queries deferred to a later stage**, same
convention as the rest of the R07.011-022 batch.
