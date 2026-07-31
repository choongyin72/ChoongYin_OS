# Screen: Well

- **Type:** OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel; navigator-GATED.
- **BF_CODE:** CO.0049 - **Treeview:** Configuration > Assets > Well_and_Reservoir_Objects > Well
- **DB view:** `OV_WELL` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-07-30 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF 4/4 pass + Playwright 8/8, DB-verified, self-clean)

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Well` -> `label.tv-link` "Well" |
| Navigator (gated) | cascade `nav:form:G:0:R:1:C:1..3:dd` = P1 Production Unit -> P1 Area -> P1 Facility 1 (SPECIFIC values; AS1 first-available leaves a deeper level empty) -> GO `#button:form:B`; 2nd-row Well & Well Hookup / Well dds = optional filters, leave EMPTY |
| Grid | `manageObject:form:T_data` (empty until cascade + GO) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Well Code*** - **Well Name*** - **Start Date*** (date) + **Well Type*** (first-available). NO Op Production Unit field. (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Well Code` (ro) - **`Well Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_WELL`.

## Automation (code in ec-automation)
- **Playwright:** `py/well_iud.py` (shared engine `ec_object_iud.py` + `apply_ovgm_navigator`).
- **RF:** T3 `pageobjects/Configuration/Assets/Well_and_Reservoir_Objects/well_page.resource` (**label-driven**) + suite `tests/Configuration/Assets/Well_and_Reservoir_Objects/well_iud.robot`.
- **Gate:** `verify_screen.py` -> OVERALL PASS.

## Quirks
- OV-GM navigator-gated: grid empty until cascade + GO. Navigator needs SPECIFIC P1 values - the
  first-available AS1 scope leaves a deeper nav level empty (the original park reason, see
  OV_SWEEP_PARKED). 2nd-row Well filter dds are optional - leave empty. No form parent field needed
  (rows list under the nav scope without an Op Production Unit field, like Facility Class 1).
