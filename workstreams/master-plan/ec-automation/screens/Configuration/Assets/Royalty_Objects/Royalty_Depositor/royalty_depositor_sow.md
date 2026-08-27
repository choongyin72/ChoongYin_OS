# EC Screen IUD Operation Test - Statement of Work (SOW)
**Project:** Woodside Pluto ECaaS - EC Web App System Test
**Task:** EC Screen Insert/Update/Delete (IUD) Automation - Royalty Depositor
**Screen:** Configuration > Assets > Royalty Objects > Royalty Depositor (RC.0052)
**Author:** Choong-Yin Lee / Claude Opus 4.8
**Date:** 2026-06-25 (original build) — **updated 2026-08-28** to reflect the Bank-pattern
conversion (PR #448, merged 2026-08-23, Batch 5 of the Bank-pattern conversion project) and the
lean-deliverable backfill (`docs/lean-deliverable-backfill-workorder.md` Batch 8, owner decision
2026-08-27 retiring the lean waiver).
**Version:** 2.0

---

## 0. UPDATE NOTE (2026-08-28 backfill)

This SOW originally described the pre-conversion, hardcoded-field-id Playwright/RF driver
(2026-06-25). **PR #448** (merged 2026-08-23) converted the RF stack to the label-driven,
properties-file-driven, T2-consolidated **Bank pattern** (mirrors `bank_page.resource`/
`state_page.resource`), per the `ec-bank-pattern-converter` skill. Section 2 below is updated to
match the real, current RF implementation; Section 1 (requirement/acceptance criteria) is
unchanged — the business intent of the screen never changed, only the automation shape.

**Real dev story from PR #448 (verbatim facts, not invented):** the conversion replaced the older
hardcoded-field-id clone with the label-driven/properties-file-driven/T2-consolidated pattern,
including explicit grid-filter wiring from day one (`Find/Clear Royalty Depositor Row By Filter`).
Live recon on 2026-08-23 confirmed the screen uses SCREEN-PREFIXED labels ("Royalty Depositor
Code"/"Royalty Depositor Name", matching State's own "State Code" precedent) and a much richer
`objectForm` than the prior driver ever used (Official Name, Comments, System Company, Address
Line 1-8, Phone/Fax/Email, Country, etc.) — only Code/Name/Start Date are mandatory (live
`MandatoryCellStyle` scan), so field scope was deliberately kept unchanged from the already-proven
prior driver (no scope expansion). The first live attempt hit a transient shared-sandbox account
lockout plus a cross-session "unsaved changes" dialog artifact from a concurrent parallel Batch-5
agent sharing the same `sysadmin` login on the shared sandbox — not a defect in this screen's
automation; confirmed clear 5/5 on retry after self-cleaning a leftover test row. A 2026-08-25
follow-up alignment fix removed a leftover inline `Royalty Depositor Should Exist In DB` keyword
(and its TC02 call) that had violated Bank's pure-screen-only verification convention
(2026-08-18) — the same deviation class as DOA Credit Limit (PR #503); re-verified live 5/5,
full-tree dryrun 841/841 at that time, DB self-clean 0 residual.

---

## 1. REQUIREMENT

### 1.1 Objective
Automate Insert, Update, Delete (IUD) on the Royalty Depositor screen to validate that the
screen correctly creates, modifies and deletes royalty-depositor master records, with EC data
integrity maintained throughout the lifecycle and the sandbox left exactly as found.

### 1.2 Scope
Single screen, one PR (Option 1). Royalty Depositor is the 2nd of the 8 screens under
Configuration > Assets > Royalty Objects (sibling of Royalty Owner).

### 1.3 Constraints
- **NEVER modify existing production/configuration data.**
- All test data prefixed `AUTOTEST_RD_`; a unique per-run code is generated (EC keeps deleted
  codes in the base table, so codes are never reused).
- Target environment: **sandbox** web `https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/`
  (user `sysadmin`), DB ground-truth `localhost:1521/ORCL` (`ECKERNEL_EC`).

### 1.4 Acceptance Criteria
| Operation | Pass Condition |
|---|---|
| INSERT | New record with `AUTOTEST_RD_*` code appears in the list AND in `ov_royalty_depositor` |
| UPDATE | Royalty Depositor Name changed and persisted (visible in the row) |
| DELETE | Record removed from `ov_royalty_depositor` after End Date = Start Date + Save |
| CLEANUP | Environment returned to pre-test state (object truly deleted, 0 residual) |

---

## 2. DESIGN

### 2.1 Screen classification (recon via resolve_ec_screen.py + scan_ec_screen.py)
| Property | Value |
|---|---|
| Screen name | Royalty Depositor |
| Treeview path | Configuration > Assets > Royalty Objects > Royalty Depositor |
| Screen type | **Manage-Object (OV)** - Bank family (date-only navigator, NOT OV-GM) |
| CLASS_TYPE | OBJECT (=> OV) |
| TIME_SCOPE | VERSIONED (=> date-effective; DELETE = End Date = Start Date) |
| Base table | COMPANY |
| Version table | COMPANY_VERSION |
| Object view | `OV_ROYALTY_DEPOSITOR` |
| App | EC_REVN |
| Grid tbody id | `manage_object_nav_nav:form:T_data` |
| Toolbar | Insert + Delete enabled; New Object form has 3 yellow-mandatory fields |

### 2.2 IUD design (identical mechanic to Bank / Royalty Owner)
```
INSERT:  Insert toolbar -> "New Object" -> objectForm (3 mandatory fields):
           R:0 = Royalty Depositor Code   (tab:tabPanel:objectForm:form:G:0:R:0:C:1:in)
           R:1 = Royalty Depositor Name   (tab:tabPanel:objectForm:form:G:0:R:1:C:1:in)
           R:2 = Start Date               (tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input)
         -> Save -> GO -> verify in list + ov_royalty_depositor.

UPDATE:  Click row span -> updateAttributes:
           Code: tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in (read-only)
           Name: tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in (editable)
         -> edit Name -> Save -> GO -> verify.

DELETE:  EC toolbar Delete disabled for date-effective master data.
         End Date set equal to Start Date (zero-length window):
           End Date: tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
         -> Save -> GO -> object removed from ov_royalty_depositor (TRUE delete, DB-verified).
```

### 2.3 Test data
| Field | Value |
|---|---|
| Code | `AUTOTEST_RD_<run>` (unique per run) |
| Name (Insert) | `AUTOTEST Royalty Depositor <run>` |
| Name (Update) | `AUTOTEST Royalty Depositor <run> UPDATED` |
| Start Date | `2000-01-01` |
| End Date (Delete) | `2000-01-01` (= Start Date -> true delete) |

### 2.4 Technology stack — CURRENT (post-PR #448, Bank pattern)
Robot Framework only (the pre-existing standalone `playwright/ec_iud_royalty_depositor.py` bundle
stays as a legacy reference — the Universal Screen Engine now covers that role for new work,
per owner decision 2026-08-27, and this bundle is NOT rebuilt to a Playwright driver here).
RF stack, T3 -> T2 -> T1:
- T3 page object: `pageobjects/Configuration/Assets/Royalty_Objects/royalty_depositor_page.resource`
  — label-driven field resolution (`code_label=Royalty Depositor Code`), properties-file-driven
  test data (`testdata/royalty_depositor_{insert,update,form_verify,grid_verify}.properties`),
  explicit grid-filter wiring (`Find/Clear Royalty Depositor Row By Filter`), per-TC login/logout.
- T2: `resources/manage_object.resource` (reused as-is, no shared-file edits).
- T1: `resources/common.resource` (reused as-is).
- DB verify: `libraries/DbVerify.py` — `Verify Object Insert Exists` / `Verify Object Found` /
  `Verify Object Removed`, all against `OV_ROYALTY_DEPOSITOR`.
- Fixed test code `AUTOTEST_ROYALTY_DEP` (matches Bank/Account's own convention), not a
  per-run-generated code — every run must complete TC05 (delete) so the code is free for the
  next run.

### 2.5 Grid/label facts confirmed live on 2026-08-23 (PR #448 recon)
- Grid columns: **Royalty Depositor Code / Royalty Depositor Name / Start Date / End Date**
  (screen-prefixed labels, not generic "Code"/"Name").
- Only Code / Name / Start Date are yellow-mandatory on Insert; every other `objectForm` field
  (Official Name, Comments, System Company, Company Number, Registration Details, Interface
  Sequence Owner, Address Line 1-8, Phone, Fax, Email, Original Number, Fin Code, Country) is
  optional and deliberately out of scope (no scope expansion vs. the prior driver).
- Update form (`updateAttributes`) exposes Name only for edit; Code is read-only; Start/End Date
  live only in `objectdates`, not `updateAttributes`.

---

## 3. KNOWN RISKS
- Not an OV-GM screen (date-only navigator) - no lazy-redraw risk; standard Bank-family timing.
- EC keeps deleted codes in the base table; unique per-run codes avoid re-insert rejection. The
  current RF suite mitigates this by re-deleting the same fixed code every run rather than
  generating a fresh code per run (see 2.4).
- Shared-sandbox risk (materialized once, PR #448): a concurrent agent's session on the same
  `sysadmin` login can produce a transient account lockout or a stale "unsaved changes" dialog —
  not a defect in this screen's automation; mitigated by a single retry, never a killed process
  (per this repo's shared-environment process rule).

---

## 4. DELIVERABLES
| Deliverable | Path | Status |
|---|---|---|
| RF T3 page object | `pageobjects/Configuration/Assets/Royalty_Objects/royalty_depositor_page.resource` | Done (PR #448) — NOT modified by this backfill |
| RF test suite | `tests/Configuration/Assets/Royalty_Objects/royalty_depositor_iud.robot` | Done (PR #448) — NOT modified by this backfill |
| Testdata properties (4 files) | `testdata/royalty_depositor_{insert,update,form_verify,grid_verify}.properties` | Done (PR #448) — NOT modified |
| Legacy Playwright bundle (reference only) | `playwright/ec_iud_royalty_depositor.py` | Pre-existing (2026-06-25); waived from rebuild per Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md` |
| SOW | this document | Updated 2026-08-28 (this backfill) |
| README | `README.md` | Updated 2026-08-28 (this backfill) |
| JOURNAL | `JOURNAL.md` | Added 2026-08-28 (this backfill) |
| Evidence | `evidence/2026-08-28-live-run/` | Added 2026-08-28 (this backfill; live 5/5) |
| CHECKLIST | `CHECKLIST.md` | Added 2026-08-28 (this backfill) |
| KB selector map | `ec-ui-knowledge/screens/royalty_depositor.md` | Added 2026-08-28 (this backfill) |
| Registry + scorecard rows | `docs/ec_screen_registry.md`, `docs/automation-scorecard.md` | Done (PR #448) — NOT modified by this backfill |
