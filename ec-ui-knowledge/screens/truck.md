# Screen: Truck

- **Type:** PLAIN OV (Bank family, date-effective) - EMPTY navigator (GO only), CUSTOM grid id `truck_object:form:T_data`.
- **BF_CODE:** CO.0264 - **Treeview:** Configuration > Assets > Transport_Objects > Truck
- **DB view:** `OV_TRUCK` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-07-31 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF 4/4 pass + Playwright 8/8, DB-verified, self-clean)

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Truck` -> `label.tv-link` "Truck" |
| Navigator | NONE - no nav fields; click GO `#button:form:B` to populate the grid |
| Grid | `truck_object:form:T_data` (empty until GO) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Truck Code*** - **Truck Name*** - **Start Date*** (date) + dropdowns UOM, Transport Company. (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Truck Code` (ro) - **`Truck Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_TRUCK`.

## Automation (code in ec-automation)
- **Playwright:** `py/truck_iud.py` (shared engine `ec_object_iud.py` + `click_go`).
- **RF:** T3 `pageobjects/Configuration/Assets/Transport_Objects/truck_page.resource` (**label-driven**) + suite `tests/Configuration/Assets/Transport_Objects/truck_iud.robot`.
- **Gate:** `verify_screen.py` -> OVERALL PASS.

## Quirks
- 9 MANDATORY fields (several render WHITE, not yellow): Code/Name/Start Date + Licence Plate No + Tractor Gross Vehicle Qty + Vehicle Gross Combined Qty + Unladen Truck Qty + UOM + Transport Company. Derive such sets from EC's save-time 'Required fields are empty' message, not the yellow-cell heuristic.
- An UNSAVED CHANGES dialog (YES/NO) can block GO right after the End=Start close - answer YES
  (that commits the intended delete).
