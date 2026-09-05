# R07.003 — Onshore Daily Operations Report — Completion Notes (2026-08-30)

**Phase:** LAYOUT ONLY. Sixth and final of the 6 previously-unbuilt R07 reports
(full-rigor scope confirmed by owner). 5 PHYSICAL PAGES — the largest/most
structurally complex report in this batch, requiring a genuinely NEW multi-page
architecture (see below).

**Build location:** `C:\Projects\INPEX\sources\CrystalReports\R07.003\output\`.

## Report shape (measured directly)
- A3-sized portrait page (842x1191pt), ~22pt margins — same convention as every
  other R07 report.
- Page1 (`<title>`): same overall shape as R07.004's Daily Onshore Report (HSE/
  POB/Production table/Gas Export Pipeline/Inventory/Offtakes), PLUS a section
  R07.004 does NOT have — "Production Quality" (a 7-row x 11-column table:
  C1/C2/C3/iC4/nC4/iC5/nC5/C6+/CO2/N2/HHV(Btu/Scf) mol% breakdown for each
  Train's LNG/propane/butane rundown, plus CPF rich gas export to GEP). The main
  "Production, Internal Consumption & Losses" table uses the exact same 7-column
  shape as R07.004/R07.006 (Daily/MTD Quantity each Volume+Mass, plus their own
  Short Term Forecast(tonnes), plus MTD Variance(%)) — confirmed via direct
  recon, not assumed. The Gas Export Pipeline section uses H2S(ppmV) where
  R07.004 uses CO2(mol%) — a genuinely different column, caught by recon.
- Pages 2-5 hold content that shares R07.004's EXACT sample values for
  Consumables/CCPP/Environmental (confirmed via direct comparison) but this
  report additionally has "Major Equipment Status" and "Production Risks"
  tables (both showing placeholder `"No Records Found"` rows) before those, and
  — the genuinely new structural element — a "Comments" section spanning pages
  3-5 containing 6 free-text narrative entries (HSE/Executive/Production/
  Maintenance & Implementation/Coatings & Insulation/Engineering), each authored
  by "Isabella Boyd" and varying wildly in length (6 to 68 lines).

## Architecture decision: forced-page-break `<detail>` band, not a giant `<summary>`
This is the FIRST report in the R07/R10 batch requiring content to span MORE
THAN ONE extra physical page beyond `<title>`. The established 2-page pattern
(oversized `<summary>` relying on natural band-overflow, ~13pt over the ~1117pt
per-page budget) does NOT generalize to spanning many pages:

1. **First attempt** — one `<summary height="3660">` band holding page2's tables
   plus all 6 comment entries stacked via a computed cumulative offset. This
   FAILED TO COMPILE: `"The summary section and the margins do not fit the page
   height."` JasperReports validates `<title>`/`<summary>` band height against a
   SINGLE page's usable space; declaring a band many times taller than one page
   is rejected outright — it is not just a soft pagination quirk, unlike the
   small ~13pt overflow every 2-page R07 report already relies on.
2. **Fix** — replaced `<summary>` with a `<detail>` band, filled via
   `JREmptyDataSource(4)` (4 virtual records), each gated by
   `printWhenExpression` on the built-in `$V{REPORT_COUNT}` variable
   (1 = page2 tables, 2/3/4 = the 3 Comments page-groupings). Giving the detail
   band `splitType="Prevent"` and a declared height close to one full page
   (1100 vs ~1117 usable) means a record is placed atomically and the next
   record never has room left on the same page — no explicit group or
   `isStartNewPage` needed, confirmed via an isolated minimal repro
   (`mini2.jrxml`, 4 unconditional records → clean 5-page result).
3. **Second bug, same architecture** — with real (conditional) content the
   detail band collapsed to effectively ZERO height whenever every element in a
   record was hidden by `printWhenExpression`, losing the forced page break
   entirely (confirmed via `mini3.jrxml`: 4 conditional-only elements produced
   only 2 pages, not 5). **Fix:** add one UNCONDITIONAL (never
   printWhenExpression-gated) 1x1090 spacer rectangle per record, forcing the
   band to always reserve full-page space regardless of which content is
   visible.
