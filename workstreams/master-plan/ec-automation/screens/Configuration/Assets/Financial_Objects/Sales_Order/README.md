# Sales Order — IUD automation bundle

**Screen:** Configuration → Assets → Financial Objects → Sales Order
**Type:** Manage Object (OV), plain manage-object OV (no navigator) — Bank-pattern conversion (PR
#444, merged 2026-08-23, Batch 5).
**Delete:** End Date = Start Date (zero-length window) — EC true delete (object removed from
`OV_PRODUCT_SALES_ORDER`).
**Status:** live **5/5 PASS** (Bank pattern, TC01-TC05), DB-verified, self-cleaning.
See [sales_order_sow.md](sales_order_sow.md) and [JOURNAL.md](JOURNAL.md).

This bundle has TWO historical layers: a **Playwright reference driver** from the screen's
original 2026-06-11 IUD build, and the **current, maintained Robot Framework suite** from the
2026-08-23 Bank-pattern conversion (PR #444). The RF suite is the screen's real, up-to-date
automation; the Playwright driver is kept as a historical reference only, per
`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H (no NEW Playwright work for Bank-pattern
conversions — the Universal Screen Engine replaces that role going forward).

## Run — Robot Framework (current, maintained automation)
```bash
# from workstreams/master-plan/ec-automation/

# 1. dryrun (structure only, no browser/DB)
py -m robot --dryrun --outputdir tmp_dryrun tests/Configuration/Assets/Financial_Objects/sales_order_iud.robot

# 2. live headless run (real browser, real DB writes, self-cleaning — TC05 deletes the fixed
#    AUTOTEST_SO code so the next run starts clean)
EC_HEADLESS=true py -m robot --outputdir tmp_live tests/Configuration/Assets/Financial_Objects/sales_order_iud.robot

# 3. live headed run (visible browser, for a watched demo)
EC_HEADLESS=false py -m robot --outputdir tmp_live tests/Configuration/Assets/Financial_Objects/sales_order_iud.robot
```

## DB self-clean check (ground truth — `OV_PRODUCT_SALES_ORDER`)
Run from a fresh connection (never reuse a mid-test session), to confirm the fixed test code
(`AUTOTEST_SO`) is absent and no `AUTOTEST%` residual rows exist:
```sql
SELECT COUNT(*) FROM OV_PRODUCT_SALES_ORDER WHERE CODE = 'AUTOTEST_SO';   -- expect 0
SELECT CODE, NAME FROM OV_PRODUCT_SALES_ORDER WHERE UPPER(CODE) LIKE 'AUTOTEST%' OR UPPER(NAME) LIKE 'AUTOTEST%';  -- expect no rows
```

## Key facts
- No navigator — plain manage-object OV; only the universal Date+GO as-at-date bar is present
  (`NAV_DD_COUNT=0`, confirmed live).
- Code label is SCREEN-PREFIXED: **"Product Sales Order Code"** (not the generic "Code" Bank/Cost
  Centre use).
- Two mandatory reference dropdowns beyond Code/Name/Start Date — **Company** and **Field**,
  neither a cascade. Insert uses real literal option text (`Acme Chemicals` / `Apollo`), not
  `__FIRST__` (Batch 2 VAT Code round-trip gotcha).
- Grid columns: Product Sales Order Code / Name / Start Date / End Date (20+ pre-existing rows,
  e.g. `BU_0001`).
- The RF suite uses the FIXED test code `AUTOTEST_SO` (not a per-run timestamp).
- Explicit grid-filter wiring (`Find/Clear Sales Order Row By Filter`) delegates to the shared T2
  `Find/Clear Object Row By Filter` keywords.

## Folder
- `sales_order_sow.md` — statement of work / spec (original 2026-06-11 Playwright build).
- `JOURNAL.md` — work journal (added 2026-08-28 backfill; covers both the original build and the
  PR #444 Bank-pattern conversion).
- `CHECKLIST.md` — deliverable checklist (added 2026-08-28 backfill).
- `playwright/ec_iud_sales_order.py` — historical Playwright reference driver, thin config over
  the shared engine (`../../Basic_Objects/_shared/iud_engine.py`). NOT the current automation;
  kept as-is, unmodified by this backfill.
- `investigation/` — recon scripts used to learn the screen (original build; unmodified).
- `evidence/` — screenshots + `results.json` from the original Playwright run, plus
  `evidence/backfill_2026-08-28/` (fresh RF dryrun + live re-run captured by this backfill).

## Equivalent RF files (outside this bundle, treeview-mirrored)
- T3 page object: `pageobjects/Configuration/Assets/Financial_Objects/sales_order_page.resource`
- Suite: `tests/Configuration/Assets/Financial_Objects/sales_order_iud.robot`
- Test data: `testdata/sales_order_{insert,update,form_verify,grid_verify}.properties`
- KB selector map: `ec-ui-knowledge/screens/sales_order.md`
