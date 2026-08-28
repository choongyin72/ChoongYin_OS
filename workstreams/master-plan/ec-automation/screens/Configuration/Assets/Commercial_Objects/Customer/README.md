# Customer — IUD automation bundle

Screen: Configuration > Assets > Commercial Objects > Customer.
**Plain Bank-pattern OV (Manage-Object), no navigator.** DELETE = **End Date = Start Date**
(zero-length window) — EC true delete (object removed from `OV_CUSTOMER`).

The RF suite is the primary, currently-maintained automation (converted to the Bank pattern via
PR #435, merged 2026-08-23). The Playwright reference flow (`playwright/ec_iud_customer.py`,
2026-06-12) is a legacy artifact, permanently waived from future rebuilds per
`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H, and unchanged by this backfill.

## RF suite (primary)
- T3 page object: `pageobjects/Configuration/Assets/Commercial_Objects/customer_page.resource`
- Suite: `tests/Configuration/Assets/Commercial_Objects/customer_iud.robot`
- Test data: `testdata/customer_insert.properties`, `customer_update.properties`,
  `customer_form_verify.properties`, `customer_grid_verify.properties`
- Credentials: `CUSTOMER_EC_USER` / `CUSTOMER_EC_PASS` in `resources/credentials.py` (defaults to
  `EC_USER`/`EC_PASS`, which default to `sysadmin`/`sysadmin`)

### Run commands (from `workstreams/master-plan/ec-automation/`)
```bash
# Dry-run parse check (fast, no browser/DB)
py -m robot --dryrun --outputdir /tmp/customer_dryrun tests/Configuration/Assets/Commercial_Objects/customer_iud.robot

# Live headless run (real EC + DB)
EC_HEADLESS=true py -m robot --outputdir results/customer tests/Configuration/Assets/Commercial_Objects/customer_iud.robot

# robocop
py -m robocop check pageobjects/Configuration/Assets/Commercial_Objects/customer_page.resource tests/Configuration/Assets/Commercial_Objects/customer_iud.robot
```

DB self-clean check (fresh connection, run AFTER the live suite completes) — use a scratch
script (never inline `-c`), e.g. `Workplaces/<task>/dbcheck.py`:
```python
import oracledb
conn = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM OV_CUSTOMER WHERE CODE = 'AUTOTEST_CUST'")
print(cur.fetchone()[0])   # expect 0
conn.close()
```
Run with `py Workplaces/<task>/dbcheck.py`.

## Legacy Playwright reference (unchanged)
```bash
py -X utf8 playwright/ec_iud_customer.py
EC_HEADED=1 EC_SLOWMO=400 py -X utf8 playwright/ec_iud_customer.py   # watchable
```

## Folder
- `customer_sow.md` — statement of work / spec (updated 2026-08-28 for the RF conversion)
- `JOURNAL.md` — work journal (backfilled 2026-08-28 from PR #435's body)
- `evidence/` — `customer_*.png` + `customer_results.json` (legacy Playwright run, 2026-06-12);
  `rf_backfill_2026-08-28/` (RF suite re-run evidence: log.html/report.html/output.xml/summary)
- `investigation/` — recon scripts used to learn the screen (legacy, Playwright-era)
- `playwright/ec_iud_customer.py` — thin config over the shared engine (legacy)
- `CHECKLIST.md` — `docs/IUD-DELIVERABLE-CHECKLIST.md` copy, ticked with real evidence

## KB selector map
`ec-ui-knowledge/screens/customer.md` (repo root) — nav path, DB view, grid id, insert/update/
delete selectors, mandatory-yellow fields, quirks.
