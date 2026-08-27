# Screen: Storage Flow

- **Type:** OV (EC Object Configuration, date-effective) - **FULL Bank pattern** (`manage_object_nav`);
  label-driven, properties-file-driven, T2-consolidated, explicit grid-filter wiring. No mandatory
  navigator dropdown (universal Date + GO bar only) - but the Insert form DOES have mandatory
  dropdowns (see below), correcting the earlier "none mandatory" note.
- **BF_CODE:** CO.2091 - **Treeview:** Configuration > Assets > Tank_and_Storage_Objects > Storage Flow _(DB treeview JSON)_
- **DB view:** `OV_STORAGE_FLOW` (versioned; key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-08-28 - EC 14.2.4 - local sandbox - live dryrun 5/5 + live headless 5/5
  (on retry, see Quirks) + DB self-clean 0 residual via fresh `oracledb` connection

## Selectors `[from storage_flow_page.resource Variables section, 2026-08-23 Batch 10 build]`
| Purpose | Selector |
|---|---|
| Open | search `Storage Flow` -> `label.tv-link` "Storage Flow" |
| Grid | `${STORAGE_FLOW_TABLE}` = shared T2 `${OV_MANAGE_OBJECT_TABLE}` = `manage_object_nav_nav:form:T_data` (needs GO to load) |
| Grid filter | `Find/Clear Storage Flow Row By Filter` -> T2 `Find/Clear Object Row By Filter` on `${STORAGE_FLOW_TABLE}` (filters the Code column) |
| Delete field id | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (End Date, objectdates form) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL, zero hardcoded ids)
**Storage Flow Code*** - **Storage Flow Name*** - **Start Date*** (date) - End Date -
**Flow Direction*** (dropdown, `__FIRST__`) - **Storage*** (dropdown, `__FIRST__`). (`*` mandatory)

Mandatory-yellow fields confirmed via the screen's own already-proven page object/Playwright
driver (`py/storage_flow_iud.py` `INSERT_FIELDS`), per the Batch-9 Process Train lesson: a static
CSS mandatory-field scan alone can miss a de-facto-mandatory dropdown.

### Update (`updateAttributes`) / Delete (`objectdates`)
`Storage Flow Code` (ro) - **`Storage Flow Name`** (only field updatable here). Delete:
**`End Date`** = Start Date -> leaves `OV_STORAGE_FLOW`.

## Test data (properties files, `testdata/storage_flow_*.properties`)
- `_insert.properties`: `Storage Flow Code=AUTOTEST_STFLOW`, `Storage Flow Name=AUTOTEST Storage
  Flow`, `Start Date=2000-01-01`, `Flow Direction=__FIRST__`, `Storage=__FIRST__`
- `_update.properties`: `Storage Flow Name=AUTOTEST Storage Flow UPDATED`
- `_form_verify.properties` / `_grid_verify.properties`: post-update Code/Name (+ Start Date for
  grid) - `Flow Direction`/`Storage` deliberately excluded from round-trip checks (their rendered
  option label after `__FIRST__` resolution is not knowable ahead of time)

## Automation (code in ec-automation)
- **Playwright:** `py/storage_flow_iud.py` (2026-07-26 build, unchanged by the Batch 10 conversion)
  -> 7/7 (update Name); used as the source of truth for the mandatory Flow Direction/Storage
  dropdowns during the conversion.
- **RF:** T3 `pageobjects/Configuration/Assets/Tank_and_Storage_Objects/storage_flow_page.resource`
  (label-driven, properties-file-driven, T2-consolidated, grid-filter wired) + suite
  `tests/.../storage_flow_iud.robot` (5-TC, fixed `AUTOTEST_STFLOW` code, per-TC Login/Logout) ->
  live 5/5 (2026-08-28 re-verification, on retry - see Quirks).
- Dedicated credentials `STORAGE_FLOW_EC_USER`/`STORAGE_FLOW_EC_PASS` in `resources/credentials.py`.

## Quirks
- Insert form has TWO mandatory dropdowns (`Flow Direction`/`Storage`), not zero - the original
  2026-07-26 KB entry said "no mandatory dropdowns," which was superseded by the Batch 10
  conversion's more careful mandatory-field check against the proven driver.
- `Flow Direction`/`Storage` use `__FIRST__` and are excluded from the round-trip form-label
  compare (resolved reference values can re-render as different display text after reload).
- Live re-run 2026-08-28 hit a one-off `TC01` login-page-load timeout (60s waiting for the menu
  search box) on the first attempt; TC02-05 (the real IUD cycle) passed that same attempt; a
  single retry came back clean 5/5. Non-reproducible; not chased further.
- Delete via `objectdates` End Date = Start Date; grid redraw after delete is async (matches
  Bank/Berth/State/Storage sibling screens in this same folder).
