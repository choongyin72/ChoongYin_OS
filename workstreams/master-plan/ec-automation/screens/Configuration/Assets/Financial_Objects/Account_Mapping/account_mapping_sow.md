# EC Screen IUD Operation Test — Statement of Work (SOW)
**Project:** EC Web App System Test (local sandbox)
**Task:** EC Screen Insert/Update/Delete (IUD) Automation — Account Mapping
**Author:** Choong-Yin Lee / Claude
**Date:** 2026-06-11 (original) — updated 2026-08-28 (deliverable backfill,
`docs/lean-deliverable-backfill-workorder.md` Batch 8, covering the 2026-08-23 RF Bank-pattern
conversion, PR #450)
**Version:** 2.0 — supersedes v1.0's PARKED status. The old v1.0 (below, kept for history) recorded
the RF live batch as "TC02 blocked; suite preserved in tests/.../_parked/" using per-run-timestamped
codes and first-available dropdown picks. That parked suite was fully rebuilt (not merely
un-parked) by PR #450 (2026-08-23, Batch 6 — the FINAL screen of the original 23-screen Bank-pattern
conversion candidate pool) into the label-driven, properties-file-driven, T2-consolidated Bank
pattern matching Bank/Customer/Cost Object Mapping. Live RF 5/5 PASS confirmed at that PR's merge.

---

## 1. REQUIREMENT
Automate IUD on the **Account Mapping** screen with DB-level proof. Constraints: NEVER touch
existing data; fixed test code `AUTOTEST_AM` (confirmed absent from `OV_FIN_ACCOUNT_MAPPING` before
use, freed again by TC05 each run); local sandbox, dedicated `ACCOUNT_MAPPING_EC_USER`/
`ACCOUNT_MAPPING_EC_PASS` credentials (`resources/credentials.py`).

