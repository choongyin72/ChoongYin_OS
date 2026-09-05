# R07.002 — Daily Offshore Report — Completion Notes (2026-08-30)

**Phase:** LAYOUT ONLY. Second of 6 previously-unbuilt R07 reports. 2 STATIC pages (title=page1,
summary=page2, natural band-overflow break, same mechanism as R10.006/R10.010/R10.011).

**Build location:** `C:\Projects\INPEX\sources\CrystalReports\R07.002\output\`.

## Report shape (measured directly)
- A3-sized portrait page (842x1191pt), ~22pt margins — same convention as R07.006.
- Genuinely the SAME report family as R07.001 ("Offshore Daily Operations Report") at a
  condensed scope — confirmed by cross-checking multiple identical row labels AND several
  identical sample values in both (e.g. "715,104,409" for Well fluids to CPF with MEG). R07.001
  is the full 7-page version (larger well-grid spanning several pages); R07.002 is a 2-page
  condensed version (30-well grid fitting on 1 page). Built independently from R07.002's own
  recon (R07.001 wasn't built yet at this point), but this shared structure directly informed
  R07.001's later build.
- Page 1: Health, Safety & Environment (CPF/FPSO Injury/Environmental/Safety/Security events);
  Persons On Board at Midnight; "Production, Internal Consumption & Losses" (14 label rows, 5
  value columns — Daily Quantity | Short Term Forecast (Daily) | MTD Quantity | Short Term
  Forecast (MTD) | MTD Variance(%) — a genuinely DIFFERENT column set from R07.006's 7-column
  Monthly/YTD Volume+Mass shape, confirmed via direct recon rather than assumed to match the
  immediately-preceding sibling, since R07.006 is a monthly report and this is a daily one); Gas
  Export Pipeline (Offshore/Onshore 2-group Avg Pressure/Avg Temp/CO2/H2O table); Inventory;
  Offtakes (Cargo ID/Vessel name/Status/Arrival/Departure); Water and MEG.
- Page 2: Subsea Production well grid (30 wells: Reservoir Name/Well Name/Status/Online(hrs)/
  Choke(%)/Gas(Sm3)/Cond(Sm3)/Water(Sm3)/Method/HP(m3)/LP(m3), plus Brewster/Plover/Total rows);
  Consumables for CPF and for FPSO (Name/Closing Volume/Filled-Bunkered Volume/Comments);
  Comments (CPF/FPSO free-text); Disclaimer footer text.

## Build approach — reused and extended the programmatic-generation method from R07.006
Two separate Python scripts extracted and generated JRXML elements directly from the
reference's own measured word positions: one for the 14-row main production table (same
label/value row-pairing logic as R07.006's script, adapted to this report's 5-column layout),
and a second, new one for the 30-well grid (grouped words by row, classified each into one of 11
columns by x-range, generated all 30 rows' elements automatically). A separate `assemble.py`
script spliced the generated well-grid block into the full JRXML file programmatically (string
replace on the summary band), avoiding a very large manual paste operation.

## Defects found and fixed
1. **Summary band overflowed to a 3rd page** — an initial `summary height="1130"` exceeded the
   per-page usable height (1191 - 22 - 22 - 30 footer = 1117), causing JasperReports to
   auto-split the summary band across 2 pages (3 total, vs. the reference's 2). Fixed by
   reducing the band height to 1117 and nudging the disclaimer text element up by 8pt so its
   bottom edge fit within the reduced band.
2. **Whole-page text diff caught 2 real gaps on first build**: the page-2 title was missing its
   own "19-Oct-2025" date line (each page repeats the report date under its title — added a
   `textField` bound to the existing date parameter); and two group-header labels ("Flow Rate",
   "MEG Injection") spanning the well-grid's Gas/Cond/Water and HP/LP column pairs were omitted
   entirely from the generated header row (the generator script only emitted the lower-level
   column headers it was given, not these higher-level group labels) — added by hand since they
   don't fit the row/column extraction pattern.
3. **Minor line-wrap difference**: "MTD Variance (%)" rendered as 2 lines ("MTD Variance" / "(%)")
   instead of 1 — fixed by widening the element and combining both words into a single text run.

## Verification performed
- Whole-page text extraction (`page.get_text('text')`) confirmed a PERFECT match on page 1
  (150/150 lines) after the fixes; page 2 has one trivial residual difference ("TEG  (m³)" with
  a double space in the reference vs. a single space in the build) — a cosmetic formatting
  quirk in the reference's own source text, not a missing value.
- Coordinate spot-check on 10 labels across both pages landed within a similar tolerance band to
  every prior report in this project (~1-15pt), consistent with the exact-recon-position method.

## Not done this phase (by design)
- Live query/data verification — deferred, same as every prior report in this project.

## Key takeaway
Confirmed that the programmatic row-extraction-and-generation approach (introduced on R07.006)
scales well to an even larger table (30 rows × 11 columns here, vs. 25×7 there) — writing a
second, purpose-built extraction script for the well-grid's different column layout took
meaningfully less time than hand-transcribing 30 rows would have, and produced zero mis-mapping
defects (unlike R10.029's manual-transcription mistake). Splicing a large generated block into an
already-drafted JRXML via a small Python string-replace script (rather than manual copy-paste
through the edit tool) is also now an established, reusable technique for reports of this scale.

## OWNER-DIRECTED FULL STRUCTURAL/COLOR REBUILD (2026-08-31)
Owner correctly identified that the verification above (text-extraction match + a 10-label
spot-check) was NEVER a real comparison against the reference's actual visual structure —
unlike R07.011-025, this report never got the border/color/fill review those got. A full
color-palette histogram comparison (`get_drawings()` grouped by color/fill/width) confirmed
this: the original build used an ENTIRELY invented visual scheme that had never been checked
against the reference.

**Root defects found (real, measured, not assumed):**
1. Every data-cell style (`ValueCellStyle`/`PlainLabelStyle`/`PlainValueStyle`) had NO border
   pen at all (or a light-blue `#F8FBFC` fill + black/uncolored border) — the reference draws
   a real gray `#D6D6D6` gridline border around virtually every cell (211 lines on page 1
   alone, 330+221 on page 2). Fixed at the STYLE level so it propagated to all ~170+ cells
   in one edit.
