# EC Screen IUD Operation Test — Statement of Work (SOW)
**Project:** EC Web App System Test (local sandbox)
**Task:** EC Screen Insert/Update/Delete (IUD) Automation — Bank Account
**Author:** Choong-Yin Lee / Claude Fable 5
**Date:** 2026-06-11
**Version:** 1.0 — COMPLETE (RF suite + Playwright reference, live + DB-verified)

---

## 1. REQUIREMENT
Automate IUD on the **Bank Account** screen with DB-level proof. Constraints: NEVER touch
existing data; test codes `AUTOTEST_BACC_<timestamp>`; local sandbox, user sysadmin.

| Operation | Pass condition | Status |
|---|---|---|
| INSERT | AUTOTEST row in grid AND present in `OV_BANK_ACCOUNT` | PASS |
| UPDATE | Name change visible in grid row | PASS |
| DELETE | End=Start -> gone from grid AND absent in `OV_BANK_ACCOUNT` | PASS |

## 2. DESIGN
| Property | Value |
|---|---|
| Treeview path | Configuration > Assets > Financial Objects > Bank Account |
| Screen type | Manage Object (OV) |
| List/grid id | `manage_object_nav_nav:form:T_data` |
| DB view | `OV_BANK_ACCOUNT` |
| Delete semantics | End Date = Start Date (true delete) |

### DOM reference (rows derived from recon LABELS, not assumed positions)
```
INSERT: Code  tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
        Name  tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
        Start tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
        Sort Code:            tab:tabPanel:objectForm:form:G:0:R:8:C:1:in (MANDATORY text)
UPDATE: Code  tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in (guard)
        Name  tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
DELETE: End   tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
```

### Test data
Code `AUTOTEST_BACC_<timestamp>` | Name `Bank Account <code>` (+` UPD`) | Start=End `2003-01-01`

| Extra mandatory field | Test value |
|---|---|
| Sort Code | `000000` |
| Customer (reference dropdown, banner-discovered) | first available option |
| Bank (reference dropdown, banner-discovered) | first available option |
| Currency (reference dropdown, banner-discovered) | first available option |

## 3. DEVELOPMENT
Generated DATA-DRIVEN from the section recon (`investigation/financial_objects_recon.py`
output): field rows are picked by their `:C:0:la` labels, so row-shift screens and
relocated dates are handled automatically. Extra MANDATORY fields get fixed safe test
values (cleaned up by the delete).

## 4. TEST EXECUTION
| Run | Mode | Result |
|---|---|---|
| RF dryrun | headless | PASS |
| RF live batch | headless | TC01–TC04 4/4 PASS, DB-verified |
| Playwright reference run | headless | see `evidence/bank_account_results.json` |

## 5. DELIVERABLES
RF suite + page object under `tests|pageobjects/.../Financial_Objects/bank_account_*`,
this bundle, and a registry row in `docs/ec_screen_registry.md`.

## 6. LESSONS (section-wide)
1. Label-driven generation beats positional assumptions (VAT Code keeps its dates at
   R1/R2 and Name at R6; Cost Object/Account Mapping insert an Alternative Code row
   into the update form).
2. Extra mandatory TEXT/checkbox fields need no user decision — safe throwaway values
   suffice (dropdowns DO need a decision; this section had none).
3. Same OV invariants as everywhere: navigator GO after save, DB as ground truth,
   End=Start true delete.

## 7. ADDENDUM (2026-08-23, PR #478) — Bank-pattern RF conversion, FINAL of the 23-screen pool

_This addendum documents the RF-layer conversion; Sections 1-6 above describe the ORIGINAL
2026-06-11 Playwright-era build and stay unchanged as historical record._

**What changed:** the RF suite (`bank_account_page.resource` + `bank_account_iud.robot`) was
rebuilt from the OLD hardcoded-field-id pattern (`Fill New Object Form ${BANK_ACCOUNT_INS_CODE}
...`, generated-timestamp code, single Suite-Setup login) to Bank/Berth's label-driven,
properties-file-driven, T2-consolidated pattern — the same shape as every other screen in
Batches 2-11 of the Bank-pattern conversion project. This was the **final screen of the confirmed
23-screen Bank-pattern candidate pool**.

**Classification (confirmed live 2026-08-23):** plain Bank-pattern OV (manage-object), no
mandatory navigator. Grid id `manage_object_nav_nav:form:T_data`. Code label is
SCREEN-PREFIXED **"Bank Account Code"** (not the generic "Code" that Bank itself uses) —
confirmed via a fresh objectForm/updateAttributes ECCell label dump (30 fields).

**Test data used:** fixed code `AUTOTEST_BACC` (not a generated/unique code — every run must
complete TC05 delete so the code is free for the next run); Name `AUTOTEST Bank Account`
(+` UPDATED`); Start Date `2003-01-01`; extra mandatory fields Sort Code (`000000`/`000001`) +
Bank/Customer/Currency reference dropdowns (`__FIRST__`, per Storage Flow Batch-10 precedent —
excluded from the round-trip form-label compare since a resolved reference value can re-render
different display text after reload). A live Vendor dropdown exists but is neither in the
screen's own proven Playwright driver nor static-mandatory — deliberately omitted (IUD-fill-only-
needed-fields).

**Dev story (from PR #478's real body):** rebuilt following the Process Train Batch-9 lesson —
trusted the screen's own already-proven Playwright driver's field set (Sort Code + Bank/Customer/
Currency dropdowns) over a static CSS mandatory scan, since Customer showed
`{mandatory:false}` on the live pass but the proven driver + this SOW confirm it's a
conditional-mandatory business rule (invisible to static scanning, only surfacing as a save-time
banner). Zero edits to shared `manage_object.resource`/`common.resource` (Batch 11 ground rule).

**Result:** live 5/5 (TC01 clean-state, TC02 insert, TC03 update, TC04 find, TC05 delete),
full-tree dryrun 772/772, robocop 7 issues (2 VAR02 + 5 DOC02, same baseline-noise class accepted
throughout the batch series), grid-filter keyword confirmed firing (`Find/Clear Object Row By
Filter` 15x each in output.xml), fresh-connection DB self-clean 0 residual `AUTOTEST%` rows in
`OV_BANK_ACCOUNT` before and after.
