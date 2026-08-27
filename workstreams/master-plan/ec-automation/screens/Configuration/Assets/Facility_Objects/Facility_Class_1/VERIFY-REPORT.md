# VERIFY-REPORT - Facility Class 1

_Original run 2026-07-30 by `scripts/verify_screen.py` against the retired 4-TC/first-available-nav
shape (superseded numbers below). Section below is HAND-ASSEMBLED 2026-08-27 for this backfill,
citing the exact command + real exit code/output for every tick - `scripts/verify_screen.py` requires
a `--driver` (Playwright) argument, which this backfill does not build per Section H's Playwright
waiver, so the RF-only gates below were run directly instead of through that wrapper._

## 2026-08-27 backfill re-run (current automation: 5-TC, fixed code AUTOTEST_FC1, PR #526/#530 shape)

**OVERALL: PASS** (RF-only gates; Playwright gate intentionally not re-run - driver retained as-is,
not part of this backfill's scope)

- [x] **10** robocop clean - `robocop check pageobjects/.../facility_class_1_page.resource
      tests/.../facility_class_1_iud.robot` -> 7 issues (2 VAR02 + 5 DOC02), same non-regression
      baseline as Area / as PR #530 cited.
- [x] **16** hygiene (R16 creds / R20 ASCII) - `py scripts/check_bundle_hygiene.py` (repo root) ->
      RESULT: PASS.
- [x] **11** robot --dryrun - 5 tests, 5 passed, 0 failed.
- [x] **12** LIVE RF suite (EC_HEADLESS=true; pure-screen-verify, DB check inside shared T2
      `Verify Object Removed`; independent fresh-connection DB self-clean = 0 residual
      `AUTOTEST_FC1%` rows) - 5 tests, 5 passed, 0 failed.

## 2026-07-30 original run (historical - superseded by PR #526/#530's conversion)

- [x] **10** robocop clean - exit=0
- [x] **16** hygiene (R16 creds / R20 ASCII) - exit=0
- [x] **11** robot --dryrun - 4/4 pass, 0 fail
- [x] **12** LIVE RF suite (DB-verified + self-clean in-suite) - 4/4 pass, 0 fail
- [x] **PW** Playwright driver 8/8 - Overall: ALL PASS (driver unchanged since; still passing per
      JOURNAL.md, not re-run for this backfill)
