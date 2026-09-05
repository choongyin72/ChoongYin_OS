# R07.012 — FC Lifting Report — Conversion Recon Spec

**Status: BUILD COMPLETE.** The build described as pending below was carried out in a later
session directly under `C:\Projects\INPEX\sources\CrystalReports\R07.012\output\` (outside this
repo) — see `COMPLETION-NOTES.md` in this same folder for what was actually built, the defects
found and fixed against the real Crystal-Reports PDF, and the hands-on JasperReports lessons that
came out of it (also folded into `DeepDiveLearnings/JASPERREPORT-7-0-3.MD` Part D for reuse on the
next report). The recon content below is kept as-is for historical reference — it was the accurate
pre-build state as of 2026-08-29 and its data-structure/query findings (§6) remained correct
throughout the build.

~~**Status: RECON ONLY. No JRXML has been built. No conversion work has started.**~~ *(superseded — see above)*
Per explicit owner instruction (2026-08-29): recon/deep-dive only until told to proceed with the
build. This file is the pre-build spec — everything a build would need, verified against real
sources (the PDF, programmatically, and the live local sandbox DB), not guessed.

**Source materials** (`C:\Projects\INPEX\sources\CrystalReports\R07.012\`):
- `crytsal report in pdf\R07.012 - FC Lifting Report (July 2025).pdf` — the only artifact
  showing the report's real layout (no `.rpt` Crystal source file exists anywhere under
  `C:\Projects\INPEX`, confirmed via a full-tree search).
- `queries\queries.sql` — 2 queries, one of which (the main data query) is **not sufficient as
  written** — see "Data structure" below.
- `output\` — empty.

Target: JasperReports 7.0.3, Standard JRXML format, per `DeepDiveLearnings/JASPERREPORT-7-0-3.MD`.

---

## 1. Page geometry (extracted via PyMuPDF, not estimated)

- **Page size: A3 Landscape — 1190.55 × 841.85 pt** (72dpi). This is `pageWidth="1191"
  pageHeight="842" orientation="Landscape"` in JRXML (round to nearest whole pt; verify against
  Studio's own A3-landscape preset which may differ by <1pt — confirm in Studio before finalizing).
- Content bounding box observed: x 22.65→1163.58, y 27.99→803.73.
  - Left margin ≈ 22.65pt (round 23)
  - Right margin ≈ 1190.55 − 1163.58 ≈ 27pt
  - Top margin ≈ 28pt
  - Bottom margin ≈ 841.85 − 803.73 ≈ 38pt

## 2. Logo

- Embedded raster image, bbox (22.65, 28.0)–(167.0, 102.55) → width ≈144.35pt, height ≈74.55pt.
- Source pixel size 236×124px @96dpi, DeviceRGB, no alpha mask.
- **Not yet extracted as a standalone file** — needs extracting from the PDF (`page.get_image_info`
  gave `xref=15`; can pull via `doc.extract_image(15)`) before it can be used as a Jasper
  `<image>` resource. Not done yet — recon only.

## 3. Fonts, sizes, colors — every distinct combo found in the PDF, by role

| Role | Font | Size | Color | Notes |
|---|---|---|---|---|
| Title "Lifting Report" | ArialBoldItalic | 21pt | `#000000` | bbox (522.8,28.0)-(660.4,51.5) — roughly centered, top-right of logo |
| Subtitle lines ("Field Condensate" / "(in US BBL at 60F)" / month) | ArialItalic | 12pt | `#000000` | 3 lines, centered under title |
| "Publish Date: ..." band | ArialBoldItalic | 9pt | `#FFFFFF` | on `#454087` fill |
| Column header row (all 14 columns) | ArialBoldItalic | 9pt | `#FFFFFF` | on `#454087` fill |
| Data cells, non-zero value | Arial | 8pt | `#000000` | |
| Data cells, **zero value** | Arial | 8pt | `#FFFFFF` | **deliberate — invisible on white background, a zero-suppression trick.** Needs a conditional expression (`$F{...} == 0 ? white : black`), not a static style. |
| "Total" row (label + all totals) | ArialBold | 8pt | `#000000` | bold, NOT italic — distinct from the header row style |
| Footnote disclaimer | ArialItalic | 10pt | `#000000` | single line, full width |
| Footer strip (refresh date / classification / page N of M) | ArialBoldItalic | 6pt | `#000000` | 3 separate text fields, left/center/right aligned respectively |

**⚠ Font risk, per `JASPERREPORT-7-0-3.MD` Rule 10:** this report uses Arial bold-italic in two
places (title 21pt, header row 9pt). Arial has no bold-italic PDF variant without a registered
font-extension JAR — the italic silently drops in PDF export with zero error shown. Two options,
to decide before building:
1. Register an Arial font-extension JAR so `isBold`+`isItalic` render correctly (closer visual
   fidelity to the original, more setup).
2. Substitute `DejaVu Sans` (bundled with JasperReports 7.0.3, renders bold-italic natively) —
   faster to stand up, but the font will not be pixel-identical to Arial (different letterforms/
   metrics), which conflicts with the "match the Crystal PDF exactly" requirement.

This is a real decision point, not something to silently pick — **flagging for the owner's call**
before the build starts.

## 4. Colors and lines

- Fill `#454087` (dark indigo/purple-blue) — used for the "Publish Date" band and the column
  header row. Only fill color found in the entire document (16 filled rects total).
- Border/stroke `#454087`, width 1.5pt — used around the header band area (2 occurrences).
- Grid lines `#D6D6D6` (light gray), width 1.0pt — table cell borders (462 line segments).

