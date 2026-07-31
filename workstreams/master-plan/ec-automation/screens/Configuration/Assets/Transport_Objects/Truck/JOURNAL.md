# JOURNAL - Truck (CO.0264) plain OV IUD

## 2026-07-31
- **Branch:** `feature/ov-gm-truck` (branch name is historical; the gated-navigator/PR #244 claim was WRONG - this is a plain OV build).
  Check-existing gate: grep ec-automation -> only this build; reused shared engine (ec_object_iud.py) + T2 + DbVerify.
- **Recon** (`investigation/recon.py`, read-only + tmp/truck/config.json scan): plain OV (grid `truck_object:form:T_data`). Nav: date field `nav:form:G:0:R:1:C:0:da_input` -> GO `#button:form:B` (no cascade). Mandatory Truck Code / Truck Name / Start Date.
- **Built** (generator `tmp/gen_ovgm.py` -> proven Node/Chemical-Tank template): label-driven T3 (no hardcoded
  ids); Playwright driver + RF T3/suite.
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4 pass, Playwright 8/8. DB residual 0.

## Lessons
- Plain OV: date-only navigator + GO; no cascade and no Op PU, so the grid lists straight after
  Save + GO. Generic engine handled the nav/appear/absent/pagination gestures with zero tuning.

_Family text corrected 2026-07-31 (prose only; code and gate results unchanged): this bundle shipped with OV-GM wording that does not describe this screen - the packager templates were OV-GM-only until then._
