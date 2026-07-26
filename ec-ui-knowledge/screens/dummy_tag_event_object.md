# Screen: Dummy Tag Event Object

- **Type:** OV (EC Object Configuration, date-effective) - Bank-family (`manage_object_nav`); plain (optional dropdowns only, none mandatory)
- **BF_CODE:** CO.1063 - **Treeview:** Configuration > Integration_Services > Dummy Tag Event Object _(DB treeview JSON)_
- **DB view:** `OV_DUMMY_TAG_EVENT` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-07-26 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF 4/4 + Playwright 7/7, DB-verified, self-clean)

## Selectors `[fresh scan 2026-07-26]`
| Purpose | Selector |
|---|---|
| Open | search `Dummy Tag Event Object` -> `label.tv-link` "Dummy Tag Event Object" |
| Grid | `manage_object_nav_nav:form:T_data` (needs GO to load) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Dummy Tag Event Object Code*** - **Dummy Tag Event Object Name*** - **Start Date*** (date) - End Date - optional dropdowns. (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Dummy Tag Event Object Code` (ro) - **`Dummy Tag Event Object Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_DUMMY_TAG_EVENT`.

## Automation (code in ec-automation)
- **Playwright:** `py/dummy_tag_event_object_iud.py` -> 7/7 (update Name).
- **RF:** T3 `pageobjects/Configuration/Integration_Services/dummy_tag_event_object_page.resource` (**label-driven, NO hardcoded ids**) + suite `tests/.../dummy_tag_event_object_iud.robot` -> live 4/4.
- **Gate:** `verify_screen.py` -> OVERALL PASS.

## Quirks
- Plain OV; no mandatory dropdowns. Generic engine handles appear/absent/pagination.
