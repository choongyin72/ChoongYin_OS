# Screen: HCB System

- **Type:** OV (EC Object Configuration, date-effective) - Bank-family (`manage_object_nav`); has a mandatory dropdown (see correction below)
- **BF_CODE:** CD.0097 - **Treeview:** Configuration > Assets > Revenue Lists > HCB System _(DB treeview JSON)_
- **DB view:** `OV_BALANCE` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`, `BALANCE_CATEGORY`)
- **Last verified:** 2026-08-25 - EC 14.2.4 - local sandbox - RF 5/5 live, dryrun 842/842, DB self-clean (fresh connection)

## CORRECTION (2026-08-25)
The prior version of this note claimed "optional dropdowns only, none mandatory". A live
MandatoryCellStyle scan of `objectForm` (2026-08-25, headless Playwright recon) found this is
WRONG: **`HCB Category` is mandatory**, alongside Code/Name/Start Date. Options (live
dropdown-panel scan): `Operating area system` / `Single field system` / `Plant / terminal
system`. It is also present in `updateAttributes` (confirmed on the existing `RHEA_WETGFAS`
record: R7). Do not trust the "no mandatory dropdown" claim on any other note without a live
re-scan - this is exactly the doc-vs-reality mismatch this project has repeatedly found.

## Selectors `[fresh scan 2026-08-25]`
| Purpose | Selector |
|---|---|
| Open | search `HCB System` -> `label.tv-link` "HCB System" |
| Grid | `manage_object_nav_nav:form:T_data` (needs GO to load); headers = Code/Name/Start Date/End Date |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Code*** - **Name*** - **Start Date*** (date) - End Date - Description - Comments - Mass UOM
(dropdown) - Volume UOM (dropdown) - Energy UOM (dropdown) - **HCB Category*** (dropdown).
(`*` mandatory - live MandatoryCellStyle scan 2026-08-25)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Code` (ro) - **`Name`** - Description - Comments - Mass/Volume/Energy UOM (dropdown) -
**`HCB Category`** (dropdown, present here too). Delete: **`End Date`** = Start Date (label-driven
fill on `objectdates`) -> leaves `OV_BALANCE`.

## Automation (code in ec-automation)
- **Playwright:** `py/hcb_system_iud.py` -> 7/7 (update Name). Unchanged by the 2026-08-25 conversion.
- **RF (Bank-pattern conversion, 2026-08-25):** T3
  `pageobjects/Configuration/Assets/Revenue_Lists/hcb_system_page.resource` - label-driven,
  **properties-file-driven** (`testdata/hcb_system_insert.properties`,
  `hcb_system_update.properties`, `hcb_system_grid_verify.properties`,
  `hcb_system_form_verify.properties`), explicit `Find/Clear HCB System Row By Filter` grid-filter
  wiring, fixed test code `AUTOTEST_HCB`, per-TC Login/Logout, PURE SCREEN verification only (no
  inline DB-verify keyword calls in the .robot file - removed `Field Should Equal In View`/
  `*Should Exist/Not Exist In DB` that the prior driver called directly, matching Bank's
  owner-requested 2026-08-18 convention). Suite `tests/.../hcb_system_iud.robot` -> live 5/5
  (TC01-05: clean-state/insert/update/find/delete).
- Dryrun 842/842 full-tree. DB self-clean confirmed via fresh oracledb connection (0 residual
  `AUTOTEST_HCB` rows in `OV_BALANCE`).

## Quirks
- HAS a mandatory dropdown (`HCB Category`) - do not treat as fully-plain OV. Generic engine
  handles appear/absent/pagination for the rest.
- Existing real record `RHEA_WETGFAS` (`BALANCE_CATEGORY='FIELD'` in DB) - never touched by tests.
