# Reservoir Block (CO.0133) - OV IUD bundle

Manage-Object (OV) screen: **Configuration > Assets > Well_and_Reservoir_Objects > Reservoir Block**.
Full Insert / Update / Delete (End Date = Start Date), DB-verified against `OV_RESV_BLOCK`,
self-cleaning. **Full Bank-pattern**: label-driven (no hardcoded field ids), properties-file-driven
Insert/Update/Verify, explicit grid-filter wiring - upgraded from an earlier partial label-driven
build (2026-07-26) to the full Bank/Berth shape in Batch 9 of the Bank-pattern conversion project
(PR #466, merged 2026-08-23).

**This bundle's SOW/README/JOURNAL/evidence/CHECKLIST/KB-map artifacts were backfilled 2026-08-28**
per `docs/lean-deliverable-backfill-workorder.md` (Batch 10) - the RF automation itself was NOT
touched, rebuilt, or re-verified from scratch; a dryrun + one live confirmation run was executed
purely to capture fresh evidence for this backfill.

## Artifacts
- **SOW:** `reservoir_block_sow.md`
- **RF T3 (page object):** `../../../pageobjects/Configuration/Assets/Well_and_Reservoir_Objects/reservoir_block_page.resource`
- **RF suite:** `../../../tests/Configuration/Assets/Well_and_Reservoir_Objects/reservoir_block_iud.robot`
- **Properties (test data):** `../../../testdata/reservoir_block_{insert,update,form_verify,grid_verify}.properties`
- **evidence/backfill-2026-08-28/** - dryrun + live-run artifacts captured for this backfill (output.xml, log.html, report.html, per-TC screenshots)
- **evidence/** (root) - original 2026-07-26 build's Playwright screenshots + `rf_report.html` (earlier, superseded, partial build - kept for history)
- **investigation/recon.py** - original recon script from the 2026-07-26 build (Playwright bundle stays waived per Section H of the deliverable checklist; not rebuilt)
- Playwright driver `py/reservoir_block_iud.py` still exists from the earlier build and is unchanged by this backfill or by PR #466.

## Commands

**Dryrun** (from `workstreams/master-plan/ec-automation/`):
```
robot --dryrun --outputdir <out> tests/Configuration/Assets/Well_and_Reservoir_Objects/reservoir_block_iud.robot
```

**Live headless run:**
```
EC_HEADLESS=true robot --outputdir <out> tests/Configuration/Assets/Well_and_Reservoir_Objects/reservoir_block_iud.robot
```

**DB self-clean check (fresh connection, after a live run):**
```sql
SELECT CODE FROM OV_RESV_BLOCK WHERE CODE LIKE 'AUTOTEST%';
-- Expect 0 rows if the suite's TC05 (Delete) ran and self-cleaned.
```
(via `oracledb`, same connection convention as `libraries/DbVerify.py` - env vars
`EC_DB_USER`/`EC_DB_PASS`/`EC_DB_DSN`, local-sandbox fallback `ECKERNEL_EC`/`energy`/`localhost:1521/ORCL`.)

## Verified (real runs, not hand-ticked - this backfill, 2026-08-28)
- `robot --dryrun`: **5/5 PASS** (TC01-TC05).
- `EC_HEADLESS=true robot` (live): **5/5 PASS** (TC01 clean-state, TC02 insert, TC03 update, TC04 find, TC05 delete).
- Fresh-connection DB self-clean: `SELECT CODE FROM OV_RESV_BLOCK WHERE CODE LIKE 'AUTOTEST%'` -> **0 rows**.
- robocop on the T3+suite: exit 1, but the **same 9 baseline issues** (8x DOC02, 1x VAR02) as the
  accepted `berth_iud.robot` exemplar - parity, not a regression (matches PR #466's original finding).
- Hygiene (`py scripts/check_bundle_hygiene.py`, run from repo root): **PASS** - no hardcoded creds/
  non-ASCII/doc contradictions attributable to this bundle (2 pre-existing, unrelated warnings on
  `Contract_Area/investigation/live_recon_contract_area.py`).