## 5. Layout structure (bands, mapped to JasperReports 7.0.3 concepts per the rules doc)

- **Title band**: logo (image) + "Lifting Report" title + 3 subtitle lines. Static, one-time.
- **Page header band** (repeats if the report ever spans >1 page — this sample is "Page 1 of 1"
  but the footer's `Page N of M` field implies pagination support must exist): "Publish Date"
  band (`#454087` fill) + the 14-column header row (same fill).
- **Detail band**: one row per `DAYTIME`, columns: Date, Production*, Inventory*, Lifted Qty,
  INPEX, TOTAL, OPIC, Osaka Gas, Kansai Electric, JERA, Toho Gas, Cargo ID, Vessel, Lifting
  Status. A special **"Opening Inventory"** row (label only + one Inventory value) precedes the
  first dated row — see Data Structure §2 below for its real source.
- **Summary/column-footer band**: "Total" row — sums for Production, Lifted Qty, INPEX, TOTAL
  (shows 0 in the sample — needs checking why), OPIC, Osaka Gas, Kansai Electric, JERA, Toho Gas.
- **Page footer band**: disclaimer footnote (from a DB lookup, not static text — see §3 below) +
  refresh-date/classification/page-count strip.

## 6. Data structure — confirmed live against the local sandbox DB, NOT the same as `queries.sql`

**`queries.sql`'s second query, as written, will NOT reproduce this report.** Confirmed via live
data (`TV_FC_LIFTING_REPORT`, a physical table, 470 rows):

1. **The table is not one-row-per-day.** On a non-lifting day there's exactly 1 row. On a lifting
   day there's **one row per participating customer**, all sharing the same `DAYTIME`/
   `CARGO_NAME`/`CARRIER_NAME`/`CARGO_STATUS`/`TOTAL_LIFTED_QTY`, each with its own `LIFTED_QTY`
   value identified by `COMPANY_NAME`/`COMPANY_CODE` on that row. Verified on `2025-07-09` (6
   rows: Osaka Gas, Kansai Electric, JERA, Toho Gas, INPEX, OPIC) — every `LIFTED_QTY` value
   matches the PDF's per-customer column exactly (21,144 / 9,666 / 9,666 / 5,920 / 3,383 /
   546,270, allowing for rounding).
2. **The report's fixed per-customer columns (INPEX/OPIC/Osaka Gas/Kansai Electric/JERA/Toho Gas)
   require a pivot** the current query doesn't do — e.g. `MAX(CASE WHEN COMPANY_CODE =
   'INPEX_ICHTHYS' THEN LIFTED_QTY END) AS INPEX_QTY` per customer, `GROUP BY DAYTIME`, plus a
   plain (non-grouped) passthrough for the days with no cargo at all. This pivot query does not
   exist yet in `queries.sql` and needs writing before any JasperReports `<field>` mapping is
   possible.
3. **`NAME_CPC_ICHTHYS`/`NAME_CHUBU_ELECTRIC_ICHTHYS`/etc.** are NOT company identifiers by name —
   they're legacy-named slot columns whose **stored value** is the current real display label
   (`NAME_CPC_ICHTHYS` = `'OPIC'`, `NAME_CHUBU_ELECTRIC_ICHTHYS` = `'JERA'`, confirmed live,
   identical on every row of the table including no-cargo days). These are the source for the
   report's column **header** text (dynamic/configurable, matching the disclaimer-text pattern
   below) — not per-row data values.
4. **"Opening Inventory" row** — confirmed: its value (323,715) exactly equals
   `PROD_CLOSING_BALANCE` for `2025-06-30` (the day before the report month starts). Needs its
   own small lookup query — `SELECT PROD_CLOSING_BALANCE FROM TV_FC_LIFTING_REPORT WHERE DAYTIME
   = (first day of report month) - 1` (verify this exact form once the real "first day of report
   month" parameter is defined) — this lookup is **not present** in `queries.sql` either.
5. **Disclaimer footnote** — sourced from `tv_ec_codes WHERE code_type='Z_REPORT_TEXT' AND
   code='LIQUIDS_INVENTORY_DISCLAIMER'` (query 1 in `queries.sql`, this one IS complete/correct as
   written) — confirms the footnote text is configurable in EC, not to be hardcoded as static
   text in the Jasper report.
6. **Unresolved, not yet checked:** why the PDF's "TOTAL" column total row shows `0` while INPEX's
   total (`1,720,992`) and the day totals visibly sum higher — need to check what `NAME_TOTAL_
   ICHTHYS`/a `TOTAL`-coded row actually represents before assuming it's a simple SUM(INPEX).
   Also not yet checked: whether `MONTH_FORECAST` and `PROD_FORECAST` map to any visible column
   in the PDF at all (neither appears to have an obvious counterpart in the visible report) —
   possible unused/forecast-only fields not needed for this specific report variant.

---

## What's still needed before a build can start

1. **Owner decision on the Arial bold-italic font risk** (§3 above) — extension JAR vs DejaVu Sans
   substitution.
2. **The corrected pivot query** for the main dataset (§6.2) — needs drafting and verifying
   against the PDF's exact numbers before it becomes the report's `<queryString>`.
3. **The Opening Inventory lookup query** (§6.4) — needs drafting.
4. **The logo image** needs extracting from the PDF as a standalone file for use as a Jasper
   image resource.
5. **The TOTAL column / row-0 discrepancy** (§6.6) needs investigating, not assumed.
6. **Local sandbox Jaspersoft Studio 7.0.3 availability** — not yet confirmed installed.

None of these have been started — this file is recon output only, per the owner's explicit
"don't start conversion work yet" instruction.
