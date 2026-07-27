# Screen: Task Process

- **Type:** OV (EC Object Configuration, date-effective) - Bank-family (`manage_object_nav`); plain (optional dropdowns only, none mandatory)
- **BF_CODE:** CO.0191 - **Treeview:** Configuration > Task_List > Task Process _(DB treeview JSON)_
- **DB view:** `OV_TASK_PROCESS` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-07-26 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF 4/4 + Playwright 7/7, DB-verified, self-clean)

## Selectors `[fresh scan 2026-07-26]`
| Purpose | Selector |
|---|---|
| Open | search `Task Process` -> `label.tv-link` "Task Process" |
| Grid | `manage_object_nav_nav:form:T_data` (needs GO to load) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Task Process Code*** - **Task Process Name*** - **Start date*** (date) - End date - optional dropdowns. (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Task Process Code` (ro) - **`Task Process Name`**. Delete: **`End date`** = Start Date -> leaves `OV_TASK_PROCESS`.

## Automation (code in ec-automation)
- **Playwright:** `py/task_process_iud.py` -> 7/7 (update Name).
- **RF:** T3 `pageobjects/Configuration/Task_List/task_process_page.resource` (**label-driven, NO hardcoded ids**) + suite `tests/.../task_process_iud.robot` -> live 4/4.
- **Gate:** `verify_screen.py` -> OVERALL PASS.

## Quirks
- Plain OV; no mandatory dropdowns. Generic engine handles appear/absent/pagination.
