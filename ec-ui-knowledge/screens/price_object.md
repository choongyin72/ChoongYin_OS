# Screen: Price Object

- **Type:** OV-GM (manage-object, groupmodel), date-effective (`CLASS_TYPE=OBJECT`/`TIME_SCOPE_CODE=VERSIONED`).
- **BF_CODE:** CO.3016 — **Treeview:** Configuration > Assets > Sales Objects > Price Object
- **DB base/version:** `PRODUCT_PRICE` / `PRODUCT_PRICE_VERSION` (label ambiguous with `INVENTORY_PRICE_OBJECT`
  — both share the same base tables; the correct class for this BF is `PRICE_OBJECT` -> `OV_PRICE_OBJECT`)
- **DB view:** `OV_PRICE_OBJECT` (key `CODE`)
- **Pattern:** Converted to the **Area full pattern** in PR #536 (2026-08-26) — 5-TC RF STRUCTURE
  (Clean State/Insert/Update/Find/Delete) while REMAINING OV-GM; this file only records what is
  Price-Object-specific (transcribed from `price_object_page.resource`'s own Variables section).
- **Last verified:** 2026-08-26 (PR #536, live 5/5) — EC 14.2.4 — local sandbox.

**Not the same screen as** "Product Price Object" (CD.0011, PR #502, `ec-ui-knowledge/screens/
product_price_object.md` if present) — that is a distinct custom-URL controller with NO navigator at all.

## Selectors `[from price_object_page.resource Variables section, transcribed 2026-08-27]`

| Purpose | Selector |
|---|---|
| Grid (rows) | `manageObject:form:T_data` |
| Navigator dropdown (Business Unit, MANDATORY) | `nav:form:G:0:R:1:C:1:dd` — value = `EC LNG Norway` (this screen's own sandbox default) |
| Navigator fill mechanism | Shared T2 `Apply Navigator From Properties` (`resources/manage_object.resource`), driven by `testdata/price_object_navigator.properties` |
| Grid-filter | `Find/Clear Price Object Row By Filter` → shared T2 `Find/Clear Object Row By Filter` on the grid's Code column |
| Insert/Update/Verify | Delegates to shared T2 `Insert/Update/Verify Object *` keywords, all called with `code_label=Price Object Code` |
| Delete End Date field | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (hardcoded, not label-driven — End Date label sits at `C:2`, Start Date at `C:1`, same row-packing rationale as Bank's/Area's own del-enddate id) |

## Mandatory / yellow fields
- **Navigator (before the grid loads any rows):** Business Unit dropdown + GO — genuine OV-GM requirement,
  not removed by the 2026-08-26 structural conversion. 2 sibling dropdown columns on the SAME nav row are
  unrelated optional filters, NOT cascade children — do not treat this as a multi-level cascade.
- **Insert form:** Price Object Code, Price Object Name, Start Date, Product Name, Price Concept, UOM,
  Price Rounding Rule (mandatory); Business Unit must equal the navigator's captured value or the inserted
  row is invisible under the filtered grid scope.
- **Update form:** Price Object Name only (Price Object Code is read-only in `updateAttributes`).
- Field labels are **screen-prefixed**: "Price Object Code" / "Price Object Name" (like Area's "Area
  Code"), NOT the generic "Code"/"Name" that Bank/Object List use.

## Quirks
- **Business Unit value confirmed LIVE 2026-08-26 = "EC LNG Norway"** — NOT "Royalty Canada", the value
  used by sibling screens Property/Price Index/Division Order/Royalty Contract (a different environment
  default). Do not reuse a sibling screen's documented navigator value for this screen without verifying —
  each screen's default resolves independently.
- **Original park reason ("pager-walk click timeout") was wrong, twice.** The real defect (found for
  issue #321, 2026-08-02): inserting with Business Unit left unset leaves `BUSINESS_UNIT_CODE` NULL, so the
  row is genuinely invisible under any page of a BU-scoped grid — the same class of bug as Message Group
  and Planned Well, not a pagination mechanism issue. Fixed originally by binding the navigator's captured
  Business Unit into the insert form's own Business Unit dropdown (`gen_ovgm.py`'s `parent_dd` mechanism);
  the Area-pattern conversion carries this forward via the shared `Apply Navigator From Properties`
  keyword's own binding.
- **False-cascade navigator row**: 2 OPTIONAL filter dropdown columns share the nav row with the one
  mandatory Business Unit dropdown (same class of shape as Service/CO.2103) — the RF T3 uses a direct
  single-dropdown fill via the shared navigator-properties keyword rather than the shared multi-level
  cascade keyword, to avoid timing out on the empty optional columns.
- **Ambiguous class label**: "Price Object" matches both `PRICE_OBJECT` and `INVENTORY_PRICE_OBJECT` in
  `class_property_cnfg` (both share base tables `PRODUCT_PRICE`/`PRODUCT_PRICE_VERSION`). The correct view
  for THIS BF code is `OV_PRICE_OBJECT` (confirmed via the original park doc's own earlier investigation).
- **Fixed test code `AUTOTEST_PRICE_OBJECT`** (not a generated/unique code, since the PR #536 conversion —
  the original 2026-08-03 build used a generated `AUTOTEST_PO_<timestamp>` code) — every run must complete
  TC05 so the code is free for the next run.

## Automation (code lives in ec-automation — this file is the MD selector reference)
- **RF (the maintained suite):** T3
  `ec-automation/pageobjects/Configuration/Assets/Sales_Objects/price_object_page.resource` (T2
  `resources/manage_object.resource` + `libraries/PropertiesReader.py`) + suite
  `ec-automation/tests/Configuration/Assets/Sales_Objects/price_object_iud.robot` (5 TCs: Clean
  State/Insert/Update/Find/Delete, per-TC Login/Logout). Run:
  `EC_HEADLESS=true robot tests/Configuration/Assets/Sales_Objects/price_object_iud.robot` → 5/5 PASS,
  self-clean 0 residual in `OV_PRICE_OBJECT`.
- **Playwright (pre-existing reference, waived from further build per Section H of
  `docs/IUD-DELIVERABLE-CHECKLIST.md` — Universal Screen Engine replaces this role going forward):**
  `ec-automation/py/price_object_iud.py` (generated by `gen_ovgm.py`, `parent_dd="Business Unit"`,
  `nav_levels=1`), kept unchanged since the 2026-08-03 build.
- Full bundle (SOW/README/JOURNAL/evidence/CHECKLIST):
  `ec-automation/screens/Configuration/Assets/Sales_Objects/Price_Object/`.
