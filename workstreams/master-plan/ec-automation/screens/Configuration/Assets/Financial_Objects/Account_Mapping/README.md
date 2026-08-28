# Account Mapping — IUD automation bundle

**Screen:** Configuration > Assets > Financial Objects > Account Mapping.
**Type:** Plain OV (manage-object, custom-URL, **no navigator** — GO-button locator
`button:form:B` confirmed 0 matches live, 2026-08-23), Bank-pattern classification, date-effective
(`OV_FIN_ACCOUNT_MAPPING`).
**Delete:** End Date = Start Date (true delete, hardcoded field id — packed Start/End Date row).
**Status:** live **5/5 PASS** (Bank pattern, TC01–TC05), DB-verified, self-cleaning.
See [account_mapping_sow.md](account_mapping_sow.md) and [JOURNAL.md](JOURNAL.md).

**The maintained/live test is the Robot Framework suite**, converted to the full Bank-pattern
5-TC structure via PR #450 (2026-08-23, Batch 6, the FINAL screen of the original 23-screen
Bank-pattern conversion candidate pool). The Playwright driver below is the original 2026-06-12
reference implementation, preserved unchanged — per owner decision 2026-08-27
(`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H), no new/updated Playwright bundle is built for
Bank-pattern conversions (the Universal Screen Engine replaces that role going forward). This
README, `JOURNAL.md`, `evidence/backfill_2026-08-28/`, `CHECKLIST.md`, and the KB map
`ec-ui-knowledge/screens/account_mapping.md` were added/refreshed by the 2026-08-28 deliverable
backfill (`docs/lean-deliverable-backfill-workorder.md`, Batch 8) — **the RF automation itself was
NOT modified by this backfill.**

## Layout
- `playwright/ec_iud_account_mapping.py` — the original 2026-06-12 Playwright driver (thin config
  over the shared engine), NOT modified by PR #450 or this backfill.
- `investigation/financial_objects_recon.py` — read-only recon from the original 2026-06-12 build,
  unchanged.
- `evidence/` — screenshots + `account_mapping_results.json` from the original 2026-06-12 run, plus
  `backfill_2026-08-28/` (RF dryrun + live run output + DB self-clean evidence captured by this
  backfill).
- `account_mapping_sow.md` — statement of work / spec (updated 2026-08-28 with the PR #450
  Bank-pattern conversion story).
- `JOURNAL.md` — work journal (refreshed 2026-08-28 backfill to cover the PR #450 conversion).
- `CHECKLIST.md` — deliverable checklist (refreshed 2026-08-28 backfill).

## Run — Robot Framework (maintained suite)
```bash
# from workstreams/master-plan/ec-automation/

# 1. dryrun (structure only, no browser/DB)
py -m robot --dryrun --outputdir tmp_dryrun tests/Configuration/Assets/Financial_Objects/account_mapping_iud.robot

# 2. live headless run (real browser, real DB writes, self-cleaning — TC05 deletes the fixed
#    AUTOTEST_AM code so the next run starts clean)
EC_HEADLESS=true py -m robot --outputdir tmp_live tests/Configuration/Assets/Financial_Objects/account_mapping_iud.robot

# 3. live headed run (visible browser, for a watched demo)
EC_HEADLESS=false py -m robot --outputdir tmp_live tests/Configuration/Assets/Financial_Objects/account_mapping_iud.robot
```

## DB self-clean check (ground truth — OV_FIN_ACCOUNT_MAPPING)
Run BEFORE and AFTER the live suite, from a fresh connection each time (never reuse a mid-test
session), to confirm the fixed test code (`AUTOTEST_AM`) is absent and no `AUTOTEST%` residual rows
exist:
```sql
SELECT COUNT(*) FROM OV_FIN_ACCOUNT_MAPPING WHERE CODE = 'AUTOTEST_AM';  -- expect 0
SELECT CODE FROM OV_FIN_ACCOUNT_MAPPING WHERE CODE LIKE 'AUTOTEST%';     -- expect no rows
```
(`libraries/DbVerify.py` uses the generic `CODE` column on every `OV_*` view.)

## Run — Playwright (original reference, unmodified since 2026-06-12)
```bash
# from this folder — headless (default); a fresh AUTOTEST code is generated per run
py -X utf8 playwright/ec_iud_account_mapping.py

# live (visible browser) + slow-motion
EC_HEADED=1 EC_SLOWMO=400 py -X utf8 playwright/ec_iud_account_mapping.py
```

## Key facts
- No navigator — plain custom-URL manage-object OV. Confirmed NOT a scope mismatch despite the
  "Mapping" name (genuine Code/Name manage-object OV with an `objectForm`-New-Object flow, same
  outcome as Cost Object Mapping in Batch 4).
- Insert form (`objectForm`) mandatory: Code, Name, Start Date, plus 8 mandatory reference
  dropdowns (Line Item Type, Financial Code, Company Category, Status, Debit / Credit, Debit PK,
  Credit PK, Financial Account) and one cascade dependency (Account Category, statically
  non-mandatory but required for Financial Account's option list to populate).
- The 9-dropdown REFERENCE COMBINATION (not any single field) is this screen's real unique key —
  `JOU_ENT_ALL_ALL_ALL_ACCRUAL_CREDIT`, reused unchanged from the screen's own 2026-06-12
  Playwright-proven combination.
- Grid is a 75-row, 13-column custom grid with NO Start Date column (unlike Bank's 3-column grid);
  grid-verify checks Code/Name only.
- Line Item Type re-renders as the short internal code `ALL` after any form reload — excluded from
  the live-DOM round-trip form-label check, relying on DB ground truth instead.
- The RF suite uses the FIXED test code `AUTOTEST_AM` (not a per-run timestamp — since PR #450);
  the Playwright driver still uses the original per-run `AUTOTEST_AM_<timestamp>` convention.

## Equivalent RF files (outside this bundle, treeview-mirrored)
- T3 page object: `pageobjects/Configuration/Assets/Financial_Objects/account_mapping_page.resource`
- Suite: `tests/Configuration/Assets/Financial_Objects/account_mapping_iud.robot`
- Test data: `testdata/account_mapping_{insert,update,form_verify,grid_verify}.properties`
- KB selector map: `ec-ui-knowledge/screens/account_mapping.md`
