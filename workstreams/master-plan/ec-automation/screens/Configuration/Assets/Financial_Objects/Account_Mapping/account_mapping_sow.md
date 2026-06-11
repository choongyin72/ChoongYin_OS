# EC Screen IUD Operation Test — Statement of Work (SOW)
**Project:** EC Web App System Test (local sandbox)
**Task:** EC Screen Insert/Update/Delete (IUD) Automation — Account Mapping
**Author:** Choong-Yin Lee / Claude Fable 5
**Date:** 2026-06-11
**Version:** 0.9 — PARKED 2026-06-12: needs valid business combination across 11 reference dropdowns (validation layers stack); plan: deep-dive Revenue setup in ECpedia/EC docs first. Financial Account column also effective-date-filtered (use Start Date >= 2003-01-01).

---

## 1. REQUIREMENT
Automate IUD on the **Account Mapping** screen with DB-level proof. Constraints: NEVER touch
existing data; test codes `AUTOTEST_AM_<timestamp>`; local sandbox, user sysadmin.

| Operation | Pass condition | Status |
|---|---|---|
| INSERT | (parked) | BLOCKED |
| UPDATE | Name change visible in grid row | PASS |
| DELETE | End=Start -> gone from grid AND absent in `OV_FIN_ACCOUNT_MAPPING` | PASS |

## 2. DESIGN
| Property | Value |
|---|---|
| Treeview path | Configuration > Assets > Financial Objects > Account Mapping |
| Screen type | Manage Object (OV) |
| List/grid id | `manageObject:form:T_data` |
| DB view | `OV_FIN_ACCOUNT_MAPPING` |
| Delete semantics | End Date = Start Date (true delete) |

### DOM reference (rows derived from recon LABELS, not assumed positions)
```
INSERT: Code  tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
        Name  tab:tabPanel:objectForm:form:G:0:R:2:C:1:in
        Start tab:tabPanel:objectForm:form:G:0:R:3:C:1:da_input
UPDATE: Code  tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in (guard)
        Name  tab:tabPanel:updateAttributes:form:G:0:R:2:C:1:in
DELETE: End   tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
```

### Test data
Code `AUTOTEST_AM_<timestamp>` | Name `Account Mapping <code>` (+` UPD`) | Start=End `2000-01-01`

| Extra mandatory field | Test value |
|---|---|
| Line Item Type (reference dropdown, banner-discovered) | first available option |
| Financial Code (reference dropdown, banner-discovered) | first available option |
| Company Category (reference dropdown, banner-discovered) | first available option |
| Status (reference dropdown, banner-discovered) | first available option |
| Debit / Credit (reference dropdown, banner-discovered) | first available option |
| Debit PK (reference dropdown, banner-discovered) | first available option |
| Credit PK (reference dropdown, banner-discovered) | first available option |

## 3. DEVELOPMENT
Generated DATA-DRIVEN from the section recon (`investigation/financial_objects_recon.py`
output): field rows are picked by their `:C:0:la` labels, so row-shift screens and
relocated dates are handled automatically. Extra MANDATORY fields get fixed safe test
values (cleaned up by the delete).

## 4. TEST EXECUTION
| Run | Mode | Result |
|---|---|---|
| RF dryrun | headless | PASS |
| RF live batch | headless | TC02 blocked; suite preserved in tests/.../_parked/ |
| Playwright reference run | headless | see `evidence/account_mapping_results.json` |

## 5. DELIVERABLES
RF suite + page object under `tests|pageobjects/.../Financial_Objects/account_mapping_*`,
this bundle, and a registry row in `docs/ec_screen_registry.md`.

## 6. LESSONS (section-wide)
1. Label-driven generation beats positional assumptions (VAT Code keeps its dates at
   R1/R2 and Name at R6; Cost Object/Account Mapping insert an Alternative Code row
   into the update form).
2. Extra mandatory TEXT/checkbox fields need no user decision — safe throwaway values
   suffice (dropdowns DO need a decision; this section had none).
3. Same OV invariants as everywhere: navigator GO after save, DB as ground truth,
   End=Start true delete.
