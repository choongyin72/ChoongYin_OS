# Daily Water Injection Flowline, by Flowline — N1 edit

Edit-in-place daily-status automation for the EC **Daily Water Injection Flowline, by Flowline** screen
(EC Production → Daily → Group Model - by Flowline). The N1 daily-status-grid pattern generalized to
water-injection flowlines (`IFLW_DAY_STATUS`). Direct sibling of PFLW ("Daily Production Flowline, by
Flowline") — same grid component, so the RF suite reuses `daily_status_grid` (T2) + `DbVerify` verbatim.

## Two parts (per the project convention)
1. **RF suite** (the productised test) — runs from the project root:
   - T3: `pageobjects/EC_Production/Well_and_Reservoir/Daily/Group_Model_-_by_Flowline/iflw_water_flowline_status_page.resource`
   - Suite: `tests/EC_Production/Well_and_Reservoir/Daily/Group_Model_-_by_Flowline/daily_water_injection_flowline_status_edit.robot`
2. **Playwright bundle** (this folder, freestyle prototype + discovery trail + spec):
   - `iflw_water_flowline_sow.md` — statement of work
   - `playwright/ec_edit_iflw_water_flowline.py` — standalone edit→DB-verify→restore prototype
   - `investigation/` — recon scripts (data scope, injection type, screen crack, grid-cell map)
   - `evidence/` — screenshots from a full run

## Run

```bash
# RF suite (from ec-automation/) — headed (watchable), the interactive default
EC_HEADLESS=false robot --outputdir results tests/EC_Production/Well_and_Reservoir/Daily/Group_Model_-_by_Flowline/daily_water_injection_flowline_status_edit.robot

# Playwright prototype (from this folder)
EC_HEADED=1 py -X utf8 playwright/ec_edit_iflw_water_flowline.py
```

| Env var | Default | Purpose |
|---|---|---|
| `EC_HEADED` | `0` | `1` = show the browser (prototype) |
| `EC_URL` | sandbox URL | override the EC web app URL |
| `EC_DB_DSN` | `localhost:1521/ORCL` | Oracle DSN for the DB ground-truth check |

## Scope + oracle
- Scope: **2019-12-20** · PU "P1 Production Unit" → Area "P1 Area" → Facility "P1 Facility 1" →
  Flowline **"P1 F003 WI"**. Target cell **C2 = On Strm[hr] = `ON_STREAM_HRS`** (unitless).
- DB ground truth: `IFLW_DAY_STATUS.(OBJECT_ID, DAYTIME)`; assert `ON_STREAM_HRS=18` then restore NULL.
- ⚠️ Select the flowline by EXACT name `P1 F003 WI` (a dataless `P1 0600 F003 WI` also exists).

Status: **live 3/3 PASS** (2026-06-15), DB-verified, self-cleaning, robocop clean.
