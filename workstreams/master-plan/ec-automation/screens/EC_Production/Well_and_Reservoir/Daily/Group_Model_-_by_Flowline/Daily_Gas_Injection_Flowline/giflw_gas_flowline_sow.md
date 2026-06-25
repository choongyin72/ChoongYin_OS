# EC Screen N1 Edit Operation Test — Statement of Work (SOW)
**Project:** Woodside Pluto ECaaS — EC Web App System Test
**Screen:** Daily Gas Injection Flowline, by Flowline (EC Production > Well and Reservoir > Daily > Group Model - by Flowline)
**Author:** Choong-Yin Lee / Claude Opus 4.8
**Date:** 2026-06-15
**Version:** 1.0 — COMPLETE (live 4/4, DB-verified against IFLW_DAY_STATUS, self-cleaning)
**Capability:** UPDATE-ONLY — New/Delete toolbar disabled (no record insert/delete, by the business-domain
nature); the suite tests the full edit of the measured value (set / change / clear).

---

## 1. REQUIREMENT
Automate edit-in-place data entry on the **Daily Gas Injection Flowline, by Flowline** N1 status grid and
validate that an edited measured value **persists to the database** (DB ground truth, not just the UI).
Gas-injection flowline rows live in `IFLW_DAY_STATUS` with `INJ_TYPE='GI'`. Sibling of the
Water-Injection / Production flowline screens (same grid component) — reuses `daily_status_grid` (T2) +
`DbVerify` verbatim. Target cell: **C2 = On Strm[hr] = `ON_STREAM_HRS`** (unitless).

### Acceptance Criteria
| Operation | Pass Condition | Status |
|---|---|---|
| GRID LOAD | the cascade scope renders one flowline daily row | ✅ PASS (live 2026-06-15) |
| SET | On Strm[hr]=18 shows on-screen AND in `IFLW_DAY_STATUS.ON_STREAM_HRS` | ✅ PASS |
| CHANGE | value changed to 24 and persisted | ✅ PASS |
| CLEAR | cell cleared → DB column NULL (update-to-null, not a record delete) | ✅ PASS |
| CLEANUP | cell restored to NULL; DB-verified (no residue) | ✅ PASS |

## 2. DESIGN
Pattern **N1 — edit-in-place daily-status grid** (non-iframed). Nav: From/To date (G:0/G:1) → cascade
PU(G:2) → Area(G:3) → Facility Class 1(G:4) → Flowline(G:5) → GO `button:form:B`. Grid
`daily_flowline_status:form:T_data`; cell `…:T:{idx}:C2_in`. **UPDATE-ONLY** (New/Delete disabled).

### Working scope (data-bearing, verified)
| Field | Value |
|---|---|
| Date | 2019-12-20 (6 GI flowlines have P rows that day) |
| PU / Area / Facility | P1 Production Unit / P1 Area / P1 Facility 1 |
| Flowline | **P1 F004 GI** (OV_FLOWLINE NAME; CODE `P1 F004`) |

### Deliverables
- **RF suite:** `tests/EC_Production/Well_and_Reservoir/Daily/Group_Model_-_by_Flowline/daily_gas_injection_flowline_status_edit.robot`
  + `pageobjects/EC_Production/Well_and_Reservoir/Daily/Group_Model_-_by_Flowline/giflw_gas_flowline_status_page.resource` (T3);
  reuses `daily_status_grid` (T2, incl. `Clear Daily Status Cell` from PR #24) + `DbVerify` — no new shared code.
- **Playwright prototype:** `playwright/ec_edit_giflw_gas_flowline.py` (freestyle set→change→clear, update-only).
- **Investigation:** `investigation/` recon scripts (GI data scope + screen crack).
- **Evidence:** `evidence/` — 01_grid_loaded / 02_value_set / 03_value_changed / 04_value_cleared.

## 3. RESULT
Live **4/4 PASS** (2026-06-15). DB-verified set 18 → change 24 → clear NULL in `IFLW_DAY_STATUS`;
self-cleaning. robocop clean; dryrun green. **Stacked on PR #24** (uses its `Clear Daily Status Cell`).