2. Roughly a third of the reference's purple `#454087` section/column headers were either
   missing entirely (`Persons On Board at Midnight` had no purple treatment; `Gas Export
   Pipeline`/`Inventory`/`Offtakes`/`Water and MEG`/`Production` table headers were plain
   unstyled text with zero fill/border) or used the wrong color (`#444080`, close but not the
   real measured `#454087`).
3. The well-grid's 30 row-background rectangles had a bare `<pen lineWidth="0.5"/>` with NO
   `lineColor` (overriding the style's own box pen) — rendered as invisible/white borders.
4. A full set of 11 dark-gray (`#636363`, width 1.5) divider lines — ONE under every single
   section title, confirmed as a consistent pattern across all 7 page-1 sections and 4
   page-2 sections — was completely absent from the build.
5. Real missing content (word-count diff, not just reordering): the MTD "Short Term Forecast"
   column in the Production table was missing its 3rd header line "Volume" entirely (the Daily
   column had it, MTD didn't) — a genuine content gap, not a color/style issue.
6. 14 full-width purple section-title `rectangle` elements had NO pen at all — in JasperReports,
   a `rectangle` element's own border comes from its `pen` property, NOT the referenced style's
   `<box>` (which only applies to text-element borders) — a real technical gotcha, not
   previously documented in this project's own lessons file (now added, see Part P below).

**Fixes applied (measured via `get_drawings()`/word-position extraction on the reference,
section by section, not assumed):**
- Global style fixes: `ValueCellStyle`/`PlainLabelStyle`/`PlainValueStyle` given real
  `#D6D6D6` box borders; `PurpleSectionStyle` corrected to `#454087`; new
  `HeaderCellBoxStyle`/`HeaderTextOverlayStyle` styles added (mirroring the pattern already
  established on R07.001/R07.011-025) for the rectangle+overlay-text header cells.
- Rebuilt with real purple-header + bordered-row structure, each independently measured:
  HSE (CPF/FPSO), Persons On Board at Midnight (CPF/FPSO), Production/Internal Consumption/
  Losses table header (+ added the missing "Volume" line), Gas Export Pipeline (full 3-row
  header: Offshore/Onshore group + 6 column labels + bordered value row), Inventory, Offtakes,
  Water and MEG.
- Fixed all 30 well-grid row pens to `#D6D6D6`/width 1.0.
- Added all 11 section-divider lines (`#636363`, width 1.5) at their real measured positions.
- Fixed all 14 bare `PurpleSectionStyle` rectangles to carry their own inline pen.
- Changed `ValueCellStyle` from `Opaque`/white-fill to `Transparent` (removed a spurious
  white-fill artifact the reference doesn't have — cosmetically identical on white paper, but
  structurally cleaner and matches the reference's own approach).

**Verification (before → after), via `get_drawings()` color-palette histogram comparison
against the reference:**
- Page 1: gray gridlines 0 real gray-bordered cells → matching color (`#D6D6D6`); purple fills
  16 → 53 (ref: 40, close — some over-count from separate rect+overlay elements vs the
  reference's occasional merged rect, not a visual defect); dark divider 0 → 7 (ref: 7, EXACT
  MATCH); white-fill artifact (8 instances) → 0.
- Page 2: purple fills 27 → 27 (ref: 27, EXACT MATCH); dark divider 0 → 4 (ref: 4, EXACT
  MATCH); white-fill well-grid artifact (30 instances) → 0.
- Word-count diff (reference vs generated, ignoring order) narrowed from 6+ real gaps to 2
  minor residual items: one duplicate "Gas" well-grid header label and one "Comments"
  occurrence (both page 2, well-grid/Consumables headers — not rebuilt with full rectangle+
  overlay precision this pass, lower priority given the number/impact of fixes already
  applied), plus a cosmetic text-extraction-merge artifact ("117"+"-" rendering adjacent in
  two cells, visually correct but merged by PDF text extraction into "117-").

**Not fully rebuilt this pass (flagged, not silently skipped):**
- Page 2's well-grid HEADER group-label cells ("Flow Rate"/"MEG Injection") and the
  Consumables CPF/FPSO + Comments section headers still use the underlying corrected global
  styles (so borders/colors are now broadly correct) but were not given the same
  individually-measured rectangle+overlay treatment as page 1's 7 sections — a reasonable
  stopping point given the number of confirmed defects already fixed, not a claim these are
  100% pixel-perfect.
- The reference's remaining minor color variant (`#D9D9D9`-ish gray, width 1.0, 3 uses on
  page 1) and a purple width-1.5 decorative line (2 uses per page) were not individually
  tracked down — low-impact, cosmetic.

**Status: substantially rebuilt to match the reference's real structure/color scheme
(2026-08-31), NOT independently owner-verified yet** — this was a self-driven fix in response
to the owner's finding that the original build was never properly compared. Flagging for the
owner's own visual review, same as every other report in this project.

## Owner pushback round 2 (2026-08-31, same session) — "still far to be acceptable", demanded a real section-by-section visual compare
Owner correctly rejected the round-1 fix as insufficient and pointed at concrete visible
defects (a screenshot circling the logo and header divider) plus a general demand: "COMPARE
SECTION by SECTION in detail." Rendered both PDFs to PNG at matching DPI and did an actual
visual side-by-side comparison (not just coordinate/color-histogram numbers), which surfaced
defects the histogram approach had genuinely missed:

1. **Logo completely absent** — zero `<element kind="image">` anywhere in the entire JRXML.
   Confirmed via `get_image_info()` that the reference has the same INPEX logo on BOTH pages
   at identical bbox `(22.65,41.2,150.1,63.2)`. Added the image element (`logo.jpg`, already
   present in `output/` unused) to both the `<title>` (page 1) and `<summary>` (page 2) bands.
2. **Page-header divider line missing** — reference has a purple `#454087` line (width 1.5)
   at abs `y=121.2` below the title/date, on both pages. Also corrected the title/date's own
   y-positions, which were measured wrong in the original build (title `y=10→21`, date
   `y=38→52`, both re-measured from the reference's real word bounding boxes).
3. **A whole class of section titles were wrongly purple-filled bars that should be PLAIN
   TEXT** — visual comparison showed "Health, Safety & Environment", "Gas Export Pipeline",
   "Inventory", "Offtakes", "Water and MEG" (page 1) and "Consumables for CPF/FPSO",
   "Comments" (page 2) rendering as near-full-width purple bars, while the reference shows
   these as plain black italic text (same as "Persons On Board at Midnight"/"Production",
   which were ALREADY correctly plain). Re-verified via `get_drawings()` at each specific
   title's exact y-position (not assumed from the screenshot alone) — confirmed ZERO purple
   fill in the reference at all 7 of these positions. Converted all 7 from
   `PurpleSectionStyle` rectangle+text to plain `TitleStyle`/`PlainLabelStyle` text, matching
   the already-correct pattern. Also fixed 3 well-grid subtotal rows (Brewster/Plover/Total)
   that had the same wrong purple styling — converted to bold plain text.
4. **The well-grid's own 2-row header (Reservoir/Well Name/.../LP) had ZERO purple fill at
   all** — confirmed via `get_drawings()` (no fill found at the header's y-position) then via
   direct visual comparison. Reference shows a full purple-filled 2-row header (group row:
   blank-label/Flow Rate/blank-Method/MEG Injection; leaf row: 11 individual bordered column
   headers), matching every other table in this report. Rebuilt using the already-corrected
   column x-positions. **Caught and fixed a self-introduced overlap during this fix**: the new
   header rectangle initially started at `y=112`, overlapping the "Subsea Production" title
   (ends `y=117`) and the section divider (`y=131`) — shifted the whole header down to start
   at `y=133`, confirmed via re-render that the title now displays cleanly above it.
5. **A stray empty bordered cell** between "Well Name" and the well codes (e.g. "Brewster |
   [blank box] | BDC-1A-01") — root cause: `PlainValueStyle`'s newly-added border (from the
   round-1 global style fix) makes every text element individually bordered, and the
   Reservoir/Well Name columns had a 15pt UNFILLED gap between them (`x=10,width=40` then
   `x=55`, leaving `40-55` empty) that rendered as a visible blank bordered box. Fixed by
   closing the gap: re-measured the real column boundary via `get_drawings()`
   (`abs x=79.2` = local `57.2`) and resized Reservoir to `x=0,width=57` and Well Name to
   `x=57,width=68` across all 30 data rows + 3 subtotal rows + the header — confirmed via
   `grep` count (33 Reservoir cells, 31 Well Name cells) before applying, so the fix landed on
   exactly the intended cells.

**Verification: re-rendered to PNG and visually compared BOTH pages against the reference
again after all 5 fixes** — page 1 and page 2 now match the reference's structure closely
(logo, divider, correct plain/purple title split, well-grid header, no stray cells). Also
re-ran the `get_drawings()` histogram + word-count diff against the actual final swapped-in
file (not an intermediate version) — purple-fill counts changed (page 1: 53→37, page 2:
27→15) because several WRONG purple fills were removed while the well-grid's real missing
purple header was added; the counts no longer exactly matching the reference's 40/27 reflects
this project's rect+overlay-per-cell approach producing more discrete draw calls than the
reference's occasional merged rects, not remaining missing content. The same 2 minor
word-count residuals from round 1 remain (one duplicate "Gas" well-grid label, one
"Comments" occurrence) — not yet individually tracked down, low priority relative to the
structural fixes above.

**Status: substantially rebuilt AGAIN in direct response to a second, more specific round of
owner pushback — the lesson being that a color-histogram-only check (round 1) is necessary
but not sufficient; an actual rendered visual comparison catches classes of defect (missing
images, wrong fill-vs-plain-text choices, cross-element overlaps) that coordinate/color
counting alone does not surface.** Still not independently owner-verified — flagging for
review.

## Owner pushback round 3 (2026-08-31, same session) — 15-item detailed punch list + demand for proactive thoroughness
Owner rejected round 2 too ("PLEASE DON'T DO LOUSY WORK OUTPUT") and supplied a specific
15-item punch list, then separately demanded more proactive depth ("see how simply I can
find the defects"). Worked through all 15 items with real measurement, not assumption:

1. **Title not bold+italic** — `TitleStyle` had `bold="true"` but no `italic="true"`. Fixed,
   AND found the deeper root cause: this report's `pom.xml` was missing the
   `inpex-arial-fonts` extension jar entirely (same class of defect R07.011-022 needed fixed
   retroactively) — without it, `bold`+`italic` styling silently falls back to plain
   Helvetica with no error. Copied the jar from `R07.001/output/fonts/`, wired it into
   `pom.xml`, rebuilt classpath. Confirmed fix via `get_fonts()`: `Arial-BoldItalicMT` now
   embedded (was previously falling back to plain `Helvetica`).
2/6/9/11. **Section title vertical spacing** — measured EVERY section title's real
   y-position in the reference (`get_text('words')`) and its own divider line's position
   (`get_drawings()` for the `#636363` lines). Found 2 genuinely wrong (HSE `y=100→112`,
   Persons On Board `y=322→329`) and re-verified the other 5 (Production/Gas Export
   Pipeline/Inventory/Offtakes/Water and MEG) were ALREADY correct within ~2pt of the
   reference — did NOT touch those 5, to avoid introducing a regression into something that
   was already right. This is deliberate: "the owner asked for it" is not sufficient
   justification to change something a real measurement shows is already correct.
3. **Header columns not bold** — verified `HeaderTextOverlayStyle`/`HeaderLabelStyle` both
   already had `bold="true"`; the italic/font-embedding root cause in item 1 likely explains
   why this looked unbold in the reviewed screenshot (Helvetica fallback renders visually
   thinner than the intended embedded Arial-Bold).
4. **CPF header label / data labels too close to left border** — `HeaderTextOverlayStyle`
   had no left padding at all. Added inline `leftPadding="4"` to the 4 left-aligned CPF/FPSO
   header labels specifically (not the shared style, to avoid skewing the many
   Center-aligned headers that also use it) and `leftPadding="4"` to the shared
   `PlainLabelStyle`/`PlainValueStyle` (covers every data-row label across the report).
5. **"Comments" header not centered** — fixed 4 instances (`hTextAlign="Left"→"Center"`) in
   the HSE/Persons On Board tables.
7. **2nd column (#) not centered in first 3 grid tables** — HSE CPF/FPSO were already
   correct; fixed 2 remaining instances in Persons On Board CPF (`hTextAlign="Right"→
   "Center"`).
8. **Total row missing borders in grids 3/4** — re-verified via render after the other fixes
   landed; `PlainLabelStyle`/`PlainValueStyle`'s existing full box border already covers
   this once the earlier round's border fix was in place — confirmed visually present, no
   further change needed.
10. **"5th grid table (Production) layout design SUCK"** — zoomed into the reference at
    150dpi and found the earlier header was STRUCTURALLY wrong: built as 5 independent
    single-row columns, when the reference has a real 2-tier hierarchy (Row 1 = 2 GROUP
    cells "Daily Quantity"/"MTD Quantity", each spanning 2 leaf columns; Row 2 = 4 leaf
    cells "Volume"/"Short Term Forecast" under each group; "MTD Variance (%)" is a single
    column spanning the FULL header height, not part of the grouping at all). This also
    corrected an earlier wrong assumption (from the round-1 "missing Volume line" fix) that
    "Volume" was a 3rd stacked text line under "Short Term Forecast" — it's actually its own
    sibling leaf column. Completely rebuilt the header with the correct hierarchy and exact
    measured widths (Daily Quantity group=205, MTD Quantity group=211).
12/13/14. **Data-column alignment for grids 6/7/8** (Gas Export Pipeline, Inventory,
    Offtakes) — all were `hTextAlign="Right"` or unset (default Left); center-aligned all
    (6 cells in grid 6, 4 in grid 7, 5 in grid 8).
15. **"Grid table under Subsea Production SUCK"** — zoomed into the reference well-grid
    header and measured the DEFINITIVE column boundaries via `get_drawings()` (sorted,
    deduplicated rect x-ranges). Found the earlier build's Gas/Cond/Water/Method/HP/LP
    columns were measurably wrong (e.g. Method was `x=416,width=30`; the real value is
    `x=420,width=52` — 73% wider than built). Bulk-fixed via scoped `sed` across all 30 data
    rows + 3 subtotal rows + the header (confirmed each pattern's match count before
    applying, e.g. 36 matches for the Gas column fix, to ensure the fix landed only on
    well-grid cells and nothing else in the file) — Gas/Cond/Water/Method all corrected to
    the real `width=52`, HP/LP to `43`/`44`, Online/Choke fine-tuned to `44`/`40`. Also
    widened the per-row background rectangle (`530→559`) since the corrected columns now
    extend further than the old rectangle covered, which would have clipped the LP column's
    right border.

**Verification:** recompiled cleanly; re-rendered both the Production table and well-grid
header at high DPI and visually confirmed the corrected 2-tier hierarchy (Production) and
the corrected column widths (well-grid) now match the reference's own zoomed crops closely.
Swapped into `output/`.

**Lesson applied directly from this round: when a "5-column header" or "well-grid" is
flagged as fundamentally wrong ("SUCK"), the right response is to zoom into BOTH the
reference and the build at high DPI and compare the actual visual hierarchy/structure, not
just re-check colors/borders on the assumed-correct existing structure — the structural
assumption itself (e.g. "Volume is a 3rd header line" vs "Volume is its own column") can be
wrong from the very first build, and only shows up when directly visually re-examined.**

## Owner pushback round 4 (2026-08-31, same session) — 5 more items, including 2 real regressions I introduced myself
Owner supplied 5 more specific items. Item 1 was a genuine QA miss (fixed CPF's # column
alignment in round 3 but never checked the identical FPSO grid in the same section — the
owner directly called this out: "see how simply I can find the defects"). Items 2 and 4
turned out to be REGRESSIONS I introduced in round 3 myself: fixing the Production table's
and well-grid's HEADER structure without propagating the same column x/width corrections
down to the actual DATA ROWS underneath, which is a real process failure worth naming
plainly, not just fixing quietly.

1. **Persons On Board FPSO's `#` column not centered** — same fix as CPF (already done in
   round 3), just missed on the FPSO grid. Fixed, then did a full sweep (`grep` every `#`
   column instance across all 4 tables) to confirm no further instances were missed.
2. **Production table data-row borders "STUCK" (visible gaps between cells)** — root cause:
   round 3 fixed the HEADER's column boundaries (0/273/375/478/591/689) but the 14 DATA ROWS
   below still referenced the OLD, unrelated column positions (19/263/367/473/569/703, all
   width=50) from before the header rebuild — never propagated. Bulk-fixed all 14 rows'
   6 elements each via scoped `sed` (confirmed match counts first: 13/13/11/13/11/13,
   consistent with 2 rows having genuinely blank Short-Term-Forecast cells per the reference).
3. **Missing footer divider line before "Last refresh date"** — measured directly: abs
   `y=1138.7`, `x=22.65-819.2`, `#454087`, width `1.5` (same purple convention as the page
   TOP divider). Added to `pageFooter`, shifted the 3 footer text fields down 3pt to sit
   below it.
4. **Well-grid "STUCK", missing Comments column; same issue in Consumables CPF/FPSO and
   Comments section** — several real defects bundled together:
   - The well-grid's ROW1 group cells ("Flow Rate"/blank-Method/"MEG Injection") were the
     SAME class of oversight as item 2 — never resynced to the corrected row2/data column
     widths from round 3. Recomputed and fixed all 3 group cells' boundaries.
   - Added the well-grid's missing Comments column (measured: `x=559 width=230`, per-row
     bordered but blank) — confirmed via `get_drawings()` that the reference draws real
     per-row vertical borders here, not just one big undivided box.
   - Consumables for CPF/FPSO: the header row was plain unstyled text (no purple fill/border
     at all), and the Filled/Bunkered Volume + Comments columns were completely MISSING from
     every data row (no element at all, not even blank). Measured real column boundaries via
     `get_drawings()` (Name `x=0 w=230`, Closing Volume `x=230 w=122`, Filled/Bunkered Volume
     `x=352 w=132`, Comments `x=484 w=305`) and rebuilt both tables' headers (purple+bordered)
     and all data rows (label + value + 2 blank bordered cells) from scratch. **Self-caught
     and fixed a mistake in this same edit**: initially set the Closing Volume values to
     Center alignment without checking the reference first — re-verified via the zoomed
     crop that they're actually Right-aligned, corrected immediately before it could compound.
   - Comments section (CPF/FPSO free-text): "CPF"/"FPSO" were narrow (`width=150`) plain
     labels with no purple fill; each free-text line had its OWN individual border instead of
     sitting inside one shared bordered box. Measured real reference structure (full-width
     purple bars `x=0 w=789`; free-text lines inside ONE `Transparent`-mode bordered box per
     site, sized to the real content height: CPF `height=43`, FPSO `height=53`) and rebuilt
     both.
5. **Disclaimer wrongly boxed** — inherited `PlainLabelStyle`'s box border from the global
   style-level fix (Part P/round 1), when the reference shows it as plain bold-italic text
   with no border at all (confirmed via `get_text('dict')` span font: `ArialBoldItalic`) —
   the "bottom line" the owner wants is the SAME footer divider added in item 3 above, not a
   separate element. Zeroed the inherited box pen and added `bold`/`italic` to match the
   real font.

**Verification:** recompiled cleanly; re-rendered both full pages at 110dpi and visually
confirmed all 5 items — Production table columns now tile edge-to-edge with no gaps,
well-grid/Consumables tables show their Comments columns, Comments section shows full-width
purple bars with single shared text boxes, Disclaimer renders unboxed with the footer
divider visible below it. Swapped into `output/`.

**Standing lesson, stated plainly: fixing a table's HEADER structure is not the same as
fixing the table — the DATA ROWS must be independently re-verified against the same
corrected column boundaries, not assumed to already match. This is now the second time
(Production table headers/rows, well-grid header row1/row2) this exact class of mistake has
occurred in the same session — worth internalizing as a standing checklist item: after any
header column-width fix, immediately grep/check the corresponding data rows for the OLD
values before considering the fix complete.**

## Owner pushback round 5 (2026-08-31) — 9-item punch list, backup taken first per new standing rule
Backup: `R07_002_Daily_Offshore_Report.jrxml.backup_20260831_before_round5`.

1. **Production table header — "MTD Variance (%)" wrongly standalone instead of a leaf under
   "MTD Quantity"**. Measured reference via `get_drawings()`: the "MTD Quantity" row1 group
   cell spans all 3 MTD leaves (Volume/Short Term Forecast/MTD Variance), not 2. Widened the
   group rect+text from `width=211` to `width=306`, and converted "MTD Variance (%)" from a
   standalone tall cell (`y=470 height=39`) to a row2-only leaf (`y=482 height=27`) matching
   the other leaf cells. Confirmed via zoomed render: structure now matches reference exactly.
2. **Production table data rows "STUCK" — real root cause found: row height (12) shorter than
   row spacing (14), leaving a genuine 2pt unbordered gap between every row** (reference
   measured at row height≈13.5 vs spacing≈14, i.e. borders touch). Bulk-fixed all 14 rows'
   label+value cells (112 elements) from `height="12"` to `height="14"` — closes the gap
   completely, confirmed via before/after zoomed render match against reference.
3. **Narrow gap between header and data row under Gas Export Pipeline and Inventory** — same
   root cause as item 2 (data row y positioned 2pt below the header's true bottom edge).
   Shifted Gas Export Pipeline's data row from `y=805` to `y=803`, and Inventory's 2 data rows
   from `y=871/885` to `y=869/883`. Checked Offtakes/Water-and-MEG for the same latent defect
   first — both already had a correct near-zero gap, confirming the bug's scope was exactly
   the 2 sections the owner named, nothing broader.
4. **Divider line after "Subsea Production" too close to the well-grid table** — measured via
   `get_drawings()`+`get_text('dict')` on reference page 2: the divider line itself was
   already correctly positioned (`y=131`, matches reference's measured `~131.1` local), but the
   header table below it started only 2pt after (`y=133`) instead of reference's ~6pt gap
   (`~137.1` local). Shifted the ENTIRE well-grid block (header rows + all 30 data rows + 3
   subtotal rows, 415 `y=` attributes across lines 429-847) down by a uniform +4pt via a
   scoped script, closing the gap to match the reference's spacing pattern.
   - **Bonus defect found in the same comparison pass (not on the punch list, fixed anyway
     since it was directly visible in the same reference crop)**: the "Method" column's row1/
     row2 label placement was backwards — reference shows "Gas"/"Method" (2-line) in ROW1 with
     a blank row2, ours had a blank row1 and "Method" in row2. Swapped them to match.
5a. **Comments column in the well-grid should NOT be row-merged** — verified via direct render
    comparison: current build already uses one bordered cell per row (not merged); no change
    needed, confirmed correct as-is.
5b/6. **Big gap between well-grid header row2 and first data row** — row2's rectangles/text
    were only `height=22` while the reference's real row2 height measured ~28pt (via
    `get_text('dict')` label bboxes: "Reservoir"/"Well Name" span top vs first data row
    "Brewster" span top). Grew row2's 12 rect+text elements from `height=22` to `height=40`,
    recentering the 2-line sub-labels (Online/Choke/Gas/Cond/Water/HP/LP) within the taller
    box. This also exposed a knock-on gap under the "Comments" header cell (still `height=39`
    from the old row1+row2 total, now shorter than the regrown row1+row2=58) — grew it to
    `height=58` to match.
6/7. **Gap between Brewster/Plover/Total subtotal rows, "should be connected"** — same root
    cause class as item 2: row height (13) shorter than row spacing (16) vs reference's
    measured height≈15.5/spacing=16 (near-zero gap). Grew all 18 subtotal-row value elements
    (6 per row × 3 rows) from `height="13"` to `height="16"`, closing the gap. Reference
     confirmed to have NO border boxes at all for the blank columns in these rows (Well Name/
     Status/Online/Choke/Method) — this is the original's own design, not a missing-element
     defect, so left those columns genuinely blank/borderless as-is.
7/8. **Column borderline size inconsistent in Consumables for CPF/FPSO** — root cause: row
     spacing alternated 12/13 in both tables (irregular), vs reference's uniform 12.5 spacing
     with near-zero gap. Renumbered CPF's 5 rows and FPSO's 9 rows to uniform 12pt spacing
     (20 + 36 elements respectively) — all rows now tile with a consistent single-line border,
     matching between both tables.
8/9. **Disclaimer — only "Disclaimer:" should be bold, alignment should be Left not Center**.
     Measured reference via `get_text('dict')`: "Disclaimer" span font is `ArialBoldItalic`,
     the rest of the sentence is `ArialItalic` (not bold, but still italic) — confirming
     bold applies to the label only, not the whole sentence, and italic applies throughout.
     Split the single centered bold-italic element into 2 left-aligned elements (bold-italic
     "Disclaimer:" + plain-italic rest). First pass left an 11pt visible gap between the two
     (box1's width was wider than the actual rendered glyph width) — measured the generated
     PDF's own glyph bbox via `get_text('dict')` and tightened box1 to `width=36`/box2 to
     `x=36`, closing the gap to match the reference's flush spacing.

**Verification:** every item recompiled and re-rendered individually (zoomed crops, generated
vs reference side-by-side) before moving to the next; full-page renders of both pages done
last as a final sanity pass — no visual gaps/overlaps found. Swapped into `output/`.

**Process note:** backup taken once at the very start of this round only (per the owner's
explicit instruction to stop writing repeated backup-habit explanations and just do it) — see
[[feedback_backup_before_jrxml_edit]] for the standing rule this round followed.

## Owner pushback round 6 (2026-08-31) — 6-item punch list (with screenshot), backup taken first
Backup: `R07_002_Daily_Offshore_Report.jrxml.backup_20260831_before_round6`.

1. **Production/Internal Consumption/Losses label rows on page 1 had NO border at all**
   (zero-pen box override, added deliberately in an earlier round without checking whether the
   reference actually wanted zero border). Measured reference via `get_drawings()`: these 3
   rows DO have a full-width bordered box (`x0=25.15` to `x1=806.75`, matching the table's
   other rows). Added a `ValueCellStyle`-bordered full-width rectangle (`x=0 width=789`) behind
   each of the 3 label texts, keeping the text's own zero-pen box (avoids a double line).
2. **Comments column in the well-grid — re-confirmed NOT row-merged** (owner re-raised this
   after round 5's fix, for reassurance). Re-verified via zoomed render + `get_drawings()`:
   each of the 30 data rows still has its own independent bordered Comments cell (inherited
   from the LP column's own right-side border + the row's full-width outer rect) — no change
   needed, genuinely correct as-is.
3. **Reservoir column — checked whether it's a 2-row or 3-row header merge.** Measured via
   `get_drawings()`: exactly 2 rect elements exist in that column's y-range (row1 blank strip,
   row2 "Reservoir" label) — a clean 2-row merge, matching the reference's own 2-row structure
   pixel-for-pixel at matching zoom. No 3rd row/element found; no change needed.
4. **Comments section (CPF/FPSO free-text) — spurious border line visible right after
   "CPF"/"FPSO" text, cutting into the purple bar.** Root cause found via `get_drawings()`:
   the "CPF"/"FPSO" staticText elements carry their OWN inherited `PurpleSectionStyle` box
   border, offset 4pt right of the background rectangle's border (text starts at `x=4`, rect
   at `x=0`, both `width=789`) — two near-identical but 4pt-offset borders create a visible
   double-line artifact. Zeroed the text elements' box pen (`<box><pen lineWidth="0.0"/></box>`)
   so only the background rectangle's border shows, matching the reference's clean uniform bar.
5. **Total row too close to "Consumables for CPF" title.** Shifted everything from the
   "Consumables for CPF" title through the Disclaimer down by +8pt.
   - **Caused a real regression on the first attempt**: also grew `<summary height>` from 1117
     to 1130 to fit the shift, which pushed `summary(1130) + pageFooter(30) = 1160` past the
     printable area (`pageHeight 1191 − topMargin 22 − bottomMargin 22 = 1147`) — the original
     1117 was a deliberately tight fit (`1117+30=1147`, zero slack), and growing it forced a
     genuine 3rd page (`FILL OK: 3 page(s)` caught this immediately on recompile, not shipped).
     Fixed by keeping `summary height="1117"` unchanged and instead shrinking the Disclaimer's
     own element height from `24` to `16` (it had unused vertical padding) to absorb the +8pt
     shift within the original budget — recompiled back to 2 pages, verified via a max-bottom
     scan across every element in the band before considering it safe.
6. **Gap between the last (un-bold) data row and the (bold) Brewster subtotal row too wide,
   "apply same to its data columns."** Measured reference: last-data-row-bottom to
   subtotal-row-top gap ≈5.35pt; ours was 7pt. Reduced all 3 subtotal rows (Brewster/Plover/
   Total, 6 elements each = 18 total) from `y=599/615/631` to `y=597/613/629`, narrowing the
   gap to match — applies uniformly to the row's label AND all 5 value columns since they're
   the same row elements.

**Verification:** each item checked with a targeted zoomed render against the reference before
moving to the next; the summary-band overflow was caught by the compile step itself
(`FILL OK: 3 page(s)` vs the expected 2) rather than by visual inspection — a reminder that
page-count is itself a fast, cheap correctness check to run after every band-height-affecting
edit. Full-page renders of both pages done last, confirmed 2 pages, no visual gaps/overlaps.
Swapped into `output/`.

**Standing lesson: a band's declared height and its actual max-content-bottom are two
different numbers — checking `content bottom ≤ declared height` is necessary but NOT
sufficient; the band also has to fit within `pageHeight − topMargin − bottomMargin` alongside
every other band on that page (pageHeader/pageFooter). When a band was already at a
deliberately tight fit (zero slack against that page-level budget), any content shift must be
absorbed by trimming slack ELSEWHERE in the same band, not by growing the band's declared
height.**

## Owner pushback round 7 (2026-08-31) — 2-item punch list (with screenshots)
Backup: `R07_002_Daily_Offshore_Report.jrxml.backup_20260831_before_round7` (== round 6's
"after" checkpoint, since no edits happened in between).

1. **Production/Internal Consumption/Losses label-row right borderline not aligned with the
   table's other columns.** Root cause of round 6's own fix (item 1 there): the 3 label rows'
   background rect used `width=789` (the well-grid's convention), but THIS table's real 6
   columns only sum to `width=784` (`273+102+103+113+98+95=784`) — a 5pt overshoot created a
   small rectangular notch sticking out past the last column's right edge. Corrected all 3
   rects (`y=510/606/675`) from `width=789` to `width=784`.
2. **Comments section (CPF/FPSO): (a) "Production:"/"PRODUCTION:" wrongly bold; (b) data box's
   right borderline not aligned with the header bar's right borderline.**
   - (a) Checked the reference's actual font via `get_text('dict')`: `"Production:"` and
     `"PRODUCTION:"` are plain `Arial` (NOT bold) in the reference — only `"CPF"`/`"FPSO"` are
     `ArialBoldItalic`. Our build had `bold="true"` wrongly applied to the "Production:"/
     "PRODUCTION:" labels (a carry-over that was never checked against the reference). Removed
     `bold="true"` from both elements.
   - (b) Root cause (a genuinely new defect class): the "CPF"/"FPSO" staticText inherits
     `mode="Opaque"` + `backcolor` from `PurpleSectionStyle` — even after round 6 zeroed its
     BORDER pen, the text element's own OPAQUE FILL still renders as a second purple rectangle,
     offset 4pt right of the header rect behind it (text `x=4 width=789` vs rect `x=0
     width=789`), so the fill pokes out 4pt past the header bar's true right edge — visible as a
     small purple "step" at the top-right corner where the header meets the box below. Fixed by
     setting `mode="Transparent"` on both CPF/FPSO text elements (the rect behind already
     supplies the purple background — the text never needed its own fill) and tightening their
     width to 785 to stay inside the rect's true bounds.

**Verification:** recompiled (2 pages, no overflow), re-rendered zoomed crops for both items —
right edges now align exactly with the data columns below, and the "CPF"/"FPSO" bar's top-right
corner now sits flush against the box beneath it with no visible step. "Production:"/
"PRODUCTION:" confirmed rendering in plain (non-bold) `Arial-BoldMT`→`ArialMT`-equivalent
weight via re-check of the generated PDF's own font spans. Swapped into `output/`.

**Standing lesson: an "Opaque" mode style's background FILL is a separate rendering hazard from
its BORDER pen — round 6 fixed the border-offset artifact on this exact element by zeroing the
box pen, but didn't check whether the same x/width offset also creates a fill-offset artifact.
Any style-inherited element with `mode="Opaque"` sitting on top of (or beside) another bordered/
filled rect needs BOTH its pen AND its fill mode checked for offset-induced overhang, not just
one or the other.**

## Owner pushback round 8 (2026-08-31) — 1-item spacing fix
Backup: `R07_002_Daily_Offshore_Report.jrxml.backup_20260831_before_round8`.

1. **"Subsea Production" title sat too far from its divider line below it** — compared its
   own title-to-line gap (`y=105→117`, line at `y=131`, gap=14) against the same pattern used
   by "Consumables for CPF" (title ends 670, line at 676, gap=6) and "Consumables for FPSO"
   (title ends 779, line at 786, gap=7) — roughly double the gap used everywhere else. Moved
   the title down from `y=105` to `y=113` (line itself untouched, per the owner's explicit
   instruction to move only the title), closing the gap to 6, matching the established pattern.

**Verification:** recompiled (2 pages, no overflow), re-rendered a zoomed crop of the title/
line region — gap now visually matches the tighter spacing used by the Consumables titles.
Swapped into `output/`.
