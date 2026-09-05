# R10.002 — Monthly LNG Contract Price — rebuild notes (2026-09-04)

## ✅ OWNER-VERIFIED COMPLETE (2026-09-04)
*"Done for R10.002 report layout.. its look nice and OK with original crystal report layout."*

## Type 2 applied (owner request via screenshot, 2026-09-04)
**The 2.8pt purple sliver before the `Applicable JCC` row was REMOVED**, leaving a clean
full-width white gap with a borderline above and below. This is a DELIBERATE DEVIATION — Crystal
draws that sliver at abs y=272.2 h=2.8 to keep the purple label column unbroken. Same
preference the owner approved on R10.001. The borderlines either side come for free now that
the white-pen bug is fixed.

Rebuilt against `crytsal report in pdf/R10.002 - Monthly LNG Contract Price.pdf`.
Files: `output/R10_002_Monthly_LNG_Contract_Price.jrxml` + `.pdf`.
Backup: `*.backup_20260904_rebuild`.

## Verification
| Check | Result |
|---|---|
| pages / images | 1/1 · 1/1 |
| embedded fonts | 20 BoldItalic / 15 Plain / 4 Bold — **exact match** |
| words | 0 missing · 0 extra |
| span positions | **0 of 39** off at 1.5pt; **dx = 0 for all 39** |
| font/size mismatches | 0 |

Residual border-audit flags, all accounted for:
- vertical flags at x=28–53 are the **logo raster's edges**, not borders — a bitmap edge
  profile differs from a drawn rule
- `MISSING 798.24 / EXTRA 799.68` is the footer TEXT row (the detector treats a full-width text
  line as a rule); the 1.4pt delta is within the <1.5pt span tolerance already passed
- 2 of 24 rules render 0.48/0.72 against the reference's 0.24. Left alone: the reference's
  border fills are 0.3pt and ours are a 0.5pt pen, which the detector reads as equal at 300dpi
  for 22 of 24 rules. Not worth a global pen change for a sub-0.5pt difference on two rules.

## Type 1 — defects against the reference (all fixed)
Same systemic set as R10.001 — no font jar, zero italics, sizes 8.0/16/7.0 instead of
9.0/18/8.0, purple `#444080` instead of the measured `#444088`, no logo, no footer rule, and a
1pt tiling gap. **Plus five defects specific to this report:**

1. **Footer is `Arial-BoldMT` — bold, NOT italic.** R10.001's footer is BoldItalic. Copying
   R10.001's pattern here would have been wrong; each report's fonts must be read from its own
   reference.
2. **Footer has a SECOND line** at abs y=805.7 (the timestamp). The build concatenated label
   and value onto one line, so the report was a line short.
3. **Info-block VALUE cells are unfilled white.** Only x=0 and x=255 carry purple at abs
   y=137.5/150.8/164.1/177.5. The build used `ValueCellStyle` (`#F8FBFC`). The JCC and LNG
   tables DO use `#F8FBFC`, so the two cannot share a style — hence a new `InfoValueStyle`.
4. **Info-block row 4, third column is a PURPLE LABEL cell**, not blank — the reference fills
   x=283 (local 255) purple on that row. The build used `BlankCellStyle`.
5. **The LNG table's `May-2025` is a purple LABEL, not a value.** The reference fills that cell
   purple and sets the text `Arial-BoldItalicMT`; the build rendered it `ArialMT` on `#F8FBFC`.
   Same shape as R10.001's section-3 first column.

Also corrected by measurement: JCC month values are **right-aligned** (built as centred, ~30pt
out), and `InfoValueStyle` needed `leftPadding` 1 not 3 (one padding error, 6 spans).

## ⚠️ TYPE-2 CANDIDATE — left in deliberately
The **2.8pt purple filler** at local y=244 (abs 272.2) is built because Crystal has it. The
owner had the equivalent REMOVED from R10.001 as a presentation preference, but ruled that
type-2 decisions are per report — so it stays here until they say otherwise.

Other R10.001 type-2 changes NOT applied here, for the same reason:
- empty corner cells left as Crystal has them (the JCC and LNG header rows have one)
- the info-block row-4 blank value cell at x=383 is retained

## Method note
The white-pen bug applies here too: 36 bare `<pen lineWidth="0.5"/>` were inheriting
`HeaderCellStyle`'s white `forecolor` and outlining purple cells invisibly. All given an
explicit `lineColor="#000000"`.
