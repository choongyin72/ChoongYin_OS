# Choke Model — IUD bundle

Insert / Update / Delete automation for EC **Choke Model** (Configuration > Assets > Stream Objects; CO.0217).
OV Manage-Object; DELETE = End Date = Start Date. 4th OV-reuse-target on the shared `py/ec_object_iud.py` engine.

## Run
**Verify gate (auto-generates the tick report):**
```
py scripts/verify_screen.py --name "Choke Model" \
  --t3 workstreams/master-plan/ec-automation/pageobjects/Configuration/Assets/Stream_Objects/choke_model_page.resource \
  --suite workstreams/master-plan/ec-automation/tests/Configuration/Assets/Stream_Objects/choke_model_iud.robot \
  --driver workstreams/master-plan/ec-automation/py/choke_model_iud.py --out <bundle>/VERIFY-REPORT.md
```
**Playwright:** `EC_HEADED=1 py -X utf8 workstreams/master-plan/ec-automation/py/choke_model_iud.py`
**RF:** `EC_HEADLESS=false robot --outputdir results/_chkm workstreams/master-plan/ec-automation/tests/Configuration/Assets/Stream_Objects/choke_model_iud.robot`

## Layout
- Playwright: `py/choke_model_iud.py` · RF: `pageobjects/.../Stream_Objects/choke_model_page.resource` + `tests/.../choke_model_iud.robot`
- KB map: `ec-ui-knowledge/screens/choke_model.md` · SOW/JOURNAL/CHECKLIST here · recon `investigation/` · proof `evidence/` + `VERIFY-REPORT.md`

## Status
verify_screen.py OVERALL PASS (RF 4/4 + Playwright 7/7), DB-verified vs `OV_CHOKE_MODEL`, self-clean. 2026-07-26.
