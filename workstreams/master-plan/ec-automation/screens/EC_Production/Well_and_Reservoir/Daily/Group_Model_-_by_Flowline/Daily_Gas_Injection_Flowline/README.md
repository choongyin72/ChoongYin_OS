# Daily Gas Injection Flowline, by Flowline — N1 edit (UPDATE-only)

Edit-in-place daily-status automation for the EC **Daily Gas Injection Flowline, by Flowline** screen
(EC Production → Well and Reservoir → Daily → Group Model - by Flowline). N1 daily-status-grid for
gas-injection flowlines (`IFLW_DAY_STATUS`, `INJ_TYPE='GI'`). Sibling of the Water-Injection / Production
flowline screens — same grid component, so the RF suite reuses `daily_status_grid` (T2) + `DbVerify`.

⚠️ **UPDATE-ONLY screen:** New (insert) / Delete toolbar icons are **disabled** — the daily row is
pre-instantiated by EC batch processes; no record insert/delete (by the business-domain nature). The
suite exercises the full edit: **set → change → clear** the value (clear = update to null, not a delete).

## Two parts
1. **RF suite:**
   - T3: `pageobjects/EC_Production/Well_and_Reservoir/Daily/Group_Model_-_by_Flowline/giflw_gas_flowline_status_page.resource`
   - Suite: `tests/EC_Production/Well_and_Reservoir/Daily/Group_Model_-_by_Flowline/daily_gas_injection_flowline_status_edit.robot`
2. **Playwright bundle** (this folder): `giflw_gas_flowline_sow.md`, `playwright/ec_edit_giflw_gas_flowline.py`,
   `investigation/`, `evidence/` (01_grid_loaded / 02_value_set / 03_value_changed / 04_value_cleared).

## Run
```bash
# RF suite (from ec-automation/), headed + watchable (EC_SLOWMO from PR #26)
EC_HEADLESS=false EC_SLOWMO=700ms robot --outputdir results tests/EC_Production/Well_and_Reservoir/Daily/Group_Model_-_by_Flowline/daily_gas_injection_flowline_status_edit.robot

# Playwright prototype (from this folder); EC_HOLD=<s> pauses per step
EC_HEADED=1 EC_HOLD=6 py -X utf8 playwright/ec_edit_giflw_gas_flowline.py
```

## Scope + oracle
- Scope: **2019-12-20** · P1 Production Unit → P1 Area → P1 Facility 1 → **P1 F004 GI**. Cell **C2 = On Strm[hr] = `ON_STREAM_HRS`** (unitless).
- DB ground truth: `IFLW_DAY_STATUS.(OBJECT_ID, DAYTIME)` (INJ_TYPE='GI'); set 18 → change 24 → clear (→NULL), each verified.

Status: **live 4/4 PASS** (2026-06-15), DB-verified, self-cleaning, robocop clean. **Stacked on PR #24.**