4. **Third bug, same architecture** — even with the spacer, only record 1
   ("REPORT_COUNT==1") ever printed; records 2-4 never appeared. Root cause: the
   Python helper that injects `printWhenExpression` used a regex that correctly
   handled non-self-closing `<element ...>...</element>` tags but, for
   self-closing `<element .../>` tags (the plain `<rectangle>` section-header
   bars), inserted `<printWhenExpression>` immediately AFTER the closing `/>` —
   leaving it as a DANGLING sibling directly inside `<band>`, not a child of
   that element. The compact-format loader silently accepted this malformed
   placement and (empirically) treated it as the BAND's OWN
   printWhenExpression — the last one encountered wins, which is why only the
   `REPORT_COUNT==1` record's content ever rendered. **Fix:** the injection
   helper now converts a self-closing `<element attrs/>` to an explicit
   `<element attrs><printWhenExpression>...</printWhenExpression></element>`
   pair BEFORE inserting the condition, so it always lands as a real child.
5. **Result:** exactly 5 physical pages, matching the reference's own
   `Page N of 5` footer.

## Other defects found and fixed
6. **Column boundary off-by-a-fraction dropped 2 values** in the main table's
   "Fuel gas common" row: "9" (abs x=380.6, just outside column B's 320-380
   range by 0.6pt) and "32" (abs x=465.5, just outside column C's 405-465 range
   by 0.5pt) — same defect class as R07.004's dropped "32" value, but here
   caught proactively via a whole-page text diff on the FIRST build attempt
   rather than requiring a separate fix pass. Fixed by widening both ranges by
   1pt.
7. **Wrong title text copied from a sibling report without checking THIS
   report's own recon**: every element referencing the running title used
   `"Ichthys: Onshore Daily Operations Report"`, following the "Ichthys: "
   prefix convention every other R07 report uses — but R07.003's own reference
   PDF has NO "Ichthys:" prefix at all (confirmed via direct recon: `y=46.0:
   Onshore | Daily | Operations | Report`, no "Ichthys" text anywhere on any of
   its 5 pages). This is exactly the standing project rule in practice — a
   structurally-similar sibling's convention does not automatically transfer;
   this specific value must be verified against THIS report's own reference.
   Fixed by removing the prefix everywhere (title band + all 4 detail records).
8. **CDATA over-escaping reintroduced**: `gen_comments.py`'s `esc()` helper
   escaped `<`/`>` to `&lt;`/`&gt;` before writing into `<![CDATA[...]]>` blocks
   for the narrative comment text (which contains literal `<`/`>` characters in
   flaring-limit comparisons, e.g. "Warm – 4k Sm3 (<20k Sm3)"), producing
   literal "&lt;20k Sm3" instead of "<20k Sm3" in the rendered PDF — the exact
   same bug class documented as Part K3 in
   `DeepDiveLearnings/JASPERREPORT-7-0-3.MD` from R07.004's `&`-escaping
   mistake, but for `<`/`>` this time instead of `&`. Fixed by removing the
   escaping entirely (CDATA content is already literal; only the literal
   sequence `]]>` would need guarding, and this report's text doesn't contain
   it — checked directly).

## Verification performed
- Whole-page text extraction confirmed a PERFECT match (0 missing, 0 extra) on
  pages 1, 3, 4, and 5 after the fixes above.
- Page 2 has one residual apparent diff (4 value+label pairs in the CCPP
  section glued into one line by PyMuPDF's text-line grouping, e.g. "148 Avg.
  Main steam header pressure (kPa)") — confirmed via `search_for()` coordinate
  check that value and label are correctly separated and non-overlapping in
  both the reference and generated PDF (within ~1-6pt), the same known
  PyMuPDF line-join artifact class already documented for R07.004/R07.006's
  CCPP sections; every individual word is present when searched for
  separately.
- Page count confirmed exactly 5, matching the reference's own `Page N of 5`
  footer text on every page.
- 6 comment entries confirmed extracted correctly via the "Isabella Boyd"
  author-marker split (HSE=30 lines, Executive=6, Production=68, Maintenance &
  Implementation=44, Coatings & Insulation=34, Engineering=24 — cross-checked
  against a direct line-count of the reference's own raw text) and correctly
  grouped into the reference's own observed page3/4/5 groupings (HSE+Executive
  / Production alone / Maintenance & Implementation+Coatings & Insulation+
  Engineering) rather than a computed height-budget guess (an earlier
  computed-budget attempt, using an assumed 10.5pt/line height, mis-split
  Production away from the other 3 categories the reference visibly keeps
  together on page 5 — recalibrating to the reference's own measured
  ~9.7pt/line ratio and using its own observed groupings fixed this).

## Not done this phase (by design)
- Live query/data verification — deferred, same as every prior report in this
  project.

## Key takeaway
This report required a genuinely NEW multi-page architecture (forced-page-break
`<detail>` band via `printWhenExpression` on `$V{REPORT_COUNT}`, not the
established oversized-`<summary>`-with-natural-overflow trick, which does not
generalize beyond one extra page). Three distinct, non-obvious defects had to
be found and fixed to make this architecture work correctly: (1) an
unconditional spacer element is required per record or the band silently
collapses to zero height and the forced page break is lost; (2) a
`printWhenExpression`-injection helper must correctly convert self-closing
`<element/>` tags to an explicit open/close pair, or the condition ends up
dangling as a sibling inside `<band>` and gets silently misinterpreted as the
BAND's own printWhenExpression, corrupting every record after the first. Both
were only found by writing and testing minimal isolated repro files
(`mini.jrxml`/`mini2.jrxml`/`mini3.jrxml`) rather than debugging inside the
full ~400-element production JRXML directly — a useful debugging pattern for
any future report needing a similarly novel band-level mechanism.

---

## 2026-08-31 — Full rigor re-audit (owner-directed, per the R07.002 8-round post-mortem
checklist in `DeepDiveLearnings/JASPERREPORT-7-0-3.MD`)

