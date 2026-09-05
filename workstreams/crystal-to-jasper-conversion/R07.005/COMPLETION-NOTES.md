# R07.005 — Offshore Production Report — Completion Notes (2026-08-30)

**Phase:** LAYOUT ONLY. Fifth of 6 previously-unbuilt R07 reports (full-rigor scope
confirmed by owner). 2 STATIC pages (title=page1, summary=page2, natural
band-overflow break).

**Build location:** `C:\Projects\INPEX\sources\CrystalReports\R07.005\output\`.

## Report shape (measured directly)
- A3-sized portrait page (842x1191pt), ~22pt margins — same convention as every
  other R07 report.
- MONTHLY offshore report (JULY 2025 sample) — the monthly parallel to R07.006's
  monthly onshore report, and the monthly counterpart to R07.002's daily offshore
  report.
- Largest well-grid of the R07 batch so far: 29 wells x 15 data columns
  (Measured/Allocated/Forecast Production, each with Gas(kSm³)/Cond(Sm³)/
  Water(Sm³), plus MEG Injection HP(m³)/LP(m³)), generated programmatically via
  `gen_wellgrid.py`, followed by a 3-row per-field totals block (Brewster/
  Plover/Total) generated separately from the same measured column positions.
- Second table "Production, Internal Consumption & Losses" uses the SAME
  5-column shape (Monthly Quantity/Short Term Forecast/YTD Quantity/Annual
  Budget Forecast/YTD Variance(%)) as R07.002's DAILY offshore report — single
  "Volume" unit, not the dual Volume+Mass used by the onshore reports (R07.004/
  R07.006). Confirms (from the other direction this time) that column SHAPE
  tracks the onshore/offshore distinction, not reporting cadence — R07.002
  (daily) and R07.005 (monthly) share the same 5-column offshore shape despite
  different cadences, mirroring the R07.004/R07.006 onshore finding.
- 17 label rows in the main table generated programmatically (same
  column-x-range classification approach as R07.004's main table generator).
- Inventory and Liftings sections hand-written (only 2 rows each).
- Page 2: Water and MEG (4 rows), Comments (CPF:/FPSO:).

## Defects found and fixed
1. **Growing-offset bug reintroduced by the well-grid generator, then caught
   before compiling**: the first version of `gen_wellgrid.py` computed each
   row's y from a fixed-increment formula (`start_ly + i * 13`) instead of
   each row's own measured position — the exact same bug class as R10.010,
   which the R10.011 "exact-position method" lesson was supposed to have
   permanently eliminated. Caught by checking the real recon y-deltas between
   consecutive well rows (208, 222, 236, ... — uniformly 14pt apart, not 13),
   which would have produced a 29pt cumulative drift by the last of 29 rows.
   Fixed by using each row's own measured `y` directly (`L(y)`) instead of a
   formula. **Lesson: even when the "exact-position method" is the established
   default, a NEW generator script for a NEW report can still slip back into
   formula-based positioning unless explicitly checked — the fix must be
   re-verified per-script, not assumed to carry over from having been applied
   in a prior report.**
2. **`COL_WIDTHS` (used for element placement) was NOT derived from `COLS`
   (used for column classification during extraction) — a second, more subtle
   version of the same "measured value doesn't match rendered position" defect
   class**: `COL_WIDTHS` held independently-invented local x/width pairs (e.g.
   `MP_GAS: (207, 44)`) that did not correspond to `COLS`' own measured abs
   range for that same column (`MP_GAS: (268, 315)`, which correctly matches
   the reference's own recon). The values were correctly CLASSIFIED into the
   right named column, but then RENDERED at the wrong x position — up to 25pt
   off, silently, with the value still readable and plausible so a text diff
   alone would not have caught it. Caught by a coordinate spot-check comparing
   `search_for()` results between reference and generated PDF for values like
   "18,664" (ref x=278.7 vs first-pass gen x=253.1). Fixed by deriving
   `COL_WIDTHS` directly from `COLS` (`{name: (L(x0), x1-x0) for name, x0, x1
   in COLS}`) instead of maintaining a second, independently-typed table.
3. **Compounding error from defect #2**: the well-grid column HEADER positions
   in `assemble.py` had been copied from the same wrong `COL_WIDTHS` numbers
   (e.g. using `L(207)` for the "Gas"/MP_GAS sub-header, when the header
   word's own real recon position was abs x=268) — so both the header row AND
   the data rows were consistently misaligned by the same wrong offset, which
   is why a first-pass visual read might not have looked "obviously broken" (a
   header and its column both being wrong by the same delta can look internally
   consistent even though both are wrong relative to the reference). Fixed by
   rewriting every well-grid header/sub-header element to use the ACTUAL
   measured recon word positions (e.g. `L(268)` for "Gas", `L(317)` for
   "Cond") instead of the `COL_WIDTHS` placement values.
4. **One header word placed on the wrong line in the main table's multi-line
   column header** ("Quantity" of "Monthly Quantity" was placed at the same y
   as "Volume" instead of at the same y as "Monthly" — a transcription slip
   while hand-authoring the 4-line nested header block for "Monthly Quantity /
   Short Term Forecast / YTD Quantity / Annual Budget Forecast / YTD Variance
   (%)"). Fixed by moving it to the correct line/y matching the reference's
   own row grouping (confirmed via recon: "Monthly" and "Quantity" are both at
   abs y=701.9, while "Volume" is a separate sub-label at abs y=719.7).

## Verification performed
- Whole-page text extraction (`page.get_text('text')`) confirmed page 2 is a
  PERFECT match (23/23 lines). Page 1 has 5 apparent "missing"/9 "extra" line
  pairs, all confirmed to be PyMuPDF line-join artifacts in the main table's
  4-line nested header block (same artifact class already documented for
  R07.004/R07.006) — every individual word ("Monthly", "Quantity", "Short",
  "Term", "Annual", "Budget", "YTD", "Variance", "(%)") is present when
  searched for individually.
- Coordinate spot-check via `search_for()` on 10 representative labels/values
  spanning the well-grid body, the well-grid totals row, and both table titles
  — all landed within the same ~1-20pt tolerance already accepted throughout
  this project (the residual is a right-alignment width-overestimate from
  using each column's full measured boundary rather than its exact text right
  edge — the same class of imprecision already documented and accepted for
  R10.031/R07.004's header spot-checks, not a functional defect: no column
  overlaps, no value landed in the wrong column).
- Row-order check on the generated PDF's own extracted well-grid row (BDC-1A-01)
  confirmed all 15 values appear in the correct left-to-right column sequence
  with proper spacing and no overlaps between adjacent columns.

## Not done this phase (by design)
- Live query/data verification — deferred, same as every prior report in this
  project.

## Key takeaway
Two genuinely new defect sub-classes for this project, both variants of the
same root cause (a rendered position not actually traced back to its own
measured recon value):
1. A generator script re-introducing the formula-based row-height bug that an
   earlier report's lesson was supposed to have eliminated — the lesson must
   be re-applied and re-verified per NEW script, not assumed to persist.
2. A SEPARATE "placement" table (`COL_WIDTHS`) drifting out of sync with the
   "classification" table (`COLS`) it was meant to correspond to — both were
   internally self-consistent (values correctly classified, headers
   consistently offset the same way as their data), which is precisely why a
   quick visual read would not have caught it. Both were only caught by a
   `search_for()` coordinate check comparing generated vs. reference PDF, not
   by the whole-page text diff — reinforcing the standing project rule that a
   clean text diff is necessary but never sufficient.

---

## FULL RE-AUDIT (2026-08-31) — same rigor as R07.002's 8-round rebuild, per the
Post-mortem 12-item checklist in `DeepDiveLearnings/JASPERREPORT-7-0-3.MD`

**Trigger:** the 2026-08-30 build above was verified with only a text-extraction
match + a 10-label coordinate spot-check — exactly the shallow verification
method that R07.002 needed 8 owner-pushback rounds to expose as insufficient.
This pass re-ran the full 12-item checklist from scratch: color/fill histogram
(`get_drawings()`), full-page render-and-look, `get_text('dict')` font checks,
and a whole-page word-frequency diff. It found the SAME class of wholesale
defects R07.002 had — this build had never actually been color/border/font
audited despite being marked "done."

### Defects found and fixed (13 distinct items, mapped to the 12 checklist categories)

1. **[Category 1 — color/fill scheme] Entire color/border scheme was invented,
   not measured.** `get_drawings()` histogram showed: 0 of the reference's 599+18
   gray `#D6D6D6` gridline borders present anywhere; 0 of 36+4 real purple
   `#454087` header fills (the only 2 "purple" elements in the build used the
   wrong shade `#444080` AND were on the WRONG elements — see #12); 0 of the
   4+2 dark `#636363` section dividers; 0 of the 2+2 `#454087` divider lines
   under the title. `ValueCellStyle` used an invented light-blue `#F8FBFC`
   fill with a bare black `width=0.5` pen instead of the reference's real
   scheme. Fixed at the STYLE level (`ValueCellStyle`/`PlainLabelStyle`/
   `PlainValueStyle` given real `#D6D6D6` box borders; `PurpleSectionStyle`
   corrected to `#454087`; new `HeaderCellBoxStyle`/`HeaderTextOverlayStyle`
   pair added for the rectangle+overlay header pattern, per Part D1/P1 — a
   `rectangle` element's border comes from its OWN `pen`, never a referenced
   style's `<box>`).
2. **[Category 2 — logo/dividers/title position] Logo image completely
   absent** (zero `<element kind="image">` in the whole file) **and title/date
   were at the wrong y** (measured directly from this report's own reference:
   logo abs bbox (22.65,39.35,150.2,61.35) -> local x=0 y=17 w=128 h=22; title
   abs y=41.1-64.6 -> local y=19, was y=10; date abs y=73.3-85.6 -> local y=51,
   was y=38). Added the logo + corrected positions on both the title band
   AND the summary band (page 2 needs its own copy per Part E2 — `<title>`
   only ever prints page 1).
   - **Logo extraction gotcha (new, not previously documented):** the
     reference PDF's embedded logo XObject (xref 21, plain `FlateDecode`
     `DeviceRGB`, no unusual filters) decodes to a visibly DISTORTED image via
     EVERY direct-extraction method tried — `Pixmap(doc, xref)`,
     `page.extract_image()`, and a fully manual `zlib.decompress()` of the raw
     stream all produced the same wrong, sheared-looking logo, even though the
     decompressed byte count matched `width*height*3` exactly (no predictor
     mismatch). Yet `page.get_pixmap(clip=...)` — i.e. asking MuPDF to actually
     RENDER that region of the real page — produces a perfectly correct
     "INPEX" logo every time. **Root cause not fully identified** (something in
     the image's actual PDF-level color/transform handling differs from a
     naive raw-byte interpretation); **the reliable fix is to extract the logo
     via a high-DPI `get_pixmap(clip=<real bbox>)` crop of the reference page
     itself, never via `Pixmap(doc, xref)`/`extract_image()` on the image
     object directly** — worth adding to the lessons file as a new rule for
     future reports with embedded raster logos.
3. **[Category 3 — font extension jar] `inpex-arial-fonts.jar` was never wired
   into this report's `pom.xml`/`output/fonts/` at all** — every other R07/R10
   report in this project has it; R07.005 was missing it entirely, meaning
   every `isBold`+`isItalic` combination (used throughout: title, all 6
   section titles, all purple header cells, footer italic) had zero chance of
   rendering as real bold-italic in PDF. Copied the jar from R07.002's
   `output/fonts/`, added the `com.inpex:inpex-arial-fonts` system-scoped
   dependency to `pom.xml`. Verified via `get_text('dict')` on the real
   exported PDF (not assumed): every checked span now reports
   `font='Arial-BoldItalicMT'` or `'Arial-ItalicMT'`, matching the reference's
   own `ArialBoldItalic`/`ArialItalic`.
4. **[Category 4 — header fix must propagate to data rows] Multiple tables'
   data rows still referenced pre-rebuild column boundaries after their
   headers were rebuilt**, producing visible border gaps/overlaps once real
   borders existed (Part R1/Q3 — "adding a border can expose a pre-existing
   coordinate gap that was invisible when borderless"):
   - Well-grid: the "Online (hrs)" data column sat at local x=208 while
     "Status at month end" ended at x=183 — a real, ~25pt UNBORDERED gap in
     the original build that, once every cell got a box border this session,
     rendered as a distinct blank bordered column with no data in it. Fixed
     by re-pointing all 29 rows' Online-column value to x=183 width=47
     (confirmed via a 600dpi zoom crop, byte-for-byte matching the reference
     at the same crop).
   - Main table ("Production, Internal Consumption & Losses"): all 5 value
     columns across all ~13 data rows were re-pointed from their old x/width
     (258/373/473/558/678) to the rebuilt header's real sub-column boundaries
     (215/329/440/556/670); the label column widened 280->213 to match the
     header's merged label cell (except the 4 full-width bold sub-header rows
     "Production"/"Internal Consumption"/"Losses"/"Delivered", widened
     280->787 since the reference draws ONE full-width box for those, not a
     per-column box).
   - Inventory table: label 300->326, value cells re-pointed to 329/556 to
     match the header.
   - Liftings table: label 200->224, 3 value cells re-pointed to 228/407/598.
   - Water and MEG (page 2): label cells shrunk 390->326 (they OVERLAPPED
     390pt into the Monthly-Quantity column, 63pt past the header's real
     boundary at 329 — same defect class, opposite direction).
5. **[Category 5 — row height vs. row spacing] Not applicable as a separate
   defect this pass** — the well-grid/main-table row heights were already
   sized to their real recon spacing in the 2026-08-30 build; no gap/STUCK
   border defect of this specific class was found once the column-boundary
   fixes above were applied.
6. **[Category 5b/new — SILENT TEXT DROP, found only by a whole-page
   word-frequency diff, not by any visual glance] THREE elements lost their
   text entirely, with zero compile warning, exactly the Part F1/N2 class of
   bug:**
   - The MAIN TITLE "Ichthys: Offshore Production Report" (21pt bold-italic)
     was completely absent from BOTH pages' extracted text — `height="24"`
     was too short for 21pt text (F1's rule of thumb: `fontSize*1.2` +
     margin, ~29-30pt needed here). This is the single most severe defect of
     the session: every full-page render I looked at BEFORE running
     `page.get_text('text')` looked fine to a quick glance (the blank space
     where the title should be just reads as "a bit of whitespace under the
     logo" unless you're specifically looking for the title text) — it was
     only caught by the mandatory whole-page word-count diff against the
     reference. Fixed by growing height 24->30 on both the title-band and
     summary-band copies.
   - The main table's "YTD Quantity" row-1 group header (the one positioned
     at its own real recon bbox rather than centered across the full fill,
     per the earlier session's approach) was ALSO dropped — first by the same
     height-too-short cause (11 -> 14 fixed it enough to stop the outright
     drop), then STILL missing the word "Quantity" specifically (only "YTD"
     rendered) because the element's width (63pt, taken directly from the
     reference's own measured text width) was too narrow for this engine's
     actual Arial-BoldItalicMT metrics — the reference's measured width is
     not a safe proxy for this engine's render width. Fixed by widening to 90pt.
   - **Rule reinforced: a full-page `page.get_text('text')` word-frequency
     diff against the reference (Part P4) is MANDATORY after every session,
     not optional — this class of bug produces a render that still "looks
     fine" in a full-page screenshot glance (a few extra points of blank
     space reads as normal margin, not as "the title is gone") and would
     have shipped as a genuinely broken report otherwise.**
7. **[Category 6 — blank/empty columns] Not found this pass** — every column
   in every table had a genuine element in every row this session (no
   omitted-element defect of the R2 class was discovered).
8. **[Category 7 — free-text blocks] "Note: Excludes liftings in progress at
   month-end" was `PlainLabelStyle` at plain 6pt with no italic** — reference
   is `ArialItalic` 9pt. Fixed the font, and explicitly zeroed its box border
   (`<box><pen lineWidth="0.0"/></box>`) since `PlainLabelStyle` now carries a
   border at the style level and this is a free-standing disclaimer, not a
   table cell (Part R4).
9. **[Category 8 — bold/italic/alignment verified per-element] Confirmed via
   `get_text('dict')` span font names** (not assumed): title/section-titles/
   header-cells all `Arial-BoldItalicMT`; body values plain `Arial` 8pt (was
   6.5pt — wrong size, confirmed via the reference's own span sizes); footer
   `Arial-ItalicMT` 6pt (was plain 7pt, no italic).
10. **[Category 9 — row-rect width re-derived per table] The 32 well-grid
    row-background rectangles (`ValueCellStyle`, bare `pen lineWidth="0.5"`,
    no `lineColor`, width fixed at 699 regardless of the table's real column
    sum) were REMOVED entirely** — the reference has ZERO fill/background on
    well-grid data rows (confirmed via `get_drawings()`: no extra fill color
    in that region), so the "699-wide row rect" was never a real reference
    convention to fix the width of — it needed removing, not resizing. Every
    cell's own border now comes from `PlainValueStyle`/`PlainLabelStyle`'s
    style-level `<box>` pen instead.
11. **[Category 10 — opaque-fill overlay offset] The two WRONGLY-purpled
    section titles ("Water and MEG"/"Comments" on page 2) were both fill AND
    border wrong** — see #12; once converted to plain `TitleStyle` text (no
    fill/border at all, matching the reference), this category became
    not-applicable for them. The genuine purple header-cell rectangles
    (`HeaderCellBoxStyle`) all use the rectangle-owns-its-own-pen pattern
    (Part P1), so no opaque-text-over-rect offset defect was introduced this
    session.
12. **[Owner-caught-class defect, Part Q1(b)] "Water and MEG" and "Comments"
    (page 2) were WRONGLY given the full `PurpleSectionStyle` rectangle+fill
    treatment** — the reference shows these as PLAIN italic-bold titles
    (identical treatment to "Subsea Production"/"Inventory"/"Liftings" on
    page 1); only the TABLE HEADER row below each is purple, not the section
    title itself. This is the exact defect class R07.002's owner-review
    round 2 found ("roughly half the section titles were wrongly purple-filled
    bars") — confirmed here by direct recon (`get_text('dict')` showing black,
    not white, text color at that y-position) before fixing, not assumed.
13. **[Category 11 — section-title-to-divider spacing] All 6 section titles
    (Subsea Production, Production/Internal Consumption/Losses, Inventory,
    Liftings, Water and MEG, Comments) were missing their gray `#636363`
    width-1.5 divider line entirely** (this report had 0 of the reference's
    6 total section dividers before this pass) **and the title band/summary
    band were both missing the top-level purple `#454087` divider** under the
    date. All 8 dividers added at their real measured abs-y positions (minus
    margin for local y), and cross-checked for consistent title-to-divider
    gap against each other (all title-band dividers sit 18pt below their
    title's own y, matching across all 4 page-1 titles and both page-2
    titles — self-consistent, Part T3).

### Verification performed (real commands, real evidence — not assumed)
- `get_drawings()` color-palette histogram, reference vs. every intermediate
  build, through 4 iterations until every purple-fill/divider-line category
  matched the reference count exactly (page 1: purple fills 36 ref / 35 gen —
  off by 1, investigated via direct visual zoom crop, no visible defect found,
  accepted as a rect-count artifact not a rendering gap; dark dividers 4/4
  page1, 2/2 page2 EXACT MATCH; purple dividers 2/2 page1, 2/2 page2 EXACT
  MATCH).
- `page.get_pixmap()` full-page renders at 150dpi for every intermediate
  build (7 rounds) and 600dpi zoom crops of the well-grid header, main-table
  header, inventory/liftings, and the Online-column gap specifically — each
  crop directly compared side-by-side against the identical crop region of
  the reference PDF.
- `get_text('dict')` span-level font verification: confirmed real
  `Arial-BoldItalicMT`/`Arial-ItalicMT` rendering (not a silent fallback to
  plain Helvetica) for every bold/italic element checked.
- **Whole-page `page.get_text('text')` word-frequency diff (Counter subtraction,
  Part P4), both pages, FINAL BUILD: 0 missing, 0 extra on page 1 AND page 2** —
  a perfect match, achieved only after finding and fixing the 2 silently-dropped
  text elements in item #6 above.
- Recompiled and re-checked page count (2 pages, matching the reference)
  after every band-height-adjacent change (title height, header cell heights),
  per Part S2/O2 — no unexpected page-count drift at any point.
- Confirmed the font extension jar is actually on the runtime classpath
  (`mvn dependency:build-classpath` re-run after adding the system-scoped
  dependency) and produces the correct font names in the exported PDF, not
  just "added to pom.xml and assumed to work."

### The gray-gridline count residual (not fixed, disclosed)
`get_drawings()` reports far more `#D6D6D6` width-1.0 line entries in the
generated PDF (2263 vs. the reference's 599 on page 1; 60 vs. 18 on page 2).
Investigated via a 600dpi zoom crop of a representative well-grid region,
compared directly against the same crop of the reference: **the rendered
output is visually indistinguishable from the reference** — same line
weight, same color, no doubled/thickened lines apparent at zoom. The count
discrepancy is attributed to this build's `<box>`-per-style-per-element
approach (every `PlainValueStyle`/`PlainLabelStyle` cell independently
declares all 4 box sides) producing more separate line-drawing primitives
than however the reference's original Crystal-Reports-exported PDF grouped
its own border strokes — a measurement-method artifact (per Part D4's
standing warning to verify a checking method before trusting a raw count),
not a visual defect. Flagged here rather than silently ignored: if a future
owner review finds a real visual thickness difference at this project's
established review rigor, this is the place to look first (Part M8's "shared
topPen+bottomPen double-draws every interior boundary" pattern would be the
next thing to check, by removing `topPen` from the shared cell style and
re-measuring) — not attempted this pass given the zoom-crop evidence showed
no actual visual defect to fix.

### Final state
- **Page count: 2 (confirmed matching reference), reproduced via a fresh
  `mvn dependency:build-classpath` + compile from the checked-in `pom.xml`/
  `output/fonts/inpex-arial-fonts.jar`/JRXML with zero manual steps.**
- Whole-page word-frequency diff: **0/0 missing, 0/0 extra, both pages.**
- Color-fill histogram: purple fills, dark dividers, and purple dividers all
  match the reference count (within 1, investigated and accepted).
- Fonts: real `Arial-BoldItalicMT`/`Arial-ItalicMT` confirmed rendering via
  `get_text('dict')`, not assumed from a visual glance.
- Backups: `.backup_20260831_pre_audit` (before this session's first edit)
  and `.backup_20260831_post_audit_verified` (after all fixes, verified) both
  retained alongside the original `.backup_20260830_091500`.
- **This report is now considered genuinely visually matching its reference**
  at the same rigor level R07.002 required 8 owner-pushback rounds to reach —
  achieved here in one session by applying that report's own lessons
  up front, plus finding 2 new defect sub-classes (the logo-extraction
  distortion, and the silently-dropped title/header text) not previously
  documented anywhere in the project's lessons file. Both should be added to
  `DeepDiveLearnings/JASPERREPORT-7-0-3.MD` as new Parts.

## Owner rejection (2026-08-31) — personal full-page visual comparison, one real fix found
The owner rejected this report alongside R07.003/004/006 despite the audit above reporting it
verified — the audit's checks (word-diff, histogram, font check) were real but not a substitute
for reading the whole page directly. A personal full-page render-and-read comparison of R07.005
found one confirmed, measured defect (checked via `search_for` coordinates, not visual guess):
sub-item labels under Production/Internal Consumption/Losses/Delivered were under-indented —
reference delta ≈11.7pt from the section label, build was only ≈10.75pt short of that (13
elements at `x=2`, moved to `x=13`; re-measured after fix: 39.0pt absolute vs reference's 38.75pt,
matching within 0.3pt). Page 2 and the rest of page 1 were re-checked directly and found to
already match closely — no other defects found in this pass. Recompiled, page count unchanged
at 2.
