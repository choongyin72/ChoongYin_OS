# JOURNAL - Shift (CO.0224) OV-GM + mandatory-free-text IUD

## 2026-07-31
- **Branch:** `feature/shift-iud-v3`. Previously PARKED: mandatory free-text field
  **Start Time (HH:MI)** - the field class the OV-GM generator cannot fill (only Code/Name/Start
  Date + dropdowns/popups).
- **UNPARKED without any generator change:** hand-built (4 prior hand-builds established the
  pattern) - the fix is literally one extra text field in the insert list.
- **Field semantics from EXISTING DATA (owner technique):** owner screenshot of the P1 S001 row's
  edit form gave every element's ground truth - Start Time format '07:00', Op Production Unit set
  to the nav PU, Duration/Period/Cycle optional. Banked as standing habit
  (feedback_scan_existing_row_first): select an existing row and read its populated values before
  building.
- **Navigator = SPECIFIC P1 values** (P1 Production Unit -> P1 Area -> P1 Facility 1; lists the 4
  existing P1 shifts). **Op Production Unit = nav PU** (parent-matching).
- **DB pre-checks:** BF CO.0224 (DefaultScreenTreeview); OV_SHIFT confirmed by real lookup
  ('P1 S001' present, 4 rows); Start Date 2020-01-01 (P1 shifts effective 2011).
- `verify_screen.py` -> **OVERALL PASS (first try)**: robocop 0, hygiene 0, dryrun 4/4,
  LIVE RF 4/4, Playwright 8/8. DB residual 0.
- **#265 lesson applied:** registry/scorecard rows column-diffed vs the Channel sibling; wording
  corrected to the free-text + specific-values facts.

## Lessons
- The "generator extension" framing was stale: once hand-building is routine, a mandatory free-text
  field is a one-line addition, not a tooling project. Re-evaluate old park reasons against current
  capabilities before treating them as still-binding.
- Existing-row values are the cheapest complete spec for a screen's fields.
