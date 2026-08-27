# External Location - EC Object IUD bundle

**Screen:** Configuration > Assets > Facility_Objects > External Location (BF CO.0227). OV-GM (grid
`manageObject:form:T_data`), zero-mandatory-nav edge case (GO only, no mandatory navigator scope),
date-effective. See `external_location_sow.md` (classification + dev story), `JOURNAL.md` (work
history), `CHECKLIST.md` (21-item deliverable status). Driver `py/external_location_iud.py`
(untouched since 2026-08-01); RF T3/suite converted to Area's 5-TC pattern by PR #524/#528
(2026-08-26).

## Files
- T3 page object: `pageobjects/Configuration/Assets/Facility_Objects/external_location_page.resource`
- Suite: `tests/Configuration/Assets/Facility_Objects/external_location_iud.robot` (5 TCs)
- Test data: `testdata/external_location_{navigator,insert,update,form_verify,grid_verify}.properties`
- Credentials: `EXTERNAL_LOCATION_EC_USER`/`EXTERNAL_LOCATION_EC_PASS` in `resources/credentials.py`
- Playwright driver (pre-existing, not part of the RF conversion): `py/external_location_iud.py`
- KB selector map: `ec-ui-knowledge/screens/external_location.md`

## How to run

All commands run from `workstreams/master-plan/ec-automation/`.

**Dryrun (full tree, checks for suite/variable/test-code collisions):**
```
robot --dryrun --outputdir <out-dir> tests/
```

**Live headless run (this screen only):**
```
EC_HEADLESS=true robot --outputdir <out-dir> tests/Configuration/Assets/Facility_Objects/external_location_iud.robot
```

**Live headed run (visual confirmation):**
```
EC_HEADLESS=false robot --outputdir <out-dir> tests/Configuration/Assets/Facility_Objects/external_location_iud.robot
```

**DB self-clean check (fresh connection, after any live run - the suite's own TEST_CODE is fixed
`AUTOTEST_EXTERNAL_LOCATION`, so this must read 0 both before and after a clean run):**
```sql
SELECT COUNT(*) FROM OV_EXTERNAL_LOCATION WHERE CODE LIKE 'AUTOTEST_EXTERNAL_LOCATION%';
```
Via Python (`oracledb`, env vars `EC_DB_USER`/`EC_DB_PASS`/`EC_DB_DSN`, default
`ECKERNEL_EC`/`energy`/`localhost:1521/ORCL`):
```python
import os, oracledb
conn = oracledb.connect(user=os.environ.get("EC_DB_USER", "ECKERNEL_EC"),
                         password=os.environ.get("EC_DB_PASS", "energy"),
                         dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"))
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM OV_EXTERNAL_LOCATION WHERE CODE LIKE 'AUTOTEST_EXTERNAL_LOCATION%'")
print(cur.fetchone()[0])
```

**Hygiene (repo-wide, run from repo root):**
```
py scripts/check_bundle_hygiene.py
```
