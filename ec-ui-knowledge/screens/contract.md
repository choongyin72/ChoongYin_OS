# Screen: Contract

- **Type:** OV-GM (EC Object Configuration, date-effective, versioned) - manage-object groupmodel;
  Business-Unit-GATED (single-dropdown navigator, same shape as Area's/Contract Area's own).
- **BF_CODE:** CO.2016 - **Treeview:** Configuration > Assets > Contract_Objects > Contract
- **DB view:** `OV_CONTRACT` (generic `CODE` column, per `libraries/DbVerify.py` - NOT a
  screen-specific `CONTRACT_CODE` column; also `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-08-27 - EC 14.2.4 - local sandbox - RF dryrun 5/5 PASS + live headless
  5/5 PASS (TC01-TC05, second attempt after 1 transient UI-timing flake), fresh-connection DB
  self-clean 0 residual, `check_bundle_hygiene.py` PASS (backfill re-run of PR #546's Area-pattern
  conversion, merged 2026-08-26; supersedes the 2026-08-02 entry below's original 4-TC build)

## Selectors
| Purpose | Selector |
|---|---|
| Grid | `manageObject:form:T_data` (empty until nav Business Unit + GO) |
| Navigator (single dropdown) | `nav:form:G:0:R:1:C:1:dd` = Business Unit -> GO (`button:form:B`) |
| Delete (End Date field) | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (hardcoded, not
  label-driven - the row packs Start Date C:1 + End Date C:3 with the End Date label at C:2) |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Contract Code*** - **Contract Name*** - Start Date* (date) - **End Date*** (date, **UNUSUAL -
mandatory on Insert**, unlike most OV-GM screens where End Date is optional/delete-only) -
**Contract Year Start*** (**UNUSUAL - extra mandatory field not present on Area/Contract
Area/most other OV-GM screens**) - Contract Template (dropdown, `__FIRST__`) - **Contract Area***
(dropdown, MANDATORY - value `TS5 Contract Area`, must sit under the nav Business Unit's own
scope or the inserted row never lists in the filtered grid). Labels are SCREEN-PREFIXED ("Contract
Code"/"Contract Name"), like Area's "Area Code"/"Area Name" - NOT the generic "Code"/"Name"
Bank/Object List use. (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Contract Code` (ro, guard) - **`Contract Name`** (only field listed in
`testdata/contract_update.properties` - Contract Code is read-only post-insert). Delete:
**`End Date`** = Start Date (zero-length window) -> true delete, row leaves `OV_CONTRACT`.

### Grid columns (confirmed live)
Contract Code / Contract Name / Start Date (End Date excluded from grid-verify - stays blank
until deleted, same convention as every other converted OV-GM screen).

## Navigator values (this environment)
Business Unit = `TS5 BU` (single dropdown, PROVEN explicit value reused as-is from the screen's
own prior driver, NOT first-available and NOT the "TS3 BU" an earlier task brief mistakenly
cited) - driven by `testdata/contract_navigator.properties` via the shared T2
`Apply Navigator From Properties` keyword.

## Automation (code in ec-automation)
- **RF (maintained/live test):** T3
  `pageobjects/Configuration/Assets/Contract_Objects/contract_page.resource` (label-driven,
  2026-08-26 Area-pattern conversion, PR #546) + suite
  `tests/Configuration/Assets/Contract_Objects/contract_iud.robot` (5 TC: Clean State / Insert /
  Update / Find / Delete, per-TC login/logout, fixed test code `AUTOTEST_CONTRACT`).
- **Playwright (historical reference only, NOT maintained):** `py/contract_iud.py` at the repo's
  `ec-automation/py/` root - original 2026-08-02 build (shared engine `ec_object_iud.py` + explicit
  `select_dropdown`, PROVEN values not `apply_ovgm_navigator`), preserved unchanged; no new
  Playwright bundle is built for Area-pattern work (owner decision 2026-08-27, Universal Screen
  Engine replaces this role).
- **Test data:** `testdata/contract_{navigator,insert,update,form_verify,grid_verify}.properties`.
- **Credentials:** dedicated pair `CONTRACT_EC_USER`/`CONTRACT_EC_PASS` in
  `resources/credentials.py`.

## Quirks
- OV-GM Business-Unit-gated: grid empty until the nav Business Unit dropdown + GO completes.
- **End Date mandatory on Insert** and **Contract Year Start mandatory on Insert** are both
  genuinely unusual for this screen - do not assume every OV-GM/Area-shaped screen shares this;
  most leave End Date optional and have no Contract-Year-Start-equivalent field at all.
- Contract Area (insert field) MUST equal `TS5 Contract Area`, sitting under the nav Business
  Unit=TS5 BU scope, or the inserted row is invisible under the filtered navigator scope - same
  convention as every other OV-GM screen converted in this program.
- OV-GM grids redraw lazily after Save+GO - the T3 keywords wait for the row span to render
  before the first assertion.
- Live runs can hit transient `Could not find active page` UI-timing flakes during AJAX-heavy
  navigator/grid redraws (seen 3x during the original PR #546 conversion, once during this
  backfill's evidence capture) - a DB read after a flaky attempt already shows the correct end
  state; this is UI-timing, not a business-logic defect. One retry is sufficient; do not grind.
- Distinct from the sibling screens **Contract Area** (BU-gated, `OV_CONTRACT_AREA`), **Contract
  Capacity**, and **Contract Inventory** - do not confuse when grepping/searching by "contract".
- **Branch-name collision, PR #546 vs PR #542 (sibling "Contract Area" conversion):** both agents
  were independently assigned the branch name `feature/contract-area-pattern-conversion`; this
  Contract's push silently appended its commit on top of Contract Area's commit on the shared
  branch/PR (#542). Contract's own agent self-detected this (unexpected commit history in its
  worktree), self-fixed by cherry-picking its own commit onto a fresh branch off `origin/master`
  (`contract-conversion-fix`) and raised PR #546 clean, but could NOT itself unwind PR #542 (a
  force-push attempt was blocked by the environment's own safety guardrail) - that side needed
  separate, owner-approved intervention. See
  `screens/Configuration/Assets/Contract_Objects/Contract/JOURNAL.md` for the full account.
  Contract's own conversion content was never at issue.
- DB self-clean checks against `OV_CONTRACT` must use the generic `CODE` column, not a
  screen-specific `CONTRACT_CODE` column.
