# JOURNAL - Collection Point (CO.0205) OV-GM IUD

## 2026-08-01
- **Branch:** `feature/collection-point-iud`.
  Check-existing gate: 0b grep ec-automation -> only this build (checked: 0 other file(s) reference 'collection_point'); reused shared engine (ec_object_iud.py) + T2 + DbVerify.
- **Recon** (`investigation/recon.py`, read-only + tmp/collection_point/config.json scan): OV-GM (grid `manageObject:form:T_data`).
  Nav: Production Unit -> Area -> Operator Route cascade + GO. Mandatory Collection Point Code / Collection Point Name / Start Date.
- **Built** (generator `tmp/gen_ovgm.py`): label-driven T3 (no hardcoded ids); Playwright driver + RF T3/suite.
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4 pass, Playwright 8/8. DB residual 0.

## Lessons
- OV-GM: nav cascade uses PROVEN explicit values (scripts/find_populated_scope.py), not first-available - do not assume the first option has usable data underneath. Generic engine handled the nav/appear/absent/pagination gestures with zero tuning.
