# EC Screen IUD Operation Test - Statement of Work (SOW)
**Project:** Woodside Pluto ECaaS - EC Web App System Test
**Task:** EC Screen Insert/Update/Delete (IUD) Automation - Tract
**Screen:** Configuration > Assets > Royalty Objects > Tract (RC.0056)
**Author:** Choong-Yin Lee / Claude Opus 4.8
**Date:** 2026-06-26
**Version:** 1.0

---

## 1. REQUIREMENT

### 1.1 Objective
Automate Insert, Update, Delete (IUD) on the Tract screen to validate creation, modification
and deletion of tract master records, with EC data integrity maintained and the sandbox left
exactly as found.

### 1.2 Scope
Single screen, one PR (Option 1). Tract is the 5th Royalty Objects screen built and the
**first OV-GM (gated)** one in the folder.

### 1.3 Constraints
- **NEVER modify existing production/configuration data.** Unit Agreement parents are READ-ONLY seed.
- All test data prefixed `AUTOTEST_TR_`; unique per-run code (EC keeps deleted codes in the base table).
- Target: **sandbox** web `https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/` (`sysadmin`),
  DB `localhost:1521/ORCL` (`ECKERNEL_EC`).

### 1.4 Acceptance Criteria
| Operation | Pass Condition |
|---|---|
| INSERT | New `AUTOTEST_TR_*` code appears in the UA-filtered list AND in `ov_tract` |
| UPDATE | Tract Name changed and persisted (visible in the row) |
| DELETE | Record removed from `ov_tract` after End Date = Start Date + Save |
| CLEANUP | Environment returned to pre-test state (0 residual) |

---

## 2. DESIGN

### 2.1 Screen classification (recon: resolve_ec_screen.py + scan_ec_screen.py + tract_recon.py)
| Property | Value |
|---|---|
| Screen name | Tract |
| Treeview path | Configuration > Assets > Royalty Objects > Tract |
| Screen type | **OV-GM (Manage-Object, gated)** - NOT plain Bank family |
| CLASS_TYPE / TIME_SCOPE | OBJECT (OV) / VERSIONED (date-effective; DELETE = End=Start) |
| Base table / view | `TRACT` / `OV_TRACT` |
| App | EC_REVN |
| **Navigator (gated)** | date `nav:form:G:0:R:1:C:0:da_input` + **mandatory dd `nav:form:G:1:R:1:C:0:dd` = Unit Agreement** + GO `button:form:B` |
| Nav options | Unit Agreement 1..4 (Unit Agreement 1 has existing data) |
| Grid tbody id | **`manageObject:form:T_data`** (OV-GM grid; lazy redraw) |
| Insert mandatory | Code R0, Name R1, Start Date R2, **Unit Agreement dd R3 (`objectForm…R:3:C:1:dd`, must = nav scope)** |
| Update / Delete | updateAttributes Code R0 / Name R1 ; objectdates End Date R0:C3 (EC-standard, shared with Transport System) |

### 2.2 IUD design (OV-GM, mirrors Transport System exemplar)
```
NAV:     pick Unit Agreement (e.g. 'Unit Agreement 1') in nav dd + GO -> grid loads.
INSERT:  Insert -> New Object -> objectForm: Code R0 / Name R1 / Start Date R2 +
         Unit Agreement dd R3 = same UA as nav (grid-visibility parent) -> Save -> refresh.
UPDATE:  select row -> updateAttributes Name R1 -> Save -> refresh.
DELETE:  objectdates End Date R0:C3 = Start Date (zero-length window) -> Save ->
         extra Apply Navigator (lazy GM redraw) -> gone from ov_tract (TRUE delete).
```
**Date:** `${TEST_START_DATE_REFDD}` - the Unit Agreement parent must be effective at the form
Start Date for the reference dropdown to offer it ([[reference_ec_object_start_date_version]]).

### 2.3 Test data
| Field | Value |
|---|---|
| Code | `AUTOTEST_TR_<run>` (unique per run) |
| Name (Insert/Update) | `AUTOTEST Tract <run>` / `... UPDATED` |
| Nav + Insert parent (Unit Agreement) | `Unit Agreement 1` |
| Start/End Date | `${TEST_START_DATE_REFDD}` (End = Start -> true delete) |

### 2.4 Technology + deliverables
RF suite layered T3 -> T2 (`manage_object.resource`, reused as-is - no shared-file edits) + T1
(`common.resource`) + `DbVerify.py`. **RF-only**, following the OV-GM exemplar precedent
(Transport System ships no Playwright bundle); the live + DB-verified RF suite is the proof.
- T3: `pageobjects/Configuration/Assets/Royalty_Objects/tract_page.resource`
- Suite: `tests/Configuration/Assets/Royalty_Objects/tract_iud.robot`
- Evidence: `evidence/` (RF step captures from the live run)

---

## 3. KNOWN RISKS
- **OV-GM lazy redraw** - grid redraws asynchronously after Save+GO; T3 delete adds an extra
  `Apply Navigator`, and `Row Should Exist` (T2) awaits the row (R17).
- Insert parent dd MUST equal the nav Unit Agreement or the row never lists under the filter.
- Reference dropdown only offers Unit Agreements effective at the form Start Date -> use REFDD date.
