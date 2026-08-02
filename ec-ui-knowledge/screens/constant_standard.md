# Screen: Constant Standard

- **Type:** TV-style inline-editable grid (`cstandard:form:T_data`), but `CLASS_TYPE=OBJECT`/
  `TIME_SCOPE_CODE=VERSIONED` per `class_cnfg` - date-effective underneath the TV-looking grid.
- **BF_CODE:** CO.0102 - **Treeview:** Configuration > Assets > Hydrocarbon Objects > Constant Standard
- **DB view:** `OV_CONSTANT_STANDARD` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-08-02 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF 4/4 pass + Playwright 7/7, DB-verified, self-clean)

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Constant Standard` -> `label.tv-link` "Constant Standard" |
| Grid | `cstandard:form:T_data` (no navigator - loads immediately) |
| Insert | hover `//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]` -> click `.../a[normalize-space(.)='Constant Standard']` (see Quirks) |
| Blank row lookup | `Find Constant Standard Row By Code` with `${EMPTY}` code (matches C0_in with value `''`) |
| Cell ids | `cstandard:form:T:{row}:C0_in` (Code) / `C1_in` (Name) / `C2_da_input` (Start Date) / `C3_da_input` (End Date) / `C4_da_input` (Daytime) / `C5_in` (Description) / `C6_in` (Reference Pressure) / `C7_cb` (Editable) |
| Save / Refresh | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `//a[@title='Refresh [Ctrl+r]']` |

## Quirks (the whole reason this screen took 3 park attempts to crack)
- **The Insert menu item's VISIBLE text ("CONSTANT STANDARD", all caps) is NOT its real DOM text.**
  The actual text is `"Constant Standard"` (title case) - the all-caps rendering is pure CSS
  `text-transform`. Every case-sensitive text search for the all-caps string silently fails to
  match, which looks exactly like "this isn't a real clickable item, just a tooltip." Always
  inspect the real `onclick`/text via `page.evaluate`/`outerHTML`, never trust a screenshot's
  rendered casing.
- **Both the Insert AND Delete toolbar icons have a submenu item with the IDENTICAL text**
  ("Constant Standard"). A global `//a[text()='Constant Standard']` search will match whichever one
  happens to be first in the DOM (usually the wrong, disabled one) - always scope the xpath to the
  specific icon's own `<li class="ui-menu-parent">` ancestor (`[.//span[contains(@class,'ui-icon-
  insert')]]` vs `ui-icon-delete`). This project's own `resources/table_class.resource` already
  documents this exact pattern ("the Delete submenu often has an identically named item") - consult
  it before re-discovering the gap.
- **"Daytime" (C4) is a genuinely separate mandatory field on Insert**, not derived from Start Date
  (C2) despite looking related - Save rejects the insert without it.
- **Delete is End Date = Start Date in the inline C3 cell, NOT the toolbar Delete button.** This
  class is date-effective (`VERSIONED`) despite the TV-looking grid; the toolbar Delete icon was
  never fully wired up in this bundle since the simpler End=Start path (identical to the standard OV
  close gesture) was confirmed working first.
- **Every Insert/Update/Delete operation MUST call `Refresh Screen` after `Save`** (matching the
  `Language` T3 exemplar exactly) - omitting it leaves the toolbar's Save button in a state that
  fails to re-enable for the next operation's cell edit, timing out on the next Save click.

## Automation (code in ec-automation)
- **Playwright:** `py/constant_standard_iud.py` (bespoke driver - does NOT use the OV-GM generator, since this pattern doesn't fit it).
- **RF:** T3 `pageobjects/Configuration/Assets/Hydrocarbon_Objects/constant_standard_page.resource` + suite `tests/Configuration/Assets/Hydrocarbon_Objects/constant_standard_iud.robot`. Reuses shared T1 keywords `Type Cell By Id`/`Get Cell Value By Id`/`Save`/`Refresh Screen`.
- **Gate:** `verify_screen.py` -> OVERALL PASS.
