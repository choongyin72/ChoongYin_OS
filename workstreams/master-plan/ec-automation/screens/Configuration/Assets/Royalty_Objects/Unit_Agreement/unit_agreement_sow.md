# EC Screen IUD Operation Test - Statement of Work (SOW)
**Project:** Woodside Pluto ECaaS - EC Web App System Test
**Task:** EC Screen Insert/Update/Delete (IUD) Automation - Unit Agreement
**Screen:** Configuration > Assets > Royalty Objects > Unit Agreement (RC.0055)
**Author:** Choong-Yin Lee / Claude Opus 4.8
**Date:** 2026-06-25 (original); updated 2026-08-28 for the Bank-pattern conversion + deliverable backfill
**Version:** 2.0

---

## 0. UPDATE — 2026-08-28 (deliverable backfill, `docs/lean-deliverable-backfill-workorder.md` Batch 8)

This SOW originally described the 2026-06-25 hand-written, hardcoded-field-id build (Sections 1-4
below, kept unchanged as history). That build was **converted to the full Bank pattern via PR #446**
(merged 2026-08-23T07:08:31Z, Batch 5 of the original Bank-pattern conversion project). This update
records what PR #446 actually changed, pulled from its own PR body — not invented:

- **Classification confirmed:** plain manage-object OV, Bank family — **no navigator** (date-only,
  not OV-GM). Grid `manage_object_nav_nav:form:T_data`, reused via T2's `${OV_MANAGE_OBJECT_TABLE}`
  constant in the T3, not re-hardcoded.
- **View/slug mismatch (confirmed live, registry-documented):** the object view is `OV_UNIT_AGR`
  (base table `UNIT_AGR`, app `EC_REVN`) — the automation slug/screen folder is "unit_agreement" /
  "Unit Agreement"; the DB view name does not simply derive from that slug. `libraries/DbVerify.py`
  calls always cite `ov_unit_agr` explicitly rather than deriving it.
- **Real field labels (live recon, 2026-08-23):** Unit Agreement's own Code/Name labels are
  **screen-prefixed** — "Unit Agreement Code" / "Unit Agreement Name" — NOT the generic "Code"/"Name"
  Bank itself uses. `updateAttributes` (the Update tab) exposes exactly 3 labels: Unit Agreement Code
  (read-only), Unit Agreement Name, Comments. Start Date/End Date live only in `objectForm`
  (insert) and `objectdates` (delete) — never in `updateAttributes`.
- **Mandatory fields (insert):** Unit Agreement Code, Unit Agreement Name, Start Date. Comments is
  optional (`{mandatory:false}`). End Date is deliberately left unset at insert — setting it equal to
  Start Date at insert time would create a zero-length, true-delete-on-insert window.
- **Delete mechanism:** End Date = Start Date via the packed `objectdates` row
  (`tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input`) — hardcoded deliberately (not label-driven),
  same documented precedent as Bank's own `py/ec_object_iud.py` `END_DATE_ID` constant: this row
  packs two fields (Start Date at `C:1`, End Date at `C:3` with its label at `C:2`) that the
  one-field-per-row label scan cannot safely resolve. The exact id was already proven live by this
  screen's own prior hand-written driver before the conversion.
- **Grid-filter wiring** (`Find/Clear Unit Agreement Row By Filter`, delegating to the shared T2
  `Find/Clear Object Row By Filter`) was included in PR #446 from day one, not bolted on later.
