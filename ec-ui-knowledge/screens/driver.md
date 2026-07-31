# Screen: Driver

- **Type:** Plain OV (EC Object Configuration, date-effective) - Bank family; date-only navigator + GO.
- **BF_CODE:** CO.0266 - **Treeview:** Configuration > Assets > Transport_Objects > Driver
- **DB view:** `OV_DRIVER` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-07-31 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF 4/4 pass + Playwright 8/8, DB-verified, self-clean)

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Driver` -> `label.tv-link` "Driver" |
| Navigator | date field `nav:form:G:0:R:1:C:0:da_input` -> GO `#button:form:B` (no cascade) |
| Grid | `driver_object:form:T_data` (lists after GO) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Driver Code*** - **Driver Name*** - **Start Date*** (date) + dropdowns Gender of driver. (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Driver Code` (ro) - **`Driver Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_DRIVER`.

## Automation (code in ec-automation)
- **Playwright:** `py/driver_iud.py` (shared engine `ec_object_iud.py` + `click_go`).
- **RF:** T3 `pageobjects/Configuration/Assets/Transport_Objects/driver_page.resource` (**label-driven**) + suite `tests/Configuration/Assets/Transport_Objects/driver_iud.robot`.
- **Gate:** `verify_screen.py` -> OVERALL PASS.

## Quirks
- Plain OV (Bank family): the navigator is a single DATE field + GO - no cascade, and no Op
  Production Unit to satisfy.
- An UNSAVED CHANGES dialog (YES/NO) can block GO right after the End=Start close - answer YES
  (that commits the intended delete).

_Family text corrected 2026-07-31 (prose only; code and gate results unchanged): this bundle shipped with OV-GM wording that does not describe this screen - the packager templates were OV-GM-only until then._
