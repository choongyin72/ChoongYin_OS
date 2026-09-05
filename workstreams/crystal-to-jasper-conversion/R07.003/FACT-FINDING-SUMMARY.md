# R07.003 — Fact-Finding Summary: how the layout defects were traced and fixed
**Date:** 2026-08-31 · **Report:** Onshore Daily Operations Report (5 pages, A3 portrait)
**Result:** 597 measured differences → **0** on pages 1-4, 0 real on page 5
(3 residual items on page 5 are a PDF text-extraction artefact, visually verified identical)

---

## 1. Why the earlier attempts kept failing

Every earlier pass used a **single-attribute check** — a colour histogram, or a word-count
diff, or a zoomed crop of one suspected area. Each check "passed" on the one thing it looked
at while missing everything beside it. That is why defect after defect survived and the owner
kept finding them by eye.

The specific failure was not the tooling — `get_drawings()` / `get_text('dict')` are the right
primitives — it was **never comparing every attribute of every element in one pass**, and never
reading whole pages at readable scale.

## 2. What actually worked: one exhaustive, all-attribute comparison

A single script (`tmp/deepdive_r003.py`) that, for **every text span on every page**, pairs the
generated PDF against the reference and checks **all** of:

| Check | Catches |
|---|---|
| font size | the systemic 6.5pt-vs-9pt defect (was ~460 spans) |
| bold / italic (from real font name) | wrong emphasis |
| text colour | white-on-purple vs plain black |
| fill behind the text | section titles wrongly given a purple bar |
| x-position (both edges) | wrong column, wrong alignment, wrong indent |
| text present / missing / extra | silently dropped or duplicated content |

Plus a second script (`tmp/diff_drawings.py`) comparing **drawings** (fills, borders, rules) —
added after the span diff reached zero but the page still *looked* wrong, proving the span
diff alone was still blind to rectangles.

Two supporting habits mattered as much as the scripts:
- **Every candidate defect was confirmed with real coordinates/font names before editing.**
  Three visual impressions turned out FALSE on measurement ("everything is missing italic",
  "the header has a dashed border", "page-3 Comments is the wrong colour") and were dropped
  instead of "fixed".
- **Re-render and actually look after each fix.** The numbers hit zero twice while the page
  was still visibly wrong; only looking exposed the remaining border/fill defects.

## 3. Root causes found (grouped — 597 differences collapsed to ~12 real causes)

| # | Root cause | Evidence | Scale |
|---|---|---|---|
| 1 | **Style font sizes wrong**: `PlainLabel/PlainValue`=6.5, `HeaderLabel`=6.5, `PurpleSection`=8.0, footer=7.0 vs reference 9 / 10 / 10 / 6 | per-span size diff | ~460 spans |
| 2 | **Main title 16pt instead of 21pt** | `get_text('dict')` size | 5 pages |
| 3 | **9 section titles rendered as purple bars** (Health Safety & Environment, Gas Export Pipeline, Inventory, Offtakes, Major Equipment Status, Production Risks, Consumables, CCPP, Environmental) — reference has **no fill at all** on any of them | `get_drawings()` fill probe at each title's exact position | 9 titles + 9 backing rects removed |
| 4 | **Header cells too short for the corrected 10pt text** → JasperReports *silently dropped* 66 header labels | missing-text diff | 92 cells 10→14pt |
| 5 | **Group headers wrapped** ("Daily Quantity" → "Daily"/"Quantity") because the centred label box was narrower than the text | extra/missing-text pair | 5 labels |
| 6 | **`HeaderLabelStyle` is `mode="Opaque"`** — every header *text* painted its own purple box on top of the cell, so any size mismatch showed as a notch, sliver, or a bar overhanging the table edge | drawings diff (78 gen-only purple fills vs 40 in ref) | 38 texts → transparent twin style; 9 backing rects added |
| 7 | **HSE / POB rows had a ~5pt gap**: boxes 12pt tall but rows spaced 17pt / 15pt; reference rows touch | row-band geometry | 20 cells |
| 8 | **Alignment wrong**: POB 19-Oct/20-Oct, all Gas Export Pipeline and all Inventory values were `Right` but the reference **centres** them (verified: text-centre == column-centre) | left-gap vs right-gap measurement | 24 cells |
| 9 | **Consumables data rows missing cells entirely** for the blank *Filled Volume* and *Comments* columns — a blank column still needs a bordered element or it visually disappears | drawings diff: ref 4 verticals per row, gen 2 | 5 rows rebuilt to a 4-cell grid |
| 10 | **Production Quality values misaligned** by 6-9pt across 11 columns | per-row left-to-right cell pairing | 27 cells |
| 11 | **Text dropped by an undersized box**: "Economizer drain weld repair ongoing." lost when the comment body grew to 9pt | missing-text diff | box 666→900 |
| 12 | **Character-level mismatch**: reference uses `º` (U+00BA) in *exactly one* label ("Avg. Main steam header temperature (ºC)") while every other degree sign is `°` (U+00B0) — an inconsistency in the original Crystal report that must be reproduced to match | codepoint scan | 1 label |

Also fixed: footer middle text was centred but is left-aligned at x=349 in the original; a
stray extra "Comments" line inside the Executive comment body; a hard line-break that the
original keeps on one line; Disclaimer 6.5→9pt (and its box widened after 9pt truncated it
to "Disclaim").

## 4. Mistakes made during the fix (and what they teach)

- **A fix that created a new defect twice.** Correcting the indent by shifting `x` without
  reducing `width` pushed the label's own border 11pt into the next column — which is exactly
  the "STUCK" gap being reported. *Lesson: when moving a bordered cell, x and width must change
  together, or use padding instead of x.*
- **A blanket change caught the wrong element.** Setting the Environmental headers to 9pt also
  hit the Production Risks "Description"; a page-2 centring rule was applied to page 3's
  identically-named header. *Lesson: scope every bulk edit by record/page, then re-verify.*
- **Curing one artefact exposed another.** Making header text transparent removed the notches
  but also removed the purple from cells that had no backing rectangle (Production Quality) —
  caught immediately because the diff went 0 → 11. *Lesson: re-run the full diff after every
  structural change; a regression is only cheap if it is found in the same minute.*

## 5. The check that should run first, every time

1. Render **every page in full** and read it against the reference page.
2. Run the **all-attribute span diff** (size, bold, italic, colour, fill, position, presence).
3. Run the **drawings diff** (fills, borders) — the span diff cannot see rectangles.
4. Confirm each candidate with real coordinates/fonts **before** editing.
5. After each fix: recompile, **check the page count**, re-run the diffs, and look again.

## 6. Verification evidence (final state)

- `deepdive_r003.py`: pages 1-4 = **0** differences; page 5 = 3 items, each verified by
  high-DPI render to be identical text that the reference PDF merely splits into two spans.
- Compile: `COMPILE OK` / `FILL OK: 5 page(s)` / `EXPORT OK` — page count matches the
  reference's own "Page N of 5".
- Visual: all 5 pages rendered and read side-by-side against the reference.
- Backups retained at each verified checkpoint, ending
  `...jrxml.backup_20260831_opus_ALL5PAGES_MATCH`.

## 7. Not done (by design)

Data-query binding remains deferred to a later phase (owner-confirmed) — this pass is layout
only, using `JREmptyDataSource`.

## 8. Applies to R07.004 / R07.005 / R07.006

These share the same build lineage, so causes **1, 3, 4, 6, 7, 8, 9** should be assumed present
until disproved by the same measurements. The two scripts run unchanged against any report by
swapping the two file paths.
