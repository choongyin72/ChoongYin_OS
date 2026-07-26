# Screen: Transactional Inventory Properties

- **Type:** OV (EC Object Configuration, date-effective) - Bank-family (`manage_object_nav`); plain (optional dropdowns only, none mandatory)
- **BF_CODE:** IN.0023 - **Treeview:** EC_Revenue > Inventory > Transactional_Inventory > Configuration > Transactional Inventory Properties _(DB treeview JSON)_
- **DB view:** `OV_TRANS_INVENTORY` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-07-26 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF 4/4 + Playwright 7/7, DB-verified, self-clean)

## Selectors `[fresh scan 2026-07-26]`
| Purpose | Selector |
|---|---|
| Open | search `Transactional Inventory Properties` -> `label.tv-link` "Transactional Inventory Properties" |
| Grid | `manage_object_nav_nav:form:T_data` (needs GO to load) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Code*** - **Name*** - **Start Date*** (date) - End Date - optional dropdowns. (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Code` (ro) - **`Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_TRANS_INVENTORY`.

## Automation (code in ec-automation)
- **Playwright:** `py/transactional_inventory_properties_iud.py` -> 7/7 (update Name).
- **RF:** T3 `pageobjects/EC_Revenue/Inventory/Transactional_Inventory/Configuration/transactional_inventory_properties_page.resource` (**label-driven, NO hardcoded ids**) + suite `tests/.../transactional_inventory_properties_iud.robot` -> live 4/4.
- **Gate:** `verify_screen.py` -> OVERALL PASS.

## Quirks
- Plain OV; no mandatory dropdowns. Generic engine handles appear/absent/pagination.
