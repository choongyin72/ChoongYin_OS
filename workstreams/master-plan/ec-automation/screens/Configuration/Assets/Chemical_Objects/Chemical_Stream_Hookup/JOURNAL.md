# JOURNAL - Chemical Stream Hookup (CO.0260) OV-GM IUD

## 2026-08-01
- **Branch:** `feature/chemical-stream-hookup-iud`.
  Check-existing gate: 0b grep ec-automation -> only this build (checked: 0 other file(s) reference 'chemical_stream_hookup'); reused shared engine (ec_object_iud.py) + T2 + DbVerify.
- **Recon** (`investigation/recon.py`, read-only + tmp/chemical_stream_hookup/config.json scan): OV-GM (grid `manageObject:form:T_data`).
  Nav: Production Unit -> Area -> Facility Class 1 cascade + GO. Mandatory Chemical Stream Hookup Code / Chemical Stream Hookup Name / Start Date.
- **Built** (generator `tmp/gen_ovgm.py`): label-driven T3 (no hardcoded ids); Playwright driver + RF T3/suite.
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4 pass, Playwright 8/8. DB residual 0.

## Lessons
- OV-GM: first-available nav scope + Op PU first-available lists the row after GO (parent-dd need not equal the nav PU - probe per screen). Generic engine handled the nav/appear/absent/pagination gestures with zero tuning.
