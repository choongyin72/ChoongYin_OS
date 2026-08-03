# SOW - Remote Endpoint Configuration (CO.1082)

## 1. Screen identity
- **BF Code:** CO.1082
- **Treeview path:** Configuration > Integration Services > Remote Endpoint Configuration
- **Type:** TV-style inline-editable grid, no navigator (`CLASS_TYPE=OBJECT`, `TIME_SCOPE_CODE=INVARIANT`).
- **DB base table:** `ENDPOINT_CONFIG` (no version table).
- **DB view:** `OV_ENDPOINT_CONFIG`.
- Discovered via a DB-first coverage audit (`CLASS_CNFG` where `CLASS_TYPE='OBJECT'`) cross-referenced
  against every tracking doc; the class's own `class_property_cnfg` LABEL ("Endpoint configuration")
  differs from the live menu title ("Remote Endpoint Configuration") - confirmed via a live menu
  search before committing to build.

## 2. Insert / Update / Delete
Hover the Insert toolbar icon's own `<li>` -> click "Remote Endpoint configuration" (already
correctly title-cased, no CSS-uppercase illusion) -> a blank row appears. Columns: Code (C0,
mandatory), Name (C1, mandatory), Remote Type (C2, dropdown), Description (C3, optional). Delete is
physical (this class is `TIME_SCOPE_CODE=INVARIANT`) - select the row, Delete toolbar's own
identically-worded submenu item, Save.

## 3. Critical gotcha: Code format
Code must be **lowercase alphanumeric with hyphens only** (a DNS-slug format) - EC rejects this
project's usual `AUTOTEST_XX_` uppercase-underscore convention with a live validation error:
*"Invalid Code, must consist of lower case alphanumeric characters or '-', and must start and end
with an alphanumeric character (e.g. 'my-name', or '123-abc')".* Uses `autotest-rec-<timestamp>`
instead.

## 4. Refresh Screen gotcha
Every Insert/Update/Delete operation must call `Refresh Screen` immediately after `Save`, matching
the proven `Language`/`Constant Standard` T3 pattern - omitting it leaves the toolbar's Save button
in a state that fails to re-enable for the next operation's cell-click, timing out on the next Save
click. Cost one live RF failure (TC03 Update, 30s Save-button timeout) before being added.