The verification performed on 2026-08-30 (above) was a whole-page text-extraction match plus a
handful of coordinate spot-checks — exactly the class of "looks right" verification that let
R07.002 ship with 8 rounds' worth of real defects undetected. Re-running the full 12-item
checklist against R07.003's own reference PDF (via `page.get_drawings()` color histograms,
`page.get_text('dict')` span-font checks, and rendered-PNG visual comparison, never assumption)
found the following genuinely real defects, none of which the 2026-08-30 text-match caught:

1. **Font extension jar entirely missing (checklist item 3).** `pom.xml` had no
   `com.inpex:inpex-arial-fonts` dependency (every other R07/R10 report in this project does).
   Confirmed via `get_text('dict')`: the whole document rendered in plain `Helvetica` with the
   bold flag never set, despite `bold="true"` on 7 elements and `fontName="Arial"` throughout.
   Fixed by copying `R07.002/output/fonts/inpex-arial-fonts.jar` into R07.003's own
   `output/fonts/` and adding the matching `<dependency scope="system">` block to `pom.xml`.
   Confirmed fixed: a minimal isolated repro (`mini_fonttest.jrxml`) rendered `Arial-BoldMT`/
   `ArialMT` after the fix, vs `Helvetica` before.

2. **Invented purple fill color (checklist item 1).** `PurpleSectionStyle` used `#444080`;
   `get_drawings()` fill-color histogram against the reference showed the real color is
   `#454087` (48/30/3 fills across pages 1-2, zero at `#444080`) — the exact same invented-color
   defect class as R07.002's Part P1/O1. Fixed.

3. **Zero `<box>` pens and zero `<element kind="line">` dividers anywhere in the entire
   769-line file (checklist items 1, 2, 5, 6).** The whole report had no cell borders and no
   section-title divider lines at all — `grep -c '<box'` and `grep -c 'kind="line"'` both
   returned 0 before this pass. The reference has 355+80+8+4+6 gray `#D6D6D6` width-1.0 borders
   and 8 dark-gray/purple width-1.5 divider lines across its 5 pages. This is a substantially
   bigger gap than anything found on R07.002 (which at least had borders, just wrong colors).
   Fixed by adding a `<box>` pen to `PlainLabelStyle`/`PlainValueStyle` (borders every data
   cell project-wide via one style edit) and adding 8 measured `<element kind="line">` dividers
   (1 under the title, 1 under each of the 7 section titles: HSE, Production/Internal
   Consumption/Losses, Production Quality, Gas Export Pipeline, Inventory, Offtakes, plus the
   per-record divider on the Comments pages).

4. **Column-header cells rendered as plain bold text with no purple fill at all (checklist
   item 1).** `HeaderLabelStyle` had no `mode`/`backcolor` — every column header ("#",
   "Comments", "19-Oct", "Avg Pressure", etc, 87 elements) rendered as plain black bold text
   instead of the reference's white-bold-italic-on-`#454087` bar. Fixed by adding
   `mode="Opaque" backcolor="#454087" forecolor="#FFFFFF"` directly to the style — deliberately
   WITHOUT a `<box>` pen, per Part D1 in the lessons file (an opaque text element's own border
   is drawn under its fill and never appears; the reference itself shows no internal divider
   between same-color adjacent header cells anyway, confirmed via a zoomed recon of the HSE/POB
   header row).

