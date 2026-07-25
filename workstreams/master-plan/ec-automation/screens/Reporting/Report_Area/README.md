# Report Area — IUD bundle

Insert / Update / Delete automation for EC **Report Area** (Reporting > Report Area; RP.0017).
OV Manage-Object; DELETE = End Date = Start Date. 2nd OV-reuse-target on the shared `py/ec_object_iud.py` engine.

## Run
**Playwright** (from repo root):
```
EC_HEADED=1 py -X utf8 workstreams/master-plan/ec-automation/py/report_area_iud.py
```
**RF** (headed = the proof):
```
EC_HEADLESS=false robot --outputdir results/_rpta \
  workstreams/master-plan/ec-automation/tests/Reporting/report_area_iud.robot
```
Env: `EC_URL`, `EC_USERNAME`/`EC_USER`, `EC_PASSWORD`/`EC_PASS` (default local sandbox + sysadmin); `EC_DB_*` for DB ground truth.

## Layout
- Playwright driver: `py/report_area_iud.py` · RF: `pageobjects/Reporting/report_area_page.resource` + `tests/Reporting/report_area_iud.robot`
- KB map: `ec-ui-knowledge/screens/report_area.md` · SOW/JOURNAL/CHECKLIST here · recon `investigation/` · proof `evidence/`

## Status
Playwright 7/7 + RF 4/4, live, DB-verified vs `OV_REPORT_AREA`, self-clean. 2026-07-25.
