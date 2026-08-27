# Operator Route - EC Object IUD bundle

**Screen:** Configuration > Assets > Facility_Objects > Operator Route (BF CO.0244). OV-GM (grid
`manageObject:form:T_data`), navigator-GATED (mandatory 2-level Production Unit -> Area cascade +
GO), date-effective. See `operator_route_sow.md`, `JOURNAL.md`, `CHECKLIST.md`.

**RF automation (current, post PR #533 Area-pattern conversion - this bundle documents it, does
not rebuild it):**
- T3 `pageobjects/Configuration/Assets/Facility_Objects/operator_route_page.resource`
- Suite `tests/Configuration/Assets/Facility_Objects/operator_route_iud.robot` (5 TCs: Verify Clean
  State, Insert, Update, Find, Delete)
- `testdata/operator_route_{navigator,insert,update,form_verify,grid_verify}.properties`

**Playwright driver (unchanged since 2026-08-01, waived from further change - Universal Screen
Engine is the owner-decided replacement going forward):** `py/operator_route_iud.py`.

## Run commands

All commands run from `workstreams/master-plan/ec-automation/`.

```bash
# Dry-run (syntax/collision check, no browser)
robot --dryrun --outputdir results/or_dryrun tests/Configuration/Assets/Facility_Objects/operator_route_iud.robot

# Live headless run (EC sandbox, screenshots + log/report/output.xml under --outputdir)
EC_HEADLESS=true robot --outputdir results/or_live tests/Configuration/Assets/Facility_Objects/operator_route_iud.robot

# Live headed run (visible browser, for manual eyeballing)
EC_HEADLESS=false robot --outputdir results/or_live tests/Configuration/Assets/Facility_Objects/operator_route_iud.robot
```

## DB self-clean check pattern

Fixed test code `AUTOTEST_OR` must be 0 rows in `OV_OPERATOR_ROUTE` both BEFORE and AFTER a run
(the suite's own TC05 Delete + TC01 Verify Clean State already enforce this in-suite; this is the
independent, fresh-connection re-check):

```sql
SELECT COUNT(*) FROM OV_OPERATOR_ROUTE WHERE CODE LIKE 'AUTOTEST_OR%';
```

Run via a fresh `oracledb` connection (not the same session the suite used), e.g.:

```python
import oracledb
conn = oracledb.connect(user='ECKERNEL_EC', password='energy', dsn='localhost:1521/ORCL')
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM OV_OPERATOR_ROUTE WHERE CODE LIKE 'AUTOTEST%'")
print(cur.fetchone())  # expect (0,)
```

## Folder
- `operator_route_sow.md` - SOW: classification, nav/grid/cell shape, test data, dev story.
- `JOURNAL.md` - per-branch work journal (base build 2026-08-01 + Area-pattern conversion 2026-08-26,
  backfilled 2026-08-27).
- `evidence/` - `results.json` + screenshots from the 2026-08-01 base-build Playwright run (8/8),
  plus `rf_2026-08-27/` (log.html/report.html/output.xml/screenshots/results.json) from this
  backfill's one-time live RF re-run (5/5) of the already-proven, already-merged Area-pattern suite.
- `investigation/` - `recon.py`, the read-only recon script from the 2026-08-01 base build (kept;
  item 5 of the deliverable checklist stays waived for Bank-/Area-pattern work per Section H).
- `CHECKLIST.md` - the full `docs/IUD-DELIVERABLE-CHECKLIST.md`, ticked with real evidence.
- `VERIFY-REPORT.md` - auto-generated 2026-08-01 (base-build 4-TC gates only; see `CHECKLIST.md`
  for the current 5-TC gate evidence re-run for this backfill).
