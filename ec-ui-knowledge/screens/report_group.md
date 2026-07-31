# Screen: Report Group

- **Type:** Plain OV (EC Object Configuration, date-effective) - Bank family; date-only navigator + GO.
- **BF_CODE:** CO.0158 - **Treeview:** Configuration > Assets > Facility_Objects > Report Group
- **DB view:** `OV_REPORT_GROUP` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-07-31 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF 4/4 pass + Playwright 8/8, DB-verified, self-clean)

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Report Group` -> `label.tv-link` "Report Group" |
| Navigator | date field `nav:form:G:0:R:1:C:0:da_input` -> GO `#button:form:B` (no cascade) |
| Grid | `report_group_table:form:T_data` (lists after GO) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Reporting Group Code*** - **Reporting Group Name*** - **Start Date*** (date) + dropdowns Business Area. (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Reporting Group Code` (ro) - **`Reporting Group Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_REPORT_GROUP`.

## Automation (code in ec-automation)
- **Playwright:** `py/report_group_iud.py` (shared engine `ec_object_iud.py` + `click_go`).
- **RF:** T3 `pageobjects/Configuration/Assets/Facility_Objects/report_group_page.resource` (**label-driven**) + suite `tests/Configuration/Assets/Facility_Objects/report_group_iud.robot`.
- **Gate:** `verify_screen.py` -> OVERALL PASS.

## Quirks
- Plain OV (Bank family): the navigator is a single DATE field + GO, no cascade and no Op PU.
- An UNSAVED CHANGES dialog (YES/NO) can block GO right after the End=Start close - answer YES
  (that commits the intended delete).
