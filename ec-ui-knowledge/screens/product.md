# Screen: Product

- **Type:** plain OV (Manage-Object, Bank family), date-effective — no navigator dropdown/cascade.
- **BF code:** CO.0007   **Class:** PRODUCT (`PRODUCT_MAINTAIN`)
- **Treeview path:** Configuration > Assets > Hydrocarbon Objects > Product
- **Open via:** menu search
- **DB view (ground truth):** `OV_PRODUCT` (versioned; base table `PRODUCT`, key `OBJECT_CODE` /
  view column `CODE`)
- **NOT the same class as its Product-named siblings** — disambiguate carefully when grepping:
  - "Product Description" (CD.0012) — `product_description_page.resource` / `product_description_iud.robot`
  - "Product Group" (RC.0053) — `product_group_page.resource` / `product_group_iud.robot`
  - "Product Price Object" — `product_price_object_page.resource`
  - "Product Split Key" — `product_split_key_page.resource`
  - This screen's own files are `product_page.resource` / `product_iud.robot` — confirmed distinct
    via `resolve_ec_screen.py` (CLASS_TYPE=OBJECT, TIME_SCOPE_CODE=VERSIONED, base table `PRODUCT`,
    view `OV_PRODUCT`) before PR #485 built it.
- **Last verified:** 2026-08-28 · EC 14.2.4 · local sandbox · RF dryrun 5/5 PASS + live headless
  5/5 PASS (TC01-TC05, first attempt), fresh-connection DB self-clean 0 residual
  (`PRODUCT`/`OV_PRODUCT`), `check_bundle_hygiene.py` PASS (backfill re-run of PR #485's brand-new
  Bank-pattern build, merged 2026-08-24).

## Selectors

| Purpose | Selector |
|---|---|
| Grid | `manage_object_nav_nav:form:T_data` (reused via T2's `${OV_MANAGE_OBJECT_TABLE}` constant, not re-hardcoded) |
| Navigator Date (optional) | single date field in the nav row (default; left untouched — not mandatory) |
| GO | `button:form:B` |
| Delete (End Date field) | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (hardcoded, not label-driven — same `C:3` framework-invariant convention as Bank) |

### New Object form (`objectForm`) — labels (T3 resolves BY LABEL, `code_label="Product Code"`)
**Product Code*** — **Product Name*** — **Start Date*** (date) — Description (plain text) —
Sort Order (plain text) — Hydrocarbon Component / Product Group / Product Type / ERP Code
(dropdowns, all OPTIONAL, left unset — no live-verified valid option values for AUTOTEST data).
Labels are SCREEN-PREFIXED ("Product Code"/"Product Name"), like Area's "Area Code"/"Area Name" and
Tank's "Tank Code"/"Tank Name" — NOT the generic "Code"/"Name" Bank/Object List use. (`*` = mandatory,
confirmed live via `scan_ec_screen.py` 2026-08-24)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Product Code` (read-only, guard) — **`Product Name`**, **`Description`** (the only fields edited by
the suite's TC03). **Product Type / ERP Code exist on Insert's `objectForm` but are NOT present on
`updateAttributes`** (confirmed live, 2026-08-24) — do not assume Insert's field set carries over to
Update. Start Date/End Date live only in `objectdates`, not `updateAttributes`, same pattern as
Bank/Area/Tank. Delete: **`End Date`** = Start Date (zero-length window) -> true delete, row leaves
`OV_PRODUCT`.

### Grid columns
Product Code / Product Name / Start Date / End Date (standard manage-object grid shape).

## Test data (this environment)
Fixed code `AUTOTEST_PRODUCT` (not a per-run generated code) — confirmed absent from
`PRODUCT.OBJECT_CODE` before use; every run must complete TC05 (Delete) to keep the code reusable.
Start Date = End Date = `2000-01-01`. See `testdata/product_{insert,update,form_verify,grid_verify}.properties`.

## Quirks
- Screen-prefixed Code/Name labels mean every shared T2 call must pass
  `code_label=${PRODUCT_CODE_LABEL}` ("Product Code") — a bare default `code_label="Code"` silently
  fails to find the field.
- Update form drops Product Type/ERP Code entirely vs Insert's form — do not carry an Insert field
  list forward to an Update call without re-checking `updateAttributes` live.
- No navigator mandatory dropdown/cascade — grid stays empty until GO is clicked, even with the
  date field left at its default.

## Automation (code lives in ec-automation — this file is the MD selector reference)
- **RF only** — no Playwright bundle exists or is required (owner decision 2026-08-27,
  `docs/IUD-DELIVERABLE-CHECKLIST.md` Section H permanently waives items 4/5 for Bank-/Area-pattern
  builds; the Universal Screen Engine is the replacement).
- T3 `pageobjects/Configuration/Assets/Hydrocarbon_Objects/product_page.resource` + suite
  `tests/Configuration/Assets/Hydrocarbon_Objects/product_iud.robot` (T2 `manage_object.resource` +
  T1 `common.resource`). Validated live 5/5 (2026-08-24, PR #485; re-confirmed 2026-08-28 backfill
  re-run).
- Full bundle: `screens/Configuration/Assets/Hydrocarbon_Objects/Product/` (SOW/README/JOURNAL/
  evidence/CHECKLIST, added 2026-08-28 backfill — Batch 12).
