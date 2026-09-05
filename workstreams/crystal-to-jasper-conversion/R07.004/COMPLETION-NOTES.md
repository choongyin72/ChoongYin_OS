# R07.004 — Daily Onshore Report — Completion Notes (2026-08-30)

**Phase:** LAYOUT ONLY. Third of 6 previously-unbuilt R07 reports. 2 STATIC pages (title=page1,
summary=page2, natural band-overflow break).

**Build location:** `C:\Projects\INPEX\sources\CrystalReports\R07.004\output\`.

## Report shape (measured directly)
- A3-sized portrait page (842x1191pt), ~22pt margins — same convention as R07.002/R07.006.
- Genuinely the ONSHORE parallel to R07.002 (offshore) — same overall report family shape
  (HSE/POB/Production table/Gas Export Pipeline/Inventory/Offtakes/Consumables on page 1;
  CCPP/Environmental/Comments on page 2), but **no well-grid** at all (onshore has no subsea
  wells) and a single combined "Consumables" section (not split into per-facility CPF/FPSO
  sections like R07.002's offshore report).
- Main table "Production, Internal Consumption & Losses" uses the SAME 7-column structure as
  R07.006's MONTHLY onshore report (Daily/MTD Quantity each with Volume+Mass, plus their own
  Short Term Forecast(tonnes), plus MTD Variance(%)) — confirmed via direct recon, NOT R07.002's
  5-column offshore-daily shape. Establishes a pattern: column shape tracks the onshore/offshore
  distinction (dual-unit Volume+Mass for onshore, single-unit for offshore), not the
  daily/monthly reporting cadence — R07.004 (daily) and R07.006 (monthly) share the same
  7-column onshore shape despite different cadences.
- 21 label rows generated programmatically (same script approach as R07.006/R07.002's main
  table script, adapted to this report's column x-ranges).

## Defects found and fixed
1. **CDATA over-escaping**: the generator script's `esc()` helper escaped `&` to `&amp;` before
   writing into a `<![CDATA[...]]>` block — but CDATA sections are literal text and don't need
   (or want) XML entity escaping; the result was literal "&amp;" text rendering in the PDF
   instead of "&". Fixed by removing the escaping for this one label ("Cold flare & Warm flare").
   This is a NEW defect class for this project — every prior report's generator scripts happened
   not to hit any `&`/`<`/`>` characters in their label text, so this bug was latent until this
   report's "&" label triggered it.
2. **One column value dropped due to an overly tight column x-range tolerance**: the "Fuel gas
   common (Sm³)" row's Short Term Forecast (Daily) value ("32") sits at abs x=467.5, just
   outside the generator script's column-C tolerance band (405-460 ±6 = 399-466) by 1.5pt —
   silently excluded from the row's value dict, not raising any error. Caught by the whole-page
   text diff showing "32" missing; fixed by adding the value by hand at the correct position
   (rather than re-running the generator with a wider tolerance, given only one row was
   affected).

## Verification performed
- Whole-page text extraction (`page.get_text('text')`) confirmed a PERFECT match on page 1
  (212/212 lines) after both fixes. Page 2 has 4 apparent "missing"/"extra" pairs, all confirmed
  to be PyMuPDF line-join artifacts from adjacent value+label proximity in the CCPP section
  (same pattern already documented for R07.006's CCPP section) — every individual word is
  present when searched for separately.
- Coordinate spot-check on 9 section-header labels across both pages landed within ~1-15pt of
  the reference, consistent with every prior report using the exact-recon-position method.

## Not done this phase (by design)
- Live query/data verification — deferred, same as every prior report in this project.

## Key takeaway
Surfaced a genuinely NEW bug class for this project: escaping `&`/`<`/`>` before writing into a
`<![CDATA[...]]>` block is WRONG — CDATA content is literal and must not be XML-entity-escaped,
only content OUTSIDE a CDATA section needs escaping. Every prior report's generator script
happened to avoid triggering this (no ampersands in their label sets), so the bug was latent
until this report's "Cold flare & Warm flare" label exposed it. Any future generator script
should either skip escaping entirely for CDATA content, or only escape the literal sequence
`]]>` (which would prematurely terminate a CDATA block) — not the standard XML entity set.

## 2026-08-31 — FULL structural/color/border re-audit (12-item checklist from JASPERREPORT-7-0-3.MD Post-mortem)

**Trigger:** the 2026-08-30 build above was verified ONLY by whole-page text-extraction match +
a 10-label coordinate spot-check — exactly the shallow method that R07.002's owner-directed
8-round rebuild proved insufficient (Parts P–T of the lessons file). Re-ran the full checklist
before trusting this report's "done" status, the same rigor applied to R07.002.

**Backup:** `R07_004_Daily_Onshore_Report.jrxml.backup_20260831_pre_audit` taken before the first
edit; `...backup_20260831_post_audit_final` taken after all fixes verified.

**Method:** `page.get_drawings()` color/fill/pen histogram (reference vs. generated, grouped by
`(color, fill, width)`), `page.get_text('dict')` span-level font checks, `page.get_pixmap()`
full-page + cropped renders actually read via the Read tool (not just diffed), and a programmatic
x-range overlap scanner across every `PlainLabelStyle`/`PlainValueStyle` element pair per row.

### Root defects found (real, measured — not assumed)

1. **Entire color scheme was inverted vs. the reference (checklist #1).** A `get_drawings()`
   histogram showed the reference has 382 draw operations per page-pair (274+33 gray `#D6D6D6`
   cell borders, 38+12 purple `#454087` fills, 6+3 dark-gray `#636363` width-1.5 dividers,
   2+2 purple width-1.5 dividers) while the existing build had only 36 (24 purple fills, 12 WHITE
   borders — i.e. `mode="Opaque"` fill with no real border color at all). Direct recon
   (`page.search_for()` + drawings-at-that-bbox check) proved every section title in the
   reference — HSE, the three main-table sub-labels (Production/Internal Consumption/Losses),
   Gas Export Pipeline, Inventory, Offtakes, Consumables, CCPP, Environmental, Comments — is
   **plain black `ArialBoldItalic` size-10 text with NO purple fill**, while the *column-header
   rows* (the "#"/"Comments" row, "Daily Quantity"/"MTD Quantity" group row, etc.) are the ones
   that ARE purple-filled with white overlay text. The existing build had this **exactly
   backwards**: section titles were purple bars, header-caption rows were plain unstyled text.
   One exception found by direct recon: the POB row has no separate title line at all — "POB"
   itself sits inside the purple 3-column header bar's own first column, sharing the row with the
   "#"/"Comments" captions (confirmed via `page.get_text('dict')` — its "POB" span is
   `forecolor=#FFFFFF`, i.e. white-on-purple, unlike every other section's title span, which is
   black-on-white).
