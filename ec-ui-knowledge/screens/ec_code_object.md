# Screen: EC Code Object

- **Type:** OV (EC Object Configuration, date-effective) - Bank-family (`manage_object_nav`); plain (optional dropdowns only, none mandatory)
- **BF_CODE:** CD.0135 - **Treeview:** Configuration > Codes > EC Code Object _(DB treeview JSON)_
- **DB view:** `OV_EC_CODE_OBJECT` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-07-26 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF 4/4 + Playwright 7/7, DB-verified, self-clean)

## Selectors `[fresh scan 2026-07-26]`
| Purpose | Selector |
|---|---|
| Open | search `EC Code Object` -> `label.tv-link` "EC Code Object" |
| Grid | `manage_object_nav_nav:form:T_data` (needs GO to load) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Object Code*** - **Name*** - **Start Date*** (date) - End Date - optional dropdowns. (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Object Code` (ro) - **`Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_EC_CODE_OBJECT`.

## Automation (code in ec-automation)
- **Playwright:** `py/ec_code_object_iud.py` -> 7/7 (update Name).
- **RF:** T3 `pageobjects/Configuration/Codes/ec_code_object_page.resource` (**label-driven, NO hardcoded ids**) + suite `tests/.../ec_code_object_iud.robot` -> live 4/4.
- **Gate:** `verify_screen.py` -> OVERALL PASS.

## Quirks
- Plain OV; no mandatory dropdowns. Generic engine handles appear/absent/pagination.
