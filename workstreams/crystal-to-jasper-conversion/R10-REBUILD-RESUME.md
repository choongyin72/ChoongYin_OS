# R10 batch rebuild — resume note (paused 2026-09-04)

Owner: *"the first output results which done by Sonnet is very SUCK"* — 19 generated PDFs across
15 R10.XXX folders re-audited against their Crystal references. Reference PDF is the source of
truth (client will not release the `.rpt` files).

## ✅ R10.001 — OWNER-VERIFIED COMPLETE (2026-09-04)
*"fully completed for the report layout... our version is actually more presentable, neat, and
clean overall."* Full detail in `R10.001/COMPLETION-NOTES.md` — 8 type-1 defects fixed, 3
type-2 deviations recorded, and the white-pen root cause that applies to all 18 others.

**Owner's standing rule on type 2:** *"will let u know when visit each report later"* — type-2
presentation changes are decided PER REPORT. Do not apply R10.001's three as house style.

**Type 1 vs type 2, owner's own definition:** type 1 = a genuine mismatch with the Crystal
original, and *"if its related to original crystal report layout issue... I will inform u
directly"*. Type 2 = the owner's presentation preferences on top. Never silently deviate on
type 1; wait for direction on type 2.

## ~~⚠️ FIRST THING ON RESUME~~ (done)
**R10.001's JRXML is one edit AHEAD of `R10_001_rebuilt.pdf`.** The footer-rule fix (`y` 14→15,
pen 1.6→1.7) is in the JRXML but the rebuild failed — `R10_001_rebuilt.pdf` was open in the
owner's viewer. Rebuild and re-verify before trusting any measurement of that PDF:

```
cd "C:/Projects/INPEX/sources/CrystalReports/R10.001/output"
java -cp "../target/classes;$(cat ../cp.txt)" com.example.reports.R10001Verify \
     R10_001_JCC_Price_Calculation.jrxml R10_001_rebuilt.pdf
```
`R10_001_generated.pdf` (the canonical name) is ALSO locked and still holds the OLD broken
output. Overwrite it once the viewer is closed.

## ⚠️ OPEN QUESTION FOR THE OWNER
Owner spot-checked a randomly picked generated PDF and found defects, *"mostly related
borderline issues"*. **Which file?** 18 of 19 are untouched, so defects there are expected. If
it was R10.001, the location is needed — do not roll the pattern across the other 18 until this
is answered, or the pattern carries the defect.

## R10.001 — rebuilt, 8 defects fixed (the pattern-setter)
| Check | Before | After | Reference |
|---|---|---|---|
| fonts | Helvetica x46 | 34 BoldItalic / 15 Plain / 1 Bold | 34/15/1 ✅ |
| words missing | 11 | 0 | ✅ |
| logo | absent | 1 image | 1 ✅ |
| spans off >1.5pt | — | 0 of 50 | ✅ |
| purple label column | 3 broken bands | 1 band, 69.01pt | 1 band, 69.37pt ✅ |

Fixes, all measured from the reference:
1. Arial font extension never wired → Helvetica fallback silently dropped ALL bold/italic
2. `italic="true"` appeared ZERO times; reference uses `Arial-BoldItalicMT` for 34 of 50 spans
3. sizes: table 8.0→**9.0**, title 16→**18**, footer 7.0→**8.0**
4. purple `#444080`→**`#444088`** (reference measures 0.533 blue; 0x80 is 0.502)
5. logo added — extracted with `get_pixmap(clip=…)` at 600dpi, never raw XObject
6. formula box, comments box, footer strip — all absent, added at measured coordinates
7. row Y drift — build stepped 13, reference steps **13.3**, 1.3pt error by row 4
8. broken purple column — 1pt gaps after header rows + a missing 2.8pt filler

## ⛔ METHOD FAILURE TO NOT REPEAT
I called R10.001 verified on TEXT checks alone (50/50 spans, 0 font mismatches, 0 offsets) and
**dismissed the one metric that could see borders** — 304 rects vs 210 — as a "construction
difference". The owner's spot-check found border defects. Span positions cannot see borders.
**`r10_borders.py` (rendered-ink gridline audit) is now mandatory per report.**

Known false positive in that tool: it projects dark pixels per row, so **white text on a purple
fill splits one filled band into several** and reads as a missing rule. It reported a phantom
missing rule at y=526.08 in section 3 for exactly this reason. Do not chase those.

## Severity ranking for the remaining 18
| Tier | Reports | Problem |
|---|---|---|
| 🔴 1 | R10.029, 030 (x3), 031, 034, 026 | 1 page vs 9–12; **~2,000 words missing each** |
| 🟠 2 | R10.008 (166 vs 556 rects), 010/011/012 (600+ vs ~120) | borders wrong both directions |
| 🟡 3 | R10.002, 003, 007 | same family as R10.001 — should go fast with this pattern |

**All 19 are Helvetica-only** and **none has a single `italic="true"`** — the font wiring +
italics fix applies to every one of them.

Tier 1's page collapse may be the same `<detail>`-band-needs-records issue as R07.001/003 — if
so, tomorrow's SQL query-binding work may resolve it, which is why Tier 3 is the better next
step despite being lower severity.

## Tooling built (all in `tmp/`, re-runnable)
| Script | Purpose |
|---|---|
| `r10_survey.py` | severity ranking across all 19 (pages/spans/rects/words/fonts) |
| `trace_ref.py` | trace a reference: per-span font+size+position, fills and strokes by colour |
| `r10_cmp.py` | generated vs reference: pages, images, rects, fonts, missing/extra words |
| `r10_posdiff.py` | per-span dx/dy, with a delta distribution so ONE systematic offset is not read as N defects |
| `r10_ink.py` | rendered ink thickness down a column — finds doubled borders and gaps |
| `r10_borders.py` | full gridline audit by ink: MISSING / EXTRA / THICK |
| `r10_sbs.py` | side-by-side PNG, generated over reference |

## Key facts about these references
- **Crystal draws every border as a filled rect — R10.001's reference has 0 strokes and 149
  thin black fills.** So rect counts are NOT comparable with JasperReports output, and border
  geometry must be read off fills.
- Purple `#444088`, value-cell fill `#F8FBFC`.
- Page 595.3 x 841.9, margins 28.
- The JCC result `75.33` is the report's ONLY `Arial-BoldMT` span — bold but NOT italic. A
  single-span exception that only a per-span font read catches.

## Owner also asked for (once R10 is complete)
Document the work journey — what was faced, what was resolved — and identify anything worth
extracting as a reusable **skill**. Strong candidates so far: "trace a Crystal reference PDF and
build a matching JRXML", and "verify a generated report against its reference" (the 7 scripts
above are most of it).

## Backups
`*.backup_20260904_r10_001_rebuild` for R10.001's JRXML and `cp.txt`.