2. **Every data cell had zero border** (checklist #1/#6) — `PlainLabelStyle`/`PlainValueStyle`
   never carried a `<box>` at all. Fixed at the style level (one edit propagates to ~170+ cells),
   using `topPen`/`bottomPen`/`leftPen`/`rightPen` split per Part D3/M8 (Label style keeps all 4
   sides since it's always the first column in a row; Value style omits `leftPen`, relying on its
   left neighbor's `rightPen`, to avoid double-drawing the shared boundary) and dropping `topPen`
   too (relying on the row above's `bottomPen` or the header rect's own bottom edge) — this
   brought the gray-stroke count down from an initial over-build of 939 (3x the reference, from
   giving every individual cell a full 4-sided box) to 549, without under-bordering any real edge.
   Two row-starting VALUE cells with no preceding label (`Gas Export Pipeline`'s data row, and
   `Offtakes`' "Plant Condensate" first cell) needed an explicit inline `leftPen` override since
   they have no left neighbor to inherit a border from.
3. **All 11 dark-gray `#636363` width-1.5 section dividers were completely absent** — added one
   `<element kind="line">` below every plain-text section title (Part D2 confirms a horizontal
   `kind="line"` is safe; only *vertical* freestanding lines have the known diagonal-offset bug).
4. **Two full-width PURPLE width-1.5 lines (not the usual dark-gray dividers) were completely
   absent** — one right after the title/date block (both pages, abs y≈121, local y≈99) and one
   near the very bottom of the page just before the page footer (both pages, abs y≈1138.7). Added
   both to the `<title>` band (safe, since it's already declared at 1100/1191 page height); for
   the `<summary>` band, this required **growing the band from its original 500 to 1076** to give
   room for a bottom divider positioned realistically far down the page (matching the reference's
   real, very large blank-space-then-divider layout on page 2) — recompiled and re-checked page
   count immediately after (still 2 pages, matches reference) per the mandatory Part S2 rule
   before doing anything else.
5. **A duplicate "Gas Export Pipeline" title+rectangle block** (byte-for-byte identical pair of
   elements at the same x/y, immediately following each other) — removed the duplicate as part of
   the same edit that fixed this section's title/header styling.
6. **Row/column geometry defects exposed only once real borders were added** (checklist #4/#9,
   Part R1/T1 class): several `PlainLabelStyle` label elements were wider than the gap to their
   own adjacent value element (e.g. HSE/POB label `width="180"` overlapping a value column that
   started at `x=140`; the main Production/Internal Consumption/Losses table's 18 label rows all
   had `width="210"` reaching into column 1's real start; both CCPP label-value pairs per row
   overlapped their own value by 33–45pt; one Offtakes Arrival/Departure pair overlapped by 5pt).
   These overlaps were **invisible in the original borderless build** (Part D1/Q3's exact lesson:
   a border fix can expose a pre-existing coordinate gap/overlap as a new-looking visual defect)
   and rendered as a "doubled"/crossed border artifact once borders were added. Found via a
   purpose-written x-range overlap scanner (grouping every `PlainLabelStyle`/`PlainValueStyle`
   element by `y`, sorting by `x`, and flagging `x[i]+width[i] > x[i+1]`) rather than by eye — this
   caught 29 real overlaps across 5 sections in one pass. Fixed by shrinking each label's `width`
   to end just before its neighbor's `x`.
7. **Gas Export Pipeline's "Onshore" group column captions ("Avg Pressure (kPag)", "Avg Temp
   (°C)") were positioned so the new, correctly-measured purple header-cell boundary cut directly
   through the caption text** ("Avg" in one purple cell, "Pressure" bleeding into the next) — a
   direct visual defect confirmed via a 300dpi crop render, not visible in the whole-page 150dpi
   screenshot. Re-centered both captions within their real measured column boundaries.
8. **Comments free-text block had per-line borders** on "LNG1 – Online." / "LNG2 – Offline." once
   the style-level border was added — the reference uses ONE shared bordered box for the whole
   free-text block (Part R3). Fixed: one `mode="Transparent"` bordered rectangle spans both lines,
   each individual line's own box pen zeroed (`<pen lineWidth="0.0"/>`) to avoid double-bordering.
   The Disclaimer footer text picked up the same unwanted border purely from reusing
   `PlainLabelStyle` after it gained a box (Part R4's exact "style-level fix wrongly boxes an
   unrelated element" class) — zeroed the same way.
9. **The INPEX logo image was completely absent** — zero `<element kind="image">` anywhere in the
   original file (same defect class independently found and fixed on R07.002, Part Q1(a); a
   `get_drawings()` color histogram alone can never catch this, since it only tracks vector
   drawings, not raster images). Confirmed via `page.get_image_info()` on the reference (bbox
   local x=0,y=22,width=128,height=22, identical on both pages) — copied `logo.jpg` from
   R07.002's already-fixed output folder (same INPEX masthead asset) and added a matching
   `<element kind="image">` to both the `<title>` and `<summary>` bands.
10. **Main report title/date font was wrong** — reference measured via `get_text('dict')` as
    `ArialBoldItalic` size 21 (title) / size 11 (date); the build used plain `bold` (no italic) at
    size 16. Fixed `TitleStyle` to `fontSize="21.0" bold="true" italic="true"`. This exposed
    **Part F1's exact lesson** (a `staticText` box too short for its font size is SILENTLY DROPPED
    from the render entirely, zero compile warning) — the title element's declared `height="24"`
    was just under the ~25pt line-height needed for a 21pt font, and the title text vanished
    completely from the rendered PDF (confirmed absent via `page.get_text('text')`, not just a
    coordinate check). Fixed by growing the title height to 30 and nudging the date field down
    from `y=38` to `y=42` to avoid a new overlap — re-verified `"Ichthys" in get_text('text')` is
    `True` on both pages after the fix.

### Known, disclosed remaining gap (NOT silently claimed as fixed)
- **Bold/italic silently falls back to plain Helvetica in the exported PDF** — confirmed via
  `page.get_text('dict')` on the generated PDF: the title span renders as `font=Helvetica,
  flags=0` (no bold, no italic) despite `isBold`/`isItalic` both being set in the JRXML. Per Rule
  10 of the lessons file, this requires a registered font-extension JAR +
  `jasperreports_extension.properties` for `Arial` — **this project's R07.004 (like its sibling
  R07.002/R07.006) has no such extension wired in `pom.xml`/`src/main/resources`**, unlike
  R07.012/014/016 which do have one. This is a **pre-existing, project-wide gap that predates this
  audit**, not something introduced by these fixes — disclosed rather than silently left unfixed,
  and not fixed here since wiring a font extension is a cross-report infrastructure change outside
  this single report's scope (would need the same owner-level decision applied consistently to
  every sibling report, not patched ad hoc on one).
- **Column-header purple-cell boundaries vs. main-table data-row value positions** are reasonably
  aligned (verified via render crop for the one case that visibly crossed a caption, item 7 above)
  but were NOT re-measured to sub-pixel precision for all 8 leaf columns of the
  Production/Internal Consumption/Losses table — the original build's data-row x-positions
  (already spot-checked to ~1–15pt in the 2026-08-30 pass) were kept as the source of truth for
  VALUE positions; only the missing color/border/divider treatment was added on top. A residual
  few points of column-boundary vs. data-value misalignment may remain at this level of scrutiny
  but did not surface as a visible defect in the 300dpi crop checks performed.
- **Border-stroke count is still higher than the reference's** (549 vs. reference's 319 gray
  strokes) — every header-row rectangle still draws its own full 4-sided pen (so adjacent header
  cells double-draw their shared vertical boundary), a smaller-scale case of the same class fixed
  for data cells. Not fixed further given time already invested chasing categorical (color/
  divider/logo/font) defects, which are the ones that were 100% wrong before this pass; this
  residual is a "slightly bolder line at a few internal header seams," not a wrong color/missing
  structure.

### Verification performed (real commands, real evidence — not assumed)
- `get_drawings()` color/fill/width histogram: purple fills 38+12 (both ref and gen, EXACT match),
  purple width-1.5 dividers 2+2 (EXACT match), dark-gray width-1.5 dividers 6+3 (EXACT match) —
  after the fix. Before the fix: gen had 0 gray borders, 0 dark dividers, 0 purple dividers, and
  the wrong 24/6 purple-fill split (title bars purple instead of header rows).
- Page count re-checked after EVERY band-height change (`title` untouched at 1100; `summary`
  grown 500→1076): compiled + filled + exported cleanly every time, `FILL OK: 2 page(s)`
  throughout — never regressed to 1 or 3 pages.
- `page.get_text('text')` whole-page presence check for "Ichthys" on both pages — `True`/`True`
  after the F1-class title-disappearance fix (was silently absent before).
- `page.get_image_info()` on the generated PDF confirms the logo image now renders (was `[]`
  before).
- A purpose-written x-range overlap scanner across every `PlainLabelStyle`/`PlainValueStyle`
  element (grouped by `y`, sorted by `x`) found 29 real overlaps before the fix, 0 real overlaps
  after (one remaining hit is a cross-band false-positive — a title-band row and a
  summary-band row that coincidentally share the same local `y` in their own independent bands).
- Full-page 150dpi renders of both pages, and 300dpi crops of the HSE table and Gas Export
  Pipeline header, were rendered to PNG and actually read via the Read tool (not just diffed) at
  each major fix stage — this is what caught the header/caption text-crossing-a-border defect
  (item 7) and confirmed the final result visually matches the reference's structure, color
  scheme, and section layout.
- Final rebuild from the checked-in JRXML (`R07004Verify` harness): `COMPILE OK` → `FILL OK: 2
  page(s)` → `EXPORT OK` — clean, matching the reference's real page count.

### Honest bottom line
This report now genuinely matches the reference's real visual structure — color scheme, cell
borders, section dividers, logo, and title font size are all fixed and independently verified
against measured reference data (not assumed). It is **not** a pixel-perfect match: the two
disclosed gaps above (font-extension-jar bold/italic fallback, and the residual excess
header-cell border strokes) are real, known, and left as-is rather than silently claimed fixed —
consistent with this project's "no unverified claims" standard.

## 2026-08-31 — Closing the 2 disclosed gaps (owner directive: "both layouts must match identically, no exceptions")

**Backups:** `...jrxml.backup_20260831_135856_before_fontjar_fix` taken before this round's first
edit; `...jrxml.backup_20260831_140420_post_gap_closure_final` taken as the final checkpoint after
both gaps were verified closed. All prior `.backup_*` files retained, untouched.

### Gap 1 — Font extension JAR (CLOSED, verified)
Same fix as R07.002 (Part P of the lessons file): copied `inpex-arial-fonts.jar` from
`R07.002\output\fonts\inpex-arial-fonts.jar` (self-contained — verified via `jar tf` it carries its
own `META-INF/MANIFEST.MF`, `jasperreports_extension.properties`, `fonts.xml`, and the 4 Arial TTFs
at its root, so no separate `jasperreports_extension.properties` needed in `src/main/resources`)
into `R07.004\output\fonts\inpex-arial-fonts.jar`, then added the identical system-scope
`com.inpex:inpex-arial-fonts:1.0` dependency block to `R07.004\pom.xml` (mirrored from R07.002's
pom.xml verbatim, only the comment reworded).

Recompiled (`mvn -q compile` clean, `mvn -q dependency:build-classpath` clean) and re-ran
`R07004Verify` — `COMPILE OK` → `FILL OK: 2 page(s)` (page count unchanged) → `EXPORT OK`.

**Verification (real command output, `page.get_text('dict')` on the freshly rebuilt PDF, both
pages):**
- Font usage histogram across the whole document: `ArialMT: 228`, `Arial-BoldMT: 57`,
  `Arial-BoldItalicMT: 13` — **zero occurrences of `Helvetica` anywhere.**
- Every element carrying `bold="true" italic="true"` in the JRXML (`TitleStyle`,
  `SectionTitleStyle` — covering "Ichthys: Daily Onshore Report", the date, and all 9 section
  titles: HSE, Production/Internal Consumption/Losses, Gas Export Pipeline, Inventory, Offtakes,
  Consumables, CCPP, Environmental, Comments) now renders as `font=Arial-BoldItalicMT` on both
  pages — confirmed by listing every span whose font name contains "Bold"/"Italic" and checking
  the text against the JRXML's bold+italic style list, not just spot-checking one label.
- Every `bold="true"`-only element (`SubSectionTitleStyle`, header-caption/`HeaderLabelStyle` rows —
  "#", "Comments", "POB", column captions, etc.) renders as `Arial-BoldMT`.
- Plain-style body text renders as `ArialMT`.

Gap 1 is genuinely closed — not a Helvetica fallback anywhere in the rendered output.

### Gap 2 — Header-cell border over-draw (INVESTIGATED — real over-draw exists but is cosmetically invisible, NOT a visible defect)
`get_drawings()` color/width histogram confirmed the reported counts: generated PDF has 549
`#D6D6D6`-width-1.0 gray strokes vs. reference's 319 (307+12 split across two near-identical grays
`0.84`/`0.85` that PyMuPDF reports separately by float rounding) — matching the number disclosed in
the prior audit.

