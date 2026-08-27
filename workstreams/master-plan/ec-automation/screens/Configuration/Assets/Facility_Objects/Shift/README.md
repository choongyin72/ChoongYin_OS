# Shift - IUD bundle

**Screen:** Configuration > Assets > Facility_Objects > Shift (BF CO.0224). OV-GM (grid
`manageObject:form:T_data`), Area-pattern **5-TC / per-TC-login / pure-screen-verify**
structure (converted PR #547, merged 2026-08-26), with a genuine 3-level Production Unit ->
Area -> Facility Class 1 navigator cascade + GO (SPECIFIC P1 values, kept exactly as the prior
driver proved it - navigator fill delegated to the shared T2 `Apply Navigator From Properties`)
and a mandatory free-text **Start Time (HH:MI)** insert extra (`07:00`, format from the
existing P1 S001 row). View `OV_SHIFT`. Date-effective; DELETE = End Date = Start Date.

- **RF:** T3 `pageobjects/Configuration/Assets/Facility_Objects/shift_page.resource` + suite
  `tests/Configuration/Assets/Facility_Objects/shift_iud.robot` (5 TCs: Verify Clean State /
  Insert / Update / Find / Delete, each with its own Login/Logout).
- **Playwright:** `py/shift_iud.py` (thin, shared engine `ec_object_iud.py`) - out of scope for
  re-verification in this backfill (Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md`: the
  Playwright bundle stays permanently waived, superseded by the Universal Screen Engine).
- **Testdata (properties files):** `testdata/shift_navigator.properties`,
  `testdata/shift_insert.properties`, `testdata/shift_update.properties`,
  `testdata/shift_form_verify.properties`, `testdata/shift_grid_verify.properties`.
- **Credentials:** `SHIFT_EC_USER`/`SHIFT_EC_PASS` in `resources/credentials.py`.
- **Fixed test code:** `AUTOTEST_SHIFT` (confirmed free in `OV_SHIFT` before use; every run must
  complete TC05 Delete so the code is free for the next run).

## Run commands

All commands run from `workstreams/master-plan/ec-automation/`.

Dry-run (syntax/keyword-resolution check only, no browser):
```
robot --dryrun --outputdir results/_shift_dryrun tests/Configuration/Assets/Facility_Objects/shift_iud.robot
```

Full-tree dryrun (regression check - confirms no other suite's keyword resolution broke):
```
robot --dryrun --outputdir results/_dryrun_full tests/
```

Live headless run (the real evidence-producing run):
```
EC_HEADLESS=true robot --outputdir results/_shift_live tests/Configuration/Assets/Facility_Objects/shift_iud.robot
```

Live headed run (visual confirmation):
```
EC_HEADLESS=false robot --outputdir results/_shift_live_headed tests/Configuration/Assets/Facility_Objects/shift_iud.robot
```

## DB self-clean check (fresh connection, post-run)

Against the local sandbox (`localhost:1521/ORCL`, `ECKERNEL_EC`/`energy`) or the target EC
environment's own DSN (`EC_DB_DSN`/`EC_DB_USER`/`EC_DB_PASS` env vars, see
`libraries/DbVerify.py`) - confirm the fixed test code leaves 0 residual rows:
```sql
SELECT COUNT(*) FROM OV_SHIFT WHERE CODE = 'AUTOTEST_SHIFT';
SELECT COUNT(*) FROM OV_SHIFT WHERE CODE LIKE 'AUTOTEST%';
```
Both must return 0 after a completed 5-TC run (TC05 Delete always runs).

## Verify gate

`VERIFY-REPORT.md` in this folder is the auto-generated record from the 2026-07-31 build
(`scripts/verify_screen.py`, OVERALL PASS against the then-4-TC suite) - it predates PR #547's
Area-pattern conversion. This backfill (2026-08-28) does not regenerate `VERIFY-REPORT.md`
(the tool requires the exact `--t3`/`--suite` shape at the time it was built); the current
state is instead documented in `JOURNAL.md` and `evidence/rf_backfill_2026-08-28/` - full-tree
dryrun 883/883, live RF 5/5, robocop exit 0, hygiene PASS, DB self-clean 0 residual, all
re-run and cited fresh for this backfill.
