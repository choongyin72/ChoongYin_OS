# Storage — EC Object IUD bundle

**Screen:** Configuration > Assets > Tank_and_Storage_Objects > Storage (BF CO.0034). OV-GM
(manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED (3-level
Production Unit -> Area -> Facility Class 1 cascade + GO), date-effective. Converted to the full
Area pattern in PR #537 (merged 2026-08-26); see `storage_sow.md` for the classification/nav/grid
details and `JOURNAL.md` for the conversion narrative. This bundle backfills the documentation/
evidence artifacts the 2026-08-23/26 lean waiver skipped — it does not change any RF file.

## Files
- **RF T3 (page object):** `pageobjects/Configuration/Assets/Tank_and_Storage_Objects/storage_page.resource`
- **RF suite:** `tests/Configuration/Assets/Tank_and_Storage_Objects/storage_iud.robot`
- **Test data:** `testdata/storage_{navigator,insert,update,form_verify,grid_verify}.properties`
- **Playwright driver (pre-existing, waived — not touched):** `py/storage_iud.py`
- **KB selector map:** `ec-ui-knowledge/screens/storage.md`

## Run — dryrun (syntax/keyword check, no browser)
```bash
cd workstreams/master-plan/ec-automation
robot --dryrun --outputdir <outdir> tests/Configuration/Assets/Tank_and_Storage_Objects/storage_iud.robot
```

## Run — live headless
```bash
cd workstreams/master-plan/ec-automation
EC_HEADLESS=true robot --outputdir <outdir> tests/Configuration/Assets/Tank_and_Storage_Objects/storage_iud.robot
```

## Run — live headed (visible browser)
```bash
cd workstreams/master-plan/ec-automation
EC_HEADLESS=false robot --outputdir <outdir> tests/Configuration/Assets/Tank_and_Storage_Objects/storage_iud.robot
```

## DB self-clean check (fresh connection, after a run)
```bash
py -c "
import oracledb
conn = oracledb.connect(user='ECKERNEL_EC', password='energy', dsn='localhost:1521/ORCL')
cur = conn.cursor()
cur.execute(\"SELECT CODE, OBJECT_START_DATE, OBJECT_END_DATE FROM OV_STORAGE WHERE CODE LIKE 'AUTOTEST%'\")
for row in cur:
    print(row)
conn.close()
"
```
No output (empty result set) = 0 residual `AUTOTEST%` rows in `OV_STORAGE`. TC05 (Delete) must
complete for `AUTOTEST_STG` (the fixed test code) to be free again for the next run.

## Notes
- Test code is FIXED (`AUTOTEST_STG`), not generated/timestamped — a run that fails before TC05
  deletes it will leave it occupied for the next run; check the DB query above before re-running.
- The 3-level navigator cascade + GO must complete (`Open Storage Screen With Navigator Values
  Populated`) before the grid is populated at all — every TC does this via `Login To EC
  Application` -> `Open Storage Screen With Navigator Values Populated`.
