# Screen: Contract Area Setup

- **Type:** Custom-URL OV (EC Object Configuration, date-effective) - grid loads directly; toolbar Refresh.
- **BF_CODE:** CO.2038 - **Treeview:** Configuration > Assets > Contract_Objects > Contract Area Setup
- **DB view:** `OV_CONTRACT_AREA_SETUP` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-07-31 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF 4/4 pass + Playwright 7/7, DB-verified, self-clean)

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Contract Area Setup` -> `label.tv-link` "Contract Area Setup" |
| Navigator | none - grid loads from the screen URL; re-query via toolbar Refresh `[Ctrl+r]` |
| Grid | `nav:form:T_data` (lists on open) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Contract Area Setup Code*** - **Contract Area Setup Name*** - **Start Date*** (date). (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Contract Area Setup Code` (ro) - **`Contract Area Setup Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_CONTRACT_AREA_SETUP`.

## Automation (code in ec-automation)
- **Playwright:** `py/contract_area_setup_iud.py` (shared engine `ec_object_iud.py` + toolbar Refresh).
- **RF:** T3 `pageobjects/Configuration/Assets/Contract_Objects/contract_area_setup_page.resource` (**label-driven**) + suite `tests/Configuration/Assets/Contract_Objects/contract_area_setup_iud.robot`.
- **Gate:** `verify_screen.py` -> OVERALL PASS.

## Quirks
- Custom-URL OV: no navigator GO; the toolbar Refresh `[Ctrl+r]` is the re-query gesture.

_Family text corrected 2026-07-31 (prose only; code and gate results unchanged): this bundle shipped with OV-GM wording that does not describe this screen - the packager templates were OV-GM-only until then._
