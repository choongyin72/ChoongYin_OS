# EC Screen IUD Operation Test — Statement of Work (SOW)
**Project:** EC Web App System Test (local sandbox)
**Task:** EC Screen Insert/Update/Delete (IUD) Automation — Sub Field
**Author:** Choong-Yin Lee / Claude Fable 5
**Date:** 2026-06-12
**Version:** 0.9 — ⚠ PARKED 2026-06-12: groupmodel not enabled for SUB_FIELD in this environment: inserts persist to OV_SUB_FIELD but the grid can never list them (same as Production Sub Unit) - confirmed by probe + DB on 2026-06-12

---

## 1. REQUIREMENT
Automate IUD on the **Sub Field** screen with DB-level proof. Constraints: NEVER touch
existing data; test codes `AUTOTEST_SFLD_<timestamp>`; local sandbox, user sysadmin.

| Operation | Pass condition | Status |
|---|---|---|
| INSERT | AUTOTEST row in grid AND present in `OV_SUB_FIELD` | BLOCKED |
| UPDATE | Name change visible in grid row | BLOCKED |
| DELETE | End=Start -> gone from grid AND absent in `OV_SUB_FIELD` | BLOCKED |

## 2. DESIGN
| Property | Value |
|---|---|
| Treeview path | Configuration > Assets > Commercial Objects > Sub Field |
| Screen type | Manage Object (OV-GM groupmodel) |
| List/grid id | `manageObject:form:T_data` |
| DB view | `OV_SUB_FIELD` |
| Delete semantics | End Date = Start Date (true delete) |

### DOM reference (rows derived from recon LABELS)
```
INSERT: Code  tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
        Name  tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
        Start tab:tabPanel:objectForm:form:G:0:R:5:C:1:da_input
UPDATE: Code  tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in (guard)
        Name  tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
DELETE: End   tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
```

### Test data
Code `AUTOTEST_SFLD_<timestamp>` | Name `Sub Field <code>` (+` UPD`) | Start=End `2003-01-01`
(section-wide 2003-01-01: reference dropdowns are effective-date-filtered — the object
Start Date acts as a version; seed objects start 2003-01-01)

## 3. DEVELOPMENT
Generated DATA-DRIVEN from the section recon (`investigation/commercial_objects_recon.py`).
PARKED: groupmodel not enabled for SUB_FIELD in this environment: inserts persist to OV_SUB_FIELD but the grid can never list them (same as Production Sub Unit) - confirmed by probe + DB on 2026-06-12

## 4. TEST EXECUTION
| Run | Mode | Result |
|---|---|---|
| RF dryrun | headless | PASS |
| RF live | headless | TC02 blocked; suite preserved in tests/.../_parked/ |
| Playwright reference run | headless | see `evidence/sub_field_results.json` |

## 5. DELIVERABLES
RF suite + page object under `tests|pageobjects/.../Commercial_Objects/sub_field_*`,
this bundle, registry row in `docs/ec_screen_registry.md`.
