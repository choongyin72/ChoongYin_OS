# Screen: Reservoir Formation

- **Type:** OV (EC Object Configuration, date-effective) - Bank-family (`manage_object_nav`); plain (optional dropdowns only, none mandatory)
- **BF_CODE:** CO.0135 - **Treeview:** Configuration > Assets > Well_and_Reservoir_Objects > Reservoir Formation _(DB treeview JSON)_
- **DB view:** `OV_RESV_FORMATION` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-07-26 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF 4/4 + Playwright 7/7, DB-verified, self-clean)

## Selectors `[fresh scan 2026-07-26]`
| Purpose | Selector |
|---|---|
| Open | search `Reservoir Formation` -> `label.tv-link` "Reservoir Formation" |
| Grid | `manage_object_nav_nav:form:T_data` (needs GO to load) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Reservoir Formation Code*** - **Reservoir Formation Name*** - **Start Date*** (date) - End Date - optional dropdowns. (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Reservoir Formation Code` (ro) - **`Reservoir Formation Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_RESV_FORMATION`.

## Automation (code in ec-automation)
- **Playwright:** `py/reservoir_formation_iud.py` -> 7/7 (update Name).
- **RF:** T3 `pageobjects/Configuration/Assets/Well_and_Reservoir_Objects/reservoir_formation_page.resource` (**label-driven, NO hardcoded ids**) + suite `tests/.../reservoir_formation_iud.robot` -> live 4/4.
- **Gate:** `verify_screen.py` -> OVERALL PASS.

## Quirks
- Plain OV; no mandatory dropdowns. Generic engine handles appear/absent/pagination.
