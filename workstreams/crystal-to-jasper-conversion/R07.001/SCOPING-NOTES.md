# R07.001 — Offshore Daily Operations Report — Scoping Notes (2026-08-30)

**Status: SCOPED, NOT BUILT.** This is an honest stop, not a silent gap — see rationale below.

## Why this wasn't attempted in the same session as R07.021-025
This report is dramatically larger and more heterogeneous than every other report in this
batch combined. R07.011-025 (15 reports) are each essentially ONE table (a daily grid, or a
single annual matrix) with at most one recap block. R07.001 is **7 pages** with roughly
**15-20 largely independent sections**, several of which have data-driven VARIABLE row/
paragraph counts (not a fixed shape that can be measured once and trusted) — building this
properly means treating it closer to "7 separate reports" in effort than "1 more report."

Attempting a rushed build now (at the tail end of a long unsupervised stretch) would mean
guessing at column boundaries and section shapes I have not actually measured — exactly the
failure mode the project's "no guessing" hard rule exists to prevent. Stopping to scope and
report back, rather than fabricating something low-quality, is the correct call per that rule
and per "no self-made shortcuts" (STOP rather than silently cut corners under time pressure).

## Full page-by-page recon (fresh run, `recon.py` — fixed a real bug along the way, see below)

**Page 1** — multiple stacked sections:
- HSE incident summary: CPF/FPSO × Injury/Environmental/Safety/Security events, with counts
  AND free-text comments per event (e.g. the ASV Medivac incident, HPU hydraulic oil leaks).
- Injury/Environmental counts table (CPF vs FPSO, Main facility vs Total).
- **Production, Internal Consumption & Losses**: ~13 metric rows (Well fluids to CPF w/wo MEG,
  CPF rich gas export, condensate rundown, fuel gas ×3, flare/venting ×3) × Daily/MTD/MTD
  Variance %/Short Term Forecast columns.
- **Production Quality**: gas composition mol% (C1/C2/C3/iC4/nC4/iC5/nC5/N2/CO2/C6+) for CPF
  rich gas export.
- **Gas Export Pipeline**: Offshore/Onshore × Avg Pressure/Avg Temp/H2S/H2O.
- **Inventory**: Field Condensate + GEP Rich Gas × Opening/Closing/Available Ullage/Days to
  Max Inventory.
- **Cargo**: Cargo ID/Vessel name/Status/Arrival/Departure (variable row count — one row per
  active cargo, e.g. "IC25-FC-022"/"Yuan Lan Wan").
- **Water and MEG**: 4 metrics (LP/HP MEG injected, FPSO produced water/water overboard) ×
  Daily/MTD.

**Page 2** — the well-grid: **30 wells** (BDC-1A-01 through BDC-5-05, plus Brewster/Plover
facilities) × MEG Injection (LP m³, HP m³) / Bottom Hole (Pressure kPag, Temp °C via Virtual
Flow Meter) / Well Head (Press kPag, Temp °C) / an "Available"+facility-name status pair per
well. This is the single densest section in the whole report.

**Page 3** — Production Risks for CPF: a **variable-row risk register** (Area/Tag/Description/
Work Order/Focal/Plan/Priority columns), each risk item carrying multi-line free-text
Description + "Mitigation:" + "LT Solution:" paragraphs. Row count is driven by how many open
risks exist, not fixed.

**Page 4** — appears to be a continuation table (dates like "03-08-2024", plus "Planned"/"OOS"/
"Comments"/"Estimated RTS" column headers found at the page boundary) — **not yet fully
parsed**, needs its own dedicated recon pass.

