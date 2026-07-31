# JOURNAL - Report Group (CO.0158) plain OV IUD

## 2026-07-31
- **Branch:** `feature/report-group-iud`.
  Check-existing gate: 0b grep ec-automation -> only this build (checked: 0 other file(s) reference 'report_group'); reused shared engine (ec_object_iud.py) + T2 + DbVerify.
- **Recon** (`investigation/recon.py`, read-only + tmp/report_group/config.json scan): plain OV (Bank family, grid `report_group_table:form:T_data`).
  Nav: date-only navigator + GO (no cascade). Mandatory Reporting Group Code / Reporting Group Name / Start Date + dropdowns Business Area.
- **Built** (generator `tmp/gen_ov.py`): label-driven T3 (no hardcoded ids); Playwright driver + RF T3/suite.
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4 pass, Playwright 8/8. DB residual 0.

## Lessons
- Plain OV: date-only navigator + GO; no cascade and no Op PU to satisfy, so the grid lists immediately after Save + GO. Generic engine handled the nav/appear/absent/pagination gestures with zero tuning.
