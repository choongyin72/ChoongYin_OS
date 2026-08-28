# Chemical Transport Tank (CO.0257) - OV IUD bundle

_Updated 2026-08-28 (lean-deliverable backfill, Batch 9). Automation itself is unchanged - this
bundle refresh only brings the docs/evidence in line with the Batch 8 Bank-pattern conversion
(PR #461, merged 2026-08-23), which had left the SOW/README/JOURNAL/CHECKLIST/KB map describing
the older, superseded 2026-07-26 partial build._

Manage-Object (OV) screen: **Configuration > Assets > Chemical_Objects > Chemical Transport Tank**.
Full Bank-pattern conversion (properties-file-driven insert/update/verify + explicit grid-filter
wiring), Insert / Update / Delete (End Date = Start Date), DB-verified against `OV_CHEM_TRANS_TANK`,
self-cleaning. **NOT** the "Chemical Tank" screen (a separate, Area-pattern OV-GM navigator screen
already backfilled in Batch 4) - confirm the file paths above before touching anything.

## Artifacts
- **SOW:** `chemical_transport_tank_sow.md`
- **RF T3:** `../../../../pageobjects/Configuration/Assets/Chemical_Objects/chemical_transport_tank_page.resource`
- **RF suite:** `../../../../tests/Configuration/Assets/Chemical_Objects/chemical_transport_tank_iud.robot`
- **Test data:** `../../../../testdata/chemical_transport_tank_insert.properties`,
  `chemical_transport_tank_update.properties`, `chemical_transport_tank_form_verify.properties`,
  `chemical_transport_tank_grid_verify.properties`
- **evidence/** — `pre-batch8-2026-07-26/` (original 4-TC build's screenshots + `rf_report.html`,
  kept for history) and `batch8-live-2026-08-28/` (fresh 5-TC live run captured for this backfill:
  per-TC screenshots + `log.html`/`output.xml`/`report.html`)
- **investigation/** `recon.py` (from the original 2026-07-26 build; read-only recon, unchanged)
- **JOURNAL.md** / **CHECKLIST.md** (this backfill)
- Playwright driver `py/chemical_transport_tank_iud.py` is unaffected by the Batch 8 conversion
  (`py/` per owner rule) - the Playwright bundle waiver (Section H) does not remove an existing one.

## Commands

Dryrun (from `workstreams/master-plan/ec-automation/`):
```
robot --dryrun --outputdir Workplaces/<scratch>/dryrun tests/Configuration/Assets/Chemical_Objects/chemical_transport_tank_iud.robot
```

Live headless run:
```
EC_HEADLESS=true robot --outputdir Workplaces/<scratch>/live tests/Configuration/Assets/Chemical_Objects/chemical_transport_tank_iud.robot
```

DB self-clean check (fresh connection, run AFTER the live suite, expect 0):
```sql
SELECT COUNT(*) FROM OV_CHEM_TRANS_TANK WHERE UPPER(CODE) LIKE 'AUTOTEST%';
```
(The suite's own TC01/TC05 already assert this via the shared T2 `Verify Object Does Not
Exist`/`Verify Object Removed` keywords, which call `Code Should Be Absent In View` -
`libraries/DbVerify.py` - against `OV_CHEM_TRANS_TANK` for the real DB check, not just a UI check.)

## Verified (this backfill, 2026-08-28)
- `robot --dryrun` on this suite: **5/5 pass**.
- `EC_HEADLESS=true robot` (live): **5/5 pass** on the first attempt (TC01-05: clean-state / insert /
  update / find / delete).
- DB self-clean: confirmed in-suite via TC01 (`Verify Object Does Not Exist`, pre-run) and TC05
  (`Verify Object Removed`, post-run) - both assert against `OV_CHEM_TRANS_TANK` via
  `libraries/DbVerify.py`. A direct standalone `oracledb` connection from the local shell timed out
  (network path issue on this box, not a suite failure - the suite's own DB assertions inside the
  live run are the ground truth here and both passed).
- No RF/page-object/test-data files were modified for this backfill - documentation and evidence
  only.

## Original PR #461 verified evidence (Batch 8, merged 2026-08-23)
- Live RF suite: 5/5 pass. `robot --dryrun` full tree: 758/758 pass.
- DB self-clean via a fresh `oracledb` connection: 0 residual `AUTOTEST%` rows in `OV_CHEM_TRANS_TANK`.
- Grid filter fired: `output.xml` grep for `Find Chemical Transport Tank Row By Filter` -> 7 hits.
