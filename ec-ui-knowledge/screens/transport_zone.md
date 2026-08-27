# Screen: Transport Zone

- **Type:** OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel;
  Business-Unit-GATED (single-dropdown navigator, same shape as Area's own).
- **Treeview:** Configuration > Assets > Dispatching Objects > Transport Zone
- **DB view:** `OV_TRANSPORT_ZONE` (generic `CODE` column, per `libraries/DbVerify.py` - NOT a
  screen-specific `TRANSPORT_ZONE_CODE` column)
- **Last verified:** 2026-08-28 - EC 14.2.4 - local sandbox - RF dryrun 5/5 PASS + live headless
  5/5 PASS (TC01-TC05, after one disclosed page-load-timeout on the first attempt + passing
  retry), fresh-connection DB self-clean 0 residual, `check_bundle_hygiene.py` PASS (backfill
  re-run of PR #557's Area-pattern conversion, merged 2026-08-26)

## Selectors
| Purpose | Selector |
|---|---|
| Grid | `manageObject:form:T_data` (empty until nav BU + GO) |
| Navigator group | `nav:form:G:0` - THREE columns |
| Navigator Date (pre-filled, not empty-mandatory) | `nav:form:G:0` C:0 |
| **Navigator Business Unit (mandatory dd)** | `nav:form:G:0` C:1 -> GO |
| Navigator 2nd dropdown (optional filter, `mandatory:false` confirmed live) | `nav:form:G:0` C:2 |
| Delete (End Date field) | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (hardcoded, not
  label-driven - the row packs Start Date C:1 + End Date C:3 with the End Date label at C:2) |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Transport Zone Code*** - **Transport Zone Name*** - Start Date* (date) - **Transport System
Name*** (dropdown, mandatory, R:5, bound to the nav Business Unit scope - "TS5 Transport System"
pairs with nav "TS5 BU"). Zone Type (R:2) and End Date (R:4) confirmed `mandatory:false` -
deliberately excluded from insert data. Labels are SCREEN-PREFIXED ("Transport Zone
Code"/"Transport Zone Name"), like Area's "Area Code"/"Area Name" - NOT the generic "Code"/"Name"
Bank/Object List use. (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Transport Zone Code` is READ-ONLY in `updateAttributes` - **`Transport Zone Name`** is the only
field actually re-edited by TC03. Delete: **`End Date`** = Start Date (zero-length window) ->
true delete, row leaves `OV_TRANSPORT_ZONE`.

## Navigator values (this environment)
Business Unit = `TS5 BU` - driven by `testdata/transport_zone_navigator.properties` via the shared
T2 `Apply Navigator From Properties` keyword. Insert Transport System Name dropdown = `TS5
Transport System` (must pair with the TS5 BU nav scope or the inserted row is not visible under
this OV-GM navigator scope).

## Automation (code in ec-automation)
- **RF (maintained/live test):** T3
  `pageobjects/Configuration/Assets/Dispatching_Objects/transport_zone_page.resource`
  (label-driven, 2026-08-26 Area-pattern conversion, PR #557) + suite
  `tests/Configuration/Assets/Dispatching_Objects/transport_zone_iud.robot` (5 TC: Clean State /
  Insert / Update / Find / Delete, per-TC login/logout, fixed test code
  `AUTOTEST_TRANSPORT_ZONE`).
- **Playwright:** none. No Playwright bundle exists and none is built for Area-pattern work
  (owner decision 2026-08-27, Universal Screen Engine replaces this role).
- **Test data:** `testdata/transport_zone_{navigator,insert,update,form_verify,grid_verify}.properties`.
- **Credentials:** dedicated pair `TRANSPORT_ZONE_EC_USER`/`TRANSPORT_ZONE_EC_PASS` in
  `resources/credentials.py`.

## Quirks
- OV-GM Business-Unit-gated: grid empty until the nav Business Unit dropdown + GO completes.
- The navigator's second dropdown (`C:2`) LOOKS like it might also be mandatory (same row as
  Business Unit) but is confirmed live `mandatory:false` - GO succeeds with only the Business Unit
  filled. Do not assume every dropdown on the navigator row is required.
- The navigator's Date column (`C:0`) is `mandatory:true` in the DOM but ALREADY defaulted/filled
  on load - no live fill action is needed for it, unlike Business Unit.
- DB self-clean checks against `OV_TRANSPORT_ZONE` must use the generic `CODE` column, not a
  screen-specific `TRANSPORT_ZONE_CODE` column.
- A shared-environment page-load timeout was hit once during this backfill's own live-run evidence
  capture (TC01 timed out waiting for the menu search textbox at
  `[id="menu:searchForm:searchTxt"]`) - not reproduced on immediate retry; treat a single such
  failure as environment/timing contention, not a screen defect, before re-investigating the
  automation itself.
- See `screens/Configuration/Assets/Dispatching_Objects/Transport_Zone/JOURNAL.md` for the full
  backfill account (this KB entry summarizes; that JOURNAL is the fuller narrative).
