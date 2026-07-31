# Screen: Well Bore Interval

- **Type:** OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel; navigator-GATED.
- **BF_CODE:** CO.0057 - **Treeview:** Configuration > Assets > Well_and_Reservoir_Objects > Well Bore Interval
- **DB view:** `OV_WELL_BORE_INTERVAL` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-07-31 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF 4/4 pass + Playwright 8/8, DB-verified, self-clean)

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Well Bore Interval` -> `label.tv-link` "Well Bore Interval" |
| Navigator (gated) | PER-FIELD groups `nav:form:G:1..G:6:R:1:C:0:dd`: G:1 P1 Production Unit / G:2 P1 Area / G:3 P1 Facility 1 / G:4 **P1 W008 OP** (real well) / **G:6 P1 W008 WB001** (well bore) -> GO. G:5 = 0 options in every scope tried, SKIP |
| Grid | `manageObject:form:T_data` (empty until cascade + GO) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Well Bore Interval Code*** - **Well Bore Interval Name*** - **Start Date*** (date) + popups Well Bore - Op Production Unit (first-available, grid visibility). (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Well Bore Interval Code` (ro) - **`Well Bore Interval Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_WELL_BORE_INTERVAL`.

## Automation (code in ec-automation)
- **Playwright:** `py/well_bore_interval_iud.py` (shared engine `ec_object_iud.py` + `apply_ovgm_navigator`).
- **RF:** T3 `pageobjects/Configuration/Assets/Well_and_Reservoir_Objects/well_bore_interval_page.resource` (**label-driven**) + suite `tests/Configuration/Assets/Well_and_Reservoir_Objects/well_bore_interval_iud.robot`.
- **Gate:** `verify_screen.py` -> OVERALL PASS.

## Quirks
- OV-GM navigator-gated: grid empty until cascade + GO. First-available nav PU is a sparse test scope - it is
  NOT necessarily a valid Op Production Unit option, and it empties nav-scoped popups (see issue OV_SWEEP_PARKED);
  the 'Well Bore' popup list grid is `Objects:form:T_data` (generic PopupList helpers give a false 'empty source'); pick the nav-scope bore BY VALUE. Popup LABEL is 'Well Bore'.
