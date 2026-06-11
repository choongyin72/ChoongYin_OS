# EC Screen IUD Operation Test — Statement of Work (SOW)
**Project:** EC Web App System Test (local sandbox)
**Task:** EC Screen Insert/Update/Delete (IUD) Automation — Customer
**Author:** Choong-Yin Lee / Claude Fable 5
**Date:** 2026-06-12
**Version:** 1.0 — COMPLETE (RF suite + Playwright reference, live + DB-verified)

---

## 1. REQUIREMENT
Automate IUD on the **Customer** screen with DB-level proof. Constraints: NEVER touch
existing data; test codes `AUTOTEST_CUST_<timestamp>`; local sandbox, user sysadmin.

| Operation | Pass condition | Status |
|---|---|---|
| INSERT | AUTOTEST row in grid AND present in `OV_CUSTOMER` | PASS |
| UPDATE | Name change visible in grid row | PASS |
| DELETE | End=Start -> gone from grid AND absent in `OV_CUSTOMER` | PASS |

## 2. DESIGN
| Property | Value |
|---|---|
| Treeview path | Configuration > Assets > Commercial Objects > Customer |
| Screen type | Manage Object (OV) |
| List/grid id | `manage_object_nav_nav:form:T_data` |
| DB view | `OV_CUSTOMER` |
| Delete semantics | End Date = Start Date (true delete) |

### DOM reference (rows derived from recon LABELS)
```
INSERT: Code  tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
        Name  tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
        Start tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
        ERP Customer Code:    tab:tabPanel:objectForm:form:G:0:R:6:C:1:in (MANDATORY text)
        Official Name:        tab:tabPanel:objectForm:form:G:0:R:7:C:1:in (MANDATORY text)
UPDATE: Code  tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in (guard)
        Name  tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
DELETE: End   tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
```

### Test data
Code `AUTOTEST_CUST_<timestamp>` | Name `Customer <code>` (+` UPD`) | Start=End `2003-01-01`
(section-wide 2003-01-01: reference dropdowns are effective-date-filtered — the object
Start Date acts as a version; seed objects start 2003-01-01)

| Extra mandatory field | Test value |
|---|---|
| ERP Customer Code | `ERP999` |
| Official Name | `AUTOTEST Official` |
| Customer Group (reference dd, banner-discovered) | first available option |

## 3. DEVELOPMENT
Generated DATA-DRIVEN from the section recon (`investigation/commercial_objects_recon.py`).
Banner-discovered mandatory dropdowns resolved in fix round 1; Field links into its groupmodel via the Geo Area dropdown (= navigator Area).

## 4. TEST EXECUTION
| Run | Mode | Result |
|---|---|---|
| RF dryrun | headless | PASS |
| RF live | headless | TC01–TC04 4/4 PASS, DB-verified |
| Playwright reference run | headless | see `evidence/customer_results.json` |

## 5. DELIVERABLES
RF suite + page object under `tests|pageobjects/.../Commercial_Objects/customer_*`,
this bundle, registry row in `docs/ec_screen_registry.md`.
