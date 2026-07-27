# Screen: Deferment Group

- **Type:** OV (EC Object Configuration, date-effective) - Bank-family (`manage_object_nav`); plain (optional dropdowns only, none mandatory)
- **BF_CODE:** CO.0149 - **Treeview:** Configuration > Assets > Facility_Objects > Deferment Group _(DB treeview JSON)_
- **DB view:** `OV_DEFERMENT_GROUP` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-07-26 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF 4/4 + Playwright 7/7, DB-verified, self-clean)

## Selectors `[fresh scan 2026-07-26]`
| Purpose | Selector |
|---|---|
| Open | search `Deferment Group` -> `label.tv-link` "Deferment Group" |
| Grid | `manage_object_nav_nav:form:T_data` (needs GO to load) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Deferment Group Code*** - **Deferment Group Name*** - **Start Date*** (date) - End Date - optional dropdowns. (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Deferment Group Code` (ro) - **`Deferment Group Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_DEFERMENT_GROUP`.

## Automation (code in ec-automation)
- **Playwright:** `py/deferment_group_iud.py` -> 7/7 (update Name).
- **RF:** T3 `pageobjects/Configuration/Assets/Facility_Objects/deferment_group_page.resource` (**label-driven, NO hardcoded ids**) + suite `tests/.../deferment_group_iud.robot` -> live 4/4.
- **Gate:** `verify_screen.py` -> OVERALL PASS.

## Quirks
- Plain OV; no mandatory dropdowns. Generic engine handles appear/absent/pagination.
