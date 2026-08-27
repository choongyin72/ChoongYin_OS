# Evidence capture - Shift (CO.0224) lean-deliverable backfill, Batch 4

Captured 2026-08-28, backfilling the documentation/evidence bundle for the Area-pattern
conversion already merged via PR #547 (2026-08-26). No RF/Playwright automation files were
modified for this capture - this is a re-run of the already-proven, already-merged suite.

## Commands run (from `workstreams/master-plan/ec-automation/`, in the isolated worktree
`C:/tmp/wt-shift-backfill`)

1. `robot --dryrun --outputdir results/_shift_dryrun tests/Configuration/Assets/Facility_Objects/shift_iud.robot`
   -> **5 tests, 5 passed, 0 failed**.
2. `robot --dryrun --outputdir results/_dryrun_full tests/` (full-tree regression check)
   -> **883 tests, 883 passed, 0 failed** - no regression from touching only doc/evidence files.
3. `EC_HEADLESS=true robot --outputdir results/_shift_live_backfill tests/Configuration/Assets/Facility_Objects/shift_iud.robot`
   -> **5 tests, 5 passed, 0 failed** (TC01 Verify Clean State / TC02 Insert / TC03 Update /
   TC04 Find / TC05 Delete). First attempt succeeded - no timeout, no retry needed.
4. `py -m robocop check pageobjects/Configuration/Assets/Facility_Objects/shift_page.resource tests/Configuration/Assets/Facility_Objects/shift_iud.robot`
   -> **7 issues found, exit=0** (all DOC02 "missing test-case documentation" style warnings -
   non-fatal, pre-existing shape; not a regression introduced by this backfill, which touched
   no RF files).
5. `py scripts/check_bundle_hygiene.py` (repo-root script, whole-repo scan)
   -> **RESULT: PASS** - no hardcoded creds (R16) / pure ASCII (R20) / no CHECKLIST-vs-
   VERIFY-REPORT contradiction flagged for Shift.
6. DB self-clean, fresh `oracledb` connection (`localhost:1521/ORCL`, `ECKERNEL_EC`), run
   AFTER the live suite completed:
   - `SELECT COUNT(*) FROM OV_SHIFT WHERE CODE = 'AUTOTEST_SHIFT'` -> **0**
   - `SELECT COUNT(*) FROM OV_SHIFT WHERE CODE LIKE 'AUTOTEST%'` -> **0**

## Files in this folder
- `log.html` / `report.html` / `output.xml` - the live run's real Robot Framework artifacts.
- `TC0*_*.png` - the per-TC-step screenshots (login/open_screen/action/verify/logout) captured
  by the suite's own `Capture Step` keyword during the live run.
- This `results-summary.md`.

## Relationship to the pre-existing `evidence/` files
The `sh_0[1-5]_*.png` + `results.json` already in `evidence/` (dated 2026-07-31) are from the
ORIGINAL 4-TC Playwright build, predating PR #547's Area-pattern conversion - kept as-is (not
overwritten) since they document a real prior run. This folder documents the CURRENT (post-#547)
5-TC RF suite.
