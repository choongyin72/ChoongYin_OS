# Screen: Collection Point

- **Type:** OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel; navigator-GATED.
- **BF_CODE:** CO.0205 - **Treeview:** Configuration > Assets > Facility_Objects > Collection Point
- **DB view:** `OV_COLLECTION_POINT` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-08-01 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF 4/4 pass + Playwright 8/8, DB-verified, self-clean)

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Collection Point` -> `label.tv-link` "Collection Point" |
| Navigator | cascade `nav:form:G:0:R:1:C:1..N:dd` (PROVEN explicit values, not first-available) -> GO `#button:form:B` |
| Grid | `manageObject:form:T_data` (empty until cascade + GO) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Collection Point Code*** - **Collection Point Name*** - **Start Date*** (date). (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Collection Point Code` (ro) - **`Collection Point Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_COLLECTION_POINT`.

## Automation (code in ec-automation)
- **Playwright:** `py/collection_point_iud.py` (shared engine `ec_object_iud.py` + `apply_ovgm_navigator`).
- **RF:** T3 `pageobjects/Configuration/Assets/Facility_Objects/collection_point_page.resource` (**label-driven**) + suite `tests/Configuration/Assets/Facility_Objects/collection_point_iud.robot`.
- **Gate:** `verify_screen.py` -> OVERALL PASS.

## Quirks
- OV-GM: nav cascade uses PROVEN explicit values from `scripts/find_populated_scope.py` (not first-available) - the alphabetically/positionally-first option is NOT guaranteed to have data underneath it; see ov-gm-navigator-capability.md.
