# JOURNAL - Perforation Interval (CO.0153) 7-group nav + inner-GO popup IUD

## 2026-07-31
- **Branch:** `feature/perf-interval-iud`. Group A #4 - completes the 4-level well hierarchy
  (Well -> Well Bore -> Well Bore Interval -> Perforation Interval).
- **Recon facts (all executed):** 7 per-field nav groups. Along the P1 chain: **G:5 = ZERO options**
  (unusable filter, skipped - 4th screen with this quirk), **G:6 = the well bore** (1 option),
  **G:7 = the well bore interval** (1 option). Grid then shows 'No records found' (no perforations
  on that interval yet - our row is the first). DB: OV_PERF_INTERVAL = 225 rows.
- **NEW popup TYPE discovered (3rd variant):** the 'Well Bore Interval' popup
  (`well_bore_interval_gm_popup`) inherits the outer nav scope (G:1-G:4/G:6 pre-filled - proven by
  reading its inner inputs) but its list grid `Objects:form:T_data` is EMPTY until the popup's OWN
  inner GO (`button:form:B`) is clicked. First recon showed an empty tbody, which would have read as
  "no data"; driving the inner GO populated it. Popup catalogue is now:
  (1) plain `PopupList:form:T_data`, (2) already-populated `Objects:form:T_data` (Well Bore),
  (3) inner-GO `Objects:form:T_data` (this screen), plus Chemical Stream's Object-Type+GO variant.
- Also mandatory: 'Reservoir Block Formation' dropdown (first-available).
- Built by adapting the proven WBI pair; 2 robocop LEN03 refactors along the way (nav helper reused;
  popup split into `Open ... Popup List` + `Pick ...`). Driver 8/8 on the FIRST run.
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4,
  Playwright 8/8. Self-clean 0 residual.

## Lessons
- An EMPTY popup list is not evidence of missing data - check whether the popup has its own GO/filter
  controls first. Two screens in a row (Chemical Stream, this one) failed for exactly that reason.
- Splitting a long screen-local keyword into `Open ... List` + `Pick ...` satisfies robocop LEN03 and
  makes the popup's two phases (drive -> select) independently reusable.
