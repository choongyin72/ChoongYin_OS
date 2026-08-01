# JOURNAL - Contract (CO.2016) OV-GM IUD

## 2026-08-02
- **Branch:** `feature/contract-iud`.
  Check-existing gate: 0b grep ec-automation -> only this build (checked: 0 other file(s) reference 'contract'); reused shared engine (ec_object_iud.py) + T2 + DbVerify.
- **Recon** (`investigation/recon.py`, read-only + tmp/contract/config.json scan): OV-GM (grid `manageObject:form:T_data`).
  Nav: Business Unit cascade + GO. Mandatory Contract Code / Contract Name / Start Date + dropdowns Contract Template, Contract Area=TS5 Contract Area.
- **Built** (generator `tmp/gen_ovgm.py`): label-driven T3 (no hardcoded ids); Playwright driver + RF T3/suite.
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4 pass, Playwright 8/8. DB residual 0.

## Lessons
- OV-GM: nav cascade uses PROVEN explicit values (scripts/find_populated_scope.py), not first-available - do not assume the first option has usable data underneath. Generic engine handled the nav/appear/absent/pagination gestures with zero tuning.
