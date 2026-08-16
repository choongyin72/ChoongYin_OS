# Screen: Chemical Stream

- **Type:** OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel; navigator-GATED.
- **BF_CODE:** CO.0258 - **Treeview:** Configuration > Assets > Chemical_Objects > Chemical Stream
- **DB view:** `OV_CHEM_STREAM` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-07-30 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF 4/4 pass + Playwright 8/8, DB-verified, self-clean)

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Chemical Stream` -> `label.tv-link` "Chemical Stream" |
| Navigator (gated) | cascade `nav:form:G:0:R:1:C:1..3:dd` = P1 Production Unit -> P1 Area -> P1 Facility 1 (SPECIFIC values - From Connection popup source empty under first-available AS1) -> GO `#button:form:B` |
| Grid | `manageObject:form:T_data` (empty until cascade + GO) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Chemical Stream Code*** - **Chemical Stream Name*** - **Start Date*** (date) + **Chemical Stream Type*** (first-available) + **From Connection*** POPUP (stream_node_ref_popup: inner Object Type dd `nav:form:G:4` = CHEM_TANK -> inner GO `button:form:B` -> grid `manage_object_nav_nav:form:T_data`, first row; screen-LOCAL picker - generic PopupList helpers do not fit). Start Date is R:0, BEFORE Code. (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
**Corrected 2026-08-16 (was stale - previously listed only Code/Name):** live `field_inventory()`
scan found **36 fields**, not 2. All optional (no mandatory yellow on Update). 21 are dropdowns:
`Actual Dosage Method`, `Alloc Data Frequency`, `Alloc Fixed`, `Alloc Period`,
`Chemical Stream Type`, `Class Attribute`, `Class Name`, `Cp Area`, `Cp Collection Point`,
`Cp Operator Route`, `Cp Production Unit`, `Geo Area`, `Geo Field`, `Injection Phase`, `Op Area`,
`Op Facility Class 1`, `Op Production Unit`, `Stream Category`, `Stream Phase`, `Stream Type`,
`Usage Reporting`. 3 are popups: `From Connection`, `Production Object`, `To Connection`. The rest
are text (`Chemical Stream Code` ro, `Chemical Stream Name`, `Actual Rate Method`,
`Actual Rate Source`, `Latitude`, `Longitude`, `Maximum Flow Rate [L/d]`,
`Minimum Measurable Flow Rate [L/d]`, `Sort Order`, `Stream Node Diagram Label`,
`Target Dosage [ppm]`, `Target Rate Method`). Delete: **`End Date`** = Start Date -> leaves
`OV_CHEM_STREAM`.

Note: `Alloc Data Frequency`/`Cp Area`/`Cp Collection Point`/`Cp Operator Route`/`Geo Field` are
type-to-search autocompletes with no default list - `select(label, "__FIRST__")` cannot resolve
these (confirmed live), a real search value is required.

## Automation (code in ec-automation)
- **Playwright:** `py/chemical_stream_iud.py` (shared engine `ec_object_iud.py` + `apply_ovgm_navigator`).
- **RF:** T3 `pageobjects/Configuration/Assets/Chemical_Objects/chemical_stream_page.resource` (**label-driven**) + suite `tests/Configuration/Assets/Chemical_Objects/chemical_stream_iud.robot`.
- **Gate:** `verify_screen.py` -> OVERALL PASS.

## Quirks
- OV-GM navigator-gated: grid empty until cascade + GO. First-available nav PU is a sparse test scope - it is
  NOT necessarily a valid Op Production Unit option, and it empties nav-scoped popups (see issue OV_SWEEP_PARKED);
  navigator needs SPECIFIC P1 values; the From Connection popup needs INNER driving (Object Type + GO) - 'empty source' errors can mean undriven popup, not missing data.
