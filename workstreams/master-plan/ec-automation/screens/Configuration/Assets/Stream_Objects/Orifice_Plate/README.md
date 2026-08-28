# Orifice Plate (CO.0089) — OV IUD bundle

Manage-Object (OV) screen: **Configuration > Assets > Stream_Objects > Orifice Plate**. Full
Insert / Update / Find / Delete, DB-verified against `OV_ORIFICE_PLATE`, self-cleaning.
**Full Bank-pattern**: properties-file-driven insert/update, explicit grid-filter wiring, dedicated
credentials, fixed test code — converted via PR #463 (Batch 8, merged 2026-08-23).

> Refreshed 2026-08-28 as part of the lean-deliverable-backfill project
> (`docs/lean-deliverable-backfill-workorder.md`, Batch 10) — this bundle predated PR #463 and still
> described the older generator-scaffolded build. No RF/py automation files were touched by this
> refresh.

## Artifacts
- **SOW:** `orifice_plate_sow.md`
- **JOURNAL:** `JOURNAL.md`
- **RF T3:** `../../../../pageobjects/Configuration/Assets/Stream_Objects/orifice_plate_page.resource`
- **RF suite:** `../../../../tests/Configuration/Assets/Stream_Objects/orifice_plate_iud.robot` (TC01-05)
- **Properties:** `testdata/orifice_plate_{insert,update,form_verify,grid_verify}.properties`
- **evidence/** — `rf_log_2026-08-28.html` / `rf_report_2026-08-28.html` / `rf_output_2026-08-28.xml`
  + per-TC step screenshots from the 2026-08-28 live re-run (this backfill).
- **KB map:** `ec-ui-knowledge/screens/orifice_plate.md` (refreshed 2026-08-28)
- Playwright driver (`py/orifice_plate_iud.py`) exists but is NOT part of this backfill's scope —
  items 4/5 of the deliverable checklist stay waived per Section H (superseded by the Universal
  Screen Engine going forward).

## Run commands (from `workstreams/master-plan/ec-automation/`)

```bash
# dryrun (syntax/wiring check, no browser/DB)
robot --dryrun --outputdir Workplaces/orifice-plate-backfill/dryrun tests/Configuration/Assets/Stream_Objects/orifice_plate_iud.robot

# live headless run (CI-style)
EC_HEADLESS=true robot --outputdir results tests/Configuration/Assets/Stream_Objects/orifice_plate_iud.robot

# live headed run (watchable)
EC_HEADLESS=false robot --outputdir results tests/Configuration/Assets/Stream_Objects/orifice_plate_iud.robot
```

## DB self-clean check (fresh connection, matches PR #463's pattern)

```python
import os, oracledb
conn = oracledb.connect(
    user=os.environ.get("EC_DB_USER", "ECKERNEL_EC"),
    password=os.environ.get("EC_DB_PASS", "energy"),
    dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"),
)
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM OV_ORIFICE_PLATE WHERE CODE LIKE 'AUTOTEST%'")
print(cur.fetchone()[0])   # expect 0 before AND after a run
```

## Verified (real runs, not hand-ticked, this backfill session 2026-08-28)
- `robot --dryrun`: **5/5 PASS**.
- `EC_HEADLESS=true robot` (live): **5/5 PASS**.
- Filter keyword fired: `grep -c "Find Orifice Plate Row By Filter" evidence/rf_output_2026-08-28.xml` → **13**.
- `py -m robocop check` on the page object + suite: **9 issues** (1x VAR02 + 5x DOC02, on the same
  test cases as PR #463 reported — matches the accepted Batch 7 exemplar pattern).
- `py scripts/check_bundle_hygiene.py` (repo root): **PASS** (no hardcoded creds / ASCII-clean /
  no CHECKLIST-vs-VERIFY-REPORT contradiction for this bundle).
- DB self-clean: fresh `oracledb` connection, `OV_ORIFICE_PLATE` `AUTOTEST%` count = **0** (before
  and after the live re-run).
