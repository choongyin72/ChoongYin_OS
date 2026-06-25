# Pattern — Well Gas Component Analysis (WR.0010.01) — Phase 1 recon / design

_Phase 1 (live recon) for the WR.0010.01 build. Well-level sibling of PO.0020/PO.0019. Companion to the
Phase-0 SME `WELL-GAS-COMPONENT-ANALYSIS-SME.md` (PR #51). Read-only. Verified live 2026-06-17 (with
on-screen guidance from the user: Well Finder for scope + yellow=mandatory nav). See
[[feedback_finder_first_scope_resolution]]._

## Navigator (9 fields; only the YELLOW ones are mandatory)
Live-confirmed background colours: **mandatory = yellow `rgb(252,249,192)`**, optional = white.
| Group | Field | Mandatory? | Value |
|---|---|---|---|
| G:0 / G:1 | From / To Date | (date) | 2025-04-01 |
| G:2 | Production Unit | **yellow** | P1 Production Unit |
| G:3 | Area | **yellow** | P1 Area |
| G:4 | Facility Class 1 | **yellow** | P1 Facility 1 |
| G:5 | Well & Well Hookup | yellow* | _(leave empty)_ |
| G:6 | Well | yellow* | _(leave empty)_ |
| G:7 | Analysis Status | white (optional) | _(leave empty)_ |
| G:8 | Sampling Method | white (optional) | _(leave empty)_ |

*G:5/G:6 render yellow but the grid **loads without them** — filling them wrong (e.g. a Well name into
"Well & Well Hookup") over-filters to **0 rows** (the trap that cost the first recon). GO = `go_button:form:B`.

## Interaction — DIFFERS from stream/oil: select the analysis row
PU/Area/Facility + GO loads the **analysis HEADER grid** listing **all analyses valid as of the date**
(date-effective — e.g. 2011 analyses still appear in 2025). You then **SELECT the target analysis row**;
its components load in the `component_set` grid. (Stream/oil narrowed to ONE analysis via the Stream
dropdown, so no row-select was needed — this is the one extra step for wells.)
- `analysis:form:T:{row}:C{n}_in` columns: **C0=Analysis No, C1=Well Name, C2=datetime, C3=Valid From,
  C4=Analysis Status, C6=Sampling**. Resolve the target row by **Well Name + date** (or Analysis No).
- Target: **`P1 W260 GP Comp Gas`, Analysis No 1088, @ 2025-04-01** (Valid From 2025-04-01, status New, Spot)
  = header row `analysis:form:T:5:C0_in` in the recon (resolve by name, don't hardcode the index).

## Component grid + editable cell
- After selecting the analysis row: `component_set:form:T:{row}:C1_in` = **MOL_PCT** (editable; like the
  GAS stream PO.0020 — C1, NOT the C2/wt% that oil PO.0019 uses). C2..C5 unpopulated; sum row
  `component_set:form:T:ft_COMP_MOL_PCT_in` read-only.
- 9 components (CO2 · H2S · N2 · Methane · Ethane · Propane · i-Butane · n-Butane · C5+), all **0.1
  (synthetic; sum 0.90)** — accepted (realistic data = later). Methane = component row T:3 (by label).

## DB ground truth
View `DV_WELL_COMP_ANALYSIS`, `ANALYSIS_TYPE='WELL_GAS_COMP'`, key (OBJECT_ID, DAYTIME, COMPONENT_NO),
measure **MOL_PCT**. OBJECT_CODE `P1_W260_GP_COMP_GAS` ↔ WELL_VERSION NAME `P1 W260 GP Comp Gas`
(build resolves OID via `Object Id By Name WELL_VERSION 'P1 W260 GP Comp Gas'`). Reuse
**`component_value_should_be(view, oid, date, component_no, 'MOL_PCT', expected)`** — no DbVerify change.

## Build plan (Phase 2)
Thin T3 (clone the gas T3) with: nav = mandatory-only (Date + PU + Area + Facility Class 1) → GO; a new
**Select Analysis Row** keyword (find `analysis:form` row by Well Name + date, click it); component cell
`C1_in`/MOL_PCT; guard a 2nd component. Suite (3 TCs) — **TC03 reload + RE-SELECT the analysis row before
revert** (the composition 2nd-Save-won't-re-arm quirk + the row-select must be redone after reload). The
edit→Save→DB write gesture is identical to the proven PO.0020 (C1 mol%); the Phase-2 live run is the edit
proof (self-cleaning via reload+reselect+revert) — no separate ad-hoc probe (avoids the same-session-revert
dirty-cell trap seen on PO.0019).

## Recon scripts
`recon_wellcomp_db.py` (model + targets), `recon_wellcomp_screen.py` (nav-field count + go_button),
`recon_wellcomp_nav.py` (well scope via WELL_VERSION + dropdown options), `recon_wellcomp_grid2.py`
(mandatory-nav load + analysis-row select + component-cell map + yellow-mandatory detection).
