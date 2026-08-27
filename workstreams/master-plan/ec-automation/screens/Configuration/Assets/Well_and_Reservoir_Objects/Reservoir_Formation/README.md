# Reservoir Formation (CO.0135) - OV IUD bundle

Manage-Object (OV) screen: **Configuration > Assets > Well_and_Reservoir_Objects > Reservoir Formation**.
Full Bank-pattern conversion (Batch 9, PR #467, merged 2026-08-23): properties-file-driven Insert/Update,
explicit grid-filter wiring, fixed test code, per-TC login/logout, 5 test cases (TC01-05). DB-verified
against `OV_RESV_FORMATION`, self-cleaning.

## Artifacts
- **SOW:** `reservoir_formation_sow.md`
- **RF T3:** `../../../../pageobjects/Configuration/Assets/Well_and_Reservoir_Objects/reservoir_formation_page.resource`
- **RF suite:** `../../../../tests/Configuration/Assets/Well_and_Reservoir_Objects/reservoir_formation_iud.robot`
- **Test data:** `testdata/reservoir_formation_insert.properties`, `_update.properties`,
  `_form_verify.properties`, `_grid_verify.properties`
- **evidence/** - re-run artifacts (log/report/output.xml, screen-scoped) from this backfill's evidence
  capture run
- **Playwright driver:** `py/reservoir_formation_iud.py` (unchanged by Batch 9; NOT rebuilt by this
  backfill - the `investigation/`/Playwright-bundle items are waived permanently per
  `docs/IUD-DELIVERABLE-CHECKLIST.md` Section H, superseded by the Universal Screen Engine)
- **KB map:** `ec-ui-knowledge/screens/reservoir_formation.md`

## Commands

Run everything from `workstreams/master-plan/ec-automation/`.

**Dryrun** (screen-scoped, confirms syntax/parse without executing):
```
robot --dryrun --outputdir Workplaces/reservoir-formation-backfill/dryrun tests/Configuration/Assets/Well_and_Reservoir_Objects/reservoir_formation_iud.robot
```

**Live headless run** (the real evidence-capture run):
```
EC_HEADLESS=true robot --outputdir Workplaces/reservoir-formation-backfill/live tests/Configuration/Assets/Well_and_Reservoir_Objects/reservoir_formation_iud.robot
```

**DB self-clean check** (fresh connection, run AFTER the live suite's own TC05 delete; expect 0 rows):
```sql
SELECT COUNT(*) FROM OV_RESV_FORMATION WHERE CODE = 'AUTOTEST_RESVF';
```

## Verified (real runs, not hand-ticked)
Batch 9 (PR #467, 2026-08-23): robocop 0 (11 pre-existing VAR02/DOC02 findings, same class as Berth) -
hygiene 0 - dryrun 762/762 (full-tree) - **LIVE RF 5/5** (TC01-05) - filter keyword fired 7x
(output.xml grep) - DB self-clean 0 residual `AUTOTEST_RESVF` rows (fresh oracledb connection).

This backfill (2026-08-28): re-ran the suite live once more for evidence capture - see `evidence/` and
`CHECKLIST.md` for the fresh run's own N/N result and citations.
