# Screen: Data Extract Setup

- **Type:** OV (EC Object Configuration, date-effective) - Bank-family (`manage_object_nav`); plain (mandatory extra beyond Code/Name/Start Date: Data Extract Type (dropdown))
- **BF_CODE:** SP.0043 - **Treeview:** Configuration > Assets > Data_Mapping_Objects > Data Extract Setup _(DB treeview JSON)_
- **DB view:** `OV_SUMMARY_SETUP` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`); Data Extract Type maps to `SUMMARY_SETUP_VERSION.SUMMARY_TYPE` (distinct values `ACTUAL`/`FORECAST`, confirmed live 2026-08-25)
- **Last verified:** 2026-08-25 - EC 14.2.4 - local sandbox - rebuilt to FULL Bank-pattern, live RF 5/5, DB-verified, self-clean (fresh oracledb re-read = 0 residual `AUTOTEST%` rows in `OV_SUMMARY_SETUP`)

## Selectors `[fresh scan 2026-07-26]`
| Purpose | Selector |
|---|---|
| Open | search `Data Extract Setup` -> `label.tv-link` "Data Extract Setup" |
| Grid | `manage_object_nav_nav:form:T_data` (needs GO to load) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Data Extract Setup Code*** - **Data Extract Setup Name*** - **Start Date*** (date) - End Date - optional dropdowns. (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Data Extract Setup Code` (ro) - **`Data Extract Setup Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_SUMMARY_SETUP`.

## Automation (code in ec-automation)
- **Playwright:** `py/data_extract_setup_iud.py` -> 7/7 (update Name, unchanged).
- **RF:** T3 `pageobjects/Configuration/Assets/Data_Mapping_Objects/data_extract_setup_page.resource` - rebuilt 2026-08-25 to mirror `bank_page.resource`/`state_page.resource`/`data_extract_set_page.resource` exactly: properties-file-driven Insert/Update (`testdata/data_extract_setup_{insert,update,form_verify,grid_verify}.properties`), explicit `Find/Clear Data Extract Setup Row By Filter` grid-filter wiring, fixed test code `AUTOTEST_DXS`, dedicated `DATA_EXTRACT_SETUP_EC_USER/PASS` credential pair, per-TC Login/Logout, PURE SCREEN verification only (the old suite's inline `Field Should Equal In View` DB-verify call directly in the .robot file was removed). Suite `tests/.../data_extract_setup_iud.robot` -> live 5/5 (was 4/4, now includes a TC04 Find test case matching Bank's 5-TC shape).
- **Gate:** robocop parity with `data_extract_set_iud.robot` exemplar (5 DOC02 + 4 VAR02 baseline, 0 extra), full-tree dryrun 842/842, live 5/5, DB self-clean (fresh oracledb re-read = 0 residual `AUTOTEST%` rows).

## Quirks
- Plain OV; mandatory extra beyond Code/Name/Start Date: Data Extract Type (dropdown), value `Actual` maps to DB `SUMMARY_TYPE`/`SUMMARY_SETUP_VERSION.SUMMARY_TYPE` = `ACTUAL`. Generic engine handles appear/absent/pagination.
- Labels are SCREEN-PREFIXED ("Data Extract Setup Code"/"Data Extract Setup Name"), NOT the generic "Code"/"Name" some Bank-family screens (e.g. Data Extract Set, Bank) use - confirmed via the New Object form screenshot and live recon 2026-08-25 (matches State's own screen-prefixed "State Code"/"State Name" precedent, not a universal convention).
