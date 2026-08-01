# Screen: External Location

- **Type:** OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel; navigator-GATED. NO mandatory nav scope - fields are optional filters.
- **BF_CODE:** CO.0227 - **Treeview:** Configuration > Assets > Facility_Objects > External Location
- **DB view:** `OV_EXTERNAL_LOCATION` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-08-01 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF 4/4 pass + Playwright 8/8, DB-verified, self-clean)

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `External Location` -> `label.tv-link` "External Location" |
| Navigator | GO only (navigator fields are optional filters, no mandatory scope) |
| Grid | `manageObject:form:T_data` (lists on GO with no filters set) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**External Location Code*** - **External Location Name*** - **Start Date*** (date). (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`External Location Code` (ro) - **`External Location Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_EXTERNAL_LOCATION`.

## Automation (code in ec-automation)
- **Playwright:** `py/external_location_iud.py` (shared engine `ec_object_iud.py` + `click_go`).
- **RF:** T3 `pageobjects/Configuration/Assets/Facility_Objects/external_location_page.resource` (**label-driven**) + suite `tests/Configuration/Assets/Facility_Objects/external_location_iud.robot`.
- **Gate:** `verify_screen.py` -> OVERALL PASS.

## Quirks
- GO-only navigator: fields are optional FILTERS (not a scope cascade) - GO alone loads the grid. Do not assume a mandatory scope exists on every OV-GM-shaped screen.
