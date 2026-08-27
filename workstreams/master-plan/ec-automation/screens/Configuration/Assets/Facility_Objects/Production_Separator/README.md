# Production Separator - EC Object IUD bundle

**Screen:** Configuration > Assets > Facility_Objects > Production Separator (BF CO.0042). OV-GM
(grid `manageObject:form:T_data`), navigator-GATED, date-effective. **Area-pattern** RF suite
(5 TCs, per-TC login/logout, properties-file-driven) since PR #551 (merged 2026-08-26). See
`production_separator_sow.md` (classification/nav/mandatory-fields/dev-story), `JOURNAL.md`
(what actually happened, both builds), `CHECKLIST.md` (21-item gate evidence).

Driver `py/production_separator_iud.py` is pre-existing, unchanged since 2026-07-30 and waived
from further build (Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md` - the Universal Screen Engine
is the owner-decided replacement for hand-written Playwright drivers going forward). The RF suite
is the maintained/live test.

## Files
- T3: `pageobjects/Configuration/Assets/Facility_Objects/production_separator_page.resource`
- Suite: `tests/Configuration/Assets/Facility_Objects/production_separator_iud.robot`
- Testdata: `testdata/production_separator_{navigator,insert,update,form_verify,grid_verify}.properties`
- Credentials: `PRODUCTION_SEPARATOR_EC_USER`/`PRODUCTION_SEPARATOR_EC_PASS` in `resources/credentials.py`

## Commands (run from `workstreams/master-plan/ec-automation/`)

Dryrun (structure-only, no live browser):
```
py -m robot --dryrun tests/Configuration/Assets/Facility_Objects/production_separator_iud.robot
```

Live headless run:
```
EC_HEADLESS=true py -m robot tests/Configuration/Assets/Facility_Objects/production_separator_iud.robot
```

Live headed run (visible browser, for demo/debug):
```
py -m robot tests/Configuration/Assets/Facility_Objects/production_separator_iud.robot
```

DB self-clean check (fresh connection, after a live run - `AUTOTEST_PSEP` and any residual
`AUTOTEST%` row in `OV_PRODSEPARATOR` must both be 0; confirmed live via a standalone oracledb
script against the environment's `EC_DB_USER`/`EC_DB_PASS`/`EC_DB_DSN` - see
`libraries/DbVerify.py` for the standard connection pattern):
```sql
SELECT COUNT(*) FROM OV_PRODSEPARATOR WHERE CODE = 'AUTOTEST_PSEP';
SELECT COUNT(*) FROM OV_PRODSEPARATOR WHERE CODE LIKE 'AUTOTEST%';
```
Both must return 0 after TC05 (Delete) completes.

## Evidence
- `evidence/psep_0[1-5]_*.png` + `evidence/results.json` - original 2026-07-30 build (pre-Area-
  pattern, Playwright + old 4-TC RF).
- `evidence/backfill_2026-08-27/` - this backfill's fresh dryrun + live re-run of the CURRENT
  (PR #551) 5-TC Area-pattern suite, plus the DB self-clean result.
