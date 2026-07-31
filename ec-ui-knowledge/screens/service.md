# Screen: Service

- **Type:** OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel; navigator-GATED.
- **BF_CODE:** CO.2103 - **Treeview:** Configuration > Assets > Service_Objects > Service
- **DB view:** `OV_SERVICE` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-08-01 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF 4/4 pass + Playwright 8/8, DB-verified, self-clean)

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Service` -> `label.tv-link` "Service" |
| Navigator | cascade `nav:form:G:0:R:1:C:1..N:dd` (first-available) -> GO `#button:form:B` |
| Grid | `manageObject:form:T_data` (empty until cascade + GO) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Service Code*** - **Service Name*** - **Start Date*** (date) + dropdowns Service Template, Service Type, Service Status, Contract=TS3 GTA Shipper A, Transport System=TS3 Transport System - Op Production Unit (first-available, grid visibility). (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Service Code` (ro) - **`Service Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_SERVICE`.

## Automation (code in ec-automation)
- **Playwright:** `py/service_iud.py` (shared engine `ec_object_iud.py` + `apply_ovgm_navigator`).
- **RF:** T3 `pageobjects/Configuration/Assets/Service_Objects/service_page.resource` (**label-driven**) + suite `tests/Configuration/Assets/Service_Objects/service_iud.robot`.
- **Gate:** `verify_screen.py` -> OVERALL PASS.

## Quirks
- OV-GM navigator-gated: grid empty until cascade + GO. First-available nav PU is a sparse test
  scope - NOT necessarily a valid Op Production Unit option, and it empties nav-scoped popups
  (see tmp/OV_SWEEP_PARKED.md); parent-dd + Op PU use first-available, probe per screen.
