# Screen: Product Group

- **Type:** OV (manage-object, date-effective), **Bank pattern** (label-driven,
  properties-file-driven, T2-consolidated, explicit grid-filter wiring)
- **Treeview path:** Configuration > Assets > Royalty Objects > Product Group (RC.0053)
- **DB view (ground truth):** `OV_PRODUCT_GROUP` (base `PRODUCT_GROUP`; app `EC_REVN`)
- **Last verified:** 2026-08-28 (backfill re-run) - originally converted 2026-08-23 (PR #445,
  Batch 5) - EC sandbox web `https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/` - live I-U-D
  5/5 DB-verified, self-clean 0 residual.
- **Pattern:** follows the Bank pattern (see `bank.md`); this file records what is Product
  Group-specific. Distinct from "Product" (CO.0007) and "Product Description" (CD.0012) -
  confirmed distinct screens.

## Selectors `[from pageobjects/Configuration/Assets/Royalty_Objects/product_group_page.resource — transcribed, not re-scanned]`

| Purpose | Selector / value |
|---|---|
| Grid id | `manage_object_nav_nav:form:T_data` (`${OV_MANAGE_OBJECT_TABLE}`, shared T2 constant) |
| Delete End Date field | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` |
| Insert Code | `tab:tabPanel:objectForm:form:G:0:R:0:C:1:in` (label "Product Group Code") |
| Insert Name | `tab:tabPanel:objectForm:form:G:0:R:1:C:1:in` (label "Product Group Name") |
| Insert Start Date | `tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input` |
| Update Code (read-only) | `tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in` |
| Update Name (editable) | `tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in` |
| Own credential pair | `PRODUCT_GROUP_EC_USER`/`PRODUCT_GROUP_EC_PASS` (`resources/credentials.py`) |

### Form labels (`@{PG_FORM_LABELS}`)
`Product Group Code`, `Product Group Name` - screen-prefixed labels, confirmed live 2026-08-23
via the New Object form's ECCell label dump - **NOT** the generic "Code"/"Name" Bank/Object List
use.

### Mandatory-yellow fields
Only **Start Date** is CSS-mandatory beyond Code/Name on Insert. Sort Order, Product Group Type
(dropdown), and Comments are optional and are deliberately left OUT of the IUD flow (fill-only-
needed-fields convention). Start Date is **Insert-only** - confirmed live it is NOT present on
`updateAttributes` (which shows only Product Group Code, Product Group Name, Sort Order, Product
Group Type, Comments).

### Delete
`objectdates` panel, row R0: End Date = Start Date (zero-length window) -> Save -> GO -> row
removed from `OV_PRODUCT_GROUP` (true delete, DB-verified).

### Grid filter
`Find Product Group Row By Filter` / `Clear Product Group Row Filter` - explicit wrappers around
the shared T2 `Find Object Row By Filter`/`Clear Object Row Filter` (`resources/
manage_object.resource`), wired into Update/Find/Verify-Found/Delete (matches Bank/State/
Account's own explicit filter usage, owner decision 2026-08-22).

## Quirks
- Fixed test code `AUTOTEST_PRODUCT_GROUP` (not per-run generated) - confirmed free live before
  being wired in (2026-08-23); every run must complete TC05 (delete) so the code stays free for
  the next run.
- Start Date is Insert-only; do not expect it on the Update tab.
- Screen-prefixed field labels ("Product Group Code"/"Product Group Name") - do not assume the
  generic "Code"/"Name" labels Bank itself uses.

## Automation (code lives in ec-automation - this file is the MD selector reference)
- **RF:** T3 `ec-automation/pageobjects/Configuration/Assets/Royalty_Objects/
  product_group_page.resource` + suite `ec-automation/tests/Configuration/Assets/
  Royalty_Objects/product_group_iud.robot` (T2 `manage_object` + T1 `common` + `DbVerify.py`, no
  shared-file edits). Validated live 5/5 (2026-08-23 original PR #445 run; 5/5 re-confirmed
  2026-08-28 backfill re-run).
- **Legacy Playwright:** `ec-automation/screens/Configuration/Assets/Royalty_Objects/
  Product_Group/playwright/ec_iud_product_group.py` - predates the Universal Screen Engine; kept
  as a reference walkthrough, not rebuilt (permanently waived per
  `docs/IUD-DELIVERABLE-CHECKLIST.md` Section H).
