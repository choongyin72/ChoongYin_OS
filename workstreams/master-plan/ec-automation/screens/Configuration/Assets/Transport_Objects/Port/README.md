# Port (CO.2003) — OV IUD bundle

_Backfilled 2026-08-28 (Batch 10, `docs/lean-deliverable-backfill-workorder.md`) — documentation/
evidence around already-working, already-merged automation (PR #465). No automation files touched
by this backfill._

Manage-Object (OV) screen: **Configuration > Assets > Transport Objects > Port**. Full Bank-pattern
conversion (PR #465, Batch 9, 2026-08-23): label-driven, properties-file-driven Insert/Update/Verify,
explicit grid-filter wiring — matches `bank_page.resource`/`berth_page.resource` exactly. Full
Insert/Update/Delete (End Date = Start Date), DB-verified against `OV_PORT`, self-cleaning.

## Artifacts
- **SOW:** `port_sow.md`
- **RF T3:** `../../../../pageobjects/Configuration/Assets/Transport_Objects/port_page.resource`
- **RF suite:** `../../../../tests/Configuration/Assets/Transport_Objects/port_iud.robot`
- **Testdata:** `../../../../testdata/port_{insert,update,form_verify,grid_verify}.properties`
- **Playwright driver (unchanged, out of scope for this backfill):** `../../../../py/port_iud.py`
- **investigation/** recon.py (2026-07-26, pre-conversion recon; kept as historical record)
- **evidence/** — `port_0[1-5]_*.png` + `rf_report.html` (2026-07-26, pre-conversion Playwright/RF
  run, kept as historical record) PLUS `TC0[1-5] *.png` + `log.html`/`output.xml`/`report.html`
  (2026-08-28, this backfill's fresh live RF re-run against the current Batch-9 shape)
- **CHECKLIST.md** — this bundle's 21-item deliverable checklist, ticked with real evidence
- **JOURNAL.md** — built / done-well / lessons / decisions / evidence, covering both the original
  build and the Batch-9 conversion
- **VERIFY-REPORT.md** — the ORIGINAL 2026-07-26 auto-generated `verify_screen.py` report (predates
  Batch 9; kept as historical record, not re-run by this backfill — see CHECKLIST.md for the fresh
  gate evidence gathered directly instead)

## Run

Dryrun:
```
cd workstreams/master-plan/ec-automation
py -m robot --dryrun --outputdir <outdir> tests/Configuration/Assets/Transport_Objects/port_iud.robot
```

Live headless run:
```
cd workstreams/master-plan/ec-automation
EC_HEADLESS=true py -m robot --outputdir screens/Configuration/Assets/Transport_Objects/Port/evidence tests/Configuration/Assets/Transport_Objects/port_iud.robot
```

robocop (T3 + suite):
```
py -m robocop check workstreams/master-plan/ec-automation/pageobjects/Configuration/Assets/Transport_Objects/port_page.resource workstreams/master-plan/ec-automation/tests/Configuration/Assets/Transport_Objects/port_iud.robot
```

Hygiene:
```
py scripts/check_bundle_hygiene.py --bundle workstreams/master-plan/ec-automation/screens/Configuration/Assets/Transport_Objects/Port
```

DB self-clean check (fresh connection; relies on `libraries/DbVerify.py` defaults —
`EC_DB_USER`/`EC_DB_PASS`/`EC_DB_DSN`, default `ECKERNEL_EC`/`energy`/`localhost:1521/ORCL`):
```sql
SELECT COUNT(*) FROM OV_PORT WHERE CODE LIKE 'AUTOTEST%';
-- expect 0
```

## Verified (real runs, not hand-ticked — 2026-08-28 backfill re-run)
- robocop: 9 issues (VAR02/DOC02-style) — same count/kind as Berth's own baseline, not a regression.
- `--dryrun`: 5/5 pass.
- LIVE RF (`EC_HEADLESS=true`): **5/5 pass** (TC01 Verify Clean State, TC02 Insert, TC03 Update, TC04
  Find, TC05 Delete).
- Grid-filter keyword `Find Port Row By Filter` fired **15x** (grep on the fresh `output.xml`).
- Hygiene: PASS (no hardcoded creds, pure ASCII, no CHECKLIST/VERIFY-REPORT contradiction).
- DB self-clean: fresh `oracledb` connection, `SELECT COUNT(*) FROM OV_PORT WHERE CODE LIKE
  'AUTOTEST%'` = **0**.

Historical (2026-07-26, pre-conversion, kept for record): robocop 0 · hygiene 0 · dryrun 4/4 ·
LIVE RF 4/4 · Playwright 7/7 · self-clean 0 residual (`VERIFY-REPORT.md`).
