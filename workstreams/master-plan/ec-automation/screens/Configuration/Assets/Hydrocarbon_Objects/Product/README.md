# Product — IUD bundle

**Screen:** Configuration > Assets > Hydrocarbon Objects > Product (BF `CO.0007`, class `PRODUCT`).
Plain OV (Bank family), date-effective, no navigator dropdown/cascade — single optional Date + GO.
View `OV_PRODUCT`. DELETE = End Date = Start Date (true delete, `objectdates` row).

Genuinely **brand-new build** (PR #485, merged 2026-08-24) — RF-only per the owner-approved lean
Bank-pattern-new-screen deliverable (`docs/IUD-DELIVERABLE-CHECKLIST.md` Section G); no Playwright
bundle exists or is required (Section H keeps items 4/5 permanently waived — the Universal Screen
Engine is the replacement).

- **RF T3:** `pageobjects/Configuration/Assets/Hydrocarbon_Objects/product_page.resource`
  (locators/keywords in Variables + Keywords; delegates to shared T2 `manage_object.resource` + T1
  `common.resource`).
- **RF suite:** `tests/Configuration/Assets/Hydrocarbon_Objects/product_iud.robot` — 5 TCs (TC01
  clean-state, TC02 Insert, TC03 Update, TC04 Find, TC05 Delete).
- **Test data:** `testdata/product_insert.properties`, `product_update.properties`,
  `product_form_verify.properties`, `product_grid_verify.properties`.

## Run commands
From `workstreams/master-plan/ec-automation/`:

```bash
# dryrun (syntax-only, no browser/DB)
robot --dryrun --outputdir results/product_dryrun tests/Configuration/Assets/Hydrocarbon_Objects/product_iud.robot

# live headless run
EC_HEADLESS=true robot --outputdir results/product_live tests/Configuration/Assets/Hydrocarbon_Objects/product_iud.robot
```

DB self-clean check pattern (fresh connection, run AFTER the live suite finishes):

```sql
SELECT
  (SELECT COUNT(*) FROM PRODUCT WHERE OBJECT_CODE = 'AUTOTEST_PRODUCT') AS base_cnt,
  (SELECT COUNT(*) FROM PRODUCT_VERSION pv JOIN PRODUCT p ON p.OBJECT_ID = pv.OBJECT_ID
     WHERE p.OBJECT_CODE = 'AUTOTEST_PRODUCT') AS version_cnt,
  (SELECT COUNT(*) FROM OV_PRODUCT WHERE CODE = 'AUTOTEST_PRODUCT') AS view_cnt
FROM DUAL;
```
All three counts must be 0 after TC05 (Delete) completes — the fixed test code `AUTOTEST_PRODUCT`
only stays reusable for the next run if every run cleans up after itself.

## Bundle contents
- `product_sow.md` — classification, nav/grid/cell shape, test data, dev story (from PR #485).
- `README.md` — this file.
- `JOURNAL.md` — built / done-well / done-wrong / blockers→resolution / decisions / evidence, modeled
  on `screens/Configuration/Assets/Financial_Objects/Bank/JOURNAL.md`.
- `evidence/` — artifacts from a real re-run of the suite captured during this backfill.
- `CHECKLIST.md` — the 21-item deliverable checklist, ticked with real evidence citations.

## Not touched by this backfill
No RF automation files (`product_page.resource`, `product_iud.robot`, `testdata/product_*.properties`)
were modified — this backfill only adds documentation/evidence around the already-working, already-
verified automation from PR #485.
