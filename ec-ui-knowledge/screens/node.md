# Screen: Node

- **Type:** OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel; navigator-GATED.
- **BF_CODE:** CD.0006 - **Treeview:** Configuration > Assets > Calculation_Objects > Node
- **DB view:** `OV_NODE` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-07-30 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF 4/4 pass + Playwright 8/8, DB-verified, self-clean)

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Node` -> `label.tv-link` "Node" |
| Navigator (gated) | cascade `nav:form:G:0:R:1:C:1..N:dd` = Production Unit -> Area -> Facility Class 1 (first-available) -> GO `#button:form:B` |
| Grid | `manageObject:form:T_data` (empty until cascade + GO) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Node Code*** - **Node Name*** - **Start Date*** (date) - Op Production Unit (first-available, grid visibility). (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Node Code` (ro) - **`Node Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_NODE`.

## Automation (code in ec-automation)
- **Playwright:** `py/node_iud.py` (shared engine `ec_object_iud.py` + `apply_ovgm_navigator`).
- **RF:** T3 `pageobjects/Configuration/Assets/Calculation_Objects/node_page.resource` (**label-driven**) + suite `tests/Configuration/Assets/Calculation_Objects/node_iud.robot`.
- **Gate:** `verify_screen.py` -> OVERALL PASS.

## Quirks
- OV-GM navigator-gated: grid empty until cascade + GO. First-available nav PU is a sparse test scope - it is
  NOT necessarily a valid Op Production Unit option, and it empties nav-scoped popups (see issue OV_SWEEP_PARKED);
  parent-dd + Op PU use first-available, probe per screen.