- **Dev story / real gotcha (from PR #446's own body):** live recon on 2026-08-23 confirmed the
  screen-prefixed labels and the `updateAttributes` 3-field scope via a throwaway RF script (deleted
  before commit) rather than assuming from the 2026-06-25 SOW's original description below. The
  CURRENT T3 (`unit_agreement_page.resource`) uses the label-driven, properties-file-driven pattern
  described above; Section 2.2's field-id table below reflects the PRE-conversion shape and is kept
  for history only.
- **No shared-file edits** — T2 (`resources/manage_object.resource`) and T1 (`resources/
  common.resource`) keywords were reused as-is.
- **Test code changed from per-run to fixed:** the current live suite uses the FIXED code
  `AUTOTEST_UA` (confirmed absent from `OV_UNIT_AGR` before use), not the original per-run
  `AUTOTEST_UA_<run>` described in Section 2.3 below — TC05 (delete) must complete every run so the
  code stays free for the next run.

### Test data (current, PR #446 / the live suite as of this backfill)
| Field | Value |
|---|---|
| Code | `AUTOTEST_UA` (fixed, not per-run) |
| Name (Insert) | `AUTOTEST Unit Agreement` |
| Name (Update) | `AUTOTEST Unit Agreement UPDATED` |
| Comments (Insert) | `AUTOTEST Comments` |
| Comments (Update) | `AUTOTEST Comments UPDATED` |
| Start Date | `2000-01-01` |
| End Date (Delete) | `2000-01-01` (= Start Date -> true delete) |

---

## 1. REQUIREMENT (original, 2026-06-25 — history)

### 1.1 Objective
Automate Insert, Update, Delete (IUD) on the Unit Agreement screen to validate that the screen
correctly creates, modifies and deletes unit agreement master records, with EC data integrity
maintained throughout the lifecycle and the sandbox left exactly as found.

### 1.2 Scope
Single screen, one PR (Option 1). Unit Agreement is the 4th of the 8 screens under
Configuration > Assets > Royalty Objects.

### 1.3 Constraints
- **NEVER modify existing production/configuration data.**
- All test data prefixed `AUTOTEST_UA_`; a unique per-run code is generated (EC keeps deleted
  codes in the base table, so codes are never reused).
- Target environment: **sandbox** web `https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/`
  (user `sysadmin`), DB ground-truth `localhost:1521/ORCL` (`ECKERNEL_EC`).

### 1.4 Acceptance Criteria
| Operation | Pass Condition |
|---|---|
| INSERT | New record with `AUTOTEST_UA_*` code appears in the list AND in `ov_unit_agr` |
| UPDATE | Unit Agreement Name changed and persisted (visible in the row) |
| DELETE | Record removed from `ov_unit_agr` after End Date = Start Date + Save |
| CLEANUP | Environment returned to pre-test state (object truly deleted, 0 residual) |

---

## 2. DESIGN

### 2.1 Screen classification (recon via resolve_ec_screen.py + scan_ec_screen.py)
| Property | Value |
|---|---|
| Screen name | Unit Agreement |
| Treeview path | Configuration > Assets > Royalty Objects > Unit Agreement |
| Screen type | **Manage-Object (OV)** - Bank family (date-only navigator, NOT OV-GM) |
| CLASS_TYPE | OBJECT (=> OV) |
| TIME_SCOPE | VERSIONED (=> date-effective; DELETE = End Date = Start Date) |
| Base table | UNIT_AGR |
| Object view | `OV_UNIT_AGR` |
| App | EC_REVN |
| Grid tbody id | `manage_object_nav_nav:form:T_data` |
| Mandatory insert fields | Code (R0), Name (R1), Start Date (R2) |

### 2.2 IUD design (identical mechanic to Bank)
```
INSERT:  Insert toolbar -> "New Object" -> objectForm (3 mandatory fields):
           R:0 = Unit Agreement Code   (tab:tabPanel:objectForm:form:G:0:R:0:C:1:in)
           R:1 = Unit Agreement Name   (tab:tabPanel:objectForm:form:G:0:R:1:C:1:in)
           R:2 = Start Date    (tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input)
         -> Save -> GO -> verify in list + ov_unit_agr.

UPDATE:  Click row span -> updateAttributes:
           Code: tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in (read-only)
           Name: tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in (editable)
         -> edit Name -> Save -> GO -> verify.

DELETE:  End Date set equal to Start Date (zero-length window):
           End Date: tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
         -> Save -> GO -> object removed from ov_unit_agr (TRUE delete, DB-verified).
```

### 2.3 Test data
| Field | Value |
|---|---|
| Code | `AUTOTEST_UA_<run>` (unique per run) |
| Name (Insert) | `AUTOTEST Unit Agreement <run>` |
| Name (Update) | `AUTOTEST Unit Agreement <run> UPDATED` |
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
| Playwright bundle | `playwright/ec_iud_unit_agreement.py` |
| RF T3 page object | `pageobjects/Configuration/Assets/Royalty_Objects/unit_agreement_page.resource` |
| RF test suite | `tests/Configuration/Assets/Royalty_Objects/unit_agreement_iud.robot` |
| SOW | this document |
| Evidence | `evidence/` (after a live run) |
| Registry + scorecard rows | `docs/ec_screen_registry.md`, `docs/automation-scorecard.md` |
