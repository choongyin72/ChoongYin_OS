# Pattern — Stream Oil Component Analysis (PO.0019) — Phase 1 recon / design

_Phase 1 (live recon + grid-cell mapping + de-risk probe) for the PO.0019 build. Sibling of the gas
analysis ([[pattern_composition_analysis_design]] / PO.0020). Companion to the Phase-0 SME doc
`STREAM-OIL-COMPONENT-ANALYSIS-SME.md` (PR #48). Read-only recon; the edit probe self-reverts.
Verified live 2026-06-17._

## Screen + navigator (same family as gas, ONE scope difference)
- Screen: **"Stream Oil Component Analysis"** (a.k.a. "Oil / Condensate Stream Component Analysis").
- 8-field navigator, GO = **`go_button:form:B`** (same as gas).
| Group | Field | Value (this target) |
|---|---|---|
| G:0 / G:1 | dates (`…da_input`) | 2023-06-01 |
| G:2 | Production Unit | `P1 Production Unit` |
| G:3 | Area | `P1 Area` |
| G:4 | **Facility Class 1** | **`P1 Facility Allocation`** ⚠️ NOT "P1 Facility 1" — the oil target sits under the *Allocation* facility (`OV_STREAM.OP_FCTY_1_CODE = P1_FCTY_ALLOCATION`); using P1 Facility 1 gives a dropdown without this stream |
| G:5 | Stream | `P1 Alloc S001 M OIL` |
| G:6 | Analysis Status | **`Approved`** (`*New` → empty grid) |
| G:7 | Sampling Method | **`*Spot`** |

## The editable cell — DIFFERENT column than gas
Two grids (header `analysis:form` + component grid). The component grid cells are
`component_set:form:T:{row}:C{n}_in`, BUT:
- **Gas (PO.0020): mol% = `C1_in`.** Oil: `C1_in` (mol%) is **EMPTY**.
- **Oil (PO.0019): the populated, editable measure = `C2_in` = WT_PCT.** ✅ DB-PROVEN.
- C3/C4/C5 unpopulated; sum row `component_set:form:T:ft_COMP_WT_PCT_in` (read-only) = 1.00.
- Component row order (resolve by LABEL, never hardcode index): Nitrogen(T:0) · Carbon Dioxide(T:1) ·
  **Methane(T:2)** · Ethane(T:3) · Propane(T:4) · i-Butane(T:5) · n-Butane(T:6) · i-Pentane(T:7) ·
  n-Pentane(T:8) · Hexane(T:9) · C7+(T:10) · C5+(T:11). (Methane=T:2 here, vs T:3 on gas — order differs.)

## DB ground truth
- View `DV_STRM_COMP_ANALYSIS`, `ANALYSIS_TYPE='STRM_OIL_COMP'`, key (OBJECT_ID, DAYTIME, COMPONENT_NO);
  **measure = `WT_PCT`** (MOL_PCT NULL for oil). OBJECT_CODE `P1 ALLOC S001 OIL` ↔ OV_STREAM NAME
  `P1 Alloc S001 M OIL` (build resolves OID via `Object Id By Name OV_STREAM 'P1 Alloc S001 M OIL'`).
- Reuse the existing **`component_value_should_be(view, oid, date, component_no, 'WT_PCT', expected)`** —
  **no DbVerify change → no R12 canary.**
- ⚠️ **Synthetic data (accepted by user 2026-06-17):** every component wt% ≈ 0.1 (sum 1.00, not 100). The
  edit→Save→DB→revert gesture is fully valid on it (proves the write path); realistic data is a later
  enhancement.

## De-risk probe result (DB-PROVEN gesture)
Edit Methane `C2_in` (wt%) 0.1 → **0.2** → Save → **`DV_STRM_COMP_ANALYSIS.WT_PCT` (COMPONENT_NO=C1) = 0.2**;
guard Ethane (C2) wt% **unchanged at 0.1** = Save persisted only the edited component (no normalize-on-save).
- ⚠️ **Build note (carry into TC03):** the **revert Save will NOT re-arm in the same session** after the
  first commit — the suite MUST **reload (re-GO) before the revert edit**, exactly like the gas T3's
  `Reload And Find Target Component`. (Two probe reverts failed for this reason; both dirty cells were
  cleaned via fresh-session restores — see recon scripts. Fresh-session edit+Save is reliable.)

## Build plan (Phase 2)
Thin T3 `po0019_stream_oil_comp_analysis_page.resource` (clone the gas T3; Variables: SCOPE_FACILITY=
`P1 Facility Allocation`, TARGET_STREAM=`P1 Alloc S001 M OIL`, SCOPE_DATE=2023-06-01, TARGET_COMPONENT_LABEL=
Methane, TARGET_COMPONENT_NO=C1, **COMP_COLUMN=WT_PCT**, **cell suffix `C2_in`**, GUARD C2/Ethane) + suite
(3 TCs, reload-before-revert). Reuses `component_value_should_be` verbatim. → live headed 3/3 DB-verified.

## Recon scripts (reproducible)
`recon_oilcomp_sme.py` (model), `recon_oilcomp_target2.py` (navigable-target search), `recon_oilcomp_scope.py`
(facility scope), `recon_oilcomp_grid2.py` (grid map), `recon_oilcomp_probe.py` (wt% gesture proof),
`recon_oilcomp_check.py` + `recon_oilcomp_restore.py`/`restore2.py` (dirty-cell self-clean evidence).
