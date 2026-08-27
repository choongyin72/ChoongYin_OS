# Cost Object Mapping — IUD automation bundle

**Screen:** Configuration > Assets > Financial Objects > Cost Object Mapping
**Type:** OV (manage-object), no navigator — Bank-pattern.
**Delete:** End Date = Start Date (zero-length window ⇒ true delete from `OV_FIN_COST_OBJECT`).
**Status:** live **5/5 PASS** (Bank pattern, TC01-TC05), DB-verified, self-cleaning.
See [cost_object_mapping_sow.md](cost_object_mapping_sow.md) and [JOURNAL.md](JOURNAL.md).

**The Robot Framework suite is the current, maintained automation for this screen** — rebuilt
2026-08-23 via PR #442 (Batch 4 of the Bank-pattern conversion project) from an older
hardcoded-field-id pattern to the label-driven, properties-file-driven, T2-consolidated shape
used by `bank_page.resource`. The `playwright/` and `investigation/` folders in this bundle are a
**historical reference** from the original 2026-06-11 build, predating the RF conversion — left
untouched by this backfill, not re-run, not the source of truth going forward.

## Layout
- `cost_object_mapping_sow.md` — statement of work / spec (refreshed 2026-08-28 to reflect the
  current RF-only implementation).
- `JOURNAL.md` — work journal (added 2026-08-28 backfill).
- `CHECKLIST.md` — deliverable checklist (added 2026-08-28 backfill).
- `playwright/`, `investigation/`, `evidence/*.png`/`results.json` — legacy 2026-06-11 Playwright
  bundle, kept as historical reference, unmodified by this backfill.
- `evidence/backfill_2026-08-28/` — fresh dryrun + live re-run of the current RF suite, captured
  by this backfill.

## Run — Robot Framework (the current, maintained automation for this screen)
```bash
# from workstreams/master-plan/ec-automation/

# 1. dryrun (structure only, no browser/DB)
py -m robot --dryrun --outputdir tmp_dryrun tests/Configuration/Assets/Financial_Objects/cost_object_mapping_iud.robot

# 2. live headless run (real browser, real DB writes, self-cleaning — TC05 deletes the fixed
#    AUTOTEST_CMAP code so the next run starts clean)
EC_HEADLESS=true py -m robot --outputdir tmp_live tests/Configuration/Assets/Financial_Objects/cost_object_mapping_iud.robot

# 3. live headed run (visible browser, for a watched demo)
EC_HEADLESS=false py -m robot --outputdir tmp_live tests/Configuration/Assets/Financial_Objects/cost_object_mapping_iud.robot
```

## DB self-clean check (ground truth — `OV_FIN_COST_OBJECT`)
Run from a fresh connection (never reuse a mid-test session), to confirm the fixed test code
(`AUTOTEST_CMAP`) is absent and no `AUTOTEST%` residual rows exist:
```sql
SELECT COUNT(*) FROM OV_FIN_COST_OBJECT WHERE CODE = 'AUTOTEST_CMAP';   -- expect 0
SELECT CODE, NAME FROM OV_FIN_COST_OBJECT WHERE UPPER(CODE) LIKE 'AUTOTEST%' OR UPPER(NAME) LIKE 'AUTOTEST%';  -- expect no rows
```
(Uses `EC_DB_USER`/`EC_DB_PASS`/`EC_DB_DSN` env vars, sandbox defaults `ECKERNEL_EC`/`energy`/
`localhost:1521/ORCL`, per `libraries/DbVerify.py`/`resources/environment.py`.)

## Key facts
- No navigator — plain OV, only the universal Date+GO as-at-date bar (no mandatory nav dropdown).
- Insert/update fields use generic **"Code"/"Name"** labels (like Bank), not screen-prefixed
  labels (unlike Area/Tank's "Area Code"/"Tank Code").
- 4 mandatory reference dropdowns: Object Type, Cost Object (CASCADE — depends on Start Date +
  Object Type both being set first), Company, Distribution Object Type. All 4 use real literal
  option text, not `__FIRST__`.
- The RF suite uses the FIXED test code `AUTOTEST_CMAP` (not a per-run timestamp).
- Grid columns: Code, Name, Start Date (3-column, Bank convention).

## Equivalent RF files (outside this bundle, treeview-mirrored)
- T3 page object: `pageobjects/Configuration/Assets/Financial_Objects/cost_object_mapping_page.resource`
- Suite: `tests/Configuration/Assets/Financial_Objects/cost_object_mapping_iud.robot`
- Test data: `testdata/cost_object_mapping_{insert,update,form_verify,grid_verify}.properties`
- KB selector map: `ec-ui-knowledge/screens/cost_object_mapping.md`
