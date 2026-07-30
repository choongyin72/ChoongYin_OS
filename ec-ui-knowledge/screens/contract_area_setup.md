# Screen: Contract Area Setup

- **Type:** CUSTOM-URL OV (EC Object Configuration, date-effective) - NO navigator, NO GO button.
- **BF_CODE:** CO.2038 - **Treeview:** Configuration > Assets > Contract_Objects > Contract Area Setup
- **DB view:** `OV_CONTRACT_AREA_SETUP` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-07-30 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF 4/4 pass + Playwright 7/7, DB-verified, self-clean)

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Contract Area Setup` -> `label.tv-link` "Contract Area Setup" |
| Navigator | NONE - custom-URL OV, grid loads directly on screen open |
| Grid | `nav:form:T_data` |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / reload | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / toolbar **Refresh** (no GO - engine `click_go` + T2 `Save And Refresh List` fall back automatically) |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Contract Area Setup Code*** - **Contract Area Setup Name*** - **Start Date*** (date) + **2 mandatory
ref dropdowns: Contract Area Name*, Contract Name*** (first-available). No Op Production Unit field. (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Contract Area Setup Code` (ro) - **`Contract Area Setup Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_CONTRACT_AREA_SETUP`.

## Automation (code in ec-automation)
- **Playwright:** `py/contract_area_setup_iud.py` (shared engine `ec_object_iud.py`; NO apply_ovgm_navigator -
  first custom-URL OV on the shared engine).
- **RF:** T3 `pageobjects/Configuration/Assets/Contract_Objects/contract_area_setup_page.resource` (**label-driven**) + suite `tests/Configuration/Assets/Contract_Objects/contract_area_setup_iud.robot`.
- **Gate:** `verify_screen.py` -> OVERALL PASS.

## Quirks
- **Start Date must be 2020-01-01 (not 2000-01-01):** the 2 mandatory ref dropdowns only offer objects
  effective at the form Start Date - DB-checked 28 contract areas + 98 contracts effective at 2020-01-01
  (vs sparse/none at 2000-01-01). Count the candidate parents BEFORE picking a Start Date.
- View starts empty on the sandbox (0 configured rows) - the AUTOTEST row is created + true-deleted per run.
