# Royalty Depositor - IUD bundle

Configuration > Assets > Royalty Objects > **Royalty Depositor** (RC.0052).
Manage-Object (OV) screen, Bank family. DELETE = End Date = Start Date (true delete in `OV_ROYALTY_DEPOSITOR`).

**Current RF automation is the Bank-pattern conversion delivered by PR #448 (merged 2026-08-23,
Batch 5 of the Bank-pattern conversion project).** This bundle's documentation/evidence artifacts
were backfilled 2026-08-28 (`docs/lean-deliverable-backfill-workorder.md` Batch 8, per the
2026-08-27 owner decision retiring the Section G lean waiver) — the RF suite itself was **not**
touched by the backfill.

## Contents
- `royalty_depositor_sow.md` - Statement of Work (recon + design + acceptance criteria; updated
  2026-08-28 to describe the current Bank-pattern RF implementation).
- `README.md` - this file.
- `JOURNAL.md` - work journal for the PR #448 conversion, backfilled 2026-08-28 from the PR's own
  body/commit history.
- `CHECKLIST.md` - `docs/IUD-DELIVERABLE-CHECKLIST.md` copy, ticked with real evidence.
- `playwright/ec_iud_royalty_depositor.py` - legacy freestyle Playwright IUD walkthrough
  (pre-dates PR #448; kept as a reference only — new Playwright drivers are waived in favour of
  the Universal Screen Engine, owner decision 2026-08-27).
- `evidence/2026-08-28-live-run/` - log.html/report.html/output.xml + step screenshots +
  Browser-library playwright log from the 2026-08-28 backfill live confirmation run (5/5 PASS).
  Earlier screenshots directly under `evidence/` predate PR #448 and are kept as historical
  reference for the pre-conversion driver.

## RF suite (the proof — unchanged by this backfill)
- T3 page object: `pageobjects/Configuration/Assets/Royalty_Objects/royalty_depositor_page.resource`
- Test suite:     `tests/Configuration/Assets/Royalty_Objects/royalty_depositor_iud.robot`
- Testdata:       `testdata/royalty_depositor_{insert,update,form_verify,grid_verify}.properties`
- Reuses T2 `resources/manage_object.resource` + T1 `resources/common.resource` + `libraries/DbVerify.py` (no shared-file edits).
- Fixed test code: `AUTOTEST_ROYALTY_DEP` (matches Bank/Account's own convention — NOT a
  per-run-generated `AUTOTEST_RD_<run>` code; every run must complete TC05 so the code stays free
  for the next run).

## Run

```bash
# From the ec-automation root (workstreams/master-plan/ec-automation):

# Dryrun (syntax/keyword-resolution check, no browser/DB):
robot --dryrun --outputdir results tests/Configuration/Assets/Royalty_Objects/royalty_depositor_iud.robot

# Live headless run (the proof):
EC_HEADLESS=true robot --outputdir results tests/Configuration/Assets/Royalty_Objects/royalty_depositor_iud.robot

# Live headed run (visual confirmation):
EC_HEADLESS=false robot --outputdir results tests/Configuration/Assets/Royalty_Objects/royalty_depositor_iud.robot

# Legacy Playwright walkthrough (reference/demo only, screenshots):
EC_HEADED=1 py -X utf8 screens/Configuration/Assets/Royalty_Objects/Royalty_Depositor/playwright/ec_iud_royalty_depositor.py
```

## DB self-clean check (fresh connection, after any live run)

```python
import oracledb
conn = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM OV_ROYALTY_DEPOSITOR WHERE CODE = 'AUTOTEST_ROYALTY_DEP'")
print("residual rows:", cur.fetchone()[0])   # must be 0 after a completed run
conn.close()
```

Env: sandbox web `https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/` (`sysadmin`/`sysadmin`),
DB `localhost:1521/ORCL` (`ECKERNEL_EC`/`energy`). Test data `AUTOTEST_ROYALTY_DEP` only; self-cleaning.
