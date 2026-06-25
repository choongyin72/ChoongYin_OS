# Pattern — Stream Gas Component Analysis (PO.0020) — Phase 1 recon / design

_Phase 1 (live recon + grid-cell mapping) for the composition build. Read-only; no DB writes, no Save.
Companion to the Phase-0 SME doc `DeepDiveLearnings/business-domains/COMPONENT-ANALYSIS-SME.md`
(PR #40, open — content reference only, R11). Re-verified live 2026-06-17._

## What the screen is
**Stream Gas Component Analysis (PO.0020)** — captures a gas stream's **per-component composition**
(`MOL_PCT` to C6+) from lab/analyser samples. Lives in the **Laboratory → Sample Analysis** area.
Unlike the daily-status grids (one row per object×day), composition is **one row per COMPONENT**, so it
is a NEW pattern grain (not a `daily_status_grid` reuse).

## Navigator model (8 fields) — verified live
| Group | Field | Set to |
|---|---|---|
| G:0 | `nav:form:G:0:R:1:C:0:da_input` (date "from") | scope date |
| G:1 | `nav:form:G:1:R:1:C:0:da_input` (date "to") | scope date |
| G:2 | Production Unit (dd) | `P1 Production Unit` |
| G:3 | Area (dd) | `P1 Area` |
| G:4 | Facility Class 1 (dd) | `P1 Facility 1` |
| G:5 | Stream (dd) | `P1 S038_AGA3_1985_AGA8_Y_1` |
| G:6 | **Analysis Status** (dd) | **`Approved`** |
| G:7 | **Sampling Method** (dd) | **`*Spot`** |

- **GO button = `go_button:form:B`** (NOT the daily-grid `button:form:B`).
- **Grid-load condition (the key gotcha):** the grid is EMPTY unless G:6/G:7 MATCH the real analysis.
  `*New` (first option) → empty grid. For this target, **`Approved` + `*Spot`** loads it.
- PU/Area/Facility resolve via **Stream Finder** (`navButton:form:B`); on a flaky empty scrape, fall
  back to the known P1 scope above.

## Grids — two of them
1. **`analysis:form:T:0:*`** — the analysis header row (mostly read-only):
   C0=analysis no (`1000`), C1=stream name, C2=datetime, **C3_da_input**=date (editable),
   **C4_dd_input**=Analysis Status (`Approved`, editable), C6=sampling (`Spot`), C23=`50.62` (ro agg).
2. **`component_set:form:T:{row}:C1_in`** — the COMPONENT grid; **C1_in = the editable `MOL_PCT` cell**
   (not read-only). C2..C5 unpopulated. Sum row read-only: `component_set:form:T:ft_COMP_MOL_PCT_in`
   = `100.00` (+ `ft_COMP_WT_PCT_in`, `ft_COMP_MOL_ENERGY_in`).

### Component row order (set order) → DB COMPONENT_NO  (verified live vs DB)
| UI row | UI label | MOL_PCT | DB COMPONENT_NO |
|---|---|---|---|
| T:0 | Nitrogen | 1.84 | N2 |
| T:1 | Carbon Dioxide | 0.00 | CO2 |
| T:2 | Hydrogen Sulfide | 2.60 | H2S |
| T:3 | **Methane** | **70.68** | **C1** |
| T:4 | Ethane | 14.14 | C2 |
| T:5 | Propane | 6.74 | C3 |
| T:6 | i-Butane | 0.81 | IC4 |
| T:7 | n-Butane | 1.90 | NC4 |
| T:8 | i-Pentane | 0.38 | IC5 |
| T:9 | n-Pentane | 0.43 | NC5 |
| T:10 | Hexane | 0.26 | C6 |
| T:11 | C7+ | 0.22 | C7+ |

Rows are NOT in DB-COMPONENT_NO order — resolve the row by UI label (or DB COMPONENT_NO via this map),
never hardcode blindly. (Methane=T:3 here.)

## Live target (sandbox)
- Stream `P1 S038_AGA3_1985_AGA8_Y_1` @ **2011-11-01**, SAMPLING_METHOD=`SPOT`, RECORD_STATUS=`P`
  (Preliminary), 12 gas components, MOL_PCT sums to **100**. OBJECT_ID `96D7FD4F6CB90217E053020011AC1940`.
- Chosen because: Preliminary (editable, not a one-off), realistic full composition, sums to 100 (no
  Normalize needed). The sandbox has only ONE Approved gas analysis; the rest are Preliminary.

## DB ground truth
- View **`DV_STRM_COMP_ANALYSIS`**, keyed `(OBJECT_ID, DAYTIME, COMPONENT_NO)`; columns
  `MOL_PCT`/`WT_PCT`/`MOL_WT`/`DENSITY`/`RECORD_STATUS`/`ANALYSIS_TYPE`/`SAMPLING_METHOD`.
- ⚠️ **Navigator "Analysis Status" (Approved/Rejected/Information/*New) is a UI workflow state, NOT the
  DB `RECORD_STATUS` (P/A).** This Preliminary (`P`) analysis displays under the **Approved** filter with
  the header C4_dd showing `Approved`. So filter by the UI status that loads it, verify by the DB column.

## Build plan (Phases 2–5, when authorised)
- **Phase 2 — DbVerify:** new append-only `component_value_should_be(view, object_id, daytime,
  component_no, column, expected)` filtering `COMPONENT_NO`; back up DbVerify.py first + R12 canary
  (dryrun a consumer + 1 random sibling).
- **Phase 3 — T3 + suite:** thin T3 (8-field nav + `go_button:form:B` + the component grid) + a 3-TC
  suite. **R10:** check the New/Delete toolbar enabled-state before labelling the gesture — the edit
  test is UPDATE only.
- **Phase 4 — live + verify + self-clean:** edit Methane mol% (T:3, 70.68 → a sentinel within
  98–102%) → Save → assert `DV_STRM_COMP_ANALYSIS.MOL_PCT` for `COMPONENT_NO='C1'`; **guard
  normalize-on-save** by asserting Ethane (`C2`) stays 14.14; revert to 70.68. Do NOT click
  Normalize / Mol→Wt (they recalc the whole set).
- **Phase 5 — package:** registry + scorecard rows → PR.

## Reproducible recon
- `tmp/scripts/recon_comp_target.py` — lock a clean target (status/sampling/components).
- `tmp/scripts/recon_comp_molpct.py` — which gas analyses have populated MOL_PCT.
- `tmp/scripts/recon_comp_stream.py` — OV_STREAM code/name for Stream Finder.
- `tmp/scripts/recon_comp_grid2.py` — load the grid (iterate Analysis Status until non-empty) + dump all
  grid inputs. Output: `tmp/recon_comp/grid2.json`.
