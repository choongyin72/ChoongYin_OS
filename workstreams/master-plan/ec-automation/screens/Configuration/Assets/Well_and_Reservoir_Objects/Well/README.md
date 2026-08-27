# Well - IUD bundle

**Screen:** Configuration > Assets > Well_and_Reservoir_Objects > Well (BF CO.0049). OV-GM (grid
`manageObject:form:T_data`) with a 5-dd navigator - only the standard 3-level cascade is needed,
filled with SPECIFIC P1 values (2nd-row Well filter dds left empty; owner screenshot ground truth).
View `OV_WELL` (versioned, confirmed via 'P1 W001 OP'). Date-effective; DELETE = End Date = Start
Date.

Converted to the Area-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE by PR #540
(2026-08-26) - see `JOURNAL.md` for the full history, including Well's earlier role as a
regression canary for the shared `Apply Navigator From Properties` keyword.

- **Playwright driver:** `py/well_iud.py` (thin, shared engine; screen-local
  `apply_well_navigator` with specific P1 values + GO) - unchanged by PR #540, which was an
  RF-only structural conversion.
- **RF:** T3 `pageobjects/Configuration/Assets/Well_and_Reservoir_Objects/well_page.resource`
  (navigator fill now delegates to the shared T2 `Apply Navigator From Properties` in
  `resources/manage_object.resource`, driven by `testdata/well_navigator.properties` - replacing
  the base build's own screen-local `Apply Well Navigator` T3 keyword) + suite
  `tests/Configuration/Assets/Well_and_Reservoir_Objects/well_iud.robot` (5 TCs, per-TC
  login/logout, fixed test code `AUTOTEST_WELL`, zero inline DB-verify calls - DB check lives in
  the shared T2 `Verify Object Removed`).
- **Insert extras:** Well Type first-available (`__FIRST__` sentinel). Start Date 2020-01-01
  (DB-checked).
- **Legacy verify record:** `VERIFY-REPORT.md` in this folder is the ORIGINAL 2026-07-30
  `verify_screen.py` auto-generated report (robocop 0 / hygiene 0 / dryrun 4/4 / live RF 4/4 /
  Playwright 8/8) - predates the 5-TC conversion; kept as historical record, not re-generated
  because `verify_screen.py` was written against the older 4-TC shape. Fresh evidence for the
  current 5-TC suite is in `evidence/` (this backfill, 2026-08-27).

## Commands

Dryrun (single suite):
```
cd workstreams/master-plan/ec-automation
robot --dryrun tests/Configuration/Assets/Well_and_Reservoir_Objects/well_iud.robot
```

Live headless run:
```
cd workstreams/master-plan/ec-automation
EC_HEADLESS=true robot --outputdir <out-dir> tests/Configuration/Assets/Well_and_Reservoir_Objects/well_iud.robot
```

DB self-clean check (fresh connection, run AFTER the live run - expect 0 rows once TC05 Delete has
completed):
```
py -c "import oracledb; c=oracledb.connect(user='ECKERNEL_EC', password='energy', dsn='localhost:1521/ORCL'); cur=c.cursor(); cur.execute(\"SELECT COUNT(*) FROM OV_WELL WHERE CODE='AUTOTEST_WELL'\"); print(cur.fetchone()[0]); c.close()"
```
(In practice, write this to a scratch `.py` file under `Workplaces/<task>/` per repo convention -
never `py -c` inline in a committed script; shown inline here only as the illustrative one-liner.)

Full-tree regression dryrun (confirms zero collisions from Well's fixed test code / shared
keyword usage):
```
cd workstreams/master-plan/ec-automation
robot --dryrun tests/
```
