# Screen: Contract Inventory

- **Type:** OV-GM (EC Object Configuration, date-effective, versioned) - manage-object groupmodel;
  navigator-GATED (single group `G:0`, single row `R:1`, increasing-column shape, same as
  Area's/Facility Class 1's own).
- **BF_CODE:** CO.2054 - **Treeview:** Configuration > Assets > Contract_Objects > Contract Inventory
- **DB view:** `OV_CONTRACT_INVENTORY` (generic `CODE` column per `libraries/DbVerify.py`; also
  `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-08-28 - EC 14.2.4 - local sandbox - RF dryrun 5/5 PASS + live headless
  5/5 PASS (TC01-TC05, first attempt, no retry needed), fresh-connection DB self-clean 0 residual
  before+after, `check_bundle_hygiene.py` PASS (backfill re-run of PR #556's Area-pattern
  conversion, merged 2026-08-26; supersedes the 2026-08-02 entry below's original 4-TC build)

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Contract Inventory` -> `label.tv-link` "Contract Inventory" |
| Grid | `manageObject:form:T_data` (empty until navigator + GO) |
| Navigator | single group `G:0`, single row `R:1`, increasing column: `C:1` Business Unit
  (`nav:form:G:0:R:1:C:1:dd`, genuinely mandatory-yellow+empty) -> `C:2` Contract Area
  (`nav:form:G:0:R:1:C:2:dd`, stays optional/white even after `C:1` is filled) -> GO
  (`#button:form:B`) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |
| Delete (End Date field) | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (hardcoded, not
  label-driven - the row packs Start Date `C:1` + End Date `C:3` with the End Date label at `C:2`) |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Contract Inventory Code*** - **Contract Inventory Name*** - Start Date* (date, lives in
`objectdates`, not `objectForm`) + a fixed "Contract name" dropdown = `TS5 Shipper C` (carried
over unchanged from the pre-conversion Playwright driver). Labels are SCREEN-PREFIXED ("Contract
Inventory Code"/"Contract Inventory Name"), like Area's "Area Code"/"Area Name" - NOT the generic
"Code"/"Name" Bank/Object List use. No "Business Unit"/"Contract Area" field exists on
`objectForm` - confirmed live, so there is no field-reuse conflict with the navigator. (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Contract Inventory Code` (ro, guard) - **`Contract Inventory Name`** (only field listed in
`testdata/contract_inventory_update.properties`). Delete: **`End Date`** = Start Date (zero-length
window) -> true delete, row leaves `OV_CONTRACT_INVENTORY`.

### Grid columns (confirmed live)
Contract Inventory Code / Contract Inventory Name / Start Date / End Date - same 4-column shape
as Area/Facility Class 1.

## Navigator values (this environment)
Business Unit = the only genuinely mandatory dropdown (live mandatory-yellow DOM check,
2026-08-26). Contract Area is still filled in `testdata/contract_inventory_navigator.properties`
for behavioral parity with the already-proven prior driver scope, not because it is strictly
required - filling Business Unit does NOT turn Contract Area's background yellow. Fill delegates
to the shared T2 `Apply Navigator From Properties` keyword, with ZERO shared-file changes needed
for this same-row/increasing-column shape.

## Automation (code in ec-automation)
- **RF (maintained/live test):** T3
  `pageobjects/Configuration/Assets/Contract_Objects/contract_inventory_page.resource`
  (label-driven, 2026-08-26 Area-pattern conversion, PR #556) + suite
  `tests/Configuration/Assets/Contract_Objects/contract_inventory_iud.robot` (5 TC: Clean State /
  Insert / Update / Find / Delete, per-TC login/logout, fixed test code
  `AUTOTEST_CONTRACT_INVENTORY`).
- **Playwright (historical reference only, NOT maintained):** `py/contract_inventory_iud.py` at
  the repo's `ec-automation/py/` root - original 2026-08-02 build (shared engine
  `ec_object_iud.py` + explicit `select_dropdown`, PROVEN values not `apply_ovgm_navigator`),
  preserved unchanged; no new Playwright bundle is built for Area-pattern work (owner decision
  2026-08-27, Universal Screen Engine replaces this role).
- **Test data:** `testdata/contract_inventory_{navigator,insert,update,form_verify,grid_verify}.properties`.
- **Credentials:** dedicated pair `CONTRACT_INVENTORY_EC_USER`/`CONTRACT_INVENTORY_EC_PASS` in
  `resources/credentials.py`.

## Quirks
- OV-GM navigator-gated: grid empty until the navigator's Business Unit dropdown + GO completes.
- The navigator's real mandatory-yellow shape needed a live DOM re-check before PR #556's
  conversion - the pre-existing registry note read as a genuine 2-level "Business Unit -> Contract
  Area" mandatory cascade, but only Business Unit actually gates the grid. Don't assume a
  same-looking prior note is still accurate without a live re-check.
- Delete `objectdates` End Date field id is hardcoded, not label-driven, same rationale as every
  other OV-GM screen with a packed Start/End Date row.
- OV-GM grids redraw lazily after Save+GO - the T3 keywords wait for the row span to render before
  the first assertion.
- Distinct from the sibling screens **Contract** (`OV_CONTRACT`, Business-Unit single-dropdown
  navigator), **Contract Area** (`OV_CONTRACT_AREA`), and **Contract Capacity** - do not confuse
  when grepping/searching by "contract".
- **A "detached-HEAD collision-recovery" story was checked for this screen's own PR (#556) during
  the 2026-08-28 backfill and NOT found** in the PR body, commit message, or branch reflog. The
  real, disclosed git/branch collision from this batch belongs to the SIBLING screen **Contract**
  (CO.2016, PR #546 vs PR #542) - see `screens/Configuration/Assets/Contract_Objects/Contract/
  JOURNAL.md`. What PR #556's own reviewer DID disclose was a `credentials.py` hunk carrying four
  screens' credential pairs from a shared working state (Contract Inventory's own plus
  Pilot/Pipeline Segment/Property's) - confirmed clean at merge (exactly one pair per screen), but
  flagged as the same shared-checkout hazard class.
- DB self-clean checks against `OV_CONTRACT_INVENTORY` must use the generic `CODE` column, not a
  screen-specific column.
