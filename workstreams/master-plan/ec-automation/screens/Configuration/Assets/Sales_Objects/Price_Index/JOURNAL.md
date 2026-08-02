# JOURNAL - Price Index (CO.3009) OV-GM IUD

## 2026-08-02
- **Branch:** `feature/retry-price-index-iud`. Previously parked (park record in
  `docs/ov-non-bank-targets.md`) as "2nd dropdown mis-persists" - the New-Object form fills Frequency
  then Business Unit (`parent_dd`) in sequence, and Business Unit silently persisted `SS1_BU` instead
  of the requested `Royalty Canada`/`ROYALTY_CA`, reproduced 3 times originally and suspected as a
  deeper widget-state issue in the shared `select_dropdown()` engine (same symptom independently seen
  on Property and Royalty Contract).
- **Real root cause (same as Property - see [[feedback_child_object_date_must_follow_parent]]):** the
  generator config's `start_date` was `2000-01-01`, but the target Business Unit "Royalty Canada"
  (`ROYALTY_CA`) is only effective from `2003-01-01` onward (`OV_BUSINESS_UNIT.OBJECT_START_DATE`).
  EC's Business Unit reference dropdown only offers parents already effective by the record's own
  Start Date; with `2000-01-01`, "Royalty Canada" wasn't even in the filtered option list, so the
  fallback silently took a different available option.
- **Fix:** changed `tmp/cfg_pi.json`'s `start_date` to `2003-01-01`, regenerated via `tmp/gen_ovgm.py`.
  No shared-engine change, no id/navigator-template gap this time (Price Index's Date and Business
  Unit dropdown ARE in the same navigator group `G:0`, unlike Property).
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4 pass,
  Playwright driver 8/8. DB residual 0.

## Lessons
- Confirms the Property finding generalizes: this exact symptom class (a reference dropdown
  "silently" landing on the wrong value) was a test-data date mismatch on 2 screens running the
  same generator pattern, not a shared-engine defect. Same fix (`start_date >= the referenced
  object's own effective date`) resolved it on the first retry, no new investigation needed.
