# Screen: Remote Endpoint Configuration

- **Type:** TV-style inline-editable grid, no navigator (`CLASS_TYPE=OBJECT`/`TIME_SCOPE_CODE=INVARIANT`).
- **BF_CODE:** CO.1082 - **Treeview:** Configuration > Integration Services > Remote Endpoint Configuration
- **DB base table:** `ENDPOINT_CONFIG` (no version table)
- **DB view:** `OV_ENDPOINT_CONFIG` (key `CODE`)
- **Last verified:** 2026-08-03 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS
  (RF 4/4 pass + Playwright 7/7, DB-verified, self-clean, full I-U-D physical delete)

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Remote Endpoint Configuration` -> `label.tv-link` "Remote Endpoint Configuration" |
| Grid | `endpointconfig:form:T_data` (no navigator - loads immediately) |
| Insert | hover `//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]` -> click submenu (already correctly title-cased "Remote Endpoint configuration") |
| Cell ids | `endpointconfig:form:T:{row}:C0_in` (Code) / `C1_in` (Name) / `C2_dd_input` (Remote Type, dropdown) / `C3_in` (Description, optional) |
| Delete | select row (click C0 cell) -> Delete toolbar's own `<li>` -> identically-worded submenu item -> Save |

## Quirks
- **The class's own `class_property_cnfg` LABEL ("Endpoint configuration") does NOT match the live
  menu title ("Remote Endpoint Configuration")** - same class of naming gap as Contact Group Set,
  confirmed via a live menu search before committing to build.
- **Code must be lowercase alphanumeric + hyphens only (a DNS-slug format).** EC rejects this
  project's usual `AUTOTEST_XX_` uppercase-underscore convention with a live validation error:
  *"Invalid Code, must consist of lower case alphanumeric characters or '-', and must start and end
  with an alphanumeric character (e.g. 'my-name', or '123-abc')".* Use `autotest-rec-<timestamp>`
  instead.
- **Every Insert/Update/Delete operation MUST call `Refresh Screen` after `Save`** (matching the
  `Language`/`Constant Standard` T3 exemplars) - omitting it leaves the toolbar's Save button in a
  state that fails to re-enable for the next operation's cell-click, timing out on the next Save
  click. Cost one live RF failure (TC03 Update, 30s timeout) before being added here.
- Insert/Delete toolbar submenu text is already correctly title-cased - no CSS-uppercase illusion,
  no ambiguous Insert/Delete collision (unlike Constant Standard's original blocker).

## Automation (code in ec-automation)
- **Playwright:** `py/remote_endpoint_config_iud.py` (bespoke driver, matches Language exemplar).
- **RF:** T3 `pageobjects/Configuration/Integration_Services/remote_endpoint_config_page.resource`
  + suite `tests/Configuration/Integration_Services/remote_endpoint_config_iud.robot`. Reuses shared
  T1 keywords `Type Cell By Id`/`Select First EC Dropdown Option`/`Save`/`Refresh Screen`.
- **Gate:** `verify_screen.py` -> OVERALL PASS.
