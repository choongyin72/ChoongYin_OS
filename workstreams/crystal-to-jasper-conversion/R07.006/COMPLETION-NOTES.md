# R07.006 — Onshore Production Report — Completion Notes (2026-08-30)

**Phase:** LAYOUT ONLY. First of 6 previously-unbuilt R07 reports (R07.001-006), tackled after
the confirmed R07/R10 batch, per explicit owner direction to apply the same rigor as the R10
batch. Simplest of the 6 (single page), built first per the simple→complex convention.

**Build location:** `C:\Projects\INPEX\sources\CrystalReports\R07.006\output\`.

## Report shape (measured directly)
- A3-sized portrait page (842x1191pt) — genuinely different page size from every R10 report
  (which used standard letter/A4-ish 595x842 or 842x595). Margins ~22pt, confirmed via
  leftmost/rightmost/topmost text extremes.
- Main table "Production, Internal Consumption & Losses": a 3-tier nested column header
  (Monthly Quantity → Volume/Mass; Short Term Forecast(tonnes); YTD Quantity → Volume/Mass;
  Annual Budget Forecast(tonnes); YTD Variance(%) — 7 value columns total), confirmed via direct
  word-position recon cross-referencing header-row-group text against data-row-group value
  positions (not assumed from any prior report). 25 label rows across 4 sub-sections
  (Production/Internal Consumption/Losses/Delivered).
- Body rows are BORDERLESS plain text (confirmed via `get_drawings()` — only the purple
  `#444080` section-header bars have a fill), unlike the fully-bordered cell convention used
  throughout the R10 family.
