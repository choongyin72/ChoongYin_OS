# Calculation Group Context (CO.0245) - OV IUD bundle

Manage-Object (OV) screen: **Configuration > Assets > Calculation_Objects > Calculation Group Context**. Full
Insert / Update / Delete (End Date = Start Date), DB-verified against `OV_CALC_GRP_CONTEXT`, self-cleaning.
Built **label-driven, zero hardcoded field ids** on the shared engine + T2 (2026-07-26), then brought up to the
full **Bank-pattern** shape - properties-file-driven Insert/Update/Verify + explicit grid-filter wiring - by
PR #455 (batch 7, 2026-08-23). This backfill (batch 9 of
`docs/lean-deliverable-backfill-workorder.md`) restores the SOW/README/JOURNAL/evidence/CHECKLIST/KB-map
artifacts that the 2026-08-23 lean waiver (Section G) allowed to be skipped for the PR #455 conversion; the
existing RF automation was NOT touched.

## Artifacts
- **SOW:** `calculation_group_context_sow.md`
- **JOURNAL:** `JOURNAL.md`
- **RF T3:** `../../../pageobjects/Configuration/Assets/Calculation_Objects/calculation_group_context_page.resource`
- **RF suite:** `../../../tests/Configuration/Assets/Calculation_Objects/calculation_group_context_iud.robot`
- **Testdata:** `../../../testdata/calculation_group_context_{insert,update,form_verify,grid_verify}.properties`
- **Playwright driver (pre-existing, not rebuilt - Section H waives new Playwright work for Bank/Area conversions):**
  `../../../py/calculation_group_context_iud.py`
- **investigation/** `recon.py` (pre-existing, read-only) - **evidence/** step screenshots + `rf_report.html`
  (2026-07-26 original build) + `evidence/2026-08-28-backfill/` (this backfill's dryrun/live re-run)
- **KB selector map:** `ec-ui-knowledge/screens/calculation_group_context.md`

## Commands

Run from `workstreams/master-plan/ec-automation/`:

```bash
# Dryrun (syntax/keyword-resolution check, no browser)
py -m robot --dryrun --outputdir Workplaces/calculation-group-context-backfill/dryrun \
    tests/Configuration/Assets/Calculation_Objects/calculation_group_context_iud.robot

# Live headless run (5 TCs: clean-state, insert, update, find, delete)
EC_HEADLESS=true py -m robot --outputdir Workplaces/calculation-group-context-backfill/live \
    tests/Configuration/Assets/Calculation_Objects/calculation_group_context_iud.robot

# DB self-clean check (fresh connection, independent of the test run's own assertions)
py -c "
import oracledb
conn = oracledb.connect(user='ECKERNEL_EC', password='energy', dsn='localhost:1521/ORCL')
cur = conn.cursor()
cur.execute(\"SELECT COUNT(*) FROM OV_CALC_GRP_CONTEXT WHERE CODE = 'AUTOTEST_CGC_BANK'\")
print(cur.fetchone()[0])
conn.close()
"
```

## Verified (real runs, not hand-ticked)
- **Original build (2026-07-26):** robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4, Playwright 7/7, self-clean 0
  residual (`verify_screen.py` OVERALL PASS).
- **PR #455 Bank-pattern conversion (2026-08-23):** live 5/5 (TC01-05, added TC04 Find), DB self-clean via fresh
  oracledb connection (`AUTOTEST_CGC_BANK` count = 0), grid-filter wiring confirmed fired via `output.xml` grep
  (23 hits), `robot --dryrun` on the full `tests/` tree 753/753 pass, robocop parity vs `bank_iud.robot`'s
  accepted DOC02 baseline.
- **This backfill (2026-08-28):** re-ran dryrun (5/5 PASS) and one live headless run (5/5 PASS) for evidence
  capture only - see `evidence/2026-08-28-backfill/`; DB self-clean re-confirmed 0 residual via a fresh
  connection. No automation files were modified.
