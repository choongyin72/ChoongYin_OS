# JOURNAL - Pilot Boat () OV-GM IUD

## 2026-07-30
- **Branch:** `feature/ov-gm-pilot-boat` (stacked on the gated-navigator capability, PR #244).
  Check-existing gate: grep ec-automation -> only this build; reused shared engine (ec_object_iud.py) + T2 + DbVerify.
- **Recon** (`investigation/recon.py`, read-only + tmp/pilot_boat/config.json scan): OV-GM (grid
  `manageObject:form:T_data`), navigator cascade Production Unit -> Area -> Facility Class 1. Mandatory Pilot Boat Code / Pilot Boat Name / Start Date.
- **Built** (generator `tmp/gen_ovgm.py` -> proven Node/Chemical-Tank template): label-driven T3 (no hardcoded
  ids); Playwright driver + RF T3/suite. Op Production Unit set first-available for grid visibility.
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4 pass, Playwright 8/8. DB residual 0.

## Lessons
- OV-GM: first-available nav scope + Op PU first-available lists the row after GO (parent-dd need not equal
  the nav PU - probe per screen). Generic engine handled cascade/appear/absent/pagination with zero tuning.
