# Screen: Conversion Group

- **Type:** OV (EC Object Configuration, date-effective) - Bank-family (`manage_object_nav`); plain (optional dropdowns only, none mandatory)
- **BF_CODE:** CO.1049 - **Treeview:** Configuration > System > Units > Conversion Group _(DB treeview JSON)_
- **DB view:** `OV_CONVERSION_GROUP` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-07-26 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF 4/4 + Playwright 7/7, DB-verified, self-clean)

## Selectors `[fresh scan 2026-07-26]`
| Purpose | Selector |
|---|---|
| Open | search `Conversion Group` -> `label.tv-link` "Conversion Group" |
| Grid | `manage_object_nav_nav:form:T_data` (needs GO to load) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Conversion Group Code*** - **Conversion Group Name*** - **Start Date*** (date) - End Date - optional dropdowns. (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Conversion Group Code` (ro) - **`Conversion Group Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_CONVERSION_GROUP`.

## Automation (code in ec-automation)
- **Playwright:** `py/conversion_group_iud.py` -> 7/7 (update Name).
- **RF:** T3 `pageobjects/Configuration/System/Units/conversion_group_page.resource` (**label-driven, NO hardcoded ids**) + suite `tests/.../conversion_group_iud.robot` -> live 4/4.
- **Gate:** `verify_screen.py` -> OVERALL PASS.

## Quirks
- Plain OV; no mandatory dropdowns. Generic engine handles appear/absent/pagination.
