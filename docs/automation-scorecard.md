# EC Automation Scorecard
_Last updated: 2026-06-15_

## N-Series Patterns (Production Data Interaction)

| Pattern | Variant | Object Type | Status | Notes | Date |
|---------|---------|-------------|--------|-------|------|
| N1 | Daily status edit-in-place | PWEL (WR.0001) | ✅ Live 3/3 | Reference impl | - |
| N1 | Daily status edit-in-place | STRM (PO.0002) | ✅ Live 3/3 | | - |
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