5. **Missing italic everywhere (checklist item 8).** `italic="true"` appeared 0 times in the
   whole file before this pass. `get_text('dict')` span-font checks on the reference show every
   title/section-header/column-header as `ArialBoldItalic`, and the footer strip/disclaimer
   suffix as `ArialItalic` (non-bold) — confirmed on ALL 5 pages, not assumed from one page.
   Fixed by adding `italic="true"` to `TitleStyle`, `PurpleSectionStyle`, `HeaderLabelStyle`,
   and `FooterStripStyle`.

6. **Missing INPEX logo (checklist item 2).** Zero `<element kind="image">` in the whole file —
   the same defect class R07.002 had. Fixed by copying `logo.jpg` into R07.003's own output
   folder and adding the image element at the measured position (local x=1,y=22,w=128,h=22).
   Title/date text were also repositioned (measured directly from THIS report's own reference,
   not copied from R07.002's values) since their old y-values (10/38) collided with the new
   logo's y-range.

7. **HSE and POB column geometry never matched the reference at all (checklist item 4/9).**
   The original build's label column overshot into the "#"/value column's real start (e.g.
   label `width="180"` starting at the same x where the "#" column's real border sits at
   x=134), and the "#"/"Comments" header cells used arbitrary x/width values (`x=150 w=40`,
   `x=460 w=150`) that didn't correspond to either the label's real end or the Comments
   column's real start (x=187). Once borders were added (fix #3), this rendered as disconnected,
   floating boxes rather than a tiled grid. Fixed by re-measuring the real column boundaries
   directly from the reference's own `get_drawings()` rects (both the header purple-fill rects
   AND the data-row border verticals independently agree: label 1-134, #/value2 134-187,
   Comments 187-798 for HSE; label 2-134, 19-Oct 134-202, 20-Oct 202-271, Comments 271-798 for
   POB) and rebuilding both tables' header and data-row elements to those exact boundaries. Also
   fixed: the POB header row's own "POB" label was plain black text (`PlainLabelStyle`) instead
   of the reference's white-bold-italic-on-purple first header cell; and the Night Shift row was
   missing its own blank bordered 20-Oct cell (a genuine R2 "blank column still needs an
   element" violation, not just a cosmetic gap).
   **Disclosed limitation (not fixed this pass):** the SAME column-geometry defect very likely
   also affects the main "Production, Internal Consumption & Losses" table, Production Quality,
   Gas Export Pipeline, Inventory, Offtakes (page 1) and Major Equipment Status/Production
   Risks/Consumables/CCPP/Environmental (page 2) — re-measuring and rebuilding all of those to
   the same tiled-edge-to-edge standard was judged out of scope for this pass (would require the
   same per-table `get_drawings()` remeasurement done for HSE/POB, repeated ~11 more times) and
   is flagged here as follow-up work rather than silently left unaddressed.

8. **Production Quality header row: two columns overlapping + wrong labels + one column's
   header missing entirely (checklist item 4).** The header row had `N2` at `x=553 w=45` and
   `C6+` at `x=561 w=37` — a 37pt overlap producing a garbled "NC6+"-looking render — while the
   DATA rows underneath (already correct) used `x=553` for `C6+`, `x=603` for `CO2`, `x=663` for
   `N2`, and `x=713` for `HHV(Btu/Scf)` (confirmed via the "CPF rich gas export to GEP" row's own
   `9.87` value at `x=603`, matching the reference's real CO2 value/position). The header row
   had never been updated to match: it mislabeled `x=553` as "N2", mislabeled `x=603` as
   "HHV(Btu/Scf)", mislabeled `x=663` as "CO2", and had no header at all for `x=713`. Fixed by
   correcting all 4 header labels/positions to match the data rows' own already-correct column
   mapping (`get_text('dict')` word-position dump against the reference confirmed the real
   order is C1,C2,C3,iC4,nC4,iC5,nC5,C6+,CO2,N2,HHV(Btu/Scf)).

9. **A visible solid black vertical line down the left edge of pages 2-5.** The unconditional
   1x1090 spacer rectangle (added in the 2026-08-30 build specifically to stop the detail band
   collapsing to zero height, see the "Key takeaway" section above) had no `mode`/`pen`
   attributes — a bare `<element kind="rectangle">` defaults to a black width-1.0 border, the
   same class of bug as Part M3 in the lessons file ("a bare pen silently defaults to black").
   This was never visible in the 2026-08-30 text-only verification since a vertical line has no
   text content to diff. Fixed by adding `mode="Transparent"` and an explicit
   `<pen lineWidth="0.0"/>` — confirmed via re-render that the black line is gone and the page
   count is still exactly 5 (i.e. the spacer still does its actual job of reserving height).

10. **The "Comments" table (pages 3-5) rendered as ONE overlapping text blob per entry, with
    the section title/header row drawn on TOP of the comment body text, instead of a genuine
    3-column table (checklist items 1, 4, 7).** `gen_comments.py`'s extraction correctly split
    the reference into 6 entries but never split each entry into its 3 real columns (Comment
    Type / Comments / Author) — it dumped "Isabella Boyd\n<Type>\n<body text>" as one single
    710pt-wide text block, and (compounding the defect) the FIRST entry on record 2 was placed
    at `y=40`, directly on top of the title (y=10-30), date (y=38-52), and the "Comments"
    section header row (y=139-149) — visually confirmed via rendered PNG (the header bar
    literally overlaps mid-paragraph in the "Degraded/Impaired SCE" line). Fixed for all 6
    entries across all 3 pages by: measuring the reference's real 3-column boundaries via
    `get_drawings()` (Comment Type x=6-159, Comments x=160-645, Author x=646-790); splitting the
    first two lines ("Isabella Boyd", the type name) out of each entry's body text into their
    own positioned elements in the Comment Type and Author columns; and repositioning each
    entry's start y to clear the title/header above it. Record 2 (page 3) keeps the full
    title+divider+header-row treatment (matches the reference, which repeats it there); records
    3 and 4 (pages 4-5) correctly do NOT repeat the section title/header row, only the plain
    title+date+divider — confirmed by checking the reference's own page 4/5 layout directly
    rather than assuming header-repeat-per-page from page 3's convention.
    **Disclosed judgment call:** record 4 (page 5, 3 entries + the Disclaimer footer) was
    already filling essentially the entire 1100pt detail-band budget in the original build
    (entry 3 ending at y=1036, Disclaimer at y=1087, ~1pt of slack). The standard ~99pt-deep
    divider gap used on every other page would have overflowed the band. Used a compressed
    54pt gap for this page's divider instead (disclosed in an inline JRXML comment) rather than
    shrinking real per-line content heights to make room — a real, deliberate trade-off, not a
    silently-skipped fix.

### Verification performed this pass
- Page count reconfirmed exactly 5 after every edit that touched a band height or a
  `printWhenExpression`-gated block (the font/color/border/divider edits didn't touch band
  heights and weren't re-checked for page count on every single one, only after the batches
  that plausibly could affect it — disclosed here rather than claimed as "checked every time").
- `get_drawings()` color/fill histogram compared page-by-page (all 5 pages) before and after
  the font/color/border fixes.
- `get_text('dict')` span-font audit compared page-by-page (all 5 pages) before and after the
  italic fix; confirmed `Arial-BoldMT`/`ArialMT` rendering via an isolated `mini_fonttest.jrxml`
  repro before touching the production file.
- Full-page PNG renders (150dpi) of all 5 generated pages visually compared side-by-side against
  the reference's own 150dpi renders — this is what caught defects #6 (logo), #7 (HSE/POB
  geometry), #8 (Production Quality header collision), #9 (black spacer line), and #10 (Comments
  overlap), none of which the histogram/font checks alone could have found.
