# Screen: Create Calculation

- **Type:** TV-style table class - inline grid edits; per-screen delete gesture.
- **BF_CODE:** CO.1042 - **Treeview:** Configuration > Assets > Calculation_Objects > Create Calculation
- **DB view:** `OV_CALCULATION` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-07-31 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF 4/4 pass + Playwright 8/8, DB-verified, self-clean)

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Create Calculation` -> `label.tv-link` "Create Calculation" |
| Navigator | per-screen context/date navigator (see SOW) |
| Grid | `calculation:form:T_data` |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Calculation Code*** - **Calculation Name*** - **Start Date*** (date). (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Calculation Code` (ro) - **`Calculation Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_CALCULATION`.

## Automation (code in ec-automation)
- **Playwright:** `py/create_calculation_iud.py` (shared engine `ec_object_iud.py`).
- **RF:** T3 `pageobjects/Configuration/Assets/Calculation_Objects/create_calculation_page.resource` (**label-driven**) + suite `tests/Configuration/Assets/Calculation_Objects/create_calculation_iud.robot`.
- **Gate:** `verify_screen.py` -> OVERALL PASS.

## Quirks
- TV-style: rows are edited in place; the delete gesture is per screen (see SOW).

_Family text corrected 2026-07-31 (prose only; code and gate results unchanged): this bundle shipped with OV-GM wording that does not describe this screen - the packager templates were OV-GM-only until then._
