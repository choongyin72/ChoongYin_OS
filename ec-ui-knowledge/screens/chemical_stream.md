# Screen: Chemical Stream

- **Type:** OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel; navigator-GATED.
- **BF_CODE:** CO.0258 - **Treeview:** Configuration > Assets > Chemical_Objects > Chemical Stream
- **DB view:** `OV_CHEM_STREAM` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-08-27 - EC 14.2.4 - local sandbox - live RF 5/5 pass (post PR #545
  Area-pattern conversion), DB-verified, self-clean (fresh oracledb connection, 0 residual
  `AUTOTEST%` rows in `OV_CHEM_STREAM` before and after). Prior state (2026-07-30):
  `verify_screen.py` OVERALL PASS, RF 4/4 pass + Playwright 8/8.

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
- **Playwright (unchanged since 2026-07-30):** `py/chemical_stream_iud.py` (shared engine
  `ec_object_iud.py` + `apply_ovgm_navigator`).
- **RF (converted to the Area pattern, PR #545, merged 2026-08-26):** T3
  `pageobjects/Configuration/Assets/Chemical_Objects/chemical_stream_page.resource` (**label-driven**,
  5 TCs' worth of keywords) + suite
  `tests/Configuration/Assets/Chemical_Objects/chemical_stream_iud.robot` (5 TCs: Verify Clean
  State/Insert/Update/Find/Delete). Navigator fill now delegates to the shared T2
  `Apply Navigator From Properties` (`resources/manage_object.resource`) driven by
  `testdata/chemical_stream_navigator.properties` (replacing the old screen-local
  `Apply Chemical Stream Navigator` keyword). Per-TC `Login To EC Application`/
  `Logout From EC Application` on ONE browser opened once in Suite Setup, own credential pair
  `CHEMICAL_STREAM_EC_USER`/`CHEMICAL_STREAM_EC_PASS` in `resources/credentials.py`. Fixed test
  code `AUTOTEST_CHS` (was a per-run timestamped code before the conversion). Insert/Update/Verify
  driven by `testdata/chemical_stream_{insert,update,form_verify,grid_verify}.properties` via the
  shared T2 `Insert/Update Object From Properties`/`Verify Object *`. Explicit
  `Find/Clear Chemical Stream Row By Filter` grid-filter wiring into Update/Find/Verify-Found/
  Delete. Zero inline DB-verify calls remain in the `.robot` file — DB checks now live only inside
  the shared T2 `Verify Object Removed`.
- **From Connection popup handling — PRESERVED UNCHANGED by the conversion:** `stream_node_ref_popup`
  is not the standard `object_popup` — screen-local T3 keywords `Open From Connection Popup List`
  (select Object Type = CHEM_TANK in the popup's own inner dd `nav:form:G:4`, click the popup's own
  inner GO `button:form:B`, wait for the popup's own list grid
  `manage_object_nav_nav:form:T_data` — NOT the generic `PopupList:form:T_data`) and
  `Pick From Connection Popup` (pick the first row). The generic T1 popup keywords in
  `resources/popup.resource` do not fit this popup type and were never used here.
- **Gate (pre-conversion snapshot):** `verify_screen.py` -> OVERALL PASS (2026-07-30). Post-conversion
  evidence lives in `screens/Configuration/Assets/Chemical_Objects/Chemical_Stream/evidence/
  2026-08-27_area_pattern_backfill/` (live 5/5 RF run, robocop, dryrun, DB self-clean check).

## Quirks
- OV-GM navigator-gated: grid empty until cascade + GO. First-available nav PU is a sparse test scope - it is
  NOT necessarily a valid Op Production Unit option, and it empties nav-scoped popups (see issue OV_SWEEP_PARKED);
  navigator needs SPECIFIC P1 values; the From Connection popup needs INNER driving (Object Type + GO) - 'empty source' errors can mean undriven popup, not missing data.
- **Fixed 2026-08-17: the From Connection popup dialog can render mostly/fully BELOW the visible
  viewport** (triggered from a field far down the long New Object form). Scrolling (page-level or
  `scrollIntoView`) does NOT fix this - confirmed by direct measurement, the dialog's position is
  independent of document scroll. It's a PrimeFaces `.ui-dialog`, draggable via its own
  `.ui-dialog-titlebar.ui-draggable-handle` - drag it (real mouse down/move/up) to near the top of
  the screen and normal clicks work afterward. See `ensure_dialog_in_view()` in `engine.py` and
  `reference_ec_popup_dialog_draggable` memory for the general technique (applies to any EC popup,
  not just this screen).
