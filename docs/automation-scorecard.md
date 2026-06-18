# EC Automation Scorecard
_Last updated: 2026-06-15_

## N-Series Patterns (Production Data Interaction)

| Pattern | Variant | Object Type | Status | Notes | Date |
|---------|---------|-------------|--------|-------|------|
| N1 | Daily status edit-in-place | PWEL (WR.0001) | ✅ Live 3/3 | Reference impl | - |
| N1 | Daily status edit-in-place | STRM (PO.0002) | ✅ Live 3/3 | | - |
| N1 | Daily status edit-in-place | STRM-OIL (PO.0001) | ✅ Live 3/3 | Sibling of gas stream; "Oil"=generic-EC name for Pluto "Daily Liquid Stream Status"; C5=GRS_VOL; scope P1 @ 2023-01-01 (P1 Cond); reuses T2 verbatim (no shared-file change) | 16 Jun |
| N1 | Daily status edit-in-place | STRM-WAT (PO.0003) | ✅ Live 3/3 | Sibling of gas/oil stream; Daily Water Stream Status; C3=GRS_VOL; scope P1 @ 2023-01-01 (P1 S087); reuses T2 verbatim (no shared-file change); stacked on PR #35 | 17 Jun |
| N1 | Daily status edit-in-place | STRM-ELE (PO.0066) | ✅ Live 3/3 | Sibling; Daily Electrical Stream Status; **C2=POWER_CONSUMPTION** (no volume — electrical); scope P1 @ 2011-01-01 (P1 S046); reuses T2 verbatim (no shared-file change); stacked on PR #36 | 17 Jun |
| N1 | Daily status edit-in-place | TANK-VCF (PO.0005.02) | ✅ Live 3/3 | TANK variant; Daily Tank Status - VCF Calc; grid `dip_table:form`; **C4=Liquid Dip → DV_TANK_DAY_DIP_STATUS.LIQUID_DIP_LEVEL** (view, no base table); name is an INPUT (C1) so row-find by C1 value, not textContent; save triggers VCF recalc; OV_TANK; scope P1 @ 2011-01-01 (P1 T006); reuses T2 verbatim (no shared-file change) | 17 Jun |
| N1 | Daily status edit-in-place | IWEL | ✅ Live 3/3 | | - |
| N1 | Daily status edit-in-place | EQPM | ✅ Live 3/3 | Non-iframed; C4=AVG_PRESS | 14 Jun |
| N1 | Sub-daily status edit | PWEL | ✅ Live 3/3 | Datetime-keyed PK; UI↔DB unit conversion (~14.5x pressure) | 14 Jun |
| N1 | Daily status edit-in-place | PFLW (flowline) | ✅ Live 3/3 | Date-range nav (From+To); 4-level cascade; ON_STREAM_HRS unitless | 15 Jun |
| N1 | Sub-daily status edit | STRM | ✅ Live 3/3 | Datetime-keyed PK; GRS_VOL unitless; doc errors fixed (R7) | 15 Jun |
| N1 | Daily status edit (**UPDATE-only**) | IFLW (water inj flowline) | ✅ Live 4/4 | New/Delete toolbar DISABLED (no record insert/delete — business-domain nature); suite edits the value set/change/clear (clear=update-to-null); sibling of PFLW; IFLW_DAY_STATUS; C2=ON_STREAM_HRS; menu-mirrored path; Bank-style bundle | 15 Jun |
| N1 | Daily status edit (**UPDATE-only**) | GIFLW (gas inj flowline) | ✅ Live 4/4 | Sibling of WI (same grid); IFLW_DAY_STATUS INJ_TYPE=GI; P1 F004 GI; set/change/clear; menu-mirrored path; Bank-style bundle; **stacked on PR #24** | 15 Jun |
| N1 | Monthly status edit | PWEL | ⏸ Parked | Sparse data (13 rows), poor target | 14 Jun |
| N3 | Status process P→V | HA.0001 Daily | ✅ Live 2/2 | Dual DB oracle: ROWS_UPDATED + RECORD_STATUS count | 14 Jun |
| N3 | Status process V→A | HA.0001 Daily | ⏸ Parked | STIM_DAY_VALUE empty (0 rows); WELL_FLUID_ANALYSIS needs WHERE vars + data/SME — next: seed data | 15 Jun |
| N3 | Status process V→A | HA.0001 Monthly | 🔵 Build-ready | Thin new T3 for Monthly Data Status Processes screen | 14 Jun |
| N3 | Status process →A (month) | Monthly Data Status Processes (P1_FwdUpdPar1) | 🔵 Built, dryrun-green, live GATED | Screen model verified live (single Date G:0 + Process G:1); target IWEL_DAY_STATUS 19,659 P rows (data EXISTS); suite `monthly_status_process_run.robot` + thin T3; live behind `--variable LIVE_OK:yes` (no-WHERE → large reversible mutation; confirm blast radius + oracle grain on first observed run) | 15 Jun |
| N1 | Composition edit (per-component) | STRM-GAS-COMP (PO.0020) | ✅ Live 3/3 | NEW pattern: per-COMPONENT rows (not object×day); 8-field nav + `go_button:form:B`; grid loads on Analysis Status=Approved + Sampling=*Spot; edit Methane MOL_PCT (COMPONENT_NO=C1) → `DV_STRM_COMP_ANALYSIS`; Ethane(C2) guard proves no normalize-on-save; new append-only DbVerify `component_value_should_be`; target P1 S038_AGA3_1985_AGA8_Y_1 @ 2011-11-01 | 17 Jun |
| N1 | Composition edit (per-component) | STRM-OIL-COMP (PO.0019) | ✅ Live 3/3 | Oil/condensate sibling of PO.0020; edits **WT_PCT** (cell `C2_in`; oil's C1=mol% empty); Facility Class 1=**P1 Facility Allocation** (not P1 Facility 1); target P1 Alloc S001 M OIL @ 2023-06-01; reuses `component_value_should_be` (col=WT_PCT) — no DbVerify change/no canary; Ethane(C2) guard; TC03 reload-before-revert (2nd Save won't re-arm same session); synthetic wt% data (accepted; realistic=later) | 17 Jun |
| N1 | Composition edit (per-component) | WELL-GAS-COMP (WR.0010.01) | ✅ Live 3/3 | Well-level gas-comp sibling of PO.0020; mandatory (yellow) nav only = Date+PU+Area+Facility → GO; **NEW: SELECT the analysis row** in the header grid (lists all date-valid analyses) before components load; edit Methane MOL_PCT (C1, cell `C1_in` like gas) → `DV_WELL_COMP_ANALYSIS` (ANALYSIS_TYPE=WELL_GAS_COMP); Ethane(C2) guard; reuses `component_value_should_be` (no DbVerify change/no canary); name source WELL_VERSION; TC03 reload+RE-SELECT before revert; target P1 W260 GP Comp Gas @ 2025-04-01 (synthetic 0.1) | 17 Jun |

