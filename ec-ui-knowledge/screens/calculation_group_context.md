# Screen: Calculation Group Context

- **Type:** OV (EC Object Configuration, date-effective) - **full Bank-pattern** (`manage_object_nav`);
  properties-file-driven Insert/Update/Verify + explicit grid-filter wiring since PR #455 (batch 7,
  2026-08-23); no mandatory navigator dropdowns (optional dropdowns only)
- **BF_CODE:** CO.0245 - **Treeview:** Configuration > Assets > Calculation_Objects > Calculation Group
  Context _(DB treeview JSON)_
- **DB view:** `OV_CALC_GRP_CONTEXT` (versioned; key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Grid id:** `manage_object_nav_nav:form:T_data` (shared T2 constant `${OV_MANAGE_OBJECT_TABLE}`, threaded
  through the T3 as `${CALCULATION_GROUP_CONTEXT_TABLE}`)
- **Last verified:** 2026-08-28 - EC 14.2.4 - local sandbox - dryrun 5/5 PASS, live 5/5 PASS, DB self-clean
  0 residual (fresh oracledb connection), hygiene PASS (backfill re-run; original PR #455 conversion merged
  2026-08-23, original build 2026-07-26)

## Selectors `[from _page.resource Variables section + fresh 2026-08-28 re-run]`
| Purpose | Selector / keyword |
|---|---|
| Open | search `Calculation Group Context` -> `label.tv-link` "Calculation Group Context" |
| Grid | `manage_object_nav_nav:form:T_data` (needs GO to load - `Open EC Screen` + `Apply Navigator`) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |
| Grid filter (Code column) | `Find Calculation Group Context Row By Filter` -> shared T2 `Find Object Row By Filter` on `${CALCULATION_GROUP_CONTEXT_TABLE}`; cleared via `Clear Calculation Group Context Row Filter` -> `Clear Object Row Filter` |
| Insert (properties-driven) | `Insert Calculation Group Context Record And Save` -> `Insert Object From Properties And Verify Code` using `testdata/calculation_group_context_insert.properties` |
| Update (properties-driven) | `Update Calculation Group Context Record And Save` -> `Update Object From Properties` using `testdata/calculation_group_context_update.properties` |
| Delete | `Delete Calculation Group Context Record And Save` -> `Select Object Row` + `Fill OV Date By Label objectdates "End Date"` + `Save` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL, NO hardcoded field ids)
- **Mandatory (yellow when empty):** `Calculation Group Context Code`, `Calculation Group Context Name`,
  `Start Date` (date).
- **Optional:** `Calculation Group Object Class`, `Calculation Group List Class` (dropdowns, filled
  `__FIRST__` via properties - not mandatory), `End Date`.
- **Important:** the Code label is NOT the generic "Code" used by Bank - it is the full "Calculation Group
  Context Code" string. Every T2 helper call must pass
  `code_label=${CALCULATION_GROUP_CONTEXT_CODE_LABEL}` explicitly.

### Update (`updateAttributes`) / Delete (`objectdates`)
`Calculation Group Context Code` (read-only) - **`Calculation Group Context Name`** (editable, DB-verified
via `Field Should Equal In View OV_CALC_GRP_CONTEXT`). Delete: **`End Date`** = Start Date -> row leaves
`OV_CALC_GRP_CONTEXT`.

## Test data / credentials
- Fixed test code `AUTOTEST_CGC_BANK` (matches Bank's own fixed-code convention, since PR #455 - the
  original 2026-07-26 build used a generated-unique `AUTOTEST_CGC_<timestamp>` code instead). Every run must
  complete TC05 (delete) to free the code for the next run.
- Dedicated credentials `CALCULATION_GROUP_CONTEXT_EC_USER` / `CALCULATION_GROUP_CONTEXT_EC_PASS` in
  `resources/credentials.py`.
- Driven by `testdata/calculation_group_context_{insert,update,form_verify,grid_verify}.properties`.

## Automation (code in ec-automation)
- **Playwright (pre-existing, NOT rebuilt or touched by the PR #455 conversion or this backfill - item 4/5
  permanently waived for Bank-pattern conversions, Section H):** `py/calculation_group_context_iud.py` ->
  7/7 (update Name).
- **RF T3:** `pageobjects/Configuration/Assets/Calculation_Objects/calculation_group_context_page.resource`
  - label-driven field resolution (kept from the 2026-07-26 build) + properties-file-driven insert/update/
  verify + explicit grid-filter wiring (added by PR #455).
- **RF suite:** `tests/Configuration/Assets/Calculation_Objects/calculation_group_context_iud.robot` - 5 TCs
  (TC01 clean-state, TC02 insert, TC03 update, TC04 find, TC05 delete), per-TC login/logout, one browser
  opened once in Suite Setup.
- **Gate history:** original build `verify_screen.py` -> OVERALL PASS (4/4 RF + 7/7 Playwright, 2026-07-26).
  PR #455 conversion -> live 5/5, DB self-clean, grid-filter fired (23 `output.xml` hits), dryrun 753/753 on
  the full tree (2026-08-23). This backfill -> dryrun 5/5, live 5/5, robocop 13 DOC02 (matches `bank_iud`
  baseline), hygiene PASS, DB self-clean 0 residual (2026-08-28).

## Quirks
- Plain Bank-layout OV (single Date+GO navigator, no mandatory navigator scope). No mandatory dropdowns;
  the two optional dropdowns are filled `__FIRST__` via properties, never required.
- Code field label is the full "Calculation Group Context Code" string, not the generic "Code" - a
  copy-paste of Bank's own keyword calls without threading this label through will silently fail to
  resolve the field.
- Generic engine handles appear/absent/pagination with zero screen-specific tuning.
