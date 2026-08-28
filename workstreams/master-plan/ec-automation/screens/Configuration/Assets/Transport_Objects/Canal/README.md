# Canal (CO.2069) - OV IUD bundle

Manage-Object (OV) screen: **Configuration > Assets > Transport Objects > Canal**. Full Insert /
Update / Delete (End Date = Start Date), DB-verified against `OV_CANAL`, self-cleaning. Full
**Bank-pattern** shape (properties-file-driven + explicit grid-filter wiring), converted via
PR #458 (Batch 7, 2026-08-23). This bundle was refreshed 2026-08-28 (Batch 9 of
`docs/lean-deliverable-backfill-workorder.md`) to restore SOW/README/JOURNAL/evidence/CHECKLIST/KB
artifacts that PR #458's lean waiver skipped — **no RF file was touched to produce this refresh.**

## Artifacts
- **SOW:** `canal_sow.md`
- **RF T3:** `../../../../pageobjects/Configuration/Assets/Transport_Objects/canal_page.resource`
- **RF suite:** `../../../../tests/Configuration/Assets/Transport_Objects/canal_iud.robot`
- **Test data:** `../../../../testdata/canal_{insert,update,form_verify,grid_verify}.properties`
- **evidence/** — `rf_batch9_2026-08-28/` (this backfill's fresh dryrun + live run artifacts);
  earlier `canal_0[1-5]_*.png` + `rf_report.html` predate the Bank-pattern conversion (kept for
  history, superseded by the fresh run for current evidence).
- **Playwright:** waived permanently for Bank-/Area-pattern work (Section H,
  `docs/IUD-DELIVERABLE-CHECKLIST.md`) — the Universal Screen Engine (`py/engine.py`) is the
  owner-decided replacement; no new Playwright driver is built for this screen going forward.

## Exact commands

**Dryrun** (from `workstreams/master-plan/ec-automation/`):
```
robot --dryrun --outputdir <outdir> tests/Configuration/Assets/Transport_Objects/canal_iud.robot
```

**Live headless run:**
```
EC_HEADLESS=true robot --outputdir <outdir> tests/Configuration/Assets/Transport_Objects/canal_iud.robot
```

**robocop:**
```
robocop check pageobjects/Configuration/Assets/Transport_Objects/canal_page.resource tests/Configuration/Assets/Transport_Objects/canal_iud.robot
```

**Hygiene** (from repo root):
```
py scripts/check_bundle_hygiene.py
```

**DB self-clean check** (fresh connection, against `OV_CANAL`) — the pattern used for this
backfill's evidence:
```python
import oracledb
conn = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = conn.cursor()
cur.execute("SELECT CODE FROM OV_CANAL WHERE CODE LIKE '%KIEL%'")
print(cur.fetchall())   # expect []  after a clean TC05 delete
```
(Or via the shared RF library: `libraries/DbVerify.py`'s `Code Should Be Absent In View OV_CANAL
CANAL_KIEL`, as used inside the suite's own TC05 verification.)

## Verified (real runs)
- robocop: 9 issues (DOC02/style baseline — matches Bank's own accepted baseline).
- hygiene: exit 0, PASS.
- dryrun: 5/5 pass.
- **Live RF: 5/5 pass** (2026-08-28 re-run, first attempt, no retry needed).
- DB self-clean: 0 residual `CANAL_KIEL` rows, fresh connection.
