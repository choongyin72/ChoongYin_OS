# Screen: Loading Arm

- **Type:** OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel; navigator-GATED.
- **BF_CODE:** CO.2078
- **Treeview:** Configuration > Assets > Transport_Objects > Loading Arm
- **DB view:** `OV_LOADING_ARM` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-07-30 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF 4/4 pass + Playwright 8/8, DB-verified, self-clean)

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Loading Arm` -> `label.tv-link` "Loading Arm" |
| Navigator (gated) | cascade `nav:form:G:0:R:1:C:1..N:dd` = Production Unit -> Area -> Facility Class 1 (first-available) -> GO `#button:form:B` |
| Grid | `manageObject:form:T_data` (empty until cascade + GO) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Loading Arm Code*** - **Loading Arm Name*** - **Start Date*** (date) - Op Production Unit (first-available, grid visibility). (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Loading Arm Code` (ro) - **`Loading Arm Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_LOADING_ARM`.

## Automation (code in ec-automation)
- **Playwright:** `py/loading_arm_iud.py` (shared engine `ec_object_iud.py` + `apply_ovgm_navigator`).
- **RF:** T3 `pageobjects/Configuration/Assets/Transport_Objects/loading_arm_page.resource` (**label-driven**) + suite `tests/Configuration/Assets/Transport_Objects/loading_arm_iud.robot`.
- **Gate:** `verify_screen.py` -> OVERALL PASS.

## Quirks
- OV-GM navigator-gated: grid empty until cascade + GO. First-available nav PU is a sparse test scope - it is
  NOT necessarily a valid Op Production Unit option, and it empties nav-scoped popups (see issue OV_SWEEP_PARKED);
  parent-dd + Op PU use first-available, probe per screen.
