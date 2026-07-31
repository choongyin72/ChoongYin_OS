# JOURNAL - Contract Area Setup (CO.2038) custom-URL OV IUD

## 2026-07-31
- **Branch:** `feature/ov-gm-contract-area-setup` (branch name is historical; the gated-navigator/PR #244 claim was WRONG - this is a custom-URL OV build).
  Check-existing gate: grep ec-automation -> only this build; reused shared engine (ec_object_iud.py) + T2 + DbVerify.
- **Recon** (`investigation/recon.py`, read-only + tmp/contract_area_setup/config.json scan): custom-URL OV (grid `nav:form:T_data`). Nav: none - grid loads from the screen URL; re-query via toolbar Refresh `[Ctrl+r]`. Mandatory Contract Area Setup Code / Contract Area Setup Name / Start Date.
- **Built** (generator `tmp/gen_ovgm.py` -> proven Node/Chemical-Tank template): label-driven T3 (no hardcoded
  ids); Playwright driver + RF T3/suite.
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4 pass, Playwright 7/7. DB residual 0.

## Lessons
- Custom-URL OV: no navigator GO; the toolbar Refresh is the re-query gesture. Generic engine handled the nav/appear/absent/pagination gestures with zero tuning.

_Family text corrected 2026-07-31 (prose only; code and gate results unchanged): this bundle shipped with OV-GM wording that does not describe this screen - the packager templates were OV-GM-only until then._
