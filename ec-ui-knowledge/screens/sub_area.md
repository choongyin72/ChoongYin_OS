# Screen: Sub Area

- **Type:** OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel; navigator-GATED.
- **Treeview:** Configuration > Assets > Basic Objects > Sub Area
- **DB view:** `OV_SUB_AREA` (generic `CODE` column, per `libraries/DbVerify.py` - NOT a
  screen-specific `SUB_AREA_CODE` column, confirmed live 2026-08-27)
- **Last verified:** 2026-08-27 - EC 14.2.4 - local sandbox - RF dryrun 5/5 PASS + live headless
  5/5 PASS (TC01-TC05), fresh-connection DB self-clean 0 residual, `check_bundle_hygiene.py` PASS
  (backfill re-run of PR #538's Area-pattern conversion, merged 2026-08-26)

## Selectors
| Purpose | Selector |
|---|---|
| Grid | `manageObject:form:T_data` (empty until cascade + GO) |
| Navigator (gated, 2-level cascade, same row) | `nav:form:G:0:R:1:C:1:dd` (Production Unit) -> `nav:form:G:0:R:1:C:2:dd` (Area) -> GO |
| Delete (End Date field) | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (hardcoded, not label-driven - the row packs Start Date C:1 + End Date C:3 with the label at C:2) |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Sub Area Code*** - **Sub Area Name*** - Start Date* (date) - **Op Production Unit*** (dropdown,
MANDATORY) - **Op Area*** (dropdown, MANDATORY). Labels are SCREEN-PREFIXED ("Sub Area Code"/"Sub
Area Name"), like Area's "Area Code"/"Area Name" - NOT the generic "Code"/"Name" Bank/Object List
use. (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Sub Area Code` (ro, guard) - **`Sub Area Name`**. Delete: **`End Date`** = Start Date (zero-length
window) -> true delete, row leaves `OV_SUB_AREA`.

### Grid columns (confirmed live, `manageObject:form:T_head` scan)
Sub Area Code / Sub Area Name / Start Date / End Date (4-column shape, same as Area/Facility
Class 1).

## Navigator values (this environment)
Op Production Unit = `Production Unit`, Op Area = `Offshore area` (user-approved 2026-06-11,
unchanged by the PR #538 conversion) - driven by `testdata/sub_area_navigator.properties` via the
shared T2 `Apply Navigator From Properties` keyword.

## Automation (code in ec-automation)
- **RF (maintained/live test):** T3
  `pageobjects/Configuration/Assets/Basic_Objects/sub_area_page.resource` (label-driven, 2026-08-26
  Area-pattern conversion, PR #538) + suite
  `tests/Configuration/Assets/Basic_Objects/sub_area_iud.robot` (5 TC: Clean State / Insert /
  Update / Find / Delete, per-TC login/logout, fixed test code `AUTOTEST_SUB_AREA`).
- **Playwright (historical reference only, NOT maintained):** `playwright/ec_iud_sub_area.py`
  under `screens/Configuration/Assets/Basic_Objects/Sub_Area/` - original 2026-06-11 build,
  preserved unchanged; no new Playwright bundle is built for Area-pattern work (owner decision
  2026-08-27, Universal Screen Engine replaces this role).
- **Test data:** `testdata/sub_area_{navigator,insert,update,form_verify,grid_verify}.properties`.
- **Credentials:** dedicated pair `SUB_AREA_EC_USER`/`SUB_AREA_EC_PASS` in
  `resources/credentials.py`.

## Quirks
- OV-GM navigator-gated: grid empty until the PU -> Area cascade + GO completes.
- LEADING-SPACE QUIRK (original 2026-06-11 recon): the sandbox area names are stored with a
  leading space (`' Offshore area'`, invisible in any trimmed UI display) - option matching must
  use normalize-space on `data-item-label`. Handled inside the shared navigator-fill keyword; not
  screen-local code.
- `objectForm` fills Op Production Unit/Op Area on insert (matching the navigator context) - this
  is DIFFERENT from Facility Class 1, which is proven to work with those fields left BLANK. Do not
  assume one screen's blank-field behavior applies to the other; each is its own proven, tested
  shape.
- DB self-clean checks against `OV_SUB_AREA` must use the generic `CODE` column, not a
  screen-specific `SUB_AREA_CODE` column (confirmed live 2026-08-27; the screen-specific column
  name does not exist in the view).
