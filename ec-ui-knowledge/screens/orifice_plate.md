# Screen: Orifice Plate

- **Type:** OV (EC Object Configuration, date-effective) - Bank-family (`manage_object_nav`); plain (optional dropdowns only, none mandatory)
- **BF_CODE:** CO.0089 - **Treeview:** Configuration > Assets > Stream_Objects > Orifice Plate _(DB treeview JSON)_
- **DB view:** `OV_ORIFICE_PLATE` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-07-26 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF 4/4 + Playwright 7/7, DB-verified, self-clean)

## Selectors `[fresh scan 2026-07-26]`
| Purpose | Selector |
|---|---|
| Open | search `Orifice Plate` -> `label.tv-link` "Orifice Plate" |
| Grid | `manage_object_nav_nav:form:T_data` (needs GO to load) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Orifice Code*** - **Orifice Name*** - **Start Date*** (date) - End Date - optional dropdowns. (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Orifice Code` (ro) - **`Orifice Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_ORIFICE_PLATE`.

## Automation (code in ec-automation)
- **Playwright:** `py/orifice_plate_iud.py` -> 7/7 (update Name).
- **RF:** T3 `pageobjects/Configuration/Assets/Stream_Objects/orifice_plate_page.resource` (**label-driven, NO hardcoded ids**) + suite `tests/.../orifice_plate_iud.robot` -> live 4/4.
- **Gate:** `verify_screen.py` -> OVERALL PASS.

## Quirks
- Plain OV; no mandatory dropdowns. Generic engine handles appear/absent/pagination.