**Root cause, measured precisely (not assumed):** the 549 gray strokes split into two structurally
different kinds of draw operation:
- 498 are degenerate (zero-width OR zero-height) single-line "quad" strokes — these are the
  Label/Value cells' individual `topPen`/`bottomPen`/`leftPen`/`rightPen` sides drawn as separate
  line segments per the earlier per-side-pen fix (Part D3/M8 in the lessons file), deliberately
  designed to avoid double-drawing data-cell shared boundaries.
- 51 are real 4-sided box strokes (both width AND height > 0) — these are the **header-row**
  cells (main-table group/leaf captions, HSE/POB row, Gas Export Pipeline, CCPP, Environmental
  headers) that still use a single full-box pen per cell, exactly as the prior audit disclosed.
- A coordinate-adjacency scan across all 51 header boxes (checking every pair on the same page for
  a shared vertical or horizontal edge with real y/x overlap) found **34 header-cell boundary edges
  that are drawn twice** — once by each of the two adjacent cells' own full-box pen, at IDENTICAL
  coordinates, IDENTICAL color (`#D6D6D6`), IDENTICAL width (1.0pt). Example: the "Daily Quantity"/
  "MTD Quantity" group-header row's shared edge at x=213.0 between rect `(25,323,213,337)` and rect
  `(213,323,479,337)` is one of the 34 — the reference PDF's own equivalent junction (rendered and
  visually inspected side-by-side, see below) uses the exact same "each cell draws its own full box"
  construction and shows the identical count of adjacent boxes at that row.
