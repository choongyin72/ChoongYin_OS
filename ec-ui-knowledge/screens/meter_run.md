# Screen: Meter Run

- **Type:** OV (EC Object Configuration, date-effective) - Bank-family (`manage_object_nav`); plain (mandatory extras beyond Code/Name/Start Date: Type of Taps, Pipe Material, Location of Taps (dropdowns), Pipe Diameter [mm], Diameter Meas Temp [deg R], All Calibration Factor)
- **BF_CODE:** CO.0091 - **Treeview:** Configuration > Assets > Stream_Objects > Meter Run _(DB treeview JSON)_
- **DB view:** `OV_METER_RUN` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-07-26 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF 4/4 + Playwright 7/7, DB-verified, self-clean)

## Selectors `[fresh scan 2026-07-26]`
| Purpose | Selector |
|---|---|
| Open | search `Meter Run` -> `label.tv-link` "Meter Run" |
| Grid | `manage_object_nav_nav:form:T_data` (needs GO to load) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Meter Run Code*** - **Meter Run Name*** - **Start Date*** (date) - End Date - optional dropdowns. (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Meter Run Code` (ro) - **`Meter Run Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_METER_RUN`.

## Automation (code in ec-automation)
- **Playwright:** `py/meter_run_iud.py` -> 7/7 (update Name).
- **RF:** T3 `pageobjects/Configuration/Assets/Stream_Objects/meter_run_page.resource` (**label-driven, NO hardcoded ids**) + suite `tests/.../meter_run_iud.robot` -> live 4/4.
- **Gate:** `verify_screen.py` -> OVERALL PASS.

## Quirks
- Plain OV; mandatory extras beyond Code/Name/Start Date: Type of Taps, Pipe Material, Location of Taps (dropdowns), Pipe Diameter [mm], Diameter Meas Temp [deg R], All Calibration Factor. Generic engine handles appear/absent/pagination.
