# EC Screen IUD Operation Test — Statement of Work (SOW)
**Project:** EC Web App System Test (local sandbox)
**Task:** EC Screen Insert/Update/Delete (IUD) Automation — VAT Code
**Author:** Choong-Yin Lee / Claude Fable 5
**Date:** 2026-06-11
**Version:** 1.0 — COMPLETE (RF suite + Playwright reference, live + DB-verified)

---

## 1. REQUIREMENT
Automate IUD on the **VAT Code** screen with DB-level proof. Constraints: NEVER touch
existing data; test codes `AUTOTEST_VAT_<timestamp>`; local sandbox, user sysadmin.

| Operation | Pass condition | Status |
|---|---|---|
| INSERT | AUTOTEST row in grid AND present in `OV_VAT_CODE` | PASS |
| UPDATE | Name change visible in grid row | PASS |
| DELETE | End=Start -> gone from grid AND absent in `OV_VAT_CODE` | PASS |

## 2. DESIGN
| Property | Value |
|---|---|
| Treeview path | Configuration > Assets > Financial Objects > VAT Code |
| Screen type | Manage Object (OV) |
| List/grid id | `manage_object_nav_nav:form:T_data` |
| DB view | `OV_VAT_CODE` |
| Delete semantics | End Date = Start Date (true delete) |

### DOM reference (rows derived from recon LABELS, not assumed positions)
```
INSERT: Code  tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
        Name  tab:tabPanel:objectForm:form:G:0:R:6:C:1:in
        Start tab:tabPanel:objectForm:form:G:0:R:1:C:1:da_input
        VAT Code:             tab:tabPanel:objectForm:form:G:0:R:3:C:1:in (MANDATORY text)
        Rate (Decimal):       tab:tabPanel:objectForm:form:G:0:R:7:C:1:in (MANDATORY text)
UPDATE: Code  tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in (guard)
        Name  tab:tabPanel:updateAttributes:form:G:0:R:4:C:1:in
DELETE: End   tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
```

### Test data
Code `AUTOTEST_VAT_<timestamp>` | Name `VAT Code <code>` (+` UPD`) | Start=End `2000-01-01`

| Extra mandatory field | Test value |
|---|---|
| VAT Code | `AT9` |
| Rate (Decimal) | `0.1` |
| Country (reference dropdown, banner-discovered) | first available option |
| VAT Type (reference dropdown, banner-discovered) | first available option |

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
| Playwright reference run | headless | see `evidence/vat_code_results.json` |

## 5. DELIVERABLES
RF suite + page object under `tests|pageobjects/.../Financial_Objects/vat_code_*`,
this bundle, and a registry row in `docs/ec_screen_registry.md`.

## 6. LESSONS (section-wide)
1. Label-driven generation beats positional assumptions (VAT Code keeps its dates at
   R1/R2 and Name at R6; Cost Object/Account Mapping insert an Alternative Code row
   into the update form).
2. Extra mandatory TEXT/checkbox fields need no user decision — safe throwaway values
   suffice (dropdowns DO need a decision; this section had none).
3. Same OV invariants as everywhere: navigator GO after save, DB as ground truth,
   End=Start true delete.