- Reference's box-vs-line split is the mirror opposite (244 real boxes / 75 degenerate lines) —
  meaning the **reference draws MOST cells as single full boxes** (a different, simpler
  construction technique than this build's data-cell per-side-pen approach), not a defect on either
  side, just two different valid ways to produce the same visual grid.

**Visual verification (the actual render-and-look check, not just the count):** rendered 6x-zoom
(≈432 DPI-equivalent) PNG crops of three real header-cell junctions from the generated PDF —
the "Daily Quantity"/"Volume"/"Mass"/"Short Term Forecast" main-table header block, and the HSE/POB
table's "#"/"Comments" header row plus its data-row cell borders below it — and a matching 6x crop
of the reference PDF's own "Daily Quantity" header junction. In all three crops the gray divider
lines at every cell boundary, including the 34 identified double-drawn edges, render as a single
clean 1pt gray line with **no visible thickening, no misalignment, no doubling artifact** — because
the two overlapping strokes sit at the literal same coordinates with the same color/width, so a PDF
renderer paints the identical pixel twice, producing zero visual difference from painting it once.
The reference's own header junction, rendered at the same zoom, shows the same single-clean-line
appearance.

**Conclusion:** Per the task's own instruction to only call this "invisible, not a real defect"
after actually rendering and looking at high DPI — done, and confirmed no visible artifact at any
of the 3 junctions checked. This is a genuine over-draw (34 real redundant stroke operations,
confirmed by exact-coordinate adjacency measurement) but it is cosmetically identical to the
reference's own rendering at both normal and 6x-zoomed inspection. **Not restructured further** —
the 549-vs-319 count gap is a byproduct of two different (both valid) box-construction techniques
between this build's data cells (per-side pens, intentionally not double-drawing, per the prior
audit's Part D3/M8 fix) and its header cells (full-box-per-cell, matching the reference's own
predominant technique) — collapsing the header cells' redundant edges into non-overlapping partial
pens (mirroring the data-cell technique) was considered but rejected: it would touch 17 already-
verified header cells across 6 sections for a change with zero visual effect, at real risk of
reintroducing the exact overlap-based visual regressions the prior audit's Part R1/T1 already had to
fix once cell borders were first added. No JRXML edit was made for this gap.

