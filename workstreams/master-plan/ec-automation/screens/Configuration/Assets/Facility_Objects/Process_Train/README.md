# Process Train (CO.0120) - OV IUD bundle

Manage-Object (OV) screen: **Configuration > Assets > Facility_Objects > Process Train**. Full Insert /
Update / Delete (End Date = Start Date), DB-verified against `OV_PROCESS_TRAIN`, self-cleaning. Converted
to the full **Bank/Berth pattern** in Batch 9 of the Bank-pattern conversion program (PR #469, merged
2026-08-23): properties-file-driven testdata, T2-consolidated helpers, explicit grid-filter wiring.

This bundle was refreshed 2026-08-28 as part of `docs/lean-deliverable-backfill-workorder.md` (Batch 10) -
the doc/evidence artifacts here now reflect the PR #469 rebuild, not the original 2026-07-26 scaffold.
**The RF automation itself was NOT touched by this refresh** - only documentation/evidence were added.

## Artifacts
(all paths below are relative to `workstreams/master-plan/ec-automation/`)
- **SOW:** `screens/Configuration/Assets/Facility_Objects/Process_Train/process_train_sow.md`
- **RF T3 (page object):** `pageobjects/Configuration/Assets/Facility_Objects/process_train_page.resource`
- **RF suite:** `tests/Configuration/Assets/Facility_Objects/process_train_iud.robot`
- **Testdata:** `testdata/process_train_{insert,update,form_verify,grid_verify}.properties`
- **Playwright driver (pre-existing, not rebuilt):** `py/process_train_iud.py`
- **KB selector map:** `ec-ui-knowledge/screens/process_train.md` (repo root, not under `ec-automation/`)
- **investigation/** recon.py (pre-existing, read-only) - **evidence/** screenshots + `output.xml`/`log.html`/`report.html`
- **VERIFY-REPORT.md** - hand-refreshed 2026-08-28 against the real dryrun/live re-run cited below

## Commands

Dryrun (syntax/keyword-resolution check, no browser):
```bash
cd workstreams/master-plan/ec-automation
robot --dryrun --outputdir <out> tests/Configuration/Assets/Facility_Objects/process_train_iud.robot
```

Live headless run:
```bash
cd workstreams/master-plan/ec-automation
EC_HEADLESS=true robot --outputdir <out> tests/Configuration/Assets/Facility_Objects/process_train_iud.robot
```

DB self-clean check (fresh connection, run after the suite completes - TC05 deletes the fixed test code):
```sql
SELECT COUNT(*) FROM OV_PROCESS_TRAIN WHERE CODE LIKE 'AUTOTEST_PT%';
-- expect 0
```
(equivalent Python: `oracledb.connect(...)` against `OV_PROCESS_TRAIN`, same pattern as
`libraries/DbVerify.py`'s `_code_present`.)

Robocop / hygiene:
```bash
cd workstreams/master-plan/ec-automation
py -m robocop check pageobjects/Configuration/Assets/Facility_Objects/process_train_page.resource \
    tests/Configuration/Assets/Facility_Objects/process_train_iud.robot
py scripts/check_bundle_hygiene.py
```

## Verified (real runs, 2026-08-28 backfill re-run)
robocop 9 issues (4 VAR02 + 5 DOC02, baseline-matching, no new defect class) - hygiene PASS -
dryrun **5/5** - **LIVE RF 5/5** - fresh-connection self-clean: **0** residual `AUTOTEST_PT%` rows in
`OV_PROCESS_TRAIN`.
