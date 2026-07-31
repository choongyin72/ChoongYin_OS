# JOURNAL - Well (CO.0049) OV-GM IUD (specific-values nav)

## 2026-07-30
- **Branch:** `feature/well-iud-v2`. Previously PARKED: original scan found 5 mandatory nav dds with
  the 5th empty under the first-available AS1 path (fill timeout, grid never loaded).
- **UNPARKED by owner screenshot:** with only the standard 3-level cascade filled with SPECIFIC P1
  values (P1 Production Unit -> P1 Area -> P1 Facility 1) + GO, the grid lists wells while the
  2nd-row dds (Well & Well Hookup / Well) stay EMPTY - they are optional filters, and the park was a
  data-scope artifact of the AS1 path, not a structural blocker.
- **DB pre-checks (real facts):** BF CO.0049 (DefaultScreenTreeview); resolver matched
  ['WELL','FORECAST_WELL'] -> OV_WELL confirmed the live view by REAL lookup ('P1 W001 OP' present,
  506 rows); P1 wells effective 2010-01-01 -> Start Date 2020-01-01.
- **Built HAND-WRITTEN (no generator - specific nav values unsupported):** thin driver with
  screen-local `apply_well_navigator`; T3 with screen-local `Apply Well Navigator` on T1
  `Select EC Dropdown Option` + `Apply Navigator`. Insert: Well Type first-available; NO Op
  Production Unit field on this form (rows list under the nav scope regardless, like Facility Class 1).
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4 pass,
  Playwright 8/8. DB residual 0.
- **#265 lesson applied:** registry/scorecard rows column-diffed vs the Channel sibling; nav column
  states SPECIFIC P1 values (not the template first-available text).

## Lessons
- Second confirmation (after Lifting Account) that "deep cascade with an empty level" parks are
  DATA-SCOPE gaps: one owner-provided working scope resolves them in a single pass.
- A scan's "mandatory" flag on extra nav dds can be scope-dependent: under the P1 path the 2nd-row
  Well dds were ignorable filters.
