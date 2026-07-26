# Screen: Inventory Area

- **Type:** OV (EC Object Configuration, date-effective) - Bank-family (`manage_object_nav`); plain (optional dropdowns only, none mandatory)
- **BF_CODE:** CD.0115 - **Treeview:** Configuration > Assets > Inventory_Objects > Inventory Area _(DB treeview JSON)_
- **DB view:** `OV_INVENTORY_AREA` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-07-26 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF 4/4 + Playwright 7/7, DB-verified, self-clean)

## Selectors `[fresh scan 2026-07-26]`
| Purpose | Selector |
|---|---|
| Open | search `Inventory Area` -> `label.tv-link` "Inventory Area" |
| Grid | `manage_object_nav_nav:form:T_data` (needs GO to load) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Inventory Area Code*** - **Inventory Area Name*** - **Start Date*** (date) - End Date - optional dropdowns. (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Inventory Area Code` (ro) - **`Inventory Area Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_INVENTORY_AREA`.

## Automation (code in ec-automation)
- **Playwright:** `py/inventory_area_iud.py` -> 7/7 (update Name).
- **RF:** T3 `pageobjects/Configuration/Assets/Inventory_Objects/inventory_area_page.resource` (**label-driven, NO hardcoded ids**) + suite `tests/.../inventory_area_iud.robot` -> live 4/4.
- **Gate:** `verify_screen.py` -> OVERALL PASS.

## Quirks
- Plain OV; no mandatory dropdowns. Generic engine handles appear/absent/pagination.
