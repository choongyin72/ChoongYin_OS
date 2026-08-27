# Data Extract Set (SP.0049) - OV IUD bundle

Manage-Object (OV) screen: **Configuration > Assets > Data_Mapping_Objects > Data Extract Set**. Plain
Bank-family OV (no navigator cascade), rebuilt to the **FULL Bank-pattern** shape via PR #474
(2026-08-23, Batch 10): properties-file-driven insert/update/verify + explicit grid-filter wiring,
label-driven (zero hardcoded field ids), DB-verified against `OV_SUMMARY_SET`, self-cleaning.

This backfill (docs-only, 2026-08-28, Batch 11 of `docs/lean-deliverable-backfill-workorder.md`) adds
the documentation/evidence artifacts this screen's lean-era conversion PR skipped. **No RF automation
file was modified** - the page object, suite, and testdata are exactly as PR #474 left them.

## Artifacts
- **SOW:** `data_extract_set_sow.md`
- **RF T3:** `../../../../pageobjects/Configuration/Assets/Data_Mapping_Objects/data_extract_set_page.resource`
- **RF suite:** `../../../../tests/Configuration/Assets/Data_Mapping_Objects/data_extract_set_iud.robot`
- **Testdata:** `../../../../testdata/data_extract_set_{insert,update,form_verify,grid_verify}.properties`
- **investigation/** recon.py (pre-existing, 2026-07-26 build; untouched)
- **evidence/** screenshots + `evidence/live_run_2026-08-28/` (this backfill's evidence-capture run)
- **Playwright driver** (waived from this backfill per Section H - covered by the Universal Screen
  Engine going forward): `../../../../py/data_extract_set_iud.py` (pre-existing, unchanged, still 7/7
  per PR #474)

## Commands

Dry-run the suite (syntax/keyword check only, no browser):
```
cd workstreams/master-plan/ec-automation
robot --dryrun --outputdir results/_dryrun tests/Configuration/Assets/Data_Mapping_Objects/data_extract_set_iud.robot
```

Live headless run:
```
cd workstreams/master-plan/ec-automation
EC_HEADLESS=true robot --outputdir results/_live tests/Configuration/Assets/Data_Mapping_Objects/data_extract_set_iud.robot
```

DB self-clean check (fresh connection, run BEFORE and AFTER a live run - both must return zero rows for
the fixed test code to stay reusable):
```sql
SELECT CODE FROM OV_SUMMARY_SET WHERE CODE = 'AUTOTEST_DXT';
```

## Verified (real runs, not hand-ticked)
Per PR #474 (2026-08-23): robocop same-profile-as-exemplar (5 DOC02 + 4 VAR02, no regression) - dryrun
767/767 (full tree) - **LIVE RF 5/5** - DB self-clean 0 residual (fresh `oracledb` connection,
before AND after). Playwright 7/7 (pre-existing, unchanged). See `CHECKLIST.md` for the full
21-item gate mapping and this backfill's own evidence-capture run.
