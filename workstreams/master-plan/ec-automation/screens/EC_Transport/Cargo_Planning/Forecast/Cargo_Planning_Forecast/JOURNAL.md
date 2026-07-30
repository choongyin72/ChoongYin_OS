# JOURNAL - Cargo Planning Forecast (CP.0030) custom forecast-manager IUD

## 2026-07-31
- **Branch:** `feature/cargo-planning-forecast-iud-v2`. Previously PARKED: 4-level nav with the 4th
  level empty under first-available AS1 + ambiguous DB class match (2 candidates) + mandatory End Date.
- **UNPARKED via owner screenshot + fresh recon, all real facts:**
  - Nav scope: **P1 cascade + Storage P1_CRUDE_STOR** (owner screenshot; 'No records found' under
    the scope is fine - our insert is the first row).
  - Fresh recon (`tmp/recon_cpf.py`): navigator = **PER-FIELD groups** `nav:form:G:1..G:4:R:1:C:0`
    (unlike the standard single-row cascade); grid = **`fcst:form:T_data`** (custom prefix);
    the circled `new_fcst` panel + COPY FROM FORECAST/ORIGINAL = the copy-existing dialog
    (owner-confirmed, untouched); the standard `objectForm` is the insert form.
  - Ambiguous class resolved EMPIRICALLY: after insert the code appears in BOTH
    `OV_FCST_MNGR_FCST_LIST` and `OV_FORECAST_TRAN_CP` (both over base FORECAST) - the screen's own
    class view `OV_FCST_MNGR_FCST_LIST` is primary; driver self-clean checks BOTH.
  - Mandatory End Date: Start 2026-01-01 / End 2026-12-31 spans the nav date so the row lists.
    **End=Start delete PROVEN a true delete** on attempt 1 despite the mandatory insert End Date.
- **Built HAND-WRITTEN** (per-field nav groups + custom grid unsupported by generator).
- `verify_screen.py` -> **OVERALL PASS (first try)**: robocop 0, hygiene 0, dryrun 4/4,
  LIVE RF 4/4, Playwright 8/8. Self-clean 0 residual in BOTH views.
- **#265 lesson applied:** registry/scorecard rows column-diffed vs the Channel sibling; wording
  corrected to the custom-layout facts.

## Lessons
- Navigator layouts vary per module: EC Transport screens use per-field G-groups (G:1..G:N, C:0)
  vs Configuration screens' single-row cascade (G:0, C:1..N) - dump the nav input ids, never assume.
- An "ambiguous class match" resolves itself empirically post-insert: check which candidate views
  the real row lands in.
- 4th consecutive data-scope unpark: the whole "deep cascade" park class was one owner screenshot
  away per screen.