- Did NOT re-verify: exact per-row column tiling for the main Production table, Production
  Quality data rows, Gas Export Pipeline, Inventory, Offtakes, or the page-2 tables (Major
  Equipment Status/Production Risks/Consumables/CCPP/Environmental) — these likely have the
  same HSE/POB-class column-gap defect (visible as small floating-box gaps in the page 1/2
  renders) but re-measuring and rebuilding all of them to a tiled-edge-to-edge standard was
  judged out of scope for this pass and is flagged as follow-up work (see item 7 above).

### Honest bottom line
This pass found and fixed 10 distinct, real, confirmed defects spanning essentially every one
of the 12 checklist categories (color/fill, dividers/logo, font extension, header-vs-data
consistency, row geometry, blank-column elements, spacer/opaque-fill artifacts, and a genuine
content/structure bug in the Comments table that the original text-match verification could
never have caught since it only checks whether words are present, not whether they overlap).
The report is now substantially closer to the reference — logo, colors, italics, dividers,
HSE/POB/Production-Quality/Comments-table structure all genuinely match now, confirmed via
rendered-PNG visual comparison, not assumed. It is NOT yet a claim of pixel-perfect, fully
column-tiled match: the disclosed remaining gap (item 7's follow-up list) is real and would
need the same per-table `get_drawings()` remeasurement this pass did for HSE/POB, repeated for
every other table in the report, to close completely.

---

## 2026-08-31 (later same day) — Closing the disclosed column-tiling gap (owner-directed follow-up)

Backup taken first: `output/R07_003_Onshore_Daily_Operations_Report.jrxml.backup_20260831_140309_before_column_tiling_fix`.
Final checkpoint after all fixes: `...backup_20260831_142602_after_column_tiling_fix`.

Re-measured every remaining table's real column boundaries directly from the reference PDF's
own `get_drawings()` fill/border rects (never eyeballed), per Part R (header-fix ≠ table-fix)
and Part S1 (row height vs. row spacing) in `JASPERREPORT-7-0-3.MD`. All 10 tables named in the
prior pass's disclosed follow-up list were checked. Findings, table by table:

1. **Main "Production, Internal Consumption & Losses" table — REAL, SEVERE defect, fixed.**
   The data-row value columns and the label column were built from `gen_maintable.py`'s guessed
   "bins around visible word x-positions" (`COLS = [("A", 237, 310), ...]`), not the reference's
   real cell/border boundaries. Measured real boundaries via `get_drawings()` border rects on a
   populated data row (label 1-189, then 7 value columns 189-278-365-455-541-631-709-790, local
   coords) and cross-checked against right-aligned value text right-edges (all 7 matched the
   real boundaries to within 1-2pt). The label column alone was 47pt too wide (235 vs real 188),
   overlapping 25% into column 1's real space. Rewrote all 18 data rows' `x`/`width` (7 column
   patterns, ~120 elements via targeted regex substitution) plus the label width. **Separately**,
   the reference's 2-tier header is a SEAMLESS purple grid (`get_drawings()` fill rects tile
   edge-to-edge across both header rows with only a hairline white divider between cells), but
   the existing header static-text elements are individually shrink-wrapped to their own text
   width — leaving large white gaps between them. Confirmed the header TEXT positions themselves
   already matched the reference's real word coordinates almost exactly (e.g. "Volume" at real
   x=215.9,y=335.7 vs the file's existing x=216,y=336) — an earlier attempt to "recenter" these
   labels onto my own assumed column centers was WRONG and reverted; the fix is background fill,
   not moving text. Added 11 full-column-width `PurpleSectionStyle` background rectangles behind
   the existing (unmoved) header labels — 3 for the group-tier row (label/Daily Qty
   group/merged MTD Qty+MTD Variance group — confirmed via `get_drawings()` that the reference
   draws the MTD group and MTD Variance column as ONE continuous row1 rect, not two) and 8 for
   the leaf-tier row (label + 7 real data columns). Re-rendered and visually confirmed: the
   header now tiles exactly like the reference's seamless purple grid, and the data rows'
   columns align under the correct headers (previously they did not).