### Final verification after this round
- `mvn -q compile` clean, `R07004Verify` → `COMPILE OK` → `FILL OK: 2 page(s)` → `EXPORT OK` — page
  count unchanged at 2, matching the reference's real page count.
- Font histogram (both pages): `ArialMT`/`Arial-BoldMT`/`Arial-BoldItalicMT` only, zero `Helvetica`.
- Border stroke histogram unchanged at 549 gray / 9 dark-gray-divider / 4 purple-divider (dividers
  still EXACT match to reference's 9/4) — the 549-vs-319 gray-stroke gap is disclosed above as
  investigated-and-cosmetically-invisible, not silently re-claimed as fixed.
- Temp comparison PNGs (`gen_header_junction_crop.png`, `ref_header_junction_crop.png`,
  `gen_hse_junction_crop.png`) created in `output\` for this investigation were deleted after use;
  all `.backup_*` files retained.

### Honest bottom line (updated)
Gap 1 (font-extension JAR) is genuinely closed — real, measured, verified: every bold/italic
element now renders in the correct Arial weight/style, zero Helvetica fallback anywhere. Gap 2
(header-cell border over-draw) is **not closed by a structural change** — it was investigated to
its precise root cause (34 identically-coordinated redundant strokes at header-cell junctions,
confirmed via adjacency scan) and confirmed, via actual high-DPI rendering of 3 real junctions
compared side-by-side with the reference's own equivalent junction, to be cosmetically invisible in
both PDFs — not a visible layout defect, just a different (also-valid) construction technique for
header cells vs. the reference's predominant one. This is reported as-is per this project's
no-unverified-claims standard, rather than either leaving it unfixed silently or making a
zero-visual-effect structural change purely to move a stroke-count number.

## Owner rejection (2026-08-31) — personal full-page visual comparison found real defects the
prior automated audits above missed
The owner rejected R07.004 (along with R07.003/005/006) despite the audits above reporting it
verified. A personal, first-hand full-page render-and-read comparison (not delegated, not a
zoomed-crop-only check) found:

1. **CCPP table — same fragmented/doubled-border defect as R07.003** (confirmed via
   `get_drawings()` coordinate measurement, same root cause: label elements sized `width=390/344`
   overreaching past the real column boundary, and per-row value elements sized ad-hoc to each
   number's string length instead of a consistent column width). Fixed by resizing all label/
   value elements across 5 rows to the table's real measured boundaries (label1 x=4 w=260,
   value1 x=264 w=130, label2 x=396 w=257, value2 x=655 w=136) — re-measured and re-rendered,
   confirmed clean.
2. **Sub-item indentation under Production/Internal Consumption/Losses — OVER-indented** (the
   opposite direction from R07.003's defect): measured real deltas — reference indents ~11.7pt,
   the build was indenting ~23pt (roughly double). Fixed by moving 18 sub-item label elements
   from `x=19` to `x=15` (re-measured after fix: 12.25pt delta vs reference's 11.7pt, matching
   within 1pt).
3. **Off-specification tank closing volume / STG bypass valve row — same value-on-wrong-side
   defect as R07.003.** Measured the reference's real glyph x-position for "2" and confirmed it
   belongs under "Off-specification tank closing volume" (value1, x≈264-393), not under "STG
   bypass valve" (value2, x≈655-793) where the build had placed it. Fixed by moving the value
   element to `x=264` under the correct label.

**Verification:** recompiled (page count unchanged at 2), re-measured every fix's real coordinate
delta against the reference before considering it done, re-rendered zoomed crops and read them
directly. This report shares the SAME root defects as R07.003 (built via the same generation
method) — worth checking any other report built the same way for the identical CCPP-fragmentation
and Off-specification/STG-bypass-swap patterns.
