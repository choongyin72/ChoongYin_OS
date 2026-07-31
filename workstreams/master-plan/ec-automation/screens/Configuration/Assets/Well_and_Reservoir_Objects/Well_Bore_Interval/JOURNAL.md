# JOURNAL - Well Bore Interval (CO.0057) OV-GM 6-group nav + mandatory-popup IUD

## 2026-07-31
- **Branch:** `feature/well-bore-interval-iud`. Group A #3 - completes the well hierarchy
  (Well -> Well Bore -> Well Bore Interval).
- **Recon facts (all executed, nothing assumed):** 6 per-field nav groups. Under P1 + real well:
  **G:5 = ZERO options** (unusable filter, skipped - same as Well Bore's G:5), **G:6 = exactly one
  option, the well bore `P1 W008 WB001`**. Grid then lists the real interval `P1 W008 WB001 WBI001`.
  Mandatory 'Well Bore' popup (pin R:4) list grid = `Objects:form:T_data`, containing exactly the
  nav-scope bore. DB: OV_WELL_BORE_INTERVAL = 167 rows, base WEBO_INTERVAL.
- **Built by ADAPTING the proven Well Bore pair** (driver/T3/suite) rather than the generator
  (per-field nav + popup unsupported). The blanket rename needed 2 real corrections, both caught by
  post-edit greps: the popup LABEL on this screen is 'Well Bore' (not 'Well'), and G:6 had to be
  added to the navigator sequence.
- One robocop FAIL (LEN03: nav keyword 11/10 keywords) -> refactored into a `Select Nav Group Value`
  helper (also removes 5 repeated Sleep lines), re-ran clean.
- Driver 8/8 on the FIRST run; `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0,
  dryrun 4/4, LIVE RF 4/4, Playwright 8/8. Self-clean 0 residual.

## Lessons
- Adapting a proven sibling pair is fast but the clone-error checklist matters: label text and nav
  sequence differ even between adjacent hierarchy screens - grep every substituted token afterwards.
- The "phantom mandatory nav group" pattern (scan says mandatory, zero options in every scope) has
  now appeared on 3 screens (Well G:5, Well Bore G:5, WBI G:5) - treat it as a known EC quirk, and
  prove the grid loads without it rather than hunting for values.
