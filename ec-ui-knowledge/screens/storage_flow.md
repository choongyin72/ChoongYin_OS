# Screen: Storage Flow

- **Type:** OV (EC Object Configuration, date-effective) - Bank-family (`manage_object_nav`); plain (optional dropdowns only, none mandatory)
- **BF_CODE:** CO.2091 - **Treeview:** Configuration > Assets > Tank_and_Storage_Objects > Storage Flow _(DB treeview JSON)_
- **DB view:** `OV_STORAGE_FLOW` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-07-26 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF 4/4 + Playwright 7/7, DB-verified, self-clean)

## Selectors `[fresh scan 2026-07-26]`
| Purpose | Selector |
|---|---|
| Open | search `Storage Flow` -> `label.tv-link` "Storage Flow" |
| Grid | `manage_object_nav_nav:form:T_data` (needs GO to load) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Storage Flow Code*** - **Storage Flow Name*** - **Start Date*** (date) - End Date - optional dropdowns. (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Storage Flow Code` (ro) - **`Storage Flow Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_STORAGE_FLOW`.

## Automation (code in ec-automation)
- **Playwright:** `py/storage_flow_iud.py` -> 7/7 (update Name).
- **RF:** T3 `pageobjects/Configuration/Assets/Tank_and_Storage_Objects/storage_flow_page.resource` (**label-driven, NO hardcoded ids**) + suite `tests/.../storage_flow_iud.robot` -> live 4/4.
- **Gate:** `verify_screen.py` -> OVERALL PASS.

## Quirks
- Plain OV; no mandatory dropdowns. Generic engine handles appear/absent/pagination.
