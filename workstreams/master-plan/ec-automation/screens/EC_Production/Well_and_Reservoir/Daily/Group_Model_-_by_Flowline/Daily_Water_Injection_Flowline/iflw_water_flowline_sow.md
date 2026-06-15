# EC Screen N1 Edit Operation Test — Statement of Work (SOW)
**Project:** Woodside Pluto ECaaS — EC Web App System Test
**Task:** N1 daily-status grid edit + DB-verify automation
**Screen:** Daily Water Injection Flowline, by Flowline (EC Production > Daily > Group Model - by Flowline)
**Author:** Choong-Yin Lee / Claude Opus 4.8
**Date:** 2026-06-15
**Version:** 1.1 — COMPLETE (live 4/4, DB-verified against IFLW_DAY_STATUS, self-cleaning).
**Capability:** UPDATE-ONLY — the New/Delete toolbar is disabled (no record insert/delete on this screen,
by the business-domain nature); the suite tests the full edit of the measured value (set / change / clear).

---

## 1. REQUIREMENT

### 1.1 Objective
Automate edit-in-place data entry on the **Daily Water Injection Flowline, by Flowline** N1 status grid
and validate that an edited measured value **persists to the database** (not just the UI):
1. The date-range + 4-level cascade renders the pre-instantiated (flowline × day) row.
2. A measured cell edit is staged + saved.
3. The value is verified BOTH on-screen AND in `IFLW_DAY_STATUS` (DB ground truth).
4. The cell is restored to its original (NULL) state — no residue.

### 1.2 Scope
Water-injection flowline daily status (`IFLW_DAY_STATUS`, INJ_TYPE='WI'). Direct sibling of the
completed PFLW ("Daily Production Flowline, by Flowline") — shares the same grid component
(`daily_flowline_status:form`), so it reuses the N1 `daily_status_grid` (T2) + `DbVerify` verbatim.
Target cell: **C2 = On Strm[hr] = `ON_STREAM_HRS`** (unitless — no UI↔DB unit conversion).

### 1.3 Constraints
- **NEVER modify existing production/configuration data** beyond the single test cell, which is
  restored to its NULL original by the self-clean teardown.
- Target environment: local sandbox (`ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/`), user `sysadmin`.
- DB ground truth via oracledb thin (`EC_DB_DSN` default `localhost:1521/ORCL`).

### 1.4 Acceptance Criteria
| Operation | Pass Condition | Status |
|---|---|---|
| GRID LOAD | The cascade scope renders one flowline daily row | ✅ PASS (live 2026-06-15) |
| EDIT+PERSIST | On Strm[hr] = 18 shows on-screen AND in `IFLW_DAY_STATUS.ON_STREAM_HRS` | ✅ PASS |
| CLEANUP | Cell restored to NULL; DB-verified back to NULL (no residue) | ✅ PASS |

---

## 2. DESIGN

### 2.1 Screen model (verified live 2026-06-15)
Pattern **N1 — edit-in-place daily-status grid** (non-iframed; content in `dashboard.jsf?top=false`).

```
Navigator: From Date (G:0) + To Date (G:1, same day)
         → cascade  PU (G:2) → Area (G:3) → Facility Class 1 (G:4) → Flowline (G:5, leaf)
         → GO (button:form:B)
Grid:      daily_flowline_status:form:T_data  (one row = the chosen flowline's day)
Cell:      daily_flowline_status:form:T:{idx}:C2_in   (C2 = On Strm[hr] = ON_STREAM_HRS)
Save:      toolbar Save (menubar, execute=@all)
```

### 2.2 Working scope (data-bearing)
| Field | Value |
|---|---|
| Date | 2019-12-20 (9 WI flowlines have P rows that day) |
| PU / Area / Facility | P1 Production Unit / P1 Area / P1 Facility 1 |
| Flowline | **P1 F003 WI** (OV_FLOWLINE NAME; CODE `P1 F003`) |

⚠️ **Name trap (resolved):** a *dataless* `P1 0600 F003 WI` exists under "P1 Facility 0600". The
data-bearing flowline is `P1 F003 WI` under "P1 Facility 1" — select by exact name.

### 2.3 DB oracle
`IFLW_DAY_STATUS`, key `(OBJECT_ID, DAYTIME)`; `OBJECT_ID` resolved from `OV_FLOWLINE` by name.
Assert `ON_STREAM_HRS == 18` after save; restore to NULL and assert NULL after cleanup.

### 2.4 Deliverables (this bundle + RF suite)
- **RF suite:** `tests/EC_Production/Well_and_Reservoir/Daily/Group_Model_-_by_Flowline/daily_water_injection_flowline_status_edit.robot`
  (TC01–03) + `pageobjects/EC_Production/Well_and_Reservoir/Daily/Group_Model_-_by_Flowline/iflw_water_flowline_status_page.resource`
  (T3); reuses `daily_status_grid` (T2) + `DbVerify` — no new shared code.
- **Playwright prototype:** `playwright/ec_edit_iflw_water_flowline.py` (freestyle edit: set→change→clear, update-only).
- **Investigation:** `investigation/` recon scripts (data scope, injection-type, screen crack, grid cells).
- **Evidence:** `evidence/` screenshots from a full run.

---

## 3. RESULT
Live **4/4 PASS** (2026-06-15, headed). DB ground-truth confirmed `ON_STREAM_HRS` set 18 -> changed 24 ->
cleared to NULL in `IFLW_DAY_STATUS` (each step asserted), then restored to NULL. robocop clean; dryrun
4/4. Self-cleaning (0 residue).
