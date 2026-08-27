# Screen: Contract Area

- **Type:** OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel;
  Business-Unit-GATED (single-dropdown navigator, same shape as Area's own).
- **Treeview:** Configuration > Assets > Contract Objects > Contract Area
- **DB view:** `OV_CONTRACT_AREA` (generic `CODE` column, per `libraries/DbVerify.py` - NOT a
  screen-specific `CONTRACT_AREA_CODE` column)
- **Last verified:** 2026-08-27 - EC 14.2.4 - local sandbox - RF dryrun 5/5 PASS + live headless
  5/5 PASS (TC01-TC05), fresh-connection DB self-clean 0 residual, `check_bundle_hygiene.py` PASS
  (backfill re-run of PR #542's Area-pattern conversion, merged 2026-08-26)

## Selectors
| Purpose | Selector |
|---|---|
| Grid | `manageObject:form:T_data` (empty until nav BU + GO) |
| Navigator (single dropdown) | `nav:form:G:0:R:1:C:1:dd` = Business Unit -> GO (`button:form:B`) |
| Nav date (optional) | `nav:form:G:0:R:1:C:0:da_input` |
| Delete (End Date field) | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (hardcoded, not
  label-driven - the row packs Start Date C:1 + End Date C:3 with the End Date label at C:2) |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Contract Area Code*** - **Contract Area Name*** - Start Date* (date) - End Date (optional) -
Comments (optional) - **Business Unit Name*** (dropdown, MANDATORY - must equal the nav BU or the
inserted row never lists in the filtered grid) - Use as Property (checkbox, optional). Labels are
SCREEN-PREFIXED ("Contract Area Code"/"Contract Area Name"), like Area's "Area Code"/"Area Name" -
NOT the generic "Code"/"Name" Bank/Object List use. (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Contract Area Code` (ro, guard) - **`Contract Area Name`**. Delete: **`End Date`** = Start Date
(zero-length window) -> true delete, row leaves `OV_CONTRACT_AREA`.

### Grid columns (confirmed live, `manageObject:form:T_head` scan)
Contract Area Code / Contract Area Name / Start Date / End Date (4-column shape, same as
Area/Sub Area/Facility Class 1).

## Navigator values (this environment)
Business Unit = `ECP Norway` (5 existing areas at scope-selection time - most populated BU in
this sandbox; already-used, read-only seed data) - driven by
`testdata/contract_area_navigator.properties` via the shared T2 `Apply Navigator From Properties`
keyword.

## Automation (code in ec-automation)
- **RF (maintained/live test):** T3
  `pageobjects/Configuration/Assets/Contract_Objects/contract_area_page.resource` (label-driven,
  2026-08-26 Area-pattern conversion, PR #542) + suite
  `tests/Configuration/Assets/Contract_Objects/contract_area_iud.robot` (5 TC: Clean State /
  Insert / Update / Find / Delete, per-TC login/logout, fixed test code
  `AUTOTEST_CONTRACT_AREA`).
- **Playwright (historical reference only, NOT maintained):**
  `playwright/ec_iud_contract_area.py` under
  `screens/Configuration/Assets/Contract_Objects/Contract_Area/` - original 2026-06-18 build,
  preserved unchanged; no new Playwright bundle is built for Area-pattern work (owner decision
  2026-08-27, Universal Screen Engine replaces this role).
- **Test data:** `testdata/contract_area_{navigator,insert,update,form_verify,grid_verify}.properties`.
- **Credentials:** dedicated pair `CONTRACT_AREA_EC_USER`/`CONTRACT_AREA_EC_PASS` in
  `resources/credentials.py`.

## Quirks
- OV-GM Business-Unit-gated: grid empty until the nav Business Unit dropdown + GO completes.
- Business Unit Name (insert field) MUST equal the nav Business Unit or the inserted row is
  invisible under the filtered navigator scope - same convention as every other OV-GM screen
  converted in this batch.
- OV-GM grids redraw lazily after Save+GO - the T3 keywords wait for the row span to render
  before the first assertion (a documented lesson from the original 2026-06-18 build).
- Distinct from the sibling screen **Contract Area Setup** (CO.2038, a different custom-URL OV
  screen, no navigator) - do not confuse the two when searching by "contract area".
- **Branch-name collision, PR #542 vs PR #546 (sibling "Contract" conversion):** both agents were
  independently assigned the branch name `feature/contract-area-pattern-conversion`; PR #546's
  push silently appended its Contract commit on top of this screen's commit on the shared
  branch/PR. Resolved before merge (PR #546 disclosed it; the reviewer confirmed the branch was
  back to its clean single Contract Area commit `1b0c874` before merging PR #542) - see
  `screens/Configuration/Assets/Contract_Objects/Contract_Area/JOURNAL.md` for the full account.
  Contract Area's own conversion content was never at issue.
- DB self-clean checks against `OV_CONTRACT_AREA` must use the generic `CODE` column, not a
  screen-specific `CONTRACT_AREA_CODE` column.
