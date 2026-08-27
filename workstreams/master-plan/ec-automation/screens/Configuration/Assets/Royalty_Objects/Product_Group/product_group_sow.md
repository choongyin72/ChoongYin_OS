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
| Playwright bundle | `playwright/ec_iud_product_group.py` (legacy, predates the Universal Screen Engine; kept as a reference walkthrough, not rebuilt) |
| RF T3 page object | `pageobjects/Configuration/Assets/Royalty_Objects/product_group_page.resource` |
| RF test suite | `tests/Configuration/Assets/Royalty_Objects/product_group_iud.robot` |
| SOW | this document |
| Evidence | `evidence/` (original 2026-06-25 run) + `evidence/backfill_2026-08-28/` (backfill re-run) |
| Registry + scorecard rows | `docs/ec_screen_registry.md`, `docs/automation-scorecard.md` |

---

## 5. DEV STORY / REVISION HISTORY

### 5.1 Original build (2026-06-25)
Built as a standalone Playwright + RF bundle against the older hardcoded-field-id RF pattern, per
the design in Section 2 above (sandbox web app, `AUTOTEST_PG_<run>` unique-per-run codes).

### 5.2 Bank-pattern conversion (PR #445, merged 2026-08-23, Batch 5)
Rebuilt Product Group's RF suite from the older hardcoded-field-id pattern to the label-driven,
properties-file-driven, T2-consolidated **Bank pattern** (mirrors `state_page.resource`/
`state_iud.robot` exactly), including explicit grid-filter wiring from day one. Real facts pulled
from the PR body:
- Live recon (New Object form + `updateAttributes` ECCell label dump) confirmed screen-prefixed
  labels "Product Group Code"/"Product Group Name" (NOT the generic "Code"/"Name" Bank itself
  uses) and that only **Start Date** is CSS-mandatory beyond Code/Name — Sort Order, Product Group
  Type (dropdown), and Comments are optional and deliberately left out of the IUD flow
  (fill-only-needed-fields convention).
- The suite grew from 4 TCs to 5 TCs (added TC04 Find), switched to per-TC login/logout (matching
  Bank/State's convention), and moved to a **fixed** test code `AUTOTEST_PRODUCT_GROUP` (confirmed
  free live) rather than the original per-run generated code.
- New testdata: `testdata/product_group_{insert,update,form_verify,grid_verify}.properties`.
- New dedicated credential pair `PRODUCT_GROUP_EC_USER`/`PRODUCT_GROUP_EC_PASS`
  (`resources/credentials.py`, additive only).
- No shared T1/T2 files (`resources/common.resource`, `resources/manage_object.resource`) were
  touched.
- Verification cited in the PR body: live run 5/5 PASS; fresh oracledb connection post-run
  `SELECT COUNT(*) FROM OV_PRODUCT_GROUP WHERE CODE = 'AUTOTEST_PRODUCT_GROUP'` → `0` (self-clean);
  `output.xml` grep for `Find Product Group Row By Filter` → 5 hits; robocop 9 issues (4 VAR02 + 5
  DOC02), matching the established Batch 5 baseline exactly (no new issue classes); full-tree
  dryrun 745/745 (net +1 over the prior 744 baseline, since the suite grew from 4 to 5 TCs).
- No real regression or wrong turn was disclosed in PR #445's own body.

### 5.3 This backfill (2026-08-28, Batch 7 of `docs/lean-deliverable-backfill-workorder.md`)
PR #445 was built under the 2026-08-23 lean-waiver rule (Section G of
`docs/IUD-DELIVERABLE-CHECKLIST.md`), which at the time waived JOURNAL/evidence/KB-map/CHECKLIST
for Bank-pattern conversions. That waiver was retired by the owner 2026-08-27 (Section H). This
backfill adds the retroactively-required `JOURNAL.md`, `CHECKLIST.md`, KB selector map
(`ec-ui-knowledge/screens/product_group.md`), and a fresh dryrun + live evidence-capture re-run of
the already-proven suite under `evidence/backfill_2026-08-28/`. **No RF automation file was
rebuilt, modified, or re-verified from scratch** — the existing `product_group_page.resource` and
`product_group_iud.robot` (both from PR #445) were re-run as-is for evidence capture only. This
SOW and `README.md` (which predated the JOURNAL rule) were also refreshed to describe the current
Bank-pattern shape instead of only the original 2026-06-25 build.
