# Disposition Type — IUD bundle

Insert / Update / Delete automation for EC **Disposition Type** (Configuration > Assets > Hydrocarbon Objects; CO.0208).
OV Manage-Object screen; DELETE = End Date = Start Date. First reuse-target built on the shared `py/ec_object_iud.py` engine.

## Run
**Playwright** (from repo root):
```
EC_HEADED=1 py -X utf8 workstreams/master-plan/ec-automation/py/disposition_type_iud.py
```
**RF** (headed = the proof):
```
EC_HEADLESS=false robot --outputdir results/_disp \
  workstreams/master-plan/ec-automation/tests/Configuration/Assets/Hydrocarbon_Objects/disposition_type_iud.robot
```
Env: `EC_URL`, `EC_USERNAME`/`EC_USER`, `EC_PASSWORD`/`EC_PASS` (default local sandbox + sysadmin); `EC_DB_*` for DB ground truth.

## Layout
- Playwright driver: `py/disposition_type_iud.py` (shared engine + `DbVerify.py`)
- RF: T3 `pageobjects/.../Hydrocarbon_Objects/disposition_type_page.resource` + suite `tests/.../disposition_type_iud.robot`
- KB selector map: `ec-ui-knowledge/screens/disposition_type.md`
- SOW `disposition_type_sow.md` · JOURNAL `JOURNAL.md` · CHECKLIST `CHECKLIST.md` · recon `investigation/` · run proof `evidence/`

## Status
Playwright 7/7 + RF 4/4, live, DB-verified vs `OV_DISPOSITION_TYPE`, self-clean (0 residual). 2026-07-25.
