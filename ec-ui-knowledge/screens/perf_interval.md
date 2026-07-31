# Screen: Perforation Interval

- **Type:** OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel; navigator-GATED.
- **BF_CODE:** CO.0153 - **Treeview:** Configuration > Assets > Well_and_Reservoir_Objects > Perforation Interval
- **DB view:** `OV_PERF_INTERVAL` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-07-31 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF 4/4 pass + Playwright 8/8, DB-verified, self-clean)

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Perforation Interval` -> `label.tv-link` "Perforation Interval" |
| Navigator (gated) | PER-FIELD groups `nav:form:G:1..G:7:R:1:C:0:dd`: G:1 P1 Production Unit / G:2 P1 Area / G:3 P1 Facility 1 / G:4 **P1 W008 OP** / **G:6 P1 W008 WB001** / **G:7 P1 W008 WB001 WBI001** -> GO. G:5 = 0 options, SKIP |
| Grid | `manageObject:form:T_data` (empty until cascade + GO) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Perforation Interval Code*** - **Perforation Interval Name*** - **Start Date*** (date) + dropdowns Reservoir Block Formation + popups Well Bore Interval - Op Production Unit (first-available, grid visibility). (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Perforation Interval Code` (ro) - **`Perforation Interval Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_PERF_INTERVAL`.

## Automation (code in ec-automation)
- **Playwright:** `py/perf_interval_iud.py` (shared engine `ec_object_iud.py` + `apply_ovgm_navigator`).
- **RF:** T3 `pageobjects/Configuration/Assets/Well_and_Reservoir_Objects/perf_interval_page.resource` (**label-driven**) + suite `tests/Configuration/Assets/Well_and_Reservoir_Objects/perf_interval_iud.robot`.
- **Gate:** `verify_screen.py` -> OVERALL PASS.

## Quirks
- OV-GM navigator-gated: grid empty until cascade + GO. First-available nav PU is a sparse test scope - it is
  NOT necessarily a valid Op Production Unit option, and it empties nav-scoped popups (see issue OV_SWEEP_PARKED);
  the 'Well Bore Interval' popup is the INNER-GO type: it inherits the outer scope but its list grid `Objects:form:T_data` is EMPTY until the popup's own `button:form:B` is clicked (an empty popup list is NOT proof of missing data). 'Reservoir Block Formation' dd is also mandatory.
