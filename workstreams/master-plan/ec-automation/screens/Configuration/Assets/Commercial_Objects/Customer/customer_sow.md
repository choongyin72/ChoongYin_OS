# EC Screen IUD Operation Test — Statement of Work (SOW)
**Project:** EC Web App System Test (local sandbox)
**Task:** EC Screen Insert/Update/Delete (IUD) Automation — Customer
**Author:** Choong-Yin Lee / Claude Fable 5
**Date:** 2026-06-12 (original); **updated 2026-08-28** (Bank-pattern RF conversion backfill)
**Version:** 2.0 — RF suite converted to the Bank pattern (PR #435, merged 2026-08-23); this SOW
backfilled per `docs/lean-deliverable-backfill-workorder.md` (Batch 6). Legacy Playwright
reference bundle (Section "Legacy" below) predates the conversion and is unchanged — items 4/5
(Playwright driver/investigation) are permanently waived going forward per
`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H, but this bundle already had them from the
original 2026-06-12 build, so they are left in place, untouched.

---

## 1. CLASSIFICATION
**Plain Bank-pattern OV (Manage-Object), no navigator.** Confirmed live 2026-08-23 (PR #435): 0
mandatory navigator dropdowns — only the universal Date + GO as-at-date bar. Same layout family
as Bank/Country/Vendor.

## 2. REQUIREMENT
Automate IUD on the **Customer** screen with DB-level proof. Constraints: NEVER touch
existing data; fixed test code `AUTOTEST_CUST` (RF suite; the current, reusable convention —
supersedes the original `AUTOTEST_CUST_<timestamp>` scheme from the 2026-06-12 Playwright build).

| Operation | Pass condition | Status |
|---|---|---|
| INSERT | AUTOTEST row in grid AND present in `OV_CUSTOMER` | PASS (live 5/5, 2026-08-23; re-confirmed 2026-08-28) |
| UPDATE | Name + Description change visible in grid/form | PASS |
| FIND | Grid + form round-trip match | PASS |
| DELETE | End=Start -> gone from grid AND absent in `OV_CUSTOMER` | PASS |

## 3. DESIGN
| Property | Value |
|---|---|
| Treeview path | Configuration > Assets > Commercial Objects > Customer |
| Screen type | Manage Object (OV), Bank pattern, no navigator |
| Grid id | `manage_object_nav_nav:form:T_data` (shared T2 constant `${OV_MANAGE_OBJECT_TABLE}`) |
| DB view | `OV_CUSTOMER` |
| Delete semantics | End Date = Start Date (true delete) |
| RF page object | `pageobjects/Configuration/Assets/Commercial_Objects/customer_page.resource` |
| RF suite | `tests/Configuration/Assets/Commercial_Objects/customer_iud.robot` |

### Mandatory fields (confirmed live 2026-08-23, identical set on objectForm AND updateAttributes)
Code, Name, Start Date, ERP Customer Code, Official Name, Customer Group (reference dropdown;
real first option is the literal `Non Group`, used verbatim per the VAT Code round-trip-verify
gotcha — `__FIRST__` never resolves to literal text for the TC02 comparison). Description is
optional but included (business-realistic test data, matches Bank's Name+Description update
pair). Start Date/End Date live only in `objectdates`, not `updateAttributes`.

### Test data (current RF properties files)
- `testdata/customer_insert.properties` — Code `AUTOTEST_CUST`, Name `AUTOTEST Customer`,
  Start Date `2000-01-01`, Description `AUTOTEST Customer Description`, ERP Customer Code
  `ERP999`, Official Name `AUTOTEST Official Name`, Customer Group `Non Group`.
- `testdata/customer_update.properties` — Name `AUTOTEST Customer UPDATED`, Description
  `AUTOTEST Customer Description UPDATED`.
- `testdata/customer_form_verify.properties` / `customer_grid_verify.properties` — merged
  post-update expected state for TC04's round-trip check.

## 4. DEVELOPMENT — dev story (from PR #435, merged 2026-08-23)
Converted the Customer screen's IUD RF suite from the old hardcoded-field-id pattern to
Bank/Account's label-driven, properties-file-driven, T2-consolidated pattern, with explicit
grid-filter wiring (`Find Customer Row By Filter`) included from the start rather than deferred.
Same batch as Field Group/Licence/MMS Lease/Operator Lease (Batch 3 of the original Bank-pattern
conversion project). Live recon before build confirmed the screen nav-free (0 mandatory nav
dropdowns) and confirmed the mandatory field set matched on both objectForm and
updateAttributes. Customer Group's literal first option (`Non Group`) was used verbatim in the
insert properties, not `__FIRST__`, per the VAT Code round-trip-verify gotcha carried over from
Batch 2. No shared T1/T2 files were touched; build done in an isolated clone under
`Workplaces/customer/`, own branch, no other Batch-3 screen touched.

## 5. TEST EXECUTION
| Run | Mode | Result |
|---|---|---|
| RF full-tree `--dryrun` | headless | 883/883 PASS (2026-08-28 backfill re-run) |
| RF live (suite-scoped) | headless | 5/5 PASS (`customer_iud.robot`, both 2026-08-23 original and 2026-08-28 backfill re-run) |
| robocop (`customer_page.resource` + `customer_iud.robot`) | — | 7 issues (2 VAR02 + 5 DOC02) — same count both runs |
| DB self-clean (fresh connection) | — | `OV_CUSTOMER` `AUTOTEST_CUST` = 0 residual, both runs |
| Playwright reference run (legacy, unchanged) | headless | see `evidence/customer_results.json` |

## 6. DELIVERABLES
RF suite + page object under `tests|pageobjects/.../Commercial_Objects/customer_*`, this bundle
(SOW/README/JOURNAL/evidence/CHECKLIST — backfilled 2026-08-28), registry row in
`docs/ec_screen_registry.md`, KB selector map `ec-ui-knowledge/screens/customer.md`.

## Legacy (2026-06-12 Playwright reference build — unchanged, not part of this backfill's scope)
The original 2026-06-12 build produced a standalone Playwright reference flow
(`playwright/ec_iud_customer.py`) plus its own recon scripts (`investigation/`) and evidence
(`evidence/customer_*.png`, `evidence/customer_results.json`), predating both the RF Bank-pattern
conversion (PR #435) and the current CHECKLIST rule that permanently waives items 4/5
(Playwright driver/investigation) for Bank-pattern work going forward. These files are left
as-is — nothing in them was touched by this backfill.