**Page 5** — Production Risks for FPSO (same shape as page 3's CPF version, more rows) +
**Consumables for CPF/FPSO** (Diesel/Helifuel/Lean MEG/Potable Water/TEG/Fresh MEG/H2S
Scavenger/pH Controller/Rich MEG/Sodium Hydroxide — different metric sets per facility — ×
Closing Volume/Filled-Bunkered Volume/Comments) + **Power Generation for CPF/FPSO** (Total MW
load, MW capacity available).

**Page 6** — CPF free-text narrative report: per-Author rows, each with HSE/Executive/
Production/Maintenance & Major Activities free-text paragraph sections (Comment/Comment Type
structure) — genuinely prose, not tabular data (e.g. "ERT Drill - Mass Casualty Helicopter
Crash Landing", "Daily Flaring: CPF LP flare: 1,023 m3 (baseline: 1,600)").

**Page 7** — FPSO version of page 6's narrative structure (same shape, different authors/
content).

## A real bug found and fixed during this scoping pass
The existing `recon.py` script crashed with `UnicodeEncodeError` on page 2 (a `▲` character in
the well-grid's status data, not representable in the Windows console's default `cp1252`
encoding) — this is WHY the previous session's `recon_full.txt` was missing page 1 and appeared
to stop mid-way. Fixed by running with `PYTHONIOENCODING=utf-8`; the complete 7-page text dump
now exists at `recon_fresh.txt` in this report's own folder. Future recon on this report should
use that environment variable (or write output via Python's own UTF-8 file handles) to avoid
losing pages again.

## Data deep-dive: the query manifest resolves most open questions (2026-08-30, later)
`queries/R07.001_OFF_DLY_OPS_Subqueries.sql` contains ~18 REAL, named, independently-queryable
sub-report queries — this is a goldmine for understanding the report's true structure, not just
its visual layout. Confirmed mapping (block name → real table/view → visual section):

| # | Query label | Table/view | Visual section |
|---|---|---|---|
| 1-2 | HSE (CPF/FPSO) | `RV_HSE` | Page 1 HSE incident summary |
| 3-4 | Persons On Board at Midnight (CPF/FPSO) | `RV_PERSONNEL_ONBOARD` | **CORRECTION (2026-08-31, during the block-by-block build): this IS present in the reference**, immediately below the HSE block (abs y=334-416 on page 1). Real data: CPF "Main facility"=117/"Total"=117, FPSO "Main facility"=141/"Total"=141 (JOB_CATEGORY values). The earlier "not visible" conclusion was wrong — it was a PDF-text-only scan that missed this because the table has no distinct section-title text of its own (it shares the page's visual flow directly under the HSE table); `get_drawings()` + word-position extraction during the actual build found it clearly. Lesson: a "not visible in a text-only scan" conclusion needs a `get_drawings()` cross-check before being treated as "absent from the design," not just trusted from one recon method. |
| 5 | Production, Internal Consumption & Losses | `ZV_HCA_DOR_STRM_ALLOC_DATA` | Page 1 — `REPORT_GROUP_CODE` drives 3 sub-groups (Production/Internal Consumption/Losses) within ONE query, not 3 separate ones |
| 6 | Production Quality | `ZV_HCA_STREAM_QUALITY` | Page 1 gas mol% table |
| 7 | Gas Export Pipeline | `RV_PIPE_DAY_STATUS` (code='GEP') | Page 1 |
| 8 | Inventory | `ZV_HCA_ONSHORE_INVENTORY` | Page 1 |
| 9 | Offtakes | `ZV_HCA_OFFTAKE_CARGO_INFO` | Page 1 "Cargo" table |
| 10 | Water and MEG | `ZV_HCA_DOR_STREAM_DATA` | Page 1 |
| 11 | Subsea Production | `RV_PWEL_DAY_STATUS` | Page 2 well-grid — **18 real per-well columns** confirmed (NAME/POOL_CODE/STATUS/ON_STREAM_HRS/AVG_CHOKE_SIZE/AVG_GAS_RATE/AVG_COND_RATE/AVG_WATER_RATE/EXT_GAS_RATE_1/EXT_COND_RATE_1/EXT_WAT_RATE_1/AVG_WH_PRESS/AVG_WH_TEMP/AVG_BH_PRESS/AVG_BH_TEMP/MEG_INJ_HP/MEG_INJ_LP/COMMENTS), plus Brewster/Plover pool-total columns computed via correlated subqueries that repeat the SAME value on every row of that pool — meaning the "Total" row per pool is a Crystal group-footer showing a MAX/first aggregate of an already-computed constant, not a live SUM in the report itself |
| 12 | Support Vessels | `RV_FCTY_DAY_VESSEL` | **Not visible in reference PDF** - same suppression note as #3-4 |
| 13-14 | Major Equipment Status (CPF/FPSO) | `RV_EQUIP_DOWNTIME` joined `RV_EQPM` | **Resolves Page 4** (previously "not yet parsed") — columns exactly match Page 4's Planned/OOS/Comments/Estimated RTS headers found earlier |
| 15-16 | Production Risks (CPF/FPSO) | `ZV_HCA_DOR_PROD_RISKS` | Pages 3 (CPF) / 5 (FPSO) risk registers |
| 17-18 | Consumables (CPF/FPSO) | `ZV_REP_DOR_CONSUMABLES_STATUS` | Page 5 |
| 19-20 | Power Generation (CPF/FPSO) | `RV_EQPM_POWER_DIST_EQPM` | Page 5 |
| 21-22 | Comments (CPF/FPSO) | `RV_OBJECT_ITEM_COMMENT` | Pages 6 (CPF) / 7 (FPSO) narrative reports |

**Implication for the block-by-block build:** each visual block maps to exactly one query, so
each JRXML sub-section can use the REAL field names from day one (matching this project's
established convention of real-but-deferred field names, e.g. `$F{NAME}`, `$F{AVG_GAS_RATE_SM3}`)
even though the query itself stays a placeholder/unwired until the data-query stage — this
removes most of the structural ambiguity the earlier PDF-only scoping pass had.

## Recommended path forward (not started, for the owner's call)
1. Treat this as its OWN multi-session effort, not a "finish it off" tail task — likely one
   page (or one section-group) per work session, with the same `get_drawings()` + word-level
   measurement rigor as R07.023-025.
2. Start with Page 1 (most tabular/mechanical of the 7 — fixed-shape KPI tables, only the
   Cargo section has a variable row count) as the first real build, since it's the least
   free-text-heavy and most similar in shape to reports already built.
3. The well-grid (Page 2) and the two risk registers (Pages 3/5) and the two narrative-report
   pages (Pages 6/7) each need their own dedicated recon+build pass — do NOT assume any of
   them share a column layout with each other or with the daily-grid reports already built.
4. Page 4 needs a fresh, focused recon pass (not yet understood) before any of the above.

**No JRXML/pom.xml/java harness was created for R07.001 this session** — only `recon_fresh.txt`　
(the corrected full-text dump) was added to the existing folder, which already had `recon.py`
and `recon_full.txt` (now superseded — kept, not deleted, since removing another session's
work without being asked isn't warranted here).
