# Calendar Collection IUD bundle (CD.0105)

Configuration > Assets > Date Objects > Calendar Collection. Custom-URL OV (Manage-Object,
date-effective) screen — grid `nav:form:T_data`, NO navigator GO (toolbar Refresh via T2's
`Save And Refresh List` auto-fallback). Full Insert / Update / Find / Delete, DB-verified and
self-cleaning.

**Current pattern (since PR #449, 2026-08-23, Batch 6):** label-driven, properties-file-driven,
T2-consolidated Bank pattern (mirrors `bank_page.resource`/`calendar_page.resource`). This bundle
predated the lean-deliverable rule and PR #449's own conversion, so its docs were backfilled
2026-08-27/28 (`docs/lean-deliverable-backfill-workorder.md`, Batch 8) to describe the current
state — no RF automation files were changed by this backfill.

## Files
- `calendar_collection_sow.md` -- SOW (classification, form layout, test data, dev story — covers
  both the original PR #144 build and the PR #449 Bank-pattern conversion).
- `CHECKLIST.md` -- the IUD deliverable checklist (Section H shape), ticked with evidence.
- `JOURNAL.md` -- per-branch work journal.
- `playwright/ec_iud_calendar_collection.py` -- ORIGINAL freestyle Playwright reference flow
  (screenshots + results.json), predates PR #449; left untouched (items 4/5 stay permanently
  waived for Bank-pattern work per Section H — the Universal Screen Engine replaces this role).
- `investigation/` -- read-only DOM recon from the original build (New-Object form fields +
  METHOD dropdown labels); left untouched.
- `evidence/` -- ORIGINAL 11 step screenshots + `results.json` from the PR #144 Playwright run,
  PLUS a new `rf_backfill_2026-08-28/` subfolder with this backfill's live RF run (20 screenshots
  + `output.xml` + `RESULTS.md`).

## Run commands
RF suite (the DB-verified, self-cleaning proof — CURRENT automation) — from
`workstreams/master-plan/ec-automation/`:
```
# dryrun
robot --dryrun tests/Configuration/Assets/Date_Objects/calendar_collection_iud.robot

# live headless (the proof)
EC_HEADLESS=true robot --outputdir results tests/Configuration/Assets/Date_Objects/calendar_collection_iud.robot
```

DB self-clean check pattern (independent fresh connection, separate from the RF suite's own
in-run `DbVerify` calls):
```python
import oracledb, os
conn = oracledb.connect(
    user=os.environ.get("EC_DB_USER", "ECKERNEL_EC"),
    password=os.environ.get("EC_DB_PASS", "energy"),
    dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"),
)
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM OV_CALENDAR_COLLECTION WHERE CODE = 'AUTOTEST_CALENDAR_COLLECTION'")
print(cur.fetchone()[0])  # expect 0 after a completed suite run
```

Playwright reference flow (ORIGINAL, pre-conversion; generates the older `evidence/` screenshots)
-- from repo root, left as historical reference only:
```
EC_HEADED=1 EC_CODE=AUTOTEST_CC_PW01 py "workstreams/master-plan/ec-automation/screens/Configuration/Assets/Date_Objects/Calendar_Collection/playwright/ec_iud_calendar_collection.py"
```

Read-only recon (ORIGINAL, never saves):
```
SCREEN="Calendar Collection" py tmp/scripts/scan_ec_screen.py
py "workstreams/master-plan/ec-automation/screens/Configuration/Assets/Date_Objects/Calendar_Collection/investigation/recon_new_object_form.py"
py "workstreams/master-plan/ec-automation/screens/Configuration/Assets/Date_Objects/Calendar_Collection/investigation/recon_method_dropdown.py"
```

## Credentials
Read from env — RF uses `CALENDAR_COLLECTION_EC_USER`/`CALENDAR_COLLECTION_EC_PASS` (dedicated
per-screen pair, added additively to `resources/credentials.py` in PR #449). Playwright reads
`EC_USER`/`EC_PASS` (default `sysadmin`/`sysadmin`). Never hardcoded (R16).

## DB ground truth
`OV_CALENDAR_COLLECTION` (`Code Should Be Present/Absent In View`). DELETE = End Date = Start Date
removes the object from the OV view (verified, both at original build and at this backfill's
independent re-check 2026-08-28). Base `CALENDAR_COLLECTION`/`CALENDAR_COLL_VERSION` retains
expired rows by design. 7 pre-existing rows in `OV_CALENDAR_COLLECTION`, confirmed unchanged.
