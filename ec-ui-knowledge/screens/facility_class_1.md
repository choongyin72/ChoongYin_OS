# Screen: Facility Class 1

- **Type:** OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel; navigator-GATED.
- **BF_CODE:** CO.0019 - **Treeview:** Configuration > Assets > Facility_Objects > Facility Class 1
- **DB view:** `OV_FCTY_CLASS_1` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-07-30 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF 4/4 pass + Playwright 8/8, DB-verified, self-clean)

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Facility Class 1` -> `label.tv-link` "Facility Class 1" |
| Navigator (gated) | cascade `nav:form:G:0:R:1:C:1..N:dd` = Production Unit -> Area (first-available) -> GO `#button:form:B` |
| Grid | `manageObject:form:T_data` (empty until cascade + GO) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Facility Class 1 Code*** - **Facility Class 1 Name*** - **Start Date*** (date) - Op Production Unit (first-available, grid visibility). (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Facility Class 1 Code` (ro) - **`Facility Class 1 Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_FCTY_CLASS_1`.

## Automation (code in ec-automation)
- **Playwright:** `py/facility_class_1_iud.py` (shared engine `ec_object_iud.py` + `apply_ovgm_navigator`).
- **RF:** T3 `pageobjects/Configuration/Assets/Facility_Objects/facility_class_1_page.resource` (**label-driven**) + suite `tests/Configuration/Assets/Facility_Objects/facility_class_1_iud.robot`.
- **Gate:** `verify_screen.py` -> OVERALL PASS.

## Quirks
- OV-GM navigator-gated: grid empty until cascade + GO. First-available nav PU is a sparse test scope - it is
  NOT necessarily a valid Op Production Unit option, and it empties nav-scoped popups (see issue OV_SWEEP_PARKED);
  parent-dd + Op PU use first-available, probe per screen.
