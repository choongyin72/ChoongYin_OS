# Report Area — IUD bundle

Insert / Update / Delete automation for EC **Report Area** (top-level Reporting > Report Area;
RP.0017). Plain Bank-family OV (Manage-Object, `manage_object_nav`) — simplest OV shape (Code /
Name / Start Date only; no Description, no dropdowns). DELETE = End Date = Start Date.

> **Updated 2026-08-28 (doc backfill, `docs/lean-deliverable-backfill-workorder.md` Batch 10):**
> the RF suite was converted to the full Bank pattern in PR #468 (merged 2026-08-23, Batch 9 of the
> original Bank-pattern conversion project) — 5 TCs, per-TC login/logout, properties-file-driven
> insert/update/verify, explicit grid-filter wiring, fixed test code `AUTOTEST_RPTA`. This backfill
> only refreshes documentation/evidence around that already-merged, already-live automation — no
> RF file was touched. The pre-existing Playwright driver (`py/report_area_iud.py`) is unaffected
> and stays its own separate stack (kept unchanged, permanently waived per Section H of
> `docs/IUD-DELIVERABLE-CHECKLIST.md` — the Universal Screen Engine replaces that role going
> forward).

## Layout
- **Driver (Playwright, unchanged):** `py/report_area_iud.py` (thin, shared engine `py/ec_object_iud.py` + `DbVerify.py`).
- **RF (current, post PR #468):** T3 `pageobjects/Reporting/report_area_page.resource` + suite
  `tests/Reporting/report_area_iud.robot` (5 TCs: Verify Clean State / Insert / Update / Find /
  Delete, per-TC login/logout, properties-file-driven insert/update/verify, explicit grid-filter
  wiring) + testdata `testdata/report_area_{insert,update,form_verify,grid_verify}.properties`.
- KB map: `ec-ui-knowledge/screens/report_area.md` · SOW/README/JOURNAL/CHECKLIST here · recon
  `investigation/` (pre-existing `recon.py`/`recon_update.py` + this backfill's additive
  `check_autotest_residual.py`) · proof `evidence/`.

## Run (RF, current shape)
```bash
# from workstreams/master-plan/ec-automation/

# dry run (syntax/keyword-resolution only, no browser/network)
robot --dryrun tests/Reporting/report_area_iud.robot

# live headless run (needs the EC sandbox reachable + local Oracle DB)
EC_HEADLESS=true robot --outputdir screens/Reporting/Report_Area/evidence/<date>_run tests/Reporting/report_area_iud.robot

# robocop (style/lint gate)
py -m robocop check pageobjects/Reporting/report_area_page.resource tests/Reporting/report_area_iud.robot
```

## Run (Playwright, unchanged legacy stack)
```bash
EC_HEADED=1 py -X utf8 workstreams/master-plan/ec-automation/py/report_area_iud.py
```
Env: `EC_URL`, `EC_USERNAME`/`EC_USER`, `EC_PASSWORD`/`EC_PASS` (default local sandbox + sysadmin);
`EC_DB_*` for DB ground truth.

## Verify in the database (self-clean check)
```bash
py -X utf8 screens/Reporting/Report_Area/investigation/check_autotest_residual.py
```
Expect `AUTOTEST residual rows in OV_REPORT_AREA: []` (0 residual `AUTOTEST%` rows) both before and
after a live run — the suite's own `TEST_CODE` is the fixed `AUTOTEST_RPTA`, which TC05 (Delete)
frees again every run.

## Status
RF live 5/5 (PR #468, 2026-08-23; re-confirmed live 5/5 in this backfill session, 2026-08-28),
DB-verified vs `OV_REPORT_AREA`, self-clean 0 residual. Playwright 7/7 (2026-07-25, unchanged
legacy stack). Full-tree `robot --dryrun tests/` 883/883 pass (this backfill session), no
regressions.
