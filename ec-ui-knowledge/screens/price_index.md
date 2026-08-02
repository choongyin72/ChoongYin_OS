# Screen: Price Index

- **Type:** OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel; navigator-GATED.
- **BF_CODE:** CO.3009 - **Treeview:** Configuration > Assets > Sales Objects > Price Index
- **DB view:** `OV_PRICE_INDEX` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`, `BUSINESS_UNIT_CODE`, `FREQUENCY`)
- **Last verified:** 2026-08-02 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF 4/4 pass + Playwright 8/8, DB-verified, self-clean)

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Price Index` -> `label.tv-link` "Price Index" |
| Navigator | Date + Business Unit dropdown, SAME group `nav:form:G:0:R:1:C:1:dd` (MANDATORY) -> GO `#button:form:B` |
| Grid | `manageObject:form:T_data` (empty until Business Unit + GO) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Price Index Code*** - **Price Index Name*** - **Start Date*** (date) - End Date - Source - Upload
Type - Upload Address - Units - **Frequency*** - Comments - Sort Order - Currency -
**Business Unit*** (reference dropdown, must equal nav scope) - Product. (`*` mandatory per live scan.)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Price Index Code` (ro) - **`Price Index Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_PRICE_INDEX`.

## Automation (code in ec-automation)
- **Playwright:** `py/price_index_iud.py` (shared engine `ec_object_iud.py` + explicit `select_dropdown` - PROVEN value, not `apply_ovgm_navigator`).
- **RF:** T3 `pageobjects/Configuration/Assets/Sales_Objects/price_index_page.resource` (**label-driven**) + suite `tests/Configuration/Assets/Sales_Objects/price_index_iud.robot`.
- **Gate:** `verify_screen.py` -> OVERALL PASS.

## Quirks
- **Same reference-dropdown date trap as Property** (see `ec-ui-knowledge/screens/property.md`): the
  Business Unit dropdown only offers Business Units already effective as of the record's own Start
  Date. "Royalty Canada" (`ROYALTY_CA`) is only valid from `2003-01-01` onward. Fix: use Start Date
  `>= 2003-01-01` for ANY screen with a reference dropdown. See memory
  `feedback_child_object_date_must_follow_parent`.
- Unlike Property, Date and Business Unit ARE in the same navigator group (`G:0`) here - the
  generator's default nav-dropdown id template worked without correction on this screen.