2. **Production Quality data rows — mostly already correct (per the prior pass's own note), ONE
   real defect found:** the label column's border box (width=170) overshot the real column1
   boundary (measured via `get_drawings()`: real label end ≈ local x=155) by 15-17pt, overlapping
   into the "C1" column and producing a visible double-border sliver on every one of its 7 rows.
   The C1-through-HHV(Btu/Scf) column x/width values themselves were already within a few points
   of the real measured boundaries (confirmed, e.g. CO2 at x=603 vs real 603 — exact) — no change
   needed there, matching the prior pass's claim. Fixed the label width only (170 → 155).
3. **Gas Export Pipeline — REAL defect, fixed.** Existing header/value TEXT positions already
   matched the reference's own word coordinates closely (left as-is). The defect was FILL/BORDER
   only: no background rect existed for either header row (group-tier "Offshore"/"Onshore" or
   leaf-tier 6 sub-columns), and the 6 data-value boxes (width=80 each, with 25-35pt gaps between
   them) were far narrower than the real measured columns (widths 104/106/107/107/87/86, edge-to-
   edge). Added 2 group rects + 6 leaf rects for the header, and widened all 6 value boxes to the
   real column boundaries.
4. **Inventory — REAL defect, fixed.** Same pattern: header had 4 floating shrink-wrapped labels
   with zero background fill (real reference is one continuous 4-segment purple bar); the 3
   value-group data boxes (widths 90/90/60) were far narrower than the real measured columns
   (197/200/197). Fixed both; also tightened the label column from 200→192 to match the real
   boundary exactly (was a mild 7-8pt overshoot, not as severe as Production Quality's).
5. **Offtakes — REAL defect, fixed, including an outright column OVERLAP.** The 6 data-value
   boxes did not just have gaps — several actively overlapped their neighbours (e.g. "Lucky
   Chemist" at x=270 started 18pt before Vessel Name's real column start of 289, double-bordering
   into Cargo ID's cell). Measured the real 6-column boundaries (155/130/132/132/118/119pt wide)
   via `get_drawings()` and rebuilt all 6 header-row background rects and all 6 value-row
   x/width values to match exactly.
6. **Major Equipment Status — REAL defect, TWO classes.** (a) No background fill on the header
   row at all (7 floating labels), fixed with 7 real-measured rects (Area 1-97/Tag 97-174/OOS
   174-230/Estimated+RTS 230-285/Safety+Critical 285-329/Planned 329-373/Comments 373-790).
   (b) A genuine PRE-EXISTING column-ORDER defect, not just a tiling gap: "Safety"/"Critical" and
   "Estimated"/"RTS" were positioned inside each other's real columns (both landed inside the
   174-230 "OOS" range, overlapping it), and "Planned" was one column too far left — confirmed via
   `get_text('words')` real x-order (Area, Tag, OOS, Estimated/RTS, Safety/Critical, Planned,
   Comments) vs. the file's built order. Repositioned all 3 to their real columns; also
   tightened "Safety"/"Critical"/"Planned"'s label widths from 60→44pt so they no longer spill
   into the adjacent (now correctly-narrow) columns.
7. **Production Risks — REAL defect, both classes again.** (a) No header background fill (8
   columns), fixed with 8 real-measured rects (Area 1-97/Tag 97-186/Work Order 186-253/Plan
   253-304/Priority 304-346/Risk 346-376/Description 376-754/Focal 754-790 — note: unlike Major
   Equipment Status, the real WORD order here already matched the file's built order, so no
   swap was needed for Work Order/Risk). (b) "Plan" and "Priority" were each one column too far
   left (245→267, 295→307) and "Priority"'s label width (60) was wide enough to visually collide
   with "Risk" even after repositioning — shrunk to 42pt to fit its real 304-346 column exactly.
8. **Consumables — REAL defect, fixed.** Header (Name/Closing Volume/Filled Volume/Comments) had
   no background fill; added 4 real-measured rects (1-230/230-351/351-483/483-790). Data rows are
   label+value form pairs (not a full grid) matching the reference's own thin-vertical-divider-
   only pattern — left unchanged, correctly, per Part R3's "check the reference's actual pattern"
   rule (a per-row grid fix would have been WRONG here).
9. **CCPP — REAL defect, fixed.** The 2 "Description" column headers (mirrored left/right panel
   layout) had no background fill; the reference actually draws 4 purple zones per header row
   (label1/value1/label2/value2), not 2 — added all 4 real-measured rects
   (2-264/262-393/394-653/653-790). Header text left unmoved (already close to real word x).
10. **Environmental — REAL defect, fixed.** Both of its header rows ("Stream Name"/"Volume" and
    "Description"/"Min"/"Max"/"Average"/"Avg Heat Index") had no background fill; added 2+5 real-
    measured rects. Text left unmoved.

### Verification performed this pass
- Every one of the ~15 edit batches above was followed by `mvn -q compile` +
  `R07003Verify` and a page-count check — stayed at exactly 5 pages throughout (confirmed after
  every band-adjacent change, per Part S2/checklist item 12; no band HEIGHT was touched this
  pass, only in-band element x/width/text, so no page-count risk was expected or found).
- Main table, Production Quality, GEP/Inventory/Offtakes, and the full page-2 top block (Major
  Equipment Status + Production Risks) were each re-rendered as a zoomed 150-250dpi crop and
  visually compared side-by-side against the equivalent reference crop via the Read tool after
  their fix, before moving to the next table — not batched blind.
- A final full-5-page 140dpi render was visually inspected end-to-end: page 1 (all 5 page-1
  tables), page 2 (all 5 page-2 tables), and page 3 (Comments, unaffected by this pass, confirmed
  still rendering correctly with no regression).
- Corrected my own mid-pass mistake before it shipped: an early attempt to "recenter" the main
  table's header labels onto my own computed column midpoints was checked against the
  reference's real word coordinates, found to be WRONG (the original positions were already
  correct), and reverted in the same session rather than left in.

### What was already fine, honestly (no fix needed, verified not assumed)
- Production Quality's C1-through-HHV(Btu/Scf) column x/width values (only the label width was
  wrong).