### Key Learnings
- **UI↔DB unit conversion**: UI(psi) ↔ DB(bar), factor ~14.5038. Naive "DB == typed" oracle fails on pressure/rate cols.
- **Sub-daily PK**: PWEL_SUB_DAY_STATUS keyed on (OBJECT_ID, DAYTIME[+time], SUMMER_TIME) — not TRUNC(date). Needs datetime-keyed DbVerify.
- **ec-worker**: Must be running (overlay 12); scheduler STANDBY on front-end nodes. ORA-06569 = empty data scope, not mechanism failure.
- **Data recovery**: Oracle Flashback AS OF TIMESTAMP used successfully for 192-cell restore.

---

## Section Coverage (Screen Automation)

| Section | Screens | Status | Notes |
|---------|---------|--------|-------|
| Basic Objects | 12/12 | ✅ Complete | Reference IUD suite |
| Financial Objects | 15/15 | ✅ Complete | All suites present (validated 2026-06-15) |
| Commercial Objects | ~11 screens | 🟡 Mostly complete | Sub Field parked |
| Account Mapping | 14/14 | ✅ Complete | Financial; unparked after start-date discovery |
| MIME Type Mapping | TV | ✅ Complete | Table-class/TV, both frameworks |
| Equipment | OV | ✅ Complete | 2nd OV screen |
| Language | IUD | ✅ Complete | 2nd Table-class |
| Dispatching Objects — slice 1 | 24/24 | ✅ Complete | 6 BU-gated OV-GM screens |
| Dispatching Objects — slice 2 | Nomination (TV) + Meter (popup) | ✅ Live 4/4 | Pipeline parked |
| Contract Objects | Contract Area (OV-GM, BU-gated) | ✅ Live 4/4 (2026-06-18) | 1st Contract Objects screen; built by ec-object-iud-builder; sibling of Transport System |
| ECIS Excel Upload | End-to-end | ✅ Complete | Own interface + schedule, ran live |
| Assets | Recon | ✅ Scanned | Registry complete |

---

## Framework Health

| Item | Status | Notes |
|------|--------|-------|
| robocop lint | ✅ Clean | 43→2 warnings after health pass |
| T3 Open-Screen promotion | ✅ Done | Shared keywords adopted |
| Dynamic test data | ✅ Refactored | |
| maximize-browser + expand-screen | ✅ Shared | Adopted across all suites |
| WR.0001 canary | ✅ Running | Used as regression check after each new suite |
| DB restore / teardown | ✅ Pattern established | All suites self-cleaning |

---

## Parked Items (Resume Backlog)

| Item | Reason | Next step |
|------|--------|-----------|
| N1 Monthly PWEL | Sparse data | Find a month with adequate PWEL_MTH_STATUS rows |
| N3 V→A Daily | STIM_DAY_VALUE empty (0 rows); WELL_FLUID_ANALYSIS needs WHERE_FORMULA var resolution + seeded data | Seed STIM_DAY_VALUE provisional rows or get SME confirmation on Analysis class→physical-table |
| N3 V→A Monthly | Build-ready | Thin new T3 for Monthly Data Status Processes screen |
| Dispatching Pipeline | Not attempted | Resume from slice 2 checkpoint |
| ~~Financial Objects (3 parked)~~ | Closed as stale — all 15 FO suites present (validated 2026-06-15) | — |
| Commercial Sub Field | Not attempted | |
