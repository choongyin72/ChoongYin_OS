# R10.001 — JCC Price Calculation — rebuild notes (2026-09-04)

## ✅ OWNER-VERIFIED COMPLETE (2026-09-04)
Owner reviewed in detail against the Crystal original and confirmed the layout is finished:
*"R10.001 is now fully completed for the report layout... our version is actually more
presentable, neat, and clean overall."*

Worth carrying forward as an observation, not a rule: all three type-2 changes removed things
Crystal does out of layout NECESSITY rather than design intent — unbordered empty corner cells,
placeholder blank cells, and the 2.8pt sliver hack used to keep a fill unbroken. Matching
Crystal exactly reproduces those compromises. Still per-report by owner decision (see below).

Rebuilt against `crytsal report in pdf/R10.001 - JCC Price Calculation.pdf`. The client will not
release the `.rpt` files, so the reference PDF is the source of truth and every value below was
measured from it.

Files: `output/R10_001_JCC_Price_Calculation.jrxml` + `.pdf` (name matches the JRXML stem).
Backups: `*.backup_20260904_r10_001_rebuild` for the JRXML and `cp.txt`.

## Verification — current state

| Check | Result |
|---|---|
| pages / images | 1/1 · 1/1 |
| embedded fonts | 34 BoldItalic / 15 Plain / 1 Bold — **exact match** |
| words | 0 missing · 0 extra |
| span positions | **0 of 50** off at 1.5pt tolerance; 38 at dy=0 |
| borders (rendered ink) | 0 doubled, 0 vertical issues |

Two border-audit entries, both accounted for:
- `MISSING 526.08` — tool artifact, not a defect. `r10_borders.py` projects dark pixels per
  row, so WHITE TEXT ON A PURPLE FILL splits one filled band into several and reads as a gap.
  Confirmed identical to the reference at 900dpi.
- `EXTRA 263.76` — the deliberate type-2 borderline under `X3`/`X3 R3` (deviation 3 below).

## Type 1 — defects against the Crystal reference (8, all fixed)

1. **Arial font extension never wired.** No R10 report referenced `inpex-arial-fonts.jar`, so
   `fontName="Arial"` resolved to nothing, fell back to Helvetica, and JasperReports SILENTLY
   dropped every bold/italic. All 46 spans rendered Helvetica.
2. **`italic="true"` appeared ZERO times in the file.** The reference embeds
   `Arial-BoldItalicMT` for 34 of 50 spans — every label, header, section title, the report
   title, the footer and the formula. Not inferable; it had to be read off the reference's own
   embedded fonts.
3. **Font sizes wrong throughout** — table text 8.0 → **9.0**, title 16 → **18**,
   footer 7.0 → **8.0**.
4. **Purple wrong** — `#444080` → **`#444088`**. The reference measures 0.533 blue; `0x80` is
   128/255 = 0.502 and could never have matched.
5. **Logo absent.** Extracted from the reference with `get_pixmap(clip=...)` at 600dpi — never
   raw XObject extraction, which distorts (it produced an "INbEX" garble on R07.005/006).
6. **Formula box, Comments box and footer strip were never built.** Added at measured
   coordinates: formula box abs (28.3, 470.2, w535.5, h16.7); comments box abs
   (28.3, 625.9, w537.7, h122.2); footer purple rule abs y=792.3.
7. **Row Y drift.** The build stepped rows by 13 where the reference steps by **13.3**,
   accumulating 1.3pt of error by the fourth row.
8. **Footer rule 1.2pt high and 0.24pt thick.** A `height="0"` rectangle draws its pen CENTRED
   on the nominal y, so ink spans y ± pen/2 — the position must be derived from that, not from
   the intended ink edge.

## ⚠️ Type 2 — DELIBERATE DEVIATIONS FROM CRYSTAL (owner request, 2026-09-04)

These do NOT match the reference. They are presentation improvements the owner asked for.
**Do not "correct" them back toward Crystal.**

1. **Empty corner cells given a visible border.** The empty purple top-left cell of all four
   tables. Crystal leaves these unbordered; the owner wants them closed.
2. **Middle table's two blank bottom-row cells removed.** Crystal draws them (where the left
   table has `X / 8,772,602` and the right has `Y / 60,904.973`); the owner does not want them.
3. **The 2.8pt purple slivers removed, replaced by a borderline.** Crystal draws a filler at
   abs y=261.5 h=2.8 to keep the purple label column unbroken while the value columns show the
   sum-row separation. Removed by request; the `X3`/`X3 R3` row now takes a normal bottom
   border instead. This is what produces `EXTRA 263.76` in the border audit.

Owner's standing rule: **type-2 changes are decided per report, not applied as house style.**
Do not carry these three to the other 18 reports without asking.

## 🐛 Root cause worth carrying to every other R10 report

`HeaderCellStyle` sets `forecolor="#FFFFFF"` so its text renders white. A bare
`<pen lineWidth="0.5"/>` with **no `lineColor`** inherits that forecolor — so every purple
rectangle was outlining itself in WHITE, i.e. invisibly. Cells containing text looked correct
only because their `staticText` box pen is separately black; EMPTY cells got nothing.

48 pens were given an explicit `lineColor="#000000"`.

Note the two different consequences, which need different handling:
- where Crystal HAS a border and ours renders none → a real type-1 defect, fix it
- where Crystal ALSO lacks the border → matching Crystal means leaving it absent; adding one is
  type 2 and needs the owner's call

## Method notes

- **Crystal draws every border as a FILLED RECT.** This reference has **0 strokes** and 149
  thin black fills. So rect counts are not comparable with JasperReports output (296 vs 210
  here is construction, not defect) and border geometry must be read off fills. Compare
  rendered INK instead.
- **`75.33` is the report's only `Arial-BoldMT` span** — bold but NOT italic, unlike every
  other emphasised element. A single-span exception only a per-span font read catches.
- **A text box shorter than fontSize × 1.2 makes JasperReports silently DROP the text.**
  Raising the title to 18.0 required its box to grow 20 → 22.
- Span-position checks CANNOT see borders. R10.001 passed 50/50 spans while the footer rule was
  still misplaced. The gridline ink audit is mandatory, not optional.
