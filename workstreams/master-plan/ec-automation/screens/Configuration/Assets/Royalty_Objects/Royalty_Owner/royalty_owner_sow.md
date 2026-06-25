# EC Screen IUD Operation Test - Statement of Work (SOW)
**Project:** Woodside Pluto ECaaS - EC Web App System Test
**Task:** EC Screen Insert/Update/Delete (IUD) Automation - Royalty Owner
**Screen:** Configuration > Assets > Royalty Objects > Royalty Owner (RC.0051)
**Author:** Choong-Yin Lee / Claude Opus 4.8
**Date:** 2026-06-25
**Version:** 1.0

---

## 1. REQUIREMENT

### 1.1 Objective
Automate Insert, Update, Delete (IUD) on the Royalty Owner screen to validate that the
screen correctly creates, modifies and deletes royalty-owner master records, with EC data
integrity maintained throughout the lifecycle and the sandbox left exactly as found.

### 1.2 Scope
Single screen, one PR (Option 1). Royalty Owner is the first of the 8 screens under
Configuration > Assets > Royalty Objects; siblings (Royalty Depositor, Product Group, Tract,
Unit Agreement, etc.) follow as separate PRs.

### 1.3 Constraints
- **NEVER modify existing production/configuration data.**
- All test data prefixed `AUTOTEST_RO_`; a unique per-run code is generated (EC keeps deleted
  codes in the base table, so codes are never reused).
- Target environment: **sandbox** web `https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/`
  (user `sysadmin`), DB ground-truth `localhost:1521/ORCL` (`ECKERNEL_EC`).

### 1.4 Acceptance Criteria
| Operation | Pass Condition |
|---|---|
| INSERT | New record with `AUTOTEST_RO_*` code appears in the list AND in `ov_royalty_owner` |
| UPDATE | Royalty Owner Name changed and persisted (visible in the row) |
| DELETE | Record removed from `ov_royalty_owner` after End Date = Start Date + Save |
| CLEANUP | Environment returned to pre-test state (object truly deleted, 0 residual) |

---

## 2. DESIGN

### 2.1 Screen classification (recon via resolve_ec_screen.py + scan_ec_screen.py)
| Property | Value |
|---|---|
| Screen name | Royalty Owner |
| Treeview path | Configuration > Assets > Royalty Objects > Royalty Owner |
| Screen type | **Manage-Object (OV)** - Bank family (no BU/PU navigator, NOT OV-GM) |
| CLASS_TYPE | OBJECT (=> OV) |
| TIME_SCOPE | VERSIONED (=> date-effective; DELETE = End Date = Start Date) |
| Base table | COMPANY |
| Version table | COMPANY_VERSION |
| Object view | `OV_ROYALTY_OWNER` |
| App | EC_REVN |
| Grid tbody id | `manage_object_nav_nav:form:T_data` |

### 2.2 IUD design (identical mechanic to Bank exemplar)
```
INSERT:  Insert toolbar -> hover -> "New Object" -> objectForm (3 mandatory fields):
           R:0 = Royalty Owner Code   (tab:tabPanel:objectForm:form:G:0:R:0:C:1:in)
           R:1 = Royalty Owner Name   (tab:tabPanel:objectForm:form:G:0:R:1:C:1:in)
           R:2 = Start Date           (tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input)
         -> Save -> GO -> verify in list + ov_royalty_owner.

UPDATE:  Click row span -> updateAttributes form loads:
           Code: tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in (read-only)
           Name: tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in (editable)
         -> edit Name -> Save -> GO -> verify.

DELETE:  EC toolbar Delete = DISABLED (royalty owners are date-effective master data).
         EC-correct delete = End Date set equal to Start Date (zero-length window):
           End Date: tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
         -> Save -> GO -> object removed from ov_royalty_owner (TRUE delete, DB-verified).
```

### 2.3 Test data
| Field | Value |
|---|---|
| Code | `AUTOTEST_RO_<run>` (unique per run) |
| Name (Insert) | `AUTOTEST Royalty Owner <run>` |
| Name (Update) | `AUTOTEST Royalty Owner <run> UPDATED` |
| Start Date | `2000-01-01` |
| End Date (Delete) | `2000-01-01` (= Start Date -> true delete) |

### 2.4 Technology stack
Playwright (Python sync) freestyle bundle + Robot Framework suite layered T3 -> T2
(`manage_object.resource`) + T1 (`common.resource`) + `DbVerify.py`. Screenshots per step;
results JSON at `tmp/logs/ec_iud_royalty_owner_final.json`.

---

## 3. KNOWN RISKS
- Not an OV-GM screen (no BU/PU navigator) - no lazy-redraw risk; standard Bank-family timing.
- EC keeps deleted codes in the base table; unique per-run codes avoid re-insert rejection.

---

## 4. DELIVERABLES
| Deliverable | Path |
|---|---|
| Playwright bundle | `playwright/ec_iud_royalty_owner.py` |
| RF T3 page object | `pageobjects/Configuration/Assets/Royalty_Objects/royalty_owner_page.resource` |
| RF test suite | `tests/Configuration/Assets/Royalty_Objects/royalty_owner_iud.robot` |
| SOW | this document |
| Evidence | `evidence/` (after a live run) |
| Registry + scorecard rows | `docs/ec_screen_registry.md`, `docs/automation-scorecard.md` |
