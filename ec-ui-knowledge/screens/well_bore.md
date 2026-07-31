# Screen: Well Bore

- **Type:** OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel; navigator-GATED.
- **BF_CODE:** CO.0054 - **Treeview:** Configuration > Assets > Well_and_Reservoir_Objects > Well Bore
- **DB view:** `OV_WELL_BORE` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-07-31 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF 4/4 pass + Playwright 8/8, DB-verified, self-clean)

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Well Bore` -> `label.tv-link` "Well Bore" |
| Navigator (gated) | PER-FIELD groups `nav:form:G:1..G:4:R:1:C:0:dd` = P1 Production Unit -> P1 Area -> P1 Facility 1 -> **P1 W008 OP** (a REAL well; first-available is `P1 Graph 001`, a graph with no bores) -> GO; G:5 'Well' = 0 options, skip |
| Grid | `manageObject:form:T_data` (empty until cascade + GO) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Well Bore Code*** - **Well Bore Name*** - **Start Date*** (date) + popups Well - Op Production Unit (first-available, grid visibility). (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Well Bore Code` (ro) - **`Well Bore Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_WELL_BORE`.

## Automation (code in ec-automation)
- **Playwright:** `py/well_bore_iud.py` (shared engine `ec_object_iud.py` + `apply_ovgm_navigator`).
- **RF:** T3 `pageobjects/Configuration/Assets/Well_and_Reservoir_Objects/well_bore_page.resource` (**label-driven**) + suite `tests/Configuration/Assets/Well_and_Reservoir_Objects/well_bore_iud.robot`.
- **Gate:** `verify_screen.py` -> OVERALL PASS.

## Quirks
- OV-GM navigator-gated: grid empty until cascade + GO. First-available nav PU is a sparse test scope - it is
  NOT necessarily a valid Op Production Unit option, and it empties nav-scoped popups (see issue OV_SWEEP_PARKED);
  the 'Well' popup's list grid is `Objects:form:T_data` (3rd variant; generic PopupList helpers report a false 'empty source'); pick the nav-scope well BY VALUE - the popup's first row is a graph object.