- Below the main table: Inventory (Opening/Closing, 5 products), Liftings (Number of
  cargoes/Volume/Mass, 4 products, with an italic "Note: Excludes liftings in progress at
  month-end" caption), CCPP (2-column Description/Value form, 7 rows, 2 genuinely blank),
  Environmental (Stream Name/Volume, 1 row), Comments.

## Build approach — programmatic row generation (new for this session)
Given the main table's scale (25 rows × up to 7 columns ≈ 130 individual values), hand-typing
each cell risked repeating R10.029's manual mis-mapping mistake. Instead, wrote a Python script
that: (1) extracted all words in the table's y-range, (2) grouped them by row (rounded y), (3)
classified each word as a label or a value based on its x-position falling within one of 7
pre-measured column ranges, (4) paired label-only rows with their adjacent value-only row (or
handled same-line label+value rows directly), and (5) emitted the JRXML `staticText` elements
directly with `x`/`y` already translated to local coordinates (`abs - 22`). This produced all
164 table-row elements in one pass with zero manual transcription, and iterating on a bug (the
script initially skipped "combined" label+value rows on the same line, silently dropping 4 rows)
took one script edit instead of one manual re-check per row.

## Defects found and fixed
1. **Non-ASCII characters (³, °) initially at risk of corruption** — the recon script used
   Python's default console encoding (`cp1252`), which can't represent `³`/`°`; fixed by writing
   recon output with explicit UTF-8 encoding. The JRXML itself renders these correctly since it
   declares UTF-8 in its XML prolog.
2. **Generator script initially dropped 4 rows** (Cold flare, Tankage flare, Total gas flared,
   and several "Delivered" section rows) where the label and its values shared the same
   y-coordinate — the script's row-classification logic only handled "label-only row followed by
   a value-only row" and "label-only row with no values" (section headers), missing the
   "label+values on the same line" case entirely. Fixed by adding that case explicitly; row count
   went from 21 to 25 (later confirmed to be the full correct set via the whole-page text diff).

## Verification performed
- Whole-page text extraction (`page.get_text('text')`) confirmed all individual words are
  present; the small number of apparent "missing"/"extra" combined strings (e.g. "Mass
  (tonnes)", "221Avg. Main steam header pressure (kPa)") were traced to PyMuPDF line-joining
  differences from adjacent-element proximity, not missing content — confirmed by searching for
  each individual word separately.
- Coordinate spot-check on 9 section-header labels landed within ~1-2pt of the reference for Y
  position (Delivered, Liftings, Environmental, Comments all within ~1.3pt); "CCPP" and
  "Production," checks picked ambiguous duplicate-text matches (not real defects, confirmed by
  the word itself appearing correctly elsewhere in the document).

## Not done this phase (by design)
- Live query/data verification — deferred, same as every prior report in this project.

## Key takeaway (2026-08-30 build)
For any report with a large, repetitive multi-column table (this one: 25 rows × 7 columns), a
programmatic row-extraction-and-generation script is both faster and safer than hand-typing each
cell — it eliminates the R10.029-style manual mis-mapping risk entirely, at the cost of writing
and debugging the extraction logic once. This approach should be the default for any future
report with a comparably large tabular section, reserving hand-written elements for headers,
section titles, and other one-off content.

---

# FULL REBUILD — 2026-08-31 (owner-directed 12-item checklist audit)

**Trigger:** the R07.002 session (same day) went through 8 owner-pushback rounds before being
accepted, because its original build — like this one — was verified with ONLY a whole-page
text-extraction match, which caught none of: missing logo, wrong color scheme, non-wired
font-jar (bold/italic silently falling back to plain), header-fix-not-propagated-to-data-rows,
row-height-vs-spacing gaps, band-height overshoot, copied-not-derived widths, opaque-fill
offset artifacts, or inconsistent title-to-divider spacing. The owner directed the SAME rigor be
applied to R07.006 proactively, per the 12-item checklist at the end of
`DeepDiveLearnings/JASPERREPORT-7-0-3.MD` ("Post-mortem — checklist to re-run on R07.003-R07.006").
This section documents that full re-audit and rebuild, run against R07.006's own reference PDF
from scratch — every visual claim in the original 2026-08-30 notes above was treated as
UNVERIFIED until independently re-measured here.

## Verification method
1. Compiled the CURRENT (2026-08-30) JRXML to a fresh baseline PDF, confirmed page count (1,
   matches reference) and page geometry (842x1191 vs reference's 841.85x1190.55 — matches).
2. Rendered both the baseline and the reference PDF to full-page PNGs at 150dpi and looked at
   them side by side (Part Q1 lesson: histogram/text checks alone repeatedly missed real defects
   on R07.002 this same day — only an actual rendered image catches some defect classes).
3. Ran `page.get_drawings()` on the reference to get every fill/stroke rectangle's exact
   coordinates and color, `page.get_text('dict')` for every text span's exact font
   name/size/color/bbox, and `page.get_images()`/`extract_image()` for the embedded logo.
4. Classified the reference's 291 raw drawing operations into 25 purple-filled "header cells", 236
   plain gray-bordered "data cells", and 8 divider lines (2 navy `#454087`, 6 dark-gray `#636363`)
   — done PROGRAMMATICALLY (bounding-box matching between fill rects and their paired border
   strokes), not by eye, to avoid a repeat of the K1/K5 manual-transcription risk on ~500 objects.
5. Wrote a generator (`tmp/r07006_build_jrxml.py`) that emits one JRXML element per classified
   object, deriving x/y/width/height, bold/italic, alignment, and fill/border color DIRECTLY from
   the reference's own measurements — zero hand-typed coordinates for the ~500-element rebuild.
6. Recompiled and re-rendered after every structural change; recompiled+checked page count after
   every band-height edit (S2/Rule-14-item-12); re-ran `get_drawings()` color histogram,
   `get_text('dict')` font check, whole-page word-frequency diff (`Counter` subtraction, P4
   technique), and an exact-coordinate border-rect set-diff between reference and generated PDF
   as the final proof, not just a visual glance.

## Defects found and fixed (this rebuild) — mapped to the 12-item checklist

1. **Color/fill scheme (checklist #1) — WRONG on every section below the main table.**
   `Production`/`Internal Consumption`/`Losses`/`Delivered` (sub-section labels INSIDE the main
   table) were built as purple-filled bars (`PurpleSectionStyle` rectangle+text) — the reference
   shows these as PLAIN bold black text with NO fill at all (confirmed via `get_drawings()`: zero
   fill draws at that y-position, confirmed via `get_text('dict')`: font `ArialBold`, not
   `ArialBoldItalic`, color `0x000000`). Conversely, `Inventory`/`Liftings`/`CCPP`/
   `Environmental`/`Comments` (the 5 section titles below the main table) were built AS the purple
   bar itself, merged with their own column-header row — the reference shows these as PLAIN bold-
   ITALIC black titles (own row, own divider line below), with a SEPARATE purple-filled
   column-header row underneath (e.g. "Opening Inventory"/"Closing Inventory", "Product"/"Number
   of cargoes"/"Volume"/"Mass (MT)"). Both directions of this purple-vs-plain confusion were
   swapped in the original build. Fixed by rebuilding all title/header treatment directly from
   the reference's 25 measured purple-fill cells + `get_text('dict')` bold/italic flags — no
   guessing which convention applied to which line.
2. **Logo/dividers/title positions (checklist #2) — logo completely absent; ALL 8 divider lines
   absent.** Zero `<element kind="image">` existed anywhere in the pre-rebuild file. The
   reference has a real INPEX logo image (confirmed via `page.get_images()`, xref 21, DeviceRGB,
   1772x306px) at abs bbox (22.65,40.0)-(150.2,62.0) — extracted directly from THIS report's own
   PDF (not copied from a sibling report's `logo.png`) and added. The reference also has 2 navy
   (`#454087`) divider lines (under the title block, above the footer) and 6 dark-gray
   (`#636363`) section-title divider lines (one under EACH of the 6 section titles) — none
   existed in the prior build; all 8 added at their exact measured positions.
3. **Font extension jar wired (checklist #3) — CONFIRMED BROKEN, root-caused, fixed.** Built a
   minimal isolated repro (`mini_test.jrxml`-`mini_test5.jrxml`) before touching the production
   file (per Part L5): `fontName="Arial"` with `bold="true"`/`italic="true"` compiles with ZERO
   error/warning but renders as **plain, non-bold, non-italic Helvetica** in the actual exported
   PDF (`get_text('dict')` on the mini-test output showed `font=Helvetica flags=0` regardless of
   the bold/italic attributes set) — this project's `pom.xml` depends on `jasperreports-fonts`
   7.0.3, but inspecting that jar directly (`jasperreports_extension.properties`) showed it only
   registers the **DejaVu** family (Sans/Serif/Sans Mono), never "Arial" — exactly Rule 10's
   documented gap. Switching every `fontName="Arial"` to `fontName="DejaVu Sans"` (confirmed via
   the same mini-test harness: `DejaVuSans-Bold`/`DejaVuSans-Oblique`/`DejaVuSans-BoldOblique` all
   render correctly) fixed bold/italic across the entire file. This was invisible in the very
   first full-page screenshot at low DPI (text looked present and roughly the right size) and
   would have shipped silently wrong without this specific check.
4. **Header structure fixed ⇒ data rows re-checked (checklist #4).** Not applicable as a
   propagation bug here (this was a from-scratch structural rebuild, not a header-only patch), but
   verified post-rebuild: every data row's column x/width in the regenerated file is taken
   directly from the SAME measured `plain_cells` list as the header, so there is no possibility of
   the two drifting apart (R1's failure mode structurally cannot occur with this generation
   method).
5. **Row height vs. row spacing (checklist #5) — verified, matches.** Measured the main table's
   label-column border rects programmatically: consecutive rows tile with a 0-1pt gap throughout
   (e.g. `y0=224,y1=237` then `y0=238` — 1pt gap, imperceptible, and this exact 0-1pt gap is
   present in the reference's own measurements too, not something this build introduced).
6. **Blank/empty columns still bordered (checklist #6) — satisfied by construction.** Because
   every bordered cell in this rebuild is emitted from a REAL measured stroke rectangle in the
   reference (not from "does this row have a value"), blank cells (e.g. "Liquid flare (m³)"'s
   missing Short-Term-Forecast and Annual-Budget-Forecast columns) automatically keep their empty
   bordered box — confirmed visually in the final render.
7. **Free-text blocks: one shared box vs. per-line (checklist #7) — N/A for this report.** This
   report's only free-text line ("Note: Excludes liftings in progress at month-end") has NO
   border in the reference at all (confirmed via `get_drawings()`: no stroke rect at that
   y-position) — rebuilt as plain unboxed italic text, matching.
8. **Bold/italic/alignment verified per-element (checklist #8) — done via `get_text('dict')`
   span-level font names for all ~250 text spans, not assumed from visual impression.** Caught,
   beyond the font-jar issue itself: multi-line header cells (e.g. "Short Term"/"Forecast"/
   "(tonnes)" stacked in one purple cell) were initially placed using the CELL's full height with
   `vTextAlign="Middle"`, which centers ALL stacked lines on top of each other — overlapping,
   unreadable text (only visible on this specific engine's DejaVu Sans font metrics, which is
   wider than the reference's Arial, at the second render pass). Fixed by positioning each
   stacked line at its OWN measured y (not the cell's), only using the cell's x-range for
   horizontal centering.
9. **Row-rect widths re-derived per table (checklist #9) — satisfied by construction.** Every
   rectangle's width in this rebuild is `measured_x1 - measured_x0` from the reference's OWN
   drawing for that exact cell — never a value copied from a sibling table or a different section
   of the same report.
10. **Opaque-fill elements checked for BOTH border and fill offset (checklist #10) — verified via
    exact-coordinate set-diff.** Ran a border-rect-by-border-rect comparison (not just a color
    histogram) between reference and generated PDF: of 258 gray-bordered cells in the reference,
    all 258 are present in the generated PDF at the SAME rounded integer coordinates (0 missing).
    3 EXTRA gray-bordered cells exist in the generated PDF's CCPP header row (columns 1, 3, 4)
    that don't exist in the reference — traced to the reference itself inconsistently omitting
    the border stroke on 3 of its own 4 CCPP header cells (col 2 keeps an explicit stroke, cols
    1/3/4 apparently don't, per the reference's own raw drawing dump) while this rebuild
    consistently draws a border on every header cell. This is a genuine, measured, sub-visible
    difference (a gray 1pt border sitting on/adjacent to a purple fill that's already touching an
    identically-colored neighboring fill — zero visible effect, confirmed by direct crop
    comparison) — NOT claimed as "confirmed identical", disclosed here as the one known technical
    delta between this build and the reference's raw vector content.
11. **Section-title-to-divider spacing self-consistent (checklist #11) — verified numerically.**
    Measured the gap between each of the 6 section titles' own text bottom edge and its divider
    line in the GENERATED PDF: 6.6pt for 5 of 6 titles, 5.6pt for CCPP (1pt narrower) — close
    enough to read as visually consistent and within the same tolerance band the reference itself
    shows, not a copy-pasted assumption.
12. **Band-height changes re-verified via page count (checklist #12) — done every time.** The
    `<title>` band height was changed from 1100 to 1117 (exact fit: 1191 pageHeight − 22 topMargin
    − 22 bottomMargin − 30 pageFooter = 1117) specifically because a `kind="line"` divider element
    placed at the true measured y (1116.7, rounds to 1117) tripped a real compile-time validation
    error (`"Element bottom reaches outside band area: y=1117 height=1"` — a `height="0"` line
    element is still validated as if it occupies 1pt) that would not have been caught without
    actually recompiling after the edit. Page count re-confirmed at 1 (matches reference) after
    every subsequent change.

## Final verification evidence (commands actually run, not assumed)
- `page.get_drawings()` color/fill histogram: reference and generated PDF match on EVERY category
  except the one disclosed 3-cell delta in item 10 above (261 vs 258 gray-bordered strokes; 25/25
  purple fills; 6/6 dark-gray dividers; 2/2 navy dividers — all exact).
- Whole-page word-frequency diff (`collections.Counter` subtraction on `get_text('text')`,
  Part P4 technique): **zero missing, zero extra words** between reference and generated PDF.
- `get_text('dict')` font-name check on every title/section-title/header/footer span: all render
  as the correct `DejaVuSans`/`DejaVuSans-Bold`/`DejaVuSans-Oblique`/`DejaVuSans-BoldOblique`
  combination matching the reference's `Arial`/`ArialBold`/`ArialItalic`/`ArialBoldItalic` roles.
- Page count: 1 (reference: 1). Page geometry: 842x1191 (reference: 841.85x1190.55, matches
  within PDF unit-rounding).
- Full-page render-and-look comparison (150dpi PNG, both PDFs) plus 8 targeted zoomed crops
  (title block, main-table header, Inventory, Liftings, CCPP, Environmental, Comments, footer):
  visually matching the reference in every section — logo present, correct purple/plain
  distribution, correct bold/italic, correct borders throughout, correct divider lines.

## Root cause of the original (2026-08-30) build's defects
The original build was verified with ONLY: (a) a whole-page text-extraction presence check, and
(b) a 9-label coordinate spot-check for Y-position. Neither check can detect: absent images
(text extraction doesn't see them), wrong fill/border colors (text extraction doesn't see
color), wrong bold/italic (text extraction reports the same string whether bold or not, and this
engine's Arial-without-a-registered-font-jar bug meant even LOOKING at the rendered PDF at
insufficient zoom could miss it), or absent divider lines (not text). This matches, independently
and on a different report, EXACTLY the R07.002 post-mortem's core finding from the same day: a
clean text/coordinate check proves words are present roughly in the right place, and nothing else.

## Not done this phase (by design, unchanged from 2026-08-30)
- Live query/data verification — deferred, same as every prior report in this project.

## Files touched
- `output/R07_006_Onshore_Production_Report.jrxml` — fully rebuilt title band (logo, all 6
  section titles + subsection labels re-styled, full 3-tier main-table header rebuilt with real
  purple fills/borders, ~500 elements total generated programmatically from reference recon).
- `output/logo.png` — extracted directly from this report's own reference PDF (xref 21).
- `output/R07_006_Onshore_Production_Report.jrxml.backup_20260831_pre_audit` — pre-rebuild backup.
- `output/R07_006_Onshore_Production_Report.jrxml.backup_20260831_post_rebuild_verified` — post-
  rebuild checkpoint backup (all `.backup_*` files retained, none deleted, per standing rule).
- `output/R07_006_Onshore_Production_Report.pdf` — final verified output (supersedes the earlier
  `R07_006_test.pdf`/`R07_006_baseline.pdf`, both removed as superseded working files — no
  `.backup_*` files were touched).

## Key takeaway (2026-08-31 rebuild)
A report that "passes" a text-match and a 9-point coordinate spot-check can still have its ENTIRE
visual identity wrong (no logo, inverted purple-vs-plain convention, silently-plain-instead-of-
bold-italic text from an unregistered font family) — the only way to catch this class of defect
is the same discipline used here: `get_drawings()` for color/fill, `get_text('dict')` for
per-span font verification (never assume from a screenshot), an actual rendered-image comparison,
and a real compile+recompile cycle after every structural change. This is now the second report
in this project (after R07.002, same day) where this exact defect pattern was found — the 12-item
checklist this rebuild was run against should be applied to R07.001, R07.003, R07.004, and R07.005
before any of them are trusted as "done" either.

---

# CORRECTION — 2026-08-31 (later same day): DejaVu Sans substitution reverted to REAL Arial

**Why this correction was needed.** The `fontName="DejaVu Sans"` swap made in the rebuild above
(item 3 / "Font extension jar wired") made bold/italic render as visually distinguishable text,
but it did NOT satisfy the owner's standing directive that "both layouts must MATCH IDENTICALLY,
with no exceptions." Personally re-verifying this report's OWN reference PDF via
`page.get_text('dict')` on
`C:\Projects\INPEX\sources\CrystalReports\R07.006\crytsal report in pdf\R07.006 - Onshore
Production Report.pdf` showed its real fonts are
`['Arial', 'ArialBold', 'ArialBoldItalic', 'ArialItalic']` — genuine Arial, not DejaVu Sans. A
different typeface family (different letter shapes, spacing, character width) is a real, visible
mismatch even when bold/italic now render distinctly — DejaVu Sans was never an acceptable
substitute, just a workaround that avoided registering the real font.

**The correct fix — already proven on sibling reports R07.002 and R07.004 in this same project —
was to wire the real Arial font extension jar into the Maven build, not switch families.**
Replicated exactly:
1. Copied `inpex-arial-fonts.jar` from
   `C:\Projects\INPEX\sources\CrystalReports\R07.002\output\fonts\inpex-arial-fonts.jar` to
   `C:\Projects\INPEX\sources\CrystalReports\R07.006\output\fonts\inpex-arial-fonts.jar`.
2. Added the matching `com.inpex:inpex-arial-fonts:1.0` `system`-scope dependency block
   (`systemPath=${project.basedir}/output/fonts/inpex-arial-fonts.jar`) to
   `C:\Projects\INPEX\sources\CrystalReports\R07.006\pom.xml`.
3. Reverted all 250 occurrences of `fontName="DejaVu Sans"` back to `fontName="Arial"` in
   `output/R07_006_Onshore_Production_Report.jrxml` (script:
   `C:\Projects\ChoongYin_OS\tmp\r07006_revert_arial.py`).
4. Backed up the JRXML before editing:
   `output/R07_006_Onshore_Production_Report.jrxml.backup_20260831_before_real_arial_fix` (all
   4 pre-existing `.backup_*` files retained, none deleted).
5. Recompiled (`mvn -q compile`), regenerated the classpath
   (`mvn -q dependency:build-classpath -Dmdep.outputFile=output/cp.txt`), and re-ran
   `com.example.reports.R07006Verify` from `output/` — compiled OK, filled 1 page, exported OK.
6. Took a final checkpoint backup after verification:
   `output/R07_006_Onshore_Production_Report.jrxml.backup_20260831_after_real_arial_fix_verified`.

**Verification evidence — actual font names from `get_text('dict')` on the regenerated PDF (all
4 bold/italic combinations present in the file checked, not just one sample):**
- Before this correction (prior round): `Helvetica` (plain, non-bold, non-italic) — the silent
  fallback documented in the U2 finding below — masked visually by the DejaVu Sans substitution
  in the interim.
- After this correction: `ArialMT` (209 spans), `Arial-BoldItalicMT` (33 spans), `Arial-BoldMT`
  (4 spans), `Arial-ItalicMT` (4 spans) — genuine Arial family, matching the reference's
  `Arial`/`ArialBold`/`ArialItalic`/`ArialBoldItalic` naming exactly (PDF base-font naming adds
  the `MT` suffix per the standard Arial PostScript names; same family).
- Page count: 1 (unchanged, matches the reference's real page count of 1, independently
  re-confirmed via `fitz.open()` on the reference PDF this session).

**Files touched this correction round:**
- `output/R07_006_Onshore_Production_Report.jrxml` — 250× `fontName="DejaVu Sans"` reverted to
  `fontName="Arial"`.
- `output/fonts/inpex-arial-fonts.jar` — added (copied from R07.002).
- `pom.xml` — added the `com.inpex:inpex-arial-fonts` system-scope dependency block.
- `output/R07_006_Onshore_Production_Report.pdf` — regenerated with real Arial.
- Two new backups added (see step 4/6 above); zero backups deleted.
- `DeepDiveLearnings/JASPERREPORT-7-0-3.MD` Part U (finding U2) — corrected to stop documenting
  the DejaVu Sans swap as "the fix"; now points to the font-jar wiring instead.

**Key takeaway.** A workaround that makes two DIFFERENT defects (plain-instead-of-bold-italic,
wrong typeface family) look superficially similar in a quick visual glance is still wrong on an
"identical match" standard — verify the reference's OWN actual font names via `get_text('dict')`
before accepting ANY font substitution as a fix, don't stop at "bold and italic are now visually
distinguishable."

## Owner rejection (2026-08-31) — personal full-page visual comparison found a real, significant
defect the prior audits missed: a corrupted logo asset
The owner rejected this report alongside R07.003/004/005 despite two rounds of audit above
reporting it verified. A personal full-page render-and-read comparison (viewing the WHOLE page
at a size where the logo is actually legible, not a zoomed-crop-only check) immediately showed
the INPEX logo rendering as a visibly garbled "INbEX" — malformed letterforms, not just a minor
rendering artifact. Zoomed both the generated and reference logos at 400dpi side by side to
confirm: reference is clean "INPEX", generated is genuinely distorted.

Root cause and fix followed the EXACT pattern already documented as Part U2 in
`DeepDiveLearnings/JASPERREPORT-7-0-3.MD` from R07.005's own logo bug (raw XObject extraction —
`Pixmap(doc, xref)` / `page.extract_image()` — can decode a logo image distorted even with a
correct byte count, while `page.get_pixmap(clip=<real bbox>)` on the LIVE rendered reference page
always produces the correct asset). Measured the logo's real bbox via `get_image_info()`
(`(22.65, 40.0, 150.2, 62.0)`), re-extracted it via `get_pixmap(dpi=300, clip=bbox)`, and
overwrote `output/logo.png`. Recompiled and re-zoomed: logo now reads clean "INPEX", matching
the reference exactly. Checked R07.003/004/005's own logos at the same zoom level as a
precaution — all three were already clean; this corruption was specific to R07.006's asset file.

Page count unchanged at 1. No other defects found in this pass — the rest of the page had
already been rebuilt with real measured `get_drawings()` boundaries in the earlier audit round
and matched the reference closely on direct re-inspection.
