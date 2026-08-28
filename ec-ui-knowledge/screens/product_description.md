# Screen: Product Description

- **Type:** OV (Manage-Object, plain — no navigator section), date-effective.
- **Treeview:** Configuration > Assets > Financial Objects > Product Description
- **DB view:** `OV_PRODUCT_NODE_ITEM` (key `CODE`)
- **Pattern:** Converted to the **Bank full pattern** in PR #441 (2026-08-23, Batch 4 of the
  Bank-pattern conversion project) — 5-TC RF structure (Clean State/Insert/Update/Find/Delete),
  properties-file-driven, T2-consolidated.
- **Last verified:** 2026-08-23 (PR #441, live 5/5); re-confirmed 2026-08-28 (backfill session,
  live 5/5) — EC 14.2.4 — local sandbox.

**Not the same screen as** "Product" (CO.0007, class PRODUCT,
`ec-ui-knowledge/screens/product.md` if present) or "Product Group" (RC.0053) — both distinct
sibling classes. Do not confuse when searching by "product".

## Selectors `[from product_description_page.resource Variables section, transcribed 2026-08-28]`

| Purpose | Selector |
|---|---|
| Grid (rows) | `manage_object_nav_nav:form:T_data` (shared T2 constant `OV_MANAGE_OBJECT_TABLE`, no screen-local duplicate) |
| Navigator | None — universal Date + GO bar only (`NAV_DD_COUNT=0`), no mandatory dropdown/cascade |
| Grid-filter | `Find/Clear Product Description Row By Filter` → shared T2 `Find/Clear Object Row By Filter` on the grid's Code column |
| Insert/Update/Verify | Delegates to shared T2 `Insert/Update Object From Properties`, `Verify Object Insert Exists/Form Record/Found/Does Not Exist/Removed`, `Find Object Record`, all called with `code_label=Product Node Item Code` |
| Delete End Date field | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (hardcoded, not label-driven — same row-packing shape as Bank's/Area's own del-enddate id: Start Date at `C:1`, End Date label at `C:2`, End Date input at `C:3`) |

## Mandatory / yellow fields
- **Code label is SCREEN-PREFIXED**: "Product Node Item Code" — NOT the generic "Code" that
  Bank/Cost Centre use. Passed as `code_label` to every T2 keyword that accepts it.
- **Insert form (`objectForm`) and Update form (`updateAttributes`)** both carry: Product Node
  Item Code, Name, Description (optional), plus THREE mandatory reference dropdowns — **Product**,
  **Node**, **Financial Code** (`MandatoryCellStyle` confirmed live on all three).
- Start Date/End Date live only in the `objectdates` panel, not in `updateAttributes`.
- Grid columns: Product Node Item Code / Name / Start Date / End Date.

## Quirks
- **Literal first-option dropdown values used, not `__FIRST__`**: Product=`AS3_CrudeOil`,
  Node=`Apollo FPSO`, Financial Code=`Frame Agreement` — per the Batch 2 VAT Code round-trip-
  verify gotcha (TC02's verify compares the live screen back against the same properties file
  used to insert, so a literal, stable value is required rather than a re-resolved "first
  available" that could differ between insert time and verify time).
- **Fixed test code `AUTOTEST_PD`**, Start Date `2003-01-01` (reference-dropdown date-scope
  convention — chosen so the fixed reference-dropdown values above are valid at that date). Every
  run must complete TC05 (delete) so the code is free for the next run — EC never lets a DELETED
  code be reused, but this fixed code only stays reusable if each run actually cleans up after
  itself.
- **No mandatory navigator cascade** — confirmed live: only the universal Date+GO as-at-date bar,
  `NAV_DD_COUNT=0`. Do not add a navigator-fill step when converting/maintaining this screen.
- **Disambiguation**: three similarly-named screens exist in this product family — "Product"
  (CO.0007, class PRODUCT), "Product Description" (this screen, class item held in
  `OV_PRODUCT_NODE_ITEM`), and "Product Group" (RC.0053). Confirm the real file path/registry row
  before touching any of the three.

## Automation (code lives in ec-automation — this file is the MD selector reference)
- **RF (the maintained suite):** T3
  `ec-automation/pageobjects/Configuration/Assets/Financial_Objects/product_description_page.resource`
  (T2 `resources/manage_object.resource` + `libraries/PropertiesReader.py`) + suite
  `ec-automation/tests/Configuration/Assets/Financial_Objects/product_description_iud.robot` (5
  TCs: Clean State/Insert/Update/Find/Delete, per-TC Login/Logout). Run:
  `EC_HEADLESS=true robot tests/Configuration/Assets/Financial_Objects/product_description_iud.robot`
  → 5/5 PASS, self-clean 0 residual in `OV_PRODUCT_NODE_ITEM`.
- **Playwright (pre-existing reference, waived from further build per Section H of
  `docs/IUD-DELIVERABLE-CHECKLIST.md` — Universal Screen Engine replaces this role going
  forward):** `ec-automation/playwright/ec_iud_product_description.py`, kept unchanged since the
  2026-06-11 build.
- Full bundle (SOW/README/JOURNAL/evidence/CHECKLIST):
  `ec-automation/screens/Configuration/Assets/Financial_Objects/Product_Description/`.
