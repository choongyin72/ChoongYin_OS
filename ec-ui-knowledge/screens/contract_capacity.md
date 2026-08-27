# Screen: Contract Capacity

- **Type:** OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel;
  Business-Unit-GATED (SINGLE dropdown navigator, same shape as Area's own - NOT a multi-level
  cascade, despite the original 2026-08-01 note below).
- **BF_CODE:** CO.2044 - **Treeview:** Configuration > Assets > Contract_Objects > Contract Capacity
- **DB view:** `OV_CONTRACT_CAPACITY` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-08-28 - EC 14.2.4 - local sandbox - RF dryrun 5/5 PASS + live headless
  5/5 PASS (TC01-TC05, one retry needed - see Quirks), fresh-connection DB self-clean 0 residual,
  `check_bundle_hygiene.py` PASS, robocop 7 issues (VAR02 x2 + DOC02 x5, parity with Area's own
  baseline) (backfill re-run of PR #535's Area-pattern conversion, merged 2026-08-26)

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Contract Capacity` -> `label.tv-link` "Contract Capacity" |
| Navigator (single dropdown) | `nav:form:G:0:R:1:C:1:dd` = Business Unit -> GO (`button:form:B`) |
| Grid | `manageObject:form:T_data` (empty until nav BU + GO) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |
| Delete (End Date field) | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (hardcoded, not
  label-driven - the row packs Start Date C:1 + End Date C:3 with the End Date label at C:2) |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Contract Capacity Code*** - **Contract Capacity Name*** - **Start Date*** (date) + dropdowns
Contract Name=`TS5 Shipper B Firm`, Location Name=`TS5 Domestic Gas Storage`. (`*` mandatory)
Both dropdown values must resolve under the SAME Business Unit scope as the navigator or the
inserted row is invisible in the filtered grid (OV-GM constraint).

### Update (`updateAttributes`) / Delete (`objectdates`)
`Contract Capacity Code` (ro, guard) - **`Contract Capacity Name`**. Delete: **`End Date`** =
Start Date (zero-length window) -> true delete, row leaves `OV_CONTRACT_CAPACITY`.

## Navigator value (this environment)
Business Unit = `TS5 BU` - PROVEN live by the screen's own pre-existing Playwright driver
(`py/contract_capacity_iud.py`, shipped 2026-08-01, live 8/8) - carried forward unchanged into
the Area-pattern RF conversion, not re-derived. Fill goes through the shared T2
`Apply Navigator From Properties`, driven by `testdata/contract_capacity_navigator.properties`.

## Automation (code in ec-automation)
- **RF (maintained/live test):** T3
  `pageobjects/Configuration/Assets/Contract_Objects/contract_capacity_page.resource`
  (label-driven, properties-file-driven, 2026-08-26 Area-pattern conversion, PR #535) + suite
  `tests/Configuration/Assets/Contract_Objects/contract_capacity_iud.robot` (5 TC: Clean State /
  Insert / Update / Find / Delete, per-TC login/logout, fixed test code
  `AUTOTEST_CONTRACT_CAPACITY`, zero inline DB-verify calls - pure screen verification).
- **Playwright (historical reference only, NOT maintained):** `py/contract_capacity_iud.py` -
  original 2026-08-01 build (shared engine `ec_object_iud.py` + explicit `select_dropdown`),
  preserved unchanged; no new Playwright bundle is built for Area-pattern work (owner decision
  2026-08-27, Universal Screen Engine replaces this role).
- **Test data:** `testdata/contract_capacity_{navigator,insert,update,form_verify,grid_verify}.properties`.
- **Credentials:** dedicated pair `CONTRACT_CAPACITY_EC_USER`/`CONTRACT_CAPACITY_EC_PASS` in
  `resources/credentials.py`.

## Quirks
- OV-GM Business-Unit-gated: grid empty until the nav Business Unit dropdown + GO completes.
- Contract Name/Location Name (insert fields) MUST equal values that resolve under the nav
  Business Unit or the inserted row is invisible under the filtered navigator scope.
- OV-GM grids redraw lazily after Save+GO - a documented lesson from the original 2026-08-01
  build. Reproduced live during the 2026-08-28 doc-backfill evidence capture: the first live run's
  TC05 (Delete) saw the deleted row still rendered ("1 != 0") immediately after the delete+GO
  refresh; a re-run passed 5/5 clean, and TC01's own clean-state check on that re-run confirmed no
  real DB residual was left behind - i.e. a screen-render lag, not a data/DB defect. One retry
  resolved it (see `screens/Configuration/Assets/Contract_Objects/Contract_Capacity/JOURNAL.md`).
- Distinct from the SINGLE-dropdown navigator note above vs the ORIGINAL 2026-08-01 KB entry,
  which described the navigator as a multi-level "cascade" (`nav:form:G:0:R:1:C:1..N:dd`) copied
  from a generic OV-GM template. The actual live selector (confirmed via the page-object's own
  Variables section, both 2026-08-01 and 2026-08-26) is the single fixed id
  `nav:form:G:0:R:1:C:1:dd` for Business Unit only - corrected in this refresh.
- `verify_screen.py`'s auto-generated `VERIFY-REPORT.md` in the bundle reflects the ORIGINAL
  2026-08-01/4-TC gate shape (robocop 0, dryrun 4/4, RF 4/4 + Playwright 8/8) and was NOT
  regenerated at the 2026-08-26 RF conversion (PR #535 only updated RF/testdata/registry rows).
  Current 5-TC evidence lives in the bundle's `JOURNAL.md` and `evidence/backfill_2026-08-28/`.
