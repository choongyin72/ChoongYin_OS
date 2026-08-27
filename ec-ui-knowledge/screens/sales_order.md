# Screen: Sales Order

- **Type:** OV (plain manage-object, no navigator) - Bank-pattern conversion, converted from the
  older hardcoded-field-id pattern to the label-driven, properties-file-driven, T2-consolidated
  shape via PR #444 (2026-08-23, Batch 5), mirroring Cost Object Mapping.
- **Treeview:** Configuration > Assets > Financial Objects > Sales Order.
- **DB view:** `OV_PRODUCT_SALES_ORDER` (versioned) - generic `CODE` column, per
  `libraries/DbVerify.py`.
- **Nav-free, confirmed live:** `NAV_DD_COUNT=0` - only the universal Date+GO as-at-date bar is
  present, no mandatory navigator dropdown. A naming-based scope-mismatch concern ("Sales Order"
  suggesting a possible document-header-plus-lines shape, like an invoice with line items) was
  raised in `tmp/batch5_shared_findings.md` and resolved live: this is a genuine Code/Name
  manage-object OV, same outcome as Cost Object Mapping (Batch 4), not a scope mismatch.
- **Last verified:** 2026-08-28 - EC 14.2.4 - local sandbox - RF dryrun 5/5 PASS + live headless
  5/5 PASS (TC01-TC05), fresh-connection DB self-clean 0 residual, `check_bundle_hygiene.py` PASS
  (backfill re-run of PR #444's Bank-pattern conversion, merged 2026-08-23).

## Selectors
| Purpose | Selector |
|---|---|
| Grid | `manage_object_nav_nav:form:T_data` (shared T2 constant `${OV_MANAGE_OBJECT_TABLE}`) |
| Delete (End Date field) | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (hardcoded, not
  label-driven - the row packs TWO fields, Start Date C:1 / End Date C:3, End Date label at C:2 -
  same documented shape as Bank's/Cost Object Mapping's own DEL_ENDDATE) |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
Order: **Product Sales Order Code*** - **Name*** - Start Date* (date) - End Date - Description -
Comments - Restrict Use (checkbox) - **Company*** (dropdown) - **Field*** (dropdown). Code label
is SCREEN-PREFIXED ("Product Sales Order Code"), NOT the generic "Code" Bank/Cost Centre use, same
pattern as Product Description. TWO mandatory reference dropdowns beyond Code/Name/Start Date -
Company, Field - confirmed via `MandatoryCellStyle` on the wrapping `<span>`; NEITHER is a cascade
(both populate immediately, no "Dependent field" banner). End Date/Description/Comments/Restrict
Use are all optional and omitted (IUD fills only needed fields). (`*` mandatory, confirmed via the
pristine New-Object row's yellow-background cue)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Product Sales Order Code` (ro, guard) - **`Name`** (only field edited) - Description - Comments -
Restrict Use - Company - Field. Start/End Date live only in `objectdates`, not
`updateAttributes` (same convention as Bank/Cost Object Mapping). Delete: **`End Date`** = Start
Date (zero-length window) -> true delete, row leaves `OV_PRODUCT_SALES_ORDER`.

### Grid columns (confirmed live)
Product Sales Order Code / Name / Start Date / End Date (20+ pre-existing rows, e.g. `BU_0001`).

## Test data values (this environment)
Company = `Acme Chemicals` (a clean literal option without leading/internal double-spaces, e.g.
avoiding "  Company  BP"; same clean option already proven on Cost Object Mapping). Field =
`Apollo` (a clean option, avoiding sibling options with leading spaces e.g. "  Esso Kizomba").
Real literal option text used for insert, NOT `__FIRST__` (Batch 2 VAT Code round-trip gotcha:
`__FIRST__` never resolves to literal text for the post-insert form-compare check). Fixed test
code `AUTOTEST_SO`, Start Date `2003-01-01` (reference-dropdown date-scope convention).

## Automation (code in ec-automation)
- **RF (current, maintained automation):** T3
  `pageobjects/Configuration/Assets/Financial_Objects/sales_order_page.resource` + suite
  `tests/Configuration/Assets/Financial_Objects/sales_order_iud.robot` (5 TC: Clean State /
  Insert / Update / Find / Delete, per-TC login/logout, fixed test code `AUTOTEST_SO`). Rebuilt to
  the Bank pattern via PR #444, 2026-08-23.
- **Playwright:** a historical reference driver exists,
  `screens/Configuration/Assets/Financial_Objects/Sales_Order/playwright/ec_iud_sales_order.py`
  (thin config over the shared Basic_Objects engine), from the screen's original 2026-06-11 IUD
  build - predates the Bank-pattern conversion and the Playwright-waiver rule. Kept as a
  historical reference only; NOT rebuilt or maintained going forward (owner decision 2026-08-27,
  the Universal Screen Engine replaces this role for new work).
- **Test data:** `testdata/sales_order_{insert,update,form_verify,grid_verify}.properties`.
- **Credentials:** dedicated pair `SALES_ORDER_EC_USER`/`SALES_ORDER_EC_PASS` in
  `resources/credentials.py`.
- **Explicit grid-filter wiring:** `Find/Clear Sales Order Row By Filter`, delegating to the
  shared T2 `Find/Clear Object Row By Filter` keywords - confirmed fired 5x in a fresh live
  output.xml (both at PR #444's own merge and re-confirmed by the 2026-08-28 backfill).

## Quirks
- Naming can mislead: "Sales Order" reads like it could be a document-header-plus-lines shape
  (invoice/order with line items), but it is a genuine flat Code/Name manage-object OV - confirmed
  live via `NAV_DD_COUNT=0` and the absence of any child-grid/lines section. Don't assume a
  document shape from the name alone.
- Company and Field dropdowns are mandatory but NOT cascading - either can be filled in any order,
  unlike screens where one dropdown's options depend on another (e.g. Cost Object Mapping's Cost
  Object dd).
- DB self-clean checks against `OV_PRODUCT_SALES_ORDER` must use the generic `CODE` column.
- Two historical automation layers coexist in the `screens/.../Sales_Order/` bundle: an OLDER
  Playwright driver (2026-06-11, pre-dates the conversion) and the CURRENT RF suite (PR #444,
  2026-08-23). Do not treat the Playwright driver as up-to-date with the current screen shape -
  it was not re-verified against the Bank-pattern conversion's confirmed field/dropdown facts.
