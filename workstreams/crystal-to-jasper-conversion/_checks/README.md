# Crystal → Jasper layout checks

Shared checks for the INPEX Crystal→JasperReports conversion. Every script takes a report
number and resolves both PDFs itself:

```
py crop_sheet.py                 R07.005          # LOOK first - always
py check_internal_consistency.py R07.005
py compare_ink.py                R07.005
py diag_all_lines.py             R07.005
py check_value_positions.py      R07.005
py check_vertical.py             R07.005
```

Paths come from `_common.py`:
`C:\Projects\INPEX\sources\CrystalReports\<report>\output\*.pdf` (generated) and
`...\crytsal report in pdf\*.pdf` (reference — the folder really is spelled "crytsal").

Set `GENPDF` to point at a different generated file — useful when the real PDF is locked open
in a viewer, or to validate a check against an older build:

```
GENPDF='output\_t.pdf' py check_internal_consistency.py R07.005
```

## Run them in this order

**1. `crop_sheet.py` — look at it.** Slices each page at its own section rules and writes
gen/ref crop pairs to `<report>/_crops/`. This runs FIRST. A per-attribute diff can score zero
on a section that is visibly wrong, because each check is blind exactly where its attribute is
absent (lessons file Part X, Part Y8).

**2. `check_internal_consistency.py` — the output against ITSELF.** Per table: are all column
lines the same thickness (including the one inside the header band), are row lines uniform.
No reference involved. Catches the class where the reference shares the flaw — on R07.004 a
header divider rendered 2.04pt against a 1.02pt body divider and Crystal had the same 2pt
divider, so every reference comparison called it correct (Part Z1).

**3. `check_value_positions.py` — is the content in the right box.** Compares each text's
rendered x-centre against the reference. A border check confirms the boxes and a text check
confirms the words; neither notices a correct word inside the wrong box. This found
Environmental t2's four values shifted one column right with two stacked in the same cell.

**4. `diag_all_lines.py` — missing/extra horizontal rules per page.** Found that a whole detail
record on R07.003 had no `<line>` elements at all.

**5. `compare_ink.py` — rendered ink thickness, matched gridline by gridline, both axes.**
Probes only where the strip either side is clean white so glyphs cannot inflate the reading.
This is the check that catches border doubling (Part Y1).

**6. `check_vertical.py` — y offsets of named anchors per page.**

## Two rules that cost real rework to learn

- **Validate a check against a build that HAS the defect before trusting it.** A check that has
  never fired is not a passing check. `check_internal_consistency.py` was validated this way:
  it reports the defect on R07.004's pre-fix build and 0 on the fixed build.
- **Measure the current value of what you are about to change, before changing it.** Acting on
  a magnified crop without that step made a non-defect worse on R07.004 (Part Z10).

## Run the fixes in this order

`fonts → columns/geometry → tiling/de-double → alignment → internal consistency`

Learned on R07.004 and R07.005: running de-double before column snapping means the snap
introduces fresh 1pt gaps and de-double has to run twice. And after any font change, re-run
`check_fonts_and_text.py` immediately — a box that was big enough at 8pt silently drops its
text at 9pt (lessons file Part F1).

## What these checks CANNOT see

Every check here is geometric or textual. Five defect classes got past all of them on R07.005
and the owner found them by eye — each is now covered, but know the shape:

1. **`rectangle` header elements.** A pattern matching `staticText|textField` misses the header
   entirely. Include `HeaderCellBoxStyle` rects, and enumerate a table's real styles first
   (sub-heading rows may use `SubSectionTitleStyle`).
2. **A missing cell breaks the row's horizontal LINE.** With `topPen 0`, a row's top line is
   drawn by the row above's BOTTOM border — so an absent cell leaves stubs either side of the
   gap. The boundary set can still look complete, because neighbouring cells' pens supply the
   verticals.
3. **Row OVERLAPS, not just gaps.** A row 2pt taller than its pitch puts two horizontal lines
   2pt apart with white between - reads as a "narrow gap".
4. **A tall cell spanning two header rows** stops the inter-header line crossing that column.
5. **Tolerances.** `check_value_positions.py` ran at 12pt and passed an 11.8pt indentation
   defect. It is now 4.0pt. **When a large cluster shares one shift value it is ONE systematic
   difference, not N defects** — 93 of R07.003's 135 are all -4.2pt, which is a padding
   convention, not 93 problems.

## Known limitations

- `check_value_positions.py` pairs duplicate texts by (row, then x). Sorting by y alone cannot
  pair duplicates that share a row and produced false "shifts" of up to 264pt on rows of four
  zeros.
- `check_internal_consistency.py` ignores any measured line wider than 3pt, on the basis that a
  gridline is never that thick — a wide run means the probe landed on text or a fill boundary.
- `compare_ink.py` matches gridlines within ±3pt. A rule displaced further than that reports as
  "no matching rule in ref" rather than as a shifted rule; `diag_all_lines.py` shows those
  properly as a MISSING/EXTRA pair.
