# EC Screen IUD Operation Test - Statement of Work (SOW)
**Project:** Woodside Pluto ECaaS - EC Web App System Test
**Task:** EC Screen Insert/Update/Delete (IUD) Automation - Product Group
**Screen:** Configuration > Assets > Royalty Objects > Product Group (RC.0053)
**Author:** Choong-Yin Lee / Claude Opus 4.8
**Date:** 2026-06-25
**Version:** 1.0

---

## 1. REQUIREMENT

### 1.1 Objective
Automate Insert, Update, Delete (IUD) on the Product Group screen to validate that the screen
correctly creates, modifies and deletes product-group master records, with EC data integrity
maintained throughout the lifecycle and the sandbox left exactly as found.

### 1.2 Scope
Single screen, one PR (Option 1). Product Group is the 3rd of the 8 screens under
Configuration > Assets > Royalty Objects.

### 1.3 Constraints
- **NEVER modify existing production/configuration data.**
- All test data prefixed `AUTOTEST_PG_`; a unique per-run code is generated (EC keeps deleted
  codes in the base table, so codes are never reused).
- Target environment: **sandbox** web `https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/`
  (user `sysadmin`), DB ground-truth `localhost:1521/ORCL` (`ECKERNEL_EC`).

### 1.4 Acceptance Criteria
| Operation | Pass Condition |
|---|---|
| INSERT | New record with `AUTOTEST_PG_*` code appears in the list AND in `ov_product_group` |
| UPDATE | Product Group Name changed and persisted (visible in the row) |
| DELETE | Record removed from `ov_product_group` after End Date = Start Date + Save |
| CLEANUP | Environment returned to pre-test state (object truly deleted, 0 residual) |

---

## 2. DESIGN

### 2.1 Screen classification (recon via resolve_ec_screen.py + scan_ec_screen.py)
| Property | Value |
|---|---|
| Screen name | Product Group |
| Treeview path | Configuration > Assets > Royalty Objects > Product Group |
| Screen type | **Manage-Object (OV)** - Bank family (date-only navigator, NOT OV-GM) |
| CLASS_TYPE | OBJECT (=> OV) |
| TIME_SCOPE | VERSIONED (=> date-effective; DELETE = End Date = Start Date) |
| Base table | PRODUCT_GROUP |
| Object view | `OV_PRODUCT_GROUP` |
| App | EC_REVN |
| Grid tbody id | `manage_object_nav_nav:form:T_data` |
| Mandatory insert fields | Code (R0), Name (R1), Start Date (R2). Product Group Type dd (R5) is optional |

### 2.2 IUD design (identical mechanic to Bank)
```
INSERT:  Insert toolbar -> "New Object" -> objectForm (3 mandatory fields):
           R:0 = Product Group Code   (tab:tabPanel:objectForm:form:G:0:R:0:C:1:in)
           R:1 = Product Group Name   (tab:tabPanel:objectForm:form:G:0:R:1:C:1:in)
           R:2 = Start Date           (tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input)
         -> Save -> GO -> verify in list + ov_product_group.

UPDATE:  Click row span -> updateAttributes:
           Code: tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in (read-only)
           Name: tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in (editable)
         -> edit Name -> Save -> GO -> verify.

DELETE:  End Date set equal to Start Date (zero-length window):
           End Date: tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
         -> Save -> GO -> object removed from ov_product_group (TRUE delete, DB-verified).
```

### 2.3 Test data
| Field | Value |
|---|---|
| Code | `AUTOTEST_PG_<run>` (unique per run) |
| Name (Insert) | `AUTOTEST Product Group <run>` |
| Name (Update) | `AUTOTEST Product Group <run> UPDATED` |
| Start Date | `2000-01-01` |
| End Date (Delete) | `2000-01-01` (= Start Date -> true delete) |

### 2.4 Technology stack
Playwright (Python sync) freestyle bundle + Robot Framework suite layered T3 -> T2
(`manage_object.resource`) + T1 (`common.resource`) + `DbVerify.py`. Screenshots per step.

---

## 3. KNOWN RISKS
- Not an OV-GM screen (date-only navigator) - no lazy-redraw risk; standard Bank-family timing.
- EC keeps deleted codes in the base table; unique per-run codes avoid re-insert rejection.

---

## 4. DELIVERABLES
| Deliverable | Path |
|---|---|
| Playwright bundle | `playwright/ec_iud_product_group.py` |
| RF T3 page object | `pageobjects/Configuration/Assets/Royalty_Objects/product_group_page.resource` |
| RF test suite | `tests/Configuration/Assets/Royalty_Objects/product_group_iud.robot` |
| SOW | this document |
| Evidence | `evidence/` (after a live run) |
| Registry + scorecard rows | `docs/ec_screen_registry.md`, `docs/automation-scorecard.md` |
