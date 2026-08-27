# Screen: External Location

- **Type:** OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel. Classified as
  the Area pattern's **zero-mandatory-nav edge case**: GO only - NO mandatory nav scope (fields are
  optional filters), unlike Area/Well/Test Separator/Chemical Tank.
- **BF_CODE:** CO.0227 - **Treeview:** Configuration > Assets > Facility_Objects > External Location
- **DB view:** `OV_EXTERNAL_LOCATION` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-08-27 - EC 14.2.4 - local sandbox - RF live 5/5 (dryrun 883/883, DB
  self-clean 0/0, hygiene PASS - this backfill session, re-run of the automation merged 2026-08-26 via
  PR #524/#528). Original base build: 2026-08-01, `verify_screen.py` OVERALL PASS (RF 4/4 + Playwright
  8/8, DB-verified, self-clean) - superseded by the RF structure below.

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `External Location` -> `label.tv-link` "External Location" |
| Navigator | GO only (navigator fields are optional filters, no mandatory scope) - RF delegates to
  shared T2 `Apply Navigator From Properties` with an intentionally EMPTY
  `testdata/external_location_navigator.properties` (zero data lines -> zero fills -> bare GO) |
| Grid | `manageObject:form:T_data` (lists on GO with no filters set) |
| Grid filter | `Find/Clear External Location Row By Filter` (T3) -> shared T2 `Find/Clear Object Row
  By Filter` on `manageObject:form:T_data`, filters the Code column |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |
| Delete End Date field | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (hardcoded - packs
  Start Date C:1 + End Date label C:2 + End Date input C:3 in one row; not label-scannable) |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**External Location Code*** - **External Location Name*** - **Start Date*** (date). (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`External Location Code` (ro) - **`External Location Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_EXTERNAL_LOCATION`.

## Automation (code in ec-automation)
- **Playwright:** `py/external_location_iud.py` (shared engine `ec_object_iud.py` + `click_go`) -
  built 2026-08-01, untouched by the 2026-08-26 RF conversion.
- **RF:** T3 `pageobjects/Configuration/Assets/Facility_Objects/external_location_page.resource`
  (**label-driven**, screen-prefixed `code_label=External Location Code` per T2 call, like Area) +
  suite `tests/Configuration/Assets/Facility_Objects/external_location_iud.robot` - converted
  2026-08-26 (PR #524 navigator-fill, PR #528 full structural conversion) to Area's **5-TC** pattern:
  TC01 Verify Clean State -> TC02 Insert -> TC03 Update -> TC04 Find -> TC05 Delete, per-TC
  Login/Logout, fixed test code `AUTOTEST_EXTERNAL_LOCATION`, properties-file-driven insert/update
  (`testdata/external_location_{insert,update,form_verify,grid_verify,navigator}.properties`),
  explicit grid-filter wiring, PURE SCREEN verification (zero inline DB-verify calls in the .robot -
  the DB check lives solely inside the shared T2 `Verify Object Removed`).
- **Gate (base build):** `verify_screen.py` -> OVERALL PASS, 2026-08-01. **Gate (2026-08-26
  conversion + 2026-08-27 backfill re-run):** dryrun 883/883, live RF 5/5, robocop 7 issues (VAR02
  x2 + DOC02 x5, parity with Area's reference files), fresh-connection DB self-clean 0/0, hygiene PASS.

## Quirks
- GO-only navigator: fields are optional FILTERS (not a scope cascade) - GO alone loads the grid. Do
  not assume a mandatory scope exists on every OV-GM-shaped screen.
- The RF suite drives the "no mandatory nav" behaviour through the SAME shared keyword Area uses for
  its mandatory Production-Unit cascade (`Apply Navigator From Properties`) - the difference is
  entirely in the properties file's content (empty here), not in a different code path. Confirmed via
  source-read of `PropertiesReader.read_properties()`: an all-comment file returns `{}`, so the
  keyword's fill loop runs 0 iterations and falls straight through to a bare GO.
