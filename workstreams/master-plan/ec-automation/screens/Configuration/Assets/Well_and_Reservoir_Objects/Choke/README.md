# Choke — IUD bundle

Insert / Update / Delete automation for EC **Choke** (Configuration > Assets > Well and Reservoir Objects; CO.0185).
OV Manage-Object; DELETE = End Date = Start Date. 3rd OV-reuse-target on the shared `py/ec_object_iud.py` engine.

## Run
**Verify gate (recommended — auto-generates the tick report):**
```
py scripts/verify_screen.py --name "Choke" \
  --t3 workstreams/master-plan/ec-automation/pageobjects/Configuration/Assets/Well_and_Reservoir_Objects/choke_page.resource \
  --suite workstreams/master-plan/ec-automation/tests/Configuration/Assets/Well_and_Reservoir_Objects/choke_iud.robot \
  --driver workstreams/master-plan/ec-automation/py/choke_iud.py --out <bundle>/VERIFY-REPORT.md
```
**Playwright:** `EC_HEADED=1 py -X utf8 workstreams/master-plan/ec-automation/py/choke_iud.py`
**RF:** `EC_HEADLESS=false robot --outputdir results/_choke workstreams/master-plan/ec-automation/tests/Configuration/Assets/Well_and_Reservoir_Objects/choke_iud.robot`

## Layout
- Playwright: `py/choke_iud.py` · RF: `pageobjects/.../choke_page.resource` + `tests/.../choke_iud.robot`
- KB map: `ec-ui-knowledge/screens/choke.md` · SOW/JOURNAL/CHECKLIST here · recon `investigation/` · proof `evidence/` + `VERIFY-REPORT.md`

## Status
verify_screen.py OVERALL PASS (RF 4/4 + Playwright 7/7), DB-verified vs `OV_CHOKE`, self-clean. 2026-07-25.
