# Screen: Input List

- **Type:** OV (EC Object Configuration, date-effective) - Bank-family (`manage_object_nav`); plain (optional dropdowns only, none mandatory)
- **BF_CODE:** CD.0035 - **Treeview:** Configuration > Assets > Revenue_Lists > Input List _(DB treeview JSON)_
- **DB view:** `OV_STREAM_ITEM_COLLECTION` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-08-25 - EC 14.2.4 - local sandbox - Bank-pattern conversion, live RF 5/5 (TC01-05), dryrun 842/842, DB self-clean 0 residual (fresh oracledb conn)

## Selectors `[fresh scan 2026-07-26]`
| Purpose | Selector |
|---|---|
| Open | search `Input List` -> `label.tv-link` "Input List" |
| Grid | `manage_object_nav_nav:form:T_data` (needs GO to load) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Code*** - **Name*** - **Start Date*** (date) - End Date - optional dropdowns. (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Code` (ro) - **`Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_STREAM_ITEM_COLLECTION`.

## Automation (code in ec-automation)
- **Playwright:** `py/input_list_iud.py` -> 7/7 (update Name). Unchanged by the 2026-08-25 RF conversion.
- **RF:** T3 `pageobjects/Configuration/Assets/Revenue_Lists/input_list_page.resource` (Bank pattern, properties-file-driven, explicit `Find/Clear Input List Row By Filter`) + suite `tests/.../input_list_iud.robot` (5 TCs, per-TC Login/Logout, fixed `AUTOTEST_INPUTLIST`, PURE SCREEN verification only - zero inline DB-verify calls) -> live 5/5 (2026-08-25).
- **Testdata:** `testdata/input_list_{insert,update,form_verify,grid_verify}.properties`.

## Quirks
- Plain OV; no mandatory dropdowns. Generic engine handles appear/absent/pagination.
