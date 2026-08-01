# JOURNAL - External Location (CO.0227) OV-GM IUD

## 2026-08-01
- **Branch:** `feature/external-location-iud`.
  Check-existing gate: 0b grep ec-automation -> only this build (checked: 0 other file(s) reference 'external_location'); reused shared engine (ec_object_iud.py) + T2 + DbVerify.
- **Recon** (`investigation/recon.py`, read-only + tmp/external_location/config.json scan): OV-GM (grid `manageObject:form:T_data`).
  Nav: GO only (navigator fields are optional filters, no mandatory scope). Mandatory External Location Code / External Location Name / Start Date.
- **Built** (generator `tmp/gen_ovgm.py`): label-driven T3 (no hardcoded ids); Playwright driver + RF T3/suite.
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4 pass, Playwright 8/8. DB residual 0.

## Lessons
- OV-GM: first-available nav scope + Op PU first-available lists the row after GO (parent-dd need not equal the nav PU - probe per screen). Generic engine handled the nav/appear/absent/pagination gestures with zero tuning.
