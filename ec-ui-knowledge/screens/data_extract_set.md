# Screen: Data Extract Set

- **Type:** OV (EC Object Configuration, date-effective) - Bank family (`manage_object_nav`), plain
  manage-object, no navigator cascade. Rebuilt to the FULL Bank-pattern shape (properties-file-driven
  + explicit grid-filter wiring) via PR #474 (2026-08-23, Batch 10).
- **BF_CODE:** SP.0049 - **Treeview:** Configuration > Assets > Data_Mapping_Objects > Data Extract Set
  _(DB treeview JSON)_
- **DB view:** `OV_SUMMARY_SET` (versioned; key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-08-28 (this backfill) - EC 14.2.4 - local sandbox - live RF 5/5
  (`data_extract_set_iud.robot`), dryrun 5/5, robocop 9 issues (5 DOC02 + 4 VAR02, quality-suggestions
  only, unchanged from PR #474), hygiene PASS, DB self-clean 0 residual via fresh connection.

## Selectors `[from PR #474 + fresh re-run 2026-08-28]`
| Purpose | Selector |
|---|---|
| Open | search `Data Extract Set` -> `label.tv-link` "Data Extract Set" |
| Grid | `manage_object_nav_nav:form:T_data` (= `${OV_MANAGE_OBJECT_TABLE}`, needs GO to load) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |
| Delete End Date field | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (not label-scannable per-row) |
| Grid filter | shared T2 `Find/Clear Object Row By Filter` on the Code column - explicitly wired
  into Update/Find/Verify-Found/Delete (2026-08-22 standardisation, same as Bank/Berth/Account) |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL, driven by
`testdata/data_extract_set_insert.properties`)
**Code*** - **Name*** - **Start Date*** (date) - **Owner Class*** (dropdown, value `All`).
(`*` mandatory - Owner Class corrected 2026-08-23; the original 2026-07-26 note calling it an
"optional dropdown, skipped" was WRONG.)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Code` (read-only) - **`Name`** (only field in `data_extract_set_update.properties`; Owner Class is
Insert-only, not present here). Delete: **`End Date`** = Start Date -> row leaves `OV_SUMMARY_SET`.

## Automation (code in ec-automation)
- **RF:** T3 `pageobjects/Configuration/Assets/Data_Mapping_Objects/data_extract_set_page.resource`
  (label-driven, properties-file-driven, grid-filter-wired) + suite
  `tests/Configuration/Assets/Data_Mapping_Objects/data_extract_set_iud.robot` - 5 TCs
  (clean-state/insert/update/find/delete), per-TC Login/Logout, fixed test code `AUTOTEST_DXT` -> live
  5/5 (re-confirmed 2026-08-28).
- **Playwright:** `py/data_extract_set_iud.py` -> 7/7 (pre-existing, unchanged since PR #474; owner
  decision 2026-08-27 waives new Playwright-bundle work going forward in favour of the Universal
  Screen Engine).
- **Testdata:** `testdata/data_extract_set_{insert,update,form_verify,grid_verify}.properties`.

## Quirks
- Plain OV, no navigator - single Date+GO nav to load the grid.
- Owner Class is mandatory at Insert but absent from Update - same "Insert-only field" pattern as
  Bank/Berth's own Insert-only Start Date exclusion from their update properties.
- Fixed test code `AUTOTEST_DXT` (not timestamp-suffixed) - EC never lets a deleted code be reused, so
  every run MUST complete TC05 (delete) to free the code for the next run.
- Sibling screen `Data Extract Setup` (SP.0043, `ec-ui-knowledge/screens/data_extract_setup.md`) is a
  DIFFERENT screen with its own bundle - do not conflate the two.
