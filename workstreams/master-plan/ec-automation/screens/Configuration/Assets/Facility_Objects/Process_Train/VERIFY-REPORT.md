# VERIFY-REPORT - Process Train (CO.0120)

_Hand-refreshed 2026-08-28 (`docs/lean-deliverable-backfill-workorder.md`, Batch 10) against a real
re-run of the already-proven, unmodified suite. Supersedes the 2026-08-23 report below, which still
cited the pre-Bank-pattern 4/4 counts._

**OVERALL: PASS**

- [x] **10** robocop - `py -m robocop check pageobjects/Configuration/Assets/Facility_Objects/process_train_page.resource tests/Configuration/Assets/Facility_Objects/process_train_iud.robot` - 9 issues (4 VAR02 + 5 DOC02), exit=0, baseline-matching (Bank/Berth/Port).
- [x] **16** hygiene (R16 creds / R20 ASCII) - `py scripts/check_bundle_hygiene.py` - RESULT: PASS, exit=0.
- [x] **11** `robot --dryrun tests/Configuration/Assets/Facility_Objects/process_train_iud.robot` - 5/5 pass, 0 fail.
- [x] **12** LIVE headless run - `EC_HEADLESS=true robot tests/Configuration/Assets/Facility_Objects/process_train_iud.robot` - **5/5 pass, 0 fail** (first attempt, no retry needed).
- [x] **13/15** DB ground-truth + self-clean - fresh `oracledb` connection, `SELECT COUNT(*) FROM OV_PROCESS_TRAIN WHERE CODE LIKE 'AUTOTEST_PT%'` -> **0** after the live run.

_Previous report (2026-08-23, pre-refresh): robocop exit=0 (pre-Bank-pattern build, different
issue count), hygiene exit=0, dryrun 4/4, LIVE RF 4/4, Playwright 7/7. Superseded by the 5/5 counts
above once the suite was rebuilt to 5 TCs in PR #469 (added TC04 Find) - this report was simply
never refreshed at that time; corrected now._
