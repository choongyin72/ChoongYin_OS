# Screen: Split Item Other

- **Type:** OV (EC Object Configuration, date-effective) - Bank-family (`manage_object_nav`);
  plain (no mandatory navigator, no mandatory dropdowns).
- **BF_CODE:** CD.0017 - **Treeview:** Configuration > Assets > Revenue_Split_Keys > Split Item
  Other _(DB treeview JSON)_. Class `SPLIT_ITEM_OTHER`.
- **DB view:** `OV_SPLIT_ITEM_OTHER` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **NOT** the same screen as the 6 sibling "* Split Key" screens (Product/Company/Field/Stream
  Item Category/Other/Stream Item Split Key) - those share a DIFFERENT class `SPLIT_KEY` and view
  `OV_SPLIT_KEY` via the `manage_object_split_key` controller. Confirmed by direct file-path/class
  inspection - do not conflate on name similarity alone.
- **Last verified:** 2026-08-28 - EC 14.2.4 - local sandbox - re-ran the existing suite live,
  5/5 pass, DB self-clean 0 residual via a fresh `oracledb` connection. Automation itself last
  changed 2026-08-23 (PR #471, Bank-pattern conversion, Batch 10).

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Split Item Other` -> `label.tv-link` "Split Item Other" |
| Grid | `manage_object_nav_nav:form:T_data` (shared T2 `${OV_MANAGE_OBJECT_TABLE}`; needs GO to load, GO not mandatory) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |
| Grid-filter (Update/Find/Verify-Found/Delete) | `Find/Clear Split Item Other Row By Filter` (T3) -> shared T2 `Find/Clear Object Row By Filter` on `${SPLIT_ITEM_OTHER_TABLE}` |
| Delete field | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (End Date, `objectdates` tab) |

### New Object form (`objectForm`) - mandatory-yellow fields
**Split Item Code*** (screen-prefixed) - **Name*** (GENERIC, NOT screen-prefixed - confirmed via
direct grep) - **Start Date*** (date). End Date + optional dropdowns not mandatory. (`*` =
mandatory-and-empty on a pristine Insert row, per the standard EC yellow-highlight convention.)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Split Item Code` (read-only in this form) - **`Name`** (only editable field in Update; Start
Date lives only in Insert, not in updateAttributes). Delete: **`End Date`** = Start Date -> row
leaves `OV_SPLIT_ITEM_OTHER`.

## Automation (code in ec-automation) - built via `ec-bank-pattern-converter` (PR #471, Batch 10)
- **T3** `pageobjects/Configuration/Assets/Revenue_Split_Keys/split_item_other_page.resource` -
  properties-file-driven insert/update/verify (`Insert Object From Properties And Verify Code`,
  `Update Object From Properties`, `Verify Object Insert Exists`/`Verify Object Form Record`/
  `Verify Object Found`), explicit grid-filter wiring, per-TC login/logout, own credential pair
  `SPLIT_ITEM_OTHER_EC_USER`/`SPLIT_ITEM_OTHER_EC_PASS`.
- **Suite** `tests/Configuration/Assets/Revenue_Split_Keys/split_item_other_iud.robot` - 5 TCs
  (Verify Clean State / Insert / Update / Find / Delete), fixed test code `AUTOTEST_SIO`.
- **Testdata** `testdata/split_item_other_{insert,update,form_verify,grid_verify}.properties`.
- **Playwright driver (pre-existing, unchanged since 2026-07-26):** `py/split_item_other_iud.py`
  -> 7/7 (as of the original build; superseded in priority by the Universal Screen Engine per
  the 2026-08-27 owner decision, not rebuilt for this conversion).
- **Gate (2026-08-23, PR #471):** live 5/5, full-tree dryrun 767/767, filter fired 30x (output.xml
  grep), DB self-clean via fresh connection.
- **Gate (2026-08-28, backfill re-verification):** dryrun 5/5, live 5/5, robocop 9 issues
  (baseline DOC02 style warnings, no regression), hygiene PASS, DB self-clean 0 residual via
  fresh connection.

## Quirks
- Plain OV; navigator (Date + GO) present but not mandatory - no scope value required before the
  grid can be worked with.
- "Name" is a GENERIC label (not screen-prefixed like "Split Item Code") - do not assume every
  field on this screen is screen-prefixed.
- Fixed test code `AUTOTEST_SIO` (not a generated-unique code) - every run must complete TC05
  (delete) so the code stays free for the next run; EC never lets a deleted code be reused if a
  run doesn't clean up after itself.
