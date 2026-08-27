# Contract Capacity - EC Object IUD bundle

**Screen:** Configuration > Assets > Contract_Objects > Contract Capacity (BF CO.2044). OV-GM
(grid `manageObject:form:T_data`), single-Business-Unit-dropdown navigator-GATED, date-effective.
Converted to the **Area pattern** (2026-08-26, PR #535): 5-TC RF suite, per-TC login/logout,
properties-file-driven, pure-screen verification. See `contract_capacity_sow.md`, `JOURNAL.md`,
`CHECKLIST.md`, `VERIFY-REPORT.md` (original 2026-08-01 build gate, pre-Area-conversion).

RF: T3 `pageobjects/Configuration/Assets/Contract_Objects/contract_capacity_page.resource` +
suite `tests/Configuration/Assets/Contract_Objects/contract_capacity_iud.robot`. Playwright driver
`py/contract_capacity_iud.py` is historical/pre-existing (2026-08-01), left UNTOUCHED by the
Area-pattern conversion and by this backfill — no new Playwright bundle is built for Area-pattern
work (owner decision 2026-08-27, Universal Screen Engine replaces that role).

## Commands

Run from `workstreams/master-plan/ec-automation/`.

**Dryrun** (resolution check, no live browser):
```bash
robot --dryrun tests/Configuration/Assets/Contract_Objects/contract_capacity_iud.robot
```
Expected: 5 tests, 5 passed, 0 failed.

**Live headless run:**
```bash
EC_HEADLESS=true robot --outputdir <outdir> tests/Configuration/Assets/Contract_Objects/contract_capacity_iud.robot
```
Expected: 5 tests, 5 passed, 0 failed (TC01 Verify Clean State, TC02 Insert, TC03 Update,
TC04 Find, TC05 Delete).

**DB self-clean check** (fresh oracledb connection, run AFTER the live suite):
```python
import oracledb, os
conn = oracledb.connect(
    user=os.environ.get("EC_DB_USER", "ECKERNEL_EC"),
    password=os.environ.get("EC_DB_PASS", "energy"),
    dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"),
)
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM OV_CONTRACT_CAPACITY WHERE CODE LIKE 'AUTOTEST%'")
print(cur.fetchone()[0])  # expect 0
conn.close()
```

## Bundle contents
- `contract_capacity_sow.md` — SOW (classification, nav/grid/cell shape, dev story).
- `JOURNAL.md` — work journal (original build + Area-pattern conversion + this backfill).
- `CHECKLIST.md` — 21-item deliverable checklist against `docs/IUD-DELIVERABLE-CHECKLIST.md`.
- `VERIFY-REPORT.md` — auto-generated gate report from the original 2026-08-01 build (4-TC shape;
  predates PR #535's 5-TC conversion — see JOURNAL for the current 5/5 evidence).
- `evidence/` — screenshots + `results.json` from the 2026-08-01 build, plus
  `evidence/backfill_2026-08-28/` (dryrun 5/5, live retry 5/5 `output.xml`/`log.html`/
  `report.html`, DB self-clean 0, and the honestly-disclosed attempt-1 TC05 flake).
- `investigation/recon.py` — pre-existing read-only recon script (2026-08-01 build). The live
  Playwright driver itself lives outside this bundle at `py/contract_capacity_iud.py`.
