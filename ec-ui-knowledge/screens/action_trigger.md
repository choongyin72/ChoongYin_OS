# Screen: Action Trigger

- **Type:** Custom-URL OV (EC Object Configuration, date-effective) - grid loads directly; toolbar Refresh.
- **BF_CODE:** CO.0193 - **Treeview:** Configuration > Business_Action > Action Trigger
- **DB view:** `OV_CONTROL_POINT` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-08-01 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF 4/4 pass + Playwright 7/7, DB-verified, self-clean)

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Action Trigger` -> `label.tv-link` "Action Trigger" |
| Navigator | none - grid loads from the screen URL; re-query via toolbar Refresh `[Ctrl+r]` |
| Grid | `nav:form:T_data` (lists on open) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Action Trigger Code*** - **Action Trigger Name*** - **Start Date*** (date) + dropdowns Action Trigger Type, Trigger Type. (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Action Trigger Code` (ro) - **`Action Trigger Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_CONTROL_POINT`.

## Automation (code in ec-automation)
- **Playwright:** `py/action_trigger_iud.py` (shared engine `ec_object_iud.py` + toolbar Refresh).
- **RF:** T3 `pageobjects/Configuration/Business_Action/action_trigger_page.resource` (**label-driven**) + suite `tests/Configuration/Business_Action/action_trigger_iud.robot`.
- **Gate:** `verify_screen.py` -> OVERALL PASS.

## Quirks
- Custom-URL OV: no navigator GO; the toolbar Refresh `[Ctrl+r]` is the re-query gesture.