| Operation | Pass condition | Status |
|---|---|---|
| INSERT | `AUTOTEST_AM` row in grid AND present in `OV_FIN_ACCOUNT_MAPPING` | PASS (PR #450) |
| UPDATE | Name/Description change visible in grid + form | PASS (PR #450) |
| DELETE | End=Start -> gone from grid AND absent in `OV_FIN_ACCOUNT_MAPPING` | PASS (PR #450) |

## 2. DESIGN
| Property | Value |
|---|---|
| Treeview path | Configuration > Assets > Financial Objects > Account Mapping |
| Screen type | Manage Object (OV) — plain custom-URL OV, **no navigator** (GO-button locator
`button:form:B` confirmed 0 matches live, 2026-08-23) — Bank-pattern classification |
| List/grid id | `manageObject:form:T_data` (screen-local constant, NOT the shared T2
`${OV_MANAGE_OBJECT_TABLE}`, which resolves to the navigator-based `manage_object_nav_nav:form:T_data`) |
| DB view | `OV_FIN_ACCOUNT_MAPPING` (generic `CODE` column per `libraries/DbVerify.py`) |
| Delete semantics | End Date = Start Date (true delete), field id
`tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (hardcoded, not label-driven — packed
Start/End Date row, same convention as Bank/Customer/Cost Object Mapping) |
| Mandatory reference dropdowns (8, live-confirmed 2026-08-23 via a raw outerHTML/class dump —
this screen puts the mandatory class on the input/dd-span itself, one level deeper than the usual
wrapping-tableCell technique) | Line Item Type, Financial Code, Company Category, Status,
Debit / Credit, Debit PK, Credit PK, Financial Account |
| Cascade dependency (statically non-mandatory but functionally required) | Account Category
scopes Financial Account's option list — same pattern as Cost Object Mapping's Object
Type -> Cost Object; listed BEFORE Financial Account in the insert properties file |
| Grid shape | 75-row custom grid, 13 columns (Code, Name, Product, Line Item Type, Financial
Code, Company Category, Company, Status, Debit / Credit, Debit PK, Credit PK, Account Category,
Financial Account) — notably **NO Start Date column**, unlike Bank's simpler 3-column grid (same
documented variant as Regulatory Permits, Batch 2); grid-verify checks only Code/Name |

### Test data (current, PR #450)
Fixed code `AUTOTEST_AM` | Name `AUTOTEST Account Mapping` (+` UPDATED`) | Start Date 2003-01-01 |
Description `AUTOTEST Account Mapping Description` (+` UPDATED`)

| Dropdown | Value used | Note |
|---|---|---|
| Line Item Type | All Line Item Types | re-renders as short code `ALL` after reload — excluded from the live-DOM round-trip form-label list, DB ground-truth still covers it |
| Financial Code | Journal Entry | |
| Company Category | All | |
| Status | Accrual | |
| Debit / Credit | Credit | |
| Debit PK | Debit General Ledger (40) | |
| Credit PK | Credit General Ledger (50) | |
| Account Category | Revenue | cascade dependency for Financial Account |
| Financial Account | ACCRUAL CR Acct | |

This exact 9-field combination is the screen's real unique key (ALT_CODE pattern
`LineItemType_FinancialCode_CompanyCategory_Status_DebitCredit` = `JOU_ENT_ALL_ALL_ALL_ACCRUAL_CREDIT`)
— reused unchanged from this screen's own prior Playwright IUD bundle, which first proved it
live-PASS on 2026-06-12 (see `evidence/account_mapping_results.json` in this bundle); a fresh DB
check on 2026-08-23 re-confirmed the combination was still free before PR #450 reused it.

## 3. DEVELOPMENT (real history, from PR #450's body + `account_mapping_page.resource`)
Converted from the older hardcoded-field-id IUD suite (v1.0's PARKED state) to the label-driven,
properties-file-driven, T2-consolidated Bank pattern — the FINAL screen of the original 23-screen
Bank-pattern conversion candidate pool (Batch 6). Recon-first: live DOM recon confirmed field
labels, the mandatory-dropdown set (via the input/dd-span mandatory class technique), and the grid's
13 columns with no Start Date column. Confirmed live that this is NOT a navigator-scope mismatch
despite the "Mapping" name (genuine Code/Name manage-object OV with an `objectForm`-New-Object flow,
same outcome as Cost Object Mapping in Batch 4).

**Real gotcha hit (1 retry, root-caused, not blind trial-and-error):** Line Item Type re-renders as
the short internal code `ALL` after any `updateAttributes` reload, instead of the literal `All Line
Item Types` text picked at Insert time — the same documented re-render gotcha as DOA Credit Limit's
Role Name (Batch 4). Fixed by excluding Line Item Type from the live-DOM round-trip form-label list
(`@{ACCOUNT_MAPPING_FORM_LABELS}`), relying on DB ground-truth (TC02's `Code Should Be Present In
View` DbVerify assertion) for that field instead.

## 4. TEST EXECUTION
| Run | Mode | Result |
|---|---|---|
| RF suite (PR #450, 2026-08-23) | live headless | 5/5 PASS (1 retry — Line Item Type gotcha above) |
| Fresh-connection DB self-clean (PR #450) | read-only oracledb | 0 residual `AUTOTEST_AM` rows in
`OV_FIN_ACCOUNT_MAPPING` (75 rows total, unchanged before/after) |
| This backfill's evidence-capture re-run (2026-08-28) | see `README.md` + `evidence/backfill_2026-08-28/` | see JOURNAL.md |
| Original Playwright reference run (2026-06-12) | headless | see `evidence/account_mapping_results.json` |

## 5. DELIVERABLES
RF suite + page object under `tests|pageobjects/.../Financial_Objects/account_mapping_*`
(pre-existing, PR #450, NOT modified by this backfill), this bundle (SOW/README/JOURNAL/evidence/
CHECKLIST refreshed by the 2026-08-28 backfill), registry row in
`docs/ec_screen_registry.md` (already present from PR #450), KB map
`ec-ui-knowledge/screens/account_mapping.md` (created by this backfill).

## 6. LESSONS (section-wide, carried from v1.0 + PR #450)
1. Label-driven generation beats positional assumptions.
2. Config-combination screens like Account Mapping: the reference-dropdown COMBINATION (not any
   single dropdown) is the real unique key — check the combination is free, not just one field.
3. Same OV invariants as everywhere: DB as ground truth, End=Start true delete, IUD fills only
   needed fields.
4. A field that shows its literal option text right after Insert can silently re-render as a short
   internal code after a reload — verify round-trip fields live before trusting them in the
   round-trip check list; fall back to DB ground truth for any field with this behavior.

---

## v1.0 (2026-06-11/12, superseded — kept for history)
Version 1.0 — COMPLETE 2026-06-12: unparked via VALID-AND-UNUSED combination cloned from the 75
existing rows (combination = unique key; ALT_CODE pattern FIN_PRODUCT_LIT_CC_STATUS_CLASS). Test
combo `JOU_ENT_ALL_ALL_ALL_ACCRUAL_CREDIT` + proven trio (Account Category Revenue / Financial
Account ACCRUAL CR Acct / PKs 40-50). Start Date 2003-01-01 (date-version rule). RF live batch:
"TC02 blocked; suite preserved in tests/.../_parked/" (per-run-timestamped `AUTOTEST_AM_<timestamp>`
codes, first-available dropdown picks) — this is the state PR #450 fully rebuilt.