- Consumables/CCPP/Environmental's underlying label+value form-style row layout (only their
  header background fill was missing — the reference itself does not use a per-row bordered grid
  for these sections, confirmed via `get_drawings()`, so no row-level change was made).
- Production Risks' column word ORDER (only Major Equipment Status had a real order swap).

### Bottom line
All ~11 tables named in the prior pass's disclosed follow-up list have now been individually
re-measured against the reference's own `get_drawings()` boundaries and fixed where a real
defect existed. Every table now tiles edge-to-edge where the reference itself tiles edge-to-edge,
matches the reference's real column ORDER (two genuine order-swap defects were found and fixed
in Major Equipment Status and Production Risks, beyond the originally-scoped tiling-gap class),
and no table was left as a "looks roughly right" guess. Page count re-confirmed at exactly 5
throughout. R07.003 is now considered genuinely matching its reference table-by-table for
layout/geometry, to the depth measured in this pass (get_drawings() boundaries + zoomed visual
crops); it was NOT re-run through the full 12-item checklist end-to-end in this pass (that was
already done in the prior 2026-08-31 audit above) — this pass specifically closed the one gap
that audit disclosed.

## Owner rejection (2026-08-31, all 4: R07.003-R07.006) — the automated audits above were
insufficient; personal full-page visual comparison found real defects they missed
The owner ran their own comparison of the generated PDFs against the originals and rejected ALL
FOUR reports (R07.003-R07.006) as not matching, despite the multi-agent audits above reporting
them as verified. The root cause of the gap: those audits leaned on zoomed crops, color
histograms, and word-diffs — all real checks, but none of them is "render the WHOLE page at
readable scale and actually read it end to end next to the WHOLE reference page," which is what
finally surfaced the following in R07.003 (via personal, first-hand comparison, not delegated):

