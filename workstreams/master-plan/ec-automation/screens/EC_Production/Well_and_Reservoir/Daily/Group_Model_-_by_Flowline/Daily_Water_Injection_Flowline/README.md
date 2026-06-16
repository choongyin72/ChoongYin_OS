# Daily Water Injection Flowline, by Flowline — N1 edit (UPDATE-only)

Edit-in-place daily-status automation for the EC **Daily Water Injection Flowline, by Flowline** screen
(EC Production → Well and Reservoir → Daily → Group Model - by Flowline). N1 daily-status-grid pattern
for water-injection flowlines (`IFLW_DAY_STATUS`). Direct sibling of PFLW — same grid component, so the
RF suite reuses `daily_status_grid` (T2) + `DbVerify` verbatim.

⚠️ **UPDATE-ONLY screen:** the New (insert) and Delete toolbar icons are **disabled** — by the nature of
this business domain the daily row is pre-instantiated by EC batch processes; the screen does NOT create
or delete records, you only EDIT the measured values. (Contrast the master-data IUD screens, e.g. Bank.)
So the suite exercises the full edit capability: **set → change → clear** the value (clear = update to
null, NOT a record delete).

## Two parts (per the project convention)
1. **RF suite** (the productised test) — runs from the project root:
   - T3: `pageobjects/EC_Production/Well_and_Reservoir/Daily/Group_Model_-_by_Flowline/iflw_water_flowline_status_page.resource`
   - Suite: `tests/EC_Production/Well_and_Reservoir/Daily/Group_Model_-_by_Flowline/daily_water_injection_flowline_status_edit.robot`
2. **Playwright bundle** (this folder, freestyle prototype + discovery trail + spec):
   - `iflw_water_flowline_sow.md` — statement of work
   - `playwright/ec_edit_iflw_water_flowline.py` — standalone set→change→clear prototype (DB-verified)
   - `investigation/` — recon scripts (data scope, injection type, screen crack, grid-cell map)
   - `evidence/` — screenshots (`01_grid_loaded`, `02_value_set`, `03_value_changed`, `04_value_cleared`)

## Run

```bash
# RF suite (from ec-automation/) — headed (watchable), the interactive default
EC_HEADLESS=false robot --outputdir results tests/EC_Production/Well_and_Reservoir/Daily/Group_Model_-_by_Flowline/daily_water_injection_flowline_status_edit.robot

# Playwright prototype (from this folder); EC_HOLD=<s> pauses per step so you can watch each edit
EC_HEADED=1 EC_HOLD=6 py -X utf8 playwright/ec_edit_iflw_water_flowline.py
```

| Env var | Default | Purpose |
|---|---|---|
| `EC_HEADED` | `0` | `1` = show the browser (prototype) |
| `EC_HOLD` | `0` | seconds to pause after each edit step (watchable) |
| `EC_URL` | sandbox URL | override the EC web app URL |
| `EC_DB_DSN` | `localhost:1521/ORCL` | Oracle DSN for the DB ground-truth check |

## Scope + oracle
- Scope: **2019-12-20** · PU "P1 Production Unit" → Area "P1 Area" → Facility "P1 Facility 1" →
  Flowline **"P1 F003 WI"**. Target cell **C2 = On Strm[hr] = `ON_STREAM_HRS`** (unitless).
- DB ground truth: `IFLW_DAY_STATUS.(OBJECT_ID, DAYTIME)`; set 18 → change 24 → clear (→NULL), each verified.
- ⚠️ Select the flowline by EXACT name `P1 F003 WI` (a dataless `P1 0600 F003 WI` also exists).

Status: **live 4/4 PASS** (2026-06-15), DB-verified, self-cleaning, robocop clean.
