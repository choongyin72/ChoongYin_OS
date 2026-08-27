# Product Description — EC Object IUD bundle

**Screen:** Configuration > Assets > Financial Objects > Product Description. OV (Manage-Object,
grid `manage_object_nav_nav:form:T_data`), NO navigator section (universal Date+GO bar only),
date-effective. Converted to the **Bank full pattern** in PR #441 (2026-08-23, Batch 4 of the
Bank-pattern conversion project): 5 TCs, per-TC login/logout, fixed test code `AUTOTEST_PD`,
properties-file-driven insert/update/verify, explicit grid-filter wiring, zero inline DB-verify
calls in the `.robot` file.

**Not the same screen as** "Product" (CO.0007, class PRODUCT) or "Product Group" (RC.0053) —
distinct sibling classes under related menu paths. Do not confuse when searching by "product".

## Files in this bundle
- `product_description_sow.md` — SOW: classification, grid/cell shape, test data, dev story
  (original 2026-06-11 build + the 2026-08-23 Bank-pattern conversion addendum, Section 0).
- `README.md` — this file.
- `JOURNAL.md` — per-branch work journal (built / done-well / done-wrong-or-lessons /
  blockers→resolution / decisions / evidence), covering both the original build and the PR #441
  conversion.
- `evidence/` — screenshots + `product_description_results.json` from the original 2026-06-11
  Playwright run, PLUS `log.html`/`output.xml`/`report.html`/step screenshots from a live RF run
  captured during this backfill (2026-08-28).
- `investigation/` — pre-existing `financial_objects_recon.py` from the original build
  (unchanged; items 4/5 stay waived for Bank-/Area-pattern work per Section H of
  `docs/IUD-DELIVERABLE-CHECKLIST.md`).
- `playwright/` — pre-existing `ec_iud_product_description.py` driver from the original build
  (unchanged, historical reference only).
- `CHECKLIST.md` — the IUD deliverable checklist, ticked with real evidence citations.

KB selector map: `ec-ui-knowledge/screens/product_description.md`.

## Run — from `workstreams/master-plan/ec-automation/`

```bash
# structure-only dryrun (no browser/DB)
robot --dryrun tests/Configuration/Assets/Financial_Objects/product_description_iud.robot

# live run, headless (default CI mode)
EC_HEADLESS=true robot tests/Configuration/Assets/Financial_Objects/product_description_iud.robot

# live run, headed (visible browser, for a demo/spot-check)
EC_HEADLESS=false robot tests/Configuration/Assets/Financial_Objects/product_description_iud.robot
```

## DB self-clean check pattern

```sql
SELECT COUNT(*) FROM OV_PRODUCT_NODE_ITEM WHERE CODE = 'AUTOTEST_PD';
-- expected: 0 both BEFORE and AFTER a full TC01-TC05 run (the suite's own TC05 leaves no residue)
```

Or via the shared library from a Python shell: `libraries/DbVerify.py`'s
`fetch_object("OV_PRODUCT_NODE_ITEM", "AUTOTEST_PD")` — `None` = confirmed absent.

## Playwright reference (pre-existing, unchanged)

```bash
# from this folder — headless (default); a fresh AUTOTEST code is generated per run
py -X utf8 playwright/ec_iud_product_description.py

# live (visible browser) + slow-motion
EC_HEADED=1 EC_SLOWMO=400 py -X utf8 playwright/ec_iud_product_description.py
```
This driver predates the Bank-pattern conversion and is kept only as a historical reference per
Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md` (Universal Screen Engine replaces this role
going forward) — the RF suite above is the maintained, currently-working automation.
