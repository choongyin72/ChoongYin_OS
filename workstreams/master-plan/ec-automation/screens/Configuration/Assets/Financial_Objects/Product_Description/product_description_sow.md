# EC Screen IUD Operation Test — Statement of Work (SOW)
**Project:** EC Web App System Test (local sandbox)
**Task:** EC Screen Insert/Update/Delete (IUD) Automation — Product Description
**Author:** Choong-Yin Lee / Claude Fable 5
**Date:** 2026-06-11 (original build); addendum 2026-08-23 (PR #441 Bank-pattern conversion);
backfilled 2026-08-27/28 under `docs/lean-deliverable-backfill-workorder.md` (Section H of
`docs/IUD-DELIVERABLE-CHECKLIST.md`, owner decision 2026-08-27 retiring the 2026-08-23/26 lean
waiver)
**Version:** 2.0 — RF suite converted to the full Bank pattern (PR #441); Playwright reference
kept as historical record only (Section H waives further Playwright build for Bank-pattern work)

---

## 0. ADDENDUM (2026-08-23, PR #441) — Bank-pattern conversion
Converted the Product Description IUD suite (Configuration > Assets > Financial Objects >
Product Description) from the older hardcoded-field-id pattern below (Sections 1-6, kept
unchanged as the original build's own record) to the label-driven, properties-file-driven,
T2-consolidated "Bank pattern" — Batch 4 of the original Bank-pattern conversion project (5
parallel screens per `tmp/batch4_shared_findings.md`: State Lease/Vendor/Cost Object
Mapping/DOA Credit Limit/Product Description). Real facts confirmed live during that conversion
(not assumed):
- **Classification:** plain Bank-pattern OV (Manage-Object), NO navigator section. **NOT the same
  class as "Product" (CO.0007) or "Product Group" (RC.0053)** — confirmed distinct before
  building.
- No mandatory navigator cascade — universal Date+GO bar only (`NAV_DD_COUNT=0`).
- The Code label is **screen-prefixed** — "Product Node Item Code", not the generic "Code" that
  Bank/Cost Centre use.
- Grid shows 4 columns: Product Node Item Code / Name / Start Date / End Date.
- **Three mandatory reference dropdowns** on both `objectForm` and `updateAttributes`: Product,
  Node, Financial Code (`MandatoryCellStyle` confirmed live) — literal first-option values used
  for insert (`AS3_CrudeOil` / `Apollo FPSO` / `Frame Agreement`), not `__FIRST__`, per the VAT
  Code round-trip-verify gotcha (TC02's verify compares the live screen back against the same
  properties file used to insert).
- Fixed test code `AUTOTEST_PD` (replacing the original build's generated
  `AUTOTEST_PD_<timestamp>` code below), Start Date `2003-01-01` (reference-dropdown date-scope
  convention, replacing the original `2000-01-01`).
- Explicit grid-filter wiring (`Find/Clear Product Description Row By Filter`) included from day
  one, matching Bank/Account/Customer precedent.
- Reused T2's existing consolidated keywords as-is (`Insert/Update Object From Properties`,
  `Verify Object Insert Exists/Form Record/Found/Does Not Exist/Removed`, `Find Object Record`) —
  no edits to `resources/manage_object.resource` or `resources/common.resource`.
- Live run (EC_HEADLESS=true) at PR #441 time: **5/5 PASS**. Full `tests/` dryrun: **740/740
  PASS** (baseline was 739/739 before this suite). robocop: **9 issues** (4 VAR02 + 5 DOC02) —
  identical in kind/count to the established Bank/Customer baseline. DB self-clean: fresh
  oracledb connection — `SELECT COUNT(*) FROM OV_PRODUCT_NODE_ITEM WHERE CODE = 'AUTOTEST_PD'` →
  **0** (confirmed both pre-run and post-run clean).
- See `JOURNAL.md` for the fuller narrative (pulled from PR #441's real body) and `CHECKLIST.md`
  for this backfill's own re-verification evidence (robocop/dryrun/live/DB-clean re-run
  2026-08-28).

---

## 1. REQUIREMENT
Automate IUD on the **Product Description** screen with DB-level proof. Constraints: NEVER touch
existing data; test codes `AUTOTEST_PD_<timestamp>`; local sandbox, user sysadmin.

| Operation | Pass condition | Status |
|---|---|---|
| INSERT | AUTOTEST row in grid AND present in `OV_PRODUCT_NODE_ITEM` | PASS |
| UPDATE | Name change visible in grid row | PASS |
| DELETE | End=Start -> gone from grid AND absent in `OV_PRODUCT_NODE_ITEM` | PASS |

## 2. DESIGN
| Property | Value |
|---|---|
| Treeview path | Configuration > Assets > Financial Objects > Product Description |
| Screen type | Manage Object (OV) |
| List/grid id | `manage_object_nav_nav:form:T_data` |
| DB view | `OV_PRODUCT_NODE_ITEM` |
| Delete semantics | End Date = Start Date (true delete) |

### DOM reference (rows derived from recon LABELS, not assumed positions)
```
INSERT: Code  tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
        Name  tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
        Start tab:tabPanel:objectForm:form:G:0:R:3:C:1:da_input
UPDATE: Code  tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in (guard)
        Name  tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
DELETE: End   tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
```

### Test data
Code `AUTOTEST_PD_<timestamp>` | Name `Product Description <code>` (+` UPD`) | Start=End `2000-01-01`

| Extra mandatory field | Test value |
|---|---|
| Product (reference dropdown, banner-discovered) | first available option |
| Node (reference dropdown, banner-discovered) | first available option |
| Financial Code (reference dropdown, banner-discovered) | first available option |

## 3. DEVELOPMENT
Generated DATA-DRIVEN from the section recon (`investigation/financial_objects_recon.py`
output): field rows are picked by their `:C:0:la` labels, so row-shift screens and
relocated dates are handled automatically. Extra MANDATORY fields get fixed safe test
values (cleaned up by the delete).

## 4. TEST EXECUTION
| Run | Mode | Result |
|---|---|---|
| RF dryrun | headless | PASS |
| RF live batch | headless | TC01–TC04 4/4 PASS, DB-verified |
| Playwright reference run | headless | see `evidence/product_description_results.json` |

## 5. DELIVERABLES
RF suite + page object under `tests|pageobjects/.../Financial_Objects/product_description_*`,
this bundle, and a registry row in `docs/ec_screen_registry.md`.

## 6. LESSONS (section-wide)
1. Label-driven generation beats positional assumptions (VAT Code keeps its dates at
   R1/R2 and Name at R6; Cost Object/Account Mapping insert an Alternative Code row
   into the update form).
2. Extra mandatory TEXT/checkbox fields need no user decision — safe throwaway values
   suffice (dropdowns DO need a decision; this section had none).
3. Same OV invariants as everywhere: navigator GO after save, DB as ground truth,
   End=Start true delete.
