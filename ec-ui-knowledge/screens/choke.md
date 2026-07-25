# Screen: Choke

- **Type:** OV (EC Object Configuration, date-effective) — Bank-family (`manage_object_nav`); plain (optional Choke Type dropdown, not mandatory)
- **BF_CODE:** CO.0185 · **Treeview:** Configuration > Assets > Well and Reservoir Objects > Choke _(DB treeview JSON)_
- **DB view:** `OV_CHOKE` (key `CODE`; `NAME`, `COMMENTS`, `CRITICAL_OPENING`, `CHOKE_TYPE`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-07-25 · EC 14.2.4 · local sandbox — `verify_screen.py` OVERALL PASS (RF 4/4 + Playwright 7/7, DB-verified, self-clean)

## Selectors `[fresh scan 2026-07-25]`
| Purpose | Selector |
|---|---|
| Open | search `Choke` → `label.tv-link` "Choke" |
| Grid | `manage_object_nav_nav:form:T_data` (needs GO to load; has real data e.g. `P1 C001` — never touch) |
| Insert (+) | hover `span.ui-icon-insert` → "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`)
R0 **Choke Code*** · R1 **Choke Name*** · R2 **Start Date*** (date) · R3 End Date · R4 Choke Type (dropdown, optional) · R5 Critical Opening · R6 Comments. (`*` mandatory/yellow)

### Update tab (`updateAttributes`)
R0 Choke Code (ro) · **R1 Choke Name** · R2 Choke Type (dd) · R3 Critical Opening · **R4 Comments**.

### Delete (date-close) — `objectdates`
R0: Start Date C:1, **End Date `…R:0:C:3:da_input`** = Start Date → leaves `OV_CHOKE`.

## Automation (code in ec-automation)
- **Playwright:** `py/choke_iud.py` (shared engine + DbVerify) → 7/7. Update covers Name + Comments.
- **RF:** T3 `pageobjects/Configuration/Assets/Well_and_Reservoir_Objects/choke_page.resource` + suite `tests/.../choke_iud.robot` → live 4/4 (Name + Comments DB-verified via `Field Should Equal In View`).
- **Gate:** `py scripts/verify_screen.py --name Choke ...` → OVERALL PASS (see bundle `VERIFY-REPORT.md`).

## Quirks
- Optional **Choke Type** ref dropdown (R4) — skipped (not mandatory), so the plain engine builds it.
- Grid needs GO to load; has seed data (P1 C001) — AUTOTEST_ only, never touch existing.