1. **CCPP table — fragmented/doubled internal borders**, confirmed via `get_drawings()`
   coordinate measurement (not a visual guess — an initial visual impression of "everything is
   italic" was checked this same session and found FALSE via `get_text('dict')`, so every
   subsequent claim here was measurement-verified before acting). Root cause: label elements
   were sized `width=390`, wildly overreaching into and past the neighboring value column's real
   boundary (per the table's own header rects: label1 0-264/value1 262-393/label2 394-658/
   value2 653-790) — the label's own box border landed almost exactly on the label2 boundary,
   and each row's value element had a DIFFERENT ad-hoc x/width sized to its number's string
   length, so the internal vertical border line landed at a different x on every row. Fixed by
   resizing every label/value element to the table's real, CONSISTENT column boundaries
   (label1 x=4 w=258, value1 x=264 w=129, label2 x=396 w=257, value2 x=655 w=133) across all 5
   rows — confirmed via re-measurement and a zoomed render that the fragmented look is gone.
2. **"No Records Found" wrongly boxed AND wrongly centered** (both Major Equipment Status and
   Production Risks instances) — reference has this text with NO border and LEFT-aligned at the
   table's left margin; the build had it centered inside a bordered box. Fixed by moving to
   `x=4`, adding `hTextAlign="Left"`, and zeroing the inherited `PlainLabelStyle` box pen.
3. **Sub-item row indentation under Production/Internal Consumption/Losses too shallow** —
   measured real deltas: reference indents sub-items ~11.7pt from their section label; the build
   only indented ~2pt. Fixed by moving all 18 sub-item label elements from `x=2` to `x=13`
   (re-measured after fix: 13.0pt delta, matching).
4. **Numbered sub-item list ("1./2./3./4." under LNG1/LNG2 in the Comments free text) missing
   its indent entirely** — reference indents these ~28pt from "LNG1"/"LNG2"; the raw extracted
   text had zero leading whitespace. Fixed by prepending 12 literal spaces to the 5 affected
   text lines (re-measured after fix: 28.8pt delta, matching within 1pt).
5. **Off-specification tank closing volume / STG bypass valve row — the "2" value was in the
   WRONG column** (a genuine data-position defect, not cosmetic): measured the reference's real
   glyph x-position for "2" and confirmed it sits under "Off-specification tank closing volume"
   (value1), not under "STG bypass valve" (value2) — the build had it on the wrong side. This
   same swap was independently confirmed and fixed on R07.004 too (see below) via the identical
   measurement method — worth checking on any other report sharing this row.

**Standing lesson (the reason ALL FOUR reports were rejected despite passing every automated
check the prior audits ran): a battery of targeted checks (histogram, word-diff, zoomed crops)
is not a substitute for someone actually reading the full page, end to end, next to the full
reference page, at a size where text and borders are legible — that is the check that caught
every defect in this list. It should be the FIRST verification step on any report, not a
follow-up when something "seems off."** Equally important: a visual impression from that
full-page read is still not proof by itself — the "missing italic everywhere" and "dashed
border" leads from this same session both turned out to be FALSE once checked against
`get_text('dict')`/`get_drawings()` — every defect above was confirmed with real coordinate/font
data before being fixed, not acted on from the visual impression alone.
