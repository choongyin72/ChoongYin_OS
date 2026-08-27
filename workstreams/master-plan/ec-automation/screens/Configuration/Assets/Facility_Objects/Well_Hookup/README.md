# Well Hookup - EC Object IUD bundle

**Screen:** Configuration > Assets > Facility_Objects > Well Hookup (BF CO.0108). OV-GM (grid
`manageObject:form:T_data`), navigator-GATED (3-level Production Unit -> Area -> Facility Class 1
cascade + GO), date-effective. Base build 2026-07-30 (item-1 gated-navigator capability, PR #244);
converted to Area's full pattern 2026-08-26 (PR #539). See `well_hookup_sow.md` (classification +
dev story), `JOURNAL.md` (per-branch history), `CHECKLIST.md` (deliverable gate evidence).

- **RF T3:** `pageobjects/Configuration/Assets/Facility_Objects/well_hookup_page.resource`
- **RF suite:** `tests/Configuration/Assets/Facility_Objects/well_hookup_iud.robot` (5 TCs:
  Verify Clean State / Insert / Update / Find / Delete)
- **Legacy Playwright driver (unchanged, not the current delivery path):** `py/well_hookup_iud.py`
- **Navigator values:** `testdata/well_hookup_navigator.properties`
- **Test data:** `testdata/well_hookup_{insert,update,form_verify,grid_verify}.properties`
- **DB view (ground truth):** `OV_WELL_HOOKUP` (versioned; key `CODE`)

## Run commands

All commands run from `workstreams/master-plan/ec-automation/`.

Dryrun (parse + keyword resolution only, no live EC):
```
robot --dryrun --test "*Well Hookup*" tests/
```

Live headless run:
```
EC_HEADLESS=true robot -d <output-dir> tests/Configuration/Assets/Facility_Objects/well_hookup_iud.robot
```

Live headed run (visible browser):
```
EC_HEADLESS=false robot -d <output-dir> tests/Configuration/Assets/Facility_Objects/well_hookup_iud.robot
```

## DB self-clean check pattern (fresh connection, run AFTER a live suite pass)

```python
import oracledb
conn = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM OV_WELL_HOOKUP WHERE CODE LIKE 'AUTOTEST%'")
print(cur.fetchone()[0])   # expect 0 - the fixed test code AUTOTEST_WH must always end deleted
conn.close()
```

Grid-filter wiring fired check (confirms `Find/Clear Well Hookup Row By Filter` actually ran, not
just present in source):
```
grep -c "Find Object Row By Filter" <output-dir>/output.xml
```

## Robocop / hygiene

```
py -m robocop check pageobjects/Configuration/Assets/Facility_Objects/well_hookup_page.resource tests/Configuration/Assets/Facility_Objects/well_hookup_iud.robot
py scripts/check_bundle_hygiene.py
```
