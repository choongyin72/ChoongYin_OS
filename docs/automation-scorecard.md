# EC Automation Scorecard
_Last updated: 2026-06-14_

## N-Series Patterns (Production Data Interaction)

| Pattern | Variant | Object Type | Status | Notes | Date |
|---------|---------|-------------|--------|-------|------|
| N1 | Daily status edit-in-place | PWEL (WR.0001) | ✅ Live 3/3 | Reference impl | - |
| N1 | Daily status edit-in-place | STRM (PO.0002) | ✅ Live 3/3 | | - |
| N1 | Daily status edit-in-place | IWEL | ✅ Live 3/3 | | - |
| N1 | Daily status edit-in-place | EQPM | ✅ Live 3/3 | Non-iframed; C4=AVG_PRESS | 14 Jun |
| N1 | Sub-daily status edit | PWEL | ✅ Live 3/3 | Datetime-keyed PK; UI↔DB unit conversion (~14.5x pressure) | 14 Jun |
| N1 | Monthly status edit | PWEL | ⏸ Parked | Sparse data (13 rows), poor target | 14 Jun |
| N3 | Status process P→V | HA.0001 Daily | ✅ Live 2/2 | Dual DB oracle: ROWS_UPDATED + RECORD_STATUS count | 14 Jun |
| N3 | Status process V→A | HA.0001 Daily + Monthly | 🔵 Build-ready | Chain proven safe; monthly-approve on separate screen | 14 Jun |

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
| Financial Objects | ~11 screens | 🟡 Mostly complete | 3 parked |
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
| N3 V→A Daily | Build-ready | Clone N3 P→V suite with V→A process name |
| N3 V→A Monthly | Build-ready | Thin new T3 for Monthly Data Status Processes screen |
| Dispatching Pipeline | Not attempted | Resume from slice 2 checkpoint |
| Financial Objects (3 parked) | Unknown blockers | Investigate per-screen |
| Commercial Sub Field | Not attempted | |
