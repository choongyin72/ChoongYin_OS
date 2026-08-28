# Product Group - IUD bundle

Configuration > Assets > Royalty Objects > **Product Group** (RC.0053).
Manage-Object (OV) screen, **Bank pattern** (label-driven, properties-file-driven, T2-consolidated,
explicit grid-filter wiring — rebuilt from the older hardcoded-field-id pattern via PR #445,
merged 2026-08-23, Batch 5). DELETE = End Date = Start Date (true delete in `OV_PRODUCT_GROUP`).

## Contents
- `product_group_sow.md` - Statement of Work (recon + design + acceptance criteria + dev story
  covering both the original 2026-06-25 build and the PR #445 Bank-pattern conversion).
- `README.md` - this file.
- `JOURNAL.md` - per-branch work journal (built / done well / done wrong-or-lessons /
  blockers -> resolution / decisions / evidence), backfilled 2026-08-28.
- `playwright/ec_iud_product_group.py` - legacy freestyle Playwright IUD walkthrough (screenshots
  per step; predates the Universal Screen Engine, kept as a reference, not rebuilt).
- `evidence/` - `product_group_tc0[1-4]_*.png` from the original 2026-06-25 run, plus
  `evidence/backfill_2026-08-28/` (fresh dryrun + live headless re-run captured for this backfill).
- `CHECKLIST.md` - `docs/IUD-DELIVERABLE-CHECKLIST.md` copied in, ticked with real evidence.

## RF suite (the proof)
- T3 page object: `pageobjects/Configuration/Assets/Royalty_Objects/product_group_page.resource`
- Test suite:     `tests/Configuration/Assets/Royalty_Objects/product_group_iud.robot` (5 TCs:
  Verify Clean State / Insert / Update / Find / Delete)
- Reuses T2 `resources/manage_object.resource` + T1 `resources/common.resource` +
  `libraries/DbVerify.py` (no shared-file edits). Own dedicated credential pair
  `PRODUCT_GROUP_EC_USER`/`PRODUCT_GROUP_EC_PASS` (`resources/credentials.py`).
- Fixed test code `AUTOTEST_PRODUCT_GROUP` (not a per-run generated code).

## Run (from `workstreams/master-plan/ec-automation/`)
```bash
# Dryrun (syntax/flow check, no browser):
py -m robot --dryrun --outputdir <tmp-dir> tests/Configuration/Assets/Royalty_Objects/product_group_iud.robot

# Live headless run (the proof):
EC_HEADLESS=true py -m robot --outputdir <tmp-dir> tests/Configuration/Assets/Royalty_Objects/product_group_iud.robot

# Live headed run (visual demo):
EC_HEADLESS=false py -m robot --outputdir <tmp-dir> tests/Configuration/Assets/Royalty_Objects/product_group_iud.robot

# Legacy Playwright walkthrough (demo / screenshots, not the proof):
EC_HEADED=1 py -X utf8 screens/Configuration/Assets/Royalty_Objects/Product_Group/playwright/ec_iud_product_group.py
```

## DB self-clean check (fresh connection, independent of the suite run)
```sql
SELECT COUNT(*) FROM OV_PRODUCT_GROUP WHERE CODE = 'AUTOTEST_PRODUCT_GROUP';  -- expect 0 after a live run
```
Run via `oracledb` (see `libraries/DbVerify.py` for the connection pattern: env vars
`EC_DB_USER`/`EC_DB_PASS`/`EC_DB_DSN`, default `ECKERNEL_EC`/`energy`/`localhost:1521/ORCL`).

Env: sandbox web `https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/` (`sysadmin`/`sysadmin`),
DB `localhost:1521/ORCL` (`ECKERNEL_EC`/`energy`). Test data `AUTOTEST_PRODUCT_GROUP` /
legacy `AUTOTEST_PG_*` only; self-cleaning.
