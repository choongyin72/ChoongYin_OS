# JOURNAL - Create Calculation (CO.1042) TV-style IUD

## 2026-07-31
- **Branch:** `feature/ov-gm-create-calculation` (branch name is historical; the gated-navigator/PR #244 claim was WRONG - this is a TV-style build).
  Check-existing gate: grep ec-automation -> only this build; reused shared engine (ec_object_iud.py) + T2 + DbVerify.
- **Recon** (`investigation/recon.py`, read-only + tmp/create_calculation/config.json scan): TV-style (grid `calculation:form:T_data`). Nav: per-screen context/date navigator (see SOW). Mandatory Calculation Code / Calculation Name / Start Date.
- **Built** (generator `tmp/gen_ovgm.py` -> proven Node/Chemical-Tank template): label-driven T3 (no hardcoded
  ids); Playwright driver + RF T3/suite.
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4 pass, Playwright 8/8. DB residual 0.

## Lessons
- TV-style: the row is edited in place; confirm the delete gesture per screen. Generic engine handled the nav/appear/absent/pagination gestures with zero tuning.

_Family text corrected 2026-07-31 (prose only; code and gate results unchanged): this bundle shipped with OV-GM wording that does not describe this screen - the packager templates were OV-GM-only until then._
