# Screen: Choke Model

- **Type:** OV (EC Object Configuration, date-effective) — Bank-family (`manage_object_nav`); plain (many optional dropdowns, none mandatory)
- **BF_CODE:** CO.0217 · **Treeview:** Configuration > Assets > Stream Objects > Choke Model _(DB treeview JSON)_
- **DB view:** `OV_CHOKE_MODEL` (key `CODE`; `NAME`, `SORT_ORDER`, `DESCRIPTION`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-07-26 · EC 14.2.4 · local sandbox — `verify_screen.py` OVERALL PASS (RF 4/4 + Playwright 7/7, DB-verified, self-clean)

## Selectors `[fresh scan 2026-07-26]`
| Purpose | Selector |
|---|---|
| Open | search `Choke Model` → `label.tv-link` "Choke Model" |
| Grid | `manage_object_nav_nav:form:T_data` (needs GO to load) |
| Insert (+) | hover `span.ui-icon-insert` → "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) — note Start Date at **R4**
R0 **Choke Model Code*** · R1 **Choke Model Name*** · R2 Sort Order · R3 Description · R4 **Start Date*** (date) · R5 End Date · R6+ many optional dropdowns (Parent Choke Model, Condition, Measurement Type, Loss Accounting, Op PU/Area/Facility, Geo Area/Field). (`*` mandatory)

### Update tab (`updateAttributes`)
R0 Code (ro) · **R1 Name** · R2 Sort Order · **R3 Description**.

### Delete (date-close) — `objectdates`
R0: Start Date C:1, **End Date `…R:0:C:3:da_input`** = Start Date → leaves `OV_CHOKE_MODEL`.

## Automation (code in ec-automation)
- **Playwright:** `py/choke_model_iud.py` → 7/7 (update Name + Description).
- **RF:** T3 `pageobjects/Configuration/Assets/Stream_Objects/choke_model_page.resource` + suite `tests/.../choke_model_iud.robot` → live 4/4.
- **Gate:** `verify_screen.py` → OVERALL PASS (bundle `VERIFY-REPORT.md`).

## Quirks
- Under **Stream Objects** (Choke is under Well and Reservoir Objects — siblings live in different folders; verify per screen).
- **Start Date at R4** (Sort Order R2 + Description R3 precede it) — RF T3 uses R4, not R2. Engine resolves by label anyway.
- Many optional dropdowns, all skippable (none mandatory).
