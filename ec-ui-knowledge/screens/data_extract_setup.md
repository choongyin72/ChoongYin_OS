# Screen: Data Extract Setup

- **Type:** OV (EC Object Configuration, date-effective) - Bank-family (`manage_object_nav`); plain (optional dropdowns only, none mandatory)
- **BF_CODE:** SP.0043 - **Treeview:** Configuration > Assets > Data_Mapping_Objects > Data Extract Setup _(DB treeview JSON)_
- **DB view:** `OV_SUMMARY_SETUP` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-07-26 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF 4/4 + Playwright 7/7, DB-verified, self-clean)

## Selectors `[fresh scan 2026-07-26]`
| Purpose | Selector |
|---|---|
| Open | search `Data Extract Setup` -> `label.tv-link` "Data Extract Setup" |
| Grid | `manage_object_nav_nav:form:T_data` (needs GO to load) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Data Extract Setup Code*** - **Data Extract Setup Name*** - **Start Date*** (date) - End Date - optional dropdowns. (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Data Extract Setup Code` (ro) - **`Data Extract Setup Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_SUMMARY_SETUP`.

## Automation (code in ec-automation)
- **Playwright:** `py/data_extract_setup_iud.py` -> 7/7 (update Name).
- **RF:** T3 `pageobjects/Configuration/Assets/Data_Mapping_Objects/data_extract_setup_page.resource` (**label-driven, NO hardcoded ids**) + suite `tests/.../data_extract_setup_iud.robot` -> live 4/4.
- **Gate:** `verify_screen.py` -> OVERALL PASS.

## Quirks
- Plain OV; no mandatory dropdowns. Generic engine handles appear/absent/pagination.
